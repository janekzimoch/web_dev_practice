from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from .models import User
from .models import Listing


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })

def my_listings(request):
    """ The same as index() however listis only your listings """
    listings = []
    user = str(request.user)
    for l in Listing.objects.all():
        if user == l.username:
            listings.append(l)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })

def delete_listing(request, id):
    Listing.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse("index"))

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add_listing(request):
    if request.method == 'POST':
        listing = Listing(
            username = request.user,
            title = request.POST["title"],
            description = request.POST["description"],
            bid = request.POST["bid"],
            img_url = request.POST["img_url"],
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/add_listing.html")
