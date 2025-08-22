from django.views.generic import ListView

from blog.models import Post


#Вью для блогу та постів

class BlogListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.order_by("-created_at")
