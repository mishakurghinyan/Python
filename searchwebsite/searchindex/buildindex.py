from collections import defaultdict
from searchindex.preprocessing import preprocess_text
import xml.etree.ElementTree as ET
import sys


class TermDocuments(defaultdict):
    def __init__(self):
        super().__init__(list)


    @property
    def doc_freq(self):
        return len(self)

class Index(defaultdict):
    def __init__(self):
        super().__init__(TermDocuments)

        self.doc_count = 0

def build_index():
    print('Buiolding index..')
    index = Index()
    with open ('searchindex/datasets/chess.xml') as f:
        for _, elem in ET.iterparse(f):
            if elem.tag == "row":
                docId = elem.attrib["Id"]
                text = elem.attrib["Body"].strip()
                preprocessed = preprocess_text(text)
                index.doc_count += 1
                for pos, i in enumerate(preprocessed):
                    index[i][docId].append(pos)
        print("done")
    return index

# Print the contents of the index
def build_and_print():
    index = build_index()
    index_print = [""]
    index_print.append(f"doc_count: {index.doc_count}")
    for term in sorted(index):
        index_print.append(f"{term}: {index[term].doc_freq}")
        for doc in index[term]:
            index_print.append(f"\t{doc}: {','.join([str(x) for x in sorted(index[term][doc])])}")
    return '\n'.join(index_print)

index = []
if 'runserver' in sys.argv:
    index = build_index()