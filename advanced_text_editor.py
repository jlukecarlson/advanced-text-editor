from Tkinter import *
import tkFileDialog
import os, sys, inspect

main_path= os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
dependencies_path = os.path.join(main_path, 'dependencies')
sys.path.append(dependencies_path)
from tkhtml import *
from tkutil import unbind_destroy

class Window():
    def __init__(self, parent):
        self.filename =''
        self.window = Toplevel(parent)
        self.text_box = Text(self.window, background="black", foreground="firebrick", insertbackground="white")
        self.text_box.pack(expand = 1, fill= BOTH)
        self.text_box.focus_set()
       
class Editor:
    def __init__(self, master):
        self.file_name = ""
        self.html_window=""
        #self.html_viewer=""
        
        initial_text_box = Text(root, background="black", foreground="firebrick", insertbackground="white")
        initial_text_box.pack(expand = 1, fill= BOTH)
        initial_text_box.focus_set()
        initial_text_box.insert(END, """This is a text editor made by Luke Carlson (github.com/jLukeC).""")

        self.file_opt = options = {}

        # options for opening files
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('markdown', '.md'), ('html', '.html')]
        options['initialdir'] = os.path
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'


        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = os.path
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        
        


        def find_focus():
           focus= root.focus_get()
           print focus
           print focus.get(1.0, END)
           print focus.master
           focus.master.wm_title("focused")
           

        menubar = Menu(root)
        menubar.add_command(label="Hello!", command=find_focus)
        menubar.add_command(label="fds!", command=find_focus)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_window, accelerator="Command+N")
        filemenu.add_command(label="Open", command=self.open_file, accelerator="Command+O")
        filemenu.add_command(label="Save", command=self.save_file, accelerator="Command+S")
        filemenu.add_command(label="Save as...", command=self.save_as_file)
        filemenu.add_separator()
        filemenu.add_command(label="Close Window", command=self.destroy, accelerator="Command+W")
        filemenu.add_command(label="Exit", command=self.quit_project, accelerator="Command+Q")
        menubar.add_cascade(label="File", menu=filemenu)

                             
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=find_focus)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.cut, accelerator="Command+X")
        editmenu.add_command(label="Copy", command=self.copy, accelerator="Command+C")
        editmenu.add_command(label="Paste", command=self.paste, accelerator="Command+V")
        editmenu.add_command(label="Select All", command=self.select_all, accelerator="Command+A")
        editmenu.add_command(label="Delete", command=self.delete_selection)
        menubar.add_cascade(label="Edit", menu=editmenu)

                             
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Find Focus", command=find_focus)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)


        root.bind_all("<Command-m>", self.view_html)

        root.bind_all("<Command-n>", self.new_window)
        root.bind_all("<Command-o>", self.open_file)
        root.bind_all("<Command-s>", self.save_file)
        root.bind_all("<Command-Shift-s>", self.save_as_file) #doesnt work
        root.bind_all("<Command-a>", self.select_all)
        root.bind_all("<Command-w>", self.destroy)
        root.bind_all("<Command-q>", self.quit_project)

    def view_html(self, event=''):
        focus=root.focus_get()
        file_extension = os.path.splitext(focus.master.title())[1]
        print file_extension
        if (file_extension == ".md"): #checks if it is markdown
            print "this is markdown"
        else:
            if self.html_window == '':
                self.html_window=Toplevel(root)
                self.html_window.wm_title("HTML Viewer")
                self.html_viewer=tkHTMLViewer(self.html_window)
                try:
                    self.html_viewer.display(focus.master.title())
                except:
                    print "html section couldnt work"
            else:
                try:
                    self.html_viewer.display(focus.master.title())
                except:
                    print "html section couldnt work"
  
        
    def open_file(self, event=''):
        open_file = tkFileDialog.askopenfile(mode='r', **self.file_opt)
        window_app = Window(root)
        window_app.text_box.delete(1.0, END)
        window_app.text_box.insert(END, open_file.read())
        window_app.file_name = open_file.name
        window_app.window.wm_title(window_app.file_name)
        print window_app.file_name

    def save_file(self, event=''):
        focus=root.focus_get()
        if (focus.master.title() == '' or focus.master.title() == "Luke's Text Editor"):
            self.save_as_file()
        else:
             save_file = open(focus.master.wm_title(), 'w')
             save_file.write(focus.get(1.0, END))
    
    def save_as_file(self, event=''):
        focus=root.focus_get()
        save_file = tkFileDialog.asksaveasfile(mode='w', **self.file_opt)
        save_file.write(focus.get(1.0, END))
        focus.master.wm_title(save_file.name)
        print focus.master.title()

    def copy(self):
        focus=root.focus_get()
        root.clipboard_clear()
        root.clipboard_append(focus.selection_get())

    def cut(self):
        self.copy()
        self.delete_selection()

    def paste(self):
        focus=root.focus_get()
        result = root.selection_get(selection = "CLIPBOARD")
        focus.insert(INSERT, result)

    def delete_selection(self):
        focus=root.focus_get()
        focus.delete(SEL_FIRST, SEL_LAST)
        
    def select_all(self, event=''):
        focus=root.focus_get()
        focus.tag_add("sel","1.0","end")
        
    def new_window(self, event=''):
        self.window_app = Window(root)

    def about(self):
        about_window = Toplevel(root)
        about_window.wm_title("About")
        info = Label(about_window, text="""This is a text editor made by Luke Carlson (github.com/jLukeC) over a few days in summer 2013.""")
        info.pack()
        
    def destroy(self, event=''):
        focus=root.focus_get()
        focus_parent_string=focus.winfo_parent()
        focus_parent = root.nametowidget(focus_parent_string)
        unbind_destroy(focus_parent)
        focus_parent.wm_withdraw()
        try:
            focus_parent.wm_withdraw()
        except: pass
        try:
            focus_parent.destroy()
        except: pass

    def quit_project(self):
        sys.exit()
        
if __name__=='__main__':
    root = Tk()
    root.wm_title("Luke's Text Editor")
    app = Editor(root)
    root.mainloop()

# great colors list http://wiki.tcl.tk/16166
# thank you http://www.pysol.org/ for the html viewer code (and the destroy code)
