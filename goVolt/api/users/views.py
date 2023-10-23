from django.shortcuts import render, redirect
from firebase_admin import firestore

import pandas as pd
from sodapy import Socrata


def index(request): 
    data = read_data()
    store_charge_points_fb(data)
    return render(request,'index.html')
    
def store_charge_points_fb(data):
    db = firestore.client()
    collection_name = 'charge_points'
    for record in data:
        db.collection(collection_name).add(record)
       
def read_data():
    client = Socrata("analisi.transparenciacatalunya.cat", None)
    results = client.get("tb2m-m33b", limit=10)
    results_df = pd.DataFrame.from_records(results)
    results_df = results_df.to_dict(orient='records')
    return results_df 