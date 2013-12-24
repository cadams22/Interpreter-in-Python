#####################################################################
#
# CAS CS 320, Fall 2013
# Courtney Adams
# Assignment 3 
# machine.py
# Collaborators: Dan Monahan. Matt Auerbach
#
##################################################################### 

def simulate(s):
    instructions = s if type(s) == list else s.split("\n")
    instructions = [l.strip().split(" ") for l in instructions]
    mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0, 7:-1}
    control = 0
    outputs = []
    while control < len(instructions):
        # Update the memory address for control.
        mem[6] = control 
        
        # Retrieve the current instruction.
        inst = instructions[control]
        
        # Handle the instruction.
        if inst[0] == 'label':
            pass
        elif inst[0] == 'goto':
            control = instructions.index(['label', inst[1]])
            continue
        elif inst[0] == 'branch' and mem[int(inst[2])] :
            control = instructions.index(['label', inst[1]])
            continue
        elif inst[0] == 'jump':
            control = mem[int(inst[1])]
            continue
        elif inst[0] == 'set':
            mem[int(inst[1])] = int(inst[2])
        elif inst[0] == 'copy':
            mem[mem[4]] = mem[mem[3]]
        elif inst[0] == 'add':
            mem[0] = mem[1] + mem[2]

        # Push the output address's content to the output.
        if mem[5] > -1:
            outputs.append(mem[5])
            mem[5] = -1

        # Move control to the next instruction.
        control = control + 1

    print("memory: "+str(mem))
    return outputs

# Examples of useful helper functions from lecture.    
def copy(frm, to):
   return [\
        'set 3 ' + str(frm),\
        'set 4 ' + str(to),\
        'copy '\
   ]

def setZero():
    insts = [ \
        'set 0 0 ', \
        'set 1 0 ', \
        'set 2 0 ', \
        'set 3 0 ', \
        'set 4 0 ' \
    ]
    return insts


def increment(addr):
    insts = copy(addr, 1)
    insts += [ \
        'set 2 1 ', \
        'add ' \
    ]
    insts += copy(0, addr)
    insts += setZero()

    return insts


def decrement(addr):
    insts = copy(addr, 1)
    insts += [ \
        'set 2 -1 ', \
        'add ' \
    ]
    insts += copy(0, addr)
    insts += setZero()
    
    return insts


def call(name):
    insts = decrement(7) + copy(7,4)
    insts +=[ \
        'set 3 6 ', \
        'copy ' \
    ]
    insts += copy(7,3)
    insts += [ \
        'set 4 2 ', \
        'copy ', \
        'set 1 14 ', \
        'add '
    ]
    insts += copy(7,4)
    insts += [ \
        'set 3 0 ', \
        'copy ', \
        'goto ' + name \
    ]
    insts += increment(7)

    return insts


def procedure(name, body):
    insts = [ \
        'goto ' + name + '-end ', \
        'label ' + name \
    ] 
    insts += body + copy(7,3) 
    insts += [ \
        'set 4 2 ', \
        'copy ', \
        'jump 2 ', \
        'label ' + name + '-end ' \
    ]
    return insts

# eof