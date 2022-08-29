from urllib import request
import json
import random
import time
import pronouncing
from coolname import generate

def count_syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count

def generate_rhyming_words(word):
    rhyming_words = []
    for pronunciation in pronouncing.rhymes(word):
        rhyming_words.append(pronunciation)
    return rhyming_words

def dictionary_filter(dictionary, syllables_max):
    for key in list(dictionary):
        if count_syllables(key) > syllables_max:
            del dictionary[key]
    return dictionary

def generate_cool_title():
    return ' '.join(generate())

start = time.time()

url = "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json"
response = request.urlopen(url)
english_dict = json.loads(response.read())

#Filtering dictionary for words that are too long (too many syllables)
english_dict = dictionary_filter(english_dict, 2)
sonnet = []
run = 0

#AB/CD/EF 
for couple in range(3):
    
    #creating two lines of the sonnet
    for line in range(2):
        #initiating an empty line
        new_line = []
        #setting number of available syllables
        available_syllables = 10

        #while the line does not have the right number of syllables
        while available_syllables != 0:
            #choose a random word from the dictionary
            word = random.choice(list(english_dict.keys()))
            #if the word is not too long and there exists a rhyming word
            if count_syllables(word) <= available_syllables and len(generate_rhyming_words(word)) > 0:
                new_line.append(word)
                available_syllables -= count_syllables(word)
    
        sonnet.append(new_line)

    #AB/CD/EF Rhyme
    for line in range(2):
        #initiating an empty line
        new_line = []
        #choosing a random word from the dictionary of rhyming words for the last word in the corresponding line of the couplet
        print(f"Generating dictionary for line {run}")
        print(f"Line that we're picking from: {sonnet[run]}")
        new_line.append(random.choice(list(generate_rhyming_words(sonnet[run][-1]))))
        #incrementing run by 1, so that the couplet will generate the correct dictionary of rhyming words
        run += 1
        #setting number of available syllables
        available_syllables = 10 - count_syllables(new_line[0])

        while available_syllables != 0:
            word = random.choice(list(english_dict.keys()))
            if count_syllables(word) <= available_syllables:
                new_line.append(word)
                available_syllables -= count_syllables(word)
        #reversing order of line to make it a proper sonnet
        new_line.reverse()   
    
        sonnet.append(new_line)
    run += 2 

#GG
#creating last two lines of the sonnet
new_line = []
#setting number of available syllables
available_syllables = 10
#while the line does not have the right number of syllables
while available_syllables != 0:
    #choose a random word from the dictionary
    word = random.choice(list(english_dict.keys()))
    #if the word is not too long and there exists a rhyming word
    if count_syllables(word) <= available_syllables and len(generate_rhyming_words(word)) > 0:
        new_line.append(word)
        available_syllables -= count_syllables(word)
sonnet.append(new_line)

new_line = []
#choosing a random word from the dictionary of rhyming words for the last word in the corresponding line of the couplet
print(f"Last line that we're picking from: {sonnet[-1]}")
new_line.append(random.choice(list(generate_rhyming_words(sonnet[-1][-1]))))

#setting number of available syllables
available_syllables = 10 - count_syllables(new_line[0])

while available_syllables != 0:
    word = random.choice(list(english_dict.keys()))
    if count_syllables(word) <= available_syllables:
        new_line.append(word)
        available_syllables -= count_syllables(word)
#reversing order of line to make it a proper sonnet
new_line.reverse()   
sonnet.append(new_line)

line_n =0

#capitalising first word of each line
for line in sonnet:
    line[0] = line[0].capitalize()

with open('sonnet.txt', 'w') as filehandle:

    #Creating title
    filehandle.write('%s\n' % ''.join(x.capitalize() for x in generate_cool_title()))
    filehandle.write('\n')

    #Writing sonnet to file
    for listitem in sonnet:
        list_to_string = ' '.join([str(elem) for elem in listitem])
        filehandle.write('%s\n' % list_to_string)
        if line_n % 2 != 0:
            filehandle.write('\n')
        line_n += 1


print(f"Lines in Sonnet: {len(sonnet)}")
print("Finished in %s seconds" % (time.time() - start))
