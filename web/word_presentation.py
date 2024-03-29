import random
import math

from datatypes import WordItem, WordItemPresentation, ApplicationInterface

def time():
    return (js_time() - START_TIME) / 1000

START_TIME = js_time()

def enter_leave_print(text):
    def decorate(f):
        def result(*args, **kwargs):
            print("Enter:", text)
            try:
                return f(*args, **kwargs)
            finally:
                print("Leave:", text)
        return result
    return decorate

class Timer:
    def __init__(self, duration):
        self.__start = time()
        self.__duration = duration

    def remaining_time(self):
        return self.__duration - (time() - self.__start)

def py_min(seq, key=None):
    if key is None:
        return min(seq)
    else:
        m = min([key(x) for x in seq])
        for x in seq:
            if key(x) == m:
                return x

def _calculateDecayFromActivation(x, alpha):
    """
    Referred to as "d" in the equations
    """
    c = 0.2
    return c * math.exp(x) + alpha

def calculateActivation(wordItem, time, leaveout=0):
    if len(wordItem.presentations) - leaveout <= 0:
        raise ValueError("activaton undefined for item that was not presented yet")
    else:
        return math.log(sum([(time - presentation.time)**(-presentation.decay) for presentation in wordItem.presentations[:len(wordItem.presentations) - leaveout]])) #calculate activation of second to last

def calculateNewDecay(wordItem, time, leaveout=0):
    if len(wordItem.presentations) - leaveout <= 0:
        return _calculateDecayFromActivation(0, wordItem.alpha)
    else:
        m = calculateActivation(wordItem, time, leaveout=leaveout)
        return _calculateDecayFromActivation(m, wordItem.alpha)


# TOTAL_TEST_DURATION = 57 * 60   # seconds - disabled for the online version
TEST_BLOCK_DURATION = 25 * 60  # seconds until this block is presented

ACTIVATION_PREDICTION_TIME_OFFSET = 15  # seconds
ACTIVATION_THRESHOLD_RETEST = -.8

ALPHA_ERROR_ADJUSTMENT_SUMMAND = 0.02

CORRECT_ANSWER_SCORE = 10


class AssignmentModel(object):
    __app_interface = None #: :type app_interface: ApplicationInterface
    
    def __init__(self, appInterface, stimuli):
        self.__app_interface = appInterface 

        def makeWordItem(s):
            wi = WordItem(s["word"].strip().lower())
            wi.translation = s["translation"].strip().lower()
            wi.image = s["image"].strip()
            return wi

        self.__stimuli = [makeWordItem(s) for s in stimuli]

        self.currentScore = 0

        self.__entered_word = None
        
        self.__main_time = js_time()
        self.__intermediate_session_timer = None

        self.__state = None

    def findMixedUpWord(self, typedWord):
        typedWord = typedWord.lower().strip()
        for s in self.presented_items:
            if typedWord == s.translation:
                return s
        return None

    @property
    def stimuliSummary(self):
        # This is unused atm but can be used to compile a list of 
        # the presentations etc and send this to a sever or something 
        return [{
            "word": stimulus.name,
            "translation": stimulus.translation,
            "#presentations": len(stimulus.presentations),
            "alpha": stimulus.alpha
        } for stimulus in self.__stimuli]

    @property
    def main_timer(self):
        return (js_time() - self.__main_time) / 1000

    @property
    def presented_items(self):
        return [
            x for x in self.__stimuli if len(x.presentations) > 0
        ]

    def __new_presentation(self):
        presented_items = self.presented_items
        stimulus = None
        min_activation_stimulus = None
        
        if len(presented_items) > 0:
            # Select item from presented items with activation <=
            # ACTIVATION_THRESHOLD_RETEST
            predictionTime = self.main_timer + ACTIVATION_PREDICTION_TIME_OFFSET
            activation_pairs = [
                (calculateActivation(s, predictionTime), s) 
                for s in presented_items
            ]
            minActivation, min_activation_stimulus = \
                py_min(activation_pairs, key=lambda x: x[0])
            if minActivation <= ACTIVATION_THRESHOLD_RETEST:
                stimulus = min_activation_stimulus
        if not stimulus:
            # None under that threshold? Add a new item if possible
            if len(presented_items) < len(self.__stimuli):
                stimulus = self.__stimuli[len(presented_items)]
        if not stimulus:
            stimulus = min_activation_stimulus
        if not stimulus:
            raise ValueError("Could not select any stimulus for presentation")

        new_presentation = WordItemPresentation()
        presentation_start_time = self.main_timer
        new_presentation.decay = calculateNewDecay(
            stimulus, presentation_start_time
        )
            
        self.__state = {
            "type": None,
            "answer": None,
            "item": stimulus,
            "start_time": presentation_start_time,
            "new_presentation": new_presentation,
        }
        
        if len(stimulus.presentations) == 0:
            self.__state["type"] = "learn"
            self.__app_interface.learn(
                stimulus.image, stimulus.name, stimulus.translation)
        else:
            self.__entered_word = None
            def word_entered(word):
                self.__entered_word = word 
            
            self.__state["type"] = "test"
            self.__app_interface.test(
                stimulus, entered_word_callback=word_entered)

    def __add_presentation(self, stimulus, presentation, start_time):
        presentation.time = start_time
        stimulus.presentations.append(presentation)

    @enter_leave_print("iter_run")
    def iter_run(self):
        print(self.__app_interface.done, self.__state)
        if not self.__app_interface.done:
            return
        
        if self.__state is None:
            self.__state = "instructions video"
            self.__app_interface.showInstructionVideo()
        elif self.__state == "instructions video":
            self.__state = "instructions"
            self.__app_interface.displayInstructions()
        elif self.__state in ["instructions", "recap"]:
            self.__intermediate_session_timer = Timer(TEST_BLOCK_DURATION)
            self.__new_presentation()
        elif not isinstance(self.__state, dict):
            print(f"ERROR: Invalid state: {self.__state}")
        elif self.__state.get("type") == "test":
            self.__state["type"] = "post-test"
            stimulus = self.__state["item"]
            entered_word_normalized = self.__entered_word.lower().strip()
            if entered_word_normalized.lower() == stimulus.translation.lower():
                self.currentScore += CORRECT_ANSWER_SCORE
                self.__app_interface.update_highscore(self.currentScore)
                
                self.__app_interface.displayCorrect(
                    stimulus, entered_word_normalized
                )
            else:
                stimulus.alpha += ALPHA_ERROR_ADJUSTMENT_SUMMAND
                self.__state["new_presentation"].decay = calculateNewDecay(
                    stimulus, self.__state["start_time"]
                )

                mixed_up_word = self.findMixedUpWord(entered_word_normalized)
                if mixed_up_word is not None:
                    self.__app_interface.mixedup(
                        stimulus.name,
                        stimulus.translation,
                        mixed_up_word.name,
                        mixed_up_word.translation,
                    )
                else:
                    self.__app_interface.displayWrong(stimulus, self.__entered_word)
        elif self.__state.get("type") in ["learn", "post-test"]:
            self.__add_presentation(
                self.__state["item"],
                self.__state["new_presentation"],
                self.__state["start_time"])
            if self.__intermediate_session_timer.remaining_time() <= 0:
                self.__state = "recap"
                self.__app_interface.start_recap(self.presented_items)
            else:
                self.__new_presentation()
        else:
            print("ERROR: ULTIMATE ELSE")
