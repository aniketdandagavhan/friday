from textblob import Word

def autoCorrect(word):

    result = Word(word).correct()

    return result

while(True):
    word = input("word here >> ")
    print(autoCorrect(word))