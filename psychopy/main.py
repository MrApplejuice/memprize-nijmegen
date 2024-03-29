#!/usr/bin/python

import sys
import os
import signal
from datetime import datetime

from visual import MovieVisualizer
from word_presentation import *
import editing

from dict_csv_serializer import CSVDictList

import psychopy.core as core
import psychopy.visual as visual
import psychopy.gui as gui
from psychopy.colors import Color

PROBED_WIDTH_FACTOR = None

def determineTextWidth(fontStimulus):
  global PROBED_WIDTH_FACTOR

  if PROBED_WIDTH_FACTOR is None:
    from psychopy.tools.monitorunittools import posToPix

    probe = visual.TextStim(fontStimulus.win, height=0.1, pos=(0, 0), alignHoriz='left')
    probe.text = ""
    print("Probing")
    probe.pos = (0, 0)
    x0 = posToPix(probe)[0]
    probe.pos = (1, 0)
    x1 = posToPix(probe)[0]
    PROBED_WIDTH_FACTOR = x1 - x0

  # Determine text width using psychopy's pyglet infrastructure
  return fontStimulus.boundingBox[0] / PROBED_WIDTH_FACTOR

def setLineStrikethrough(textStim, lineStim):
  lineStim.start = (textStim.pos[0], textStim.pos[1] - 0.01)
  lineStim.end = (textStim.pos[0] + determineTextWidth(textStim), textStim.pos[1] - 0.01)

IMAGES_SIZE = 1.3
IMAGES_LOCATION = (0, 1 - (IMAGES_SIZE / 2 + 0.05))
def load_all_images(win, imagePathList):
  result = {}
  for path in imagePathList:
    if path not in result:
      if not os.path.exists(path):
        raise ValueError("Image {} does not exist".format(path))
      imageStim = visual.ImageStim(win, pos=IMAGES_LOCATION)
      imageStim.image = path
      imageStim.size *= IMAGES_SIZE / imageStim.size[1]
      result[path] = imageStim
  return result

# Animation related functions
animationWindow = None
animationFunctions = []
def stepAnimations():
  for f in animationFunctions:
    f()
  
def recordKeyboardInputs(*args, **argv):
  return editing.recordKeyboardInputs(*args, idleFunction=stepAnimations, **argv)

def animatedWait(delay):
  STEP_RESOLUTION=0.01
  timer = core.CountdownTimer(delay)
  while timer.getTime() > 0:
    stepAnimations()
    if animationWindow is not None:
      animationWindow.flip()
    if timer.getTime() > STEP_RESOLUTION:
      core.wait(STEP_RESOLUTION)


class MovieViewer(object):
  def __init__(self, win):
    self.__win = win
    self.__visualizer = None
    
  def playMovie(self, filename):
    if self.__visualizer is None:
      self.__visualizer = MovieVisualizer(self.__win, filename, (0, 0), 1.0)
    self.__visualizer.restart(filename)
    
    while self.__visualizer.stillRunning:
      self.__visualizer.draw()
      self.__win.flip()

class LearnWordViewer(object):
  UPPER_TEXT_POS = (-0.25, -0.56)
  LOWER_TEXT_POS = (-0.25, -0.76)

  IMAGE_SIZE = 1.3

  def __init__(self, win, loadedImages):
    self.__win = win
    
    self.__loadedImages = loadedImages
    
    self.imageComponent = None
    self.wordText = visual.TextStim(win, height=0.1, pos=self.UPPER_TEXT_POS, alignHoriz='left')
    self.translationText = visual.TextStim(win, height=0.1, pos=self.LOWER_TEXT_POS, alignHoriz='left')
    self.instructionText = visual.TextStim(win, height=0.07, pos=(-.8, -0.56), alignHoriz='left', wrapWidth = 0.3 )
    self.instructionText.text = "Vorm een beeld bij het woord en druk Enter!" 
    
  def _prepareImage(self, image):
    self.imageComponent = self.__loadedImages[image]
    
  def show(self, image, word, translation):
    WAIT_TIMES = [15.0, 15.0] # maximum presentation times before program automatically continues, , PP can move on self-paced earlier
    ANIMATION_TIME = 0.01
    
    TEXT_HEIGHT = 0.1

    self._prepareImage(image)    
    
    self.wordText.text = word
    self.translationText.text = translation
    self.instructionText.autoDraw = True 
    
    self.imageComponent.autoDraw = True
    self.wordText.autoDraw = True
    
    # Animate text popup
    currentHeight = 0.0
    startTime = core.getTime()
    now = core.getTime()
    while now - startTime < ANIMATION_TIME:
      currentHeight = TEXT_HEIGHT * (now - startTime) / ANIMATION_TIME;
      self.wordText.height = currentHeight
      self.__win.flip()
      now = core.getTime()

    self.wordText.height = TEXT_HEIGHT
    self.__win.flip()
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(WAIT_TIMES[0] - ANIMATION_TIME))
    
    self.translationText.autoDraw = True
    
    currentHeight = 0.0
    startTime = core.getTime()
    now = core.getTime()
    while now - startTime < ANIMATION_TIME:
      currentHeight = TEXT_HEIGHT * (now - startTime) / ANIMATION_TIME;
      self.translationText.height = currentHeight
      self.__win.flip()
      now = core.getTime()

    self.translationText.height = TEXT_HEIGHT
    self.__win.flip()
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(WAIT_TIMES[1] - ANIMATION_TIME))

    self.wordText.autoDraw = False
    self.translationText.autoDraw = False
    self.imageComponent.autoDraw = False
    self.instructionText.autoDraw =False 
    
