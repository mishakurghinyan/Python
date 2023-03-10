from xml.dom.minidom import Document
from django.shortcuts import render
from django.views import generic
from searchindex.query import run_query
from searchengine.models import Document
from searchindex.preprocessing import preprocess_text
from searchindex.query_completion import complete_query
from django.http import JsonResponse
from searchindex.spellcheck import correct_spelling
import time
# Create your views here.

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"
    paginate_by = 10
    context_object_name = "searchresults"
    numResults = 0
    ms = 0


    def listToString(s):
 
        # initialize an empty string
        str1 = ""
 
        # traverse in the string
        for ele in s:
            str1 += ele
 
        # return string
        return str1

    def get_queryset(self):
        query = self.request.GET['query']
        start = time.time()
        results = run_query(query)
        self.ms = format(time.time() - start, '.3f')
        self.numResults = len(results)
        docs = [Document.objects.get(doc_id = doc_id) for doc_id in results]
        result = []
        for doc in docs:
            result.append(format_doc(doc))       
        return result
    
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['numResults'] = self.numResults
        context['ms'] = self.ms
        context['correction'] = correct_spelling(self.request.GET['query'])
        return context

def summ(text, query):
    sentences = []
    sentences = text.split('. ')
    preprocessed_query = preprocess_text(query)
    doc_result = []
    for sentence in sentences:
        preproc_sentence = preprocess_text(sentence)

        for word in preprocessed_query:
            if word in preproc_sentence:
                if sentence not in doc_result:
                    doc_result.append(f'{sentence}.')
                break
    return doc_result
def format_doc(doc):
    return f'<h5><a href = "https://chess.stackexchange.com/questions/{doc.doc_id}">{doc.title}</a></h5> <span class="query">{doc.text}</span>'

def complete(request):
    query = request.GET['q']
    completions = complete_query(query)
    return JsonResponse(completions, safe=False)

