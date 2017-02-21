#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Interface import Interface
from tkinter import *

if __name__ == '__main__':
    fen = Tk()
    fen.title('Connexion Internet')
    fen.resizable(False,False)
    
    app = Interface(fen)
    app.grid(row=0, column=0, sticky=NSEW)
    
    fen.mainloop()