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
    newtxt = newtxt.replace(u'⇒','$\\textregistered$')
    return newtxt;

def apply_style(stylename, text):
    italic = False
    bold = False
    little = False
    underline = False
    up = False
    courier = False
    for style in stylelist:
         if stylename == style.getAttribute('style:name'):
             text_property = style.firstChild
             for node in style.childNodes:
                 if node.toxml().strip() != '':
                     text_property = node

             font_family = text_property.getAttribute('fo:font-family')
             if font_family != None and font_family == 'Courier':
                 courier = True
             
             font_style = text_property.getAttribute('fo:font-style')
             if font_style != None and font_style == 'italic': 
                 italic = True
             
             font_weight = text_property.getAttribute('fo:font-weight')
             if font_weight != None and font_weight == 'bold':
                 bold = True
                 
             text_position = text_property.getAttribute('style:text-position')
             if text_position != None and text_position == '-25% 58%':
                 little = True
             if text_position != None and text_position == '30% 58%':
                 up = True
    
             style_underline =  text_property.getAttribute('style:text-underline-style')
             if style_underline != None and style_underline == 'solid':
                 underline = True

    math = False
    #1, italic bold underline
    if  italic == True and courier == True:
        text = "\\textit{%s}"% text

    if bold == True:
        text = "\\textbf{%s}"% text
    if underline == True:
        text = '\\underline{%s}'% text

    #2 font family
    if courier == True:
        if text[0] == ' ': text = '\\'+text #if text start with a space, then add a backslash at left 
        text = '{\\tt %s}' %text

    #3 math
    if (italic == True and courier == False ) or little == True or up == True:
        math = True

    updownStr = ''
    if  little == True:
        updownStr = '_'
    elif up ==  True:
        updownStr = '^'

    if math == True and text.strip() != '':
        text= text.replace("$'$","'").replace('$-$','-')
        if len(text) ==1 or bold == True or underline == True or courier == True or (little == False and up == False):
            # text length is one or text has been wrapped.
            text =text.replace(' ','\ ')
            text = "$%s%s$"% (updownStr,text)
        else:
            text = "$%s{%s}$"% (updownStr,text)

    return text


def gen_item(itemlist):
    """
    Generate one line 
    """
    #itemlist is text:p's childNodes : plan text or text:span
    linestring =''
    for tt in itemlist: 
        if(tt.nodeType == 3):  #leaf node, plan text
            linestring = linestring + txt_replace(tt.toxml())

        # text:span
        if (tt.nodeType == 1 and tt.firstChild != None):
            for node in tt.childNodes:
                if node.nodeType == 3:
                    item_style = tt.getAttribute('text:style-name')
                    item_text = txt_replace(node.toxml())
                    item_text = apply_style(item_style,item_text)
                    linestring = linestring + item_text
                elif node.nodeName == 'text:tab':
                    linestring = linestring + '\\hspace{0.2in}'
                elif node.nodeName == 'text:s':
                    spacecount =1
                    text_c = node.getAttribute('text:c');
                    if text_c != None and text_c.strip() != '' :
                        spacecount = int(text_c)
                    
                    linestring = linestring + '\\hspace{%0.2fin}' % (spacecount * 0.08)

    #combine multi math text
    if  (not linestring.__contains__('_')) and (not linestring.__contains__('^')):
        linestring =linestring.replace('$$','').replace('$ $',' ')
    return linestring


def getListLevel(text):
    """
    Get list's level and style
    """
    textlist={}
    textlist['style'] =''
    level = 0
    node = None
    while node == None or node.nodeName[:4] == 'text':
        if node == None:
            node =text.parentNode
        else:
            node = node.parentNode

        if node.nodeName == 'text:list':
            style =node.getAttribute('text:style-name')
            if style != None and style.strip() != '': 
                textlist['style'] = style
            else:
                textlist['style'] = ''
            level = level + 1

    textlist['level'] = level
    return textlist
        
def showBullet(listStylename,level):
    for style in textlistStyles:
        if listStylename == style.getAttribute('style:name'):
            for node in style.childNodes:
                if node.nodeType == 1 and int( node.getAttribute('text:level')) == level and node.nodeName == 'text:list-level-style-number':
                    return False
    return True

