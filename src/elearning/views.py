from django.db import connection
from django.shortcuts import render


# ! Les Menu De Navigation
# ? Accueil
def index_view(request):
    user_id = request.session.get('user_id', None)

    current_view_name = request.resolver_match.url_name
    context = {'title': 'Accueil', 'current_view_name': current_view_name}

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()

        context['user'] = user
        context["image_url"] = context["user"][13].replace(
            'account/static/', '')

        print(context["image_url"])

    return render(request, 'layouts/menu/index.html', context)


# ? Tutoriels
def tutoriels_view(request):
    user_id = request.session.get('user_id', None)

    current_view_name = request.resolver_match.url_name
    context = {'title': 'Tutoriels', 'current_view_name': current_view_name}

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()

        context['user'] = user
        context["image_url"] = context["user"][13].replace(
            'account/static/', '')

        print(context["image_url"])

    # print(context["user"][-1])

    return render(request, 'layouts/menu/tutoriels.html', context)







# ? Blog
def blog_view(request):
    user_id = request.session.get('user_id', None)

    current_view_name = request.resolver_match.url_name
    context = {'title': 'Blog', 'current_view_name': current_view_name}

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()

        context['user'] = user
        context["image_url"] = context["user"][13].replace(
            'account/static/', '')

        print(context["image_url"])
    # print(context["user"][-1])

    return render(request, 'layouts/menu/blog.html', context)


# ? Contact
def contact_view(request):
    user_id = request.session.get('user_id', None)

    current_view_name = request.resolver_match.url_name
    context = {'title': 'Contact', 'current_view_name': current_view_name}

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()

        context['user'] = user
        context["image_url"] = context["user"][13].replace(
            'account/static/', '')

        print(context["image_url"])
    # print(context["user"][-1])

    return render(request, 'layouts/menu/contact.html', context)
