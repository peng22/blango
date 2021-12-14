from .views import *
from django.urls import path
urlpatterns=[
  path("",index),
  path("<slug>/", post_detail, name="blog-post-detail")

]