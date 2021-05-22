import requests
import json
import datetime
from fake_useragent import UserAgent
from time import sleep


temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}

DIST_ID = 247

AGE_GROUP = {18:'18-44',
45:'45+'}


posted = []

while True:
    browser_header = {'User-Agent': temp_user_agent.random}
    msg = 'Vaccination Slot Available'
    count = 0
    DATEOBJ = datetime.date.today()+ datetime.timedelta(days=1)
    DATE = DATEOBJ.strftime('%d-%m-%Y')
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(DIST_ID, DATE)
    response = requests.get(URL, headers=browser_header)
    if response.ok:
        json_data = response.json()
        centers = json_data['sessions']
        for center in centers:
            if center['available_capacity'] > 0 and center['center_id'] not in posted:
                posted.append(center['center_id'])
                count+=1
                msg += '''

{}. Center Name : {}[Age Group : {}]
Address : {}
Pin Code : {}
Date : {}
Type : {}
Charges : Rs.{}
Vaccine Name : {}
Dose Available : {}
Dose 1 : {}
Dose 2 : {}'''.format(count,center['name'],AGE_GROUP[center['min_age_limit']],center['address'],center['pincode'],DATE,center['fee_type'],center['fee'],center['vaccine'],center['available_capacity'],center['available_capacity_dose1'],center['available_capacity_dose2'])
        print('SUCCESS')
    else:
        print('FAILED')
    msg+='\n\nBook Now : https://selfregistration.cowin.gov.in/'
    if count>0:
        tele_res = requests.post('https://api.telegram.org/bot1363999134:AAHd8OkfUhUmFBTbZp5F_gjVvGTsYh1VuUo/sendMessage',data={'chat_id':'@purbisinghbhum','text':msg})
        if tele_res.ok:
            print('POST SUCCESS')
        else:
            print('POST FAILED')
    sleep(3)
    if DATE == datetime.date.today().strftime('%d-%m-%Y'):
        posted.clear()
    




