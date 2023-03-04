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
        docs = [Document.objects.get(doc_id = doc_id).text for doc_id in results]
        result = []
        if len(docs) > 2:
            for doc in docs:
                sentences = []
                sentences = doc.split('.')
                preprocessed_query = preprocess_text(query)
                doc_result = ""
                for sentence in sentences:
                    # Preprocess the sentence
                    preproc_sentence = preprocess_text(sentence)

                    for word in preprocessed_query:
                        if word in preproc_sentence:
                            doc_result += f'{sentence}.'

                result.append(doc_result)
                        
                       
                    
        return docs
    