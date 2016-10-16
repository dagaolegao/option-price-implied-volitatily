from scipy import stats
from math import log, sqrt,exp
import pandas as pd

v_0120=dict()
stocklist={'AAPL','AMZN','BAC','GOOG','GS','HSBC','JPM','MSFT','YHOO'}
stockprice={'AAPL':116.98,'AMZN':829.28,'CIT':35.88,'BAC':15.83,'GOOG':778.19,'GS':167.42,'HSBC':37.39,'JPM':67.74,'MSFT':56.92,'YHOO':41.62}
for row in stocklist: 
    df= pd.read_excel(open('{}_2016.12.16.xlsx'.format(row),'rb'),sheetname='call')
    print(df.head())
    
    def bsm_vega(S,K,T,r,sigma):
        d1=(log(S/K)+(r+0.5*sigma**2)*T)/(sigma*sqrt(T))
        vega=S*stats.norm.pdf(d1,0.0,1.0)*sqrt(T)
        return vega
    
    def bsm_vomma(S,K,T,r,sigma):
        d1=(log(S/K)+(r+0.5*sigma**2)*T)/(sigma*sqrt(T))
        d2=d1-sigma*sqrt(T)
        vomma= bsm_vega(S,K,T,r,sigma)*d1*d2/sigma
        return vomma
    
    def bsm_call_value(S,K,T,r,sigma): #black shole model
        d1=(log(S/K)+(r+0.5*sigma**2)*T)/(sigma*sqrt(T))
        d2=d1-sigma*sqrt(T)
        
        N_d1=stats.norm.cdf(d1,0.0,1.0)
        N_d2=stats.norm.cdf(d2,0.0,1.0)
        
        call_price=(S*N_d1-K*exp(-r*T)*N_d2)
        return call_price 
        
    stock_0120=[]
    for j in range(len(df)):
        S=stockprice[row]
        K=df.ix[j,0]
        T=((17+30+16)/365)
        r=0.05
        C_star=df.ix[j,2]
        sigma=0.1 
        for i in range(10):
            f=-bsm_vega(S,K,T,r,sigma)+(bsm_vega(S,K,T,r,sigma)**2-2*(bsm_call_value(S,K,T,r,sigma)-C_star)*bsm_vomma(S,K,T,r,sigma))**0.5
            f_prime=bsm_vomma(S,K,T,r,sigma)
            sigma=sigma+(f/f_prime)         
        print(sigma)
        stock_0120.append(sigma)
        
    v_0120['{}'.format(row)]=stock_0120




