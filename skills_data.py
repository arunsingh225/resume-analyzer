"""
enhanced_skills_data.py
Expanded reference data for resume analysis across tech and non-tech domains.
Designed to improve skill extraction, domain detection, and role recommendations
for a wider range of resumes.
"""

# ---------------------------------------------------------------------------
# Skill aliases / normalization
# ---------------------------------------------------------------------------
SKILL_ALIASES = {
    # programming / tech
    "js": "javascript",
    "ts": "typescript",
    "node": "node.js",
    "nodejs": "node.js",
    "node js": "node.js",
    "nextjs": "next.js",
    "rest": "rest api",
    "restful api": "rest api",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "llms": "llm",
    "genai": "generative ai",
    "gen ai": "generative ai",
    "powerbi": "power bi",
    "ms excel": "excel",
    "advanced excel": "excel",
    "advance excel": "excel",
    "microsoft excel": "excel",
    "power point": "powerpoint",
    "ms powerpoint": "powerpoint",
    "google sheets": "spreadsheet",

    # accounts / finance
    "busy": "busy software",
    "busy accounting software": "busy software",
    "gst filing": "gst",
    "book keeping": "bookkeeping",
    "book keeping and accounting": "bookkeeping",
    "accounts payable": "accounts payable",
    "accounts receivable": "accounts receivable",
    "tally erp": "tally",
    "erp 9": "tally",
    "tally prime": "tally",
    "cbo erp": "erp",
    "inventory management": "inventory",

    # sales / customer support
    "crm tools": "crm",
    "customer relationship management": "crm",
    "inside sales": "sales",
    "tele calling": "telecalling",
    "tele-calling": "telecalling",
    "client handling": "client management",

    # hr / ops / admin
    "recruitment": "talent acquisition",
    "hiring": "talent acquisition",
    "payroll processing": "payroll",
    "vendor mgmt": "vendor management",
    "ops": "operations",

    # healthcare / misc
    "emr": "electronic medical records",
    "ehr": "electronic medical records",
}

# ---------------------------------------------------------------------------
# Domain keywords for routing resumes to the right role family
# ---------------------------------------------------------------------------
DOMAIN_KEYWORDS = {
    "tech": [
        "python", "java", "javascript", "react", "node.js", "sql", "html",
        "css", "machine learning", "deep learning", "docker", "aws", "api",
        "tensorflow", "pytorch", "git", "kubernetes", "data science"
    ],
    "data": [
        "python", "sql", "excel", "power bi", "tableau", "statistics",
        "data analysis", "data visualization", "pandas", "numpy", "reporting"
    ],
    "accounts_finance": [
        "tally", "busy software", "accounting", "bookkeeping", "gst", "taxation",
        "invoice", "billing", "ledger", "bank reconciliation", "excel", "erp",
        "accounts payable", "accounts receivable", "audit"
    ],
    "sales_marketing": [
        "sales", "lead generation", "negotiation", "crm", "digital marketing",
        "seo", "sem", "social media", "email marketing", "telecalling", "branding"
    ],
    "hr_admin": [
        "talent acquisition", "recruitment", "onboarding", "payroll", "hr operations",
        "employee engagement", "administration", "scheduling", "documentation"
    ],
    "operations_support": [
        "operations", "process improvement", "customer support", "client management",
        "documentation", "coordination", "reporting", "inventory", "dispatch"
    ],
    "healthcare": [
        "patient care", "medical billing", "hospital", "pharmacy", "healthcare",
        "electronic medical records", "insurance claims", "front desk"
    ]
}

