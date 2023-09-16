import re

import translations

from datatypes import ApplicationInterface

LEARNED_WORD_POS = [200, 500]
TRANSLATED_WORD_POS = [200, 550]

def pixipt(x, y):
    return do_new(PIXI.Point, x, y)

def split_block_strings(blocks):
    return [
        t.strip() for t in 
        re.split("-{5,}", blocks)
    ]

class TranslatableMixin:
    LANG_STRINGS = translations.Default

class Confirmable:
    _confirmable_initialized = False
    
    def __init__(self):
        if self._confirmable_initialized:
            return
        self._confirmable_initialized = True
        
        self._Confirmable__call = None
        window.addEventListener("keydown", self._confirmable__button_pressed)
        
        jQuery(self.pixi.view).on("click touchstart", self._confirmable__clicked)
        
        self._confirm__timeout = None
    
    def _confirmable_confim(self):
        if self._confirm__timeout is not None:
            window.clearTimeout(self._confirm__timeout)
            self._confirm__timeout = None
        if self._Confirmable__call is not None:
            call = self._Confirmable__call
            self._Confirmable__call = None
            call()
        
    def _confirmable__clicked(self, event):
        self._confirmable_confim()
    
    def _confirmable__button_pressed(self, event):
        if event.key == "Enter":
            self._confirmable_confim()

    def confirm(self, call):
        self._Confirmable__call = call
        
    def timed_confirm(self, call, timeout=None):
        self.confirm(call)
        if timeout is not None:
            self._confirm__timeout = window.setTimeout(
                lambda *_: self._confirmable_confim(),
                1000 * timeout)

class InstructionVideoMixin(Confirmable):
    def __init__(self):
        super().__init__()

        self._instvid__video_sprite = None
        self._instvid__video = None

        g = self._instvid__play_container = do_new(PIXI.Graphics)
        g.beginFill(0x101010).drawRoundedRect(0, 0, 400, 200, 20)
        g.anchor = pixipt(0.5, 0.5)
        g.position = pixipt(200, 200)

        g = arrow = do_new(PIXI.Graphics)

        g.beginFill(0xffffff, 0.8).moveTo(0, 0).lineTo(50, 50).lineTo(0, 100).lineTo(0, 0).lineTo(50, 50)
        g.setTransform(200 - 25, 100)
        g.scale = pixipt(1, 0.6)

        self._instvid__play_container.addChild(arrow)
        
        start_text = do_new(
            PIXI.Text,
            "Start instructions video",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
            }
        )
        start_text.position = pixipt(200, 30)
        start_text.anchor = pixipt(0.5, 0)
        self._instvid__play_container.addChild(start_text)

        self._instvid__play_container.interactive = True
        self._instvid__play_container.cursor = 'pointer'
        self._instvid__play_container.on("pointertap", self._instvid__start_clicked)

        g = self._instvid__skip_container = do_new(PIXI.Graphics)
        g.beginFill(0x101010).drawRoundedRect(0, 0, 150, 40, 10)
        g.anchor = pixipt(0.5, 0.5)
        g.position = pixipt(400 - 75, 550 - 10)

        skip_text = do_new(
            PIXI.Text,
            "Skip video",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
            }
        )
        skip_text.position = pixipt(75, 20)
        skip_text.anchor = pixipt(0.5, 0.5)
        g.addChild(skip_text)

        self._instvid__skip_container.interactive = True
        self._instvid__skip_container.cursor = 'pointer'
        self._instvid__skip_container.on("pointertap", self._instvid__cleanup)

    def _instvid__start_clicked(self):
        VIDEO_URL = "resources/video/intro.mp4"

        self.pixi.stage.removeChild(self._instvid__play_container)
        self._instvid__video = PIXI.Texture.js_from(VIDEO_URL)

        video_sprite = self._instvid__video_sprite = do_new(
            PIXI.Sprite,
            self._instvid__video,
            {}
        )
        video_source = video_sprite.texture.baseTexture.resource.source
        
        self._instvid__video_sprite.width = 800
        self._instvid__video_sprite.height = 800 / 16 * 9
        self._instvid__video_sprite.anchor = pixipt(0.5, 0.5)
        self._instvid__video_sprite.position = pixipt(400, 300)

        self.pixi.stage.addChild(self._instvid__video_sprite)

        # When playback start is delayed a _lot_ we might still need to clean things
        # up because someone clicked "skip" before playback even started

        def watchdog_cleanup():
            if self._instvid__video_sprite is None:
                window.clearInterval(interval_id)
                video_source.pause()

        interval_id = window.setInterval(watchdog_cleanup, 100)

        video_source.addEventListener(
            "ended", self._instvid__cleanup
        )
        self.pixi.stage.addChild(self._instvid__skip_container)

    def _instvid__cleanup(self):
        self.pixi.stage.removeChild(self._instvid__play_container)
        self.pixi.stage.removeChild(self._instvid__skip_container)

        if self._instvid__video_sprite != None:
            self._instvid__video_sprite.texture.baseTexture.resource.source.pause()
            self.pixi.stage.removeChild(self._instvid__video_sprite)
            self._instvid__video_sprite.destroy()
            self._instvid__video_sprite = None

        if self._instvid__video != None:
            self._instvid__video.destroy()
            self._instvid__video = None

        self._done = True

    def showInstructionVideo(self):
        self._done = False
        self.pixi.stage.addChild(self._instvid__play_container)


