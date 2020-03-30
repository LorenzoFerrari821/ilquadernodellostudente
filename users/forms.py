from django import forms
from django.contrib.auth.models import User
from .models import Profile
from catalog.models import Item

class LoginForm(forms.Form):                                                                                            #Form per il login
    username=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DecisionForm(forms.Form):                                                                                         #Form utilizzato per le decisioni si/no
    DECISION = (
        ('Y', 'Si'),
        ('N', 'No'),
    )
    decision=forms.ChoiceField(choices=DECISION,widget=forms.RadioSelect,label="Decisione")

class SignupForm(forms.ModelForm):                                                                                      #Modifica i campo per aggiungere errori e testo in italiano, si occupa della parte di dati del modello User
    error_messages = {
        'password_mismatch': "Le due password non sono uguali, riprova!",
        'unique': "Questo nome utente esiste già",
        'invalid': 'La mail inserita non è valida'
    }
    username = forms.CharField(label=("Username(*)"),error_messages=error_messages)
    password1 = forms.CharField(label=("Password(*)"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Conferma password(*)"), widget=forms.PasswordInput)
    first_name=forms.CharField(label="Nome",required=False)
    last_name = forms.CharField(label="Cognome",required=False)
    email=forms.EmailField(label="Indirizzo Email(*)", error_messages=error_messages)

    class Meta:
        model = User
        fields=('username','first_name','last_name','email')

    def clean_email(self):                                                                                              #Controlla il dominio della mail. Per django prova@prova.prova è una mail valida
        alloweddomains=['.com','.it','.org']
        email = self.cleaned_data.get('email')
        for i in alloweddomains:
            if email.endswith(i):
                return email
        raise forms.ValidationError("Il dominio della mail deve essere /'.com/',/'.it/' o /'.org/'")

    def clean_password2(self):                                                                                          #Controllo password uguali
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):                                                                                        #Specifica come salvare la password, siccome nel form ce ne sono 2
        user = super(forms.ModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):                                                                                     #Form mostrato sempre nella registrazione, ma si occupa delle info contenute nel modello Profilo
    image = forms.FileField(label="Immagine di profilo",required=False, help_text='Si consiglia l\'uso di immagini di dimensioni 400x400 px')

    class Meta:
        model=Profile
        fields=['qualification','image']

class EditUser(forms.ModelForm):                                                                                        #Form per modifica dati utente( per la password c'è un form diverso)
    error_messages = {
        'unique': "Questo nome utente esiste già",
        'invalid': 'La mail inserita non è valida'
    }
    username = forms.CharField(label=("Username(*)"), error_messages=error_messages)
    first_name = forms.CharField(label="Nome", required=False)
    last_name = forms.CharField(label="Cognome", required=False)
    email = forms.EmailField(label="Indirizzo Email(*)", error_messages=error_messages)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        alloweddomains=['.com','.it','.org']
        email = self.cleaned_data.get('email')
        for i in alloweddomains:
            if email.endswith(i):
                return email
        raise forms.ValidationError("Il dominio della mail deve essere .com, .it o .org")

class EditProfile(forms.ModelForm):                                                                                     #Form per modifica dati profilo (solo la qualifica, per l'immagine c'è un form diverso)

    class Meta:
        model = Profile
        fields = ['qualification']

class EditPassword(forms.ModelForm):                                                                                    #Form per modifica password
    password = forms.CharField(label=("Nuova Password(*)"), widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['password']

    def save(self, commit=True):                                                                                        #Specifica come salvare la password
        user = super(forms.ModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class EditImage(forms.ModelForm):                                                                                       #Permette di modificare l'immagine

    class Meta:
        model = Profile
        fields=['image']

class MessageForm(forms.Form):                                                                                          #Mostra l'area di testo per messaggi
    message = forms.CharField(label='Messaggio',widget=forms.Textarea(attrs={'rows':10, 'cols':80,'placeholder':'Scrivi qui il tuo messaggio'}))

class CreateForm(forms.ModelForm):                                                                                      #Form per creare un nuovo item
    description=forms.CharField(label="Descrizione dell'oggetto",widget=forms.Textarea(attrs={'rows':10, 'cols':58}))

    class Meta:
        model=Item
        fields=['name','description','school_level','subject','image','file','price']

class EditItem(forms.ModelForm):                                                                                        #Form per modificare un oggetto
    description = forms.CharField(label="Descrizione dell'oggetto", widget=forms.Textarea(attrs={'rows': 10, 'cols': 58}))

    class Meta:
        model = Item
        fields = ['name', 'description', 'school_level', 'subject', 'image', 'file', 'price']


