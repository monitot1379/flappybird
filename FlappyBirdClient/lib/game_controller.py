# -*- coding: utf-8 -*-
import cocos
import re
import time
from cocos.scene import *
from cocos.actions import *
from cocos.layer import *  
from cocos.text  import *
from cocos.menu import *
from cocos.rect import *
import random
from atlas import *
from land import *
from bird import *
from score import *
from pipe import *
from collision import *
from network import *
import common

#vars
gameLayer = None
gameScene = None
spriteBird = None
land_1 = None
land_2 = None
startLayer = None
pipes = None
score = 0
listener = None
account = None
password = None
ipTextField = None
errorLabel = None
isGamseStart = False
User = ''
Psw = ''
startTime=0.0
def initGameLayer():
    global spriteBird, gameLayer, land_1, land_2
    # gameLayer: 游戏场景所在的layer
    gameLayer = Layer()
    # add background
    bg = createAtlasSprite("bg_day")
    bg.position = (common.visibleSize["width"]/2, common.visibleSize["height"]/2)
    gameLayer.add(bg, z=0)
    # add moving bird
    spriteBird = creatBird()
    gameLayer.add(spriteBird, z=20)
    # add moving land
    land_1, land_2 = createLand()
    gameLayer.add(land_1, z=10)
    gameLayer.add(land_2, z=10)
    # add gameLayer to gameScene
    gameScene.add(gameLayer)

def game_start(_gameScene):
    global gameScene
    # 给gameScene赋值
    gameScene = _gameScene
    initGameLayer()
    start_botton = GameUserMenu()
    gameLayer.add(start_botton, z=20, name="start_button")
    connect(gameScene)

def createLabel(value, x, y):
    label=Label(value,  
        font_name='Times New Roman',  
        font_size=15, 
        color = (0,0,0,255), 
        width = common.visibleSize["width"] - 20,
        multiline = True,
        anchor_x='center',anchor_y='center')
    label.position = (x, y)
    return label

# single game start button的回调函数
def singleGameReady():
    removeContent()
    ready = createAtlasSprite("text_ready")
    ready.position = (common.visibleSize["width"]/2, common.visibleSize["height"] * 3/4)

    tutorial = createAtlasSprite("tutorial")
    tutorial.position = (common.visibleSize["width"]/2, common.visibleSize["height"]/2)
    
    spriteBird.position = (common.visibleSize["width"]/3, spriteBird.position[1])

    #handling touch events
    class ReadyTouchHandler(cocos.layer.Layer):
        is_event_handler = True     #: enable director.window events

        def __init__(self):
            super( ReadyTouchHandler, self).__init__()

        def on_mouse_press (self, x, y, buttons, modifiers):
            """This function is called when any mouse button is pressed

            (x, y) are the physical coordinates of the mouse
            'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
            'modifiers' is a bitwise or of pyglet.window.key modifier constants
               (values like 'SHIFT', 'OPTION', 'ALT')
            """
            self.singleGameStart(buttons, x, y)
    
        # ready layer的回调函数
        def singleGameStart(self, eventType, x, y):
            isGamseStart = True
            global startTime
            startTime=time.time()
            spriteBird.gravity = gravity #gravity is from bird.py
            # handling bird touch events
            addTouchHandler(gameScene, isGamseStart, spriteBird)
            score = 0   #分数，飞过一个管子得到一分
            # add moving pipes
            pipes = createPipes(gameLayer, gameScene, spriteBird, score)
            # 小鸟AI初始化
            # initAI(gameLayer)
            # add score
            createScoreLayer(gameLayer)
            # add collision detect
            addCollision(gameScene, gameLayer, spriteBird, pipes, land_1, land_2)
            # remove startLayer
            gameScene.remove(readyLayer)

    readyLayer = ReadyTouchHandler()
    readyLayer.add(ready)
    readyLayer.add(tutorial)
    gameScene.add(readyLayer, z=10)

def backToMainMenu():
    restartButton = RestartMenu()
    gameLayer.add(restartButton, z=50)

def showNotice():
    connected = connect(gameScene) # connect is from network.py
    if not connected:
        content = "Cannot connect to server"
        showContent(content)
    else:
        request_notice() # request_notice is from network.py

def sendScore(gameScore):
    connected = connect(gameScene) # connect is from network.py
    if not connected:
        content = "Cannot connect to server"
        showContent(content)
    else:
        send_score_to_server(gameScore)
def sendResult(gameScore,liveTime):
    connected = connect(gameScene) # connect is from network.py
    if not connected:
        content = "Cannot connect to server"
        showContent(content)
    else:
        send_result_to_server(gameScore,liveTime)

def showContent(content):
    removeContent()
    notice = createLabel(content, common.visibleSize["width"]/2+5, common.visibleSize["height"] * 9/10)
    gameLayer.add(notice, z=70, name="content")

def removeContent():
    try:
        gameLayer.remove("content")
    except Exception, e:
        pass
    

