# Ghostwriter

### NYU Natural Language Processing Final Project

### by [Carter Yu](https://github.com/carteryu) and [Dennis McDaid](https://github.com/RajahBimmy)

## Usage

To run this program, hop on a UNIX machine and type `python lyric_generator.py file_name.txt`, where `file_name.txt` should be the name of the performing artist this corpus represents. All song titles should be indicated in square brackets, and parenthesis should be avoided if possible, as they love to confuse things. Give our Ghostwriter some time to let his creative juices flow (no more than thirty seconds on modern computers), and get ready for some artistic genius.

## Introduction

The question this project aimed to answer was whether or not implementation of existing Natural Language Processing algorithms could stand as at least a semi-decent substitute for actual authorship in music. Obviously our resources were limited to the research we'd done over the course of the last month in addition to any existing knowledge from class, but we figured that this would be enough to build a basic functioning system which would suit our needs.

Our personal goal was to experiment with new and exciting algorithms, grow to better understand how and why they work the way they do, and continue to develop our knowledge of the Natural Language Processing field as a whole. Lyrical generation was appealing, especially with the range of genres and artists we could work with, and the ability to see dramatic and tangible results (regardless of how coherent they turned out to be), was a major factor in our decision-making process.

The entire project sprung from a conversation between the two of us following Taylor Swift's Grammy win earlier this year (2016) for her album _1989_. Many believed that Kendrick Lamar's _To Pimp a Butterfly_ had been snubbed at the awards ceremony, and the two of us were in a heated debate. I claimed that _1989_ was a musical work of pure genius, while Carter argued that I was just buying in to cheap lyrics and weak themes, falling for Swift's same old act of repeating herself.

The position we took when facing this project was that based on the complexity and repetition of lyrics, generated text grew in coherency. The less repetitive and intricate the parts of the song were, the more easy they'd be to replicate. Our reasoning behind this theory was based on the premise that a lot of rap music is referential to events ongoing in the modern day, and that because they are packed with double entendres, if we can't understand half the subliminal messages, we can hardly expect NLTK to interpret them.

## Method

The program's initial design was relatively simple:
1. Use Part of Speech (POS) tags to categorize our entire input
2. Calculate Hidden Markov Model (HMM) scores for each POS in our training set.
3. Use these values to traverse a Markov train of POS's and output results.

The main tool that works all the magic for us in this project is NLTK. As demonstrated through both class and the home  works, NLTK has been more than robust enough to handle tagging and categorizing all of the raw text data we have available, and only on a few occasions did we encounter any problems.

Calculating the Hidden Markov Model scores was as simple as storing a dictionary of POS's to another dictionary of potential followup POS's and their probability (from `0.0 - 1.0`). This was accomplished by obtaining the number of times POS _b_ follows POS _a_, then dividing that value by the total number of POS occurrences which take place after _a_. Using these raw Markov values, we filled a separate dictionary of these POS tags with incrementing floating point numbers. For example, if there was a 75% chance that `PRP` would be followed by `NN`, and a 25% chance that `JJ` was the only other possible value to follow `PRP`, we'd construct a dictionary where if you were to throw a random number into the range of `0.0` to `1.0`, no matter where it landed in the `0.0 - 0.750` range, the function would return a `NN`, and likewise for `JJ` in the `0.751 - 1.0` range.

While originally only intended to hold words and their Hidden Markov scores, the Pos class was soon extended beyond its original post to hold multi-part Phrases. As our results below show, tying down coherent statements based on randomized Markov chaining between POS tags alone proved to be a little too chaotic, as having no recollection of previous locations had the potential to lock into a loop. So, we expanded our definition of Parts of Speech to include multiple pieces building up one larger phrase.

All that remained was to pick a starting point and traverse the chain until an end was in sight.

## Results

Naturally, that's not what happened. You can find our first test results below:

