# interviewer/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .logic import interview_manager

@csrf_exempt 
def start_interview_endpoint(request):
    if request.method == 'POST':
        # Reset the state for a new interview
        interview_manager.__init__('interviewer/questions.json')
        response_data = interview_manager.start_interview()
        return JsonResponse(response_data)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@csrf_exempt 
def respond_to_question_endpoint(request):
    if request.method == 'POST':
        if not interview_manager.interview_started or interview_manager.current_question_index >= len(interview_manager.questions):
            return JsonResponse({"response_text": "The interview is not active or has ended.", "is_interview_over": True})
        
        try:
            data = json.loads(request.body)
            user_answer = data.get('answer')
            if user_answer is None:
                return JsonResponse({"error": "Missing 'answer' in request body"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

        response_data = interview_manager.process_answer(user_answer)
        return JsonResponse(response_data)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)
