import pandas as pd
import base64
import pickle
import os
import sys
import json
import re

data_info_all = pd.read_csv("data_info.csv", names= ['text', 'id', 'url'])
data_info = data_info_all
#data_info = data_info.head(700000)
#print(data_info)
#print(data_info['url'])

# add column "title" to data, use url for extract the titles
names = []
j=0
while j< len(data_info['id']):
  names.append(str(re.sub("http://dbpedia.org/resource/", "", data_info['url'][j])))
  j+=1

data_info['title'] = names

# Because some of the titles were numbers, the following preprocessing steps couldn't work with those articles. We filter them out here.

i = 0
for item in data_info["title"]:
  if item is float:
    data_info["title"][i] = str(data_info["title"][i])
    i+=1
  if item is int:
    data_info["title"][i] = str(data_info["title"][i])
    i+=1
  i+=1


data_links_list = os.listdir(path='data_links')
new_df = pd.DataFrame(columns= ['text', 'id', 'url', 'title', 'internal_links'])

# merge all links from one respective article in one list
  
for file in data_links_list:
 data_links = pd.read_csv("../data_links/" + file)
 sorted_links = []
 sorted_urls= []
 k = 0
 while k<len(data_links['url']):
   current_url_list = []
   current_url = data_links['url'][k]
   while data_links['url'][k] == current_url:
     current_url_list.append(data_links['internal_links'][k])
     k+=1
     if k > len(data_links['url'])-1:
       break
   sorted_links.append(current_url_list)
   sorted_urls.append(current_url)  

 data_links = pd.DataFrame(data=sorted_urls, columns=['url'])
 data_links['internal_links'] = sorted_links

 #print(data_links)

 data_links_dict = dict(zip(data_links['url'], data_links['internal_links']))
 #print(data_links_dict)

 # sort the links lists with their respective datapoints to data in info_data, drop all info_data that has been found, add the found one to new_df
 h = 0
 for item in data_info['url']:
   if item in data_links_dict.keys():
     new_df.append({'text': data_info['text'][h], 'id':data_info['id'][h], 'url': data_info['url'][h], 'title': data_info['title'][h], 'internal_links': data_links_dict[item]}, ignore_index= True)
     data_info.drop(h, inplace = True)
     h +=1
 data_info.reset_index()

new_df.to_csv(f"dbpedia_data.csv", index= False, header= True)
