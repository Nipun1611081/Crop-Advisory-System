import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd 
from flask_pymongo import PyMongo
app = Flask(__name__)
model = pickle.load(open('knn_new.pkl', 'rb'))
app.config['MONGO_URI'] = "mongodb://localhost:27017/crop"
mongo= PyMongo(app)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():


    '''
    For rendering results on HTML GUI
    '''
    balance_data = pd.read_csv("final-crop.csv")
    df=balance_data[['Crop', 'Region', 'Sowing Time', 'Soil Type']].copy()
    print(df.head(20))
    df.shape
    
    #CROP 

    save_crop=df["Crop"].unique()
    crop_dict={}
    count=1
    for i in save_crop:
      crop_dict[i]=count
      count=count+1

    def get_key(val):
        for key, value in crop_dict.items(): 
         if val == value: 
             return key
        return "key doesn't exist"  
  
    

    #REGION 
    save_region=df["Region"].unique()
    region_dict={}
    count=1
    for i in save_region:
      region_dict[i]=count
      count=count+1

    #SOWING TIME 

    save_sowing={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}


    #SOIL TYPE

    save_soil=df["Soil Type"].unique()
    soil_dict={}
    count=1
    for i in save_soil:
      soil_dict[i]=count
      count=count+1
    
    
    month= request.form["month"]
    region= request.form["region"]
    soil= request.form["soil"]
    ph= request.form["ph"]
    temp = mongo.db.temperature.find_one_or_404({'District':region})
    rain = mongo.db.rainfall.find_one_or_404({'District':region})
    #return('Temperature: '+temp[month]+'C Rainfall: '+ rain[month]+'mm.');
    #region= int(region_dict[region])
    val_temp= int(float(temp[month]))
    val_rain= int(float(rain[month]))
    month= int(save_sowing[month])
    soil= int(soil_dict[soil])
    #return "hello";
    #print (model.predict([[region,month,ph,soil]]))
    prediction = model.predict([[month,val_temp,val_temp,ph,soil,val_rain,val_rain]])
    #return('Temperature: '+temp[month]+'C Rainfall: '+ rain[month]+'mm.');
    output = get_key((prediction[0]))


    return render_template('index.html', prediction_text='Optimum crop should be {}'.format(output))

@app.route('/hello',methods=['POST'])
def hello():
    return "hello"; 


if __name__ == "__main__":
    app.run(debug=True)