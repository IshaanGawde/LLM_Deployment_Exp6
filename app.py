from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "google/flan-t5-small"

app = FastAPI(title="LLM API")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "LLM API is running"}

@app.post("/generate")
def generate(request: PromptRequest):
    inputs = tokenizer(
        request.prompt,
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=50
        )

    response = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return {"response": response}