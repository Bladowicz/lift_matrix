#!/usr/bin/python
# coding: utf-8
import collections
import sys
import src
import logging



def line_to_pairs(ll):
    ll, l, i, out = sorted(ll), len(ll), 0, []
    while i < l:
        for each in range(i+1, l):
            out.append((ll[i], ll[each]))
            pairs[(ll[i], ll[each])] += 1
        i+= 1
    return out

def line_to_singles(ll):
    for part in ll:
        single[part] += 1

def count_lines(inf):
    n = 0
    for l in open(config.in_file):
        n += 1
    return float(n)

def prepare_progress(total):
    total = int(total)
    def print_progress(nr):
        if nr%10000==0:
            z = 100*nr/total
            z = '#'*z
            sys.stdout.write('\r|{:98}|'.format(z))
            sys.stdout.write('\r|\033[1;37m{:98}\033[1;m|'.format(z))
            sys.stdout.flush()
    return print_progress

def prepare_line_processor(spaces):
    namespaces = set(spaces)
    def fun(line):
        all_parts = set()
        gen = (part for part in line if part[0] in namespaces)
        for part in gen:
            all_parts.update(set(part[1:].split()))
        line_to_singles(all_parts)
        line_to_pairs(all_parts)
    return fun

def check_names(nn):
    names = sorted(nn.iteritems(), reverse=True, key=lambda x: x[1])[:int(config.cut)]
    max_name_len = max((len(names[0][0]), len(names[-1][0])))
    max_count_len =  max((len(str(names[0][1])), len(str(names[-1][1]))))
    max_count_len += max_count_len/3 - 1
    logging.info('Max occurences {0:{2}} with {1:>{3},}'.format(names[0][0], names[0][1], max_name_len, max_count_len))
    logging.info('Min occurences {0:{2}} with {1:>{3},}'.format(names[-1][0], names[-1][1], max_name_len, max_count_len))
    names = map(lambda x: x[0], names)
    return sorted(names)


def probability_for_names(x, y):
    name = tuple(sorted([x, y]))
    if name[0] == name[1]:
        out = 1
    else:
        try:
            out = pairs[name]/((single[name[0]] * single[name[1]])/total)
        except KeyError:
            logging.error('Key not found')
            out = '--'
    return out

def main():
    global config, single, pairs, total
    config = src.input_parser.results
    logging.info('Starting to parsing file {}'.format(config.in_file))

    pairs = collections.Counter()
    single = collections.Counter()
    total = count_lines(config.in_file)

    logging.info('Counting occurances.')
    print_progress = prepare_progress(total)
    process_line = prepare_line_processor(config.namespaces)
    for nr, line in enumerate(open(config.in_file)):
        line = line.rstrip().split('|')
        process_line(line)
        print_progress(nr)
    sys.stdout.write('\r{:100}\r'.format(''))
    sys.stdout.flush()
    logging.info('Done counting. Triming to {0} top counts.'.format(config.cut))
    names = check_names(single)
    with open(config.out_file, 'w') as fw:
        logging.info('Writing to file {}'.format(config.out_file))
        fw.write('\t'.join(names)+'\n')
        for x in names:
            line = []
            for y in names:
                line.append(probability_for_names(x, y))
            fw.write( "\t".join(map(str, line)) + "\n")
        logging.info('Matrix saved.')


if __name__=="__main__":
    main()