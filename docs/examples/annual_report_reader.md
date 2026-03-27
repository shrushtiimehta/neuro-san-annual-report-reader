# Annual Report Reader

The **Annual Report Reader** analyzes a user's LinkedIn profile and delivers a personalized summary of Cognizant's 2024 Annual Report — using a single agent to read the full report rather than a multi-agent hierarchy. It is the simpler counterpart to the [Multiagent Annual Report Reader](multiagent_annual_report_reader.md).

---

## File

[annual_report_reader.hocon](../../registries/annual_report_reader.hocon)

---

## Description

This network uses a two-tier architecture: a frontman agent orchestrates two agents — one that scrapes and interprets the LinkedIn profile, and one document reader that loads the full annual report in a single call and filters it to what is most relevant for the user. Every response is grounded exclusively in the retrieved document content; no external knowledge is introduced.

- **Profile-Driven Personalization**: The LinkedIn profile is scraped via the Apify `apimaestro/linkedin-profile-detail` actor. The result is classified into broad interest categories, a seniority level (Executive, Manager, or Practitioner), and a current job title summary — all of which shape how the document reader filters and frames the content.
- **Single-Agent Document Access**: Unlike the multiagent version, the `document_reader` agent calls `CognizantDocExtractor` once with `app_name: "annual_report_2024"` to load the full combined report, then filters the result itself. This is faster and simpler but processes the entire document in one pass rather than in parallel specialized chunks.
- **Strict Grounding**: Agents are instructed never to omit or summarise retrieved content, and never to draw on external knowledge. If a topic has no match in the document, it is silently ignored rather than fabricated.

---

## Difference vs. Multiagent Annual Report Reader

| | Annual Report Reader | Multiagent Annual Report Reader |
|---|---|---|
| **Document access** | One agent, one call, full report | 10 section researchers, each reading their own chunk in parallel |
| **Speed** | Faster (single call) | Slower but more thorough |
| **Filtering** | Done by `document_reader` after loading | Done per-section before merging |
| **Best for** | Quick lookups, lighter queries | Deep, comprehensive coverage across all sections |

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
https://www.linkedin.com/in/b****h*****/
```

### AI (Annual Report Reader)

```text
## Consulting & Strategy (Executive)

We believe Cognizant is well positioned to help enterprises navigate complexity, spot opportunities and turn technology into real-world business value.

Cognizant is one of the world’s leading professional services companies, engineering modern businesses and delivering strategic outcomes for our clients. We help clients modernize technology, reimagine processes and transform experiences so they can stay ahead in today’s fast-changing world, where AI is beginning to reshape organizations in every field. We provide industry expertise and close client collaboration, combining critical perspective with a flexible engagement style. We tailor our services and solutions to specific industries with an integrated global delivery model that employs client service and delivery teams based at client locations and dedicated global and regional delivery centers.

Our collaborative services include digital services and solutions, consulting, application development, systems integration, quality engineering and assurance, engineering research and development, application maintenance, infrastructure and security as well as business process services and automation.

Our consulting professionals have deep industry-specific expertise and work closely across our practices to create intuitive operating models that leverage a wide range of technologies across our clients’ enterprises to deliver higher levels of efficiency, new value for their customers and business outcomes that align to their industries.

In order to achieve this vision and support our clients, we are focusing on accelerating growth, becoming an employer of choice and simplifying our operations through modernization and an AI-enabled IT roadmap. In executing our strategy, we seek to drive organic growth through investments in our digital and AI capabilities across industries and geographies, including the extensive training and reskilling of our technical teams and the expansion of our local workforces in the United States and other markets around the world. Additionally, we pursue select strategic acquisitions to expand our talent, experience and capabilities in key technologies or in particular geographies or industries.

Clients see us as more than a technology provider-they trust us as a strategic partner who listens, anticipates and co-creates.

We are focused on expanding our partner ecosystem across a broad range of technology companies, including hyperscalers, cloud providers, enterprise software companies, best-in-class digital software enterprises and emerging start-ups. We believe this partner ecosystem will enable us to enhance our innovative, integrated offerings, by combining third-party products with our service solutions, to deliver enterprise-wide digital transformation.

## Data & AI (Executive)

We believe the future of IT services will be defined by two unique opportunities: AI driving hyperproductivity and automation, and embedded engineering making our physical world intelligent, connected and autonomous.

We see AI-enabled opportunities in three vectors: hyperproductivity, industrializing AI and agentification.

