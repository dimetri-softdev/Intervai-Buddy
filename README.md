# IntervAI – AI Interview Practice Coach

**IntervAI** is a desktop-based interview-practice application designed to help job seekers prepare for interviews through guided, AI-powered mock interview sessions.

The application uses a **Tkinter-based graphical user interface**, **Google Gemini AI** to generate and analyse interview responses, and a **local SQLite database** to store user accounts, statistics, and interview history.

---

## 📌 Project Overview

IntervAI provides users with an interactive environment where they can practise answering interview questions and receive AI-assisted analysis of their responses.

The application is designed for individual job seekers who want a simple desktop tool for improving their interview preparation.

The system provides:

* User registration and authentication
* AI-generated interview questions
* Mock interview sessions
* AI-powered response analysis
* Interview statistics
* Interview history
* Local data persistence using SQLite
* Local fallback questions when the AI service is unavailable

---

## 🛠️ Technology Stack

| Technology        | Purpose                          |
| ----------------- | -------------------------------- |
| **Python**        | Main programming language        |
| **CustomTkinter** | Desktop graphical user interface |
| **Tkinter**       | Underlying GUI framework         |
| **Google GenAI**  | Gemini AI integration            |
| **SQLite3**       | Local database and persistence   |
| **Threading**     | Background AI requests           |
| **Figma**         | UI/design planning               |

---

## 📂 Project Structure

```text
IntervAI/
│
├── .gitignore
│
├── UI_Pics/
│   ├── Screenshots
│   └── Design documentation
│
├── ai_engine.py
│   └── AIEngine
│       ├── Question generation
│       └── Response analysis
│
├── app.py
│   └── IntervAIApp
│       ├── Authentication
│       ├── Dashboard
│       ├── Interview sessions
│       └── Analytics
│
├── database.py
│   └── DatabaseManager
│       ├── User authentication
│       ├── User statistics
│       └── Interview history
│
└── test_pipeline.py
    └── Integration testing
```

---

# 🏗️ Application Architecture

IntervAI is divided into three main components:

```text
                    ┌───────────────────┐
                    │     app.py        │
                    │   GUI / Frontend  │
                    └─────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐      ┌─────────────────┐
        │  ai_engine.py   │      │  database.py    │
        │   Gemini AI     │      │     SQLite      │
        └────────┬────────┘      └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Google Gemini   │
        │      API        │
        └─────────────────┘
```

---

## 🖥️ `app.py`

`app.py` is the main entry point for the application.

It creates the required application components and displays the authentication interface.

The application flow is approximately:

```text
Start Application
       │
       ▼
   AuthView
       │
       ▼
 Login / Register
       │
       ▼
   Dashboard
       │
       ├───────────────┐
       │               │
       ▼               ▼
Interview Session    Analytics
       │
       ▼
Generate Question
       │
       ▼
User Provides Answer
       │
       ▼
AI Analysis
       │
       ▼
Save Interview Data
```

The interview session requests questions through `AIEngine.generate_question()`.

AI requests are performed in a background thread to prevent the graphical interface from becoming unresponsive.

A local backup question list is also available if the AI request fails or exceeds the configured timeout.

---

# 🤖 `ai_engine.py`

The `ai_engine.py` module provides the application's AI functionality.

It is responsible for communicating with the **Google Gemini API** through the `google-genai` package.

The AI engine is intended to provide two primary capabilities:

### Question Generation

Generates interview questions based on the application's interview requirements.

```text
AIEngine
    │
    ▼
Gemini API
    │
    ▼
Interview Question
```

### Response Analysis

The user's interview response can be sent to the AI model for structured analysis.

The intended analysis can be used to provide feedback about the quality of the user's answer and identify areas for improvement.

---

# 🗄️ `database.py`

`database.py` contains the `DatabaseManager` class.

The application uses Python's built-in `sqlite3` library for local data persistence.

The database manager is responsible for:

* Creating database tables
* Registering users
* Authenticating users
* Managing user statistics
* Recording interview history
* Retrieving stored interview information

The database tables include:

```text
users
   │
   ├── User authentication information
   │
   ▼
user_stats
   │
   ├── Interview statistics
   │
   ▼
interview_history
   │
   └── Previous interview sessions
```

Database tables are automatically initialized through:

```python
DatabaseManager.setup_tables()
```

This allows the application to create the required database structure when it is first executed.

---

# 🧪 `test_pipeline.py`

`test_pipeline.py` is a small integration test script.

It tests the interaction between the database and AI components.

The intended pipeline is:

```text
Database Initialization
        │
        ▼
Generate Interview Question
        │
        ▼
Submit Response
        │
        ▼
AI Response Analysis
        │
        ▼
Store / Process Results
```

Run the test with:

```bash
python test_pipeline.py
```

---

# 🚀 Getting Started

## Prerequisites

Before running IntervAI, make sure you have:

* **Python 3.x**
* Internet connection for Gemini AI functionality
* A Google Gemini API key *(required for AI functionality)*

Check your Python installation:

```bash
python --version
```

---

# 📥 Clone the Repository

Clone the project:

```bash
git clone <YOUR-REPOSITORY-URL>
```

Navigate into the project:

```bash
cd <PROJECT-DIRECTORY>
```

---

# 🐍 Create a Virtual Environment

It is recommended to use a virtual environment.

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

# 📦 Install Dependencies

The repository currently does not include a `requirements.txt` file, so dependencies need to be installed manually.

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the required external packages:

