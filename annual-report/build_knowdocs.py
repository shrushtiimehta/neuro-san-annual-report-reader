import io
import os
import base64
import re
import json
import asyncio
import anthropic
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.datamodel.base_models import InputFormat

# ── Configuration ─────────────────────────────────────────────────────────────
PDF_FILE = "marketing-stunt/PRO013686_8_Cognizant_ARS_2024_PR_LR.pdf"
OUTPUT_DIR = "docs"
DO_OCR = False
MAX_AGENTS = 10  # Claude will plan at most this many top-level sections

CHART_PROMPT = (
    "This image is from a financial annual report. Analyze it carefully.\n\n"
    "If it contains a bar chart, line graph, stacked chart, or any data visualization:\n"
    "- State the chart title\n"
    "- List every year/period shown on the x-axis\n"
    "- For EACH bar or data point, give the exact or approximate numeric value and its label\n"
    "- Note whether values are in millions, billions, percentages, etc.\n"
    "- Call out the year-over-year trend (growing, declining, stable)\n"
    "- Highlight the most recent year's value vs prior years\n"
    "- Note any notable spikes, dips, or inflection points\n"
    "- Avoid all decorative elements or anything that would be irrelevant to the the financial report.\n\n"
    "If it is a KPI tile or summary stat (e.g. a large number with a label), "
    "extract every number and label shown.\n\n"
    "If it is a logo, decorative element, or photograph with no data, say so in one sentence."
)

PLANNING_PROMPT = """\
You are organizing a large PDF document so that each chunk can be read by an LLM \
without context overload, while losing zero information.

Document stats:
- Total words : {total_words:,}
- Total images: {total_images}
- Total headings: {total_headings}
- Target sections: AT MOST {max_agents} (each section = one parallel agent)
- Ideal words per subsection file: ~{ideal_words} words

Heading outline  (index · level · heading text · [words in block, images in block]):
{outline}

Use the word counts and image counts as your primary signal for balancing. \
Group thematically related, consecutive headings so that:
  1. No single subsection file exceeds ~{max_words} words (context overload risk).
  2. No subsection file is shorter than ~{min_words} words (too fragmented).
  3. Sections are roughly balanced in total word count.
  4. Images stay with the text that references them (do not split mid-section).

Rules:
- AT MOST {max_agents} top-level sections (fewer is fine if natural).
- Aim for 2–6 subsections per section.
- Every index 0 through {last_index} must appear exactly once across all subsections.
- section_name and sub_name must be snake_case, filesystem-safe, ≤60 chars.

Return ONLY a JSON array — no explanation, no markdown fences:
[
  {{
    "section_name": "snake_case",
    "subsections": [
      {{"sub_name": "snake_case", "heading_indices": [0, 1, 2]}}
    ]
  }}
]"""
# ──────────────────────────────────────────────────────────────────────────────


# ── Step 1: extract heading positions ─────────────────────────────────────────

def extract_headings(markdown: str) -> list[tuple[int, int, str]]:
    """
    Return all headings as (char_position, level, text), sorted by position.
    Levels 1–3 are captured (H1/H2/H3).
    """
    results = []
    for m in re.finditer(r"^(#{1,3}) (.+)$", markdown, re.MULTILINE):
        results.append((m.start(), len(m.group(1)), m.group(2).strip()))
    return results


# ── Step 2: ask Claude to plan the grouping ────────────────────────────────────

