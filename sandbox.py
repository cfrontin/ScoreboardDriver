
import math;
import time;
import random as rng;
import sys;

from rgbmatrix import RGBMatrix;
from rgbmatrix import RGBMatrixOptions;
from rgbmatrix import graphics;

from catholic import jesus;
from catholic import readings_pager;

# configuration for the matrix: options for my board
options= RGBMatrixOptions();
options.brightness= 50;
options.rows= 32;
options.cols= 64;
options.chain_length= 1;
options.parallel= 1;
options.hardware_mapping= 'adafruit-hat';

# object representation of the board and its canvas
matrix= RGBMatrix(options= options);
canvas= matrix.CreateFrameCanvas();

# some sexy colors
def colorset():
    set= [];
    set.append({'r': 7, 'g': 15, 'b': 25});
    set.append({'r': 255, 'g': 235, 'b': 59});
    set.append({'r': 155, 'g': 41, 'b': 21});
    set.append({'r': 36, 'g': 30, 'b': 78});
    set.append({'r': 8, 'g': 160, 'b': 69});
    return set;

# a text scrolling example

def textscroll(matrix, canvas):

    # get and load a font
    font= graphics.Font();
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/tom-thumb.bdf");
    print("font height: %f" % font.height);
    print("font baseline: %f" % font.baseline);

    # get color
    textColor= graphics.Color(000, 153, 255);

    # the position we start at: edge of the screen
    pos= canvas.width;

    # some  text
    my_text= "JUDY!!!";

    # vertical position to start
    y= font.height;

    # forever loop
    while True:

        # forever loop
        while True:

            # clear the canvas
            canvas.Clear();

            # draw the desired text
            len= graphics.DrawText(canvas, font, pos, y, textColor, my_text);
            pos -= 1;

            if (pos + len < 0):
                pos= canvas.width;
                break;

            time.sleep(0.05);
            canvas= matrix.SwapOnVSync(canvas);

        y += font.height;
        # y= y % matrix.height;
        if y > matrix.height:
            break;

# a fun noise example

def noisy(matrix, canvas):

    canvas.Clear();
    canvas= matrix.CreateFrameCanvas();

    # infinite loop
    for j in range(1000):

        for i in range(100):

            # pick a random spot on the matrix
            x= rng.randint(0, matrix.width);
            y= rng.randint(0, matrix.height);

            # pick a random color
            r= rng.randint(0, 255);
            g= rng.randint(0, 255);
            b= rng.randint(0, 255);
            # print("(r,g,b)= (%d, %d, %d)" % (r, g, b));

            # set the pixel
            canvas.SetPixel(x, y, r, g, b);

        # swap the canvas in to the screen
        matrix.SwapOnVSync(canvas);
        time.sleep(0.01);

def mlbled_offday(matrix, canvas):

    print("Hello, world!");

### MAIN LOOP

# pages= [noisy, textscroll];
pages= [noisy, jesus, readings_pager,];
# pages= [jesus, readings_pager,];
# pages= [readings_scroller,];
# pages= [readings_pager,];

debug_counter= 0;
debug_count= 1;

while True:
    for page in pages:
        page(matrix, canvas);
        # clear old canvas to prevent weird stuff

    # # for now, just cycle through
    # debug_counter += 1;
    # if debug_counter >= debug_count:
    #     break;
