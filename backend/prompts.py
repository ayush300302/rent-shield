# LLM Prompts for RentShield evaluation models

PROPERTY_CLASSIFICATION_PROMPT = """You are a property risk evaluator AI for the RentShield platform.
Your task is to classify a rental property's Location, Rent, and Deposit Needed based on the following classification rules.

Input:
- Location: {location}
- Rent: {rent} INR
- Deposit Needed: {deposit} months

Classification Rules:

1. Location Tier (1, 2, or 3):
- Tier 1: Major metropolitan cities, tech hubs, or high-cost-of-living urban centers (e.g., Mumbai, Bengaluru, Pune, Hyderabad, Delhi NCR, Chennai, Kolkata).
- Tier 2: Mid-sized cities, state capitals with moderate cost of living, or major suburban districts (e.g., Meerut, Ghaziabad, Jaipur, Ahmedabad, Lucknow, Nagpur, Indore).
- Tier 3: Small towns, rural areas, or villages (e.g., Ralegan Siddhi, Mawlynnong, Hampi, villages, or any lesser-known small municipalities).

2. Rent Tier (1, 2, or 3):
- Tier 3: Monthly rent is strictly less than 15,000 INR (Rent < 15,000).
- Tier 2: Monthly rent is between 15,000 INR and 50,000 INR inclusive (15,000 <= Rent <= 50,000).
- Tier 1: Monthly rent is strictly greater than 50,000 INR (Rent > 50,000).

3. Deposit Needed Tier (1, 2, or 3):
- Tier 1: Security deposit is exactly 1 month of rent (Deposit = 1).
- Tier 2: Security deposit is 2 to 3 months of rent inclusive (2 <= Deposit <= 3).
- Tier 3: Security deposit is strictly greater than 3 months of rent (Deposit > 3).

Your response MUST be a valid JSON object only, with no other text, wrapping, markdown blocks (like ```json), or whitespace outside the JSON.
The JSON object keys MUST match exactly:
{{
  "location": {location_default},
  "rent": {rent_default},
  "deposit_neededd": {deposit_default}
}}
Note the spelling of "deposit_neededd" with a double 'd'.
"""

OFFER_LETTER_EVALUATION_PROMPT = """You are an AI assistant designed to evaluate job offer letters for RentShield.
Your task is to analyze the text extracted from an offer letter and classify both the company tier and the salary tier based on the following rules.

Input Offer Letter Text:
{text}

Classification Rules:

1. Company Tier (1, 2, or 3):
- Tier 1: Top-tier companies (e.g., MAANG: Meta, Apple, Amazon, Netflix, Google; top global tech/finance firms, major multinationals like Microsoft, Uber, Goldman Sachs, TCS, Infosys, Wipro, or companies with very large revenues and thousands of employees).
- Tier 2: Average-sized companies (e.g., mid-sized startups or established firms with around 100-500 employees, stable revenues, or known brands that are not massive conglomerates).
- Tier 3: Unknown, small startups, local businesses, or tiny companies with low headcount and tiny revenues.

2. Salary Tier (1, 2, or 3):
- Tier 3: Monthly or annual salary corresponds to less than 4 Lakhs Per Annum (Salary < 4 LPA, or roughly < 33,000 INR per month).
- Tier 2: Monthly or annual salary corresponds to between 4 LPA and 10 LPA inclusive (4 LPA <= Salary <= 10 LPA, or roughly 33,000 to 83,000 INR per month).
- Tier 1: Monthly or annual salary corresponds to greater than 10 Lakhs Per Annum (Salary > 10 LPA, or roughly > 83,000 INR per month).

Your response MUST be a valid JSON object only, with no other text, wrapping, markdown blocks (like ```json), or whitespace outside the JSON.
The JSON object keys MUST match exactly:
{{
  "company_tier": {company_default},
  "salary_tier": {salary_default}
}}
"""

COLLEGE_EVALUATION_PROMPT = """You are an AI assistant evaluating academic credentials for RentShield, a rental fintech platform in India.
Your task is to classify a college or university into one of three tiers based on its academic reputation and prestige.

Input College Name:
{college_name}

Classification Rules:

1. College Tier (1, 2, or 3):
- Tier 1: Top 200 globally ranked institutions OR top-ranked Indian institutions including:
  IITs (IIT Bombay, IIT Delhi, IIT Madras, IIT Kanpur, IIT Kharagpur, etc.),
  IIMs (IIM Ahmedabad, IIM Bangalore, IIM Calcutta, etc.),
  NITs, BITS Pilani, AIIMS, Delhi University (top colleges), Jadavpur University,
  Top international universities (MIT, Stanford, Oxford, Cambridge, Harvard, etc.).
- Tier 2: Mid-ranked colleges including:
  Private universities with national recognition, state universities with good standing,
  Reputed private engineering/management colleges (e.g., VIT, Manipal, SRM, Symbiosis, NMIMS),
  Colleges affiliated with recognized state boards.
- Tier 3: Not well-known colleges, unrecognized institutions, local/rural colleges,
  or any institution that does not clearly fall into Tier 1 or Tier 2.

Your response MUST be a valid JSON object only, with no other text, wrapping, markdown blocks (like ```json), or whitespace outside the JSON.
The JSON object key MUST match exactly:
{{
  "college_tier": {college_default}
}}
"""

