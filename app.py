from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def health_check():
    return jsonify({"status": "ok"})

@app.route("/generate", methods=["POST"])
def generate_paper():
    data = request.json

    # Extract and validate inputs
    topic = data.get("topic", "").strip()
    format_ = data.get("format", "")
    length = data.get("length", "")
    output_type = data.get("outputType", "")

    # Validations
    if not topic:
        return jsonify({"success": False, "error": "Topic is required"}), 400
    if len(topic) > 100:
        return jsonify({"success": False, "error": "Topic must be 100 characters or less"}), 400
    if format_ not in ["ieee", "springer", "apa"]:
        return jsonify({"success": False, "error": "Invalid format"}), 400
    if length not in ["short", "medium", "long"]:
        return jsonify({"success": False, "error": "Invalid length"}), 400
    if output_type not in ["summary", "abstract", "full"]:
        return jsonify({"success": False, "error": "Invalid output type"}), 400

    # Build prompt
    prompt = f"""
    Write a research paper on the topic: {topic}.
    Format: {format_}
    Length: {length}
    Output Type: {output_type}
    """



    try:
        # Call Groq API
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        paper = response.choices[0].message.content
        return jsonify({"success": True, "paper": paper})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
