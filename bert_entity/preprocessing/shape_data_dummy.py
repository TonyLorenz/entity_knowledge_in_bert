import pandas as pd
import base64
import pickle
import os
import sys
import json
import re


#Concatenates data_info and data_links.

  
data_info = pd.read_csv("data_info.csv", names= ['text', 'id', 'url'])
#data_info = data_info.head(x)
print(data_info)
i =0
while i< len(data_info['id']):
  item = str(data_info['id'][i])
  item = re.sub("\^\^http://www.w3.org/2001/XMLSchema#integer", "", item)
  data_info['id'][i] = item
  i+=1

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

#data_info = data_info.sort_values('url')
#data_info = data_info.reset_index(drop=True)
print(data_info['url'])
data_links = pd.read_csv('data_links.csv')
#data_links = data_links.head(y)
#data_links = data_links.sort_values('url')
#data_links = data_links.reset_index(drop=True)
print(data_links)


# Merge all internal links for each respective article in a list.

  
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


print(sorted_links)
print(current_url)  

data_links = pd.DataFrame(data=sorted_urls, columns=['url'])
data_links['internal_links'] = sorted_links

print(data_links)


data_links_dict = dict(zip(data_links['url'], data_links['internal_links']))
print(data_links_dict)



# If internal links found for a datapoint in data_info: append the list, otherwise append an empty list.

  
found_url_list = []
h = 0
for item in data_info['url']:
  if item in data_links_dict.keys():
    found_url_list.append(data_links_dict[item])
  else:
    found_url_list.append([])

data_info['internal_links'] = found_url_list
data_info = data_info[['id', 'url', 'title', 'text', 'internal_links']]
print(data_info)

data_info.to_csv("dbpedia_data.csv", index= False, header= True)
