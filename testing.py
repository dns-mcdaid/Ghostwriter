#!/usr/bin/python
import nltk
import re
import sys

# COMMANDS TO KNOW:
    # nltk.word_tokenize(raw) Splits the sentence
    # nltk.pos_tag(tokens) Get the POS tags

def getLyricsFromInFile(lyric_corpus):
    songs = {}
    with open(lyric_corpus, "r") as open_corpus:
        raw_text = open_corpus.readlines()
        song_text = ""
        current_title = ""
        for line in raw_text:
            # Ensure that line is not whitespace
            if line.strip():
                if(line[0] == "["):
                    if(len(current_title) > 0):
                        # Case where a song does exist
                        songs[current_title] = song_text
                        song_text = ""
                    title = re.sub(r"\[", "", line)
                    title = re.sub(r"\]", "", title)
                    stripped = title.strip()
                    current_title = stripped
                else:
                    song_text += line
        # Add the last song and return
        songs[current_title] = song_text
        return songs

def main():
    songs = getLyricsFromInFile(sys.argv[1])
    for title in songs.keys():
        tokenized = nltk.word_tokenize(songs[title])
        tagged = nltk.pos_tag(tokenized)
        print(tagged)
        print


if __name__ == '__main__':
    main()
