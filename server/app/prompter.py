import openai

# openai.api_key = "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"
openai.api_key = "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"

output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": """
        Hello.
        """,
        }
    ],
)

print(output["choices"]["message"])
