from django.db import connection
from django.shortcuts import render


# ? Formations
def formations_view(request):
    user_id = request.session.get('user_id', None)

    current_view_name = request.resolver_match.url_name
    context = {'title': 'Formations', 'current_view_name': current_view_name}

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM account_user WHERE id = %s", [user_id])
            user = cursor.fetchone()

        context['user'] = user
        context["image_url"] = context["user"][13].replace(
            'account/static/', '')

        print(context["image_url"])

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM videos_videos")
        all_videos = cursor.fetchall()

        print(all_videos)

    return render(request, 'formations.html', context)


# ? PlayList Formations
def playslist_formations_view(request):
    user_id = request.session.get('user_id', None)

    current_view_name = request.resolver_match.url_name
    context = {'title': 'Mes Formations',
               'current_view_name': current_view_name}

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

    return render(request, 'playlist_formations.html', context)
