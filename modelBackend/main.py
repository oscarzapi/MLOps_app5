# 1. Import libraries
import pandas as pd
import numpy as np
from pycaret.regression import load_model, predict_model
from fastapi import FastAPI, UploadFile
import uvicorn
import csv
import codecs
import requests
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# 2. Create the app object
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load pretrained model
model = load_model('time-series-forecast-pipeline')

# 4. Define predict function
@app.post('/predict_from_dates')

async def insert_dates(startDate,endDate):
    startDateFormatted = str(pd.to_datetime(startDate).date())
    endDateFormatted = str(pd.to_datetime(endDate).date())

#async def upload_file(file:UploadFile):
    #contents = await file.read()
    #csv_reader = csv.reader(codecs.iterdecode(file.file,'utf-8')) 
    
    # Input the future dates to be predicted
    future_dates = pd.date_range(start=startDateFormatted, end=endDateFormatted, freq = 'MS')
    # print(startDateFormatted,type(endDateFormatted))

    future_df = pd.DataFrame()

    future_df['MonthNum'] = [i.month for i in future_dates]
    future_df['Year'] = [i.year for i in future_dates]    
    future_df['Series'] = np.arange(145,(145+len(future_dates)))
    predictions_future = predict_model(model, data=future_df)
    return predictions_future.to_dict(orient='records')

@app.post('/predict_from_file')

async def upload_file(file:UploadFile):
    csv_reader = csv.reader(codecs.iterdecode(file.file,'utf-8')) 
    header = csv_reader.__next__()
    df = pd.DataFrame(csv_reader, columns=header)
    
    future_dates = pd.date_range(start=min(df['Month']), end=max(df['Month']), freq = 'MS')
    future_df = pd.DataFrame(columns=['MonthNum', 'Year', 'Series'])

    

    future_df['MonthNum'] = pd.DatetimeIndex(df['Month']).month
    future_df['Year'] = pd.DatetimeIndex(df['Month']).year    
    future_df['Series'] = np.arange(145,(145+len(future_dates)))
    print(future_df)
    predictions_future = predict_model(model, data=future_df)
    return predictions_future.to_dict(orient='records')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)