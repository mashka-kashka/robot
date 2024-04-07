from PyQt6 import QtGui

class RoboLog:
    def __init__(self, edit, out=None, color=None):
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        #self.edit.moveCursor(QtGui.QTextCursor.en)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)