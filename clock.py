import requests
import json
import smtplib
from time import gmtime, strftime
import os
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

tickets_available = False

# Function to send email alert from Gmail if tickets are found
def send_email():
    print "Hola Mundo"
    #to_list = ['ppinzani89@gmail.com', "salasmezzano@hotmail.com", "maximartine@hotmail.com", "mariano.ulf@gmail.com", "crnicolasfrias@gmail.com"]
    #to = ", ".join(to_list)
    #gmail_user = 'ppinzani89@gmail.com'
    #gmail_pwd = '34767625'
    #smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    #smtpserver.ehlo()
    #smtpserver.starttls()
    #smtpserver.ehlo
    #try:
    #    smtpserver.login(gmail_user, gmail_pwd)
    #    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Entradas Che Culia! \n'
    #    print header
    #    msg = header + '\n Hay entradas. A comprar!!!  http://www.fifa.com/worldcup/organisation/ticketing/purchase.html \n\n'
    #    smtpserver.sendmail(gmail_user, to_list, msg)
    #    smtpserver.close()
    #    print 'done!'
    #except Exception as e:
    #    print e
    #    smtpserver.close()
    #    send_email() # Retry


@sched.scheduled_job('interval', minutes=5)
def send_email_sched():
    if tickets_available:
        send_email()


@sched.scheduled_job('interval', minutes=1)
def get_tickets_available():
    global tickets_available
    tix_data = requests.get("https://tickets.fifa.com/API/WCachedL1/en/BasicCodes/GetBasicCodesAvailavilityDemmand?currencyId=USD" )
    tix = tix_data.text
    tx = json.loads(tix)
    data = tx["Data"]
    avail = data['Availability']

    match1 = [el for el in avail if el["p"] == "IMT23"][0:3] #Arg Croatia
    match2 = [el for el in avail if el["p"] == "IMT39"][0:3] #Arg Nig
    match3 = [el for el in avail if el["p"] == "IMT52"][0:3] #Octavos
    match4 = [el for el in avail if el["p"] == "IMT07"][0:3] #Arg Isl

    match1_av = False
    match2_av = False
    match3_av = False
    match4_av = False

    for el in match1:
        if el["a"] != 0:
            match1_av = True

    for el in match2:
        if el["a"] != 0:
            match2_av = True

    for el in match3:
        if el["a"] != 0:
            match3_av = True

    for el in match4:
        if el["a"] != 0:
            match4_av = True


    if match1_av or match2_av or match3_av or match4_av or True:
        print "Hay Tickets!"
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())

        if not tickets_available:
            send_email()

        tickets_available = True
    else:
        tickets_available = False


sched.start()

