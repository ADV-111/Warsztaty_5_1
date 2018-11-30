from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, FormView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import Tweet
from .forms import TweetForm, UserRegisterForm
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


class LoginUserView(auth_views.LoginView):
    template_name = "cwirek/login.html"


class LogoutUserView(auth_views.LogoutView):
    template_name = 'cwirek/logout.html'


class RegisterUserView(View):
    form_class = UserRegisterForm

    def get(self, request):
        return render(request, "cwirek/register.html", {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto dla {username} zostało utworzone')
            return redirect('login')
        return render(request, "cwirek/register.html", {"form": form})
