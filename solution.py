import numpy as np
import sys
from collections import Counter
import random


fname = sys.argv[1]
AllLikes = []
AllDislikes = []
lookup = []
with open(fname) as f:
    for i,line in enumerate(f.readlines()):
        if i == 0:
            total = int(line)
            print(total, 'total people')
        else:
            spl = line.split()
            n = int(spl[0])
            pid = (i+1)//2 - 1
            print('person # %s'%pid)
            if (i%2)==0:
                # dislikes
                dislikes = []
                for d in range(n):
                    item = spl[d+1]
                    dislikes.append(item)
                    AllDislikes.append(item)
                (lookup[pid]).append(dislikes)
                print("dislikes:", dislikes, '\n')
            else:
                # likes
                lookup.append([])
                likes = []
                for l in range(n):
                    item = spl[l+1]
                    likes.append(item)
                    AllLikes.append(item)
                (lookup[pid]).append(likes)
                print("likes:", likes)

ingredients = list(set(AllLikes+AllDislikes))

#print(len(ingredients), 'ingredients')



## lookup[person][0] is likes, lookup[person][1] is their dislikes


def determine_score(Preferences, FinalList):
    res = 0
    for people in Preferences:
        likes = people[0]
        dislikes = people[1]
        #print("Likes:", likes)
        #print("Dislikes:", dislikes)
        eat = True
        for l in likes:
            if l not in FinalList:
                #print("%s not in %s"%(l, FinalList))
                eat = False
                break
        if eat:
            for d in dislikes:
                if d in FinalList:
                    #print("%s not in %s"%(d, FinalList))
                    eat = False
                    break
        if eat:
            #print("This person will eat\n")
            res += 1
        else:
            #print("This person will not eat\n")
            pass
    return res




"""
first idea: likes and dislikes are evenly balanced
ie a person will not eat if something they dislike is on
AND a person will not eat if something they like is NOT on
so if likes > dislikes for a particular ingredient, include it?
issue: this doesn't consider grouping of like/dislike for each person
"""

#"""

CountLikes = Counter(AllLikes)
CountDislikes = Counter(AllDislikes)

#print("LIKES:",CountLikes)
#print("DISLIKES:",CountDislikes)

FinalIngredients = []

for i in CountLikes:
    numLike = CountLikes[i]
    numDislike = CountDislikes[i]
    if numLike > numDislike:
        FinalIngredients.append(i)
    print('%d likes and %d dislikes %s'%(numLike, numDislike,i))

#print(len(FinalIngredients), FinalIngredients)
simple_score = determine_score(lookup, FinalIngredients)
print("SCORE: %d/%d"%(simple_score,total))


#"""


"""
other idea
randomly go through the list of people
the first person "seed" we start making the list around
then we keep adding ingredients and keeping track of ones we dont want
until we go through the whole list of people?

maybe do this process multiple times and choose one with highest score

or start with one person
calculate score
add one more person and calculate score again
if it is higher move on and if not remove that person's
"""


#"""
print('\nRandom Attempt')

scores = []


for x in range(1):

    Solution = []

    indices = list(range(total))
    random.shuffle(indices)
    print(indices)


    last_score = 0

    for i in indices:
        score_init = last_score
        Solution_copy = list(Solution)
        likes = lookup[i][0]
        dislikes = lookup[i][1]
        add = True
        for d in dislikes:
            if d in Solution:
                add = False
                break
        if add:
            new=False
            for l in likes:
                if l not in Solution_copy:
                    new=True
                    Solution_copy.append(l)
            if new:
                score_final = determine_score(lookup, Solution_copy)
                print(score_init, score_final)
                if score_final>score_init:
                    Solution = Solution_copy
                    last_score = score_final
                    #print('updating solution to ', Solution)

    #print(Solution)
    score = determine_score(lookup, Solution)
    print(score, total)
    scores.append(score)

print(scores)
print("Simple Score for comparison:", simple_score)
#"""


#D: I got final score 1589 which is 100 less ish than last attempt
# General range from around 1580 to 1630,,,, so i never beat the easy approach



#E: simple case gives 799
# Random algorithm gives 1685!!!! so significantly better there :)