def plan_sections(
    client: anthropic.Anthropic,
    markdown: str,
    headings: list[tuple[int, int, str]],
    max_agents: int,
) -> list[dict]:
    """
    Send the heading outline — enriched with per-block word and image counts —
    to Claude and get back a structured grouping plan.
    Claude guarantees ≤ max_agents sections and full coverage of all indices.
    """
    # Per-heading block: text from this heading's start to the next heading's start
    outline_lines = []
    total_words = len(markdown.split())
    total_images = len(re.findall(r"<!-- image-\d+ -->", markdown))

    for i, (start, level, text) in enumerate(headings):
        end = headings[i + 1][0] if i + 1 < len(headings) else len(markdown)
        block = markdown[start:end]
        word_count = len(block.split())
        image_count = len(re.findall(r"<!-- image-\d+ -->", block))

        indent = "  " * (level - 1)
        stats = f"[{word_count:,} words"
        if image_count:
            stats += f", {image_count} image{'s' if image_count > 1 else ''}"
        stats += "]"
        outline_lines.append(f"{i} · {'#' * level} · {indent}{text}  {stats}")

    outline = "\n".join(outline_lines)

    # Sizing guidance: target ~2,000 words per subsection, hard cap at 4,000, min 300
    ideal_words = max(500, total_words // (max_agents * 3))
    max_words = ideal_words * 2
    min_words = max(200, ideal_words // 4)

    prompt = PLANNING_PROMPT.format(
        total_words=total_words,
        total_images=total_images,
        total_headings=len(headings),
        max_agents=max_agents,
        ideal_words=f"{ideal_words:,}",
        max_words=f"{max_words:,}",
        min_words=f"{min_words:,}",
        outline=outline,
        last_index=len(headings) - 1,
    )

    print("Planning document structure with Claude…")
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if Claude wraps the JSON anyway
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    plan = json.loads(raw.strip())
    print(f"Claude's plan: {len(plan)} section(s)")
    for sec in plan:
        sub_names = [s["sub_name"] for s in sec["subsections"]]
        print(f"  {sec['section_name']}/  → {sub_names}")
    return plan


# ── Step 3: slice markdown according to the plan ──────────────────────────────

def apply_plan(
    markdown: str,
    headings: list[tuple[int, int, str]],
    plan: list[dict],
    preamble: str,
) -> list[tuple[str, list[tuple[str, str]]]]:
    """
    Apply Claude's plan to cut the markdown into (section, [(sub, content)]) pairs.

    - preamble (text before the first heading) is prepended to the first
      subsection of the first section so nothing is dropped.
    - Each subsection's content spans from its first heading to the start of
      the next heading not in the same subsection (or end of document).
    """
    # Build pos_map: heading_index → (start_char, end_char)
    pos_map: dict[int, tuple[int, int]] = {}
    for i, (start, _, _) in enumerate(headings):
        end = headings[i + 1][0] if i + 1 < len(headings) else len(markdown)
        pos_map[i] = (start, end)

    sections: list[tuple[str, list[tuple[str, str]]]] = []
    first_subsection_done = False

    for sec in plan:
        sec_name = sec["section_name"]
        subsections: list[tuple[str, str]] = []

        for sub in sec["subsections"]:
            sub_name = sub["sub_name"]
            indices: list[int] = sub["heading_indices"]

            if not indices:
                content = ""
            else:
                start = pos_map[indices[0]][0]
                end = pos_map[indices[-1]][1]
                content = markdown[start:end].strip()

            # Prepend preamble to the very first subsection
            if not first_subsection_done and preamble:
                content = preamble + ("\n\n" if content else "") + content
                first_subsection_done = True

            if content:
                subsections.append((sub_name, content))

        if subsections:
            sections.append((sec_name, subsections))

    return sections


# ── Image description (async-wrapped) ─────────────────────────────────────────

async def describe_image(client: anthropic.Anthropic, image_bytes: bytes) -> str:
    loop = asyncio.get_event_loop()
    b64 = base64.standard_b64encode(image_bytes).decode()
    response = await loop.run_in_executor(
        None,
        lambda: client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/png", "data": b64},
                        },
                        {"type": "text", "text": CHART_PROMPT},
                    ],
                }
            ],
        ),
    )
    return response.content[0].text.strip()


# ── Sub-agent: one subsection ──────────────────────────────────────────────────

