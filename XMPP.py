#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of Slixmpp.
    See the file LICENSE for copying permission.
"""


import logging
from getpass import getpass
import ssl
import slixmpp
import asyncio
import time
from slixmpp.exceptions import IqError, IqTimeout

from slixmpp.plugins.base import PluginManager, PluginNotFound, BasePlugin
from slixmpp.plugins.base import register_plugin, load_plugin



from slixmpp.plugins.xep_0004.stanza import Form
from slixmpp.plugins.xep_0004.stanza import FormField, FieldOption
from slixmpp.plugins.xep_0004.dataforms import XEP_0004
register_plugin(XEP_0004)

from slixmpp.plugins.xep_0009 import stanza
from slixmpp.plugins.xep_0009.rpc import XEP_0009
from slixmpp.plugins.xep_0009.stanza import RPCQuery, MethodCall, MethodResponse
register_plugin(XEP_0009)
from slixmpp.plugins.xep_0012.stanza import LastActivity
from slixmpp.plugins.xep_0012.last_activity import XEP_0012
register_plugin(XEP_0012)

from slixmpp.plugins.xep_0013.stanza import Offline
from slixmpp.plugins.xep_0013.offline import XEP_0013

register_plugin(XEP_0013)
from slixmpp.plugins.xep_0016 import stanza
from slixmpp.plugins.xep_0016.stanza import Privacy
from slixmpp.plugins.xep_0016.privacy import XEP_0016

register_plugin(XEP_0016)
from slixmpp.plugins.xep_0020 import stanza
from slixmpp.plugins.xep_0020.stanza import FeatureNegotiation
from slixmpp.plugins.xep_0020.feature_negotiation import XEP_0020

register_plugin(XEP_0020)
from slixmpp.plugins.xep_0027.stanza import Signed, Encrypted
from slixmpp.plugins.xep_0027.gpg import XEP_0027


register_plugin(XEP_0027)


from slixmpp.plugins.xep_0030 import stanza
from slixmpp.plugins.xep_0030.stanza import DiscoInfo, DiscoItems
from slixmpp.plugins.xep_0030.static import StaticDisco
from slixmpp.plugins.xep_0030.disco import XEP_0030

register_plugin(XEP_0030)

from slixmpp.plugins.xep_0033 import stanza
from slixmpp.plugins.xep_0033.stanza import Addresses, Address
from slixmpp.plugins.xep_0033.addresses import XEP_0033


register_plugin(XEP_0033)

from slixmpp.plugins.xep_0047 import stanza
from slixmpp.plugins.xep_0047.stanza import Open, Close, Data
from slixmpp.plugins.xep_0047.stream import IBBytestream
from slixmpp.plugins.xep_0047.ibb import XEP_0047


register_plugin(XEP_0047)

from slixmpp.plugins.xep_0048.stanza import Bookmarks, Conference, URL
from slixmpp.plugins.xep_0048.bookmarks import XEP_0048


register_plugin(XEP_0048)

from slixmpp.plugins.xep_0049.stanza import PrivateXML
from slixmpp.plugins.xep_0049.private_storage import XEP_0049


register_plugin(XEP_0049)
from slixmpp.plugins.xep_0050.stanza import Command
from slixmpp.plugins.xep_0050.adhoc import XEP_0050


register_plugin(XEP_0050)

from slixmpp.plugins.xep_0054.stanza import VCardTemp
from slixmpp.plugins.xep_0054.vcard_temp import XEP_0054


register_plugin(XEP_0054)

from slixmpp.plugins.xep_0059.stanza import Set
from slixmpp.plugins.xep_0059.rsm import ResultIterator, XEP_0059


register_plugin(XEP_0059)


from slixmpp.plugins.base import register_plugin

from slixmpp.plugins.xep_0060.pubsub import XEP_0060
from slixmpp.plugins.xep_0060 import stanza


register_plugin(XEP_0060)


from slixmpp.plugins.xep_0065.socks5 import Socks5Protocol
from slixmpp.plugins.xep_0065.stanza import Socks5
from slixmpp.plugins.xep_0065.proxy import XEP_0065


register_plugin(XEP_0065)


from slixmpp.plugins.xep_0066 import stanza
from slixmpp.plugins.xep_0066.stanza import OOB, OOBTransfer
from slixmpp.plugins.xep_0066.oob import XEP_0066


register_plugin(XEP_0066)

from slixmpp.plugins.xep_0070.stanza import Confirm
from slixmpp.plugins.xep_0070.confirm import XEP_0070

register_plugin(XEP_0070)

from slixmpp.plugins.xep_0071.stanza import XHTML_IM
from slixmpp.plugins.xep_0071.xhtml_im import XEP_0071


register_plugin(XEP_0071)

from slixmpp.plugins.xep_0077.stanza import Register, RegisterFeature
from slixmpp.plugins.xep_0077.register import XEP_0077


register_plugin(XEP_0077)

from slixmpp.plugins.xep_0078 import stanza
from slixmpp.plugins.xep_0078.stanza import IqAuth, AuthFeature
from slixmpp.plugins.xep_0078.legacyauth import XEP_0078


register_plugin(XEP_0078)

from slixmpp.plugins.xep_0079.stanza import (
        AMP, Rule, InvalidRules, UnsupportedConditions,
        UnsupportedActions, FailedRules, FailedRule,
        AMPFeature)
from slixmpp.plugins.xep_0079.amp import XEP_0079


register_plugin(XEP_0079)

from slixmpp.plugins.xep_0080.stanza import Geoloc
from slixmpp.plugins.xep_0080.geoloc import XEP_0080


register_plugin(XEP_0080)

from slixmpp.plugins.xep_0084 import stanza
from slixmpp.plugins.xep_0084.stanza import Data, MetaData
from slixmpp.plugins.xep_0084.avatar import XEP_0084


register_plugin(XEP_0084)

from slixmpp.plugins.xep_0085.stanza import ChatState
from slixmpp.plugins.xep_0085.chat_states import XEP_0085


register_plugin(XEP_0085)

from slixmpp.plugins.xep_0086.stanza import LegacyError
from slixmpp.plugins.xep_0086.legacy_error import XEP_0086


register_plugin(XEP_0086)

from slixmpp.plugins.xep_0091 import stanza
from slixmpp.plugins.xep_0091.stanza import LegacyDelay
from slixmpp.plugins.xep_0091.legacy_delay import XEP_0091


register_plugin(XEP_0091)

from slixmpp.plugins.xep_0092 import stanza
from slixmpp.plugins.xep_0092.stanza import Version
from slixmpp.plugins.xep_0092.version import XEP_0092


register_plugin(XEP_0092)

from slixmpp.plugins.xep_0095 import stanza
from slixmpp.plugins.xep_0095.stanza import SI
from slixmpp.plugins.xep_0095.stream_initiation import XEP_0095


register_plugin(XEP_0095)

from slixmpp.plugins.xep_0096 import stanza
from slixmpp.plugins.xep_0096.stanza import File
from slixmpp.plugins.xep_0096.file_transfer import XEP_0096


register_plugin(XEP_0096)


from slixmpp.plugins.xep_0107 import stanza
from slixmpp.plugins.xep_0107.stanza import UserMood
from slixmpp.plugins.xep_0107.user_mood import XEP_0107


register_plugin(XEP_0107)


from slixmpp.plugins.xep_0108 import stanza
from slixmpp.plugins.xep_0108.stanza import UserActivity
from slixmpp.plugins.xep_0108.user_activity import XEP_0108


register_plugin(XEP_0108)

from slixmpp.plugins.xep_0115.stanza import Capabilities
from slixmpp.plugins.xep_0115.static import StaticCaps
from slixmpp.plugins.xep_0115.caps import XEP_0115


register_plugin(XEP_0115)#


from slixmpp.plugins.xep_0122.stanza import FormValidation
from slixmpp.plugins.xep_0122.data_validation import XEP_0122


register_plugin(XEP_0122)

from slixmpp.plugins.xep_0118 import stanza
from slixmpp.plugins.xep_0118.stanza import UserTune
from slixmpp.plugins.xep_0118.user_tune import XEP_0118



register_plugin(XEP_0118)

from slixmpp.plugins.xep_0131 import stanza
from slixmpp.plugins.xep_0131.stanza import Headers
from slixmpp.plugins.xep_0131.headers import XEP_0131


register_plugin(XEP_0131)


from slixmpp.plugins.xep_0199.stanza import Ping
from slixmpp.plugins.xep_0199.ping import XEP_0199
register_plugin(XEP_0199)

from slixmpp.features.feature_starttls.starttls import FeatureSTARTTLS
from slixmpp.features.feature_starttls.stanza import *
from slixmpp.features.feature_session.session import FeatureSession
from slixmpp.features.feature_session.stanza import Session
from slixmpp.features.feature_rosterver.rosterver import FeatureRosterVer
from slixmpp.features.feature_rosterver.stanza import RosterVer
from slixmpp.features.feature_bind.bind import FeatureBind
from slixmpp.features.feature_bind.stanza import Bind
from slixmpp.features.feature_preapproval.preapproval import FeaturePreApproval
from slixmpp.features.feature_preapproval.stanza import PreApproval
from slixmpp.features.feature_mechanisms.mechanisms import FeatureMechanisms
from slixmpp.features.feature_mechanisms.stanza import Mechanisms
from slixmpp.features.feature_mechanisms.stanza import Auth
from slixmpp.features.feature_mechanisms.stanza import Success
from slixmpp.features.feature_mechanisms.stanza import Failure



class ClientH(slixmpp.ClientXMPP):

    """
    A basic Slixmpp bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)


        self.FLAG_contacts_update=0

        self.received = set()
        self.presences_received = asyncio.Event()

        self.add_event_handler("session_start", self.start)
        #self.add_event_handler('message', self.Recv_message)
        self.add_event_handler("changed_status", self.wait_for_presences)
        self.add_event_handler('connected', self.connected)
        self.add_event_handler('connection_failed', self.connected_fail)
        self.add_event_handler('failed_auth', self.auth_failed)


        #on event fire message function

    def auth_failed(self, event):
        print('XMPP File - Sorry wrong username or password')

    def connected_fail(self, event):
        print('XMPP File - Sorry I couldnt connect to server')

    def connected(self, event):
        print('XMPP File - Connected to Server')



################## Session Start Event #####################
#########################################################
    async def start(self, event):

        print('XMPP File - Session Started!!')

        future = asyncio.Future()

        def callback(result):
            future.set_result(None)
        try:
            self.get_roster(callback=callback)
            await future
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('XMPP File - Error: Request timed out')

        self.send_presence()

        self.FLAG_contacts_update=1

#########################################################

    def ChatSession(self, recipient):
        # Start chatsession wih contact

        self.send_message(mto=recipient,
                          mbody=message,
                          mtype='chat')
    
    def SendMsg(self, recipient, message):
        # The message we wish to send, and the JID that
        # will receive it.

        self.send_message(mto=recipient,
                          mbody=message,
                          mtype='chat')

    
    #def Recv_message(self, msg): # Received a message Event
        #if msg['type'] in ('normal', 'chat'):
            #print ('Messqge Recieved - XMPP FILE',msg)

            
    def disconnect_chatnao(self):
        print('Disconnecting....')
        self.disconnect(wait=2.0)
        print('Disconnected')

    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

