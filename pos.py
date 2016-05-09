"""The POS class creates an object for each part of speech, and stores words for further use."""
#!/usr/bin/python
import random
import bisect

class Pos(object):
    """Variables defined below."""
    def __init__(self, name):
        """Sets name and initializes words and parts of speech as empty."""
        self.name = name        # name of this part of speech
        self.phrases = []         # array of words which fit this part of speech
        self.next_pos = {}      # parts of speech which follow, including counts.
        self.total_pos = 0      # total number of parts of speech tags which may follow
        self.tags = []          # tags list to correspond with probabilities list.
        self.probabilities = [] # probabilities for landing on each tag.
        self.most_likely = ""   # most likely next tag.

    def add_phrase(self, phrase):
        """Adds a new phrase."""
        self.phrases.append(phrase.lower())

    def add_next_pos(self, new_pos):
        """Check if the new Part of Speech is in the dictionary, then increment."""
        if new_pos in self.next_pos:
            self.next_pos[new_pos] += 1
        else:
            self.next_pos[new_pos] = 1
        self.total_pos += 1

    def get_word_at_index(self, index):
        """"Get word from an index."""
        return self.phrases[index]

    def get_random_word(self):
        """Gets a random word from the phrases array."""
        index = random.randint(0, len(self.phrases)-1)
        return self.phrases[index]

    def get_random_pos(self):
        """Gets a random following POS tag."""
        rand_amt = random.random()
        i = bisect.bisect_right(self.probabilities, rand_amt)
        if i > 0:
            return self.tags[i-1]
        elif i == 0:
            return self.tags[i]
        raise ValueError


    def get_number_of_words(self):
        """Get the number of phrases belonging to this Part of Speech, including duplicates."""
        return len(self.phrases)

    def set_markov(self):
        """Set the markov values for the Parts of Speech in this instance."""
        base = 0.0
        current_top = 0.0
        top_tag = ""
        for tag in self.next_pos.keys():
            markov_prob = self.next_pos[tag] / float(self.total_pos)
            if markov_prob > current_top:
                current_top = markov_prob
                top_tag = tag
            self.next_pos[tag] = markov_prob
            base += markov_prob
            self.probabilities.append(base)
            self.tags.append(tag)
        if base == 0.0:
            self.tags.append("PRP")
            self.probabilities.append(1.0)
        self.most_likely = top_tag

    def find_rhyme(self, in_word, entries):
        syllables = [(word, syl) for word, syl in entries if word == in_word]
        potential_rhymes = []
        for (word, syllable) in syllables:
            potential_rhymes += [word for word, pron in entries if pron[-2:] == syllable[-2:]]
        for phrase in self.phrases:
            if phrase.find(' ') > -1:
                if phrase.split(' ')[1] in potential_rhymes:
                    return phrase
            elif phrase in potential_rhymes:
                return phrase
        # if self.name.find(':') > -1:
        #     separated = self.name.split(':')
        #     temp_name = separated[1]
        # else:
        #     temp_name = self.name
        # for rhyme in potential_rhymes:
        #     tagged = pos_tag(word_tokenize(rhyme))
        #     if tagged[0][1] == temp_name:
        #         return tagged[0][0]
        return self.get_random_word()
