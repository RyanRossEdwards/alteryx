#################################
# List all non-standard packages to be imported by your 
# script here (only missing packages will be installed)
from ayx import Package
Package.installPackages(['pandas','numpy','authlib'])


#################################
import time
import pandas as pd
import numpy as np
from ayx import Alteryx
from authlib.jose import jwt



#################################
# Format {'key':'xxx', 'secret':'yyy'}
df = Alteryx.read("#1")
auth = df.to_dict('records')[0]


#################################
header = {'alg' : 'HS256', 'typ' : 'jwt'}

# Epoch timestamp + 1 hour (token lasts for 1 hour)
ts = round(time.time() + 60 * 60)
payload = {'iss' : auth['key'], 'exp' : ts}

s = jwt.encode(header, payload, auth['secret'])

df = pd.DataFrame(data={'token' : [s.decode("utf-8")]})


#################################
Alteryx.write(df,1)