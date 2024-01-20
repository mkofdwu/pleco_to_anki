# pleco_to_anki

A simple script to format pleco flashcard exports and convert it into an anki package

<img src="./example/example.png" width="300" />

## Update (20 Jan 2024)

To make this script more accessible to fellow-chinese learners, I made an app that achieves the same purpose but doesnt require python or even a PC. https://github.com/mkofdwu/pleco_to_anki_app

## Usage

You have to use python to run this script. Install the requirements with pip install -r requirements.txt

Export the flashcards you want from pleco (menu > import/export > export cards). Set the format to text file and character set to simplified, and check 'card definitions' and 'dictionary definitions'. Transfer the exported file to your computer

Then, in this directory run `python3 ./pleco_to_anki <path_to_pleco_file> <deck_name>`. A .apkg file should be generated in the out/ directory and you can install it by opening anki and going to File > Import > select the file

If you add new flashcards and want to update the anki deck, simply run the same command. This time, the deck will only contain new cards, and you can import them in the same way.

## Problems

This software was made hastily for personal use, so there are quite a few bugs, primarily definition parsing issues
