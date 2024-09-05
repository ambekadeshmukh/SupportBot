from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Updated responses for Waterloo services
responses = {
    "greetings": "Hello! How can I assist you with Waterloo's services today?",
    "garbage_collection": "I'll check the garbage collection details for {address}. Generally, collection is weekly, but I'll need to confirm the specific day for your address.",
    "parks": "Waterloo has many beautiful parks! Some popular ones include Waterloo Park, Laurel Creek Conservation Area, and RIM Park. Dogs are allowed in most parks but must be leashed. For event bookings, you'll need to contact the city's recreation department.",
    "transit": "Waterloo is served by Grand River Transit (GRT) buses and the ION light rail. A single ride adult fare is $3.50, and monthly passes are available. You can find detailed schedules on the GRT website.",
    "fallback": "I'm sorry, I didn't understand that. Could you please rephrase your question?"
}

def get_intent(message):
    message = message.lower()
    if any(word in message for word in ["hello", "hi", "hey", "good morning"]):
        return "greetings"
    elif any(word in message for word in ["garbage", "trash", "collection", "pickup"]):
        return "garbage_collection"
    elif any(word in message for word in ["park", "dog", "event"]):
        return "parks"
    elif any(word in message for word in ["bus", "transit", "light rail", "ion"]):
        return "transit"
    else:
        return "fallback"

def get_response(message):
    intent = get_intent(message)
    if intent == "garbage_collection":
        # Extract address (this is a simplistic approach, you might want to improve this)
        address = re.search(r'for (.*)', message)
        if address:
            return responses[intent].format(address=address.group(1))
        else:
            return "What's your street address for the collection information?"
    return responses[intent]

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = get_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)