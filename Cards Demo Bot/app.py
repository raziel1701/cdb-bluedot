from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
from cardcontent import *
import smartsheet

app = Flask (__name__)
api = WebexTeamsAPI(access_token="MTRlYzczZGUtMWJlMi00NTNiLWEzOGQtOTZlZTc3MjM2ZWQ2ZDllZGJjNWItZjk2_PF84_3e7c648d-3e3d-4381-80d1-f98e1a0f9d7f")

@app.route('/', methods=['POST','GET'])
def home():
    return 'OK', 200

@app.route('/webhookreq', methods=['POST'])
def webhookreq():
    if request.method == 'POST':
        req = request.get_json()

        data_personId = req['data']['personId']
        data_roomId = req ['data']['roomId']
        
        #Loop prevention VERY IMPORTANT!!!!
        me = api.people.me()
        if data_personId == me.id:
            return 'OK', 200
        else:
            if api.messages.create(roomId=data_roomId, text='Hello World!!!', attachments=[{"contentType": "application/vnd.microsoft.card.adaptive", "content": cardcontent}]):
                return "OK"
    elif request.method == 'GET' :
        return "Yes, this is working."
    return 'OK', 200

@app.route('/cardsubmitted', methods=['POST'])
def cardsubmitted():
    if request.method == 'POST':
        req = request.get_json()

        data_id = req['data']['id']

        attachment_actions = api.attachment_actions.get(data_id)
        inputs = attachment_actions.inputs

        myName = inputs['myName']
        myEmail = inputs['myEmail']
        myTel = inputs['myTel']

        print(myName)
        print(myEmail)
        print(myTel)
        
        smart = smartsheet.Smartsheet('MrwcVMN33exf6DYdtrjWSRkX5hHCGwqYIUw6n') #Smartsheet Access Token
        smart.errors_as_exceptions(True)

        # Specify cell values for the added row                         
        newRow = smartsheet.models.Row()
        newRow.to_top = True
        # The above variables are the incoming JSON
        newRow.cells.append({ 'column_id': 7711445788977028, 'value': myName })                   #  
        newRow.cells.append({ 'column_id': 2081946254763908, 'value': myEmail, 'strict': False })   
        newRow.cells.append({ 'column_id': 6585545882134404, 'value': myTel, 'strict': False }) 
        response = smart.Sheets.add_rows(1697143820969860, newRow) # The -- xxxxxxxxxxxxxx -- on this line is the sheet ID.
    return 'OK', 200

if __name__=='__main__':
    app.debug = True
    app.run(host="0.0.0.0")

