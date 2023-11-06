from typing import List, Tuple
import keyboard as keyb;
from pynput.mouse import Controller, Button;
from screeninfo import get_monitors;

direction:List = [0, 0];
mouse_pos:List = [0, 0];
mouse = Controller();

print_key_log:bool = False;

left:str =  "s";
right:str = "d";

down:str =  "l";
up:str =    "semicolon";

up_left:str =   "w";
up_right:str =  "e";

down_left:str = "o";
down_right:str= "p";

increase_vel:str = "=";
decrease_vel:str = "minus";

velocity:float = 0.08;
increase_by:float = 0.005;
break_vel:float = 0.03;
breaked_vel:float = velocity - break_vel;

def change_direction(x:bool=False, y:bool=False):
    global direction;
    if x:
        r:bool = keyb.is_pressed(right);
        l:bool = keyb.is_pressed(left);
        if l and r: pass;
        elif l: direction[0] = -velocity;
        elif r: direction[0] = velocity;
        else: direction[0] = 0;
        return;
    if not y: return;
    d:bool = keyb.is_pressed(down);
    u:bool = keyb.is_pressed(up);
    if d and u: pass;
    elif u: direction[1] = -velocity;
    elif d: direction[1] = velocity;
    else: direction[1] = 0;

def change_speed(value:float=4.2):
    if value < increase_by: return;
    global velocity, breaked_vel;
    velocity = value;
    breaked_vel = velocity - break_vel;
    print(f"New velocity: {velocity}");

mouse_right:str = "apostrophe";
mouse_left:str = "a";

size:tuple = (0, 0);
def get_teleport_pos() -> tuple:
    xdiv3:float = size[0]/3;
    ydiv3:float = size[1]/3;
    return  ((xdiv3, ydiv3), 
            (size[0]-xdiv3, ydiv3),
            (xdiv3, size[1]-ydiv3),
            (size[0]-xdiv3, size[1]-ydiv3));

def get_monitor_size():
    global size;
    monitor = get_monitors()[0];
    size = (monitor.width, monitor.height);

get_monitor_size();

top_left:Tuple[float, float];
top_right:Tuple[float, float];

bottom_left:Tuple[float, float];
bottom_right:Tuple[float, float];

top_left, top_right, bottom_left, bottom_right = get_teleport_pos();

def teleport_to(x:float=size[0]/2, y:float=size[1]/2):
    global mouse_pos;
    mouse_pos = [x, y];
    mouse.position = mouse_pos[0], mouse_pos[1];

keyb.on_press_key(decrease_vel, lambda _: change_speed(velocity - increase_by));
keyb.on_press_key(increase_vel, lambda _: change_speed(velocity + increase_by));

keyb.on_press_key(up_left, lambda _: teleport_to(*top_left));
keyb.on_press_key(up_right, lambda _: teleport_to(*top_right));
keyb.on_press_key(down_left, lambda _: teleport_to(*bottom_left));
keyb.on_press_key(down_right, lambda _: teleport_to(*bottom_right));

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

if print_key_log:
    def print_key(key):
        print(key);

    keyb.hook(print_key);

def change_vel(value:float=4.2):
    change_speed(value);
    if direction[0]:
        change_direction(x=True);
    if direction[1]:
        change_direction(y=True);

keyb.on_press_key("space", lambda _: change_vel(breaked_vel));
keyb.on_release_key("space", lambda _: change_vel(velocity + break_vel));

keyb.on_press_key(left, lambda _: change_direction(x=True));
keyb.on_release_key(left, lambda _: change_direction(x=True))
keyb.on_press_key(right, lambda _: change_direction(x=True));
keyb.on_release_key(right, lambda _: change_direction(x=True));
keyb.on_press_key(up, lambda _: change_direction(y=True));
keyb.on_release_key(up, lambda _: change_direction(y=True));
keyb.on_press_key(down, lambda _: change_direction(y=True));
keyb.on_release_key(down, lambda _: change_direction(y=True));

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