We’re enabling hyperproductivity by automating workflows, boosting efficiency and reducing costs. For example, with our Flowsource code-assist platform, approximately 20% of code accepted by our developers in Q4 2024 was AIgenerated. Productivity gains like these play a meaningful role in many of our large deal wins and help fund future innovation.

We’re industrializing AI by modernizing our clients’ infrastructures and cloud foundations, strengthening their data approaches and reimagining user experiences to best capture the AI opportunity. Here, our AI-enabled platforms differentiate our services and provide the critical ‘last mile infrastructure’ for clients to embrace AI at scale.

AI-led agentification of the enterprise, where software executes and improves services traditionally delivered by humans, has the potential to create completely new service pools. To advance our capabilities, we launched the Cognizant AI Research Lab in 2024 and are prioritizing partnerships with the AI-native ecosystem to help accelerate enterprise adoption.

In 2024, we doubled down on AI-led innovation, launching and enhancing platforms that help enterprises adopt AI responsibly and at scale.

### Developing differentiated platforms for AI
We introduced Flowsource for full-stack engineering, Neuro Edge for real-time AI, Neuro Cybersecurity for AI-powered defense and the Neuro Multi-Agent Accelerator for AI agent development. We also expanded Neuro AI with multi-agent orchestration and launched Cognizant Moment, an AIpowered customer experience practice.

### Operationalizing at scale
With over 1,200 AI engagements at the end of 2024 (up fivefold from the prior year), we are helping enterprises unlock technical debt, modernize legacy systems, automate operations and drive hyperproductivity across their organizations.

### Strengthening strategic partnerships
Our collaborations with Microsoft, Google, NVIDIA, AWS, Palo Alto Networks and ServiceNow continue to fuel our ability to co-create and deliver cutting-edge AI solutions. We earned 32 partner recognitions, including Microsoft’s Global Growth Champion Partner of the Year and Google’s Breakthrough Partner of the Year.

We increasingly use AI-based technologies, including GenAI, in our client offerings and our own internal operations. We plan to make significant investments in our AI capabilities to meet the needs of our clients and harness AI’s value in a flexible, secure, scalable and responsible way.

## AI-enabled performance and capital allocation context (Executive)

In 2024, we made significant strides toward our goal of returning to the winner’s circle, delivering 2% revenue growth, improvements in operation margin of 80 basis points and in adjusted operating margin 1 of 20 basis points, a record $27.1 billion in trailing 12-month bookings and winning 29 large deals.

In 2024, despite a challenging macroeconomic environment, we achieved revenue growth and an enhanced operating margin even as we accelerated investments in AI-led platforms and expanded our capabilities.

In 2024 Financial results: $19.7B revenue, 2.0% increase YoY as reported, 1.9% increase YoY constant currency; 14.7% GAAP operating margin; 15.3% adjusted operating margin.

In 2024 Capital allocation: $1.2B returned to shareholders through share repurchases and dividends; $1.6B capital deployed on acquisitions.

In 2024 Cash generation: $1.8B free cash flow; $2.1B cash flow from operations.

Our capital allocation framework anticipates the deployment of approximately 50% of our free cash flow 7 for acquisitions and 50% for share repurchases and dividend payments. We review our capital allocation on an ongoing basis, considering our financial performance and liquidity position, investments required to execute our strategic plans and initiatives, acquisition opportunities, the economic outlook, regulatory changes and other relevant factors.

## Strategic acquisitions tied to Consulting & Data & AI positioning (Executive)

In 2024, we acquired Belcan, a leading global supplier of engineering research & development services for the commercial aerospace, defense, space, marine and industrial verticals, and Thirdera, an Elite ServiceNow Partner specializing in advisory, implementation and optimization solutions related to the ServiceNow platform.

On January 22, 2024, through the execution of a share purchase agreement, we acquired 100% ownership in Thirdera, an Elite ServiceNow Partner specializing in advisory, implementation and optimization solutions related to the ServiceNow platform.

On August 26, 2024, through the execution of a merger agreement, we acquired 100% ownership in Belcan, a leading global supplier of engineering research & development services for the commercial aerospace, defense, space, marine and industrial verticals. We paid $1,195 million in cash, net of cash acquired, and issued 1,470,589 shares of our Class A common stock, valued at $113 million, in connection with our acquisition of Belcan.

For the year ended December 31, 2024, revenues from acquisitions completed in 2024, since the dates of acquisition, were $384 million.

## Selected Data & AI case studies (Executive)

