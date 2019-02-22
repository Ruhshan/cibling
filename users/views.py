from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CustomUserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, ProfileInfoUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import ProfileInfo, Profile

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView

# For Password Change
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


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
            #reg_form = CustomUserRegisterForm(request.POST)
            #login_form = AuthenticationForm()
            login_form = UserLoginForm()

            if reg_form.is_valid():
                '''
                reg_form.save()
                username=reg_form.cleaned_data.get('username')
                messages.success(request, 'Account created for {}. You can now log in'.format(username))
                return redirect('login')
                '''

                reg_form.save()
                username = reg_form.cleaned_data.get('username')
                email = reg_form.cleaned_data.get('email')
                #if email.find('.ac.')!=-1:
                messages.success(request, 'Account created for {}. You can now log in'.format(username))
                return redirect('register')
                '''
                else:
                    messages.error(request, 'Please enter your academic mail')
                    return redirect('register')
                '''
                '''
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
                '''

        elif request.POST.get('submit')=='login':
            login_form = UserLoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                user = User.objects.filter(email=email).first()

                if user is not None:
                    username = user.username
                    user = authenticate(username=username,password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('newsfeed')

            return redirect('register')
            '''
            login_form=AuthenticationForm(request,request.POST)
            reg_form = UserRegisterForm()

            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    user=login_form.get_user()
                    login(request,user)
                    return redirect('newsfeed')
                else:
                    messages.ERROR('Wrong username or password given')
                    return redirect('register')

            else:
                return redirect('register')
            '''


    else:
        #reg_form = CustomUserRegisterForm()
        reg_form = UserRegisterForm()
        #login_form = AuthenticationForm()
        login_form = UserLoginForm()

    return render(request, 'users/register.html', {'reg_form':reg_form, 'login_form':login_form})

def register_login_with_username(request):
    #messages.success(request,'{}'.format(request.method))
    if request.method=='POST':
        #messages.success(request,'login/reg request {}'.format(request.POST.get('submit')))
        if request.POST.get('submit')=='register':
            reg_form=UserRegisterForm(request.POST)
            #reg_form = CustomUserRegisterForm(request.POST)
            login_form = AuthenticationForm()

            if reg_form.is_valid():
                '''
                reg_form.save()
                username=reg_form.cleaned_data.get('username')
                messages.success(request, 'Account created for {}. You can now log in'.format(username))
                return redirect('login')
                '''

                reg_form.save()
                username = reg_form.cleaned_data.get('username')
                messages.success(request, 'Account created for {}. You can now log in'.format(username))
                return redirect('register')
                '''
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
                '''

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
                    return redirect('newsfeed')
                else:
                    messages.ERROR('Wrong username or password given')
                    return redirect('register')

            else:
                return redirect('register')

    else:
        #reg_form = CustomUserRegisterForm()
        reg_form = UserRegisterForm()
        login_form = AuthenticationForm()

    return render(request, 'users/register.html', {'reg_form':reg_form, 'login_form':login_form, 'messages':messages})


def register_with_activation(request):
    #messages.success(request,'{}'.format(request.method))
    if request.method=='POST':
        #messages.success(request,'login/reg request {}'.format(request.POST.get('submit')))
        if request.POST.get('submit')=='register':
            #reg_form=UserRegisterForm(request.POST)
            reg_form = CustomUserRegisterForm(request.POST)
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
                    return redirect('newsfeed')
                else:
                    messages.ERROR('Wrong username or password given')
                    return redirect('register')

            else:
                return redirect('register')

    else:
        reg_form = CustomUserRegisterForm()
        #reg_form = UserRegisterForm()
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


class ProfileInfoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProfileInfo

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        profileinfo = self.get_object()

        if self.request.user.profile==profileinfo.profile:
            return True
        return False


@login_required
def profile_update(request):
    if request.method=='POST':
        u_form= UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, "Your Account Has Been Updated")
            return redirect('profile-edit')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form': u_form,
        'p_form': p_form,
        'pk': request.user.id
    }
    return render(request, 'users/profile_form.html', context)


@login_required
def profileinfo_update(request):
    if request.method=='POST':

        form = ProfileInfoUpdateForm(request.POST,instance=request.user.profile.profileinfo)

        if form.is_valid():
            form.save()

            messages.success(request, "Your Profile Info Has Been Updated")


    else:
        form = ProfileInfoUpdateForm(instance=request.user.profile.profileinfo)

    context={
        'form': form,
        'pk': request.user.id
    }

    return render(request, 'users/profileinfo_form.html', context)


@login_required
def timeline_about(request):
    return render(request, 'users/timeline-about.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {
        'form': form
    })
