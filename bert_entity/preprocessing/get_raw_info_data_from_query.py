import pandas as pd
import re
import random

data = pd.read_csv("info_query_out")
#data = data.head(5000)

data.to_csv("info_query_out_dummy_raw.csv", index= False, header= True)
