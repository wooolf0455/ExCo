
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""


##  FILE DESCRIPTION:
##      'lexer' package initialization

# Try importing the Cython module
try:
    import cython_lexers
    cython_lexers_found = True
except Exception as ex:
    cython_lexers_found = False
# Try importing the Nim module
try:
    import nim_lexers
    nim_lexers_found = True
except Exception as ex:
    nim_lexers_found = False

from lexers.ada import *
from lexers.awk import *
from lexers.cicode import *
from lexers.cython import *
from lexers.functions import *
from lexers.nim import *
from lexers.oberon import *
from lexers.python import *
from lexers.routeros import *
from lexers.text import *


"""
Set colors for all other lexers by dynamically creating
derived classes and adding styles to them.
"""
# Lexers that were manually defined above
predefined_lexers = [
    "QsciLexerPython",
]
# Themes that are missing when upgrading QScintilla
missing_themes = {}
# Loop through the Qsci module lexers and adjust them
for i in data.__dict__.keys():
    if i.startswith("QsciLexer") and len(i) > len("QsciLexer"):
        if not(i in predefined_lexers):
            lexer_name = i.replace("QsciLexer", "")
            styles = {}
            cls = getattr(data, i)
            for j in dir(cls):
                att_value = getattr(cls, j)
                if j[0].isupper() == True and isinstance(att_value, int):
                    styles[j] = att_value
            cls_text = "class {0}(data.{1}):\n".format(lexer_name, i)
            cls_text += "    styles = {\n"
            for style in styles:
                cls_text += "        \"{0}\" : {1},\n".format(style, styles[style])
            cls_text += "    }\n"
            cls_text += "    \n"
            cls_text += "    def __init__(self, parent=None):\n"
            cls_text += "        super().__init__()\n"
            cls_text += "        self.set_theme(data.theme)\n"
            cls_text += "    \n"
            cls_text += "    def set_theme(self, theme):\n"
            cls_text += "        self.setDefaultColor(theme.Font.Default)\n".format(lexer_name)
            cls_text += "        self.setDefaultPaper(theme.Paper.Default)\n".format(lexer_name)
            cls_text += "        missing_themes['{}'] = []\n".format(lexer_name)
            for style in styles:
                cls_text += "        for style in self.styles.keys():\n"
                cls_text += "            try:\n"
                cls_text += "                self.setPaper(\n"
                cls_text += "                    data.QColor(theme.Paper.{0}.Default), \n".format(lexer_name)
                cls_text += "                    self.styles[style]\n"
                cls_text += "                )\n"
                cls_text += "                lexers.set_font(self, style, getattr(theme.Font.{0}, style))\n".format(lexer_name)
                cls_text += "            except:\n"
                cls_text += "               if not(style in missing_themes['{}']):\n".format(lexer_name)
                cls_text += "                   missing_themes['{}'].append(style)\n".format(lexer_name)
                cls_text += "        if len(missing_themes['{}']) != 0:\n".format(lexer_name)
                cls_text += "            print(\"Lexer '{}' missing themes:\")\n".format(lexer_name)
                cls_text += "            for mt in missing_themes['{}']:\n".format(lexer_name)
                cls_text += "                print('    - ' + mt)\n"
                cls_text += "            raise Exception(\"Lexer '{}' has missing themes!\")\n".format(lexer_name)
            exec(cls_text)