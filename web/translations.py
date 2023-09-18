class NL:
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
    instruction_strings = """
In the coming hour you will learn Lithuanian words. Try to remember these words as good as possible such that you can translate them next week to English!
 
[Enter]
---------------------
Like we explained in the movie, you will see a background image at the first presentation of a new word.

These images are meant to help you create a clear, lively image for each word.
 
[Enter]
---------------------
We strongly advise you to use the method that we explained in the movie. Try at least to think of an image for each word and relate this to the translation. If you think that the rooms do not help you, you can ignore them. It is most important that you remember the words, not the rooms.
 
[Enter]
---------------------
During the task you will also practice translating the words. You can submit your translation by pressing ENTER. Translating will help you to remember the words. Next week during the test you will have to translate the words as well.
 
[Enter]
---------------------
A last tip: during practice you can press [Enter] almost always to continue to the next trial. 

Press [Enter] to start the task! Good luck!

""".strip()

    start_video_button = "Start instructions video"
    skip_video_button = "Skip video"


Default = EN
