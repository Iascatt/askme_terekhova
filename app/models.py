from django.db import models
from django.contrib.auth.models import User

# Create your models here.
LIKE = 1
DISLIKE = -1

count = 10
class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-date')[:count]

    def get_hot(self):
        return sorted(self.all(), key=lambda question: get_answers_count(question))[:count]

    def get_by_tag(self, tag):
        return self.filter(tag__exact=tag)

class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(to_question__exact=question)

    def get_answers_count(self, question):
        return self.filter(to_question__exact=question).count()

class TagManager(models.Manager):
    def get_top(self):
        return self.order_by('-popularity')[:count]
class RatingAnswerManager(models.Manager):
    def get_answers_likes(self, answer):
        return sum(self.filter(answer__exact=answer).rating[0])


class RatingQuestionManager(models.Manager):
    def get_questions_likes(self, question):
        return sum(self.filter(question__exact=question).rating[0])

class Profile(User):
    avatar = models.ImageField()
    def __str__(self):
        return f'{self.username}'

class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True)
    objects = TagManager()
    def __str__(self):
        return f'{self.tag_name}'



class Question(models.Model):
    text = models.CharField(max_length=300)
    date = models.DateField(blank=True, null=True)
    author = models.ForeignKey(Profile, models.CASCADE)
    title = models.CharField(max_length=70)
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()
    def __str__(self):
        return f'{self.title}'

class Answer(models.Model):
    text = models.CharField(max_length=300)
    date = models.DateField(blank=True, null=True)
    author = models.ForeignKey(Profile, models.CASCADE)
    to_question = models.ForeignKey(Question, models.CASCADE)
    objects = AnswerManager()


class RatingAnswer(models.Model):

    user = models.ForeignKey(Profile, models.CASCADE)
    rated = models.ForeignKey(Answer, models.CASCADE)
    objects = RatingAnswerManager()
    class Meta:
        unique_together = ('user', 'rated')

    STATUSES = [
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    ]

    rating = models.IntegerField(choices=STATUSES)


class RatingQuestion(models.Model):
    user = models.ForeignKey(Profile, models.CASCADE)
    rated = models.ForeignKey(Question, models.CASCADE)
    objects = RatingQuestionManager()
    class Meta:
        unique_together = ('user', 'rated')

    STATUSES = [
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    ]

    rating = models.IntegerField(choices=STATUSES)
