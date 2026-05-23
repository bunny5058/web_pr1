from django.shortcuts import render
import difflib
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
def search(request):
    query=request.GET.get("q", "")
    entries=util.list_entries()
    if query in entries:
        return entry(request, query)
    else:
        matches=difflib.get_close_matches(query, entries)
        return entry(request, matches[0] if matches else query)
        