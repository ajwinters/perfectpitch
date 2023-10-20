import pandas as pd
import datetime 


# using datetime module
import datetime
import random


# self.randomrange = randrange(12 * lowO, 12*highO)
#         self.tl = groupind
#         for i in range(lowO,highO):
#             ttl = [j * 12 for j in groupind]
#             self.tl.append(ttl)
#         print(self.tl)

lowO = 4
highO = 8 

xl = [0,3,4,7,8]

for i in range(lowO,highO):
    ttl = [12*i+j for j in xl]
    print(ttl)