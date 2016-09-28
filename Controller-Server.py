#!/bin/python3

#Imports the dependencies
import os, time, struct, array, socket
from fcntl import ioctl
global close_loop
global fwd
fwd = 0
global bwd
bwd = 0

#Creates string to send to client
#[0.0,0.0]
#The first number will be with -1 to 1, -1 being bwd and 1 being fwd
#Their is also a decimal number for strength optionally if we choose to use
#the bumper for throttle as we are reading from an analog throttle
#The second number is left to right same range as the first number but will include a decimal
#For Example:
#[1,0.5] is forward and turned to the right halfway
def Server():
    host = "10.0.0.6"
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    global conn, addr
    conn, addr = mySocket.accept()
    MainLoop()

def MainLoop():
    while True:
        Main()

def Main():
    cont_func()
    #if lar < -0.3:
        #print("Left")
    #if lar > 0.3:
        #print("Right")
    #if lar > -0.3 and lar < 0.3:
        #print("Straight")

    fab = fwd - bwd
    #if fab == -1:
        #print("Backwards")
    #if fab == 0:
        #print("Idle")
    #if fab == 1:
        #print("Forwards")

    fb = str(fab)
    lr = str(lar)

    global data
    data = str(fb + " " + lr)
    conn.send(data.encode())
def cont_func():
    global close_loop
    close_loop = 19

    # Iterate over the joystick devices.
    #print('Available devices:')

    #for fn in os.listdir('/dev/input'):
        #if fn.startswith('js'):
            #print(('  /dev/input/%s' % (fn)))

    # We'll store the states here.
    axis_states = {}
    button_states = {}

    # These constants were borrowed from linux/input.h
    axis_names = {
        0x00 : 'x',
        0x01 : 'y',
        0x02 : 'z',
        0x03 : 'rx',
        0x04 : 'ry',
        0x05 : 'rz',
        0x06 : 'trottle',
        0x07 : 'rudder',
        0x08 : 'wheel',
        0x09 : 'gas',
        0x0a : 'brake',
        0x10 : 'hat0x',
        0x11 : 'hat0y',
        0x12 : 'hat1x',
        0x13 : 'hat1y',
        0x14 : 'hat2x',
        0x15 : 'hat2y',
        0x16 : 'hat3x',
        0x17 : 'hat3y',
        0x18 : 'pressure',
        0x19 : 'distance',
        0x1a : 'tilt_x',
        0x1b : 'tilt_y',
        0x1c : 'tool_width',
        0x20 : 'volume',
        0x28 : 'misc',
    }

    button_names = {
        0x120 : 'trigger',
        0x121 : 'thumb',
        0x122 : 'thumb2',
        0x123 : 'top',
        0x124 : 'top2',
        0x125 : 'pinkie',
        0x126 : 'base',
        0x127 : 'base2',
        0x128 : 'base3',
        0x129 : 'base4',
        0x12a : 'base5',
        0x12b : 'base6',
        0x12f : 'dead',
        0x130 : 'a',
        0x131 : 'b',
        0x132 : 'c',
        0x133 : 'x',
        0x134 : 'y',
        0x135 : 'z',
        0x136 : 'tl',
        0x137 : 'tr',
        0x138 : 'tl2',
        0x139 : 'tr2',
        0x13a : 'select',
        0x13b : 'start',
        0x13c : 'mode',
        0x13d : 'thumbl',
        0x13e : 'thumbr',

        0x220 : 'dpad_up',
        0x221 : 'dpad_down',
        0x222 : 'dpad_left',
        0x223 : 'dpad_right',

        # XBox 360 controller uses these codes.
        0x2c0 : 'dpad_left',
        0x2c1 : 'dpad_right',
        0x2c2 : 'dpad_up',
        0x2c3 : 'dpad_down',
    }

    axis_map = []
    button_map = []

    # Open the joystick device.
    fn = '/dev/input/js0'
    #print(('Opening %s...' % fn))
    jsdev = open(fn, 'rb')

    # Get the device name.
    #buf = bytearray(63)
    buf = array.array('u', ['\0'] * 64)
    ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
    js_name = buf.tostring()
    #print(('Device name: %s' % js_name))

    # Get number of axes and buttons.
    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
    num_axes = buf[0]

    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
    num_buttons = buf[0]

    # Get the axis map.
    buf = array.array('B', [0] * 0x40)
    ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

    for axis in buf[:num_axes]:
        axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
        axis_map.append(axis_name)
        axis_states[axis_name] = 0.0

    # Get the button map.
    buf = array.array('H', [0] * 200)
    ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

    for btn in buf[:num_buttons]:
        btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
        button_map.append(btn_name)
        button_states[btn_name] = 0

    #print(('%d axes found: %s' % (num_axes, ', '.join(axis_map))))
    #print(('%d buttons found: %s' % (num_buttons, ', '.join(button_map))))

    # Main event loop
    while close_loop != 0:
        global close_loop
        close_loop = close_loop - 1
        evbuf = jsdev.read(8)
        if close_loop == 6:
            global lar
            lar = fvalue
        if close_loop == 14:
            global tlp
            tlp = 1
        else:
            global tlp
            tlp = 0
        if close_loop == 13:
            global trp
            trp = 1
        else:
            global trp
            trp = 0
        if evbuf:
            time, value, type, number = struct.unpack('IhBB', evbuf)

            #if type & 0x80:
                 #print(("(initial)",))

            if type & 0x01:
                button = button_map[number]
                if button:
                    button_states[button] = value
                    if value:
                        #print(("%s pressed" % (button)))
                        if tlp == 1:
                            if button == 'tl':
                                global bwd
                                bwd = 1
                        elif trp == 1:
                            if button == 'tr':
                                global fwd
                                fwd = 1
                    else:
                        #print(("%s released" % (button)))
                        if tlp ==1:
                            if button == 'tl':
                                global bwd
                                bwd = 0
                        elif trp == 1:
                            if button == 'tr':
                                global fwd
                                fwd = 0


            if type & 0x02:
                axis = axis_map[number]
                if axis:
                    global fvalue
                    fvalue = value / 32767.0
                    axis_states[axis] = fvalue
                    #print(("%s: %.3f" % (axis, fvalue)))

Server()
