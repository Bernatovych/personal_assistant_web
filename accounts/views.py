from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from accounts.forms import SignUpForm, ProfileUpdateForm, UpdateUserForm
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib import messages


class UserSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return redirect('account_activation_sent')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


@login_required
def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if profile.user != request.user:
        raise PermissionDenied
    form = UpdateUserForm(request.POST, instance=profile.user)
    form_profile = ProfileUpdateForm(request.POST, instance=profile)
    if request.method == 'POST':
        if form.is_valid() and form_profile.is_valid():
            form.save()
            form_profile.save()
            messages.success(request, 'Profile was updated successfully')
            return redirect('home')
    else:
        form = UpdateUserForm(instance=profile.user)
        form_profile = ProfileUpdateForm(instance=profile)
    return render(request, 'profile_update_form.html', {'form': form, 'form_profile': form_profile})
