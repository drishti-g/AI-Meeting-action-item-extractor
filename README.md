# AI Meeting Action Item Extractor

An LLM-powered application that converts unstructured meeting transcripts into structured, actionable tasks with responsible owners, deadlines, status, and confidence scores.

**Live Demo:** [AI Meeting Action Item Extractor](https://aimeetingactionitemextractor.streamlit.app/)

---

## Overview

Important action items are often buried inside long and unstructured meeting conversations. This project automates the process of identifying those actions and converting them into a structured format that is easier to review and follow up on.

The system is designed as a multi-stage pipeline:

```text
                 ┌────────────────────┐
                 │ Meeting Transcript │
                 └─────────┬──────────┘
                           ↓
                 ┌───────────────────┐
                 │     Cleaning      │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │   LLM Extraction  │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │ Structured Output │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │  Rule Validation  │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │ LLM Verification  │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │ Final Action Items│
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │    Evaluation     │
                 └───────────────────┘
```

---

## Key Features

### Action Item Extraction

Automatically identifies actionable tasks from meeting transcripts and extracts:

- **Task** — What needs to be done
- **Owner** — Who is responsible
- **Deadline** — When it needs to be completed
- **Status** — Current state of the task
- **Confidence** — Model confidence for the extracted information

### Transcript Cleaning

Before extraction, the transcript goes through a preprocessing step to remove unnecessary blank lines and clean the overall format.

The cleaned transcript can also be viewed directly in the application.

### Structured Output

The LLM output is converted into a structured schema using Pydantic.

This ensures that every extracted action item follows a consistent format instead of returning an unstructured text response.

### Rule-Based Validation

The initial extraction is checked using deterministic validation rules.

The validator checks for:

- Missing owners
- Missing deadlines
- Invalid status values
- Invalid confidence scores
- Possible duplicate tasks

### LLM Verification and Refinement

The extracted action items are passed through a second LLM verification stage.

The verification step checks the results against the original transcript for:

- Missed action items
- Duplicate tasks
- Overlapping tasks
- Incorrect owners
- Assignment conflicts
- Unsupported deadlines
- Incorrect status
- Unsupported assumptions

The original meeting transcript remains the source of truth during this stage.

### Built-in Evaluation

The application includes a dedicated evaluation section for measuring the performance of the complete pipeline.

It provides:

- Precision
- Recall
- F1 Score
- Owner Accuracy
- Deadline Accuracy
- Status Accuracy
- Individual test-case results
- Ground-truth vs model-output comparison
- True positives, false positives, and false negatives

### Custom Evaluation

The application also allows users to evaluate the model using their own data.

Users can provide:

1. Their own meeting transcript
2. Their manually prepared ground-truth action items

The transcript then passes through the same extraction, validation, and verification pipeline before the evaluation metrics are calculated.

Custom evaluation results remain separate from the official evaluation dataset.

---

## Evaluation Metrics

### Precision

Measures how many of the action items predicted by the model were correct.

```text
Precision = TP / (TP + FP)
```

### Recall

Measures how many of the actual action items were successfully identified.

```text
Recall = TP / (TP + FN)
```

### F1 Score

Provides a combined measure of precision and recall.

```text
F1 = 2 × (Precision × Recall)
     / (Precision + Recall)
```

### Field-Level Accuracy

For matched action items, the system separately evaluates:

- Owner Accuracy
- Deadline Accuracy
- Status Accuracy

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Google Gemini | LLM extraction and verification |
| LangChain | LLM integration and structured output |
| Pydantic | Data modelling and validation |
| Streamlit | Web application |
| Pandas | Result presentation |
| Git & GitHub | Version control |

---

## Project Structure

```text
AI-Meeting-Action-Item-Extractor/
│
├── .devcontainer/
├── .gitignore
├── .python-version
├── README.md
├── cleaner.py
├── evaluation_data.py
├── evaluator.py
├── main.py
├── pyproject.toml
├── requirements.txt
├── system_prompts.py
├── uv.lock
└── validator.py
```

### Core Components

**`main.py`**  
Main Streamlit application containing the extraction workflow, verification workflow, UI, and evaluation interface.

**`cleaner.py`**  
Handles transcript preprocessing and cleaning.

**`validator.py`**  
Performs deterministic validation checks on extracted action items.

**`evaluator.py`**  
Compares model predictions with ground-truth data and calculates evaluation metrics.

**`evaluation_data.py`**  
Contains the official evaluation dataset and sample transcripts.

**`system_prompts.py`**  
Contains the prompts used for action-item extraction and verification.

---

## Application Workflow

### Extract Action Items

Users can either paste their own transcript or select one of the provided sample transcripts.

The application then:

1. Cleans the transcript
2. Extracts action items using Gemini
3. Performs rule-based validation
4. Verifies and refines the extracted results using a second LLM pass
5. Displays the final structured action items

### Evaluate

The Evaluation section provides two options:

**Official Evaluation**

Run the predefined evaluation dataset and view the overall and individual test-case metrics.

**Custom Evaluation**

Provide your own transcript and ground-truth action items to independently evaluate the model.

---

## Design Approach

The project intentionally follows a simple and explainable architecture.

Instead of treating the first LLM response as the final answer, the system uses multiple stages:

```text
LLM Extraction
      ↓
Rule-Based Validation
      ↓
LLM Verification
      ↓
Final Output
      ↓
Evaluation
```

This approach keeps the system modular while providing multiple opportunities to identify and correct extraction errors.

The current implementation does not use:

- RAG
- Vector databases
- Multi-agent systems
- Fine-tuning
- External task-management databases

The focus is on building and evaluating a clear LLM-based extraction pipeline.

---

## Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Meeting-Action-Item-Extractor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY2=your_api_key_here
```

### 5. Start the application

```bash
streamlit run main.py
```

---

## Environment Variables

For local development, create a `.env` file containing:

```env
GEMINI_API_KEY2=your_api_key_here
```

For Streamlit Cloud deployment, add the API key through the application's Secrets settings.

Never commit API keys or `.env` files to the repository.

---

## Future Improvements

Potential future extensions include:

- Support for TXT, PDF, and DOCX transcript uploads
- Automatic transcription from recorded meetings
- Calendar integration
- Task-management integrations
- CSV and JSON export
- Improved handling of long transcripts
- Larger and more diverse evaluation datasets
- Automated task reminders

---

## Live Application

Try the deployed application:

**[AI Meeting Action Item Extractor](https://aimeetingactionitemextractor.streamlit.app/)**

---

## Author

**Drishti Goel**

BTech Student at GGSIPU

Interested in Machine Learning, Generative AI, Data Science,Agentic AI, Applied AI and building practical AI applications.