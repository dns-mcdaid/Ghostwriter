"""This is a testing class. In the future it should be re-implemented
as the legitimate starting point of this program."""
#!/usr/bin/python
import re
import sys
import nltk
from pos import Pos


# COMMANDS TO KNOW:
    # nltk.word_tokenize(raw) Splits the sentence
    # nltk.pos_tag(tokens) Get the POS tags

SONG_TITLES = []
PARTS_OF_SPEECH = {}

def get_lyrics_from_in_file(lyric_corpus):
    """Reads lyrics from an input and returns a dictionary of song titles containing lyrics."""
    with open(lyric_corpus, "r") as open_corpus:
        raw_text = open_corpus.readlines()
        lyrics = ""
        for line in raw_text:
            # Ensure that line is not whitespace
            if line.strip():
                if line[0] == "[":
                    title = re.sub(r"\[", "", line)
                    title = re.sub(r"\]", "", title)
                    stripped = title.strip()
                    current_title = stripped
                    SONG_TITLES.append(current_title)
                else:
                    lyrics += line
        # Add the last song and return
        return lyrics

def determine_tags(lyrics):
    """This function reads in a dictionary of songs, then breaks down their tags."""
    tokenized = nltk.word_tokenize(lyrics)
    tagged = nltk.pos_tag(tokenized)
    for index, word_with_token in enumerate(tagged):
        this_word = word_with_token[0]
        pos_string = word_with_token[1]
        if pos_string not in PARTS_OF_SPEECH:
            PARTS_OF_SPEECH[pos_string] = Pos(pos_string)

        PARTS_OF_SPEECH[pos_string].add_word(this_word)
        if index < len(tagged) - 1:
            PARTS_OF_SPEECH[pos_string].add_next_pos(tagged[index+1][1])

    # Set the markov values for each new POS in our existing POS objects.
    for tags in PARTS_OF_SPEECH.keys():
        this_pos = PARTS_OF_SPEECH[tags]
        this_pos.set_markov()

def print_footnote():
    """Prints the footnote message"""
    footnote = "Data gathered from "
    for index, title in enumerate(SONG_TITLES):
        if index < len(SONG_TITLES) - 1:
            footnote += title + ", "
        else:
            footnote += "and " + title

    artist = sys.argv[1].split(".")
    footnote += " by " + artist[0].title()
    print
    print footnote

def main():
    """Launches the program."""
    lyrics = get_lyrics_from_in_file(sys.argv[1])
    determine_tags(lyrics)
    print_footnote()


if __name__ == '__main__':
    main()
