from os import fsdecode
from xml.dom.minidom import Document
from searchindex.buildindex import index
from searchindex.preprocessing import preprocess_text
import re
from collections import defaultdict
from math import log10
from searchengine.models import Document
def run_ranked_search(query):
    results = defaultdict(float)

    query_preproc = preprocess_text(query)
    
    for term in query_preproc:
        if term in index:
            for doc_id in index[term]:
                
                tf = len(index[term][doc_id])
                df = index[term].doc_freq
                if (tf != 0) and (df != 0):
                    w = (1 + log10(tf)) * log10(index.doc_count / df)

                results[doc_id] += w
    return sorted(results, key=results.get, reverse=True)[:50]
    

def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
 
    # return string
    return str1

def run_query(query):

    match = "#(\d+)\((\w+), (\w+)\)"
    frstprt = []
    scndprt = []
    spl = query.split()
    
    if ' AND NOT ' in query:
        frstprt, scndprt = query.split('AND NOT')
        frstprt = preprocess_text(frstprt)[0]
        scndprt = preprocess_text(scndprt)[0]
        frstprt = index[frstprt]
        scndprt = index[scndprt]  
        result = [i for i in frstprt if i not in scndprt]
        return result

    elif ' AND ' in query:
        frstprt, scndprt = query.split('AND')
        frstprt = preprocess_text(frstprt)[0]
        scndprt = preprocess_text(scndprt)[0]
        frstprt = index[frstprt]
        scndprt = index[scndprt]  
        print("LOG, AND", frstprt, scndprt)
        result = [i for i in frstprt if i in scndprt]
        return result
    
    

    elif " OR NOT " in query:
        word1, word2 = query.split("OR NOT")
        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]

        results1 = index[word1]
        results2 = index[word2]

        results1_ids = []
        for i in results1:
            results1_ids.append(i)

        notresult2 = []
        # for i in range(1, index.doc_count + 1):
        for i in Document.objects.values_list('doc_id')[:50]:
            # The doc ids in the index are strings 
            # but range gives us integers
            i = str(i[0])
            if i not in results2:
                notresult2.append(i)   
        
        results1_ids = [i for i in notresult2 if i not in results1_ids]
        return results1_ids


    elif 'OR' in query:
        i = 0
        while i < len(spl):
            if spl[i] == "OR":
                i += 1
                break
            frstprt.append(spl[i])
            i += 1
        while i < len(spl):

            if spl[i] == "OR":
                i += 1
                break
            scndprt.append(spl[i])
            i += 1
        
        frstprt = listToString(frstprt)
        frstprt = preprocess_text(frstprt)[0]
        scndprt = listToString(scndprt)
        scndprt = preprocess_text(scndprt)[0]  
        res1 = index[frstprt]
        res2 = index[scndprt]
        res1.update(res2)
        
        return res1
    
    elif query.startswith('"') and query.endswith('"'):
        word1,word2 = query.split(" ")

        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]

        results = set()
        res1 = index[word1]

        for id in res1:
            pos1 = index[word1][id]
            pos2 = index[word2][id]
            locResults = [i for i in pos1 if i + 1 in pos2]
            if locResults:
                results.add(id)
        return results

    elif re.match(match, query):
        
        m = re.match(match, query)
        num = int(m.group(1))
        word1 = m.group(2)
        word2 = m.group(3)
        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]
        
        result = set()
        res1 = index[word1]
        
        for id in res1:
            cur = 0
            while cur <= num:
                pos1 = index[word1][id]
                pos2 = index[word2][id]
                locResults = [i for i in pos1 if (i + cur) in pos2]
                if locResults:
                    result.add(id)
                cur += 1
            cur = 0
            while cur <= num:
                pos1 = index[word1][id]
                pos2 = index[word2][id]
                locResults = [i for i in pos1 if (i - cur) in pos2]
                if locResults:
                    result.add(id)
                cur += 1
        return result
    else:
        return run_ranked_search(query) 

