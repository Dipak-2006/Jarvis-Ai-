import google.generativeai as genai

# Configure the Gemini API with your key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Initialize the model (Gemini 1.5 Pro is a general-purpose chat model)
model = genai.GenerativeModel('gemini-1.5-pro')

# Start a chat session
chat = model.start_chat()

# Send user message
response = chat.send_message("what is coding")

# Print the response
print(response.text)