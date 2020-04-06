
import math;
import time;
import random as rng;
import sys;

import requests;
from bs4 import BeautifulSoup;

from PIL import Image;

from rgbmatrix import RGBMatrix;
from rgbmatrix import RGBMatrixOptions;
from rgbmatrix import graphics;

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
    for j in range(100):

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

# print the daily readings

def fetch_readings():

    # USCCB daily readings page
    page= requests.get("http://usccb.org/bible/readings/");
    soup= BeautifulSoup(page.text, 'html.parser');

    # dictionary to connect USCCB link keys to bible book names
    booknames= {
            'genesis': "Genesis",
            'exodus': "Exodus",
            'leviticus': "Leviticus",
            'numbers': "Numbers",
            'deuteronomy': "Deuteronomy",
            'joshua': "Joshua",
            'judges': "Judges",
            'ruth': "Ruth",
            '1samuel': "1 Samuel",
            '2samuel': "2 Samuel",
            '1kings': "1 Kings",
            '2kings': "2 Kings",
            '1chronicles': "1 Chronicles",
            '2chronicles': "2 Chronicles",
            'ezra': "Ezra",
            'nehemiah': "Nehemiah",
            'tobit': "Tobit",
            'judith': "Judith",
            'esther': "Esther",
            '1mc': "1 Maccabees",
            '2mc': "2 Maccabees",
            'job': "Job",
            'psalms': "Psalms",
            'proverbs': "Proverbs",
            'ecclesiastes': "Ecclesiastes",
            'songofsongs': "Song of Songs",
            'wisdom': "Wisdom",
            'sirach': "Sirach",
            'isaiah': "Isaiah",
            'jeremiah': "Jeremiah",
            'lamentations': "Lamentations",
            'baruch': "Baruch",
            'ezekiel': "Ezekiel",
            'daniel': "Daniel",
            'hosea': "Hosea",
            'joel': "Joel",
            'amos': "Amos",
            'obadiah': "Obadiah",
            'jonah': "Jonah",
            'micah': "Micah",
            'nahum': "Nahum",
            'habakkuk': "Habakkuk",
            'zephaniah': "Zephaniah",
            'haggai': "Haggai",
            'zechariah': "Zechariah",
            'malachi': "Malachi",
            'matthew': "Matthew",
            'mark': "Mark",
            'luke': "Luke",
            'john': "John",
            'acts': "Acts",
            'romans': "Romans",
            '1corinthians': "1 Corinthians",
            '2corinthians': "2 Corinthians",
            'galatians': "Galatians",
            'ephesians': "Ephesians",
            'philippians': "Philippians",
            'colossians': "Colossians",
            '1thessalonians': "1 Thessalonians",
            '2thessalonians': "2 Thessalonians",
            '1timothy': "1 Timothy",
            '2timothy': "2 Timothy",
            'titus': "Titus",
            'philemon': "Philemon",
            'hebrews': "Hebrews",
            'james': "James",
            '1peter': "1 Peter",
            '2peter': "2 Peter",
            '1john': "1 John",
            '2john': "2 John",
            '3john': "3 John",
            'jude': "Jude",
            'revelation': "Revelation",
    };

    # prep items to carry daily readings
    reading1= None;
    responsorial= None;
    reading2= None;
    gospel= None;

    # function to process a scaped item
    def process_brw(wrapper):

        # print("\nwrapper:\n")
        # print(wrapper);

        text= wrapper.find('h4').find('a').text;
        href= wrapper.find('h4').find('a')['href'];

        # href= href.split('/bible/readings')[-1];
        href= href.split('/bible/')[-1];

        # print(text);
        # print(href);

        book= booknames[href.split('/')[0].lower()];
        chapter= href.split('/')[1].split(':')[0];
        verse= href.split('/')[1].split(':')[1];

        # print(book);
        # print(chapter);
        # print(verse);

        return {'book': book, 'chapter': chapter, 'verse': verse};

    for wrapper in soup.find_all(class_= "bibleReadingsWrapper"):
        if "Reading 1" in wrapper.find('h4').text:
            reading1= process_brw(wrapper);
        elif "Responsorial Psalm" in wrapper.find('h4').text:
            responsorial= process_brw(wrapper);
        elif "Reading 2" in wrapper.find('h4').text:
            reading2= process_brw(wrapper);
        elif "Gospel" in wrapper.find('h4').text and \
                not "Verse Before" in wrapper.find('h4').text:
            gospel= process_brw(wrapper);

    readings= [];
    for reading in [reading1, responsorial, reading2, gospel]:
        if reading is not None:
            readings.append(reading);
    return readings;

