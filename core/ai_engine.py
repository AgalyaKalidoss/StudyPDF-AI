from google import genai

from config import GOOGLE_API_KEY


# =====================================================
# GEMINI CLIENT
# =====================================================

client = genai.Client(
    api_key=GOOGLE_API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


# =====================================================
# GENERATE RESPONSE
# =====================================================

def generate_response(prompt):

    try:

        interaction = client.interactions.create(

            model=MODEL_NAME,

            input=prompt

        )


        if not interaction.output_text:

            return "No response was generated."


        return interaction.output_text.strip()


    except Exception as e:

        return f"AI Error: {str(e)}"


# =====================================================
# ASK PDF
# =====================================================

def ask_pdf(
    question,
    pdf_text
):

    prompt = f"""
You are StudyPDF AI, an academic assistant.

Answer the student's question using ONLY
the information provided in the PDF.

If the answer cannot be found in the PDF, say:

"I couldn't find this information in the uploaded PDF."

Do not invent information.

Give the answer clearly and academically.

Question:
{question}

PDF Content:
{pdf_text}
"""


    return generate_response(
        prompt
    )


# =====================================================
# SUMMARY
# =====================================================

def summarize_pdf(pdf_text):

    prompt = f"""
You are StudyPDF AI.

Create a clear academic summary of the PDF.

Use this structure:

## Overview

## Main Concepts

## Important Definitions

## Key Points

## Important Examples

## Quick Revision Notes

Keep the explanation student-friendly.

Use ONLY the uploaded PDF.

PDF Content:
{pdf_text}
"""


    return generate_response(
        prompt
    )


# =====================================================
# TOPIC
# =====================================================

def extract_topic(
    topic,
    pdf_text
):

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


    return generate_response(
        prompt
    )


# =====================================================
# 2-MARK QUESTIONS
# =====================================================

def generate_two_mark_questions(
    pdf_text,
    count=10
):

    prompt = f"""
You are an expert university examination
question generator.

Using ONLY the uploaded PDF, generate
{count} important 2-mark questions with answers.

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

Avoid duplicates.

Do not invent information.

PDF Content:
{pdf_text}
"""


    return generate_response(
        prompt
    )


# =====================================================
# 16-MARK QUESTIONS
# =====================================================

def generate_sixteen_mark_questions(
    pdf_text,
    count=5
):

    prompt = f"""
You are an expert university examination
preparation assistant.

Using ONLY the uploaded PDF, generate
{count} important 16-mark questions
and detailed answers.

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


    return generate_response(
        prompt
    )


# =====================================================
# IMPORTANT QUESTIONS
# =====================================================

def generate_important_questions(
    pdf_text,
    count=15
):

    prompt = f"""
You are an experienced university
exam preparation assistant.

Analyze the uploaded PDF and identify
{count} important questions.

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


    return generate_response(
        prompt
    )