class TestWordViewer(LearnWordViewer):
  UPPER_TEXT_POS = LearnWordViewer.UPPER_TEXT_POS
  LOWER_TEXT_POS = LearnWordViewer.LOWER_TEXT_POS

  ANIMATION_TIME = 0.01
  TEXT_HEIGHT = 0.1

  def __init__(self, win, loadedImages):
    super(TestWordViewer, self).__init__(win, loadedImages)
    
    self.__win = win
    
    self.wordText = visual.TextStim(win, pos=self.UPPER_TEXT_POS, alignHoriz='left')
    self.typedText = visual.TextStim(win, pos=self.LOWER_TEXT_POS, alignHoriz='left')
    self.correctAnswer = visual.TextStim(win, pos=self.LOWER_TEXT_POS, alignHoriz='left', color=Color((0, 1, 0), "rgb1"))
    self.strikeThroughLine = visual.Line(win, lineColor=(255, 0, 0), lineColorSpace="rgb255", opacity=1, lineWidth=5)
    
  def test(self, word):
    self.typedText.color = Color((1, 1, 1), "rgb1")

    self.wordText.text = word 
    self.wordText.autoDraw = True
    
    # Animate text popup
    currentHeight = 0.0
    startTime = core.getTime()
    now = core.getTime()
    while now - startTime < self.ANIMATION_TIME:
      currentHeight = self.TEXT_HEIGHT * (now - startTime) / self.ANIMATION_TIME
      self.wordText.height = currentHeight
      self.__win.flip()
      now = core.getTime()

    self.wordText.height = self.TEXT_HEIGHT
    self.__win.flip()
    
    self.typedText.height = self.TEXT_HEIGHT
    self.typedText.autoDraw = True
    
    typedWord = None
    initCountdown = core.CountdownTimer(1)
    while (not typedWord) and (initCountdown.getTime() > 0):
      history = recordKeyboardInputs(self.__win, self.typedText, shadowText="...?")
      typedWord = None if len(history) == 0 else history[-1]["current_text"].strip()

    self.wordText.autoDraw = False
    self.typedText.autoDraw = False

    return typedWord
    
  def showCorrect(self):
    self.wordText.autoDraw = True
    self.typedText.autoDraw = True
    
    self.typedText.color = Color((0, 1, 0), "rgb1")
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(0.3))

    self.wordText.autoDraw = False
    self.typedText.autoDraw = False

  def showStrikthroughLine(self):
    self.typedText.color = Color((1, 0, 0), "rgb1")

    self.typedText.draw()
    setLineStrikethrough(self.typedText, self.strikeThroughLine)
    self.strikeThroughLine.autoDraw = True

  def showWrong(self, answerToDisplay, image):
    self.wordText.autoDraw = True
    self.typedText.autoDraw = True
    
    self._prepareImage(image)

    if not self.typedText.text:
      self.typedText.text = "x"
    
    self.showStrikthroughLine()

    self.correctAnswer.text = answerToDisplay 
    self.correctAnswer.pos = (self.strikeThroughLine.end[0] + 0.02, self.typedText.pos[1])
    
    self.correctAnswer.autoDraw = True
    self.imageComponent.autoDraw = True
    
    currentHeight = 0.0
    startTime = core.getTime()
    now = core.getTime()
    while now - startTime < self.ANIMATION_TIME:
      currentHeight = self.TEXT_HEIGHT * (now - startTime) / self.ANIMATION_TIME
      self.correctAnswer.height = currentHeight
      self.__win.flip()
      now = core.getTime()
    self.correctAnswer.height = self.TEXT_HEIGHT
    self.__win.flip()
    animatedWait(1 - self.ANIMATION_TIME)
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(10))

    self.imageComponent.autoDraw = False
    self.correctAnswer.autoDraw = False
    self.strikeThroughLine.autoDraw = False
    self.wordText.autoDraw = False
    self.typedText.autoDraw = False

