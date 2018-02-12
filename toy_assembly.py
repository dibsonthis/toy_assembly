from pprint import pprint
import os
import sys

actions = ['GET','INS','EXEC_INS','MOV','EXEC_MOV','ADD','SUB','MUL','DIV','EXP','DEL','MEM','REG']

debug = False

if debug == False:
    sys.tracebacklimit=None
else:
    sys.tracebacklimit=1000


# Mock memory
memory = [  [ [],[],[],[] ],
            [ [],[],[],[] ],
            [ [],[],[],[] ],
            [ [],[],[],[] ]  ]

registers = [ [],[],[],[] ]

# Functions
def get():
    address = line[1].split('x')
    address = [int(x) for x in address]
    try:
        content = memory[address[0]][address[1]]
        try:
            content = memory[address[0]][address[1]][0]
            print('\n{}'.format(content))
            return content
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))
            return

    except IndexError:
        print('\nAddressError: address {} does not exist - error occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))
        return

def insert():
    address = line[2].split('x')
    address = [int(x) for x in address]
    try:
        if memory[address[0]][address[1]]:
            print('\nAddressError: address {} is  not empty - DEL before appending - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
        else:
            memory[address[0]][address[1]] = [float(line[1])]
    except IndexError:
        print('\nAddressError: address {} does not exist - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
        return

def exec_insert():
    address = line[2].split('x')
    address = [int(x) for x in address]
    try:
        memory[address[0]][address[1]] = [float(line[1])]
    except IndexError:
        print('\nAddressError: address {} does not exist - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
        return

def move():
    # Fetch source and destination
    source = line[1].split('x')
    source = [int(x) for x in source]
    destination = line[2].split('x')
    destination = [int(x) for x in destination]
    # Move contents of source to r1
    content = memory[source[0]][source[1]].pop()
    registers[0].append(content)
    # Move contents of r1 to destinaton
    content = registers[0].pop()
    if memory[destination[0]][destination[1]]:
        memory[source[0]][source[1]].append(content)
        print('\nAddressError: address {} is not empty - DEL address before appending - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
        # os._exit(1)
        # raise ValueError()
        return
    memory[destination[0]][destination[1]].append(content)

def exec_move():
    # Fetch source and destination
    source = line[1].split('x')
    source = [int(x) for x in source]
    destination = line[2].split('x')
    destination = [int(x) for x in destination]
    # Move contents of source to r1
    content = memory[source[0]][source[1]].pop()
    registers[0].append(content)
    # Move contents of r1 to destinaton
    content = registers[0].pop()
    memory[destination[0]][destination[1]] = [content]

def add():
    if 'x' in line[1]:
        a = line[1].split('x')
        a = [int(x) for x in a]
        try:
            a = memory[a[0]][a[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        a = float(line[1])

    if 'x' in line[2]:
        b = line[2].split('x')
        b = [int(x) for x in b]
        try:
            b = memory[b[0]][b[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        b = float(line[2])

    # Move variables to r2 and r3
    registers[1].append(a)
    registers[2].append(b)
    # Add variables and move result to r4
    registers[3].append(registers[1].pop() + registers[2].pop())
    content = registers[3].pop()
    try:
        address = line[3].split('x')
        address = [int(x) for x in address]
        if memory[address[0]][address[1]]:
            print('\nAddressError: address {} is not empty - DEL address before appending - error occured on line {} "{}"'.format(line[3], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
        memory[address[0]][address[1]].append(content)
        print('\n{}'.format(content))
        return content
    except IndexError:
        print('\n{}'.format(content))
        return content

def sub():
    if 'x' in line[1]:
        a = line[1].split('x')
        a = [int(x) for x in a]
        try:
            a = memory[a[0]][a[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        a = float(line[1])

    if 'x' in line[2]:
        b = line[2].split('x')
        b = [int(x) for x in b]
        try:
            b = memory[b[0]][b[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        b = float(line[2])

    # Move variables to r2 and r3
    registers[1].append(a)
    registers[2].append(b)
    # Add variables and move result to r4
    registers[3].append(registers[1].pop() - registers[2].pop())
    content = registers[3].pop()
    try:
        address = line[3].split('x')
        address = [int(x) for x in address]
        if memory[address[0]][address[1]]:
            print('\nAddressError: address {} is not empty - DEL address before appending - error occured on line {} "{}"\n'.format(line[3], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
        memory[address[0]][address[1]].append(content)
        print('\n{}'.format(content))
        return content
    except IndexError:
        print('\n{}'.format(content))
        return content

def mul():
    if 'x' in line[1]:
        a = line[1].split('x')
        a = [int(x) for x in a]
        try:
            a = memory[a[0]][a[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        a = float(line[1])

    if 'x' in line[2]:
        b = line[2].split('x')
        b = [int(x) for x in b]
        try:
            b = memory[b[0]][b[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        b = float(line[2])

    # Move variables to r2 and r3
    registers[1].append(a)
    registers[2].append(b)
    # Add variables and move result to r4
    registers[3].append(registers[1].pop() * registers[2].pop())
    content = registers[3].pop()
    try:
        address = line[3].split('x')
        address = [int(x) for x in address]
        if memory[address[0]][address[1]]:
            print('\nAddressError: address {} is not empty - DEL address before appending - error occured on line {} "{}"'.format(line[3], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
        memory[address[0]][address[1]].append(content)
        print('\n{}'.format(content))
        return content
    except IndexError:
        print('\n{}'.format(content))
        return content

def div():
    if 'x' in line[1]:
        a = line[1].split('x')
        a = [int(x) for x in a]
        try:
            a = memory[a[0]][a[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        a = float(line[1])

    if 'x' in line[2]:
        b = line[2].split('x')
        b = [int(x) for x in b]
        try:
            b = memory[b[0]][b[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        b = float(line[2])

    # Move variables to r2 and r3
    registers[1].append(a)
    registers[2].append(b)
    # Add variables and move result to r4
    try:
        registers[3].append(registers[1].pop() / registers[2].pop())
        content = registers[3].pop()
    except ZeroDivisionError:
        print('\nDivisionError: Cannot divide by 0')
        return
    try:
        address = line[3].split('x')
        address = [int(x) for x in address]
        if memory[address[0]][address[1]]:
            print('\nAddressError: address {} is not empty - DEL address before appending - error occured on line {} "{}"'.format(line[3], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
        memory[address[0]][address[1]].append(content)
        print('\n{}'.format(content))
        return content
    except IndexError:
        print('\n{}'.format(content))
        return content

def exponent():
    if 'x' in line[1]:
        a = line[1].split('x')
        a = [int(x) for x in a]
        try:
            a = memory[a[0]][a[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        a = float(line[1])

    if 'x' in line[2]:
        b = line[2].split('x')
        b = [int(x) for x in b]
        try:
            b = memory[b[0]][b[1]][0]
        except IndexError:
            print('\nAddressError: address {} is empty - error occured on line {} "{}"'.format(line[2], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
    else:
        b = float(line[2])

    # Move variables to r2 and r3
    registers[1].append(a)
    registers[2].append(b)
    # Add variables and move result to r4
    registers[3].append(registers[1].pop() ** registers[2].pop())
    content = registers[3].pop()
    try:
        address = line[3].split('x')
        address = [int(x) for x in address]
        if memory[address[0]][address[1]]:
            print('\nAddressError: address {} is not empty - DEL address before appending - error occured on line {} "{}"'.format(line[3], index+1, ' '.join(line)))
            # os._exit(1)
            # raise ValueError()
            return
        memory[address[0]][address[1]].append(content)
        print('\n{}'.format(content))
        return content
    except IndexError:
        print('\n{}'.format(content))
        return content

def delete():
    content = line[1].split('x')
    content = [int(x) for x in content]
    if memory[content[0]][content[1]]:
        memory[content[0]][content[1]].pop()
    else:
        print('\nAddressWarning: address {} is empty - warning occured on line {} "{}"'.format(line[1], index+1, ' '.join(line)))

while True:

    code = input('\nasmb> ')

    code = code.split('\n')
    code = [x.split() for x in code]

    for index, line in enumerate(code):
        if line:

            if line[0] == 'GET':
                get()

            if line[0] == 'MOV':
                move()

            if line[0] == 'EXEC_MOV':
                exec_move()

            if line[0] == 'ADD':
                content = add()

            if line[0] == 'SUB':
                content = sub()

            if line[0] == 'MUL':
                content = mul()

            if line[0] == 'DIV':
                content = div()

            if line[0] == 'EXP':
                content = exponent()

            if line[0] == 'DEL':
                delete()

            if line[0] == 'INS':
                insert()

            if line[0] == 'EXEC_INS':
                exec_insert()

            if line[0] == 'MEM':
                for memory_line in memory:
                    print('\n{}'.format(memory_line))

            if line[0] == 'REG':
                print('\n{}'.format(registers))

            if line[0] not in actions:
                print('\nSyntaxError: No such action as {}'.format(line[0]))