# ---------------------------------------------------------------------------
# Skills by category across multiple domains
# ---------------------------------------------------------------------------
SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
        "kotlin", "swift", "r", "scala", "ruby", "php", "dart", "matlab"
    ],
    "Web Development": [
        "html", "css", "react", "angular", "vue", "next.js", "node.js", "django",
        "flask", "fastapi", "spring boot", "express", "tailwind", "bootstrap",
        "graphql", "rest api", "websocket"
    ],
    "Data & AI": [
        "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
        "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
        "seaborn", "plotly", "hugging face", "langchain", "openai", "llm",
        "generative ai", "data analysis", "data visualization", "statistical analysis",
        "power bi", "tableau", "excel"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd",
        "jenkins", "github actions", "linux", "bash", "ansible", "prometheus",
        "grafana", "nginx", "apache"
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
        "cassandra", "sqlite", "oracle", "dynamodb", "firebase", "supabase"
    ],
    "Accounts & Finance": [
        "accounting", "bookkeeping", "tally", "busy software", "gst", "taxation",
        "invoice processing", "billing", "ledger", "bank reconciliation", "erp",
        "accounts payable", "accounts receivable", "financial reporting", "audit",
        "payroll", "excel", "spreadsheet"
    ],
    "Sales & Marketing": [
        "sales", "lead generation", "crm", "negotiation", "cold calling",
        "telecalling", "customer relationship", "digital marketing", "seo", "sem",
        "social media marketing", "content marketing", "branding", "campaign management",
        "market research", "email marketing"
    ],
    "HR & Administration": [
        "talent acquisition", "recruitment", "onboarding", "payroll", "attendance",
        "employee relations", "hr operations", "documentation", "scheduling",
        "vendor management", "ms office", "excel", "word", "powerpoint"
    ],
    "Operations & Support": [
        "operations", "process improvement", "inventory", "dispatch", "coordination",
        "documentation", "reporting", "customer support", "client management",
        "data entry", "quality control"
    ],
    "Healthcare": [
        "patient care", "medical billing", "healthcare operations", "insurance claims",
        "hospital management", "electronic medical records", "pharmacy", "front desk"
    ],
    "Soft Skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "critical thinking", "time management", "project management",
        "presentation", "collaboration", "mentoring", "adaptability",
        "attention to detail", "analytical thinking"
    ]
}

