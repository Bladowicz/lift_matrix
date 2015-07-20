import argparse


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

    #parser.add_argument('-s', action='store', dest='simple_value',
    #                            help='Store a simple value')
    #
    #parser.add_argument('-c', action='store_const', dest='constant_value',
    #                            const='value-to-store',
    #                                                help='Store a constant value')
    #
    #parser.add_argument('-t', action='store_true', default=False,
    #                            dest='boolean_switch',
    #                                                help='Set a switch to true')
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
    return parser.parse_args()
results = _get()
