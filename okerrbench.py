#!/usr/bin/python3

import argparse
import okerrupdate
import time
import os
import random
from multiprocessing import Process, Queue
import logging
import json

def bench(q, p, n, args):
    # print("<{} ({})> started".format(n, os.getpid()))
    # time.sleep(10)
    # print("<{} ({})> stopped".format(n, os.getpid()))

    stats = {'OK': 0, 'n': n, 'requests_exception': 0}

    processed = 0
    numexc = 0
    stop = False
    started = time.time()
    if args.shard:
        startn = args.indicators * n
        stopn = startn + args.indicators
    else:
        startn = 0
        stopn = args.indicators

    while not stop:
        i = random.randrange(startn, stopn)
        i = p.indicator('bench:{}'.format(i))
        try:
            i.update('OK', 'benchmark')
            stats['OK'] += 1
        except okerrupdate.OkerrExc as e:
            if e.requests_exception:
                stats['requests_exception'] += 1

            elif e.requests_response:
                tag = "code:{}".format(e.requests_response.status_code)
                if tag in stats:
                    stats[tag] += 1
                else:
                    stats[tag] = 1

            elif e.args[0] in stats:
                stats[e.args[0]] += 1
            else:
                stats[e.args[0]] = 1

            if not args.quiet:
                print(e)
            numexc += 1

        processed += 1
        passed = time.time() - started

        # stop?
        if args.tries:
            if processed >= args.tries:
                stop = True
        else:
            if passed > args.seconds:
                stop = True

    passed = time.time() - started
    stats['passed'] = passed
    stats['processed'] = processed
    # print("Process {} processed {} indicators in {:.2f} sec ({:.2f} i/sec). Exceptions: {}".format(
    #    n, processed, passed, processed/passed, numexc
    # ))
    q.put(stats)
    # print(json.dumps(stats, indent=4))

def prepare(p, args):
    started = time.time()
    for n in range(args.indicators):
        i = p.indicator('bench:{}'.format(n))
        i.update('OK', 'prepare')

    passed = time.time() - started

    print("Prepared {} indicators in {:.2f} seconds ({:.2f} i/sec)".format(
        args.indicators, passed,
        args.indicators / passed))


def main():
    parser = argparse.ArgumentParser(description='okerr benchmark')

    g = parser.add_argument_group('Commands')
    g.add_argument('--prepare', action='store_true', help='Create indicators')
    g.add_argument('--test', action='store_true', help='Run test')

    g = parser.add_argument_group('Test project')
    g.add_argument('--url', help='Server URL e.g. https://alpha.okerr.com/')
    g.add_argument('--textid', '-i', metavar='TEXTID', help='Project TextID')
    g.add_argument('--secret', '-S', metavar='SECRET', help='Project secret')

    g = parser.add_argument_group('Test parameters')
    g.add_argument('--indicators', metavar='N', default=100, type=int, help='Run tests across N indicators per process')
    g.add_argument('--process', metavar='N', default=5, type=int, help='Run tests across N processes')
    g.add_argument('--shard', action='store_true', default=False,
                   help='Each process will use next shard of --indicators')
    g.add_argument('--quiet', '-q', action='store_true', default=False,
                   help='quiet mode')

    g = parser.add_argument_group('Test duration')
    g.add_argument('--tries', metavar='N', type=int, help='Each process will make N tries')
    g.add_argument('--seconds', metavar='SECONDS', type=int, default=30, help='Each process will run for SECONDS seconds')

    args = parser.parse_args()

    print("Using okerrupdate version:", okerrupdate.__version__)
    project = okerrupdate.OkerrProject(textid=args.textid, url=args.url, direct=True, secret=args.secret)
    print(project, args.textid, project.textid)
    if args.quiet:
        project.log.setLevel(logging.ERROR)

    if args.prepare:
        print("Prepare")
        prepare(project, args)
    elif args.test:
        print("Test")
        jobs = list()
        q = Queue()
        start = time.time()
        for n in range(args.process):
            p = Process(target=bench, args=(q, project, n, args))
            p.start()
            jobs.append(p)
            # p.join()

        print("wait to stop...")
        for p in jobs:
            p.join()

        passed = time.time() - start
        sum = {
            'OK': 0,
            'requests_exception': 0,
            'processed': 0
        }
        while not q.empty():
            s = q.get()
            if not args.quiet:
                print(s)
            for k, v in s.items():
                if k in sum:
                    sum[k] += v

        sum['passed'] = "{:.3f} sec".format(passed)
        sum['failed'] = sum['processed'] - sum['OK']
        sum['processed_rate'] = "{:.3f} req/sec".format(sum['processed'] / passed)
        sum['OK_rate'] = "{:.3f} req/sec".format(sum['OK'] / passed)

        print("Statistics:\n---")
        for k, v in sum.items():
            print("{}: {}".format(k,v))
        print()

    else:
        print("Need --prepare or --test")


main()

