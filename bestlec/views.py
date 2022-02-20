from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView

from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Best20, Finisher, RecommandBest20
from django.db.models import Q
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .forms import BestLecForm
from django.contrib.auth.mixins import LoginRequiredMixin



class FinisherDeleteView(DeleteView):
    model = Finisher
    success_url = reverse_lazy('bestlec:best20_list')
    success_message = "finisher is removed"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(FinisherDeleteView, self).delete(request, *args, **kwargs)

finisher_delete = FinisherDeleteView.as_view()

# 1122
# best20_delete
class Best20DeleteView(DeleteView):
    model = Best20
    success_url = reverse_lazy('bestlec:best20_list')
    success_message = "best is removed"

    def delete(self, request, *args, **kwargs):
            messages.success(self.request, self.success_message)
            return super(Best20DeleteView, self).delete(request, *args, **kwargs)

best20_delete = Best20DeleteView.as_view()


def recommand_lecture(request, id):
    recommand_count = RecommandBest20.objects.filter(Q(bestlec=id)).count()
    print("recommand_count : ", recommand_count)
    bl =  get_object_or_404(Best20, pk=id)

    if recommand_count < 1:
        rc = RecommandBest20.objects.create(author=request.user, bestlec= bl)
        print('추천을 추가')
    else:
        RecommandBest20.objects.filter(bestlec=id).delete()
        print('추천을 삭제')
    return redirect('/bestlec')



class FinisherCreateView(CreateView):
    model = Finisher
    fields = ['comment','git_hub','note']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행")
        fn = form.save(commit=False)
        # fn.bestlec = self.kwargs['bl_pk']
        fn.bestlec =  get_object_or_404(Best20, pk=self.kwargs['bl_pk'])
        fn.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        id = self.kwargs['bl_pk']
        return reverse('bestlec:FinisherList', args=[self.kwargs['bl_pk']])

# FinisherList
def FinisherList(request, id):
    fl = Finisher.objects.filter(Q(bestlec=id))
    print("fl : ", fl)
    print('해당 id에 대한 FinisherList')
    return render(request, 'bestlec/finisher_list.html', {
        'fl': fl,
        'fn_id':id
    })

# BestLecDetail
class BestLecDetail(DetailView):
    model = Best20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(todoDetail, self).get_context_data(**kwargs)
        context['comments'] = CommentForTodo.objects.filter(todo=self.object.pk)
        context['detail_id'] = self.object.pk
        context['comment_form'] = CommentForm()
        return context

def bestlec_new(request):
    if request.method=="POST":
        form = BestLecForm(request.POST, request.FILES)
        if form.is_valid():
            bslec = form.save(commit=False)
            bslec.author = request.user
            bslec.save()
            return redirect('/bestlec')
    else:
        form = BestLecForm()
    return render(request, 'bestlec/bestlec_form.html',{
        'form':form
    })

def grade_plus(request, id):
    Best20.objects.filter(Q(id=id)).update(grade = F('grade') + 1)
    print('grade +1 success')
    return redirect('/bestlec')

class Best20List(LoginRequiredMixin,ListView):
    model = Best20
    paginate_by = 20
    ordering = ['-grade']
