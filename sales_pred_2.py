# -*- coding: utf-8 -*-
"""SALES PRED 2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YjQWn7Us72tDOIjy4GbP_uyeH7N8GdjS
"""

from google.colab import drive
drive.mount('/content/drive')

import warnings
warnings.filterwarnings('ignore')
import pandas as  pd
import numpy as np
a=pd.read_csv('/content/drive/MyDrive/advertising.csv')
print (a)

"""# Data Inspection


"""

a.shape

a.info()

a.describe()

"""# Data cleaning"""

a.isnull().sum()*100/a.shape[0]

"""# Model Building"""

X = a['TV']
y = a['Sales']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.7, test_size = 0.3, random_state = 100)
X_train.head()

y_train.head()

import statsmodels.api as sm

X_train_sm = sm.add_constant(X_train)
lr = sm.OLS(y_train, X_train_sm).fit()

lr.params

print(lr. summary())

"""# ModelEvalution"""

y_train_pred = lr.predict(X_train_sm)
res = (y_train - y_train_pred)

"""# Prediction on the Test set"""

X_test_sm = sm.add_constant(X_test)
y_pred = lr.predict(X_test_sm)

y_pred.head()

from sklearn. metrics import mean_squared_error
from sklearn.metrics import r2_score

np.sqrt(mean_squared_error(y_test, y_pred))

"""# checking R-squared"""

r_squared = r2_score(y_test, y_pred)
r_squared