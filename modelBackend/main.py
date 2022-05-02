# 1. Import libraries
import pandas as pd
import numpy as np
from pycaret.regression import load_model, predict_model
from fastapi import FastAPI, UploadFile
import uvicorn
import csv
import codecs
import requests

# 2. Create the app object
app = FastAPI()


# 3. Load pretrained model
model = load_model('time-series-forecast-pipeline')

# 4. Define predict function
@app.post('/predict_from_file')

async def upload_file(file:UploadFile):
    #contents = await file.read()
    csv_reader = csv.reader(codecs.iterdecode(file.file,'utf-8')) 
    
    # Input the future dates to be predicted
    future_dates = pd.date_range(start='01/01/1961', end='01/01/1965', freq = 'MS')

    future_df = pd.DataFrame()

    future_df['MonthNum'] = [i.month for i in future_dates]
    future_df['Year'] = [i.year for i in future_dates]    
    future_df['Series'] = np.arange(145,(145+len(future_dates)))
    predictions_future = predict_model(model, data=future_df)
    print(predictions_future)
    return predictions_future.to_dict(orient='records')
        

# def predict(carat_weight, cut, color, clarity, polish, symmetry, report):
#     data = pd.DataFrame([[carat_weight, cut, color, clarity, polish, symmetry, report]])
#     data.columns = ['Carat Weight', 'Cut', 'Color', 'Clarity', 'Polish', 'Symmetry', 'Report']

#     predictions = predict_model(model, data=data) 
#     return {'prediction': int(predictions['Label'][0])}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)