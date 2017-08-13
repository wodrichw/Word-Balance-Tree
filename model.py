import csv
import json
import pyrebase
import pickle

config = {
  "apiKey":  "AIzaSyC2Kkg_j7Z4f7cKGLG9qFrz5Q4VTq8oTqo",
  "authDomain": "balancetrees-83f7a.firebaseapp.com",
  "databaseURL": "https://balancetrees-83f7a.firebaseio.com",
  "storageBucket": "balancetrees-83f7a.appspot.com",
}
firebase = pyrebase.initialize_app(config)

class WordTable:
  def __init__(self, size, type):
    if type == 'half':
      self.table = [[WordGroup(['00','01', '10'], ['11'])]]
    else:
      self.table = [[WordGroup(['0', '1'], [])]]
    for i in range(1, size):
      self.table.append([])
      for group in self.table[i-1]:
        tempColumn = WordColumn(group.words, group.rules)
        self.table[i] += tempColumn.groups
  def numVomit(self):
    for i in self.table:
      for group in i:
        print "w ", group.words
        print "r ", group.rules
  def writeCSV(self):
    with open('wordTable.csv', 'wb') as csvfile:
      tableWrite = csv.writer(csvfile, delimiter=',')
      for i in self.table:
        tempColumn = []
        for group in i:
          words = 'Words: '
          rules = 'Rules: '
          for word in group.words:
            words += word + ' '
          for rule in group.rules:
            rules += rule + ' '
          tempColumn.append(words + rules)
        tableWrite.writerow(tempColumn)

  def writeJson(self):
    dictTable = {'rows':[]}
    for row in self.table:
      dictGroups = {'groups': []}
      for group in row:
        dictGroup = {'words': [], 'rules': []}
        for word in group.words:
          dictGroup['words'].append(word)
        for rule in group.rules:
          dictGroup['rules'].append(rule)
        dictGroups['groups'].append(dictGroup)
      dictTable['rows'].append(dictGroups)

    with open('webModel/src/assets/table.json', 'w') as outfile:
      json.dump(dictTable, outfile)

class WordTree:
  def __init__(self, size):
    self.tree = {'tree': {'words': ["0", "1"], 'rules': []}}
    self.wcol = []
    self.tree = self.generateGroups(self.tree['tree'], size)
  
  def generateGroups(self, group, size):
    self.wcol.append(WordColumn(group['words'], group['rules']))
    group['children'] = []
    if len(group['words'][0]) < size:
      children = []
      for child in self.wcol[-1].children:
        childgroup = self.generateGroups(child, size)
        children.append(childgroup)
      group['children'] = children
    else: 
      group['children'] = self.wcol[-1].children
    return group

  def writeFire(self):
    db = firebase.database()
    db.child("tree").set(self.tree)
    
  def writeJson(self):
    with open('webModel/src/assets/d3/tree.json', 'w') as outfile:
      json.dump([self.tree], outfile)

  def writePickle(self):
    pickle.dump( self.tree, open( "tree.p", "wb" ) )

  def numVomit(self):
    def numRecurse(self, group):
      print "words", group['words']
      print "rules", group['rules']
      print "children"
      for child in group['children']:
        print "Words", child['words']
        print "rules", child['rules']
      numRecurse(child)         
    numRecurse(self.tree['tree'])
      
class WordColumn:
  def __init__(self, prevWordGroup, rules):
    self.prev = prevWordGroup
    self.rules = rules
    self.generateWords()
    self.pruneWords()
    self.buildWordGroups()

  def generateWords(self):
    words = self.prev
    self.words = []
    for i in range(len(self.prev)):
        self.words.append(words[i] + "0")
        self.words.append(words[i] + "1")
  def pruneWords(self):
    i = 0
    while i < len(self.words):
      for j in range(len(self.rules)):
        if self.rules[j] in self.words[i]:
          self.words.pop(i)
          i -= 1
      i += 1
  def buildWordGroups(self):
    if len(self.words[0]) < len(self.words) - 1:
      self.groups = [WordGroup(self.words[1:], [self.words[0]] + self.rules), WordGroup(self.words[:-1], [self.words[-1]] + self.rules)]
      self.children = [{'words': self.groups[0].words, 'rules': self.groups[0].rules}, {'words': self.groups[1].words, 'rules': self.groups[1].rules}]
    elif len(self.words[0]) == len(self.words) - 1:
      self.groups = [WordGroup(self.words, self.rules)]
      self.children = [{'words': self.groups[0].words, 'rules': self.groups[0].rules}]
    else:
      print "make it so spock"
    del self.prev, self.rules, self.words
 
class WordGroup:
  def __init__(self, words, rules):
    self.words = words
    self.rules = rules

t = WordTable(50, 'half')