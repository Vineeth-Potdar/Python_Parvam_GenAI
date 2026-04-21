from google import genai

client = genai.Client(api_key="AIzaSyC4VO63KH8HbzGtVnLM3j-EC69Jpx1Q6z4")

models = client.models.list()

for m in models:
    print(m.name)