async def subsection_agent(
    client: anthropic.Anthropic,
    section_name: str,
    sub_name: str,
    content: str,
    image_bytes_map: dict[int, bytes],
) -> tuple[str, str, str]:
    """
    Owns one subsection file.  Describes all its images concurrently via Claude,
    then returns (section_name, sub_name, processed_markdown).
    Output: docs/<section_name>/<sub_name>.txt
    """
    placeholder_re = re.compile(r"<!-- image-(\d+) -->")
    indices = [int(m.group(1)) for m in placeholder_re.finditer(content)]

    descriptions: dict[int, str] = {}
    if indices:
        print(f"    [{section_name}/{sub_name}] {len(indices)} image(s) → Claude…")
        tasks = {
            idx: asyncio.create_task(describe_image(client, image_bytes_map[idx]))
            for idx in indices
            if idx in image_bytes_map
        }
        for idx, task in tasks.items():
            try:
                descriptions[idx] = await task
            except Exception as exc:
                descriptions[idx] = f"[image analysis failed: {exc}]"

    def replace(m: re.Match) -> str:
        idx = int(m.group(1))
        if idx not in image_bytes_map:
            return "<!-- image: could not extract -->"
        return f"[IMAGE DESCRIPTION: {descriptions.get(idx, 'no description')}]"

    return section_name, sub_name, placeholder_re.sub(replace, content)


# ── Section agent: one H1-level group ─────────────────────────────────────────

async def section_agent(
    client: anthropic.Anthropic,
    section_name: str,
    subsections: list[tuple[str, str]],
    image_bytes_map: dict[int, bytes],
    output_dir: str,
) -> int:
    """
    One of the ≤ MAX_AGENTS top-level agents.
    Spawns sub-agents for each subsection concurrently.
    Writes: docs/<section_name>/<sub_name>.txt
    Returns the number of files written.
    """
    section_dir = os.path.join(output_dir, section_name)
    os.makedirs(section_dir, exist_ok=True)

    print(f"  [Agent: {section_name}]  {len(subsections)} subsection(s)…")

    results = await asyncio.gather(*[
        subsection_agent(client, section_name, sub_name, content, image_bytes_map)
        for sub_name, content in subsections
    ])

    for sec, sub, processed in results:
        filepath = os.path.join(output_dir, sec, f"{sub}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(processed)
        print(f"    Written: {filepath}")

    return len(results)


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = anthropic.Anthropic()

    # 1. Convert PDF → markdown via Docling
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = DO_OCR
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    pipeline_options.generate_picture_images = True
    pipeline_options.do_chart_extraction = True

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    print(f"Converting {PDF_FILE} …")
    result = converter.convert(PDF_FILE)
    doc = result.document
    markdown = doc.export_to_markdown()

    # 2. Number <!-- image --> placeholders and extract image bytes
    pictures = list(doc.pictures)
    image_bytes_map: dict[int, bytes] = {}
    counter = 0

    def number_and_extract(m: re.Match) -> str:
        nonlocal counter
        idx = counter
        counter += 1
        if idx < len(pictures):
            pil_img = pictures[idx].get_image(doc)
            if pil_img is not None:
                buf = io.BytesIO()
                pil_img.save(buf, format="PNG")
                image_bytes_map[idx] = buf.getvalue()
        return f"<!-- image-{idx} -->"

    markdown = re.sub(r"<!-- image -->", number_and_extract, markdown)
    print(f"Found {counter} placeholder(s), {len(image_bytes_map)} extractable image(s).")

    # 3. Extract heading positions from markdown
    headings = extract_headings(markdown)
    preamble = markdown[: headings[0][0]].strip() if headings else markdown.strip()
    print(f"Found {len(headings)} heading(s) across the document.")

    # 4. Ask Claude to plan the optimal grouping (≤ MAX_AGENTS sections)
    plan = plan_sections(client, markdown, headings, MAX_AGENTS)

    # 5. Slice markdown according to Claude's plan
    hierarchy = apply_plan(markdown, headings, plan, preamble)
    total_subs = sum(len(subs) for _, subs in hierarchy)
    print(f"\nFinal structure: {len(hierarchy)} section(s), {total_subs} subsection(s)")

    # 6. Launch one agent per section — all concurrent (≤ MAX_AGENTS guaranteed by plan)
    print(f"\nLaunching {len(hierarchy)} section agent(s) in parallel…\n")
    file_counts = await asyncio.gather(*[
        section_agent(client, sec_name, subs, image_bytes_map, OUTPUT_DIR)
        for sec_name, subs in hierarchy
    ])

    total = sum(file_counts)
    print(f"\nDone!  {total} file(s) written to '{OUTPUT_DIR}/'")
    print("Layout: docs/<section>/<subsection>.txt")


if __name__ == "__main__":
    asyncio.run(main())