def gen_frame(textlist):
    """
    handle one of frames in a page
    """
    stack =[]  #init list stack
    for text in textlist:
        textlist=getListLevel(text)
        level = textlist['level']
        listStylename = textlist['style']

        itemstr = "  \\item "
        if showBullet(listStylename,level) == False:
            itemstr = "  \\item[] "

        if level == 4: 
            itemstr = ' ' * 2 * 4 + "\\item[] -- "
        elif len(stack) == 0: 
            stack.append(level)
            print "  \\begin{itemize}"
        else:
            if level > stack[len(stack)-1]:
                print "    \\begin{itemize}"
                stack.append(level)
            if level < stack[len(stack)-1]:
                stack.remove(stack[len(stack)-1])
                print "    \\end{itemize}"
                if len(stack) > 0 and level < stack[len(stack)-1] :
                    stack.remove(stack[len(stack)-1])
                    print "    \\end{itemize}"

        if len(text.childNodes) > 0: 
            linestring =gen_item(text.childNodes)
            if linestring.strip() != '' :
                # if line start with [, then change it to {[}, or line will show as a bullet
                if linestring.strip()[0] == '[':
                    linestring = linestring.replace('[','{[}',1)
                print ' ' * 2 * len(stack) + itemstr +linestring


    #complete items
    for i in range(1,len(stack)+1):
        print ' ' * 2 * (len(stack)+1 -i) + "\\end{itemize}"



def handle_page(page):
    """
    Convert one "draw:page" to one slide of beamer
    """
    pre_pagename = ''

    textps = page.getElementsByTagName("text:p")
    if len(textps) == 0:
        drawName =page.getAttribute('draw:name')
        print "\\begin{frame}[fragile]{%s}" % drawName
        print "No title and No text"

    #draw:frame
    drawFrames = page.getElementsByTagName("draw:frame")
    presentFrameCount = 0
    for frame in drawFrames:
        preStyleName = frame.getAttribute("presentation:style-name")
        if preStyleName == None or preStyleName.strip() == '': continue
        presentationClass = frame.getAttribute('presentation:class')
        if presentationClass == 'notes':continue
        presentFrameCount = presentFrameCount +1
        if presentFrameCount == 1: 
            textlist =frame.getElementsByTagName("text:p")
            if len(textlist) > 0:
                pagename =gen_item(textlist[0].childNodes)
                pre_pagename = pagename
                print "\\begin{frame}[fragile]{%s}" % pagename
                gen_frame(textlist[1:])
                continue
            else:
                # if pagename not exist, use previous one
                print "\\begin{frame}[fragile]{%s}" % pre_pagename
                continue
                
        else:
            textlist =frame.getElementsByTagName("text:p")
            gen_frame(textlist)

    #if no present frame, then print the title
    if presentFrameCount == 0:
        print "\\begin{frame}[fragile]{%s}" % pre_pagename
    drawCustomShapes = page.getElementsByTagName("draw:custom-shape")
    if len(drawCustomShapes) > 0: 
        print 'some custom-shape here'
    drawImage = page.getElementsByTagName("draw:image")
    if len(drawImage) > 0 :
        print 'some draw:image here'
    if len(textps) == 1:
        print "Only title!"

    print "\\end{frame}\n"


'''
main entry
'''
#get fodp file name and parse it to xml
filename =sys.argv[1]
if not filename.endswith(".fodp"):
    print "Please input a *.fodp file!"
    sys.exit()

xmldoc = minidom.parse(filename)
root =xmldoc.firstChild

#read styles
stylelist  =root.getElementsByTagName('style:style')
print '%%style number %d ' % len(stylelist)

#read text:list-style
textlistStyles = root.getElementsByTagName('text:list-style')
print '%%text list style number %d ' % len(textlistStyles)

#read pages
pagelist = root.getElementsByTagName('draw:page')
print '%%page number %d ' % len(pagelist)

pagecount =0
for page in pagelist:
    pagecount = pagecount + 1
    print '%%page %d' % pagecount
    handle_page(page)

print '\\end{document}'
