import openai
import pandas as pd
from flask import Flask, request, jsonify

# Load the shipment tracking spreadsheet
df = pd.read_excel("faq.xlsx")  # Make sure "faq.xlsx" is in the same folder

def find_tracking_info(site_name):
    """Searches for shipment details based on site name."""
    result = df[df['Site'].str.lower() == site_name.lower()]

    if result.empty:
        return "Sorry, I couldn't find any tracking information for that site."

    info = result.iloc[0]  # Get the first match
    response = f"Delivery Status: {info['Delivery Status']}\n"
    response += f"Tracking Number: {info['Tracking Number']}\n"
    response += f"Tracking Link: {info['Proof of Delivery Link']}"
    return response

# Initialize Flask app
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("question")

    # Convert site names to uppercase and remove spaces
    site_names = [str(site).strip().upper() for site in df['Site'].unique()]
    print("Available site names:", site_names)  # Debugging line

    import re
    words = re.findall(r'\b\w+\b', user_input.upper())  # Remove punctuation
    print("Extracted words from question:", words)  # Debugging line

    # Check if any word in the question matches a site name
    matched_sites = [site for site in site_names if site in words]

    if matched_sites:
        return jsonify({"answer": find_tracking_info(matched_sites[0])})

    return jsonify({"answer": "Please provide a valid site name for tracking details."})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render uses this port
    app.run(host="0.0.0.0", port=port, debug=True)  # Force public access
