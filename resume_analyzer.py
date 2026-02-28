import PyPDF2
from docx import Document
from groq import Groq
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)


# -------------------------
# Extract text from PDF
# -------------------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


# -------------------------
# Extract text from DOCX
# -------------------------
def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


# -------------------------
# Analyze Resume with AI
# -------------------------
def analyze_resume(text):

    prompt = f"""
    Analyze the following resume and return clearly separated sections
    with headings exactly like below:

    Skills:
    - bullet points

    Strengths:
    - bullet points

    Weaknesses:
    - bullet points

    Missing Skills:
    - bullet points

    Professional Summary:
    short paragraph

    Personalized Recommendations:
    - Specific skills to learn
    - Certifications to consider
    - Project improvements
    - Resume improvement tips

    Also give an overall Resume Score out of 10 at the end in this format:
    Resume Score: X/10

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    ai_output = response.choices[0].message.content

    # Extract score safely using REGEX
    score = 7.0  # default fallback

    try:
        match = re.search(r'(\d+(\.\d+)?)/10', ai_output)
        if match:
            score = float(match.group(1))
    except:
        score = 7.0

    return ai_output, score