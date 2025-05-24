import sys
import os

import logging    
import time
import traceback
from lib.waveshare_OLED import OLED_1in51
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

    font1 = ImageFont.truetype(os.path.join('../lib/waveshare_OLED', 'Font.ttc'), 32)

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


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()