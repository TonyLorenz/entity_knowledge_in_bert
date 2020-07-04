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
            shutil.move("/content/entity_knowledge_in_bert/bert_entity/preprocessing/dbpedia_dummy.xlsx", f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/dbpedia_dummy.xlsx")
        else:
            shutil.move("/dbpedia_all.xlsx", f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}dbpedia_dummy.xlsx/")

        self.log("Download finished ")
