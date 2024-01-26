from django.shortcuts import render

# ! Les Menu De Navigation
def ma_vue(request):
    # Obtenez le nom de la vue associée à l'URL actuelle
    current_view_name = request.resolver_match.url_name
    return render(request, 'votre_template.html', {'current_view_name': current_view_name})


# ? Accueil 
def index_view(request):
    current_view_name = request.resolver_match.url_name
    context = {'current_view_name': current_view_name}
    return render(request, 'layouts/menu/index.html', context)


# ? Tutoriels 
def tutoriels_view(request):
    current_view_name = request.resolver_match.url_name
    context = {'title': 'Tutoriels', 'current_view_name': current_view_name}
    return render(request, 'layouts/menu/tutoriels.html', context)


# ? Formations 
def formations_view(request):
    current_view_name = request.resolver_match.url_name
    context = {'title': 'Formations', 'current_view_name': current_view_name}
    return render(request, 'layouts/menu/formations.html', context)


# ? Blog
def blog_view(request):
    current_view_name = request.resolver_match.url_name
    context = {'title': 'Blog', 'current_view_name': current_view_name}
    return render(request, 'layouts/menu/blog.html', context)


# ? Contact 
def contact_view(request):
    current_view_name = request.resolver_match.url_name
    context = {'title': 'Contact', 'current_view_name': current_view_name}
    return render(request, 'layouts/menu/contact.html', context)


# ? Connexion
def connexion_view(request):
    current_view_name = request.resolver_match.url_name
    context = {'title': 'Connexion', 'current_view_name': current_view_name}
    return render(request, 'layouts/auth/connexion.html', context)


# ? inscription
def inscription_view(request):
    current_view_name = request.resolver_match.url_name
    context = {'title': 'inscription', 'current_view_name': current_view_name}
    return render(request, 'layouts/auth/inscription.html', context)
