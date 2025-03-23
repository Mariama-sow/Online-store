import logging
from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import  CreateView , UpdateView
from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.db import transaction
from django.contrib import messages
from .forms import CustumAuthentificationForm , CustomUserCreationForm , PasswordResetConfirmForm , UserProfilUpdateForm, PasswordResetRequestForm
from .models import User

from .utlis.send_activation_email import send_activation_mail

from django.contrib.auth import authenticate, login, get_backends

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    authentication_form = CustumAuthentificationForm
    template_name = 'registrations/login.html'

    def get_success_url(self):
        return reverse_lazy('products:home')

    def form_valid(self, form):
        email = form.cleaned_data.get('username')  # username est en fait l'email
        password = form.cleaned_data.get('password')

        print(f"🔍 Tentative de connexion: {email} / {password}")  # Debug terminal
        user = authenticate(self.request, username=email, password=password)

        if user is None:
            print(" Échec d'authentification via `authenticate`")
            messages.error(self.request, "Email ou mot de passe incorrect.")
            return redirect("login")

        user.backend = 'users.custom_authenticate.CustomAuthentication'  # ✅ Définit le backend
        login(self.request, user)  

        print(f" Connexion réussie : {user.email}")
        return super().form_valid(form)


class CustomUserCreationView(CreateView):
    template_name ='registrations/register.html'
    form_class = CustomUserCreationForm
    success_url = ('create')

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_mail(user)

        messages.success(
            self.request,
            ("Votre compte compte a ete cree, consulter "
                "votre boite email pour activer votre compte")
        )
        return redirect(self.success_url)
    

class ActivationUserView(View):
    def get(self, request, uid, token):
        try:
            # Pour déboguer, imprimez le uid et le token
            print(f"UID reçu: {uid}")
            print(f"Token reçu: {token}")
            
            # Décodage correct du UID
            uid = force_str(urlsafe_base64_decode(uid))
            print(f"UID décodé: {uid}")
            
            # Récupérer l'utilisateur
            user = User.objects.get(pk=uid)
            print(f"Utilisateur trouvé: {user.email}")
            
            # Vérifier le token
            if default_token_generator.check_token(user, token):
                print("Token valide, activation en cours...")
                user.is_active = True
                user.save()
                messages.success(request, "Votre compte a été activé avec succès!")
                return redirect('login')
            else:
                print("Token invalide")
                messages.error(request, "Le lien d'activation est invalide.")
                return redirect('login')
                
        except Exception as e:
            print(f"Erreur d'activation: {str(e)}")
            messages.error(request, f"Erreur d'activation: {str(e)}")
            return redirect('login')
            
# class ActivationUserView(View):
#     login_url = reverse_lazy('login')

#     def get(self, request, uid, token):
#         id = urlsafe_base64_encode(uid)
#         try :
#             user = User.objects.get(id=id)
#         except User.DoesNotExist:
#             return render (request,'registrations/activation_invalid.html')
        
#         if default_token_generator.check_token(user,token):
#             user.is_active = True
#             user.save()
#             messages.success(
#                 self.request,
#                 "Votre compte a ete active. Vous pouvez vous connecter "
#             )
#             return redirect(self.login_url)
#         return render(request, 'registration/activation_invalid.html')
        
class LogoutView(View):
    login_url = reverse_lazy('login') 

    def get(self,request) :
        logout(request) 
        messages.success(
            self.request,
            "Votre a ete deconnecte"
        )
        return redirect(self.login_url)     


class UserProfilView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserProfilUpdateForm
    template_name = 'registrations/profile.html' 
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request,"Profil mis à jour avec succès! ")
        return super().form_valid(form)
        
class PasswordResetRequestView(View):
    template_name = 'registrations/password_reset_request.html'
    form_class = PasswordResetRequestForm

    def get(self, request):
        return render(request,self.template_name,{'form':self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                        reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    )

            subject = "Rénitialisation de mot de passe"
            email_template = 'registrations/password_reset_email.html'
            context = {
                'user':user,
                'reset_url': reset_url,
                'site_name': 'site'
            }
            email_content = render_to_string(email_template,context)
            
            try:
                send_mail(
                    subject,
                    email_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=email_content
                )
                messages.success(request,
                                 "Un email contenant les instructions de réinitialisation a été envoyé."
                )
                return redirect('login')
            except Exception as e:
                logger.error(f"Erreur d'envoi d'email: {e}")
                messages.error(request, 
                    "Une erreur s'est produite lors de l'envoi de l'email."
                )
        return render(request,self.template_name,{'form':form})


class PasswordResetConfirmView(View):
    template_name = 'registrations/password_reset_confirm.html'
    form_class = PasswordResetConfirmForm

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                return render(request, self.template_name, {'form':self.form_class()})
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None 
        messages.error(request,"Le lien de réinitialisation est invalide ou a expiré.")
        return redirect('login')
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None 

        form = self.form_class(request.POST)
        if user and default_token_generator.check_token(user, token) and form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
            return redirect('login')
        
        messages.error(request, "La réinitialisation du mot de passe a échoué.")
        return render(request, self.template_name, {'form': form})