from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView

from . import models

# Create your views here.


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page=per_page)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)
    page = int(page)
    num_pages = posts.paginator.num_pages
    start = page - 2 if page > 3 else 1
    end = page + 3 if page < num_pages - 4 else num_pages + 1
    avail_pages = range(start, end)
    pag_context = {"page_obj": posts, 'range': avail_pages, 'start': start, 'end': end}
    return pag_context


def index(request):
    questions = models.Question.objects.get_new()
    pag_context = paginate(questions, request, per_page=5)

    for question in questions :
        question.answers_count = models.Answer.objects.get_answers_count(question)
        question.like_number = models.RatingQuestion.objects.get_questions_likes(question)
    context = {'questions': questions, 'mode': 'new'}
    context.update(pag_context)

    return render(request, "index.html", context=context)


def hot(request):
    questions = models.Question.objects.get_hot()
    pag_context = paginate(questions, request, per_page=5)
    context = {'questions': questions, 'mode': 'hot'}
    context.update(pag_context)
    return render(request, "index.html", context=context)


def ask(request):
    return render(request, "ask.html")


def question(request, question_id: int):
    try:
        question_item = models.Question.objects.get(id=question_id)
    except IndexError:
        return HttpResponseNotFound("error 404 not found")
    else:
        answers = models.Answer.objects.get_answers(question_item)
        context = {'question': question_item, 'answers': answers}
        pag_context = paginate(answers, request, per_page=3)
        context.update(pag_context)
        return render(request, "question.html", context=context)


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def settings(request):
    return render(request, "settings.html")


def tag(request, tag_name: str):
    questions = models.QUESTIONS
    pag_context = paginate(questions, request, per_page=3)
    context = {'tag_name': tag_name}
    context.update(pag_context)
    return render(request, "tag.html", context)



