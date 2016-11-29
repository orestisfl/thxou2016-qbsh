#!/usr/bin/env python3
import logging
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

import pitch_vectors


def main(args):
    options = _parse_args(args[1:])
    logging.debug("Got options: %s.", str(options))
    ground_truth = _pickle_load(options.database)
    queries = _init_queries(options)
    assert queries is not None, "queries couldn't be initialized."
    logging.debug("Got a ground truth of size %d and %d queries.", len(ground_truth), len(queries))

    for query, pitch_vector in queries.items():
        logging.debug("Processing query: %s with a pitch vector of size %d.", query, len(pitch_vector))
        scores = options.method.search_func(pitch_vector, ground_truth)
        best = min(scores, key=scores.get)
        print(query, '==', best, 'with', scores[best], 'distance')
        print(scores)

    return 0


def _init_queries(options):
    if options.pickle:
        queries = {idx: _pickle_load(options.query_database)[idx] for idx in options.query}
    elif options.wav:
        queries = {idx: pitch_vectors.pitch_vector_from_wav(idx) for idx in options.query}
    elif options.pitch_file:
        queries = {idx: pitch_vectors.load_pitch_vector(idx) for idx in options.query}
    elif options.pickle_whole:
        queries = {}
        for database in options.query:
            queries.update(_pickle_load(database))
    if options.normalize:
        for idx, pv in queries.items():
            queries[idx] = pitch_vectors.normalize(pv)
    return queries


def _pickle_load(filename):
    with open(filename, 'rb') as file_obj:
        return pickle.load(file_obj)


def _parse_args(args):
    import argparse
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument("query", type=str, nargs='+')
    parser.add_argument(
        "--method", "-m",
        metavar="METHOD",
        type=str,
        default=SEARCH_METHODS_NAMES[0],
        choices=SEARCH_METHODS_NAMES,
        help="Search method to be used."
    )
    parser.add_argument(
        "--database", "-d",
        metavar="PICKLE FILE",
        type=str,
        default="database-midi-extract.pickle",
        help="Pickle database to be used for query matching."
    )
    parser.add_argument("--wav", action="store_true", default=False, help="Query is a .wav file")
    parser.add_argument("--pitch-file", action="store_true", default=False, help="Query is a .pv file")
    parser.add_argument(
        "--pickle",
        action="store_true",
        default=False,
        help="Query is from a pickle database. Positional arguments are used as indices."
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        default=False,
        help="Normalize query pitch vector."
    )
    parser.add_argument(
        "--pickle-whole",
        action="store_true",
        default=False,
        help="Query is the entirety of pickle databases. Positional arguments are the pickle databases to be processed."
    )
    parser.add_argument(
        "--query-database", "-q",
        metavar="PICKLE FILE",
        type=str,
        default=None,
        help="Pickle database to be used for query input. Implies '--pickle'."
    )
    options = parser.parse_args(args)

    # Validate
    if options.query_database is not None:
        options.pickle = True
    elif options.pickle:
        options.query_database = PICKLE_QUERY_DEFAULT

    actions = [options.pickle, options.wav, options.pitch_file, options.pickle_whole]
    if sum(actions) == 0:
        options.wav = True
    elif sum(actions) > 1:
        parser.error("Only one of the following can be used at each time: --wav, --pitch-file, --pickle, --pickle-whole")

    method_idx = SEARCH_METHODS_NAMES.index(options.method)
    options.method = SEARCH_METHODS[method_idx]

    return options


def dtw(x, y):
    x, y = make_same_length(x, y)
    distance, _ = fastdtw(x, y, dist=euclidean)
    return distance


def make_same_length(x, y):
    lenx = len(x)
    leny = len(y)
    if lenx > leny:
        return x[:leny], y
    elif leny > lenx:
        return x, y[:lenx]
    else:
        return x, y


def iterative_search(compare_func, **kwargs):
    def search_function(query, ground_truth):
        scores = {idx: compare_func(query, pv, **kwargs) for idx, pv in ground_truth.items()}
        return scores
    return search_function


if __name__ == '__main__':
    import sys
    import pickle
    from collections import namedtuple
    logging.basicConfig(level=logging.DEBUG)
    QUERY_TYPES = ["wav, pickle", "pv"]
    PICKLE_QUERY_DEFAULT = 'database-wav-extract.pickle'
    SearchMethod = namedtuple("SearchMethod", ["name", "search_func"])
    SEARCH_METHODS = (
        SearchMethod("dtw", iterative_search(dtw)),
    )
    SEARCH_METHODS_NAMES = tuple(x.name for x in SEARCH_METHODS)
    sys.exit(main(sys.argv))
