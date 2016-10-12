import tkFileDialog

def file_save():
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")

print file_save()
