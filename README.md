# Neuro SAN Annual Report Reader

Neuro SAN applied to Cognizant's 2024 Annual Report.

Analyzes a LinkedIn profile URL and delivers a personalized summary of Cognizant's 2024 Annual Report —
surfacing only the content most relevant to the user's industry and seniority level.
The LinkedIn profile is scraped via the Apify `apimaestro/linkedin-profile-detail` actor, classified into
a broad interest category and seniority level (Executive, Manager, or Practitioner), and used to filter
the full report in a single agent call.

For more details about Neuro SAN, please check the
[Neuro SAN](https://github.com/cognizant-ai-lab/neuro-san) library and
[Neuro SAN Studio](https://github.com/cognizant-ai-lab/neuro-san-studio) repository.

## Getting started

### Installation

Clone the repo:

```bash
git clone https://github.com/shrushtiimehta/neuro-san-annual-report-reader
```

Go to dir:

```bash
cd neuro-san-annual-report-reader
```

Ensure you have a supported version of python (e.g. 3.12 or 3.13):

```bash
python --version
```

Create a dedicated Python virtual environment:

```bash
python -m venv venv
```

Source it:

* For Windows:

  ```cmd
  .\venv\Scripts\activate.bat && set PYTHONPATH=%CD%
  ```

* For Mac:

  ```bash
  source venv/bin/activate && export PYTHONPATH=`pwd`
  ```

Install the requirements:

```bash
pip install -r requirements.txt
```

**IMPORTANT**: By default the server relies on OpenAI's `gpt-5.2` model. Set the OpenAI API key, and add it to your shell
configuration so it's available in future sessions.

You can get your OpenAI API key from <https://platform.openai.com/signup>. After signing up, create a new API key in the
API keys section in your profile.

**NOTE**: Replace `XXX` with your actual OpenAI API key.
**NOTE**: This is OS dependent.

* For macOS and Linux:

  ```bash
  export OPENAI_API_KEY="XXX" && echo 'export OPENAI_API_KEY="XXX"' >> ~/.zshrc
  ```

<!-- pyml disable commands-show-output -->
* For Windows:
    * On Command Prompt:

    ```cmd
    set OPENAI_API_KEY=XXX
    ```

    * On PowerShell:

    ```powershell
    $env:OPENAI_API_KEY="XXX"
    ```

<!-- pyml enable commands-show-output -->

**IMPORTANT**: This project also requires an Apify API key to scrape LinkedIn profiles. Get yours from the
[Apify Integrations Console](https://console.apify.com/settings/integrations) and subscribe to the
[`apimaestro/linkedin-profile-detail`](https://apify.com/apimaestro/linkedin-profile-detail) actor.

* For macOS and Linux:

  ```bash
  export APIFY_API_KEY="XXX" && echo 'export APIFY_API_KEY="XXX"' >> ~/.zshrc
  ```

<!-- pyml disable commands-show-output -->
* For Windows:
    * On Command Prompt:

    ```cmd
    set APIFY_API_KEY=XXX
    ```

    * On PowerShell:

    ```powershell
    $env:APIFY_API_KEY="XXX"
    ```

<!-- pyml enable commands-show-output -->

Other providers such as Anthropic, AzureOpenAI, Ollama and more are supported too but will require proper setup.
Look at the `.env.example` file to set up environment variables for specific use-cases.

For testing the API keys, please refer to this [documentation](./docs/api_key.md)

---

### Run

Start the server and client with a single command, from the project root directory:

1. Start the server and client with a single command, from the project root directory:

    ```bash
    python -m run
    ```

2. Navigate to [http://localhost:4173/](http://localhost:4173/) to access the UI.
3. (Optional) Check the logs:
   * For the server logs: `logs/server.log`
   * For the client logs: `logs/nsflow.log`
   * For the agents logs: `logs/thinking_dir/*`

Use the `--help` option to see the various config options for the `run` command:

```bash
python -m run --help
```

### Using the agent networks

Select the `annual_report_reader` network and share a LinkedIn profile URL, for instance:

```Analyze <linkedin-url> and summarize the annual report content most relevant to their interests or simply```
```paste the URL and let the agent do the rest.```

The agent will scrape the profile, classify the person's interest category and seniority level, and return a
personalized summary of Cognizant's 2024 Annual Report filtered to what is most relevant to their role.

You can follow up with questions:
```What does the report say about AI agent development platforms?```
