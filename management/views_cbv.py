from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView
from .models import Suggestion
from django.urls import reverse_lazy
from django.contrib import messages

from . forms import SuggestionForm

class SuggestionUpdateView(UpdateView):
    model = Suggestion
    form_class = SuggestionForm

    def get_object(self, queryset=None):
        suggestion = super(SuggestionUpdateView, self).get_object()
        if suggestion.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return suggestion

class SuggestionDeleteView(DeleteView):
    model = Suggestion
    success_url = reverse_lazy('management:suggestion_list')
    success_message = "Suggestion is removed"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SuggestionDeleteView, self).delete(request, *args, **kwargs)

class SuggestionListView(ListView):
    model = Suggestion
    paginate_by = 20

    def get_queryset(self):
        return Suggestion.objects.all().order_by('-created')
