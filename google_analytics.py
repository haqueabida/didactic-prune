#!/bin/env python2.7
"""A simple example of how to access the Google Analytics API."""

import argparse

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools




def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """

  f = open(key_file_location, 'rb')
  key = f.read()
  f.close()

  credentials = SignedJwtAssertionCredentials(service_account_email, key,
    scope=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
      property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        # return the first view (profile) id.
        return profiles.get('items')[0].get('id')

  return None


def get_results(service, profile_id):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='7daysAgo',
      end_date='today',
      metrics='ga:sessions').execute()


def print_results(results):
  # Print data nicely for the user.
  if results:
    print 'View (Profile): %s' % results.get('profileInfo').get('profileName')
    print 'Total Sessions: %s' % results.get('rows')[0][0]

  else:
    print 'No results found'


def print_users(results):
    if results:
        print results.get('Custom ')
    else:
        print "None found"

def scopes():
    # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = '509426457680-pfsj9033r8190lhov0flhlcucnoc2418@developer.gserviceaccount.com'
  key_file_location = 'client_secrets.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  profile = get_first_profile_id(service)
  
  return service, profile

"""
Gets all the users Google thinks are new
"""

def get_new_users():
    service, profile_id = scopes()
    return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='today',
      end_date='today',
      metrics='ga:sessions',
      dimensions='ga:userType, ga:dimension1').execute()   

def services():
  service, profile = scopes()
  
  serv = get_new_users()['rows']
  
  #get a list of "new users" per Google Analytics
  new_users = [int(i[1]) for i in serv if i[0]=='New Visitor']
  ret_users = [int(i[1]) for i in serv if i[0]=='Returning Visitor']
  
  return serv, new_users, ret_users

        
"""
Returns the unique
users(new, converted, or returning) of the time period selected
elapsed is defaulted to yesterday, another option is 7daysAgo
or 30daysAgo (whatever number of days you like)

"""
def num_user_sessions(start = 'yesterday', end='yesterday'):
    service, profile = scopes()
    
    data = service.data().ga().get(
    ids='ga:' + profile,
    start_date=start,
    end_date=end,
    metrics='ga:users', dimensions='ga:dimension1').execute()
    
    try:
        num = [int(i[0]) for i in data['rows']]
    except KeyError:
        num = []
        
    return num

#serv = services()
#print serv['rows']
