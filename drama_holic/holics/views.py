from django.shortcuts import render
from django.http import HttpResponse 
from .models import dramas, user_drama_watching_status
from .models import animes, user_anime_watching_status
from .models import mangas, user_manga_watching_status
import requests
from traceback import print_exc





# Create your views here.
def home(request) :
    return  render(request, "holics/home.html")

def add(request):
    return render(request, "holics/api.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "mangas": mangas.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all()
    })

def showList(request):
        
    return render(request, "holics/library.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "mangas": mangas.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all()
    })


def fetch_pop_movies(request):

    if request.method == "POST":
        movie = request.POST.get('drama')
        no_ep = request.POST.get('no_ep')
        
        API_KEY = 'bb8bca8b23c3cd367e4427c2e163e971'
        BASE_URL = "https://api.themoviedb.org/3"

        headers = {
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }



        params = {
            "api_key": API_KEY,
            "query": movie
        }
        response = ""
        url = f'{BASE_URL}/search/movie'
        while response == "":
            try :
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    if response.json():
                        data = response.json()
                        if data["results"][0]:
                            first_movie = data["results"][0]
                            title = first_movie["title"]
                            overview = first_movie["overview"]
                            poster = first_movie["poster_path"]
                            if movie != None and movie != "":
                                d = dramas(title = title, total_ep = no_ep,  thumbnail_img = poster)
                                d.save()
                        else:
                            return HttpResponse("No drama found")
                    else:
                        return HttpResponse("No json data")
                else:
                    print(response.status_code)
                    print("error fetching data")
            except Exception as e:
                print ('type is:', e.__class__.__name__)
                print_exc()


        
    return render(request, "holics/api.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "manga": mangas.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all(),
    })
    
    
def add_anime(request):
    if request.method == 'POST': 
        anime_title = request.POST.get("anime")
        season = request.POST.get("season_no")
        curr_ep = request.POST.get("curr_ep")
        anilist_root = "https://graphql.anilist.co"

                
        query = """
        query ($search: String) {

        Media(search: $search, type: ANIME) {

            bannerImage

            coverImage {
            extraLarge
            large
            medium
            color
            }

            nextAiringEpisode {
            episode
            airingAt
            timeUntilAiring
            }

            airingSchedule {
            nodes {
                episode
                airingAt
            }
            }

            title {
            native
            english
            }

            status
            popularity
            episodes
        }
        }
        """
        variables = {
            "search": anime_title
        }   
        response = ""
        while response == "":
            try :
                response = requests.post(
                anilist_root,
                json={
                    "query" : query,
                    "variables": variables
                    }
                )
                
                if  response.json():
                    data = response.json()
                    if data["data"]["Media"]:
                        media = data["data"]["Media"]
                        if media["title"]:
                            title = media["title"]["english"]
                            original_title = media["title"]["native"]
                        else:
                            title = "unknown"
                        
                                
                        next_airing = media["nextAiringEpisode"]
                        if next_airing:
                            last_released_ep = next_airing["episode"] - 1
                            next_ep_release_date = next_airing["airingAt"]
                        else:
                            last_released_ep = media["episodes"]
                            next_ep_release_date = None
                            
                        if media["episodes"]:
                            total_ep = media["episodes"]
                        elif next_airing:
                            total_ep = None
                            
                        status = media["status"]
                        thumbnail_img = media["coverImage"]["extraLarge"]
                                    
    

                        # adding anime to animes list
                        anime = animes(title = title, original_title = original_title, total_ep = total_ep, status = status, thumbnail_img = thumbnail_img)
                        anime.save()

                        watch_status = user_anime_watching_status(anime = anime, last_released_ep = last_released_ep, next_ep_release_date = next_ep_release_date,last_watched_ep = curr_ep)   
                        watch_status.save()            
                    else:
                        print("no anime found aaaaaaa")
                else:
                    print("no data")          
                
            except Exception as e:
                print_exc()
        
        
        
    return render(request, "holics/library.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "mangas": mangas.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all()
    })
    
    
    
    
def add_manga(request):
    if request.method == 'POST': 
        manga_title = request.POST.get("manga")
        season = request.POST.get("season_no")
        curr_ep = request.POST.get("curr_ep")
        anilist_root = "https://graphql.anilist.co"

                
        query = """
        query ($search: String) {

        Media(search: $search, type: MANGA) {

            bannerImage

            coverImage {
            extraLarge
            large
            medium
            color
            }

            nextAiringEpisode {
            episode
            airingAt
            timeUntilAiring
            }

            airingSchedule {
            nodes {
                episode
                airingAt
            }
            }

            title {
            native
            english
            }

            status
            popularity
            episodes
        }
        }
        """
        variables = {
            "search": manga_title
        }   
        response = ""
        while response == "":
            try :
                response = requests.post(
                anilist_root,
                json={
                    "query" : query,
                    "variables": variables
                    }
                )
                
                
                if  response.json():
                    data = response.json()
                    if data["data"]["Media"]:
                        media = data["data"]["Media"]
                        if media["title"]:
                            title = media["title"]["english"]
                            original_title = media["title"]["native"]
                        else:
                            title = "unknown"
                        
                                
                        next_airing = media["nextAiringEpisode"]
                        if next_airing:
                            last_released_ep = next_airing["episode"] - 1
                            next_ep_release_date = next_airing["airingAt"]
                        else:
                            last_released_ep = media["episodes"]
                            next_ep_release_date = None
                        total_ep = None   
                        if media["episodes"]:
                            total_ep = media["episodes"]
                        
                        status = media["status"]
                        thumbnail_img = media["coverImage"]["extraLarge"]
                                    
    

                        # adding anime to animes list
                        manga = mangas(title = title, original_title = original_title, total_ep = total_ep, status = status, thumbnail_img = thumbnail_img)
                        manga.save()
                            

                        watch_status = user_manga_watching_status(manga = manga, last_released_ep = last_released_ep, next_ep_release_date = next_ep_release_date,last_watched_ep = curr_ep)   
                        watch_status.save()            
                    else:
                        print("no manga found aaaaaaa")
                else:
                    print("no data")          
                
            except Exception as e:
                print("exception", e)
                print_exc()
        
        
                
    return render(request, "holics/library.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "mangas": mangas.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all()
    })