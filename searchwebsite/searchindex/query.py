from searchindex.buildindex import index
from searchindex.preprocessing import preprocess_text


def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
 
    # return string
    return str1

def run_query(query):
    
    frstprt = []
    scndprt = []
    spl = query.split()
    if ' AND NOT ' in query:
        frstprt, scndprt = query.split(' AND NOT ')
        frstprt = preprocess_text(frstprt)[0]
        scndprt = preprocess_text(scndprt)[0]
        frstprt = index[frstprt]
        scndprt = index[scndprt]  
        result = [i for i in frstprt if i not in scndprt]
        if query:
            return result or ['Chka']
        else: 
            return ['Chka']

    elif ' AND ' in query:
        frstprt, scndprt = query.split(' AND ')
        frstprt = preprocess_text(frstprt)[0]
        scndprt = preprocess_text(scndprt)[0]
        frstprt = index[frstprt]
        scndprt = index[scndprt]  
        result = [i for i in frstprt if i in scndprt]
        if query:
            return (result) or ['Chka']
        else: 
            return ['Chka']
    
    

    elif " OR NOT " in query:
        word1, word2 = query.split(" OR NOT ")

        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]

        results1 = index[word1]
        results2 = index[word2]

        results1_ids = []
        for i in results1:
            results1_ids.append(i)

        notresult2 = []
        for i in range(1, index.doc_count + 1):
            # The doc ids in the index are strings 
            # but range gives us integers
            i = str(i)
            if i not in results2:
                notresult2.append(i)   
        
        
        for i in notresult2:
            if i not in results1_ids:
                results1_ids.append(i)
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
        
        if query:
            return (res1) or ['Chka']
        else: 
            return ['Chka']

    