# ---------------------------------------------------------------------------
# Job roles with metadata and domain tags
# ---------------------------------------------------------------------------
JOB_ROLES = {
    # Tech / Data
    "Data Scientist": {
        "domain": "data",
        "required": ["python", "machine learning", "statistics", "pandas", "numpy", "sql"],
        "good_to_have": ["deep learning", "pytorch", "tensorflow", "spark", "tableau"],
        "avg_salary": "$95,000 – $140,000",
        "demand": "Very High"
    },
    "Data Analyst": {
        "domain": "data",
        "required": ["sql", "python", "excel", "data visualization", "statistics"],
        "good_to_have": ["tableau", "power bi", "r", "pandas", "google analytics"],
        "avg_salary": "$60,000 – $95,000",
        "demand": "High"
    },
    "Business Analyst": {
        "domain": "data",
        "required": ["excel", "sql", "reporting", "requirement gathering", "communication"],
        "good_to_have": ["power bi", "tableau", "jira", "process mapping"],
        "avg_salary": "$70,000 – $110,000",
        "demand": "High"
    },
    "Full Stack Developer": {
        "domain": "tech",
        "required": ["javascript", "react", "node.js", "html", "css", "sql", "git"],
        "good_to_have": ["typescript", "docker", "aws", "graphql", "mongodb"],
        "avg_salary": "$85,000 – $130,000",
        "demand": "High"
    },
    "Backend Developer": {
        "domain": "tech",
        "required": ["python", "sql", "rest api", "git", "linux"],
        "good_to_have": ["docker", "aws", "redis", "kafka", "postgresql"],
        "avg_salary": "$80,000 – $125,000",
        "demand": "High"
    },
    "Frontend Developer": {
        "domain": "tech",
        "required": ["javascript", "react", "html", "css", "git"],
        "good_to_have": ["typescript", "vue", "angular", "figma", "testing"],
        "avg_salary": "$75,000 – $115,000",
        "demand": "High"
    },
    "ML Engineer": {
        "domain": "tech",
        "required": ["python", "machine learning", "tensorflow", "pytorch", "docker", "git"],
        "good_to_have": ["kubernetes", "mlflow", "airflow", "spark", "aws"],
        "avg_salary": "$110,000 – $160,000",
        "demand": "Very High"
    },
    "DevOps Engineer": {
        "domain": "tech",
        "required": ["linux", "docker", "kubernetes", "ci/cd", "aws", "bash"],
        "good_to_have": ["terraform", "ansible", "prometheus", "jenkins", "python"],
        "avg_salary": "$90,000 – $140,000",
        "demand": "Very High"
    },
    "AI/LLM Engineer": {
        "domain": "tech",
        "required": ["python", "llm", "langchain", "openai", "nlp", "hugging face"],
        "good_to_have": ["fine-tuning", "vector databases", "fastapi", "docker"],
        "avg_salary": "$120,000 – $175,000",
        "demand": "Explosive"
    },
    "Mobile Developer": {
        "domain": "tech",
        "required": ["swift", "kotlin", "react native", "flutter", "git"],
        "good_to_have": ["firebase", "rest api", "ci/cd", "testing", "ux"],
        "avg_salary": "$80,000 – $130,000",
        "demand": "High"
    },

    # Accounts / Finance
    "Accountant": {
        "domain": "accounts_finance",
        "required": ["accounting", "tally", "excel", "ledger", "bookkeeping"],
        "good_to_have": ["gst", "erp", "bank reconciliation", "financial reporting"],
        "avg_salary": "$35,000 – $70,000",
        "demand": "High"
    },
    "Accounts Executive": {
        "domain": "accounts_finance",
        "required": ["tally", "busy software", "excel", "billing", "accounting"],
        "good_to_have": ["gst", "invoice processing", "erp", "bookkeeping"],
        "avg_salary": "$30,000 – $60,000",
        "demand": "High"
    },
    "MIS Executive": {
        "domain": "accounts_finance",
        "required": ["excel", "reporting", "data analysis", "spreadsheet", "communication"],
        "good_to_have": ["power bi", "sql", "dashboarding", "erp"],
        "avg_salary": "$35,000 – $65,000",
        "demand": "High"
    },
    "Billing Executive": {
        "domain": "accounts_finance",
        "required": ["billing", "invoice processing", "excel", "accounting", "erp"],
        "good_to_have": ["gst", "tally", "busy software"],
        "avg_salary": "$28,000 – $55,000",
        "demand": "Moderate"
    },
    "Finance Executive": {
        "domain": "accounts_finance",
        "required": ["accounting", "excel", "financial reporting", "analysis", "bookkeeping"],
        "good_to_have": ["erp", "gst", "audit", "taxation"],
        "avg_salary": "$40,000 – $75,000",
        "demand": "High"
    },

    # Sales / Marketing
    "Sales Executive": {
        "domain": "sales_marketing",
        "required": ["sales", "communication", "negotiation", "client management", "lead generation"],
        "good_to_have": ["crm", "reporting", "telecalling"],
        "avg_salary": "$30,000 – $70,000",
        "demand": "High"
    },
    "Digital Marketing Executive": {
        "domain": "sales_marketing",
        "required": ["digital marketing", "seo", "social media marketing", "content marketing", "analytics"],
        "good_to_have": ["sem", "email marketing", "google analytics", "canva"],
        "avg_salary": "$35,000 – $75,000",
        "demand": "High"
    },
    "Customer Success Executive": {
        "domain": "sales_marketing",
        "required": ["communication", "customer support", "client management", "problem solving", "crm"],
        "good_to_have": ["reporting", "upselling", "presentation"],
        "avg_salary": "$35,000 – $70,000",
        "demand": "High"
    },

    # HR / Admin
    "HR Executive": {
        "domain": "hr_admin",
        "required": ["recruitment", "communication", "documentation", "onboarding", "coordination"],
        "good_to_have": ["payroll", "hr operations", "employee engagement", "excel"],
        "avg_salary": "$35,000 – $65,000",
        "demand": "Moderate"
    },
    "Admin Executive": {
        "domain": "hr_admin",
        "required": ["documentation", "scheduling", "coordination", "excel", "communication"],
        "good_to_have": ["vendor management", "reporting", "powerpoint"],
        "avg_salary": "$28,000 – $55,000",
        "demand": "Moderate"
    },

    # Operations / Support
    "Operations Executive": {
        "domain": "operations_support",
        "required": ["operations", "coordination", "reporting", "documentation", "communication"],
        "good_to_have": ["excel", "inventory", "process improvement"],
        "avg_salary": "$32,000 – $60,000",
        "demand": "High"
    },
    "Customer Support Executive": {
        "domain": "operations_support",
        "required": ["customer support", "communication", "problem solving", "documentation", "crm"],
        "good_to_have": ["ticketing", "client management", "excel"],
        "avg_salary": "$28,000 – $50,000",
        "demand": "High"
    },
    "Data Entry Operator": {
        "domain": "operations_support",
        "required": ["data entry", "excel", "documentation", "accuracy", "typing"],
        "good_to_have": ["erp", "reporting"],
        "avg_salary": "$22,000 – $40,000",
        "demand": "Moderate"
    },

    # Healthcare
    "Medical Billing Executive": {
        "domain": "healthcare",
        "required": ["medical billing", "invoice processing", "insurance claims", "excel", "documentation"],
        "good_to_have": ["healthcare operations", "electronic medical records"],
        "avg_salary": "$30,000 – $60,000",
        "demand": "Moderate"
    },
    "Hospital Operations Executive": {
        "domain": "healthcare",
        "required": ["healthcare operations", "coordination", "documentation", "reporting", "communication"],
        "good_to_have": ["patient care", "excel", "insurance claims"],
        "avg_salary": "$35,000 – $65,000",
        "demand": "Moderate"
    }
}

