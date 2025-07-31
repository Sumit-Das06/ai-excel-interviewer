AI-Powered Excel Mock Interviewer
Project for the Coding Ninjas AI Engineer Assignment
By: Sumit Das

1. Project Overview
This project is a proof-of-concept (PoC) for an AI-powered system designed to automate the technical screening of a candidate's Microsoft Excel skills. The system simulates a real-world technical interview by presenting candidates with practical business problems and evaluating the formulas they write to solve them.

The goal is to provide a consistent, scalable, and reliable evaluation method, addressing the bottlenecks in the manual screening process, as outlined in the assignment brief.

2. Features
Interactive Chat Interface: A user-friendly web interface built with Streamlit that provides a seamless, conversational experience for the candidate.

Structured Interview Flow: The agent guides the candidate through a series of questions, from a warm introduction to a conclusive summary, mimicking a real interview structure.

Hybrid Evaluation Engine: A smart, two-step process to evaluate answers, combining the best of deterministic and AI-based approaches:

A fast, reliable check for exact formula matches to ensure speed and accuracy for standard answers.

A fallback to Google's Gemini LLM for semantic evaluation of functionally equivalent but syntactically different formulas (e.g., XLOOKUP vs. VLOOKUP).

Automated Feedback Report: At the end of the interview, the agent generates a detailed, constructive summary of the candidate's performance, including an overall score and a topic-by-topic breakdown.

3. Tech Stack & Justification
Backend: Django & Django REST Framework

Justification: Chosen for its robust, "batteries-included" structure which encourages rapid, secure, and scalable development. Its organized nature is ideal for building a system that can be expanded upon post-PoC.

Frontend: Streamlit

Justification: Selected for its ability to rapidly create and deploy data-centric web applications directly from Python, making it perfect for building an interactive PoC frontend with minimal overhead.

AI/LLM: Google's Gemini 1.5 Flash

Justification: Used for its strong reasoning capabilities and speed. It is leveraged in two key ways:

Offline: To bootstrap the system by generating the initial high-quality question bank, solving the "cold start" problem.

Online: As part of the hybrid evaluation engine to provide intelligent semantic analysis of user answers.

Language: Python

Justification: The universal language for AI/ML development with an unparalleled ecosystem of libraries and frameworks.

4. How to Run Locally
Prerequisites:

Python 3.9+

A Google AI API Key (from Google AI Studio)

Setup:

Clone the repository:

git clone https://github.com/Sumit-Das06/ai-excel-interviewer
cd excel_interviewer_project

Install dependencies:

pip install django djangorestframework google-generativeai

Add your API Key:

Open the file interviewer/logic.py.

Find the line API_KEY = "YOUR_SECRET_GOOGLE_AI_API_KEY" and replace the placeholder with your actual Google AI API key.

Execution:

You will need two separate terminals to run the application.

Run the Backend Server:

In your first terminal, navigate to the project root and run:

python manage.py runserver

The backend will be running at http://127.0.0.1:8000.

Run the Frontend Application:

(Note: The frontend.py file is provided in the parent directory for this PoC).

In a second terminal, navigate to the folder containing frontend.py and run:

pip install streamlit requests
streamlit run frontend.py

The application will open automatically in your web browser.