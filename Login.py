# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import NumericProperty

test = 'true'

class Loading(FloatLayout):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Loading, self).__init__(**kwargs)
        anim = Animation(angle = 360, duration=2)
        anim += Animation(angle = 360, duration=2)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0



class LoginWinClass(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

################### Create some widgets
        self.loadingwid = Loading()
        self.notify = Label(text='[color=425159]Login failed, check your login details, or verify connection[/color]', \
            opacity=0, markup=True)
        self.forget = Label(text='[color=425159]Forgot password[/color]', opacity=0.8, markup=True)

############# LAYOUT

        self.layout = BoxLayout(size_hint_y = 1, orientation = 'vertical', spacing='10dp')

############ LOGO

        self.logo = Image(source='NohaChat2.png', height='200', size_hint_y=None)

########### LINE 1

        self.UNLabel = Label(text='[color=425159]User Name[/color]', markup=True, font_size= "15sp")

        self.usernameTI = TextInput(multiline=False,
            size_hint=(0.8,None), pos_hint={"center_x":0.5,"center_y":0.5})

        self.layout.add_widget(self.logo)
        self.layout.add_widget(self.UNLabel)
        self.layout.add_widget(self.usernameTI)

########### LINE 2
        self.PASLabel = Label(text='[color=425159]Password[/color]', markup=True, font_size= "15sp")

        self.passwordTI = TextInput(password=True, multiline=False, size_hint=(0.8,None), pos_hint={"center_x":0.5,"center_y":0.5})

        self.layout.add_widget(self.PASLabel)
        self.layout.add_widget(self.passwordTI)


########### LINE 3
        self.Loginbutton = Button(text='[color=425159]Login[/color]', pos_hint={"center_x":0.5,"center_y":0.5}, markup=True,  background_normal='',
        background_color=( 1, .3, .4, .85), size_hint_x=0.2)

        self.layout.add_widget(self.Loginbutton)
        Fillsspace3 = Label(height=10, size_hint=(None,None))
        self.layout.add_widget(Fillsspace3)
        #self.layout.add_widget(self.loadingwid) #Show Loading animation for testing
        self.layout.add_widget(self.forget)
        self.Fillsspace4 = Label(height=5, size_hint=(None,None))
        self.layout.add_widget(self.Fillsspace4)
        self.layout.add_widget(self.notify)  ### Add notify text that appears in case of failed login. opacity =0 to hide for now


########### ADD to Window

        Fillsspace1 = Label(size_hint=(None,None))
        Fillsspace2 = Label(size_hint=(None,None))

        self.add_widget(Fillsspace1)
        self.add_widget(self.layout)
        self.add_widget(Fillsspace2)


 #### UNCOMMENT TO ONLY TEST THIS PAGE#####     

if test == 'true':
    class NohaChat(App):

        def build(self):
            return LoginWinClass()


    if __name__ == '__main__':
        NohaChat().run()

