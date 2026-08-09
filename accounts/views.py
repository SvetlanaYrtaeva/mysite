from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import RegisterForm
from .models import Profile


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


@login_required
def about_me(request):
    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    return render(
        request,
        'accounts/about_me.html',
        {'profile': profile}
    )


@login_required
def user_list(request):
    users = User.objects.all().order_by('username')

    return render(
        request,
        'accounts/user_list.html',
        {'users': users}
    )


@login_required
def user_detail(request, pk):
    selected_user = get_object_or_404(User, pk=pk)
    profile = selected_user.profile

    can_edit = (
        request.user.is_staff
        or request.user == selected_user
    )

    return render(
        request,
        'accounts/user_detail.html',
        {
            'selected_user': selected_user,
            'profile': profile,
            'can_edit': can_edit,
        }
    )


class AboutMeView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/about_me.html'
    fields = ['avatar']
    success_url = reverse_lazy('accounts:about_me')

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Profile
    fields = ['avatar']
    template_name = 'accounts/profile_form.html'

    def test_func(self):
        profile = self.get_object()

        return (
            self.request.user.is_staff
            or self.request.user == profile.user
        )

    def get_success_url(self):
        return reverse_lazy('accounts:about_me')