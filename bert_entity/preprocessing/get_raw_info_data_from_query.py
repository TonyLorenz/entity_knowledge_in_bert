import pandas as pd
import re
import random

    """
    Make csv from queried info data.
    """
  
data = pd.read_csv("query_out")
#data = data.head(5000)

data.to_csv("data_info.csv", index= False, header= True)
