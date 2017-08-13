import json
import pickle

class TestTree:
  def __init__(self):
    self.loadDict()

  def loadDict(self):
    with open('d3/tree.json') as data_file:    
      self.tree = pickle.load( open( "tree.p", "rb" ) )
  
  def testBranching(self):
    def checkHeights(words):
      heights = []
      minH, maxH = -1, -1
      for word in words:
        height = 0
        for num in word:
          height += int(num)
        if minH == -1 or minH > height:
          minH = height
        if maxH == -1 or maxH < height:
          maxH = height
        heights.append(height)
      if len(words[0]) == len(words) -1:
        if maxH - minH > 1:
          print "Balance Violatino"
      else:
        print "Complexity violation"
    def branchCrawl(group):
      checkHeights(group['words'])
      if 'children' in group:
        for child in group['children']:
          branchCrawl(child)
    branchCrawl(self.tree)

t = TestTree()
t.testBranching()