from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import logout
from django.utils import timezone


# Logique du décirateur
def custom_login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/connexion/')
        return f(request, *args, **kwargs)

    return decorated_function


# ? Logout
def logout_view(request):
    logout(request)
    return redirect('connexion')


# ? Connexion
def connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ? utilisateur existe ?
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE email = %s", [email])
            user = cursor.fetchone()

        if user and check_password(password, user[1]):
            request.session['user_id'] = user[0]
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE account_user
                    SET last_login = %s WHERE email = %s""", [timezone.now(), email])
            return redirect("accueil")

        else:
            messages.error(request, "Email ou mot de passe incorrect")
            return render(request, "connexion.html")

    else:
        current_view_name = request.resolver_match.url_name
        context = {'title': 'Connexion',
                   'current_view_name': current_view_name, }
        return render(request, 'connexion.html', context)


# ? Gestion Back-End inscription
# @custom_login_required
def inscription_view(request):
    if request.method == 'POST':

        nom = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        role = request.POST.get('role', 'apprenant')

        # default_image = 'account/static/images/default.jpg'

        # ? Password pareil??
        if password != confirmpassword:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('inscription')

        # ? utilisateur existe ?
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE email = %s", [email])
            existing_user = cursor.fetchone()

        if existing_user:
            messages.error(request, "Email déjà utilisé par un utilisateur !")
            return render(request, 'inscription.html', )

        hashed_password = make_password(password)

        # Insértion account_user
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO account_user
                (username, email, password, role, nom, date_joined, first_name, last_name, 
                is_staff, is_active, is_superuser, last_login)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                [nom, email, hashed_password, role, nom, timezone.now(), nom, nom, False, True, False,
                 timezone.now()])

            # Récupérez l'ID du nouvel utilisateur
            cursor.execute(
                "SELECT id FROM account_user WHERE email = %s", [email])
            user_id = cursor.fetchone()[0]

        # Insertion nouvel apprenant
        if role == 'apprenant':
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO account_apprenant (nom_apprenant, is_premium, user_id) VALUES (%s, %s, %s)",
                    [nom, False, user_id])

        messages.success(request, "Inscription réussie!")

        request.session['user_id'] = user_id
        return redirect('accueil')

    else:
        current_view_name = request.resolver_match.url_name
        context = {'title': 'inscription',
                   'current_view_name': current_view_name, }
        return render(request, 'inscription.html', context)
