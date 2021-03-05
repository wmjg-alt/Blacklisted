from bs4 import BeautifulSoup
import nltk
import random
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

class Markov(object):
    
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()
        
    
    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words
        
    
    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """
        
        if len(self.words) < 3:
            return
        
        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])
            
    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]
                
    def generate_markov_text(self, size=40):
            seed = random.randint(0, self.word_size-3)
            size = random.randint(size/2, size)
            seed_word, next_word = self.words[seed], self.words[seed+1]
            w1, w2 = seed_word, next_word
            gen_words = []
            for i in range(0,size):
                gen_words.append(w1)
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            gen_words.append(w2)
            target = ' '.join(gen_words)
            return target

def red(mark):
    target = mark.generate_markov_text()
    for x in range(1, len(target)):
        if target[0-x] in ".?!":
            target = target[:(0-x)+1]
            break
            
    if (len(target) < 5):
        return red(mark)
    else:
        return target

lines=[]
def buildcorp(target):
    global lines
    f1 = open("BL_Season1_TS.txt", "r", encoding="utf8")
    f2 = open("BL_Season2_TS.txt", "r", encoding="utf8")
    f3 = open("BL_Season3_TS.txt", "r", encoding="utf8")
    f4 = open("BL_Season4_TS.txt", "r", encoding="utf8")
    f5 = open("BL_Season5_TS.txt", "r", encoding="utf8")
    f6 = open("BL_Season6_TS.txt", "r", encoding="utf8")
    f7 = open("BL_Season7_TS.txt", "r", encoding="utf8")
    text1 = BeautifulSoup(f1.read(),'lxml').get_text()
    text2 = BeautifulSoup(f2.read(),'lxml').get_text()
    text3 = BeautifulSoup(f3.read(),'lxml').get_text()
    text4 = BeautifulSoup(f4.read(),'lxml').get_text()
    text5 = BeautifulSoup(f5.read(),'lxml').get_text()
    text6 = BeautifulSoup(f6.read(),'lxml').get_text()
    text7 = BeautifulSoup(f7.read(),'lxml').get_text()
    scripts = text1 + text2 + text3 + text4 + text5 + text6 + text7
    
    print(len(scripts))
    lines = scripts.splitlines()
    print("ALL LINES: ",len(lines))

    reds = [l[len(target)+2:] for l in lines if l[0:len(target)+1].lower() == target.lower()+":"]
    print(target.upper()+" LINES: ",len(reds))
    with open(target+'.txt', "w", encoding="utf-8") as f:
        for item in reds:
            f.write("%s\n" % item)

def gimme10(target):
    reddy = open(target+'.txt', "r", encoding="utf-8")
    m = Markov(reddy)
    for x in range(0,10):
        print(target.upper()+":", red(m))

