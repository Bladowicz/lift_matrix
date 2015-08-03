import argparse
import logging
import os
import sys

def validate_args(conf):
    conf.in_file = conf.in_file[0]
    if not os.path.exists(conf.in_file):
        logging.error('Input file does not exist')
        sys.exit()
    else:
        if not os.access(conf.in_file, 4):
            logging.error('Dont have permissions to read input file.')
            sys.exit()

    conf.out_file = conf.out_file[0]
    if os.path.exists(conf.out_file):
            logging.warning('Output file exists - overwriting.')
            if not os.access(conf.out_file, 2):
                logging.error('Dont have permissions to write in output file.')
                sys.exit()

    if conf.lift_dev:
        try:
            conf.lift_dev = float(conf.lift_dev)
        except:
            logging.error('Failed to get min lift dev value')
            sys.exit()

    if conf.lift_dump_file:
        if os.path.exists(conf.lift_dump_file):
            logging.warning('Dump file exists - overwriting.')
            if not os.access(conf.lift_dump_file, 2):
                logging.error('Dont have permissions to write in dump file.')
                sys.exit()


def _get():
    parser = argparse.ArgumentParser(description='This program, creates lift matrix basing on .vw files.')
    parser.add_argument(action='store', dest='in_file',
                                help='Input file in Vopal Wabbit input format',
                                nargs=1,
                                )

    parser.add_argument(action='store', dest='out_file',
                                help='Output file in matrix format',
                                nargs=1,
                                )

    parser.add_argument('-C', action='store', dest='lift_dev',
                                help='Min lift deviation from conversion',
                                default=None)

    parser.add_argument('-d', action='store', dest='lift_dump_file',
                                help='Output file for dumped features from -C',
                                default=None)
    
    parser.add_argument('-n', action='store', dest='namespaces',
                                help='String made of concatenated first laters of namespaces',
                                default='h')

    parser.add_argument('-c', action='store', dest='cut',
                                help='Cut top C of occurences',
                                default=250)

    parser.add_argument('-l', action='store_true', default=False,
                                dest='clog',
                                                    help='Count logarithm of value.')

   # parser.add_argument('-F', action='store_true', default=False,
   #                             dest='force_overwrite',
   #                                                 help='Overwrite output file.')
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
