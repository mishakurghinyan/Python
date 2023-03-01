from django.shortcuts import render
from django.views import generic
from searchindex.preprocessing import preprocess_text

# Create your views here.

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"

    context_object_name = "searchresults"

    def get_queryset(self):
        query = self.request.GET['query']

        return preprocess_text(query)