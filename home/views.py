from django.shortcuts import render




def home(request):                                                                                                      #Mostra la pagina iniziale
    user = request.user
    return render(request, "home.html", { 'user': user})
