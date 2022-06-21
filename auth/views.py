from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, CustomPasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, account_password_reset
#from django.contrib.auth.models import User
from accounts.models import User
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from django.template import RequestContext

from courses.models import Course

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return render(request, self.template_name, context)

def error_404_view(request, template_name="error404.html"):
    response = render(None, 'error404.html')
    response.status_code = 404
    return response

def error_500_view(request, template_name="error500.html"):
    response = render(None, 'error500.html')
    response.status_code = 500
    return response

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account activation'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def password_reset(request):
    reset_type = 'reset_request'
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = get_user_model().objects.get(email=form.cleaned_data["email"])
            except:
                form.errors['email'] = ["No user with that email exists"]
                return render(request, 'password_reset.html', context={'form': form, 'type': reset_type})
            
            if user:
                current_site = get_current_site(request)
                mail_subject = 'Password recovery'
                message = render_to_string('registration/reset_password_email.html',{
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_password_reset.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
        return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/password_reset.html', {'form': form})

def reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_password_reset.check_token(user, token):
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')