class MixedUpViewer(object):
  UPPER_TEXT_POSITIONS = [LearnWordViewer.UPPER_TEXT_POS, (-LearnWordViewer.UPPER_TEXT_POS[0], LearnWordViewer.UPPER_TEXT_POS[1])]
  LOWER_TEXT_POSITIONS = [LearnWordViewer.LOWER_TEXT_POS, (-LearnWordViewer.LOWER_TEXT_POS[0], LearnWordViewer.LOWER_TEXT_POS[1])]

  TEXT_HEIGHT = 0.1

  def __init__(self, win, testScreen):
    self.__win = win
    
    self.mixedUpText = visual.TextStim(win, pos=(self.UPPER_TEXT_POSITIONS[0][0], 0), alignHoriz='left', text="Je hebt twee woorden door elkaar gehaald:", height=self.TEXT_HEIGHT)
    self.upperTexts = [testScreen.wordText,  visual.TextStim(win, pos=self.UPPER_TEXT_POSITIONS[1], alignHoriz='left')]
    self.lowerTexts = [testScreen.typedText, visual.TextStim(win, pos=self.LOWER_TEXT_POSITIONS[1], alignHoriz='left')]
    self.strikeThroughLine = testScreen.strikeThroughLine
    
    self.showStrikethroughLine = testScreen.showStrikthroughLine
    
  def show(self, leftUpper, leftLower, rightUpper, rightLower):
    TEXT_HEIGHT = self.TEXT_HEIGHT
    
    ANIMATION_TIME = 0.2
    FORCED_WAIT = 1
    TOTAL_WAIT = 10
    
    self.upperTexts[0].autoDraw = True
    self.lowerTexts[0].autoDraw = True
    self.showStrikethroughLine()
    self.mixedUpText.autoDraw = True
    self.__win.flip()
    animatedWait(1)

    self.upperTexts[0].text = leftUpper
    self.upperTexts[1].text = rightUpper
    self.lowerTexts[0].text = leftLower
    self.lowerTexts[1].text = rightLower

    for t in self.upperTexts + self.lowerTexts:
      t.color = Color((1, 1, 1), "rgb1")
      t.autoDraw = True
    self.strikeThroughLine.autoDraw = False
      
    currentHeight = 0.0
    startTime = core.getTime()
    now = core.getTime()
    while now - startTime < ANIMATION_TIME:
      currentHeight = TEXT_HEIGHT * (now - startTime) / ANIMATION_TIME;
      for t in self.upperTexts + self.lowerTexts:
        if t != self.upperTexts[0]: # Do not animate upper left word
          t.height = currentHeight
      self.__win.flip()
      now = core.getTime()
    for t in self.upperTexts + self.lowerTexts:
      t.height = TEXT_HEIGHT
    self.__win.flip()
    
    animatedWait(FORCED_WAIT - ANIMATION_TIME)
    
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(TOTAL_WAIT - FORCED_WAIT))

    for t in self.upperTexts + self.lowerTexts:
      t.autoDraw = False
    self.mixedUpText.autoDraw = False


def calculateParabolaFunction(p1, p2, p3):
  alpha = (p1[1] - p2[1]) / (p2[1] - p3[1])
  c = (alpha * (p2[0]**2 - p3[0]**2) + p2[0]**2 - p1[0]**2) / (2 * (p2[0] + alpha * p2[0] - p1[0] - alpha * p3[0]))
  b = (p1[1] - p2[1]) / ((p1[0] - c)**2 - (p2[0] - c)**2)
  a = p1[1] - b * (p1[0] - c)**2
  
  def parabola(x):
    return a + b * (x - c)**2
  return parabola

