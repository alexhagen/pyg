import Ipython.display

class ImageWithCaption(TextDisplayObject):
    def __init__(self, image, caption, label):
        pass
        
    def _repr_html_(self):
        return HTML(string)

    def _repr_latex_(self):
        return Latex(string)
