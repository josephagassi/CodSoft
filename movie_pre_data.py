# -*- coding: utf-8 -*-
"""MOVIE PRE DATA

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Is4ujhuCF5VrdT95tNDb4JqVmoPfesW7
"""

from google.colab import drive

drive.mount("/content/drive")

import numpy as np
import pandas as pd
a=pd.read_csv("/content/drive/MyDrive/IMDb Movies India.csv",encoding='latin1')
print(a)

a.info()

import numpy as np
a.shape

a.columns

"""# Unnecessary columns for the analysis"""

a=a.drop(columns=["Name",'Actor 2',"Actor 3"])
a.head()

a.dropna(inplace=True)

a.drop_duplicates(inplace=True)
a.shape

"""# Handling Columns


"""

a['Year'].unique()

def handleYear(value):
  value = str(value).strip('()')
  return int(value)
a['Year']= a['Year'].apply(handleYear)
a['Year'].head()

a['Duration'].unique()

def handleDuration(value):
  value=str(value). split(' ')
  value=value[0]
  return int(value)
a['Duration']=a['Duration'].apply(handleDuration)
a['Duration'].head()

a['Genre'].unique()

def split_genre_column(a,Genre):
  a['Genre1']= a[Genre].str.split(',', expand=True)[0]
  a['Genre2']= a[Genre].str.split(',', expand=True)[1]
  a['Genre3']= a[Genre].str.split(',', expand=True)[2]
  return a

split_genre_column(a ,'Genre')

a.isna().sum()

a =a.fillna(0)
a.isna().sum()

G=['Genre1','Genre2','Genre3']
for x in G:
  a[x],_ =pd.factorize(a[x])
# Removed the drop function from here
a.head()

a['Votes'].unique()

def handleVotes(value):
    value = str(value).replace(',','')
    return int(value)
a['Votes'] =a['Votes'].apply(handleVotes)
a['Votes'].head()

"""# Feature Engineering"""

a['aAge'] =2024 -a ['Year']
a['aAge']

DirectorCounts =a['Director'].value_counts()
a['DirectorPopularity']= a['Director'].map(DirectorCounts)
ActorCounts= a['Actor 1'].value_counts()
a['ActorPopularity']=a['Actor 1'].map(ActorCounts)

a['LogVotes']=np.log1p(a['Votes'])
a['LogVotes']

DirectorAvgRating = a.groupby('Director')['Rating'].mean()
a['DirectorAvgRating'] = a['Director'].map(DirectorAvgRating)

ActorAvgRating = a[['Actor 1']].stack().reset_index(name='Actor')
ActorAvgRating = ActorAvgRating.merge(a[['Rating']], left_on='level_0', right_index=True)
ActorAvgRating = ActorAvgRating.groupby('Actor')['Rating'].mean()
a['ActorAvgRating'] = a['Actor 1'].map(ActorAvgRating)

a['Genre1 encoded'] =round(a.groupby('Genre1')['Rating'].transform('mean'),1)
a['Genre2 encoded']=round(a.groupby('Genre2')['Rating'].transform('mean'),1)
a['Genre3 encoded'] =round(a.groupby('Genre3')['Rating'].transform('mean'),1)
a['Votes encoded'] =round(a.groupby('Votes')['Rating'].transform('mean'), 1)
a['Director encoded']= round(a.groupby('Director')['Rating'].transform('mean'), 1)
a['Actor 1 encoded']= round(a.groupby('Actor 1')['Rating'].transform('mean'), 1)
a.head()

a.drop(columns=['Genre1','Votes','Director','Actor 1','Genre2','Genre3'],inplace=True)
a['Rating'] =round(a['Rating'],1)

"""# Building the model"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

X=a.drop("Rating",axis=1)
Y=a["Rating"]

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=52)

model=LinearRegression()
model.fit(X_train,Y_train)


X_test_prediction= model.predict(X_test)

mse =mean_squared_error(Y_test,X_test_prediction)
print(f"Mean Squared Error (MSE): {mse:.2f}")

r2 = r2_score(Y_test,X_test_prediction)
print(f"R-squared score: {r2:.2f}")

"""# SVC"""

from sklearn.svm import SVR

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.1)

model_SVR = SVR(kernel='linear',C=1.0,epsilon=0.1,gamma='scale')
model_SVR.fit(X_train,Y_train)
X_test_prediction_SVR=model_SVR.predict(X_test)

mse_SVR =mean_squared_error(Y_test,X_test_prediction_SVR)
print(f"Mean Squared Error (MSE): {mse_SVR:.2f}")

r2_SVR= r2_score(Y_test,X_test_prediction_SVR)
print(f"R-squared score: {r2_SVR:.2f}")