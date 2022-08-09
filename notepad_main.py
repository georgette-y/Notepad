from tkinter import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
from tkinter import colorchooser
from my_font_types import my_fonts
from tkinter.ttk import Combobox
from tkinter.tix import *
from datetime import date
import time

today = date.today() 
t = time.localtime()
window = Tk() 
window.title("Notepad")
window.geometry("500x400")

main_frame = Frame(window)
main_frame.pack(pady=23,fill="both",expand="True")
main_frame.pack_propagate(False)

notepad_frame = Frame(window)
notepad_frame.place(x=0,y=0)
notepad_frame.pack_propagate(False)

menu_bar = Menu(window)
window.config(menu=menu_bar)

text_scroll = Scrollbar(main_frame)
text_scroll.pack(side = RIGHT, fill=Y)

text = Text(main_frame, undo=True, selectbackground="pink", selectforeground="black", yscrollcommand=text_scroll.set,maxundo=-1)
text.pack(expand=True,fill="both")

text_scroll.config(command=text.yview)

Files = (('All Files', '*.*'),
    ('Python Files', '*.py'),
    ('Text Document', '*.txt'))

t = time.localtime()

global file_path
file_path = None 

window.iconbitmap("./resources/notebook.ico")

global selected
selected = None

num = 9
used_font = 'Segoe UI'
tip = Balloon(notepad_frame)

global editing_box
editing_box = Listbox(window,width=10,height=3)

def new():
    if messagebox.askyesno(title="Notepad", message="Would you like to save this file?"): 
        text_input = text.get("1.0", END) 
        file = asksaveasfile(filetypes = Files, defaultextension = ".txt", mode="w") 
        try:
            file.write(text_input)
            file.close()
            text.delete("1.0",END)
        except:
            ""
    else:
        text.delete("1.0",END)
    text.update() 
    
def open_file():
    file = filedialog.askopenfile(filetypes = Files, defaultextension = ".txt", mode="r")
    if file is not None:
        try:
            file_path = file.name
            file_content = file.read()
            text.delete("1.0",END)
            text.insert(END,file_content) 
        except:
            messagebox.showerror(title="Notepad", message="Please choose a different file.")

def save_file():
    global file_path
    if file_path is not None:
        with open(file_path,"w") as w_file:
            text_input = text.get("1.0", END) 
            w_file.write(text_input)
    else:
        file = asksaveasfile(filetypes = Files, defaultextension = ".txt", mode="a")
        try:
            file_path = file.name
            text_input = text.get("1.0", END)
            file.write(text_input)
            file.close()
        except:
            ""

def save_as_file():
    file = asksaveasfile(filetypes = Files, defaultextension = ".txt", mode="a")
    try:
        file_path = file.name
        text_input = text.get("1.0", END)
        file.write(text_input)
        file.close()
    except:
        ""

def cut(e):
    global selected
    if e:
        selected = window.clipboard_get()
    else:
        if text.selection_get():
            selected = text.selection_get()
            text.delete("sel.first", "sel.last")
            window.clipboard_clear()
            window.clipboard_append(selected)

def copy(e):
    global selected
    if e:
        selected = window.clipboard_get()
    if text.selection_get():
        selected = text.selection_get() 
        window.clipboard_clear()
        window.clipboard_append(selected)

def paste(e):
    global selected
    if e:
        selected = window.clipboard_get()
    else:
        if selected:
            position = text.index(INSERT)
            text.insert(position, selected)

def delete():
    if text.selection_get():
        text.delete("sel.first", "sel.last")

def select_all():
    text.tag_add("sel","1.0","end")

x = 0 
def date(nbr):
    global x
    x += 1
    dates = {1: today.strftime("%d/%m/%Y"),2:today.strftime("%B %d, %Y"),
             3: today.strftime("%m/%d/%y"),4:today.strftime("%b-%d-%Y")}
    try:
        text.edit_undo()
    except:
        ""
    if x != 4:
        text.insert(END,dates[x])
    else:
        text.insert(END,dates[x])
        x = 0

file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save as", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

