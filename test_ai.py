from core.ai_engine import generate_response


print("=" * 50)
print("       STUDYPDF AI - GEMINI TEST")
print("=" * 50)

response = generate_response(
    "Explain Artificial Intelligence in 3 simple points."
)

print("\nGemini Response:\n")
print(response)

print("\n" + "=" * 50)
print("             TEST COMPLETE")
print("=" * 50)