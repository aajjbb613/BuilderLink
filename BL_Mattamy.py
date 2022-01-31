import requests
import json
import pyodbc 

apiKey = "XXX"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=XXX;"
                        "Database=inSight;"
                        "Trusted_Connection=yes;")

cursor = cnxn.cursor()

board_id = "711201285"
#711201285 = Mattamy Homes
#695791534 = Minto
#718348165 = Caivan
#1190887252 = Urbandale

#Minto (Site/phase = status3),(Phase = status1),(Req Dil Date = date1),(Box count = numbers6 )(name = name)
#When calling for status check text not values... 

def SQLWrite(ssite, sdate, slot, sphase, sbox, smeasured, sbuilder, sinfo):
    SQLQW = "EXECUTE [dbo].[spAPP_utlImportOrderFromMonday_LKL]  @customerName = '"
    SQLQW += ssite
    SQLQW += "' ,@requestDate = '"
    SQLQW += sdate
    SQLQW += "',@lot = '"
    SQLQW += slot
    SQLQW += "',@phase ='"
    SQLQW += sphase
    SQLQW += "',@boxCount = "
    SQLQW += sbox
    SQLQW += ",@measured ="
    SQLQW += smeasured
    SQLQW += ",@builder ="
    SQLQW += sbuilder
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
    Cleanme = Cleanme.split("'text': ",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
    Cleanme = Cleanme.replace("'","")
    Cleanme = Cleanme.replace('"',"")
    return Cleanme

def CleanBuild(Cleanme):
    Cleanme = Cleanme.split("'text': ",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
    Cleanme = Cleanme.replace("' '","'")
    Cleanme = Cleanme.replace("''","'")
    Cleanme = Cleanme.replace('"',"")
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
    
def CleanName(Cleanme):
    Cleanme = Cleanme.split("'name': ",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
    Cleanme = Cleanme.replace("'","")
    Cleanme = Cleanme.replace('"',"")
    return Cleanme
    
def CleanBox(Cleanme):
    Cleanme = Cleanme.split("'column_values': ",1)[1]
    Cleanme = Cleanme.split("}]}]",1)[0]
    Cleanme = Cleanme.replace("[","")
    Cleanme = Cleanme.replace(']',"")
    return Cleanme
    
def CheckMeasured(CheckMe):
    if (CheckMe == 'Measured'):
        return '1'
    elif(CheckMe == 'Placeholder'):
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
        print (info)
        name = GetName(board_id,cleanItems)
        name = CleanName(str(name))
        builder = GetCV(board_id,cleanItems,'status3')
        builder = CleanBuild(str(builder))
        site = GetCV(board_id,cleanItems,'status0')
        site = CleanSite(str(site))
        phase = GetCV(board_id,cleanItems,'status1')
        phase = CleanText(str(phase))
        date = GetCV(board_id,cleanItems,'date1')
        date = CleanText(str(date))
        box = GetCV(board_id,cleanItems,'numbers5')
        box = CleanText(str(box))
        if not box:
            box = 'null'
        measured = GetCV(board_id,cleanItems,'insight_forecasting')
        measured = CleanText(str(measured))
        measured = CheckMeasured(measured)
        if(measured == '1' or measured == '0'):
            #print(name + builder + site + phase + date + box + measured)
            SQLWrite(site,date,name,phase,box,measured,builder,info)
        elif(measured == '2'):
            print("already ordered")
        else:
            print(measured)
    except Exception as e: print(e)
        #print("Error " + y)
        
    
