import requests
import json
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

def call_groq(prompt):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    response = requests.post(GROQ_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def get_summary(text):
    prompt = f"""Summarize the following study material in simple, easy-to-understand points.
Give 8-10 key points. Use simple language a student can understand.

Text:
{text[:3000]}

Format your response as a numbered list of key points."""
    return call_groq(prompt)

def get_mcqs(text):
    prompt = f"""Generate 10 multiple choice questions from the following study material.

Text:
{text[:3000]}

Respond ONLY in this exact JSON format (no markdown, no backticks):
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
      "answer": "A. option1",
      "explanation": "Brief explanation why this is correct"
    }}
  ]
}}"""
    raw = call_groq(prompt)
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)

def get_flashcards(text):
    prompt = f"""Create 10 flashcards from the following study material.
Each flashcard has a term and its definition.

Text:
{text[:3000]}

Respond ONLY in this exact JSON format (no markdown, no backticks):
{{
  "flashcards": [
    {{
      "term": "Term or concept",
      "definition": "Clear simple definition"
    }}
  ]
}}"""
    raw = call_groq(prompt)
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)

def get_important_topics(text):
    prompt = f"""From the following study material, identify the most important topics a student should focus on for an exam.

Text:
{text[:3000]}

Respond ONLY in this exact JSON format (no markdown, no backticks):
{{
  "topics": [
    {{
      "topic": "Topic name",
      "importance": "HIGH or MEDIUM",
      "description": "Why this topic is important and what to know about it"
    }}
  ]
}}"""
    raw = call_groq(prompt)
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)