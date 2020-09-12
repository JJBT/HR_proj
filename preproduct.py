import pandas as pd

filename = 'V3_pred.xlsx'
df = pd.read_excel(filename)
df = df[['links', 'full/xgb_recall_predict', 'full/rf_fake_predict']]
df.rename(columns={'full/xgb_recall_predict': 'predict1', 'full/rf_fake_predict': 'predict2'}, inplace=True)
df.to_excel(filename)
