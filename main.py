from flask import Flask, request, Response
from transformers import pipeline
import requests

app = Flask(__name__)

# Replace with your actual bot token
bot_token = "7429562748:AAFCReITBvMbUWn8COZIvvVyUgYjocGMOME"
url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

# Initialize the LLM pipeline with a lightweight model
generator = pipeline('text-generation', model='distilbert/distilgpt2')

@app.route('/webhook', methods=['POST'])
def post_example():
    if request.method == 'POST':
        # Access POST data from the request
        msg = request.get_json()
        print("Message: ", msg)

        # Try to parse the message
        try:
            chat_id = msg['message']['chat']['id']
            text = msg['message']['text']  # This gets the text from the msg
            print("Received text:", text)

            # Generate a response using the LLM
            response = generator(text, max_length=1000, num_return_sequences=1)
            reply_text = response[0]['generated_text']

            # Send the response back to the Telegram chat
            payload = {
                'chat_id': chat_id,
                'text': reply_text
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
