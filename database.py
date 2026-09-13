import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "launchpad.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            organizer TEXT NOT NULL,
            city TEXT NOT NULL,
            mode TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            tags TEXT NOT NULL,
            note TEXT,
            url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Resources table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            type TEXT NOT NULL,
            icon TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            url TEXT NOT NULL,
            likes INTEGER DEFAULT 0
        )
    """)

    # Degrees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS degrees (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            full_title TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            duration_years INTEGER DEFAULT 4,
            semesters_count INTEGER DEFAULT 8
        )
    """)

    # Roadmap Semesters table (8 semesters per degree)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_semesters (
            id TEXT PRIMARY KEY,
            degree_id TEXT NOT NULL,
            year INTEGER NOT NULL,
            semester_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            focus_areas TEXT NOT NULL,
            academic_core TEXT NOT NULL,
            industry_prep TEXT NOT NULL,
            milestone TEXT NOT NULL,
            FOREIGN KEY (degree_id) REFERENCES degrees(id)
        )
    """)

    # Roadmap Tasks table (actionable checkboxes per semester)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_tasks (
            id TEXT PRIMARY KEY,
            semester_id TEXT NOT NULL,
            task_order INTEGER NOT NULL,
            task_text TEXT NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY (semester_id) REFERENCES roadmap_semesters(id)
        )
    """)

    # User task progress tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            task_id TEXT PRIMARY KEY,
            completed BOOLEAN NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Saved events (bookmarks)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_events (
            event_id TEXT PRIMARY KEY,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    """)

    # User preferences (e.g. selected degree and active semester)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Hackathon Squad Posts (Teammate Finder)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS squad_posts (
            id TEXT PRIMARY KEY,
            hackathon_id TEXT,
            hackathon_name TEXT NOT NULL,
            project_title TEXT NOT NULL,
            leader_name TEXT NOT NULL,
            leader_college TEXT NOT NULL,
            roles_needed TEXT NOT NULL,
            current_members INTEGER DEFAULT 1,
            team_size INTEGER DEFAULT 4,
            tech_stack TEXT NOT NULL,
            description TEXT NOT NULL,
            contact_type TEXT NOT NULL,
            contact_value TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Freshers Internships and Off-Campus Hiring Board
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id TEXT PRIMARY KEY,
            company TEXT NOT NULL,
            role_title TEXT NOT NULL,
            opportunity_type TEXT NOT NULL,
            eligible_batches TEXT NOT NULL,
            role_category TEXT NOT NULL,
            location TEXT NOT NULL,
            stipend_or_ctc TEXT NOT NULL,
            apply_url TEXT NOT NULL,
            deadline TEXT,
            description TEXT NOT NULL,
            skills TEXT NOT NULL,
            selection_process TEXT,
            status TEXT DEFAULT 'Active',
            featured BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Project Idea Vault & Architecture Blueprints
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            tagline TEXT NOT NULL,
            level TEXT NOT NULL,
            domain TEXT NOT NULL,
            problem_statement TEXT NOT NULL,
            target_audience TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            architecture_diagram TEXT NOT NULL,
            components TEXT NOT NULL,
            data_flow TEXT NOT NULL,
            database_schema TEXT NOT NULL,
            interview_qa TEXT NOT NULL,
            milestones TEXT NOT NULL,
            github_starter_url TEXT,
            stars INTEGER DEFAULT 0,
            featured BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Saved Projects (Bookmarks)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_projects (
            project_id TEXT PRIMARY KEY,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    """)

    conn.commit()
    seed_data(cursor, conn)
    seed_degree_roadmaps(cursor, conn)
    seed_squad_posts(cursor, conn)
    seed_opportunities(cursor, conn)
    seed_projects(cursor, conn)
    conn.close()

