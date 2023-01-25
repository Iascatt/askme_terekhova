from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random
from app import models
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'пользователей — ratio; вопросов — ratio * 10; ответы — ratio * 100; тэгов - ratio; оценок пользователей - ratio * 200'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
    def handle(self, ratio, *args, **options):
        for i in range(ratio):
            new_user = models.Profile.objects.create(username=f"User {i}")
            new_user.save()

        for i in range(ratio):
            new_tag = models.Tag.objects.create(tag_name=f"Tag {i}")
            new_tag.save()

        all_profiles = models.Profile.objects.all()
        all_tags = models.Tag.objects.all()
        for i in range(ratio * 10):
            new_question = models.Question.objects.create(
                title = f"Question {i}",
                date = date.today() - timedelta(random.randint(0, 1000)),
                author = random.choice(all_profiles),
                text = f"Hello, world! Asking question {i}.",
                )
            new_question.tags.set(set([random.choice(all_tags) for j in range(random.randint(0, 5))]))

            new_question.save()

        all_questions = models.Question.objects.all()


        for i in range(ratio * 100):
            new_answer = models.Answer.objects.create(
                text = f"Hello, here is answer {i}",
                date = date.today() - timedelta(random.randint(0, 1000)),
                author = random.choice(all_profiles),
                to_question = random.choice(all_questions)
                )
            new_answer.save()

        all_answers = models.Answer.objects.all()


        for i in range(ratio * 100):
            try:
                new_rating = models.RatingQuestion.objects.create(
                    rated=random.choice(all_questions),
                    user=random.choice(all_profiles),
                    rating=random.choice([models.LIKE,models.DISLIKE])
                )
            except IntegrityError:
                continue
            new_rating.save()


        for i in range(ratio * 100):
            try:
                new_rating = models.RatingAnswer.objects.create(
                    rated = random.choice(all_answers),
                    user=random.choice(all_profiles),
                    rating=random.choice([models.LIKE,models.DISLIKE])
                )
            except IntegrityError:
                continue
            new_rating.save()
