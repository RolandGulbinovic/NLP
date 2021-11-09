
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import webbrowser

from scraping import get_markes, get_modeliai, get_category, get_detales


# Graphical interfeisas
def GUI(mark_list, mark_title, ft):
    def get_tokens(words): # gauti atskirus zodzius
        tokens = words.split()
        return tokens

    def relevant_words(searching): # naudojant fasttext paketo lietuvisku zodziu vektoriu randami 10 panasiausi zodziai
        relevant_word_list = []
        for i in searching:
            relevant_word_list += ft.get_nearest_neighbors(i, k = 10)

        for i in range(len(relevant_word_list)):
            relevant_word_list[i] = relevant_word_list[i][1].lower()
            
        return relevant_word_list
    
    def mark_changed(event): # metodas, kad gauti markes modelius Combobox
        global model_title
        model_title, x = get_modeliai(Combo_mark.get(), mark_title)
        Combo_model.config(value = x)

    def model_changed(event): # metodas, kad gauti kategorijas listbox
        global parts_title
        parts_title, x = get_category(Combo_model.get(), model_title)
    
        for i in range(len(x)):
            listbox.delete(i)
        for i in range(len(x)):
            listbox.insert(i, x[i])
    
    def vidurkis(x):
        mean = 0
        n = len(x)
        for i in x:
            mean += i
        
        mean = mean/n
    
        return mean
    
    root = tk.Tk()
    root.geometry("500x500")
    root.pack_propagate(False)
    root.resizable(0, 0)

    frame1 = tk.LabelFrame(root, text = "Detales")
    frame1.place(height=250, width=500)

    file_frame = tk.LabelFrame(root, text = "Paieška")
    file_frame.place(height = 70, width = 200, rely=0.65,relx = 0.60)

    # TreeView, kad duomenys parodyti
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1,relwidth=1)

    search = tk.Entry(file_frame, width = 15)
    search.place(rely=0.40, relx = 0.25)
    
    metai = tk.Entry(root, width = 15)
    metai.place(rely=0.58, relx = 0.60)
    
    filter_metai = tk.Button(root, text = "vidurki", command=lambda: vidurkiai())
    filter_metai.place(rely=0.59, relx=0.80)
    
    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treescrollx.pack(side="bottom", fill = "x")
    treescrolly.pack(side="right", fill= "y")

    button1 = tk.Button(root, text = "Visi prekės",height = 3, width = 20, command=lambda: Load_data())
    button1.place(rely=0.80, relx=0.60)

    button2 = tk.Button(file_frame, text = "Ieškoti", command=lambda: Search())
    button2.place(rely=0.35, relx=0.65)
    model_list = []
    marke = tk.StringVar()
    model = tk.StringVar()

    
    button3 = tk.Button(root, text = "Atidaryti", command=lambda: selectItem())
    button3.place(rely=0.50, relx=0.75)
    
    
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
    
    # metodas, kuris atidaro pasirinktos prekes puslapi
    def selectItem():
        curItem = tv1.focus()
        webbrowser.open(tv1.item(curItem)['values'][4])
    
    # parodo duomenys TreeView
    def Load_data():
        clear_data()
        global detales
        detales = get_detales(listbox.get("anchor"), Combo_mark.get(), parts_title)\
        
        cols = detales.columns.tolist()
        cols = cols[:3] + [cols[4]] +[cols[3]]
        
        detales = detales[cols]
        
        tv1["column"] = list(detales.columns)
        tv1["show"] = "headings"
        for column in tv1["column"]:
            tv1.heading(column, text=column)

        df_rows = detales.to_numpy().tolist()
        for row in df_rows:
            tv1.insert("", "end", values=row)
            
        return None
    
    # Semantine paieska
    def Search():
        clear_data()
        
        searching = str(search.get())
        
        
        d1 = pd.DataFrame()
        search_tokens = []
        search_tokens.append(get_tokens(searching))
        
        relevant_word = relevant_words(search_tokens[0])
        
        k = 0
        match_index = set()
        for value in detales.Detalė.values:
            for i in value.split():
                if i.lower() in search_tokens[0]:
                    match_index.add(k)
                if i.lower() in relevant_word:
                    match_index.add(k)
            k += 1

        k = 0
        for value in detales.daugiau_info.values:
            for i in value:
                if i.lower() in search_tokens[0]:
                    match_index.add(k)
                if i.lower() in relevant_word:
                    match_index.add(k)
            k += 1
            
        k = 0
        for value in detales.Info.values:
            for i in value.split():
                if i.lower() in search_tokens[0]:
                    match_index.add(k)
                if i.lower() in relevant_word:
                    match_index.add(k)
            k += 1
            
        for i in match_index:
            d1 = d1.append(detales.iloc[i])
        
        cols = d1.columns.tolist()
        cols = cols[:3] + [cols[4]] +[cols[3]]
        d1 = d1[cols]
        
        tv1["column"] = list(d1.columns)
        tv1["show"] = "headings"
        for column in tv1["column"]:
            tv1.heading(column, text=column)

        df_rows = d1.to_numpy().tolist()
        for row in df_rows:
            tv1.insert("", "end", values=row)
        return None
    
    def vidurkiai():
        pas_metai = str(metai.get())
        
        indexai = []
        metai_visi = []
        for i in detales.daugiau_info.values:
            metai_visi.append(i[9])

        for idx, m in enumerate(metai_visi):
            if m == pas_metai:
                indexai.append(idx)
        

        test_detales = pd.DataFrame()
        
        for i in indexai:
            test_detales = test_detales.append(detales.iloc[i])

        vid = []
        for i in test_detales.Kaina.values:
            i = float(i[1:])
            vid.append(i)
        
        mean = vidurkis(vid)
        mean = format(mean, '.2f')
        messagebox.showinfo("Informacija", "{year} metų šios prekės vidurkis yra: {price} eurų".format(year = pas_metai, price = mean))
        
    # Istrinti senus duomenys
    def clear_data():s
        tv1.delete(*tv1.get_children())


    root.mainloop()
    
    
