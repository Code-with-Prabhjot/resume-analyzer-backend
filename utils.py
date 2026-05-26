# utils.py

# Your growing dictionary of alternative names
SKILL_SYNONYMS = {
    "ml": "machine learning",
    "dl": "deep learning",
    "js": "javascript",
    "node": "node.js",
    "reactjs": "react",
    "html5": "html",  
    "css3": "css",
    "c++": "c plus plus",
    "c#": "c sharp",
    "dot net": ".net",
    "aws": "amazon web services",
    "gcp": "google cloud",
    # --- BATCH 1: ML, AI & Data Science ---
    "dsa": "data structures and algorithms",
    "numpy": "numpy library",
    "pandas": "pandas library",
    "sklearn": "scikit-learn",
    "scikitlearn": "scikit-learn",
    "ann": "neural networks architecture",
    "neural networks": "neural networks architecture",
    "tf": "tensorflow",
    "cv": "computer vision",
    "rl": "reinforcement learning",
    "xgb": "xgboost",
    "ml ops": "mlops",
    "time series": "time series analysis",
    "recommendation engine": "recommender systems",
    "gnn": "graph neural networks",
    "a/b testing": "ab testing",
    "ab test": "ab testing",
    "gradient descent": "gradient descent optimization",
    "transformer": "transformers architecture",
    "transformers": "transformers architecture",
    "nlp": "natural language processing (nlp)",
    "cnn": "convolutional neural networks (cnn)",
    "rnn": "recurrent neural networks (rnn)",
    "sql": "sql for data science",
    "spark": "big data (spark)",
    "apache spark": "big data (spark)",
    "docker": "docker and kubernetes for ml",
    "kubernetes": "docker and kubernetes for ml",
    "k8s": "docker and kubernetes for ml",
    "git": "git and version control",
    "github": "git and version control",
    "gitlab": "git and version control",
    "dvc": "dvc (data version control)",
    "gan": "generative adversarial networks (gan)",
    "gans": "generative adversarial networks (gan)",
    "llm": "large language models (llms)",
    "llms": "large language models (llms)",
    "flask": "model deployment (flask/fastapi)",
    "fastapi": "model deployment (flask/fastapi)",
    "eda": "exploratory data analysis (eda)",
    "matplotlib": "data visualization (matplotlib/seaborn)",
    "seaborn": "data visualization (matplotlib/seaborn)",
    "shap": "ml model interpretability (shap/lime)",
    "lime": "ml model interpretability (shap/lime)",
    # --- BATCH 2: Advanced ML, LLMs & MLOps ---
    
    # Common Abbreviations & Slang
    "sgd": "stochastic gradient descent",
    "attention": "attention mechanism",
    "self-attention": "attention mechanism",
    "fine tuning": "fine-tuning models",
    "finetuning": "fine-tuning models",
    "unit testing": "unit testing for ml code",
    "pytest": "unit testing for ml code", # Often used interchangeably on resumes
    "bash": "linux/bash scripting",
    "linux": "linux/bash scripting",
    "shell scripting": "linux/bash scripting",
    "rest api": "api integration",
    "apis": "api integration",
    "hyperparameter tuning": "hyperparameter optimization (optuna)",
    "adversarial attacks": "ml security (adversarial attacks)",
    "xai": "explainable ai (xai)",
    "cuda": "cuda programming",
    "multimodal": "multimodal machine learning",
    "ltr": "recommendation ranking (ltr)",
    "learning to rank": "recommendation ranking (ltr)",
    "asr": "speech recognition (asr)",
    "speech to text": "speech recognition (asr)",
    "stt": "speech recognition (asr)",
    "tts": "text-to-speech (tts)",
    "nas": "neural architecture search (nas)",
    "model monitoring": "model monitoring and drift detection",
    "drift detection": "model monitoring and drift detection",
    "data drift": "model monitoring and drift detection",
    "concept drift": "model monitoring and drift detection",
    "ci/cd": "continuous integration for ml (ci/cd)",
    "cicd": "continuous integration for ml (ci/cd)",
    "ci-cd": "continuous integration for ml (ci/cd)",
    "continuous integration": "continuous integration for ml (ci/cd)",
    "ray": "ray framework",
    "maas": "model as a service (maas)",

    # Unbundling your bracketed/grouped terms
    "word2vec": "word embeddings (word2vec)",
    "word embeddings": "word embeddings (word2vec)",
    "bert": "bert and elmo models",
    "elmo": "bert and elmo models",
    "roberta": "bert and elmo models", # Good bonus to catch
    "onnx": "onnx (open neural network exchange)",
    "optuna": "hyperparameter optimization (optuna)",
    "vector databases": "vector databases (pinecone/milvus)",
    "pinecone": "vector databases (pinecone/milvus)",
    "milvus": "vector databases (pinecone/milvus)",
    "weaviate": "vector databases (pinecone/milvus)", # Another very popular one
    "rag": "rag (retrieval-augmented generation)",
    "retrieval augmented generation": "rag (retrieval-augmented generation)",
    "fpga": "fpga/asic for ml",
    "asic": "fpga/asic for ml",
    # --- BATCH 3: Core ML, Deep Learning, Architectures & Tooling ---
    
    # Core ML Algorithms & Techniques
    "gp": "gaussian processes",
    "pgm": "probabilistic graphical models",
    "hidden markov": "hidden markov models (hmm)",
    "support vector machine": "support vector machines (svm)",
    "k-nearest neighbors": "k-nearest neighbors (knn)",
    "k-nearest neighbor": "k-nearest neighbors (knn)",
    "gradient boosting": "gradient boosting machines (gbm)",
    "lgbm": "lightgbm",
    "feature selection": "feature selection techniques",
    "smote": "imbalanced data handling",
    "imbalanced data": "imbalanced data handling",
    "image augmentation": "data augmentation (vision)",
    "text augmentation": "text augmentation (nlp)",

    # Unbundling Grouped ML Concepts
    "hmm": "hidden markov models (hmm)",
    "svm": "support vector machines (svm)",
    "knn": "k-nearest neighbors (knn)",
    "decision tree": "decision trees and random forests",
    "decision trees": "decision trees and random forests",
    "random forest": "decision trees and random forests",
    "random forests": "decision trees and random forests",
    "gbm": "gradient boosting machines (gbm)",

    # Neural Network Foundations & Architectures
    "backprop": "backpropagation algorithm",
    "backpropagation": "backpropagation algorithm",
    "vanishing gradient": "vanishing and exploding gradients",
    "exploding gradient": "vanishing and exploding gradients",
    "batchnorm": "batch normalization",
    "batch norm": "batch normalization",
    "dropout": "dropout and weight decay",
    "weight decay": "dropout and weight decay",
    "relu": "activation functions (relu/sigmoid/softmax)",
    "sigmoid": "activation functions (relu/sigmoid/softmax)",
    "softmax": "activation functions (relu/sigmoid/softmax)",
    "long short term memory": "long short-term memory (lstm)",
    "vision transformer": "vision transformers (vit)",
    "unet": "u-net architecture",
    "resnet": "resnet and inception models",
    "inception": "resnet and inception models",
    "variational autoencoder": "variational autoencoders (vae)",

    # Unbundling Architectures
    "lstm": "long short-term memory (lstm)",
    "gru": "gated recurrent units (gru)",
    "vit": "vision transformers (vit)",
    "vae": "variational autoencoders (vae)",

    # Modern GenAI, Agents & RL
    "rlhf": "reinforcement learning from human feedback (rlhf)",
    "q-learning": "q-learning and deep q-networks (dqn)",
    "q learning": "q-learning and deep q-networks (dqn)",
    "deep q networks": "q-learning and deep q-networks (dqn)",
    "policy gradient": "policy gradient methods",
    "ppo": "proximal policy optimization (ppo)",
    "ner": "named entity recognition (ner)",
    "topic modeling": "topic modeling (lda)",
    "seq2seq": "sequence-to-sequence models",
    "sequence to sequence": "sequence-to-sequence models",
    "ocr": "optical character recognition (ocr)",
    "few shot": "few-shot and zero-shot learning",
    "zero shot": "few-shot and zero-shot learning",
    "few-shot learning": "few-shot and zero-shot learning",
    "zero-shot learning": "few-shot and zero-shot learning",
    "pruning": "model pruning",
    "distillation": "knowledge distillation",
    "tensorrt": "tensorrt optimization",
    "ort": "onnx runtime",
    "llamaindex": "llama-index",
    "ai agents": "autogen and ai agents",
    "ai agent": "autogen and ai agents",
    "lora": "lora and qlora (fine-tuning)",
    "qlora": "lora and qlora (fine-tuning)",

    # Unbundling GenAI Terms
    "dqn": "q-learning and deep q-networks (dqn)",
    "lda": "topic modeling (lda)",
    "autogen": "autogen and ai agents",
    "peft": "peft (parameter-efficient fine-tuning)",

    # MLOps Infrastructure, Workflows & Security
    "tensorflow extended": "tfx (tensorflow extended)",
    "feature store": "feature stores (feast/hopsworks)",
    "evidently": "evidently ai (monitoring)",
    "evidentlyai": "evidently ai (monitoring)",
    "wandb": "weights & biases (w&b)",
    "weights and biases": "weights & biases (w&b)",
    "comet": "comet ml",
    "cometml": "comet ml",
    "airflow": "apache airflow for ml pipelines",
    "prefect": "prefect (workflow orchestration)",
    "dask": "dask for parallel computing",
    "triton": "triton inference server",
    "lightning": "pytorch lightning",
    "huggingface": "hugging face ecosystem",
    "hf": "hugging face ecosystem",
    "faiss": "vector search (faiss)",
    "differential privacy": "differential privacy in ml",
    "homomorphic encryption": "homomorphic encryption for ml",
    "model lineage": "model lineage and provenance",
    "data drift": "data drift and concept drift",
    "concept drift": "data drift and concept drift",
    "ab testing": "a/b testing for machine learning",
    "mab": "multi-armed bandits",
    "cold start": "recommender cold start problem",

    # Unbundling Infrastructure Tools
    "tfx": "tfx (tensorflow extended)",
    "feast": "feature stores (feast/hopsworks)",
    "hopsworks": "feature stores (feast/hopsworks)",
    "w&b": "weights & biases (w&b)",
    "ragas": "llm evaluation (ragas/langsmith)",
    "langsmith": "llm evaluation (ragas/langsmith)",
    # --- BATCH 4: Specialized ML & Civil/Structural Engineering ---
    
    # Advanced ML & Tooling Unbundling
    "geospatial ml": "geospatial machine learning",
    "hgnn": "hypergraph neural networks",
    "kg": "knowledge graphs for ai",
    "knowledge graph": "knowledge graphs for ai",
    "knowledge graphs": "knowledge graphs for ai",
    "model distillation": "model distillation for llms",
    "tensorboard": "tensorboard for visualization",
    "plotly": "plotly and dash for ml apps",
    "dash": "plotly and dash for ml apps",
    "streamlit": "streamlit for ml prototyping",
    "gradio": "gradio for model demos",
    "einsum": "einsum for deep learning",
    "autodiff": "automatic differentiation",
    "mixed precision": "mixed precision training",
    "amp": "mixed precision training",
    "gradient accumulation": "gradient accumulation",
    "clip": "clip (contrastive language-image pre-training)",
    "dreambooth": "stable diffusion fine-tuning (dreambooth)",
    "ai governance": "ai governance and compliance",

    # Civil & Structural Engineering - Slang & Acronyms
    "rc design": "reinforced concrete design",
    "rcc design": "reinforced concrete design",
    "reinforced concrete": "reinforced concrete design",
    "geotech": "geotechnical engineering",
    "fluid dynamics": "fluid mechanics",
    "surveying": "surveying and geomatics",
    "geomatics": "surveying and geomatics",
    "transportation": "transportation engineering",
    "hydrology": "hydrology and water resources",
    "water resources": "hydrology and water resources",
    "construction management": "construction project management",
    "cpm": "construction project management",
    "steel design": "steel structural design",
    "autocad": "autocad proficiency",
    "auto cad": "autocad proficiency",
    "bim": "bim - building information modeling",
    "building information modeling": "bim - building information modeling",
    "revit": "bim - building information modeling", # Very common industry software for BIM
    "matrix methods": "matrix methods of structural analysis",
    "highway design": "highway engineering",
    "wastewater treatment": "wastewater treatment design",
    "estimating and costing": "construction estimating and costing",
    "cost estimating": "construction estimating and costing",
    "gis": "gis - geographic information systems",
    "geographic information systems": "gis - geographic information systems",
    "arcgis": "gis - geographic information systems", # Bonus: Industry standard GIS software
    "qgis": "gis - geographic information systems",   # Bonus: Open source GIS software
    "bridge design": "bridge engineering",
    "earthquake engineering": "seismology and earthquake engineering",
    "seismic design": "seismology and earthquake engineering",
    "traffic engineering": "traffic flow theory",
    "hydraulics": "hydraulics and pneumatic systems",
    "pneumatics": "hydraulics and pneumatic systems",
    "fea": "finite element analysis - fea",
    "finite element analysis": "finite element analysis - fea",
    "fem": "finite element analysis - fea",
    "finite element method": "finite element analysis - fea",
    # --- BATCH 5: Civil, Structural & Construction Management ---
    
    # Common Acronyms & Industry Slang
    "qs": "quantity surveying",
    "shm": "structural health monitoring",
    "dgps": "total station and dgps",
    "total station": "total station and dgps",
    "swm": "solid waste management",
    "waste management": "solid waste management",
    "hse": "safety and risk management",
    "osha": "safety and risk management",
    "precast": "precast concrete construction",
    "retrofitting": "rehabilitation of structures",
    "suds": "sustainable urban drainage systems (suds)",
    "mep": "building services engineering",
    "building services": "building services engineering",
    "fvm": "finite volume method",
    "cfs": "cold-formed steel design",
    "cold formed steel": "cold-formed steel design",
    "pms": "pavement management systems",
    "prefab": "modular construction",
    "cfd": "computational fluid dynamics (cfd)",
    "ssi": "soil-structure interaction",
    "pt design": "post-tensioning design",
    "post tensioning": "post-tensioning design",

    # Unbundling Software, Certifications & Tools
    "primavera": "p6 primavera and ms project",
    "primavera p6": "p6 primavera and ms project",
    "ms project": "p6 primavera and ms project",
    "microsoft project": "p6 primavera and ms project",
    "leed": "green building and leed",
    "leed ap": "green building and leed",
    "green building": "green building and leed",
    "scada": "scada in water systems",

    # Unbundling Grouped/Truncated Concepts
    "tender management": "contracts and tender management",
    "tendering": "contracts and tender management",
    "contract management": "contracts and tender management",
    "masonry design": "masonry structure design",
    "timber design": "timber structural design",
    "composite design": "composite material design",
    "engineering drawing": "civil engineering drawing",
    "mechanics of solids": "solid mechanics",
    "material testing": "building materials and testing",
    "high rise design": "tall building design",
    "marine engineering": "harbor and port engineering",
    "port engineering": "harbor and port engineering",
    "plastic analysis": "plastic analysis of structures",
    "engineering ethics": "values and ethics in engineering",
    "fire safety": "fire safety in buildings",
    "nfpa": "fire safety in buildings", # Bonus: The major fire safety code
    "real estate valuation": "valuation of real estate",
    "property valuation": "valuation of real estate",
    "shell structures": "shell and spatial structures",
    "disaster recovery": "disaster management",
    "construction law": "civil engineering law",
    "acoustics": "building acoustics",
    "smart cities": "smart cities infrastructure",
    "bathymetry": "hydrographic surveying",
    "soil consolidation": "seepage and consolidation",
    "seepage": "seepage and consolidation",
    "pile testing": "deep foundation testing",
    "deep foundations": "deep foundation testing",
    "signal timing": "traffic signal timing",
    # --- BATCH 6: Advanced Civil, Environmental, & Construction Tech ---
    
    # Advanced Modeling & Software Acronyms
    "swmm": "stormwater modeling (swmm)",
    "epa swmm": "stormwater modeling (swmm)",
    "hec-ras": "hec-ras modeling",
    "hec ras": "hec-ras modeling",
    "epanet": "pipe network analysis (epanet)",
    "lidar": "lidar data processing",
    "drone surveying": "uav/drone surveying",
    "uav surveying": "uav/drone surveying",
    "drones": "uav/drone surveying",
    
    # Industry Acronyms & Certifications
    "lrfd": "advanced steel design (lrfd)",
    "ndt": "non-destructive testing (ndt) in civil",
    "non-destructive testing": "non-destructive testing (ndt) in civil",
    "lcca": "lifecycle cost analysis (lcca)",
    "life cycle cost analysis": "lifecycle cost analysis (lcca)",
    "peb": "pre-engineered buildings (peb)",
    "pre-engineered buildings": "pre-engineered buildings (peb)",
    "eia": "environmental impact assessment (eia)",
    "its": "intelligent transportation systems (its)",
    "intelligent transportation systems": "intelligent transportation systems (its)",
    
    # Unbundling Grouped/Truncated Concepts
    "earth retaining structures": "earth-retaining structures design",
    "retaining structures": "earth-retaining structures design",
    "value engineering": "value engineering in construction",
    "dispute resolution": "arbitration and dispute resolution",
    "hazardous waste": "hazardous waste management",
    "soil nailing": "anchors and soil nailing",
    "pipe network analysis": "pipe network analysis (epanet)",
    "3d printing in construction": "additive manufacturing in construction (3d printing)",
    "construction 3d printing": "additive manufacturing in construction (3d printing)",
    "iot in construction": "internet of things (iot) in infrastructure",
    "iot": "internet of things (iot) in infrastructure", # Contextual mapping for civil resumes
    "augmented reality": "augmented reality in construction",
    "virtual reality": "virtual reality in bim",
    "vr in bim": "virtual reality in bim",
    # --- BATCH 7: Sustainable Engineering, Core CS & Full-Stack ---
    
    # Sustainable Engineering & MEP Acronyms
    "iaq": "indoor air quality management",
    "bem": "building energy modeling (bem)",
    "building energy modeling": "building energy modeling (bem)",
    "hvac": "hvac system integration",
    "fm": "facilities management",
    "ppp": "public-private partnerships (ppp) in construction",
    "p3": "public-private partnerships (ppp) in construction",
    
    # Core Computer Science Acronyms
    "os": "operating systems",
    "dbms": "database management systems",
    "rdbms": "database management systems",
    "oop": "object oriented programming",
    "oops": "object oriented programming",
    "object-oriented programming": "object oriented programming",
    "discrete math": "discrete mathematics",
    "comp arch": "computer architecture",
    "toc": "theory of computation",
    
    # Web Development & Tech Slang
    "ts": "typescript",
    "golang": "go",         # 'go programming' gets auto-cleaned to 'go'
    "rustlang": "rust",     # 'rust programming' gets auto-cleaned to 'rust'
    "react": "react js",
    "reactjs": "react js",
    "express": "express js",
    "expressjs": "express js",
    "node": "node js",
    "nodejs": "node js",
    "mongo": "mongodb",
    "postgres": "postgresql",
    "gql": "graphql",
    
    # Security & Mobile Development
    "infosec": "cybersecurity",
    "pentesting": "penetration testing",
    "pen testing": "penetration testing",
    "crypto": "cryptography",
    "android": "android development",
    "ios": "ios development",
    # --- BATCH 8: Mobile, Big Data, DevOps, & Web Frameworks ---
    
    # Mobile & Game Dev
    "rn": "react native",
    "react-native": "react native",
    "unity": "unity engine",
    "unity3d": "unity engine",
    "unreal": "unreal engine",
    "ue4": "unreal engine",
    "ue5": "unreal engine",
    
    # Architecture, Methodologies & Testing
    "websockets": "web sockets",
    "socket.io": "web sockets",
    "agile": "agile methodology",
    "tdd": "test driven development",
    "stlc": "software testing life cycle",
    "jira": "bug tracking",         # Often used synonymously on resumes
    "bugzilla": "bug tracking",
    "ux": "user experience design",
    "ui/ux": "user experience design",
    "user experience": "user experience design",
    "rwd": "responsive web design",
    "responsive design": "responsive web design",
    "fp": "functional programming",
    "solid": "solid principles",
    
    # Security & Auth
    "oauth": "oauth 2.0",
    "oauth2": "oauth 2.0",
    "jwt": "json web tokens",
    "jwts": "json web tokens",
    "regex": "regular expressions",
    "regexp": "regular expressions",
    
    # Frontend & Backend Frameworks
    "scss": "sass",
    "tailwind": "tailwind css",
    "vue": "vue js",
    "vuejs": "vue js",
    "vue.js": "vue js",
    "next": "next js",
    "nextjs": "next js",
    "next.js": "next js",
    "wasm": "webassembly",
    "rails": "ruby on rails",
    "ror": "ruby on rails",
    
    # Big Data, Databases & Cloud
    "elastic search": "elasticsearch",
    "elk": "elasticsearch",         # ELK stack implies Elasticsearch
    "serverless": "serverless computing",
    "lambda": "serverless computing", # AWS Lambda is synonymous with serverless
    "terraform": "terraform cloud",
    "spark": "apache spark",        # Overrides older "big data (spark)"
    "hadoop": "apache hadoop",
    "azure": "microsoft azure",     # Overrides older bundled cloud tag
    "gcp": "google cloud platform", # Overrides older bundled cloud tag
    "cassandra": "apache cassandra",
    "dynamodb": "amazon dynamodb",
    "dynamo db": "amazon dynamodb",
    "airflow": "apache airflow",    # Overrides older "apache airflow for ml pipelines"
    "flink": "apache flink",
    "hive": "apache hive",
    "spark streaming": "apache spark streaming",
    "databricks": "databricks",
    # --- BATCH 9: Backend, Architecture, Security & Electrical Engineering ---

    # Web, APIs & Frontend Libraries
    "springboot": "spring boot",
    "spring-boot": "spring boot",
    "asp.net": "asp.net core",
    "dotnet core": "asp.net core",
    ".net core": "asp.net core",
    "apollo": "graphql apollo",
    "apollo graphql": "graphql apollo",
    "three.js": "three js",
    "threejs": "three js",
    "d3.js": "d3 js",
    "d3js": "d3 js",
    "socket.io": "socket io",
    "pwa": "progressive web apps",

    # Security & Networking
    "oidc": "openid connect",
    "iam": "iam basics",
    "identity and access management": "iam basics",
    "ssl": "ssl tls",
    "tls": "ssl tls",
    "ssh": "ssh protocol",
    "burpsuite": "burp suite",
    "burp": "burp suite",
    "digital forensics": "computer forensics",
    "zero trust": "zero trust architecture",
    "iac": "infrastructure as code",

    # Cloud, DevOps & System Architecture
    "cloudformation": "cloudformation",
    "cfn": "cloudformation",
    "aws cloudformation": "cloudformation",
    "istio": "service mesh istio",
    "service mesh": "service mesh istio",
    "sre": "site reliability engineering",
    "elk": "elk stack",
    "distributed systems": "distributed systems theory",
    "paxos": "paxos and raft",
    "raft": "paxos and raft",
    "microfrontends": "micro frontends",
    "event driven": "event driven architecture",
    "cqrs": "cqrs and event sourcing",
    "event sourcing": "cqrs and event sourcing",
    "ddd": "domain driven design",
    "active mq": "activemq",
    "nifi": "apache nifi",
    "bq": "bigquery",
    "google bigquery": "bigquery",
    "redshift": "amazon redshift",

    # Low-Level Software & Embedded
    "genai": "generative ai",
    "gen-ai": "generative ai",
    "mcu": "microcontrollers",
    "mpu": "microprocessors",
    "asm": "assembly language",
    "assembly": "assembly language",
    "gdb": "gdb debugger",
    "llvm": "llvm basics",
    "real-time operating systems": "rtos",
    "real time operating systems": "rtos",

    # Electrical & Hardware Engineering
    "fpga": "fpga programming",      # Unifies "fpga programming" and "fpga design"
    "vlsi": "vlsi design",
    "pcb": "pcb design",
    "printed circuit board": "pcb design",
    "circuit design": "circuit theory",
    "digital logic": "digital electronics",
    "analog design": "analog electronics",
    "power systems": "power systems analysis",
    "control theory": "control systems",
    "emc": "electromagnetics",
    "emi": "electromagnetics",
    "motors and drives": "electrical machines",
    "solar pv": "solar photovoltaics",
    "photovoltaics": "solar photovoltaics",
    "wind energy": "wind energy engineering",
    "smart grid": "smart grid technology",
    "smart grids": "smart grid technology",
    "switchgear and protection": "power system protection",
    "plc": "plc programming",
    "simulink": "matlab and simulink",
    "dsp": "digital signal processing",
    "bms": "battery management systems",
    "ev": "electric vehicle technology",
    "electric vehicles": "electric vehicle technology",
    # --- BATCH 10: Electrical, Power Systems, Hardware & EV Tech ---

    # Hardware Description & Microcontrollers
    "verilog": "verilog hdl",
    "rpi": "raspberry pi",
    "raspi": "raspberry pi",
    "arm": "arm architecture",
    "cmos": "cmos analog design",
    "mixed signal": "mixed signal design",

    # Simulation & Design Software
    "pspice": "pspice simulation",
    "ltspice": "ltspice simulation",
    "digsilent": "digsilent powerfactory",
    "powerfactory": "digsilent powerfactory",
    "autocad e": "autocad electrical",
    "autocad elec": "autocad electrical",
    
    # Motors, Drives & Industrial Automation
    "vfd": "variable frequency drive configuration",
    "variable frequency drives": "variable frequency drive configuration",
    "bldc": "bldc motor control",
    "brushless dc": "bldc motor control",
    "stepper motors": "stepper motor control",
    "servo motors": "servo motor tuning",
    "lim": "linear induction motors",
    "hmi": "hmi design",
    "human machine interface": "hmi design",
    "dcs": "dcs", # Distributed Control Systems
    "distributed control systems": "dcs",
    "soft starters": "soft starter commissioning",
    
    # Power Systems, Grid & Analysis
    "hvdc": "hvdc transmission",
    "facts": "facts devices",
    "flexible ac transmission": "facts devices",
    "load flow": "load flow analysis",
    "power flow": "load flow analysis",
    "opf": "optimal power flow",
    "short circuit studies": "short circuit analysis",
    "wams": "wide area monitoring systems",
    "pmu": "phasor measurement units",
    "dsm": "demand side management",
    "earthing": "earthing and grounding systems",
    "grounding": "earthing and grounding systems",
    "cable sizing": "power cable sizing",
    
    # Diagnostics & Protection
    "relay coordination": "relay coordination",
    "megger": "insulation resistance testing", # Industry slang for insulation testing
    "partial discharge": "partial discharge measurement",
    "spd": "surge protection devices",
    "lps": "lightning protection systems",
    "cb": "circuit breaker maintenance",
    "circuit breakers": "circuit breaker maintenance",
    "gis switchgear": "gas insulated switchgear",
    
    # EV, Batteries & Power Electronics
    "v2g": "vehicle-to-grid integration",
    "vehicle to grid": "vehicle-to-grid integration",
    "obc": "on-board charger design",
    "traction inverters": "traction inverter control",
    "li-ion": "lithium-ion battery chemistry",
    "lithium ion": "lithium-ion battery chemistry",
    "soc":"soc and soh estimation algorithms",
    "soh": "soc and soh estimation algorithms",
    "state of charge": "soc and soh estimation algorithms",
    "ess": "energy storage systems",
    "smes": "superconducting magnetic energy storage",
    "ultracapacitors": "supercapacitors",
    
    # Communications & Overrides
    "satcom": "satellite communications",
    "fiber optics": "optical fiber communications",
    "rf": "microwave engineering",
    "emi": "emi/emc", # Overrides the Batch 9 generic mapping for explicit EMC
    "emc": "emi/emc",
    "wpt": "wireless power transfer",
    "digital twin": "digital twins",
    # --- BATCH 11: Embedded Protocols, Control Systems & Biomed ---

    # Wireless, RF & Telecommunications
    "lora": "lora technology",
    "lorawan": "lora technology",
    "zigbee": "zigbee protocol",
    "sdr": "software defined radio",
    "crn": "cognitive radio networks",
    "mimo": "massive mimo",
    "mmwave": "millimeter wave circuit design",
    "silicon photonics": "silicon photonics",

    # DSP, Vision & Control Theory
    "isp": "image signal processing",
    "machine vision": "machine vision systems",
    "mpc": "model predictive control",
    "smc": "sliding mode control design",
    "h-infinity": "h-infinity control theory",
    "kalman filter": "kalman filter implementation",
    "particle filter": "particle filter algorithms",
    "op-amp": "operational amplifiers",
    "op amp": "operational amplifiers",
    "opamps": "operational amplifiers",

    # Embedded Protocols & Interfaces
    "iiot": "industrial iot architecture",
    "modbus": "modbus rtu/tcp",
    "profibus": "profibus and profinet protocols",
    "profinet": "profibus and profinet protocols",
    "ethercat": "ethercat communication",
    "i2c": "i2c protocol",
    "spi": "spi protocol",
    "uart": "uart communication",
    "rs-485": "uart and rs-485 serial",
    "rs485": "uart and rs-485 serial",
    "can": "can bus",
    "canbus": "can bus",
    "usb": "usb protocol",
    "pcie": "pcie interface design",
    "pci express": "pcie interface design",
    "ethernet": "ethernet in embedded systems",
    "adc": "adc and dac circuits",
    "dac": "adc and dac circuits",

    # Hardware, PCB & Signal Integrity
    "si": "signal integrity",                 # Massive embedded keyword
    "pi": "power integrity simulation",       # Massive embedded keyword
    "pcb layout": "pcb design and layout",
    "mems": "mems sensor fabrication",
    "rf design": "rf circuit design",

    # Biomedical Engineering
    "mri": "magnetic resonance imaging hardware",
    "ct scan": "computed tomography electronics",
    "pacemaker": "cardiac pacemakers and icds",
    "icd": "cardiac pacemakers and icds",
    "biosensors": "electrochemical biosensors",

    # Safety, Compliance & Standards
    "iso 9001": "iso 9001 quality standards",
    "iec 61508": "iec 61508 functional safety",
    "iso 26262": "iso 26262 automotive safety",
    "fusa": "iec 61508 functional safety", # Industry slang for Functional Safety
    "ul 508a": "ul 508a industrial panels",
    "ce mark": "ce compliance testing",
    "rohs": "rohs and weee directives",
    "weee": "rohs and weee directives",
    # --- BATCH 12: VLSI, Hardware Verification, IoT & Power Electronics ---

    # VLSI, Chip Design & Physical Verification
    "soc": "system-on-chip design",
    "system on chip": "system-on-chip design",
    "sta": "static timing analysis",
    "dft": "design for testability (dft)",
    "drc": "physical verification (drc/lvs)",
    "lvs": "physical verification (drc/lvs)",
    "design rule check": "physical verification (drc/lvs)",
    "layout versus schematic": "physical verification (drc/lvs)",
    "cts": "clock tree synthesis",
    "rfic": "rfic design",
    "pmic": "power management ic design",

    # Hardware Verification
    "sv": "systemverilog for verification",
    "systemverilog": "systemverilog for verification",
    "system verilog": "systemverilog for verification",
    "uvm": "uvm (universal verification methodology)",

    # Advanced Electronics & RF
    "smps": "smps design and analysis",
    "switched mode power supply": "smps design and analysis",
    "pll": "pll and frequency synthesizers",
    "phase locked loop": "pll and frequency synthesizers",
    "lna": "low-noise amplifier design",
    "low noise amplifier": "low-noise amplifier design",
    
    # IoT, Comms & Firmware
    "mqtt": "mqtt protocol",
    "ble": "bluetooth low energy",
    "lorawan": "lora and lorawan",
    "nb-iot": "nb-iot (narrowband iot)",
    "nbiot": "nb-iot (narrowband iot)",
    "nfc": "nfc (near field communication)",
    "gnss": "gnss/gps receiver design",
    "gps": "gnss/gps receiver design",
    "ota": "over-the-air (ota) updates",
    "device drivers": "device driver development",
    "bare metal": "bare metal programming",
    
    # Control Systems & Industrial Comms
    "foc": "motor control algorithms (foc)",
    "field oriented control": "motor control algorithms (foc)",
    "pid": "pid controller tuning",
    "proportional integral derivative": "pid controller tuning",
    "opc-ua": "opc-ua communication",
    "opc ua": "opc-ua communication",

    # Manufacturing, Quality & Soft Skills
    "qms": "quality management systems",
    "ip": "intellectual property for engineers",
    # --- BATCH 13: High-Speed PCB, Automotive & Mechanical Engineering ---

    # Hardware Reliability, Testing & Standards
    "esd": "electrostatic discharge (esd) protection",
    "halt": "reliability testing (halt/hass)",
    "hass": "reliability testing (halt/hass)",
    "fmea": "failure mode and effects analysis (fmea)",
    "dfm": "dfm (design for manufacturing) for pcbs",
    "smt": "surface mount technology (smt) processes",
    "puf": "hardware security (puf - physical unclonable functions)",
    "jtag": "jtag debugging and boundary scan",
    "vna": "vector network analyzer (vna) calibration",
    "ipc-610": "ipc-610 pcb assembly standards",
    "ipc 610": "ipc-610 pcb assembly standards",

    # High-Speed PCB, FPGA & Interfaces
    "serdes": "serdes (serializer/deserializer) design",
    "ddr": "ddr4/ddr5 memory interfacing",
    "ddr4": "ddr4/ddr5 memory interfacing",
    "ddr5": "ddr4/ddr5 memory interfacing",
    "mipi": "mipi dsi/csi interface design",
    "lvds": "lvds signaling",
    "rigid flex": "rigid-flex pcb design",
    "usb pd": "usb power delivery (usb-pd)",
    "sdc": "fpga timing constraints (sdc)",
    "vitis": "vitis hls (high level synthesis)",
    "hls": "vitis hls (high level synthesis)",
    "lvgl": "embedded gui development (touchgfx/lvgl)",
    "touchgfx": "embedded gui development (touchgfx/lvgl)",

    # Automotive & Medical Electronics
    "adas": "adas (advanced driver assistance systems) hardware",
    "lin bus": "automotive lin bus",
    "can fd": "can-fd (flexible data-rate)",
    
    # Mechanical Engineering & 3D CAD
    "mechanics of materials": "strength of materials",
    "kom": "kinematics of machinery",
    "dom": "dynamics of machinery",
    "gd&t": "geometric dimensioning and tolerancing",
    "gdt": "geometric dimensioning and tolerancing",
    "3d cad": "solidworks",     # Maps generic 3D modeling to your specific tool
    "creo": "solidworks",       # Another major CAD tool, routed to the Solidworks bucket
    "siemens nx": "solidworks", # Another major CAD tool
    "fea": "finite element analysis",
    "cfd": "computational fluid dynamics",
    
    # Manufacturing & Industrial
    "cnc": "cnc programming",
    "rac": "refrigeration and air conditioning",
    "tqm": "total quality management",
    # --- BATCH 14: Mechanical, Aerospace, Automotive & Advanced Manufacturing ---

    # CAD, PLM & Manufacturing Software
    "fusion360": "fusion 360",
    "autodesk fusion": "fusion 360",
    "creo": "ptc creo",
    "pro-e": "ptc creo",
    "pro/engineer": "ptc creo",
    "nx": "nx-unigraphics",
    "unigraphics": "nx-unigraphics",
    "plm": "product lifecycle management",       # Massive mechanical keyword
    "product lifecycle management": "plm",
    "erp": "erp for manufacturing",
    
    # Automotive & Electric Vehicles
    "hev": "hybrid electric vehicles",
    "ev powertrain": "electric vehicle powertrain",
    "btms": "battery thermal management systems",
    "kers": "kinetic energy recovery systems",
    "nvh": "theory of vibrations",               # Noise, Vibration, & Harshness - huge in Automotive
    "engine calibration": "internal combustion engine calibration",
    "ic engine": "internal combustion engine calibration",
    
    # Aerospace, Fluids & Thermal Systems
    "turbomachinery": "turbo machinery",
    "aerodynamics": "fluid mechanics",
    "hypersonics": "supersonic and hypersonic flows",
    "supersonics": "supersonic and hypersonic flows",
    "heat exchangers": "heat exchanger design",
    "hex design": "heat exchanger design",
    "csm": "computational structural mechanics",
    "mbd": "multibody dynamics",
    
    # Materials, Mechanics & Manufacturing
    "scm": "supply chain management",
    "rp": "rapid prototyping",
    "3d printing": "additive manufacturing",     # Maps general 3D printing to Additive Mfg
    "fracture mechanics": "fatigue and fracture",
    "fatigue analysis": "fatigue and fracture",
    "sma": "shape memory alloys",
    "pressure vessels": "high-pressure vessel design",
    "asme bpvc": "high-pressure vessel design",  # Boiler & Pressure Vessel Code (Industry Standard)
    "industry 4.0": "digital manufacturing",
    
    # Biomechanics & Niche Tech
    "biomechanics": "bio-mechanics",
    "orthotics": "prosthetics and orthotics",
    "prosthetics": "prosthetics and orthotics",
    
    # Unbundling / Normalization
    "wind turbines": "wind turbine engineering",
    "solar energy": "solar energy engineering",
    # --- BATCH 15: Automotive, Manufacturing, Robotics & Facilities ---

    # Automotive, Metrology & Testing
    "cvt": "continuous variable transmissions",
    "nvh": "nvh analysis",                           # Overrides previous mapping!
    "noise vibration and harshness": "nvh analysis",
    "crashworthiness": "crashworthiness and impact analysis",
    "cmm": "coordinate measuring machine",
    "dic": "digital image correlation",
    "tolerance stackup": "tolerancing stack-up analysis",

    # DFx, Sustainability & Advanced Manufacturing
    "dfa": "design for assembly",
    "dfma": "design for assembly",                   # DFMA covers Manufacturing & Assembly
    "dfe": "design for environment",
    "lca": "life cycle assessment",
    "mim": "metal injection molding",
    "lost wax casting": "investment casting",
    "forging": "forging process design",
    "sheet metal": "sheet metal fabrication",
    "jigs and fixtures": "jig and fixture design",
    "tool and die": "tool and die making",
    "tooling design": "tool and die making",
    "awjm": "abrasive waterjet machining",
    "waterjet cutting": "abrasive waterjet machining",
    "edm": "non-traditional machining",              # Electrical Discharge Machining

    # Industrial Engineering & Robotics
    "ppc": "production planning and control",
    "agv": "automated guided vehicles",
    "agvs": "automated guided vehicles",
    "amr": "automated guided vehicles",              # Autonomous Mobile Robots (similar context)
    "cobots": "human-robot collaboration",
    "cobot": "human-robot collaboration",
    "machine vision": "machine vision for robotics", # Overrides generic mapping to fit robotics context

    # Thermal, Piping & Facilities Engineering
    "chp": "combined heat and power",
    "cogeneration": "combined heat and power",
    "whr": "waste heat recovery",
    "piping stress analysis": "pipeline stress analysis",
    "caesar ii": "pipeline stress analysis",         # Industry standard piping stress software
    "fire protection": "fire protection engineering",

}

def normalize_skill(skill):
    return SKILL_SYNONYMS.get(skill.lower(), skill.lower())

def load_skills():
    try:
        with open("skills.txt", "r", encoding="utf-8") as f:
            raw_skills = [line.strip().lower() for line in f if line.strip()]
            
            cleaned_skills = set()
            for skill in raw_skills:
                # Auto-cleans the text file upon loading
                skill = skill.replace(" programming", "")
                skill = skill.replace(" framework", "")
                skill = skill.replace(" development", "")
                cleaned_skills.add(skill)
                
            return list(cleaned_skills)
    except Exception as e:
        print("Error loading skills:", e)
        return []

# Initialize the database here
SKILLS_DB = load_skills()