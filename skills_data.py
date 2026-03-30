"""
data/skills_data.py
Reference data: skills by domain, job roles, companies, courses
"""

# ── Tech skills by category ─────────────────────────────────────────────────
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
        "data analysis", "data visualization", "statistical analysis"
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
    "Tools & Practices": [
        "git", "github", "gitlab", "jira", "agile", "scrum", "tdd", "unit testing",
        "pytest", "selenium", "postman", "swagger", "figma", "adobe xd"
    ],
    "Mobile": [
        "android", "ios", "react native", "flutter", "xamarin", "swift", "kotlin"
    ],
    "Soft Skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "critical thinking", "time management", "project management",
        "presentation", "collaboration", "mentoring"
    ]
}

# ── Job roles with required skills ──────────────────────────────────────────
JOB_ROLES = {
    "Data Scientist": {
        "required": ["python", "machine learning", "statistics", "pandas", "numpy", "sql"],
        "good_to_have": ["deep learning", "pytorch", "tensorflow", "spark", "tableau"],
        "avg_salary": "$95,000 – $140,000",
        "demand": "Very High"
    },
    "Full Stack Developer": {
        "required": ["javascript", "react", "node.js", "html", "css", "sql", "git"],
        "good_to_have": ["typescript", "docker", "aws", "graphql", "mongodb"],
        "avg_salary": "$85,000 – $130,000",
        "demand": "High"
    },
    "ML Engineer": {
        "required": ["python", "machine learning", "tensorflow", "pytorch", "docker", "git"],
        "good_to_have": ["kubernetes", "mlflow", "airflow", "spark", "aws"],
        "avg_salary": "$110,000 – $160,000",
        "demand": "Very High"
    },
    "Backend Developer": {
        "required": ["python", "sql", "rest api", "git", "linux"],
        "good_to_have": ["docker", "aws", "redis", "kafka", "postgresql"],
        "avg_salary": "$80,000 – $125,000",
        "demand": "High"
    },
    "Frontend Developer": {
        "required": ["javascript", "react", "html", "css", "git"],
        "good_to_have": ["typescript", "vue", "angular", "figma", "testing"],
        "avg_salary": "$75,000 – $115,000",
        "demand": "High"
    },
    "DevOps Engineer": {
        "required": ["linux", "docker", "kubernetes", "ci/cd", "aws", "bash"],
        "good_to_have": ["terraform", "ansible", "prometheus", "jenkins", "python"],
        "avg_salary": "$90,000 – $140,000",
        "demand": "Very High"
    },
    "Data Analyst": {
        "required": ["sql", "python", "excel", "data visualization", "statistics"],
        "good_to_have": ["tableau", "power bi", "r", "pandas", "google analytics"],
        "avg_salary": "$60,000 – $95,000",
        "demand": "High"
    },
    "Cloud Architect": {
        "required": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform"],
        "good_to_have": ["security", "networking", "python", "cost optimization"],
        "avg_salary": "$130,000 – $180,000",
        "demand": "High"
    },
    "AI/LLM Engineer": {
        "required": ["python", "llm", "langchain", "openai", "nlp", "hugging face"],
        "good_to_have": ["fine-tuning", "vector databases", "fastapi", "docker"],
        "avg_salary": "$120,000 – $175,000",
        "demand": "Explosive"
    },
    "Mobile Developer": {
        "required": ["swift", "kotlin", "react native", "flutter", "git"],
        "good_to_have": ["firebase", "rest api", "ci/cd", "testing", "ux"],
        "avg_salary": "$80,000 – $130,000",
        "demand": "High"
    }
}

# ── Companies by domain ──────────────────────────────────────────────────────
COMPANIES = {
    "Data Science / AI": [
        {"name": "OpenAI", "type": "AI Research", "size": "1k–5k", "url": "https://openai.com/careers"},
        {"name": "DeepMind", "type": "AI Research", "size": "1k–5k", "url": "https://deepmind.google/about/careers/"},
        {"name": "Anthropic", "type": "AI Safety", "size": "500–1k", "url": "https://www.anthropic.com/careers"},
        {"name": "DataRobot", "type": "AutoML", "size": "1k–5k", "url": "https://www.datarobot.com/careers/"},
        {"name": "Palantir", "type": "Data Analytics", "size": "3k–5k", "url": "https://www.palantir.com/careers/"},
        {"name": "Databricks", "type": "Data Platform", "size": "5k+", "url": "https://www.databricks.com/company/careers"},
    ],
    "Full Stack / Web": [
        {"name": "Vercel", "type": "Frontend Cloud", "size": "500–1k", "url": "https://vercel.com/careers"},
        {"name": "Netlify", "type": "Web Platform", "size": "200–500", "url": "https://www.netlify.com/careers/"},
        {"name": "Shopify", "type": "E-commerce", "size": "10k+", "url": "https://www.shopify.com/careers"},
        {"name": "Stripe", "type": "Fintech", "size": "5k–10k", "url": "https://stripe.com/jobs"},
        {"name": "GitHub", "type": "Dev Tools", "size": "3k+", "url": "https://github.com/about/careers"},
    ],
    "Cloud / DevOps": [
        {"name": "AWS (Amazon)", "type": "Cloud", "size": "100k+", "url": "https://aws.amazon.com/careers/"},
        {"name": "Google Cloud", "type": "Cloud", "size": "100k+", "url": "https://careers.google.com"},
        {"name": "Microsoft Azure", "type": "Cloud", "size": "100k+", "url": "https://careers.microsoft.com"},
        {"name": "HashiCorp", "type": "DevOps Tools", "size": "2k+", "url": "https://www.hashicorp.com/careers"},
    ],
    "General Tech": [
        {"name": "Meta", "type": "Social / AI", "size": "80k+", "url": "https://www.metacareers.com"},
        {"name": "Apple", "type": "Consumer Tech", "size": "150k+", "url": "https://www.apple.com/careers/"},
        {"name": "Netflix", "type": "Streaming", "size": "10k+", "url": "https://jobs.netflix.com"},
        {"name": "Uber", "type": "Mobility", "size": "30k+", "url": "https://www.uber.com/us/en/careers/"},
    ]
}

