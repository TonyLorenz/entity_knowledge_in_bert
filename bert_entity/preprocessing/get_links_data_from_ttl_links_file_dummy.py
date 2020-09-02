import re
import pandas as pd


# Read through page_links_en.ttl file that contains all internal links. Then puts URI and internal link into individual strings.

  
fp = open('page_links_en.ttl', 'r')
print("fp = open('page_links_en.ttl', 'r') done")

line = fp.readline()
print("line = fp.readline() done")
cnt = 0
print("cnt = 0 done")

#url = []
links = []

while cnt<5000008:
  if cnt<8:
    line = fp.readline()
    print("cnt 8")
    cnt+=1
    
print("while done")
links_df = pd.DataFrame(links, columns=['internal_links'])
print("dataframe done")

print(links_df)

url = []

i =0


#Split and edit each line to get URI and internal links individually as strings.

  
while i<len(links_df['internal_links']):
  item = str(links_df['internal_links'][i])
  item = item.split(' ')
  #item[0] = str(item[0])
  item[0] = re.sub("<", "", item[0])
  item[0] = re.sub(">", "", item[0])
  url.append(item[0])
  print(item[0])
  #item[2] = str(item[2])
  item[2] = re.sub("<", "", item[2])
  item[2] = re.sub(">", "", item[2])
  links_df['internal_links'][i] = item[2]
  print(item[2])
  print(item)
  i+=1


links_df['url'] = url
print(links_df) 

links_df.to_csv("data_links.csv", index= False)
print("to_csv done")
