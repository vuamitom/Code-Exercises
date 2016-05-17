import math, collections

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.bigram = collections.defaultdict(lambda: 0)
    self.unigram = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for idx, datum in enumerate(sentence.data):
        if idx < len(sentence.data) - 1:  
          token = datum.word + ' ' + sentence.data[idx + 1].word
          count = self.bigram.get(token, 0)
          self.bigram[token] = count + 1
        count = self.unigram.get(datum.word, 0)
        self.unigram[datum.word] = count + 1
        self.total += 1 

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    # TODO your code here
    # TODO your code here
    score = 0.0 
    for idx, w in enumerate(sentence[:(len(sentence) - 1)]):
      w2 = sentence[idx + 1]
      token = w + ' ' + w2
      count = self.bigram.get(token, 0)      
      p1 = count / (self.unigram.get(w) * 1.0) if count > 0 else 0       
      p2 = self.unigram[w2] / (1.0 * self.total)
      p = 0.6 * p1  +  0.4 * p2
      if p > 0.000000000001: 
        score += math.log(p)
      else:
        score -= math.log(self.total)                   
    return score
