ppt2beamer
==========

This program aims to convert *.ppt, *.pptx, and *.fodp to latex beamers.

usage
==========
If you have a *.ppt or *.pptx file, first save it as a *.fodp file with LibrOffice.

Then::

$./fodp2tex.py example.fodp > body.tex
$cat header.tex body.tex > beamer.tex
