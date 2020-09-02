import re
import pandas as pd

fp = open('page_links_en.ttl', 'r')
#print("fp = open('page_links_en.ttl', 'r') done")
j= 0
while j < 3672112:
 fp.readline()
 j+=1
print("tail done!")
line = fp.readline()
#print("line = fp.readline() done")

#print("cnt = 0 done")
counter = 0
#url = []
while counter <200:
 links = []
 cnt = 0
 while cnt<918028:
   if cnt<8:
     line = fp.readline()
     #print("cnt 8")
     cnt+=1
   else:
    links.append(line)
    line = fp.readline()
    cnt += 1
    print(cnt)

 print("while done")
#links_df = pd.read_table(fp, names=['internal_links'])
#print(links_df.head())
 print("links_df done!")
 links_df = pd.DataFrame(links, columns=['internal_links'])
#print("dataframe done")

#print(links_df)

 url = []

 i =0

 while i<len(links_df['internal_links']):
   item = str(links_df['internal_links'][i])
   item = item.split(' ')
   #item[0] = str(item[0])
   item[0] = re.sub("<", "", item[0])
   item[0] = re.sub(">", "", item[0])
   url.append(item[0])
  # print(item[0])
   #item[2] = str(item[2])
   item[2] = re.sub("<", "", item[2])
   item[2] = re.sub(">", "", item[2])
   links_df['internal_links'][i] = item[2]
   #print(item[2])
   #print(item)
   i+=1
   print(i)

 links_df['url'] = url
 #print(links_df) 

 links_df.to_csv(f"data_links_{counter}.csv", index= False)
 print(f"Counter {counter} done!")
 counter += 1
#print("to_csv done")
