"""
Math side of things.

:author: 2013, Pascal Hartig <phartig@rdrei.net>
:license: BSD
"""

import itertools
from numpy.core.multiarray import array
from numpy.linalg.linalg import pinv


def extract_teams(results):
    teams = set(itertools.chain.from_iterable((x['teamHome'], x['teamAway'])
                                              for x in results))
    return dict(zip(teams, xrange(len(teams))))


def build_selection_matrix(results, teams):
    matrix = []

    for result in results:
        index_a, index_b = teams[result['teamHome']], teams[result['teamAway']]
        line = [0] * len(teams)
        line[index_a] = 1
        line[index_b] = -1

        matrix.append(line)

    return array(matrix)


def build_result_vector(results):
    return array([int(x['goalsHome']) - int(x['goalsAway']) for x in results])


def map_scores_to_teams(scores, teams):
    inv_teams = {v: k for k, v in teams.items()}

    return {inv_teams[i]: value for (i, value) in enumerate(scores)}


def calculate_errors(score_vector, result_vector, selection_matrix):
    return result_vector.T - selection_matrix.dot(score_vector)


def calculate_scores(results):
    teams = extract_teams(results)
    selection_matrix = build_selection_matrix(results, teams)
    result_vector = build_result_vector(results)

    score_vector = pinv(selection_matrix).dot(result_vector.T)
    error_vector = calculate_errors(score_vector, result_vector,
                                    selection_matrix)

    return map_scores_to_teams(score_vector, teams), error_vector
