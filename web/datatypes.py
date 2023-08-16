class WordItemPresentation:
    def __init__(self, time=0, decay=0):
        self.decay = decay
        self.time = time
    
    def to_string(self):
        return "(Presentation: decay={d} time={t})".format(d=self.decay, t=self.time)

class WordItem:
    def __init__(self, name):
        self.name = name
        self.translation = ""
        self.alpha = .25
        self.presentations = []
        self.image = None
