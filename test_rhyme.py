import nltk

def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    potential_rhymes = set(rhymes)
    for rhyme in potential_rhymes:
        tokenized = nltk.word_tokenize(rhyme)
        tagged = nltk.pos_tag(tokenized)
        print tagged[0][0]

print "word?"
word = raw_input()
print "level?"
level = input()
rhyme(word, level)