### Case study · Healthcare — Advancing healthcare by streamlining grievance management
A leading healthcare provider came to Cognizant with the goal of improving the efficiency and accuracy of the appeals and grievance process. Historically, the manual and subjective review process led to inconsistent and erroneous categorization, high administrative costs and delays in patient care.

We developed a gen AI-powered assistant to automate key tasks such as intent and detail recognition, dynamic knowledge mapping and decision support. The AI system automatically understands the intent behind appeals, extracts relevant information from various document types, and maps identified details to relevant regulations and medical records. Based on extracted information and contextual knowledge, the assistant can predict the appropriate category and subcategory and provide a summary of the case, which helps the healthcare worker make the final decision more efficiently and accurately.

This comprehensive approach ensures consistent application of rules and reduces errors, leading to faster resolution, increased throughput and a reduction in administrative costs.

### Case study · Retail — Driving sales by revolutionizing in-store shopping experiences
To maintain its leadership, a UK supermarket chain aimed to enhance the customer shopping experience by providing an intuitive and informative product-discovery solution. The focus was on addressing customer frustrations related to locating and understanding products in-store, while also streamlining store operations and freeing up staff time for enhanced customer service.

Leveraging advanced gen AI and natural language processing capabilities, Cognizant developed an app to revolutionize the product-discovery experience for our client’s customers. The app understands user intent, transforms product data into a searchable format using vector embedding, matches user queries to product data and presents results in a conversational medium. User queries are captured, translated into product matches, ranked by best results and displayed through a simple interface.

Now live in over 15 locations, the app is increasing sales through a product search that empowers shoppers and store associates.

### Case study · Life sciences — Transforming customer support with intelligent query resolution and ticketing
A prominent life sciences organization sought to streamline customer support by automating routine queries and optimizing the ticket-escalation process. The manual handling of these tasks was timeconsuming, often leading to delays and inconsistent responses. Addressing these issues would not only boost user engagement and enhance overall efficiency, it also would transform the customer support function.

Cognizant developed a robust, scalable and flexible gen AI solution that automates routine queries and optimizes the ticket-escalation process. Our solution integrates an agentic LLM model and vector databases to provide accurate responses and resolve user queries in real time. When queries require human intervention, the system automates ticket creation through REST API integration, improving support escalation.

Utilizing AWS cloud infrastructure, the solution enables scalable deployment and cost-effective handling of increased user demand. As a result, users are more satisfied, resolutions are more accurate and the whole process is more seamlessfrom automated response to ticket creation.
```

### Human

> **Example for CFO of Cognizant**

```text
https://www.linkedin.com/in/j***-d****-3*******/
```

### AI (Annual Report Reader)

```text
## To our shareholders

As I begin my third year as Cognizant's CEO, I am energized by our purpose and the momentum we're building to shape the future. We're a company that finds opportunity in change-distinguished by our ability to sense, incubate and scale new technologies-making each technology wave a bigger opportunity than the last. We excel by combining deep client connections with domain and industry expertise in a culture of co-creation and trust.

We believe the future of IT services will be defined by two unique opportunities: AI driving hyperproductivity and automation, and embedded engineering making our physical world intelligent, connected and autonomous.

## Our progress in 2024

True to our legacy, we sensed these opportunities early and invested ahead of the curve. We launched platforms to help clients harness AI at scale, expanded our capabilities and prioritized talent development. These actions have reinvigorated Cognizant, adding both resilience and durability.

Our teams achieved above-peer-average revenue growth, our best year for large deal signings, and disciplined execution that expanded profit margins and enabled smart reinvestment.

Growth isn't just about numbers-it's about people, innovation and leading through transformation. We believe Cognizant is well positioned to help enterprises navigate complexity, spot opportunities and turn technology into real-world business value.

Moving ahead, three priorities define our path.

## Accelerating growth

We pivoted to growth and added to our momentum throughout 2024. Our fourth quarter marked a high point in revenue growth during the year, large deal signings at or above $100 million total contract value, and trailing 12-month bookings, demonstrating our ability to drive real business transformation.

Client satisfaction grew, as shown by rising Net Promoter® Scores. And our industry expertise, bolstered by strategic acquisitions like Thirdera (positioning us as a leading ServiceNow® partner) and Belcan (enhancing our engineering research and development capabilities in aerospace, defense, automotive and industrials), enables us to deliver end-to-end solutions to modernize, optimize and digitize our clients' operations.

## Scaling innovation

