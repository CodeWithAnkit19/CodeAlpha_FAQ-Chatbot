
from flask import Flask, request, jsonify
from flask_cors import CORS
from rapidfuzz import fuzz, process
import re

app = Flask(__name__)
CORS(app)

faq_data = [
    {
        "question": "What courses does the college offer?",
        "aliases": ["available courses", "degree programs", "what can I study"],
        "answer": "The college offers different academic programs. Please check the official university website for the latest course list."
    },
    {
        "question": "How can I apply for admission?",
        "aliases": ["admission process", "how do I join the college", "apply for a seat"],
        "answer": "Visit the official university website, check the admission requirements, complete the application form, and follow the admission instructions."
    },
    {
        "question": "Which documents are required for admission?",
        "aliases": ["admission documents", "papers needed to join", "what certificates do I need"],
        "answer": "Commonly required documents include academic marksheets, identity proof, photographs, and applicable certificates. Confirm the exact list with the university."
    },
    {
        "question": "How do I pay my college fees?",
        "aliases": ["fee payment process", "deposit tuition fees", "pay semester fees online"],
        "answer": "Check the official university fee portal or contact the accounts department for payment methods and deadlines."
    },
    {
        "question": "What is the fee structure?",
        "aliases": ["course fees", "tuition cost", "how much does college cost"],
        "answer": "Fees depend on the course and academic session. Consult the official fee structure or university accounts department."
    },
    {
        "question": "Does the college provide scholarships?",
        "aliases": ["financial aid", "scholarship opportunities", "help paying fees"],
        "answer": "Scholarships may depend on eligibility, academic performance, and applicable schemes. Contact the scholarship or accounts department for current details."
    },
    {
        "question": "What are the attendance requirements?",
        "aliases": ["minimum attendance", "how many classes must I attend", "attendance shortage"],
        "answer": "Attendance requirements depend on university regulations and course rules. Check the current academic guidelines or contact your department."
    },
    {
        "question": "When will the examinations take place?",
        "aliases": ["exam schedule", "exam dates", "when are my exams"],
        "answer": "Check the official examination notice, academic calendar, or student portal for the latest examination schedule."
    },
    {
        "question": "Where can I check my examination results?",
        "aliases": ["view marks", "semester result", "check my grades", "result declaration"],
        "answer": "Check the official student portal or examination website using your university credentials."
    },
    {
        "question": "Where can I find the academic calendar?",
        "aliases": ["semester calendar", "holiday list", "important academic dates"],
        "answer": "The academic calendar is generally published through official university notices or the student portal."
    },
    {
        "question": "Does the college have a library?",
        "aliases": ["library facilities", "books and study material", "where can I borrow books"],
        "answer": "Check the university library information for available books, digital resources, membership rules, and opening hours."
    },
    {
        "question": "How can I get a student identity card?",
        "aliases": ["college ID card", "lost my student card", "apply for ID"],
        "answer": "Contact the relevant university office or student support desk for ID card application or replacement procedures."
    },
    {
        "question": "How can I contact the college?",
        "aliases": ["university contact details", "phone number", "college email address"],
        "answer": "Use the official university website to find verified contact numbers, email addresses, and department details."
    },
    {
        "question": "Where can I find college notices?",
        "aliases": ["latest announcements", "university updates", "important notifications"],
        "answer": "Check the official university website, notice boards, student portal, and authorized communication channels."
    },
    {
        "question": "What sports facilities are available?",
        "aliases": ["sports activities", "playground", "games at college"],
        "answer": "Contact the university sports department or student activities office for available facilities and participation details."
    },
    {
        "question": "How can I reset my student portal password?",
        "aliases": ["forgot password", "cannot log in", "recover portal account"],
        "answer": "Use the password recovery option on the official student portal. If that does not work, contact university IT support."
    },
    {
        "question": "Does the college provide placement assistance?",
        "aliases": ["job opportunities", "campus recruitment", "help finding a job", "placement cell"],
        "answer": "Contact the placement cell for information about campus recruitment, eligibility, training, internships, and participating employers."
    },
    {
        "question": "How can I get my academic certificate?",
        "aliases": ["degree certificate", "request marksheet", "obtain official documents"],
        "answer": "Contact the examination or academic office to learn the application process, required documents, and processing time."
    },
    {
        "question": "What should I do if I miss an examination?",
        "aliases": ["missed my exam", "absent from exam", "exam reappear process"],
        "answer": "Contact the examination department promptly and ask about applicable rules and any permitted re-examination process."
    },
    {
        "question": "How can I update my personal information?",
        "aliases": ["correct my name", "change contact details", "update student records"],
        "answer": "Contact the appropriate academic office and follow the official procedure for updating student records."
    },
    {
        "question": "How do I register for examinations?",
        "aliases": ["exam form submission", "examination registration", "fill exam form"],
        "answer": "Follow the official examination registration instructions and submit the required form and fees before the deadline."
    },
    {
        "question": "What extracurricular activities are available?",
        "aliases": ["clubs and societies", "college events", "student activities"],
        "answer": "Check university announcements or contact the student activities office for clubs, events, and societies."
    },
    {
        "question": "How do I access the student portal?",
        "aliases": ["student login", "university portal access", "sign in to my account"],
        "answer": "Open the official university student portal and sign in with your assigned credentials. Contact IT support if you have access problems."
    },
    {
        "question": "What are the college timings?",
        "aliases": ["class timings", "opening hours", "when does college open"],
        "answer": "College and department timings can vary. Check the official timetable or contact your department for confirmed timings."
    },
    {
        "question": "How can I get an internship?",
        "aliases": ["internship opportunities", "industry training", "find student internships"],
        "answer": "Check the placement cell's announcements, university career resources, and relevant internship postings."
    },
    {
        "question": "How do I get a bonafide certificate?",
        "aliases": ["student verification certificate", "proof of enrollment", "request bonafide"],
        "answer": "Contact the academic or administration office and ask about the bonafide certificate application procedure."
    },
    {
        "question": "Can I change my course or subject?",
        "aliases": ["course change", "subject change request", "switch academic program"],
        "answer": "Course or subject changes depend on university rules and available seats. Contact the academic office to confirm eligibility and deadlines."
    },
    {
        "question": "How can I report a technical problem?",
        "aliases": ["portal not working", "website error", "technical support"],
        "answer": "Contact the university IT help desk and provide a clear description of the issue and any relevant error message."
    },
    {
        "question": "How can I submit a complaint or grievance?",
        "aliases": ["student complaint", "report a problem", "grievance redressal"],
        "answer": "Use the official student grievance process or contact the designated university office for guidance."
    },
    {
        "question": "How can I get information about hostel facilities?",
        "aliases": ["college accommodation", "hostel fees", "room availability"],
        "answer": "Contact the university hostel or accommodation office for availability, fees, eligibility, and application details."
    }
]

