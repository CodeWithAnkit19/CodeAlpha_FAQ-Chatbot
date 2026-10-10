# College FAQ Chatbot

## Project Overview
The College FAQ Chatbot is a web-based application that helps students find answers to common college-related questions. It provides a simple chat interface where users can ask questions about admissions, fees, scholarships, examinations, results, library facilities, placements, and other student services.

## Features
- Interactive chatbot interface
- College-related frequently asked questions
- Text matching using RapidFuzz
- Alternative phrases for better question matching
- Flask-based backend API
- Responsive frontend using HTML, CSS, and JavaScript
- Error handling for unsupported questions

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Text Matching:** RapidFuzz
- **API Support:** Flask-CORS

## Project Structure
```text
FAQ-Chatbot/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Install Python Dependencies
Open the terminal in the project folder and run:

```bash
py -m pip install -r backend/requirements.txt
```

### 2. Start the Backend
Run:

```bash
py backend/app.py
```

The backend will be available at:

`http://127.0.0.1:5000`

### 3. Open the Frontend
Open `frontend/index.html` in your browser.

## Example Questions
- How can I apply for admission?
- How do I pay my college fees?
- Where can I check my examination results?
- Does the college provide placement assistance?
- How can I reset my student portal password?

## How It Works
The chatbot compares the user's question with stored FAQ questions and alternative phrases using RapidFuzz text-matching techniques. It returns the answer associated with the closest suitable match. If the match is not sufficiently strong, it provides a fallback response.

## Future Improvements
- Add more college FAQs
- Improve support for Hindi and Hinglish
- Integrate semantic language understanding
- Connect to an official college information source

## Internship Project
Developed as part of the CodeAlpha internship project tasks.