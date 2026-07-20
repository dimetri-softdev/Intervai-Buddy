import os
import json
import random
from google import genai
from google.genai import types

class AIEngine:
    def __init__(self):
        # Automatically pulls GEMINI_API_KEY from your system environment variables
        self.client = genai.Client()
    import random

# Add a few high-quality local fallbacks at the top of the file or class
BACKUP_QUESTIONS = [
    "Tell me about a time you had to deal with a conflict in a team project. How did you approach the situation, and what was the final outcome?",
    "Describe a challenging technical problem you faced recently. How did you diagnose it, and what solution did you implement?",
    "Tell me about a time you had to adapt to a sudden change in a project's requirements or priorities. How did you handle the transition?",
    "Describe a situation where you had to work with a difficult stakeholder or team member. How did you ensure the project's success?"
]

def generate_question(self, topic="Behavioral"):
    """Generates a realistic interview question based on the topic, with local safety fallbacks."""
    prompt = f"Generate one challenging {topic} interview question for a Software Engineer."
    
    try:
        # Wrap the network call itself in a try block to catch 503 / network dropouts
        response = self.client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert tech interviewer. Return only the question text.",
                max_output_tokens=250,
                timeout=5.0 # <--- FORCE IT TO GIVE UP AFTER 5 SECONDS
            )
        )
        
        if response.text:
            return response.text.strip()
        return response.candidates[0].content.parts[0].text.strip()

    except Exception as e:
        # Log the error quietly to the console for debugging
        print(f"⚠️ API Unavailable ({e}), serving local fallback question.")
        # Return a random great question from our local stash so the user session never breaks
        return random.choice(self.BACKUP_QUESTIONS)
    
    def analyze_response(self, question, user_answer):
        """Evaluates the user's answer and returns structured JSON for the dashboard."""
        
        system_instruction = (
            "You are a strict technical interview coach. Analyze the user's response to the given question. "
            "You MUST respond with a raw JSON object matching this exact structure keys: "
            "{\n"
            '  "overall_score": 8,\n'
            '  "star_score": 9,\n'
            '  "pacing_score": 6,\n'
            '  "technical_score": 8,\n'
            '  "conciseness_score": 7,\n'
            '  "headline": "Short punchy summary sentence",\n'
            '  "summary": "Paragraph detail regarding overall performance",\n'
            '  "strengths": ["bullet 1", "bullet 2", "bullet 3"],\n'
            '  "improvements": ["bullet 1", "bullet 2", "bullet 3"],\n'
            '  "senior_rewrite": "A model senior-level response version of what the user attempted to say"\n'
            "}\n"
        )

        user_prompt = f"Question: {question}\nUser Answer: {user_answer}"

        response = self.client.models.generate_content(
            model='gemini-3.5-flash', # Updated to the active model string
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json" 
            )
        )
        
        return json.loads(response.text)

# Local diagnostic script
if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not found. Please set it and restart VS Code.")
    else:
        ai = AIEngine()
        print("Testing Free Gemini Question Generation...")
        q = ai.generate_question()
        print(f"Generated Question: {q}\n")