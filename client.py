from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)