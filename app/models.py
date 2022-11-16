from django.db import models
from django.contrib.auth.models import User


# Create your models here.

QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question {question_id}',
        'text': f'Text of question {question_id}',
        'answers_number': question_id * question_id,
        'tags': ['tag' for _ in range(question_id % 5)],
        'avatar': "img/avatar-1.jfif"
    } for question_id in range(100)
]

ANSWERS = [
    {
        'id': answer_id,
        'text': f'Text of answer {answer_id}',
        'avatar': "img/avatar-2.jfif",
        'rating': answer_id
    } for answer_id in range(321)
]


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)


class Question(models.Model):
    title = models.CharField(max_length=70)
    text = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)


class Answer(models.Model):
    to_question = models.ForeignKey(Question, models.CASCADE)
    text = models.CharField(max_length=300)


class Profile(User):
    avatar = models.ImageField()


class Rating(models.Model):
    user = models.ForeignKey(Profile, models.CASCADE)
    rated = models.ForeignKey(Question, models.CASCADE)

    LIKE = 1
    DISLIKE = -1

    STATUSES = [
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    ]

    rating = models.IntegerField(choices=STATUSES)


