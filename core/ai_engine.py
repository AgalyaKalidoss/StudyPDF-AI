from google import genai

from config import GOOGLE_API_KEY


# Create Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)


MODEL_NAME = "gemini-3.6-flash"


def generate_response(prompt):
    """
    Send a prompt to Gemini and return the generated response.
    """

    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt
        )

        return interaction.output_text.strip()

    except Exception as e:
        return f"AI Error: {str(e)}"


def ask_pdf(question, pdf_text):
    """
    Answer a question using only the uploaded PDF.
    """

    prompt = f"""
You are StudyPDF AI, an academic assistant.

Answer the student's question using ONLY the information
provided in the PDF content.

If the answer cannot be found in the PDF, say:

"I couldn't find this information in the uploaded PDF."

Do not invent information.

Give the answer clearly and academically.

Question:
{question}

PDF Content:
{pdf_text}
"""

    return generate_response(prompt)


def summarize_pdf(pdf_text):
    """
    Generate a structured summary of the PDF.
    """

    prompt = f"""
You are StudyPDF AI.

Create a clear academic summary of the following PDF.

Use this structure:

## Overview

## Main Concepts

## Important Definitions

## Key Points

## Important Examples

## Quick Revision Notes

Keep the explanation student-friendly.

PDF Content:
{pdf_text}
"""

    return generate_response(prompt)


def extract_topic(topic, pdf_text):
    """
    Explain a specific topic from the PDF.
    """

    prompt = f"""
You are StudyPDF AI.

Find the topic "{topic}" in the PDF.

Explain ONLY information related to this topic.

Use:

## Topic

## Definition

## Explanation

## Key Points

## Important Concepts

## Example

## Exam Notes

If the topic does not exist, say:

"I couldn't find this topic in the uploaded PDF."

PDF Content:
{pdf_text}
"""

    return generate_response(prompt)


def generate_two_mark_questions(pdf_text, count=10):
    """
    Generate important 2-mark questions.
    """

    prompt = f"""
You are an expert university examination question generator.

Using ONLY the uploaded PDF, generate {count}
important 2-mark questions with answers.

Format:

### 1. Question
**Answer:** Short and precise answer.

### 2. Question
**Answer:** Short and precise answer.

Focus on:

- Definitions
- Concepts
- Important facts
- Short explanations

Avoid duplicates and do not invent information.

PDF Content:
{pdf_text}
"""

    return generate_response(prompt)


def generate_sixteen_mark_questions(pdf_text, count=5):
    """
    Generate detailed 16-mark questions and answers.
    """

    prompt = f"""
You are an expert university examination preparation assistant.

Using ONLY the uploaded PDF, generate {count}
important 16-mark questions and detailed answers.

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

Answers must be detailed and exam-oriented.

Do not invent information.

PDF Content:
{pdf_text}
"""

    return generate_response(prompt)


def generate_important_questions(pdf_text, count=15):
    """
    Identify important examination questions.
    """

    prompt = f"""
You are an experienced university exam preparation expert.

Analyze the uploaded PDF and identify the {count}
most important questions.

Divide them into:

## Very Important

## Important

## Moderate Priority

For each question provide:

- Question
- Priority
- Topic
- Why it is important

Use ONLY the uploaded PDF.

PDF Content:
{pdf_text}
"""

    return generate_response(prompt)