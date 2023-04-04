import pandas as pd
import numpy as np

firstOdds = [.114, .113, .112, .111, .099, .089, .079, .069, .059, .049, .039, .029, .019, .009, 0.006, 0.004]

seed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

chances = [114, 113, 112, 111, 99, 89, 79, 69, 59, 49, 39, 29, 19, 9, 6, 4]

num_teams = 16
num_picks = 5

team = 0
secondOdds = []

# Get the odds for each team getting the second pick
for i in range(len(chances)):
    chances.insert(0, chances.pop(i))
    for j in range(len(chances)):
        if j != 0:
            roundOdds = (chances[j]/1000) * (chances[0]/(1000-chances[j]))
            team += roundOdds
        
        
    secondOdds.append(team)
    team = 0

chances = [114, 113, 112, 111, 99, 89, 79, 69, 59, 49, 39, 29, 19, 9, 6, 4]
chances_new = [114, 113, 112, 111, 99, 89, 79, 69, 59, 49, 39, 29, 19, 9, 6, 4]

team = 0
secondOdds = []

team3 = 0
thirdOdds = []

team4 = 0
fourthOdds = []

team5 = 0
fifthOdds = []

remaining_probs = np.zeros((num_teams, num_teams - num_picks))

# Function that returns the rest of the draft probabilities based on probabilities from the lottery
def restOfDraft(chances, remaining_chances, rest_prob):
    for i in range(num_teams - num_picks):
        nonzeros = [j for j, e in enumerate(chances) if e != 0]
        team = min(nonzeros)
        remaining_chances[team][i] += rest_prob
        chances[team] = 0
    return remaining_chances

for i in range(num_teams): # Loop through each team
    chances.insert(0, chances.pop(i))
    for j in range(num_teams): #second round
        if j != 0: 
            roundOdds2 = (chances[j]/1000) * (chances[0]/(1000-chances[j]))
            team = roundOdds2 + team
        if i != j: # check current team is different from prev team
            for k in range(num_teams): #third round
                if k != j and k != i: # check current team is different from prev teams
                    roundOdds3 = (chances_new[k]/1000) * (chances_new[j]/(1000-chances_new[k])) * (chances[0]/(1000-chances_new[j]-chances_new[k]))
                    team3 = roundOdds3 + team3
                    for n in range(num_teams): # fourth round
                        if n != k and n != j and n != i: # check current team is different from prev teams
                            roundOdds4 = (chances_new[n]/1000) * (chances_new[k]/(1000-chances_new[n])) * (chances_new[j]/(1000-chances_new[k]-chances_new[n])) * (chances[0]/(1000-chances_new[k]-chances_new[n]-chances_new[j]))
                            team4 = roundOdds4 + team4
                            for a in range(num_teams): # fifth round
                                if a != n and a != k and a != j and a != i: # check current team is different from prev teams
                                    roundOdds5 = (chances_new[a]/1000) * (chances_new[n]/(1000-chances_new[a])) * (chances_new[k]/(1000-chances_new[n]-chances_new[a])) * (chances_new[j]/(1000-chances_new[k]-chances_new[n]-chances_new[a])) * (chances[0]/(1000-chances_new[k]-chances_new[n]-chances_new[j]-chances_new[a]))
                                    team5 = roundOdds4 + team4
                                    for b in range(num_teams): #rest of draft order
                                        if b != a and b != n and b != k and b != j and b != i: # check current team is different from prev teams
                                            restProb = (chances_new[b]/1000) * (chances_new[a]/(1000-chances_new[b])) * (chances_new[n]/(1000-chances_new[a]-chances_new[b])) * (chances_new[k]/(1000-chances_new[n]-chances_new[a]-chances_new[b])) * (chances_new[j]/(1000-chances_new[k]-chances_new[n]-chances_new[a]-chances_new[b])) * (chances[0]/(1000-chances_new[k]-chances_new[n]-chances_new[j]-chances_new[a]-chances_new[b])) 
                                            # make all of the chances 0 where a team has been selected so restOfDraft function knows which teams have been selected
                                            chances_new[b] = 0
                                            chances_new[a] = 0
                                            chances_new[n] = 0
                                            chances_new[k] = 0
                                            chances_new[i] = 0
                                            remaining_probs = restOfDraft(chances_new, remaining_probs, restProb)

                                        chances_new = [114, 113, 112, 111, 99, 89, 79, 69, 59, 49, 39, 29, 19, 9, 6, 4]
                           
    secondOdds.append(team)
    thirdOdds.append(team3)
    fourthOdds.append(team4)
    fifthOdds.append(team5)
    team = 0
    team3 = 0
    team4 = 0
    team5 = 0
    chances = [114, 113, 112, 111, 99, 89, 79, 69, 59, 49, 39, 29, 19, 9, 6, 4]
    

# Create dataframe containing all values
matrix_df = pd.DataFrame(remaining_probs, columns=['6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th'])
table = [seed, chances, firstOdds, secondOdds, thirdOdds, fourthOdds, fifthOdds]
probs_df = pd.DataFrame({'seed': seed,'Chances': chances, '1st': firstOdds, '2nd': secondOdds, '3rd': thirdOdds, '4th': fourthOdds, '5th': fifthOdds})
result = pd.concat([probs_df, matrix_df], axis=1)
cols_to_convert = result.columns[2:]

result[cols_to_convert] = result[cols_to_convert].applymap('{:.3%}'.format)

result.to_csv('DraftProbabilityTable.csv', index=False)