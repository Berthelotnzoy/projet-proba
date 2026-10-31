"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from gc3_app import views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Application de gestion du personnel dans un chantier"     # Texte affiché dans le bandeau supérieur
admin.site.site_title = "Admin Mon App"              # Titre affiché dans l'onglet du navigateur
admin.site.index_title = "Gestion du site"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csv/basculer/<int:index_ligne>/', views.basculer_affichage_csv, name='basculer_affichage_csv'),
    path('', views.accueil, name='accueil'),  # Route racine
    path('inscription/', views.inscription, name='inscription'),
    path('contact/', views.contact, name='contact'),
    path('selection/', views.selection, name='selection'),
    path('fiche_cvs/', views.afficher_fiche_csv, name='fiche'),
    path('actualite/', views.actualite, name='actualite'),
   
    ]

# Ajout pour servir les images en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)