class InstructionsMixin(Confirmable, TranslatableMixin):
    pixi = None
    
    def __init__(self):
        super().__init__()
        
        self._inst__active = False
        self._inst__current_index = None
        
        self._inst__instructions = None
        self.__assign_instructions(self.LANG_STRINGS.instruction_strings)
        
        self._inst__text_field = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "0xFFFFFF",
            })
        
        self._inst__text_field.position.set(100, 100)
        self._inst__text_field.style.wordWrap = True
        self._inst__text_field.style.wordWrapWidth = 600
        
    def __assign_instructions(self, text):
        self._inst__instructions = split_block_strings(text)
        if self._inst__active:
            self.displayInstructions()

    def displayInstructions(self):
        self._done = False
        
        if not self._inst__active:
            self.pixi.stage.addChild(self._inst__text_field)
        self._inst__active = True
        
        self.pixi.ticker.stop()
        
        if self._inst__instructions:
            if self._inst__current_index is None:
                self._inst__current_index = 0;
            else:
                self._inst__current_index += 1
            if self._inst__current_index >= len(self._inst__instructions):
                self._inst__current_index = None
                self._inst__active = False
                self._done = True
                self.pixi.stage.removeChild(self._inst__text_field)
                self.pixi.ticker.start()
            else:
                text = self._inst__instructions[self._inst__current_index]
                self._inst__text_field.text = text
                self.pixi.render()
                self.confirm(self.displayInstructions)
                
class LearnMixin(Confirmable, TranslatableMixin):
    pixi = None
    
    LEARN_WAIT_TIMES = [15.0, 15.0] # maximum presentation times before program automatically continues, , PP can move on self-paced earlier
    ANIMATION_TIME = 0.01
    
    TEXT_HEIGHT = 0.1
    
    
    def __init__(self):
        super().__init__()
        
        self._learn__image_sprite = None
        
        self._learn__sprite_visible = True
        
        self._learn__word_sprite = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
            })
        self._learn__word_sprite.position.x = LEARNED_WORD_POS[0]
        self._learn__word_sprite.position.y = LEARNED_WORD_POS[1]

        self._learn__translation_sprite = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
            })
        self._learn__translation_sprite.position.x = TRANSLATED_WORD_POS[0]
        self._learn__translation_sprite.position.y = TRANSLATED_WORD_POS[1]

        self._learn__instructions_sprite = do_new(
            PIXI.Text,
            self.LANG_STRINGS.image_learn_instruction,
            {
                "fontFamily": "Arial",
                "fontSize": 18,
                "fill": "#FFFFFF",
                "wordWrap": True,
                "wordWrapWidth": 120,
            })
        self._learn__instructions_sprite.position.x = 25
        self._learn__instructions_sprite.position.y = LEARNED_WORD_POS[1] - 25

    def _learn__destroy_image(self):
        if self._learn__image_sprite:
            self.pixi.stage.removeChild(self._learn__image_sprite)
            self._learn__image_sprite.destroy()
            self._learn__image_sprite = None
    
    @property
    def learn_sprite_visible(self):
        return self._learn__sprite_visible
    
    @learn_sprite_visible.setter
    def learn_sprite_visible(self, value):
        self._learn__sprite_visible = bool(value)
        self._learn__instructions_sprite.visible = bool(value)
        if self._learn__image_sprite is not None:
            self._learn__image_sprite.visible = self._learn__sprite_visible
    
    def _learn__create_image_sprite(self, image_url):
        sprite = PIXI.Sprite.js_from(PIXI.Cache.js_get(image_url))
        sprite.position.set(100, 50)
        x_scale = 600 / sprite.texture.orig.width
        y_scale = (500 - 2 * sprite.position.y) / sprite.texture.orig.height
        scale = min(x_scale, y_scale)
        sprite.scale = do_new(PIXI.Point, scale, scale)
         
        self._learn__image_sprite = sprite
        self._learn__image_sprite.visible = self.learn_sprite_visible
        self.pixi.stage.addChild(self._learn__image_sprite)
        
        self.pixi.render()
    
    def learn_prepare_image(self, image):
        self._learn__destroy_image()
        
        image_url = "resources/images/" + image
        if PIXI.Cache.has(image_url):
            self._learn__create_image_sprite(image_url)
            return True
        else:
            PIXI.Assets.load(image_url).then(
                lambda *_: self._learn__create_image_sprite(image_url)
            )
            return False
    
    def learn(self, image, word, translation):
        self._done = False
        
        self.pixi.ticker.stop()

        self.learn_prepare_image(image)

        self.learn_sprite_visible = True        
        self._learn__word_sprite.text = word
        
        self._learn__translation_sprite.text = translation
        self._learn__translation_sprite.visible = False
        
        self.pixi.stage.addChild(self._learn__word_sprite)
        self.pixi.stage.addChild(self._learn__translation_sprite)
        self.pixi.stage.addChild(self._learn__instructions_sprite)
        
        self.pixi.render()
        
        self.timed_confirm(self._learn__show_translation, self.LEARN_WAIT_TIMES[0])
        
    def _learn__show_translation(self):
        self._learn__translation_sprite.visible = True
        self.pixi.render()
        self.timed_confirm(self._learn__learn_done, self.LEARN_WAIT_TIMES[1])
    
    def _learn__learn_done(self):
        self.pixi.stage.removeChild(self._learn__word_sprite)
        self.pixi.stage.removeChild(self._learn__translation_sprite)
        self.pixi.stage.removeChild(self._learn__instructions_sprite)
        
        self.learn_sprite_visible = False
        self.pixi.ticker.start()
        self._done = True


