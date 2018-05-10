#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from collections import Counter
import itertools
import tqdm
import seaborn as sns
import pickle
from lowercase_tok import tokens_lowercase


dataset = sys.argv[1]
with open(dataset) as f:
    abstracts = f.read().strip().split('\n')


wdict = {}
wcounts_by_doc = [Counter() for ab in abstracts]
for i, ab in enumerate(abstracts):
    for w in ab.strip().split():
        if w not in wdict:
            wdict[w] = len(wdict)
        wcounts_by_doc[i][wdict[w]] += 1


winv = [0]*len(wdict)
for w, i in wdict.iteritems():
    winv[i] = w

K = 20
lam = 0.9
N = len(abstracts)
V = len(wdict)


class Params(object):
    def __init__(self, K, N, V, lam, pi, theta, wcounts_by_doc):
        self.K=K
        self.N=N
        self.V=V
        self.lam=lam
        self.pi=pi
        self.theta=theta
        self.pbr = np.zeros(V)
        for wcounts in wcounts_by_doc:
            for w, c in wcounts.iteritems():
                self.pbr[w] += c
        self.pbr /= np.sum(self.pbr)

class Result(object):
    def __init__(self, params, LLs, reldeltas, top10):
        self.params = params
        self.LLs = LLs
        self.reldeltas = reldeltas
        self.top10 = top10

def LL(params, wcounts_by_doc):
    ret = 0.
    for i in xrange(params.N):
        for w, c in wcounts_by_doc[i].iteritems():
            ret += c*np.log(params.lam*params.pbr[w] + (1.-params.lam)*params.pi[i].dot(params.theta.T[w]))
    return ret

def flush(**kwargs):
    s = ''
    first=True
    for k, v in kwargs.iteritems():
        if first:
            s += "%s=%s" % (k, v)
        else:
            s += ", %s=%s" % (k, v)
        first=False
    print s
    sys.stdout.flush()

def search (query, params, wdict, topk):
    # Unicode decode
    # For each w in query
    topics = []
    query_tok = tokens_lowercase(query)
    for w in query_tok.split(" "):
        w_idx = wdict[w]
        topics.append(params.theta[:,w_idx])
        # theta: w -> vector of the topics for w
        # argmax ?? among topics
    max_topic = np.argmax(np.mean(topics, axis = 0))
    # max_topic = np.argsort(-params.theta[])[0]
    # print (np.mean(topics, axis = 0))
    print (max_topic)
    #topk docs in PI (doc -> topic)
    return np.argsort(-params.pi[:,max_topic])[:topk]

def run(suffix, lam, alphamult):
    pi = stats.dirichlet.rvs(alpha=np.ones(K)*alphamult, size=N)
    theta = stats.dirichlet.rvs(alpha=np.ones(V), size=K)
    # params = Params(K,N,V,lam,pi,theta,wcounts_by_doc)
    # params, LLs, reldeltas = EM(params, wcounts_by_doc)
    with open("output_params.pkl", 'r') as rf:
        params = pickle.load(rf)
    top10 = []
    for k in xrange(K):
        top10.append(np.argsort(-params.theta[k])[:10])
    top10 = map(lambda top: ' '.join(map(lambda i: winv[i], top)), top10)
    for top in top10:
        print top
    return params
    # plt.figure()
    # plt.plot(LLs)
    # plt.savefig('lls_%s.pdf' % suffix)
    # plt.figure()
    # plt.plot(reldeltas)
    # plt.savefig('reldeltas_%s.pdf' % suffix)
    # return Result(params, LLs, reldeltas, top10)

query = sys.argv[2]
result_0_params = run('0', 0.9, 1.0)
relevant_doc_indices = (search(query, result_0_params, wdict, K))
# print(relevant_doc_indices)
if len(sys.argv) > 3:
    title_file = sys.argv[3]
    with open(title_file, 'r') as tf:
        titles = tf.readlines()
        # print(len(titles))
        for index in relevant_doc_indices:
            print(titles[index])
else:
    print(relevant_doc_indices)
# result_br = run('br', 0.3, 1.0)

# results = []
# for i in xrange(1,5):
#     results.append(run('%d' % i, 0.9, 10**i))
