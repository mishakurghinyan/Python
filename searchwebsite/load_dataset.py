import sys
import os
import json
import xml.etree.ElementTree as ET

def load_dataset():
    if len(sys.argv) == 1:
        print("ERROR: need to specify a dataset")
        return
    
    dataset_name = sys.argv[1]
    dataset_path = f"searchindex/datasets/{dataset_name}.xml"
    fixture_folder = f"searchengine/fixtures"
    fixture_path = f"searchengine/fixtures/{dataset_name}.json"

    os.makedirs(fixture_folder, exist_ok=True)

    with open(dataset_path) as f:
        with open(fixture_path, 'wt') as fixture:
            idx = 1
            fixture.write("[")
            for _, elem in ET.iterparse(f):
                if elem.tag == "DOC":
                    doc_id = elem.find("DOCID").text
                    text = elem.find("TEXT").text.strip()
                    
                    if idx > 1:
                        fixture.write(",")

                    fixture_object = {
                        'model': 'searchengine.Document',
                        'pk': idx,
                        'fields': {
                            'doc_id': doc_id,
                            'text': text
                        }
                    }

                    fixture.write(json.dumps(fixture_object))
                    
                    idx += 1

            fixture.write("]")
    
    os.system("python manage.py flush --no-input")
    os.system(f"python manage.py loaddata {dataset_name}.json")
    

if __name__ == '__main__':
    load_dataset()