import os
import json
import logging
from backend.utils import get_env_var, parse_json_from_llm

logger = logging.getLogger(__name__)

# Initialize client if API key is available
GEMINI_API_KEY = get_env_var("GEMINI_API_KEY") or get_env_var("GOOGLE_API_KEY")

has_gemini_client = False
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        has_gemini_client = True
        logger.info("Gemini API configured successfully.")
    except ImportError:
        logger.warning("google-generativeai package not installed, falling back to heuristic evaluation.")
else:
    logger.warning("No GEMINI_API_KEY or GOOGLE_API_KEY found, using heuristic evaluation.")

def run_llm_classification(prompt: str, fallback_evaluation_fn) -> dict:
    """
    Run LLM property classification. If Gemini API key is missing or calls fail,
    falls back to a rule-based evaluation function.
    """
    if has_gemini_client:
        try:
            import google.generativeai as genai
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return parse_json_from_llm(response.text)
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}. Falling back to heuristics.")
            return fallback_evaluation_fn()
    else:
        return fallback_evaluation_fn()

def get_heuristic_property_classification(location: str, rent: int, deposit: int) -> dict:
    """Heuristic property classification following the rules defined in the prompt."""
    loc_lower = location.lower().strip()
    
    # 1. Location Classification Heuristic
    # Popular/Metro tier 1
    t1_cities = ["mumbai", "bengaluru", "bangalore", "pune", "hyderabad", "delhi", "ncr", "chennai", "kolkata"]
    # Mid-sized tier 2
    t2_cities = ["meerut", "ghaziabad", "jaipur", "ahmedabad", "lucknow", "nagpur", "indore", "surat", "patna", "bhopal", "vadodara", "coimbatore"]
    
    if any(city in loc_lower for city in t1_cities):
        location_tier = 1
    elif any(city in loc_lower for city in t2_cities):
        location_tier = 2
    else:
        location_tier = 3
        
    # 2. Rent Classification Heuristic
    if rent < 15000:
        rent_tier = 3
    elif 15000 <= rent <= 50000:
        rent_tier = 2
    else:
        rent_tier = 1
        
    # 3. Deposit Classification Heuristic
    if deposit == 1:
        deposit_tier = 1
    elif 2 <= deposit <= 3:
        deposit_tier = 2
    else:
        deposit_tier = 3
        
    return {
        "location": location_tier,
        "rent": rent_tier,
        "deposit_neededd": deposit_tier
    }

def get_heuristic_offer_letter_evaluation(text: str) -> dict:
    """Heuristic offer letter parser using regex and keyword matching."""
    import re
    t = text.lower().strip()
    
    # 1. Company Tier classification heuristic
    t1_keywords = ["google", "meta", "apple", "amazon", "netflix", "microsoft", "uber", "goldman", "tcs", "infosys", "wipro"]
    t2_keywords = ["midstart", "average", "techcorp", "150 employees", "mid-sized", "medium"]
    
    if any(kw in t for kw in t1_keywords):
        company_tier = 1
    elif any(kw in t for kw in t2_keywords):
        company_tier = 2
    else:
        company_tier = 3
        
    # 2. Salary Tier classification heuristic
    salary_tier = 3  # Default to tier 3 (<4 LPA)
    
    # Check for LPA patterns: e.g. "15 LPA", "15 Lakhs Per Annum"
    lpa_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lpa|lakh|lakhs)', t)
    if lpa_match:
        val = float(lpa_match.group(1))
        if val > 10.0:
            salary_tier = 1
        elif val >= 4.0:
            salary_tier = 2
        else:
            salary_tier = 3
    else:
        # Check for monthly salary patterns: e.g. "INR 1,25,000", "Rs. 50,000"
        monthly_match = re.search(r'(?:inr|rs\.?)\s*(\d+(?:,\d+)*)', t)
        if monthly_match:
            try:
                monthly_val = int(monthly_match.group(1).replace(',', ''))
                annual = monthly_val * 12
                if annual > 1000000:
                    salary_tier = 1
                elif annual >= 400000:
                    salary_tier = 2
                else:
                    salary_tier = 3
            except ValueError:
                pass
                
    return {
        "company_tier": company_tier,
        "salary_tier": salary_tier
    }

