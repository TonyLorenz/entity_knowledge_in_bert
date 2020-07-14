import os
import subprocess
from typing import Dict
import shutil

from pipeline_job import PipelineJob


class DownloadWikiDump(PipelineJob):
    """
    Move the downloaded files to the right folder.
    """

    def __init__(self, preprocess_jobs: Dict[str, PipelineJob], opts):
        super().__init__(
            requires=[],
            provides=[f"data/versions/{opts.data_version_name}/downloads/{opts.wiki_lang_version}/"],
            preprocess_jobs=preprocess_jobs,
            opts=opts,
        )

    def _run(self):

        self.log(f"Downloading {self.opts.wiki_lang_version}")
        if self.opts.download_data_only_dummy:
            #os.mkdir(f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/")
            #shutil.move("/content/entity_knowledge_in_bert/bert_entity/preprocessing/dbpedia_dummy_excelfile.xlsx", f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/dbpedia_dummy_excelfile.xlsx")
            os.mkdir(f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/")
            data_info = pd.read_excel('dbpedia_dummy_excelfile.xlsx')
            data_info = data[['id', 'url', 'title', 'text']]
            data_info = data_info.sort_values('url')
            data_info = data_info.reset_index(drop=True)
            data_links = pd.read_excel('dbpedia_dummy.xlsx')
            data_links = data_links.sort_values('url')
            data_links = data_links.reset_index(drop=True)
            links_list_all = []
            i = 0
            j = 0
            
            links_str = ''
            while i < len(data_links):
                if data_links['url'][i] == data_info['url'][j]:
                    links_str = links_str + (data_links['internal_links'][i]) +', '
                    i+=1
                    if i == len(data_links)-1:
                        links_list_all.append(links_str)
                else:
                    links_list_all.append(links_str)
                    links_str = ''
                    j+=1
            data_info['internal_links'] = links_list_all
            data_info.to_csv(f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}dbpedia_dummy.csv/", index= False, header= True)
        else:
            os.mkdir(f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/")
            data_info = pd.read_csv('info_query_out')
            data_info = data[['id', 'url', 'title', 'text']]
            data_info = data_info.sort_values('url')
            data_info = data_info.reset_index(drop=True)
            data_links = pd.read_csv('links_query_out')
            data_links = data_links.sort_values('url')
            data_links = data_links.reset_index(drop=True)
            links_list_all = []
            i = 0
            j = 0
            
            links_str = ''
            while i < len(data_links):
                if data_links['url'][i] == data_info['url'][j]:
                    links_str = links_str + (data_links['internal_links'][i]) +', '
                    i+=1
                    if i == len(data_links)-1:
                        links_list_all.append(links_str)
                else:
                    links_list_all.append(links_str)
                    links_str = ''
                    j+=1
            data_info['internal_links'] = links_list_all
            data_info.to_csv(f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}dbpedia_all.csv/", index= False, header= True)

        self.log("Download finished ")