class TestMixin(LearnMixin, Confirmable):
    pixi = None
    
    CORRECT_WORD_WAIT_TIME = 1
    WRONG_WORD_WAIT_TIME = 2

    @property
    def text_edit_location(self):
        input_x = int(re.sub("[^0-9]", "", self._test__text_input.css("left")))
        input_y = int(re.sub("[^0-9]", "", self._test__text_input.css("top")))
        return (input_x, input_y)

    def __init__(self, dom_element):
        super().__init__()
        
        self.__test_entered_word_callback = None
        
        self._test__word_sprite = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
            })
        self._test__word_sprite.position.x = LEARNED_WORD_POS[0]
        self._test__word_sprite.position.y = LEARNED_WORD_POS[1]
        self._test__word_sprite.visible = False
        self.pixi.stage.addChild(self._test__word_sprite)
        
        # TODO: Replace by X, remove _test__correct_word!
        self._test__correct_word = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#00FF00",
            })
        self._test__correct_word.position.x = LEARNED_WORD_POS[0]
        self._test__correct_word.position.y = LEARNED_WORD_POS[1]
        self._test__correct_word.visible = False
        self.pixi.stage.addChild(self._test__correct_word)

        self._test__text_input = jQuery('<input type="text" value="" placeholder="...?" />')
        self._test__text_input.css("position", "absolute")
        self._test__text_input.css("left", str(TRANSLATED_WORD_POS[0] - 2))
        self._test__text_input.css("top", str(TRANSLATED_WORD_POS[1] - 2))
        self._test__text_input.css("font-size", "24px")
        self._test__text_input.css("color", "white")
        self._test__text_input.css("display", "none")
        self._test__text_input.css("font-family", "Arial")
        jQuery(dom_element).append(self._test__text_input)
    
    def _test__show_words(self, word, translation, real_translation=None):
        self._test__word_sprite.text = word
        
        self._test__translation = translation
        self._test__word_sprite.visible = True
        
        self._test__text_input.val(translation)
        self._test__text_input.css("display", "block")
        self._test__text_input.css("color", "white")
        self._test__text_input.css("text-decoration", "")
        self._test__text_input.prop('disabled', False)
        self._test__text_input.focus()

        metrics = PIXI.TextMetrics.measureText(translation, self._test__correct_word.style)

        input_x, input_y = self.text_edit_location

        self._test__correct_word.text = real_translation or "[missing]"
        self._test__correct_word.position.x = input_x + 10 + metrics.width
        self._test__correct_word.position.y = input_y + 2

    def test(self, word, entered_word_callback=None):
        self._done = False
        
        self.__test_entered_word_callback = entered_word_callback
        
        self._test__show_words(word.name, "")
        
        self.pixi.ticker.stop()
        self.pixi.render()
        
        self.confirm(self._test__confirmed)
        
    def displayCorrect(self, word, entered):
        self._done = False
        self._test__show_words(word.name, entered)
        self._test__text_input.css("color", "#00FF00")
        self._test__text_input.prop('disabled', True)
        
        window.setTimeout(
            lambda *_: self._test__confirmed(),
            1000 * self.CORRECT_WORD_WAIT_TIME)
        
    def displayWrong(self, word, entered):
        self.learn_sprite_visible = True
        self.learn_prepare_image(word.image)
        
        if entered.strip() == "":
            entered = "x"

        self._done = False
        self._test__show_words(word.name, entered, word.translation)
        self._test__text_input.css("color", "red")
        self._test__text_input.css("text-decoration", "line-through")
        self._test__text_input.prop('disabled', True)

        self._test__correct_word.visible = True
        
        window.setTimeout(
            lambda *_: self._test__confirmed(),
            1000 * self.WRONG_WORD_WAIT_TIME)

    def _test__confirmed(self):
        self._test__correct_word.visible = False

        self._test__text_input.css("display", "none")
        self._test__word_sprite.visible = False
        self.learn_sprite_visible = False
        
        if self.__test_entered_word_callback is not None:
            self.__test_entered_word_callback(self._test__text_input.val())
        self.__test_entered_word_callback = None
        
        self.pixi.ticker.start()
        self._done = True

