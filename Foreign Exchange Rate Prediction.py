#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, SimpleRNN
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as  tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM


# In[ ]:


realdata = realdata.rename(columns= {'Time Serie' : 'Date'})  
realdata = realdata.set_index('Date')                                  #setting Dates as index
realdata = realdata.drop(['Unnamed: 0'] , axis = 1)                    #removing a column

#Filling ND values with previous and next values
realdata = realdata.replace('ND' , np.nan)
realdata = realdata.bfill().ffill()
realdata = realdata.astype('float')    #changing dtype to float 
realdata.index = pd.to_datetime(realdata.index)      #changing index to date sequence
realdata.interpolate(inplace=True)          #to fill NA values


#printing no of days in between dates
from datetime import date 
print( ( date(2020, 1, 1) - date(2000 , 1, 3)) .days)
print('implying that some dates are missing ')


# In[ ]:



#Creating new data frame with no missing dates  and will fill missing dates data from precious and nexxt days data 

date = {}
date["Date"] = pd.date_range("2000-01-03" , "2019-12-31" , freq = "D")

data = pd.DataFrame(data= date)
data = data.set_index("Date")
data = data.merge(realdata ,left_index= True , right_index = True , how = "left")
data = data.bfill().ffill()


#Changing Dtype from object to Floats so that working can be easy
for dtype in data.dtypes:
  data = data.astype('float')

data.isna().sum()   #Will tell if there is a missing value


# In[ ]:


#Taking four yrs data  for training 
sample = data['2017-01-01' :'2019-12-31']
sample = sample.to_numpy()
print(sample.shape)
# Scaling the sample data
from sklearn.preprocessing import MinMaxScaler
scaler =  MinMaxScaler()
scaler.fit(sample)
scaledsample = scaler.transform(sample)
#Creating traing data 
train_x = np.zeros((sample.shape[0] - 395 ,365  , sample.shape[1]))
train_y = np.zeros((sample.shape[0] - 395 , 30 ,sample.shape[1]))
for i in range(0,sample.shape[0] - 395 ):
  train_x[i] = scaledsample[i:i+365 , :]
  train_y[i] = scaledsample[i+365:i+395 , :]

    
# Reshaping the data for training 
train_x = train_x.reshape(train_x.shape[0] , train_x.shape[2] , train_x.shape[1])
train_y = train_y.reshape(train_y.shape[0] , train_y.shape[2] , train_y.shape[1])
print(train_x.shape , train_y.shape )


# Changig optimizer learning rate 
optimizer = tf.keras.optimizers.RMSprop(0.001)
optimizer.learning_rate.assign(0.02)
print(optimizer.learning_rate)

 #MODEL
model_lstm = Sequential()
model_lstm.add(LSTM ((100) , batch_input_shape = (None, 22,365 ) , return_sequences=True ))
model_lstm.add(LSTM ((30) , return_sequences=True ))

model_lstm.compile(loss = 'mse' , 
              optimizer = optimizer,
              metrics = ['mae','mse'] )

model_lstm.summary()

# Early stopping to stop epochs if there is no improvement
from tensorflow.keras.callbacks import EarlyStopping
early = EarlyStopping( monitor='loss', patience=20 , verbose=1, mode='min',)

#training model 80% data and validating on 20% data 
history = model_lstm.fit(train_x[: round(0.8 * (len(train_x)))] ,
                    train_y[: round(0.8 * (len(train_x))) ] ,
                    epochs = 300
                    ,callbacks=[early] 
                    , validation_data = (train_x[round(0.8 * (len(train_x))) : ] ,
                                                  train_y[ round(0.8 * (len(train_x))) : ]))


# In[ ]:


#Plotting training and validation losss
plt.plot(history.history['loss'] , color = 'g')
plt.plot(history.history['val_loss'] , color = 'b')


# In[ ]:


predicted = model_lstm.predict(train_x)

#Taking a random point and plotting the actual and predicted data for all 22 countries 

index = 24     #index no for which model is predicting 

testdata_x = scaledsample[index : index+365 , :]
testdata_x = testdata_x.reshape(1, testdata_x.shape[1] , testdata_x.shape[0])
testdata_y = scaledsample[index+365 : index+395]

predicted_values  = model_lstm.predict(testdata_x)    #predicting values for testdata 
predicted_values = predicted_values.reshape(predicted_values.shape[0] , predicted_values.shape[2] ,predicted_values.shape[1])   
                                                               #reshaping predicted values for convenience

#putting final result in 'result'
result = []
for i in range(0,predicted_values.shape[1]):
  result.append(scaler.inverse_transform(predicted_values[:,i,:]))  
                #appending predicted values after modifying it original values (as initially data was scaled)

result = np.array(result)     #Converting numpy aray
result = result.reshape(result.shape[0] , result.shape[2] ) #Reshaping   


#Plotting the predicted and true values for all 22 columns  
count =1;
plt.figure(figsize=(30,30))
column_names = list(data.columns.values)
for i in range(0,22):
  plt.figure(figsize=(20,20))
  plt.subplot(22,2,count);
  col = i
  plt.plot(range(365,395),sample[index+365:index+395,col], 'g')               
  plt.plot(range(365,395),result[:,col], 'r')
  plt.title(column_names[col]) 
  count = count+1;

