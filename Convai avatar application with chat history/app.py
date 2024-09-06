from flask import Flask, request, render_template, jsonify
import requests
import traceback
import logging

app = Flask(__name__)
app.config["SECRET_KEY"] = "soghsrpg"

API_KEY = "33c529135149b97bdf07f81f3cebf0e9"
CHARACTER_ID = "087f9296-479e-11ef-9a41-42010a7be011"
API_URL = "https://api.convai.com/character/getResponse"

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html", conversation_history=conversation_history)

@app.route("/api_request", methods=["POST"])
def chat():
    global conversation_history 
    try:

        # Capture the user input from the request
        user_text = request.json.get('userText')

        #append user text to chat history 
        conversation_history.append({"role": "user", "message": user_text})


        # Prepare the payload with the user input
        payload = {
            'userText': user_text,
            'charID': CHARACTER_ID,
            'sessionID': '-1'
        }

        # Set the headers with the API key
        headers = {
            'CONVAI-API-KEY': API_KEY
        }

        # Make the POST request to the API
        response = requests.post(API_URL, headers=headers, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        #get API response
        api_response = response.json()

        #extract character reply 
        character_reply = api_response.get('response', '')

        # Append the character's reply to the conversation history
        conversation_history.append({"role": "chatbot", "message": character_reply})

        return jsonify({"response": character_reply, "history": conversation_history})
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(debug=True)
