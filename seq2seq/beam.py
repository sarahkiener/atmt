import torch

from itertools import count
from queue import PriorityQueue


class BeamSearch(object):
    """ Defines a beam search object for a single input sentence. """
    def __init__(self, beam_size, max_len, pad):

        self.beam_size = beam_size
        self.max_len = max_len
        self.pad = pad

        self.nodes = PriorityQueue() # beams to be expanded
        self.final = PriorityQueue() # beams that ended in EOS

        self._counter = count() # for correct ordering of nodes with same score

    def add(self, score, node):
        """ Adds a new beam search node to the queue of current nodes """
        self.nodes.put((score, next(self._counter), node))

    def add_final(self, score, node):
        """ Adds a beam search path that ended in EOS (= finished sentence) """
        # ensure all node paths have the same length for batch ops
        missing = self.max_len - node.length
        node.sequence = torch.cat((node.sequence.cpu(), torch.tensor([self.pad]*missing).long()))
        self.final.put((score, next(self._counter), node))

    def get_current_beams(self):
        """ Returns beam_size current nodes with the lowest negative log probability """
        nodes = []
        while not self.nodes.empty() and len(nodes) < self.beam_size:
            node = self.nodes.get()
            nodes.append((node[0], node[2]))
        return nodes

    def get_best(self, n_best):
        """ Returns final node with the lowest negative log probability """
        # Merge EOS paths and those that were stopped by
        # max sequence length (still in nodes)
        # n_best: n-best translations to be returned
        merged = PriorityQueue()
        for _ in range(self.final.qsize()):
            node = self.final.get()
            merged.put(node)

        for _ in range(self.nodes.qsize()):
            node = self.nodes.get()
            merged.put(node)

        # for task 3:
        # node = merged.get()
        # node = (node[0], node[2]) 
        # return node

        # for task 4: return n-best nodes in a list
        n_best_list = []
        for i in range(n_best):
        	node = merged.get()
        	node = (node[0], node[2])
        	n_best_list.append(node)
        return n_best_list


    def prune(self):
        """ Removes all nodes but the beam_size best ones (lowest neg log prob) """
        nodes = PriorityQueue()
        # Keep track of how many search paths are already finished (EOS)
        finished = self.final.qsize()
        for _ in range(self.beam_size-finished):
            node = self.nodes.get()
            nodes.put(node)
        self.nodes = nodes


class BeamSearchNode(object):
    """ Defines a search node and stores values important for computation of beam search path"""
    def __init__(self, search, emb, lstm_out, final_hidden, final_cell, mask, sequence, logProb, length):

        # Attributes needed for computation of decoder states
        self.sequence = sequence
        self.emb = emb
        self.lstm_out = lstm_out
        self.final_hidden = final_hidden
        self.final_cell = final_cell
        self.mask = mask

        # Attributes needed for computation of sequence score
        self.logp = logProb
        self.length = length

        self.search = search

    def eval(self, alpha, gamma, rank):
        """ Returns score of sequence up to this node """

        # implement length normalization
        lp = ((5 + self.length)**alpha) / ((5 + 1)**alpha)

        # for task 3:
        # return self.logp / lp

        # for task 4: implement re-ranking
        return self.logp / lp - gamma * rank