#!/usr/bin/python

#from __future__ import print_function

import httplib2
import os
import json
import sys

import time
import string
import email
import base64

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from random import randint

from subprocess import Popen

#--------------------------------------------------------------------------
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#--------------------------------------------------------------------------
#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
#CLIENT_SECRET_FILE = 'client_secret.json'

accounts = ['xxxx1.json',
            'xxxx2.json']

FROM_ADDRESS     = 'yyyy@zzzzz.com'
APPLICATION_NAME = 'Gmail API Quickstart'

#--------------------------------------------------------------------------
def get_credentials( client_secret_file ):
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
    #credential_path = os.path.join(credential_dir, 'gmail-quickstart.json')
    credential_path = os.path.join(credential_dir, client_secret_file)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#--------------------------------------------------------------------------
def main():
    
    DEVNULL = open(os.devnull, 'wb')
    
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    for account in accounts:        # Second Example
        print('-------------------------------------------------')
        print('Current account :', account)
        iCurr = 0
    
        credentials = get_credentials(account)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
    
        #
        # search the mail from the current user 'me'
        # and get result in messages
        #    
        results  = service.users().messages().list(userId='me',q='from:'+FROM_ADDRESS+' is:unread').execute()
        messages = results.get('messages', [])
        
        #
        # check message available ?
        #
        if not messages:
            print('No messages found.')
        else:
          #print('Messages:')
          
          #
          # loop for all messages
          #    
          for message in messages:
            
            iCurr = iCurr + 1 
            
            #
            # get message, google email
            #
            msg= service.users().messages().get(userId='me', id=message['id'],format='raw').execute()
            #print(msg['snippet'])
            #print(json.dumps(msg, sort_keys=True, indent=4))
                    
            isTest = False
            
            if isTest == False:
                #
                # get email content
                #
                msg_str  = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
                mime_msg = email.message_from_string(msg_str)
                #bodytext = mime_msg.get_payload()[0].get_payload();
                bodytext = mime_msg.get_payload();
                
                print('Mail {num}: {subject}'.format(num=iCurr,subject=mime_msg['subject']))      
                
                #continue
            
                if type(bodytext) is list:
                    bodytext=','.join(str(v) for v in bodytext)
                    
                #print(msg_str)    
                #print(bodytext)
                #print(msg['snippet'])
                #print(mime_msg['From'])
                
                #
                # split content in a list of line
                #        
                listing = string.split(bodytext, '\n')
                for line in listing:
                    
                    #
                    # if the line begins with http, then we have a url to open in our favorite browser
                    #
                    if line.startswith( 'http' ):
                        # show url on the screen
                        line = line.replace("3D", "")
                        print(line)
                        
                        # open firefox with the given url
                        # redirect errors to /dev/null so that they don't appear on the screen
                        #os.system('firefox -url "' + line + '" 2>/dev/null')
                        with open(os.devnull, "w") as fnull:
                            p = Popen(['firefox', line], stdout=fnull, stderr=fnull) # something long running
        
                        #
                        # we have to wait minimum 40 sec (30 sec + 10 second reserve)
                        # in order to make the surf more "human" we will make a random pause
                        #
                        pause = 40 + randint(1,20)
                        #print('Pause: ' + str(pause))
                        #time.sleep(pause)
                        for i in range(pause,0,-1):
                            #print('tasks done, now sleeping for %d seconds\r' % i)
                            sys.stdout.write('Pause...' + str(i) + ' ')
                            sys.stdout.flush()
                            sys.stdout.write('\r')
                            time.sleep(1)
                        
                        # close firefox and open next url
                        p.terminate()
            
            
            isTest = False
            # set the message as read            
            if isTest == False:
                labelTab = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
                msg2 =  service.users().messages().modify(userId='me', id=message['id'],
                                                         body=labelTab).execute()
                
                msg2 = service.users().messages().trash(userId='me', id=message['id']).execute()
            
            
            #break
        print('\n')
    
#--------------------------------------------------------------------------
if __name__ == '__main__':
    main()

#test34545
