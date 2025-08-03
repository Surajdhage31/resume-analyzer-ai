from flask import Flask, request, jsonify
import openai
import fitz  # PyMuPDF for PDF parsing

app = Flask(__name__)
openai.api_key = 'your-openai-api-key'  # Replace with your key

# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume_file' in request.files:
        file = request.files['resume_file']
        resume_text = extract_text_from_pdf(file)
    else:
        resume_text = request.json.get('resume', '')

    prompt = f"""
    You are a senior technical recruiter.

    Evaluate this software developer resume based on:
    - Technical skills (Java, Python, C/C++)
    - Formatting and clarity
    - Language and grammar
    - Relevance to job roles

    Provide:
    1. A score out of 10
    2. Strengths
    3. Suggestions for improvement

    Resume:
    {resume_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    analysis = response['choices'][0]['message']['content']
    return jsonify({'analysis': analysis})

if __name__ == '__main__':
    app.run(debug=True)
