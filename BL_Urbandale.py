import requests
import json
import pyodbc 

apiKey = "XXX"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

board_id = "1190887252"
#711201285 = Mattamy Homes
#695791534 = Minto
#718348165 = Caivan
#1190887252 = Urbandale

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=XXX;"
                        "Database=inSight;"
                        "Trusted_Connection=yes;")

cursor = cnxn.cursor()


"""
Urbandale ('Site/Project', 'id': 'status3')('Community', 'id': 'status0')(Order By Date', 'id': 'date')('Box Count', 'id': 'numbers89')


status0	community		@customerName nvarchar(100) ='The Creek Towns'
status3	site		@builder nvarchar(50)= 'Urbandale Construction Ltd.'
date6	date		@requestDate date = 'sep 5, 2022'
NAME	name		@lot nvarchar(25) = 'Unit 1'                               
status8	phase		@phase nvarchar(25) = 'Ph 1'                            
status092	block		@block nvarchar(25) = 'Block 1'
numbers89	box		@boxCount int = 17
insight_forecasting	measured		@measured bit = 0
info			@boarditem nvarchar(50) = '1190887252-2035786270'
            
            


{'data': {'boards': [{'items': [{'name': 'Lot 1', 'id': '2035786018', 'column_values': [{'title': 'Builder', 'id': 'status3', 'value': '{"index":0,"post_id":null,"changed_at":"2021-12-20T14:12:55.926Z"}'}, {'title': 'Site/Project', 'id': 'status0', 'value': '{"index":2,"post_id":null,"changed_at":"2021-12-20T14:12:58.592Z"}'}, {'title': 'Phase', 'id': 'status8', 'value': '{"index":0,"post_id":null}'}, {'title': 'Block', 'id': 'status092', 'value': '{"index":5,"post_id":null}'}, {'title': 'Model', 'id': 'model', 'value': None}, {'title': 'Home Owners', 'id': 'text0', 'value': None}, {'title': 'Job Start Received', 'id': 'documents_from_minto', 'value': None}, {'title': 'Ideal Order Date', 'id': 'date', 'value': '{"date":"2022-01-13","changed_at":"2022-01-05T17:09:50.301Z"}'}, {'title': 'Measure', 'id': 'status', 'value': None}, {'title': 'Install Bundles', 'id': 'files', 'value': None}, {'title': 'Sale Subtotal', 'id': 'numbers6', 'value': None}, {'title': 'SOLD', 'id': 'status7', 'value': None}, {'title': 'Order Date', 'id': 'date5', 'value': None}, {'title': 'Days Required for Production', 'id': 'numbers', 'value': '"-60"'}, {'title': 'Requested Delivery Date', 'id': 'date6', 'value': '{"date":"2022-03-14","changed_at":"2022-01-05T17:09:39.901Z"}'}, {'title': 'Days Req Before Closing', 'id': 'numbers2', 'value': '"-30"'}, {'title': 'Closing Date', 'id': 'date7', 'value': '{"date":"2022-04-13","changed_at":"2022-01-05T17:09:18.943Z"}'}, {'title': 'Box Count', 'id': 'numbers89', 'value': '"22"'}, {'title': 'Lot Size', 'id': 'status72', 'value': '{"index":0,"post_id":null}'}, {'title': 'Owner', 'id': 'person', 'value': '{"changed_at":"2021-12-20T14:42:42.355Z","personsAndTeams":[{"id":15486660,"kind":"person"}]}'}, {'title': 'Count for Dashboard', 'id': 'numbers1', 'value': '"1"'}, {'title': 'Insight Forecasting', 'id': 'insight_forecasting', 'value': '{"index":2,"post_id":null,"changed_at":"2022-01-07T16:40:22.891Z"}'}]}, 


"""
def SQLWrite( sname , ssite , scommunity  , sdate , sbox ,  sinfo , sphase, sblock, smeasured):
    SQLQW = "EXECUTE [dbo].[spAPP_utlImportOrderFromMonday_LKL]  @customerName = '"
    SQLQW += scommunity
    SQLQW += "',@builder = '"
    SQLQW += ssite
    SQLQW += "',@requestDate = '"
    SQLQW += sdate
    SQLQW += "',@lot = '"
    SQLQW += sname
    SQLQW += "',@phase ='"
    SQLQW += sphase
    SQLQW += "',@block ='"
    SQLQW += sblock
    SQLQW += "',@boxCount = "
    SQLQW += sbox
    SQLQW += ",@measured ="
    SQLQW += smeasured
    SQLQW += ",@boarditem ='"
    SQLQW += sinfo
    SQLQW += "'"
    print(SQLQW)
   # print("stop")
    cursor.execute(SQLQW)
   # print("hammer time")
    cnxn.commit()


