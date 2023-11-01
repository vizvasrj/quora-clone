from django.shortcuts import render

# Create your views here.
from .models import Question

from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm
from .models import Question, Answer
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def create_question(request):
    if request.method == 'POST':

        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assuming the user is logged in
            question.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'app/create_question.html', {'form': form})

from django.core.paginator import Paginator

def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    answer_list = Answer.objects.filter(question=question).order_by('-timestamp')
    answers_per_page = 2
    paginator = Paginator(answer_list, answers_per_page)
    page = request.GET.get('page')
    answers = paginator.get_page(page)
    current_page = answers.number
    has_next = answers.has_next()
    has_previous = answers.has_previous()

    return render(request, 'app/question_detail.html', {
        'question': question, 
        'answers': answers, 
        'current_page': current_page, 
        'has_next': has_next, 
        'has_previous': has_previous,
    })

def list_questions(request):
    questions = Question.objects.all()
    paginator = Paginator(questions, 2)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    current_page = questions.number
    has_next = questions.has_next()
    has_previous = questions.has_previous()

    return render(request, 'app/list_questions.html', {
        'questions': questions,
        'current_page': current_page,
        'has_next': has_next,
        'has_previous': has_previous,


    })

    # You can pass 'questions' to your template context and render them in the template

def view_question(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'app/view_question.html', {'question': question})
    # You can pass 'question' to your template context and render it in the template
    
@login_required
def add_answer(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        answer = request.POST.get('content')
        print(answer)
        Answer.objects.create(content=answer, question=question, user=request.user)
        # question.answer_set.create(answer=answer)
        # return redirect('view_question', question_id=question.id)
    return redirect('question_detail', question_id=question.id)

def user_is_author(function):
    def wrap(request, *args, **kwargs):
        answer = get_object_or_404(Answer, id=kwargs['answer_id'])
        if answer.user == request.user:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not authorized to edit this answer')
            return redirect('question_detail', question_id=answer.question.id)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


@login_required
@user_is_author
def edit_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.method == 'POST':
        answer.content = request.POST.get('content')
        answer.save()
        messages.success(request, 'Answer updated successfully')
        return redirect('question_detail', question_id=answer.question.id)
    else:
        return render(request, 'app/edit_answer.html', {'answer': answer})



@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.increment_like(request.user)
    return redirect('question_detail', question_id=answer.question.id)

@login_required
def unlike_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.decrement_like(request.user)
    return redirect('question_detail', question_id=answer.question.id)

