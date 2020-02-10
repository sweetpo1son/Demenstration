import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.api import VAR, DynamicVAR
from statsmodels.tsa.base.datetools import dates_from_str


n=15  #forcast
m=10  #samples
k=20  #hyper (fit)
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



df['Premium']=np.add(df['Premium'],16)
data = np.log(df).diff().dropna()

#print(data.head(50))
data=data.asfreq(freq='d')


resi=[]

for x in range(int(data.shape[0] * tr_size),data.shape[0]-n):  
    print(x)
    data1=data.iloc[0:x,:]

    #print(data.index)

    #print(data.head(20))


    model = VAR(data1)
    results = model.fit(k)#maxlags=15, ic='aic'


    lag_order = results.k_ar
    temp=results.forecast(data1.values[-lag_order:], n)
    
    temp=[x[0] for x in temp]
    las=np.log(df.iloc[x]['Brent'])

    temp=np.insert(temp,0,las)
    temp=np.cumsum(temp)
    temp=np.exp(temp)
    #print(temp.shape[0])
    orig=np.log(df.iloc[(x+1):(x+1+n)]['Brent'])
    #print(orig.shape[0])
    temp=np.subtract(temp[1:],orig)
    resi.append(temp)


mae=(np.abs(resi)).mean()
print(mae)


