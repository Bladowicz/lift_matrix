#!/usr/bin/python
# coding: utf-8
import logging
import collections
import sys
import src
import math


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
    for l in open(inf):
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
        if line[0][0] == '1': all_parts.add('con_1')
        gen = (part for part in line if part[0] in namespaces)
        for part in gen:
            all_parts.update(set(part[1:].split()))
        line_to_singles(all_parts)
        line_to_pairs(all_parts)
    return fun

def check_names(nn, cut):
    names = sorted(nn.iteritems(), reverse=True, key=lambda x: x[1])[:int(cut)]
    try:
        max_name_len = max((len(names[0][0]), len(names[-1][0])))
    except IndexError:
        logging.error('List of good features is empty.')
        sys.exit()
    max_count_len =  max((len(str(names[0][1])), len(str(names[-1][1]))))
    max_count_len += max_count_len/3 - 1
    logging.info('Max occurences {0:{2}} with {1:>{3},}'.format(names[0][0], names[0][1], max_name_len, max_count_len))
    logging.info('Min occurences {0:{2}} with {1:>{3},}'.format(names[-1][0], names[-1][1], max_name_len, max_count_len))
    names = map(lambda x: x[0], names)
    return sorted(names)

def prepare_prob_for_names(use_log):
    def probability_for_names(x, y):
        name = tuple(sorted([x, y]))
        if name[0] == name[1]:
            out = 1
        else:
            try:
                if not use_log:
                    out = pairs[name]/((single[name[0]] * single[name[1]])/total)
                else:
                    out = math.log(1/(pairs[name]/((single[name[0]] * single[name[1]])/total) + 0.01))
            except KeyError:
                logging.error('Key not found')
                out = '--'
            except ZeroDivisionError:
                logging.error('Zero dividead x:{} y:{}\n s1:{}\n s2:{}\n t:{}'.format(
                    x, y, single[name[0]], single[name[1]], total ))
        if x == 'con_1':
            logging.debug('Count x:{} y:{}\n s1:{}\n s2:{}\n t:{}\n result: {}'.format(
                x, y, single[name[0]], single[name[1]], total, out ))
        return out
    return probability_for_names

def remove_features(names, dev, probability, fw):
    bad_names = set()
    t = set(names)
    for y in t:
        if abs(1 - probability('con_1', y)) < fw:
            bad_names.add(y)
    for e in bad_names:
        names.remove(e)

    names.insert(0, 'con_1')
    logging.info('Features that were insignificant {}'.format(len(bad_names)))
    if fw:
        logging.info('Writing down insignificant feature to "{}"'.format(fw))
        with open(fw, 'w') as fw:
            for line in bad_names:
                fw.write(line + '\n')

def make_matrix(in_file, out_file, namespaces='h', cut=250, clog=False, lift_dev=None, lift_dump_file=None):
    global single, pairs, total
    logging.info('Starting to parsing file {}'.format(in_file))

    pairs = collections.Counter()
    single = collections.Counter()
    total = count_lines(in_file)
    logging.info('Counting occurances.')
    print_progress = prepare_progress(total)
    process_line = prepare_line_processor(namespaces)
    for nr, line in enumerate(open(in_file)):
        line = line.rstrip().split('|')
        process_line(line)
        print_progress(nr)
    sys.stdout.write('\r{:100}\r'.format(''))
    sys.stdout.flush()
    logging.info('Done counting. Triming to {0} top counts.'.format(cut))
    names = check_names(single, cut)
    probability_for_names = prepare_prob_for_names(clog)
    if lift_dev:
        remove_features(names, lift_dev, probability_for_names, lift_dump_file)
    with open(out_file, 'w') as fw:
        logging.info('Writing to file {}'.format(out_file))
        #fw.write('\t'.join(names)+'\n')
        #fw.write('\t'.join([str(single[name]) for name in names])+'\n')
        for x in names:
            line = []
            line.append(x)
            line.append(single[x])
            for y in names:
                line.append(probability_for_names(x, y))
            fw.write( "\t".join(map(str, line)) + "\n")
        logging.info('Matrix saved.')


def main():
    global config, single, pairs, total
    config = src.input_parser._get()

    in_file = config.in_file
    namespaces = config.namespaces
    cut = config.cut
    clog = config.clog
    lift_dev = config.lift_dev
    out_file = config.out_file

    ## DO IT!!!
    make_matrix(in_file, out_file, namespaces, cut, clog, lift_dev, )


if __name__=="__main__":
    main()
