# -*- coding: utf-8 -*-
"""Phishing_URL_Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aBm-FBq7u2-wi0-bk0R8B29PSCc1DqmN
"""

pip install tld

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import warnings
from sklearn import metrics
warnings.filterwarnings('ignore')
from urllib.parse import urlparse
import re
from googlesearch import search
from tld import get_tld
import os.path
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

df=pd.read_csv("/content/malicious_phish.csv")

df.shape

df.head()

df.head(10)

df.columns

df.info()

df.nunique()

df.type.value_counts()

df.describe().T

def Having_ip_address(url):
    match = re.search(
     '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
    '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
         '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        return 1
    else:
        return 0
df["use_of_ip"] = df['url'].apply(lambda i: Having_ip_address(i))

def abnormal_url(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    if match:
        return 1
    else:
        return 0

df["abnormal_url"] = df["url"].apply(lambda i: abnormal_url(i))

def google_index(url):
    site = search(url, 5)
    return 1 if site else 0
df['google_index'] = df['url'].apply(lambda i:google_index(i))

def count_dot(url):
    count_dot = url.count('.')
    return count_dot

df['count.'] = df['url'].apply(lambda i: count_dot(i))

df.head(10)

df.columns

def count_www(url):
    url.count('www')
    return url.count('www')
df['count-www'] = df['url'].apply(lambda i:count_www(i))

def count_atrate(url):
    return url.count('@')

df['count@'] = df['url'].apply(lambda i:count_atrate(i))

def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')
df['count_dir'] = df['url'].apply(lambda i: no_of_dir(i))

def no_of_embed(url):
    urldir = urlparse(url).path
    return urldir.count('//')
df["count_embed_domain"] = df['url'].apply(lambda i: no_of_embed(i))

def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0

df['short_url'] = df['url'].apply(lambda i: shortening_service(i))

def count_https(url):
    return url.count('https')
df['count-https'] = df['url'].apply(lambda i:count_https(i))

def count_http(url):
    return url.count('http')
df['count-http'] = df['url'].apply(lambda i:count_http(i))

def count_per(url):
    return url.count('%')
df['count%'] = df['url'].apply(lambda i:count_per(i))

def count_ques(url):
    return url.count('?')
df['count?'] = df['url'].apply(lambda i:count_ques(i))

def count_hyphen(url):
    return url.count('-')
df['count-'] = df['url'].apply(lambda i:count_hyphen(i))

def count_equal(url):
    return url.count('=')
df['count='] = df['url'].apply(lambda i:count_equal(i))

def url_length(url):
    return len(str(url))
df['url_length'] = df['url'].apply(lambda i:url_length(i))

def hostname_length(url):
    return len(urlparse(url).netloc)
df['hostname_length'] = df['url'].apply(lambda i:hostname_length(i))

df.head()

def suspicious_words(url):
    match = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr',
                      url)
    if match:
        return 1
    else:
        return 0

df['sus_url'] = df['url'].apply(lambda i:suspicious_words(i))

def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits+1
    return digits

df['count-digits'] = df['url'].apply(lambda i:digit_count(i))

def letter_count(url):
    letters =0
    for i in url:
        if i.isalpha:
            letters = letters+1
    return letters
df['count-letters'] = df['url'].apply(lambda i:letter_count(i))

def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return lrn(urlpath.split('/')[1])
    except:
        return 0
df['fd_length'] = df['url'].apply(lambda i:fd_length(i))
#length of top level domain
df['tld'] = df['url'].apply(lambda i:get_tld(i,fail_silently=True))

df.head(10)

df.columns

df.shape

def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1
df['tld_length'] = df['tld'].apply(lambda i:tld_length(i))

df.head

df.columns

df.head()

df = df.drop("tld",1)

df.columns

df["type"].value_counts()

df["type"].value_counts().plot(kind='pie',autopct='%1.2f%%')
plt.title("Phishing Count")
plt.show()

plt.figure(figsize=(15,15))
sns.heatmap(df.corr(), annot=True)
plt.show()

sns.set(style = "darkgrid")
ax = sns.countplot(y="type",data = df,hue = "use_of_ip")

sns.set(style = "darkgrid")
ax = sns.countplot(y="type",data = df,hue = "sus_url")

sns.set(style = "darkgrid")
ax = sns.catplot(x="type",y="hostname_length",kind = "box",data=df)

lb_make = LabelEncoder()
df['type_code'] = lb_make.fit_transform(df["type"])
df["type_code"].value_counts()

X = df[['use_of_ip','abnormal_url', 'count.', 'count-www', 'count@',
       'count_dir', 'count_embed_domain', 'short_url', 'count-https',
       'count-http', 'count%', 'count?', 'count-', 'count=', 'url_length',
       'hostname_length', 'sus_url', 'fd_length', 'tld_length', 'count-digits',
       'count-letters']]

y = df["type_code"]

X.head()

X.columns

x_train,x_test,y_train,y_test = train_test_split(X,y,stratify = y,test_size=0.2,shuffle = True,random_state=5)

rf = RandomForestClassifier(n_estimators = 100,max_features = "sqrt")

rf.fit(x_train,y_train)

y_pred_rf = rf.predict(x_test)

print(classification_report(y_test,y_pred_rf,target_names = ['benign','defacement','phishing','malware']))

score = accuracy_score(y_test,y_pred_rf)
print(f"accuracy: {score*100}")

def main(url):
    status = []
    status.append(Having_ip_address(url))
    status.append(abnormal_url(url))
    status.append(count_dot(url))
    status.append(count_www(url))
    status.append(count_atrate(url))
    status.append(no_of_dir(url))
    status.append(no_of_embed(url))

    status.append(shortening_service(url))
    status.append(count_https(url))
    status.append(count_http(url))

    status.append(count_per(url))
    status.append(count_ques(url))
    status.append(count_hyphen(url))
    status.append(count_equal(url))

    status.append(url_length(url))
    status.append(hostname_length(url))
    status.append(suspicious_words(url))
    status.append(digit_count(url))
    status.append(letter_count(url))
    status.append(fd_length(url))
    tld = get_tld(url,fail_silently=True)

    status.append(tld_length(tld))

    return status

def get_prediction_from_url(test_url):
    features_test = main(test_url)
    print(features_test)
    features_test = np.array(features_test).reshape((1, -1))
    print(features_test)
    pred = rf.predict(features_test)
    print(pred)
    if int(pred[0]) == 0:
        res="SAFE"
        return res
    elif int(pred[0]) == 1.0:
        res="DEFACEMENT"
        return res
    elif int(pred[0]) == 2.0:
        res="PHISHING"
        return res

    elif int(pred[0]) == 3.0:
        res="MALWARE"
        return res

urls = 'titaniumcorporate.co.z'
#for url in urls:
print(get_prediction_from_url(urls))

with open('Phishing_Url_detection.pickle','wb') as f:
    pickle.dump(rf,f)

columns = {
    'data_columns':[col.lower() for col in X.columns]
}
with open("columns.json","w") as f:
    f.write(json.dumps(columns))

import pickle
with open('Phishing_Url_detection.pickle','wb') as f:
    pickle.dump(rf,f)

import json
columns = {
    'data_columns':[col.lower() for col in X.columns]
}
with open("columns.json","w") as f:
    f.write(json.dumps(columns))