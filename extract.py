import functools

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.collocations import (
    BigramAssocMeasures,
    TrigramAssocMeasures,
    BigramCollocationFinder,
    TrigramCollocationFinder,
)

# Just leaving this here for now, need to install these
nltk_dependencies = (
    'averaged_perceptron_tagger'
)

bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()


# Some utilities for debugging composed functions
def debug(arg):
    import ipdb
    ipdb.set_trace()
    return arg


def echo(arg):
    print('\n{}\n'.format(arg))
    return arg


# Function composition - yay
def compose(*fns):
    def inner(fn1, fn2):
        return lambda *x, **y: fn1(fn2(*x, **y))
    return functools.reduce(inner, fns)


# This lets you apply multiple functions to the same input
def fn_add(*fns):
    def inner(fn1, fn2):
        return lambda *x, **y: fn1(*x, **y) + fn2(*x, **y)
    return functools.reduce(inner, fns)


def filter_candidates(pairs):
    return [
        pair[0] for pair in pairs if pair[1] in ['NN', 'JJ']
    ]


def extract_common(words):
    # This is hard on a small corpus...
    return []


def extract_bigram(words):
    finder = BigramCollocationFinder.from_words(words)
    return finder.nbest(bigram_measures.pmi, 5)


def extract_trigram(words):
    finder = TrigramCollocationFinder.from_words(words)
    return finder.nbest(trigram_measures.pmi, 5)


# The echos are for debugging the intermediate steps
main = compose(
    fn_add(extract_common,
           extract_bigram,
           extract_trigram),    echo,  # Get individual, bigram, and trigram keywords
    filter_candidates,          echo,  # Get nouns and adjectives
    pos_tag,                    echo,  # Tag words by part of speech
    word_tokenize,              echo,  # Separate sentence into words
)
