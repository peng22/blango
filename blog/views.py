from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from blog.forms import CommentForm
import logging
logger = logging.getLogger(__name__)

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


# Create your views here.
@cache_page(300)
@vary_on_cookie
def index(request):
#   Here it will fetch only those fields
#       posts = (
#         Post.objects.filter(published_at__lte=timezone.now())
#         .select_related("author")
#         .only("title", "summary", "content", "author", "published_at", "slug")
#     )
# here it won't fetch those fields
#     posts = (
#         Post.objects.filter(published_at__lte=timezone.now())
#         .select_related("author")
#         .defer("created_at", "modified_at")
#     )
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})
  

  
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
        
    context={
      "post":post,
      "comment_form": comment_form
    }        
    logger.info(
    "Created comment on Post %d for user %s", post.pk, request.user
    )

    return render(request, "blog/post-details.html", context)
