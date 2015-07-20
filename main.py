#!/usr/bin/python
# coding: utf-8
import collections
import sys
import src
import logging



def list_to_pairs(ll):
    l = len(ll)
    i = 0
    out = []
    while i < l:
        for each in range(i+1, l):
            out.append((ll[i], ll[each]))
            all[(ll[i], ll[each])] += 1
        i+= 1
    return out

def list_to_single(ll):
    for part in ll:
        single[part] += 1

def count_lines(inf):
    n = 0
    for l in open(config.in_file):
        n += 1
    return float(n)

def prepare_progress(total):
    total = int(total)
    def print_progress(line):
        if nr%10000==0:
            z = 100*nr/total
            z = '#'*z
            sys.stdout.write('\r|{:98}|'.format(z))
            sys.stdout.flush()
    return print_progress

def process_line(line):
    for part in line:
        if part[0] in namespaces:
            list_to_pairs(part)
            list_to_singles(part)

if __name__=="__main__":
    config = src.input_parser.results
    logging.info('Starting to parsing file {}'.format(config.in_file))

    all = collections.Counter()
    single = collections.Counter()
    total = count_lines(config.in_file)

    logging.info('Counting occurances.')
    print_progress = prepare_progress(total)
    for nr, line in enumerate(open(config.in_file)):
        line = line.rstrip().split('|')
        process_line(part)
        for part in line:
            if part[0] == 'h':
                part = part.split()[1:]
                list_to_pairs(part)
                for each in part:
                    single[each] += 1
        print_progress(nr)
    print ''
    logging.info('Done counting. Triming to {0} top counts.'.format(config.cut))
    names = sorted(single.iteritems(), reverse=True, key=lambda x: x[1])[:int(config.cut)]
    names = map(lambda x: x[0], names)
    names = sorted(names)
    with open('cluster.out', 'w') as fw:
        for x in names:
            line = []
            for y in names:
                name = tuple(sorted([x, y]))
                if name[0] == name[1]:
                    out = 1
                else:
                    try:
                        out = all[name]/((single[name[0]] * single[name[1]])/total)
                    except KeyError:
                        out = '--'
                line.append(out)
            fw.write( "\t".join(map(str, line)) + "\n")
