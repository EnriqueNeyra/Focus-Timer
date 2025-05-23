import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging    
import time
import traceback
from waveshare_OLED import OLED_1in51
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
    disp = OLED_1in51.OLED_1in51()

    logging.info("\r1.51inch OLED ")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("clear display")
    disp.clear()

    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)

    elapsed = 0
    next_tick = time.time()

    while True:
        
        image1 = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        draw.text((24,14), f"{elapsed // 60:02}:{elapsed % 60:02}", font = font1, fill = 0)
        image1 = image1.rotate(180)
        disp.ShowImage(disp.getbuffer(image1))

        elapsed += 1
        next_tick += 1
        sleep_time = max(0, next_tick - time.time())
        time.sleep(sleep_time)

    while True:
        now = time.time()

        image = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image)
        draw.text((x, y), f"{time_str}", font = self.font_cache[font_size], fill = 0)
        image = image.rotate(180)
        self.disp.ShowImage(self.disp.getbuffer(image))

        # Calculate exact next 1-second tick
        next_tick += 1
        sleep_time = max(0, next_tick - time.time())
        time.sleep(sleep_time)

        
    Himage2 = Image.new('1', (disp.width, disp.height), 255)  # 255: clear the frame 
    disp.clear()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()