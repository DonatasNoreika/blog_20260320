from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Post, Comment, CustomUser
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def posts(request):
    posts = Post.objects.order_by('-pk')
    paginator = Paginator(posts, per_page=2)
    page_number = request.GET.get('page')
    paged_posts = paginator.get_page(page_number)
    context = {
        'posts': paged_posts,
    }
    return render(request, template_name="posts.html", context=context)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'


def search(request):
    query = request.GET.get('query')
    context = {
        'query': query,
        'posts': Post.objects.filter(Q(title__icontains=query) |
                                     Q(content__icontains=query) |
                                     Q(author__username__icontains=query))
    }
    return render(request, template_name="search.html", context=context)


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "user_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UserCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = "user_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'photo']
    success_url = reverse_lazy('profile')
    template_name = "profile.html"

    def get_object(self, queryset = ...):
        return self.request.user