Enterprises need trusted partners who can guide them through adoption, integration and scaling. This is where Cognizant excels. Last year, we doubled down on AI-led solutions, launching and enhancing platforms such as Neuro® AI, Cognizant Flowsource™ and Cognizant Moment™ to help redefine our clients' efficiency, security and customer experiences. Our partnerships with hyperscalers and market leaders allow us to bring cutting-edge capabilities to our clients.

## Leading in the AI era and looking ahead with confidence

We see AI-enabled opportunities in three vectors: hyperproductivity, industrializing AI and agentification.

We're enabling hyperproductivity by automating workflows, boosting efficiency and reducing costs. For example, with our Flowsource code-assist platform, approximately 20% of code accepted by our developers in Q4 2024 was AIgenerated. Productivity gains like these play a meaningful role in many of our large deal wins and help fund future innovation.

We're industrializing AI by modernizing our clients' infrastructures and cloud foundations, strengthening their data approaches and reimagining user experiences to best capture the AI opportunity. Here, our AI-enabled platforms differentiate our services and provide the critical 'last mile infrastructure' for clients to embrace AI at scale.

AI-led agentification of the enterprise, where software executes and improves services traditionally delivered by humans, has the potential to create completely new service pools. To advance our capabilities, we launched the Cognizant AI Research Lab in 2024 and are prioritizing partnerships with the AI-native ecosystem to help accelerate enterprise adoption.

We see the market growing as these vectors layer, accelerating our momentum and unlocking new market opportunities. In 2025, we will stay focused on accelerating growth, investing in talent, scaling innovation and shaping the AI- and embedded engineering-driven future for enterprises worldwide.

## Accelerating growth in the era of AI transformation

Growth is broader than financial performance-it's helping our clients modernize, compete and seize new opportunities in a rapidly evolving landscape. In 2024, we made significant strides toward our goal of returning to the winner's circle, delivering 2% revenue growth, improvements in operation margin of 80 basis points and in adjusted operating margin 1  of 20 basis points, a record $27.1 billion in trailing 12-month bookings and winning 29 large deals. These milestones reflect not only strong commercial momentum but also the deep trust our clients place in us.

Our approach to growth is built on three key strengths:

## Industry and engineering expertise:

Our acquisitions of Thirdera and Belcan strengthened our position in ServiceNow consulting and engineering services, expanding our capabilities across critical industries like aerospace, defense, automotive, industrials, banking and healthcare.

AI-led transformation: As businesses race to integrate AI, Cognizant is leading the charge. From AI-driven software modernization to intelligent automation, we are helping enterprises accelerate their AI adoption with precision, speed and scale.

Deep client relationships: Clients see us as more than a technology provider-they trust us as a strategic partner who listens, anticipates and co-creates. Our ability to blend industry expertise with advanced

We enter 2025 with momentum and confidence. Our strategy is clear: accelerate growth, amplify talent, and scale innovation to drive transformation and create lasting value.

- Cognizant is meeting the opportunity of this most recent wave in the IT services industry, not by changing who we are, but by focusing on what's always made us great.

Jatin Dalal Chief Financial Officer

## Scaling innovation to help our clients in a fast-changing world

Innovation at Cognizant isn't just about adopting new technologies-it's about making the technology practical, scalable and transformative for our clients. In 2024, we doubled down on AI-led innovation, launching and enhancing platforms that help enterprises adopt AI responsibly and at scale.

Our approach is built on the following strategies:

## Developing differentiated platforms for AI:

We introduced Flowsource for full-stack engineering, Neuro Edge for real-time AI, Neuro Cybersecurity for AI-powered defense and the Neuro Multi-Agent Accelerator for AI agent development. We also expanded Neuro AI with multi-agent orchestration and launched Cognizant Moment, an AIpowered customer experience practice.

Operationalizing at scale: With over 1,200 AI engagements at the end of 2024 (up fivefold from the prior year), we are helping enterprises unlock technical debt, modernize legacy systems, automate operations and drive hyperproductivity across their organizations.

## Strengthening strategic partnerships:

Our collaborations with Microsoft, Google, NVIDIA, AWS, Palo Alto Networks and ServiceNow continue to fuel our ability to co-create and deliver cutting-edge AI solutions. We earned 32 partner recognitions, including Microsoft's Global Growth Champion Partner of the Year and Google's Breakthrough Partner of the Year.

## Financial performance

In 2024, despite a challenging macroeconomic environment, we achieved revenue growth and an enhanced operating margin even as we accelerated investments in AI-led platforms and expanded our capabilities. Our focus on client centricity, agility and innovation is helping clients unlock the next wave of hyperproductivity.

