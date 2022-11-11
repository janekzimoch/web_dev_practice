from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def render_page(request, page):
    print(page)
    print(request.query)
    page_md = util.get_entry(page)
    if page_md is not None:
        return render(request, "encyclopedia/page.html", {
            "title": page,
            "page": page_md
        })
    else:
        return render(request, "encyclopedia/page_not_found.html")
