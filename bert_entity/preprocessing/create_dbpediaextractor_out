import pandas as pd

data = pd.read_excel('dbpedia_dummy.xlsx')
data = data.to_dict(orient = 'records')
print(data)
i=0

print(data[i]['internal links'])


while i<3:
  internal_links_new = []
  offset_list = []
  item = data[i]['internal links'].split(', ')
  for word in item:
    word = word.replace('_',' ')
    internal_links_new.append((word, word))
    print(word)
    x = data[i]['text'].find(word)
    if x>0:
      offset_list.append((x, x + len(word)))
    else:
      offset_list.append(x)
  data[i]['internal links'] = dict(zip(offset_list, internal_links_new))
  del data[i]['internal links'][-1]
#  data[i]['internal links'] = sorted(data[i]['internal links'].items())
  data[i]['internal links'] = base64.b64encode(pickle.dumps(data[i]['internal links'])).decode('utf-8')
  print(data[i]['internal links'])
  i+=1
  #base64.b64encode(pickle.dumps(self.internal_links)).decode('utf-8')

  print(data)
