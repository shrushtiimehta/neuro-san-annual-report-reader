# Multiagent Annual Report Reader

The **Multiagent Annual Report Reader** is a multi-agent system that analyzes a user's LinkedIn profile to understand their professional interests and delivers a personalized summary of Cognizant's 2024 Annual Report and 10-K SEC filing — surfacing exactly the content most relevant to their background and role.

---

## File

[multiagent_annual_report_reader.hocon](../../registries/multiagent_annual_report_reader.hocon)

---

## Description

This network follows a three-tier architecture: a top-level frontman agent orchestrates two primary agents — one that scrapes and interprets the LinkedIn profile, another that researches the annual report — and ten specialized section researchers that each cover a distinct part of the filing. Every response is grounded exclusively in retrieved document content; no external knowledge is introduced.

- **Profile-Driven Personalization**: The LinkedIn profile is scraped via the Apify `apimaestro/linkedin-profile-detail` actor. The result is classified into broad interest categories (e.g. Data & AI, Cloud & Infrastructure, Financial Services), a seniority level (Executive, Manager, or Practitioner), and a current job title summary — all of which shape what the report researcher retrieves and how it frames the findings.
- **Seniority-Aware Depth**: Executive users receive strategic highlights only; Managers get a blend of strategy and operational detail; Practitioners receive full specifics including platform names, tooling, training programmes, and case study mechanics.
- **Document Intelligence**: Ten section researchers each call `CognizantDocExtractor` to retrieve text from internal `.txt` and `.pdf` files covering every part of the 2024 Annual Report and 10-K.
- **Strict Grounding**: Agents are instructed never to omit or summarise retrieved content, and never to draw on external knowledge. If a topic has no match in the documents, it is silently ignored rather than fabricated.

---

## Prerequisites

### Apify API (LinkedIn Profile Search)

