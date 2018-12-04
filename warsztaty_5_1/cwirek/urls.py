from django.urls import path
from .views import HomeView, TweetCreateView, LoginUserView, LogoutUserView, RegisterUserView, ProfileView, \
    ConfirmDeleteUserView, TweetDetailView, TweetDeleteView, UserTwitterListView, MessagesView

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('add_tweet/', TweetCreateView.as_view(), name='tweet-add'),
    path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweet_delete/<int:pk>/', TweetDeleteView.as_view(), name='tweet-delete'),
    path('user_tweets/<int:id_user>/', UserTwitterListView.as_view(), name='user-tweets'),
    path('user_message/<int:id_user>/', MessagesView.as_view(), name='user-message'),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_user/<int:pk>/', ConfirmDeleteUserView.as_view(), name='delete-user'),
]