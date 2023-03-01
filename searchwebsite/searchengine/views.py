from django.shortcuts import render
from django.views import generic
from searchindex.preprocessing import preprocess_text
from searchindex.buildindex import build_and_print
from searchindex.buildindex import build_index

# Create your views here.

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"

    context_object_name = "searchresults"

    def get_queryset(self):
        query = self.request.GET['query']
        index = build_index()
        query = preprocess_text(query)

        return index[query[0]] or ["No results"]



        #Build the index by calling the build_index function (you need to import it from build_index.py)