- Get API key: [Apify Integrations Console](https://console.apify.com/settings/integrations)
- Subscribe to the [`apimaestro/linkedin-profile-detail`](https://apify.com/apimaestro/linkedin-profile-detail) actor.

```bash
export APIFY_API_KEY="YOUR_API_KEY"
```

---

## Example Conversation

### Human

> **Example for Chief AI Officer of Cognizant**

```text
Analyze https://www.linkedin.com/in/b****h*****/ and summarize the annual report content most relevant to their interests.
```

### AI (Multiagent Annual Report Reader)

```text
## AI strategy framing and where Cognizant is placing bets
We believe the future of IT services will be defined by two unique opportunities: AI driving hyperproductivity and automation, and embedded engineering making our physical world intelligent, connected and autonomous.  
True to our legacy, we sensed these opportunities early and invested ahead of the curve.

We see AI-enabled opportunities in three vectors: hyperproductivity, industrializing AI and agentification.  
We see the market growing as these vectors layer, accelerating our momentum and unlocking new market opportunities.

We’re enabling hyperproductivity by automating workflows, boosting efficiency and reducing costs.  
For example, with our Flowsource code-assist platform, approximately 20% of code accepted by our developers in Q4 2024 was AIgenerated.

AI-led agentification of the enterprise, where software executes and improves services traditionally delivered by humans, has the potential to create completely new service pools.  
To advance our capabilities, we launched the Cognizant AI Research Lab in 2024 and are prioritizing partnerships with the AI-native ecosystem to help accelerate enterprise adoption.

Operationalizing at scale: With over 1,200 AI engagements at the end of 2024 (up fivefold from the prior year), we are helping enterprises unlock technical debt, modernize legacy systems, automate operations and drive hyperproductivity across their organizations.  
AI is bigger than simply the next technology wave-we believe it’s a oncein-a-generation shift that will redefine industries, reshape business models and unlock new opportunities.

In 2024, we doubled down on AI-led innovation, launching and enhancing platforms that help enterprises adopt AI responsibly and at scale.  
We introduced Flowsource for full-stack engineering, Neuro Edge for real-time AI, Neuro Cybersecurity for AI-powered defense and the Neuro Multi-Agent Accelerator for AI agent development.

We also expanded Neuro AI with multi-agent orchestration and launched Cognizant Moment, an AIpowered customer experience practice.  
Enterprises need trusted partners who can guide them through adoption, integration and scaling.

In 2025, we will stay focused on accelerating growth, investing in talent, scaling innovation and shaping the AI- and embedded engineering-driven future for enterprises worldwide.  
As we enter 2025, we do so with a clear vision, strong momentum and an unwavering commitment to our people, clients and communities around the world.

## Executive-level performance indicators tied to strategy execution
Growth is broader than financial performance-it’s helping our clients modernize, compete and seize new opportunities in a rapidly evolving landscape.  
In 2024, we made significant strides toward our goal of returning to the winner’s circle, delivering 2% revenue growth, improvements in operation margin of 80 basis points and in adjusted operating margin 1  of 20 basis points, a record $27.1 billion in trailing 12-month bookings and winning 29 large deals.

In 2024, despite a challenging macroeconomic environment, we achieved revenue growth and an enhanced operating margin even as we accelerated investments in AI-led platforms and expanded our capabilities.  
Our focus on client centricity, agility and innovation is helping clients unlock the next wave of hyperproductivity.

$19.7B revenue  
2.0% increase YoY as reported 1.9% increase YoY constant currency 2

14.7% GAAP operating margin  
15.3% adjusted operating margin 2

$1.8B free cash flow 2  
$2.1B cash flow from operations

$1.2B returned to shareholders through share repurchases and dividends  
$1.6B capital deployed on acquisitions

## Operating model and practices that support AI + transformation consulting
Cognizant is one of the world’s leading professional services companies, engineering modern businesses and delivering strategic outcomes for our clients.  
We help clients modernize technology, reimagine processes and transform experiences so they can stay ahead in today’s fast-changing world, where AI is beginning to reshape organizations in every field.

In order to achieve this vision and support our clients, we are focusing on accelerating growth, becoming an employer of choice and simplifying our operations through modernization and an AI-enabled IT roadmap.  
In executing our strategy, we seek to drive organic growth through investments in our digital and AI capabilities across industries and geographies, including the extensive training and reskilling of our technical teams and the expansion of our local workforces in the United States and other markets around the world.

Our services and solutions are organized into six integrated practices, which help us deliver these capabilities in ways that align  with  each  clients  specific  transformation  journey.  
These  practices  are  Core  Technologies  and  Insights,  Enterprise Platform Services, Industry Solutions, Intuitive Operations and Automation, Software and Platform Engineering, and Cognizant Moment,  our  new  digital  experience  practice.

Established in 2024, Cognizant Moment is our digital experience practice, designed to help clients leverage the power of AI to reimagine customer experiences and engineer innovative strategies aimed at driving growth.  
Cognizant Moment delivers intelligent ecosystem orchestration, connecting experiences as well as their underlying data, technology and operations across the entire enterprise.

Our Core Technologies and Insights practice helps clients build agile and relevant organizations that apply the power of AI, cloud, data and IoT to help them perform better and innovate faster.  
Our clients can harness data securely in cloud-first architectures, enabling them to become highly resilient enterprises that are capable of quickly adapting to market dynamics.

Our Enterprise Platform Services practice helps our clients transform multiple front- and back-office business processes, implementing enterprise-wide platforms that enable customer experience, customer relationship management, human capital management, supply chain management, enterprise resource planning and financial processes.  
Our services decrease time to market, drive efficiencies and deliver impactful experiences.

Our Intuitive Operations and Automation practice helps clients build and run modern operations through two main vehicles: AI-led automation, which includes advisory and process and IT automation solutions designed to simplify and accelerate automation adoption, and business process outsourcing services, which help deliver business outcomes including revenue growth, increased customer and employee satisfaction and cost savings.  
Our automation advisory, implementation and managed services experts partner with clients to transform end-to-end processes, design and manage the next-generation human and digital workforce, enable seamless experiences and achieve multi-fold productivity increases.

Beginning in 2025, we go to market across four industry-based operating segments, which will match our four reportable business segments - (i) Health Sciences (ii) Financial Services (iii) Products and Resources and (iv) Communications, Media and Technology.  
These changes reflect how the operating segments will be managed and reported to the CODM but will not affect the reportable segments’ financial results.

## AI ecosystem/partner strategy (platform leverage for transformation programs)
Our collaborations with Microsoft, Google, NVIDIA, AWS, Palo Alto Networks and ServiceNow continue to fuel our ability to co-create and deliver cutting-edge AI solutions.  
We earned 32 partner recognitions, including Microsoft’s Global Growth Champion Partner of the Year and Google’s Breakthrough Partner of the Year.

We work closely with partners including Adobe, Amazon Web Services, Cisco, Google, Microsoft, Oracle, Pegasystems, Salesforce, SAP, ServiceNow, Workday and many others.  
We believe this partner ecosystem will enable us to enhance our innovative, integrated offerings, by combining third-party products with our service solutions, to deliver enterprise-wide digital transformation.

## Consulting/strategy capability expansion via acquisitions (and implications)
In 2024, we acquired Belcan, a leading global supplier of engineering research & development services for the commercial aerospace, defense, space, marine and industrial verticals, and Thirdera, an Elite ServiceNow Partner specializing in advisory, implementation and optimization solutions related to the ServiceNow platform.  
Additionally, we pursue select strategic acquisitions to expand our talent, experience and capabilities in key technologies or in particular geographies or industries.

Our acquisitions of Thirdera and Belcan strengthened our position in ServiceNow consulting and engineering services, expanding our capabilities across critical industries like aerospace, defense, automotive, industrials, banking and healthcare.  
We enter 2025 with momentum and confidence.

During the third quarter of 2024, we completed the acquisition of Belcan.  
This acquisition is expected to have a modest near-term dilutive impact to our 2025 operating margin, primarily due to integration-related expenses and amortization of acquired intangibles.

## Financial levers, margin drivers, and capital allocation capacity (MD&A)
The  increase  in  our  2024  GAAP  operating  margin  and Adjusted  Operating  Margin 5 was  primarily  driven  by  net savings generated from our NextGen program and the beneficial impact of foreign currency exchange rate movements, partially offset by increased compensation costs, primarily as a result of a merit increase cycle, and the dilutive impact of recently completed acquisitions, primarily as a result of transaction and integration related expenses and amortization of acquired intangibles.  
In addition, our 2024 and 2023 GAAP operating margins were negatively impacted by the NextGen charges, as discussed in Note 4 to our consolidated financial statements, which were excluded from our Adjusted Operating Margin 5.

Our capital allocation framework anticipates the deployment of approximately 50% of our free cash flow 7 for acquisitions and 50% for share repurchases and dividend payments.  
We review our  capital  allocation  on  an  ongoing  basis,  considering  our financial performance and liquidity position, investments required to execute our strategic plans and initiatives, acquisition  opportunities,  the  economic  outlook,  regulatory changes  and  other  relevant  factors.

Cash generated from operations has historically been our primary source of liquidity to fund operations and investments to grow our business.  
As of December 31, 2024, we had cash, cash equivalents and short-term investments of $2,243 million.

Additionally, as of December 31, 2024, we had available capacity under our credit facilities of approximately $1.55 billion.  
We believe that we currently meet all conditions set forth in the Credit Agreement to borrow thereunder, and we are not aware of any conditions that would prevent us from borrowing part or all of the remaining available capacity under the revolving credit facility as of December 31, 2024 and through the date of this filing.

We expect operating cash flows, cash and short-term investment balances, together with the available capacity under our revolving credit facilities, to be sufficient to meet our operating requirements, including purchase commitments, tax payments, including the Tax Reform Act transition tax payment, and servicing our debt for the next twelve months.  
The ability to expand and grow our business in accordance with current plans, make acquisitions, meet long-term capital requirements beyond a twelve-month period and execute our capital return plan will depend on many factors, including the rate, if any, at which cash flow increases, our ability and willingness to pay for acquisitions with capital stock and the availability of public and private debt, including the ability to extend the maturity of or refinance our existing debt, and equity financing.

## Risks most material to AI-led services and transformation consulting delivery
We expect the proliferation of AI will have a significant impact on our industry, and we believe our ability to compete in this space will be critical to our financial performance.  
We increasingly use AI-based technologies, including GenAI, in our client offerings and our own internal operations.

We have incurred and plan to continue to incur significant development and operational costs to build and support our AI capabilities, including costs to ensure ongoing compliance with the complex and rapidly evolving legal landscape around AI and automation.  
If we fail to develop and implement AI solutions that meet our internal and client needs or if we are unable to bring AI-enabled solutions to market as effectively or with the same speed as our competitors, we may fail to recoup our investments in AI and our financial performance, competitive position, business and reputation may be adversely impacted.

Some services that we historically performed for our clients have been and will continue to be replaced by AI or other forms of automation, including our own AI-enabled client offerings.  
Each of the foregoing may lead to reduced demand for our services or harm our ability to obtain favorable pricing or other terms for our services, which could have a material adverse effect on our business, results of operations and financial condition.

If we do not sufficiently invest in new technologies, successfully adapt to industry developments and changing demand, develop new tools and platforms that meet our clients’ productivity expectations and evolve and expand our business at sufficient speed and scale to keep pace with the demands of the markets we serve, we may be unable to develop and maintain a competitive advantage and execute on our growth strategy, which would materially adversely affect our business, results of operations and financial  condition.  
Such reductions, replacements and delays can negatively impact our results of operations if we are unable to adapt our pricing or the pace and level of spending on new technologies is not sufficient to make up any shortfall.

Many of our contracts with clients are short-term, and our business, results of operations and financial condition could be adversely affected if our clients terminate their contracts on short notice.  
When contracts are terminated or spending delayed, we lose the anticipated revenues and might not be able to eliminate our associated costs in a timely manner.

Our failure to meet specified service levels or milestones required by certain of our client contracts may result in our client contracts being less profitable, potential liability for penalties or damages or reputational harm.  
The use of new technologies in our offerings (including GenAI) can expose us to additional risks if those technologies fail to work as predicted, which could lead to cost overruns, project delays, financial penalties, or damage to our reputation.

The less we are able to differentiate our services and solutions and/or clearly convey the value of our services and solutions, the more difficulty we have in winning new work in sufficient volumes and at our target pricing and overall economics.  
If we are not able to supply clients with services that they deem superior and successfully apply current business models with market level pricing while managing discounts, we may lose business to competitors and face downward pressure on gross margins and profitability.

If we are unable to attract, train and retain skilled employees to satisfy client demand, including highly skilled technical personnel and personnel with experience in key AI and digital areas, as well as senior management to lead our business globally, our business and results of operations may be materially adversely affected.  
For the year ended December 31, 2024 our Voluntary Attrition - Tech Services was 15.9% as compared to 13.8% for the year ended December 31, 2023.

## Cybersecurity governance disclosure (Item 1C)
*Relevant to AI executives: AI platform scaling and enterprise transformation programs increase cyber exposure and due-diligence scrutiny, making governance disclosures decision-relevant in partner selection.*

Cybersecurity risk management is an integral part of our overall enterprise risk management program.  
Our cybersecurity risk  management  program,  which  is  managed  by  Cognizant’s  Corporate  Security  team,  is  designed  to  identify,  assess  and manage  risks  from  cybersecurity  threats  and  provides  a  framework  for  handling  cybersecurity  threats  and  incidents.

In 2024, we did not identify any cybersecurity threats that have materially affected or are reasonably likely to materially affect our business strategy, results of operations, or financial condition.  
For further discussion of the cybersecurity risks and threats we face, please see Item 1A. Risk Factors.

## Regulatory/operating constraints relevant to global AI + consulting execution
Furthermore, the legal and regulatory landscape surrounding AI technologies is rapidly evolving and uncertain, with jurisdictions around the world applying, or considering applying, laws and regulations related to IP, cybersecurity, export controls, privacy, data security, and data protection to AI and automated decision-making, or general legal frameworks on AI, such as the EU AI Act, which entered into force in 2024 and parts of which apply beginning in 2025.  
As a result, we may have to expend resources to adjust our offerings in certain jurisdictions if the legal frameworks on AI are not consistent across jurisdictions, and the EU AI Act may increase costs or impact the operation of our AI services.

A substantial portion of our employees in the United States, United Kingdom, EU and other jurisdictions rely on visas to work in those areas such that any restrictions on such visas or immigration more generally or increased costs of obtaining such visas or increases in the wages we are required to pay employees on visas may affect our ability to compete for and provide services to clients in these jurisdictions, which could materially adversely affect our business, results of operations and financial condition.  
Recent changes or any additional adverse revisions to immigration laws and regulations in the jurisdictions in which we operate may cause us delays, staffing shortages, additional costs or an inability to bid for or fulfill projects for clients, any of which could have a material adverse effect on our business, results of operations and financial condition.

Anti-outsourcing legislation, if adopted, and negative perceptions associated with offshore outsourcing could impair our ability to serve our clients and materially adversely affect our business, results of operations and financial condition.  
Any slowdown or reversal of existing industry trends toward global service delivery would seriously harm our ability to compete effectively with competitors that provide the majority of their services from within the country in which our clients operate.

## GenAI execution examples (proof points)
A leading healthcare provider came to Cognizant with the goal of improving the efficiency and accuracy of the appeals and grievance process.  
We developed a gen AI-powered assistant to automate key tasks such as intent and detail recognition, dynamic knowledge mapping and decision support.

To maintain its leadership, a UK supermarket chain aimed to enhance the customer shopping experience by providing an intuitive and informative product-discovery solution.  
Now live in over 15 locations, the app is increasing sales through a product search that empowers shoppers and store associates.

A prominent life sciences organization sought to streamline customer support by automating routine queries and optimizing the ticket-escalation process.  
Utilizing AWS cloud infrastructure, the solution enables scalable deployment and cost-effective handling of increased user demand.

## Workforce scale and AI upskilling (delivery capacity signals)
*This is still relevant to an Executive view of Data & AI and Consulting & Strategy because it provides the workforce scale, skills development, and retention metrics underpinning delivery capacity and competitiveness.*

We had approximately 336,800 employees at the end of 2024, with 241,500 in India, 42,800 in North America, 15,700 in Continental Europe, 8,200 in the United Kingdom and 28,600 in various other locations throughout the rest of the world.  
In 2024, more than 277,000 employees acquired at least one skill through our learning ecosystem.

In addition to digital skills, we prioritize generative AI skill building - more than 168,000 associates, including 1,700 leaders, have taken generative AI trainings in 2024, including through Cognizant’s Synapse program.  
We regularly assess retention.
```

### Human

> **Example for CFO of Cognizant**

```text
Here is my LinkedIn profile: https://www.linkedin.com/in/j***-d****-3*******/ — what does Cognizant's annual report cover that relates to my background?
```

### AI (Multiagent Annual Report Reader)

```text
## Positioning and strategy (Consulting & Strategy)
Cognizant is one of the world’s leading professional services companies, engineering modern businesses and delivering strategic outcomes for our clients.  
We help clients modernize technology, reimagine processes and transform experiences so they can stay ahead in today’s fast-changing world, where AI is beginning to reshape organizations in every field.

We believe the future of IT services will be defined by two unique opportunities: AI driving hyperproductivity and automation, and embedded engineering making our physical world intelligent, connected and autonomous.  
Moving ahead, three priorities define our path.

In order to achieve this vision and support our clients, we are focusing on accelerating growth, becoming an employer of choice and simplifying our operations through modernization and an AI-enabled IT roadmap.  
In executing our strategy, we seek to drive organic growth through investments in our digital and AI capabilities across industries and geographies, including the extensive training and reskilling of our technical teams and the expansion of our local workforces in the United States and other markets around the world.

## Financial Services segment (business context + demand drivers)
Our FS segment includes banking, capital markets, payments and insurance companies.  
Demand in this segment is driven by our clients’ need to modernize legacy infrastructure and adopt digital technologies to serve their customers while complying with significant regulatory requirements and adapting to market changes.

These technologies enable enhanced customer experience, through automation, analytics and AI-driven value creation in areas such as digital lending, hyper-personalized banking, fraud detection, underwriting and next-generation payments.  
Clients are also increasingly leveraging technology services partners as end-to-end orchestrators uniting hyperscalers, independent software vendors, fintech players, data providers, and enterprise and business process management platforms to deliver integrated solutions at scale and speed.

## 2024 performance highlights (company-level outcomes)
In 2024, despite a challenging macroeconomic environment, we achieved revenue growth and an enhanced operating margin even as we accelerated investments in AI-led platforms and expanded our capabilities.  
Our focus on client centricity, agility and innovation is helping clients unlock the next wave of hyperproductivity.

$19.7B revenue; 2.0% increase YoY as reported; 1.9% increase YoY constant currency 2.  
14.7% GAAP operating margin; 15.3% adjusted operating margin 2.

$1.8B free cash flow 2; $2.1B cash flow from operations.  
$1.2B returned to shareholders through share repurchases and dividends; $1.6B capital deployed on acquisitions.

## Financial Services (mix and segment performance)
For the year ended December 31, 2024, the distribution of our revenues across our four reportable business segments was as follows: Financial Services 29.1%.  
In 2024, we went to market across seven industry-based operating segments, which are aggregated into four reportable business segments: Financial Services (FS) Banking; Insurance.

Revenues of $19,736 million across our business segments and geographies were as follows for the year ended December 31, 2024: FS 5753.  
Change in revenues was driven by the following factors: Reduced demand for discretionary work negatively impacted revenues across all segments; Clients in our Financial Services, Products and Resources, and Communications, Media and Technology segments were particularly affected.

Segment operating profit and operating margin percentage were as follows: Financial Services 2024 1241 21.6%; Financial Services 2023 1156 19.9%.  
In 2024, segment operating margins across all our segments were negatively impacted by increased compensation costs, partially offset by savings generated from our NextGen program and the beneficial impact of foreign currency exchange rate movements. Segment operating profit in the Financial Services segment was positively impacted by reduced resales of third-party products in connection with our integrated offerings strategy.

## 2024 commercial momentum (growth, bookings, large deals)
Our teams achieved above-peer-average revenue growth, our best year for large deal signings, and disciplined execution that expanded profit margins and enabled smart reinvestment.  
We pivoted to growth and added to our momentum throughout 2024.

In 2024, we made significant strides toward our goal of returning to the winner’s circle, delivering 2% revenue growth, improvements in operation margin of 80 basis points and in adjusted operating margin 1 of 20 basis points, a record $27.1 billion in trailing 12-month bookings and winning 29 large deals.  
These milestones reflect not only strong commercial momentum but also the deep trust our clients place in us.

## AI-led initiatives and platforms (hyperproductivity, industrializing AI, agentification)
We see AI-enabled opportunities in three vectors: hyperproductivity, industrializing AI and agentification.  
We’re enabling hyperproductivity by automating workflows, boosting efficiency and reducing costs.

For example, with our Flowsource code-assist platform, approximately 20% of code accepted by our developers in Q4 2024 was AIgenerated.  
Productivity gains like these play a meaningful role in many of our large deal wins and help fund future innovation.

Operationalizing at scale: With over 1,200 AI engagements at the end of 2024 (up fivefold from the prior year), we are helping enterprises unlock technical debt, modernize legacy systems, automate operations and drive hyperproductivity across their organizations.  
AI-led agentification of the enterprise, where software executes and improves services traditionally delivered by humans, has the potential to create completely new service pools.

## Partnerships (AI ecosystem; awards)
Our collaborations with Microsoft, Google, NVIDIA, AWS, Palo Alto Networks and ServiceNow continue to fuel our ability to co-create and deliver cutting-edge AI solutions.  
We earned 32 partner recognitions, including Microsoft’s Global Growth Champion Partner of the Year and Google’s Breakthrough Partner of the Year.

## NextGen program (profitability and reinvestment linkage)
At the end of 2024, we completed our NextGen program, which was aimed at simplifying our operating model, optimizing corporate functions and consolidating and realigning office space to reflect the post-pandemic hybrid work environment.  
The savings generated by the program are funding continued investments in our people, revenue growth opportunities and the modernization of our office space.

In 2024, we incurred $134 million of employee separation, facility exit and other costs related to the program, bringing the total costs incurred since inception to $363 million. See Note 4 to our consolidated financial statements.  
Our non-GAAP financial measures Adjusted Operating Margin and Adjusted Income from Operations exclude unusual items, such as NextGen charges.

## Capital allocation, liquidity, and 12-month outlook (financial outcomes)
Our capital allocation framework anticipates the deployment of approximately 50% of our free cash flow 7 for acquisitions and 50% for share repurchases and dividend payments.  
We review our capital allocation on an ongoing basis, considering our financial performance and liquidity position, investments required to execute our strategic plans and initiatives, acquisition opportunities, the economic outlook, regulatory changes and other relevant factors.

As of December 31, 2024, we had cash, cash equivalents and short-term investments of $2,243 million.  
Additionally, as of December 31, 2024, we had available capacity under our credit facilities of approximately $1.55 billion.

We expect operating cash flows, cash and short-term investment balances, together with the available capacity under our revolving credit facilities, to be sufficient to meet our operating requirements, including purchase commitments, tax payments, including the Tax Reform Act transition tax payment, and servicing our debt for the next twelve months.  
Our remaining Tax Reform Act transition tax payment of $157 million is due in the second quarter of 2025.

## M&A (capability expansion; margin impact)
In 2024, we acquired Belcan, a leading global supplier of engineering research & development services for the commercial aerospace, defense, space, marine and industrial verticals, and Thirdera, an Elite ServiceNow Partner specializing in advisory, implementation and optimization solutions related to the ServiceNow platform.  
Client satisfaction grew, as shown by rising Net Promoter® Scores. And our industry expertise, bolstered by strategic acquisitions like Thirdera (positioning us as a leading ServiceNow® partner) and Belcan (enhancing our engineering research and development capabilities in aerospace, defense, automotive and industrials), enables us to deliver end-to-end solutions to modernize, optimize and digitize our clients’ operations.

During the third quarter of 2024, we completed the acquisition of Belcan. See Note 3 to our consolidated financial statements.  
This acquisition is expected to have a modest near-term dilutive impact to our 2025 operating margin, primarily due to integration-related expenses and amortization of acquired intangibles.

## Executive outlook statements (demand environment, AI, regulatory/tax)
We continue to expect the focus of our clients to be on their transformation into AI-ready, technology-driven, dataenabled, customer-centric and differentiated businesses.  
To support this transformation and drive greater business resiliency, we expect clients will continue to demand services and solutions that can enhance productivity and deliver cost savings.

We increasingly use AI-based technologies, including GenAI, in our client offerings and our own internal operations.  
As AI-based technologies or other forms of automation evolve, we expect that demand for some services that we currently perform for our clients may be reduced and our ability to obtain favorable pricing or other terms for our services may be diminished.

Potential tax law and other regulatory changes, including possible U.S. corporate income tax reform and the Code on Social Security, 2020 in India, among other items, may impact our future results.  
We are currently evaluating the potential impact of the amendment, which, depending on its final terms when entered into force, could increase our effective income tax rate, as CTS India is a subsidiary of our wholly-owned Mauritius entity.

## Key risks (Financial Services; Consulting & Strategy)
Investing in our common stock involves a high degree of risk. You should carefully consider the risks described below in addition to the other information set forth in this Annual Report on Form 10-K, including Part II, Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations and our consolidated financial statements and related notes, before making an investment decision.  
The occurrence of any of the following risks or additional risks and uncertainties not presently known to us, or that we currently believe to be immaterial, could materially and adversely affect our business, financial condition, prospects, or results of operations.

### Macroeconomic and geopolitical demand risk (including Financial Services exposure)
Global macroeconomic conditions have a significant effect on our business as well as the businesses of our clients.  
For example, in 2024 some of our clients continued to reduce their discretionary spending in response to economic uncertainty, which negatively impacted our revenues.

Many of our clients are in the financial services and healthcare industries, so any decrease in growth or significant consolidation in these industries or regulatory policies that restrict these industries may reduce demand for our services.  
Our business is particularly susceptible to economic and political conditions in the markets where our clients or operations are concentrated.

### Competition and pace of technology change
The markets we serve and operate in are highly competitive, subject to rapid change and characterized by a large number of participants, as described in Part I, Item 1. Business-Competition.  
If we do not sufficiently invest in new technologies, successfully adapt to industry developments and changing demand, develop new tools and platforms that meet our clients’ productivity expectations and evolve and expand our business at sufficient speed and scale to keep pace with the demands of the markets we serve, we may be unable to develop and maintain a competitive advantage and execute on our growth strategy, which would materially adversely affect our business, results of operations and financial condition.

### AI risk (investment, demand substitution, legal and reputational)
We expect the proliferation of AI will have a significant impact on our industry, and we believe our ability to compete in this space will be critical to our financial performance.  
If we fail to develop and implement AI solutions that meet our internal and client needs or if we are unable to bring AI-enabled solutions to market as effectively or with the same speed as our competitors, we may fail to recoup our investments in AI and our financial performance, competitive position, business and reputation may be adversely impacted.

Furthermore, the legal and regulatory landscape surrounding AI technologies is rapidly evolving and uncertain, with jurisdictions around the world applying, or considering applying, laws and regulations related to IP, cybersecurity, export controls, privacy, data security, and data protection to AI and automated decision-making, or general legal frameworks on AI, such as the EU AI Act, which entered into force in 2024 and parts of which apply beginning in 2025.  
Compliance with new or changing laws, regulations, industry standards or ethical requirements and expectations relating to AI may impose significant operational costs requiring us to change our service offerings or business practices, particularly as we expand the use of such technologies, or may limit or prevent our ability to develop, deploy, or use AI technologies.

### Profitability and capital return strategy
We may not be able to achieve our profitability goals and maintain our capital return strategy.  
Failure to carry out our capital return strategy may adversely impact our reputation with shareholders and shareholders’ perception of our business and the trading price of our common stock.

### NextGen execution risk
Our NextGen program and the associated reductions in headcount and consolidation of office space could disrupt our business and may not result in anticipated savings.  
If we are unable to realize the expected operational efficiencies and cost savings from our NextGen program, our operating results and financial condition would be adversely affected.

### Cybersecurity (including 2024 status and governance)
*Relevant to Consulting & Strategy executives in Financial Services: regulated clients will scrutinize cyber posture and incident history in vendor selection and ongoing governance, particularly in AI-enabled and data-heavy transformations.*

Cybersecurity risk management is an integral part of our overall enterprise risk management program. Our cybersecurity risk management program, which is managed by Cognizant’s Corporate Security team, is designed to identify, assess and manage risks from cybersecurity threats and provides a framework for handling cybersecurity threats and incidents.  
In 2024, we did not identify any cybersecurity threats that have materially affected or are reasonably likely to materially affect our business strategy, results of operations, or financial condition. For further discussion of the cybersecurity risks and threats we face, please see Item 1A. Risk Factors.

We face legal, reputational and financial risks if we fail to protect client and/or Cognizant data from cybersecurity incidents.  
For example, we have experienced a security incident involving a ransomware attack, which resulted in unauthorized access to certain data and caused significant disruption to our business.

### Contract termination and performance-linked contract economics
Many of our contracts with clients are short-term, and our business, results of operations and financial condition could be adversely affected if our clients terminate their contracts on short notice.  
Many of our client contracts include clauses that tie our compensation to the achievement of agreed-upon performance standards, productivity improvements or milestones. Failure to satisfy any such requirements could significantly reduce our fees under the contracts, increase the cost to us of meeting performance standards or milestones, delay expected payments, subject us to potential damage claims under the contract terms or harm our reputation.

### Foreign currency exposure (profitability)
Fluctuations in foreign currency exchange rates, or the failure of our hedging strategies to mitigate such fluctuations, can adversely impact our profitability, results of operations and financial condition.  
Including the impact of the hedges, the depreciation of the Indian rupee positively impacted our operating margin for the year ended December 31, 2024 by 44 basis points as compared to the year ended December 31, 2023.
```

### Human

> **Example for Data Scientist**

```text
Here is my LinkedIn profile: https://www.linkedin.com/in/s*******-m****/ — what does Cognizant's annual report cover that relates to my background?
```

### AI (Multiagent Annual Report Reader)

```text
## AI strategy and 2025 outlook (Annual Report narrative)
We believe the future of IT services will be defined by two unique opportunities: AI driving hyperproductivity and automation, and embedded engineering making our physical world intelligent, connected and autonomous.  
We see AI-enabled opportunities in three vectors: hyperproductivity, industrializing AI and agentification.

We’re industrializing AI by modernizing our clients’ infrastructures and cloud foundations, strengthening their data approaches and reimagining user experiences to best capture the AI opportunity. Here, our AI-enabled platforms differentiate our services and provide the critical last mile infrastructure for clients to embrace AI at scale.  
AI-led agentification of the enterprise, where software executes and improves services traditionally delivered by humans, has the potential to create completely new service pools. To advance our capabilities, we launched the Cognizant AI Research Lab in 2024 and are prioritizing partnerships with the AI-native ecosystem to help accelerate enterprise adoption.

We see the market growing as these vectors layer, accelerating our momentum and unlocking new market opportunities. In 2025, we will stay focused on accelerating growth, investing in talent, scaling innovation and shaping the AI- and embedded engineering-driven future for enterprises worldwide.

## Key 2024 Data & AI initiatives and platforms (Annual Report narrative)
True to our legacy, we sensed these opportunities early and invested ahead of the curve. We launched platforms to help clients harness AI at scale, expanded our capabilities and prioritized talent development. These actions have reinvigorated Cognizant, adding both resilience and durability.  
Enterprises need trusted partners who can guide them through adoption, integration and scaling. This is where Cognizant excels. Last year, we doubled down on AI-led solutions, launching and enhancing platforms such as Neuro® AI, Cognizant Flowsource™ and Cognizant Moment™ to help redefine our clients’ efficiency, security and customer experiences. Our partnerships with hyperscalers and market leaders allow us to bring cutting-edge capabilities to our clients.

Developing differentiated platforms for AI: We introduced Flowsource for full-stack engineering, Neuro Edge for real-time AI, Neuro Cybersecurity for AI-powered defense and the Neuro Multi-Agent Accelerator for AI agent development. We also expanded Neuro AI with multi-agent orchestration and launched Cognizant Moment, an AIpowered customer experience practice.

## Data & AI metrics (Annual Report narrative)
For example, with our Flowsource code-assist platform, approximately 20% of code accepted by our developers in Q4 2024 was AIgenerated. Productivity gains like these play a meaningful role in many of our large deal wins and help fund future innovation.  
Enabling hyperproductivity: Today, 20% of our developers’ written code is AI-assisted, accelerating software development and reducing technical debt. Beyond engineering, we are leveraging AI across more than 200 internal use cases, from automating operations to improving customer interactions.  
Operationalizing at scale: With over 1,200 AI engagements at the end of 2024 (up fivefold from the prior year), we are helping enterprises unlock technical debt, modernize legacy systems, automate operations and drive hyperproductivity across their organizations.

A culture of innovation is reaching every corner of our business, driven by the success of our Bluebolt® innovation program that delivered nearly 240,000 ideas to clients in 2024doubling that of the prior year-of which 47,000 were implemented by clients.

## Skills and talent (Annual Report narrative + 10-K Business)
Cognizant invests in our 335,000 associates and our communities, empowering individuals to thrive in the AI era and deliver innovation at scale. We have trained 230,000 associates in AI, and more than 400,000 people have benefited from our Synapse skilling program. In 2024, we sustained historically high employee satisfaction scores for the second consecutive year, reinforcing our commitment to being an employer of choice.  
Building tomorrow’s workforce: We equip our teams with skills to lead clients through technology transformations, including AI. Our award-winning learning ecosystem, patent pending MySkills platform and alllevel leadership programs help associates anticipate industry shifts.

In 2024, more than 277,000 employees acquired at least one skill through our learning ecosystem.  
In addition to digital skills, we prioritize generative AI skill building - more than 168,000 associates, including 1,700 leaders, have taken generative AI trainings in 2024, including through Cognizant’s Synapse program.

We had approximately 336,800 employees at the end of 2024, with 241,500 in India, 42,800 in North America, 15,700 in Continental Europe, 8,200 in the United Kingdom and 28,600 in various other locations throughout the rest of the world. As of December 31, 2024, women represented approximately 38% of our workforce.

## Data & AI service lines and delivery mechanics (10-K Business)
Our services include AI and other technology services and solutions, consulting, application development, systems integration, quality engineering and assurance, application maintenance, infrastructure and security as well as business process services and automation. Additionally, we develop, license, implement and support proprietary and third-party software products and platforms. Central to our strategy to align with our clients need for continuous transformation is our sustained investment in new technologies, including new forms of AI, cloud, data modernization, automation, digital engineering and IoT. These capabilities enable clients to put AI at the core of their operations, improve the experiences they offer to their customers, tap into new revenue streams, automate operations, defend against digital- and AI-native competitors and reduce costs.

Our services and solutions are organized into six integrated practices, which help us deliver these capabilities in ways that align with each client’s specific transformation journey. These practices are Core Technologies and Insights, Enterprise Platform Services, Industry Solutions, Intuitive Operations and Automation, Software and Platform Engineering, and Cognizant Moment, our new digital experience practice.

Our Core Technologies and Insights practice helps clients build agile and relevant organizations that apply the power of AI, cloud, data and IoT to help them perform better and innovate faster. Our clients can harness data securely in cloud-first architectures, enabling them to become highly resilient enterprises that are capable of quickly adapting to market dynamics.  
AI and analytics, which helps clients identify and adopt the best AI use cases for their enterprise and formulate actionable insights from unstructured data to drive a greater understanding of their customers and operations.  
Cloud, infrastructure and security, which helps simplify, modernize and safeguard IT environments, creating a solid foundation for AI innovation.

We operate in an integrated global delivery model, with delivery centers worldwide to provide our full range of services to our clients. Our model leverages methodologies, tools, AI and other enablers to optimize delivery by enhancing people’s capabilities through technology. We continue to modernize our delivery operations through lean processes, increased automation and integrated, AI-infused systems.

## Partnerships relevant to AI delivery (Annual Report narrative + 10-K Business)
Our collaborations with Microsoft, Google, NVIDIA, AWS, Palo Alto Networks and ServiceNow continue to fuel our ability to co-create and deliver cutting-edge AI solutions. We earned 32 partner recognitions, including Microsoft’s Global Growth Champion Partner of the Year and Google’s Breakthrough Partner of the Year.  
We work closely with partners including Adobe, Amazon Web Services, Cisco, Google, Microsoft, Oracle, Pegasystems, Salesforce, SAP, ServiceNow, Workday and many others.

## Client case studies (Annual Report narrative)
A leading healthcare provider came to Cognizant with the goal of improving the efficiency and accuracy of the appeals and grievance process. Historically, the manual and subjective review process led to inconsistent and erroneous categorization, high administrative costs and delays in patient care.  
We developed a gen AI-powered assistant to automate key tasks such as intent and detail recognition, dynamic knowledge mapping and decision support. The AI system automatically understands the intent behind appeals, extracts relevant information from various document types, and maps identified details to relevant regulations and medical records. Based on extracted information and contextual knowledge, the assistant can predict the appropriate category and subcategory and provide a summary of the case, which helps the healthcare worker make the final decision more efficiently and accurately.  
This comprehensive approach ensures consistent application of rules and reduces errors, leading to faster resolution, increased throughput and a reduction in administrative costs.

To maintain its leadership, a UK supermarket chain aimed to enhance the customer shopping experience by providing an intuitive and informative product-discovery solution. The focus was on addressing customer frustrations related to locating and understanding products in-store, while also streamlining store operations and freeing up staff time for enhanced customer service.  
Leveraging advanced gen AI and natural language processing capabilities, Cognizant developed an app to revolutionize the product-discovery experience for our client’s customers. The app understands user intent, transforms product data into a searchable format using vector embedding, matches user queries to product data and presents results in a conversational medium. User queries are captured, translated into product matches, ranked by best results and displayed through a simple interface.  
Now live in over 15 locations, the app is increasing sales through a product search that empowers shoppers and store associates.

A prominent life sciences organization sought to streamline customer support by automating routine queries and optimizing the ticket-escalation process. The manual handling of these tasks was timeconsuming, often leading to delays and inconsistent responses. Addressing these issues would not only boost user engagement and enhance overall efficiency, it also would transform the customer support function.  
Cognizant developed a robust, scalable and flexible gen AI solution that automates routine queries and optimizes the ticket-escalation process. Our solution integrates an agentic LLM model and vector databases to provide accurate responses and resolve user queries in real time. When queries require human intervention, the system automates ticket creation through REST API integration, improving support escalation.  
Utilizing AWS cloud infrastructure, the solution enables scalable deployment and cost-effective handling of increased user demand. As a result, users are more satisfied, resolutions are more accurate and the whole process is more seamlessfrom automated response to ticket creation.

## AI risks and regulatory outlook (10-K Risk Factors)
We expect the proliferation of AI will have a significant impact on our industry, and we believe our ability to compete in this space will be critical to our financial performance.  
We increasingly use AI-based technologies, including GenAI, in our client offerings and our own internal operations.  
We have incurred and plan to continue to incur significant development and operational costs to build and support our AI capabilities, including costs to ensure ongoing compliance with the complex and rapidly evolving legal landscape around AI and automation.  
If we fail to develop and implement AI solutions that meet our internal and client needs or if we are unable to bring AI-enabled solutions to market as effectively or with the same speed as our competitors, we may fail to recoup our investments in AI and our financial performance, competitive position, business and reputation may be adversely impacted.

AI technology and services require access to high-quality datasets, foundation models, and other AI system components. We currently rely, in part, on third parties to provide these components. In the future, we may face difficulties acquiring the necessary rights from third parties due to market competition and other factors. This challenge could hinder our ability to develop, implement or maintain AI technologies. To overcome this, we may need to invest in alternative strategies, such as forming alliances or developing our own resources.

In addition, the development, adoption, and use of AI technologies are all still in their early stages and ineffective or inadequate AI development or deployment practices by us, our clients, or third parties with whom we do business could result in unintended consequences. Such consequences may include, for example, employees making decisions based on biased or inaccurate information; unauthorized disclosure of sensitive information; operational inefficiencies leading to decreased productivity; deliberate misuse; or infringement of third-party IP rights.  
Additionally, the use of AI by us or our business partners may create new cybersecurity vulnerabilities, including those which may not be recognized at the time.  
The uncertainty around the safety and security of new and emerging AI applications requires significant investment to test for security, accuracy, bias, and other variables - efforts that can be complex, costly, and potentially impact our profit margins, and may cause decreased demand for our services or harm to our business, results of operations, financial condition, or reputation.

Furthermore, the legal and regulatory landscape surrounding AI technologies is rapidly evolving and uncertain, with jurisdictions around the world applying, or considering applying, laws and regulations related to IP, cybersecurity, export controls, privacy, data security, and data protection to AI and automated decision-making, or general legal frameworks on AI, such as the EU AI Act, which entered into force in 2024 and parts of which apply beginning in 2025.  
As a result, we may have to expend resources to adjust our offerings in certain jurisdictions if the legal frameworks on AI are not consistent across jurisdictions, and the EU AI Act may increase costs or impact the operation of our AI services.  
Failure to appropriately conform to this evolving landscape may result in legal liability, regulatory action, or brand and reputational harm.

## Talent risks specific to AI and digital skills (10-K Risk Factors)
If we are unable to attract, train and retain skilled employees to satisfy client demand, including highly skilled technical personnel and personnel with experience in key AI and digital areas, as well as senior management to lead our business globally, our business and results of operations may be materially adversely affected.  
For the year ended December 31, 2024 our Voluntary Attrition - Tech Services was 15.9% as compared to 13.8% for the year ended December 31, 2023. If our attrition levels increase significantly, it could materially adversely affect our business and results of operations.  
Competition for skilled labor is intense and, in some jurisdictions in which we operate and in key AI and digital areas, there are more open positions than qualified persons to fill these positions.

## Cybersecurity governance (10-K Item 1C)
*Relevant to senior Data & AI leaders: expanding GenAI and data platforms increases exposure to cyber threats and third-party risk, and the governance model affects how AI systems are assessed, audited, and escalated when incidents occur.*

Cybersecurity risk management is an integral part of our overall enterprise risk management program. Our cybersecurity risk  management  program,  which  is  managed  by  Cognizant's  Corporate  Security  team,  is  designed  to  identify,  assess  and manage  risks  from  cybersecurity  threats  and  provides  a  framework  for  handling  cybersecurity  threats  and  incidents. The program is also aligned with the risk assessment framework established by the enterprise risk management team.  
Our  cybersecurity  risk  management  framework  includes  steps  for  assessing  the  severity  of  a  cybersecurity  threat (including an escalation process for potentially material cybersecurity threats and incidents to an internal committee comprised of members of senior management), identifying the source of a cybersecurity threat (including whether the cybersecurity threat is associated with a third-party service provider), implementing cybersecurity countermeasures and mitigation strategies. The internal  committee is responsible for assessing the materiality of cybersecurity threats and incidents and informs designated members of executive leadership and of the Board of Directors of material cybersecurity threats and incidents.

Cognizant's  cybersecurity  risk  management  program  is  guided  by  industry-recognized  security  frameworks,  including ISO/IEC 27001, TISAX and NIST. The program is periodically audited as part of external certification audits. We also engage third-party cybersecurity experts to assist with risk assessment and conduct penetration testing among other items. Key findings from the audits and third-party risk assessments are summarized and communicated to the Company's senior leadership and the Audit Committee, and remediation actions are implemented to enhance our overall cybersecurity program.

As  part  of  our  overall  enterprise  risk  management  program,  we  prioritize  the  identification  and  management  of cybersecurity risk at several levels. Our Board of Directors has overall oversight responsibility for our risk management, and delegates cybersecurity risk management oversight to the Audit Committee, which is responsible for ensuring that management has processes in place designed to identify and evaluate cybersecurity risks and implement processes and programs to manage cybersecurity risks and mitigate cybersecurity incidents.

In 2024, we did not identify any cybersecurity threats that have materially affected or are reasonably likely to materially affect our business strategy, results of operations, or financial condition. For further discussion of the cybersecurity risks and threats we face, please see Item 1A. Risk Factors.

## Business outlook statements tied to AI adoption and pricing (MD&A overview)
We continue to expect the focus of our clients to be on their transformation into AI-ready, technology-driven, dataenabled, customer-centric and differentiated businesses. To support this transformation and drive greater business resiliency, we expect clients will continue to demand services and solutions that can enhance productivity and deliver cost savings.  
We increasingly use AI-based technologies, including GenAI, in our client offerings and our own internal operations. AI technologies and services are part of a highly competitive and rapidly evolving market. We plan to make significant investments in our AI capabilities to meet the needs of our clients and harness AI’s value in a flexible, secure, scalable and responsible way. As AI-based technologies or other forms of automation evolve, we expect that demand for some services that we currently perform for our clients may be reduced and our ability to obtain favorable pricing or other terms for our services may be diminished.
```

---

## Architecture Overview

### Frontman Agent: Profile_Report_Reader

- Acts as the sole point of interaction with the user.
- Collects the LinkedIn URL, passes it to `search_profile`, and forwards the profile summary to `annual_report_researcher`.
- Formats the final response and handles follow-up questions by re-querying `annual_report_researcher` with more targeted prompts.

### Primary Agents

**search_profile**
- Calls `LinkedinProfileScraper` with the LinkedIn URL.
- Returns two structured lines: broad interest categories and seniority level.

**annual_report_researcher**
- Calls all section researchers simultaneously, passing the user's interest category and seniority level to each.
- Filters responses by category first, then seniority, and merges into one complete answer.
- Delegates to: `BusinessOverview_Researcher`, `AnnualReport_Researcher`, `AuditorReport_Researcher`, `Controls_Researcher`, `MDA_Researcher`, `NotesFinancials_Researcher`, `RiskFactorsOne_Researcher`, `RiskFactorsTwo_Researcher`, `Schedules_Researcher`, `StockholderMDA_Researcher`

### Section Researchers and Their Sub-Agents

| Section Researcher | Sub-Agents |
|---|---|
| **BusinessOverview_Researcher** | `BusinessOverview_Segments`, `Competition_IP_People`, `Glossary_ForwardLooking`, `SEC_FilingHeader`, `Services_Solutions_Delivery` |
| **AnnualReport_Researcher** | `AI_Era_Industry_Expertise`, `Cover_ShareholderLetter`, `Financial_Performance_Summary`, `Partnerships_CaseStudies` |
| **AuditorReport_Researcher** | `Auditor_Report_Opinions`, `Consolidated_FinancialStmts`, `Notes_AcctgPoliciesRevenue` |
| **Controls_Researcher** | `FinancialStmts_IntroControls`, `OtherInfo_PartIII`, `PartIV_ExhibitsSignatures` |
| **MDA_Researcher** | `Critical_EstimatesMarketRisk`, `Liquidity_CapitalResources`, `Operating_MarginIncome` |
| **NotesFinancials_Researcher** | `Benefits_StockCompSegments`, `BusinessCombos_InvestmentsPPE`, `FairValue_OCICommitments`, `IncomeTaxes_Derivatives`, `Leases_GoodwillAccruedDebt` |
| **RiskFactorsOne_Researcher** | `AI_ContractRisks`, `Cyber_CurrencyPandemicRisks`, `Profitability_GrowthNextgen`, `RiskFactors_IntroMacro` |
| **RiskFactorsTwo_Researcher** | `Climate_ESGBusinessContinuity`, `Cybersecurity_Properties`, `Legal_RegulatoryLegislative`, `Tax_LitigationIP` |
| **Schedules_Researcher** | `Directors_BoardCommittees`, `Executive_CommitteeCorpInfo`, `Valuation_AccountsCertifications` |
| **StockholderMDA_Researcher** | `Equity_DividendsPerformance`, `MDA_ExecSummaryRevenues`, `Results_OperationsDetail` |

---

## Functional Tools

**LinkedinProfileScraper** (`ApifyLinkedinProfileScraper`)
- Uses the Apify `apimaestro/linkedin-profile-detail` actor via the `APIFY_API_KEY` environment variable.
- Returns name, about section, current job, work experience, education, and most recent original post.

**CognizantDocExtractor** (`ExtractDocs`)
- Retrieves text from `.txt` and `.pdf` files under `coded_tools/annual_report/knowdocs/`.
- Accepts either a section-level `app_name` (returns all files in that directory) or a file-level `app_name` (returns a single document).

---

## Debugging Hints

- Check whether `search_profile` returned both lines (interest categories, seniority).
- Check whether `annual_report_researcher` called the right section researchers for the user's category.
- Check whether `CognizantDocExtractor` returned content (look for `ERROR: No PDF or text files found` in logs).
- If LinkedIn returns empty fields, the scraper logs a rate-limiting warning — wait a few minutes and retry.

---
