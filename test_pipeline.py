# test_pipeline.py
import time
from database import DatabaseManager
from ai_engine import AIEngine

def run_integration_test():
    print("🚀 Starting IntervAI Engine Integration Test...\n")
    
    # 1. Test Database Manager Initialization
    try:
        print("[ ] Checking Database Connection...")
        db = DatabaseManager()
        print("    👉 Success: Database connection established.\n")
    except Exception as e:
        print(f"❌ DATABASE ERROR: Could not initialize DatabaseManager.\nDetail: {e}\n")
        return

    # 2. Test AI Engine Prompt Generation
    try:
        print("[ ] Requesting interview question from AI Engine...")
        ai = AIEngine()
        start_time = time.time()
        question = ai.generate_question("Behavioral")
        duration = time.time() - start_time
        
        print(f"    👉 Success ({duration:.2f}s): Generated Question:")
        print(f"       \"{question}\"\n")
    except Exception as e:
        print(f"❌ AI GENERATION ERROR: Failed to fetch question from LLM.\nDetail: {e}\n")
        return

    # 3. Test Response Analysis & Parsing Flow
    try:
        print("[ ] Submitting mock answer for evaluation...")
        mock_answer = (
            "In my last project, we had a schema design conflict. I set up a meeting, "
            "presented data benchmarks comparing normalized vs denormalized performance, "
            "and we compromised on a hybrid model that speed up queries by 30%."
        )
        
        start_time = time.time()
        analysis = ai.analyze_response(question, mock_answer)
        duration = time.time() - start_time
        
        print(f"    👉 Success ({duration:.2f}s): Received Performance Metrics:")
        print(f"       - Overall Score: {analysis.get('overall_score')}/10")
        print(f"       - STAR Score:    {analysis.get('star_score')}/10")
        print(f"       - Technical:     {analysis.get('technical_score')}/10")
        print(f"       - Strengths Picked Up: {len(analysis.get('strengths', []))}")
        print(f"       - Improvements Picked Up: {len(analysis.get('improvements', []))}\n")
        
        # Verify critical dictionary keys expected by render_analytics_ui
        required_keys = ["overall_score", "summary", "star_score", "pacing_score", "technical_score", "conciseness_score", "strengths", "improvements"]
        missing_keys = [key for key in required_keys if key not in analysis]
        
        if missing_keys:
            print(f"⚠️  WARNING: Dictionary is missing expected keys: {missing_keys}")
            print("This will cause an error inside render_analytics_ui!")
        else:
            print("🎉 PIPELINE CLEAR: Data structure perfectly matches UI expectations.")
            
    except Exception as e:
        print(f"❌ AI ANALYSIS ERROR: Assessment workflow failed.\nDetail: {e}\n")

if __name__ == "__main__":
    run_integration_test()