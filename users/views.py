from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CustomUserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, ProfileInfoUpdateForm, InstituteUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import ProfileInfo, Profile, Country

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
from django.conf import settings
# Create your views here.

def register(request):
    if request.method=='POST':
        if request.POST.get('submit')=='register':
            reg_form=UserRegisterForm(request.POST)
            login_form = UserLoginForm()

            if reg_form.is_valid():

                user = reg_form.save()
                username = reg_form.cleaned_data.get('username')

                current_site = get_current_site(request)
                mail_subject = 'Activate your Cibling account.'
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })

                email = EmailMessage(subject=mail_subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[user.email])

                email.send()

                return render(request, 'users/registration_success.html', {"pending_confirmation":True})

            else:
                username = reg_form.cleaned_data.get('username')

                return render(request, 'users/register.html', {'reg_form': reg_form, 'login_form': login_form, 'reg_error':True})

        elif request.POST.get('submit')=='login':
            login_form = UserLoginForm(request.POST)
            next_param = request.GET.get('next')

            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                user = User.objects.filter(email=email).first()

                if user is not None:
                    username = user.username
                    user = authenticate(username=username,password=password)
                    if user is not None:
                        login(request, user)

                        if next_param is not None:
                            return redirect(next_param)
                        return redirect('newsfeed')



            return render(request, 'users/register.html', {'reg_form': UserRegisterForm(), 'login_form': login_form, 'reg_error':False})

    else:
        reg_form = UserRegisterForm()
        countries = Country.objects.all()
        login_form = UserLoginForm()
        messages.success(request, "Please register")

    return render(request, 'users/register.html', {'reg_form': reg_form, 'login_form':login_form,'countries':countries})


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
        return render(request, 'users/registration_success.html',{"pending_confirmation":False})
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
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
        institute_form = InstituteUpdateForm(request.POST, instance=request.user.profile)


        if form.is_valid() and institute_form.is_valid():
            form.save()
            institute_form.save()

            messages.success(request, "Your Profile Info Has Been Updated")


    else:
        form = ProfileInfoUpdateForm(instance=request.user.profile.profileinfo)
        institute_form = InstituteUpdateForm(instance=request.user.profile, initial={'country':request.user.profile.institute.country,
                                              'institute':request.user.profile.institute})


    context={
        'form': form,
        'institute_form':institute_form,
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