def jesus(matrix, canvas):

    canvas.Fill(7, 15, 25);

    image= Image.open('img/jesus_is_cool.jpg');
    (img_width, img_height)= image.size;

    image= image.resize((matrix.width,
            math.floor(img_height/img_width*matrix.width)), Image.ANTIALIAS);
    (img_width, img_height)= image.size;

    x_img= 0;
    y_img= 0;

    N_img= 100;
    delta= +1;
    passed= False;

    for i in range(N_img):
        canvas.SetImage(image, x_img, -y_img);
        canvas.SetImage(image, x_img, -y_img + img_height);

        canvas= matrix.SwapOnVSync(canvas);
        time.sleep(0.1);

        y_img += delta;

        if y_img > (img_height - matrix.height):
            delta= -1;

        if y_img < 8:
            if (delta < 0):
                if passed:
                    passed= True;
                else:
                    break;

    time.sleep(1.0);

def readings_scroller(matrix, canvas):

    # scroll timer
    sleeptime= 0.2;
    sleeptime_first= 2.0;
    is_first= True;

    # the position we start at: edge of the screen
    x_text= 0;
    y_text= 10;

    while True:

        # get and load a font
        font_head= graphics.Font();
        font_head.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/tom-thumb.bdf");
        vskip= math.floor(1.5*font_head.height);
        hskip= math.floor(0.5*font_head.height);

        # get color
        textColor= graphics.Color(000, 153, 255);

        # fetch readings
        readings= fetch_readings();

        # clear the canvas
        canvas.Clear();

        # draw the desired text
        len= graphics.DrawText(canvas, font_head,
                x_text + 0.0*hskip, y_text + 0.0*vskip, textColor,
                "Daily readings:");

        # get and load a font
        font_read= graphics.Font();
        font_read.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/tom-thumb.bdf");
        vskip= math.floor(1.5*font_read.height);
        hskip= math.floor(0.5*font_read.height);

        i= 0;
        for reading in readings:
            if reading is not None:
                i += 1;
                # draw the desired text
                len= graphics.DrawText(canvas, font_read,
                        x_text + 1.0*hskip, y_text + i*vskip, textColor,
                        reading['book']);
                i += 1;
                len= graphics.DrawText(canvas, font_read,
                        x_text + 2.0*hskip, y_text + i*vskip, textColor,
                        reading['chapter'] + ":" + reading['verse']);

        canvas= matrix.SwapOnVSync(canvas);

        if is_first:
            time.sleep(sleeptime_first);
            is_first= False;
        else:
            time.sleep(sleeptime);

        y_text -= 1;

        if y_text < -(i + 2)*vskip:
            break;

