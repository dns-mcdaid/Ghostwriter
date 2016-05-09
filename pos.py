"""The POS class creates an object for each part of speech, and stores words for further use."""
#!/usr/bin/python
import random

class Pos(object):
    """Variables defined below."""
    def __init__(self, name):
        """Sets name and initializes words and parts of speech as empty."""
        self.name = name    # name of this part of speech
        self.words = []     # array of words which fit this part of speech
        self.next_pos = {}  # parts of speech which follow, including counts.
        self.total_pos = 0

    def add_word(self, word):
        """Adds a new word."""
        self.words.append(word)

    def add_next_pos(self, new_pos):
        """Check if the new Part of Speech is in the dictionary, then increment."""
        if new_pos in self.next_pos:
            self.next_pos[new_pos] += 1
        else:
            self.next_pos[new_pos] = 1
        self.total_pos += 1

    def get_word_at_index(self, index):
        """"Get word from an index."""
        return self.words[index]

    def get_random_word(self):
        """Gets a random word from the words array."""
        index = random.randint(0, len(self.words))
        return self.words[index]

    def get_number_of_words(self):
        """Get the total number of words belonging to this Part of Speech, including duplicates."""
        return len(self.words)

    def set_markov(self):
        """Set the markov values for the Parts of Speech in this instance."""
        for tag in self.next_pos.keys():
            new_amt = self.next_pos[tag] / float(self.total_pos)
            self.next_pos[tag] = new_amt
