from django.shortcuts import render, reverse, redirect
from users.models import Profile
from catalog.models import Item, HaveItem, ReviewsObject
from checkout.models import Cart
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse


@login_required()
def additem(request, item_id):  # aggiunge l'item selezionato al carrello
    user = request.user
    profile = Profile.objects.get(user=user)
    item = Item.objects.get(pk=item_id)
    purchaseditems = HaveItem.objects.get_or_create(profile=profile)[
        0].itemspurchased.all()  # Lista degli oggetti posseduti dall'utente
    n_reviews = (ReviewsObject.objects.filter(
        reviewed_object__name=item.name).count())  # Lista, per ogni oggetto salva il numero di recensioni
    vote = round(item.vote * 2) / 2
    cart = Cart.objects.get_or_create(owner=profile)[0]  # Prende il carrello dell'utente o lo crea
    itemsincart = cart.get_cart_items()  # Ottiene tutti gli item nel carrello
    for entry in itemsincart:
        if entry == item:  # L'oggetto è già nel carrello
            msg = "Questo oggetto è già nel tuo carrello!"
            return render(request, 'detail.html', {'user': user, 'item': item, 'reviews': n_reviews, 'vote_list': vote,
                                                   'msg_already_in_cart': msg})
    if item in purchaseditems:  # Oggetto già comprato dall'utente
        msg = "Hai già comprato questo oggetto in passato!"
        return render(request, 'detail.html',
                      {'user': user, 'item': item, 'msg_already_purchased': msg, 'reviews': n_reviews,
                       'vote_list': vote})
    if item.vendor == profile:
        msg = "Non puoi comprare un oggetto messo in vendita da te."
        return render(request, 'detail.html',
                      {'user': user, 'item': item, 'msg_already_purchased': msg, 'reviews': n_reviews,
                       'vote_list': vote})
    cart.items.add(item)  # Aggiunge l'oggetto al carrello
    cart.save()
    msg = "Oggetto aggiunto al carrello!"
    return render(request, 'detail.html',
                  {'user': user, 'item': item, 'msg_success': msg, 'reviews': n_reviews, 'vote_list': vote})


@login_required()
def deleteitem(request, item_id):  # Elimina oggetti dal carrello
    user = request.user
    profile = Profile.objects.get(user=user)
    cart=Cart.objects.get(owner=profile)
    item=Item.objects.get(id=item_id)
    cart.items.remove(item)
    return redirect(reverse('checkout:Cart'))


@login_required()
def cart(request):  # Mostra il carrello
    n_reviews = []  # Lista, per ogni oggetto salva il numero di recensioni
    vote_list = []  # Lista che contiene il voto di ogni oggetto
    user = request.user
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.get_or_create(owner=profile)[0]
    if cart.get_cart_items().count() == 0:
        return render(request, 'cart.html',
                      {'user': user})  # Non passiamo il carrello al template, significa che è vuoto
    for item in cart.get_cart_items():
        n_reviews.append(ReviewsObject.objects.filter(reviewed_object__name=item.name).count())
        vote_list.append(round(item.vote * 2) / 2)
    return render(request, 'cart.html',
                  {'cart': cart, 'user': user, 'reviews': n_reviews[::-1], 'vote_list': vote_list[::-1]})


@login_required()
def placeorder(request, cart_id):  # Processa l'ordine e rimanda ad una pagina di download.Invia una mail di conferma
    user = request.user
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.get(id=cart_id)
    body = "Ti ringraziamo per il tuo acquisto. Hai acquistato i seguenti oggetti:\n"
    item_list = HaveItem.objects.get_or_create(profile=profile)[0]  # Lista degli oggetti posseduti dall'utente
    for item in cart.get_cart_items():  # Aggiungiamo gli oggetti alla lista di oggetti posseduti dall'utente
        item_list.itemspurchased.add(item)
        body += item.name + " al prezzo di " + str(item.price) + " euro.\n"
    profile.save()
    cart.items.clear()  # Svuotiamo il carrello
    cart.save()
    body += "Ricorda che è possibile scaricare i file acquistati dal tuo profilo utente!" \
            "Grazie," \
            "Lo Staff"
    subject = "Riepilogo acquisto"
    email = EmailMessage(subject, body, to=[user.email])  # Mandiamo una mail di riepilogo all'utente
    email.send()
    return render(request, 'purchasesuccess.html', {'user': user})


@login_required()
def payment(request, cart_id):
    # Questa views fornisce una pagina in cui specificare il metodo di pagamento ed elabora il pagamento grazie all'utilizzo componenti accessori esterni a django.
    # Funzione soltanto simulata, all'invocazione di questa view si viene rediretti alla view placeorder.
    return redirect(reverse('checkout:Placeorder', kwargs={'cart_id': cart_id}))


@login_required()
def retrieve(request, item_id):  # Permette all'utente di scaricare il file richiesto
    item = Item.objects.get(pk=item_id)
    path = item.file.path
    name = item.name
    name += ".pdf"
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename=' + name  # Modifichiamo gli header fields, trattarli come dizionari
        response['Content-Type'] = 'application/pdf; charset=utf-16'
        return response
