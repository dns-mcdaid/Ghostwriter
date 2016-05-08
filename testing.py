"""This is a testing class. In the future it should be re-implemented
as the legitimate starting point of this program."""
#!/usr/bin/python
import re
import sys
import nltk



# COMMANDS TO KNOW:
    # nltk.word_tokenize(raw) Splits the sentence
    # nltk.pos_tag(tokens) Get the POS tags

def get_lyrics_from_in_file(lyric_corpus):
    """Reads lyrics from an input and returns a dictionary of song titles containing lyrics."""
    songs = {}
    with open(lyric_corpus, "r") as open_corpus:
        raw_text = open_corpus.readlines()
        song_text = ""
        current_title = ""
        for line in raw_text:
            # Ensure that line is not whitespace
            if line.strip():
                if line[0] == "[":
                    if len(current_title) > 0:
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

def determine_tags(songs):
    """This function reads in a dictionary of songs, then breaks down their tags."""
    noun_match = {}
    total_successors = 0
    for title in songs.keys():
        tokenized = nltk.word_tokenize(songs[title])
        tagged = nltk.pos_tag(tokenized)
        for index, word_with_token in enumerate(tagged):
            if index < len(tagged) - 1:
                if word_with_token[1] == "NN" or word_with_token[1] == "NNP":
                    next_tag = tagged[index+1][1]
                    if len(next_tag) > 1:
                        if next_tag in noun_match:
                            noun_match[next_tag] += 1
                        else:
                            noun_match[next_tag] = 1
                        total_successors += 1

    print total_successors
    temp_total = 0
    for following_tag, count in noun_match.items():
        print following_tag
        to_add = count / float(total_successors)
        print to_add
        temp_total += to_add
    print temp_total

def main():
    """Launches the program."""
    songs = get_lyrics_from_in_file(sys.argv[1])
    determine_tags(songs)



if __name__ == '__main__':
    main()