# Build a searchable list of FAQ questions and alternative phrases.
search_items = []

for index, item in enumerate(faq_data):
    search_items.append({
        "text": item["question"],
        "faq_index": index
    })

    for alias in item["aliases"]:
        search_items.append({
            "text": alias,
            "faq_index": index
        })


def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def find_best_answer(user_question):
    question = normalize_text(user_question)

    if not question:
        return "Please enter a question so I can help you."

    # Handle greetings and thanks separately.
    if question in ["hi", "hello", "hey", "good morning", "good afternoon"]:
        return "Hello! Welcome to the College FAQ Chatbot. How can I help you?"

    if question in ["thanks", "thank you", "thank you so much"]:
        return "You're welcome! Feel free to ask another college-related question."

    choices = {
        item["text"]: item["faq_index"]
        for item in search_items
    }

    match = process.extractOne(
        question,
        list(choices.keys()),
        scorer=fuzz.WRatio
    )

    if match is None:
        return fallback_answer()

    matched_text, score, _ = match

    # Also compare important words for partially similar questions.
    if score < 48:
        partial_match = process.extractOne(
            question,
            list(choices.keys()),
            scorer=fuzz.token_set_ratio
        )

        if partial_match and partial_match[1] > score:
            matched_text, score, _ = partial_match

    if score < 55:
        return fallback_answer()

    faq_index = choices[matched_text]
    return faq_data[faq_index]["answer"]


def fallback_answer():
    return (
        "Sorry, I couldn't confidently match that question. "
        "Try asking about admissions, fees, scholarships, attendance, "
        "exams, results, library, placements, hostel, or student services."
    )


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "College FAQ Chatbot API is running."
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")

    if not isinstance(question, str):
        return jsonify({
            "answer": "Please enter your question as text."
        }), 400

    return jsonify({
        "question": question,
        "answer": find_best_answer(question)
    })


if __name__ == "__main__":
    print("College FAQ Chatbot backend is running...")
    print("API available at: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
