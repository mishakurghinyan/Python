from xml.dom.minidom import Document
from django.shortcuts import render
from django.views import generic
from searchindex.query import run_query
from searchengine.models import Document

# Create your views here.

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"

    context_object_name = "searchresults"

    def get_queryset(self):
        query = self.request.GET['query']
        results = run_query(query)
        docs = [Document.objects.get(doc_id = doc_id).text for doc_id in results]
        return docs or ['No Results']
    