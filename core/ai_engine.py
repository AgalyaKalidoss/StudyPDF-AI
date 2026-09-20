from google import genai

from config import GOOGLE_API_KEY


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=GOOGLE_API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


# ==========================================
# COMMON AI FUNCTION
# ==========================================

def generate_response(prompt):

    try:

        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt
        )

        if interaction.output_text:

            return interaction.output_text.strip()

        return "No response was generated."

    except Exception as e:

        print(
            "GEMINI ERROR:",
            repr(e)
        )

        return f"AI Error: {str(e)}"


# ==========================================
# ASK PDF
# ==========================================

def ask_pdf(
    question,
    pdf_text
):

    prompt = f"""
You are StudyPDF AI, an academic assistant.

Answer the student's question using ONLY
the information provided in the PDF.

Rules:

1. Do not use outside information.
2. Do not invent facts.
3. If the answer is not available in the PDF,
   clearly say that it was not found.
4. Give a clear and student-friendly answer.
5. Use headings or bullet points when useful.

Question:
{question}

PDF CONTENT:
{pdf_text}
"""

    return generate_response(prompt)


# ==========================================
# SUMMARY
# ==========================================

def summarize_pdf(pdf_text):

    prompt = f"""
You are StudyPDF AI.

Create a useful academic summary of the uploaded PDF.

Use this structure:

## Overview

## Main Concepts

## Important Definitions

## Key Points

## Important Examples

## Quick Revision Notes

Rules:

- Use ONLY the PDF.
- Do not invent information.
- Keep it student-friendly.
- Highlight exam-relevant points.
- Avoid unnecessary repetition.

PDF CONTENT:
{pdf_text}
"""

    return generate_response(prompt)


# ==========================================
# TOPIC EXTRACTION
# ==========================================

def extract_topic(
    topic,
    pdf_text
):

    prompt = f"""
You are StudyPDF AI.

Find the topic "{topic}" in the uploaded PDF.

Explain ONLY information related to that topic.

Use:

## Topic

## Definition

## Explanation

## Key Points

## Important Concepts

## Example

## Exam Notes

If the topic cannot be found,
say:

"I couldn't find this topic in the uploaded PDF."

PDF CONTENT:
{pdf_text}
"""

    return generate_response(prompt)


# ==========================================
# 2-MARK QUESTIONS
# ==========================================

def generate_two_mark_questions(
    pdf_text,
    count=10
):

    prompt = f"""
You are an expert university examination
question generator.

Using ONLY the uploaded PDF, generate
{count} important 2-mark questions
with short answers.

Use this exact style:

### 1. Question

**Answer:** Short and precise answer.

### 2. Question

**Answer:** Short and precise answer.

Focus on:

- Definitions
- Important concepts
- Key facts
- Short explanations
- Terminology
- Important formulas if present

Rules:

- Use ONLY the PDF.
- Do not invent information.
- Avoid duplicate questions.
- Answers should be suitable for a 2-mark exam question.

PDF CONTENT:
{pdf_text}
"""

    return generate_response(prompt)


# ==========================================
# 16-MARK QUESTIONS
# ==========================================

def generate_sixteen_mark_questions(
    pdf_text,
    count=5
):

    prompt = f"""
You are an expert university examination
preparation assistant.

Using ONLY the uploaded PDF, generate
{count} important 16-mark questions
with detailed answers.

For every question use:

# Question

## Introduction

## Definition / Concept

## Detailed Explanation

## Important Points

## Example / Application

## Advantages

## Limitations

## Conclusion

Rules:

- Use ONLY the PDF.
- Do not invent information.
- Make answers detailed.
- Make answers suitable for university examinations.
- Avoid duplicate questions.

PDF CONTENT:
{pdf_text}
"""

    return generate_response(prompt)


# ==========================================
# IMPORTANT QUESTIONS
# ==========================================

def generate_important_questions(
    pdf_text,
    count=15
):

    prompt = f"""
You are an experienced university
examination preparation expert.

Analyze the uploaded PDF and generate
{count} important examination questions.

Organize them into:

## Very Important

## Important

## Moderate Priority

For each question provide:

- Question
- Topic
- Priority
- Why it is important

Rules:

- Use ONLY the uploaded PDF.
- Do not invent information.
- Avoid duplicates.
- Focus on topics actually present in the PDF.

PDF CONTENT:
{pdf_text}
"""

    return generate_response(prompt)
