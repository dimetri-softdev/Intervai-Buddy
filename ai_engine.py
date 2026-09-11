import json
import os
from groq import Groq


class AIEngine:

    def __init__(self):
        # Fetch key from environment variables to keep repository secure
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("[Warning]: GROQ_API_KEY environment variable is not set.")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

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

    def generate_question(self, topic="Behavioral"):
        prompt = (
            f"You are an expert technical and behavioral interviewer. Generate"
            f" ONE clear, challenging {topic} interview question. Return ONLY"
            " the question text itself without intro or outro."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq API Error: {e}")
            return (
                "Tell me about a time you had to deal with a difficult"
                " challenge at work."
            )

    def analyze_response(self, question, user_answer):
        """Analyzes candidate's answer using Groq Llama 3.3, provides a score out of 10,

        explains the score, and gives tips for improvement.
        """
        prompt = f"""
        You are an expert technical and behavioral interview coach evaluating a candidate's response.

        Question Asked: "{question}"
        Candidate's Response: "{user_answer}"

        Evaluate the response carefully. Return ONLY a valid JSON object with the following keys:
        {{
            "overall_score": <float between 1.0 and 10.0>,
            "score_reason": "<1-2 sentences explaining why they earned this specific score>",
            "improvement_tips": "<2-3 actionable tips on how to improve this answer or hit the STAR method better>"
        }}
        Do not include markdown formatting or extra text outside the raw JSON object.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content.strip()
            analysis_data = json.loads(content)
            return analysis_data

        except Exception as e:
            print(f"[AIEngine Error] Analysis failed: {e}")
            return {
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


if __name__ == "__main__":
    engine = AIEngine()
    print("AIEngine initialized successfully!")