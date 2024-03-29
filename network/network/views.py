from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Post

from time import gmtime, strftime
import numpy as np
import json


def _sort_posts_by_time(posts):
    post_times = [post.time_published for post in posts]
    sorted_inds = np.argsort(post_times)[::-1].tolist()  # [::-1] for descending order
    sorted_posts = []
    for ind in sorted_inds:
        post = posts[ind]
        print(post)
        print(post.user)
        post['author'] = post.user
        post['num_likes'] = len(post.users_liked.all())
        print(post)
    return sorted_posts

def index(request):
    posts_per_page = 10
    posts = Post.objects.order_by('time_published')[::-1]

    # print([p.id for p in posts_srt])
    # context = {'posts': {}}
    # post_times = [post.time_published for post in posts]
    # sorted_inds = np.argsort(post_times)[::-1].tolist()  # [::-1] for descending order
    # # sorted_posts = _sort_posts_by_time(posts)
    # for ind in sorted_inds:
    #     post = posts[ind]
    #     context['posts'][post.id] = {'author': post.user, 
    #                                  'time_published': post.time_published,
    #                                  'text_body': post.text_body,
    #                                  'text_title': post.text_title,
    #                                  'num_likes': len(post.users_liked.all())}
    # print([id for id, k in context['posts'].items()])
    # paginator
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {'page_obj': page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def send_post(request,):
    if request.method == "POST":
        if request.POST['post_id'] != "-1":  # enter 
            post = Post.objects.get(id=request.POST['post_id'])
            post.text_body = request.POST["text_body"]
            post.text_title = request.POST["text_title"]
            post.save()
        else:
            time_published = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            # create a new entry to the database and persist it
            post = Post(
                user = request.user,
                text_body = request.POST["text_body"],
                text_title = request.POST["text_title"],
                time_published = time_published
            )
            post.save()
    return HttpResponseRedirect(reverse("index"))

def is_liked(data, post_id):
    new_user_like = User.objects.get(id = data['user_id'])
    post = Post.objects.get(id = post_id)        
    if new_user_like in post.users_liked.all():
        return True
    else:
        return False

def like_post_get(request, post_id, user_id):
    if request.method == "GET":
        # data = request.GET #json.loads(request.GET)  # Get method doesn't have a body, but i need user_id. So you will need to create a seperate view. 
        liked = is_liked({'user_id':user_id}, post_id)
        return JsonResponse({"liked": liked}, status=302)

def like_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(id = post_id)        
        liked = is_liked(data, post_id)
        new_user_like = User.objects.get(id = data['user_id'])
        if liked:
            post.users_liked.remove(new_user_like)
            post.num_likes -= 1
            post.save()
        else:
            post.users_liked.add(new_user_like)
            post.num_likes += 1
            post.save()
        # num_likes = len(post.users_liked.all())
        return JsonResponse({"num_likes": post.num_likes, "liked": not liked}, status=302)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


def get_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())


