from copy import deepcopy
import itertools
#-------------------------------------------------------------
#    similarity count empty intersections            
def similarity(rule1,rule2,d):
    unions = []
    intersections = []
    indexes = []
    difference = 0
    for i in range( len(rule1) - 1 ):
        union = rule1[i] | rule2[i]
        intersection = rule1[i] & rule2[i]
        unions.append(union)
        intersections.append(intersection)
        if intersection == set():
            difference +=1
            indexes.append(i)
    if difference <= d:
        return [True, unions, intersections, indexes]
    else:
        return [False, None, None, None]
#-------------------------------------------------------------
#    expand r int its one-instance rules
def expandRule(rule):
    rules = []
    sets = rule[0:-1]
    #print('sets', sets)
    combinations = itertools.product(*sets)
    for i in combinations:
        temp_rule = []
        combination = i
        #print(combination,type(combination))
        for j in combination:
            _set = set()
            _set.add(j)
            temp_rule.append(_set)
        
        temp_rule.append(rule[-1]) # Append category
        rules.append(temp_rule)
#    print(rules)
    return rules
#print(expandRule([{1,2,3},{2,3},'A']))
#-------------------------------------------------------------
#    check if all one-instance rules of a rule exist in the
#    original rules 
def allRules(rule, originalRules):
    expand = expandRule(rule)
    suma = 0
    for r in expand:
        if r in originalRules:
            suma+=1
    if suma == len(expand):
        return True
    else:
        return False
#-------------------------------------------------------------
#    createRules for similarity "count empty intersections"
def create_rule(rule1, unions, originalRules, d):
    rule = deepcopy(rule1)
    for i in range(len(rule1)-1):
        rule[i] = unions[i]
    all_rules = allRules(rule, originalRules)
    if all_rules:
        return rule
    else:
        return False
#    if d >=2:
#        contradiction = contradictions(rule,rules_other_classes)
#        if contradiction == False:
#            return rule
#        else:
#            return False
#--------------------------------------------------------------
#  True if a rule1 is subset of rule2, False otherwhise
def contained( rule1, rule2 ):
    #if rule1[-1] == rule2[-1]:
    equalParameters = 0
    for i in range( len(rule1) - 1 ):
        if rule1[i].issubset(rule2[i]):
            equalParameters +=1
    if equalParameters == len(rule1) - 1:
        return True
    else:
        return False
    #else:
    #    return False
# TESTS
#print(contained( [{1},{1},'A'],[{1},{1,2,3},'A']) )
#True
#print(  contained( [{2},{7},'D'],[{2,5},{7},'D']   )   )
#True
#---------------------------------------------------------------
#def deleteRedundant( rules ):
#    nonRedundant = []
#    for i in range(0, len(rules)):
#        redundant = False
#        rule1 = rules[i]
#        for j in range(0, len(rules)):
#            rule2 = rules[j]
##            print('rule1 rule2',rule1, rule2)
#            if rule1 != None and rule2 != None and i != j and contained(rule1,rule2) == True:
#          #      print(rule1,'contained in', rule2)
#                redundant = True
#        if redundant == True:
#            rules[i] = None
#    [nonRedundant.append(r) for r in rules if r != None]
#    return nonRedundant
#----------------------------------------------------------------
#    remove redundant rules
def deleteRedundant( rules ):#more eficient
    nonRedundant = []
    for i in range(0, len(rules)):
        redundant = False
        rule1 = rules[i]
        for j in range( i+1, len(rules)):
            rule2 = rules[j]
#            print('rule1 rule2',rule1, rule2)
            if rule1 != None and rule2 != None and contained(rule1,rule2) == True:
          #      print(rule1,'contained in', rule2)
                redundant = True
        if redundant == True:
            rules[i] = None
    [nonRedundant.append(r) for r in rules if r != None]
    return nonRedundant

def search_patterns(rulesCurrentCategory, d, originalRules):
    newRules = []
    for i in range( 0, len(rulesCurrentCategory) ):
        r1 = rulesCurrentCategory[i]
        for j in range(i+1, len(rulesCurrentCategory)):
            r2 = rulesCurrentCategory[j]
            [pattern, unions, intersections, indexes] = similarity(r1, r2, d)
            if pattern:
                rule = create_rule(r1, unions, originalRules, d)
                if rule!=False and rule not in newRules:
                    newRules.append(rule)
#    print(rulesCurrentCategory,newRules)
    [rulesCurrentCategory.append(r) for r in newRules]
    #print('deleting redundant rules . . . . ')
    rules = deleteRedundant(rulesCurrentCategory)
    return rules

def iterate(rulesCurrentCategory,d):
    originalRules = deepcopy(rulesCurrentCategory)
    extractedRules = []
    rules = search_patterns(rulesCurrentCategory, d, originalRules)#it'll need here rules other categories to compare with when d >= 2
    print('rules in the first extraction : ', rules)
    while rules != extractedRules:
        extractedRules = deepcopy(rules)#is the deepcopy needed??
        rules = search_patterns(extractedRules, d, originalRules)
        print('rules extracted within the while : ', rules)
    return rules
#iterate([ [{2},{2},'A'], [{4},{2},'A'], [{2},{3},'A'] ], 1)







