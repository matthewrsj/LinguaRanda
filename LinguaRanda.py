import string
import random
import csv


def make_new_lang(wfile='newlang.csv', rfile='/usr/share/dict/american-english'):
    csvfile = open(wfile, 'wb')
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in open(rfile, 'r'):
        original = line.rstrip('\n')
        if not original.endswith('\'s'):
            translation = ''
            vowels = 'aeiou'
            identity = string.maketrans('','')
            consonants = string.ascii_lowercase
            consonants.translate(identity, vowels)
            for _ in range(len(original)):
                c_count = 0
                s = string.ascii_lowercase
                for i in reversed(translation):
                    if i in vowels:
                        break
                    for c in consonants:
                        c_count = c_count + 1 if i == c else c_count
                if c_count > 1:
                    s = vowels
                translation += ''.join(random.SystemRandom().choice(s))
            writer.writerow([original,translation])


if __name__=='__main__':
    make_new_lang()
