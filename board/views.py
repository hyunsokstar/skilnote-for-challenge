from .models import Manual
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ManualForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 1122

# class ManualListView(LoginRequiredMixin,ListView):
#     model = Manual
#     paginate_by = 10
#
#     def get_template_names(self):
#         if self.request.is_ajax():
#             return ['board/_manual_list.html']
#         return ['board/manual_list.html']

def ManualListView(request):
    manual_list = Manual.objects.all()
    query = request.GET.get('q')

    if query:
        manual_list = Manual.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(manual_list, 5) # 6 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    print("posts check: ", posts)

    context = {
        # 'object_list':manual_list,
        'page':page,
        'posts':posts
    }

    return render(request, "board/manual_list.html", context)

class ManulUpdate(UpdateView):
    model = Manual
    form_class = ManualForm

def delete_manual(request, pk):
    manual = Manual.objects.get(pk=pk)

    if request.user == manual.author:
        manual.delete()
        messages.success(request,'게시물을 삭제했습니다.')
        return redirect('/board/')
    else:
        messages.success(request,'당사자만 삭제 가능합니다.')
        return redirect('/board/')

class ManualCreateView(CreateView):
    model = Manual
    form_class = ManualForm

    def form_valid(self, form):
        fn = form.save(commit=False)
        fn.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('board:manual_list')



class ManualDetailView(DetailView):
    model = Manual
    # def get_template_names(self):
    #     if self.request.is_ajax():
    #         return ['todo/_todo_detail.html']
    #     return ['todo/todo_detail.html']

        # def get_context_data(self, *, object_list=None, **kwargs):
        #     context = super(todoDetail, self).get_context_data(**kwargs)
        #     context['comments'] = CommentForTodo.objects.filter(todo=self.object.pk)
        #     context['detail_id'] = self.object.pk
        #     context['comment_form'] = CommentForm()
        #     return context
