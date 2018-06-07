【安装与启动】
0.安装python2.7.14、cocos2d。
1.通过FlappyBirdServer/start_server.bat启动服务端。
2.通过FlappyBirdClient/start_client.bat启动客户端。


【功能说明】1.点击‘用户注册’注册，点击’用户登陆’登陆
            2.点击“notice”按钮显示服务器公告，该功能用于演示服务器客户端通讯功能。
            3.点击客户端界面空白处可以触发小鸟跳跃，避开栏杆。

【代码说明】

1.[客户端]
        逻辑代码在FlappyBirdClient\lib目录下。
        资源文件在FlappyBirdClient\data目录下。
        用户战绩在FlappyBirdClient\score目录下。
            难度设置：根据难度修改pipe.py中管道的水平距离与高度偏移值。
            用户管理：在登录，注册时向服务器发送用户信息。
            数据记录与同步：在score文件夹中记录用户分数
2.[服务端]
        代码在FlappyBirdServer目录下。
        用户战绩在FlappyBirdServer\score目录下。
            用户管理：收到注册信息时将用户信息储存在FlappyBirdServer\user.txt中。
            数据记录与同步：在收到用户的战绩时储存在FlappyBirdServer\score目录。