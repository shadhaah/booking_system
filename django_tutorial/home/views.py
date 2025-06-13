from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import Departments, Doctors

# For AI Q&A
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------- Your Existing Views --------------------

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'confirmation.html')
    else:
        form = BookingForm()
    dict_form = {'form': form}
    return render(request, 'booking.html', dict_form)

def doctors(request):
    dict_docs = {'doctors': Doctors.objects.all()}
    return render(request, 'doctors.html', dict_docs)

def contact(request):
    return render(request, 'contact.html')

def department(request):
    dict_dept = {'dept': Departments.objects.all()}
    return render(request, 'department.html', dict_dept)

# -------------------- NEW: AI Q&A Features --------------------

# Load AI model and Q&A data once
model = SentenceTransformer('all-MiniLM-L6-v2')

qa_file_path = os.path.join(settings.BASE_DIR, 'data', 'qa_data.json')
with open(qa_file_path, 'r') as f:
    qa_data = json.load(f)

questions = [item['question'] for item in qa_data]
answers = [item['answer'] for item in qa_data]
question_embeddings = model.encode(questions)

@csrf_exempt
@require_POST
def ai_qa_local(request):
    user_input = json.loads(request.body).get("question", "")

    if not user_input:
        return JsonResponse({"answer": "Please enter a question."})

    user_embedding = model.encode([user_input])
    similarities = cosine_similarity(user_embedding, question_embeddings)[0]

    best_match_idx = np.argmax(similarities)
    best_score = similarities[best_match_idx]

    if best_score > 0.6:
        return JsonResponse({"answer": answers[best_match_idx]})
    else:
        return JsonResponse({"answer": "Sorry, I couldn't find an answer to that question."})

def ask_page(request):
    return render(request, 'ask.html')
