import csv
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .models import Photo
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MiniContactForm
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def accueil(request):
   

    return render(request,'gc3_app/index.html')


def contact(request):
    return render(request,'gc3_app/contact.html', )


def actualite(request):
    photos = Photo.objects.all().order_by('-date_ajout')
    return render(request, 'gc3_app/actualite.html', {'photos': photos})

def inscription(request):
    if request.method == 'POST':
        form = MiniContactForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            statut = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            accepte = "Oui" if form.cleaned_data['accepte_conditions'] else "Non"
            telephone = form.cleaned_data['telephone']
            cni = form.cleaned_data['cni']
            # Chemin vers le fichier CSV (enregistré à la racine du projet)
            csv_file_path = os.path.join(settings.BASE_DIR, 'messages.csv')
            
            # Vérifie si le fichier existe déjà pour ajouter les en-têtes si besoin
            file_exists = os.path.isfile(csv_file_path)

            # Écriture dans le fichier CSV (mode 'a' pour ajouter à la suite)
            with open(csv_file_path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Si le fichier vient d'être créé, on écrit la première ligne d'en-tête
                if not file_exists:
                    writer.writerow(['Nom', 'Email','telephone', 'cni','Statut','Message','Accepte'])
                
                # Ajout des données du formulaire
                writer.writerow([nom, email,telephone,cni, statut, message,'non'])

            messages.success(request, f'Merci {nom}, votre message a bien été enregistré dans le fichier CSV !')
            return redirect('accueil')
    else:
        form = MiniContactForm()

    return render(request, 'gc3_app/inscription.html', {'form': form})



@staff_member_required
def afficher_fiche_csv(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'messages.csv')
    
    # Traitement de la mise à jour lorsqu'on clique sur "Enregistrer"
    if request.method == 'POST':
        lignes_selectionnees = request.POST.getlist('lignes') # Indices des lignes cochées

        if os.path.exists(csv_file_path):
            lignes = []
            with open(csv_file_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                lignes = list(reader)
            
            if lignes:
                for index in range(1, len(lignes)):
                    # S'assure que la ligne possède bien au moins 7 colonnes
                    while len(lignes[index]) < 7:
                        lignes[index].append('non')
                    
                    # Si la ligne est cochée -> 'oui', sinon -> 'non' (colonne index 6: Accepte)
                    if str(index) in lignes_selectionnees:
                        lignes[index][6] = 'oui'
                    else:
                        lignes[index][6] = 'non'
                
                # Réécriture propre du fichier CSV
                with open(csv_file_path, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(lignes)
                
                messages.success(request, "La sélection pour l'accueil a été mise à jour avec succès !")
        return redirect('selection') # Remplacez par le nom de votre url si besoin (ex: 'afficher_fiche_csv')

    # Lecture des données pour affichage
    messages_data = []
    header = []

    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for index, row in enumerate(reader, start=1):
                while len(row) < 7:
                    row.append('non')
                messages_data.append((index, row))

    context = {
        'header': header,
        'messages_data': messages_data,
    }
    return render(request, 'gc3_app/fiche_cvs.html', context)

#def afficher_fiche_csv(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'messages.csv')
    messages_data = []
    header = []

    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            # On associe chaque ligne à son index réel dans le fichier
            for index, row in enumerate(reader, start=1):
                messages_data.append((index, row))

    context = {
        'header': header,
        'messages_data': messages_data,
    }
    return render(request, 'gc3_app/fiche_cvs.html', context)


#def afficher_fiche_csv(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'messages.csv')
    messages_liste = []
    headers = []

    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
            if data:
                headers = data[0]       # Première ligne = en-têtes (Nom, Email, Message)
                messages_liste = data[1:] # Lignes suivantes = données
                messages_liste = messages_liste[::-1]

    context = {
        'headers': headers,
        'messages_liste': messages_liste,
    }
    return render(request, 'gc3_app/fiche_cvs.html', context)



def selection(request):
    personnes_selectionnees = []
    csv_file_path = os.path.join(settings.BASE_DIR, 'messages.csv')
    
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None) # Ignore l'en-tête du fichier CSV
            for row in reader:
                # Vérifie que la ligne a au moins 7 colonnes et que la colonne 'Accepte' (index 6) vaut 'oui'
                if len(row) >= 7 and row[6].strip().lower() == 'oui':
                    personnes_selectionnees.append({
                        'nom': row[0],
                        'email': row[1],
                        'telephone': row[2],
                        'cni': row[3],
                        'statut': row[4],
                        'message': row[5]
                    })

    context = {
        'personnes': personnes_selectionnees,
    }
    return render(request, 'gc3_app/selection.html', context)


def basculer_affichage_csv(request, index_ligne):
    csv_file_path = os.path.join(settings.BASE_DIR, 'messages.csv')
    
    if os.path.exists(csv_file_path):
        lignes = []
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            lignes = list(reader)
        
        # Vérifier que l'index existe (en sautant l'en-tête, index 0)
        if lignes and 0 < index_ligne < len(lignes):
            # La colonne d'affichage est la 6ème (index 5)
            # S'il n'y a pas assez de colonnes, on les complète
            while len(lignes[index_ligne]) < 7:
                lignes[index_ligne].append('Non')
                
            statut_actuel = lignes[index_ligne][6].strip().lower()
            
            # On inverse le statut
            if statut_actuel == 'oui':
                lignes[index_ligne][6] = 'Non'
            else:
                lignes[index_ligne][6] = 'Oui'
                
            # Réécrire tout le fichier CSV mis à jour
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(lignes)
                
    return redirect('fiche_cvs')