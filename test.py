import time
t = time.time()
import matplotlib.pyplot as plt
import numpy as np
from GA import GA

"""
pseudocode

START
Generate the initial population
Compute fitness
REPEAT
    Selection
    Crossover
    Mutation
    Compute fitness
UNTIL population has converged
STOP

"""
t0 = time.time()
levels = []

for i in range(1, 11):
    file = "levels/level" + str(i) + ".txt"
    with open(file, "r") as f:
        levels.append(f.read())

# test for level 8 
# first approach due to given table
obj = GA()
test_level = 8
test_level -= 1
inital_pop = 200
score_method = 1
select_method = 1
crossover_method = 1
pm = 0.1 #mutation probablity 
#print(len(levels[test_level]) , levels[test_level])

# init population
inital_population = obj.generate_initial_population(inital_pop,len(levels[test_level]))
# calculate scores
scores = []
for i in range(len(inital_population)):
    scores.append(obj.objective(inital_population[i], levels[test_level], score_method)[0])
population = inital_population
pop_scores = scores
generation = 0
max_score_gen = []
min_score_gen = []
mean_score_gen = []

while True:
    # calculate max, min and mean score of genration
    max_score_gen.append(max(pop_scores))
    min_score_gen.append(min(pop_scores))
    mean_score_gen.append(np.mean(pop_scores))
    
    #increment generation
    generation += 1

    # selection parents for crossover
    parents = obj.select_individuals(population, pop_scores , len(population),select_method)
    # crossover
    childs = obj.crossover(parents, crossover_method)
    # mutation  
    mutated_childs = []
    for child in childs:
        mutated_childs.append(obj.mutate(child, pm))
    # calculate scores of mutated childs
    mutated_scores = []
    for i in range(len(mutated_childs)):
        mutated_scores.append(obj.objective(mutated_childs[i], levels[test_level], score_method)[0])

    # add mutated childs to population and
    # select from the new population for next generation
    population = mutated_childs + population
    pop_scores = mutated_scores + pop_scores

    # select for new genration 
    population = obj.select_individuals(population, pop_scores , len(inital_population),select_method)

    #calculate scores for new genration
    new_scores = []
    for i in range(len(population)):
        new_scores.append(obj.objective(population[i], levels[test_level], score_method)[0])

    pop_scores = new_scores

    # check stop condition
    mean_change = abs((mean_score_gen[generation-1] - mean_score_gen[generation-2 ])\
                       / mean_score_gen[generation-1] ) * 100
    print(f"generation : {generation}\n mean change :{mean_change}")
    if generation > 1 :
        if generation == 100 or mean_change < 0.05:
            break

_, w = obj.objective(population[-1], levels[test_level], score_method)  
print(f"best : {population[-1]}\n \
      level: {levels[test_level]} \
      \nwith score {pop_scores[-1]} \nwin : {w}")
#plots

plt.figure()
plt.xlabel("Generation")    
plt.ylabel("Score")

plt.plot(max_score_gen, label="Max score")
plt.plot(min_score_gen, label="Min score")
plt.plot(mean_score_gen, label="Mean score")

plt.legend()
t1 = time.time()
plt.show()
