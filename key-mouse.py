from typing import List
import keyboard as keyb;
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

left:str = "s";
right:str = "d";

down:str = "l";
up:str = "semicolon";

velocity:float = 0.05;
boost_val:float = 0.10;
boosted_vel:float = velocity + boost_val;

def change_direction(x:float|None, y:float|None):
    global direction;

    if x is None:
        r:bool = keyb.is_pressed(right);
        l:bool = keyb.is_pressed(left);
        if l and r: pass;
        elif l: direction[0] = -velocity;
        elif r: direction[0] = velocity;
        else: direction[0] = 0;
    elif y is None:
        d:bool = keyb.is_pressed(down);
        u:bool = keyb.is_pressed(up);
        if d and u: pass;
        elif u: direction[1] = -velocity;
        elif d: direction[1] = velocity;
        else: direction[1] = 0;
    else:
        direction = [x, y];

def change_speed(value:float=4.2):
    if value < boost_val: return;
    global velocity, boosted_vel;
    velocity = value;
    boosted_vel = velocity + boost_val;
    print(f"New velocity: {velocity}");

mouse_left:str = "a";
mouse_right:str = "apostrophe";

keyb.on_press_key("minus", lambda _: change_speed(velocity - 0.005));
keyb.on_press_key("=", lambda _: change_speed(velocity + 0.005));

lclick = keyb.on_press_key(mouse_left, lambda _: None);
rclick = keyb.on_press_key(mouse_right, lambda _: None);

mouse_activated:bool = False;
def activate_mouse_click() -> None:
    global lclick, rclick, mouse_activated;
    if mouse_activated:
        mouse_activated = False;
        keyb.unhook_key(lclick);
        keyb.unhook_key(rclick);
        return;
    mouse_activated = True;
    lclick = keyb.on_press_key(mouse_left, lambda _: mouse.click(Button.left));
    rclick = keyb.on_press_key(mouse_right, lambda _: mouse.click(Button.right));

keyb.on_press_key("`", lambda _: activate_mouse_click())

def print_key(key):
    print(key);

keyb.hook(print_key);

def change_vel(value:float=4.2):
    change_speed(value);
    if direction[0]:
        if direction[0] < 0:
            change_direction(-velocity, direction[1]);
        else:
            change_direction(velocity, direction[1]);
    if direction[1]:
        if direction[1] < 0:
            change_direction(direction[0], -velocity);
        else:
            change_direction(direction[0], velocity);

keyb.on_press_key("space", lambda _: change_vel(boosted_vel));
keyb.on_release_key("space", lambda _: change_vel(velocity - boost_val));

keyb.on_press_key(left, lambda _: change_direction(-velocity, direction[1]));
keyb.on_release_key(left, lambda _: change_direction(None, direction[1]))
keyb.on_press_key(right, lambda _: change_direction(velocity, direction[1]));
keyb.on_release_key(right, lambda _: change_direction(None, direction[1]));
keyb.on_press_key(up, lambda _: change_direction(direction[0], -velocity));
keyb.on_release_key(up, lambda _: change_direction(direction[0], None));
keyb.on_press_key(down, lambda _: change_direction(direction[0], velocity));
keyb.on_release_key(down, lambda _: change_direction(direction[0], None));

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
