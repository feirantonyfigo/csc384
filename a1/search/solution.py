#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    # initialize manhattan distance to 0
    md = 0
    # traverse through each box
    for box in state.boxes:
        # initialize minimum distance to closest is 2**31 (integer inf)
        minDist = float('inf')
        # traverse through each storage point
        for stP in state.storage:
            # update closest storage point (shortest distance)
            minDist = min(minDist, (abs(box[0]-stP[0])+abs(box[1]-stP[1])))
        # increment manhattan distance
        md += minDist
    return md


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

# helper function to determine whether there is a dead situation
def check_dead(state, box):
    # there are such two cases that the game is dead, need to stop searching
    # box[0] - x , box[1] - y

    # case 1: corner condition -> blocked in any two near directions
    # 1) check if left is an obstacle/wall
    left = box[0] == 0 or (box[0]-1, box[1]) in state.obstacles
    # 2) check if right is an obstacle/wall
    right = box[0] == state.width-1 or (box[0]+1, box[1]) in state.obstacles
    # 3) check if up is an obstacle/wall
    up = box[1] == 0 or (box[0], box[1]-1) in state.obstacles
    # 4) check if down is an obstacle/wall
    down = box[1] == state.height-1 or (box[0],box[1]+1) in state.obstacles
    # calculate boolean for case 1
    if (left and up) or (left and down) or (right and up) or (right and down):
        return True

    # case 2: edge condition -> box on the edge but storage not on the edge or together with another box
    # 1) check left-most / right-most edge
    isEdged = True
    if box[0] == 0 or box[0] == state.width-1:
        # if close-by location has another box, dead situation
        if (box[0], box[1]-1) in state.boxes or (box[0],box[1]+1) in state.boxes:
            return True
        for stP in state.storage:
            if stP[0] == box[0]:
                isEdged = False
                break
        if isEdged:
            return True
    # 2) check top / bottom edge
    if box[1] == 0 or box[1] == state.height-1:
        # if close-by location has another box, dead situation
        isEdged = True
        if (box[0]-1,box[1]) in state.boxes or (box[0]+1,box[1]) in state.boxes:
            return True
        for stP in state.storage:
            if stP[1] == box[1]:
                isEdged = False
                break
        if isEdged:
            return True
    # calculate dead condition result, determine whether it is dead
    return False

# record previous state boxes
pre_boxes = None
# record previous box heuristic
pre_heuristic = 0

def heur_alternate(state):
    #IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    # global values declaration, see above
    global pre_boxes
    global pre_heuristic

    # if previous boxes is valid and boxes haven't moved
    if pre_boxes and pre_boxes == state.boxes:
        hVal = 0
        # add the distance from each box to nearest robot in heuristic
        for box in state.boxes:
            minDist = min([abs(robot[0] - box[0]) + abs(robot[1] - box[1]) - 1 for robot in state.robots])
            hVal += minDist
        return pre_heuristic+hVal

    # return value - h value
    hVal = 0

    # when encountering dead condition, end the path
    for box in [box for box in state.boxes if box not in state.storage]:
        if check_dead(state, box):
            #print("got dead")
            return float('inf')

    # greedy heur_manhattan_distance (each storage point can only be used once)
    # originated from the original heur_manhattan_distance_function
    # record used storage point
    usedStorage = set([])
    for box in state.boxes:
        # compute minDist and storage point to use
        minDist, next_stP = min([(abs(box[0]-st[0])+abs(box[1]-st[1]), st) for st in state.storage if st not in usedStorage],
        key = lambda x: x[0])
        # increment manhattan distance
        hVal += minDist
        usedStorage.add(next_stP)

    # update previous box heuristic to current hVal
    pre_heuristic = hVal

    # add the distance from each box to nearest robot in heuristic
    for box in state.boxes:
        minDist = min([abs(robot[0] - box[0]) + abs(robot[1] - box[1])-1 for robot in state.robots])
        hVal += minDist


    return hVal

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    # according to formula: f(n) = g(n) + weight *h(n)
    fval = sN.gval + weight * sN.hval
    return fval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  # wrapper function
  wrapped_fval_function = (lambda sN : fval_function(sN,weight))

  # Initialize Search Engine
  # search strategy custom, with cc_level as default
  sE = SearchEngine(strategy='custom')
  # initialize search (** goal_fn = sokoban_goal_state)
  sE.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

  # Initialize costbound and search result
  costbound = [float('inf'), float('inf'), float('inf')]
  result = sE.search(timebound)
  final_res = False
  start_time = os.times()[0]

  # continue search while within timebound
  while timebound >= 0:
      # if no result found
      if not result:
          return final_res
      elapsed_time = os.times()[0]-start_time
      # update timebound (decrease elapsed_time)
      timebound -= elapsed_time
      if result.gval <= costbound[0]:
          costbound[0] = result.gval
          final_res = result
      start_time = os.times()[0]
      result = sE.search(timebound, costbound)

  return final_res

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  # Initialize Search Engine
  # search strategy best_first, with cc_level as default
  sE = SearchEngine(strategy='best_first')
  # initialize search (** goal_fn = sokoban_goal_state)
  sE.init_search(initial_state, sokoban_goal_state, heur_fn)

  # Initialize costbound and search result
  costbound = [float('inf'), float('inf'), float('inf')]
  result = sE.search(timebound)
  final_res = False
  start_time = os.times()[0]

  # continue search while within timebound
  while timebound >= 0:
      # if no result found
      if not result:
          return final_res
      elapsed_time = os.times()[0] - start_time
      # update timebound (decrease elapsed_time)
      timebound -= elapsed_time
      if result.gval <= costbound[0]:
          costbound[0] = result.gval
          final_res = result
      start_time = os.times()[0]
      result = sE.search(timebound, costbound)
  return final_res