# ── Course recommendations by skill ─────────────────────────────────────────
COURSES = {
    "python": [
        {"title": "Python for Everybody", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/specializations/python"},
        {"title": "Complete Python Bootcamp", "platform": "Udemy", "level": "Beginner", "url": "https://www.udemy.com/course/complete-python-bootcamp/"},
    ],
    "machine learning": [
        {"title": "ML Specialization (Andrew Ng)", "platform": "Coursera", "level": "Intermediate", "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
        {"title": "Fast.ai Practical Deep Learning", "platform": "fast.ai", "level": "Intermediate", "url": "https://course.fast.ai"},
    ],
    "deep learning": [
        {"title": "Deep Learning Specialization", "platform": "Coursera", "level": "Advanced", "url": "https://www.coursera.org/specializations/deep-learning"},
        {"title": "PyTorch for Deep Learning", "platform": "Udemy", "level": "Intermediate", "url": "https://www.udemy.com/course/pytorch-for-deep-learning-and-computer-vision/"},
    ],
    "react": [
        {"title": "React — The Complete Guide", "platform": "Udemy", "level": "Intermediate", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"},
        {"title": "Full Stack Open", "platform": "University of Helsinki", "level": "Intermediate", "url": "https://fullstackopen.com"},
    ],
    "aws": [
        {"title": "AWS Certified Solutions Architect", "platform": "Udemy", "level": "Intermediate", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/"},
        {"title": "AWS Skill Builder", "platform": "AWS", "level": "All levels", "url": "https://skillbuilder.aws"},
    ],
    "docker": [
        {"title": "Docker & Kubernetes: The Practical Guide", "platform": "Udemy", "level": "Intermediate", "url": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"},
    ],
    "sql": [
        {"title": "SQL for Data Science", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/learn/sql-for-data-science"},
        {"title": "Mode SQL Tutorial", "platform": "Mode", "level": "Beginner", "url": "https://mode.com/sql-tutorial/"},
    ],
    "nlp": [
        {"title": "NLP with HuggingFace Transformers", "platform": "HuggingFace", "level": "Advanced", "url": "https://huggingface.co/learn/nlp-course/"},
        {"title": "Natural Language Processing Specialization", "platform": "Coursera", "level": "Advanced", "url": "https://www.coursera.org/specializations/natural-language-processing"},
    ],
    "llm": [
        {"title": "LangChain for LLM App Development", "platform": "DeepLearning.AI", "level": "Intermediate", "url": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/"},
        {"title": "Building LLM Apps", "platform": "DeepLearning.AI", "level": "Intermediate", "url": "https://www.deeplearning.ai"},
    ],
    "kubernetes": [
        {"title": "Certified Kubernetes Administrator (CKA)", "platform": "Linux Foundation", "level": "Advanced", "url": "https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/"},
    ],
    "data visualization": [
        {"title": "Data Visualization with Python", "platform": "Coursera", "level": "Beginner", "url": "https://www.coursera.org/learn/python-for-data-visualization"},
    ],
    "default": [
        {"title": "Search on Coursera", "platform": "Coursera", "level": "Various", "url": "https://www.coursera.org"},
        {"title": "Search on Udemy", "platform": "Udemy", "level": "Various", "url": "https://www.udemy.com"},
    ]
}

# ── ATS keywords by section ──────────────────────────────────────────────────
ATS_KEYWORDS = {
    "action_verbs": [
        "developed", "built", "designed", "implemented", "led", "managed",
        "created", "optimized", "improved", "increased", "reduced", "delivered",
        "collaborated", "architected", "deployed", "automated", "analyzed",
        "launched", "scaled", "mentored", "coordinated", "drove", "achieved"
    ],
    "sections": [
        "experience", "education", "skills", "projects", "certifications",
        "summary", "objective", "achievements", "publications", "languages"
    ],
    "metrics_patterns": [
        r'\d+%', r'\$\d+', r'\d+x', r'\d+ million', r'\d+ thousand',
        r'\d+ users', r'\d+ team', r'\d+ years'
    ]
}