def GetItems(BID): #pass Board ID, returns Item ID
    query = 'query{ boards (ids: '
    query += BID
    query += '){items{id}}}'
    data = {'query' : query}
    r = requests.post(url=apiUrl, json=data, headers=headers) # make request
    x = r.json()
    return x
    
def GetName(BID,ID):
    query = 'query{ boards (ids: '
    query += BID
    query += '){items (ids:'
    query += ID
    query += ') { name }}}'
    data = {'query' : query}
    r = requests.post(url=apiUrl, json=data, headers=headers) # make request
    return (r.json());

def GetCV(BID,ID,CV):
    query = 'query{ boards (ids: '
    query += BID
    query += '){items (ids:'
    query += ID
    query += ') {column_values(ids:'
    query += CV
    query += '){text}}}}'
    data = {'query' : query}
    r = requests.post(url=apiUrl, json=data, headers=headers) # make request
    return (r.json());

def CleanToItemID(jsonLine):
    line = str(jsonLine)
    line = line.split(",")
    return line

def CleanIID(item_ID):
    item_ID = item_ID.split("'id': '", 1)[1]
    item_ID = item_ID.replace("]}]}","")
    item_ID = item_ID.replace("'}","")
    return item_ID
    
def CleanText(Cleanme):
    Cleanme = Cleanme.split("'text':",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
    Cleanme = Cleanme.replace("'","")
    Cleanme = Cleanme.replace('"',"")
    return Cleanme
    
def CleanName(Cleanme):
    Cleanme = Cleanme.split("'name':",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
    Cleanme = Cleanme.replace("'","")
    Cleanme = Cleanme.replace('"',"")
    return Cleanme
    
def CleanBox(Cleanme):
    Cleanme = Cleanme.split("'column_values':",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
    Cleanme = Cleanme.replace("[","")
    Cleanme = Cleanme.replace(']',"")
    return Cleanme
    
def CleanSite(Cleanme):
    Cleanme = Cleanme.split("'text': ",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
   # Cleanme = Cleanme.replace("'","")
    Cleanme = Cleanme.replace('"',"")
    charCheck = "'"
    if (charCheck == Cleanme[0]):
        Cleanme = Cleanme[1:]
    if (charCheck == Cleanme[-1]):
        Cleanme = Cleanme[:-1]
    Cleanme = Cleanme.replace("'s","''s")
    return Cleanme
    
def CheckMeasured(CheckMe):
    if (CheckMe == 'Measured'):
        return '1'
    elif(CheckMe == ' Placeholder'):
        return '0'
    else:
        print(CheckMe)
        return '2'
    
#test main
items = GetItems(board_id)
IID = CleanToItemID(items)
IID.pop()
for y in IID:
    try:
        cleanItems = CleanIID(y)
        info = board_id +"-"+ cleanItems
        print(info)
        name = GetName(board_id,cleanItems)
        name = CleanName(str(name))
        site = GetCV(board_id,cleanItems,'status3')
        site = CleanSite(str(site))
        community = GetCV(board_id,cleanItems,'status0')
        community = CleanText(str(community))
        date = GetCV(board_id,cleanItems,'date6')
        date = CleanText(str(date))
        box = GetCV(board_id,cleanItems,'numbers89')
        box = CleanText(str(box))        
        if not box:
            box = 'null'
        phase = GetCV(board_id,cleanItems,'status8')
        phase = CleanText(str(phase))
        block = GetCV(board_id,cleanItems,'status092')
        block = CleanText(str(block))
        measured = GetCV(board_id,cleanItems,'insight_forecasting')
        measured = CleanText(str(measured))
        measured = CheckMeasured(measured)
        if(measured == '1' or measured == '0'):
            #print(name + builder + site + phase + date + box + measured)
            #print(name + site + community  + date + " Box count: " + box +"  ID:"+  board_id +"-"+ cleanItems + phase + block) 
            SQLWrite(name,site,community,date,box,info,phase,block,measured)
            #SQLWrite(site,date,name,phase,box,measured,builder,info)
        elif(measured == '2'):
            print("already ordered")
        else:
            print(measured)
    except:
        print("Error " + y)