class HighscoreMixin(TestMixin, TranslatableMixin):
    pixi = None

    current_highscore = 0

    def _highscore__update_text(self):
        self._highscore__text.text = self.LANG_STRINGS.score_pattern.format(
            score=self.current_highscore
        )

    def __init__(self):
        self._highscore__text = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
            })
        self._highscore__text.position.set(600, 550)
        self._highscore__update_text()
        self.pixi.stage.addChild(self._highscore__text)

        self._highscore__jumpy_text = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#00FF00",
            })
        self._highscore__jumpy_text.position.set(600, 550)
        self._highscore__jumpy_text.text = f"NONE"
        self._highscore__jumpy_text.visible = False
        self.pixi.stage.addChild(self._highscore__jumpy_text)

        self._highscore__jump_anim_data = None

        PIXI.Ticker.shared.add(self._highscore__jumpy_text_anim)

    def _highscore__jumpy_text_anim(self, _):
        if self._highscore__jump_anim_data is None:
            self._highscore__jumpy_text.visible = False
        else:
            self._highscore__jump_anim_data["t_index"] += PIXI.Ticker.shared.elapsedMS

            start_pos = self._highscore__jump_anim_data["start"]
            end_pos = self._highscore__jump_anim_data["end"]
            
            duration = self._highscore__jump_anim_data["duration"]
            t_index = self._highscore__jump_anim_data["t_index"]
            if t_index > duration:
                self._highscore__jump_anim_data = None
                return
            
            f = t_index / duration
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * f
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * f - 200 * (1 - (f * 2 - 1)**2)

            self._highscore__jumpy_text.position.set(x, y)
            self._highscore__jumpy_text.visible = True

    def __start_jumpy_text(self, text):
        target = self._highscore__text.position

        self._highscore__jumpy_text.text = text
        self._highscore__jump_anim_data = {
            "duration": 300,
            "t_index": 0,
            "start": self.text_edit_location,
            "end": [target.x + 50, target.y],
        }

    def update_highscore(self, new_score):
        if new_score > self.current_highscore:
            self.__start_jumpy_text(f"+{new_score - self.current_highscore}")
        self.current_highscore = new_score
        self._highscore__update_text()

class MixedUpMixing(Confirmable):
    def _mixedup__create_text(self, text, pos):
        result = do_new(
            PIXI.Text,
            text,
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
            }
        )
        result.position.set(pos[0], pos[1])
        result.visible = False
        self.pixi.stage.addChild(result)
        return result

    def __init__(self):
        super().__init__()

        self._mixedup__instructions = self._mixedup__create_text(
            "You mixed up two words:",
            [LEARNED_WORD_POS[0], 400],
        )

        self._mixedup__display_matrix = [
            self._mixedup__create_text(
                "ORG WORD",
                [LEARNED_WORD_POS[0], LEARNED_WORD_POS[1]],
            ),
            self._mixedup__create_text(
                "ORG WORD",
                [TRANSLATED_WORD_POS[0], TRANSLATED_WORD_POS[1]],
            ),
            self._mixedup__create_text(
                "ORG WORD",
                [LEARNED_WORD_POS[0] + 200, LEARNED_WORD_POS[1]],
            ),
            self._mixedup__create_text(
                "ORG WORD",
                [TRANSLATED_WORD_POS[0] + 200, TRANSLATED_WORD_POS[1]],
            ),
        ]

        PIXI.Ticker.shared.add(self._mixedup__increase_size)

    def _mixedup__increase_size(self):
        for i in self._mixedup__display_matrix:
            x = i.scale.x
            x += PIXI.Ticker.shared.elapsedMS / 1000 / 0.2
            if x > 1:
                x = 1
            i.scale.set(x, x)

    def mixedup(self, a1, b1, a2, b2):
        self._mixedup__instructions.visible = True
        self._done = False

        def mark_done():
            self._mixedup__instructions.visible = False
            for i in self._mixedup__display_matrix:
                i.visible = False
            self._done = True

        def show_words():
            for i, a in zip(self._mixedup__display_matrix, [a1, b1, a2, b2]):
                i.text = a
                i.visible = True
                i.scale.set(0, 0)

            self.confirm(mark_done)

        window.setTimeout(show_words, 1000)

