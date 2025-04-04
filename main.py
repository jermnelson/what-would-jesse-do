"""Python source code for What Would Jesse Do?"""
__author__ = "Jeremy Nelson"

import random

from js import document

def show_wwjd():
    invisible_wwjds = document.querySelector("li.invisible")
    wwjd_idx = random.randint(0, len(invisible_wwjds)+1)
    invisible_wwjds[wwjd_idx].classes.pop()
    
