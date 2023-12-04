import openai
from flask import Flask, request, jsonify
from db_operations.connection import create_client,close_client,load_data
from db_operations.query_data import search_items

app = Flask(__name__)

def get_search_terms(user_input):
    try:
        # Ask the model to interpret the user's query in terms of searchable database terms
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Interpret this user's query for a database search: '{user_input}'",
            max_tokens=50
        )
        interpreted_query = response.choices[0].text.strip()
        return interpreted_query
    except openai.error.OpenAIError as e:
        print(f"Error with OpenAI API: {e}")
        return ""

@app.route('/search')
def search():
    user_input = request.args.get('q', '')
    interpreted_query = get_search_terms(user_input)
    
    client = create_client()
    results = []
    try:
        if interpreted_query:
            results = search_items(interpreted_query, client)
    finally:
        client.close()
    return jsonify([result.to_dict() for result in results])  # Convert results to a list of dicts

if __name__ == "__main__":
    app.run(debug=True)