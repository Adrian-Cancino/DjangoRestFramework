from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostRetrieveDestroy.as_view(), name='post_delete'),
    path('posts/<int:pk>/vote', views.VoteCreate.as_view(), name='post_vote'),
]
