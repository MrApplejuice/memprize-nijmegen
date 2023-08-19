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

class ApplicationInterface:
    def learn(self, image, word, translation):
        raise NotImplementedError()

    def test(self, word, answerToDisplay, imageAnswer):
        raise NotImplementedError()

    def displayCorrect(self, typedWord, correctAnswer):
        raise NotImplementedError()

    def displayWrong(self, typedWord, correctAnswer, image):
        raise NotImplementedError()

    def mixedup(self, leftUpper, leftLower, rightUpper, rightLower):
        raise NotImplementedError()

    def update_highscore(self, score):
        raise NotImplementedError()

    def displayInstructions(self):
        raise NotImplementedError()

    def start_recap(self, word_items):
        raise NotImplementedError()
    
    # `done` should be a property, but transcrypt cannot override a prop in
    # the subclass.
    done = False
