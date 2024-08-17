from flask import Flask, request, Response
from huggingface_hub import InferenceClient
import requests

app = Flask(__name__)

# Replace with your actual bot token
bot_token = "7429562748:AAFCReITBvMbUWn8COZIvvVyUgYjocGMOME"
url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

# Initialize the Hugging Face InferenceClient with your API key
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token="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",
)

@app.route('/webhook', methods=['POST'])
def post_example():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id = msg['message']['chat']['id']
            text = msg['message']['text']

            # Generate chat-like response using the Hugging Face InferenceClient
            response_text = ""
            for message in client.chat_completion(
                messages=[{"role": "user", "content": text}],
                max_tokens=500,
                stream=True,
            ):
                response_text += message.choices[0].delta.content

            # Send the response back to the Telegram chat
            payload = {
                'chat_id': chat_id,
                'text': response_text
            }
            r = requests.post(url, json=payload)

            if r.status_code == 200:
                return Response('ok', status=200)
            else:
                return Response('Failed to send message to Telegram', status=500)
        except Exception as e:
            print("Error:", e)
            return Response('Error processing the message', status=500)

    return Response('ok', status=200)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