# ---------------------------------------------------------------------------
# Role groups by domain (useful for filtering recommendations)
# ---------------------------------------------------------------------------
DOMAIN_ROLE_MAP = {}
for role_name, role_meta in JOB_ROLES.items():
    DOMAIN_ROLE_MAP.setdefault(role_meta["domain"], []).append(role_name)

# ---------------------------------------------------------------------------
# Companies by domain
# ---------------------------------------------------------------------------
COMPANIES = {
    "Data Science / AI": [
        {"name": "OpenAI", "type": "AI Research", "size": "1k–5k", "url": "https://openai.com/careers"},
        {"name": "DeepMind", "type": "AI Research", "size": "1k–5k", "url": "https://deepmind.google/about/careers/"},
        {"name": "Anthropic", "type": "AI Safety", "size": "500–1k", "url": "https://www.anthropic.com/careers"},
        {"name": "Databricks", "type": "Data Platform", "size": "5k+", "url": "https://www.databricks.com/company/careers"},
    ],
    "Full Stack / Web": [
        {"name": "Vercel", "type": "Frontend Cloud", "size": "500–1k", "url": "https://vercel.com/careers"},
        {"name": "Netlify", "type": "Web Platform", "size": "200–500", "url": "https://www.netlify.com/careers/"},
        {"name": "Shopify", "type": "E-commerce", "size": "10k+", "url": "https://www.shopify.com/careers"},
        {"name": "Stripe", "type": "Fintech", "size": "5k–10k", "url": "https://stripe.com/jobs"},
    ],
    "Cloud / DevOps": [
        {"name": "AWS (Amazon)", "type": "Cloud", "size": "100k+", "url": "https://aws.amazon.com/careers/"},
        {"name": "Google Cloud", "type": "Cloud", "size": "100k+", "url": "https://careers.google.com"},
        {"name": "Microsoft Azure", "type": "Cloud", "size": "100k+", "url": "https://careers.microsoft.com"},
    ],
    "Accounts / Finance": [
        {"name": "Deloitte", "type": "Advisory / Finance", "size": "100k+", "url": "https://www2.deloitte.com/global/en/careers.html"},
        {"name": "EY", "type": "Audit / Tax", "size": "100k+", "url": "https://careers.ey.com"},
        {"name": "KPMG", "type": "Audit / Advisory", "size": "100k+", "url": "https://kpmg.com/careers"},
        {"name": "Genpact", "type": "Finance Operations", "size": "100k+", "url": "https://www.genpact.com/careers"},
    ],
    "Sales / Marketing": [
        {"name": "HubSpot", "type": "CRM / Marketing", "size": "5k+", "url": "https://www.hubspot.com/careers"},
        {"name": "Salesforce", "type": "CRM", "size": "50k+", "url": "https://careers.salesforce.com"},
        {"name": "Zomato", "type": "Consumer / Sales Ops", "size": "10k+", "url": "https://www.zomato.com/careers"},
    ],
    "General": [
        {"name": "Meta", "type": "Social / AI", "size": "80k+", "url": "https://www.metacareers.com"},
        {"name": "Apple", "type": "Consumer Tech", "size": "150k+", "url": "https://www.apple.com/careers/"},
        {"name": "Uber", "type": "Mobility", "size": "30k+", "url": "https://www.uber.com/us/en/careers/"},
    ]
}

