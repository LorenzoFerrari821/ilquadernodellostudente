from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, DecisionForm, SignupForm, ProfileForm, EditUser, EditPassword, EditProfile, EditImage, \
    MessageForm, CreateForm, EditItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Profile
from catalog.models import HaveItem, Item, ReviewsObject
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from decimal import Decimal


def signup(request):  # Gestisce la registrazione
    user = request.user
    if request.method == 'POST':  # L'utente ha inserito i dati
        sf = SignupForm(request.POST)  # Form per i dati del modello User
        pf = ProfileForm(request.POST, request.FILES)  # Form per i dati del modello Profile
        if sf.is_valid() and pf.is_valid():
            user = sf.save()  # Salva l'utente nel db e lo ritorna
            profile = pf.save(commit=False)  # Salva il profilo ma non lo inserisce nel db
            profile.user = user  # Imposta manualmente l'user
            profile.save()  # Ora salva nel db
            username = sf.cleaned_data.get('username')
            password = sf.cleaned_data.get('password1')
            logout(request)  # Logout preventivo se utente già connesso
            user = authenticate(username=username, password=password)
            login(request, user)
            msg = "Complimenti, ti sei registrato su Ilquadernodellostudente. Clicca su questo bottone per tornare alla home."
            return render(request, 'signup-form.html', {'user': user, 'msg_success': msg})
        else:
            return render(request, 'signup-form.html',
                          {'user': user, 'sf': sf, 'pf': pf})  # Ci sono degli errori, rimostriamo i form con gli errori
    else:  # Prima invocazione della pagina, mostriamo i form vuoti
        sf = SignupForm()
        pf = ProfileForm()
        return render(request, 'signup-form.html', {'sf': sf, 'pf': pf, 'user': user})


def login_view(request):  # Mostra il form di login
    user = request.user
    if request.method == 'GET':  # Prima invocazione della pagina, mostriamo il form vuoto
        form = LoginForm()
        return render(request, "login-form.html", {'form': form, 'user': user})
    else:  # L'utente ha immesso i dati
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,
                                password=password)  # Ritorna un utente registrato se credenziali giuste
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home:Home'))
                else:  # Utente bloccato
                    msg = "L'account è stato disabilitato dall'amministrazione."
                return render(request, 'login-form.html', {'msg_warning': msg, 'user': user})
            else:  # Dati errati
                msg = "Il nome utente e/o la password sono errati. Clicca su questo bottone per riprovare"
                return render(request, 'login-form.html', {'msg_fail': msg, 'user': user})
        else:
            return render(request, 'login-form.html',
                          {'form': form, 'user': user})  # Ci sono degli errori, rimostriamo il form con gli errori


@login_required()
def logout_view(request):  # Pagina di logout
    user = request.user
    if request.method == 'GET':  # Prima invocazione della pagina, mostriamo il form vuoto
        form = DecisionForm()
        return render(request, "logout-form.html", {'form': form, 'user': user})
    else:  # Processiamo la decisione
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data['decision']
            if decision == 'Y':
                logout(request)
                return redirect(reverse('home:Home'))
            else:
                return redirect(reverse('users:Profile', kwargs={'user_id': user.id}))


@login_required()
def profile(request, user_id):  # Mostra il profilo utente
    user = request.user
    if user_id == '' or int(
            user_id) == user.id:  # Se l'utente visualizza il suo profilo mostriamo i bottoni per editare i dati
        profile = Profile.objects.get(user=user)
        return render(request, "profile.html", {'user': user, 'profile': profile})
    else:  # Altrimenti non li mostriamo, ma mostriamo un pannello per messaggi
        user_visited = get_object_or_404(User, pk=user_id)  # Ricaviamo il profilo visitato, se esiste
        profile = Profile.objects.get(user=user_visited)
        if request.method == 'GET':  # Pagina appena invocata, mostriamo il form per i messaggi vuoto
            form = MessageForm()
            return render(request, "profile.html",
                          {'user': user, 'user_visited': user_visited, 'profile': profile, 'form': form})
        else:  # L'utente ha spedito un messaggio
            form = MessageForm(request.POST)
            if form.is_valid():  # Inviamo una mail all'utente
                msg = form.cleaned_data['message']
                subject = "Messaggio dall'utente:" + user.username
                body = "L'utente " + user.username + " ti ha inviato il seguente messaggio:\n" + msg + "\nSe vuoi continuare a parlare con questo utente puoi " \
                                                                                                       "inviargli una mail all'indirizzo: " + user.email
                email = EmailMessage(subject, body, to=[user_visited.email])  # Impostiamo oggetto, corpo e destinatario
                email.send()
                msg_success = "Il tuo messaggio è stato inviato all'utente"
                return render(request, "profile.html",
                              {'user': user, 'user_visited': user_visited, 'profile': profile, 'form': form,
                               'msg_success': msg_success})


