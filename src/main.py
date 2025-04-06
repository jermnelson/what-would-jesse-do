"""Python source code for What Would Jesse Do?"""
__author__ = "Jeremy Nelson"

import random

from pyscript.web import page

def show_wwjd():
    invisible_wwjds = page.find(".invisible")
    wwjd_idx = random.randint(0, len(invisible_wwjds)+1)
    print(wwjd_idx, len(invisible_wwjd))
    invisible_wwjds[wwjd_idx].classes.pop()
    
