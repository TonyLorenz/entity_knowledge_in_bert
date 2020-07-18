import pandas as pd
import re
import random

data = pd.read_csv("info_query_out")
#data = data.head(5000)

data.to_csv("data_info.csv", index= False, header= True)
