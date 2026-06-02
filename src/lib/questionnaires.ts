export type Option = { value: string; label: string };
export type Question = {
  id: string;
  title: string;
  subtitle?: string;
  options: Option[];
};

const opts = (...labels: string[]): Option[] =>
  labels.map((l) => ({ value: l, label: l }));

export const renterQuestions: Question[] = [
  {
    id: "city",
    title: "Which city are you renting in?",
    options: opts(
      "Mumbai",
      "Bengaluru",
      "Pune",
      "Hyderabad",
      "Delhi NCR",
      "Chennai",
      "Kolkata",
      "Other",
    ),
  },
  {
    id: "monthly_rent",
    title: "What is your monthly rent?",
    options: opts("Under ₹15k", "₹15k–₹30k", "₹30k–₹60k", "₹60k+"),
  },
  {
    id: "deposit_months",
    title: "How many months of deposit has the landlord asked for?",
    options: opts("1–2 months", "3–5 months", "6–10 months", "10+ months"),
  },
  {
    id: "move_timeline",
    title: "When are you planning to move?",
    options: opts("Looking now", "Within 30 days", "1–3 months", "Just exploring"),
  },
  {
    id: "employment",
    title: "What best describes your employment type?",
    options: opts("Salaried", "Freelancer", "Business owner", "Student", "Gig worker"),
  },
  {
    id: "income",
    title: "What is your monthly income?",
    options: opts("Under ₹25k", "₹25k–₹50k", "₹50k–₹1L", "₹1L+"),
  },
  {
    id: "interest",
    title: "If RentShield reduced your deposit from 6 months to 1 month, would you use it?",
    options: opts("Definitely", "Probably", "Maybe", "Unlikely"),
  },
  {
    id: "biggest_challenge",
    title: "What is the biggest challenge when renting?",
    options: opts(
      "Large security deposit",
      "Brokerage fees",
      "Finding trustworthy landlords",
      "Documentation hassles",
      "Moving costs",
      "Other",
    ),
  },
];

export const ownerQuestions: Question[] = [
  {
    id: "city",
    title: "Which city is your property in?",
    options: opts("Mumbai", "Bengaluru", "Pune", "Hyderabad", "Any other"),
  },
  {
    id: "property_type",
    title: "What type of property do you own?",
    options: opts("Apartment", "Independent house", "Villa", "PG", "Co-living", "Commercial"),
  },
  {
    id: "furnishing",
    title: "What is the furnishing level?",
    options: opts("Fully furnished", "Semi-furnished", "Unfurnished"),
  },
  {
    id: "monthly_rent",
    title: "What is the monthly rent?",
    options: opts("Under ₹20k", "₹20k–₹50k", "₹50k–₹1L", "₹1L+"),
  },
  {
    id: "deposit_required",
    title: "How many months of deposit do you currently require?",
    options: opts("1–2 months", "3–5 months", "6–10 months", "10+ months"),
  },
  {
    id: "worry",
    title: "What worries you most about tenants?",
    options: opts(
      "Property damage",
      "Missed rent",
      "Delayed eviction",
      "Illegal occupancy",
      "Maintenance negligence",
      "Frequent tenant turnover",
      "Other",
    ),
  },
  {
    id: "past_losses",
    title: "Have you experienced tenant-related losses before?",
    options: opts("Yes, major damage", "Minor issues only", "Never"),
  },
  {
    id: "accept_lower_deposit",
    title: "Would you accept a lower deposit if damages were insured?",
    options: opts("Yes", "Maybe", "No"),
  },
  {
    id: "deposit_reduction",
    title: "How much deposit reduction would you consider?",
    options: opts("1 month", "2 months", "3 months", "No reduction", "Other"),
  },
  {
    id: "vacancy_time",
    title: "How quickly do you usually find tenants?",
    options: opts("Within 1 month", "2 months", "More than 2 months"),
  },
  {
    id: "tenant_source",
    title: "How do you currently find tenants?",
    options: opts("Broker", "NoBroker", "Magicbricks", "Friends/family", "Housing society", "Social media"),
  },
  {
    id: "verification",
    title: "Would you use a tenant verification / risk score to vet tenants?",
    options: opts("Yes", "No", "Maybe"),
  },
];
