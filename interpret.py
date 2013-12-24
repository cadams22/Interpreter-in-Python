######################################################################
#
# CAS CS 320, Fall 2013
# Courtney Adams
# Assignment 3 
# interpret.py
# Collaborators: Dan Monahan. Matt Auerbach
#
##################################################################### 

exec(open('parse.py').read())

'''
def vnot(v):
    if v == 'True':  return 'False'
    if v == 'False': return 'True'

def vand(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'True'
    if v1 == 'True'  and v2 == 'False': return 'False'
    if v1 == 'False' and v2 == 'True':  return 'False'
    if v1 == 'False' and v2 == 'False': return 'False'

def vor(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'True'
    if v1 == 'True'  and v2 == 'False': return 'True'
    if v1 == 'False' and v2 == 'True':  return 'True'
    if v1 == 'False' and v2 == 'False': return 'False'
'''

Node = dict
Leaf = str

def evaluate(env, t):
    if type(t) is Node:
        for label in t:
            children=t[label]
            
            if label is 'Plus':
                return evalTerm(env,children[0]) + evalTerm(env,children[1])
            
            elif label is 'Variable':
                return evalTerm(env,env[children[0]])

            elif label is 'Number':
                return children[0]

def evalFormula(env, f):
    if type(f) is Node:
        for label in f:
            children = f[label]
            if label is 'And':
                return vand(evalFormula(env,children[0]), evalFormula(env,children[1]))
            elif label is 'Not':
                return vnot(evalFormula(env, children[0]))
            elif label is 'Variable':
                return evalFormula(env,env[children[0]])  
            elif label is 'Or':
                return vor(evalFormula(env,children[0]), evalFormula(env,children[1]))

    elif type(f) is Leaf:
        if f is 'True':
            return 'True'
        else:
            return 'False'           


def execProgram(env, s):
    if type(s) is Leaf:
        if s is 'End':
            return (env, [])

    elif type(s) is Node:
        for label in s:
            children = s[label]
            if label is 'Print':
                e = children[0]
                if (evalFormula(env, e)):
                    v = evalFormula(env, e)
                else: 
                    v = evalTerm(env, e)
                (env, o)  = execProgram(env, children[1])
                return(env, [v] + o)

            elif label is 'Assign':
                x = children[0]['Variable'][0]
                env[x] = children[1]
                (env, o) = execProgram(env, children[2])
                return (env, o)

            elif label is 'If':
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalFormula(env, e)
                if v is 'True':
                    (env, o1)=execProgram(env, p1)
                    (env, o2)=execProgram(env, p2)
                    return(env, o1 + o2)
                elif v is'False':
                    (env, o1)=execProgram(env, p2)
                    return(env, o1)

            elif label is 'While':
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalFormula(env, e)
                if v is 'True':
                    (env, o1) = execProgram(env, p1)
                    (env, o2) = execProgram(env, p2)
                    return (env,o1 + o2)
                elif v is 'False':
                    (env2, o1) = execProgram(env, p2)
                    return (env2,o1)

            elif label is 'Procedure':
                x = children[0]['Variable'][0]
                env[x] = children[1]
                (env, o) = execProgram(env,children[2])
                return (env, o)

            elif label is 'Call':
            	(env, o1) = execProgram(env, env[children[0]['Variable'][0]])
            	(env, o2) = execProgram(env, children[1])
            	return (env, o1 + o2)
                    
def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o