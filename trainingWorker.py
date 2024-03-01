import pandas as pd
import numpy as np
import xgboost as xgb
import datetime as dt
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# TIME SERIES

def cleanDataTS(df):
    """
    Clean data for time series model
    """
    df = df.copy()
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter # quarter of year
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    for col in ['especie', 'hora', 'ultimo', 'apertura', 
                'varMTD', 'varYTD', 'var6M', 'var12M',
                'variacion',
                'volumen']:
        df = df.drop(col, axis=1)
    return df

def loadLatestXGBModel(policy='latest') -> xgb.Booster:    
    """
    Load XGBoost model from /trained/xgb_time_series/
    Policy: 'latest' or 'best' model
        latest: load the latest model
        best: load the model with the best score
    """

    # get all available models
    files = os.listdir('trained/xgb_time_series/')    
    if len(files) == 0:
        raise Exception('No models found in /trained/xgb_time_series/')

    # policies
    value = files[0].split('_')[1]
    if policy == 'score':
        value = files[0].split('_')[2]    

    model_id = files[0]
    for file in files[1:]:
        _, date, score = file.split('_')
        date = dt.datetime.strptime(date, '%Y-%m-%d-%H-%M-%S')
        score = float(score.split('.')[0])
        if policy == 'latest' and date > value:
            value = date
            model_id = file
        elif policy == 'score' and score > value:
            value = score
            model_id = file            

    return xgb.XGBRegressor().load_model(fname='trained/xgb_time_series/'+model_id)

def trainXGBModel(df, reg):
    """
    Train XGBoost model for time series
    - df: DataFrame with data
    - reg: XGBoostRegressor model
    """
 
    features = [
    'anterior', 'timestamp', 'dayofweek',
    'quarter', 'month', 'year',
    'dayofyear', 'dayofmonth', 'weekofyear'
    ]
    target = 'cierre'

    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)    

    reg.fit(X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)], # cross-validation metrics
        verbose=False)

    score = mean_squared_error(y_test, xgb_model.predict(X_test))
    return reg, score

# REINFORCEMENT LEARNING
# ToDo

if __name__ == '__main__':

    # load MEP data
    df = pd.read_csv('datasets/rava-dolar-mep-historico.csv')
    df = df.set_index('fecha')
    df.index = pd.to_datetime(df.index)

    # load & re-train timeSeries model XGBoost
    xgb_model = loadLatestXGBModel(policy='latest')

    # only keep NEW rows (not trained ones)
    last_trained_date = dt.datetime.now() - dt.timedelta(days=1)
    # df = df[df.index > last_trained_date]
    df = cleanDataTS(df)

    xgb_model, xgb_score = trainXGBModel(df, xgb_model)

    # train reinforcement learning model
    
    # save models into '/trained/type_model/timestamp/'
    xgb_model.save_model('trained/xgb_time_series/'+dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'_'+str(xgb_score)+'.json')    

