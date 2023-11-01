from django import template

register = template.Library()
from app.models import Answer, User


@register.filter
def custom_filter(user, answer):
    # Get the answer and user objects
    # answer = Answer.objects.get(id=answer_id)
    # user = User.objects.get(id=user_id)

    # Check if the answer is liked by the user
    if answer.answerlike_set.filter(user=user).exists():
        return True
    else:
        return False
