from time import sleep
from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.hpacket import HPacket
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

print(f'[FFBot] Application Started!')

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
        "RoomPlaceItem": 95,
        "RoomUserTalk": 52,
        "RoomUserTalk_In": 24,
        "UserTyping": 317,
        "RoomPlaceItem_Wired": 93
    }
else:
    headers = {
        "RoomUserWalk": 3725,
        "RoomPlaceItem":  1810,
        "RoomUserTalk": 654,
        "RoomUserTalk_In": 3139,
        "UserTyping": 3550,
        "RoomPlaceItem_Wired": 1855
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
isWired = None

RoomUserTalkIn = headers["RoomUserTalk_In"]
RoomUserTalkOut = headers["RoomUserTalk"]
RoomPlaceItem = headers["RoomPlaceItem"]
RoomUserWalk = headers["RoomUserWalk"]
UserTyping = headers["UserTyping"]
RoomPlaceItemWired = headers["RoomPlaceItem_Wired"]

def SendMessage(msg):
    msg = f'[FallingFurni] ~ {msg}'
    if str(client_type).__contains__(flash_string):
        extension.send_to_client(HPacket(RoomUserTalkIn, 1, msg, 0, 33, 0, 0))
    else:
        extension.send_to_client(HPacket(RoomUserTalkIn, 0, msg, 0, 33, "", -1))

def RoomUserTalk(message):
    global disableType, Capture, FallingFurni, specific, autoStop, isWired

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
    elif text.startswith(f'{prefix}wired'):
        if isWired == True:
            isWired = False
            SendMessage(F'FFBot Wired: OFF')
        else:
            isWired = True
            SendMessage(F'FFBOT Wired: ON')
    else:
        SendMessage(f'Command Not Found: {text}')

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

def FFBotWithWired(message):
    global isWired, location_x, location_y, autoStop

    if isWired == True:
        packet = message.packet

        def walk_to_tile(x, y):
            extension.send_to_server(HPacket(RoomUserWalk, x, y))

        if specific == True:
            walk_to_tile(location_x, location_y)
            if autoStop == True:
                isWired = False
        else:
            if(str(client_type).__contains__(flash_string)):
                (_, _, x, y, _, _, _, _, _, _, _, _, _, _,) = packet.read('iiiiissiisiiis')
            else:
                (_, _, x, y, w, w, w, w, w, w, w, w, w) = packet.read('liiiliiisiils')
            walk_to_tile(x, y)
            if autoStop == True:
                isWired = False

#############################################################################
# Falling Furni        By Luizin                                            #
extension.intercept(Direction.TO_SERVER, RoomUserTalk, RoomUserTalkOut)     #
extension.intercept(Direction.TO_SERVER, DisableType, UserTyping)           #
extension.intercept(Direction.TO_SERVER, CaptureTile, RoomUserWalk)         #
extension.intercept(Direction.TO_CLIENT, FFBot, RoomPlaceItem)              #
extension.intercept(Direction.TO_CLIENT, FFBotWithWired, RoomPlaceItemWired)#
#############################################################################
