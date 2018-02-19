# coding: utf-8
# python3

# curses API 文档：https://docs.python.org/3/library/curses.html#module-curses
import curses
from random import randint

# curses ASCII键值列表，仅列出了本程序中使用到的按键
KEY_ESC = 0x1b

# 场地大小
HEIGHT = 20
WIDTH = 40

# Snake通过一维数组snake[]进行保存
# 则 snake[i]%WIDTH 和 snake[i]/WIDTH 分别表示 snake[i] 的横坐标和纵坐标。
# snake[i]的取值范围是 WIDTH+1 ~ WIDTH*HEIGHT-1，且 snake[i]%WIDTH != 0; 初始值全为 0
snake = [0, 0]

# 蛇头必是Snake数组的第一个元素
HEAD = 0
snake[HEAD] = 3*WIDTH + 3   # 蛇头初始位置为 (3,3)
snake_size = 1              # 蛇初始长度为 1

# 由于snake是一维数组，所以对应元素直接加上以下值就表示向四个方向移动
direction_left = -1
direction_right = 1
direction_up = -WIDTH
direction_down = WIDTH

# 检查坐标 idx 是否为free, “是”返回 True，“否”返回 False
def is_idx_free(idx):
    return not (idx in snake[:snake_size])

# 检查蛇头是否撞到边界
def is_head_hit_border():
    return snake[HEAD] <= WIDTH or snake[HEAD] >= WIDTH*HEIGHT or snake[HEAD]%WIDTH == 0

# 检测蛇头是否撞到蛇尾
def is_head_hit_body():
    return (snake[HEAD] in snake[1:-1])

# food类
class FOOD(object):
    def __init__(self, SYMBOL='#', en_color=False):
        self.symbol = SYMBOL
        self.color_enable = en_color
        self.new_color = 0
    def new_food(self):
        global WIDTH, HEIGHT, snake_size, snake, window
        # set idx
        idx_free = False
        while not idx_free:
            x_idx = randint(1, WIDTH-2)
            y_idx = randint(1, HEIGHT -2)
            self.idx = x_idx + y_idx * WIDTH
            idx_free = is_idx_free(self.idx)
        # set color
        self.color = self.new_color
        self.new_color = randint(1,5) if self.color_enable else 0
        # display
        window.addch(int(self.idx / WIDTH), self.idx % WIDTH, self.symbol, 
                    curses.color_pair(self.new_color))

def snake_move(direction):
    global snake, snake_size, WIDTH, HEIGHT

    for i in range(snake_size, 0, -1):
        snake[i] = snake[i-1]
    snake[HEAD] += direction

    # 绘制蛇身
    p_temp = snake[1]
    window.addch(int(p_temp/WIDTH), p_temp%WIDTH, '*', curses.color_pair(food.color))
    
    # 绘制蛇头
    window.addch(int(snake[HEAD]/WIDTH), snake[HEAD]%WIDTH, '#', 
                curses.color_pair(food.color))

    # 检测是否犯规
    if is_head_hit_body() or is_head_hit_border():
        raise EXIT_Exception("EXIT")

    # 判断是否吃到食物
    if snake[HEAD] == food.idx:
        snake_size += 1
        snake.append(0)
        if snake_size < WIDTH*HEIGHT: food.new_food()
    else:
        window.addch(int(snake[snake_size]/WIDTH), snake[snake_size]%WIDTH, ' ', 
                    curses.color_pair(0))  

# 自定义一个EXIT_Exception异常类，继承 Exception，用于捕获按键 “Esc” 和 “^C”
class EXIT_Exception(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

# 颜色配置
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

# 窗口配置
window = curses.newwin(HEIGHT+1, WIDTH+1, 0, 0)
window.keypad(1)    # Enable keypad
curses.noecho()     # 关闭屏幕回显                 
curses.curs_set(0)
window.border(0)    # 绘制边界
window.nodelay(1)

food = FOOD('@', True)
food.new_food()
direction = direction_right

try:
    while True:
        window.border(0)
        window.addstr(0, 2, ' Score: ' + str(snake_size-1) + ' ', curses.color_pair(3))
        window.timeout(150)

        key_press = window.getch()
        
        if key_press == KEY_ESC:
            raise EXIT_Exception("EXIT")
        elif key_press == curses.KEY_UP and direction != direction_down:
            direction = direction_up
        elif key_press == curses.KEY_LEFT and direction != direction_right:
            direction = direction_left
        elif key_press == curses.KEY_DOWN and direction != direction_up:
            direction = direction_down
        elif key_press == curses.KEY_RIGHT and direction != direction_left:
            direction = direction_right
        
        snake_move(direction)     
except:
    window.addstr(1, 2, ' Game Over',curses.color_pair(3))
    window.addstr(2, 2, ' Press any key to continue.',curses.color_pair(3))
    while True:
        if window.getch()!=-1: break
    curses.echo()
    curses.endwin()
    print('\nGame End, Your Score = ' + str(snake_size-1) + '\n')

