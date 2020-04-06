
import math;
import time;
import random as rng;
import sys;

import requests;
from bs4 import BeautifulSoup;

from PIL import Image;

image= Image.open('img/jesus_is_cool.jpg');

(image_width, image_height)= image.size;

# make image fit our screen.
image= image.resize((64, math.floor(image_height/image_width*64)));
image.show();
