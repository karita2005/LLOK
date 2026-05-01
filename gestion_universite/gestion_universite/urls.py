"""
Configuration des URLs principales du projet gestion_universite.

Les URLs de l'application 'inscription' sont incluses via un include().
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    # URLs de l'application inscription (page d'accueil + CRUD)
    path('', include('inscription.urls')),
]
