import pandas as pd
import datetime 
import numpy as np

# using datetime module
import datetime
import random
import uuid


x = 19.75
y = 15.25

il = np.arange(1,20,.25)

df = pd.DataFrame(data={"range":il,"number of cuts": x/il})

print(df)