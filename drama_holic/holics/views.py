from django.shortcuts import render
from django.http import HttpResponse 
from .models import dramas, user_drama_watching_status
from .models import animes, user_anime_watching_status
from .models import mangas, user_manga_watching_status
from .models import movies, user_movie_data
from datetime import date , datetime

import requests
from traceback import print_exc



# Create your views here.
def home(request) :
    return  render(request, "holics/home.html")



def add(request):
    return render(request, "holics/add.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "mangas": mangas.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all()
    })


def showList(request):
        
    d = dramas.objects.all()
    for drama in d:
        for w in drama.drama_watchstat.all():
            now = datetime.now()
            today = now.date()
            if w.next_ep_release_date != None and w.next_ep_release_date < today:
                title = drama.title
                base = "https://www.episodate.com/api"
                url = f"{base}/search"
                
                try:
                    response = requests.get(
                        url,
                        params={"q":title},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        id = data["tv_shows"][0]["id"]
                        url = f"{base}/show-details"  
                        tv_show = data["tv_shows"][0]
                        title = tv_show["name"]
                        status = tv_show["status"]
                        thumbnail_img = tv_show["image_thumbnail_path"]
                        print(thumbnail_img)
                        
                        season = 1
                            
                        response = requests.get(
                            url,
                            params={"q":id},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            show_details = response.json()
                            episodes = show_details["tvShow"]["episodes"]
                            tv_shoe =  show_details["tvShow"]
                            max_season  = drama.max_season
                            next_ep_release_date = None
                            last_released_ep = None
                            
                            if tv_shoe["status"] == "Running":
                                for ep in episodes:
                                    if ep["season"] > max_season:
                                        max_season = ep["season"]
                                
                                for ep in episodes:
                                    if ep["season"] == max_season:
                                        date = ep["air_date"]
                                        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                        ep_date = date.date()
                                        if ep_date > date.today().date():
                                            next_ep_release_date = ep_date
                                            next_ep_no = ep["episode"]
                                            last_released_ep = next_ep_no - 1
                                            break
                            if next_ep_release_date != None and last_released_ep != None:
                                w.next_ep_release_date = next_ep_release_date
                                w.last_released_ep = last_released_ep
                                w.save()
                        else:
                            print(response.status_code)
                except Exception as e:
                    print(e)
                    print_exc()
            
        
    return render(request, "holics/library.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "mangas": mangas.objects.all(),
        "movies": movies.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all(),
        "watch_movie_status" : user_movie_data.objects.all()
    })
    

def add_movies(request):
    if request.method == "POST":
        movie_title = request.POST.get("movie")
        watch_status_input = request.POST.get("watch_status")
        
        status_map = {
            "1": "Completed",
            "2": "Plan to watch",
            "3": "Dropped",
            "Ongoing": "Ongoing"
        }
        watch_status = status_map.get(watch_status_input, watch_status_input)
        
        like = True if request.POST.get("fav") else False

        API_KEY = 'bb8bca8b23c3cd367e4427c2e163e971'
        BASE_URL = "https://api.themoviedb.org/3"

        headers = {
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }

        params = {
            "api_key": API_KEY,
            "query": movie_title
        }

        try:
            response = requests.get(f"{BASE_URL}/search/movie", headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and data.get("results"):
                    first_movie = data["results"][0]
                    title = first_movie.get("title")
                    poster = first_movie.get("poster_path")
                    release_date = first_movie["release_date"]
                    if title:
                        movie = movies(title=title, thumbnail_img=poster, release_date = release_date)
                        movie.save()
                        watch_status = user_movie_data(movies=movie, watch_status=watch_status, like=like)
                        watch_status.save()
        except Exception as e:
            print(e)
            print_exc()

    return render(request, "holics/library.html", {
        "dramas" : dramas.objects.all(),
        "animes": animes.objects.all(),
        "mangas": mangas.objects.all(),
        "watch_manga_status" : user_manga_watching_status.objects.all(),
        "watch_drama_status": user_drama_watching_status.objects.all(),
        "watch_anime_status" : user_anime_watching_status.objects.all(),
        "movies": movies.objects.all()
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
    
 
 
def add_drama(request):
    if request.method == "POST":
        
        drama_name = request.POST.get("drama")
        last_watched_ep = request.POST.get("no_ep")
        season = request.POST.get("season")
        
        base = "https://www.episodate.com/api"
        url = f"{base}/search"
        
        try:
            response = requests.get(
                url,
                params={"q":drama_name},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                id = data["tv_shows"][0]["id"]
                url = f"{base}/show-details"  
                tv_show = data["tv_shows"][0]
                title = tv_show["name"]
                status = tv_show["status"]
                thumbnail_img = tv_show["image_thumbnail_path"]
                print(thumbnail_img)
                
                season = 1
                    
                response = requests.get(
                    url,
                    params={"q":id},
                    timeout=10
                )
                
                if response.status_code == 200:
                    show_details = response.json()
                    episodes = show_details["tvShow"]["episodes"]
                    max_season = 0
                    if tv_show["status"] == "Running":
                        for ep in episodes:
                            if ep["season"] == season:
                                date = ep["air_date"]
                                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                                ep_date = date.date()
                                if ep_date > date.today().date():
                                    next_ep_release_date = ep_date
                                    next_ep_no = ep["episode"]
                                    last_released_ep = next_ep_no - 1
                                    break
                            if ep["season"] > int(season):
                                last_released_ep = 0
                                for ep in episodes:
                                    if ep["season"] == season:
                                        if last_released_ep < ep["episode"]:
                                            last_released_ep = ep["episode"]
                                break
                            
                                                                
                        for ep in episodes:
                            if ep["season"] > max_season:
                                max_season = ep["season"]
                                            
                    elif tv_show["status"] == "Ended":
                        last_released_ep = 0
                        next_ep_release_date = None
                        for ep in episodes:
                            if ep["season"] > max_season:
                                max_season = ep["season"]
                        for ep in episodes:
                            if ep["season"] == max_season:
                                if last_released_ep < ep["episode"]:
                                    last_released_ep = ep["episode"]
                                
                                    
                    if status == "Ended":
                        total_ep = last_released_ep
                    else:
                        total_ep = len(episodes)
                        
                        
                    d = dramas(title = title, thumbnail_img = thumbnail_img,max_season = max_season )
                    d.save()
                    
                    w = user_drama_watching_status(drama = d, season = season, last_watched_ep = last_watched_ep, last_released_ep = last_released_ep,next_ep_release_date = next_ep_release_date)
                    w.save()
                                
                else:
                    print(response.status_code)
                                        
        except Exception as e:
            print(e)
            print_exc()
   
    return render(request, "holics/library.html", {
    "dramas" : dramas.objects.all(),
    "animes": animes.objects.all(),
    "mangas": mangas.objects.all(),
    "watch_manga_status" : user_manga_watching_status.objects.all(),
    "watch_drama_status": user_drama_watching_status.objects.all(),
    "watch_anime_status" : user_anime_watching_status.objects.all(),
    })
    