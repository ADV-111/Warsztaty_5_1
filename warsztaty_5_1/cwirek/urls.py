from django.urls import path
from .views import HomeView, TweetCreateView, LoginUserView, LogoutUserView, RegisterUserView, ProfileView, \
    ConfirmDeleteUserView, TweetDetailView, TweetDeleteView, UserTwitterListView, MessagesView, MessageReceivedView, \
    AllMessagesView, MessageSentView, MessageReceivedSpecificView, MessageSentSpecificView, ChangePasswordView

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('add_tweet/', TweetCreateView.as_view(), name='tweet-add'),
    path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweet_delete/<int:pk>/', TweetDeleteView.as_view(), name='tweet-delete'),
    path('user_tweets/<int:id_user>/', UserTwitterListView.as_view(), name='user-tweets'),
    path('user_message/<int:id_user>/', MessagesView.as_view(), name='user-message'),
    path('user_received_messages/', MessageReceivedView.as_view(), name='user-received-messages'),
    path('user_sent_messages/', MessageSentView.as_view(), name='user-sent-messages'),
    path('user_messages/', AllMessagesView.as_view(), name='user-messages'),
    path('user_received_messages/<int:id_message>/', MessageReceivedSpecificView.as_view(), name='user-message-specific'),
    path('user_sent_messages/<int:id_message>/', MessageSentSpecificView.as_view(), name='user-message-sent-specific'),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete_user/<int:pk>/', ConfirmDeleteUserView.as_view(), name='delete-user'),
]