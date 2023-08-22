from PyQt5.QtWidgets import QColorDialog, QWidget

#~colorpicker|just opens a QColorPicker. simple as that! :)|v1.0
# 11 lines of code... amazing :P

class colorpicker(QWidget):
    def __init__(self):
        super(colorpicker, self).__init__()
        QColorDialog.getColor()

window = colorpicker()