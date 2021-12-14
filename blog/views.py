from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from blog.forms import CommentForm

# Create your views here.
def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    context={
      "posts":posts,
      
    }
    
    return render(request, "blog/index.html",context)

  
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
    return render(request, "blog/post-details.html", context)
