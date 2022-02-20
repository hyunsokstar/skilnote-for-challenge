from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, resolve_url

from .models import Suggestion , RecommandSuggestion
from django.db.models import Q
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .forms import SuggestionForm

# Create your views here.
def recommand_suggestion(request, id):
    recommand_count = RecommandSuggestion.objects.filter(Q(suggestion=id)).count()
    print("recommand_count : ", recommand_count)
    sl =  get_object_or_404(Suggestion, pk=id)

    if (recommand_count == 0):
        rc = RecommandSuggestion.objects.create(author=request.user, suggestion = sl)
        print('추천을 추가')
    else:
        RecommandSuggestion.objects.filter(suggestion=id).delete()
        print('추천을 삭제')
    return redirect('/management/suggestion/list')

def suggestion_new(request):
    if request.method=="POST":
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.author = request.user
            suggestion.save()
            return redirect('management:suggestion_list')
    else:
        form = SuggestionForm()
    return render(request, 'management/suggestion_form.html',{
        'form':form
    })