class RecapMixin(LearnMixin, Confirmable, TranslatableMixin):
    def __init__(self):
        self._recap__pre_strings = split_block_strings(self.LANG_STRINGS.recap_pre_instructions)
        self._recap__during_strings = split_block_strings(self.LANG_STRINGS.recap_during_instructions)
        self._recap__post_strings = split_block_strings(self.LANG_STRINGS.recap_post_instructions)

        self._recap__center_text = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
                "align": "left",
                "wordWrap": True,
                "wordWrapWidth": 500,
                "visible": False,
            }
        )
        self._recap__center_text.position.set(400, 300)
        self._recap__center_text.anchor.set(0.5)
        self.pixi.stage.addChild(self._recap__center_text)

        self._recap__bottom_text = do_new(
            PIXI.Text,
            "",
            {
                "fontFamily": "Arial",
                "fontSize": 24,
                "fill": "#FFFFFF",
                "align": "center",
                "wordWrap": True,
                "wordWrapWidth": 500,
                "visible": False,
            }
        )
        self._recap__bottom_text.position.set(400, 500)
        self._recap__bottom_text.anchor.set(0.5)
        self.pixi.stage.addChild(self._recap__bottom_text)

    def start_recap(self, word_items):
        grouped_by_image = {i.image: [] for i in word_items}
        for item in word_items:
            grouped_by_image[item.image].append(item)

        self._done = False

        def yield_seq():
            for s in self._recap__pre_strings:
                yield self._recap__center_text, 10, s, None

            for image, item_list in grouped_by_image.items():
                for s in self._recap__during_strings:
                    words = "  ".join(f"{i.name}={i.translation}" for i in item_list)
                    s = s.format(words=words)
                    yield self._recap__bottom_text, (1, 15), s, image
            
            for s in self._recap__post_strings:
                yield self._recap__center_text, (0, 5), s, None

        gen = yield_seq()

        def run():
            self.pixi.ticker.stop()
            self._recap__center_text.visible = False
            self._recap__bottom_text.visible = False
            self.learn_sprite_visible = False

            try:
                pixi_text, timeouts, text, image = next(gen)
            except StopIteration:
                self._done = True
                self.pixi.ticker.start()
                return
            
            forced_timeout, timeout = timeouts
            
            pixi_text.text = text
            pixi_text.visible = True
            self.pixi.render()
            if image is not None:
                self.pixi.ticker.start()
                self.learn_prepare_image(image)
                self.learn_sprite_visible = True

            self.timed_confirm(run, timeout)

        run()


class PIXIInterface(
    InstructionVideoMixin,
    InstructionsMixin,
    LearnMixin,
    TestMixin,
    HighscoreMixin,
    MixedUpMixing,
    RecapMixin,
    ApplicationInterface
):
    def __init__(self, dom_element):
        self.__done = True
        self.done_callback = None
        
        self.pixi = do_new(PIXI.Application,
            800, 600, 
            {
                "background": "#A0A0A0",
            })
        dom_element.appendChild(self.pixi.view)
        window.pixi_app = self.pixi
        
        self.pixi.renderer.background.color = "#A0A0A0"

        LearnMixin.__init__(self)
        InstructionVideoMixin.__init__(self)
        InstructionsMixin.__init__(self)
        TestMixin.__init__(self, dom_element)
        HighscoreMixin.__init__(self)
        MixedUpMixing.__init__(self)
        RecapMixin.__init__(self)

    @property
    def _done(self):
        return self.__done
    
    @_done.setter
    def _done(self, v):
        call = not self.__done and v 
        self.__done = v
        if call and self.done_callback != None:
            self.done_callback()

    @property
    def done(self):
        return self._done
