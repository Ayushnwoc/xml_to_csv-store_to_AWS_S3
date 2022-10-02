#importing libraries
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import boto
import boto.s3.connection
import pandas as pd
from io import StringIO

# Storing start time
start_time = datetime.now()

# opening xml file
with open('DLTINS_20210117_01of01.xml', 'r') as f:
    data = f.read()

# Passing the stored data inside the beautifulsoup parser,
# storing the returned object
try:
    Bs_data = BeautifulSoup(data, "xml")
except:
    print("Error in storing data inside beautifulsoup parser.")
    exit()

# Finding all instances of respective tags
id = Bs_data.find_all('Id')
name = Bs_data.find_all('FullNm')
a = Bs_data.find_all('ClssfctnTp')
b = Bs_data.find_all('CmmdtyDerivInd')
c = Bs_data.find_all('NtnlCcy')
d = Bs_data.find_all('Issr')

cols = ["FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm", "FinInstrmGnlAttrbts.ClssfctnTp",
        "FinInstrmGnlAttrbts.CmmdtyDerivInd", "FinInstrmGnlAttrbts.NtnlCcy", "Issr"]

# opening csv file and writing in it
with open('output.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(cols)
    for i in range(len(a)):
        row = []
        if id is not None:
            row.append(id[i].text)
        else:
            row.append("NA")
        if name is not None:
            row.append(name[i].text)
        else:
            row.append("NA")
        if a is not None:
            row.append(a[i].text)
        else:
            row.append("NA")
        if b is not None:
            row.append(b[i].text)
        else:
            row.append("NA")
        if c is not None:
            row.append(c[i].text)
        else:
            row.append("NA")
        if d is not None:
            row.append(d[i].text)
        else:
            row.append("NA")
        write.writerow(row)

# Now upload to AWS S3 bucket
# we will need aws access key id and its secret key
access_key = 'fake_key'
secret_key = 'fake_pass'

# getting bucket object
conn = boto.connect_s3(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)

# creating bucket
bucket_csv = conn.create_bucket('store_csv')

#reading csv file and uploading to aws s3 bucket
dataf = pd.read_csv('output.csv')
s3 = boto3.client('s3',
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)

csv_buf = StringIO()
dataf.to_csv(csv_buf,header=True,index=False)
csv_buf.seek(0)

#store file as store.csv
s3.put_pbject(Bucket = 'store_csv' , Body = csv_buf.getvalue() , Key = 'store.csv')


# storing end time
end_time = datetime.now()

# printing total duration of code
print('Duration of Program Execution: {}'.format(end_time - start_time))