## Financial results

$19.7B

revenue

2.0% increase YoY as reported 1.9% increase YoY constant currency 2

14.7%

15.3%

GAAP operating margin

adjusted operating margin 2

## Capital allocation

$1.2B

returned to shareholders through share repurchases and dividends

$1.6B

capital deployed on acquisitions

## Cash generation

$1.8B

free cash

flow 2

$2.1B

cash flow from

operations

## Item 1. Business — Overview (consulting + strategic outcomes framing)

Cognizant is one of the world's leading professional services companies, engineering modern businesses and delivering strategic outcomes for our clients. We help clients modernize technology, reimagine processes and transform experiences so they can stay ahead in today's fast-changing world, where AI is beginning to reshape organizations in every field. We provide industry expertise and close client collaboration, combining critical perspective with a flexible engagement style. We tailor our services and solutions to specific industries with an integrated global delivery model that employs client service and delivery teams based at client locations and dedicated global and regional delivery centers. Our collaborative services include digital services and solutions, consulting, application development, systems integration, quality engineering and assurance, engineering research and development, application maintenance, infrastructure and security as well as business process services and automation. Digital, AI-enhanced services continue to be an important part of our portfolio, aligning with our clients' focus on becoming data-enabled, customer-centric and differentiated businesses.

In order to achieve this vision and support our clients, we are focusing on accelerating growth, becoming an employer of choice and simplifying our operations through modernization and an AI-enabled IT roadmap. In executing our strategy, we seek to drive organic growth through investments in our digital and AI capabilities across industries and geographies, including the extensive training and reskilling of our technical teams and the expansion of our local workforces in the United States and other markets around the world. Additionally, we pursue select strategic acquisitions to expand our talent, experience and capabilities in  key  technologies  or  in  particular  geographies  or  industries.  In  2024,  we  acquired  Belcan,  a  leading  global  supplier  of engineering research & development services for the commercial aerospace, defense, space, marine and industrial verticals, and Thirdera,  an  Elite  ServiceNow  Partner  specializing  in  advisory,  implementation  and  optimization  solutions  related  to  the ServiceNow platform. See Note 3 to our consolidated financial statements for additional information.

We  are  focused  on  expanding  our  partner  ecosystem  across  a  broad  range  of  technology  companies,  including hyperscalers, cloud providers, enterprise software companies, best-in-class digital software enterprises and emerging start-ups. We believe this  partner  ecosystem  will  enable  us  to  enhance  our  innovative,  integrated  offerings,  by  combining  third-party products with our service solutions, to deliver enterprise-wide digital transformation.

## Services and Solutions (consulting positioning across practices)

Our  services  include  AI  and  other  technology  services  and  solutions,  consulting,  application  development,  systems integration, quality engineering and assurance, application maintenance, infrastructure and security as well as business process services  and  automation.  Additionally,  we  develop,  license,  implement  and  support  proprietary  and  third-party  software products and platforms. Central to our strategy to align with our clients' need for continuous transformation is our sustained investment in new technologies, including new forms of AI, cloud, data modernization, automation, digital engineering and IoT.  These  capabilities  enable  clients  to  put  AI  at  the  core  of  their  operations,  improve  the  experiences  they  offer  to  their customers, tap into new revenue streams, automate operations, defend against digital- and AI-native competitors and reduce costs.

Our services and solutions are organized into six integrated practices, which help us deliver these capabilities in ways that align  with  each  client's  specific  transformation  journey.  These  practices  are  Core  Technologies  and  Insights,  Enterprise Platform Services, Industry Solutions, Intuitive Operations and Automation, Software and Platform Engineering, and Cognizant Moment,  our  new  digital  experience  practice.  Our  consulting  professionals  have  deep  industry-specific  expertise  and  work closely across our practices to create intuitive operating models that leverage a wide range of technologies across our clients' enterprises  to  deliver  higher  levels  of  efficiency,  new  value  for  their  customers  and  business  outcomes  that  align  to  their industries.

## Digital Experience Services (Cognizant Moment)

Established in 2024, Cognizant Moment is our digital experience practice, designed to help clients leverage the power of AI to reimagine customer experiences and engineer innovative strategies aimed at driving growth. Cognizant Moment delivers intelligent ecosystem orchestration, connecting experiences as well as their underlying data, technology and operations across the entire enterprise. This approach enables clients to leverage generative AI's content generation capabilities alongside human ingenuity  to  innovate  and  differentiate  by  informing  and  automating  processes,  and  creating  dynamic,  hyper-personalized experiences for their customers.

