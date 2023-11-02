import keyboard as keyb;
from pynput.mouse import Controller, Button;
from screeninfo import get_monitors;

direction:list = [0, 0];
mouse_pos:list = [0, 0];
mouse = Controller();

size:tuple = (0, 0);
def get_monitor_size():
    global size;
    monitor = get_monitors()[0];
    size = (monitor.width, monitor.height);

def change_direction(x:float, y:float):
    global direction;
    direction = [x, y];

def click(left:bool=False):
    if left:
        mouse.click(Button.left);
    else:
        mouse.click(Button.right);

keyb.on_press_key("a", lambda _: click(True));
keyb.on_press_key("apostrophe", lambda _: click(False));

keyb.on_press_key("s", lambda _: change_direction(-0.05, direction[1]));
keyb.on_release_key("s", lambda _:
    change_direction(0 if direction[0] == -0.05 else direction[0], direction[1]))
keyb.on_press_key("d", lambda _: change_direction(0.05, direction[1]));
keyb.on_release_key("d", lambda _:
    change_direction(0 if direction[0] == 0.05 else direction[0], direction[1]));
keyb.on_press_key("semicolon", lambda _: change_direction(direction[0], -0.05));
keyb.on_release_key("semicolon", lambda _:
    change_direction(direction[0], 0 if direction[1] == -0.05 else direction[1]));
keyb.on_press_key("l", lambda _: change_direction(direction[0], 0.05));
keyb.on_release_key("l", lambda _:
    change_direction(direction[0], 0 if direction[1] == 0.05 else direction[1]));

get_monitor_size();

while True:
    if direction[0] or direction[1]:
        if direction[0] < 0:
            if mouse_pos[0] > 0:
                mouse_pos[0] += direction[0];
        else:
            if mouse_pos[0] < size[0]:
                mouse_pos[0] += direction[0];
        if direction[1] < 0:
            if mouse_pos[1] > 0:
                mouse_pos[1] += direction[1];
        else:
            if mouse_pos[1] < size[1]:
                mouse_pos[1] += direction[1];
        mouse.position = (mouse_pos[0], mouse_pos[1]);
