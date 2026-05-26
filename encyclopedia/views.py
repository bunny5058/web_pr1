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
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect('index')

    entries = util.list_entries()

    # Exact match (case-insensitive) -> redirect to that entry's page
    for e in entries:
        if e.lower() == query.lower():
            return redirect('entry', title=e)

    # Substring (case-insensitive) matches -> show results page
    matches = [e for e in entries if query.lower() in e.lower()]
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "matches": matches
    })
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
        elif any(e.lower() == title.lower() for e in util.list_entries()):
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