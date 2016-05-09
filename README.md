# Ghostwriter

### NYU Natural Language Processing Final Project

### by [Carter Yu](https://github.com/carteryu) and [Dennis McDaid](https://github.com/RajahBimmy)

## Abstract

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

Being forced to eyeball our results made us realize where our program was following the right patterns, and where it was falling off path dramatically. We realized we needed to break the rules a little and filter our data to make it more accessible. We removed all punctuation, then added it back in for special cases, we forced chains to store themselves in groups of three at a time, and then keep an intense record on their descendants (i.e. rather than `JJ` knowing to go to `NN`, `PRP:DT:JJ` knew to go to `NN`). The goal of these changes was to force a half-baked Markov chain so that the phrase structure would make more sense and gain credibility.

## Discussion

## Conclusion

## References
