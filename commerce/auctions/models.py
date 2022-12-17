from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # a watchlist of suctions - add ids
    # ids of auctions user is bidding and how much is he bidding
    pass

class Listing(models.Model):
    username = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_biddings')
    bid = models.FloatField(default=0)  # ensure this is a float
    img_url = models.CharField(max_length=512)

    def __str__(self):
        return f"Owner: {self.username}; item: {self.title}, descirption: {self.description}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watching_users')




class Comments():
    # comment content
    # comment author
    pass