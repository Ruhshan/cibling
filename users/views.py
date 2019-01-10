from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# email confirmation things
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# Create your views here.


def register(request):
    #messages.success(request,'{}'.format(request.method))
    if request.method=='POST':
        #messages.success(request,'login/reg request {}'.format(request.POST.get('submit')))
        if request.POST.get('submit')=='register':
            reg_form=UserRegisterForm(request.POST)
            login_form = AuthenticationForm()

            if reg_form.is_valid():
                '''
                reg_form.save()
                username=reg_form.cleaned_data.get('username')
                messages.success(request, 'Account created for {}. You can now log in'.format(username))
                return redirect('login')
                '''
                user=reg_form.save(commit=False)
                user.is_active=False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = reg_form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')

        elif request.POST.get('submit')=='login':
            login_form=AuthenticationForm(request,request.POST)
            reg_form = UserRegisterForm()

            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    user=login_form.get_user()
                    login(request,user)
                    return redirect('timeline-about')
                else:
                    return redirect('register')

            else:
                return redirect('login')

    else:
        reg_form = UserRegisterForm()
        login_form = AuthenticationForm()

    return render(request, 'users/register.html', {'reg_form':reg_form, 'login_form':login_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
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



@login_required
def timeline_about(request):
    return render(request, 'users/timeline-about.html')
