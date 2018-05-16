import requests
import json
import smtplib
from time import gmtime, strftime
from apscheduler.schedulers.blocking import BlockingScheduler
import os

sched = BlockingScheduler()

# Handling Key Import Errors
def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


# Function to send email alert from Gmail if tickets are found
@sched.scheduled_job('interval', minutes=1)
def send_email():
    to_list = ['ppinzani89@gmail.com']
    to = ", ".join(to_list)
    gmail_user = get_env_variable['GMAIL_USER']
    gmail_pwd = get_env_variable['GMAIL_PASS']
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Entradas Che Culia! \n'
    print header
    msg = header + '\n Prueba \n\n'
    smtpserver.sendmail(gmail_user, to_list, msg)
    print 'done!'
    smtpserver.close()


def get_tickets_available(sc):
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

    #for el in match4:
    #    if el["a"] != 0:
    #        match4_av = True


    if match1_av or match2_av or match3_av or match4_av:
        print "Hay Tickets!"
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
        send_email()
        sc.enter(600, 1, get_tickets_available,(sc, ))

    sc.enter(300, 1, get_tickets_available,(sc, ))


sched.start()

## Function to send email alert from Gmail if tickets are found
#def send_email():
#    to_list = ['ppinzani89@gmail.com', "salasmezzano@hotmail.com", "maximartine@hotmail.com", "mariano.ulf@gmail.com", "crnicolasfrias@gmail.com"]
#    to = ", ".join(to_list)
#    gmail_user = 'ppinzani89@gmail.com'
#    gmail_pwd = '34767625'
#    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
#    smtpserver.ehlo()
#    smtpserver.starttls()
#    smtpserver.ehlo
#    smtpserver.login(gmail_user, gmail_pwd)
#    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Entradas Che Culia! \n'
#    print header
#    msg = header + '\n Hay Tickets! A compraar!! \n\n'
#    smtpserver.sendmail(gmail_user, to_list, msg)
#    print 'done!'
#    smtpserver.close()
#
#
#def get_tickets_available(sc):
#    tix_data = requests.get("https://tickets.fifa.com/API/WCachedL1/en/BasicCodes/GetBasicCodesAvailavilityDemmand?currencyId=USD" )
#    tix = tix_data.text
#    tx = json.loads(tix)
#    data = tx["Data"]
#    avail = data['Availability']
#
#    match1 = [el for el in avail if el["p"] == "IMT23"][0:3] #Arg Croatia
#    match2 = [el for el in avail if el["p"] == "IMT39"][0:3] #Arg Nig
#    match3 = [el for el in avail if el["p"] == "IMT52"][0:3] #Octavos
#    match4 = [el for el in avail if el["p"] == "IMT07"][0:3] #Arg Isl
#
#    match1_av = False
#    match2_av = False
#    match3_av = False
#    match4_av = False
#
#    for el in match1:
#        if el["a"] != 0:
#            match1_av = True
#
#    for el in match2:
#        if el["a"] != 0:
#            match2_av = True
#
#    for el in match3:
#        if el["a"] != 0:
#            match3_av = True
#
#    #for el in match4:
#    #    if el["a"] != 0:
#    #        match4_av = True
#
#
#    if match1_av or match2_av or match3_av or match4_av:
#        print "Hay Tickets!"
#        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
#        send_email()
#        sc.enter(600, 1, get_tickets_available,(sc, ))
#
#    sc.enter(300, 1, get_tickets_available,(sc, ))
#
#
#
#s = sched.scheduler(time.time, time.sleep)
#s.enter(300, 1, get_tickets_available,(s, ))
#s.run()
