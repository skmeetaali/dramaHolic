from django.shortcuts import render
from django.http import HttpResponse 

dramas = ["Weak hero", "Weak hero 2", "All of us are dear", "Train to Busan"]
manhuas = ["Change you story", "Jinx", "Heaven official's blessings"]
animes = ["Solo leveling", "Demon slayer"]

# Create your views here.
def home(request) :
    return  render(request, "holics/home.html")


def showList(request):
    if request.method == "POST":
        drama_name = request.POST.get('drama')
        if drama_name != None and drama_name != "" and drama_name not in dramas:
            dramas.append(drama_name)
        
        anime_name = request.POST.get('anime')
        if anime_name != None and anime_name != "":
            animes.append(anime_name)
        
        manhua_name = request.POST.get('manhua')
        if manhua_name != None and manhua_name != "":
            manhuas.append(manhua_name)
    
    return render(request, "holics/library.html", {
        "dramas" : dramas,
         "animes": animes  , 
         "manhuas": manhuas
    })
 
