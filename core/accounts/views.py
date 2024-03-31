from django.views import generic
from django.views.generic import base 
from django.contrib.auth import views
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .forms import SignUpForm,LoginForm
from django.contrib.auth.tokens import default_token_generator

class RegistrationView(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("accounts:email_verification_send")
    

class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


class EmailVerificationSendView(generic.TemplateView):
    template_name = 'accounts/email_verification_send.html'



# def activate(request, uidb64, token):  
#     User = get_user_model()  
#     try:  
#         uid = force_text(urlsafe_base64_decode(uidb64))  
#         user = User.objects.get(pk=uid)  
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
#         user = None  
#     if user is not None and account_activation_token.check_token(user, token):  
#         user.is_active = True  
#         user.save()  
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
#     else:  
#         return HttpResponse('Activation link is invalid!')  

class AccountActivationView(base.TemplateResponseMixin,generic.View):
    template_name = 'accounts/email_verification_check.html'
    
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        try:  
            uid = force_text(urlsafe_base64_decode(kwargs["uidb64"]))  
            user = User.objects.get(pk=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and default_token_generator.check_token(user, kwargs["token"]):  
            user.is_verified = True  
            user.save()
            print("yes")
            return redirect(reverse("accounts:login"))
        print("no")
        return redirect(reverse("accounts:login"))
        
    
class LogoutView(views.LogoutView):
    template_name = 'accounts/logged_out.html'

class PasswordChangeView(views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    
class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
    
class PasswordResetView(views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/emails/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    
class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    
class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'