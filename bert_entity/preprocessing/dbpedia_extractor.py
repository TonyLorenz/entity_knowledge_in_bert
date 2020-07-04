import base64
import glob
import io
import json
import multiprocessing
import os
import pickle
import sys
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
              data = pd.read_excel(input_file)
              data = data.to_dict(orient = 'records')
              #  print(data)
              i=0

              #  print(data[i]['internal links'])


              while i<len(data):
                internal_links_new = []
                offset_list = []
                item = data[i]['internal links'].split(', ')
                for word in item:
                  word = word.replace('_',' ')
                  internal_links_new.append((word, word))
            #      print(word)
                  x = data[i]['text'].find(word)
                  if x>0:
                    offset_list.append((x, x + len(word)))
                  else:
                    offset_list.append(x)
                data[i]['internal links'] = dict(zip(offset_list, internal_links_new))
                del data[i]['internal links'][-1]
            #    data[i]['internal links'] = sorted(data[i]['internal links'].items())
                data[i]['internal links'] = base64.b64encode(pickle.dumps(data[i]['internal links'])).decode('utf-8')
                print(data[i]['internal links'])
                i+=1
              #    base64.b64encode(pickle.dumps(self.internal_links)).decode('utf-8')

              #    print(data)
              new_file = f"db_file_{counter}.txt"
              os.makedirs(f"data/versions/{self.opts.data_version_name}/wikiextractor_out/{self.opts.wiki_lang_version}")
              f = open(f"data/versions/{self.opts.data_version_name}/wikiextractor_out/{self.opts.wiki_lang_version}/{new_file}","w")
              f.write( str(data))
              f.close()

        self.log("WikiExtractor finished")