class HighscoreViewer(object):
  HIGHSCORE_TEXT_POS = (.6, -0.9)
  
  ANIMATION_CONTROL_POINTS = (tuple(TestWordViewer.LOWER_TEXT_POS),
                              ((TestWordViewer.LOWER_TEXT_POS[0] + HIGHSCORE_TEXT_POS[0]) / 2, 0), 
                              (HIGHSCORE_TEXT_POS[0] + 0.1, HIGHSCORE_TEXT_POS[1]))
  ANIMATION_DURATION = 0.3

  # Parameters a, b, c defining the parabola  a + b * (x - c)^2
  __ANIMATION_PATH_PARABOLA = (calculateParabolaFunction(*ANIMATION_CONTROL_POINTS),)
  
  @property
  def ANIMATION_PATH_PARABOLA(self):
    """ small property to unpack packed parabola function """
    return self.__ANIMATION_PATH_PARABOLA[0]

  def __init__(self, win):
    global animationFunctions
    
    self.__win = win
    
    self.__score = 0
    self.highscoreText = visual.TextStim(win, pos=self.HIGHSCORE_TEXT_POS, alignHoriz='left', height=0.07)
    self.updateHighscore(self.__score)
    self.highscoreText.autoDraw = True
    
    self.animationTextStim = visual.TextStim(win, pos=(0.0, 0.0), color=Color((0, 1, 0), "rgb1"), alignHoriz='center', height=0.14)
    self.animationStartTime = None
    self.animationText = ""
    
    animationFunctions.append(self.__updateAnimation)
    
  def updateHighscore(self, score):
    if score - self.__score > 0:
      self.animate("+{}".format(score - self.__score))
    self.__score = score
    self.highscoreText.text = "Jouw score: {}".format(score)
    
  def animate(self, scoreText):
    self.animationStartTime = core.getTime()
    self.animationText = scoreText
    
  def __updateAnimation(self):
    if self.animationStartTime is not None:
      timeOffset = core.getTime() - self.animationStartTime
      if timeOffset > self.ANIMATION_DURATION:
        self.animationTextStim.autoDraw = False
        self.animationStartTime = None
      else:
        self.animationTextStim.autoDraw = False # Hack to guarantee that this stimulus is one of the last drawn...
        self.animationTextStim.autoDraw = True
        self.animationTextStim.text = self.animationText
        
        x = self.ANIMATION_CONTROL_POINTS[0][0] + timeOffset / self.ANIMATION_DURATION * (self.ANIMATION_CONTROL_POINTS[2][0] - self.ANIMATION_CONTROL_POINTS[0][0])
        y = self.ANIMATION_PATH_PARABOLA(x)
        
        self.animationTextStim.pos = (x, y)

class InstructionsViewer(object):
  def __init__(self, win, texts):
    self.__win = win
    
    self.__texts = texts
    
    self.textStim = visual.TextStim(win, pos=(-.5, 0), wrapWidth=1, alignHoriz='left', height=0.1)
  
  def show(self):
    self.textStim.autoDraw = True
    for text in self.__texts:
      self.textStim.text = text
      recordKeyboardInputs(self.__win, None)
    self.textStim.autoDraw = False
    
    
class InbetweenSessionViewer(object):
  def __init__(self, win, loadedImages):
    self.__win = win
    self.__loadedImages = loadedImages
    
    self.instructionText = visual.TextStim(win, pos=(-.5, 0), wrapWidth=1, alignHoriz='left', height=0.1)
    self.instructionText.text = """
Je hebt al veel woorden geleerd. Laten we eens kijken hoe goed je de woorden onthouden hebt! 
[Enter]
    """.strip()
    
    self.instructionText2 = visual.TextStim(win, pos=(-.5, 0), wrapWidth=1, alignHoriz='left', height=0.1)
    self.instructionText2.text = """
Ga eerst in gedachten de kamers af waarin je je de woorden voorgesteld hebt. Weet je nog welke kamers je gezien hebt?
[Enter]
    """.strip()

    self.endText = visual.TextStim(win, pos=(-.5, 0), wrapWidth=1, alignHoriz='left', height=0.1)
    self.endText.text = """
Goed! Nu ga je weer verder oefenen! [Enter]
    """.strip()

    self.wordsText = visual.TextStim(win, pos=(0, -0.66), wrapWidth=1, alignHoriz='center', height=0.075)
  
  def showImagesAndWords(self, imageWordsPairs):
    IMAGE_WAIT = 15
    IMAGE_FORCED_WAIT = 0
    
    WORDS_AND_IMAGE_WAIT = 15
    WORDS_AND_IMAGE_FORCED_WAIT = 1
    
    self.instructionText.autoDraw = True
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(10))
    self.instructionText.autoDraw = False
    
    self.instructionText2.autoDraw = True
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(10))
    self.instructionText2.autoDraw = False
    
    for image, wordTranslationDataPairs in imageWordsPairs:
      imageStim = self.__loadedImages[image]
      
      imageStim.autoDraw = True

      self.__win.flip()
      
      self.wordsText.text = "Denk nu aan alle woorden die je je in deze kamer voorgesteld hebt. Druk dan op [Enter]!"
      self.wordsText.autoDraw = True
      animatedWait(IMAGE_FORCED_WAIT)
      recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(IMAGE_WAIT - IMAGE_FORCED_WAIT))
      
      self.wordsText.text = "Dit zijn de woorden:\n" + "   ".join(["=".join((w, t)) for w, t in wordTranslationDataPairs])
      
      self.__win.flip()
      animatedWait(WORDS_AND_IMAGE_FORCED_WAIT)
      recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(WORDS_AND_IMAGE_WAIT - WORDS_AND_IMAGE_FORCED_WAIT))

      imageStim.autoDraw = False
      self.wordsText.autoDraw = False
    
    self.endText.autoDraw = True
    recordKeyboardInputs(self.__win, None, countdown=core.CountdownTimer(5))
    self.endText.autoDraw = False

