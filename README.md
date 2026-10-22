# Experiment 6 – Setting up LLM Deployment Infrastructure

This project implements and documents a basic Large Language Model (LLM) deployment infrastructure using a pre-trained FLAN-T5-small model. The application accepts a text prompt, performs inference using the LLM, and returns the generated response through a REST API. The API is implemented using FastAPI, served using Uvicorn, tested through Swagger UI, and containerized using Docker.

---

## 1. Experiment Overview

### Aim

To set up a basic LLM deployment infrastructure by creating an inference application, exposing the model through a REST API, and containerizing the application using Docker.

### Problem Statement

Develop a simple LLM application that accepts a text prompt and returns a generated response. Expose the application through a FastAPI REST API and package it into a Docker container for deployment.

### Objectives

- Understand the basic requirements of LLM deployment.
- Load a pre-trained LLM and perform inference.
- Create a REST API using FastAPI.
- Run the API using Uvicorn.
- Test the API using Swagger UI.
- Containerize the application using Docker.
- Verify the containerized LLM API.

The experiment follows the deployment flow:

```text
Client
   ↓
FastAPI REST API
   ↓
Inference Function
   ↓
Tokenizer + FLAN-T5-small
   ↓
Generated Response
```

---

## 2. Model Used

The application uses:

```text
google/flan-t5-small
```

FLAN-T5-small is used only for inference in this experiment. No model fine-tuning is performed.

The model and tokenizer are loaded using:

```python
AutoTokenizer
AutoModelForSeq2SeqLM
```

The application performs text-to-text generation directly using the model's `generate()` method.

### Important Compatibility Note

The application does not use the older:

```python
pipeline("text2text-generation", ...)
```

approach because newer Transformers releases removed that pipeline. Direct `AutoModelForSeq2SeqLM` inference is therefore used in the final working implementation.

---

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Hugging Face Transformers | Loading and running the LLM |
| PyTorch | Model inference |
| FastAPI | REST API framework |
| Uvicorn | ASGI server for FastAPI |
| Swagger UI | Interactive API testing |
| Docker | Application containerization |
| Pydantic | Request-data validation |

---

## 4. Project Structure

```text
LLM_Deployment/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
```

The following local/generated files are intentionally excluded from version control:

```text
venv/
.venv/
__pycache__/
*.pyc
.env
```

---

## 5. Application Architecture

The deployment architecture consists of the following stages:

```text
User / Client
      │
      ▼
FastAPI REST API
      │
      ▼
POST /generate
      │
      ▼
Prompt Tokenization
      │
      ▼
FLAN-T5-small
      │
      ▼
Text Generation
      │
      ▼
JSON Response
```

FastAPI provides the API endpoints, Uvicorn runs the application server, and Docker packages the application and its dependencies into a container.

---

## 6. API Endpoints

### GET `/`

Used to verify that the FastAPI application is running.

Example response:

```json
{
  "message": "LLM API is running"
}
```

### POST `/generate`

Accepts a text prompt and returns a generated LLM response.

Example request:

```json
{
  "prompt": "What is artificial intelligence?"
}
```

Example response:

```json
{
  "response": "artificial intelligence"
}
```

---

## 7. Local Setup

### Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run FastAPI Locally

```bash
uvicorn app:app --reload
```

The API is then available at:

```text
http://127.0.0.1:8000
```

Swagger UI can be opened at:

```text
http://127.0.0.1:8000/docs
```

---

## 8. Swagger UI Testing

Swagger UI provides an interactive interface for testing the REST API.

Open:

```text
http://127.0.0.1:8000/docs
```

The available endpoints are:

```text
GET  /
POST /generate
```

For `/generate`, select **Try it out**, enter a prompt, and select **Execute**.

---

## 9. Experiment Prompts and Actual Outputs

The following five prompts were used to test the LLM API.

| Sr. No. | Prompt | Generated Response |
|---:|---|---|
| 1 | What is artificial intelligence? | artificial intelligence |
| 2 | Explain machine learning in simple words. | Machine learning is a process of learning. |
| 3 | What is a neural network? | a neural network |
| 4 | Explain the Transformer model. | The Transformer is a redesigned version of the X-ray ray. |
| 5 | What is natural language processing? | natural language processing |

The API successfully accepted all five prompts and returned generated responses.

Some responses were short or imperfect, especially the Transformer response. This is an expected limitation of using a small pre-trained model without task-specific fine-tuning.

---

## 10. Docker Deployment

Docker is used to package the FastAPI application together with its Python runtime and dependencies.

### Build the Docker Image

From the project directory:

```bash
docker build -t llm-api .
```

The resulting image is:

```text
llm-api:latest
```

Verify the image:

```bash
docker images
```

### Run the Docker Container

```bash
docker run -p 8000:8000 llm-api
```

The container runs Uvicorn on:

```text
0.0.0.0:8000
```

The API can then be accessed from the host machine through:

```text
http://localhost:8000
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

---

## 11. Docker Deployment Workflow

```text
app.py
   │
   ├── requirements.txt
   │
   ▼
Dockerfile
   │
   ▼
docker build
   │
   ▼
llm-api Docker Image
   │
   ▼
docker run
   │
   ▼
Container
   │
   ▼
Uvicorn + FastAPI
   │
   ▼
Swagger UI
   │
   ▼
/generate
   │
   ▼
FLAN-T5-small Response
```

---

## 12. Deployment Verification

| Deployment Method | API Working? | Observation |
|---|---|---|
| Direct FastAPI | Yes | FastAPI application ran successfully using Uvicorn and generated LLM responses. |
| Docker Container | Yes | The application ran successfully inside the Docker container and the `/generate` endpoint was successfully accessed through Swagger UI. |

Both direct and Dockerized deployment were successfully verified.

---

## 13. Deployment Components

| Component | Role |
|---|---|
| **FLAN-T5-small** | Performs LLM inference and generates responses. |
| **FastAPI** | Provides the REST API endpoints. |
| **Uvicorn** | Runs the FastAPI application as an ASGI server. |
| **Swagger UI** | Provides an interactive interface for API testing. |
| **Docker** | Containerizes the application and its dependencies. |

---

## 14. Dockerfile

The application is containerized using the following Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Explanation

- `FROM python:3.11-slim` provides a lightweight Python environment.
- `WORKDIR /app` sets the working directory inside the container.
- `COPY requirements.txt .` copies the dependency file.
- `RUN pip install --no-cache-dir -r requirements.txt` installs the required Python packages.
- `COPY app.py .` copies the application source code.
- `EXPOSE 8000` documents the port used by the API.
- `CMD` starts the FastAPI application using Uvicorn.

---

## 15. Recreating the Project on Another Computer

This repository contains the files required to recreate the application on another computer.

Clone the repository:

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd LLM_Deployment
```

### Option 1 – Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application:

```bash
uvicorn app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

### Option 2 – Run Using Docker

Build the Docker image:

```bash
docker build -t llm-api .
```

Run the container:

```bash
docker run -p 8000:8000 llm-api
```

Then open:

```text
http://localhost:8000/docs
```

The Python virtual environment does not need to be copied from the original computer because it can be recreated using `requirements.txt`.

The Docker image also does not need to be uploaded to the repository because it can be rebuilt from the Dockerfile.

The FLAN-T5 model files are downloaded automatically when the application first loads the model on the new computer.
