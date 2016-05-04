# LinguaRanda

Lingua Randa translates words in a dictionary file (words separated by newlines)
into random words while following these restrictions:

* No more than two consonants in a row
* No more than three vowels in a row

The user can add weights to letters selected in the randomization by passing
them to the `-v` and `-c` tags as arguments.

```
usage: LinguaRanda.py [-h] [-w WORDLIST] [-o OUTPUT] [-v WVOWELS] [-c WCONS]

optional arguments:
  -h, --help            show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        path to wordlist file
  -o OUTPUT, --output OUTPUT
                        path to output file
  -v WVOWELS, --wvowels WVOWELS
                        string containing extra weight characters for vowels
  -c WCONS, --wcons WCONS
                        string containing extra weight characters for
                        consonants
```

Example:

```
LinguaRanda.py -v 'iiiiiooeeu' -c 'ttttrrrl'
```

produces a dictionary with more `i`s, `o`s, `e`s, `u`s, `t`s, `r`s, and `l`s
than other letters.

The original word list is defined by the user with the `-w` flag or is set to
`/usr/share/dict/american-english` by default.

The translation is output to a csv file. The file is defined by the user with
the `-o` flag or set to `./newlang.csv` by default.
