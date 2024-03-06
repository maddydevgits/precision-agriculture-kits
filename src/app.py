from flask import Flask,render_template,redirect,request,session
from web3 import Web3,HTTPProvider
import json
import urllib3

def readData():
    req='https://api.thingspeak.com/channels/2454779/feeds.json'
    http=urllib3.PoolManager()
    response=http.request('get',req)
    # print(response.data)
    data=response.data.decode('utf-8')
    data=json.loads(data)
    data=data['feeds']
    return(data)

def preprocessData(data):
    cleandata=[]
    for i in data:
        dummy=[]
        dummy.append(i['created_at'])
        dummy.append(i['entry_id'])
        dummy.append(float(i['field1']))
        dummy.append(float(i['field2']))
        dummy.append(float(i['field3']))
        dummy.append(float(i['field4']))
        dummy.append(float(i['field5'].split('\r\n')[0]))
        cleandata.append(dummy)
    return cleandata


app=Flask(__name__)
app.secret_key='1234'

def connect_with_agriculture(acc):
    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    if acc==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=acc

    artifact_path="./build/contracts/agriculture.json"

    with open(artifact_path) as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']

    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return contract,web3 

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/indexdata',methods=['post','get'])
def indexdata():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    try:
        contract,web3=connect_with_agriculture(0)
        tx_hash=contract.functions.addUser(username,password).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('index.html',res='user added')
    except:
        return render_template('index.html',res="user already added")

@app.route('/logindata',methods=['get','post'])
def logindata():
    username=request.form['username1']
    password=request.form['password1']
    print(username,password)
    contract,web3=connect_with_agriculture(0)
    _usernames,_passwords=contract.functions.viewUsers().call()
    if username not in _usernames:
        return render_template('login.html',err='you dont have any account')
    for i in range(len(_usernames)):
        if(_usernames[i]==username and _passwords[i]==password):
            session['username']=username
            return redirect('/dashboard')
    return render_template('login.html',err='login invalid')

@app.route('/dashboard')
def dashboardPage():
    return render_template('dashboard.html')

@app.route('/model')
def modelPage():
    data=readData()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        value=i[2]
        contract,web3=connect_with_agriculture(0)
        result=contract.functions.precisionForSoilMoisture(int(value)).call()
        if result==1:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[2])
            dummy.append('its a dry')
            dummy.append('Soil lacks sufficient moisture for healthy plant growth')
            dummy.append('Increase irrigation frequency or water application to ensure plants receive adequate moisture. Consider mulching(Growthing Techiniques)to retain soil moisture.')
            mAlerts.append(dummy)
        elif result==2:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[2])
            dummy.append('its a moist')
            dummy.append('Soil moisture is moderate but may require monitoring to prevent waterlogging.')
            dummy.append('Monitor soil moisture regularly to prevent overwatering. Adjust irrigation schedule as needed to maintain optimal moisture levels.')
            mAlerts.append(dummy)
        elif result==3:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[2])
            dummy.append('its a Wet')
            dummy.append('Soil moisture is ideal for most crops.')
            dummy.append('Continue regular monitoring to ensure moisture levels remain within the optimal range. Adjust irrigation as needed based on weather conditions and crop requirements.')
            mAlerts.append(dummy)
        elif result==4:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[2])
            dummy.append('it is a Damp(slightly wet)')
            dummy.append('Soil is quite wet and may lead to waterlogging and root rot.')
            dummy.append('Improve drainage in the field to prevent waterlogging. Reduce irrigation frequency to allow excess moisture to evaporate.')
            mAlerts.append(dummy)
        
    return render_template('alerts.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/model1')
def model1Page():
    data=readData()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        value=i[3]
        contract,web3=connect_with_agriculture(0)
        result=contract.functions.precisionForHumidity(int(value)).call()
        if result==1:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[3])
            dummy.append('Low Humidity')
            dummy.append('Plants may suffer from moisture stress')
            dummy.append('Consider watering more often and providing shade.')
            mAlerts.append(dummy)
        elif result==2:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[3])
            dummy.append('moderate Humidity')
            dummy.append('Conditions are generally suitable for most crops.')
            dummy.append('Monitor humidity regularly to maintain consistency.')
            mAlerts.append(dummy)
        elif result==3:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[3])
            dummy.append('High Humidity')
            dummy.append('Increased risk of fungal diseases.')
            dummy.append('Improve ventilation and avoid overwatering to prevent fungal growth.')
            mAlerts.append(dummy)

    return render_template('alerts1.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/model2')