class RestartMenu(Menu):
    def __init__(self):  
        super(RestartMenu, self).__init__()
        self.menu_valign = CENTER  
        self.menu_halign = CENTER
        items = [
                (ImageMenuItem(common.load_image("button_restart.png"), self.initMainMenu)),
                (ImageMenuItem(common.load_image("button_notice.png"), showNotice))
                ]  
        self.create_menu(items,selected_effect=zoom_in(),unselected_effect=zoom_out())

    def initMainMenu(self):
        gameScene.remove(gameLayer)
        initGameLayer()
        isGamseStart = False
        singleGameReady()

class SingleGameStartMenu(Menu):
    def __init__(self):  
        super(SingleGameStartMenu, self).__init__()
        self.menu_valign = CENTER
        self.menu_halign = CENTER
        items = [
                (ImageMenuItem(common.load_image("button_start.png"), self.initMainMenu)),
                (ImageMenuItem(common.load_image("button_notice.png"), showNotice)),
				(ImageMenuItem(common.load_image("button_user3.png"), self.signOut)),
				(ImageMenuItem(common.load_image("button_user4.png"), self.switch)),
                ]  
        self.create_menu(items,selected_effect=zoom_in(),unselected_effect=zoom_out())

    def initMainMenu(self):
        gameScene.remove(gameLayer)
        initGameLayer()
        isGamseStart = False
        singleGameReady()
		
    def signOut(self):
        try:
            gameLayer.remove("restartButton")
        except Exception, e:
            pass
        usersignin()
        
    def switch(self):
        try:
            gameLayer.remove("restartButton")
        except Exception, e:
            pass
        usersignin()
		#showContent("switch")
		
    '''def gameStart(self): 
        gameLayer.remove(gameLayer)
        singleGameReady()'''

def signMenu():
    try:
        gameLayer.remove("signinButton")
    except Exception, e:
        pass
    restartButton = SingleGameStartMenu()
    gameLayer.add(restartButton, z=20,name="restartButton")
	
def startLog():
    connected = connect(gameScene) # connect is from network.py
    if not connected:
        content = "Cannot connect to server"
        showContent(content)
    else:
        print User,Psw
        send_log_user_info(User,Psw)

class GameUserMenu(Menu):
    def __init__(self):
        super(GameUserMenu,self).__init__()
        self.menu_valign = CENTER
        self.menu_halign = CENTER
        items = [
                (ImageMenuItem(common.load_image("button_user1.png"), self.signIn)),
                (ImageMenuItem(common.load_image("button_user2.png"), self.register))
                ]  
        self.create_menu(items,selected_effect=zoom_in(),unselected_effect=zoom_out())
	
    def signIn(self):
        gameLayer.remove("start_button")
        usersignin()
	
    def register(self):
        gameLayer.remove("start_button")
        userregister()
        #usersignin()
	
		
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))		
class signinMenu(Menu):
    def __init__( self ):
        super( signinMenu, self ).__init__(u'登录')
        x,y = director.get_window_size()
        
        # then add the items
        item1 = EntryMenuItem(u'用户名:', self.on_user_callback, '',
                              max_length=10)
        item2 = EntryMenuItem(u'密码:', self.on_password_callback, '',
                              max_length=10)
        item3 = MenuItem(u'登录', startLog)	
        item1.scale=0.3	
        item2.scale=0.3	
        item3.scale=0.5	
        items=[item1,item2,item3]
        self.create_menu( items, 
                          layout_strategy=fixedPositionMenuLayout(
                            [(50, 320), (50, 280), (120, 230)  ]))
							
    def on_user_callback (self, value):
        global User
        User= value
        
    def on_password_callback (self, value):
        global Psw
        Psw= value

def sendRegUserInfo():
    connected = connect(gameScene) # connect is from network.py
    if not connected:
        content = "Cannot connect to server"
        showContent(content)
        return False
    else:
        print('user:', User)
        print('password:', Psw)
        send_new_user_info(User,Psw)
        return True

def usersignin():
    try:
        gameLayer.remove("Button")
    except Exception, e:
        pass
    signinButton = signinMenu()
    gameLayer.add(signinButton, z=20,name="signinButton")
def userReg():
    if User=='' or Psw=='':
        content = u'用户名密码不能为空'
        showContent(content)
        return
    if not re.search('^(?![A-Z]+$)(?![a-z]+$)(?!\d+$)',Psw):
        content = u'密码需为数字和字母'
        showContent(content)
        return
    isSuc = sendRegUserInfo()
    if isSuc:
        usersignin()
class RegisterMenu(Menu):

    
    def __init__( self ):
        super( RegisterMenu, self ).__init__(u'注册')
        x,y = director.get_window_size()
        self.menu_halign = LEFT
        # then add the items
        item1 = EntryMenuItem(u'用户名:', self.on_user_callback, '',
                              max_length=10)
        item2 = EntryMenuItem(u'密码:', self.on_password_callback, '',
                              max_length=10)
        item3 = MenuItem(u'注册', userReg)
        item1.scale=0.3
        item2.scale=0.3
        item3.scale=0.5
        items=[item1,item2,item3]
        self.create_menu( items, 
                          layout_strategy=fixedPositionMenuLayout(
                            [(50, 320), (50, 280), (90, 230) ]))
    def on_user_callback (self, value):
        global User
        User= value
        
    def on_password_callback (self, value):
        global Psw
        Psw= value


def userregister():
    Button = RegisterMenu()
    gameLayer.add(Button, z=20,name="Button")

