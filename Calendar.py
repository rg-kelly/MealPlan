from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret_calendar.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
dateFormat = "%Y-%m-%d"

mealCalendarId = 'qn8ga252asppaafdm1doffesh0@group.calendar.google.com'
familyCalendarId = 'family09160014585628777217@group.calendar.google.com'
rachelCalendarId = 'vq9lae4ug7r5s4o2tomc46jih0@group.calendar.google.com'
seanCalendarId = 'q4qejnvvltkce3p4lp60eqnqko@group.calendar.google.com'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(summaryParam = "", date = datetime.datetime.strftime(datetime.datetime.now(), dateFormat), start = "5:30", end = "6:30"):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http, developerKey='complete-road-172122')
    
    currentSummary, events, event = getDinnerEvents(date, checkNonMealCalendars=False, returnEventObject=True)
    newSummaryIsNone = (summaryParam == "")
    defaultExtraReminder = {'useDefault': False, 'overrides': [{'minutes': 540, 'method': 'popup'}, {'minutes': 30, 'method': 'popup'}]}

    if events:
        print(events)
        if newSummaryIsNone:
            print("====== Deleting existing event {} ======".format(summaryParam))
            service.events().delete(calendarId=mealCalendarId, eventId=events[0].get('id', None)).execute()
        else:
            if currentSummary != None and currentSummary != summaryParam:            
                print("====== Updating existing event to {} ======".format(summaryParam))
                event['summary'] = summaryParam
                
                if checkIfMealNeedsExtraReminder(summaryParam):
                    print("************ Adding extra reminder...")
                    event['reminders'] = defaultExtraReminder                
                
                updated_event = service.events().update(calendarId=mealCalendarId, eventId=event['id'], body=event).execute()
                print(updated_event['updated'])
            else:
                print("====== Summary did not change - nothing to do in Calendar ======")        
                
    elif not events and not newSummaryIsNone:
        eventBody = {"summary": summaryParam,
         "start": {"dateTime": "{}T1{}:00-07:00".format(date, start)}, # 7:00 from March to Nov
         "end": {"dateTime": "{}T1{}:00-07:00".format(date, end)}}     # 8:00 from Nov to March (Daylight savings related...)
        
        if checkIfMealNeedsExtraReminder(summaryParam):
            print("************ Adding extra reminder...")
            eventBody['reminders'] = defaultExtraReminder
        
        event = service.events().insert(calendarId=mealCalendarId, body=eventBody).execute()
        print("====== {} event created ======".format(summaryParam))

    elif not events and newSummaryIsNone:
        print("====== No current events and no new summary is provided - nothing to do here ======")
        
    print("\n")
    
def checkIfMealNeedsExtraReminder(mealName):
    extraReminderRecipeList = ["Pulled pork", "Salsa chicken", "Beef roast"]
    
    for recipe in extraReminderRecipeList:
        if mealName.__contains__(recipe):
            return True
        else:
            return False

def getDinnerEvents(currentDate, checkNonMealCalendars = False, returnEventObject = True):
    """ Retrieve events from Google calendars. From personal/social calendar(s), currently just want the summary data
    but from the meal calendar we may also need to have the event object available for updating/deleting.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http, developerKey='complete-road-172122')
    
    minDate = '{}T00:00:00Z'.format(currentDate)
    maxDate = '{}T00:00:00Z'.format(datetime.datetime.strftime(datetime.datetime.strptime(currentDate, dateFormat) + datetime.timedelta(days=1), dateFormat))
    # TODO: Need to adjust timing for Family calendar because it is in UTC tz which is 5 hours ahead of CST..
    returnList = False
    
    if checkNonMealCalendars == False:
        calendarList = [mealCalendarId]
    else:
        calendarList = [familyCalendarId, seanCalendarId, rachelCalendarId]
        summaryList = []
    numberOfCalendars = len(calendarList)
    
    for calendar in calendarList:        
        eventsResult = service.events().list(
            calendarId=calendar, timeMin=minDate, timeMax=maxDate, maxResults=1, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        
        if events:
            event = service.events().get(calendarId=calendar, eventId=events[0].get('id', None)).execute()
            eventSummary = event.get('summary', None)
            
            if numberOfCalendars > 1:
                summaryList.append(eventSummary)
                returnList = True
        else:
            event = None
            eventSummary = None
            
    if returnEventObject:
        return eventSummary, events, event
    elif returnList:
        return " / ".join(summaryList)
    else:
        return eventSummary
    
#if __name__ == '__main__':
    #main()
#summary = getDinnerEvents('2018-07-15', checkNonMealCalendars=True, returnEventObject=False)
#print(summary)