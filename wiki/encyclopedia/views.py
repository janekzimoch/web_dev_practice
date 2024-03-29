from django.shortcuts import render
from django.http import HttpResponse
import random

from . import util


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def render_page(request, page):
    page_md = util.get_entry(page)
    if page_md is not None:
        return render(request, "encyclopedia/page.html", {
            "title": page,
            "page": page_md
        })
    else:
        return render(request, "encyclopedia/page_not_found.html")


def search(request):
    searched_entry = request.GET['page']
    entries = util.list_entries()
    releted_entries = [entry for entry in entries if searched_entry in entry]
    if searched_entry in entries:
        page_md = util.get_entry(searched_entry)
        return render(request, "encyclopedia/page.html", {
            "title": searched_entry,
            "page": page_md
        })
    elif len(releted_entries) > 0:
        return render(request, "encyclopedia/related_pages.html", {
            "releted_entries": releted_entries
        })
    else:
        return render(request, "encyclopedia/page_not_found.html")

def create_new_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        existing_entries = util.list_entries()
        if title in existing_entries:
            return render(request, "encyclopedia/error.html")
        # save page
        util.save_entry(title, body)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": body
        })
    else:
        return render(request, "encyclopedia/create_new_page.html")

def edit_page(request, title):
    page = util.get_entry(title)
    if request.method == 'POST':
        page = request.POST['body']
        util.save_entry(title, page)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": page
        })
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "page": page
        })


def random_page(request):
    entries = util.list_entries()
    page_ind = random.randint(0,len(entries))-1
    print(page_ind)
    title = entries[page_ind]
    body = util.get_entry(title)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": body
    })


