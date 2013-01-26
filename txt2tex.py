#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:       Yufei Gu
@license:      GNU General Public License 2.0 or later
@contact:      flyrain000@gmail.com
"""

from xml.dom import minidom
import sys

def txt_replace(text):
    newtxt = ''
    for c in text:
        if c == '$' or c == '_' or c== '{' or c == '}' or c == '#' or c == '%':
            newtxt= newtxt + '\\'+c
        elif c == '\\':
            newtxt = newtxt + '$\\backslash$'
        else:
            newtxt = newtxt + c
    
    newtxt = newtxt.replace('&lt;',"<").replace('&gt;',">").replace('&amp;','\\&').replace('&quot;','"')
    newtxt = newtxt.replace('&','\\&')
    newtxt = newtxt.replace(u'…', '...').replace(u'“','``').replace(u'”',"''").replace(u'‘',"'").replace(u'’',"'")
    newtxt = newtxt.replace(u'≤', '$\\leq$').replace(u'',"$'$").replace(u'','$\\delta$').replace(u'','$\\leq$').replace(u'','$\\geq$')
    newtxt = newtxt.replace(u'','$\\not =$')
    newtxt = newtxt.replace(u'|–','$\\vdash$').replace(u'','$\\cup$').replace(u'','$\\nu$')
    newtxt = newtxt.replace(u'•','$\\bullet$').replace(u'','$\\in$').replace(u'','$\\tau$')
    newtxt = newtxt.replace(u'','$\\times$').replace(u'×','$\\times$').replace(u'','$\\varnothing$').replace(u'','$\\vee$')
    newtxt = newtxt.replace(u'','$\\subseteq$')
    #arrow
    newtxt = newtxt.replace(u'','$\\Rightarrow$').replace(u'','$\\leftarrow$').replace(u'','$\\Leftarrow$').replace(u'','$\\rightarrow$')
    newtxt = newtxt.replace(u'','')
    newtxt = newtxt.replace(u'','$\\wedge$').replace(u'´',"$'$")
    newtxt = newtxt.replace(u'','$\\notin$').replace(u'','$\\forall$').replace(u'','$\\exists{}$')
    newtxt = newtxt.replace(u'→','$\\rightarrow$').replace(u'','$\\rightarrow$')
    #em-dash and minus in math
    newtxt = newtxt.replace(u'—','---').replace(u'–','$-$')
    #Greek letters
    newtxt = newtxt.replace(u'','$\\alpha$').replace(u'','$\\rho$').replace(u'','$\\omega$')
    newtxt = newtxt.replace(u'','$\\Delta$').replace(u'','$\\sigma$').replace(u'', '$\\Sigma$')
    newtxt = newtxt.replace(u'', '$\\pi$').replace(u'','$\\mu$').replace(u'','$\\varphi$')
    newtxt = newtxt.replace(u'', '$\\phi$')

    newtxt = newtxt.replace(u'æ','\\ae{}').replace(u'è',"\\`{e}")
    newtxt = newtxt.replace(u'≈','$\\approx$').replace(u'~','$\\sim$').replace(u'≠','$\\neq$').replace(u'','$\\equiv$').replace(u'','$\\oplus$')
    newtxt= newtxt.replace(u'','$\\uparrow$').replace(u'','$\\Leftrightarrow$').replace(u'†','$\\dag$').replace(u'','$\\neg{}$')
    newtxt = newtxt.replace(u'','$\\cap$').replace(u'','$\\lfloor$').replace(u'','$\\rfloor$').replace(u'≥','$\\geq$').replace(u'','$\\not \\subset$').replace(u'','$\\approx$')
    newtxt = newtxt.replace(u'⇒','$\\textregistered$').replace(u'ø','$\\o$');
    newtxt = newtxt.replace(u'®','$\\textsuperscript{\\textregistered}$').replace(u'：',':')
    return newtxt;


def strReplace(text):
    newtxt = text.rstrip()
    newtxt = newtxt.replace('\xe2\x80\xa6', '...').replace('\xe2\x80\x9c','``')
    newtxt = newtxt.replace('\xe2\x80\x9d', "''").replace('_','\\_').replace('\xe2\x80\x99s',"'");
    return newtxt

'''
main entry
'''
import re

filename =sys.argv[1]
f = open(filename)
count = 5
lines = f.readlines()
isBegin = True
i = 0
while i < len(lines):
    line = lines[i];
    if line.startswith( "\\end{frame}\\n\\begin{frame}[fragile]{}"):
        if isBegin == True:
            isBegin = False 
            print "  \\end{itemize}"
        
        count = count +1
        title = ''
        if(i+2 < len(lines)):
            title = lines[i +2]
            i = i + 2
        print "\\end{itemize}"
        print "\\end{frame}\n\n\n %%page %d" % count 
        
        print "\\begin{frame}[fragile]{%s}" % strReplace(title)
        print "\\begin{itemize}"

    elif line == '\n' or re.match('\d{1,2}$',line.rstrip()) != None:
        i = i +1
        continue
    elif line.startswith('\xe2\x80\xa2\xe2\x80\xaf') :
        if isBegin == True:
            isBegin = False 
            print "  \\end{itemize}"

        line=line.replace('\xe2\x80\xa2\xe2\x80\xaf','  \\item ')
        print strReplace(line)
    elif line.startswith('\xe2\x80\x93\xe2\x80\xaf'):
        if isBegin == False: 
            print "  \\begin{itemize}"
            isBegin = True
        line=line.replace('\xe2\x80\x93\xe2\x80\xaf','    \\item ')
        print strReplace(line)
    elif line.startswith('\x0c'):
        if isBegin == True:
            isBegin = False 
            print "  \\end{itemize}"
        
        count = count +1
        title = line.replace('\x0c','');
        print "\\end{itemize}"
        print "\\end{frame}\n\n\n %%page %d" % count 
        
        print "\\begin{frame}[fragile]{%s}" % strReplace(title)
        print "\\begin{itemize}"
  
    else:
        print strReplace(line)

    i = i+1