def seed_data(cursor, conn):
    events = [
            (
                "innohacks",
                "Innohacks 4.0",
                "Innogeeks / KIET",
                "Ghaziabad, Delhi NCR",
                "Offline",
                "2026-09-02",
                "2026-09-26",
                json.dumps(["National", "Open innovation"]),
                "Student-led national hackathon",
                "https://innohacks-4.devfolio.co/"
            ),
            (
                "binary-hacks",
                "Binary Hacks 4.0",
                "The Binary Club",
                "Ghaziabad, Uttar Pradesh",
                "Offline",
                "2026-09-21",
                "2026-09-22",
                json.dumps(["CSE", "36 hours"]),
                "Offline build sprint",
                "https://binary-hacks-4.devfolio.co/"
            ),
            (
                "hacknex",
                "HackNex Season 2",
                "JIS College of Engineering",
                "Kalyani, West Bengal",
                "Offline",
                "2026-09-25",
                "2026-09-26",
                json.dumps(["AI / ML", "FinTech", "EdTech"]),
                "Beginners and experienced builders",
                "https://hacknex-season-2.devfolio.co/"
            ),
            (
                "nexhack",
                "NexHack 2.0",
                "IITM, New Delhi",
                "New Delhi",
                "Offline",
                "2026-09-25",
                "2026-09-26",
                json.dumps(["AI", "National", "36 hours"]),
                "Build solutions for real problems",
                "https://nexhack-2.devfolio.co/"
            ),
            (
                "cognition",
                "Cognition GameJam '26",
                "SIESGST Technical Team",
                "Navi Mumbai, Maharashtra",
                "Offline",
                "2026-09-25",
                "2026-09-26",
                json.dumps(["Game dev", "Design", "Prototype"]),
                "Prototype submission: 11 Sep",
                "https://cognition-gamejam-1.devfolio.co/"
            ),
            (
                "hackoverflow",
                "HackOverflow 3.0",
                "Department of IT, Pillai College",
                "Panvel, Navi Mumbai",
                "Online",
                "2026-09-12",
                "2026-09-14",
                json.dumps(["Web3", "Cloud", "Open Innovation"]),
                "Pan-India student hackathon with mentorship",
                "https://hackoverflow-3.devfolio.co/"
            ),
            (
                "synthethic-hacks",
                "Synthetic Hacks",
                "Dev Community India",
                "Bengaluru, Karnataka",
                "Online",
                "2026-09-18",
                "2026-09-20",
                json.dumps(["Generative AI", "APIs", "Remote"]),
                "Build full-stack AI agents and micro-apps",
                "https://devpost.com/"
            ),
            (
                "hack-chennai",
                "Hack Chennai 2026",
                "Anna University & GDG",
                "Chennai, Tamil Nadu",
                "Offline",
                "2026-09-28",
                "2026-09-30",
                json.dumps(["AI", "Cloud", "36 hours"]),
                "South India's premier student developer hackathon",
                "https://devfolio.co/"
            ),
            (
                "hyderabad-build",
                "T-Hub GenAI Hackathon",
                "IIIT Hyderabad & T-Hub",
                "Hyderabad, Telangana",
                "Offline",
                "2026-10-03",
                "2026-10-05",
                json.dumps(["GenAI", "LLMs", "Startups"]),
                "Rapid prototype build with venture incubation track",
                "https://devfolio.co/"
            ),
            (
                "desert-hacks",
                "DesertHacks 2026",
                "LNMIIT & Turing Club",
                "Jaipur, Rajasthan",
                "Offline",
                "2026-10-10",
                "2026-10-12",
                json.dumps(["Open Innovation", "IoT", "Cybersec"]),
                "36-hour flagship hackathon in the Pink City",
                "https://devfolio.co/"
            ),
            (
                "gujarat-hack",
                "Gujarat Innovation Hackfest",
                "DA-IICT & IEEE",
                "Gandhinagar, Gujarat",
                "Offline",
                "2026-10-15",
                "2026-10-17",
                json.dumps(["FinTech", "Web3", "Hardware"]),
                "Build real tech solutions for Western India industries",
                "https://devfolio.co/"
            ),
            (
                "kerala-build",
                "Kochi DevSprint 2026",
                "Maker Village & CUSAT",
                "Kochi, Kerala",
                "Offline",
                "2026-10-20",
                "2026-10-22",
                json.dumps(["Robotics", "CleanTech", "AI"]),
                "Hardware + Software dual-track campus hackathon",
                "https://devfolio.co/"
            ),
            (
                "punjab-hacks",
                "Punjab HackSprint",
                "TIET Patiala & MLH",
                "Patiala, Punjab",
                "Offline",
                "2026-10-24",
                "2026-10-26",
                json.dumps(["Full-Stack", "Mobile", "Beginner"]),
                "Mentored hackathon for North India freshers",
                "https://devfolio.co/"
            ),
            (
                "bhopal-hacks",
                "Central India Hackfest",
                "MANIT Bhopal & ACM",
                "Bhopal, Madhya Pradesh",
                "Offline",
                "2026-11-01",
                "2026-11-03",
                json.dumps(["EdTech", "AgriTech", "AI"]),
                "Biggest collegiate tech showdown in Central India",
                "https://devfolio.co/"
            ),
            (
                "odisha-hack",
                "Kalinga Innovate 2026",
                "KIIT & Tech Society",
                "Bhubaneswar, Odisha",
                "Offline",
                "2026-11-07",
                "2026-11-09",
                json.dumps(["Smart Cities", "HealthTech", "Cloud"]),
                "East India premier hackathon with top incubators",
                "https://devfolio.co/"
            ),
            (
                "sih-national",
                "Smart India Hackathon 2026",
                "Ministry of Education & AICTE",
                "Pan-India (Multiple Nodal Centers)",
                "Online",
                "2026-11-15",
                "2026-11-20",
                json.dumps(["National", "Hardware & Software", "Government"]),
                "World's biggest open innovation model for engineering students",
                "https://sih.gov.in/"
            )
        ]
    cursor.executemany("""
        INSERT OR IGNORE INTO events (id, name, organizer, city, mode, start_date, end_date, tags, note, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, events)

    # Check resources
    cursor.execute("SELECT COUNT(*) FROM resources")
    if cursor.fetchone()[0] == 0:
        resources = [
            ("start", "Docs", "M", "MDN Learn", "A structured path through HTML, CSS, JavaScript, browser APIs, and web fundamentals.", "https://developer.mozilla.org/en-US/docs/Learn_web_development", 14),
            ("start", "Roadmap", "R", "roadmap.sh", "Visual maps for frontend, backend, DevOps, data structures, and other technical paths.", "https://roadmap.sh/", 29),
            ("start", "Course", "C", "CS50x", "A strong computer science foundation covering algorithms, data structures, C, Python, SQL, and web development.", "https://cs50.harvard.edu/x/", 38),
            ("start", "Practice", "F", "freeCodeCamp", "Interactive lessons and projects for web development, JavaScript, Python, and more.", "https://www.freecodecamp.org/learn/", 22),
            ("solve", "DSA Sheet", "T", "take U forward", "A topic-by-topic DSA sequence with explanations, patterns, and practice problems.", "https://takeuforward.org/", 51),
            ("solve", "Problem Set", "C", "CSES", "A focused collection of algorithmic problems for building competitive programming fundamentals.", "https://cses.fi/problemset/", 19),
            ("solve", "Contests", "CF", "Codeforces", "Regular programming contests and a large archive of problems across difficulty levels.", "https://codeforces.com/", 26),
            ("solve", "Interview", "L", "LeetCode", "Practice data structures, algorithms, SQL, and interview-style questions.", "https://leetcode.com/problemset/", 43),
            ("ship", "Git", "G", "GitHub Skills", "Short interactive courses for GitHub workflows, pull requests, Actions, and collaboration.", "https://skills.github.com/", 17),
            ("ship", "Deploy", "V", "Vercel Docs", "Deploy frontend projects quickly and learn the basics of production hosting.", "https://vercel.com/docs", 24),
            ("ship", "APIs", "P", "Postman Learning", "Learn how to inspect, test, document, and work with APIs.", "https://learning.postman.com/", 15),
            ("ship", "Frontend", "R", "React Learn", "Official React lessons for components, state, events, and building user interfaces.", "https://react.dev/learn", 31),
            ("watch", "YouTube", "T", "take U forward", "DSA explanations, patterns, interview preparation, and problem-solving walkthroughs.", "https://www.youtube.com/@takeUforward", 45),
            ("watch", "YouTube", "C", "CodeWithHarry", "Beginner-friendly programming, web development, Python, JavaScript, and project tutorials.", "https://www.youtube.com/@CodeWithHarry", 62),
            ("watch", "YouTube", "K", "Kunal Kushwaha", "Open source, backend, Java, DevOps, and community-driven developer learning.", "https://www.youtube.com/@kunalkushwaha", 39),
            ("watch", "YouTube", "F", "freeCodeCamp", "Long-form courses on programming, web development, databases, and computer science.", "https://www.youtube.com/@freecodecamp", 33)
        ]
        cursor.executemany("""
            INSERT INTO resources (category, type, icon, title, description, url, likes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, resources)

    conn.commit()

def seed_degree_roadmaps(cursor, conn):
    cursor.execute("SELECT COUNT(*) FROM degrees")
    if cursor.fetchone()[0] > 0:
        return

    degrees = [
        ("btech_cse", "B.Tech CSE", "Computer Science & Engineering", "Core software engineering, algorithms, system design, and placement excellence.", "⚡"),
        ("btech_aiml", "B.Tech AI & ML", "Artificial Intelligence & Machine Learning", "Mathematics for ML, neural networks, computer vision, NLP, and intelligent systems.", "🧠"),
        ("btech_it", "B.Tech IT", "Information Technology", "Enterprise web architectures, cloud engineering, cybersecurity, and databases.", "🌐"),
        ("bca_cs", "BCA / B.Sc CS", "Computer Applications & Science", "Hands-on application development, modern stacks, industry projects, and off-campus preparation.", "💻"),
        ("btech_ece", "B.Tech ECE", "Electronics & Communication", "C/C++, embedded systems, IoT devices, microcontrollers, and hardware-software integration.", "🔌")
    ]
    cursor.executemany("""
        INSERT INTO degrees (id, name, full_title, description, icon)
        VALUES (?, ?, ?, ?, ?)
    """, degrees)

    # Dictionary defining the 8 semesters for each degree
    roadmaps_data = {
        "btech_cse": [
            # Year 1
            (1, 1, "Programming Foundations & The Command Line",
             ["C / C++ Basics", "Linux & Bash", "Git & GitHub", "Engineering Math I"],
             "Calculus, Engineering Physics, Fundamentals of Programming in C/C++, Digital Logic.",
             "Terminal navigation, Git commit workflows, GitHub profile setup, solving 30 problems on HackerRank/LeetCode Easy.",
             "Build a command-line utility or text-based game in C/C++ and push to GitHub.",
             [
                 ("Install VS Code, GCC/Clang, Git, and a Linux environment (WSL or native)", "Code"),
                 ("Master variables, pointers, memory allocation, loops, and functions in C", "Theory"),
                 ("Solve 25 beginner algorithmic problems on LeetCode/HackerRank", "Code"),
                 ("Push your first documented repository to GitHub with a proper README.md", "Ship"),
                 ("Join your college coding club / ACM / IEEE student chapter", "Career")
             ]),
            (1, 2, "Object-Oriented Programming & Web Starters",
             ["OOP Concepts", "Data Structures Basics", "HTML / CSS / JS", "Discrete Mathematics"],
             "Object-Oriented Programming (Java or C++), Discrete Mathematics, Basic Data Structures (Arrays, Strings).",
             "Build interactive browser interfaces, understand DOM manipulation, practice recursion and time complexity analysis.",
             "Participate in your first college 24hr hackathon and build a working web app.",
             [
                 ("Master OOP: Classes, Inheritance, Polymorphism, Encapsulation in C++ or Java", "Theory"),
                 ("Implement dynamic arrays, strings, linear search, and binary search from scratch", "Code"),
                 ("Build a responsive portfolio website with HTML5, CSS3, and JavaScript", "Ship"),
                 ("Form a team of 3-4 peers and register for a fresher hackathon", "Career"),
                 ("Start a consistent problem-solving streak on LeetCode (reach 75 solved)", "Code")
             ]),
            # Year 2
            (2, 3, "Core Data Structures & Backend Fundamentals",
             ["Linear DSA", "Node.js / Express or Python", "Relational Databases & SQL", "Computer Organization"],
             "Data Structures (Linked Lists, Stacks, Queues, Binary Trees), Computer Organization & Architecture, DBMS.",
             "Design relational schemas in PostgreSQL/MySQL, build RESTful APIs with CRUD operations and Postman testing.",
             "Ship a full-stack CRUD application with persistent database and API endpoints.",
             [
                 ("Implement Linked Lists, Stacks, Queues, and Binary Search Trees with traversal logic", "Code"),
                 ("Learn SQL: schema design, foreign keys, normalization, joins, and indexing", "Theory"),
                 ("Build a REST API using Express (Node.js) or FastAPI (Python) connected to PostgreSQL", "Ship"),
                 ("Participate in Codeforces Div 3 / LeetCode Biweekly Contests regularly", "Code"),
                 ("Start writing short technical blogs or LinkedIn posts explaining DSA patterns", "Career")
             ]),
            (2, 4, "Advanced DSA & Operating Systems",
             ["Graphs & Trees", "Operating Systems", "Computer Networks", "Dynamic Programming"],
             "Operating Systems (Processes, Threads, Semaphores, Deadlocks, Memory Management), Computer Networks (OSI, TCP/IP).",
             "Graph algorithms (BFS, DFS, Dijkstra), Dynamic Programming memoization & tabulation, multi-threading in code.",
             "Develop an authenticated full-stack application (JWT auth, database relationships, role-based access).",
             [
                 ("Master Tree traversals, BFS/DFS, Heaps, Priority Queues, and Disjoint Set Union", "Code"),
                 ("Solve the top 20 classic Dynamic Programming problems (Knapsack, LCS, LIS)", "Code"),
                 ("Understand OS internals: process scheduling, virtual memory, paging, and deadlocks", "Theory"),
                 ("Build a web app with user authentication, JWT tokens, and secure passwords", "Ship"),
                 ("Draft your first professional software engineer resume formatted with Overleaf/LaTeX", "Career")
             ]),
            # Year 3
            (3, 5, "Database Internals, Cloud & Open-Source",
             ["Advanced DBMS", "Docker & Containers", "Open-Source / Hackathons", "Software Engineering"],
             "Database Management Systems (ACID, Transactions, Concurrency Control, B+ Trees), Software Engineering Principles.",
             "Containerization with Docker, deploying web applications to cloud (AWS/Vercel/Render), CI/CD pipelines.",
             "Make your first meaningful open-source contribution to a public repository.",
             [
                 ("Containerize a full-stack project using Docker and write a multi-container Docker Compose file", "Ship"),
                 ("Learn ACID properties, transaction isolation levels, and indexing strategies in DBMS", "Theory"),
                 ("Submit your first Pull Request to an open-source GitHub project (Hacktoberfest or OSS orgs)", "Ship"),
                 ("Compete in a national hackathon (Smart India Hackathon, Devfolio circuit, or MLH)", "Career"),
                 ("Reach 250+ DSA problems solved across LeetCode / Striver's SDE Sheet", "Code")
             ]),
            (3, 6, "Low-Level Design, System Design & Summer Internships",
             ["Low-Level Design (LLD)", "High-Level Design (HLD)", "Mock Interviews", "Summer Internship Search"],
             "Design Patterns (Factory, Singleton, Observer, Strategy), Microservices vs Monolith, Cloud Architecture.",
             "UML class diagrams, object-oriented design interviews, caching with Redis, rate limiters, message queues.",
             "Secure an off-campus or on-campus summer internship or research assistantship.",
             [
                 ("Learn SOLID principles and implement classic design patterns in code", "Theory"),
                 ("Practice designing parking lot, Tic-Tac-Toe, and URL shortener in LLD interviews", "Code"),
                 ("Study System Design: DNS, load balancers, caching (Redis), database sharding, CDN", "Theory"),
                 ("Apply to 50+ summer internship openings through LinkedIn, Wellfound, and campus placement drives", "Career"),
                 ("Conduct 5 peer mock technical interviews with timed DSA and behavioral questions", "Career")
             ]),
            # Year 4
            (4, 7, "Placement Drives & Capstone Project Architecture",
             ["Campus Placements", "SDE Interview Sprints", "Capstone Project Phase 1", "Core CS Revision"],
             "Comprehensive revision of DBMS, OS, Computer Networks, OOP, and Aptitude / Quantitative Reasoning.",
             "High-intensity coding test preparation, speed solving, deep-dive project explanations, behavioral leadership answers.",
             "Clear technical rounds and secure full-time SDE job offer(s).",
             [
                 ("Revise top 100 interview questions in Operating Systems, DBMS, and Computer Networks", "Theory"),
                 ("Practice speed coding 2 DSA problems daily under 45 minutes", "Code"),
                 ("Architect and begin building your Major Final Year Capstone Project with modern architecture", "Ship"),
                 ("Attend campus placement drives and apply to off-campus SDE-1 hiring challenges", "Career"),
                 ("Master STAR method for behavioral and leadership interview rounds", "Career")
             ]),
            (4, 8, "Capstone Deployment, Open Source & Career Launch",
             ["Capstone Finalization", "Production Deployment", "Full-Time Transition", "Higher Studies / GATE"],
             "Final Project Defense, Technical Documentation, Software Ethics, Career Launch or Higher Studies (GATE/GRE).",
             "Production-grade deployment, automated tests, monitoring, performance benchmarking, transitioning to industry engineering.",
             "Deploy production capstone with live users, present project defense, and graduate with distinction.",
             [
                 ("Deploy final year capstone project to production with live domain, CI/CD, and monitoring", "Ship"),
                 ("Write comprehensive IEEE/college format project documentation and presentation slides", "Theory"),
                 ("Read clean code principles and industry engineering best practices", "Code"),
                 ("Contribute back to junior tech communities and conduct college fresher mentorship", "Career"),
                 ("Prepare onboarding checklist: salary negotiations, tech stack ramp-up, and career goals", "Career")
             ])
        ],

        "btech_aiml": [
            (1, 1, "Python Mastery & Mathematical Foundations",
             ["Python for Dev", "Linear Algebra", "Linux & Git", "Calculus & Probability"],
             "Linear Algebra (Matrices, Eigenvalues), Multivariable Calculus, Discrete Mathematics, Python Basics.",
             "Python idiomatic scripting, NumPy vectorization, Git version control, setting up Jupyter lab environments.",
             "Build a CLI data analysis script that processes CSV datasets and plots charts.",
             [
                 ("Master modern Python: list comprehensions, generators, decorators, and OOP", "Code"),
                 ("Study Linear Algebra: vectors, matrix transformations, dot products, and eigenvalues", "Theory"),
                 ("Learn NumPy and Pandas for manipulating high-dimensional tabular data", "Code"),
                 ("Build and document a Python data extraction and visualization utility on GitHub", "Ship"),
                 ("Join AI/Data science student communities and Kaggle forums", "Career")
             ]),
            (1, 2, "Exploratory Data Analysis & Scientific Computing",
             ["Pandas & Matplotlib", "Probability & Statistics", "Data Scraping", "Data Structures in Python"],
             "Probability Distributions, Hypothesis Testing, Central Limit Theorem, Data Structures & Algorithms.",
             "Data cleaning, exploratory data analysis (EDA), Seaborn visualizations, web scraping with BeautifulSoup.",
             "Publish a complete Kaggle EDA notebook with clear insights and narrative.",
             [
                 ("Master statistical concepts: mean, variance, Bayes theorem, distributions, p-values", "Theory"),
                 ("Build custom data visualization dashboards using Seaborn and Plotly", "Code"),
                 ("Implement classic search and sorting algorithms in Python", "Code"),
                 ("Complete an end-to-end Exploratory Data Analysis project on a real-world dataset", "Ship"),
                 ("Participate in beginner Kaggle tabular competitions", "Career")
             ]),
            (2, 3, "Classical Machine Learning Algorithms",
             ["Scikit-Learn", "Regression & Classification", "Feature Engineering", "Relational Databases & SQL"],
             "Linear/Logistic Regression, Decision Trees, Random Forests, SVM, k-Means, PCA, SQL for data retrieval.",
             "Model evaluation metrics (ROC-AUC, F1, precision, recall), hyperparameter tuning (GridSearchCV), cross-validation.",
             "Deploy a trained Scikit-Learn prediction model as an interactive Streamlit web app.",
             [
                 ("Derive gradient descent and cost functions mathematically for linear models", "Theory"),
                 ("Train and evaluate models using Scikit-Learn pipelines", "Code"),
                 ("Master SQL queries for data analytics: window functions, aggregations, and subqueries", "Code"),
                 ("Build and deploy an interactive ML web application on Streamlit Cloud", "Ship"),
                 ("Solve 100+ Python DSA questions focusing on arrays, hashing, and trees", "Code")
             ]),
            (2, 4, "Deep Learning Foundations & PyTorch",
             ["PyTorch", "Neural Networks", "Backpropagation", "Computer Vision Basics"],
             "Artificial Neural Networks (ANN), Convolutional Neural Networks (CNN), Optimization (Adam, SGD), Tensor Math.",
             "PyTorch tensor operations, custom DataLoader, training loops, transfer learning with ResNet.",
             "Build and train an image classification model and containerize the inference API.",
             [
                 ("Understand forward pass, backpropagation, and chain rule mathematically", "Theory"),
                 ("Train deep CNNs using PyTorch on GPU (Google Colab / Kaggle)", "Code"),
                 ("Apply data augmentation and transfer learning using torchvision models", "Code"),
                 ("Deploy a computer vision model using FastAPI and Docker", "Ship"),
                 ("Write a detailed blog post breaking down your neural network architecture", "Career")
             ]),
            (3, 5, "Natural Language Processing & Transformers",
             ["Hugging Face", "NLP & Transformers", "Embeddings & Vectors", "MLOps Basics"],
             "Word Embeddings (Word2Vec), Recurrent Networks (LSTM, GRU), Self-Attention Mechanisms, Transformer Architectures.",
             "Fine-tuning BERT and GPT models with Hugging Face Transformers, vector databases (Chroma/Pinecone).",
             "Build a Retrieval-Augmented Generation (RAG) assistant using LangChain/LlamaIndex and Hugging Face.",
             [
                 ("Study Transformer architecture: query, key, value attention equations and multi-head attention", "Theory"),
                 ("Build a document question-answering system using LLM embeddings and vector search", "Ship"),
                 ("Track model training experiments using MLflow or Weights & Biases", "Code"),
                 ("Participate in an AI-focused national hackathon with working prototype", "Career"),
                 ("Reach 200+ DSA problems solved to ensure technical round readiness", "Code")
             ]),
            (3, 6, "MLOps, Scalable AI & Summer Internships",
             ["MLOps Pipelines", "Model Serving & Docker", "System Design for ML", "Summer Internship Drives"],
             "Model monitoring, drift detection, CI/CD for machine learning, scalable inference architecture, data privacy.",
             "Dockerizing AI microservices, Triton/FastAPI serving, caching inference, low-latency prediction pipelines.",
             "Secure an AI/ML Engineer, Data Scientist, or Data Analyst summer internship.",
             [
                 ("Study Machine Learning System Design: streaming vs batch prediction, feature stores, caching", "Theory"),
                 ("Build an automated CI/CD pipeline that retrains and tests model performance", "Ship"),
                 ("Prepare your AI portfolio showcasing 3 distinct end-to-end deployed projects", "Career"),
                 ("Apply to 40+ AI/Data roles at startups and tech firms with custom cover letters", "Career"),
                 ("Conduct mock interviews covering ML theory, math derivations, and coding rounds", "Career")
             ]),
            (4, 7, "Generative AI, Large Models & Placement Drives",
             ["Generative AI", "Agentic Workflows", "Campus Placements", "Major AI Capstone Phase 1"],
             "Fine-tuning techniques (LoRA, QLoRA), Reinforcement Learning from Human Feedback (RLHF), Placement Prep.",
             "Prompt engineering, multi-agent architectures (CrewAI, LangGraph), high-throughput inference optimization.",
             "Clear campus placement or off-campus technical rounds for Machine Learning roles.",
             [
                 ("Learn parameter-efficient fine-tuning (PEFT/LoRA) on custom datasets", "Theory"),
                 ("Implement an autonomous AI agent workflow solving multi-step tasks", "Ship"),
                 ("Revise core computer science: OS, DBMS, SQL, and algorithms for placement interviews", "Theory"),
                 ("Participate actively in placement hiring tests and coding rounds", "Career"),
                 ("Scope out your final year AI research capstone project with measurable benchmarks", "Ship")
             ]),
            (4, 8, "Research Publication, Capstone Deployment & Career Launch",
             ["AI Capstone Defense", "Research Paper", "Production Deployment", "Full-Time Transition"],
             "Model explainability (SHAP, LIME), AI Safety & Ethics, Research Paper Writing, Career Launch.",
             "Deploying large models to cloud endpoints, cost optimization, latency quantization (ONNX, TensorRT).",
             "Complete final capstone defense, publish research or release open-weights model, and launch career.",
             [
                 ("Complete production deployment of Capstone AI system with user metrics and monitoring", "Ship"),
                 ("Draft and submit a research paper to a recognized conference or arXiv preprint", "Theory"),
                 ("Document your model weights, dataset cards, and demo on Hugging Face Spaces", "Ship"),
                 ("Mentor 1st and 2nd year students on AI roadmaps and hackathons", "Career"),
                 ("Ramp up on your hiring company's production tech stack before day one", "Career")
             ])
        ],

        "btech_it": [
            (1, 1, "IT Foundations, Scripting & Terminal",
             ["C / Python", "Linux System Administration", "Git & GitHub", "Web Architecture"],
             "Fundamentals of Programming, Discrete Mathematics, Computer Hardware & Peripherals.",
             "Bash scripting, Linux permissions, package management, Git workflows, HTTP protocol fundamentals.",
             "Write a bash automation script that backups directories and monitors system resources.",
             [
                 ("Set up a dual-boot or virtualized Linux development environment", "Code"),
                 ("Master C or Python programming fundamentals: control flow, functions, memory", "Theory"),
                 ("Write 5 useful shell scripts for automating local workstation tasks", "Ship"),
                 ("Push clean code to GitHub and write markdown documentation", "Ship"),
                 ("Join IT student chapters and attend cybersecurity / web workshops", "Career")
             ]),
            (1, 2, "Modern Web Development & Networking Basics",
             ["HTML5 / CSS3 / JavaScript", "Computer Networks Basics", "OOP in Java", "Data Structures"],
             "Object-Oriented Programming (Java), Data Structures (Arrays, Lists, Stacks), Network Topologies.",
             "Semantic HTML, Flexbox/Grid CSS, JavaScript asynchronous programming (Promises, async/await).",
             "Build a responsive web application that fetches data from public REST APIs.",
             [
                 ("Master OOP principles and write modular Java code", "Theory"),
                 ("Learn Network basics: IP addresses, subnetting, DNS, TCP vs UDP", "Theory"),
                 ("Build a responsive multi-page web application with API integrations", "Ship"),
                 ("Solve 50 coding problems focusing on string and array manipulation", "Code"),
                 ("Compete in your first 24-hour campus hackathon", "Career")
             ]),
            (2, 3, "Enterprise Databases & Backend Engineering",
             ["SQL & Relational DBs", "Node.js / Express or Django", "Non-Linear DSA", "Software Engineering"],
             "Database Management Systems, Software Engineering Methodologies (Agile, Scrum), Data Structures (Trees, Queues).",
             "Relational database design, 3NF normalization, RESTful API architecture, postman automation tests.",
             "Design and build an enterprise-grade inventory or ticketing backend system.",
             [
                 ("Implement Tree and Graph data structures and traversal algorithms", "Code"),
                 ("Write complex SQL queries: joins, group by, transactions, and store procedures", "Theory"),
                 ("Build a robust backend API with role-based access control and database persistence", "Ship"),
                 ("Participate in competitive programming contests on LeetCode/HackerEarth", "Code"),
                 ("Document API endpoints with Swagger / OpenAPI specifications", "Ship")
             ]),
            (2, 4, "Operating Systems, Cloud Basics & DevOps",
             ["Linux Administration", "Operating Systems", "AWS / Cloud Basics", "Docker Containers"],
             "Operating Systems (Virtual Memory, Scheduling, Deadlocks), Cloud Computing Fundamentals.",
             "Deploying virtual machines on AWS EC2, S3 bucket management, Docker containerization, reverse proxies (Nginx).",
             "Deploy a containerized web application behind an Nginx reverse proxy on a cloud VPS.",
             [
                 ("Study OS core concepts: process synchronization, memory paging, and file systems", "Theory"),
                 ("Learn Docker: write Dockerfiles, manage volumes, and configure container networks", "Code"),
                 ("Launch a cloud instance on AWS/GCP, configure security groups and deploy an app", "Ship"),
                 ("Solve 50 intermediate DSA problems on Dynamic Programming and Graphs", "Code"),
                 ("Update your tech resume with live deployed project URLs", "Career")
             ]),
            (3, 5, "Cloud Architecture, CI/CD & Cybersecurity",
             ["CI/CD Pipelines", "Information Security", "Microservices", "Advanced Databases (NoSQL)"],
             "Information Security & Cryptography, Web Application Vulnerabilities (OWASP Top 10), Distributed Systems.",
             "GitHub Actions CI/CD pipelines, MongoDB/Redis integration, securing web apps with HTTPS/CORS, penetration testing basics.",
             "Build an automated CI/CD pipeline that tests, builds, and deploys your code on git push.",
             [
                 ("Implement automated testing and deployment using GitHub Actions", "Ship"),
                 ("Study cryptography: symmetric/asymmetric encryption, hashing, SSL/TLS certificates", "Theory"),
                 ("Audit a web application for OWASP Top 10 vulnerabilities (XSS, SQLi, CSRF)", "Code"),
                 ("Integrate Redis caching to speed up high-latency database queries", "Ship"),
                 ("Compete in a national hackathon focusing on cloud or security", "Career")
             ]),
            (3, 6, "System Design, Infrastructure & Summer Internships",
             ["System Design (HLD)", "Kubernetes Basics", "Mock Interviews", "Summer Internship Drives"],
             "High-Level System Design, Load Balancing, Microservices Communication, Reliability Engineering.",
             "Designing scalable architectures: messaging queues (RabbitMQ/Kafka), caching layers, database replication.",
             "Secure an IT, Cloud Engineer, DevOps, or Software Engineering summer internship.",
             [
                 ("Learn System Design fundamentals: horizontal scaling, CDN, database replication", "Theory"),
                 ("Practice designing scalable platforms: Netflix, WhatsApp, or E-commerce backend", "Code"),
                 ("Learn basic Kubernetes concepts: pods, deployments, services, and ingress", "Theory"),
                 ("Apply to 50+ IT/Software/DevOps internship openings across industry channels", "Career"),
                 ("Take mock technical interviews on core networking, OS, and algorithms", "Career")
             ]),
            (4, 7, "Campus Placements, Enterprise Systems & Capstone Phase 1",
             ["Campus Placements", "Core IT Revision", "Major Capstone Project", "Interview Preparation"],
             "Full revision of Computer Networks, DBMS, OS, Cloud Services, and Quantitative Aptitude.",
             "Technical interview sprints, architectural deep dives, behavioral questions, coding problem solving.",
             "Clear on-campus or off-campus recruitment drives for high-paying engineering roles.",
             [
                 ("Revise high-yield questions in Computer Networks, SQL, OS, and System Design", "Theory"),
                 ("Solve 2 interview DSA problems daily under timed constraints", "Code"),
                 ("Begin implementing your Major IT Capstone project with cloud infrastructure", "Ship"),
                 ("Attend placement coding assessments and technical interviews", "Career"),
                 ("Master answers for behavioral, situational, and conflict resolution rounds", "Career")
             ]),
            (4, 8, "Capstone Deployment, Industry Certification & Career Launch",
             ["Capstone Defense", "Cloud Certification", "Production Rollout", "Career Transition"],
             "Capstone Project Evaluation, Enterprise Architecture, Software Maintenance, Professional Ethics.",
             "Full production monitoring with Prometheus/Grafana, cloud certification prep (AWS Solutions Architect / Cloud Practitioner).",
             "Present final capstone defense, earn an industry cloud credential, and onboard into full-time role.",
             [
                 ("Complete production deployment of your Capstone system with uptime monitoring", "Ship"),
                 ("Prepare for and complete an AWS Certified Cloud Practitioner or Solutions Architect exam", "Career"),
                 ("Write comprehensive technical handover and system architecture documentation", "Theory"),
                 ("Mentor junior students on cloud computing, DevOps, and placements", "Career"),
                 ("Prepare transition plan for corporate engineering onboarding", "Career")
             ])
        ],

        "bca_cs": [
            (1, 1, "Programming Fundamentals in C & Office Tools",
             ["C Language", "Computer Fundamentals", "Git Basics", "Mathematical Foundations"],
             "Computer Fundamentals, Programming in C, Problem Solving Techniques, Communication Skills.",
             "Writing clean C programs, algorithm flowcharts, setting up code editors, creating a GitHub account.",
             "Build a student report card or billing management CLI program in C.",
             [
                 ("Install code editor and learn C syntax: data types, loops, arrays, pointers", "Code"),
                 ("Understand computer architecture: CPU, memory, storage, and binary arithmetic", "Theory"),
                 ("Build a menu-driven console application in C with file storage", "Ship"),
                 ("Create your GitHub account and push your first project", "Ship"),
                 ("Focus on developing strong English communication and technical vocabulary", "Career")
             ]),
            (1, 2, "Object-Oriented Programming in C++ & Web Design",
             ["C++ / OOP", "HTML & CSS", "JavaScript Basics", "Data Structures Intro"],
             "Object-Oriented Programming with C++, Web Technology Basics, Basic Data Structures.",
             "C++ classes, objects, constructors, file handling, creating styled landing pages with HTML/CSS.",
             "Design and deploy an interactive multi-page portfolio website on GitHub Pages.",
             [
                 ("Master C++ OOP: inheritance, function overloading, polymorphism", "Theory"),
                 ("Learn HTML5 semantic tags and modern CSS styling with Flexbox", "Code"),
                 ("Add JavaScript interactivity for form validation and dynamic UI", "Code"),
                 ("Deploy your personal portfolio on GitHub Pages for free", "Ship"),
                 ("Solve 30 beginner coding problems on HackerRank", "Code")
             ]),
            (2, 3, "Data Structures, Java & Relational Databases",
             ["Java Programming", "Data Structures", "DBMS & SQL", "Web Scripting"],
             "Core Java (Packages, Exceptions, Collections), Data Structures (Lists, Stacks, Queues), DBMS.",
             "Java Swing/JavaFX or web app development, writing relational SQL queries, table normalization.",
             "Build a desktop or web-based inventory/library management system with database connection.",
             [
                 ("Master Core Java: OOP, interfaces, exception handling, and ArrayLists", "Theory"),
                 ("Implement stacks, queues, and linked lists in Java", "Code"),
                 ("Learn SQL: CREATE, INSERT, SELECT, JOIN, and database constraints", "Code"),
                 ("Build a complete database-backed application connected via JDBC or backend API", "Ship"),
                 ("Participate in online coding challenges on LeetCode or GeeksforGeeks", "Career")
             ]),
            (2, 4, "Full-Stack Web Development & Operating Systems",
             ["Node.js & Express", "MongoDB / NoSQL", "Operating Systems", "React Basics"],
             "Operating Systems (Processes, Memory, File Systems), Web Frameworks, Database Systems.",
             "Building RESTful APIs with Node.js and Express, connecting to MongoDB, building React UI components.",
             "Create and deploy a full-stack MERN (MongoDB, Express, React, Node) application.",
             [
                 ("Study Operating System concepts: multitasking, memory management, file systems", "Theory"),
                 ("Build backend REST APIs with Express and test them with Postman", "Code"),
                 ("Learn React fundamentals: components, props, state, and useEffect", "Code"),
                 ("Deploy full-stack project with frontend on Vercel and backend on Render", "Ship"),
                 ("Create an updated resume highlighting live project links and GitHub repo", "Career")
             ]),
            (3, 5, "Python, Advanced Web & Internship Preparation",
             ["Python for Dev", "Advanced React / Next.js", "Software Testing", "Internship Drives"],
             "Python Programming, Software Engineering & Testing Methodologies, Cloud Fundamentals.",
             "Modern frontend architectures, state management, building full-stack applications with Python or JavaScript.",
             "Secure an off-campus web development, QA, or software engineering internship.",
             [
                 ("Learn Python scripting, dictionary/list operations, and utility libraries", "Code"),
                 ("Build an e-commerce or social media web application with search and filter features", "Ship"),
                 ("Study software testing: unit tests, manual testing, test case documentation", "Theory"),
                 ("Apply to 30+ internship opportunities on Internshala, Wellfound, and LinkedIn", "Career"),
                 ("Practice 100+ DSA interview questions on arrays, strings, and trees", "Code")
             ]),
            (3, 6, "MCA / Placement Prep & Final Capstone Project",
             ["Full-Time Job Search", "MCA Entrances (NIMCET) / Placements", "Capstone Project", "System Fundamentals"],
             "Final Year Project Development, Core Computer Science Revision, Placement Preparation or MCA Entrance Prep.",
             "Interview preparation, speed coding, mock technical interviews, deploying production capstone project.",
             "Graduate with a placed job offer or top rank in MCA entrance examination.",
             [
                 ("Complete and polish your final year capstone project with clean code and documentation", "Ship"),
                 ("If pursuing jobs: practice coding rounds, aptitude tests, and HR interview answers", "Career"),
                 ("If pursuing MCA: solve NIMCET / state entrance exam previous year papers", "Theory"),
                 ("Conduct mock interviews with peers focusing on project explanations", "Career"),
                 ("Deploy all major projects to live URLs and ensure GitHub profile is polished", "Ship")
             ]),
            # For 4-year degree consistency (BCA Honours / B.Sc 4-year NEP format)
            (4, 7, "Advanced Software Engineering & Enterprise Stacks",
             ["Enterprise Java / Spring Boot", "Cloud Deployment", "Placement Sprints", "Capstone Phase 1"],
             "Enterprise Application Development, Cloud Architecture, Advanced Data Analytics.",
             "Spring Boot or Django enterprise frameworks, microservices architecture, cloud deployment.",
             "Build and deploy an enterprise-grade service with automated test coverage.",
             [
                 ("Learn Spring Boot or Django for enterprise-grade backend development", "Code"),
                 ("Implement authentication, payment gateway integration, and email notifications", "Ship"),
                 ("Revise DBMS, Operating Systems, and Networks for high-tier company interviews", "Theory"),
                 ("Participate in off-campus hiring drives and tech challenges", "Career"),
                 ("Solve 2 medium LeetCode problems daily", "Code")
             ]),
            (4, 8, "Major Capstone Defense & Industry Launch",
             ["Capstone Defense", "Production Architecture", "Full-Time Transition", "Career Launch"],
             "Capstone Evaluation, Software Architecture, Industry Practices, Career Launch.",
             "CI/CD automation, production monitoring, scalable database queries, full-time engineering onboarding.",
             "Present final capstone defense, receive bachelor degree, and commence engineering career.",
             [
                 ("Deploy production-grade capstone project with live user traffic and monitoring", "Ship"),
                 ("Complete technical documentation and slide deck for final jury defense", "Theory"),
                 ("Network with alumni and industry professionals on LinkedIn", "Career"),
                 ("Review employment contracts, offer letters, and corporate expectations", "Career"),
                 ("Celebrate your journey from fresher to full-stack engineer", "Career")
             ])
        ],

        "btech_ece": [
            (1, 1, "C Programming & Electronic Circuits Foundations",
             ["C Language", "Basic Electronics", "Engineering Math", "Git & Linux"],
             "Network Analysis, Electronic Devices & Circuits, Programming for Problem Solving (C), Calculus.",
             "Writing C programs, breadboard circuit prototyping, using multimeters/oscilloscopes, Git version control.",
             "Simulate basic diode and transistor circuits and write a C calculation utility.",
             [
                 ("Master C syntax, bitwise operations, memory layout, and pointer arithmetic", "Code"),
                 ("Understand electronic components: resistors, capacitors, diodes, and transistors", "Theory"),
                 ("Set up a Linux development environment and learn terminal commands", "Code"),
                 ("Simulate analog circuits using LTspice or Proteus", "Ship"),
                 ("Join your college IEEE, Robotics, or Electronics club", "Career")
             ]),
            (1, 2, "Digital Electronics & Python for Engineers",
             ["Digital Logic", "Python Programming", "Microcontroller Basics", "Signals & Systems"],
             "Digital System Design (Logic Gates, Flip-Flops, Combinational & Sequential Circuits), Signals & Systems.",
             "Python scripting for hardware automation, logic gate minimization with Karnaugh maps, Arduino starters.",
             "Build your first Arduino sensor project (temperature/motion detection with display).",
             [
                 ("Master logic gates, boolean algebra, multiplexers, and flip-flops", "Theory"),
                 ("Learn Python programming for data plotting and serial communication", "Code"),
                 ("Program an Arduino or ESP32 microcontroller using C/C++", "Ship"),
                 ("Read sensor data (DHT11/Ultrasonic) and display output on LCD/OLED", "Ship"),
                 ("Participate in a college hardware/IoT hackathon", "Career")
             ]),
            (2, 3, "Embedded C & Microcontroller Architecture",
             ["Embedded C", "Microcontrollers (8051 / ARM)", "Data Structures in C", "Analog Communication"],
             "Microprocessor & Microcontroller Architecture (8051 / ARM Cortex-M), Analog Communication, Data Structures.",
             "Embedded C programming: register manipulation, timers, interrupts, UART/SPI/I2C communication protocols.",
             "Build a multi-sensor IoT node communicating over UART/I2C protocols.",
             [
                 ("Implement arrays, linked lists, and circular queues in C for embedded systems", "Code"),
                 ("Learn microcontroller registers, GPIO pins, and interrupt service routines (ISR)", "Theory"),
                 ("Interface multiple peripherals using I2C and SPI protocols on STM32 / ESP32", "Ship"),
                 ("Solve 50 coding problems in C/C++ on algorithmic logic", "Code"),
                 ("Start designing circuit schematics using KiCad or EasyEDA", "Ship")
             ]),
            (2, 4, "PCB Design, IoT & Operating Systems",
             ["KiCad PCB Design", "ESP32 & Wi-Fi/BLE", "Real-Time OS (RTOS)", "Operating Systems"],
             "Linear Integrated Circuits (Op-Amps), Digital Signal Processing (DSP) intro, Operating Systems.",
             "Custom PCB schematic and board layout in KiCad, FreeRTOS task scheduling, MQTT/HTTP IoT telemetry.",
             "Design, fabricate, and assemble your own custom IoT PCB board.",
             [
                 ("Design a custom circuit schematic and 2-layer PCB layout in KiCad", "Ship"),
                 ("Learn FreeRTOS: tasks, queues, semaphores, and mutexes on microcontrollers", "Theory"),
                 ("Connect ESP32 to cloud MQTT brokers (AWS IoT Core / HiveMQ) for telemetry", "Ship"),
                 ("Study operating systems: process scheduling, memory management, and concurrency", "Theory"),
                 ("Update your engineering portfolio with high-resolution photos of your PCBs", "Career")
             ]),
            (3, 5, "FPGA, Verilog HDL & Computer Networks",
             ["Verilog HDL", "FPGA Programming", "Computer Networks", "DSA for Embedded"],
             "Digital VLSI Design, Verilog Hardware Description Language, Computer Networks (TCP/IP, Ethernet, CAN).",
             "Writing synthesizable Verilog, FPGA simulation with ModelSim/Vivado, CAN bus in automotive systems.",
             "Implement a state machine or digital ALU processor on an FPGA development board.",
             [
                 ("Learn Verilog syntax: modules, always blocks, blocking vs non-blocking assignments", "Code"),
                 ("Simulate and test digital circuits with testbenches in ModelSim/Vivado", "Theory"),
                 ("Implement an SPI/UART master controller in Verilog on an FPGA", "Ship"),
                 ("Study Computer Networks: OSI model, TCP/IP, sockets, and industrial buses (CAN, RS-485)", "Theory"),
                 ("Solve 150+ DSA problems in C++ for core embedded firmware interview rounds", "Code")
             ]),
            (3, 6, "Firmware Development & Core Hardware Internships",
             ["Embedded Linux", "Firmware Architecture", "System Design for IoT", "Core ECE Internships"],
             "Embedded Linux (Yocto/Buildroot), Wireless Communication (BLE, Zigbee, LoRa), Hardware System Design.",
             "Writing Linux device drivers, kernel compiling, low-power optimization, memory-constrained design.",
             "Secure a core firmware, embedded software, or IoT engineering summer internship.",
             [
                 ("Build custom Linux kernel images for Raspberry Pi or BeagleBone", "Ship"),
                 ("Practice embedded interview questions: volatile keyword, bit masking, memory leaks", "Theory"),
                 ("Implement low-power sleep modes and battery monitoring in battery-powered devices", "Ship"),
                 ("Apply to 40+ hardware/embedded/semiconductor firms (Texas Instruments, Qualcomm, ST, Bosch)", "Career"),
                 ("Conduct mock technical interviews covering C pointers, microcontroller architecture, and circuits", "Career")
             ]),
            (4, 7, "Core Placement Sprints & Capstone Hardware Phase 1",
             ["Hardware / Embedded Placements", "Digital Electronics Revision", "Capstone Phase 1", "Interview Prep"],
             "Comprehensive revision of C/C++, Embedded Systems, Digital Electronics, Microprocessors, and Aptitude.",
             "Placement tests for semiconductor, automotive, consumer electronics, and software companies.",
             "Clear core technical interview rounds and receive job offer in embedded or semiconductor field.",
             [
                 ("Revise high-yield topics in Embedded C, pointer arithmetic, and microcontrollers", "Theory"),
                 ("Practice speed coding for technical rounds in C/C++", "Code"),
                 ("Architect and order components for your Major Final Year Hardware Capstone Project", "Ship"),
                 ("Attend on-campus placement drives for core electronics and software profiles", "Career"),
                 ("Prepare crisp explanations for all personal hardware and firmware projects", "Career")
             ]),
            (4, 8, "Capstone Testing, Defense & Industry Onboarding",
             ["Capstone Hardware Defense", "EMC / FCC Testing", "Firmware Hardening", "Career Launch"],
             "Major Project Evaluation, Embedded Security & Secure Boot, Product Compliance, Professional Ethics.",
             "Hardware debugging, firmware OTA updates, automated hardware-in-the-loop (HIL) testing, career onboarding.",
             "Complete final hardware capstone demonstration, pass project jury defense, and launch engineering career.",
             [
                 ("Complete working hardware enclosure, power supply, and firmware for capstone project", "Ship"),
                 ("Implement secure Over-The-Air (OTA) firmware update mechanism", "Ship"),
                 ("Write comprehensive engineering thesis and presentation for final capstone defense", "Theory"),
                 ("Conduct mentor sessions for junior robotics and electronics club members", "Career"),
                 ("Prepare transition checklist for joining embedded software / semiconductor industry", "Career")
             ])
        ]
    }

    for deg_id, sems in roadmaps_data.items():
        for sem in sems:
            year, sem_num, title, focus, academic, industry, milestone, tasks = sem
            sem_id = f"{deg_id}-sem-{sem_num}"
            cursor.execute("""
                INSERT INTO roadmap_semesters (id, degree_id, year, semester_number, title, focus_areas, academic_core, industry_prep, milestone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sem_id,
                deg_id,
                year,
                sem_num,
                title,
                json.dumps(focus),
                academic,
                industry,
                milestone
            ))

            for idx, task_data in enumerate(tasks):
                task_text, category = task_data
                task_id = f"{sem_id}-task-{idx}"
                cursor.execute("""
                    INSERT INTO roadmap_tasks (id, semester_id, task_order, task_text, category)
                    VALUES (?, ?, ?, ?, ?)
                """, (task_id, sem_id, idx + 1, task_text, category))

    conn.commit()

# --- Database Helper Functions ---

def get_all_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events ORDER BY start_date ASC")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r["id"],
            "name": r["name"],
            "organizer": r["organizer"],
            "city": r["city"],
            "mode": r["mode"],
            "start": r["start_date"],
            "end": r["end_date"],
            "tags": json.loads(r["tags"]),
            "note": r["note"],
            "url": r["url"]
        })
    return result

def add_event(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    event_id = data.get("id")
    if not event_id:
        import re
        event_id = re.sub(r'[^a-zA-Z0-9]', '-', data.get("name", "event")).lower().strip('-')
        cursor.execute("SELECT id FROM events WHERE id = ?", (event_id,))
        if cursor.fetchone():
            event_id = f"{event_id}-{int(datetime.now().timestamp())}"

    tags = data.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    cursor.execute("""
        INSERT INTO events (id, name, organizer, city, mode, start_date, end_date, tags, note, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_id,
        data.get("name"),
        data.get("organizer", "Independent"),
        data.get("city", "Online"),
        data.get("mode", "Online"),
        data.get("start"),
        data.get("end"),
        json.dumps(tags),
        data.get("note", ""),
        data.get("url", "#")
    ))
    conn.commit()
    conn.close()
    return event_id

def get_saved_event_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT event_id FROM saved_events")
    rows = cursor.fetchall()
    conn.close()
    return [r["event_id"] for r in rows]

def toggle_saved_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT event_id FROM saved_events WHERE event_id = ?", (event_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM saved_events WHERE event_id = ?", (event_id,))
        saved = False
    else:
        cursor.execute("INSERT INTO saved_events (event_id) VALUES (?)", (event_id,))
        saved = True
    conn.commit()
    conn.close()
    return saved