edit_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo        Ctrl+Z", command=text.edit_undo)
edit_menu.add_command(label="Redo         Shift+Ctrl+Z", command=text.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut            Ctrl+X", command=lambda: cut(False))
edit_menu.add_command(label="Copy         Ctrl+C", command=lambda: copy(False))
edit_menu.add_command(label="Paste         Ctrl+V", command=lambda: paste(False))
edit_menu.add_command(label="Delete        Del", command=delete)
edit_menu.add_command(label="Select All   Ctrl+A", command=select_all)

window.bind("<Control-x>",cut)
window.bind("<Control-c>",copy)
window.bind("<Control-v>",paste)

count = 0 
count2 = 0
count3 = 0

def change_colors():
    global count
    color = colorchooser.askcolor()
    if text.tag_ranges('sel'):
        text.tag_add('colortag_' + str(count), SEL_FIRST,SEL_LAST)
        text.tag_configure('colortag_' + str(count), foreground=color[1])
        count += 1
    else:
        for tag in text.tag_names():
            text.tag_remove(tag, "1.0", "end")
        try:
            text.config(foreground=color[1])
        except:
            ""

color_button = Button(notepad_frame,text="  Color  ",font=("Verdana",8),command=change_colors)
color_button.grid(row=0,column=0,padx=1)

tip.bind_widget(color_button,balloonmsg="Change the text's foreground color.")

font_label = Label(notepad_frame,text="   Font  ")
font_label.grid(row=0,column=2,padx=1)

tip.bind_widget(font_label,balloonmsg="Change the font style and size")

combo_box = AutocompleteCombobox(
    notepad_frame, 
    completevalues=my_fonts,
    )

combo_box.grid(row=0,column=3,padx=1)

my_sizes = list(range(0,101))

my_scnd_combo = Combobox(
    notepad_frame,
    width=3
    )

my_scnd_combo["values"]=my_sizes
my_scnd_combo.grid(row=0,column=4,padx=1)

def selected_item(event):
    global used_font,count2
    if combo_box.get() != "":
        if text.tag_ranges('sel'):
            try:
                text.tag_add('font_tag' + str(count2),SEL_FIRST,SEL_LAST)
                text.tag_configure('font_tag' + str(count2),font=(combo_box.get(),int(num)))
                used_font = combo_box.get()
                count2 += 1
            except:
                ""
        else:
            for tag in text.tag_names():
                text.tag_remove(tag, "1.0", "end")
            try:
                text.configure(font=(combo_box.get(),int(num)))
                used_font = combo_box.get()
            except:
                ""

def selected_num(event):
    global num,count3
    if my_scnd_combo.get() != "":
        if text.tag_ranges('sel'):
            try:
                text.tag_add('size_tag' + str(count3),SEL_FIRST,SEL_LAST)
                text.tag_configure('size_tag' + str(count3),font=(used_font,my_scnd_combo.get()))
                num = my_scnd_combo.get()
                count3 += 1
            except:
                ""
        else:
            for tag in text.tag_names():
                text.tag_remove(tag, "1.0", "end")
            try:
                text.configure(font=(used_font,my_scnd_combo.get()))
                num = my_scnd_combo.get()
            except:
                ""

def search_for_me(event):
    start_pos = "1.0"
    for tag in text.tag_names():
        text.tag_remove(tag, "1.0", "end")
    countVar = StringVar()
    while start_pos != "end":
        pos = text.search(search_entry.get(), start_pos, stopindex="end", count=countVar)
        start_pos =  "%s + %sc" % (pos, int(countVar.get())+1)
        text.tag_configure("search", background="yellow")
        text.tag_add("search", pos, "%s + %sc" % (pos, countVar.get()))

date_button = Button(notepad_frame,text="  date  ",font=("Verdana",8),command=lambda: date(x))
date_button.grid(row=0,column=1,padx=1)

search_label = Label(notepad_frame,text="Search")
search_label.grid(row=0,column=5,padx=1)

search_entry = Entry(notepad_frame)
search_entry.grid(row=0,column=6,padx=1)

search_entry.bind("<Return>",search_for_me)
combo_box.bind("<<ComboboxSelected>>",selected_item)
my_scnd_combo.bind("<<ComboboxSelected>>",selected_num)

window.mainloop() 
