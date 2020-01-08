import random

stringList = list()

with open("words.txt",'r', encoding="utf8") as f:
    for line in f:
        stringList.append(line.strip())

class wordSource:
    def getWord():
        word = "Default word"
        while len(word) > 10:
            word = random.choice(stringList).upper()

        return word