def model2Page():
    data=readData()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        value=i[4]
        contract,web3=connect_with_agriculture(0)
        result=contract.functions.precisionForTemperature(int(value)).call()
        if result==1:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[4])
            dummy.append('cold')
            dummy.append('Risk of frost damage to sensitive plants.')
            dummy.append('Use frost protection measures like row covers or mulching.')
            mAlerts.append(dummy)
        elif result==2:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[4])
            dummy.append('cool')
            dummy.append('Generally favorable conditions for most crops.')
            dummy.append('Monitor for potential temperature fluctuations and adjust planting schedules accordingly.')
            mAlerts.append(dummy)
        elif result==3:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[4])
            dummy.append('Moderate')
            dummy.append('Optimal temperatures for most crops.')
            dummy.append('Maintain adequate irrigation to prevent stress during warmer periods.')
            mAlerts.append(dummy)
        elif result==4:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[4])
            dummy.append('warm')
            dummy.append('Risk of heat stress in some crops.')
            dummy.append('Provide shading or consider adjusting irrigation to cool plants.')
            mAlerts.append(dummy)
        elif result==5:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[4])
            dummy.append('HOT')
            dummy.append('High risk of heat stress and reduced yields.')
            dummy.append('Implement shading, increase irrigation frequency, and schedule work during cooler parts of the day.')
            mAlerts.append(dummy)

    return render_template('alerts2.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/model3')
def model3Page():
    data=readData()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        value=i[5]
        contract,web3=connect_with_agriculture(0)
        result=contract.functions.precisionForRainfall(int(value)).call()
        if result==1:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[5])
            dummy.append('Light Rain')
            dummy.append('Light rain may not provide sufficient moisture for crops, especially during dry spells.')
            dummy.append('Consider supplemental irrigation if rainfall is insufficient. Monitor soil moisture to ensure adequate hydration for plants.')
            mAlerts.append(dummy)
        elif result==2:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[5])
            dummy.append('Moderate Rain')
            dummy.append('Moderate rain can benefit crops but may cause soil erosion and runoff if intense or prolonged.')
            dummy.append('Implement soil conservation measures like mulching and contour farming to prevent erosion. Monitor drainage to prevent waterlogging.')
            mAlerts.append(dummy)
        elif result==3:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[5])
            dummy.append('Heavy Rain')
            dummy.append('Heavy rain can lead to flooding, soil erosion, and crop damage.')
            dummy.append('Ensure proper drainage to prevent waterlogging. Protect vulnerable crops from physical damage or lodging. Consider terracing or building raised beds in flood-prone areas.')
            mAlerts.append(dummy)
        
    return render_template('alerts3.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/model4')
def model4Page():
    data=readData()
    data=preprocessData(data)
    mAlerts=[]
    for i in data:
        value=i[6]
        contract,web3=connect_with_agriculture(0)
        result=contract.functions.precisionForLightIntensity(int(value)).call()
        if result==1:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[6])
            dummy.append('low light')
            dummy.append('Insufficient light for photosynthesis.')
            dummy.append('Consider supplemental lighting for plants indoors or in shaded areas.')
            mAlerts.append(dummy)
        elif result==2:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[6])
            dummy.append('Moderate Light')
            dummy.append('Suitable light levels for most plants.')
            dummy.append('Monitor for any changes and adjust lighting as needed for optimal growth.')
            mAlerts.append(dummy)
        elif result==3:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[6])
            dummy.append('Bright Light')
            dummy.append('Ideal light levels for many plants.')
            dummy.append('Ensure plants are not exposed to direct sunlight for extended periods to prevent burning.')
            mAlerts.append(dummy)
        elif result==4:
            dummy=[]
            dummy.append(i[0])
            dummy.append(i[1])
            dummy.append(i[6])
            dummy.append('Sunlight')
            dummy.append('Risk of sunburn and heat stress in plants.')
            dummy.append('Provide shade during the hottest part of the day to protect plants from excessive heat and UV radiation.')
            mAlerts.append(dummy)
        
    return render_template('alerts4.html',l1=len(mAlerts),mAlerts=mAlerts)

@app.route('/logout')
def logoutPage():
    session['username']=None
    return redirect('/')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=9001,debug=True)