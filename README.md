AuditGuard AI 🛡️An Enterprise-Grade Autonomous Compliance & Risk Audit Pipeline with Decoupled Human-in-the-Loop (HITL) Workflows and RAGAS Benchmarking.AuditGuard AI is an automated compliance auditing pipeline designed to ingest, evaluate, and route regulatory documents and vendor contracts. Built with FastAPI, n8n, PostgreSQL, and Docker, the system intelligently branches low-confidence audit evaluations to a non-blocking Human-in-the-Loop (HITL) review form while logging all operational decisions and high-confidence assessments for compliance reporting.📐 Architecture Overview                          ┌───────────────────────────┐
                          │   Incoming Document /     │
                          │   Webhook Payload Ingestion│
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │  FastAPI Audit Engine     │
                          │  (/audit Service)         │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │  n8n Orchestration        │
                          │  (IF Confidence Threshold)│
                          └──────┬─────────────┬──────┘
                                 │             │
                Score >= 0.90    │             │   Score < 0.90
            ┌────────────────────┘             └────────────────────┐
            ▼                                                       ▼
┌───────────────────────┐                               ┌───────────────────────┐
│ Postgres Auto-Pass Log│                               │ Interactive Email     │
│ (audit_logs table)    │                               │ Review Alert          │
└───────────────────────┘                               └───────────┬───────────┘
                                                                    │
                                                                    ▼
                                                        ┌───────────────────────┐
                                                        │ n8n Form Sub-Workflow │
                                                        │ (Compliance Officer)  │
                                                        └───────────┬───────────┘
                                                                    │
                                                                    ▼
                                                        ┌───────────────────────┐
                                                        │ Postgres Review Log   │
                                                        │ (review_decisions)    │
                                                        └───────────────────────┘
✨ Key FeaturesAutomated Audit Processing: Fast ingestion and heuristic analysis via a microservice architecture built on FastAPI.Intelligent Branching Logic: Evaluates risk and extraction confidence scores (Threshold = 0.90).Non-blocking HITL Interface: Low-confidence documents automatically trigger external n8n Form review interfaces sent directly to reviewers via email alerts without crashing or blocking main pipeline execution.Persistent Audit Trail: Relational persistence with PostgreSQL running in Docker to log both automated decisions (audit_logs) and human overrides (review_decisions).Quantitative Evaluation: Integrated benchmarking environment utilizing the RAGAS framework to evaluate Faithfulness, Relevancy, and Context Precision.🛠️ Tech StackBackend API: FastAPI, Uvicorn, Python 3.10+Workflow Automation: n8n (Webhooks, IF Branching, Form Triggers, Email Nodes)Database & Infrastructure: PostgreSQL, Docker, Docker DesktopEvaluation Framework: RAGAS, Hugging Face datasets, PandasDevOps & Tooling: Git, GitHub, SQL, Virtualenv🗄️ Database SchemaPostgreSQL runs inside a Docker container (auditguard-postgres) hosting the auditguard database with two main tables:1. audit_logs (Automated Pass Branch)Column NameData TypeDescriptionidSERIAL PRIMARY KEYAuto-incrementing record IDfilenameVARCHAR(255)Name of audited contract or documentoverall_confidenceFLOATSystem audit confidence scorestatusVARCHAR(50)Audit status (AUTO_APPROVED)created_atTIMESTAMPRecord timestamp2. review_decisions (HITL Branch)Column NameData TypeDescriptionidSERIAL PRIMARY KEYAuto-incrementing record IDfilenameVARCHAR(255)Name of flagged documentreviewer_actionVARCHAR(50)Human decision (APPROVE, REJECT, NEEDS_MODIFICATION)notesTEXTReviewer notes / override justificationreviewed_atTIMESTAMPTimestamp of form submission🚀 Quickstart GuidePrerequisitesDocker Desktop installed and runningPython 3.10+n8n running locally or via Docker1. Database SetupSpin up the PostgreSQL database container and run migrations:Bash# Start Postgres Container
docker run --name auditguard-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=auditguard \
  -p 5432:5432 -d postgres:latest

# Initialize Tables
docker exec -it auditguard-postgres psql -U postgres -d auditguard -c "
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY, 
    filename VARCHAR(255) NOT NULL, 
    overall_confidence FLOAT NOT NULL, 
    status VARCHAR(50) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS review_decisions (
    id SERIAL PRIMARY KEY, 
    filename VARCHAR(255) NOT NULL, 
    reviewer_action VARCHAR(50) NOT NULL, 
    notes TEXT, 
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"
2. Backend Service SetupBash# Install dependencies
pip install fastapi uvicorn pydantic

# Start FastAPI server
uvicorn backend.main:app --reload
3. n8n Workflow ImportOpen n8n (http://localhost:5678).Import workflows/01_Compliance_Audit_Pipeline.json.Import workflows/02_Compliance_Review_Handler.json.Configure PostgreSQL node credentials (Host: 127.0.0.1 / host.docker.internal, DB: auditguard).Activate both workflows.📊 Quantitative Evaluation (RAGAS)To benchmark extraction fidelity and rule-matching accuracy, the project includes an automated evaluation suite in evals/eval_pipeline.py.Bashcd evals
pip install -r requirements-eval.txt
python eval_pipeline.py
Key Metrics TrackedFaithfulness: Verifies extracted compliance statements match source contract context.Context Precision: Measures retrieval relevance for compliance checks.Answer Relevancy: Ensures extracted outputs directly address target audit queries.📂 Repository StructurePlaintextauditguard-ai/
├── backend/
│   └── main.py                     # FastAPI compliance audit service
├── evals/
│   ├── eval_pipeline.py            # RAGAS benchmarking script
│   └── requirements-eval.txt
├── workflows/
│   ├── 01_Compliance_Audit_Pipeline.json  # Main audit & branching workflow
│   └── 02_Compliance_Review_Handler.json # HITL form trigger & logging sub-workflow
├── .gitignore
└── README.md
