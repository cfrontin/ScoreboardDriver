
import json;
import math;
import time;
import textwrap;
import urllib.request;

from datetime import datetime;
from datetime import timedelta;
from bs4 import BeautifulSoup;
from PIL import Image;

from rgbmatrix import RGBMatrix;
from rgbmatrix import graphics;

def fetch_readings_api():

    today= datetime.today();

    # dictionary to connect USCCB link keys to bible book names
    booknames= {
            'GN': "Genesis",
            'EX': "Exodus",
            'LV': "Leviticus",
            'NM': "Numbers",
            'DT': "Deuteronomy",
            'JOS': "Joshua",
            'JGS': "Judges",
            'RU': "Ruth",
            '1 SM': "1 Samuel",
            '2 SM': "2 Samuel",
            '1 KGS': "1 Kings",
            '2 KGS': "2 Kings",
            '1 CHR': "1 Chronicles",
            '2 CHR': "2 Chronicles",
            'EZR': "Ezra",
            'NEH': "Nehemiah",
            'TB': "Tobit",
            'JDT': "Judith",
            'JUDITH': "Judith", # weird bug
            'EST': "Esther",
            '1 MC': "1 Maccabees",
            '2 MC': "2 Maccabees",
            'JB': "Job",
            'PS': "Psalms",
            'PRV': "Proverbs",
            'ECCL': "Ecclesiastes",
            'SG': "Song of Songs",
            'WIS': "Wisdom",
            'SIR': "Sirach",
            'IS': "Isaiah",
            '1 IS': "Isaiah", # weird bug
            'JER': "Jeremiah",
            'LAM': "Lamentations",
            'BAR': "Baruch",
            'EZ': "Ezekiel",
            'DN': "Daniel",
            'HOS': "Hosea",
            'JL': "Joel",
            'AM': "Amos",
            'OB': "Obadiah",
            'JON': "Jonah",
            'MI': "Micah",
            'NA': "Nahum",
            'HB': "Habakkuk",
            'ZEP': "Zephaniah",
            'HG': "Haggai",
            'ZEC': "Zechariah",
            'MAL': "Malachi",
            'MT': "Matthew",
            'MK': "Mark",
            'LK': "Luke",
            'JN': "John",
            'ACTS': "Acts",
            'ROM': "Romans",
            '1 COR': "1 Corinthians",
            '2 COR': "2 Corinthians",
            'GAL': "Galatians",
            'EPH': "Ephesians",
            'PHIL': "Philippians",
            'COL': "Colossians",
            '1 THES': "1 Thessalonians",
            '2 THES': "2 Thessalonians",
            '1 TM': "1 Timothy",
            '2 TM': "2 Timothy",
            'TI': "Titus",
            'PHLM': "Philemon",
            'HEB': "Hebrews",
            'JAS': "James",
            '1 PT': "1 Peter",
            '2 PT': "2 Peter",
            '1 JN': "1 John",
            '2 JN': "2 John",
            '3 JN': "3 John",
            'JUDE': "Jude",
            'RV': "Revelation",
    };

    # prep items to carry daily readings
    reading1= None;
    responsorial= None;
    reading2= None;
    gospel= None;

    title= None;
    season= None;

    url_raw= "https://raw.githubusercontent.com/conciergewebco/weekly-readings/master/weekly-readings-api.json";
    with urllib.request.urlopen(url_raw) as url_data:
        reading_data= json.loads(url_data.read().decode());

    # dig down to the data of interest
    reading_data= reading_data['dates'];
    reading_data= reading_data["%04d" % today.year];
    reading_data= reading_data["%02d" % today.month];
    reading_data= reading_data["%02d" % today.day];

    title= reading_data['title'];
    season= reading_data['lit_season'];

    for rd_ky in reading_data['readings'].keys():
        book= None;
        chapverse= None;

        swapped= False;
        for bk_key in booknames.keys():
            if reading_data['readings'][rd_ky].startswith(bk_key):
                book= booknames[bk_key];
                chapverse_pre= reading_data['readings'][rd_ky][(len(bk_key) + 1):].replace('—', '-');
                print(chapverse_pre); # DEBUG!!!!!
                if reading_data['readings'][rd_ky][(len(bk_key) + 1):].count(' ') < 2:
                    chapverse= chapverse_pre.replace('AND', 'and');
                else:
                    chapverse= chapverse_pre.replace(' AND', ', and');
                swapped= True;
                break;
        if not swapped:
            raise Exception("invaled bible book key: %s" %
                    reading_data['readings'][rd_ky]);

        if rd_ky == 'reading_1':
            reading1= {'book': book, 'chapverse': chapverse};
        elif rd_ky == 'psalm':
            responsorial= {'book': book, 'chapverse': chapverse};
        elif rd_ky == 'reading_2':
            reading2= {'book': book, 'chapverse': chapverse};
        elif rd_ky == 'gospel':
            gospel= {'book': book, 'chapverse': chapverse};

    readings= [];
    for reading in [reading1, responsorial, reading2, gospel]:
        if reading is not None:
            readings.append(reading);

    return (readings, title, season);

