import numpy as np

class GA:
    def __init__(self):
        pass
    
    """ 1st step
        generat
        .e random initial population which consists of n 
        individuals each of length 12 bit
        each bit represents an action (0, 1 or 2)
    """
    def generate_initial_population(self, popsize, level_length):
        pop = [np.random.randint(0, 3, level_length) for n in range(popsize)]
        return pop
    
    """ 2nd step
        assign score to each individual
        score is calculated by the objective function
        with 2 methods (with and without winning score) 
    """
    def objective(self, individual, level, method):
        """
            points : 
                winning 5pts
                each step 1pts
                killing a gumpa 2pts
                mushrooms 2pts
                jump in last step 1pts
                useless jump -0.5pts
        """
        step = 0
        steps = []
        mushrooms = 0   
        gumpas = 0
        useless_jump = 0
        win = 0
        winflag = False
        flag = 0
        max_run = 0
        for i in range(len(individual)):
            # check if the individual kills a gumpa in this step 
            if i>2 and level[i] == 'G' and individual[i-2] == 1:
                gumpas += 2
            # check if the individual jumps useless in this step
            if i < len(level ) - 2 :
                if individual[i] == 1 and not (level[i+1] == 'G' or level[i+2] == 'G') and not i==len(individual)-2:
                    useless_jump += -0.5

            # jump in final step for flag
            if i == len(individual) - 2 and individual[i] == 1:
                flag = 1

            # check step
            # check if the individual collects a mushroom in this step
            if level[i] == 'M' and not individual[max(0,i-1)] == 1: #max is for check in i=0
                mushrooms += 2
                step += 1   
            elif (level[i] == '_'):
                step += 1
            elif (level[i] == 'G' and individual[i - 1] == 1):
                step += 1
            elif (level[i] == 'L' and individual[i - 1] == 2):
                step += 1
            else:
                steps.append(step)
                step = 0

        steps.append(step)
        # max run without lose
        max_run = max(steps)

        if (max_run == len(level)) :
            winflag = True
        
        #check if the individual wins   
        if winflag and method == 1:
            win = 5
        # print(f"step :{step} max_run :{max_run} mushrooms :{mushrooms} gumpas :{gumpas} useless_jump :{useless_jump} win :{win}")
        # print(steps)
        pts = win + max_run + mushrooms + gumpas + useless_jump + flag
        return pts, winflag

    """ 3rd step
        method 1 :select n best individuals from the population
        method 2 :weighted select due to score of each individual
    """
    def select_individuals(self, pop, scores, selection_size, method):
        selected = []

        if method == 1 :
            selected = list(zip(scores, pop))
            selected.sort(key=lambda x: x[0])
            selected = [x[1] for x in selected[-selection_size:]]
        # selection using SUS 
        if method == 2:
            total_score = sum(scores)
            step_score = total_score / selection_size
            start_point = np.random.rand() * step_score
            points = [start_point + i * step_score for i in range(selection_size)]
            for point in points:
                i = 0
                while sum(scores[:i]) < point:
                    i += 1
                selected.append(pop[i-1])

        return selected

    def crossover(self, selected_individuals, method ):
        
        level_length = len(selected_individuals[0])        
        gen = []

        # single point crossover
        def single_point_crossover(parent1, parent2):
            point = np.random.randint(0, level_length)
            child1 = np.concatenate((parent1[:point] , parent2[point:]))
            child2 = np.concatenate((parent2[:point] , parent1[point:]))
            return child1, child2
        
        def two_point_crossover(parent1, parent2):
            point1 = np.random.randint(0, level_length)
            point2 = np.random.randint(point1, level_length)
            child1 = np.concatenate((parent1[:point1] , parent2[point1:point2] , parent1[point2:]))
            child2 = np.concatenate((parent2[:point1] , parent1[point1:point2] , parent2[point2:]))
            return child1, child2
        
        shuffled_list = selected_individuals
        np.random.shuffle(shuffled_list)

        if method == 1:
            for i in range(0, len(shuffled_list), 2):
                child1, child2 = single_point_crossover(selected_individuals[i],\
                                                         selected_individuals[i+1])
                gen.append(child1)
                gen.append(child2)
            
        if method == 2:
            for i in range(0, len(shuffled_list), 2):
                child1, child2 = two_point_crossover(selected_individuals[i],\
                                                         selected_individuals[i+1])
                gen.append(child1)
                gen.append(child2)

        return gen 

    def mutate(self, individual, p):
        # mutate some genes randomly
        change_size = np.random.randint(0, np.ceil(len(individual) / 2))
        mutation_list = np.random.choice(range(len(individual)), change_size, replace=False)
        for i in mutation_list:
            if np.random.rand() < p:
                individual[i] = np.random.randint(0, 3)
        return individual