def readings_pager(matrix, canvas):

    # colors
    c_bg= {'r': 7, 'g': 15, 'b': 25};
    c_text= {'r': 255, 'g': 235, 'b': 59};

    # scroll timer
    sleeptime= 10.0;
    scrolltime= 0.25;

    # the position we start at: edge of the screen
    x_text= 3;
    y_text= 7;

    # get and load a font
    font_head= graphics.Font();
    font_head.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/tom-thumb.bdf");
    vskip= math.floor(1.5*font_head.height);
    hskip= math.floor(0.5*font_head.height);

    # get and load a font
    font_read= graphics.Font();
    font_read.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/tom-thumb.bdf");

    # get color
    textColor= graphics.Color(c_text['r'], c_text['g'], c_text['b']);

    # fetch readings
    readings= fetch_readings();

    # clear the canvas
    canvas.Clear();
    canvas.Fill(c_bg['r'], c_bg['g'], c_bg['b']);

    def do_reading(canvas, header, reading):

        keep_scrolling= True;
        offset= 0;

        while keep_scrolling:

            # clear the canvas
            canvas.Clear();
            canvas.Fill(c_bg['r'], c_bg['g'], c_bg['b']);

            # draw the desired text
            graphics.DrawText(canvas, font_head,
                    x_text + 0.0*hskip, y_text + 0.0*vskip, textColor,
                    header);

            # draw the desired text
            graphics.DrawText(canvas, font_read,
                    x_text + 1.0*hskip, y_text + 1.0*vskip, textColor,
                    reading['book']);
            len_txt= graphics.DrawText(canvas, font_read,
                    x_text + 2.0*hskip + offset,
                    y_text + 2.0*vskip, textColor,
                    reading['chapter'] + ":" + reading['verse']);

            offset -= 1;
            keep_scrolling= x_text + 2.0*hskip + offset + len_txt > matrix.width;

            # swap, pause, then clear the canvas
            canvas= matrix.SwapOnVSync(canvas);
            time.sleep(scrolltime);

        # swap, pause, then clear the canvas
        time.sleep(sleeptime - scrolltime);
        canvas.Clear();

    do_reading(canvas, "1st reading:", readings[0]);
    do_reading(canvas, "Responsorial:", readings[1]);
    if len(readings) > 3:
        do_reading(canvas, "2nd reading:", readings[2]);
        do_reading(canvas, "Gospel:", readings[3]);
    else:
        do_reading(canvas, "Gospel:", readings[2]);

    # # draw the desired text
    # graphics.DrawText(canvas, font_head,
    #         x_text + 0.0*hskip, y_text + 0.0*vskip, textColor,
    #         "First reading:");
    #
    # # draw the desired text
    # graphics.DrawText(canvas, font_read,
    #         x_text + 1.0*hskip, y_text + 1.0*vskip, textColor,
    #         readings[0]['book']);
    # len_txt= graphics.DrawText(canvas, font_read,
    #         x_text + 2.0*hskip, y_text + 2.0*vskip, textColor,
    #         readings[0]['chapter'] + ":" + readings[0]['verse']);
    #
    # # swap, pause, then clear the canvas
    # canvas= matrix.SwapOnVSync(canvas);
    # time.sleep(sleeptime);
    # canvas.Clear();

    # # draw the desired text
    # graphics.DrawText(canvas, font_head,
    #         x_text + 0.0*hskip, y_text + 0.0*vskip, textColor,
    #         "Responsorial:");
    #
    # graphics.DrawText(canvas, font_read,
    #         x_text + 1.0*hskip, y_text + 1.0*vskip, textColor,
    #         readings[1]['book']);
    # graphics.DrawText(canvas, font_read,
    #         x_text + 2.0*hskip, y_text + 2.0*vskip, textColor,
    #         readings[1]['chapter'] + ":" + readings[1]['verse']);
    #
    # # swap, pause, then clear the canvas
    # canvas= matrix.SwapOnVSync(canvas);
    # time.sleep(sleeptime);
    # canvas.Clear();

    # # draw the desired text
    # graphics.DrawText(canvas, font_head,
    #         x_text + 0.0*hskip, y_text + 0.0*vskip, textColor,
    #         "2nd reading:");
    #
    # vskip= math.floor(1.5*font_read.height);
    # hskip= math.floor(0.5*font_read.height);
    #
    # graphics.DrawText(canvas, font_read,
    #         x_text + 1.0*hskip, y_text + 1.0*vskip, textColor,
    #         readings[2]['book']);
    # graphics.DrawText(canvas, font_read,
    #         x_text + 2.0*hskip, y_text + 2.0*vskip, textColor,
    #         readings[2]['chapter'] + ":" + readings[2]['verse']);

    # if len(readings) > 3:
    #
    #     # swap, pause, then clear the canvas
    #     canvas= matrix.SwapOnVSync(canvas);
    #     time.sleep(sleeptime);
    #     canvas.Clear();
    #
    #     # clear the canvas
    #     canvas.Clear();
    #
    #     # draw the desired text
    #     graphics.DrawText(canvas, font_head,
    #             x_text + 0.0*hskip, y_text + 0.0*vskip, textColor,
    #             "Daily gospel:");
    #
    #     graphics.DrawText(canvas, font_read,
    #             x_text + 1.0*hskip, y_text + 1.0*vskip, textColor,
    #             readings[3]['book']);
    #     graphics.DrawText(canvas, font_read,
    #             x_text + 2.0*hskip, y_text + 2.0*vskip, textColor,
    #             readings[3]['chapter'] + ":" + readings[3]['verse']);
    #
    # # swap, pause, then clear the canvas
    # canvas= matrix.SwapOnVSync(canvas);
    # time.sleep(sleeptime);
    # canvas.Clear();


### MAIN LOOP

# pages= [noisy, textscroll];
pages= [noisy, jesus, readings_pager,];
# pages= [jesus, readings_pager,];
# pages= [readings_scroller,];

debug_counter= 0;
debug_count= 1;

while True:
    for page in pages:
        page(matrix, canvas);
        # clear old canvas to prevent weird stuff
        canvas.Clear();
        canvas= matrix.CreateFrameCanvas();

    # # for now, just cycle through
    # debug_counter += 1;
    # if debug_counter >= debug_count:
    #     break;
