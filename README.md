# "Investigating Entity Knowledge in BERT with Simple Neural End-To-End Entity Linking" - _DBPedia Edition_

# Information

This project is based on Samuel Broscheit's project https://github.com/samuelbroscheit/entity_knowledge_in_bert. The aim was to exchang the database Wikipedia that he used with another database in order to build a pipeline for other databases. I this case I used DBPedia which is also based on Wikipedia.

Altered files:

- create_wiki_training_data.py
- create_integerized_wiki_training.py
- collect_mention_entity_counts.py

Added files

- get_links_data_from_ttl_links_file.py
- get_raw_info_data_from_query.py
- shape_data.py
- load_dbpedia_data.py
- dbpedia_extractor.py

Added files by superviser

- NeuralELwBERT

(Explenations in ### Preprocessing tasks)

# Process

The original model with Wikipedia has roughly three steps: (1) Downloading and extracting the data (Wikiextractor), (2) Preprocessing the data, (3) Training and Finetuning on the KB and the benchmark dataset. We have replaced step (1) and then continued stept (2) and (3) with our data.

This is what steps we took in downloading and preparing the data:

1. Downloading all datasets from DBpedia that we need
2. Using the java code in the *NeuralELwBERT* folder to query over "Info_data" so that we get (columns 'id', 'url', 'text') from all DBPedia articles and putting them into csv format with *get_raw_info_data_from_query.py*
3. Extracting all internal links with from page_links_en.ttl *get_links_data_from_ttl_links_file.py*
4. Adding "title" to the dataset, sorting all internal links according to their respective articles and putting them in a the lists in column "internal_links" with *shape_data.py*
5. Find internal links in abstracts of each respective article to create mentions and put data in exact shape that the Wikiextractor outputs with *dbpedia_extractor.py*
6. Attach data to the rest of the code with *load_dbpedia_data.py*

_Only_dummy_ --> we only run it with a dummy here because we set up the pipeline like this, to run over entire DBPedia data, we need to split the data

# Setup

```
git clone --recurse-submodules https://github.com/TonyLorenz/entity_knowledge_in_bert.git
```

**Step 1 & 2: Get Info_data: (columns 'id', 'url', 'text')**

Load data and set up querying steps

```
cd entity_knowledge_in_bert/java_code
mkdir input_files
cd input_files
wget --> http://downloads.dbpedia.org/2016-10/core-i18n/en/long_abstracts_en.ttl.bz2 http://downloads.dbpedia.org/2016-10/core-i18n/en/page_ids_en.ttl.bz2
bzip2 -d --> http://downloads.dbpedia.org/2016-10/core-i18n/en/long_abstracts_en.ttl.bz2 http://downloads.dbpedia.org/2016-10/core-i18n/en/page_ids_en.ttl.bz2
cd ..

mkdir query_in
mv query.txt query_in

```

Load data into the triple database and execute queries

```
cd ..
mkdir query_out
java - jar neuralbert_load_data.jar
java -jar neuralbert_execute_queries.jar

mv query_out/query_out ../bert_entity/preprocessing
cd ../bert_entity/preprocessing

```

Extract info data from query and put in csv shape with columns 'id', 'title', 'text'

```
python3 get_raw_info_data_from_query.py
```

**Step 1 & 3: Get Internal_links_data (columns 'id', 'internal_links')**


Download dbpedia data with page links

```
wget http://downloads.dbpedia.org/2016-10/core-i18n/en/page_links_en.ttl.bz2
bzip2 -d page_links_en.ttl.bz2

```
Extract the url's and internal links from ttl file and put in csv shape with columns 'id' 'internal_links'

```
python3 get_links_data_from_ttl_links_file.py
```

**Step 4: Shape data and merge info and internal_links**

run shape_data.py

```
python3 shape_data.py
```
--> now you have a dbpedia_data.csv file with columns 'id', 'url', 'title', 'text', 'internal_links'

--> Step 5 & 6 are integrated in the preprocessing of the orignal code


**Prepare running of original code**

Prepare files

```
cd entity_knowledge_in_bert
# git install requirements.txt
git submodule update --init
# Add paths to environment
source setup_paths
# Create directory
mkdir -p data/benchmarks/
# install pretrained BERT
mkdir tmp
cd tmp
wget http://resources.mpi-inf.mpg.de/yago-naga/aida/download/aida-yago2-dataset.zip
ls -l
unzip aida-yago2-dataset.zip
ls -l
# move benchmark dataset in aida-yago2-dataset folder
cp -r aida-yago2-dataset ../data/benchmarks/
cd ../data/benchmarks/aida-yago2-dataset
wget https://raw.githubusercontent.com/marcocor/bat-framework/master/src/main/resources/datasets/aida/AIDA-YAGO2-dataset-update.tsv
mv AIDA-YAGO2-dataset-update.tsv AIDA-YAGO2-dataset.tsv
cd ../../../
```


# Preprocessing & Running model


**Run preprocessing**
```
python3 bert_entity/preprocess_all.py --create_integerized_training_valid_size 20 --create_integerized_training_test_size 20 -c config/dummy__preprocess.yaml

```
**Run training on DBPedia dummy**
```
python3 bert_entity/train.py -c config/dummy__train_on_wiki.yaml
```

**Finetune on AIDA-CoNLL benchmark**
```
python3 bert_entity/train.py -c config/dummy__train_on_aida_conll.yaml
```

**Evaluate the best model on the AIDA-CoNLL benchmark**

```
python3 bert_entity/train.py -c config/dummy__train_on_aida_conll.yaml --eval_on_test_only True --resume_from_checkpoint data/checkpoints/dummy_aidaconll_00001/best_f1-0.pt
```



# Explenation of preprocessing tasks

Preprocessing consists of the following tasks (the respective code is in `bert_entity/preprocessing`):

- NeuralELwBERT
  - Program for querying DBPedia with sparql.
- get_links_data_from_ttl_links_file.py
  - Reads through all the lines in the links ttl file from DBPedia. Extracts only the url and the respective links and puts them into csv with columns 'url', 'internal_links'.
- get_raw_info_data_from_query.py
  - Reads through the lines of the extracted query with informationa and text, extracted from DBPedia and puts them into a csv file with columns 'id', 'url, 'text'.
- shape_data.py
  - Reads info_data and links_data. 
  - Extracts the names of the articles from the urls and brings info_data in the shape of 'id', 'url, 'title', 'text'.
  - Merges all links from respective articles into one array per article.
  - Merges and saves info_data and links_data into csv with columns 'id', 'url, 'title', 'text', 'internal_links'.
- load_dbpedia_data.py
  - Attaches the dbpedia_data.csv file to Broscheit's preprocessing code.
- dbpedia_extractor.py
  - Edits internal_links so that only the title of the resource is left. Finds those titles in text of respective article which are then the mentions.
  - Finds position of mention in text and brings them in tuple shape ((start position, end position), (title, mention)).
  - Replaces the contents of the 'internal_links' with the tuples and drop those that couldn't be found in the text.


- CreateRedirects
  - Create a dictionary containing redirects for Wikipedia page names [(*)](#footnote). The redirects are used for the Wikipedia mention extractions as well as for the AIDA-CONLL benchmark. 
  
      ```  
      "AccessibleComputing": "Computer_accessibility"
      ```
    
- CreateResolveToWikiNameDicts
    - Create a dictionary that map Freebase Ids and Wikipedia pages ids to Wikipedia page names [(*)](#footnote). The disambiguations are used to detect entity annotations in the AIDA-CONLL benchmark that have become incompatible for newer Wikipedia versions.

      ```  
      "/m/01009ly3": "Dysdera_ancora"
      ```

      ```  
      "10": "Computer_accessibility"
      ```

- CreateDisambiguationDict
    - Create a dictionary containing disambiguations for Wikipedia page names [(*)](#footnote). The disambiguations are used to detect entity annotations in
    the AIDA-CONLL benchmark that have become incompatble for newer Wikipedia
    versions.

      ```  
      "Alien": ["Alien_(law)", "Alien_(software)", ... ] 
      ```

- DownloadWikiDump
    - Download the current Wikipedia dump. Either download one file for a dummy / prototyping version. Set `download_data_only_dummy` to True for just one file, ootherwise download all files. Set `download_2017_enwiki` to True if not the latest dump should be retrieved but a 2017 dump like in the paper. 
    
- Wikiextractor
    - Run Wikiextractor on the Wikipedia dump and extract all the mentions from it.
    
- CollectMentionEntityCounts
    - Collect mention entity counts from the Wikiextractor files.

- PostProcessMentionEntityCounts
    - Create entity indexes that will later be used in the creation of the Wikipedia training data. First, based on the configuration key `num_most_freq_entities` the **top k most popular entities** are selected. Based on those, other mappings are created to only
    contain counts and priors concerning the top k popular entities. Later the top k popular entities will also restrict the training  data to only contain instances that contain popular entities.
    Also, if `add_missing_conll_entities` is set, the entity ids necessary for the AIDA-CONLL benchmark that are missing in the top k popular entities are added. This is to ensure that the evaluation measures are comparable to prior work. 
    
- CreateAIDACONLL
    - Read the AIDA-CONLL benchmark dataset in and merge it with the NER annotations. Requires you to provide `data/benchmarks/aida-yago2-dataset/AIDA-YAGO2-dataset.tsv`. Please make sure that you have the correct file with 6 columns: Token, Mention, Yago Name, Wiki Name, Wiki Id, Freebase Id. 
    
- CreateKeywordProcessor
    - Create a tri-based matcher to detect possible mentions of our known entities. We use this later to add autmatic annotations to the text. However, as we do not know the true entity for those mentions, they will have multiple labels, i.e. all entities from the p(e|m) prior.

- CreateWikiTrainingData
    - Create sequence labelling data. Tokenization is done with BertTokenizer. Tokens are either have a label when they have an associated Wikipedia link, or when they are in spans detected by the keyword matcher. Subsequently, we count the mentions in this data and create a discounted prior p(e|m) and the set of necessary Wikpedia articles, i.e. all the articles that contain links to the top k popular entities.

- CreateIntegerizedWikiTrainingData
    - Create overlapping chunks of the Wikipedia articles. Outputs are stored as Python lists with integer ids. Configured by `create_integerized_training_instance_text_length` 
    and `create_integerized_training_instance_text_overlap`.

        Each worker creates his own shard, i.e., the number of shards is determined by `create_integerized_training_num_workers`.

        Only saves a training instance (a chunk of a Wikipedia article) if at least one entity in that chunk has not been seen more than `create_integerized_training_max_entity_per_shard_count` times. This downsamples highly frequent entities. Has to be set in relation to `create_integerized_training_num_workers`
         and `num_most_freq_entities`. For the CONLL 2019 paper experiments the setting was

        ```
        create_integerized_training_max_entity_per_shard_count = 10
        create_integerized_training_num_workers = 50
        num_most_freq_entities = 500000
        ```
        
- CreateIntegerizedCONLLTrainingData
    - Create overlapping chunks of the benchmark articles. Outputs are stored as Python lists with integer ids. Configured by `create_integerized_training_instance_text_length` 
    and `create_integerized_training_instance_text_overlap`.

###### Footnote 
_Here we use an already extracted mapping provided by DBPedia that was created from a 2016 dump. Please note that in the experiments for the paper a Wikipedia dump from 2017 was used. The DbPedia dictionaries might not  be adequate for the latest wiki dumps._

# Options

### Available options for Preprocessing
 
 Preprocessing supports the following configurations: 


```  

  --debug                       Print debug messages  

   # General settings

  --wiki_lang_version           Wiki language version, e.g. enwiki

  --data_version_name           Data identifier/version; e.g. if you experiment with different 
                                preprocessing options you should use different names here to create 
                                new directories. 

  --num_most_freq_entities      Number of most frequent entities that should be collected from the
                                entity set collected from the Wikipedia dump

  --add_missing_conll_entities  Whether entities for the AIDA CONLL benchmark that are missing from
                                the most frequent entities collected from the Wikipedia dump should
                                be added to the entity vocabulary

  --uncased                     Should the input token dictionary be uncased



   # CollectMentionEntityCounts

  --collect_mention_entities_num_workers 
                                Number of worker for parallel processing of the Wikipedia dump to
                                collect mention entities.



   # CreateWikiTrainingData

  --create_training_data_num_workers 
                                Number of worker for parallel processing to create the sequence
                                tagging training data

  --create_training_data_num_entities_in_necessary_articles 
                                Threshold on the #entities in necessary articles (i.e. articles that 
                                contain entities in the most frequent entity vocabulary) that should 
                                be considered for training data
                                

   # CreateIntegerizedWikiTrainingData
                                
  --create_integerized_training_num_workers 
                                Number of worker for parallel processing to create the integerized 
                                sequence tagging training data, also determines the number of created
                                shards.
                                
  --create_integerized_training_instance_text_length 
                                Text length of the integerized training instances
                                
  --create_integerized_training_instance_text_overlap 
                                Overlap between integerized training instances

  --create_integerized_training_max_entity_per_shard_count 
                                Max count per entity in each shard. For each 
    
  --create_integerized_training_valid_size 
                                Sample size for validation data.

  --create_integerized_training_test_size 
                                Sample size for test data.


```  

### Available options for Training
 
 Training supports the following configurations: 

```
  --debug                               DEBUG

  --logdir                              LOGDIR; the output dir where checkpints and logfiles are stored

  --data_workers                        number of data workers to prepare training instances

  --data_version_name                   use the same identifier that was used for the same key in 
                                        preprocessing


  --device                              GPU device used for training
  --eval_device                         GPU device used for evaluation
  --out_device                          GPU device used to collect the most probable entities in the batch 

  --dataset                             'EDLDataset' for training on Wikipedia or 'CONLLEDLDataset' 
                                        for training on AIDA-CONLL

  --model                               Either 'Net' for training on Wikipedia or 'ConllNet' for 
                                        training on AIDA-CONLL

  --eval_on_test_only                   only run evaluation on test (requires --resume_from_checkpoint)

  --batch_size                          batch size in training
  --eval_batch_size                     batch size in evluation
  --accumulate_batch_gradients          accumulate gradients over this many batches

  --n_epochs                            max number of epochs
  --finetuning                          start finetuning after this many epochs
  --checkpoint_eval_steps               evaluate every this many epochs
  --checkpoint_save_steps               save a checkpoint every this many epochs
  --dont_save_checkpoints               dont_save_checkpoints               

  --sparse                              Use a sparse embedding layer

  --encoder_lr                          encoder learning rate
  --decoder_lr                          decoder learning rate
  --encoder_weight_decay                encoder weight decay
  --decoder_weight_decay                decoder weight decay
  --bert_dropout                        BERT_DROPOUT

  --label_size                          nr of entities considered in the label vector for each instance
  --topk_neg_examples                   TOPK_NEG_EXAMPLES
  --entity_embedding_size               entity_embedding_size               
  --project                             project entity embedding

  --resume_from_checkpoint              path of checkpoint to resume from 
  --resume_reset_epoch                  reset the epochs from the checkpoint for resuming (f.ex.
                                        training on AIDA-CONLL)
  --resume_optimizer_from_checkpoint    resume optimizer from checkpoint

  --eval_before_training                evluate once before training
  --data_path_conll                     path to the conll file that was create in data_version_name
  --exclude_parameter_names_regex       regex to exclude params from training, i.e. freeze them
```