def fetch_readings():
    # return fetch_readings_scrape()[0];
    return fetch_readings_api();

def jesus(matrix, canvas):

    canvas.Clear();

    (readings, title, season)= fetch_readings();

    # open the file with the picture
    if "good friday" in title.lower():
        image= Image.open('img/jesus_is_dead.jpg');
    else:
        image= Image.open('img/jesus_is_cool.jpg');
    (img_width, img_height)= image.size;

    # convert to fit the thing
    image= image.resize((matrix.width,
            math.floor(img_height/img_width*matrix.width)), Image.ANTIALIAS);
    (img_width, img_height)= image.size;

    # position
    x_img= 0;
    y_img= 0;

    # scroll presets
    delta= +1;
    passed= False;

    # loop
    while True:
        canvas.SetImage(image, x_img, -y_img);
        # canvas.SetImage(image, x_img, -y_img + img_height);

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

    time.sleep(4.0);

def readings_pager(matrix, canvas):

    # colors
    c_bg= {'r': 7, 'g': 15, 'b': 25};
    c_text= {'r': 255, 'g': 235, 'b': 59};
    c_head= {'r': 155, 'g': 41, 'b': 21};

    # default setting while fetching
    canvas.Clear();
    canvas.Fill(c_bg['r'], c_bg['g'], c_bg['b']);

    # fetch readings
    (readings, title, season)= fetch_readings();

    # change based on liturgical season
    if "good friday" in title.lower():
        c_bg= {'r': 0, 'g': 0, 'b': 0};
        c_text= {'r': 255, 'g': 255, 'b': 255};
        c_head= {'r': 255, 'g': 255, 'b': 255};
    elif 'ordinary' in season.lower():
        c_bg= {'r': 3, 'g': 76, 'b': 44};
        c_text= {'r': 255, 'g': 235, 'b': 59};
        c_head= {'r': 155, 'g': 41, 'b': 21};
    elif ('advent' in season.lower() and 'third week' in title.lower()):
        c_bg= {'r': 181, 'g': 92, 'b': 124};
        c_text= {'r': 220, 'g': 220, 'b': 220};
        c_head= {'r': 18, 'g': 13, 'b': 49};
    elif ('lent' in season.lower()) or ('advent' in season.lower()):
        c_bg= {'r': 79, 'g': 6, 'b': 127};
        c_text= {'r': 255, 'g': 235, 'b': 59};
        c_head= {'r': 58, 'g': 86, 'b': 131};
    elif 'easter' in season.lower():
        c_bg= {'r': 255, 'g': 253, 'b': 158};
        c_text= {'r': 0, 'g': 71, 'b': 119};
        c_head= {'r': 7, 'g': 59, 'b': 58};
    elif 'christmas' in season.lower():
        c_bg= {'r': 11, 'g': 110, 'b': 79};
        c_text= {'r': 255, 'g': 253, 'b': 158};
        c_head= {'r': 155, 'g': 41, 'b': 21};

    # scroll timer
    sleeptime= 10.0;
    scrolltime= 0.5;

    # get color
    textColor= graphics.Color(c_text['r'], c_text['g'], c_text['b']);
    headColor= graphics.Color(c_head['r'], c_head['g'], c_head['b']);

    # get and load a font
    font_title= graphics.Font();
    font_title.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf");
    vskip= math.floor(1.5*font_title.height);
    hskip= math.floor(0.5*font_title.height);

    # the position we start at: edge of the screen
    x_title= 3;
    y_title= 12;

    buffer= 3;

    numchars= math.floor((matrix.width - 2*buffer)/6);
    title_printable= textwrap.wrap(title, numchars);

    def do_title(canvas, lines):

        keep_scrolling= True;
        offset= 0;

        while keep_scrolling:

            # clear the canvas
            canvas.Clear();
            canvas.Fill(c_bg['r'], c_bg['g'], c_bg['b']);

            i= 0;

            for line in lines:
                # draw the desired text
                graphics.DrawText(canvas, font_title,
                        x_title + 1.0*hskip, y_title + i*vskip + offset,
                        textColor, line);
                i += 1;

            # scroll on, flag if it should keep scrolling after
            offset -= 1;
            keep_scrolling= y_title + (i + 2)*vskip + offset > matrix.width - buffer;

            # swap, then pause
            canvas= matrix.SwapOnVSync(canvas);
            time.sleep(scrolltime);

        # swap, pause, then clear the canvas
        time.sleep(sleeptime - scrolltime);
        canvas.Clear();

    do_title(canvas, title_printable);

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
                    x_text + 0.0*hskip, y_text + 0.0*vskip, headColor,
                    header);

            # draw the desired text
            graphics.DrawText(canvas, font_read,
                    x_text + 1.0*hskip, y_text + 1.0*vskip, textColor,
                    reading['book']);
            len_txt= graphics.DrawText(canvas, font_read,
                    x_text + 2.0*hskip + offset,
                    y_text + 2.0*vskip, textColor,
                    reading['chapverse']);

            # scroll on, flag if it should keep scrolling after
            offset -= 1;
            keep_scrolling= x_text + 2.0*hskip + offset + len_txt > matrix.width - buffer;

            # swap, then pause
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

