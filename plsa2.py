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

def EM(params, wcounts_by_doc, eps=0.0001):
    doclens = np.array([sum(doc.values()) for doc in wcounts_by_doc])
    doclensum = np.sum(doclens)
    oldLL = None
    LLs = []
    reldiffs = []
    for it in tqdm.tqdm(itertools.count(0)):
        newLL = LL(params, wcounts_by_doc)
        if oldLL is not None:
            if newLL < oldLL:
                raise Exception("you have a bug")
            LLs.append(newLL)
            reldiff = abs((newLL - oldLL)/oldLL)
            reldiffs.append(reldiff)
            flush(it=it, LL=newLL, delta=abs(oldLL-newLL), reldelta=reldiff)
            if reldiff < eps:
                break
        oldLL = newLL
        ndocs = np.zeros_like(params.pi)
        nwords = np.zeros((V,K))
        for i, doc in enumerate(wcounts_by_doc):
            mythetaT = np.array([params.theta.T[w] for w in doc])
            mypbr = np.array([params.pbr[w] for w in doc])
            q = mythetaT * params.pi[i] * (1.-params.lam)
            q = (q.T / (np.sum(q, axis=1) + params.lam*mypbr)).T
            for j, (w, c) in enumerate(doc.iteritems()):
                nwords[w] += c*q[j]
                ndocs[i] += c*q[j]
        params.pi = ndocs / np.sum(ndocs, axis=1)[:,np.newaxis]
        params.theta = nwords.T / np.sum(nwords.T, axis=1)[:,np.newaxis]
    return params, LLs, reldiffs


def run(suffix, lam, alphamult):
    pi = stats.dirichlet.rvs(alpha=np.ones(K)*alphamult, size=N)
    theta = stats.dirichlet.rvs(alpha=np.ones(V), size=K)
    params = Params(K,N,V,lam,pi,theta,wcounts_by_doc)
    params, LLs, reldeltas = EM(params, wcounts_by_doc)
    with open("output_params.pkl", 'w') as wf:
        pickle.dump(params, wf)
    top10 = []
    for k in xrange(K):
        top10.append(np.argsort(-params.theta[k])[:10])
    top10 = map(lambda top: ' '.join(map(lambda i: winv[i], top)), top10)
    for top in top10:
        print top
    # plt.figure()
    # plt.plot(LLs)
    # plt.savefig('lls_%s.pdf' % suffix)
    # plt.figure()
    # plt.plot(reldeltas)
    # plt.savefig('reldeltas_%s.pdf' % suffix)
    return Result(params, LLs, reldeltas, top10)


result_0 = run('0', 0.9, 1.0)
# result_br = run('br', 0.3, 1.0)

# results = []
# for i in xrange(1,5):
#     results.append(run('%d' % i, 0.9, 10**i))