```
one questions ? ) am who 's Getting To cross a gon
From to hiding drones n't and revolt out again
But is comfort fire to be ( for blue now is mercy now
and understand what me crumbling never to sir Revere
me locked expendable me by Open n't tried to
You trapped around together killed 's free confusion )
're got wrong forever on your free Drones !
why It persisting finally is Running now and forever )
Your run ( make homes just gone n't left you
na freedom there is inciting to hide razed But this
```

Needless to say, something had to be changed. While the concept of "Hiding" previous values from the current decision-maker is an interesting approach to Machine Learning and Data traversal, it led to some terrible lyrical generation when left on its own. As the process of refining our project went on, the reality sunk in that without good material to test our generated text against, there was always going to be problems.

Being forced to eyeball our results made us realize where our program was following the right patterns, and where it was falling off path dramatically. We realized we needed to break the rules a little and filter our data to make it more accessible. We removed all punctuation, then added it back in for special cases, we forced chains to store themselves in groups of three at a time, and then keep an intense record on their descendants (i.e. rather than `JJ` knowing to go to `NN`, `PRP:DT:JJ` knew to go to `NN`). The goal of these changes was to force a half-baked Markov chain so that the phrase structure would make more sense and gain credibility. Suddenly, "? ) am who 's Getting To cross a gon" became "__you say__ _been waiting there with this_ __not that good style.__" While still nonsensical overall, parts of the larger phrase are plausible, which was a big step in the right direction. Part of the problem was the fact that we were sacrificing proper logical punctuation to spare ourselves random parenthesis in places, but we did our best to remove abbreviations and random apostrophe instances through implementation of the following checker:

```python
if pos_string not in PARTS_OF_SPEECH:
    PARTS_OF_SPEECH[pos_string] = Pos(pos_string)

    if this_word[0] == "\'":
        if tagged[index-1][0].rstrip()+this_word in contractions:
            this_word = tagged[index-1][0].rstrip()+this_word
            PARTS_OF_SPEECH[pos_string].add_phrase(this_word)
    else:
        PARTS_OF_SPEECH[pos_string].add_phrase(this_word)
```

While researching how exactly Markov Chains work, I stumbled upon the Rose-Hulman Institute of Technology's [explanation](http://www.rose-hulman.edu/Users/faculty/young/CS-Classes/csse221/200810/Projects/Markov/markov.html) of practically applying Markov chains. They present _The Beatitudes_, a section of the Bible wherein Jesus offers blessing to different groups of people, following an algorithm which is replicable through Markov Chaining. In short, the algorithm can be cut down to "Blessed are the `NP`, for they will `VP`." Finding the original text online, we copied the corpus into our project and began testing how we could best generate our own words of wisdom. Using the visualization below as an example, when we increased the number of tags to consider before using the next word on a small corpus, the likelihood of getting stuck in a self-referential loop or exactly mirroring the original input increased dramatically. The larger the working data set, the less likely this was to happen.

![markov](markov.png)

_The Beatitudes_ text is actually the main driving factor which led us to stick with the two preceding tags as the point of origin for the next tag. As seen earlier, when we used one it was too few, but when we used three, we wound up encountering heavily incoherent repetition along the lines of "theirs is the theirs is the theirs is the children of god." Rather than iterating on the "Blessed are the `X` for they `Y`", the generation found itself caught in a loop from inside of the existing text. What we found is that by factoring in just two prior tags to determine the next probability, while the results may never make sense, there are decently sized chunks within the output which could be taken out of context and potentially used in a song.

## Discussion

There was a lot of frustration in trying to get this program to work in a meaningful way. No, it will never pass any turing test in its current state, but the lyrical content could provide some diamonds in the rough for spring boarding into other songs. A lot of the challenges we faced were similar to the ones we encountered in homework 4. Punctuation was out to catch us, and so we had to make the decision to cut it cold turkey. Instead, we implemented line changes was by counting the syllables in a new line of the song, and comparing them to the average length of a line this artist performs. This was a little trickier with some of the rap songs, as many feature long speeches as interludes. Hence, this is why we chose to actively ignore any lines of a song that were in parens. In these cases, it wasn't just the spastic nature of seeing parens left and right in our output, but also the fickleness of what text we could (or rather, couldn't) expect to come from inside. While Kendrick Lamar uses these sections to go on rants about culture and the meaning of spoken word, Taylor Swift uses them almost exclusively for either Ooh's and Ahh's or repeating the last two words she just sang. Instances like these did a wonderful job at confusing the Markov Chains, and led to more closed circular sets of POS's than anything else.

