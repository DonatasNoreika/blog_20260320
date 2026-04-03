from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from .models import Post, Comment, CustomUser
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CustomUserCreateForm, CommentForm


def posts(request):
    posts = Post.objects.order_by('-pk')
    paginator = Paginator(posts, per_page=2)
    page_number = request.GET.get('page')
    paged_posts = paginator.get_page(page_number)
    context = {
        'posts': paged_posts,
    }
    return render(request, template_name="posts.html", context=context)


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return super().form_valid(form)


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


class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content', 'photo']
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content', 'photo']

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.id})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "post_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("posts")

    def test_func(self):
        return self.get_object().author == self.request.user

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    fields = ['content']
    template_name = "comment_form.html"

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.id})

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    context_object_name = "comment"
    template_name = "comment_delete.html"

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.id})

    def test_func(self):
        return self.get_object().author == self.request.user