@login_required()
def editdata(request):  # Modifica i dati personali (user e profile)
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':  # L'utente ha modificato i dati
        eu = EditUser(request.POST, instance=user)
        ep = EditProfile(request.POST, instance=profile)
        if eu.is_valid() and ep.is_valid():  # Se il form è valido salviamo i dati immessi
            user = eu.save()
            ep.save()
            msg = "Le modifiche sono state apportate con successo.Clicca qui per tornare l tuo profilo"
            return render(request, 'edit-data.html', {'user': user, 'msg_success': msg})
        else:
            return render(request, 'edit-data.html', {'user': user, 'eu': eu, 'ep': ep})
    else:  # Prima invocazione della pagina, mostriamo i form con i dati attuali
        eu = EditUser(instance=user)
        ep = EditProfile(instance=profile)
        return render(request, 'edit-data.html', {'eu': eu, 'ep': ep, 'user': user})


@login_required()
def editimage(request):  # Permette di modificare l'immagine
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':  # L'utente ha caricato una nuova immagine
        ei = EditImage(request.POST, request.FILES, instance=profile)
        if ei.is_valid():  # Salviamo la nuova immagine
            ei.save()
            msg = "Le modifiche sono state apportate con successo. Clicca qui per tornare al tuo profilo"
            return render(request, 'edit-data.html', {'user': user, 'msg_success': msg})
        else:  # L'utente ha caricato una immagine non valida
            return render(request, 'edit-data.html', {'user': user, 'ei': ei})
    else:
        ei = EditImage(instance=profile)  # Prima invocazione della pagina, mostriamo i form con i dati attuali
        return render(request, 'edit-data.html', {'ei': ei, 'user': user})


@login_required()
def editpassword(request):  # Permette di cambiare la password
    user = request.user
    if request.method == 'POST':  # L'utente ha inserito una nuova password
        epw = EditPassword(request.POST, instance=user)
        if epw.is_valid():
            epw.save()  # L'user viene sloggato automaticamente da django, rifacciamo il login
            username = user.username
            password = user.password
            user = authenticate(username=username, password=password)
            login(request, user)
            msg = "Le modifiche sono state apportate con successo.Clicca qui per tornare al tuo profilo"
            return render(request, 'edit-data.html', {'user': user, 'msg_success': msg})
        else:  # Errori nel form
            return render(request, 'edit-data.html', {'user': user, 'epw': epw})
    else:
        epw = EditPassword(instance=user)
        return render(request, 'edit-data.html', {'epw': epw, 'user': user})


@login_required()
def purchaselist(request):  # Lista degli oggetti comprati dall'utente
    user = request.user
    profile = Profile.objects.get(user=user)
    n_reviews = []  # Lista che contiene, per ogni oggetto, il numero di voti ricevuti
    vote_list = []  # Lista che contiene il voto di ogni oggetto
    purchased_item = HaveItem.objects.get_or_create(profile=profile)[
        0].itemspurchased.all()  # Lista degli oggetti comprati dall'utente
    for item in purchased_item:
        n_reviews.append(ReviewsObject.objects.filter(
            reviewed_object__name=item.name).count())  # Per ogni oggetto ricaviamo il numero di recensioni
        vote_list.append(round(item.vote * 2) / 2)
    reviewed_object = ReviewsObject.objects.get_or_create(profile=profile)[
        0].reviewed_object.all()  # Lista oggetti recensiti dall'utente
    return render(request, "itemspurchasedlist.html",
                  {'purchased_item': purchased_item, 'reviewed_object': reviewed_object, 'user': user,
                   'reviews': n_reviews[::-1], 'vote_list': vote_list[::-1]})


@login_required()
def create(request):  # Permette di creare una nuova inserzione
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'GET':
        form = CreateForm()
        return render(request, 'createitem.html', {'form': form, 'user': user})
    else:
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)  # Salva l'oggetto e lo ritorna
            item.vendor = profile  # Imposta l'utente proprietario
            item.save()  # Salva l'oggetto nel db
            msg = "Inserzione creata con successo! Clicca su questo bottone per tornare al tuo profilo"
            return render(request, 'createitem.html', {'user': user, 'msg_success': msg})
        else:
            return render(request, 'createitem.html', {'user': user, 'form': form})


