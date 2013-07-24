advanced-text-editor
====================

a text editor made in python. Can handle multiple windows and the major mac shortcuts.
It is the advanced version of [my other editors](https://github.com/jLukeC/mega-project-list/blob/master/python/text-editor/basic_text_editor.py)


Hardest parts
--------------
**Allowing multiple windows** took a while especially since file commands did not work if I had trouble... (look below)

**Determining text widget in focus** without this, multiple windows couldn't work nor file commands. The solution ended up being trivial but it took a while to reach, especially since root.focus_get() returns a decimal number when printed out

**Generally Keeping the Code Clean** still a struggle but as I learn more about Tkinter I have made sure to make my code my straightforward and less of a mess


PS this readme was written using my editor
