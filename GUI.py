# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 13:00:46 2021

@author: rolan
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

from scraping import get_markes, get_modeliai, get_category, get_detales

def GUI(mark_list, mark_title):
    def mark_changed(event):
        global model_title
        model_title, x = get_modeliai(Combo_mark.get(), mark_title)
        Combo_model.config(value = x)

    def model_changed(event):
        global parts_title
        parts_title, x = get_category(Combo_model.get(), model_title)
    
        for i in range(len(x)):
            listbox.delete(i)
        for i in range(len(x)):
            listbox.insert(i, x[i])

    def category_changed(event):
        global detales

    root = tk.Tk()
    root.geometry("500x500")
    root.pack_propagate(False)
    root.resizable(0, 0)

    frame1 = tk.LabelFrame(root, text = "Detales")
    frame1.place(height=250, width=500)

    file_frame = tk.LabelFrame(root, text = "Ieskoti")
    file_frame.place(height = 100, width = 200, rely=0.50,relx = 0.60)

    ##
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1,relwidth=1)

    search = tk.Entry(file_frame, width = 15)
    search.place(rely=0.40, relx = 0.25)

    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treescrollx.pack(side="bottom", fill = "x")
    treescrolly.pack(side="right", fill= "y")

    button1 = tk.Button(root, text = "Visi prekės",height = 3, width = 20, command=lambda: Load_data())
    button1.place(rely=0.80, relx=0.60)

    button2 = tk.Button(file_frame, text = "Paieška", command=lambda: Search())
    button2.place(rely=0.35, relx=0.65)
    model_list = []
    marke = tk.StringVar()
    model = tk.StringVar()

    Combo_mark = ttk.Combobox(root, values = mark_list)
    Combo_mark.set("Markė")
    Combo_mark.place(relx = 0.05, rely = 0.55)
    ## MARKE
    Combo_mark.bind('<<ComboboxSelected>>',  mark_changed)


    Combo_model = ttk.Combobox(root, values = [])
    Combo_model.set("Modelis")
    Combo_model.place(relx = 0.05, rely = 0.60)
    Combo_model.bind('<<ComboboxSelected>>', model_changed)
    ## Model

    listbox = tk.Listbox(root, width = 47, selectmode = "SINGLE")
    listbox.place(relx = 0, rely = 0.65)
    #listbox.bind('<<ListboxSelect>>', category_changed)


    def Load_data():
        clear_data()

        detales = get_detales(listbox.get("anchor"), Combo_mark.get(), parts_title)

        tv1["column"] = list(detales.columns)
        tv1["show"] = "headings"
        for column in tv1["column"]:
            tv1.heading(column, text=column)

        df_rows = detales.to_numpy().tolist()
        for row in df_rows:
            tv1.insert("", "end", values=row)
        return None

    def Search():
        clear_data()
        a = str(search.get())
        d1 = detales[detales['Detalė'].str.contains(a)]

        tv1["column"] = list(d1.columns)
        tv1["show"] = "headings"
        for column in tv1["column"]:
            tv1.heading(column, text=column)

        df_rows = d1.to_numpy().tolist()
        for row in df_rows:
            tv1.insert("", "end", values=row)
        return None

    def clear_data():
        tv1.delete(*tv1.get_children())


    root.mainloop()