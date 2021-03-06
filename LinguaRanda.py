#!/usr/bin/env python

import string
import random
import csv
import argparse


class LinguaRanda(object):

    def __init__(self, tfile='newlang.csv'):
        # file that contains all the translations
        self.tfile = tfile
        # dictionary containing original to new translations
        self.tdict = None
        # dictionary containing new to original translations
        self.tdict_to_orig = None
        self.phonemesc = []
        self.phonemesv = []
        self.phonemescv = []
        self.phonemesr = []
        self.__get_phonemes()

    def make_new_lang(self, wfile='newlang.csv',
                      rfile='/usr/share/dict/american-english',
                      wvowels='', wcons='',
                      vlim=3, clim=2):
        """
        Create a new language csv file `wfile` that contains translations from
        `rfile` to randomize language. Weight letter frequency by `wvowels` and
        `wcons`. Limit consecutive vowels and consonants by `vlim` and `clim`.
        Also sets self.tdict and self.tdict_to_orig.
        """
        # List of created translations to check for duplicates
        dup_checker = list()
        # CSV file to write to, delimit with commas
        writer = csv.writer(open(wfile, 'wb'), delimiter=',')
        # Set the bi-directional dicts
        self.tdict = dict()
        self.tdict_to_orig = dict()
        prev = 'a'

        # Open the rfile, read in each word, one per line
        for line in open(rfile, 'r'):
            dup = True
            # Keep generating random words until it isn't a duplicate of a
            # previously generated word
            while dup is True:
                original = line.rstrip('\n')
                nextl = original[0]
                if nextl != prev:
                    print nextl
                    prev = nextl
                # Not interested in words that are just possessives of other
                # words or that are proper nouns
                if (not original.endswith('\'s') and not original[0].isupper()
                    and (original == 'i' or original == 'a' or len(original) != 1)):
                    translation = ''
                    vowels, consonants = self.__w_consonants_vowels(wvowels,
                                                                    wcons)
                    #for i in range(len(original)):
                    while len(translation) < len(original):
                        # Fill letter choice pool for next letter
                        pool = self.__fill_letter_pool(translation,
                                                       vowels, consonants,
                                                       vlim, clim)
                        n = ''.join(random.SystemRandom().choice(pool))
                        # Select next letter from pool
                        translation += n #''.join(random.SystemRandom()
                                               #.choice(pool))

                    # Duplicate not found, add word to appropriate places
                    if translation not in dup_checker:
                        dup_checker.append(translation)
                        writer.writerow([original, translation])
                        self.tdict[original] = translation
                        self.tdict_to_orig[translation] = original
                        dup = False
                    # Duplicate found, try again
                    else:
                        dup = True
                # If doesn't end in 's or start with uppercase (this is
                # dictionary specific!) set dup to False so we can continue
                # to next word
                else:
                    dup = False

        # Don't need this anymore?
        del(dup_checker)

    def translate_phrase(self, phrase, to_new):
        """
        Translate a phrase from original language to new language if to_new is
        True, vice versa if to_new is False.
        """
        # Remove punctuation from string
        phrase = phrase.translate(string.maketrans('', ''), string.punctuation)
        words = phrase.split(' ')

        # If the in-memory translation dict does not exist, create it
        if self.tdict is None or self.tdict_to_orig is None:
            self.__read_dict()

        # Set proper translation dictionary depending on to_new flag
        dictionary = self.tdict if to_new else self.tdict_to_orig
        result = ''

        # Append translation to result
        for word in words:
            word = word.lower()
            result += dictionary[word] if word in dictionary else word
            result += ' '

        return result

    def __get_phonemes(self):
        self.phonemesc = []
        self.phonemesv = []
        self.phonemescv = []
        self.phonemesr = []
        f = open('phonemes/phonemev', 'r')
        for line in f.readlines():
            self.phonemesv.append(line[:-1])
        f = open('phonemes/phonemec', 'r')
        for line in f.readlines():
            self.phonemesc.append(line[:-1])
        f = open('phonemes/phonemecv', 'r')
        for line in f.readlines():
            self.phonemescv.append(line[:-1])
        f = open('phonemes/phonemer', 'r')
        for line in f.readlines():
            self.phonemesr.append(line[:-1])

    def __w_consonants_vowels(self, wvowels, wcons):
        """
        Return weighted sets of vowels and consonants. Just appends the
        user-defined weights to the vowel and consonant strings.
        """
        vowels = 'aeiou'
        cons = string.ascii_lowercase.translate(string.maketrans('', ''),
                                                vowels)
        vowels += wvowels
        cons += wcons
        return vowels, cons

    def __fill_letter_pool(self, word, vowels, consonants, vlim, clim):
        """
        NEEDS WORK
        Fill letter pool for random letter selection. This is based on what is
        already in `word` already. Only `vlim` consecutive vowels and `clim`
        consecutive consonants are allowed. The `vowels` and `consonants`
        strings are the weighted selections of vowels and consonants.
        """
        c_count = 0
        # Check last letter in the word. If consonant continue checking for
        # consonants. Vice versa for vowels
        if word[-1:] in self.phonemesc:
            lastset = self.phonemesc
            otherset = self.phonemesv
            limit = clim
        else:
            lastset = self.phonemesv
            otherset = self.phonemesc
            limit = vlim

        # Count last consecutive vowels or consonants
        for i in reversed(word):
            for c in set(lastset):
                c_count = c_count + 1 if i == c else c_count

        # Letter pool is the 'other' set if vlim or clim is exceeded
        # otherwise return both
        # TODO: Come up with a better way to select pool
        option = self.phonemesv + self.phonemescv + self.phonemesr
        return otherset if c_count > limit - 1 else option

    def __read_dict(self):
        """
        Populate bi-directional dicts with self.tfile translation file
        """
        # Original to new
        with open(self.tfile, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.tdict = {row[0]: row[1] for row in reader}

        # New to original
        with open(self.tfile, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.tdict_to_orig = {row[1]: row[0] for row in reader}


def main():
    # Command line flags
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wordlist',
                        help='path to wordlist file')
    parser.add_argument('-o', '--output',
                        help='path to output translations file')
    parser.add_argument('-v', '--wvowels',
                        help=('string containing extra weight characters for '
                              'vowels'))
    parser.add_argument('-c', '--wcons',
                        help=('string containing extra weight characters for '
                              'consonants'))
    parser.add_argument('-vl', '--vlimit',
                        help=('integer limit of consecutive vowels allowed, '
                              'default 3'))
    parser.add_argument('-cl', '--climit',
                        help=('integer limit of consecutive consonants '
                              'allowed, default 2'))
    parser.add_argument('-t', '--translate',
                        help='string to translate to new language')
    parser.add_argument('-tf', '--tfile',
                        help='path to translations file')
    parser.add_argument('-tb', '--translate_back',
                        help='string to translate back to original language')
    args = parser.parse_args()

    output = args.output if args.output else 'newlang.csv'
    wordlist = (args.wordlist if args.wordlist
                else '/usr/share/dict/american-english')
    wvowels = args.wvowels if args.wvowels else ''
    wcons = args.wcons if args.wcons else ''
    vlimit = args.vlimit if args.vlimit else 3
    climit = args.climit if args.climit else 2

    lingua = LinguaRanda(args.tfile) if args.tfile else LinguaRanda()

    if args.translate:
        print lingua.translate_phrase(args.translate, True)
    elif args.translate_back:
        print lingua.translate_phrase(args.translate_back, False)
    else:
        lingua.make_new_lang(wfile=output, rfile=wordlist, wvowels=wvowels,
                             wcons=wcons, vlim=vlimit, clim=climit)
        print 'output translations to {}'.format(output)


if __name__ == '__main__':
    main()
