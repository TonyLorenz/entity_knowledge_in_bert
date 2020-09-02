import pandas as pd
import base64
import pickle
import os
import sys
import json
import re

data_info_all = pd.read_csv("data_info.csv", names= ['text', 'id', 'url', 'title'])
data_info = data_info_all
#data_info = data_info.head(700000)
#print(data_info)
#print(data_info['url'])

data_links_list = os.listdir(path='data_links')
#data_links_list = ['data_links8.csv', 'data_links9.csv']
new_df = pd.DataFrame(columns= ['text', 'id', 'url', 'title', 'internal_links'])


for file in data_links_list:
 data_links = pd.read_csv("../data_links/" + file)
# print(data_info['url'])

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
   #print(current_url_list)


 #print(sorted_links)
 #print(current_url)  

 data_links = pd.DataFrame(data=sorted_urls, columns=['url'])


 data_links['internal_links'] = sorted_links

 #print(data_links)


 data_links_dict = dict(zip(data_links['url'], data_links['internal_links']))
 #print(data_links_dict)

 h = 0
 for item in data_info['url']:
   if item in data_links_dict.keys():
     new_df.append({'text': data_info['text'][h], 'id':data_info['id'][h], 'url': data_info['url'][h], 'title': data_info['title'][h], 'internal_links': data_links_dict[item]}, ignore_index= True)
     data_info.drop(h, inplace = True)
     h +=1
 data_info.reset_index()

 #data_info['internal_links'] = found_url_list
 #data_info = data_info[['id', 'url', 'title', 'text', 'internal_links']]
 print(len(data_info))
 new_df.to_csv(f"dbpedia_data.csv", index= False, header= True)
