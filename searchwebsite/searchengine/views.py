from django.shortcuts import render
from django.views import generic
from searchindex.query import run_query

# Create your views here.

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"

    context_object_name = "searchresults"

    def get_queryset(self):
        query = self.request.GET['query']
        return run_query(query)



        #Build the index by calling the build_index function (you need to import it from build_index.py)