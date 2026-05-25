from django.shortcuts import render, redirect
import difflib
import random
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, title):
    md= util.get_entry(title)
    if md is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    html=markdown2.markdown(md)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html
    })
def random_page(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No encyclopedia entries are available."
        })
    title = random.choice(entries)
    return redirect('entry', title=title)

def search(request):
    query=request.GET.get("q", "")
    entries=util.list_entries()
    if query in entries:
        return entry(request, query)
    else:
        matches=difflib.get_close_matches(query, entries)
        return entry(request, matches[0] if matches else query)
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title or not content:
            return render(request, "encyclopedia/new_page.html", {
                "error": "Title and content are required.",
                "title": title,
                "content": content
            })
        elif title in util.list_entries():
            return render(request, "encyclopedia/new_page.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })

        util.save_entry(title, content)
        return redirect('entry', title=title)

    return render(request, "encyclopedia/new_page.html")
def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        if not content:
            return render(request, "encyclopedia/edit_page.html", {
                "error": "Content is required.",
                "title": title,
                "content": content
            })

        util.save_entry(title, content)
        return redirect('entry', title=title)

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })