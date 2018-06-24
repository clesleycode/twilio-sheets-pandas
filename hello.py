import pandas as pd
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

def check_registration(number):
	# get most updated spreadsheet
	sheet = client.open("Registrations").sheet1
	list_of_hashes = sheet.get_all_records()
	
	df1 = pd.DataFrame(list_of_hashes)

	return len(df1[df1['Number:'] == number]) != 0


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	body = request.values.get('From', None)

	cleaned_num = int(body[2:])
	resp = MessagingResponse()
	
	if check_registration(cleaned_num):
		resp.message("Congratulations! You registered for DevFest.")
	else: 
		resp.message("You didn't register for DevFest :( But you can here: devfe.st")

	return str(resp)


if __name__ == "__main__":
	app.run(debug=True)
