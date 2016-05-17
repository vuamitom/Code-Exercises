import collections, math
class StupidBackoffLanguageModel:

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
    # TODO your code here    
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
    score = 0.0 
    for idx, w in enumerate(sentence[:(len(sentence) - 1)]):
      w2 = sentence[idx + 1]
      token = w + ' ' + w2
      count = self.bigram.get(token, 0)      
      if count > 0:        
        score += math.log(count)                
        score -= math.log(self.unigram.get(w))
      elif w2 in self.unigram:
        score += math.log(self.unigram[w2])
        score -= math.log(self.total)
      else: 
        score -= math.log(self.total + 1)
    return score