# def readings_scroller(matrix, canvas):
#
#     # scroll timer
#     sleeptime= 0.2;
#     sleeptime_first= 2.0;
#     is_first= True;
#
#     # the position we start at: edge of the screen
#     x_text= 0;
#     y_text= 10;
#
#     while True:
#
#         # get and load a font
#         font_head= graphics.Font();
#         font_head.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/tom-thumb.bdf");
#         vskip= math.floor(1.5*font_head.height);
#         hskip= math.floor(0.5*font_head.height);
#
#         # get color
#         textColor= graphics.Color(000, 153, 255);
#
#         # fetch readings
#         readings= fetch_readings();
#
#         # clear the canvas
#         canvas.Clear();
#
#         # draw the desired text
#         len= graphics.DrawText(canvas, font_head,
#                 x_text + 0.0*hskip, y_text + 0.0*vskip, textColor,
#                 "Daily readings:");
#
#         # get and load a font
#         font_read= graphics.Font();
#         font_read.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/tom-thumb.bdf");
#         vskip= math.floor(1.5*font_read.height);
#         hskip= math.floor(0.5*font_read.height);
#
#         i= 0;
#         for reading in readings:
#             if reading is not None:
#                 i += 1;
#                 # draw the desired text
#                 len= graphics.DrawText(canvas, font_read,
#                         x_text + 1.0*hskip, y_text + i*vskip, textColor,
#                         reading['book']);
#                 i += 1;
#                 len= graphics.DrawText(canvas, font_read,
#                         x_text + 2.0*hskip, y_text + i*vskip, textColor,
#                         reading['chapverse']);
#
#         canvas= matrix.SwapOnVSync(canvas);
#
#         if is_first:
#             time.sleep(sleeptime_first);
#             is_first= False;
#         else:
#             time.sleep(sleeptime);
#
#         y_text -= 1;
#
#         if y_text < -(i + 2)*vskip:
#             break;

