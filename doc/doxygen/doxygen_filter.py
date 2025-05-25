#!/usr/bin/env python

# pylint: disable=I0011, C0103,C0301,C0302,R0902,R0911,R0912,R0915,W1201,W0614,W0401,W0402

""" Fileter sourcecoude for Sphinx
"""

import getopt
import os.path
import sys
# import logging

from stat import *

# Output file stream
outfile = sys.stdout
# outfile = open('test_out.txt','w')

# Output buffer
# outbuffer = []

# out_row = 0
# out_col = 0

# Variables used by rec_name_n_param()
name = ""
param = ""
# doc_string = ""
# record_state = 0
# bracket_counter = 0

# Comment block buffer
# comment_block = []
# comment_finished = 0


# ===============================================================================
# dump
# ===============================================================================
def dump(filename):
    """ Just dump the contents of the given filename to stdout
    @param filename file to dump
    @returns Nothing
    """

    with open(filename, "r", encoding="utf-8") as f:
        r = f.readlines()

    for s in r:
        sys.stdout.write(s)


# ===============================================================================
# do_filter
# ===============================================================================
def do_filter(filename):
    """ Perform the sphinx filter on the given filename
    @param filename The file to filter
    """

    # logging.info('do_filter(%s)' % filename)

    global name

    # _path, name = os.path.split(filename)
    # root, _ext = os.path.splitext(name)
    #
    # # set module name for tok_eater to use if there's a module doc string
    # name = root

    sys.stderr.write('Filtering "' + filename + '"...' + '\r\n')

    # Open the sourcefile and read all the lines
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    text = ''.join(lines)
    if '@file' not in text:
        print('Missing @file description')
    if '@brief' not in text:
        print('Missing @brief description')

    # Determine the number of lines
    # linenr = 0

    for s in lines:
        # linenr += 1
        if s.strip() == '@dumpFuncname':
            continue
        if s.strip() == '@dumpArgs':
            continue
        if '@file' in s:
            p = s.replace('@file', '@package')
            p = p.replace('.py', '')
            outfile.write(p)
            p = s.replace('@file', '@namespace')
            p = p.replace('.py', '')
            outfile.write(p)
        ##        if s.startswith('    """'):
        ##            s = s.replace('"""', '"""!')
        ##            sys.stderr.write(s)
        ##        if s.startswith('        """'):
        ##            s = s.replace('"""', '"""!')
        ##            sys.stderr.write(s)
        if '    """' in s:
            s = s.replace('"""', '"""!')
        if ':param' in s:
            s = s.replace(':param', '@param')
            s = s.replace(':', '', 1)
        if '@param' in s:
            s = s.replace('@param:', '@param')
            s = s.replace(':', '', 1)
        if ':return' in s:
            s = s.replace(':return', '@return')
            s = s.replace(':returns', '@return')
            s = s.replace(':', '', 1)
        if '@return' in s:
            s = s.replace('@return:', '@return')
            s = s.replace('@returns:', '@return')
        outfile.write(s)

    # # Now flush the output buffer
    # for s in outbuffer:
    #     outfile.write(s)
    #     # logging.info(s.strip())


# ===============================================================================
# filter_file
# ===============================================================================
def filter_file(filename, _out=sys.stdout):
    """ Perform the shpinx filter on the given filename
    :param filename:
    :param _out:
    """

    # global outfile

    try:
        _root, ext = os.path.splitext(filename)

        if ext == ".py":
            do_filter(filename)
        else:
            dump(filename)

        sys.stderr.write("OK\n")
    except IOError as e:
        sys.stderr.write(e[1] + "\n")


# ===============================================================================
# __main__
# ===============================================================================
if __name__ == "__main__":

    # -----------------------------------
    # Logging setup
    # -----------------------------------
    # logging.basicConfig(level=logging.DEBUG,
    # format='%(levelname)-5s: %(message)s',
    # filename = 'sphinx_filter.log',
    # filemode = 'w+')

    # Get arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf", ["help"])
        # logging.debug('%s %s' % (opts, args))
    except getopt.GetoptError:
        # logging.error(e)
        sys.exit(1)

    # Determine filename
    testfilename = ''.join(args)
    # logging.debug('filename = %s' % testfilename)

    # Filter the file
    filter_file(testfilename)
