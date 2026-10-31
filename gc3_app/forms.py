from django import forms

class MiniContactForm(forms.Form):
    CHOICES_SUJET = [
        ('ingenieur', 'ingenieur'),
        ('technicien', 'technicien'),
        ('manoeuvre qualifie', 'manoeuvre_qualifie'),
        ('non qualifie', 'manoeuvre'),
    ]
    nom = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nom@exemple.com'})
    )
    telephone = forms.CharField(
        max_length=20,
        label="Numéro de téléphone",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: +237 6XXXXXXXX'})
    )
    cni = forms.CharField(
        max_length=50,
        label="Numéro de CNI",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 112233445'})
    )
    # Ajout des boutons radio pour le sujet
    sujet = forms.ChoiceField(
        choices=CHOICES_SUJET,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="statut de l'ouvrier",
        initial='general'
        )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre message...'})
    )
    # Ajout de la case à cocher (obligatoire ou facultative)
    accepte_conditions = forms.BooleanField(
        required=True,
        label="J'accepte que mes données soient enregistrées",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )