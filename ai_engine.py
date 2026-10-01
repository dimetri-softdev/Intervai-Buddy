import json
import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


class AIEngine:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("[Warning]: GROQ_API_KEY environment variable is not set.")

        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-120b"
        self.coding_model = "qwen/qwen3.8-27b"

    def transcribe_audio(self, audio_file_path):
        """Transcribes audio using Groq's Whisper model."""
        try:
            if not os.path.exists(audio_file_path):
                return ""

            with open(audio_file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(os.path.basename(audio_file_path), file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    language="en",
                )
            return transcription.text.strip()
        except Exception as e:
            print(f"[Whisper Transcription Error]: {e}")
            return ""

    def generate_question(self, topic="Behavioral", language=None):
        if topic == "Coding":
            language = language or "Python"
            prompt = (
                f"Create one concise {language} coding interview challenge."
                " State the task, function signature, and one small example."
                " Keep it under 100 words. Do not include a solution."
            )
        else:
            prompt = (
                f"You are an expert {topic} interviewer. Generate ONE clear,"
                f" challenging question appropriate for a {topic} interview."
                " Return only the question text without an introduction or outro."
            )
        try:
            response = self.client.chat.completions.create(
                model=self.coding_model if topic == "Coding" else self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2 if topic == "Coding" else 0.7,
                max_tokens=180 if topic == "Coding" else 150,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq API Error: {e}")
            fallback_questions = {
                "Behavioral": "Tell me about a time you handled a difficult challenge at work.",
                "Technical": "How would you diagnose and resolve a performance issue in a production service?",
                "Coding": "How would you remove duplicate values from a list while preserving their order?",
                "System Design": "How would you design a highly available URL-shortening service?",
            }
            return fallback_questions.get(
                topic, fallback_questions["Behavioral"]
            )

    def analyze_response(
        self, question, user_answer, interview_type="Behavioral", language=None
    ):
        """Analyze a candidate's answer using expectations for the chosen interview type.

        Return a score out of 10, its rationale, and improvement tips.
        """
        if interview_type == "Coding":
            language = language or "Python"
            prompt = f"""
            You are a rigorous coding interviewer reviewing a candidate's {language} solution.

            Coding prompt: "{question}"
            Candidate's {language} code:
            ```{language.lower()}
            {user_answer}
            ```

            Assess whether the code solves the stated problem. Reason through normal and edge cases,
            identify syntax or logic issues, and do not claim the code was executed. Return ONLY a
            valid JSON object with these keys:
            {{
                "is_correct": <true, false, or null if correctness cannot be determined>,
                "correctness_feedback": "<concise explanation of correctness or the specific defect>",
                "time_complexity": "<Big-O time complexity or unknown>",
                "space_complexity": "<Big-O space complexity or unknown>",
                "overall_score": <float between 1.0 and 10.0>,
                "score_reason": "<1-2 sentences explaining the score>",
                "improvement_tips": "<2-3 actionable code-specific improvements>"
            }}
            Do not include markdown formatting or text outside the JSON object.
            """
        else:
            prompt = f"""
            You are an expert {interview_type} interview coach evaluating a candidate's response.

            Question Asked: "{question}"
            Candidate's Response: "{user_answer}"

            Evaluate the response against expectations for a {interview_type} interview. Return ONLY a valid JSON object with the following keys:
            {{
                "overall_score": <float between 1.0 and 10.0>,
                "score_reason": "<1-2 sentences explaining why they earned this specific score>",
                "improvement_tips": "<2-3 actionable tips relevant to this interview type>"
            }}
            Do not include markdown formatting or extra text outside the raw JSON object.
            """

        try:
            response = self.client.chat.completions.create(
                model=(
                    self.coding_model
                    if interview_type == "Coding"
                    else self.model
                ),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content.strip()
            analysis_data = json.loads(content)
            return analysis_data

        except Exception as e:
            print(f"[AIEngine Error] Analysis failed: {e}")
            fallback = {
                "overall_score": 6.5,
                "score_reason": (
                    "Your answer covered the basics but lacked specific details"
                    " or measurable outcomes."
                ),
                "improvement_tips": (
                    "Use the STAR method (Situation, Task, Action, Result) to"
                    " structure your response with concrete metrics."
                ),
            }
            if interview_type == "Coding":
                fallback.update(
                    {
                        "is_correct": None,
                        "correctness_feedback": "Correctness could not be checked because the AI service is unavailable.",
                        "time_complexity": "Unknown",
                        "space_complexity": "Unknown",
                    }
                )
            return fallback


if __name__ == "__main__":
    engine = AIEngine()
    print("AIEngine initialized successfully!")