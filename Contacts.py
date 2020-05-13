
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty, StringProperty
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import Line
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import sp, dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from kivy.factory import Factory



#############Chat Bubble #################

class chatbubblelabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_texture_size(self,*args):
        if Window.width*0.9 < self.texture_size[0]:
            self.width= Window.width*0.9
            self.text_size = (Window.width*0.9, None)
        else:
            self.width = self.texture_size[0]

        self.height = self.texture_size[1]



################ Update sticker


class Messages(BoxLayout):
    pass



class Contacts_ChatHistory(Button):
    def __init__(self, **kwargs):
        super(Contacts_ChatHistory, self).__init__(**kwargs)
        self.jid=None
        self.history =None
        self.secondary_text=None

    def set_jid(self, input_jid):
        self.jid=input_jid
        

    def get_jid(self):
        print('you pointed to the widget  ', self.jid)
        return self.jid

    def create_history(self):
        self.history = Messages()


    def get_history(self):
        return self.history

    def Sender_chat_bubble(self, position='right', textmsg=''):
        print('Checkpoint - Sender chat bubble \n')
        string= str(textmsg)
        if string.isspace()==True:
            return 0
        chatbubble = chatbubblelabel(text=textmsg, pos_hint= {position: 1})

        self.Expand_Scroll_View(chatbubble)


    def Expand_Scroll_View(self, message):
        print('Checkpoint - Expand_Scroll_View \n')
        message.texture_update()
        scroll_to_point = message

        self.history.add_widget(scroll_to_point)




class ChatWinContacts(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.contacts_wid={} # list of all JID and their associated chat widget with history
        self.contactnameJID= {} # list of all contact names and their associated JID

 
    def display_roster_contact(self, contactbutton):
        self.ids.container.add_widget(contactbutton)




'''
class chatnaoapp(App):
    def build(self):
        self.ContactsPage = ChatWinContacts()
        self.contactsscreen = Screen(name = "Contacts")
        self.contactsscreen.add_widget(self.ContactsPage)


        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(self.contactsscreen)

        return self.screen_manager



chatnaoapp().run()
'''
