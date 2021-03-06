%stateful LSTM(Long Short Term Memory)

from keras.layers.core import Dense, Dropout, Activation
from keras.layers import LSTM

import  os
from keras.models import Sequential, load_model


from sklearn.preprocessing import MinMaxScaler
import  pandas as pd
import numpy as np

dic={'batch_size': 1000, 'dropout1': 0.31955278974391277, 'dropout3': 0.6936110582868452, 'dropout4': 0.5044383573441469, 'units1': 428.0, 'units3': 290.0, 'units4': 202.0}
forword=30
look_back=120
tr_size=0.1
ep=50

df=pd.read_excel('test_data.xlsx')
df1=df.copy()


df1=df1[['日期（月度）','USA_output','OPEC_output','demand_current','supply_current']]
#df1=df1.bfill()
df1=df1.dropna()


df1=df1.rename(columns={"日期（月度）":'日期（日期）'})
df1=df1.set_index('日期（日期）')


df1=df1.asfreq(freq='d')

df1=df1.bfill()
#print(df1.head(40))

df=df.set_index('日期（日期）')


df=df[['Brent','USD','CRB','Premium','trade','BDI']]


df=df.ffill()
df=df.bfill()



df=df.join(df1)

df=df.dropna()
df=df.astype('float64')

#df_raw=df.copy()


#df['flag']=[ (lambda y: 1 if (y%7==6)|(y%7==0) else 0)(x) for x in range(df.shape[0])]
print(df.shape[0])
#print(df_raw.shape[0])




#print(df)



#df=df.iloc[0:50]



dataset=df.values
#dataset = dataset.astype('float32')
#print(dataset)
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)






train_size = int(len(dataset) * tr_size)
trainlist = dataset[:train_size]
testlist = dataset[train_size:]



def create_dataset(dataset, look_back,forword):

        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-forword):
            a = dataset[i:(i+look_back)]
            dataX.append(a)
            dataY.append(dataset[(i + look_back):(i+look_back+forword)])
        return np.array(dataX),np.array(dataY)


trainX,trainY  = create_dataset(trainlist,look_back,forword)
testX,testY = create_dataset(testlist,look_back,forword)


trainY=np.reshape(trainY,(trainY.shape[0],-1))

#print(trainX)
#print(trainY)


def trainModel():

    model = Sequential()
    model.add(LSTM(
        int(dic['units3']),batch_input_shape=(1, trainX.shape[1], trainX.shape[2]),return_sequences=True, stateful=True))
    model.add(Dropout(dic['dropout3']))
    model.add(LSTM(
        int(dic['units4']),batch_input_shape=(1, trainX.shape[1], trainX.shape[2]),return_sequences=False, stateful=True))
    model.add(Dropout(dic['dropout4']))

    model.add(Dense(
        trainY.shape[1]))
    model.add(Activation("relu"))

    model.compile(loss='mse', optimizer='adam')
    

    return model



model=trainModel()

for x in range(50):
    print(x)
    model.fit(trainX, trainY, epochs=1, batch_size=1,shuffle=False,verbose=2)
    model.reset_states()


model.save('model2.h5')    



#y_hat  =  model.predict(np.reshape(trainX[0:2],(-1,trainX.shape[1],trainX.shape[2])))
y_hat  =  model.predict(testX,batch_size = 1)




def retrive(hat):
    hat=np.reshape(hat,(-1,df.shape[1]))
    hat=scaler.inverse_transform(hat)
    hat=np.reshape(hat,(-1,forword,df.shape[1]))
    result=[[y[1] for y in x] for x in hat]
    #print(np.array(result))
    return np.array(result)


#print(df_raw.iloc[train_size:])

diff=retrive(y_hat)-retrive(testY)


mae=(np.abs(diff)).mean()
#rmse=np.sqrt((diff**2).mean())
print(mae)
fo = open("res.txt", "w")
fo.write(repr(mae))
fo.close()
