class NL:
    stimuli_file = "stimuli_nl.csv"

    instruction_strings = """
In het komende uur ga je Litouwse woorden leren. Probeer deze woorden zo goed mogelijk te onthouden,
zodat je ze volgende week op een toets naar het Nederlands kunt vertalen!
 
[Enter]
---------------------
Zoals in het filmpje werd uitgelegd, zie je bij de eerste presentatie van een nieuw woord een achtergrondplaatje.
 
Deze plaatjes zijn bedoeld om je te helpen om een duidelijk, levendig beeld te bedenken bij elk woord.
 
[Enter]
---------------------
We raden je sterk aan om de methode te gebruiken die in de film uitgelegd werd. Probeer in elk geval een beeld te bedenken bij elk woord en koppel het aan de vertaling.
 
Mocht je vinden dat de plaatjes je niet helpen, dan mag je de plaatjes negeren. Het gaat erom dat je de woorden onthoudt, niet de achtergrondplaatjes.
 
[Enter]
---------------------
Straks tijdens het oefenen ga je ook oefenen om de woorden te vertalen. Je kunt de vertaling indienen door ENTER te drukken.

Het vertalen helpt je om de woorden te onthouden. Volgende week tijdens de toets moet je de woorden ook vertalen.
 
[Enter]
---------------------
Een laatste tip: tijdens het oefenen kun je bijna altijd op [Enter] drukken om sneller door te gaan met de volgende trial.
 
Druk [Enter] om met het oefenen te beginnen! Veel succes!

""".strip()
    
    image_learn_instruction = "Vorm een beeld bij het woord en druk Enter!"

    score_pattern = "Score: {score}"

    recap_pre_instructions = """
Je hebt al veel woorden geleerd. Laten we eens kijken hoe goed je de woorden onthouden hebt! 

[Enter]
---------------
Ga eerst in gedachten de kamers af waarin je je de woorden voorgesteld hebt. Weet je nog welke kamers je gezien hebt?

[Enter]
""".strip()
    
    recap_during_instructions = """
Denk nu aan alle woorden die je je in deze kamer voorgesteld hebt. Druk dan op [Enter]!
---------------
Dit zijn de woorden:
{words}
""".strip()

    recap_post_instructions = """
Goed! Nu ga je weer verder oefenen! [Enter]
""".strip()
    
    start_video_button = "Instructie video starten"
    skip_video_button = "Video overslaan"


class EN(NL):
    stimuli_file = "stimuli_en.csv"
    
    instruction_strings = """
In the next hour, you will practice Lithuanian words. Please try to remember the words as well as you can, so that you can translate them into Dutch on a test next week. 
 
[Enter]
---------------------
As we explained in the movie, new words are always introduced together with a background image. 

These images are meant to help you create a clear, vivid image for each word. 

[Enter]
---------------------
We strongly recommend that you try to use the method explained in the movie. In any case, try to come up with an image of the Lithuanian word that you can link to the translation. 

If the background images are not helpful for you, you can ignore them. It is important that you remember the words and their translation, not the background image. 
 
[Enter]
---------------------
During practice, you will repeatedly enter the translation of the words. You can submit a translations by pressing [Enter]. 

Translating the words from memory will help you remember them! It helps you prepare for the test next week, where you will also translate the words. 
 
[Enter]
---------------------
A last tip: During practice, you can almost always press [Enter] to continue more quickly to the next trial. 

When you are ready, please press [Enter] to start practicing! 

""".strip()
    
    image_learn_instruction = "Make an image of the word and press [Enter]"

    score_pattern = "Score: {score}"

    recap_pre_instructions = """
You already practiced quite a lot of words! Let’s see how well you can remember them! 

[Enter]
---------------
First, please think of the background images in which you pictured the different words. Do you remember all the rooms that you have seen so far? 

[Enter]
""".strip()
    
    recap_during_instructions = """
Now please think of the words that you pictured in this location and their translations. Then press [Enter] to see if you remembered them all.
---------------
These are the words:
{words}
""".strip()

    recap_post_instructions = """
Well done! Now you can continue practicing the words! [Enter]
""".strip()

    start_video_button = "Start instructions video"
    skip_video_button = "Skip video"


Default = EN
