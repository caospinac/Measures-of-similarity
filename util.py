# built in library
import re
import unicodedata as ucd

# external libraries
import pandas as pd
from nltk.corpus import stopwords as sw

# own
import measures as ms


def std_zipper(P, Q):
    P, Q = sorted(list(P)), sorted(list(Q))
    for i in range(min(len(P), len(Q))):
        yield (P[i], Q[i])


def remove_accents(string):
    return ''.join(
        c for c in ucd.normalize('NFD', string)
        if ucd.category(c) != 'Mn')


def assume_zeros(Q, D):
    if type(Q) == set:
        return Q, D
    ql, dl = len(Q), len(D)
    if ql > dl:
        D += [0] * (ql - dl)
    else:
        Q += [0] * (dl - ql)
    return Q, D


def filter_sw(list_value):
    values = [remove_accents(value) for value in list_value]
    return list(filter(lambda x: x not in sw.words('spanish'), values))


def word_set(value):
    words = [s.lower() for s in re.findall('\w{3,}', value)]
    return set(filter_sw(words))


def num_list(string):
    return [
        eval(num)
        for num in re.findall(r"[+-]?\d*\.?\d+", string)
    ]


def token_list(value):
    return num_list(value) + list(word_set(value))


def to_dict(names, values):
    return dict(zip(names, values))


def df_to_dic(df):
    mat = [list(row) for row in df.as_matrix()]
    dic = dict()
    for row in mat:
        dic.update({'{}'.format(row[0]): row[1:]})
    return dic


def matrix(n, default=None):
    return [[default] * n for x in range(n)]


def read_excel_from_request(body):
    with open("/tmp/file.xlsx", "wb") as f:
        f.write(body)
    xls = pd.read_excel("/tmp/file.xlsx")
    return xls.values.tolist()


def implement(func_name):
    if func_name == 'euclidian_dist':
        return ms.euclidian_dist
    elif func_name == 'cos_coeff':
        return ms.cos_coeff
    elif func_name == 'vector_coeff':
        return ms.vector_coeff
    elif func_name == 'dice_coeff':
        return ms.dice_coeff
    elif func_name == 'jaccard_coeff':
        return ms.jaccard_coeff
    elif func_name == 'overlap_coeff':
        return ms.overlap_coeff
    elif func_name == 'hamming_dist':
        return ms.hamming_dist
    elif func_name == 'boolean_dist':
        return ms.boolean_dist
    elif func_name == 'tanimoto_dist':
        return ms.tanimoto_dist
    elif func_name == 'similarities':
        return ms.similarities
    elif func_name == 'dissimilarities':
        return ms.dissimilarities


def similarity_matrix(data, function):

    for k in data:
        data[k] = token_list(data[k].__str__())

    mat = matrix(len(data))
    for i, k in enumerate(data):
        for j, l in enumerate(data):
            mat[i][j] = round(function(data[k], data[l]), 2)
    return mat


def do(data, measure):
    return similarity_matrix(
        data, implement(measure)
    )


def boolean_arrays(Q, D):
    U = Q | D
    Qa = []
    Da = []
    for u in U:
        Qa.append(int(u in Q))
        Da.append(int(u in D))
    return Qa, Da


def str_part(listx):
    return list(filter(lambda x: type(x) == str, listx))


def normalized_vectors(P, Q):
    strl_P, strl_Q = str_part(P), str_part(Q)
    P, Q = [p for p in P if p not in strl_P], [q for q in Q if q not in strl_Q]
    strl_P, strl_Q = boolean_arrays(set(strl_P), set(strl_Q))
    P, Q = assume_zeros(P + strl_P, Q + strl_Q)
    return P, Q


if __name__ == '__main__':
    print("--- Test ---")
    s1 = {'a', 'p', 's', 'i'}
    s2 = {'a', 'p'}
    print(boolean_arrays(s1, s2))
    print(remove_accents("árbol"))
    print(list(filter_sw(list(s1))))
