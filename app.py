from flask import Flask, request, render_template
import pandas as pd
from geopy.distance import geodesic

app = Flask(__name__)
#df=pd.read_pickle('clustering.pkl')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    df=pd.read_pickle('clustering.pkl')
    lat=float(request.form['Latitude'])
    lon=float(request.form['Longitude']) 
    state=str(request.form['StateName']).upper()
    site_count=int(request.form['SiteCount'])
    
    df=df[df['StateName']==state]
    add1=(lat,lon)
    distance_list=[]
    
    df=df.reset_index()
    for i in range(len(df)):
        add2=(df['Latitude'][i],df['Longitude'][i])
        distance_list.append(geodesic(add1, add2).km)
    df['Distance_in_KM']=distance_list

  
    df=df.sort_values(by='Distance_in_KM')
    df=df.reset_index()
    df=df[['CustomerSiteId','UniqueID','SiteName','StateName','Latitude','Longitude','Priority','Distance_in_KM']]
    df=df.head(site_count)
    
    
    return render_template('after.html',tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == "__main__":
    app.run(debug=True)