#####################################################################
#
# CAS CS 320, Fall 2013
# Courtney Adams
# Assignment 3 
# compile.py
# Collaborators: Dan Monahan. Matt Auerbach
#
##################################################################### 

from parse import tokenizeAndParse
import machine as m
import random

Node = dict
Leaf = str

def compileTerm(env, t, heap):
    insts = []
    if type(t) is Node:
        for label in t:
            children=t[label]
            if label is "Plus":
                heap += 1
                (insts1, n1, heap)  = compileTerm(env, children[0], heap)
                (insts2, n2, heap) = compileTerm(env, children[1], heap)
                insts = insts1 + insts2 
                insts += m.copy(n1,1)
                insts += m.copy(n2,2)
                insts += ['add ']
                insts += m.copy(0,heap)
                return (insts, heap, heap)
            
            elif label is "Variable":
                heap += 1
                if children[0] in env:
                    insts += m.copy(env[children[0]], heap)
                return (insts, heap, heap)

            elif label is "Number":
                heap += 1
                insts = ['set ' + str(heap) + ' ' + str(children[0])]
                return (insts, heap, heap)

def compileFormula(env, f, heap):             # Uses compileFormula from notes
    if type(f) is Leaf:
        if f is 'True':
            heap += 1
            inst = ['set ' + str(heap) + ' 1 ']
            return (inst, heap, heap)

        if f is 'False':
            heap += 1
            inst = ['set ' + str(heap) + ' 0']
            return (inst, heap, heap)

    if type(f) is Node:
        insts = []
        for label in f:
            children = f[label]
            if label is 'Not':
                (insts, f1, heap) = compileFormula(env, children[0], heap)
                fresh = random.randint(0, 100000000)
                instsNot = [ \
                    "branch setZero" + str(fresh) + " " + str(f1),\
                    "set " + str(f1) + " 1",\
                    "goto finish" + str(fresh),\
                    "label setZero" + str(fresh),\
                    "set " + str(f1) + " 0",\
                    "label finish" + str(fresh)\
                ]
                return (insts + instsNot, f1, heap)

            elif label is 'Or':
                fresh = random.randint(0, 100000000)
                (insts1, f1, heap) = compileFormula(env, children[0], heap)
                (insts2, f2, heap) = compileFormula(env, children[1], heap)
                heap += 1
                instsOr = m.copy(f1, 1) + m.copy(f2, 2)
                instsOr += [ \
                    "add",\
                    "branch setOne" + str(fresh) + " 0",\
                    "goto finish" + str(fresh),\
                    "label setOne" + str(fresh),\
                    "set 0 1",\
                    "label finish" + str(fresh)]
                instsOr += m.copy(0, heap)
                return (insts1 + insts2 + instsOr, heap, heap)

            elif label is 'And':
                fresh2 = random.randint(0, 100000000)
                t1 = children[0]
                t2 = children[1]
                (insts1, f1, heap) = compileFormula(env, t1, heap)
                (insts2, f2, heap) = compileFormula(env, t2, heap)
                heap += 1
                instsOr = m.copy(f1,1) + m.copy(f2,2) + m.copy(0,1) 
                instsOr += [ \
                    'set 2 -2 ', \
                    'add ', \
                    'branch setZero' + str(fresh2) + ' 0',\
                    'set 0 1',  \
                    'goto finish' + str(fresh2),\
                    'label setZero' + str(fresh2),\
                    'set 0 0',\
                    'label finish' + str(fresh2) \
                ]
                instsOr += m.copy(0,heap)
                return (insts1 + insts2 + instsOr, heap, heap)

            elif label is "Variable":
                heap += 1
                if children[0] in env:
                    insts += m.copy(env[children[0]], heap)
                return (insts, heap, heap)


def compileProgram(env, s, heap):
    if type(s) is Leaf:
        if s is 'End':
            return ([], heap, heap)

    elif type(s) is Node:
        insts = []
        for label in s:
            children = s[label]

        if label is 'Print':
            e = children[0]
            r =  compileFormula(env, e, heap)
            if(r) :
                (insts, f1, heap)  = r
            else :
                r = compileTerm(env, e, heap)
                if (r) :
                    (insts, f1, heap) = r

            insts += m.copy(f1, 5)

            (insts2, f2, heap) = compileProgram(env, children[1], heap)
            return (insts + insts2, f2, heap)

        elif label is 'Assign':
                x = children[0]['Variable'][0]
                f = children[1]
                r = compileFormula(env, f, heap)
                if(r):
                    (insts, env[x], heap) = r
                else:
                    r = compileTerm(env, f, heap)
                    if(r):
                        (insts, env[x], heap) = r
                
                (insts2, f2, heap) = compileProgram(env, children[2], heap)
                return (insts + insts2, f2, heap)

        elif label is 'If':
            e = children[0]
                
            r = compileFormula(env, e, heap)
            if(r):
                (insts, f1, heap)  = r
            else:
                r = compileTerm(env, e, heap)
                if (r):
                    (insts,f1, heap) = r

            fresh = random.randint(0, 100000000)
            insts += [ \
                'branch start' + str(fresh) + ' ' + str(f1), \
                'label start' + str(fresh) \
            ]
            (insts2, f2, heap) = compileProgram(env, children[1], heap)
            insts2 += ['label finish' + str(fresh)]
            (insts3, f3, heap) = compileProgram(env, children[2], heap)
            return (insts + insts2 + insts3, f3, heap)

        elif label is 'While':
            e = children[0]
            r =  compileFormula(env, e, heap)
            if(r):
                (insts, f1, heap)  = r
            else:
                r = compileTerm(env, e, heap)
                if (r):
                    (insts,f1, heap) = r
            
            fresh = random.randint(0, 100000000)
            insts += [ \
                'branch start' + str(fresh) + ' ' + str(f1), \
                'goto finish' + str(fresh), \
                'label start' + str(fresh) \
            ]
            (insts2, f2, heap) = compileProgram(env, children[1], heap)

            r =  compileFormula(env, e, heap)
            if(r):
                (insts3, f25, heap)  = r
            else:
                r = compileTerm(env, e, heap)
                if (r):
                    (insts3,f25, heap) = r

            insts3 += ['branch start' + str(fresh) + ' ' + str(f25), \
            'label finish' + str(fresh)]
            (insts4, f3, heap) = compileProgram(env, children[2], heap)
            return (insts + insts2 + insts3 + insts4, f3, heap)

        elif label is 'Procedure':
            (body, f1, heap) = compileProgram(env, children[1], heap)
            insts += m.procedure(children[0]['Variable'][0], body)
            (insts2, f2, heap) = compileProgram(env, children[2], heap)
            return (insts + insts2, f2, heap)

        elif label is 'Call':
            insts += m.call(children[0]['Variable'][0])
            (insts2, f1, heap) = compileProgram(env, children[1], heap)
            return (insts + insts2, f1, heap)

def compile(s):
    return compileProgram({},tokenizeAndParse(s),8)[0]