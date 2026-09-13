// CODE MIRCHI - Complete 4-Year & 8-Semester Degree Roadmaps Data
const defaultDegrees = [
  {
    "id": "btech_cse",
    "name": "B.Tech CSE",
    "full_title": "Computer Science & Engineering",
    "description": "Core software engineering, algorithms, system design, and placement excellence.",
    "icon": "\u26a1",
    "duration_years": 4,
    "semesters_count": 8
  },
  {
    "id": "btech_aiml",
    "name": "B.Tech AI & ML",
    "full_title": "Artificial Intelligence & Machine Learning",
    "description": "Mathematics for ML, neural networks, computer vision, NLP, and intelligent systems.",
    "icon": "\ud83e\udde0",
    "duration_years": 4,
    "semesters_count": 8
  },
  {
    "id": "btech_it",
    "name": "B.Tech IT",
    "full_title": "Information Technology",
    "description": "Enterprise web architectures, cloud engineering, cybersecurity, and databases.",
    "icon": "\ud83c\udf10",
    "duration_years": 4,
    "semesters_count": 8
  },
  {
    "id": "bca_cs",
    "name": "BCA / B.Sc CS",
    "full_title": "Computer Applications & Science",
    "description": "Hands-on application development, modern stacks, industry projects, and off-campus preparation.",
    "icon": "\ud83d\udcbb",
    "duration_years": 4,
    "semesters_count": 8
  },
  {
    "id": "btech_ece",
    "name": "B.Tech ECE",
    "full_title": "Electronics & Communication",
    "description": "C/C++, embedded systems, IoT devices, microcontrollers, and hardware-software integration.",
    "icon": "\ud83d\udd0c",
    "duration_years": 4,
    "semesters_count": 8
  }
];

