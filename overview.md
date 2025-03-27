# 类

## game_launcher:
陈耀信

    主要处理游戏的基础设施、类与类间的通信、每个循环调用各类的update函数、I/O、绘图

    __init__() 
    调用各类的构造函数：Player(), Map()；
    初始化pygame的基本组件：screen, clock；
    初始化Group（用于碰撞检测）：bulletGroup, enemyGroup()
    
    launch() 游戏主函数：
    1. 事件监测：处理I/O，调用相应的类接口（如在键盘按下W键时调用player类中的前行函数）
        player.go_up_begin()
        player.go_down_begin()
        player.go_left_begin()
        player.go_right_begin()
        player.go_up_end()
        player.go_down_end()
        player.go_left_end()
        player.go_right_end()
        player.fire()
    2. 核心内容：self.generateEnemy(), self.generateProps()；
    3. 检测精灵之间的碰撞：
        self.checkPlayer_Enemy()
        self.checkPlayer_Props()
        self.checkBullet_Enemy()
    4. 画画：group.draw(), screen.bilt()
    5. 更新组件状态
        self.bulletGroup.update()
        self.enemyGroup.update()
        self.propsGroup.update()
        self.player.update()

    6. 刷新窗口

    generateEnemy()：生成敌人的逻辑

    generateProps()：生成道具的逻辑

    self.checkPlayer_Enemy()：检测玩家和敌人的碰撞

    self.checkPlayer_Props()：检测玩家和道具的碰撞

    self.checkBullet_Enemy()：检测子弹和敌人的碰撞

    接口需求：
    player：玩家构造函数；player的前进后退左右移动函数；发射子弹的函数；update()
    map：地图构造函数；地图绘制方案（结合视野问题）；life成员；status成员
    bullet：子弹构造函数；update()
    enemy：敌人构造函数；update()
    props：道具构造函数；update()（注：道具生成逻辑在game_launcher里写吧）


## player
葛苏杭

继承pygame.sprite类

1. 二维运动
2. 发射bullet
3. 与props互动
4. 与地图互动
5. 与enemy互动

#### 数据成员：
血量 子弹数 自己的位置坐标（数组） 状态（props相关） 图片及其rect



## map: 赵涵
1. 提供player移动接口
2. （地图生成？）

#### 数据成员：
地图数组 图片及其rect

***

## 后三个类由张宝樑、杨峻负责

## bullet
继承pygame.sprite类

1. 与地图互动
2. 与enemy互动

#### 数据成员：
子弹的位置坐标（数组） 图片及其rect


## enemy（生成逻辑？
继承pygame.sprite类

1. 与player互动
2. 与地图互动

#### 数据成员：
血量 位置（数组） 图片及其rect


## Power-Up道具(血包 大子弹？)
继承pygame.sprite类

#### 数据成员：
道具类型 图片及其rect