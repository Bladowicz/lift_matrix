import argparse
import logging
import os
import sys

def validate_args(conf):
    if not os.path.exists(conf.in_file):
        logging.error('Input file does not exist')
        sys.exit()
    else:
        if not os.access(conf.in_file, 4):
            logging.error('Dont have permissions to read input file.')
            sys.exit()

    if os.path.exists(conf.out_file):
        if conf.force_overwrite:
            logging.warning('Output file exists - overwriting.')
        else:
            logging.error('Output file already exists. Please change name, of add -F')
            sys.exit()

    if not os.access(conf.out_file, 2):
        logging.error('Dont have permissions to write in output file.')
        sys.exit()




def _get():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='in_file',
                                help='Input file in Vopal Wabbit input format',
                                default='input.vw')

    parser.add_argument('-o', action='store', dest='out_file',
                                help='Output file in matrix format',
                                default='output.txt')


    parser.add_argument('-n', action='store', dest='namespaces',
                                help='String made of concatenated first laters of namespaces',
                                default='h')

    parser.add_argument('-c', action='store', dest='cut',
                                help='Cut top C of occurences',
                                default=250)

    parser.add_argument('-l', action='store_true', default=False,
                                dest='clog',
                                                    help='Count logarithm of value.')

    parser.add_argument('-F', action='store_true', default=False,
                                dest='force_overwrite',
                                                    help='Overwrite output file.')
    #parser.add_argument('-f', action='store_false', default=False,
    #                            dest='boolean_switch',
    #                                                help='Set a switch to false')
    #
    #parser.add_argument('-a', action='append', dest='collection',
    #                            default=[],
    #                                                help='Add repeated values to a list',
    #                                                                    )
    #
    #parser.add_argument('-A', action='append_const', dest='const_collection',
    #                            const='value-1-to-append',
    #                                                default=[],
    #                                                                    help='Add different values to list')
    #parser.add_argument('-B', action='append_const', dest='const_collection',
    #                            const='value-2-to-append',
    #                                                help='Add different values to list')
    #
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    out =  parser.parse_args()
    validate_args(out)
    return out
results = _get()
