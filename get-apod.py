#!/usr/bin/env python
#
# Get APOD
#
# This python script downloads the current Astronomy Picture of the Day.
# Then, if you have the Python Imaging Library installed, it displays
# the picture in a Tkinter window.
# Pay attention to the text window!  You can read the explanation of
# of the picture there.  Even if there is no picture (sometimes there
# is a video) you can still see the title and explanation.
# The script also has an optional command-line argument that lets you
# view the picture for specific date.  The format of the date is YYMMDD.
#
# Usage:  python get-apod.py [YYMMDD]
#
# Author: Joseph Maruschek (joe.maruschek@gmail.com)
#
import sys        # needed for the command-line argument
import textwrap   # needed for pretty-printing the explanation
import urllib     # needed for urlopen() and urlretrieve()
import re         # needed for regular expressions
from Tkinter import *  # for displaying the picture
import Image      # needed for jpeg support
import ImageTk    # needed to convert image to a Tk-compatible image
# if you have Pillow instead of PIL, use these two lines instead:
#from PIL import Image
#from PIL import ImageTk

def display_picture(picture_file,title):
    """This routine creates a simple Tkinter window to show a picture"""
    # Create a window
    root=Tk()
    root.wm_title(title)

    # Load image and convert it for Tkinter
    img = Image.open(picture_file)
    photo = ImageTk.PhotoImage(img)

    # Use a label widget to display the photo
    w=Label(image=photo,bd=0)
    w.image=photo
    w.pack()

    # Start the window loop
    root.mainloop()

def remove_html(text):
    """
    This function removes embedded html from a string
    using brute force: it copies one string to another
    and skips anything in <...>.
    """
    no_html=""
    copy=True
    for char in text:
        if char=="<":
            copy=False
        if copy:
            no_html=no_html+char
        if char==">":
            copy=True
    return no_html

def find_title_and_explanation(text):
    """ This function tries to find the title and explanation of the picture """
    #print text
    match=re.search(r'<center>\s*<b>(.*)</b> <br>',text)
    if match:
        title=match.group(1)
    else:
        title="No title"
    match=re.search(r'(Explanation:.*<p> <center>)',text,re.DOTALL)
    if match:
        expl=remove_html(match.group(1))
    else:
        expl="No explanation."
    # I do three things to the explanation before returning it:
    # I split it up into a list of words to get rid of the extra
    # whitespace and newlines, I then join that list back into one
    # string with just a space between each word, and then I use
    # the textwrap library to nicely format the text for printing.
    return title,textwrap.fill(" ".join(expl.split()))
    
##--------------Main program starts here-----------------------

# Set this variable to the address you use for APOD
apod_base="http://apod.nasa.gov/apod/"

# Make a request for the APOD web site
if len(sys.argv)>1: # if there is a command-line argument, ask for that date
    request = urllib.urlopen(apod_base+"ap"+sys.argv[1]+".html")
else:
    request = urllib.urlopen(apod_base)
content = request.read()

# Search the content for the IMG tag
match=re.search(r'IMG SRC="(.*)"',content)
if match:
    picture_url=apod_base+match.group(1)
    match=re.search(r'/([^/]*)$',picture_url)  # get the file name of the pic
    if match:
        picture_file=match.group(1)
        urllib.urlretrieve(picture_url,picture_file)  # save pic into a file
        title,expl=find_title_and_explanation(content)
        print expl
        display_picture(picture_file,title)
    else:
        print "Could not extract name of file."
else:
    print "No picture today.  Probably a video."
    title,expl=find_title_and_explanation(content)
    print title
    print expl

if sys.platform=="win32": raw_input("Press Enter to close")