## 2024 Financial Results (10-K MD&A excerpts with business significance context)

In 2024, we made significant strides toward our goal of returning to the winner's circle, delivering 2% revenue growth, improvements in operation margin of 80 basis points and in adjusted operating margin 1  of 20 basis points, a record $27.1 billion in trailing 12-month bookings and winning 29 large deals.

Revenue up $383 million or 2.0% from 2023; an increase of 1.9% in constant currency 1

Income from Operations up $203 million or 7.5% from 2023

Adjusted Income from Operations 1 up $108 million or 3.7% from 2023

Operating margin up 80 basis points from 2023

Adjusted Operating Margin 1 up 20 basis points from 2023

Diluted EPS up $0.30 or 7.1% from 2023

Adjusted Diluted EPS 1 up $0.20 or 4.4% from 2023

During  the  year  ended  December  31,  2024,  revenues  increased  by  $383  million  as  compared  to  the  year  ended December  31,  2023,  representing  an  increase  of  2.0%,  or  1.9%  on  a  constant  currency  basis 1 .  Our  recently  completed acquisitions contributed 200 basis points to revenue growth. Additionally, revenues were positively impacted by growth in our Health Sciences segment, partially offset by weakness primarily in our Products and Resources (excluding the impact of our recently completed acquisitions) and Financial Services segments.

Change in revenues was driven by the following factors:

- North America revenues, particularly in the Health Sciences segment, were positively impacted by the ramp up of several recently won large deals;
- Recently completed acquisitions contributed 200 basis points of growth to the overall change in revenues, including approximately 600 basis points of growth to our Products and Resources segment (primarily in North America) and approximately 150 basis points of growth to our Communications, Media and Technology segment (primarily in North America);
- The resale of third-party products, primarily in North America, in connection with our integrated offerings strategy, contributed 70 basis points of growth to the overall change in revenue;
- Reduced demand for discretionary work negatively impacted revenues across all segments. Clients in our Financial Services, Products and Resources, and Communications, Media and Technology segments were particularly affected;
- Revenue decline in our United Kingdom region was primarily driven by weakness in the Communications, Media and Technology and Financial Services segments; and
- Revenue decline in our Rest of World region was primarily driven by weakness in the Products and Resources and Financial Services segments.

## Capital Allocation Framework

Our capital allocation framework anticipates the deployment of approximately 50% of our free cash flow 7 for acquisitions and 50% for share repurchases and dividend payments. We review our  capital  allocation  on  an  ongoing  basis,  considering  our financial performance and liquidity position, investments required to execute our strategic plans and initiatives, acquisition  opportunities,  the  economic  outlook,  regulatory changes  and  other  relevant  factors.  As  these  factors  may change  over  time,  the  actual  amounts  expended  on  stock repurchase activity, dividends, and acquisitions, if any, during any  particular  period  cannot  be  predicted  and  may  fluctuate from time to time.

2023: Acquisitions 409; Share Repurchases 1064; Dividend Payments 591; Total 2064

2024: Acquisitions 1615; Share Repurchases 605; Dividend Payments 600; Total 2820

## Strategic acquisitions (with full 10-K acquisition context)

On January 22, 2024, through the execution of a share purchase agreement, we acquired 100% ownership in Thirdera, an Elite  ServiceNow  Partner  specializing  in  advisory,  implementation  and  optimization  solutions  related  to  the ServiceNow platform.

On August 26, 2024, through the execution of a merger agreement, we acquired 100% ownership in Belcan, a leading global  supplier  of  engineering  research  &  development  services  for  the  commercial  aerospace,  defense,  space,  marine  and industrial verticals. We paid $1,195 million in cash, net of cash acquired, and issued 1,470,589 shares of our Class A common stock, valued at $113 million, in connection with our acquisition of Belcan.

Goodwill from our acquisition of Thirdera is expected to benefit all of our reportable segments and has been allocated as such. Goodwill from our acquisition of Belcan has been allocated to our Product and Resources segment. For the year ended December 31, 2024,  revenues  from  acquisitions  completed  in  2024,  since  the  dates  of  acquisition,  were  $384  million.

## Business Outlook (AI + demand environment)

We continue  to  expect  the  focus  of  our  clients  to  be  on  their  transformation  into  AI-ready,  technology-driven,  dataenabled, customer-centric and differentiated businesses. To support this transformation and drive greater business resiliency, we expect clients will continue to demand services and solutions that can enhance productivity and deliver cost savings.

