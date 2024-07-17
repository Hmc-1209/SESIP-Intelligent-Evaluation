from dotenv import dotenv_values
import openai

API_KEY = dotenv_values("../../../../.env").get("API_KEY")
client = openai.OpenAI(api_key=API_KEY)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "assistant", "content": "Please answer the following question in a simply way."},
    {"role": "user", "content": "Could you tell me what is SESIP SFR? Separate sentences with |"}
  ]
)

print(completion.choices[0].message)