The other major challenge was working on a rhyme scheme. We really wanted to implement this, since rhymes are the primary building blocks for most pop songs today. Unfortunately, it proved to be an extremely time-consuming challenge. While trying to find a perfect rhyme at an optimal speed proved difficult, we were able to find the next best thing by scouring the web for some guidance. After several days of searching, we found _[Kash's Tech Blog](https://kashthealien.wordpress.com/)_, which provided a pretty decent algorithm for determining a rhyme. NLTK provides us with CMU's dictionary, which contains thousands upon thousands of words, as well as their pronunciation. With a given word, let's use "bear" for arguments sake, it only takes a few seconds to return a list of words which fit a certain degree of rhyme similarity. If the degree is one, it returns a good couple hundred entries of words which might sounds somewhat similar, but they're clearer not rhymes. At degree two, we get results we'd expect (i.e. "pear", "care", "lair"). And at degree three, we get words that sound nearly identical (i.e. "bare", "behr"). The time penalty on finding all rhymes for a given word actually isn't all that bad, but when bring POS tags into the equation, our results get much worse. During the text generation process, this program will keep track of words it has at the end of some lines, to use as a template for the rhyme scheme. In the meantime, we rely on the Markov chain brings our generated text up to the desired POS at the end of the next line. The way we implemented our solution was by checking to see if any of the current words (gotten from our corpus) belonging to the POS are in the active rhyme set. If so, we have a new end of line, otherwise, just load another Markov-random word from this POS. In our original implementation, we traversed the rhyme set, looking for a word which both rhymed with the template and fit the given POS we were working with, but this tactic made the program twenty times slower, as there were cases with a huge number of words to tokenize and decipher.

__Our Rhyming Algorithm:__

```python
def find_rhyme(self, in_word, entries):
    # First, obtain the syllables belonging to this word.
    syllables = [(word, syl) for word, syl in entries if word == in_word]
    potential_rhymes = []
    for (word, syllable) in syllables:
        # Add any rhymes with a score of 2 or more.
        potential_rhymes += [word for word, pron in entries if pron[-2:] == syllable[-2:]]
    for phrase in self.phrases:
        if phrase.find(' ') > -1:
            # Check if we have an available phrase which also rhymes with the word.
            if phrase.split(' ')[1] in potential_rhymes:
                return phrase
        elif phrase in potential_rhymes:
            return phrase
    # Otherwise, return a boring old random word.
    return self.get_random_word()
```

## Conclusion
Overall, we felt that we learned a great deal from working on this project. Of course, a lot more improvements can be made regarding the results of our project. We do plan on continuing this project once the semester is over, as we have a clear direction on how we can improve this if we had more time. For instance, a simple way to produce more meaningful results would be to add more content with the training corpus. Another way would be to write additional features that can intelligently and adequately handle punctuation. Punctuation can be a nuisance because NLTK parses it and interprets it as a POS. This can be good or bad, depending on the context and so it would take quite a bit of time to research and figure out a clever solution to this. As it stands now, the most common punctuation is the comma and we realized that it slightly improved results if we simply took it out. Lastly, our implementation for designing the prior probabilities table could definitely be optimized. For now, we're proud of what we've built from scratch and we look forward to continuing this in the summer.

## References
1. https://web.stanford.edu/~jurafsky/slp3/8.pdf
2. http://cs.nyu.edu/courses/spring16/CSCI-UA.0480-011/lecture4-hmm.pdf
3. http://iaesjournal.com/online/index.php/IJAI/article/view/801/1028
4. http://mlg.eng.cam.ac.uk/zoubin/papers/ijprai.pdf
5. http://www.nltk.org/
6. https://kashthealien.wordpress.com/2013/06/15/213/