def showParticipantDataDialog():
  dlg = gui.Dlg(title="Participant data")
  dlg.addField("ID")
  dlg.addField("Age")
  dlg.addField("Gender", choices=["male", "female"])
  dlg.show()
  
  if not dlg.OK:
    return None
  else:
    return dict(list(zip(("participant_id", "participant_age", "participant_gender"), dlg.data)))

if __name__ == '__main__':
  if ("?" in sys.argv[1:]) or ("help" in sys.argv[1:]):
    print("""
Usage:
  python main [windowed]
  
Parameter:
  fullscreen    Specify the parameter "fullscreen" to start the application in fullscreen mode
""")
  else:
    fullscreenMode = "fullscreen" in sys.argv[1:]
    
    print(("Starting in", "fullscreen" if fullscreenMode else "window", "mode"))
    
    participantInfo = showParticipantDataDialog()
    if participantInfo is None:
      sys.exit(0)

    mainWindow = visual.Window(fullscr=fullscreenMode, size=(1280, 720))
    animationWindow = mainWindow
    if mainWindow.winType != "pyglet":
      raise ValueError("Cannot only determine font widths for non-pyglet fonts")
    print(("Main window uses backend: ", mainWindow.winType))

    # Load stimuli
    stimuli = CSVDictList()
    stimuli.load("resources/stimuli.csv")

    instructionTexts = CSVDictList()
    instructionTexts.load("resources/instructions.csv")
    
    allImages = load_all_images(mainWindow, [x["image"] for x in stimuli])

    # Initialize different "scenes"
    movieViewer = MovieViewer(mainWindow)
    instructionsViewer = InstructionsViewer(mainWindow, [x["text"] for x in instructionTexts])
    learnWordViewer = LearnWordViewer(mainWindow, allImages)
    testWordViewer = TestWordViewer(mainWindow, allImages)
    highscoreHighscoreViewer = HighscoreViewer(mainWindow)
    mixedupViewer = MixedUpViewer(mainWindow, testWordViewer)
    inbetweenSessionViewer = InbetweenSessionViewer(mainWindow, allImages)
    finalScreenViewer = InstructionsViewer(mainWindow, ["""Je bent klaar met het experiment. Bedankt en tot volgende week!"""])
    
    #movieViewer.playMovie("/media/crepo/TEMP/Mnemonic_task/stimuli/MemrisePrizev3.wmv")
    
    class ThisAppInterface(ApplicationInterface):
      def learn(self, *args):
        learnWordViewer.show(*args)
      def test(self, *args):
        return testWordViewer.test(*args)
      def updateHighscore(self, *args):
        highscoreHighscoreViewer.updateHighscore(*args)
      def mixedup(self, *args):
        mixedupViewer.show(*args)
      def displayCorrect(self, typedWord, correctWord):
        testWordViewer.showCorrect()
      def displayWrong(self, typedWord, correctWord, image):
        testWordViewer.showWrong(correctWord, image)
      def displayInstructions(self):
        instructionsViewer.show()
      def startInbetweenSession(self, imageWordPairs):
        inbetweenSessionViewer.showImagesAndWords(imageWordPairs)
    
    assignmentModel = AssignmentModel(ThisAppInterface(), stimuli)

    def saveData():
      targetFilename = "learn-data-summary.csv"
      nowString = datetime.now().isoformat()
      
      learnDataList = CSVDictList()
      if os.path.exists(targetFilename):
        learnDataList.load(targetFilename)
      
      for d in assignmentModel.stimuliSummary:
        d["time"] = nowString
        d = dict(list(participantInfo.items()) + list(d.items()))
        learnDataList.append(d)
      
      learnDataList.save(targetFilename)

    def handleTermination(signal, frame):
      print("Saving session data before termination")
      saveData()
      sys.exit(1)
      
    signal.signal(signal.SIGINT, handleTermination)
    assignmentModel.run()
    
    saveData()
    finalScreenViewer.show()