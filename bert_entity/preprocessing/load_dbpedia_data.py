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
            os.mkdir(f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/")
            shutil.move("/content/entity_knowledge_in_bert/bert_entity/preprocessing/dbpedia_dummy_excelfile.xlsx", f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/dbpedia_dummy_excelfile.xlsx")
        else:
            os.mkdir(f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/")
            shutil.move("/dbpedia_all.csv", f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}dbpedia_dummy.csv/")

        self.log("Download finished ")
