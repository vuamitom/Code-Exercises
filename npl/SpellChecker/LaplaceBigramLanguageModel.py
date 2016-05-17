import math, collections

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here    
    self.bigram = None    
    self.train(corpus)    

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """    
    self.vocal = set([w.word for sentence in corpus.corpus for w in sentence.data])       
    self.bigram = {(s1 + ' ' + s2):1 for s1 in self.vocal for s2 in self.vocal}
    self.cache = {s:len(self.vocal) for s in self.vocal}
    # TODO your code here
    for sentence in corpus.corpus:
      for idx, datum in enumerate(sentence.data[:(len(sentence.data)-1)]):  
        token = datum.word + ' ' + sentence.data[idx + 1].word
        self.bigram[token] = self.bigram[token] + 1
        self.cache[datum.word] += 1 

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here 
    score = 0.0 
    for idx, w in enumerate(sentence[:(len(sentence) - 1)]):
      token = w + ' ' + sentence[idx + 1]
      count = self.bigram.get(token, 0)      
      if count > 0:        
        score += math.log(count)        
        total = self.cache[w]
        score -= math.log(total)
      else:
        if w in self.vocal:            
          total = self.cache[w]
          score -= math.log(total)
        else:
          score -= math.log(len(self.vocal))                   
    return score
