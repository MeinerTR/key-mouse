from typing import List
import keyboard as keyb;
import mouse;
from pynput.mouse import Controller, Button;
from screeninfo import get_monitors;

direction:List = [0, 0];
mouse_pos:List = [0, 0];
mouse = Controller();

size:tuple = (0, 0);
def get_monitor_size():
    global size;
    monitor = get_monitors()[0];
    size = (monitor.width, monitor.height);

def change_direction(x:float, y:float):
    global direction;
    direction = [x, y];

keyb.on_press_key("a", lambda _: mouse.click(Button.left));
keyb.on_press_key("apostrophe", lambda _: mouse.click(Button.right));

vert_vel:float = 0.05;
horz_vel:float = 0.05;

def change_vel(value:float=4.2):
    global horz_vel, vert_vel;
    horz_vel = value;
    vert_vel = value;
    if direction[0]:
        if direction[0] < 0:
            change_direction(-horz_vel, direction[1]);
        else:
            change_direction(horz_vel, direction[1]);
    if direction[1]:
        if direction[1] < 0:
            change_direction(direction[0], -vert_vel);
        else:
            change_direction(direction[0], vert_vel);

keyb.on_press_key("space", lambda _: change_vel(0.1));
keyb.on_release_key("space", lambda _: change_vel(0.05));

keyb.on_press_key("s", lambda _: change_direction(-horz_vel, direction[1]));
keyb.on_release_key("s", lambda _:
    change_direction(0 if direction[0] == -horz_vel else direction[0], direction[1]))
keyb.on_press_key("d", lambda _: change_direction(horz_vel, direction[1]));
keyb.on_release_key("d", lambda _:
    change_direction(0 if direction[0] == horz_vel else direction[0], direction[1]));
keyb.on_press_key("semicolon", lambda _: change_direction(direction[0], -vert_vel));
keyb.on_release_key("semicolon", lambda _:
    change_direction(direction[0], 0 if direction[1] == -vert_vel else direction[1]));
keyb.on_press_key("l", lambda _: change_direction(direction[0], vert_vel));
keyb.on_release_key("l", lambda _:
        change_direction(direction[0], 0 if direction[1] == vert_vel else direction[1]));

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
