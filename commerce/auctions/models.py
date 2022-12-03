from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # a watchlist of suctions - add ids

    # ids of auctions user is bidding and how much is he bidding
    pass

class Auction(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    bid = models.IntegerField(default=0)
    bidder = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    # img = models.ImageField()  # may require a python liblary



    # history of bids - or at least the latest bid value

    # names of people bidding
    # image of an item - by defult could go to some placeholder ("no image  provided")
    # name of the item
    # category fo the item
    # description of the item
    # comments for the acution


class Bid():
    # bid value
    # person makign bid
    pass

class Comments():
    # comment content
    # comment author
    pass