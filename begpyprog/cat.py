#!/usr/bin/env python
####################################################################################################
"""
A simple implementation of the UNIX ``cat`` command. It only implements the ``--number`` option.
It is useful for illustrating file layout and best practices in Python. 

This is a triple quoted docstring for the whole module (this file). If you import this module
somewhere else and run ``help(cat)``, you will see this.

This docstring also contains a ``doctest`` which serves as an example of programmatically using
the code. It also functions as a doctest. The ``doctest`` module can execute this docstring and
validate it by checking any output.

#
# Additional explanatory comments:
#
# Not needed - believe because of universal newline:
#>>> import os
#>>> line_end = os.linesep
#>>> fin = StringIO.StringIO('hello' + line_end + 'world' + line_end)
#
# This doesn't work, need to escape newlines as '\\n'
#>>> fin = StringIO.StringIO('hello\nworld\n')
#
# Not needed but shows how to use options:
#>>> print fout.getvalue() #doctest: +NORMALIZE_WHITESPACE
#
# Run doctest from command line:
# python -m doctest [-v] cat.py
#

>>> import StringIO
>>> fin = StringIO.StringIO('hello\\nworld\\n')
>>> fout = StringIO.StringIO()
>>> cat = Catter([fin], show_numbers=True)
>>> cat.run(fout)
>>> print fout.getvalue()
     0  hello
     1  world
<BLANKLINE>
"""

import argparse
import logging
import sys

__version__ = '0.0.2'

logging.basicConfig(level=logging.DEBUG)

class Catter(object):
    """
    A class to concatenate files to standard out
     
    This is a class docstring, ``help(cat.Catter)`` would show this.
    """
    
    def __init__(self, files, show_numbers=False):
        self.files = files
        self.show_numbers = show_numbers
    
    def run(self, fout):
        # use 6 spaces for numbers and right align
        fmt = '{0:>6}  {1}'
        count = 0
        for fin in self.files:
            logging.debug('catting {0}'.format(fin))
            for line in fin.readlines():
                if self.show_numbers:
                    fout.write(fmt.format(count, line))
                    count += 1
                else:
                    fout.write(line)
    
def main(args):
    """
    Logic to run a cat with arguments
    """
    parser = argparse.ArgumentParser(
        description='Concatenate FILE(s), or '
        'standard input, to standard output')
    parser.add_argument('--version',
        action='version', version=__version__)
    parser.add_argument('-n', '--number',
        action='store_true',
        help='number all output lines')
    parser.add_argument('files', nargs='*',
        type=argparse.FileType('r'),
        default=[sys.stdin], metavar='FILE')
    parser.add_argument('--run-tests',
        action='store_true',
        help='run module tests')
    args = parser.parse_args(args)
    
    if args.run_tests:
        import doctest
        doctest.testmod()
    else:
        cat = Catter(args.files, args.number)
        cat.run(sys.stdout)
        logging.debug('done catting')

if __name__ == '__main__':
    main(sys.argv[1:])