We increasingly use AI-based technologies, including GenAI, in our client offerings and our own internal operations. AI technologies  and  services  are  part  of  a  highly  competitive  and  rapidly  evolving  market.  We  plan  to  make  significant investments in our AI capabilities to meet the needs of our clients and harness AI's value in a flexible, secure, scalable and responsible way. As AI-based technologies or other forms of automation evolve, we expect that demand for some services that we currently perform for our clients may be reduced and our ability to obtain favorable pricing or other terms for our services may be diminished.

During  the  third  quarter  of  2024,  we  completed  the  acquisition  of  Belcan.  See  Note  3  to  our  consolidated  financial statements. This acquisition is expected to have a modest near-term dilutive impact to our 2025 operating margin, primarily due to integration-related expenses and amortization of acquired intangibles.
```

### Human

> **Example for Data Scientist**

```text
https://www.linkedin.com/in/s*******-m****/
```

### AI (Annual Report Reader)

```text
## Services and Solutions

Our  services  include  AI  and  other  technology  services  and  solutions,  consulting,  application  development,  systems integration, quality engineering and assurance, application maintenance, infrastructure and security as well as business process services  and  automation.  Additionally,  we  develop,  license,  implement  and  support  proprietary  and  third-party  software products and platforms. Central to our strategy to align with our clients’ need for continuous transformation is our sustained investment in new technologies, including new forms of AI, cloud, data modernization, automation, digital engineering and IoT.  These  capabilities  enable  clients  to  put  AI  at  the  core  of  their  operations,  improve  the  experiences  they  offer  to  their customers, tap into new revenue streams, automate operations, defend against digital- and AI-native competitors and reduce costs.

In  most  cases,  our  clients  operate  in  hybrid  technology  environments,  running  critical  new  digital  initiatives  alongside essential legacy systems. In the AI era, our clients have an accelerated need to modernize their businesses, which has intensified demand  for  next-gen  capabilities  in  AI,  automation,  digital  commerce  and  secure  distributed  work.  We  believe  our  deep understanding of our clients’ established systems and their digital ambitions provides us with a unique advantage as we work with them to architect solutions that are both transformative and practical.

Our services and solutions are organized into six integrated practices, which help us deliver these capabilities in ways that align  with  each  client’s  specific  transformation  journey.  These  practices  are  Core  Technologies  and  Insights,  Enterprise Platform Services, Industry Solutions, Intuitive Operations and Automation, Software and Platform Engineering, and Cognizant Moment,  our  new  digital  experience  practice.  Our  consulting  professionals  have  deep  industry-specific  expertise  and  work closely across our practices to create intuitive operating models that leverage a wide range of technologies across our clients’ enterprises  to  deliver  higher  levels  of  efficiency,  new  value  for  their  customers  and  business  outcomes  that  align  to  their industries.

## Core Technologies and Insights

Our Core Technologies and Insights practice helps clients build agile and relevant organizations that apply the power of AI, cloud, data and IoT to help them perform better and innovate faster. Our clients can harness data securely in cloud-first architectures, enabling them to become highly resilient enterprises that are capable of quickly adapting to market dynamics. Areas of focus within this practice are:

- AI and analytics, which helps clients identify and adopt the best AI use cases for their enterprise and formulate actionable insights from unstructured data to drive a greater understanding of their customers and operations;
- Cloud, infrastructure and security, which helps simplify, modernize and safeguard IT environments, creating a solid foundation for AI innovation; and
- IoT, which enables the convergence of the physical and the digital in smart products.

## Enterprise Platform Services

Our Enterprise Platform Services practice helps our clients transform multiple front- and back-office business processes, implementing enterprise-wide platforms that enable customer experience, customer relationship management, human capital management, supply chain management, enterprise resource planning and financial processes. Our services decrease time to market, drive efficiencies and deliver impactful experiences. Our clients can better share information, simplify IT processes, automate workflow and improve flexibility. This practice focuses on application services, which help enterprises engage their partner  ecosystems  more  productively,  and  run  their  operations  and  financial  organizations  more  efficiently  while  enabling improved employee and customer experiences. We work closely with partners including Adobe, Amazon Web Services, Cisco, Google, Microsoft, Oracle, Pegasystems, Salesforce, SAP, ServiceNow, Workday and many others.

## Industry Solutions

Our Industry  Solutions  practice  was  established  in  2023  as  part  of  Cognizant’s  strategy  to  build  differentiation  at  the industry level. The practice integrates industry technologists and thought leaders specialized in vertical micro-segments. These teams  work  with  specialized  partners  to  develop  industry-specific  products  and  services  that  enable  clients  to  improve productivity, increase operational excellence and accelerate innovation.

