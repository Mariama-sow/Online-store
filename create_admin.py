import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinestore.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    if not User.objects.filter(email='sowmariam@gmail.com').exists():
        User.objects.create_superuser(
            first_name='Mariam',
            last_name='Sow',
            email='sowmariam@gmail.com',
            password=os.getenv('ADMIN_PASSWORD')  # Mieux: utiliser une variable d'environnement
        )
        print("Superutilisateur créé !")
except Exception as e:
    print("Erreur:", str(e))