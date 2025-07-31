# interviewer/logic.py
import json
import google.generativeai as genai

# --- LLM CONFIGURATION ---
try:
    API_KEY = "YOUR_SECRET_GOOGLE_AI_API_KEY" 
    
    if "YOUR_SECRET" in API_KEY:
        raise ValueError("API Key not set. Please replace 'YOUR_SECRET_GOOGLE_AI_API_KEY'.")

    genai.configure(api_key=API_KEY)
    llm = genai.GenerativeModel('gemini-1.5-flash')
    print("Successfully configured Gemini LLM.")
    LLM_ENABLED = True
except Exception as e:
    print(f"Could not configure Gemini LLM: {e}. Running in non-LLM mode.")
    LLM_ENABLED = False


class InterviewManager:
    
    # Manages the state and flow of a single interview session.
    def __init__(self, questions_path: str):
        print("Initializing InterviewManager...")
        try:
            with open(questions_path, 'r') as f:
                self.questions = json.load(f)
            print(f"Successfully loaded {len(self.questions)} questions.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading questions: {e}")
            self.questions = []
        
        self.current_question_index = -1
        self.interview_started = False
        self.results = []

    def _normalize_formula(self, formula: str) -> str:
        # Function to clean up a formula for comparison.
        return formula.strip().upper().replace(" ", "")

    def _evaluate_answer(self, user_answer: str):
        
        question_data = self.questions[self.current_question_index]
        correct_formula = question_data['correct_formula']
        
        normalized_user_answer = self._normalize_formula(user_answer)
        normalized_correct_formula = self._normalize_formula(correct_formula)

        is_correct = (normalized_user_answer == normalized_correct_formula)
        evaluation_method = "Direct Match"

        is_formula_question = "=" in correct_formula
        if not is_correct and LLM_ENABLED and is_formula_question:
            print("Direct match failed. Attempting LLM semantic evaluation...")
            try:
                prompt = f"""
                You are a strict Excel interview evaluator. Your task is to determine if a user's submitted formula correctly solves a given problem.

                **The Problem:**
                {question_data['problem_description']}

                **The Expected Correct Formula:**
                `{correct_formula}`

                **The User's Submitted Formula:**
                `{user_answer}`

                **Your Task:**
                Carefully analyze the user's formula. Does it correctly solve the specific problem described? The user's formula is only correct if it achieves the same result as the expected formula for the given problem. A formula that is syntactically valid but does not solve the problem is incorrect.

                Respond with only a single word: "Correct" or "Incorrect".
                """
                response = llm.generate_content(prompt)
                print(f'response---{response}')
                
                if response.text.strip().lower().startswith("correct"):
                    is_correct = True
                    evaluation_method = "LLM Semantic Match"
                    print("LLM evaluated the answer as Correct.")
                else:
                    print(f"LLM evaluated the answer as Incorrect. response: {response.text}")

            except Exception as e:
                print(f"LLM evaluation failed with error: {e}")
        
        self.results.append({
            "question_id": question_data['id'],
            "topic": question_data['topic'],
            "user_answer": user_answer,
            "is_correct": is_correct,
            "evaluation_method": evaluation_method
        })
        
        return is_correct

    def start_interview(self):
        self.interview_started = True
        self.current_question_index = 0
        self.results = []
        intro_text = (
            "Hello! I'm your AI-powered Excel mock interviewer from Coding Ninjas. "
            "I'm going to ask you a series of questions. For most, I'll expect you to write the correct formula. "
            "Let's start."
        )
        return self.get_next_question(intro_text)

    def get_next_question(self, prefix_text: str = ""):
        if not self.questions:
             return {"response_text": "Error: No questions loaded.", "is_interview_over": True}
        if self.current_question_index >= len(self.questions):
            return self.end_interview()
        question = self.questions[self.current_question_index]
        question_text = (
            f"{prefix_text}\n\n--- Question {self.current_question_index + 1}/{len(self.questions)} ---\n\n"
            f"**Topic:** {question['topic']}\n\n"
            f"**Problem:** {question['problem_description']}\n\n"
            f"**Data Context:** {question['example_data']}"
        )
        return {
            "response_text": question_text,
            "question_id": question['id'],
            "is_interview_over": False
        }
    
    def process_answer(self, user_answer: str):
        is_correct = self._evaluate_answer(user_answer)
        if is_correct:
            acknowledgement = "That's correct! Well done. Here is your next question."
        else:
            correct_answer = self.questions[self.current_question_index]['correct_formula']
            acknowledgement = f"That's not quite right. The correct answer is `{correct_answer}`. Let's try the next one."
        self.current_question_index += 1
        return self.get_next_question(acknowledgement)

    def end_interview(self):
        if not self.results:
            return {"response_text": "The interview ended before any questions were answered.", "is_interview_over": True}
        correct_answers = sum(1 for result in self.results if result['is_correct'])
        total_questions = len(self.results)
        score_percentage = (correct_answers / total_questions) * 100
        report = f"### Your Interview Performance Summary\n\n"
        report += f"**Overall Score:** {correct_answers}/{total_questions} ({score_percentage:.1f}%)\n\n---\n\n"
        report += "#### Performance by Topic:\n\n"
        for result in self.results:
            status = "✅ Correct" if result['is_correct'] else "❌ Incorrect"
            evaluation_method = result.get('evaluation_method', 'N/A')
            report += f"* **Topic:** {result['topic']} - {status}\n"
        report += "\n\nThank you for completing the assessment!"
        return {"response_text": report, "is_interview_over": True}

interview_manager = InterviewManager('interviewer/questions.json')
