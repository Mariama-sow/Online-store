from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from users.utlis.send_activation_email import send_activation_mail

from .models import User

class CustumAuthentificationForm(AuthenticationForm):
    # Remplacer username par email
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(
            self.request, username=email, password=password
        )
        if user is None:
            raise ValidationError(
                "Email ou Mot de passe incorrect."
            )
        if not user.is_active:
            send_activation_mail(user)
            raise ValidationError(
                ("Votre compte n'est pas ete actif, consulter votre boite "
                    "email pour activer votre compte")
            )
        return self.cleaned_data
    
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    email = forms.EmailField(
        required=True, 
        help_text="Requis. Entrez une adresse email valide.",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
    )
    profil = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'profil', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email existe déjà")
        return email
    

class UserProfilUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','profil']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            }),
            'email':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'profil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
                
            })

        }
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'votre adresse email'
        }), 
        label="Emails"
    )
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Aucun compte n'est associé à cette adresse email")
        return email
    
class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': ' Nouveau mot de passe'
        }),
        min_length=8
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Confirmer le nouveau mot de passe'
        })
    )

    def clean(self):
        cleaned_deta = super().clean()
        password = cleaned_deta.get('password')
        password_confirm = cleaned_deta.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Les mots de passe ne correspondent pas. ")
            validate_password(password)
        return cleaned_deta
