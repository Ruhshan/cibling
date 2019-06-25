from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from .forgot_password_form import ForgotPasswordForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage



class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'users/forgot_password.html',{'form':form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            current_site = get_current_site(request)
            mail_subject = 'Recover your Cibling password.'
            password = self._update_password(user)

            message = render_to_string('users/recover_password_email.html',
                                       {
                                           "user":user,
                                           "domain":current_site.domain,
                                           "password":password
                                       })
            email = EmailMessage(subject=mail_subject, body=message, from_email=settings.EMAIL_HOST_USER,
                                 to=[form.cleaned_data['email']])
            email.send()

            return render(request, 'users/forgot_password.html', {'form': form, 'valid':True, 'email':form.cleaned_data['email']})
        else:
            return render(request, 'users/forgot_password.html', {'form': form})

    def _update_password(self, user):
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        return password