def get_all_resources(category=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if category and category != "all":
        cursor.execute("SELECT * FROM resources WHERE category = ? ORDER BY id ASC", (category,))
    else:
        cursor.execute("SELECT * FROM resources ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def like_resource(resource_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE resources SET likes = likes + 1 WHERE id = ?", (resource_id,))
    conn.commit()
    cursor.execute("SELECT likes FROM resources WHERE id = ?", (resource_id,))
    row = cursor.fetchone()
    conn.close()
    return row["likes"] if row else 0

# --- Degree & Semester Roadmap Helpers ---

def get_degrees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM degrees")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_degree_roadmap(degree_id="btech_cse", semester_num=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verify degree
    cursor.execute("SELECT * FROM degrees WHERE id = ?", (degree_id,))
    degree_row = cursor.fetchone()
    if not degree_row:
        degree_id = "btech_cse"
        cursor.execute("SELECT * FROM degrees WHERE id = ?", (degree_id,))
        degree_row = cursor.fetchone()

    degree_info = dict(degree_row)

    # Fetch all semesters for degree
    cursor.execute("""
        SELECT * FROM roadmap_semesters
        WHERE degree_id = ?
        ORDER BY semester_number ASC
    """, (degree_id,))
    semester_rows = cursor.fetchall()

    # Fetch all tasks for this degree's semesters
    cursor.execute("""
        SELECT t.*, rs.degree_id, rs.semester_number
        FROM roadmap_tasks t
        JOIN roadmap_semesters rs ON t.semester_id = rs.id
        WHERE rs.degree_id = ?
        ORDER BY t.task_order ASC
    """, (degree_id,))
    all_tasks = cursor.fetchall()

    # Fetch progress
    cursor.execute("SELECT task_id, completed FROM user_progress")
    progress_rows = cursor.fetchall()
    progress_map = {r["task_id"]: bool(r["completed"]) for r in progress_rows}

    conn.close()

    # Map tasks into semesters
    semesters = []
    total_degree_tasks = len(all_tasks)
    completed_degree_tasks = sum(1 for t in all_tasks if progress_map.get(t["id"], False))

    for s_row in semester_rows:
        sem_tasks = []
        for t in all_tasks:
            if t["semester_id"] == s_row["id"]:
                sem_tasks.append({
                    "id": t["id"],
                    "order": t["task_order"],
                    "text": t["task_text"],
                    "category": t["category"],
                    "completed": progress_map.get(t["id"], False)
                })

        sem_completed = sum(1 for st in sem_tasks if st["completed"])
        sem_total = len(sem_tasks)
        sem_percent = round((sem_completed / sem_total * 100)) if sem_total > 0 else 0

        semesters.append({
            "id": s_row["id"],
            "year": s_row["year"],
            "semester_number": s_row["semester_number"],
            "title": s_row["title"],
            "focus_areas": json.loads(s_row["focus_areas"]),
            "academic_core": s_row["academic_core"],
            "industry_prep": s_row["industry_prep"],
            "milestone": s_row["milestone"],
            "tasks": sem_tasks,
            "tasks_count": sem_total,
            "completed_count": sem_completed,
            "progress_percent": sem_percent
        })

    overall_progress = round((completed_degree_tasks / total_degree_tasks * 100)) if total_degree_tasks > 0 else 0

    # If specific semester requested, find it
    active_semester = None
    if semester_num:
        try:
            s_num = int(semester_num)
            for sem in semesters:
                if sem["semester_number"] == s_num:
                    active_semester = sem
                    break
        except ValueError:
            pass

    if not active_semester and semesters:
        active_semester = semesters[0]

    return {
        "degree": degree_info,
        "semesters": semesters,
        "active_semester": active_semester,
        "overall_stats": {
            "total_tasks": total_degree_tasks,
            "completed_tasks": completed_degree_tasks,
            "progress_percent": overall_progress
        }
    }

def toggle_task(task_id, completed=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM user_progress WHERE task_id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
        new_val = True if completed is None else bool(completed)
        cursor.execute("INSERT INTO user_progress (task_id, completed) VALUES (?, ?)", (task_id, 1 if new_val else 0))
    else:
        new_val = (not row["completed"]) if completed is None else bool(completed)
        cursor.execute("UPDATE user_progress SET completed = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?", (1 if new_val else 0, task_id))

    conn.commit()
    conn.close()
    return new_val

def set_user_preference(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_preferences (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (key, str(value)))
    conn.commit()
    conn.close()

def get_user_preferences():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM user_preferences")
    rows = cursor.fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}

def get_stats(degree_id="btech_cse"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM saved_events")
    saved_count = cursor.fetchone()[0]

    conn.close()

    degree_data = get_degree_roadmap(degree_id)
    overall_stats = degree_data["overall_stats"]

    return {
        "total_events": total_events,
        "saved_count": saved_count,
        "total_tasks": overall_stats["total_tasks"],
        "completed_tasks": overall_stats["completed_tasks"],
        "progress_percent": overall_stats["progress_percent"],
        "degree_id": degree_id
    }

# --- Squad Up (Hackathon Teammate Finder) Operations ---

def seed_squad_posts(cursor, conn):
    cursor.execute("SELECT COUNT(*) FROM squad_posts")
    if cursor.fetchone()[0] > 0:
        return

    squads = [
        (
            "squad-medlens-ai",
            "smart-india-hackathon",
            "Smart India Hackathon 2026",
            "MedLens AI: Early Diabetic Retinopathy Screening for Rural Clinics",
            "Arjun Verma",
            "RVCE Bengaluru (Sem 5)",
            json.dumps(["Frontend (React / Tailwind)", "UI/UX Designer"]),
            2,
            4,
            json.dumps(["PyTorch", "FastAPI", "Next.js", "TailwindCSS"]),
            "Building a lightweight fundus camera image classifier using MobileNetV3 and Gemini Flash for primary healthcare workers in rural PHCs. Core computer vision pipeline is 80% finished. We urgently need a solid frontend builder to craft the clinician dashboard and a designer for smooth patient onboarding.",
            "Discord",
            "arjun_v#9841",
            "Open",
            "2026-09-08 14:30:00"
        ),
        (
            "squad-defi-crop",
            "ethindia-2026",
            "ETHIndia Web3 Summit",
            "AgriShield: Parametric Rainfall Crop Insurance on L2",
            "Neha R.",
            "IIT Roorkee (Sem 6)",
            json.dumps(["Web3 / Smart Contracts", "Backend (Node.js / Express)"]),
            2,
            4,
            json.dumps(["Solidity", "Hardhat", "Chainlink", "Next.js", "Polygon"]),
            "Parametric automated payouts for smallholder farmers triggered when local rainfall drops below threshold. Using Chainlink Functions with IMD weather APIs. Need a Solidity dev to harden the escrow contract and a backend engineer to handle webhook alerts and satellite data.",
            "LinkedIn",
            "https://linkedin.com/in/neha-dev",
            "Open",
            "2026-09-09 11:20:00"
        ),
        (
            "squad-campus-bite",
            "innohacks",
            "Innohacks 4.0",
            "CampusBite: Real-Time Surplus Hostel Food Redistribution App",
            "Karan Patel",
            "KIET Ghaziabad (Sem 3)",
            json.dumps(["Mobile (Flutter)", "Backend (Python / FastAPI)"]),
            2,
            3,
            json.dumps(["Flutter", "FastAPI", "PostgreSQL", "Google Maps API"]),
            "Connecting college mess dining halls with nearby shelters and day scholars when extra food is available at closing hours. Figma wireframes and database schemas are done! Looking for a Flutter enthusiast to build the clean mobile interface and GPS delivery tracking.",
            "Telegram",
            "@karan_kiet",
            "Open",
            "2026-09-10 18:45:00"
        ),
        (
            "squad-neuro-scribe",
            "hackoverflow-3",
            "HackOverflow 3.0",
            "NeuroScribe: Real-Time Hinglish Lecture Speech-to-Markdown Notes",
            "Siddharth Nair",
            "COEP Tech Pune (Sem 4)",
            json.dumps(["AI / ML (Whisper / LLM)", "Frontend (React / Canvas)"]),
            3,
            4,
            json.dumps(["Whisper API", "FastAPI", "React", "ChromaDB", "WebSockets"]),
            "Optimizing real-time acoustic transcription for Indian college classrooms (mixed Hindi-English / technical jargon) that auto-generates structured Markdown study notes and flashcards. Looking for someone experienced with WebSockets or low-latency audio streaming.",
            "Discord",
            "sid_nair#2049",
            "Open",
            "2026-09-11 09:15:00"
        ),
        (
            "squad-cybershield",
            "cognition-gamejam",
            "Cognition CyberSprint",
            "ScamSentry: On-Device Real-Time Phishing & Deepfake Audio Guard",
            "Ananya Iyer",
            "SRM University Chennai (Sem 5)",
            json.dumps(["Android (Kotlin)", "UI/UX Designer"]),
            1,
            3,
            json.dumps(["Kotlin", "Android SDK", "TFLite", "Firebase"]),
            "An on-device background service that flags suspicious AI voice clones and impersonation patterns on WhatsApp audio calls to protect elderly parents and senior citizens. Looking for a passionate Android developer who understands background services and audio buffers.",
            "Email",
            "ananya.iyer.dev@gmail.com",
            "Open",
            "2026-09-11 16:00:00"
        ),
        (
            "squad-codex-visualizer",
            "binary-hacks",
            "Binary Hacks 4.0",
            "Algorhythm: 3D Interactive Data Structure & Graph Visualizer for Freshers",
            "Rohit Deshmukh",
            "VIT Vellore (Sem 3)",
            json.dumps(["Three.js / WebGL", "Frontend (React)"]),
            2,
            3,
            json.dumps(["Three.js", "React", "TypeScript", "TailwindCSS"]),
            "Making complex dynamic programming state transitions, B-Trees, and Dijkstra graphs intuitively understandable through interactive 3D spatial simulations in the browser. Looking for a creative WebGL or Three.js developer.",
            "Discord",
            "rohit_desh#8812",
            "Open",
            "2026-09-12 10:30:00"
        )
    ]

    cursor.executemany("""
        INSERT INTO squad_posts (
            id, hackathon_id, hackathon_name, project_title, leader_name,
            leader_college, roles_needed, current_members, team_size,
            tech_stack, description, contact_type, contact_value, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, squads)
    conn.commit()

def get_all_squads(role_filter=None, hackathon_filter=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM squad_posts WHERE 1=1"
    params = []

    if hackathon_filter and hackathon_filter.lower() != "all":
        query += " AND (LOWER(hackathon_id) LIKE ? OR LOWER(hackathon_name) LIKE ?)"
        pattern = f"%{hackathon_filter.lower()}%"
        params.extend([pattern, pattern])

    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        roles_needed = json.loads(r["roles_needed"]) if r["roles_needed"] else []
        tech_stack = json.loads(r["tech_stack"]) if r["tech_stack"] else []

        if role_filter and role_filter.lower() != "all":
            # Match if any role contains the role_filter term
            rf = role_filter.lower()
            if not any(rf in role.lower() for role in roles_needed):
                continue

        result.append({
            "id": r["id"],
            "hackathon_id": r["hackathon_id"],
            "hackathon_name": r["hackathon_name"],
            "project_title": r["project_title"],
            "leader_name": r["leader_name"],
            "leader_college": r["leader_college"],
            "roles_needed": roles_needed,
            "current_members": r["current_members"],
            "team_size": r["team_size"],
            "tech_stack": tech_stack,
            "description": r["description"],
            "contact_type": r["contact_type"],
            "contact_value": r["contact_value"],
            "status": r["status"],
            "created_at": r["created_at"]
        })
    return result

def add_squad_post(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    post_id = f"squad-{int(datetime.now().timestamp() * 1000)}"
    roles_json = json.dumps(data.get("roles_needed", []))
    tech_json = json.dumps(data.get("tech_stack", []))

    cursor.execute("""
        INSERT INTO squad_posts (
            id, hackathon_id, hackathon_name, project_title, leader_name,
            leader_college, roles_needed, current_members, team_size,
            tech_stack, description, contact_type, contact_value, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        post_id,
        data.get("hackathon_id", ""),
        data.get("hackathon_name", "Open Hackathon"),
        data.get("project_title", "Untitled Project"),
        data.get("leader_name", "Student Leader"),
        data.get("leader_college", "Campus Developer"),
        roles_json,
        int(data.get("current_members", 1)),
        int(data.get("team_size", 4)),
        tech_json,
        data.get("description", ""),
        data.get("contact_type", "Discord"),
        data.get("contact_value", ""),
        data.get("status", "Open")
    ))
    conn.commit()
    conn.close()
    return post_id

def toggle_squad_status(squad_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM squad_posts WHERE id = ?", (squad_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    new_status = "Filled" if row["status"] == "Open" else "Open"
    cursor.execute("UPDATE squad_posts SET status = ? WHERE id = ?", (new_status, squad_id))
    conn.commit()
    conn.close()
    return new_status

# --- Freshers Internships & Off-Campus Hiring Board ---

def seed_opportunities(cursor, conn):
    cursor.execute("SELECT COUNT(*) as count FROM opportunities")
    if cursor.fetchone()["count"] > 0:
        return

    opps = [
        (
            "opp-google-step-2026",
            "Google",
            "STEP Intern (Student Training in Engineering Program) 2026",
            "Summer Internship",
            json.dumps(["2027", "2028"]),
            "Software Engineering",
            "Bengaluru / Hyderabad (Hybrid)",
            "₹1,15,000 / month",
            "https://careers.google.com/jobs/results/?q=STEP%20Intern",
            "Rolling / Early Apply",
            "Google's Student Training in Engineering Program (STEP) is a 10-12 week developmental internship for first and second-year undergraduate students with a passion for computer science. Work on production-level projects alongside Google engineers and mentors.",
            json.dumps(["Data Structures", "Algorithms", "C++ / Java / Python", "Problem Solving"]),
            "Round 1: Google Online Challenge (2 DSA questions on strings/graphs, 60 mins). Round 2 & 3: Two 45-minute technical interviews focusing on data structures, complexity analysis, and clean coding.",
            "Active",
            1
        ),
        (
            "opp-amazon-sde-intern-2026",
            "Amazon",
            "Software Development Engineer (SDE) Intern - Summer 2026",
            "Summer Internship",
            json.dumps(["2026", "2027"]),
            "Software Engineering",
            "Bengaluru / Hyderabad / Chennai",
            "₹1,10,000 / month",
            "https://amazon.jobs/en/jobs/",
            "15 Oct 2026",
            "Join Amazon as an SDE intern to build large-scale distributed systems, low-latency APIs, and scalable customer-facing microservices. Excellent pre-placement offer (PPO) conversion rates for top performers.",
            json.dumps(["DSA", "Java / C++", "Object-Oriented Design", "SQL", "System Design Basics"]),
            "Round 1: Amazon Online Assessment on Hackerrank (2 Coding problems + Amazon Leadership Principles survey + Work Simulation). Round 2 & 3: Technical interview rounds covering DSA, Trees, Graphs, and Leadership Principles.",
            "Active",
            1
        ),
        (
            "opp-microsoft-engage-2026",
            "Microsoft",
            "Software Engineer Intern / Engage Mentorship Program",
            "Summer Internship",
            json.dumps(["2026", "2027"]),
            "Software Engineering",
            "Hyderabad / Bengaluru / Noida",
            "₹1,25,000 / month",
            "https://careers.microsoft.com/",
            "Rolling Apply",
            "Hands-on mentorship, code reviews with Microsoft engineers, and a chance to build next-generation Azure, M365, and AI workloads. Fast-track PPO path to full-time Software Engineer.",
            json.dumps(["Data Structures", "Algorithms", "Dynamic Programming", "C# / C++ / Python"]),
            "Round 1: Codility Online Assessment (3 algorithmic problems, 90 mins). Round 2: Technical live coding and system design basics. Round 3: Techno-managerial round on Azure architecture & culture fit.",
            "Active",
            1
        ),
        (
            "opp-flipkart-runway-2026",
            "Flipkart",
            "Flipkart Runway / SDE Summer Intern 2026",
            "Summer Internship",
            json.dumps(["2026", "2027"]),
            "Backend",
            "Bengaluru (Onsite)",
            "₹1,00,000 / month",
            "https://www.flipkartcareers.com/",
            "05 Nov 2026",
            "Flipkart Runway is designed to give students early exposure to India's largest e-commerce infrastructure. Work on high-throughput checkout pipelines, inventory algorithms, and distributed search.",
            json.dumps(["Data Structures", "Java", "Multi-Threading", "Kafka Basics", "RDBMS"]),
            "Round 1: Unstop Coding Assessment (MCQs on CS fundamentals + 2 hard DSA problems). Round 2: Machine Coding Round (2 hours to write runnable, modular OOP code). Round 3: Tech Interview on DSA & LLD.",
            "Active",
            1
        ),
        (
            "opp-goldman-sachs-summer-2026",
            "Goldman Sachs",
            "Summer Analyst - Engineering 2026",
            "Summer Internship",
            json.dumps(["2026", "2027"]),
            "Software Engineering",
            "Bengaluru / Hyderabad",
            "₹1,00,000 / month",
            "https://www.goldmansachs.com/careers/students/programs/",
            "20 Oct 2026",
            "Work in Goldman Sachs Global Investment Research and Global Banking & Markets technology. Build ultra-low latency trading systems, risk engines, and quant analytical models.",
            json.dumps(["Algorithms", "C++", "Python", "Computer Networks", "Operating Systems", "Probability"]),
            "Round 1: GS Aptitude & Coding OA (HackerRank with DSA + Math/Quant + CS Core MCQs). Round 2 & 3: Technical interview rounds covering Trees, Heaps, DP, and Operating Systems/DBMS fundamentals.",
            "Active",
            1
        ),
        (
            "opp-razorpay-sde1-2026",
            "Razorpay",
            "Software Development Engineer - 1 (Off-Campus FTE)",
            "Off-Campus Full-Time",
            json.dumps(["2026"]),
            "Backend",
            "Bengaluru (Hybrid)",
            "24 - 28 LPA CTC",
            "https://razorpay.com/jobs/",
            "Rolling / Urgent Hiring",
            "Razorpay powers financial infrastructure for millions of Indian businesses. Looking for sharp 2026 batch freshers to design scalable payment gateways, reconciliation engines, and UPI switches.",
            json.dumps(["Go / Java / Python", "Microservices", "REST APIs", "PostgreSQL", "Redis", "Distributed Systems"]),
            "Round 1: Online Coding Test on HackerEarth. Round 2: Machine Coding Round (Design an in-memory payment ledger or splitwise clone). Round 3: Problem Solving & Data Structures. Round 4: Cultural Fitment.",
            "Active",
            1
        ),
        (
            "opp-swiggy-intern-6m-2026",
            "Swiggy",
            "Software Engineering Intern (6-Month Final Sem)",
            "6-Month Internship",
            json.dumps(["2026"]),
            "Frontend",
            "Bengaluru / Remote",
            "₹60,000 / month + PPO",
            "https://careers.swiggy.com/",
            "30 Nov 2026",
            "Full-time 6-month internship during 8th semester for 2026 graduates. Work directly with Swiggy Instamart and Food Marketplace platform teams. Converts to full-time SDE-1 upon graduation.",
            json.dumps(["React", "Node.js", "Golang", "AWS", "Docker", "Database Indexing"]),
            "Round 1: Take-home full-stack prototype assignment or Hackerrank coding challenge. Round 2: Tech round assessing frontend state management and backend architecture. Round 3: Engineering Manager review.",
            "Active",
            0
        ),
        (
            "opp-cisco-ideathon-2026",
            "Cisco",
            "Software Consulting Engineer / Network Software Intern",
            "Summer Internship",
            json.dumps(["2026", "2027"]),
            "Software Engineering",
            "Bengaluru",
            "₹95,000 / month",
            "https://jobs.cisco.com/",
            "10 Nov 2026",
            "Cisco's flagship collegiate internship program. Build cloud networking infrastructure, edge security switches, and kernel networking modules. High PPO conversion rate for 2026/2027 grads.",
            json.dumps(["Computer Networks", "C / C++", "Python", "Linux Internals", "TCP/IP Protocol"]),
            "Round 1: Cisco Ideathon Online Assessment (CN & OS MCQs + 2 Coding questions). Round 2: Technical Interview covering OSI Model, Subnetting, Socket programming, and DSA. Round 3: Managerial & HR.",
            "Active",
            0
        ),
        (
            "opp-tcs-digital-prime-2026",
            "TCS",
            "TCS National Qualifier Test (NQT) - Digital & Prime Trainee",
            "Off-Campus Full-Time",
            json.dumps(["2026"]),
            "Software Engineering",
            "Pan-India (Major Metros)",
            "7.2 - 9.5 LPA CTC",
            "https://www.tcs.com/careers/india/tcs-national-qualifier-test",
            "Rolling Drive",
            "Pan-India off-campus hiring drive for all engineering graduates. Top performers in NQT Advanced section are directly interviewed for high-growth TCS Prime (9 LPA) and TCS Digital (7 LPA) roles.",
            json.dumps(["Java", "Python", "Data Structures", "SQL", "Aptitude & Reasoning"]),
            "Round 1: TCS NQT Exam (Foundation Section + Advanced Coding Section with 2 problems). Round 2: Technical Interview on projects, OOP concepts, and SQL queries. Round 3: HR & Management round.",
            "Active",
            0
        ),
        (
            "opp-atlassian-grad-2026",
            "Atlassian",
            "Associate Software Engineer (Off-Campus FTE)",
            "Off-Campus Full-Time",
            json.dumps(["2026"]),
            "Software Engineering",
            "Bengaluru / Remote-first",
            "26 - 32 LPA CTC",
            "https://www.atlassian.com/company/careers/graduates",
            "Rolling Apply",
            "Join Atlassian in building Jira, Confluence, and Trello. Work in a distributed, modern engineering culture with state-of-the-art CI/CD, microservices, and React design systems.",
            json.dumps(["Java", "Kotlin", "React", "Distributed Architecture", "REST APIs", "Unit Testing"]),
            "Round 1: HackerRank Online Test (3 algorithmic questions, 90 mins). Round 2: Data Structures & Algorithms live coding. Round 3: System Design / Concurrency round. Round 4: Values Interview.",
            "Active",
            1
        )
    ]

    cursor.executemany("""
        INSERT INTO opportunities (
            id, company, role_title, opportunity_type, eligible_batches,
            role_category, location, stipend_or_ctc, apply_url, deadline,
            description, skills, selection_process, status, featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, opps)
    conn.commit()


def get_all_opportunities(type_filter=None, batch_filter=None, category_filter=None, search_query=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM opportunities WHERE 1=1"
    params = []

    if type_filter and type_filter != "all":
        query += " AND LOWER(opportunity_type) LIKE LOWER(?)"
        params.append(f"%{type_filter}%")

    if batch_filter and batch_filter != "all":
        query += " AND eligible_batches LIKE ?"
        params.append(f"%{batch_filter}%")

    if category_filter and category_filter != "all":
        query += " AND LOWER(role_category) LIKE LOWER(?)"
        params.append(f"%{category_filter}%")

    if search_query and search_query.strip():
        term = f"%{search_query.strip()}%"
        query += " AND (company LIKE ? OR role_title LIKE ? OR skills LIKE ? OR location LIKE ?)"
        params.extend([term, term, term, term])

    query += " ORDER BY featured DESC, created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        try:
            d["eligible_batches"] = json.loads(d["eligible_batches"])
        except Exception:
            d["eligible_batches"] = [d["eligible_batches"]]
        try:
            d["skills"] = json.loads(d["skills"])
        except Exception:
            d["skills"] = [d["skills"]]
        # Standardize aliases so both JS frontends and raw db field names work
        d["title"] = d.get("role_title")
        d["type"] = d.get("opportunity_type")
        d["category"] = d.get("role_category")
        d["stipend"] = d.get("stipend_or_ctc")
        d["rounds"] = d.get("selection_process")
        result.append(d)
    return result


def get_opportunity_by_id(opp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunities WHERE id = ?", (opp_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    try:
        d["eligible_batches"] = json.loads(d["eligible_batches"])
    except Exception:
        d["eligible_batches"] = [d["eligible_batches"]]
    try:
        d["skills"] = json.loads(d["skills"])
    except Exception:
        d["skills"] = [d["skills"]]
    d["title"] = d.get("role_title")
    d["type"] = d.get("opportunity_type")
    d["category"] = d.get("role_category")
    d["stipend"] = d.get("stipend_or_ctc")
    d["rounds"] = d.get("selection_process")
    return d


def add_opportunity(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    opp_id = f"opp-{int(datetime.now().timestamp() * 1000)}"
    batches = data.get("eligible_batches") or data.get("batches") or ["2026"]
    if isinstance(batches, str):
        batches = [b.strip() for b in batches.split(",") if b.strip()]
    batches_json = json.dumps(batches)

    skills = data.get("skills", ["DSA", "Problem Solving"])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]
    skills_json = json.dumps(skills)

    cursor.execute("""
        INSERT INTO opportunities (
            id, company, role_title, opportunity_type, eligible_batches,
            role_category, location, stipend_or_ctc, apply_url, deadline,
            description, skills, selection_process, status, featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        opp_id,
        data.get("company", "Tech Company"),
        data.get("role_title") or data.get("title", "Software Engineering Intern"),
        data.get("opportunity_type") or data.get("type", "Summer Internship"),
        batches_json,
        data.get("role_category") or data.get("category", "Software Engineering"),
        data.get("location", "Pan-India / Remote"),
        data.get("stipend_or_ctc") or data.get("stipend", "Competitive"),
        data.get("apply_url", "#"),
        data.get("deadline", "Rolling Apply"),
        data.get("description", ""),
        skills_json,
        data.get("selection_process") or data.get("rounds", "Online Assessment + Technical Interview"),
        data.get("status", "active"),
        1 if data.get("featured") else 0
    ))
    conn.commit()
    conn.close()
    return opp_id


def get_saved_opportunities():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT opportunity_id FROM saved_opportunities ORDER BY saved_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [r["opportunity_id"] for r in rows]


def toggle_saved_opportunity(opp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT opportunity_id FROM saved_opportunities WHERE opportunity_id = ?", (opp_id,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute("DELETE FROM saved_opportunities WHERE opportunity_id = ?", (opp_id,))
        saved = False
    else:
        cursor.execute("INSERT INTO saved_opportunities (opportunity_id) VALUES (?)", (opp_id,))
        saved = True
    conn.commit()
    conn.close()
    return saved


# ==========================================
# PROJECT IDEA VAULT & ARCHITECTURE BLUEPRINTS
# ==========================================

def seed_projects(cursor, conn):
    cursor.execute("SELECT count(*) as count FROM projects")
    if cursor.fetchone()["count"] > 0:
        return

    projects = [
        (
            "proj-rate-limiter",
            "Distributed Rate Limiter & Edge Reverse Proxy",
            "High-throughput token-bucket & sliding-window edge reverse proxy capable of throttling 100k+ req/sec",
            "Advanced",
            "Systems & Cloud",
            "Microservices and public APIs collapse during sudden traffic surges, flash sales, DDoS spikes, or abusive bot scraping if not protected at network ingress by a distributed, sub-millisecond rate limiter.",
            "Fintech Gateways, High-Volume E-Commerce, Public REST APIs, SaaS Gateways",
            json.dumps(["Go", "Redis", "Lua", "Docker", "Prometheus", "Grafana"]),
            """[Client Traffic (100k+ req/s)]
            │
            ▼
    [Edge Reverse Proxy (TLS Termination)]
            │
            ▼
    [Go Rate Limiter Worker Cluster]
       ├── (Local In-Memory Cache) ────> [Fast Path: Per-Core Token Bucket]
       ├── (Atomic Lua Scripts) ───────> [Redis Cluster (Sliding Window Log & Counter)]
       └── (Telemetry Ingestion) ──────> [Prometheus Metrics Exporter]
                                                │
                                                ▼
                                    [Grafana Live Latency Dashboard]""",
            json.dumps([
                {"name": "Edge Gateway / Proxy", "role": "Terminates TLS, extracts client IP or API key, enforces timeout budgets, and returns HTTP 429 Too Many Requests with Retry-After header.", "tech": "Go / NGINX"},
                {"name": "Go Limiter Core", "role": "Implements concurrent Token Bucket and Sliding Window algorithms with Goroutines and atomic operations.", "tech": "Go (Golang)"},
                {"name": "Redis Distributed Cluster", "role": "Maintains shared state across all proxy nodes using single-roundtrip atomic Lua scripts to prevent distributed race conditions.", "tech": "Redis + Lua"},
                {"name": "Prometheus & Grafana Exporter", "role": "Tracks real-time throughput, throttle rejection rate, p95/p99 latency, and Redis connection pool stats.", "tech": "Prometheus / Grafana"}
            ]),
            json.dumps([
                "1. Client sends HTTP request with header `X-API-Key: client_sec_...` to Edge Proxy.",
                "2. Go reverse proxy extracts tenant identity and queries in-memory LRU tier config.",
                "3. If cache warm, executes atomic Redis Lua script evaluating current sliding timestamp window.",
                "4. If token count exceeds threshold, immediately returns HTTP 429 with `Retry-After: 30` header without burdening origin upstream.",
                "5. If permitted, forwards request to backend microservice and streams response back to client asynchronously."
            ]),
            """-- Redis Key Space Design
KEY: rate_limit:{api_key}:{minute_timestamp} -> Hash { count: 48, window_start: 1726132800 } (TTL 120s)
KEY: tenant_tier:{api_key} -> String: "enterprise" (10,000 req/min)

-- Config Database (PostgreSQL / SQLite)
CREATE TABLE client_rate_limits (
    id TEXT PRIMARY KEY,
    tenant_name TEXT NOT NULL,
    api_key_hash TEXT UNIQUE NOT NULL,
    tier TEXT DEFAULT 'free', -- free: 60/min, pro: 1000/min, enterprise: 10000/min
    burst_limit INTEGER NOT NULL,
    window_seconds INTEGER DEFAULT 60,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_tenant_key ON client_rate_limits(api_key_hash);""",
            json.dumps([
                {"q": "Why use Redis Lua scripts instead of standard GET and INCR?", "a": "Standard GET and INCR suffer from race conditions in concurrent distributed setups where multiple gateway replicas read an old count before incrementing. Lua scripts execute atomically on Redis in a single thread, guaranteeing zero race conditions without costly distributed locks."},
                {"q": "How does Token Bucket differ from Leaky Bucket and Sliding Window?", "a": "Token Bucket allows bursts of traffic up to bucket capacity while maintaining an average rate. Leaky Bucket enforces a smooth, constant egress rate regardless of burst. Sliding Window prevents boundary bursts at edge-of-minute transitions."},
                {"q": "What happens if Redis goes down?", "a": "Implement fail-open or graceful degradation with a local in-memory fallback (e.g. Uber's ratelimit leaky-bucket library in Go) logging warnings to alerts, ensuring upstream services aren't completely starved."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Foundation", "desc": "Build standalone Token Bucket and Sliding Window in Go with unit tests and atomic sync primitives."},
                {"phase": "Phase 2: Redis Integration", "desc": "Write atomic Lua scripts for sliding counter and test distributed state across 3 Go instances."},
                {"phase": "Phase 3: High Load Benchmarking", "desc": "Run vegeta or wrk load tests pushing 50,000 req/sec to benchmark p99 latency under 2ms."},
                {"phase": "Phase 4: Observability & Packaging", "desc": "Add Prometheus metrics, Grafana dashboard, Docker Compose setup, and CI GitHub Actions."}
            ]),
            "https://github.com/uber-go/ratelimit",
            142,
            1
        ),
        (
            "proj-collab-canvas",
            "Real-Time Collaborative Document Canvas",
            "Multiplayer interactive canvas with Conflict-Free Replicated Data Types (CRDTs) and sub-50ms peer sync",
            "Intermediate",
            "Full-Stack",
            "Collaborative editors (Figma/Notion-style) face split-brain concurrency conflicts and state divergence when multiple users edit simultaneously over flaky mobile network connections.",
            "Design teams, remote engineering squads, classroom whiteboards, hackathon squads",
            json.dumps(["TypeScript", "React", "Node.js", "WebSockets", "Yjs (CRDT)", "Redis PubSub"]),
            """[Client Browser A (React + Canvas)]        [Client Browser B (React + Canvas)]
                 │ (Binary WebSocket)                       │ (Binary WebSocket)
                 ▼                                          ▼
      [Node.js WebSocket Gateway Cluster (Sticky Session / Balancer)]
                 │                                          │
                 ├── (Yjs CRDT Document Engine) ────────────┤
                 │                                          │
                 ▼                                          ▼
     [Redis Pub/Sub Message Backplane (Cross-Instance Room Sync)]
                 │
                 ▼
     [PostgreSQL + S3 Snapshot Worker (Debounced Periodic Persistence)]""",
            json.dumps([
                {"name": "Frontend Canvas Engine", "role": "Renders vector shapes, freehand paths, and presence cursors on HTML5 Canvas / SVG with 60fps smoothing.", "tech": "React + TypeScript + Konva/SVG"},
                {"name": "Yjs CRDT Layer", "role": "Resolves multi-peer concurrent inserts, updates, and deletes mathematically without needing a centralized lock.", "tech": "Yjs / Y-Websocket"},
                {"name": "WebSocket Room Gateway", "role": "Maintains persistent duplex binary channels and routes delta updates to room occupants.", "tech": "Node.js / ws"},
                {"name": "Redis Pub/Sub Backplane", "role": "Synchronizes document updates across multiple horizontal WebSocket server instances.", "tech": "Redis"},
                {"name": "Document Snapshot Worker", "role": "Debounces client deltas and writes compiled document states to PostgreSQL and S3 every 30 seconds.", "tech": "Node.js / BullMQ"}
            ]),
            json.dumps([
                "1. User clicks or drags shape on React canvas; local state updates instantly (zero optimistic latency).",
                "2. Yjs encodes edit into compact binary State Vector Update diff.",
                "3. WebSocket client pushes binary diff to Node.js gateway over persistent duplex connection.",
                "4. Server broadcasts update to room peers via Redis Pub/Sub cluster.",
                "5. Peer clients apply incoming CRDT diff; mathematical convergence guarantees identical canvas state without conflict prompts."
            ]),
            """-- Relational Metadata & Document Snapshots
CREATE TABLE rooms (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE room_snapshots (
    id TEXT PRIMARY KEY,
    room_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    document_blob BLOB NOT NULL, -- Compressed Yjs binary snapshot
    snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);
CREATE INDEX idx_room_snapshots ON room_snapshots(room_id, version DESC);

CREATE TABLE user_collaborators (
    room_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT DEFAULT 'editor', -- viewer, editor, owner
    PRIMARY KEY (room_id, user_id)
);""",
            json.dumps([
                {"q": "What is the key difference between Operational Transformation (OT) and CRDTs?", "a": "OT (used in Google Docs) requires a central authoritative server to transform operations based on sequence numbers, making peer-to-peer and offline-first syncing difficult. CRDTs are conflict-free mathematically: operations are commutative and associative, allowing any peer to merge deltas in any order and converge on the exact same state."},
                {"q": "How do you handle presence indicators like live cursors?", "a": "Presence data (mouse coordinates, user avatar, active tool) is ephemeral and does not need to be stored in the CRDT document history. Use a lightweight pub/sub awareness channel over WebSockets broadcasting at 30-60Hz."},
                {"q": "How do you prevent unbounded CRDT memory growth (tombstones)?", "a": "Use state-vector garbage collection and take periodic snapshots (e.g., every 50 edits or 60s) where the full document is compacted and stored as a baseline snapshot."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Canvas Prototype", "desc": "Build HTML5 Canvas / SVG whiteboard in React with shape selection, dragging, and stroke rendering."},
                {"phase": "Phase 2: WebSocket & Presence", "desc": "Implement Node.js WebSocket server and broadcast live cursor locations with user colors."},
                {"phase": "Phase 3: Yjs CRDT Integration", "desc": "Integrate Yjs shared types (Y.Map, Y.Array) to achieve simultaneous multi-user conflict resolution."},
                {"phase": "Phase 4: Persistence & Production", "desc": "Add Redis Pub/Sub for horizontal scaling and periodic PostgreSQL snapshot backups."}
            ]),
            "https://github.com/yjs/yjs",
            128,
            1
        ),
        (
            "proj-multilingual-rag",
            "Multilingual AI RAG Engine for Indian Legal & Govt Schemes",
            "Retrieval-Augmented Generation system with cross-lingual embeddings (Hindi, Tamil, Telugu, English) and verifiable source citations",
            "Intermediate",
            "AI & GenAI",
            "Over 800 million citizens struggle to navigate complex government welfare schemes, agricultural subsidies, and statutory rights due to dense official legal jargon and lack of localized vernacular interfaces.",
            "Rural citizens, Common Service Centers (CSCs), NGO field volunteers, legal aid clinics",
            json.dumps(["Python", "FastAPI", "LangChain", "pgvector (PostgreSQL)", "BGE-M3 Embeddings", "Llama-3 / Gemini 1.5 Flash"]),
            """[Govt Gazette PDFs / Schemes / Laws]
                     │
                     ▼
       [Document Ingestion & Chunking Pipeline]
                     │ (Recursive Character + Semantic Splitting)
                     ▼
       [BGE-M3 Multilingual Embedding Model (1024-dim)]
                     │
                     ▼
       [PostgreSQL + pgvector (HNSW Index)]
                     │
    [Citizen Query (Hindi / Tamil / English)]
                     │
                     ▼
       [Hybrid Search: Dense Vector + Sparse BM25 Keyword Search]
                     │
                     ▼
     [Cross-Encoder Reranker + Source Chunk Retrieval]
                     │
                     ▼
       [LLM Prompt Synthesizer (Strict Citation Guardrails)]
                     │
                     ▼
    [Bilingual Vernacular Response with Verified Legal Source Links]""",
            json.dumps([
                {"name": "Ingestion & OCR Worker", "role": "Extracts text from multi-page government PDFs, extracts tables, and splits documents using semantic boundary markers.", "tech": "Python / PyMuPDF / Tesseract"},
                {"name": "BGE-M3 Multilingual Vectorizer", "role": "Generates 1024-dimensional dense and lexical sparse embeddings across 100+ languages including 10+ Indic languages.", "tech": "Hugging Face / PyTorch"},
                {"name": "pgvector Database", "role": "Stores document vectors and executes sub-10ms nearest-neighbor similarity searches using HNSW cosine distance indexing.", "tech": "PostgreSQL + pgvector extension"},
                {"name": "Hybrid Reranker & Guardrail", "role": "Combines vector cosine score with keyword BM25 score, reranks top 5 chunks, and validates LLM answers against source citations.", "tech": "FlashRank / Cross-Encoder"},
                {"name": "Vernacular API Gateway", "role": "Exposes streaming REST endpoints and handles voice-to-text / text-to-speech audio outputs.", "tech": "FastAPI + WebSockets"}
            ]),
            json.dumps([
                "1. User submits query in Hindi: 'किसान क्रेडिट कार्ड योजना के लिए आवश्यक दस्तावेज क्या हैं?'",
                "2. FastAPI translates/embeds query using BGE-M3 cross-lingual vector space.",
                "3. pgvector runs HNSW cosine search retrieving top 8 relevant scheme clauses.",
                "4. Cross-encoder reranker trims context to the 3 most precise statutory provisions.",
                "5. LLM prompt enforces zero-hallucination constraint: 'Answer strictly using context and cite section numbers'.",
                "6. API returns streaming structured answer with clickable source document references."
            ]),
            """-- Enable pgvector Extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE government_schemes (
    id TEXT PRIMARY KEY,
    ministry TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT NOT NULL, -- Agriculture, Education, Healthcare, Pension
    source_url TEXT NOT NULL,
    published_date TEXT
);

CREATE TABLE scheme_chunks (
    id TEXT PRIMARY KEY,
    scheme_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(1024), -- BGE-M3 1024-dim representation
    metadata JSONB, -- page number, section header, eligibility criteria
    FOREIGN KEY (scheme_id) REFERENCES government_schemes(id)
);

-- HNSW Vector Index for High-Speed Cosine Search
CREATE INDEX idx_scheme_embedding ON scheme_chunks 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);

CREATE INDEX idx_chunk_text_tsv ON scheme_chunks USING gin(to_tsvector('english', chunk_text));""",
            json.dumps([
                {"q": "Why use Hybrid Search (Vector + BM25) instead of pure vector search?", "a": "Vector search excels at semantic matching ('money for poor farmers' -> PM-KISAN), but often misses exact acronyms, scheme codes, and numerical statutory clauses (e.g. 'Section 80CCD'). Hybrid search combines semantic dense vectors with sparse BM25 keyword matching for optimal recall."},
                {"q": "How do you prevent LLMs from hallucinating non-existent government benefits?", "a": "1) Strict prompt guardrails: instruct model to state 'Not mentioned in official source' if context is absent. 2) Lower generation temperature (0.0 - 0.2). 3) Verification step: check if generated factual claims map back to source chunk token spans."},
                {"q": "How does cross-lingual embedding work without translating every document?", "a": "Multilingual models like BGE-M3 map semantically identical sentences across Hindi, Tamil, and English into the exact same vector space neighborhood, allowing an English query to find relevant Hindi gazettes and vice versa."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Document Processing", "desc": "Write PDF parsing pipeline extracting text and metadata from 20 central government scheme circulars."},
                {"phase": "Phase 2: Vector DB & HNSW", "desc": "Setup PostgreSQL with pgvector and populate embeddings with BGE-M3 using chunk overlap."},
                {"phase": "Phase 3: RAG Retrieval & Prompting", "desc": "Implement hybrid search with reciprocal rank fusion (RRF) and verifiable citation synthesis."},
                {"phase": "Phase 4: Vernacular UI & Testing", "desc": "Deploy interactive frontend with audio input, language switch, and benchmark against 50 test legal queries."}
            ]),
            "https://github.com/pgvector/pgvector",
            195,
            1
        ),
        (
            "proj-flash-sale-switch",
            "High-Concurrency Flash Sale & Ticket Reservation Engine",
            "Distributed reservation engine handling 50,000 TPS with zero overselling using Redis Redlock & Kafka FIFO queues",
            "Advanced",
            "FinTech & High-Scale",
            "Ticketing portals (like IRCTC or BookMyShow) and flash sales (Flipkart Big Billion Days) crash or oversell inventory when tens of thousands of concurrent requests attempt to purchase the same inventory in a single second.",
            "Railway and concert ticket systems, e-commerce mega sales, high-frequency booking portals",
            json.dumps(["Go", "Spring Boot", "Kafka", "Redis (Redlock)", "PostgreSQL", "Docker"]),
            """[50,000 Concurrent Buyers]
                     │
                     ▼
           [API Ingress & Rate Limiter]
                     │
                     ▼
          [Go Flash Sale Gatekeeper]
                     │
         (Atomic Lua Decr & Reservation Token)
                     ▼
           [Redis Cluster (In-Memory Inventory Cache)]
                     │
       ┌─────────────┴──────────────┐
       ▼                            ▼
 [Stock Depleted]             [Stock Available]
  (Instant 409 Sold Out)       │
                               ▼
                   [Kafka 'orders.reserved' Topic]
                               │ (Partitioned by product_id)
                               ▼
                   [Worker Consumer Service Pool]
                               │
                               ├── (PostgreSQL ACID Order Ledger)
                               └── (5-Minute Expiry Countdown in Redis)
                                          │
                        (If unpaid in 5 min ──> Stock Restocked back to Redis)""",
            json.dumps([
                {"name": "Go Fast-Gatekeeper", "role": "Accepts customer reservation requests, issues cryptographic checkout tokens, and offloads heavy database writes.", "tech": "Go / Gin"},
                {"name": "Redis Inventory Cache", "role": "Maintains exact stock counts in memory; executes atomic check-and-decrement Lua scripts in sub-millisecond time.", "tech": "Redis Enterprise / Cluster"},
                {"name": "Kafka Event Bus", "role": "Buffers purchase events, guarantees in-order FIFO processing per product partition, and prevents database write saturation.", "tech": "Apache Kafka"},
                {"name": "Order Finalizer Worker", "role": "Consumes Kafka reservation events, creates pending orders in PostgreSQL, and schedules payment timeouts.", "tech": "Spring Boot / Go"},
                {"name": "PostgreSQL Order Store", "role": "ACID transactional database holding confirmed financial invoices and immutable order ledgers.", "tech": "PostgreSQL"}
            ]),
            json.dumps([
                "1. User taps 'Book Now' for a high-demand ticket (50k requests in second 0).",
                "2. Go gateway invokes Redis Lua script: `if redis.call('get', key) > 0 then decrement and return token`.",
                "3. If stock is zero, user immediately gets 409 'Sold Out' within 2ms without touching PostgreSQL.",
                "4. If stock decremented, gateway publishes reservation event to Kafka partitioned by `product_id`.",
                "5. Consumer picks event, creates temporary hold order in DB, and sets 5-minute TTL payment lock in Redis.",
                "6. If user pays within 5 minutes, status flips to 'CONFIRMED'; if timeout expires, background worker re-increments Redis stock."
            ]),
            """-- Flash Sale Products & High-Speed Reservation Ledger
CREATE TABLE flash_sale_items (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    total_stock INTEGER NOT NULL,
    available_stock INTEGER NOT NULL,
    sale_start TIMESTAMP NOT NULL,
    sale_end TIMESTAMP NOT NULL,
    price_cents INTEGER NOT NULL
);

CREATE TABLE ticket_reservations (
    reservation_id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    status TEXT NOT NULL, -- PENDING_PAYMENT, CONFIRMED, EXPIRED, CANCELLED
    reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    payment_txn_id TEXT,
    FOREIGN KEY (item_id) REFERENCES flash_sale_items(id)
);
CREATE INDEX idx_res_status_exp ON ticket_reservations(status, expires_at);
CREATE UNIQUE INDEX idx_user_single_purchase ON ticket_reservations(item_id, user_id) 
WHERE status IN ('PENDING_PAYMENT', 'CONFIRMED');""",
            json.dumps([
                {"q": "How do you guarantee that a product with 100 stock is not sold to 101 people under 50k RPS?", "a": "Atomic decrement on Redis using Lua scripts: the read-decrement-verify sequence runs in a single thread on Redis without context switches. Once Redis returns 0, all subsequent requests are rejected immediately at the edge. PostgreSQL is never exposed to raw concurrent decr queries."},
                {"q": "What happens if a user books a ticket but abandons the payment gateway screen?", "a": "The reservation token is created with a 5-minute Redis key TTL. A dead-letter or scheduled rollback consumer listens to Redis key expiration events (or runs a periodic 10-second sweep on `ticket_reservations WHERE status = 'PENDING' AND expires_at < NOW()`) and atomicaly rolls back Redis stock by +1."},
                {"q": "Why partition Kafka topics by product_id?", "a": "Kafka guarantees FIFO order within a partition. By keying each event by `product_id`, all transactions for that specific item execute sequentially on the same consumer thread, eliminating row lock contention across the cluster."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Concurrency Benchmark Setup", "desc": "Write basic Go HTTP server and benchmark race conditions with k6 simulating 10,000 concurrent requests against plain SQL."},
                {"phase": "Phase 2: Redis Atomic Gatekeeper", "desc": "Implement Redis Lua check-and-decrement and verify zero overselling under intense load."},
                {"phase": "Phase 3: Kafka Async Pipeline", "desc": "Connect Kafka producer and consumer with DLQ and 5-minute automatic reservation expiry sweep."},
                {"phase": "Phase 4: Chaos Testing", "desc": "Simulate worker failure mid-reservation and verify inventory consistency and self-healing."}
            ]),
            "https://github.com/segmentio/kafka-go",
            176,
            1
        ),
        (
            "proj-upi-payment-gateway",
            "UPI-Compliant Microservices Payment Gateway Switch",
            "Fault-tolerant transactional payment orchestrator with Transactional Outbox pattern, idempotency keys, and automated reconciliation",
            "Advanced",
            "FinTech & High-Scale",
            "Network drops between merchant checkouts, payment aggregators, and NPCI banks cause duplicate debits, missing transactions, and customer disputes without strict transactional idempotency and outbox patterns.",
            "Payment aggregators, fintech startups, digital wallet providers, banking switches",
            json.dumps(["Java / Spring Boot", "Go", "PostgreSQL", "Kafka", "Redis", "Resilience4j"]),
            """[Merchant Mobile App / Web Checkout]
                     │ (POST /api/v1/payments + Idempotency-Key: uuid)
                     ▼
           [API Gateway & Idempotency Filter]
                     │
                     ▼
        [Payment Orchestrator Service]
                     │
        ┌────────────┴────────────────────────┐
        │ [ACID Transaction Boundary]         │
        │ 1. Insert 'PAYMENT_INITIATED'       │
        │ 2. Insert Outbox Event Record       │
        └─────────────────────────────────────┘
                     │ (Debezium Change Data Capture / Outbox Poller)
                     ▼
         [Kafka Topic: 'payment.outbox']
                     │
                     ▼
         [Bank Adapter & NPCI Gateway Switch]
                     │
        ┌────────────┴─────────────┐
        ▼                          ▼
 [Success / Failure Callback]  [Network Timeout (Resilience4j Circuit Breaker)]
        │                          │
        ▼                          ▼
 [Emit Webhook to Merchant]    [Auto-Query Status / Reverse Txn]
                                   │
                                   ▼
                       [End-of-Day Reconciliation Engine]""",
            json.dumps([
                {"name": "Idempotency Interceptor", "role": "Hashes payload and client-provided Idempotency Key in Redis to prevent double debits when user clicks 'Pay' twice.", "tech": "Redis + Spring Interceptor"},
                {"name": "Payment Orchestration Core", "role": "Coordinates payment lifecycle states: INITIATED, AUTHENTICATING, SUCCESS, FAILED, REFUNDED.", "tech": "Java / Spring Boot"},
                {"name": "Transactional Outbox Engine", "role": "Guarantees at-least-once event delivery to message brokers without two-phase commit distributed deadlocks.", "tech": "PostgreSQL + Debezium CDC"},
                {"name": "Bank Circuit Breaker & Retry", "role": "Applies exponential backoff with jitter and breaks circuit when banking APIs report degraded latency.", "tech": "Resilience4j"},
                {"name": "Automated Reconciliation Batch", "role": "Parses midnight bank settlement files against internal transaction ledgers to flag balance mismatches.", "tech": "Spring Batch / Go"}
            ]),
            json.dumps([
                "1. Merchant app issues payment request with HTTP header `X-Idempotency-Key: 9b1deb4d-...`",
                "2. Idempotency filter checks Redis: if key exists and completed, immediately replays saved response.",
                "3. Orchestrator opens ACID transaction: writes `orders` row and `outbox_events` row in PostgreSQL.",
                "4. Outbox poller streams event to Kafka, which invokes banking simulator via TLS client certificate.",
                "5. Upon bank response or webhook, payment state flips to `SUCCESS` and merchant webhook is queued with signature verification.",
                "6. If bank drops connection, background status poller queries NPCI API every 30s for 3 minutes before triggering auto-reversal."
            ]),
            """-- Payment Core Schema with Idempotency & Outbox Pattern
CREATE TABLE payments (
    id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL,
    amount_inr_paise BIGINT NOT NULL, -- Always store currency in lowest denomination (paise)
    currency TEXT DEFAULT 'INR',
    customer_vpa TEXT NOT NULL, -- e.g. user@okhdfcbank
    status TEXT NOT NULL, -- INITIATED, SUCCESS, FAILED, TIMEOUT, REFUNDED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE idempotency_keys (
    key_hash TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL,
    payment_id TEXT NOT NULL,
    request_hash TEXT NOT NULL,
    response_body TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (payment_id) REFERENCES payments(id)
);

CREATE TABLE outbox_events (
    id BIGSERIAL PRIMARY KEY,
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_unprocessed_outbox ON outbox_events(id) WHERE processed = FALSE;""",
            json.dumps([
                {"q": "What is the Transactional Outbox pattern and why is it vital in payments?", "a": "When writing to a database and publishing to a message broker (Kafka), you cannot execute both in a single ACID transaction. If the database commit succeeds but Kafka fails, events are lost. If Kafka succeeds but DB rollbacks, phantom events are fired. The Outbox pattern writes the business entity and the outbox event into the SAME SQL database transaction. A separate process streams outbox rows to Kafka, guaranteeing 100% reliable event dispatch."},
                {"q": "Why store monetary values in paise (integers) rather than floats or doubles?", "a": "Floating point arithmetic (IEEE 754) introduces rounding inaccuracies (e.g. 0.1 + 0.2 = 0.30000000000000004). Financial ledgers must use exact integers representing the lowest currency denomination (paise / cents) or arbitrary-precision numeric types to prevent compounding accounting errors."},
                {"q": "How do you handle merchant webhooks securely?", "a": "Sign webhook payloads using HMAC-SHA256 with a secret merchant key. Include a timestamp to prevent replay attacks. Implement exponential backoff retry for failed delivery (HTTP != 200)."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Double-Entry Ledger", "desc": "Design PostgreSQL schema for debit/credit ledger and implement Idempotency-Key validation filter."},
                {"phase": "Phase 2: Transactional Outbox & Kafka", "desc": "Build outbox event polling worker to publish reliable payment status messages."},
                {"phase": "Phase 3: Bank Simulator & Circuit Breakers", "desc": "Create NPCI mock gateway with randomized latency, timeouts, and Resilience4j circuit breaker fallback."},
                {"phase": "Phase 4: Reconciliation & Webhooks", "desc": "Write end-of-day bank statement reconciliation script and HMAC-signed webhook delivery system."}
            ]),
            "https://github.com/resilience4j/resilience4j",
            154,
            1
        ),
        (
            "proj-cloud-cost-agent",
            "Cloud Infrastructure Cost & Observability Agent",
            "Real-time Kubernetes resource leak detector and FinOps cost predictor with ClickHouse columnar storage",
            "Intermediate",
            "DevOps & Cloud",
            "Engineering teams overspend 30% to 40% on AWS/GCP due to orphan EBS storage volumes, over-provisioned Kubernetes pods, and unindexed egress networking.",
            "DevOps engineers, FinOps practitioners, cloud platform teams, cost-conscious startups",
            json.dumps(["Go", "Python", "ClickHouse", "Prometheus", "Next.js", "Docker"]),
            """[Kubernetes Cluster (DaemonSet Agents)]
                     │ (Per-Pod CPU, Memory, Storage Usage)
                     ▼
           [Go Telemetry Collector]
                     │
                     ├── (AWS / GCP Cloud Pricing API Scraper)
                     │
                     ▼
       [ClickHouse Columnar Database (MergeTree)]
                     │
        ┌────────────┴────────────────────────┐
        ▼                                     ▼
 [Anomaly & Waste Detection Engine]   [FinOps Web Dashboard (Next.js)]
   - Underutilized Pods (< 10% CPU)     - Real-Time Team Spend Allocation
   - Unattached Cloud Disks             - Projected Monthly Invoices
   - High Egress Data Spikes            - 1-Click Slack / Email Alerts""",
            json.dumps([
                {"name": "K8s DaemonSet Agent", "role": "Collects container cgroup CPU, memory, and filesystem metrics every 15 seconds across all nodes.", "tech": "Go / client-go"},
                {"name": "Cloud Pricing Worker", "role": "Pulls cloud provider spot, on-demand, and reserved pricing tables to map compute seconds to rupees/dollars.", "tech": "Python / Cloud APIs"},
                {"name": "ClickHouse Analytical DB", "role": "Stores high-cardinality time-series metrics with 10x compression and runs sub-second analytical queries over billions of rows.", "tech": "ClickHouse"},
                {"name": "Idle Detection Engine", "role": "Runs automated rules identifying pods where allocated memory exceeds 5x actual consumption over 7 days.", "tech": "Python / SciPy"},
                {"name": "FinOps Dashboard", "role": "Displays interactive cost drilldowns by namespace, team tag, and microservice with downloadable CSV reports.", "tech": "Next.js + Tailwind + Chart.js"}
            ]),
            json.dumps([
                "1. Go DaemonSet reads container resource metrics from local kubelet cgroups.",
                "2. Metrics collector tags records with Kubernetes namespace, deployment name, and cluster region.",
                "3. Ingest worker batches and writes 10,000 metrics/sec into ClickHouse MergeTree tables.",
                "4. Anomaly detector evaluates hourly cost per microservice against 30-day baseline.",
                "5. When an orphan volume or unused pod is identified, automated Slack alert is sent to team with estimated monthly savings."
            ]),
            """-- ClickHouse High-Performance Analytical Telemetry Tables
CREATE TABLE container_resource_telemetry (
    timestamp DateTime CODEC(DoubleDelta, LZ4),
    cluster_id LowCardinality(String),
    namespace LowCardinality(String),
    pod_name String,
    container_name LowCardinality(String),
    cpu_cores_requested Float32,
    cpu_cores_actual Float32,
    ram_mb_requested Float32,
    ram_mb_actual Float32,
    hourly_cost_usd Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (cluster_id, namespace, container_name, timestamp);

CREATE TABLE cost_recommendations (
    id UUID DEFAULT generateUUIDv4(),
    detected_at DateTime DEFAULT now(),
    resource_type LowCardinality(String), -- POD, UNATTACHED_DISK, IDLE_LOAD_BALANCER
    resource_identifier String,
    reason String,
    estimated_monthly_saving_usd Float64,
    status LowCardinality(String) DEFAULT 'OPEN'
) ENGINE = ReplacingMergeTree()
ORDER BY (resource_type, resource_identifier, detected_at);""",
            json.dumps([
                {"q": "Why choose ClickHouse over traditional databases like PostgreSQL or MongoDB for telemetry?", "a": "ClickHouse is a columnar database designed specifically for Online Analytical Processing (OLAP). It achieves 80-90% data compression on repetitive logs and scans billions of rows per second by reading only the required columns, making aggregations across millions of metric data points sub-second."},
                {"q": "How do you calculate the actual cost of a Kubernetes Pod sharing a multi-tenant EC2 node?", "a": "Calculate the node's hourly cost (e.g. AWS c6i.2xlarge = $0.34/hr). Compute the pod's fractional request of total node allocatable CPU and RAM: `pod_cost = max(pod_cpu / node_cpu, pod_ram / node_ram) * node_hourly_cost`."},
                {"q": "How do you prevent alerts from flooding when traffic naturally dips at night?", "a": "Use rolling baseline percentiles (e.g. comparing Tuesday 3 AM against historical Tuesdays 3 AM) rather than static absolute thresholds, and require an underutilization condition to persist for at least 72 continuous hours before classifying as waste."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Metric Collector", "desc": "Write lightweight Go agent using client-go to stream container CPU and RAM usage to console."},
                {"phase": "Phase 2: ClickHouse Setup", "desc": "Deploy ClickHouse in Docker and benchmark high-throughput batch writes of synthetic metric rows."},
                {"phase": "Phase 3: Waste Detection Algorithm", "desc": "Implement rules identifying unattached storage and oversized memory allocations."},
                {"phase": "Phase 4: Web UI & Slack Bot", "desc": "Build Next.js analytics dashboard with interactive cost breakdown charts and Slack webhook alerts."}
            ]),
            "https://github.com/ClickHouse/ClickHouse",
            89,
            0
        ),
        (
            "proj-verifiable-credentials",
            "Decentralized Verifiable Credential & College Degree Ledger",
            "Tamper-proof academic diploma verification system using Ethereum smart contracts, IPFS metadata, and zero-knowledge proofs",
            "Foundations",
            "Full-Stack",
            "Fake university degrees, altered marks cards, and forged certificates plague campus hiring, requiring weeks of manual verification calls and costly third-party background verification agencies.",
            "Colleges & Universities, Corporate HR verification teams, Recruiters, Students",
            json.dumps(["Solidity", "Hardhat", "IPFS", "Ethers.js", "React", "TailwindCSS"]),
            """[University Registrar Admin Portal]
                     │
         (Uploads Degree PDF + Enters Student Roll No)
                     ▼
           [SHA-256 Hash + IPFS Pinning]
                     │ (Metadata pinned to IPFS decentralized storage)
                     ▼
         [Polygon / Ethereum Smart Contract]
                     │
           (Method: `issueCredential(recipientAddress, ipfsHash)`)
                     ▼
      [Soulbound (Non-Transferable) NFT Minted to Student]
                     │
                     ▼
        [Instant Verification Portal (QR Scan)]
                     │
      (HR Scans QR Code on Resume ──> Instant Validated Green Checkmark on Blockchain)""",
            json.dumps([
                {"name": "University Registrar Portal", "role": "Web interface where authorized university admins sign and issue digital degrees using their authorized Web3 wallet.", "tech": "React + Ethers.js"},
                {"name": "Verifiable Credential Smart Contract", "role": "Soulbound ERC-721 contract storing cryptographic hashes of issued certificates with multi-sig revocation authority.", "tech": "Solidity + Hardhat"},
                {"name": "IPFS Storage Layer", "role": "Provides decentralized, content-addressed storage for certificate PDF metadata, transcripts, and institution signatures.", "tech": "IPFS / Pinata"},
                {"name": "Instant Verification Widget", "role": "Public web viewer where any recruiter can paste an IPFS hash or scan a QR code to verify validity in 1 second.", "tech": "React + TailwindCSS"}
            ]),
            json.dumps([
                "1. College admin logs in with university MetaMask wallet (verified against registrar smart contract role).",
                "2. System hashes student degree document using SHA-256 and pins certificate metadata JSON to IPFS.",
                "3. Smart contract executes `issueCertificate(studentAddress, certHash, ipfsCID)` emitting an immutable event.",
                "4. Student receives a verifiable Soulbound Token (SBT) in their crypto wallet with a permanent verification URL.",
                "5. Recruiter scans QR code on candidate resume; verification viewer queries Polygon RPC to prove cryptographic validity without trusting any intermediary."
            ]),
            """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UniversityDegreeRegistry {
    address public owner;
    
    struct Degree {
        string studentName;
        string studentRollNo;
        string degreeName;
        string department;
        uint256 graduationYear;
        string ipfsCid;
        bytes32 documentHash;
        bool isRevoked;
    }

    mapping(address => bool) public authorizedRegistrars;
    mapping(bytes32 => Degree) public degreesByHash;
    
    event DegreeIssued(bytes32 indexed docHash, string rollNo, address indexed issuedBy);
    event DegreeRevoked(bytes32 indexed docHash, string reason);

    modifier onlyRegistrar() {
        require(authorizedRegistrars[msg.sender] || msg.sender == owner, "Not authorized registrar");
        _;
    }

    function issueDegree(
        bytes32 docHash,
        string memory name,
        string memory rollNo,
        string memory degreeTitle,
        string memory ipfsCid
    ) external onlyRegistrar {
        require(degreesByHash[docHash].documentHash == bytes32(0), "Degree already issued");
        degreesByHash[docHash] = Degree(name, rollNo, degreeTitle, "CSE", block.timestamp, ipfsCid, docHash, false);
        emit DegreeIssued(docHash, rollNo, msg.sender);
    }
}""",
            json.dumps([
                {"q": "What is a Soulbound Token (SBT) and why is it essential for academic credentials?", "a": "Standard ERC-721 NFTs can be transferred or sold from one wallet to another. A college degree must be non-transferable (soulbound) so that a student cannot sell or lend their degree token to another person."},
                {"q": "Why store the PDF on IPFS rather than putting the entire document on the Ethereum blockchain?", "a": "Storing arbitrary data on the Ethereum blockchain is prohibitively expensive (several dollars per kilobyte in gas). IPFS provides content-addressed distributed storage at zero/low cost, while only the 32-byte SHA-256 hash is committed to the blockchain."},
                {"q": "How can a university revoke a degree if fraud or plagiarism is discovered later?", "a": "The smart contract includes an authorized `revokeDegree(bytes32 docHash, string reason)` function callable only by the university multi-sig wallet, which marks `isRevoked = true` while preserving the permanent audit log."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Smart Contract Design", "desc": "Write Solidity contract with registrar access control and deploy on Polygon Mumbai / Amoy testnet."},
                {"phase": "Phase 2: IPFS File Pinning", "desc": "Integrate Pinata / Web3.Storage to generate content-addressed hashes of student certificates."},
                {"phase": "Phase 3: Registrar Dashboard", "desc": "Build clean issuance dashboard for university staff with batch CSV degree upload."},
                {"phase": "Phase 4: Public QR Verifier", "desc": "Create fast mobile-responsive web viewer where recruiters verify authenticity with 1 click."}
            ]),
            "https://github.com/nomicfoundation/hardhat",
            104,
            0
        ),
        (
            "proj-video-transcoder",
            "Distributed Video Transcoder & Adaptive Bitrate (HLS) Pipeline",
            "Cloud-native video chunking & multi-resolution HLS packaging pipeline with distributed worker nodes and S3/MinIO object storage",
            "Advanced",
            "Systems & Cloud",
            "High-resolution video uploads buffer, crash, or fail on low-bandwidth Indian 4G/5G mobile networks without adaptive bitrate streaming (1080p, 720p, 480p, 360p HLS playlists).",
            "EdTech portals, video sharing apps, streaming course platforms, creator communities",
            json.dumps(["Go", "Python", "FFmpeg", "MinIO / S3", "Redis Queue", "Docker"]),
            """[User Video Upload (.mp4 / .mov)]
                     │ (Direct Presigned Upload)
                     ▼
          [MinIO / S3 'raw-videos' Bucket]
                     │
                     ▼
       [Go Master Orchestrator Service]
                     │
       (Splits Video Job into 1080p, 720p, 480p tasks)
                     ▼
           [Redis Task Queue (BullMQ / Asynq)]
                     │
        ┌────────────┴────────────────────────┐
        ▼                                     ▼
 [Worker Node 1 (FFmpeg)]              [Worker Node 2 (FFmpeg)]
  - Extracts Audio (.aac)               - Transcodes 1080p -> 720p
  - Segments into 6s .ts chunks         - Generates .m3u8 Playlist
        │                                     │
        └────────────┬────────────────────────┘
                     │
                     ▼
         [MinIO / S3 'hls-output' Bucket]
                     │ (master.m3u8 + index_720p.m3u8 + segment0.ts)
                     ▼
        [Video.js / Hls.js Adaptive Video Player]""",
            json.dumps([
                {"name": "Presigned Upload Gateway", "role": "Generates secure direct-to-S3 upload URLs so large video files bypass web server RAM completely.", "tech": "Go / AWS SDK"},
                {"name": "Job Dispatcher", "role": "Probes uploaded media container specs (codec, bitrate, resolution) and dispatches parallel transcoding tasks.", "tech": "Go / FFprobe"},
                {"name": "Distributed FFmpeg Worker Pool", "role": "Executes hardware/CPU-accelerated video encoding into H.264 / AAC and generates HLS transport segments (.ts).", "tech": "Docker + FFmpeg + Go"},
                {"name": "MinIO / S3 Object Store", "role": "Stores master playlist manifests, variant playlists, and video chunks with HTTP Range request support.", "tech": "MinIO (Self-hosted S3)"},
                {"name": "Adaptive Web Player", "role": "Monitors client bandwidth in real-time and dynamically shifts video resolution up or down without freezing.", "tech": "React + Video.js / Hls.js"}
            ]),
            json.dumps([
                "1. User drops a 500MB raw 4K/1080p video on the browser.",
                "2. Frontend requests presigned S3 URL from API and uploads directly to MinIO bucket.",
                "3. MinIO webhook triggers Go orchestrator, which inspects video stream metadata with FFprobe.",
                "4. Orchestrator queues parallel transcoding jobs in Redis for 1080p (5Mbps), 720p (2.5Mbps), and 480p (1Mbps).",
                "5. FFmpeg worker slices video into 6-second `.ts` chunks and compiles adaptive `master.m3u8` playlist.",
                "6. Player client plays `master.m3u8`; viewer automatically gets crisp 1080p on Wi-Fi and seamless 480p on patchy mobile data."
            ]),
            """-- Video Transcoding Catalog & Rendition Records
CREATE TABLE video_assets (
    id TEXT PRIMARY KEY,
    uploader_id TEXT NOT NULL,
    title TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    duration_seconds INTEGER,
    raw_storage_path TEXT NOT NULL,
    status TEXT NOT NULL, -- UPLOADED, PROCESSING, READY, FAILED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE video_renditions (
    id TEXT PRIMARY KEY,
    video_id TEXT NOT NULL,
    resolution TEXT NOT NULL, -- 1080p, 720p, 480p, 360p
    bitrate_kbps INTEGER NOT NULL,
    playlist_path TEXT NOT NULL, -- e.g. hls/video_123/720p.m3u8
    segment_count INTEGER NOT NULL,
    file_size_bytes BIGINT,
    FOREIGN KEY (video_id) REFERENCES video_assets(id)
);
CREATE INDEX idx_renditions_video ON video_renditions(video_id);""",
            json.dumps([
                {"q": "How does HTTP Live Streaming (HLS) prevent video buffering?", "a": "HLS breaks video files into tiny 4-to-6 second segments (`.ts` files) indexed by a text playlist (`.m3u8`). If the user's internet speed slows down, the player downloads the next 6-second segment at a lower resolution (e.g. 480p instead of 1080p) without stalling video playback."},
                {"q": "Why should video uploads bypass the web backend server entirely?", "a": "If a web server buffers a 1GB video upload into memory, high concurrent traffic will cause out-of-memory crashes and saturate server network sockets. Generating a presigned S3 URL lets the client upload directly to cloud storage."},
                {"q": "How do you handle worker crashes during a 10-minute long encode?", "a": "Use atomic queue locks (e.g. Redis visibility timeouts). If a worker stops heartbeating for 60 seconds, Redis automatically releases the job back to the queue for another healthy worker to resume."}
            ]),
            json.dumps([
                {"phase": "Phase 1: FFmpeg Scripting", "desc": "Write FFmpeg commands converting a sample video into HLS multi-bitrate folders and test with local VLC."},
                {"phase": "Phase 2: MinIO & Presigned Uploads", "desc": "Set up local MinIO container and implement presigned multipart upload API."},
                {"phase": "Phase 3: Worker Queue System", "desc": "Build Go job coordinator and Dockerized worker pool processing video chunks in parallel."},
                {"phase": "Phase 4: Frontend Player & Metrics", "desc": "Integrate Video.js player with real-time encoding progress bar and bandwidth toggle."}
            ]),
            "https://github.com/FFmpeg/FFmpeg",
            118,
            0
        ),
        (
            "proj-ast-code-reviewer",
            "AI Automated AST Code Review & Security Vulnerability Bot",
            "Static analysis bot parsing Tree-sitter Abstract Syntax Trees combined with LLM prompt context to catch SQLi, memory leaks, and anti-patterns on PRs",
            "Foundations",
            "AI & GenAI",
            "Manual code reviews in student hackathons and college projects take days, miss critical security bugs (unwashed SQL queries, exposed API tokens), and bottleneck sprint deliveries.",
            "Student developers, open-source maintainers, hackathon teams, college project evaluators",
            json.dumps(["Python", "Tree-sitter (AST)", "FastAPI", "GitHub Webhooks", "OpenAI / Gemini API"]),
            """[Developer Opens Pull Request on GitHub]
                     │ (GitHub Webhook: `pull_request.opened`)
                     ▼
           [FastAPI Webhook Receiver]
                     │
                     ├── (Clones Unified Git Diff)
                     ▼
         [Tree-sitter AST Parser Engine]
                     │
        ┌────────────┴────────────────────────┐
        ▼                                     ▼
 [Deterministic Rule Scanner]          [Semantic Context Extractor]
  - Regex Token / Key Leaks             - Enclosing Function Signatures
  - Raw SQL String Concatenation        - Variable Scope & Invariants
        │                                     │
        └────────────┬────────────────────────┘
                     │
                     ▼
      [LLM Review Synthesizer (Structured JSON Output)]
                     │
                     ▼
      [GitHub REST API: Post Inline Code Comments on Specific PR Lines]""",
            json.dumps([
                {"name": "Webhook Ingress", "role": "Validates HMAC GitHub webhook secrets and extracts repository name, PR number, and commit SHA.", "tech": "FastAPI"},
                {"name": "Tree-sitter Parser", "role": "Parses Python, JavaScript, and Java source files into concrete Abstract Syntax Trees to identify exact node coordinates.", "tech": "tree-sitter / py-tree-sitter"},
                {"name": "Security Heuristic Scanner", "role": "Catches obvious anti-patterns deterministically (e.g. `eval()`, hardcoded AWS secrets, SQL interpolation) in zero milliseconds.", "tech": "Python AST queries"},
                {"name": "LLM Code Doctor", "role": "Receives the AST context, function docstring, and git diff to analyze logic bugs and suggest clean refactoring.", "tech": "Gemini API / GPT-4o-mini"},
                {"name": "GitHub Comment Publisher", "role": "Publishes markdown-formatted inline suggestions directly onto the corresponding line of the pull request.", "tech": "PyGithub / REST API"}
            ]),
            json.dumps([
                "1. Developer pushes a new commit to a GitHub pull request.",
                "2. GitHub fires webhook event `pull_request.synchronize` to the FastAPI service.",
                "3. Service extracts changed files and builds Abstract Syntax Trees using Tree-sitter grammar.",
                "4. If a function contains `SELECT * FROM users WHERE id = ' + user_id`, deterministic scanner flags CWE-89 SQL Injection.",
                "5. Surrounding function block is sent to LLM with prompt: 'Provide fixed code snippet and explain security impact'.",
                "6. Bot posts inline review comment on GitHub PR with clickable one-click 'Apply suggestion' button."
            ]),
            """-- Code Review History & Security Metrics
CREATE TABLE reviewed_repositories (
    id TEXT PRIMARY KEY,
    repo_full_name TEXT UNIQUE NOT NULL, -- e.g. "org/repo"
    installation_id TEXT NOT NULL,
    default_branch TEXT DEFAULT 'main',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pull_request_audits (
    id TEXT PRIMARY KEY,
    repo_id TEXT NOT NULL,
    pr_number INTEGER NOT NULL,
    commit_sha TEXT NOT NULL,
    files_analyzed INTEGER NOT NULL,
    issues_found INTEGER NOT NULL,
    llm_tokens_used INTEGER NOT NULL,
    review_status TEXT NOT NULL, -- PASSED, WARNINGS, BLOCKED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (repo_id) REFERENCES reviewed_repositories(id)
);

CREATE TABLE detected_vulnerabilities (
    id TEXT PRIMARY KEY,
    audit_id TEXT NOT NULL,
    file_path TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    rule_category TEXT NOT NULL, -- SECURITY, PERFORMANCE, CODE_SMELL
    description TEXT NOT NULL,
    suggested_fix TEXT NOT NULL,
    FOREIGN KEY (audit_id) REFERENCES pull_request_audits(id)
);""",
            json.dumps([
                {"q": "Why use Tree-sitter AST parsing instead of just feeding the entire code file to an LLM?", "a": "Sending large codebases to an LLM is slow, expensive, and risks exceeding token context limits. AST parsing allows you to surgically identify only modified functions and structural scopes, dramatically reducing LLM costs by 80% while eliminating false positives."},
                {"q": "What is an Abstract Syntax Tree (AST)?", "a": "An AST is a hierarchical tree representation of source code structure produced by a compiler/parser. Instead of treating code as plain strings, an AST represents variables, loops, and function calls as typed tree nodes, making precise structural queries possible."},
                {"q": "How do you prevent the bot from spamming developers on minor stylistic choices?", "a": "Configure severity thresholds (HIGH: SQLi / RCE / Leak -> Block PR; MEDIUM: Performance -> Comment; LOW: Naming -> Suppress unless explicitly requested in repo config)."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Tree-sitter Experiments", "desc": "Parse sample Python code with tree-sitter to locate function definitions and dangerous calls."},
                {"phase": "Phase 2: GitHub Webhook Setup", "desc": "Create FastAPI webhook receiver and authenticate using GitHub App private key."},
                {"phase": "Phase 3: LLM Inline Prompting", "desc": "Formulate structured JSON prompt generating concrete inline diff replacements."},
                {"phase": "Phase 4: GitHub Action / App Release", "desc": "Package as a reusable GitHub Action and run it against 10 real open-source student PRs."}
            ]),
            "https://github.com/tree-sitter/tree-sitter",
            91,
            0
        ),
        (
            "proj-iot-telemetry-hub",
            "IoT Cold Chain Telemetry & Predictive Alert Hub",
            "Low-power MQTT sensor telemetry ingestion pipeline with InfluxDB time-series storage and automated temperature anomaly detection",
            "Foundations",
            "Systems & IoT",
            "Vaccines, insulin, dairy products, and perishable farm produce spoil during transport across Indian states if refrigerated vehicle temperatures fluctuate above safe thresholds without instant alerts.",
            "Pharma logistics, dairy supply chains, cold storage warehouses, agri-tech startups",
            json.dumps(["ESP32 / C++", "MQTT (Mosquitto)", "Python", "InfluxDB", "Grafana", "Twilio / WhatsApp API"]),
            """[Refrigerated Vehicle / Warehouse (ESP32 + DHT22 + GPS)]
                             │ (Low-Power MQTT over cellular 4G/GSM)
                             ▼
              [Mosquitto MQTT Message Broker]
                             │
                             ▼
             [Python High-Throughput Stream Consumer]
                             │
        ┌────────────────────┴────────────────────────┐
        ▼                                             ▼
 [InfluxDB Time-Series Database]            [Anomaly Detection Rule Engine]
  - Sub-second timestamped readings          - Moving Average Temperature
  - Retention policy (30 days raw)           - Breach: > 4°C for > 3 minutes
        │                                             │
        ▼                                             ▼
 [Grafana Real-Time Vehicle Dashboard]      [Automated Twilio / WhatsApp SOS Alert]
  - Live GPS Route on Map                    - Alerts Driver & Logistics Hub
  - Temperature vs Humidity graphs""",
            json.dumps([
                {"name": "Edge Telemetry Firmware", "role": "Samples temperature, humidity, and GPS coordinates every 10 seconds and publishes compact JSON payloads over MQTT.", "tech": "ESP32 / C++ / FreeRTOS"},
                {"name": "MQTT Mosquitto Broker", "role": "Lightweight pub/sub message broker optimized for high latency and intermittent cellular connectivity.", "tech": "Eclipse Mosquitto"},
                {"name": "Stream Ingest Worker", "role": "Consumes MQTT messages from `vehicles/+/telemetry` topics, validates ranges, and writes batch points to InfluxDB.", "tech": "Python / paho-mqtt"},
                {"name": "InfluxDB Time-Series DB", "role": "Stores and aggregates chronological sensor data with automatic downsampling policies.", "tech": "InfluxDB v2"},
                {"name": "Emergency Alert Dispatcher", "role": "Detects thermal breaches and fires automated WhatsApp messages and SMS alerts to logistics managers.", "tech": "Twilio / WhatsApp Cloud API"}
            ]),
            json.dumps([
                "1. ESP32 microcontroller in refrigerated truck reads temperature from Dallas DS18B20 digital sensor.",
                "2. Microcontroller publishes payload `{\"truck_id\": \"MH-04-1234\", \"temp\": 7.8, \"lat\": 19.076, \"lon\": 72.877}` over MQTT.",
                "3. Python stream consumer receives message and writes to InfluxDB measurement `coldchain_telemetry`.",
                "4. Anomaly detector calculates 3-minute rolling average: detects temperature breached safe 2°C - 4°C threshold.",
                "5. Alert worker immediately dispatches WhatsApp message with current vehicle location link to logistics control room."
            ]),
            """-- InfluxDB Bucket Definition & Measurement Line Protocol
-- Measurement: coldchain_metrics
-- Tags: vehicle_id, route_id, driver_id, city
-- Fields: temperature_celsius (float), humidity_pct (float), battery_volts (float), lat (float), lon (float)

-- Example InfluxDB Line Protocol:
-- coldchain_metrics,vehicle_id=TRUCK_DELHI_01,route_id=DEL_MUM_04 temperature_celsius=6.4,humidity_pct=65.2,lat=28.6139,lon=77.2090 1726132800000000000

-- SQLite / Relational Metadata for Fleet Management
CREATE TABLE logistics_vehicles (
    id TEXT PRIMARY KEY,
    vehicle_number TEXT UNIQUE NOT NULL,
    cargo_type TEXT NOT NULL, -- VACCINES, PERISHABLES, DAIRY
    min_temp_celsius REAL NOT NULL,
    max_temp_celsius REAL NOT NULL,
    driver_name TEXT NOT NULL,
    driver_phone TEXT NOT NULL,
    active_status TEXT DEFAULT 'IN_TRANSIT'
);

CREATE TABLE incident_alerts (
    id TEXT PRIMARY KEY,
    vehicle_id TEXT NOT NULL,
    breach_type TEXT NOT NULL, -- OVERHEAT, FREEZE_RISK, SENSOR_OFFLINE
    recorded_value REAL NOT NULL,
    alert_sent_to TEXT NOT NULL,
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES logistics_vehicles(id)
);""",
            json.dumps([
                {"q": "Why use MQTT instead of HTTP REST API for IoT devices?", "a": "HTTP headers create high network overhead (hundreds of bytes per request), requires creating TCP handshakes repeatedly, and drains microcontroller batteries. MQTT is an ultra-lightweight binary protocol with a 2-byte fixed header, keep-alive heartbeats, and Quality of Service (QoS) levels designed specifically for unreliable cellular networks."},
                {"q": "What happens if the truck drives through a rural area with no cellular connectivity for 30 minutes?", "a": "The ESP32 firmware utilizes on-board SPI Flash or SD card storage to buffer readings with local RTC timestamps. Once 4G connectivity restores, the device replays the buffered payloads in order with QoS 1."},
                {"q": "How does InfluxDB handle storage when sensors generate millions of rows per month?", "a": "InfluxDB uses Retention Policies and Continuous Queries (Downsampling). For example: retain raw 10-second data for 7 days, downsample to 5-minute averages for 30 days, and retain 1-hour averages indefinitely, reducing storage by 95%."}
            ]),
            json.dumps([
                {"phase": "Phase 1: Sensor Simulation", "desc": "Write Python script generating realistic temperature fluctuations simulating highway transport."},
                {"phase": "Phase 2: MQTT & InfluxDB Pipeline", "desc": "Set up Mosquitto broker and ingest streaming data into InfluxDB bucket."},
                {"phase": "Phase 3: Alert Triggering", "desc": "Implement threshold breach detector and hook up Twilio / WhatsApp alert simulator."},
                {"phase": "Phase 4: Grafana Telemetry Dashboard", "desc": "Create live Grafana dashboard tracking truck temperatures, battery levels, and route map."}
            ]),
            "https://github.com/eclipse/mosquitto",
            82,
            0
        )
    ]

    cursor.executemany("""
        INSERT INTO projects (
            id, title, tagline, level, domain, problem_statement,
            target_audience, tech_stack, architecture_diagram, components,
            data_flow, database_schema, interview_qa, milestones,
            github_starter_url, stars, featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, projects)
    conn.commit()


def format_project_row(row):
    d = dict(row)

    # Safely decode JSON fields
    for field in ["tech_stack", "components", "data_flow", "interview_qa", "milestones"]:
        val = d.get(field)
        if isinstance(val, str):
            try:
                d[field] = json.loads(val)
            except Exception:
                d[field] = []
        elif val is None:
            d[field] = []

    # Provide alias keys for frontend convenience
    d["stack"] = d.get("tech_stack", [])
    d["diagram"] = d.get("architecture_diagram", "")
    d["schema"] = d.get("database_schema", "")
    d["qa"] = d.get("interview_qa", [])
    return d


def get_all_projects(level=None, domain=None, search=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM projects WHERE 1=1"
    params = []

    if level and level.lower() not in ["all", "all levels"]:
        query += " AND LOWER(level) = LOWER(?)"
        params.append(level)

    if domain and domain.lower() not in ["all", "all domains"]:
        query += " AND LOWER(domain) LIKE ?"
        params.append(f"%{domain.lower()}%")

    if search:
        search_pattern = f"%{search.lower()}%"
        query += """ AND (
            LOWER(title) LIKE ? OR 
            LOWER(tagline) LIKE ? OR 
            LOWER(problem_statement) LIKE ? OR 
            LOWER(tech_stack) LIKE ? OR
            LOWER(domain) LIKE ?
        )"""
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern, search_pattern])

    query += " ORDER BY featured DESC, stars DESC, created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [format_project_row(r) for r in rows]


def get_project_by_id(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return format_project_row(row)
    return None


def add_project(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    proj_id = f"proj-{int(datetime.now().timestamp() * 1000)}"

    tech_stack = data.get("tech_stack") or data.get("stack") or ["React", "Node.js"]
    if isinstance(tech_stack, str):
        tech_stack = [s.strip() for s in tech_stack.split(",") if s.strip()]
    tech_stack_json = json.dumps(tech_stack)

    components = data.get("components") or []
    if isinstance(components, str):
        try:
            components = json.loads(components)
        except Exception:
            components = [{"name": "Core Service", "role": components, "tech": "Standard"}]
    components_json = json.dumps(components)

    data_flow = data.get("data_flow") or []
    if isinstance(data_flow, str):
        try:
            data_flow = json.loads(data_flow)
        except Exception:
            data_flow = [s.strip() for s in data_flow.split("\n") if s.strip()]
    data_flow_json = json.dumps(data_flow)

    interview_qa = data.get("interview_qa") or data.get("qa") or []
    if isinstance(interview_qa, str):
        try:
            interview_qa = json.loads(interview_qa)
        except Exception:
            interview_qa = []
    interview_qa_json = json.dumps(interview_qa)

    milestones = data.get("milestones") or []
    if isinstance(milestones, str):
        try:
            milestones = json.loads(milestones)
        except Exception:
            milestones = [{"phase": "Phase 1", "desc": milestones}]
    milestones_json = json.dumps(milestones)

    tagline = data.get("tagline") or data.get("summary") or "Production-grade distributed system blueprint"
    arch_diagram = data.get("architecture_diagram") or data.get("diagram") or data.get("system_diagram") or "[Client Web/Mobile] ---> [API Gateway / Proxy] ---> [Microservices & Queue] ---> [PostgreSQL / Redis]"
    db_schema = data.get("database_schema") or data.get("schema") or data.get("db_schema") or "-- Primary schema\nCREATE TABLE core_records (\n  id UUID PRIMARY KEY,\n  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()\n);"
    github_starter = data.get("github_starter_url") or data.get("github_sample") or "https://github.com"

    if not components:
        components = [
            {"name": "Client Interface", "role": "Interactive user dashboard and realtime subscriber", "tech": tech_stack[0] if tech_stack else "React"},
            {"name": "Backend Service", "role": "Business logic execution, auth validation & event publishing", "tech": tech_stack[1] if len(tech_stack) > 1 else "Node.js / Go"},
            {"name": "Data Storage / Cache", "role": "Persistent state with indexed lookups & cache tier", "tech": tech_stack[2] if len(tech_stack) > 2 else "PostgreSQL"}
        ]
        components_json = json.dumps(components)

    if not data_flow:
        data_flow = [
            "Client issues authenticated request payload over HTTPS / WebSocket.",
            "API Gateway rate-limits, authorizes JWT token, and delegates to service cluster.",
            "Backend performs domain transaction, persists data, and invalidates cache keys."
        ]
        data_flow_json = json.dumps(data_flow)

    if not milestones:
        milestones = [
            {"phase": "Phase 1", "desc": "Design schema, project scaffolding, and setup local Docker compose environment."},
            {"phase": "Phase 2", "desc": "Implement core business logic endpoints and integration test suite."},
            {"phase": "Phase 3", "desc": "Setup caching, background asynchronous worker, and connection pooling."},
            {"phase": "Phase 4", "desc": "Benchmarking with k6/wrk, CI/CD pipeline, and public documentation deployment."}
        ]
        milestones_json = json.dumps(milestones)

    cursor.execute("""
        INSERT INTO projects (
            id, title, tagline, level, domain, problem_statement,
            target_audience, tech_stack, architecture_diagram, components,
            data_flow, database_schema, interview_qa, milestones,
            github_starter_url, stars, featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        proj_id,
        data.get("title", "Untitled Architecture Blueprint"),
        tagline,
        data.get("level", "Intermediate"),
        data.get("domain", "Full-Stack"),
        data.get("problem_statement", ""),
        data.get("target_audience", "Engineering Students & Freshers"),
        tech_stack_json,
        arch_diagram,
        components_json,
        data_flow_json,
        db_schema,
        interview_qa_json,
        milestones_json,
        github_starter,
        0,
        1 if data.get("featured") else 0
    ))
    conn.commit()
    conn.close()
    return proj_id


def get_saved_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT project_id FROM saved_projects ORDER BY saved_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [r["project_id"] for r in rows]


def toggle_saved_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT project_id FROM saved_projects WHERE project_id = ?", (project_id,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute("DELETE FROM saved_projects WHERE project_id = ?", (project_id,))
        saved = False
    else:
        cursor.execute("INSERT INTO saved_projects (project_id) VALUES (?)", (project_id,))
        saved = True
    conn.commit()
    conn.close()
    return saved

