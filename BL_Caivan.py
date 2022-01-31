import requests
import json
import pyodbc 

apiKey = "XXX"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

board_id = "718348165"
#711201285 = Mattamy Homes
#695791534 = Minto
#718348165 = Caivan
#1190887252 = Urbandale

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=LK-SQL03;"
                        "Database=inSight;"
                        "Trusted_Connection=yes;")

cursor = cnxn.cursor()


"""


status3		community	@customerName nvarchar(100) ='Richmond Fox Run Singles'
status82	site		@builder nvarchar(50)= 'Caivan Communities'
dup__of_desired_delivery_date date			@requestDate date = 'sep 15, 2022'
name	  	name	@lot nvarchar(25) = 'Lot 95'
status1		phase	@phase nvarchar(25) = 'Ph 3'
			@block nvarchar(25) 
numbers5	box		@boxCount int = 21
status86    measured			@measured bit = 0
info			@boarditem nvarchar(50) = '718348165-1943399536'
            
            

{'data': {'boards': [{'items': [{'name': 'Lot 95', 'column_values': [{'title': 'Site/Project', 'id': 'status3', 'value': '{"index":3,"post_id":null,"changed_at":"2021-11-24T22:34:33.697Z"}', 'text': 'Richmond Fox Run Singles'}, {'title': 'Builder', 'id': 'status82', 'value': '{"index":104,"post_id":null,"changed_at":"2021-11-24T22:34:35.412Z"}', 'text': 'Caivan Communities'}, {'title': 'Phase', 'id': 'status1', 'value': '{"index":10,"post_id":null,"changed_at":"2021-11-24T22:34:30.063Z"}', 'text': 'Ph 3'}, {'title': 'Model Type', 'id': 'text', 'value': '"OT3603"', 'text': 'OT3603'}, {'title': 'Req OP', 'id': 'people', 'value': None, 'text': ''}, {'title': 'Design Assistant', 'id': 'people2', 'value': None, 'text': ''}, {'title': 'Caivan Designer', 'id': 'people5', 'value': None, 'text': ''}, {'title': 'Req OP Date', 'id': 'date5', 'value': None, 'text': ''}, {'title': 'Appliances', 'id': 'status80', 'value': None, 'text': None}, {'title': 'Customer Upgrade Quote', 'id': 'dup__of_appliances', 'value': None, 'text': None}, {'title': 'Pucklight Plans', 'id': 'status54', 'value': None, 'text': None}, {'title': 'Order Package Completed', 'id': 'dup__of_pucklight_plans', 'value': None, 'text': None}, {'title': 'Builder Email (Rough)', 'id': 'email', 'value': None, 'text': ''}, {'title': 'Measured', 'id': 'status', 'value': None, 'text': ''}, {'title': 'Req. Submit Order', 'id': 'people0', 'value': None, 'text': ''}, {'title': 'Measured Date', 'id': 'date76', 'value': None, 'text': ''}, {'title': 'Final Dwgs', 'id': 'files6', 'value': None, 'text': ''}, {'title': 'Sale Subtotal', 'id': 'numbers9', 'value': None, 'text': ''}, {'title': 'Desired Delivery Date', 'id': 'date3', 'value': None, 'text': ''}, {'title': 'Requested Delivery Date', 'id': 'dup__of_desired_delivery_date', 'value': '{"date":"2022-09-15","changed_at":"2021-12-02T23:19:45.649Z"}', 'text': '2022-09-15'}, {'title': 'Flagged for Pictures', 'id': 'status972', 'value': None, 'text': None}, {'title': 'Submitted to Acct', 'id': 'status7', 'value': None, 'text': None}, {'title': 'Ordered Date', 'id': 'date77', 'value': None, 'text': ''}, {'title': 'Work Order #', 'id': 'text6', 'value': None, 'text': ''}, {'title': 'Corrections for Site', 'id': 'text17', 'value': None, 'text': ''}, {'title': 'Builder Email (Finishing)', 'id': 'email3', 'value': None, 'text': ''}, {'title': 'Construction Admin Email', 'id': 'email_text', 'value': None, 'text': ''}, {'title': 'Send Final Drawings Email', 'id': 'status2', 'value': None, 'text': None}, {'title': 'Delivered', 'id': 'status719', 'value': None, 'text': None}, {'title': 'Delivery Date', 'id': 'date0', 'value': None, 'text': ''}, {'title': 'Check', 'id': 'check', 'value': None, 'text': ''}, {'title': 'Box Count', 'id': 'numbers5', 'value': '"21"', 'text': '21'}, {'title': 'Civic Address', 'id': 'civic_address', 'value': '"601 Terrier Circle"', 'text': '601 Terrier Circle'}, {'title': 'Owner/Head Designer', 'id': 'person', 'value': None, 'text': ''}, {'title': 'Count for Dashboard', 'id': 'numbers7', 'value': '"1"', 'text': '1'}, {'title': 'B Service', 'id': 'button0', 'value': None, 'text': 'Click for B Service'}, {'title': 'Caivan BILLABLE SERVICE Intake', 'id': 'connect_boards6', 'value': None, 'text': ''}, {'title': '*INTERNAL* Caivan - 2021', 'id': 'connect_boards0', 'value': '{"linkedPulseIds":[{"linkedPulseId":1943428004}]}', 'text': 'Lot 95'}, {'title': 'Docs Order Package', 'id': 'mirror_1', 'value': None, 'text': ''}, {'title': 'Acct. $ Sheet', 'id': 'mirror7', 'value': None, 'text': ''}, {'title': 'Insight Forecasting', 'id': 'status86', 'value': '{"index":2,"post_id":null,"changed_at":"2021-11-24T22:43:42.680Z"}', 'text': 'Placeholder'}]}]}]}, 'account_id': 6496421}



"""
def SQLWrite( sname , ssite , scommunity  , sdate , sbox ,  sinfo , sphase, smeasured):
   
    sblock = 'null'
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
        site = GetCV(board_id,cleanItems,'status82')
        site = CleanSite(str(site))
        community = GetCV(board_id,cleanItems,'status3')
        community = CleanText(str(community))
        date = GetCV(board_id,cleanItems,'dup__of_desired_delivery_date')
        date = CleanText(str(date))
        box = GetCV(board_id,cleanItems,'numbers5')
        box = CleanText(str(box))
        if not box:
            box = 'null'
        phase = GetCV(board_id,cleanItems,'status1')
        phase = CleanText(str(phase))
        measured = GetCV(board_id,cleanItems,'status86')
        measured = CleanText(str(measured))
        measured = CheckMeasured(measured)
        if(measured == '1' or measured == '0'):
            #print(name + builder + site + phase + date + box + measured)
            #print(name + site + community  + date + " Box count: " + box +"  ID:"+  board_id +"-"+ cleanItems + phase) 
            SQLWrite(name,site,community,date,box,info,phase,measured)
            #SQLWrite(site,date,name,phase,box,measured,builder,info)
        elif(measured == '2'):
            print("already ordered")
        else:
            print(measured)
    except:
        print("Error " + y)
