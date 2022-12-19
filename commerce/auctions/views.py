from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from .models import User
from .models import Listing
from .models import Watchlist
from .models import Category

def _apply_category(request, listings):
    if request.method == 'POST' and request.POST['category'] != 'All':
        print(request.POST.get('listings'))
        print('123')
        sel_cat = request.POST['category']
        list_ = Category.objects.filter(category=sel_cat).values_list('listing', flat=True)
        listings = listings.filter(id__in=list_)
    else:
        sel_cat = 'All'
        listings = listings.all()
    return listings, sel_cat

def index(request):
    categories = Category.objects.all()
    # print(request.context.listings)
    listings = Listing.objects.all()
    listings, sel_cat = _apply_category(request, listings)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "sel_cat": sel_cat,
        "view_type": 'index',
        "categories": categories,
    })

def my_listings(request):
    """ The same as index() however listis only your listings """
    user = str(request.user)
    categories = Category.objects.all()
    listings = Listing.objects.filter(username=user)
    print(listings)
    listings, sel_cat = _apply_category(request, listings)
    print(listings)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "sel_cat": sel_cat,
        "view_type": 'my_listings',
        "categories": categories,
    })

def my_biddings(request):
    listings = []
    biddings = request.user.my_biddings.all()
    for listing in biddings:
        if str(listing.username) != str(listing.bidder):
            listings.append(listing)
    listings, sel_cat = _apply_category(request, listings)
    categories = Category.objects.all()        
    return render(request, "auctions/index.html", {
        "listings": listings,
        "sel_cat": sel_cat,
        "view_type": 'my_biddings',
        "categories": categories,
    })

def my_watchlist(request):
    listings = []
    watched_listings_ids = request.user.watched_listings.all().values_list('listing', flat=True)
    listings = Listing.objects.filter(id__in=watched_listings_ids)
    print(listings)
    listings, sel_cat = _apply_category(request, listings)
    print(listings)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "sel_cat": sel_cat,
        "view_type": 'my_watchlist',
        "categories": categories,
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
    categories = listing.listings_categories.all()
    print(listing)
    print(categories)
    is_in_watchlist_bool = _is_in_watchlist(request, id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "min_bid": listing.bid + 0.01,
        "is_in_watchlist": is_in_watchlist_bool,
        "categories": categories,
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
            bidder = request.user
          # note we need to initiate as owner (even thou he is not a bidder), because we can't set a default to anything meanigful.
        )
        listing.save()
        print(request.POST["categories"])
        print(request.POST["categories"].split(', '))
        for cat in request.POST["categories"].split(', '):
            category = Category(
                listing = listing,
                category = cat
            )
            category.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/add_listing.html")
