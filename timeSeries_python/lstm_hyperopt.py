%hyper-parameters optmisation for LSTM model

from keras.layers.core import Dense, Dropout, Activation
from keras.layers import LSTM

import  os
from keras.models import Sequential, load_model

from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from sklearn.preprocessing import MinMaxScaler
import  pandas as pd
import numpy as np

forword=15
look_back=60
tr_size=0.86


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


def retrive(hat):
    hat=np.reshape(hat,(-1,df.shape[1]))
    hat=scaler.inverse_transform(hat)
    result=[x[0] for x in hat]
    #print(np.array(result))
    return np.array(result)

y_glob=retrive(testY)

#print(trainX)
#print(trainY)


space= { 
                      'units3': hp.quniform('units3',64,512,1),
                      'dropout3': hp.uniform('dropout3',0.25,0.75),
                      'units4': hp.quniform('units4',64,512,1),
                      'dropout4': hp.uniform('dropout4',0.25,0.75),
                                        
'batch_size' : hp.quniform('batch_size',28,128,1),
'units1':hp.quniform('units1',64,512,1),

'dropout1':hp.uniform('dropout1',0.25,0.75),
}


def trainModel(params):

    model = Sequential()
    model.add(LSTM(
        int(params['units1']),
        input_shape=(trainX.shape[1], trainX.shape[2]),
        return_sequences=True))
    model.add(Dropout(params['dropout1']))



    model.add(LSTM(int(params['units3']),return_sequences=True))
    model.add(Dropout(params['dropout3']))

    model.add(LSTM(int(params['units4']),return_sequences=False))

    model.add(Dropout(params['dropout4']))
    model.add(Dense(trainY.shape[1]))
    model.add(Activation("relu"))

    model.compile(loss='mse', optimizer='adam')
    model.fit(trainX, trainY, epochs=30, batch_size=int(params['batch_size']), verbose=2)
    y_hat  =  model.predict(testX)



    diff=retrive(y_hat)-y_glob

    #rmse=np.sqrt((diff**2).mean())
    mae=(np.abs(diff)).mean()
    return {'loss': mae, 'status': STATUS_OK}



trials = Trials()
best = fmin(trainModel, space, algo=tpe.suggest, max_evals=30, trials=trials)
fo = open("res3.txt", "w")
fo.write( repr(best))
fo.close()

