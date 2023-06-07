from pixi_interface import PIXIInterface
from word_presentation import AssignmentModel

def determineTextWidth(fontStimulus):
    # Determine text width using psychopy's pyglet infrastructure
    glyphList = fontStimulus._font.get_glyphs(fontStimulus.text)
    thisPixWidth = sum([0] + [x.advance for x in glyphList])
    return thisPixWidth * fontStimulus.height / fontStimulus._fontHeightPix / 1.5


def setLineStrikethrough(textStim, lineStim):
    lineStim.start = (textStim.pos[0], textStim.pos[1] - 0.01)
    lineStim.end = (textStim.pos[0] + determineTextWidth(textStim), textStim.pos[1] - 0.01)


IMAGES_SIZE = 1.3
IMAGES_LOCATION = (0, 1 - (IMAGES_SIZE / 2 + 0.05))

def load_all_images(imagePathList):
    result = {}
    for path in imagePathList:
        if path not in result:
            pass
            # # if not os.path.exists(path):
            # #  raise ValueError("Image {} does not exist".format(path))
            #imageStim = visual.ImageStim(win, pos=IMAGES_LOCATION)
            #imageStim.image = path
            #imageStim.size *= IMAGES_SIZE / imageStim.size[1]
        #result[path] = imageStim
    return result


async def load_data():
    import transcrypt_csv

    data = await asyncMakeRequest("resources/stimuli.csv")
    return transcrypt_csv.parse_csv(data.strip())
    

async def main():
    csv_data = await load_data()

    # Artificial dataset
    stimuli = [
        {
            "word": f"test-{i}",
            "translation": f"t-{i}",
            "image": f"room{(i+1)%10}.jpg"
        } for i in range(10)
    ]

    stimuli = [
        dict(zip(["word", "translation", "image"], row)) for row in csv_data[1:]
    ]
    
    pixi_interface = PIXIInterface(
        document.getElementById("main"))
    model = AssignmentModel(pixi_interface, stimuli)

    pixi_interface.done_callback = lambda : window.setTimeout(model.iter_run, 0)
    
    model.iter_run()
    #load_all_images(imagePathList)

