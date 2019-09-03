from django.urls import path, re_path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('',views.PostListView.as_view(),name='post_list'),
    path('user/<str:username>/',views.UserPostListView.as_view(),name='userpost_list'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('profile/',views.profile,name='profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    # path('userprofile/<str:username>/',views.userprofile,name='userprofile'),
    # this path was created to check the userprofile it worked fine.
    # but then I merged that with userpost_list view.
    # to check profile and posts of a user at the same time not only profile.
]
