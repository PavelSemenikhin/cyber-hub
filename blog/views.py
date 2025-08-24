from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import ListView, DetailView, CreateView

from blog.forms import PostCreateForm, CommentForm
from blog.models import Post, Comment


#Вью для блогу та постів
class BlogListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 8

    def get_queryset(self):
        queryset = Post.objects.order_by("-created_at").prefetch_related("comments", "game", "owner")

        game_id = self.request.GET.get("game")
        search_query = self.request.GET.get("search")

        if game_id:
            queryset = queryset.filter(game_id=game_id)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query) |
                Q(owner__username__icontains=search_query) |
                Q(game__name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from tournaments.models import Game
        context["games"] = Game.objects.all()
        context["selected_game_id"] = self.request.GET.get("game")
        context["search_query"] = self.request.GET.get("search", "")
        return context


#Вью ндля перегляду делатей посту
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comments.all()  # тепер усі, бо видалених немає
        context["comment_count"] = post.comments.count()
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.owner = request.user
            comment.save()
            return self.get(request, *args, **kwargs)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


#Вью створення посту
class PostCreateView(LoginRequiredMixin ,generic.CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:post-detail", kwargs={"pk": self.object.pk})


#Вью на редагування посту
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner

    def get_success_url(self):
        return reverse_lazy("blog:post-detail", kwargs={"pk": self.object.pk})


#Вью для видалення посту
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:blog")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post successfully deleted.")
        return super().delete(request, *args, **kwargs)


#Вью для видалення коментара
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        post_pk = comment.post.pk
        comment.delete()
        return redirect("blog:post-detail", pk=post_pk)

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        return self.request.user == comment.owner