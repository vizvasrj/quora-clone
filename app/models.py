from django.db import models
from django.contrib.auth.models import User  # Assuming you are using the built-in User model

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate questions with users
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  # This is just for a more user-friendly representation
    

class Answer(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate answers with users
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Associate answers with questions
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    
    def __str__(self):
        return self.content[:50]  # This is just for a more user-friendly representation

    def increment_like(self, user):
        if not self.answerlike_set.filter(user=user).exists():
            self.like += 1
            self.save()
            AnswerLike.objects.create(answer=self, user=user)

    def decrement_like(self, user):
        if self.answerlike_set.filter(user=user).exists():
            self.like += 1
            self.save()
            AnswerLike.objects.filter(answer=self, user=user).delete()

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('answer', 'user')
