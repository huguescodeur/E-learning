import base64
from functools import wraps
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import logout
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
        default_image = "account/static/images/user_profil/default_image.png"

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
                is_staff, is_active, is_superuser, last_login, image)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                [nom, email, hashed_password, role, nom, timezone.now(), nom, nom, False, True, False,
                 timezone.now(), default_image])

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


# ? Settings
@custom_login_required
def settings_view(request):
    user_id = request.session.get('user_id', None)

    current_view_name = request.resolver_match.url_name
    context = {'title': 'Paramètres', 'current_view_name': current_view_name}

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()

        print(user)

        context['user'] = user
        context["image_url"] = context["user"][13].replace(
            'account/static/', '')

        print(context['user'])
        print(context["image_url"])
    # print(context["user"][-1])

    return render(request, 'settings/settings.html', context)


# ? Update User Info Compte
@custom_login_required
def update_user_info_view(request):
    user_id = request.session.get('user_id', None)

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        old_password = request.POST.get('password-actuel')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        print("Name", name)
        print("Email", email)
        print("Old_password", old_password)
        print("New_password", new_password)
        print("Confirm_password", confirm_password)

        with connection.cursor() as cursor:
            if name:
                cursor.execute(
                    "UPDATE account_user SET nom = %s, username = %s, first_name = %s, last_name = %s WHERE id = %s",
                    [name, name, name, name, user_id]
                )

                print("New Name", name)
            if email:
                try:
                    validate_email(email)
                    cursor.execute("UPDATE account_user SET email = %s WHERE id = %s", [
                        email, user_id])
                except ValidationError:
                    return JsonResponse({'error_message': 'Email non valide.'})

            if old_password and new_password and confirm_password:
                current_password = user[1]
                if not check_password(old_password, current_password):
                    return JsonResponse({'error_message': 'Le mot de passe actuel est incorrect.'})

                if new_password != confirm_password:
                    return JsonResponse({'error_message': 'Les mots de passe ne correspondent pas.'})

                if check_password(old_password, user[1]):
                    hashed_password = make_password(new_password)
                    cursor.execute("UPDATE account_user SET password = %s WHERE id = %s", [
                        hashed_password, user_id])
                    print("Password updated", new_password)
                    # return redirect(reverse('settings'))
                    return JsonResponse({'redirect_url': reverse('settings')})

        return redirect(request.META.get('HTTP_REFERER', 'settings'))
        # return redirect(reverse('settings'))


# ? Update image
@custom_login_required
def update_image_view(request):
    user_id = request.session.get('user_id', None)

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()

    if request.method == 'POST':
        image_data = request.FILES['new-image']
        file_name = "{}_{}".format(user[12], image_data.name.replace(' ', '_'))
        file_path = "account/static/images/user_profil/{}".format(file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in image_data.chunks():
                destination.write(chunk)

        with connection.cursor() as cursor:
            cursor.execute("UPDATE account_user SET image = %s WHERE id = %s", [
                           file_path, user_id])

        return JsonResponse({'redirect_url': reverse('settings')})
    else:
        return JsonResponse({'status': 'failed'})


# ? Delete account
@custom_login_required
def delete_account_view(request):
    user_id = request.session.get('user_id', None)
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM account_apprenant WHERE user_id = %s", [user_id])
        cursor.execute(
            "DELETE FROM account_formateur WHERE user_id = %s", [user_id])
        cursor.execute("DELETE FROM account_user WHERE id = %s", [user_id])
        logout(request)
    return JsonResponse({'redirect_url': reverse('connexion')})
