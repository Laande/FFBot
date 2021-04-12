from time import sleep
from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.hpacket import HPacket
from g_python.hparsers import HEntity
import sys

if sys.version_info[0] >= 3:
    pass
else:
    print("[FFBot] You need python 3.0+ for run this application.")
    exit()

extension_info = {
    "title": "FFBot",
    "description": "Bot for FallingFurni",
    "author": "Luizin",
    "version": "1.0"
}

extension = Extension(extension_info=extension_info, args=sys.argv)
extension.start()

def client_type():
    sleep(0.50)
    return extension.connection_info["client_type"]

client_type = client_type()

unity_string = "UNITY"
flash_string = "FLASH"

headers = {}

if str(client_type).__contains__(unity_string):
    headers = {
        "RoomUserWalk": 75,
        "ObjectAdd": 95,
        "RoomUserTalk": 52,
        "RoomUserTalk_In": 24,
        "UserTyping": 317,
    }
else:
    headers = {
        "RoomUserWalk": 3725,
        "ObjectAdd":  1810,
        "RoomUserTalk": 654,
        "RoomUserTalk_In": 3139,
        "UserTyping": 3550,
    }


prefix = "!"

disableType = None 
isStarted = None
Capture = None
FallingFurni = None
location_x = None
location_y = None
specific = None
autoStop = None

RoomUserTalkIn = headers["RoomUserTalk_In"]
RoomUserTalkOut = headers["RoomUserTalk"]
ObjectAdd = headers["ObjectAdd"]
RoomUserWalk = headers["RoomUserWalk"]
UserTyping = headers["UserTyping"]

def SendMessage(msg):
    msg = f'[FallingFurni] ~ {msg}'
    if str(client_type).__contains__(flash_string):
        extension.send_to_client(HPacket(RoomUserTalkIn, 1, msg, 0, 33, 0, 0))
    else:
        extension.send_to_client(HPacket(RoomUserTalkIn, 0, msg, 0, 33, "", -1))

def RoomUserTalk(message):
    global disableType, Capture, FallingFurni, specific, autoStop

    message.is_blocked = True
    packet = message.packet
    (text, _, _) = packet.read("sii")
    text = str(text)

    if text.startswith(f"{prefix}disabletype"):
        if disableType == True:
            disableType = False
        else:
            disableType = True

        if disableType == True:
            SendMessage("IgnoreType: ON")
        else:
            SendMessage("IgnoreType: OFF")

    elif text.startswith(f"{prefix}ffbot"):
        if FallingFurni == True:
            FallingFurni = False
            SendMessage("FallingFurni: OFF")
        else:
            FallingFurni = True
            SendMessage("FallingFurni: ON")

    elif text.startswith(f'{prefix}capture'):
        if Capture == True:
            Capture = False
            SendMessage("Capture: OFF")
        else:
            Capture = True
            SendMessage("Capture: ON")

    elif text.startswith(f'{prefix}specific'):
        if specific == True:
            specific = False
            SendMessage("Specific Tile: OFF")
        else:
            specific = True
            SendMessage("Specific Tile: ON")

    elif text.startswith(f'{prefix}autostop'):
        if autoStop == True:
            autoStop = False
            SendMessage("AUTO STOP: OFF")
        else:
            autoStop = True
            SendMessage("AUTO STOP: ON")


def DisableType(msg):
    if disableType == True:
        msg.is_blocked = True
    else:
        msg.is_blocked = False

def CaptureTile(msg):
    global location_x, location_y
    if Capture == True:
        msg.is_blocked = True
        packet = msg.packet
        (x, y) = packet.read('ii')
        location_x = x
        location_y = y
        SendMessage(f"Capture Position: {x},{y}")
    else:
        msg.is_blocked = False

def FFBot(message):
    global location_x, location_y, FallingFurni, autoStop

    if FallingFurni == True:
        packet = message.packet
        
        def walk_to_tile(x, y):
            extension.send_to_server(HPacket(RoomUserWalk, x, y))

        if specific == True:
            walk_to_tile(location_x, location_y)
            if autoStop == True:
                FallingFurni = False
        else:
            if(str(client_type).__contains__(flash_string)):
                (_, _, x, y, _, _, _, _, _, _, _, _, _,) = packet.read('iiiiissiisiii')
            else:
                (_, _, x, y, _, _, _, _, _, _, _, _, _,) = packet.read('liiiiliiisiil')
                
            walk_to_tile(x, y)
            if autoStop == True:
                FallingFurni = False
            

##########################################################################
# Falling Furni        By Luizin                                         #
extension.intercept(Direction.TO_SERVER, RoomUserTalk, RoomUserTalkOut)  #
extension.intercept(Direction.TO_SERVER, DisableType, UserTyping)        #
extension.intercept(Direction.TO_SERVER, CaptureTile, RoomUserWalk)      #
extension.intercept(Direction.TO_CLIENT, FFBot, ObjectAdd)               #
##########################################################################
