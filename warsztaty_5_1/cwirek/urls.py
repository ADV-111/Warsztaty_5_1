from django.urls import path
from .views import HomeView, TweetCreateView, LoginUserView, LogoutUserView, RegisterUserView

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('add_tweet/', TweetCreateView.as_view(), name='tweet-add'),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
]