```bash
python -m pip install customtkinter google-genai
```

> **Note:** `sqlite3` is included with Python and does not need to be installed separately.

---

# 🔑 Gemini API Configuration

IntervAI uses the Google Gemini API for AI-powered question generation and response analysis.

The application expects the following environment variable:

```text
GEMINI_API_KEY
```

## Windows Command Prompt

```cmd
set GEMINI_API_KEY=your_api_key_here
```

## Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

## macOS / Linux

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Replace:

```text
your_api_key_here
```

with your actual Gemini API key.

### ⚠️ Security

**Never commit your API key to GitHub.**

Do not place the API key directly inside:

```text
app.py
ai_engine.py
```

Use an environment variable or another secure secrets-management method instead.

---

# ▶️ Running the Application

Once the virtual environment is activated and dependencies are installed, run:

```bash
python app.py
```

The IntervAI desktop application should open.

---

# 🎯 Basic Usage

### 1. Register or Log In

Launch the application and use the authentication interface to create an account or log into an existing account.

### 2. Open the Dashboard

After authentication, the application displays the main dashboard.

### 3. Start an Interview Session

Start a mock interview session.

The application requests an interview question from the AI engine.

### 4. Answer the Question

Enter your response through the application's interface.

### 5. Analyse Your Response

The response can be sent to Gemini for AI-powered analysis.

### 6. Review Your Progress

Interview statistics and previous sessions can be accessed through the application's dashboard and analytics functionality.

---

# 🔄 AI Fallback System

IntervAI includes a local fallback mechanism for interview questions.

If the Gemini API request:

* Fails
* Times out
* Cannot be reached
* Encounters another runtime problem

the application can use a predefined list of local interview questions.

```text
                Generate Question
                       │
                       ▼
                  Gemini API
                       │
             ┌─────────┴─────────┐
             │                   │
           Success             Failure
             │                   │
             ▼                   ▼
       AI Question        Local Question
```

This allows the application to remain usable even when the AI service is temporarily unavailable.

---

# ⚠️ Current Development Issues

The current version of `ai_engine.py` contains **method scoping/indentation issues** that should be corrected before treating the application as production-ready.

Some functions, including:

```text
generate_question()
analyze_response()
```

are currently outside the intended `AIEngine` class scope or have incorrect indentation.

There is also an issue where `generate_question()` references:

```python
self.BACKUP_QUESTIONS
```

while `BACKUP_QUESTIONS` is defined at module level.

This can result in runtime errors.

### Recommended Fix

The AI-related methods should be correctly placed inside the `AIEngine` class, and the backup questions should either:

* Become a class variable, or
* Be referenced as a module-level variable.

For example:

```python
class AIEngine:

    BACKUP_QUESTIONS = [
        # backup questions
    ]

    def generate_question(self):
        # implementation
        pass

    def analyze_response(self, response):
        # implementation
        pass
```

The exact implementation should follow the existing project requirements.

---

# 🧪 Testing Status

The project currently includes:

```text
test_pipeline.py
```

which can be used to test the integration between:

* SQLite database
* AI question generation
* AI response analysis

Run:

```bash
python test_pipeline.py
```

Because of the current `ai_engine.py` scoping issues, some tests may fail until those issues are corrected.

---

# 📸 UI & Design

The `UI_Pics` directory contains screenshots and design documentation related to the application's interface.

```text
UI_Pics/
├── Application screenshots
└── Design documentation
```

These resources can be used to understand the intended visual design and user experience.

---

# 📋 Current Features

* ✅ Desktop graphical interface
* ✅ User registration
* ✅ User authentication
* ✅ Local SQLite database
* ✅ Interview dashboard
* ✅ Mock interview sessions
* ✅ AI-generated interview questions
* ✅ Local question fallback
* ✅ AI response analysis
* ✅ Interview history
* ✅ User statistics
* ✅ Analytics interface
* ✅ Background AI requests
* ✅ Integration testing

---

# 🔮 Future Improvements

Potential improvements include:

* [ ] Fix `AIEngine` class scoping and indentation
* [ ] Add `requirements.txt`
* [ ] Improve AI response analysis
* [ ] Add more interview categories
* [ ] Add difficulty levels
* [ ] Add technical interview questions
* [ ] Add behavioural interview questions
* [ ] Improve interview scoring
* [ ] Add detailed performance reports
* [ ] Add progress charts
* [ ] Improve error handling
* [ ] Add automated unit tests
* [ ] Improve database security
* [ ] Package the application as a Windows executable
* [ ] Improve UI/UX
* [ ] Add configurable interview settings

---

# 📦 Recommended `requirements.txt`

A future version of the project should include a `requirements.txt` file.

Example:

```text
customtkinter
google-genai
```

Dependencies can then be installed using:

```bash
pip install -r requirements.txt
```

---

# 🔒 Security Considerations

Because the application stores authentication and interview information locally, security should be considered when extending the project.

Important considerations include:

* Never commit API keys
* Store secrets using environment variables
* Avoid storing plaintext passwords
* Validate user input
* Handle API failures safely
* Protect sensitive user information
* Use secure password hashing
* Add appropriate error handling

---

# 📄 License

This project is intended for educational and development purposes unless otherwise specified by the project owner.

---

## 👨‍💻 Project

**IntervAI – AI Interview Practice Coach**

Built with:

**Python • CustomTkinter • Google Gemini AI • SQLite**

