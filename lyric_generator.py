"""This is a testing class. In the future it should be re-implemented
as the legitimate starting point of this program."""
#!/usr/bin/python
import re
import sys
import string
from nltk import pos_tag, word_tokenize
from pos import Pos

SONG_TITLES = []
PARTS_OF_SPEECH = {}

def get_lyrics_from_in_file(lyric_corpus):
    """Reads lyrics from an input and returns a dictionary of song titles containing lyrics."""
    with open(lyric_corpus, "r") as open_corpus:
        raw_text = open_corpus.readlines()
        lyrics = ""
        base = ""
        punc = set(string.punctuation)
        for line in raw_text:
            # Ensure that line is not whitespace
            if line.strip():
                if line[0] == "(":
                    continue
                elif line[0] == "[":
                    title = re.sub(r"\[", "", line)
                    title = re.sub(r"\]", "", title)
                    stripped = title.strip()
                    current_title = stripped
                    SONG_TITLES.append(current_title)
                else:
                    lyrics += base + line.strip()
                    if lyrics[len(lyrics) - 1] not in punc:
                        base = ", "
                    else:
                        base = " "
            elif len(lyrics) > 0 and lyrics[len(lyrics)-1] != "\n":
                lyrics += ".\n"   # Cheating to get the songs to recognize ends of lines.
                base = ""
        # Add the last song and return
        print lyrics
        return lyrics

def determine_tags(lyrics):
    """This function reads in a dictionary of songs, then breaks down their tags."""
    tokenized = word_tokenize(lyrics)
    tagged = pos_tag(tokenized)
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

def generate():
    """Generates random lyrics using Markov Chaining."""
    word_count = 0
    current_pos = "NN"
    output = ""
    while word_count < 100:
        this_pos = PARTS_OF_SPEECH[current_pos]
        output += this_pos.get_random_word() + " "
        current_pos = this_pos.get_random_pos()
        word_count += 1
    print output


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
    # determine_tags(lyrics)
    # generate()
    # print_footnote()


if __name__ == '__main__':
    main()