const defaultRoadmaps = {
  "btech_cse": {
    "degree": {
      "id": "btech_cse",
      "name": "B.Tech CSE",
      "full_title": "Computer Science & Engineering",
      "description": "Core software engineering, algorithms, system design, and placement excellence.",
      "icon": "\u26a1",
      "duration_years": 4,
      "semesters_count": 8
    },
    "semesters": [
      {
        "id": "btech_cse-sem-1",
        "year": 1,
        "semester_number": 1,
        "title": "Programming Foundations & The Command Line",
        "focus_areas": [
          "C / C++ Basics",
          "Linux & Bash",
          "Git & GitHub",
          "Engineering Math I"
        ],
        "academic_core": "Calculus, Engineering Physics, Fundamentals of Programming in C/C++, Digital Logic.",
        "industry_prep": "Terminal navigation, Git commit workflows, GitHub profile setup, solving 30 problems on HackerRank/LeetCode Easy.",
        "milestone": "Build a command-line utility or text-based game in C/C++ and push to GitHub.",
        "tasks": [
          {
            "id": "btech_cse-sem-1-task-0",
            "order": 1,
            "text": "Install VS Code, GCC/Clang, Git, and a Linux environment (WSL or native)",
            "category": "Code",
            "completed": true
          },
          {
            "id": "btech_cse-sem-1-task-1",
            "order": 2,
            "text": "Master variables, pointers, memory allocation, loops, and functions in C",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-1-task-2",
            "order": 3,
            "text": "Solve 25 beginner algorithmic problems on LeetCode/HackerRank",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-1-task-3",
            "order": 4,
            "text": "Push your first documented repository to GitHub with a proper README.md",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-1-task-4",
            "order": 5,
            "text": "Join your college coding club / ACM / IEEE student chapter",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 1,
        "progress_percent": 20
      },
      {
        "id": "btech_cse-sem-2",
        "year": 1,
        "semester_number": 2,
        "title": "Object-Oriented Programming & Web Starters",
        "focus_areas": [
          "OOP Concepts",
          "Data Structures Basics",
          "HTML / CSS / JS",
          "Discrete Mathematics"
        ],
        "academic_core": "Object-Oriented Programming (Java or C++), Discrete Mathematics, Basic Data Structures (Arrays, Strings).",
        "industry_prep": "Build interactive browser interfaces, understand DOM manipulation, practice recursion and time complexity analysis.",
        "milestone": "Participate in your first college 24hr hackathon and build a working web app.",
        "tasks": [
          {
            "id": "btech_cse-sem-2-task-0",
            "order": 1,
            "text": "Master OOP: Classes, Inheritance, Polymorphism, Encapsulation in C++ or Java",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-2-task-1",
            "order": 2,
            "text": "Implement dynamic arrays, strings, linear search, and binary search from scratch",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-2-task-2",
            "order": 3,
            "text": "Build a responsive portfolio website with HTML5, CSS3, and JavaScript",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-2-task-3",
            "order": 4,
            "text": "Form a team of 3-4 peers and register for a fresher hackathon",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_cse-sem-2-task-4",
            "order": 5,
            "text": "Start a consistent problem-solving streak on LeetCode (reach 75 solved)",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_cse-sem-3",
        "year": 2,
        "semester_number": 3,
        "title": "Core Data Structures & Backend Fundamentals",
        "focus_areas": [
          "Linear DSA",
          "Node.js / Express or Python",
          "Relational Databases & SQL",
          "Computer Organization"
        ],
        "academic_core": "Data Structures (Linked Lists, Stacks, Queues, Binary Trees), Computer Organization & Architecture, DBMS.",
        "industry_prep": "Design relational schemas in PostgreSQL/MySQL, build RESTful APIs with CRUD operations and Postman testing.",
        "milestone": "Ship a full-stack CRUD application with persistent database and API endpoints.",
        "tasks": [
          {
            "id": "btech_cse-sem-3-task-0",
            "order": 1,
            "text": "Implement Linked Lists, Stacks, Queues, and Binary Search Trees with traversal logic",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-3-task-1",
            "order": 2,
            "text": "Learn SQL: schema design, foreign keys, normalization, joins, and indexing",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-3-task-2",
            "order": 3,
            "text": "Build a REST API using Express (Node.js) or FastAPI (Python) connected to PostgreSQL",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-3-task-3",
            "order": 4,
            "text": "Participate in Codeforces Div 3 / LeetCode Biweekly Contests regularly",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-3-task-4",
            "order": 5,
            "text": "Start writing short technical blogs or LinkedIn posts explaining DSA patterns",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_cse-sem-4",
        "year": 2,
        "semester_number": 4,
        "title": "Advanced DSA & Operating Systems",
        "focus_areas": [
          "Graphs & Trees",
          "Operating Systems",
          "Computer Networks",
          "Dynamic Programming"
        ],
        "academic_core": "Operating Systems (Processes, Threads, Semaphores, Deadlocks, Memory Management), Computer Networks (OSI, TCP/IP).",
        "industry_prep": "Graph algorithms (BFS, DFS, Dijkstra), Dynamic Programming memoization & tabulation, multi-threading in code.",
        "milestone": "Develop an authenticated full-stack application (JWT auth, database relationships, role-based access).",
        "tasks": [
          {
            "id": "btech_cse-sem-4-task-0",
            "order": 1,
            "text": "Master Tree traversals, BFS/DFS, Heaps, Priority Queues, and Disjoint Set Union",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-4-task-1",
            "order": 2,
            "text": "Solve the top 20 classic Dynamic Programming problems (Knapsack, LCS, LIS)",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-4-task-2",
            "order": 3,
            "text": "Understand OS internals: process scheduling, virtual memory, paging, and deadlocks",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-4-task-3",
            "order": 4,
            "text": "Build a web app with user authentication, JWT tokens, and secure passwords",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-4-task-4",
            "order": 5,
            "text": "Draft your first professional software engineer resume formatted with Overleaf/LaTeX",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_cse-sem-5",
        "year": 3,
        "semester_number": 5,
        "title": "Database Internals, Cloud & Open-Source",
        "focus_areas": [
          "Advanced DBMS",
          "Docker & Containers",
          "Open-Source / Hackathons",
          "Software Engineering"
        ],
        "academic_core": "Database Management Systems (ACID, Transactions, Concurrency Control, B+ Trees), Software Engineering Principles.",
        "industry_prep": "Containerization with Docker, deploying web applications to cloud (AWS/Vercel/Render), CI/CD pipelines.",
        "milestone": "Make your first meaningful open-source contribution to a public repository.",
        "tasks": [
          {
            "id": "btech_cse-sem-5-task-0",
            "order": 1,
            "text": "Containerize a full-stack project using Docker and write a multi-container Docker Compose file",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-5-task-1",
            "order": 2,
            "text": "Learn ACID properties, transaction isolation levels, and indexing strategies in DBMS",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-5-task-2",
            "order": 3,
            "text": "Submit your first Pull Request to an open-source GitHub project (Hacktoberfest or OSS orgs)",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-5-task-3",
            "order": 4,
            "text": "Compete in a national hackathon (Smart India Hackathon, Devfolio circuit, or MLH)",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_cse-sem-5-task-4",
            "order": 5,
            "text": "Reach 250+ DSA problems solved across LeetCode / Striver's SDE Sheet",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_cse-sem-6",
        "year": 3,
        "semester_number": 6,
        "title": "Low-Level Design, System Design & Summer Internships",
        "focus_areas": [
          "Low-Level Design (LLD)",
          "High-Level Design (HLD)",
          "Mock Interviews",
          "Summer Internship Search"
        ],
        "academic_core": "Design Patterns (Factory, Singleton, Observer, Strategy), Microservices vs Monolith, Cloud Architecture.",
        "industry_prep": "UML class diagrams, object-oriented design interviews, caching with Redis, rate limiters, message queues.",
        "milestone": "Secure an off-campus or on-campus summer internship or research assistantship.",
        "tasks": [
          {
            "id": "btech_cse-sem-6-task-0",
            "order": 1,
            "text": "Learn SOLID principles and implement classic design patterns in code",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-6-task-1",
            "order": 2,
            "text": "Practice designing parking lot, Tic-Tac-Toe, and URL shortener in LLD interviews",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-6-task-2",
            "order": 3,
            "text": "Study System Design: DNS, load balancers, caching (Redis), database sharding, CDN",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-6-task-3",
            "order": 4,
            "text": "Apply to 50+ summer internship openings through LinkedIn, Wellfound, and campus placement drives",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_cse-sem-6-task-4",
            "order": 5,
            "text": "Conduct 5 peer mock technical interviews with timed DSA and behavioral questions",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_cse-sem-7",
        "year": 4,
        "semester_number": 7,
        "title": "Placement Drives & Capstone Project Architecture",
        "focus_areas": [
          "Campus Placements",
          "SDE Interview Sprints",
          "Capstone Project Phase 1",
          "Core CS Revision"
        ],
        "academic_core": "Comprehensive revision of DBMS, OS, Computer Networks, OOP, and Aptitude / Quantitative Reasoning.",
        "industry_prep": "High-intensity coding test preparation, speed solving, deep-dive project explanations, behavioral leadership answers.",
        "milestone": "Clear technical rounds and secure full-time SDE job offer(s).",
        "tasks": [
          {
            "id": "btech_cse-sem-7-task-0",
            "order": 1,
            "text": "Revise top 100 interview questions in Operating Systems, DBMS, and Computer Networks",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-7-task-1",
            "order": 2,
            "text": "Practice speed coding 2 DSA problems daily under 45 minutes",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-7-task-2",
            "order": 3,
            "text": "Architect and begin building your Major Final Year Capstone Project with modern architecture",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-7-task-3",
            "order": 4,
            "text": "Attend campus placement drives and apply to off-campus SDE-1 hiring challenges",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_cse-sem-7-task-4",
            "order": 5,
            "text": "Master STAR method for behavioral and leadership interview rounds",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_cse-sem-8",
        "year": 4,
        "semester_number": 8,
        "title": "Capstone Deployment, Open Source & Career Launch",
        "focus_areas": [
          "Capstone Finalization",
          "Production Deployment",
          "Full-Time Transition",
          "Higher Studies / GATE"
        ],
        "academic_core": "Final Project Defense, Technical Documentation, Software Ethics, Career Launch or Higher Studies (GATE/GRE).",
        "industry_prep": "Production-grade deployment, automated tests, monitoring, performance benchmarking, transitioning to industry engineering.",
        "milestone": "Deploy production capstone with live users, present project defense, and graduate with distinction.",
        "tasks": [
          {
            "id": "btech_cse-sem-8-task-0",
            "order": 1,
            "text": "Deploy final year capstone project to production with live domain, CI/CD, and monitoring",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_cse-sem-8-task-1",
            "order": 2,
            "text": "Write comprehensive IEEE/college format project documentation and presentation slides",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_cse-sem-8-task-2",
            "order": 3,
            "text": "Read clean code principles and industry engineering best practices",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_cse-sem-8-task-3",
            "order": 4,
            "text": "Contribute back to junior tech communities and conduct college fresher mentorship",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_cse-sem-8-task-4",
            "order": 5,
            "text": "Prepare onboarding checklist: salary negotiations, tech stack ramp-up, and career goals",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      }
    ],
    "active_semester": {
      "id": "btech_cse-sem-1",
      "year": 1,
      "semester_number": 1,
      "title": "Programming Foundations & The Command Line",
      "focus_areas": [
        "C / C++ Basics",
        "Linux & Bash",
        "Git & GitHub",
        "Engineering Math I"
      ],
      "academic_core": "Calculus, Engineering Physics, Fundamentals of Programming in C/C++, Digital Logic.",
      "industry_prep": "Terminal navigation, Git commit workflows, GitHub profile setup, solving 30 problems on HackerRank/LeetCode Easy.",
      "milestone": "Build a command-line utility or text-based game in C/C++ and push to GitHub.",
      "tasks": [
        {
          "id": "btech_cse-sem-1-task-0",
          "order": 1,
          "text": "Install VS Code, GCC/Clang, Git, and a Linux environment (WSL or native)",
          "category": "Code",
          "completed": true
        },
        {
          "id": "btech_cse-sem-1-task-1",
          "order": 2,
          "text": "Master variables, pointers, memory allocation, loops, and functions in C",
          "category": "Theory",
          "completed": false
        },
        {
          "id": "btech_cse-sem-1-task-2",
          "order": 3,
          "text": "Solve 25 beginner algorithmic problems on LeetCode/HackerRank",
          "category": "Code",
          "completed": false
        },
        {
          "id": "btech_cse-sem-1-task-3",
          "order": 4,
          "text": "Push your first documented repository to GitHub with a proper README.md",
          "category": "Ship",
          "completed": false
        },
        {
          "id": "btech_cse-sem-1-task-4",
          "order": 5,
          "text": "Join your college coding club / ACM / IEEE student chapter",
          "category": "Career",
          "completed": false
        }
      ],
      "tasks_count": 5,
      "completed_count": 1,
      "progress_percent": 20
    },
    "overall_stats": {
      "total_tasks": 40,
      "completed_tasks": 1,
      "progress_percent": 2
    }
  },
  "btech_aiml": {
    "degree": {
      "id": "btech_aiml",
      "name": "B.Tech AI & ML",
      "full_title": "Artificial Intelligence & Machine Learning",
      "description": "Mathematics for ML, neural networks, computer vision, NLP, and intelligent systems.",
      "icon": "\ud83e\udde0",
      "duration_years": 4,
      "semesters_count": 8
    },
    "semesters": [
      {
        "id": "btech_aiml-sem-1",
        "year": 1,
        "semester_number": 1,
        "title": "Python Mastery & Mathematical Foundations",
        "focus_areas": [
          "Python for Dev",
          "Linear Algebra",
          "Linux & Git",
          "Calculus & Probability"
        ],
        "academic_core": "Linear Algebra (Matrices, Eigenvalues), Multivariable Calculus, Discrete Mathematics, Python Basics.",
        "industry_prep": "Python idiomatic scripting, NumPy vectorization, Git version control, setting up Jupyter lab environments.",
        "milestone": "Build a CLI data analysis script that processes CSV datasets and plots charts.",
        "tasks": [
          {
            "id": "btech_aiml-sem-1-task-0",
            "order": 1,
            "text": "Master modern Python: list comprehensions, generators, decorators, and OOP",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-1-task-1",
            "order": 2,
            "text": "Study Linear Algebra: vectors, matrix transformations, dot products, and eigenvalues",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-1-task-2",
            "order": 3,
            "text": "Learn NumPy and Pandas for manipulating high-dimensional tabular data",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-1-task-3",
            "order": 4,
            "text": "Build and document a Python data extraction and visualization utility on GitHub",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-1-task-4",
            "order": 5,
            "text": "Join AI/Data science student communities and Kaggle forums",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_aiml-sem-2",
        "year": 1,
        "semester_number": 2,
        "title": "Exploratory Data Analysis & Scientific Computing",
        "focus_areas": [
          "Pandas & Matplotlib",
          "Probability & Statistics",
          "Data Scraping",
          "Data Structures in Python"
        ],
        "academic_core": "Probability Distributions, Hypothesis Testing, Central Limit Theorem, Data Structures & Algorithms.",
        "industry_prep": "Data cleaning, exploratory data analysis (EDA), Seaborn visualizations, web scraping with BeautifulSoup.",
        "milestone": "Publish a complete Kaggle EDA notebook with clear insights and narrative.",
        "tasks": [
          {
            "id": "btech_aiml-sem-2-task-0",
            "order": 1,
            "text": "Master statistical concepts: mean, variance, Bayes theorem, distributions, p-values",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-2-task-1",
            "order": 2,
            "text": "Build custom data visualization dashboards using Seaborn and Plotly",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-2-task-2",
            "order": 3,
            "text": "Implement classic search and sorting algorithms in Python",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-2-task-3",
            "order": 4,
            "text": "Complete an end-to-end Exploratory Data Analysis project on a real-world dataset",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-2-task-4",
            "order": 5,
            "text": "Participate in beginner Kaggle tabular competitions",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_aiml-sem-3",
        "year": 2,
        "semester_number": 3,
        "title": "Classical Machine Learning Algorithms",
        "focus_areas": [
          "Scikit-Learn",
          "Regression & Classification",
          "Feature Engineering",
          "Relational Databases & SQL"
        ],
        "academic_core": "Linear/Logistic Regression, Decision Trees, Random Forests, SVM, k-Means, PCA, SQL for data retrieval.",
        "industry_prep": "Model evaluation metrics (ROC-AUC, F1, precision, recall), hyperparameter tuning (GridSearchCV), cross-validation.",
        "milestone": "Deploy a trained Scikit-Learn prediction model as an interactive Streamlit web app.",
        "tasks": [
          {
            "id": "btech_aiml-sem-3-task-0",
            "order": 1,
            "text": "Derive gradient descent and cost functions mathematically for linear models",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-3-task-1",
            "order": 2,
            "text": "Train and evaluate models using Scikit-Learn pipelines",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-3-task-2",
            "order": 3,
            "text": "Master SQL queries for data analytics: window functions, aggregations, and subqueries",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-3-task-3",
            "order": 4,
            "text": "Build and deploy an interactive ML web application on Streamlit Cloud",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-3-task-4",
            "order": 5,
            "text": "Solve 100+ Python DSA questions focusing on arrays, hashing, and trees",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_aiml-sem-4",
        "year": 2,
        "semester_number": 4,
        "title": "Deep Learning Foundations & PyTorch",
        "focus_areas": [
          "PyTorch",
          "Neural Networks",
          "Backpropagation",
          "Computer Vision Basics"
        ],
        "academic_core": "Artificial Neural Networks (ANN), Convolutional Neural Networks (CNN), Optimization (Adam, SGD), Tensor Math.",
        "industry_prep": "PyTorch tensor operations, custom DataLoader, training loops, transfer learning with ResNet.",
        "milestone": "Build and train an image classification model and containerize the inference API.",
        "tasks": [
          {
            "id": "btech_aiml-sem-4-task-0",
            "order": 1,
            "text": "Understand forward pass, backpropagation, and chain rule mathematically",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-4-task-1",
            "order": 2,
            "text": "Train deep CNNs using PyTorch on GPU (Google Colab / Kaggle)",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-4-task-2",
            "order": 3,
            "text": "Apply data augmentation and transfer learning using torchvision models",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-4-task-3",
            "order": 4,
            "text": "Deploy a computer vision model using FastAPI and Docker",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-4-task-4",
            "order": 5,
            "text": "Write a detailed blog post breaking down your neural network architecture",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_aiml-sem-5",
        "year": 3,
        "semester_number": 5,
        "title": "Natural Language Processing & Transformers",
        "focus_areas": [
          "Hugging Face",
          "NLP & Transformers",
          "Embeddings & Vectors",
          "MLOps Basics"
        ],
        "academic_core": "Word Embeddings (Word2Vec), Recurrent Networks (LSTM, GRU), Self-Attention Mechanisms, Transformer Architectures.",
        "industry_prep": "Fine-tuning BERT and GPT models with Hugging Face Transformers, vector databases (Chroma/Pinecone).",
        "milestone": "Build a Retrieval-Augmented Generation (RAG) assistant using LangChain/LlamaIndex and Hugging Face.",
        "tasks": [
          {
            "id": "btech_aiml-sem-5-task-0",
            "order": 1,
            "text": "Study Transformer architecture: query, key, value attention equations and multi-head attention",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-5-task-1",
            "order": 2,
            "text": "Build a document question-answering system using LLM embeddings and vector search",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-5-task-2",
            "order": 3,
            "text": "Track model training experiments using MLflow or Weights & Biases",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-5-task-3",
            "order": 4,
            "text": "Participate in an AI-focused national hackathon with working prototype",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-5-task-4",
            "order": 5,
            "text": "Reach 200+ DSA problems solved to ensure technical round readiness",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_aiml-sem-6",
        "year": 3,
        "semester_number": 6,
        "title": "MLOps, Scalable AI & Summer Internships",
        "focus_areas": [
          "MLOps Pipelines",
          "Model Serving & Docker",
          "System Design for ML",
          "Summer Internship Drives"
        ],
        "academic_core": "Model monitoring, drift detection, CI/CD for machine learning, scalable inference architecture, data privacy.",
        "industry_prep": "Dockerizing AI microservices, Triton/FastAPI serving, caching inference, low-latency prediction pipelines.",
        "milestone": "Secure an AI/ML Engineer, Data Scientist, or Data Analyst summer internship.",
        "tasks": [
          {
            "id": "btech_aiml-sem-6-task-0",
            "order": 1,
            "text": "Study Machine Learning System Design: streaming vs batch prediction, feature stores, caching",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-6-task-1",
            "order": 2,
            "text": "Build an automated CI/CD pipeline that retrains and tests model performance",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-6-task-2",
            "order": 3,
            "text": "Prepare your AI portfolio showcasing 3 distinct end-to-end deployed projects",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-6-task-3",
            "order": 4,
            "text": "Apply to 40+ AI/Data roles at startups and tech firms with custom cover letters",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-6-task-4",
            "order": 5,
            "text": "Conduct mock interviews covering ML theory, math derivations, and coding rounds",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_aiml-sem-7",
        "year": 4,
        "semester_number": 7,
        "title": "Generative AI, Large Models & Placement Drives",
        "focus_areas": [
          "Generative AI",
          "Agentic Workflows",
          "Campus Placements",
          "Major AI Capstone Phase 1"
        ],
        "academic_core": "Fine-tuning techniques (LoRA, QLoRA), Reinforcement Learning from Human Feedback (RLHF), Placement Prep.",
        "industry_prep": "Prompt engineering, multi-agent architectures (CrewAI, LangGraph), high-throughput inference optimization.",
        "milestone": "Clear campus placement or off-campus technical rounds for Machine Learning roles.",
        "tasks": [
          {
            "id": "btech_aiml-sem-7-task-0",
            "order": 1,
            "text": "Learn parameter-efficient fine-tuning (PEFT/LoRA) on custom datasets",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-7-task-1",
            "order": 2,
            "text": "Implement an autonomous AI agent workflow solving multi-step tasks",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-7-task-2",
            "order": 3,
            "text": "Revise core computer science: OS, DBMS, SQL, and algorithms for placement interviews",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-7-task-3",
            "order": 4,
            "text": "Participate actively in placement hiring tests and coding rounds",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-7-task-4",
            "order": 5,
            "text": "Scope out your final year AI research capstone project with measurable benchmarks",
            "category": "Ship",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_aiml-sem-8",
        "year": 4,
        "semester_number": 8,
        "title": "Research Publication, Capstone Deployment & Career Launch",
        "focus_areas": [
          "AI Capstone Defense",
          "Research Paper",
          "Production Deployment",
          "Full-Time Transition"
        ],
        "academic_core": "Model explainability (SHAP, LIME), AI Safety & Ethics, Research Paper Writing, Career Launch.",
        "industry_prep": "Deploying large models to cloud endpoints, cost optimization, latency quantization (ONNX, TensorRT).",
        "milestone": "Complete final capstone defense, publish research or release open-weights model, and launch career.",
        "tasks": [
          {
            "id": "btech_aiml-sem-8-task-0",
            "order": 1,
            "text": "Complete production deployment of Capstone AI system with user metrics and monitoring",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-8-task-1",
            "order": 2,
            "text": "Draft and submit a research paper to a recognized conference or arXiv preprint",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-8-task-2",
            "order": 3,
            "text": "Document your model weights, dataset cards, and demo on Hugging Face Spaces",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-8-task-3",
            "order": 4,
            "text": "Mentor 1st and 2nd year students on AI roadmaps and hackathons",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_aiml-sem-8-task-4",
            "order": 5,
            "text": "Ramp up on your hiring company's production tech stack before day one",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      }
    ],
    "active_semester": {
      "id": "btech_aiml-sem-1",
      "year": 1,
      "semester_number": 1,
      "title": "Python Mastery & Mathematical Foundations",
      "focus_areas": [
        "Python for Dev",
        "Linear Algebra",
        "Linux & Git",
        "Calculus & Probability"
      ],
      "academic_core": "Linear Algebra (Matrices, Eigenvalues), Multivariable Calculus, Discrete Mathematics, Python Basics.",
      "industry_prep": "Python idiomatic scripting, NumPy vectorization, Git version control, setting up Jupyter lab environments.",
      "milestone": "Build a CLI data analysis script that processes CSV datasets and plots charts.",
      "tasks": [
        {
          "id": "btech_aiml-sem-1-task-0",
          "order": 1,
          "text": "Master modern Python: list comprehensions, generators, decorators, and OOP",
          "category": "Code",
          "completed": false
        },
        {
          "id": "btech_aiml-sem-1-task-1",
          "order": 2,
          "text": "Study Linear Algebra: vectors, matrix transformations, dot products, and eigenvalues",
          "category": "Theory",
          "completed": false
        },
        {
          "id": "btech_aiml-sem-1-task-2",
          "order": 3,
          "text": "Learn NumPy and Pandas for manipulating high-dimensional tabular data",
          "category": "Code",
          "completed": false
        },
        {
          "id": "btech_aiml-sem-1-task-3",
          "order": 4,
          "text": "Build and document a Python data extraction and visualization utility on GitHub",
          "category": "Ship",
          "completed": false
        },
        {
          "id": "btech_aiml-sem-1-task-4",
          "order": 5,
          "text": "Join AI/Data science student communities and Kaggle forums",
          "category": "Career",
          "completed": false
        }
      ],
      "tasks_count": 5,
      "completed_count": 0,
      "progress_percent": 0
    },
    "overall_stats": {
      "total_tasks": 40,
      "completed_tasks": 0,
      "progress_percent": 0
    }
  },
  "btech_it": {
    "degree": {
      "id": "btech_it",
      "name": "B.Tech IT",
      "full_title": "Information Technology",
      "description": "Enterprise web architectures, cloud engineering, cybersecurity, and databases.",
      "icon": "\ud83c\udf10",
      "duration_years": 4,
      "semesters_count": 8
    },
    "semesters": [
      {
        "id": "btech_it-sem-1",
        "year": 1,
        "semester_number": 1,
        "title": "IT Foundations, Scripting & Terminal",
        "focus_areas": [
          "C / Python",
          "Linux System Administration",
          "Git & GitHub",
          "Web Architecture"
        ],
        "academic_core": "Fundamentals of Programming, Discrete Mathematics, Computer Hardware & Peripherals.",
        "industry_prep": "Bash scripting, Linux permissions, package management, Git workflows, HTTP protocol fundamentals.",
        "milestone": "Write a bash automation script that backups directories and monitors system resources.",
        "tasks": [
          {
            "id": "btech_it-sem-1-task-0",
            "order": 1,
            "text": "Set up a dual-boot or virtualized Linux development environment",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-1-task-1",
            "order": 2,
            "text": "Master C or Python programming fundamentals: control flow, functions, memory",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-1-task-2",
            "order": 3,
            "text": "Write 5 useful shell scripts for automating local workstation tasks",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-1-task-3",
            "order": 4,
            "text": "Push clean code to GitHub and write markdown documentation",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-1-task-4",
            "order": 5,
            "text": "Join IT student chapters and attend cybersecurity / web workshops",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_it-sem-2",
        "year": 1,
        "semester_number": 2,
        "title": "Modern Web Development & Networking Basics",
        "focus_areas": [
          "HTML5 / CSS3 / JavaScript",
          "Computer Networks Basics",
          "OOP in Java",
          "Data Structures"
        ],
        "academic_core": "Object-Oriented Programming (Java), Data Structures (Arrays, Lists, Stacks), Network Topologies.",
        "industry_prep": "Semantic HTML, Flexbox/Grid CSS, JavaScript asynchronous programming (Promises, async/await).",
        "milestone": "Build a responsive web application that fetches data from public REST APIs.",
        "tasks": [
          {
            "id": "btech_it-sem-2-task-0",
            "order": 1,
            "text": "Master OOP principles and write modular Java code",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-2-task-1",
            "order": 2,
            "text": "Learn Network basics: IP addresses, subnetting, DNS, TCP vs UDP",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-2-task-2",
            "order": 3,
            "text": "Build a responsive multi-page web application with API integrations",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-2-task-3",
            "order": 4,
            "text": "Solve 50 coding problems focusing on string and array manipulation",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-2-task-4",
            "order": 5,
            "text": "Compete in your first 24-hour campus hackathon",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_it-sem-3",
        "year": 2,
        "semester_number": 3,
        "title": "Enterprise Databases & Backend Engineering",
        "focus_areas": [
          "SQL & Relational DBs",
          "Node.js / Express or Django",
          "Non-Linear DSA",
          "Software Engineering"
        ],
        "academic_core": "Database Management Systems, Software Engineering Methodologies (Agile, Scrum), Data Structures (Trees, Queues).",
        "industry_prep": "Relational database design, 3NF normalization, RESTful API architecture, postman automation tests.",
        "milestone": "Design and build an enterprise-grade inventory or ticketing backend system.",
        "tasks": [
          {
            "id": "btech_it-sem-3-task-0",
            "order": 1,
            "text": "Implement Tree and Graph data structures and traversal algorithms",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-3-task-1",
            "order": 2,
            "text": "Write complex SQL queries: joins, group by, transactions, and store procedures",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-3-task-2",
            "order": 3,
            "text": "Build a robust backend API with role-based access control and database persistence",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-3-task-3",
            "order": 4,
            "text": "Participate in competitive programming contests on LeetCode/HackerEarth",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-3-task-4",
            "order": 5,
            "text": "Document API endpoints with Swagger / OpenAPI specifications",
            "category": "Ship",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_it-sem-4",
        "year": 2,
        "semester_number": 4,
        "title": "Operating Systems, Cloud Basics & DevOps",
        "focus_areas": [
          "Linux Administration",
          "Operating Systems",
          "AWS / Cloud Basics",
          "Docker Containers"
        ],
        "academic_core": "Operating Systems (Virtual Memory, Scheduling, Deadlocks), Cloud Computing Fundamentals.",
        "industry_prep": "Deploying virtual machines on AWS EC2, S3 bucket management, Docker containerization, reverse proxies (Nginx).",
        "milestone": "Deploy a containerized web application behind an Nginx reverse proxy on a cloud VPS.",
        "tasks": [
          {
            "id": "btech_it-sem-4-task-0",
            "order": 1,
            "text": "Study OS core concepts: process synchronization, memory paging, and file systems",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-4-task-1",
            "order": 2,
            "text": "Learn Docker: write Dockerfiles, manage volumes, and configure container networks",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-4-task-2",
            "order": 3,
            "text": "Launch a cloud instance on AWS/GCP, configure security groups and deploy an app",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-4-task-3",
            "order": 4,
            "text": "Solve 50 intermediate DSA problems on Dynamic Programming and Graphs",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-4-task-4",
            "order": 5,
            "text": "Update your tech resume with live deployed project URLs",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_it-sem-5",
        "year": 3,
        "semester_number": 5,
        "title": "Cloud Architecture, CI/CD & Cybersecurity",
        "focus_areas": [
          "CI/CD Pipelines",
          "Information Security",
          "Microservices",
          "Advanced Databases (NoSQL)"
        ],
        "academic_core": "Information Security & Cryptography, Web Application Vulnerabilities (OWASP Top 10), Distributed Systems.",
        "industry_prep": "GitHub Actions CI/CD pipelines, MongoDB/Redis integration, securing web apps with HTTPS/CORS, penetration testing basics.",
        "milestone": "Build an automated CI/CD pipeline that tests, builds, and deploys your code on git push.",
        "tasks": [
          {
            "id": "btech_it-sem-5-task-0",
            "order": 1,
            "text": "Implement automated testing and deployment using GitHub Actions",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-5-task-1",
            "order": 2,
            "text": "Study cryptography: symmetric/asymmetric encryption, hashing, SSL/TLS certificates",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-5-task-2",
            "order": 3,
            "text": "Audit a web application for OWASP Top 10 vulnerabilities (XSS, SQLi, CSRF)",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-5-task-3",
            "order": 4,
            "text": "Integrate Redis caching to speed up high-latency database queries",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-5-task-4",
            "order": 5,
            "text": "Compete in a national hackathon focusing on cloud or security",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_it-sem-6",
        "year": 3,
        "semester_number": 6,
        "title": "System Design, Infrastructure & Summer Internships",
        "focus_areas": [
          "System Design (HLD)",
          "Kubernetes Basics",
          "Mock Interviews",
          "Summer Internship Drives"
        ],
        "academic_core": "High-Level System Design, Load Balancing, Microservices Communication, Reliability Engineering.",
        "industry_prep": "Designing scalable architectures: messaging queues (RabbitMQ/Kafka), caching layers, database replication.",
        "milestone": "Secure an IT, Cloud Engineer, DevOps, or Software Engineering summer internship.",
        "tasks": [
          {
            "id": "btech_it-sem-6-task-0",
            "order": 1,
            "text": "Learn System Design fundamentals: horizontal scaling, CDN, database replication",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-6-task-1",
            "order": 2,
            "text": "Practice designing scalable platforms: Netflix, WhatsApp, or E-commerce backend",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-6-task-2",
            "order": 3,
            "text": "Learn basic Kubernetes concepts: pods, deployments, services, and ingress",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-6-task-3",
            "order": 4,
            "text": "Apply to 50+ IT/Software/DevOps internship openings across industry channels",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_it-sem-6-task-4",
            "order": 5,
            "text": "Take mock technical interviews on core networking, OS, and algorithms",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_it-sem-7",
        "year": 4,
        "semester_number": 7,
        "title": "Campus Placements, Enterprise Systems & Capstone Phase 1",
        "focus_areas": [
          "Campus Placements",
          "Core IT Revision",
          "Major Capstone Project",
          "Interview Preparation"
        ],
        "academic_core": "Full revision of Computer Networks, DBMS, OS, Cloud Services, and Quantitative Aptitude.",
        "industry_prep": "Technical interview sprints, architectural deep dives, behavioral questions, coding problem solving.",
        "milestone": "Clear on-campus or off-campus recruitment drives for high-paying engineering roles.",
        "tasks": [
          {
            "id": "btech_it-sem-7-task-0",
            "order": 1,
            "text": "Revise high-yield questions in Computer Networks, SQL, OS, and System Design",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-7-task-1",
            "order": 2,
            "text": "Solve 2 interview DSA problems daily under timed constraints",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_it-sem-7-task-2",
            "order": 3,
            "text": "Begin implementing your Major IT Capstone project with cloud infrastructure",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-7-task-3",
            "order": 4,
            "text": "Attend placement coding assessments and technical interviews",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_it-sem-7-task-4",
            "order": 5,
            "text": "Master answers for behavioral, situational, and conflict resolution rounds",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_it-sem-8",
        "year": 4,
        "semester_number": 8,
        "title": "Capstone Deployment, Industry Certification & Career Launch",
        "focus_areas": [
          "Capstone Defense",
          "Cloud Certification",
          "Production Rollout",
          "Career Transition"
        ],
        "academic_core": "Capstone Project Evaluation, Enterprise Architecture, Software Maintenance, Professional Ethics.",
        "industry_prep": "Full production monitoring with Prometheus/Grafana, cloud certification prep (AWS Solutions Architect / Cloud Practitioner).",
        "milestone": "Present final capstone defense, earn an industry cloud credential, and onboard into full-time role.",
        "tasks": [
          {
            "id": "btech_it-sem-8-task-0",
            "order": 1,
            "text": "Complete production deployment of your Capstone system with uptime monitoring",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_it-sem-8-task-1",
            "order": 2,
            "text": "Prepare for and complete an AWS Certified Cloud Practitioner or Solutions Architect exam",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_it-sem-8-task-2",
            "order": 3,
            "text": "Write comprehensive technical handover and system architecture documentation",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_it-sem-8-task-3",
            "order": 4,
            "text": "Mentor junior students on cloud computing, DevOps, and placements",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_it-sem-8-task-4",
            "order": 5,
            "text": "Prepare transition plan for corporate engineering onboarding",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      }
    ],
    "active_semester": {
      "id": "btech_it-sem-1",
      "year": 1,
      "semester_number": 1,
      "title": "IT Foundations, Scripting & Terminal",
      "focus_areas": [
        "C / Python",
        "Linux System Administration",
        "Git & GitHub",
        "Web Architecture"
      ],
      "academic_core": "Fundamentals of Programming, Discrete Mathematics, Computer Hardware & Peripherals.",
      "industry_prep": "Bash scripting, Linux permissions, package management, Git workflows, HTTP protocol fundamentals.",
      "milestone": "Write a bash automation script that backups directories and monitors system resources.",
      "tasks": [
        {
          "id": "btech_it-sem-1-task-0",
          "order": 1,
          "text": "Set up a dual-boot or virtualized Linux development environment",
          "category": "Code",
          "completed": false
        },
        {
          "id": "btech_it-sem-1-task-1",
          "order": 2,
          "text": "Master C or Python programming fundamentals: control flow, functions, memory",
          "category": "Theory",
          "completed": false
        },
        {
          "id": "btech_it-sem-1-task-2",
          "order": 3,
          "text": "Write 5 useful shell scripts for automating local workstation tasks",
          "category": "Ship",
          "completed": false
        },
        {
          "id": "btech_it-sem-1-task-3",
          "order": 4,
          "text": "Push clean code to GitHub and write markdown documentation",
          "category": "Ship",
          "completed": false
        },
        {
          "id": "btech_it-sem-1-task-4",
          "order": 5,
          "text": "Join IT student chapters and attend cybersecurity / web workshops",
          "category": "Career",
          "completed": false
        }
      ],
      "tasks_count": 5,
      "completed_count": 0,
      "progress_percent": 0
    },
    "overall_stats": {
      "total_tasks": 40,
      "completed_tasks": 0,
      "progress_percent": 0
    }
  },
  "bca_cs": {
    "degree": {
      "id": "bca_cs",
      "name": "BCA / B.Sc CS",
      "full_title": "Computer Applications & Science",
      "description": "Hands-on application development, modern stacks, industry projects, and off-campus preparation.",
      "icon": "\ud83d\udcbb",
      "duration_years": 4,
      "semesters_count": 8
    },
    "semesters": [
      {
        "id": "bca_cs-sem-1",
        "year": 1,
        "semester_number": 1,
        "title": "Programming Fundamentals in C & Office Tools",
        "focus_areas": [
          "C Language",
          "Computer Fundamentals",
          "Git Basics",
          "Mathematical Foundations"
        ],
        "academic_core": "Computer Fundamentals, Programming in C, Problem Solving Techniques, Communication Skills.",
        "industry_prep": "Writing clean C programs, algorithm flowcharts, setting up code editors, creating a GitHub account.",
        "milestone": "Build a student report card or billing management CLI program in C.",
        "tasks": [
          {
            "id": "bca_cs-sem-1-task-0",
            "order": 1,
            "text": "Install code editor and learn C syntax: data types, loops, arrays, pointers",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-1-task-1",
            "order": 2,
            "text": "Understand computer architecture: CPU, memory, storage, and binary arithmetic",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-1-task-2",
            "order": 3,
            "text": "Build a menu-driven console application in C with file storage",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-1-task-3",
            "order": 4,
            "text": "Create your GitHub account and push your first project",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-1-task-4",
            "order": 5,
            "text": "Focus on developing strong English communication and technical vocabulary",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "bca_cs-sem-2",
        "year": 1,
        "semester_number": 2,
        "title": "Object-Oriented Programming in C++ & Web Design",
        "focus_areas": [
          "C++ / OOP",
          "HTML & CSS",
          "JavaScript Basics",
          "Data Structures Intro"
        ],
        "academic_core": "Object-Oriented Programming with C++, Web Technology Basics, Basic Data Structures.",
        "industry_prep": "C++ classes, objects, constructors, file handling, creating styled landing pages with HTML/CSS.",
        "milestone": "Design and deploy an interactive multi-page portfolio website on GitHub Pages.",
        "tasks": [
          {
            "id": "bca_cs-sem-2-task-0",
            "order": 1,
            "text": "Master C++ OOP: inheritance, function overloading, polymorphism",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-2-task-1",
            "order": 2,
            "text": "Learn HTML5 semantic tags and modern CSS styling with Flexbox",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-2-task-2",
            "order": 3,
            "text": "Add JavaScript interactivity for form validation and dynamic UI",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-2-task-3",
            "order": 4,
            "text": "Deploy your personal portfolio on GitHub Pages for free",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-2-task-4",
            "order": 5,
            "text": "Solve 30 beginner coding problems on HackerRank",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "bca_cs-sem-3",
        "year": 2,
        "semester_number": 3,
        "title": "Data Structures, Java & Relational Databases",
        "focus_areas": [
          "Java Programming",
          "Data Structures",
          "DBMS & SQL",
          "Web Scripting"
        ],
        "academic_core": "Core Java (Packages, Exceptions, Collections), Data Structures (Lists, Stacks, Queues), DBMS.",
        "industry_prep": "Java Swing/JavaFX or web app development, writing relational SQL queries, table normalization.",
        "milestone": "Build a desktop or web-based inventory/library management system with database connection.",
        "tasks": [
          {
            "id": "bca_cs-sem-3-task-0",
            "order": 1,
            "text": "Master Core Java: OOP, interfaces, exception handling, and ArrayLists",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-3-task-1",
            "order": 2,
            "text": "Implement stacks, queues, and linked lists in Java",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-3-task-2",
            "order": 3,
            "text": "Learn SQL: CREATE, INSERT, SELECT, JOIN, and database constraints",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-3-task-3",
            "order": 4,
            "text": "Build a complete database-backed application connected via JDBC or backend API",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-3-task-4",
            "order": 5,
            "text": "Participate in online coding challenges on LeetCode or GeeksforGeeks",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "bca_cs-sem-4",
        "year": 2,
        "semester_number": 4,
        "title": "Full-Stack Web Development & Operating Systems",
        "focus_areas": [
          "Node.js & Express",
          "MongoDB / NoSQL",
          "Operating Systems",
          "React Basics"
        ],
        "academic_core": "Operating Systems (Processes, Memory, File Systems), Web Frameworks, Database Systems.",
        "industry_prep": "Building RESTful APIs with Node.js and Express, connecting to MongoDB, building React UI components.",
        "milestone": "Create and deploy a full-stack MERN (MongoDB, Express, React, Node) application.",
        "tasks": [
          {
            "id": "bca_cs-sem-4-task-0",
            "order": 1,
            "text": "Study Operating System concepts: multitasking, memory management, file systems",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-4-task-1",
            "order": 2,
            "text": "Build backend REST APIs with Express and test them with Postman",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-4-task-2",
            "order": 3,
            "text": "Learn React fundamentals: components, props, state, and useEffect",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-4-task-3",
            "order": 4,
            "text": "Deploy full-stack project with frontend on Vercel and backend on Render",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-4-task-4",
            "order": 5,
            "text": "Create an updated resume highlighting live project links and GitHub repo",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "bca_cs-sem-5",
        "year": 3,
        "semester_number": 5,
        "title": "Python, Advanced Web & Internship Preparation",
        "focus_areas": [
          "Python for Dev",
          "Advanced React / Next.js",
          "Software Testing",
          "Internship Drives"
        ],
        "academic_core": "Python Programming, Software Engineering & Testing Methodologies, Cloud Fundamentals.",
        "industry_prep": "Modern frontend architectures, state management, building full-stack applications with Python or JavaScript.",
        "milestone": "Secure an off-campus web development, QA, or software engineering internship.",
        "tasks": [
          {
            "id": "bca_cs-sem-5-task-0",
            "order": 1,
            "text": "Learn Python scripting, dictionary/list operations, and utility libraries",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-5-task-1",
            "order": 2,
            "text": "Build an e-commerce or social media web application with search and filter features",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-5-task-2",
            "order": 3,
            "text": "Study software testing: unit tests, manual testing, test case documentation",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-5-task-3",
            "order": 4,
            "text": "Apply to 30+ internship opportunities on Internshala, Wellfound, and LinkedIn",
            "category": "Career",
            "completed": false
          },
          {
            "id": "bca_cs-sem-5-task-4",
            "order": 5,
            "text": "Practice 100+ DSA interview questions on arrays, strings, and trees",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "bca_cs-sem-6",
        "year": 3,
        "semester_number": 6,
        "title": "MCA / Placement Prep & Final Capstone Project",
        "focus_areas": [
          "Full-Time Job Search",
          "MCA Entrances (NIMCET) / Placements",
          "Capstone Project",
          "System Fundamentals"
        ],
        "academic_core": "Final Year Project Development, Core Computer Science Revision, Placement Preparation or MCA Entrance Prep.",
        "industry_prep": "Interview preparation, speed coding, mock technical interviews, deploying production capstone project.",
        "milestone": "Graduate with a placed job offer or top rank in MCA entrance examination.",
        "tasks": [
          {
            "id": "bca_cs-sem-6-task-0",
            "order": 1,
            "text": "Complete and polish your final year capstone project with clean code and documentation",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-6-task-1",
            "order": 2,
            "text": "If pursuing jobs: practice coding rounds, aptitude tests, and HR interview answers",
            "category": "Career",
            "completed": false
          },
          {
            "id": "bca_cs-sem-6-task-2",
            "order": 3,
            "text": "If pursuing MCA: solve NIMCET / state entrance exam previous year papers",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-6-task-3",
            "order": 4,
            "text": "Conduct mock interviews with peers focusing on project explanations",
            "category": "Career",
            "completed": false
          },
          {
            "id": "bca_cs-sem-6-task-4",
            "order": 5,
            "text": "Deploy all major projects to live URLs and ensure GitHub profile is polished",
            "category": "Ship",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "bca_cs-sem-7",
        "year": 4,
        "semester_number": 7,
        "title": "Advanced Software Engineering & Enterprise Stacks",
        "focus_areas": [
          "Enterprise Java / Spring Boot",
          "Cloud Deployment",
          "Placement Sprints",
          "Capstone Phase 1"
        ],
        "academic_core": "Enterprise Application Development, Cloud Architecture, Advanced Data Analytics.",
        "industry_prep": "Spring Boot or Django enterprise frameworks, microservices architecture, cloud deployment.",
        "milestone": "Build and deploy an enterprise-grade service with automated test coverage.",
        "tasks": [
          {
            "id": "bca_cs-sem-7-task-0",
            "order": 1,
            "text": "Learn Spring Boot or Django for enterprise-grade backend development",
            "category": "Code",
            "completed": false
          },
          {
            "id": "bca_cs-sem-7-task-1",
            "order": 2,
            "text": "Implement authentication, payment gateway integration, and email notifications",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-7-task-2",
            "order": 3,
            "text": "Revise DBMS, Operating Systems, and Networks for high-tier company interviews",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-7-task-3",
            "order": 4,
            "text": "Participate in off-campus hiring drives and tech challenges",
            "category": "Career",
            "completed": false
          },
          {
            "id": "bca_cs-sem-7-task-4",
            "order": 5,
            "text": "Solve 2 medium LeetCode problems daily",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "bca_cs-sem-8",
        "year": 4,
        "semester_number": 8,
        "title": "Major Capstone Defense & Industry Launch",
        "focus_areas": [
          "Capstone Defense",
          "Production Architecture",
          "Full-Time Transition",
          "Career Launch"
        ],
        "academic_core": "Capstone Evaluation, Software Architecture, Industry Practices, Career Launch.",
        "industry_prep": "CI/CD automation, production monitoring, scalable database queries, full-time engineering onboarding.",
        "milestone": "Present final capstone defense, receive bachelor degree, and commence engineering career.",
        "tasks": [
          {
            "id": "bca_cs-sem-8-task-0",
            "order": 1,
            "text": "Deploy production-grade capstone project with live user traffic and monitoring",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "bca_cs-sem-8-task-1",
            "order": 2,
            "text": "Complete technical documentation and slide deck for final jury defense",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "bca_cs-sem-8-task-2",
            "order": 3,
            "text": "Network with alumni and industry professionals on LinkedIn",
            "category": "Career",
            "completed": false
          },
          {
            "id": "bca_cs-sem-8-task-3",
            "order": 4,
            "text": "Review employment contracts, offer letters, and corporate expectations",
            "category": "Career",
            "completed": false
          },
          {
            "id": "bca_cs-sem-8-task-4",
            "order": 5,
            "text": "Celebrate your journey from fresher to full-stack engineer",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      }
    ],
    "active_semester": {
      "id": "bca_cs-sem-1",
      "year": 1,
      "semester_number": 1,
      "title": "Programming Fundamentals in C & Office Tools",
      "focus_areas": [
        "C Language",
        "Computer Fundamentals",
        "Git Basics",
        "Mathematical Foundations"
      ],
      "academic_core": "Computer Fundamentals, Programming in C, Problem Solving Techniques, Communication Skills.",
      "industry_prep": "Writing clean C programs, algorithm flowcharts, setting up code editors, creating a GitHub account.",
      "milestone": "Build a student report card or billing management CLI program in C.",
      "tasks": [
        {
          "id": "bca_cs-sem-1-task-0",
          "order": 1,
          "text": "Install code editor and learn C syntax: data types, loops, arrays, pointers",
          "category": "Code",
          "completed": false
        },
        {
          "id": "bca_cs-sem-1-task-1",
          "order": 2,
          "text": "Understand computer architecture: CPU, memory, storage, and binary arithmetic",
          "category": "Theory",
          "completed": false
        },
        {
          "id": "bca_cs-sem-1-task-2",
          "order": 3,
          "text": "Build a menu-driven console application in C with file storage",
          "category": "Ship",
          "completed": false
        },
        {
          "id": "bca_cs-sem-1-task-3",
          "order": 4,
          "text": "Create your GitHub account and push your first project",
          "category": "Ship",
          "completed": false
        },
        {
          "id": "bca_cs-sem-1-task-4",
          "order": 5,
          "text": "Focus on developing strong English communication and technical vocabulary",
          "category": "Career",
          "completed": false
        }
      ],
      "tasks_count": 5,
      "completed_count": 0,
      "progress_percent": 0
    },
    "overall_stats": {
      "total_tasks": 40,
      "completed_tasks": 0,
      "progress_percent": 0
    }
  },
  "btech_ece": {
    "degree": {
      "id": "btech_ece",
      "name": "B.Tech ECE",
      "full_title": "Electronics & Communication",
      "description": "C/C++, embedded systems, IoT devices, microcontrollers, and hardware-software integration.",
      "icon": "\ud83d\udd0c",
      "duration_years": 4,
      "semesters_count": 8
    },
    "semesters": [
      {
        "id": "btech_ece-sem-1",
        "year": 1,
        "semester_number": 1,
        "title": "C Programming & Electronic Circuits Foundations",
        "focus_areas": [
          "C Language",
          "Basic Electronics",
          "Engineering Math",
          "Git & Linux"
        ],
        "academic_core": "Network Analysis, Electronic Devices & Circuits, Programming for Problem Solving (C), Calculus.",
        "industry_prep": "Writing C programs, breadboard circuit prototyping, using multimeters/oscilloscopes, Git version control.",
        "milestone": "Simulate basic diode and transistor circuits and write a C calculation utility.",
        "tasks": [
          {
            "id": "btech_ece-sem-1-task-0",
            "order": 1,
            "text": "Master C syntax, bitwise operations, memory layout, and pointer arithmetic",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_ece-sem-1-task-1",
            "order": 2,
            "text": "Understand electronic components: resistors, capacitors, diodes, and transistors",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-1-task-2",
            "order": 3,
            "text": "Set up a Linux development environment and learn terminal commands",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_ece-sem-1-task-3",
            "order": 4,
            "text": "Simulate analog circuits using LTspice or Proteus",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-1-task-4",
            "order": 5,
            "text": "Join your college IEEE, Robotics, or Electronics club",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_ece-sem-2",
        "year": 1,
        "semester_number": 2,
        "title": "Digital Electronics & Python for Engineers",
        "focus_areas": [
          "Digital Logic",
          "Python Programming",
          "Microcontroller Basics",
          "Signals & Systems"
        ],
        "academic_core": "Digital System Design (Logic Gates, Flip-Flops, Combinational & Sequential Circuits), Signals & Systems.",
        "industry_prep": "Python scripting for hardware automation, logic gate minimization with Karnaugh maps, Arduino starters.",
        "milestone": "Build your first Arduino sensor project (temperature/motion detection with display).",
        "tasks": [
          {
            "id": "btech_ece-sem-2-task-0",
            "order": 1,
            "text": "Master logic gates, boolean algebra, multiplexers, and flip-flops",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-2-task-1",
            "order": 2,
            "text": "Learn Python programming for data plotting and serial communication",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_ece-sem-2-task-2",
            "order": 3,
            "text": "Program an Arduino or ESP32 microcontroller using C/C++",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-2-task-3",
            "order": 4,
            "text": "Read sensor data (DHT11/Ultrasonic) and display output on LCD/OLED",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-2-task-4",
            "order": 5,
            "text": "Participate in a college hardware/IoT hackathon",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_ece-sem-3",
        "year": 2,
        "semester_number": 3,
        "title": "Embedded C & Microcontroller Architecture",
        "focus_areas": [
          "Embedded C",
          "Microcontrollers (8051 / ARM)",
          "Data Structures in C",
          "Analog Communication"
        ],
        "academic_core": "Microprocessor & Microcontroller Architecture (8051 / ARM Cortex-M), Analog Communication, Data Structures.",
        "industry_prep": "Embedded C programming: register manipulation, timers, interrupts, UART/SPI/I2C communication protocols.",
        "milestone": "Build a multi-sensor IoT node communicating over UART/I2C protocols.",
        "tasks": [
          {
            "id": "btech_ece-sem-3-task-0",
            "order": 1,
            "text": "Implement arrays, linked lists, and circular queues in C for embedded systems",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_ece-sem-3-task-1",
            "order": 2,
            "text": "Learn microcontroller registers, GPIO pins, and interrupt service routines (ISR)",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-3-task-2",
            "order": 3,
            "text": "Interface multiple peripherals using I2C and SPI protocols on STM32 / ESP32",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-3-task-3",
            "order": 4,
            "text": "Solve 50 coding problems in C/C++ on algorithmic logic",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_ece-sem-3-task-4",
            "order": 5,
            "text": "Start designing circuit schematics using KiCad or EasyEDA",
            "category": "Ship",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_ece-sem-4",
        "year": 2,
        "semester_number": 4,
        "title": "PCB Design, IoT & Operating Systems",
        "focus_areas": [
          "KiCad PCB Design",
          "ESP32 & Wi-Fi/BLE",
          "Real-Time OS (RTOS)",
          "Operating Systems"
        ],
        "academic_core": "Linear Integrated Circuits (Op-Amps), Digital Signal Processing (DSP) intro, Operating Systems.",
        "industry_prep": "Custom PCB schematic and board layout in KiCad, FreeRTOS task scheduling, MQTT/HTTP IoT telemetry.",
        "milestone": "Design, fabricate, and assemble your own custom IoT PCB board.",
        "tasks": [
          {
            "id": "btech_ece-sem-4-task-0",
            "order": 1,
            "text": "Design a custom circuit schematic and 2-layer PCB layout in KiCad",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-4-task-1",
            "order": 2,
            "text": "Learn FreeRTOS: tasks, queues, semaphores, and mutexes on microcontrollers",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-4-task-2",
            "order": 3,
            "text": "Connect ESP32 to cloud MQTT brokers (AWS IoT Core / HiveMQ) for telemetry",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-4-task-3",
            "order": 4,
            "text": "Study operating systems: process scheduling, memory management, and concurrency",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-4-task-4",
            "order": 5,
            "text": "Update your engineering portfolio with high-resolution photos of your PCBs",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_ece-sem-5",
        "year": 3,
        "semester_number": 5,
        "title": "FPGA, Verilog HDL & Computer Networks",
        "focus_areas": [
          "Verilog HDL",
          "FPGA Programming",
          "Computer Networks",
          "DSA for Embedded"
        ],
        "academic_core": "Digital VLSI Design, Verilog Hardware Description Language, Computer Networks (TCP/IP, Ethernet, CAN).",
        "industry_prep": "Writing synthesizable Verilog, FPGA simulation with ModelSim/Vivado, CAN bus in automotive systems.",
        "milestone": "Implement a state machine or digital ALU processor on an FPGA development board.",
        "tasks": [
          {
            "id": "btech_ece-sem-5-task-0",
            "order": 1,
            "text": "Learn Verilog syntax: modules, always blocks, blocking vs non-blocking assignments",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_ece-sem-5-task-1",
            "order": 2,
            "text": "Simulate and test digital circuits with testbenches in ModelSim/Vivado",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-5-task-2",
            "order": 3,
            "text": "Implement an SPI/UART master controller in Verilog on an FPGA",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-5-task-3",
            "order": 4,
            "text": "Study Computer Networks: OSI model, TCP/IP, sockets, and industrial buses (CAN, RS-485)",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-5-task-4",
            "order": 5,
            "text": "Solve 150+ DSA problems in C++ for core embedded firmware interview rounds",
            "category": "Code",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_ece-sem-6",
        "year": 3,
        "semester_number": 6,
        "title": "Firmware Development & Core Hardware Internships",
        "focus_areas": [
          "Embedded Linux",
          "Firmware Architecture",
          "System Design for IoT",
          "Core ECE Internships"
        ],
        "academic_core": "Embedded Linux (Yocto/Buildroot), Wireless Communication (BLE, Zigbee, LoRa), Hardware System Design.",
        "industry_prep": "Writing Linux device drivers, kernel compiling, low-power optimization, memory-constrained design.",
        "milestone": "Secure a core firmware, embedded software, or IoT engineering summer internship.",
        "tasks": [
          {
            "id": "btech_ece-sem-6-task-0",
            "order": 1,
            "text": "Build custom Linux kernel images for Raspberry Pi or BeagleBone",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-6-task-1",
            "order": 2,
            "text": "Practice embedded interview questions: volatile keyword, bit masking, memory leaks",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-6-task-2",
            "order": 3,
            "text": "Implement low-power sleep modes and battery monitoring in battery-powered devices",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-6-task-3",
            "order": 4,
            "text": "Apply to 40+ hardware/embedded/semiconductor firms (Texas Instruments, Qualcomm, ST, Bosch)",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_ece-sem-6-task-4",
            "order": 5,
            "text": "Conduct mock technical interviews covering C pointers, microcontroller architecture, and circuits",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_ece-sem-7",
        "year": 4,
        "semester_number": 7,
        "title": "Core Placement Sprints & Capstone Hardware Phase 1",
        "focus_areas": [
          "Hardware / Embedded Placements",
          "Digital Electronics Revision",
          "Capstone Phase 1",
          "Interview Prep"
        ],
        "academic_core": "Comprehensive revision of C/C++, Embedded Systems, Digital Electronics, Microprocessors, and Aptitude.",
        "industry_prep": "Placement tests for semiconductor, automotive, consumer electronics, and software companies.",
        "milestone": "Clear core technical interview rounds and receive job offer in embedded or semiconductor field.",
        "tasks": [
          {
            "id": "btech_ece-sem-7-task-0",
            "order": 1,
            "text": "Revise high-yield topics in Embedded C, pointer arithmetic, and microcontrollers",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-7-task-1",
            "order": 2,
            "text": "Practice speed coding for technical rounds in C/C++",
            "category": "Code",
            "completed": false
          },
          {
            "id": "btech_ece-sem-7-task-2",
            "order": 3,
            "text": "Architect and order components for your Major Final Year Hardware Capstone Project",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-7-task-3",
            "order": 4,
            "text": "Attend on-campus placement drives for core electronics and software profiles",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_ece-sem-7-task-4",
            "order": 5,
            "text": "Prepare crisp explanations for all personal hardware and firmware projects",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      },
      {
        "id": "btech_ece-sem-8",
        "year": 4,
        "semester_number": 8,
        "title": "Capstone Testing, Defense & Industry Onboarding",
        "focus_areas": [
          "Capstone Hardware Defense",
          "EMC / FCC Testing",
          "Firmware Hardening",
          "Career Launch"
        ],
        "academic_core": "Major Project Evaluation, Embedded Security & Secure Boot, Product Compliance, Professional Ethics.",
        "industry_prep": "Hardware debugging, firmware OTA updates, automated hardware-in-the-loop (HIL) testing, career onboarding.",
        "milestone": "Complete final hardware capstone demonstration, pass project jury defense, and launch engineering career.",
        "tasks": [
          {
            "id": "btech_ece-sem-8-task-0",
            "order": 1,
            "text": "Complete working hardware enclosure, power supply, and firmware for capstone project",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-8-task-1",
            "order": 2,
            "text": "Implement secure Over-The-Air (OTA) firmware update mechanism",
            "category": "Ship",
            "completed": false
          },
          {
            "id": "btech_ece-sem-8-task-2",
            "order": 3,
            "text": "Write comprehensive engineering thesis and presentation for final capstone defense",
            "category": "Theory",
            "completed": false
          },
          {
            "id": "btech_ece-sem-8-task-3",
            "order": 4,
            "text": "Conduct mentor sessions for junior robotics and electronics club members",
            "category": "Career",
            "completed": false
          },
          {
            "id": "btech_ece-sem-8-task-4",
            "order": 5,
            "text": "Prepare transition checklist for joining embedded software / semiconductor industry",
            "category": "Career",
            "completed": false
          }
        ],
        "tasks_count": 5,
        "completed_count": 0,
        "progress_percent": 0
      }
    ],
    "active_semester": {
      "id": "btech_ece-sem-1",
      "year": 1,
      "semester_number": 1,
      "title": "C Programming & Electronic Circuits Foundations",
      "focus_areas": [
        "C Language",
        "Basic Electronics",
        "Engineering Math",
        "Git & Linux"
      ],
      "academic_core": "Network Analysis, Electronic Devices & Circuits, Programming for Problem Solving (C), Calculus.",
      "industry_prep": "Writing C programs, breadboard circuit prototyping, using multimeters/oscilloscopes, Git version control.",
      "milestone": "Simulate basic diode and transistor circuits and write a C calculation utility.",
      "tasks": [
        {
          "id": "btech_ece-sem-1-task-0",
          "order": 1,
          "text": "Master C syntax, bitwise operations, memory layout, and pointer arithmetic",
          "category": "Code",
          "completed": false
        },
        {
          "id": "btech_ece-sem-1-task-1",
          "order": 2,
          "text": "Understand electronic components: resistors, capacitors, diodes, and transistors",
          "category": "Theory",
          "completed": false
        },
        {
          "id": "btech_ece-sem-1-task-2",
          "order": 3,
          "text": "Set up a Linux development environment and learn terminal commands",
          "category": "Code",
          "completed": false
        },
        {
          "id": "btech_ece-sem-1-task-3",
          "order": 4,
          "text": "Simulate analog circuits using LTspice or Proteus",
          "category": "Ship",
          "completed": false
        },
        {
          "id": "btech_ece-sem-1-task-4",
          "order": 5,
          "text": "Join your college IEEE, Robotics, or Electronics club",
          "category": "Career",
          "completed": false
        }
      ],
      "tasks_count": 5,
      "completed_count": 0,
      "progress_percent": 0
    },
    "overall_stats": {
      "total_tasks": 40,
      "completed_tasks": 0,
      "progress_percent": 0
    }
  }
};

const defaultEvents = [
  {"city":"Ghaziabad, Delhi NCR","end":"2026-09-26","id":"innohacks","mode":"Offline","name":"Innohacks 4.0","note":"Student-led national hackathon","organizer":"Innogeeks / KIET","start":"2026-09-02","tags":["National","Open innovation"],"url":"https://innohacks-4.devfolio.co/"},
  {"city":"Panvel, Navi Mumbai","end":"2026-09-14","id":"hackoverflow","mode":"Online","name":"HackOverflow 3.0","note":"Pan-India student hackathon with mentorship","organizer":"Department of IT, Pillai College","start":"2026-09-12","tags":["Web3","Cloud","Open Innovation"],"url":"https://hackoverflow-3.devfolio.co/"},
  {"city":"Bengaluru, Karnataka","end":"2026-09-20","id":"synthethic-hacks","mode":"Online","name":"Synthetic Hacks","note":"Build full-stack AI agents and micro-apps","organizer":"Dev Community India","start":"2026-09-18","tags":["Generative AI","APIs","Remote"],"url":"https://devpost.com/"},
  {"city":"Ghaziabad, Uttar Pradesh","end":"2026-09-22","id":"binary-hacks","mode":"Offline","name":"Binary Hacks 4.0","note":"Offline build sprint","organizer":"The Binary Club","start":"2026-09-21","tags":["CSE","36 hours"],"url":"https://binary-hacks-4.devfolio.co/"},
  {"city":"Kalyani, West Bengal","end":"2026-09-26","id":"hacknex","mode":"Offline","name":"HackNex Season 2","note":"Beginners and experienced builders","organizer":"JIS College of Engineering","start":"2026-09-25","tags":["AI / ML","FinTech","EdTech"],"url":"https://hacknex-season-2.devfolio.co/"},
  {"city":"New Delhi","end":"2026-09-26","id":"nexhack","mode":"Offline","name":"NexHack 2.0","note":"Build solutions for real problems","organizer":"IITM, New Delhi","start":"2026-09-25","tags":["AI","National","36 hours"],"url":"https://nexhack-2.devfolio.co/"},
  {"city":"Navi Mumbai, Maharashtra","end":"2026-09-26","id":"cognition","mode":"Offline","name":"Cognition GameJam '26","note":"Prototype submission: 11 Sep","organizer":"SIESGST Technical Team","start":"2026-09-25","tags":["Game dev","Design","Prototype"],"url":"https://cognition-gamejam-1.devfolio.co/"},
  {"city":"Chennai, Tamil Nadu","end":"2026-09-30","id":"hack-chennai","mode":"Offline","name":"Hack Chennai 2026","note":"South India's premier student developer hackathon","organizer":"Anna University & GDG","start":"2026-09-28","tags":["AI","Cloud","36 hours"],"url":"https://devfolio.co/"},
  {"city":"Hyderabad, Telangana","end":"2026-10-05","id":"hyderabad-build","mode":"Offline","name":"T-Hub GenAI Hackathon","note":"Rapid prototype build with venture incubation track","organizer":"IIIT Hyderabad & T-Hub","start":"2026-10-03","tags":["GenAI","LLMs","Startups"],"url":"https://devfolio.co/"},
  {"city":"Jaipur, Rajasthan","end":"2026-10-12","id":"desert-hacks","mode":"Offline","name":"DesertHacks 2026","note":"36-hour flagship hackathon in the Pink City","organizer":"LNMIIT & Turing Club","start":"2026-10-10","tags":["Open Innovation","IoT","Cybersec"],"url":"https://devfolio.co/"},
  {"city":"Gandhinagar, Gujarat","end":"2026-10-17","id":"gujarat-hack","mode":"Offline","name":"Gujarat Innovation Hackfest","note":"Build real tech solutions for Western India industries","organizer":"DA-IICT & IEEE","start":"2026-10-15","tags":["FinTech","Web3","Hardware"],"url":"https://devfolio.co/"},
  {"city":"Kochi, Kerala","end":"2026-10-22","id":"kerala-build","mode":"Offline","name":"Kochi DevSprint 2026","note":"Hardware + Software dual-track campus hackathon","organizer":"Maker Village & CUSAT","start":"2026-10-20","tags":["Robotics","CleanTech","AI"],"url":"https://devfolio.co/"},
  {"city":"Patiala, Punjab","end":"2026-10-26","id":"punjab-hacks","mode":"Offline","name":"Punjab HackSprint","note":"Mentored hackathon for North India freshers","organizer":"TIET Patiala & MLH","start":"2026-10-24","tags":["Full-Stack","Mobile","Beginner"],"url":"https://devfolio.co/"},
  {"city":"Bhopal, Madhya Pradesh","end":"2026-11-03","id":"bhopal-hacks","mode":"Offline","name":"Central India Hackfest","note":"Biggest collegiate tech showdown in Central India","organizer":"MANIT Bhopal & ACM","start":"2026-11-01","tags":["EdTech","AgriTech","AI"],"url":"https://devfolio.co/"},
  {"city":"Bhubaneswar, Odisha","end":"2026-11-09","id":"odisha-hack","mode":"Offline","name":"Kalinga Innovate 2026","note":"East India premier hackathon with top incubators","organizer":"KIIT & Tech Society","start":"2026-11-07","tags":["Smart Cities","HealthTech","Cloud"],"url":"https://devfolio.co/"},
];

if (typeof window !== 'undefined') {
  window.defaultDegrees = defaultDegrees;
  window.defaultRoadmaps = defaultRoadmaps;
  window.defaultEvents = defaultEvents;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { defaultDegrees, defaultRoadmaps, defaultEvents };
}

