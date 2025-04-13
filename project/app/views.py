from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db.models import F

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "app/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "app/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "app/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "app/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("app:results", args=(question.id,)))