# def fetch_readings_scrape():
#
#     # USCCB daily readings page
#     with urllib.request.urlopen("http://usccb.org/bible/readings/") as page:
#         soup= BeautifulSoup(page, 'html.parser');
#
#     # dictionary to connect USCCB link keys to bible book names
#     booknames= {
#             'genesis': "Genesis",
#             'exodus': "Exodus",
#             'leviticus': "Leviticus",
#             'numbers': "Numbers",
#             'deuteronomy': "Deuteronomy",
#             'joshua': "Joshua",
#             'judges': "Judges",
#             'ruth': "Ruth",
#             '1samuel': "1 Samuel",
#             '2samuel': "2 Samuel",
#             '1kings': "1 Kings",
#             '2kings': "2 Kings",
#             '1chronicles': "1 Chronicles",
#             '2chronicles': "2 Chronicles",
#             'ezra': "Ezra",
#             'nehemiah': "Nehemiah",
#             'tobit': "Tobit",
#             'judith': "Judith",
#             'esther': "Esther",
#             '1mc': "1 Maccabees",
#             '2mc': "2 Maccabees",
#             'job': "Job",
#             'psalms': "Psalms",
#             'proverbs': "Proverbs",
#             'ecclesiastes': "Ecclesiastes",
#             'songofsongs': "Song of Songs",
#             'wisdom': "Wisdom",
#             'sirach': "Sirach",
#             'isaiah': "Isaiah",
#             'jeremiah': "Jeremiah",
#             'lamentations': "Lamentations",
#             'baruch': "Baruch",
#             'ezekiel': "Ezekiel",
#             'daniel': "Daniel",
#             'hosea': "Hosea",
#             'joel': "Joel",
#             'amos': "Amos",
#             'obadiah': "Obadiah",
#             'jonah': "Jonah",
#             'micah': "Micah",
#             'nahum': "Nahum",
#             'habakkuk': "Habakkuk",
#             'zephaniah': "Zephaniah",
#             'haggai': "Haggai",
#             'zechariah': "Zechariah",
#             'malachi': "Malachi",
#             'matthew': "Matthew",
#             'mark': "Mark",
#             'luke': "Luke",
#             'john': "John",
#             'acts': "Acts",
#             'romans': "Romans",
#             '1corinthians': "1 Corinthians",
#             '2corinthians': "2 Corinthians",
#             'galatians': "Galatians",
#             'ephesians': "Ephesians",
#             'philippians': "Philippians",
#             'colossians': "Colossians",
#             '1thessalonians': "1 Thessalonians",
#             '2thessalonians': "2 Thessalonians",
#             '1timothy': "1 Timothy",
#             '2timothy': "2 Timothy",
#             'titus': "Titus",
#             'philemon': "Philemon",
#             'hebrews': "Hebrews",
#             'james': "James",
#             '1peter': "1 Peter",
#             '2peter': "2 Peter",
#             '1john': "1 John",
#             '2john': "2 John",
#             '3john': "3 John",
#             'jude': "Jude",
#             'revelation': "Revelation",
#     };
#
#     # prep items to carry daily readings
#     reading1= None;
#     responsorial= None;
#     reading2= None;
#     gospel= None;
#
#     # function to process a scaped item
#     def process_brw(wrapper):
#
#         # print("\nwrapper:\n")
#         # print(wrapper);
#
#         text= wrapper.find('h4').find('a').text;
#         href= wrapper.find('h4').find('a')['href'];
#
#         # href= href.split('/bible/readings')[-1];
#         href= href.split('/bible/')[-1];
#
#         # print(text);
#         # print(href);
#
#         book= booknames[href.split('/')[0].lower()];
#         chapter= href.split('/')[1].split(':')[0];
#         verse= href.split('/')[1].split(':')[1];
#
#         # print(book);
#         # print(chapter);
#         # print(verse);
#
#         chapverse= "%s:%s" % (chapter, verse);
#
#         return {'book': book, 'chapverse': chapverse};
#
#     for wrapper in soup.find_all(class_= "bibleReadingsWrapper"):
#         if "Reading 1" in wrapper.find('h4').text:
#             reading1= process_brw(wrapper);
#         elif "Responsorial Psalm" in wrapper.find('h4').text:
#             responsorial= process_brw(wrapper);
#         elif "Reading 2" in wrapper.find('h4').text:
#             reading2= process_brw(wrapper);
#         elif "Gospel" in wrapper.find('h4').text and \
#                 not "Verse Before" in wrapper.find('h4').text:
#             gospel= process_brw(wrapper);
#
#     readings= [];
#     for reading in [reading1, responsorial, reading2, gospel]:
#         if reading is not None:
#             readings.append(reading);
#     return (readings,);
