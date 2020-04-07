
import json;
import math;
import time;
import random as rng;
import sys;
import textwrap;
import urllib.request;

from datetime import datetime;
from datetime import timedelta;

import requests;
from bs4 import BeautifulSoup;

from PIL import Image;

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

url_raw= "https://raw.githubusercontent.com/conciergewebco/weekly-readings/master/weekly-readings-api.json";
with urllib.request.urlopen(url_raw) as url_data:
    reading_data= json.loads(url_data.read().decode());

# dig down to the data of interest
reading_data= reading_data['dates'];
# reading_data= reading_data["%04d" % today.year];
# reading_data= reading_data["%02d" % today.month];
# reading_data= reading_data["%02d" % today.day];

seasons= [];

# print stuff
def handler(reading_data):

    output= {};

    for key in reading_data.keys():
        print("%s:" % key);

        if key == 'readings':

            for reading_key in reading_data['readings'].keys():
                book= None;
                chapverse= None;

                print("\t%s:" % reading_key);
                swapped= False;
                for bk_key in booknames.keys():
                    if reading_data[key][reading_key].startswith(bk_key):
                        book= booknames[bk_key];
                        chapverse= reading_data[key][reading_key][(len(bk_key) + 1):];
                        print("\t\t%s" % reading_data[key][reading_key].replace(
                                bk_key, booknames[bk_key]));
                        print("\t\t\t%s" % book);
                        print("\t\t\t%s" % chapverse);
                        swapped= True;
                        break;
                if not swapped:
                    raise Exception("invalid bible book key: %s" %
                            reading_data[key][reading_key]);
        elif key == 'title':
            width_matrix= 64;
            width_char= 6;
            buffer= 2;
            numchars= math.floor((width_matrix - 2*buffer)/width_char);
            title_printable= textwrap.wrap(reading_data['title'], numchars);
            print("\t%s" % reading_data['title']);
            for line in title_printable:
                print("\t\t%s" % line);
        elif key == 'lit_season':
            if reading_data['lit_season'] not in seasons:
                seasons.append(reading_data['lit_season']);
            print("\t%s" % reading_data[key]);
        else:
            print("\t%s" % reading_data[key]);

        output[key]= {}

for year_key in reading_data.keys():
    for month_key in reading_data[year_key].keys():
        for day_key in reading_data[year_key][month_key].keys():
            # print(reading_data[year_key][month_key][day_key]);
            handler(reading_data[year_key][month_key][day_key]);

# handler(reading_data);

print("\nseasons:")
for season in seasons:
    print("\t%s" % season);
print();
