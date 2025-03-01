import base64
import glob
import io
import json
import multiprocessing
import os
import pickle
import sys
import re
import pandas as pd
from collections import Counter
from typing import Dict

from misc import normalize_wiki_entity
from pipeline_job import PipelineJob


class Wikiextractor(PipelineJob):
    """
    Run DBpedia extractor on dbpedia data.
    """
    def __init__(self, preprocess_jobs: Dict[str, PipelineJob], opts):
        super().__init__(
            requires=[
                f"data/versions/{opts.data_version_name}/downloads/{opts.wiki_lang_version}/",
            ],
            provides=[
                f"data/versions/{opts.data_version_name}/wikiextractor_out/{opts.wiki_lang_version}/",
            ],
            preprocess_jobs=preprocess_jobs,
            opts=opts,
        )

    def _run(self):

        self.log("Run WikiExtractor")
        counter = 1

        # python wikiextractor-wikimentions/WikiExtractor.py --json --filter_disambig_pages --processes $WIKI_EXTRACTOR_NR_PROCESSES --collect_links $DOWNLOADS_DIR/$WIKI_RAW/$WIKI_FILE -o $WIKI_EXTRACTOR_OUTDIR/$WIKI_FILE
    
        for input_file in glob.glob(
            f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/*"
        ):
                  

 #   Find the internal links in abstract of each respective article. Remove "uri-structure", "_" and other chars that are
 #   not part of the words that can be found in the abstracts before. Then encode it with pickle to put it in right shape.

              data = pd.read_csv(input_file)
              data = data.to_dict(orient = 'records')
              #  print(data)
              i=0

              #  print(data[i]['internal links'])
              new_file = f"db_file_{counter}.json"
              os.makedirs(f"data/versions/{self.opts.data_version_name}/wikiextractor_out/{self.opts.wiki_lang_version}")
              f = open(f"data/versions/{self.opts.data_version_name}/wikiextractor_out/{self.opts.wiki_lang_version}/{new_file}","w")

              while i<len(data):
                data[i]['title'] = str(data[i]['title'])
                internal_links_new = []
                offset_list = []
                item = data[i]['internal_links'].split(', ')
                for word in item:
                    word = re.sub('http://dbpedia.org/resource/*/', "", word)
                    word = word.replace('_',' ')
                    word = word.replace('Category:',' ')
                    word = word.replace(', ', '')
                    word = word.replace(',', '')
                    word = word.replace('\'', '')
                    word = word.replace('\'', '')
                    word = re.sub('\(*\)', "", word)
                    word = re.sub("\d", "", word)
                    word = re.sub("\(.*\)", "", word)
                    if word != "":
                        internal_links_new.append((word, word))
                    x = data[i]['text'].find(word)
                    if x>-1:
                        offset_list.append((x, x + len(word)))
                    else:
                        offset_list.append(x)
                #print(offset_list)
                #print(internal_links_new)
                data[i]['internal_links'] = dict(zip(offset_list, internal_links_new))
                if -1 in data[i]['internal_links'].keys():
                    del data[i]['internal_links'][-1]
                print(data[i]['internal_links'])    
                data[i]['internal_links'] = dict(sorted(data[i]['internal_links'].items()))
                data[i]['internal_links'] = base64.b64encode(pickle.dumps(data[i]['internal_links'])).decode('utf-8')
                print(data[i]['internal_links'])
                out_str = json.dumps(data[i])
                f.write(out_str)
                if i < len(data)-1:
                    f.write('\n')
                i+=1
              #    base64.b64encode(pickle.dumps(self.internal_links)).decode('utf-8')

              #    print(data)
              f.close()

        self.log("WikiExtractor finished")
