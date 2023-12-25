from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from .forms import RegisterUser
from .models import Question, Choice, Vote, NewUser
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic


class Home(generic.ListView):
    template_name = 'polls/home_page.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_object(self, queryset=None):
        question = super(DetailView, self).get_object(queryset)
        if question.was_published_recently or self.request.user.is_staff:
            return question
        else:
            raise PermissionDenied()


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "СДЕЛАЙТЕ ВЫБОР"
        })
    else:
        if Vote.objects.filter(question=question, user=request.user):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'ПРОГОЛОСОВАТЬ МОЖНО ТОЛЬКО ОДИН РАЗ'
            })
        else:
            question.question_vote += 1
            question.save()
            selected_choice.votes += 1
            selected_choice.save()
            user_voted = Vote.objects.create(question=question, user=request.user)
            user_voted.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class Register(CreateView):
    model = NewUser
    template_name = 'registration/register.html'
    form_class = RegisterUser
    success_url = reverse_lazy('login')
    success_page = 'registration'


class UserDetail(LoginRequiredMixin, generic.DetailView):
    model = NewUser
    template_name = 'polls/log_user.html'


class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    model = NewUser
    template_name = 'polls/update_user.html'
    success_url = '/'
    fields = ('username', 'photo_avatar')

    def get_object(self, queryset=None):
        objs = super(UserUpdate, self).get_object(queryset)
        if objs != self.request.user:
            raise PermissionDenied()
        else:
            return self.request.user


class UserDelete(LoginRequiredMixin, generic.DeleteView):
    model = NewUser
    template_name = 'polls/delete_user.html'
    success_url = reverse_lazy('polls:home_page')

