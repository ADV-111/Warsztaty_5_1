from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, FormView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from .models import Tweet, User, Comments
from .forms import TweetForm, UserRegisterForm, ProfileUpdateForm, UserUpdateForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib import messages


class HomeView(ListView):
    model = Tweet
    template_name = "cwirek/main.html"
    context_object_name = 'tweets'
    ordering = ['-creation_date']
    paginate_by = 10


class TweetCreateView(LoginRequiredMixin, FormView):
    form_class = TweetForm
    template_name = "cwirek/tweet_form.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(TweetCreateView, self).form_valid(form)


class TweetDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        form = CommentForm()
        comments = Comments.objects.filter(tweet_id=tweet.id)
        return render(request, "cwirek/tweet_detail.html", locals())

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            comment = Comments(content=content, tweet=tweet, user=request.user)
            comment.save()
            messages.success(request, "Komentarz został dodany")
        return redirect("tweet-detail", pk=pk)


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy("main")

    def test_func(self):
        tweet = self.get_object()
        if self.request.user == tweet.user:
            return True
        return False


class LoginUserView(auth_views.LoginView):
    template_name = "cwirek/login.html"


class LogoutUserView(auth_views.LogoutView):
    template_name = 'cwirek/logout.html'


class RegisterUserView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "cwirek/register.html", {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Konto dla {email} zostało utworzone')
            return redirect('login')
        return render(request, "cwirek/register.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'cwirek/profile.html', locals())

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        button = request.POST.get('button')
        if button == 'update':
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Twoje konto zostało zmodyfikowane')
                return redirect('profile')
        elif button == 'delete':
            user = request.user
            return redirect("delete-user", pk=user.id)


class ConfirmDeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy("login")

    def test_func(self):
        user = self.get_object()
        if self.request.user.id == user.id:
            return True
        return False


class UserTwitterListView(View):

    def get(self, request, id_user):
        user = get_object_or_404(User, id=id_user)
        tweets = Tweet.objects.filter(user_id=id_user)
        paginate_by = 5
        # TODO paginacja nie działa trzeba cos z nia zrobic
        return render(request, "cwirek/user_tweets.html", locals())



    # model = Tweet
    # template_name = 'cwirek/user_tweets.html'
    # context_object_name = 'posts'
    # paginate_by = 5

