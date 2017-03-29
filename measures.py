# built in library
from math import sqrt

# own
from util import boolean_arrays, normalized_vectors


labels = {
    "euclidian_dist": "Ecuclidian distance",
    "cos_coeff": "Cosine's coefficient",
    "vector_coeff": "Vectorial coefficient",
    "dice_coeff": "Dice coefficient",
    "jaccard_coeff": "Jaccard coefficient",
    "overlap_coeff": "Overlap coefficient",
    "hamming_dist": "Hamming distance",
    "boolean_dist": "Boolean coefficient",
    "tanimoto_dist": "Tanimoto distance",
    "similarities": "Similarities",
    "dissimilarities": "Dissimilarities",
}


"""
Numbers
"""


def similarities(P, Q):
    if type(P) == set:
        P, Q = boolean_arrays(P, Q)
    s = 0
    for p, q in zip(P, Q):
        s += int(p == q)
    return s


def dissimilarities(P, Q):
    if type(P) == set:
        P, Q = boolean_arrays(P, Q)
    s = 0
    for p, q in zip(P, Q):
        s += int(p != q)
    return s


def euclidian_dist(P, Q):
    """ Dissimilarity """
    P, Q = normalized_vectors(P, Q)
    return 1.0 * sqrt(
        sum((p - q) ** 2 for p, q in zip(P, Q))
    )


def cos_coeff(P, Q):
    """ Similarity """
    P, Q = normalized_vectors(P, Q)
    squares_sum_P = sum(p ** 2 for p in P)
    squares_sum_Q = sum(q ** 2 for q in Q)
    product_sum = sum(p * q for p, q in zip(P, Q))
    try:
        return 1.0 * product_sum / sqrt(squares_sum_P * squares_sum_Q)
    except:
        pass


def vector_coeff(P, Q):
    """ Similarity """
    P, Q = normalized_vectors(P, Q)
    return 1.0 * sum(p * q for p, q in zip(P, Q))


"""
Set theory
"""


def dice_coeff(Q, D):
    """ Similarity """
    Q, D = set(Q), set(D)
    try:
        return 2.0 * len(Q & D) / (len(Q) + len(D))
    except:
        pass


def jaccard_coeff(Q, D):
    """ Similarity """
    Q, D = set(Q), set(D)
    try:
        return 1.0 * len(Q & D) / len(Q | D)
    except:
        pass


def overlap_coeff(Q, D):
    """ Similarity """
    Q, D = set(Q), set(D)
    try:
        return 1.0 * len(Q & D) / min(len(Q), len(D))
    except:
        pass


def hamming_dist(Q, D):
    """ Dissimilarity """
    Q, D = set(Q), set(D)
    try:
        return 1.0 * len(Q - D) / len(Q), 1.0 * len(D - Q) / len(D)
    except:
        pass


def boolean_dist(Q, D):
    """ Similarity """
    Q, D = set(Q), set(D)
    try:
        return 1.0 * sqrt(len(Q & D))
    except:
        pass


def tanimoto_dist(Q, D):
    """ Dissimilarity """
    Q, D = set(Q), set(D)
    num = len(Q) + len(D) - 2 * len(Q & D)
    den = len(Q) + len(D) - len(Q & D)
    try:
        return num / den
    except:
        pass


if __name__ == '__main__':
    print("--- Test ---")
    a1 = [1, 1, 1, 0]
    a2 = [1, 1, 0, 1]
    s1 = {'a', 'p', 's', 'i'}
    s2 = {'a', 'p'}
    print("similarities:", similarities(s1, s2))
    print("dissimilarities:", dissimilarities(s1, s2))
    print("euclidian:", euclidian_dist(a1, a2))
    print("cosine:", cos_coeff(a1, a2))
    print("vector:", vector_coeff(a1, a2))
    print("dice:", dice_coeff(s1, s2))
    print("jaccard:", jaccard_coeff(s1, s2))
    print("overlap:", overlap_coeff(s1, s2))
    print("hamming:", hamming_dist(s1, s2))
    print("boolean:", boolean_dist(s1, s2))