## Intuitive Operations and Automation

Our Intuitive Operations and Automation practice helps clients build and run modern operations through two main vehicles: AI-led automation, which includes advisory and process and IT automation solutions designed to simplify and accelerate automation adoption, and business process outsourcing services, which help deliver business outcomes including revenue growth, increased customer and employee satisfaction and cost savings. Our automation advisory, implementation and managed services experts partner with clients to transform end-to-end processes, design and manage the next-generation human and digital workforce, enable seamless experiences and achieve multi-fold productivity increases. Our technology-driven business process outsourcing services help clients transform and run functions and industry-specific processes such as finance and accounting, omni-channel customer care, loan origination, annotation services, location-based services and medical data management.

## Software and Platform Engineering

Our  Software  and  Platform  Engineering  practice  helps  clients  develop  modern  enterprises  through  digital  software engineering products, services and solutions that support optimization and modernization of their IT estates and deliver new value for their customers. This practice manages delivery platforms that enable enterprise transformation at scale and accelerate the wide use of generative AI in the enterprise. Our clients can leverage data, technologies and our digital engineering, design and  product  development  capabilities  to  build  world-class  experiences,  and  a  responsive,  agile  and  intuitive  framework  for continuous innovation. Areas of focus are:

- Digital engineering, which delivers modern business software;
- Application development and management, which improves or reimagines applications; and
- Quality engineering and assurance, which helps clients build and run the highest quality software.

## Digital Experience Services (Cognizant Moment)

Established in 2024, Cognizant Moment is our digital experience practice, designed to help clients leverage the power of AI to reimagine customer experiences and engineer innovative strategies aimed at driving growth. Cognizant Moment delivers intelligent ecosystem orchestration, connecting experiences as well as their underlying data, technology and operations across the entire enterprise. This approach enables clients to leverage generative AI’s content generation capabilities alongside human ingenuity  to  innovate  and  differentiate  by  informing  and  automating  processes,  and  creating  dynamic,  hyper-personalized experiences for their customers.

## Global Delivery Model

We operate in an integrated global delivery model, with delivery centers worldwide to provide our full range of services to  our  clients.  Our  model  leverages  methodologies,  tools,  AI  and  other  enablers  to  optimize  delivery  by  enhancing  people’s capabilities  through  technology.  We  continue  to  modernize  our  delivery  operations  through  lean  processes,  increased automation and integrated, AI-infused systems. Our employees are deployed at client sites, local or in-country delivery centers, regional delivery centers and offshore delivery centers, as required to best serve our clients. Our extensive facilities, technology and communications infrastructure are designed to enable the effective collaboration of our global workforce across locations and geographies.
```
---

## Architecture Overview

### Frontman Agent: Profile_File_Reader

- Acts as the sole point of interaction with the user.
- Collects the LinkedIn URL, passes it to `search_profile`, and forwards the profile summary to `document_reader`.
- Formats the final response and handles follow-up questions.

### Primary Agents

**search_profile**
- Calls `LinkedinProfileScraper` with the LinkedIn URL.
- Returns two structured lines: broad interest categories and seniority level.

**document_reader**
- Calls `CognizantDocExtractor` once with `app_name: "annual_report_2024"` to load the full combined report.
- Filters the content based on interest category (primary signal) and seniority level (secondary signal).
- Returns the filtered content in full without dropping, shortening, or summarising any retrieved detail.

---

## Functional Tools

**LinkedinProfileScraper** (`LinkedinProfileScraper`)
- Uses the Apify `apimaestro/linkedin-profile-detail` actor via the `APIFY_API_KEY` environment variable.
- Returns name, about section, current job, work experience, education, and most recent original post.

**CognizantDocExtractor** (`ExtractDocs`)
- Reads `coded_tools/annual_report/complete_annual_report_2024.txt` — the full combined annual report and 10-K in a single file.
- Called once with `app_name: "annual_report_2024"`.

---

## Debugging Hints

- Check whether `search_profile` returned both lines (interest categories, seniority).
- Check whether `document_reader` called `CognizantDocExtractor` with `app_name: "annual_report_2024"`.
- Check whether `CognizantDocExtractor` found the file at `coded_tools/annual_report/complete_annual_report_2024.txt`.
- If the response seems truncated, the file may exceed the context limit — consider using the multiagent version instead.

---
