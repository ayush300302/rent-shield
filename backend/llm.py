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

def get_heuristic_college_evaluation(college_name: str) -> dict:
    """Heuristic college classification using keyword matching."""
    c = college_name.lower().strip()

    # Tier 1: IITs, IIMs, NITs, top global universities
    t1_keywords = [
        "iit", "iim", "bits pilani", "aiims", "nit ", "national institute of technology",
        "delhi university", "jadavpur", "mit", "stanford", "oxford", "cambridge",
        "harvard", "columbia", "caltech", "iisc", "indian institute of science",
        "indian institute of technology", "indian institute of management",
    ]
    # Tier 2: Known private universities and reputed state colleges
    t2_keywords = [
        "vit", "manipal", "srm", "symbiosis", "nmims", "amity", "lpu",
        "christ university", "anna university", "mumbai university", "pune university",
        "osmania", "bangalore university", "bu bhopal", "savitribai phule",
        "calcutta university", "madras university", "shivaji university",
    ]

    if any(kw in c for kw in t1_keywords):
        college_tier = 1
    elif any(kw in c for kw in t2_keywords):
        college_tier = 2
    else:
        college_tier = 3

    return {"college_tier": college_tier}

def get_heuristic_bank_evaluation(text: str) -> dict:
    """Heuristic bank statement evaluation using regex parsing."""
    import re
    from datetime import datetime

    # --- Account Age ---
    # Look for dates in various formats (DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)
    date_patterns = [
        r'\b(\d{2})[/-](\d{2})[/-](20\d{2})\b',  # DD/MM/YYYY or DD-MM-YYYY
        r'\b(20\d{2})[/-](\d{2})[/-](\d{2})\b',   # YYYY-MM-DD
    ]
    all_years = set()
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            for part in m:
                if len(part) == 4 and part.startswith("20"):
                    all_years.add(int(part))

    if all_years:
        year_span = max(all_years) - min(all_years)
        if year_span >= 3:
            account_age_tier = 1
        elif year_span >= 1:
            account_age_tier = 2
        else:
            account_age_tier = 3
    else:
        account_age_tier = 3

    # --- Transaction Frequency ---
    # Count lines that look like transactions (have amounts with digits)
    amount_pattern = r'(?:Rs\.?|INR|₹)\s*[\d,]+\.?\d*'
    txn_matches = re.findall(amount_pattern, text, re.IGNORECASE)
    txn_count = len(txn_matches)

    # Estimate monthly: if we found a year span, use it
    months = max(len(all_years) * 12, 1) if all_years else 1
    avg_txn_per_month = txn_count / months

    if avg_txn_per_month > 20:
        txn_freq_tier = 1
    elif avg_txn_per_month >= 5:
        txn_freq_tier = 2
    else:
        txn_freq_tier = 3

    # --- Transaction Volume ---
    # Extract numeric amounts
    raw_amounts = re.findall(r'[\d,]+\.?\d*', " ".join(txn_matches))
    total_credits = 0
    for amt_str in raw_amounts:
        try:
            val = float(amt_str.replace(",", ""))
            total_credits += val
        except ValueError:
            pass

    avg_monthly_credit = total_credits / months if months > 0 else 0

    if avg_monthly_credit > 100000:
        txn_vol_tier = 1
    elif avg_monthly_credit >= 25000:
        txn_vol_tier = 2
    else:
        txn_vol_tier = 3

    return {
        "account_age_tier": account_age_tier,
        "transaction_frequency_tier": txn_freq_tier,
        "transaction_volume_tier": txn_vol_tier
    }

def get_heuristic_damage_evaluation(before_desc: str, after_desc: str) -> dict:
    """Heuristic damage evaluation using keyword matching on descriptions."""
    after = after_desc.lower()

    # Keyword severity groups
    severe_keywords = [
        "destroyed", "uninhabitable", "fire", "flood", "collapsed", "mold",
        "structural damage", "completely broken", "total renovation",
    ]
    significant_keywords = [
        "broken door", "broken window", "large hole", "heavy stain",
        "damaged plumbing", "water damage", "cracked wall", "smashed",
    ]
    moderate_keywords = [
        "stain", "small hole", "broken fixture", "scratched floor",
        "chipped", "cracked", "dent", "peeling paint", "discolored",
    ]
    minor_keywords = [
        "scuff", "minor wear", "light scratch", "slight", "faded",
        "normal wear", "dust", "small mark",
    ]
    no_damage_keywords = [
        "no damage", "same condition", "perfect", "excellent",
        "pristine", "clean", "well maintained", "like new",
    ]

    # Check from most severe to least
    if any(kw in after for kw in no_damage_keywords):
        score = 0
        category = "no_damage"
    elif any(kw in after for kw in severe_keywords):
        score = 8
        category = "severe"
    elif any(kw in after for kw in significant_keywords):
        score = 6
        category = "significant"
    elif any(kw in after for kw in moderate_keywords):
        score = 4
        category = "moderate"
    elif any(kw in after for kw in minor_keywords):
        score = 2
        category = "minimal"
    else:
        # If no keywords match, assume minor damage
        score = 3
        category = "moderate"

    return {"damage_score": score, "damage_category": category}
