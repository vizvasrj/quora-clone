from django.urls import path
from .views import (
    create_question, question_detail, 
    list_questions, add_answer, 
    edit_answer, like_answer,
    unlike_answer,

)

urlpatterns = [
    path("question/create", create_question, name="create_question"),
    path("question/<int:question_id>", question_detail, name="question_detail"),
    path("", list_questions, name="list_questions"),
    # add path for add answer to given question
    path("question/<int:question_id>/add_answer", add_answer, name="add_answer"),
    # add path for edit answer
    path("answer/<int:answer_id>/edit", edit_answer, name="edit_answer"),
    # add path for like answer
    path("answer/<int:answer_id>/like", like_answer, name="like_answer"),
    # add path for unlike answer
    path("answer/<int:answer_id>/unlike", unlike_answer, name="unlike_answer"),

]