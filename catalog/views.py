from django.shortcuts import render, get_object_or_404  # scorciatoie per template e 404
from .models import Item, ReviewsObject
from users.models import Profile
from .forms import SearchForm
from checkout.models import Cart


def itemlist(request):  # mostra la lista degli oggetti
    user = request.user  # Utente loggato, lo passiamo al template per mostrare i bottoni corretti
    n_reviews = []  # Lista che contiene il numero di reviews per ogni oggetto
    vote_list = []  # Lista che contiene il voto di ogni oggetto
    item_list = Item.objects.filter(is_visible=True).order_by(
        'price')  # Lista di tutti gli oggetti nel catalogo ordinati per prezzo, eventualmente da filtrare
    if request.method == 'GET':  # Se la pagina viene invocata per la prima volta o dopo aver eseguito una ricerca con la barra di ricerca
        name = request.GET.get("q")
        if name:  # Se effettivamente è stata eseguita una ricerca
            item_list = item_list.filter(name__icontains=name)
        for item in item_list:
            n_reviews.append(ReviewsObject.objects.filter(
                reviewed_object__name=item.name).count())  # Per ogni oggetto ricaviamo il numero di recensioni
            vote_list.append(round(item.vote * 2) / 2)  # Portiamo il voto al più vicino valore utile (2.5,3,3.5.....))
        return render(request, "catalog.html",
                      {'item_list': item_list, 'user': user, 'reviews': n_reviews[::-1], 'vote_list': vote_list[::-1]})

    else:  # Richiesta fatta dal form(metodo post) nella pagina di ricerca avanzata
        form = SearchForm(request.POST)
        if form.is_valid():  # Ricaviamo i dati e filtriamo gli oggetti
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            school_level = form.cleaned_data['school_level']
            item_list = item_list.filter(name__icontains=name)
            item_list = item_list.filter(subject__icontains=subject)
            item_list = item_list.filter(school_level__icontains=school_level)
            for item in item_list:
                n_reviews.append(ReviewsObject.objects.filter(
                    reviewed_object__name=item.name).count())  # Per ogni oggetto ricaviamo il numero di recensioni
                vote_list.append(round(item.vote * 2) / 2)
        return render(request, "catalog.html",
                      {'item_list': item_list, 'user': user, 'reviews': n_reviews[::-1], 'vote_list': vote_list[::-1]})


def itemdetail(request, item_id):  # mostra la pagina di dettaglio di un preciso oggetto
    item = get_object_or_404(Item, pk=item_id, is_visible=True)
    user = request.user
    n_reviews = (ReviewsObject.objects.filter(reviewed_object__name=item.name).count())
    vote = round(item.vote * 2) / 2
    if user.is_authenticated:  # Se l'utente è loggato controlliamo che l'oggetto non skia già nel suo carrello
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.get_or_create(owner=profile)[0]  # Prende il carrello dell'utente o lo crea
        items = cart.get_cart_items()  # Ottiene tutti gli item nel carrello
        for entry in items:
            if entry == item:  # L'oggetto è già nel carrello
                msg = "Questo oggetto è già nel tuo carrello!"
                return render(request, 'detail.html',
                              {'user': user, 'item': item, 'reviews': n_reviews, 'vote_list': vote,
                               'msg_already_in_cart': msg})
    return render(request, "detail.html", {'item': item, 'user': user, 'reviews': n_reviews, 'vote_list': vote})


def search(request):  # Mostra il form della ricerca e lo spedisce alla wiew itemlist
    user = request.user
    if request.method == 'GET':
        form = SearchForm()
        return render(request, "search.html", {'form': form, 'user': user})
