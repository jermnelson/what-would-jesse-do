"""Python source code for What Would Jesse Do?"""
__author__ = "Jeremy Nelson"

import random

from pyscript.web import page

def show_wwjd():
    invisible_wwjds = page.find("li.invisible")
    wwjd_idx = random.randint(0, len(invisible_wwjds)+1)
    invisible_wwjds[wwjd_idx].classes.pop()
    
