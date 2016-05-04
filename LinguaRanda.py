import string
import random
import csv
import argparse


def make_new_lang(wfile, rfile, wvowels, wcons):
    csvfile = open(wfile, 'wb')
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    for line in open(rfile, 'r'):
        original = line.rstrip('\n')
        # Not interested in words that are just possessives of other words
        # Not interested in words that are proper nouns
        if not original.endswith('\'s') and not original[0].isupper():
            translation = ''
            vowels, consonants = w_consonants_vowels(wvowels, wcons)
            for _ in range(len(original)):
                pool = fill_letter_pool(translation, vowels, consonants)
                translation += ''.join(random.SystemRandom().choice(pool))

            writer.writerow([original,translation])


def w_consonants_vowels(wvowels, wcons):
    vowels = 'aeiou'
    cons = string.ascii_lowercase.translate(string.maketrans('', ''), vowels)
    vowels += wvowels
    cons += wcons
    return vowels, cons


def fill_letter_pool(word, vowels, consonants, vowelslim=3, conslim=2):
    c_count = 0
    if word[-1:] in consonants:
        lastset = consonants
        otherset = vowels
        limit = conslim
    else:
        lastset = vowels
        otherset = consonants
        limit = vowelslim

    for i in reversed(word):
        for c in set(lastset):
            c_count = c_count + 1 if i == c else c_count

    return otherset if c_count > limit - 1 else vowels + consonants



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wordlist',
            help='path to wordlist file')
    parser.add_argument('-o', '--output',
            help='path to output file')
    parser.add_argument('-v', '--wvowels',
            help='string containing extra weight characters for vowels')
    parser.add_argument('-c', '--wcons',
            help='string containing extra weight characters for consonants')
    args = parser.parse_args()

    output = args.output if args.output else 'newlang.csv'
    wordlist = args.wordlist if args.wordlist else '/usr/share/dict/american-english'
    wvowels = args.wvowels if args.wvowels else ''
    wcons = args.wcons if args.wcons else ''

    make_new_lang(wfile=output, rfile=wordlist, wvowels=wvowels, wcons=wcons)

if __name__=='__main__':
    main()
