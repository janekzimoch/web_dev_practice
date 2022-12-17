from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from .models import User
from .models import Listing
from .models import Watchlist


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

def my_biddings(request):
    listings = []
    biddings = request.user.my_biddings.all()
    for listing in biddings:
        print(listing.username)
        print(listing.bidder)
        if str(listing.username) != str(listing.bidder):
            listings.append(listing)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })

def my_watchlist(request):
    listings = []
    watched_listings = request.user.watched_listings.all()
    for w in watched_listings:
        listing = Listing.objects.get(id=w.listing.id)
        listings.append(listing)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })

def _is_in_watchlist(request, id):
    try:
        listing = Listing.objects.get(id=id)
        watched_listing = request.user.watched_listings.get(listing=listing)
    except Watchlist.DoesNotExist:
        watched_listing = None
    if watched_listing is None:
        return False
    else:
        return True

def remove_from_watchlist(request, id):
    watched_listings = request.user.watched_listings.all()
    listing = Listing.objects.get(id=id)
    watched_listing = watched_listings.get(listing=listing)
    watched_listing.delete()
    return HttpResponseRedirect(reverse("index"))

def add_to_watchlist(request, id):
    user = request.user
    listing = Listing.objects.get(id=id)
    watching_event = Watchlist(user=user, listing=listing)
    watching_event.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def listing(request, id):
    listing = Listing.objects.get(id=id)
    is_in_watchlist_bool = _is_in_watchlist(request, id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "min_bid": listing.bid + 0.01,
        "is_in_watchlist": is_in_watchlist_bool
    })

def bid(request, id):
    bid = request.POST['bid']
    listing = Listing.objects.get(id=id)
    listing.bidder = request.user
    listing.bid = bid
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

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
            img_url = request.POST["img_url"],
            bid = request.POST["bid"],
            bidder = request.user  # note we need to initiate as owner (even thou he is not a bidder), because we can't set a default to anything meanigful.
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/add_listing.html")