# ---------------------------------------------------------------------------
# Course recommendations by skill
# ---------------------------------------------------------------------------
COURSES = {
    "python": [
        {"title": "Python for Everybody", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/specializations/python"},
        {"title": "Complete Python Bootcamp", "platform": "Udemy", "level": "Beginner", "url": "https://www.udemy.com/course/complete-python-bootcamp/"},
    ],
    "sql": [
        {"title": "SQL for Data Science", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/learn/sql-for-data-science"},
        {"title": "Mode SQL Tutorial", "platform": "Mode", "level": "Beginner", "url": "https://mode.com/sql-tutorial/"},
    ],
    "excel": [
        {"title": "Excel Skills for Business", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/specializations/excel"},
        {"title": "Microsoft Excel - Excel from Beginner to Advanced", "platform": "Udemy", "level": "Beginner", "url": "https://www.udemy.com/course/microsoft-excel-2013-from-beginner-to-advanced-and-beyond/"},
    ],
    "tally": [
        {"title": "Tally Prime Complete Course", "platform": "Udemy", "level": "Beginner", "url": "https://www.udemy.com/"},
    ],
    "gst": [
        {"title": "GST Practitioner Course", "platform": "Udemy", "level": "Beginner", "url": "https://www.udemy.com/"},
    ],
    "power bi": [
        {"title": "Microsoft Power BI Data Analyst", "platform": "Microsoft Learn", "level": "Intermediate", "url": "https://learn.microsoft.com/"},
    ],
    "machine learning": [
        {"title": "ML Specialization (Andrew Ng)", "platform": "Coursera", "level": "Intermediate", "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
        {"title": "Fast.ai Practical Deep Learning", "platform": "fast.ai", "level": "Intermediate", "url": "https://course.fast.ai"},
    ],
    "deep learning": [
        {"title": "Deep Learning Specialization", "platform": "Coursera", "level": "Advanced", "url": "https://www.coursera.org/specializations/deep-learning"},
    ],
    "react": [
        {"title": "React — The Complete Guide", "platform": "Udemy", "level": "Intermediate", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"},
        {"title": "Full Stack Open", "platform": "University of Helsinki", "level": "Intermediate", "url": "https://fullstackopen.com"},
    ],
    "aws": [
        {"title": "AWS Certified Solutions Architect", "platform": "Udemy", "level": "Intermediate", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/"},
        {"title": "AWS Skill Builder", "platform": "AWS", "level": "All levels", "url": "https://skillbuilder.aws"},
    ],
    "digital marketing": [
        {"title": "Fundamentals of Digital Marketing", "platform": "Google", "level": "Beginner", "url": "https://grow.google/"},
    ],
    "seo": [
        {"title": "SEO Fundamentals", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/"},
    ],
    "recruitment": [
        {"title": "Talent Acquisition", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/"},
    ],
    "customer support": [
        {"title": "Customer Service Fundamentals", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/"},
    ],
    "default": [
        {"title": "Search on Coursera", "platform": "Coursera", "level": "Various", "url": "https://www.coursera.org"},
        {"title": "Search on Udemy", "platform": "Udemy", "level": "Various", "url": "https://www.udemy.com"},
    ]
}

# ---------------------------------------------------------------------------
# ATS keywords by section
# ---------------------------------------------------------------------------
ATS_KEYWORDS = {
    "action_verbs": [
        "developed", "built", "designed", "implemented", "led", "managed",
        "created", "optimized", "improved", "increased", "reduced", "delivered",
        "collaborated", "architected", "deployed", "automated", "analyzed",
        "launched", "scaled", "mentored", "coordinated", "drove", "achieved",
        "maintained", "generated", "prepared", "reconciled", "processed",
        "resolved", "supported", "monitored", "negotiated", "streamlined"
    ],
    "sections": [
        "experience", "education", "skills", "projects", "certifications",
        "summary", "objective", "achievements", "publications", "languages",
        "internship", "work history", "professional experience", "technical skills"
    ],
    "metrics_patterns": [
        r"\d+%", r"\$\d+", r"\d+x", r"\d+ million", r"\d+ thousand",
        r"\d+ users", r"\d+ team", r"\d+ years", r"\d+ months", r"\d+ clients",
        r"\d+ projects", r"\d+ reports", r"\d+ invoices"
    ]
}

# ---------------------------------------------------------------------------
# Optional generic skills that are useful when the resume has low signal
# ---------------------------------------------------------------------------
GENERAL_BASELINE_SKILLS = [
    "communication", "teamwork", "problem solving", "time management",
    "excel", "documentation", "reporting"
]

