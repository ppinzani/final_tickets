import requests
import json
import smtplib
from time import gmtime, strftime
import os
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

tickets_available = False

matches_tocheck = ["IMT23", "IMT39", "IMT52", "IMT07"] # List of matches to check FIXME
to_email_list = ['example@gmail.com'] # List of dest emails FIXME

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except:
        return ""


# Function to send email alert from Gmail if tickets are found
def send_email():
    to = ", ".join(to_email_list)
    gmail_user = get_env_variable('GMAIL_USER') # Source email username FIXME
    gmail_pwd = get_env_variable('GMAIL_PASS') # Source email password FIXME
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    try:
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Tickets Available! \n'
        msg = header + '\n There are tickets available!!!  http://www.fifa.com/worldcup/organisation/ticketing/purchase.html \n\n'
        smtpserver.sendmail(gmail_user, to_email_list, msg)
        smtpserver.close()
    except:
        smtpserver.close()
        send_email() # Retry


@sched.scheduled_job('interval', minutes=5)
def send_email_sched():
    if tickets_available and get_env_variable('SEND_EMAIL') == 'YES':
        send_email()


@sched.scheduled_job('interval', minutes=1)
def get_tickets_available():
    global tickets_available
    tix_data = requests.get("https://tickets.fifa.com/API/WCachedL1/en/BasicCodes/GetBasicCodesAvailavilityDemmand?currencyId=USD" )
    tix = tix_data.text
    tx = json.loads(tix)
    data = tx["Data"]
    avail = data['Availability']

    matches_availability = []

    for match in matches_tocheck:
        matches_availability.append([el for el in avail if el["p"] == match][0:3])

    matches_available = []

    for ind, match_av in enumerate(matches_availability):
        for el in match_av:
            if el["a"] != 0:
                matches_available.append(matches_tocheck[ind])


    if len(matches_available) > 0: #If there is at least one match available
        if not tickets_available:
            send_email()

        tickets_available = True
    else:
        tickets_available = False


sched.start()

