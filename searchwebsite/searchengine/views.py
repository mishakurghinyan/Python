from xml.dom.minidom import Document
from django.shortcuts import render
from django.views import generic
from searchindex.query import run_query
from searchengine.models import Document
from searchindex.preprocessing import preprocess_text
# Create your views here.

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"
    paginate_by = 10
    context_object_name = "searchresults"



    def get_queryset(self):
        query = self.request.GET['query']
        results = run_query(query)
        docs = [Document.objects.get(doc_id = doc_id) for doc_id in results]
        result = []
        for doc in docs:
            result.append(format_doc(doc, query))       
        return result

def summ(text, query):
    sentences = []
    sentences = text.split('. ')
    preprocessed_query = preprocess_text(query)
    doc_result = ""
    for sentence in sentences:
        preproc_sentence = preprocess_text(sentence)

        for word in preprocessed_query:
            if word in preproc_sentence:
                doc_result += f'{sentence}.'
                break
    return doc_result
def format_doc(doc, query):
    return f'<h5><a href = "https://chess.stackexchange.com/questions/{doc.doc_id}">{doc.title}</a></h5>'