@login_required()
def selectitem(request):  # Mostra tutti gli oggetti su cui è possibile eseguire una azione
    user = request.user
    profile = Profile.objects.get(user=user)
    items = Item.objects.filter(vendor=profile)  # Ottiene tutti gli oggetti venduti dall'utente
    n_reviews = []  # Lista che contiene, per ogni oggetto, il numero di voti ricevuti
    vote_list = []  # Lista che contiene il voto di ogni oggetto
    for item in items:
        n_reviews.append(ReviewsObject.objects.filter(reviewed_object__name=item.name).count())
        vote_list.append(round(item.vote * 2) / 2)
    return render(request, 'selectitem.html',
                  {'user': user, 'items': items, "reviews": n_reviews[::-1], 'vote_list': vote_list[::-1]})


@login_required()
def deleteitem(request, item_id):  # Permette di eliminare un oggetto dalla vendita
    user = request.user
    profile = Profile.objects.get(user=user)
    item = Item.objects.get(id=item_id)
    if request.method == 'GET':
        form = DecisionForm()
        return render(request, "deleteitem.html", {'form': form, 'user': user})
    else:
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data['decision']
            if decision == 'Y':  # L'utente vuole eliminare l'oggetto
                item.vendor = None  # Slega l'oggetto dall'utente
                item.is_visible = False  # L'oggetto non è più visibile nel catalogo,ma può essere ancora scaricato da chi lo ha già comprato
                item.save()
                msg = "Oggetto eliminato. Clicca su questo bottone per tornare al tuo profilo"
                return render(request, "deleteitem.html", {'form': form, 'user': user, 'msg_success': msg})
            else:
                return redirect(reverse('users:Profile', kwargs={'profile_id': profile.id}))


@login_required()
def edititem(request, item_id):  # Permette di modificare i dati degli oggetti in vendita
    user = request.user
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = EditItem(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            msg = "Le modifiche sono state apportate con successo.Clicca qui per tornare al tuo profilo"
            return render(request, 'edititem.html', {'user': user, 'msg_success': msg})
        else:
            return render(request, 'edititem.html', {'form': form, 'user': user})
    else:
        form = EditItem(instance=item)
        return render(request, 'edititem.html', {'form': form, 'user': user})


@login_required()
def review(request, item_id):  # Permette di lasciare un voto per gli oggetti acquistati
    user = request.user
    profile = Profile.objects.get(user=user)
    item = Item.objects.get(id=item_id)
    purchased_item = HaveItem.objects.get_or_create(profile=profile)[
        0].itemspurchased.all()  # Lista degli oggetti posseduti dall'utente
    reviewed_objects = ReviewsObject.objects.get_or_create(profile=profile)[
        0].reviewed_object.all()  # Lista oggetti recensiti dall'utente
    if (item not in purchased_item):  # L'utente accede a questa pagina grazie alla barra di ricerca nel browser
        msg = "Non puoi recensire questo oggetto perchè non lo hai ancora comprato! Clicca su questo bottone per tornare alla home"
        return render(request, 'review.html', {'msg': msg, 'user': user})
    elif (item in reviewed_objects):
        msg = "Hai già recensito questo oggetto! Clicca su questo bottone per tornare alla home"
        return render(request, 'review.html', {'msg': msg, 'user': user})
    if request.method == 'GET':
        return render(request, 'review.html', {'user': user, 'item': item})
    else:
        vote = Decimal(request.POST.get('rating'))  # Raccogliamo il voto
        n_reviews = (ReviewsObject.objects.filter(
            reviewed_object__name=item.name).count())  # Otteniamo il numero di recensioni dell'oggetto
        tot_vote = item.vote * n_reviews  # Calcoliamo il voto totale (approssimato) precedente (media*numero_review)
        n_reviews += 1
        vote = (tot_vote + vote) / n_reviews  # Calcoliamo la nuova media sommando il nuovo voto e una nuova recensione
        item.vote = vote
        item.save()  # Salviamo
        reviewed_objects = ReviewsObject.objects.get(profile=profile)
        reviewed_objects.reviewed_object.add(
            item)  # Aggiungiamo l'oggetto alla lista degli oggeti recensiti dall'utente
        reviewed_objects.save()
        return redirect(reverse('users:Purchaselist'))
