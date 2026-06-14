from ai.llm_client import LLMClient

client = LLMClient()

response = client.get_response("Hello, who are you?")

print(response)