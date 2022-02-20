from django.shortcuts import render, redirect
from .models import Post, Category, Tag, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import CommentForm
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView
from django.urls import reverse_lazy
from .forms import PostingFormForPost
from django.urls import reverse


class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostingFormForPost
    ordering = ['-created']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_list')


def delete_comment(request, pk):
    print('함수 실행 확인')
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    if request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url() + '#comment-list')
    else:
        return redirect('/blog/')

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
post_delete = PostDeleteView.as_view()

# todo 댓글 수정
class CommentUpdate(UpdateView):
    model = Comment
    form_class = PostingFormForPost

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment


class PostUpdate(UpdateView):
    model = Post
    fields = [
        'title', 'content', 'head_image', 'category', 'tags'
    ]

class PostList(ListView):
    model = Post
    paginate_by = 5
    ordering = ['-created']

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/post_list2.html']
        return ['blog/post_list.html']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        return context

class PostSearch(PostList):
    def get_template_names(self):
        return ['blog/post_list_search.html']
    def get_queryset(self):
        print("PostSearch 확인")
        q = self.kwargs['q']
        object_list = Post.objects.filter(Q(title__contains=q) | Q(content__contains=q)).order_by('-created')
        print("result : ", object_list)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostSearch, self).get_context_data(**kwargs)
        context['search_word'] = self.kwargs['q']
        return context

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()
        return context

class PostListByCategory(ListView):
    model = Post
    paginate_by = 5
    ordering = ['-created']

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-created')

    # post_list.html에 넘겨줄 변수를 설정
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category
        return context


# 2244
class PostListByTag(ListView):
    model = Post
    paginate_by = 5
    ordering = ['-created']

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=tag_slug)
        return tag.post_set.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        tag_slug = self.kwargs['slug']
        context['tag'] = Tag.objects.get(slug=tag_slug)
        return context

def new_comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
    else:
        return redirect('/blog/')
