from pixi_interface import PIXIInterface
from word_presentation import AssignmentModel

IMAGES_SIZE = 1.3
IMAGES_LOCATION = (0, 1 - (IMAGES_SIZE / 2 + 0.05))


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
