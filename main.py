#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ['KIVY_IMAGE'] = 'sdl2'
#from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

from threading import Thread
import time
import asyncio
import psutil
import sys
import socket

import kivy
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.utils import platform

from kivy.app import App


import XMPP as NET
import Login as lw
import Contacts as cc


kivy.require("1.11.1")
Config.set('graphics', 'fullscreen', 1)

class Chatlayout(BoxLayout):
    pass


class ChatWinClass(Chatlayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.curr_budd=None
        
        self.chatinputfield= TextInput()
        
        self.inputbar = GridLayout(cols=2, height= self.chatinputfield.height, size_hint_y=None)

        self.sendbutton = Button(text="Send")

        self.inputbar.add_widget(self.chatinputfield)
        self.inputbar.add_widget(self.sendbutton)
        self.add_widget(self.inputbar)



####################################################################
#################### Build app SCREENS ##############################   

class NohaChatApp(App):

    def build(self):
        if platform not in ('android', 'ios'):
            self.resource = socket.gethostname()
            Window.size = (500, 700)
        else:
            Window.size = Window.system_size

        Window.clearcolor = (1, 1, 1, 1)
        Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
        Window.softinput_mode='below_target'

        self.icon = 'Images/Nohachat.png' #app logo

################# Server Paramteres#####################
        self.xmpp = None
        self.state = 'signout'
        self.serverstate = 'run'
        self.serverstate_action = 'nothing'

################# Threads#####################
        self.serverthread = Thread(target=self.Run_Server, daemon=True)
        self.serverthread.start()

################# Scheduler#####################
        Clock.schedule_interval(self.scheduler, 5)

################ Notification #################

        self.notification = False

################# Screen manager #####################
        self.screen_manager = ScreenManager()

        self.Loginpage = lw.LoginWinClass()
        self.loginscreen = Screen(name = "NohaChatLogin")
        self.loginscreen.add_widget(self.Loginpage)

        self.Chatpage = ChatWinClass()
        self.chatscreen = Screen(name = "Chat")
        self.chatscreen.add_widget(self.Chatpage)

        self.Contactspage = cc.ChatWinContacts()
        self.contactsscreen = Screen(name = "Contacts")
        self.contactsscreen.add_widget(self.Contactspage)

        self.screen_manager.add_widget(self.loginscreen)
        self.screen_manager.add_widget(self.chatscreen)
        self.screen_manager.add_widget(self.contactsscreen)

########### LOGIN window BIND USER ACTION to FUNC ################
        self.Loginpage.Loginbutton.bind(on_release=self.CheckAuth)

#############  BIND CHATPAGE BUTTON ACTION to FUNCTIONS ################
####################################################################
        self.Chatpage.sendbutton.bind(on_release=self.send_message) # Binding to XMPP server

        self.Chatpage.ids.back.bind(on_release=self.gotoContactsWindow2)

        return self.screen_manager
        #return ChatWinClass()



################### SCREEN Request Function ######################
######################################################################
    def on_memorywarning(self):
        print("Memory warning")


    def gotoContactsWindow(self, _):
        print('Checkpoint- gotoContactsWindow')
        self.request_window(window_req='Contacts', curr_window= "Chat")

    def logout_from_Chat(self,_):
        print('Checkpoint- logout_from_Chat')

        self.request_window("NohaChatLogin", "Contacts")

    def request_window(self, window_req, curr_window):
        print('Checkpoint- request_window \n')
        if curr_window == "NohaChatLogin" and window_req == "Contacts"  :
            self.screen_manager.current= "Contacts"
            self.Loginpage.layout.remove_widget(self.Loginpage.loadingwid) # remove loading animation
            self.state = 'contacts' 


        elif curr_window == "Contacts" and window_req == "NohaChatLogin"  :  #Change Page from Chatting Window to Login page
            self.screen_manager.current="NohaChatLogin"
            self.state='signout'
            self.signout()
            self.Contactspage.Clear_Contacts()
            #We will not join thread because we may sign in again.

        elif curr_window == "Chat" and window_req == "Contacts"  :  #Change Page from Chat window to Contacts
            self.screen_manager.current="Contacts" 
            self.state='contacts'

        elif curr_window == "Contacts" and window_req == "Chat"  :  #Change Page from Contacts to Chat Window
            self.screen_manager.current="Chat" 
            self.state='chat_window'


################################################################


    def CheckAuth(self,_):
        print('Checkpoint - Check Auth')
        if self.state== "signout":
            self.Loginpage.notify.opacity=0
            username= self.Loginpage.usernameTI.text
            
            if username=='':
                self.Loginpage.notify.opacity=0.8
                return 0

            else:
                server= username.find("@")
                if server== -1:
                    return 0
                    #username = username+"@insert server names here.com"
       
                self.Loginpage.layout.add_widget(self.Loginpage.loadingwid) #Show Loading animation.
                self.Connect(username, self.Loginpage.passwordTI.text)
                

 



#################################################################
################## Attempt USER LOGIN #####################
    def Connect(self, JID, Password):
        print('Checkpoint - Connect', JID, Password)
        if self.state == 'signout':
            self.state = 'trylogin'
            self.xmpp=None

            self.xmpp= NET.ClientH(JID+"/"+self.resource, Password)

            self.xmpp.register_plugin('xep_0030') # Service Discovery
            self.xmpp.register_plugin('xep_0199') #XMPP Ping
            self.xmpp.register_plugin('xep_0004') # Data Forms
            self.xmpp.register_plugin('xep_0060') # PubSub
            self.xmpp.register_plugin('xep_0085') # Chat states

            #self.ssl_version = ssl.PROTOCOL_SSLv23

            self.xmpp.add_event_handler('session_start', self.serverstatus)
            self.xmpp.add_event_handler('session_start', self.gotoContactsWindow2)
            self.xmpp.add_event_handler('message', self.receive_message)
            self.xmpp.add_event_handler('connection_failed', self.login_failed)
            self.xmpp.add_event_handler('failed_auth', self.login_failed)

            self.xmpp.connect()
            self.serverstate_action= 'try login'




    def gotoContactsWindow2(self, event):
        print('Checkpoint- gotoContactsWindow')
        self.request_window(window_req='Contacts', curr_window= "NohaChatLogin")


##############################################################################################################
###################### DISPLAY CONTACTS IN THE LEFT SIDE BAR#############################################
    def display_roaster(self):
        print ('Checkpoint - Display_Roster')

        if self.xmpp is not None:

            if self.xmpp.FLAG_contacts_update==1:

                groups = self.xmpp.client_roster.groups()
                for group in groups:
                    for jid in groups[group]:

                        if jid == self.xmpp.boundjid:
                            break
                        
                        username=str(jid).split('@',1)[0]
                        displayname = self.xmpp.client_roster[jid]['name']
                        
                        if displayname:
                            name = displayname
                        else:
                            name = username

                        # Pointer to chat history
                        self.Contactspage.contacts_wid[jid] =  cc.Contacts_ChatHistory()
                        self.Contactspage.contacts_wid[jid].text = name
                        self.Contactspage.contacts_wid[jid].set_jid(jid)
                        self.Contactspage.contacts_wid[jid].bind(on_press=lambda pntrto_wid: self.actv_contact(pntrto_wid))
                        
                        self.Contactspage.display_roster_contact(self.Contactspage.contacts_wid[jid])
                        
                        self.Contactspage.contactnameJID[name] = jid

                self.xmpp.FLAG_contacts_update =0

            else:
                pass



##############################################################################################################
####################### Which Buddy was user chatting with, Which buddy does user wants to chat with#########

    def actv_contact(self, pntrto_chathistory):
        print('\nCheckpoint - actv_contact \n')
        ##### Uses pointer to Contact Widget. Class refered is Contacts_ChatHistory
        ##### Uses ChatPage add / remove widgets
        ##### 
        jid2=pntrto_chathistory.get_jid()
        print ("Jid :", jid2)
        print ("I enter function and the buddy is: ", self.Chatpage.curr_budd)

        if self.Chatpage.curr_budd == None:
            print("current buddy = None")

        else: ##page was another friend chat
            print("Active Page was  friend chat") #remove widget of friend
            pointertoChatHistory = self.Contactspage.contacts_wid[self.Chatpage.curr_budd]
            self.Chatpage.ids.scroll.remove_widget(pointertoChatHistory.history)

        if pntrto_chathistory.get_history() is not None: #chat widget was created already(active chat session) for clicked contact? if yes
            print("actv_contacty history exists")
            self.Chatpage.ids.scroll.add_widget(pntrto_chathistory.history)

        else: #If no
            print("actv_contacty history does not exist") # No current chat session
            pntrto_chathistory.create_history()
            self.Chatpage.ids.scroll.add_widget(pntrto_chathistory.history)
            self.Chatpage.ids.contactname.text=pntrto_chathistory.text


        jid=pntrto_chathistory.get_jid()
        self.Chatpage.curr_budd= jid

        print("active_contact - jid:", jid)

        ############go to chat window after clicking on a contact, and their chat history is loaded
        self.request_window(window_req='Chat', curr_window= "Contacts")

                    
 ################################################################ 

    def serverstatus(self,_):
        print ('server running')
        self.serverstate_action='run'

    def send_message(self, _):
        if self.Chatpage.curr_budd !=None:

            JID_bare= self.Chatpage.curr_budd
            Cntct_hstry_wid = self.Contactspage.contacts_wid[JID_bare]


            self.xmpp.SendMsg(JID_bare, self.Chatpage.chatinputfield.text) #send message through server
            Cntct_hstry_wid.Sender_chat_bubble(textmsg=self.Chatpage.chatinputfield.text)
            self.Chatpage.chatinputfield.select_all()
            self.Chatpage.chatinputfield.delete_selection()


    def receive_message(self, msg):
        print("Checkpoint - Recive MSG")
        print("Message recieved ", msg)
        try:
            if msg['type'] in ('normal', 'chat'):
                print("MSG in Normal Chat")
                msgstr= str(msg['body'])
                JID_bare= str(msg['from'])
                if JID_bare.find('/') != 1:  ######### Update the history of the person
                    jidtemp=JID_bare.split('/',1)[0]

                    if jidtemp in self.Contactspage.contacts_wid: #Person is in my contacts list
                        print("Contact is in my list")
                        Contact_Message_History = self.Contactspage.contacts_wid[jidtemp]
                        print("I point to contact")
                        if Contact_Message_History.history==None:
                            Contact_Message_History.create_history()
                            print("History created")
                        else:
                            print("Call Sender_chat_bubble")
                            Contact_Message_History.Sender_chat_bubble(textmsg=msgstr, position='left')
                            Contact_Message_History.secondary_text=msgstr[:15] + "..."
                                                    
                    else:
                        print("Contact not in my contactslist")
                        
                else:
                    print ("Error too many @ or no @")
                    
            else:
                print("message of non chat type received")
                
        except Exception as error:
            print(error)
            print('Error caught:', sys.exc_info())
            
        return 0


    def login_failed(self,event):
        print('Check point - login failed, check internet')
        self.state= "signout"
        self.Loginpage.layout.remove_widget(self.Loginpage.loadingwid) # remove loading animation
        self.Logingpage.notify.opacity=1
        self.xmpp.loop.call_soon_threadsafe(self.xmpp.disconnect)


################## A Scheduler #####################
######################################################
    def scheduler(self, dt):
        if self.state=='contacts':
            if self.xmpp.FLAG_contacts_update==1:
                self.display_roaster()
            self.xmpp.send_presence()

        #print('CPU load: %s Memory Usage:  %s' %(psutil.cpu_percent(), psutil.virtual_memory()[2]) )
        

 ################################################################ 



 ################## XMPP SERVER processing Thread #####################
######################################################################              
    def Run_Server(self):
        while self.serverstate=='run':
            if self.serverstate_action== 'try login' and self.xmpp is not None:
                print('attempt server processing')
                self.xmpp.process(forever=False)

                self.serverstate_action= 'failed' #xmpp.process has exit due to disconnect or failure
                print ('Server processing terminated')



################################################################




 ################## On Exit Window (user press X) #####################
######################################################################  
    def on_stop(self):
        self.serverstate='off'#Stops the while loop in thread to get ready for join.
        self.signout()
        print('thread status1: ', self.serverthread.is_alive())
        print('xmpp status=', self.serverstate_action)

        if self.serverstate_action != 'try login':
            self.serverthread.join() #thread join

        else: ### We are stuck is xmpp.process
            self.xmpp.loop.call_soon_threadsafe(self.xmpp.abort)
            print('abort tried- onstop')
            if self.serverthread.is_alive()== True:
                self.xmpp.loop.call_soon_threadsafe(self.xmpp.loop.stop)
                print('stop tried- onstop')
            if self.serverthread.is_alive()== True:
                self.xmpp.loop.call_soon_threadsafe(self.xmpp.loop.close)
                print('close tried- onstop')
            if self.serverthread.is_alive()== True:
                print('join  tried- onstop')
                self.serverthread.join()

        print('thread status2: ', self.serverthread.is_alive())
        print ('disconnected from on_Stop')


################################################################

 ################## On Pause/Resume Window (Applicable to Phones only) #####################
######################################################################  
    def on_pause(self):
        self.notification = True
        return True

    def on_resume(self):
        self.notification = False

#######################################


################## SIGNOUT XMPP #####################
######################################################################  
    def signout(self):
        self.state= "signout"
        if self.xmpp is not None: #xmpp instance is defined
            print('xmpp is not None- signout')
            self.xmpp.loop.call_soon_threadsafe(self.xmpp.disconnect) #xmpp.process will return
            if self.serverthread.is_alive()== False: # Is xmpp.process really returns
                self.xmpp = None
                print ('thead stopped, XMPP is now None')
            else:
                print('xmpp.process didnt return, thread alive..')
        else:
            print('xmpp is None- signout')
            pass
################################################################


####################### RUN APP/main thread################################################
###################################################################################
if __name__ == '__main__': 
    try:
        chat_app = NohaChatApp()    ## Create GUI app
        chat_app.run()

    except Exception as error:
        print("Something is wrong")
        print(error)
        print('Error caught:', sys.exc_info())
        chat_app.serverstate='off' #Stops the while loop in thread to get ready for join.
        if chat_app.xmpp is not None and chat_app.serverthread.is_alive()== True:
            print('xmpp is not None- exception')
            chat_app.xmpp.loop.call_soon_threadsafe(chat_app.xmpp.disconnect) #xmpp.process will return
            chat_app.serverthread.join() #thread join
            chat_app.xmpp = None
            #chat_app.xmpp.loop.call_soon_threadsafe(chat_app.xmpp.loop.stop)

        elif chat_app.xmpp is None and chat_app.serverthread.is_alive()== True:
            chat_app.serverthread.join() #thread join

        print('xmpp is None- exception, ', chat_app.xmpp)
        print('thread status: ', chat_app.serverthread.is_alive())
        print ('disconnected from Exception')
            






