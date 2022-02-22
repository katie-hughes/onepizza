import numpy as np
import sys
from collections import Counter
import random


fname = sys.argv[1]
AllLikes = []
AllDislikes = []
Preferences = []
with open(fname) as f:
    for i,line in enumerate(f.readlines()):
        if i == 0:
            total = int(line)
            print(f"There are {total} possible customers.")
        else:
            spl = line.split()
            n = int(spl[0])
            pid = (i+1)//2 - 1
            if (i%2)!=0:
                # likes
                print(f"Person # {pid}")
                Preferences.append([])
                likes = []
                for l in range(n):
                    item = spl[l+1]
                    likes.append(item)
                    AllLikes.append(item)
                (Preferences[pid]).append(likes)
                print(f"likes: {likes}")
            else:
                # dislikes
                dislikes = []
                for d in range(n):
                    item = spl[d+1]
                    dislikes.append(item)
                    AllDislikes.append(item)
                (Preferences[pid]).append(dislikes)
                print(f"dislikes: {dislikes}\n")


ingredients = list(set(AllLikes+AllDislikes))

print(f"{len(ingredients)} possible ingredients")

## Preferences[person][0] is likes, Preferences[person][1] is their dislikes


def determine_score(InputList, SolutionList):
    customers = 0
    for people in InputList:
        likes = people[0]
        dislikes = people[1]
        eat = True
        for l in likes:
            if l not in SolutionList:
                eat = False
                break
        if eat:
            for d in dislikes:
                if d in SolutionList:
                    eat = False
                    break
        if eat:
            customers += 1
    return customers




"""
first idea: likes and dislikes are evenly balanced
ie a person will not eat if something they dislike is on
AND a person will not eat if something they like is NOT on
so if likes > dislikes for a particular ingredient, include it?
issue: this doesn't consider grouping of like/dislike for each person
"""

#"""

print("\n\n1. Trying a Simple Approach\n")

CountLikes = Counter(AllLikes)
CountDislikes = Counter(AllDislikes)

#print("LIKES:",CountLikes)
#print("DISLIKES:",CountDislikes)

SimpleSolution = []

for i in CountLikes:
    numLike = CountLikes[i]
    numDislike = CountDislikes[i]
    if numLike > numDislike:
        SimpleSolution.append(i)
    print(f"{numLike} likes and {numDislike} dislikes ingredient {i}")

print(SimpleSolution)
simple_score = determine_score(Preferences, SimpleSolution)
print(f"\nScore for this approach: {simple_score}/{total}")


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
print('\n\n2.Attempt with Greedy(?) algorithm\n')

scores = []
iterations = 5

GreedySolutions = []

for x in range(iterations):
    Solution = []
    indices = list(range(total))
    random.shuffle(indices)
    last_score = 0

    for i in indices:
        score_init = last_score
        Solution_copy = list(Solution)
        likes = Preferences[i][0]
        dislikes = Preferences[i][1]
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
                score_final = determine_score(Preferences, Solution_copy)
                print(score_init, score_final)
                if score_final>score_init:
                    Solution = Solution_copy
                    last_score = score_final
                    #print('updating solution to ', Solution)

    #print(Solution)
    score = determine_score(Preferences, Solution)
    print(f"Score: {score}/{total}")
    scores.append(score)
    GreedySolutions.append(Solution)
    print()

print(f"Range of Scores: {scores}")
print(f"Simple Score for comparison: {simple_score}")


FinalSolution = []
max_greedy_score = max(scores)
if max_greedy_score > simple_score:
    print("Greedy Approach was better")
    max_greedy_index = scores.index(max_greedy_score)
    max_greedy_solution = GreedySolutions[max_greedy_index]
    FinalSolution = max_greedy_solution
else:
    print("Simple Approach was better")
    FinalSolution = SimpleSolution


print('\n\nSOLUTION\n\n')
print(len(FinalSolution),end=' ')
for i in FinalSolution:
    print(i, end=' ')
print()




#"""


#D: I got final score 1589 which is 100 less ish than last attempt
# General range from around 1580 to 1630,,,, so i never beat the easy approach



#E: simple case gives 799
# Random algorithm gives 1685!!!! so significantly better there :)
