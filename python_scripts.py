##for x in range(0, 60, 4):
##	print "\tla \t$t0, output"
##	print "\tlw \t$t3, " + str(x) + "($t0)"
##	print "\tjal \tprint_register_t3"
##
##for x in range(0, 112, 8):
##	print "\taddi \t $s0, $s0, 8"
##	print "\tmove \t $a0, $s0" 
##	print "\tjal \t sort_list"
##	print "\tadd \t $a0, $s0, $zero"
##	print "\tjal \t compact"
##	print "\taddi \t $s1, $s1, 4"
##	print "\tsw \t $v0, 0($s1)"


def print_t_registers():
    regs = []
    for x in range(0,10):
        reg = '$t'+str(x)
        regs.append(reg)
        print reg
    return regs
def print_s_registers():
    regs = []
    for x in range(0, 8):
        reg = '$s'+str(x)
        regs.append(reg)
        print reg
    return regs
def print_a_registers():
    regs = []
    for x in range(0,4):
        reg = '$a'+str(x)
        regs.append(reg)
        print reg
    return regs
def print_v_registers():
    regs = []
    for x in range(0,2):
        reg = '$v'+str(x)
        regs.append(reg)
        print reg
    return regs
def print_all_registers():
    all_regs = []
    for reg in print_a_registers():
        all_regs.append(reg)
    for reg in print_t_registers():
        all_regs.append(reg)
    for reg in print_s_registers():
        all_regs.append(reg)
    for reg in print_v_registers():
        all_regs.append(reg)
    return all_regs
def print_print_functions(all_regs):
    for reg in all_regs:
        print 'print_register_'+reg.replace('$','')+':'
        print '\tsub \t$sp, $sp, 12 \t # save $a0 and $v0 on stack'
        print '\tsw \t$ra, 0($sp)'
        print '\tsw \t$v0, 4($sp)'
        print '\tsw \t$a0, 8($sp)'
        print ''
        print '\tli \t$v0, 4'
        print '\tla \t$a0, print_reg_'+reg.replace('$','')+'_str'
        print '\tsyscall'
        print '\tmove \t$a0, '+reg
        print '\tjal \tprint_register'
        print ''
        print '\tlw \t$ra, 0($sp)'
        print '\tlw \t$v0, 4($sp)'
        print '\tlw \t$a0, 8($sp)'
        print '\tadd \t$sp, $sp, 12'
        print '\tjr \t$ra'
def print_load_save_register(regs, kernel=False):
    x = 0
    size = len(regs) * 4
    p = '$sp' #p for pointer
    if kernel:
        p = '$k0'
    print '\tsub \t'+p+', '+p+', '+str(size)+'\t# adjust/substract stackpointer'
    for reg in regs:
        print '\tsw \t'+reg+', '+str(x)+'('+p+')\t# saving register '+reg
        x = x + 4
    print ''
    x = 0
    for reg in regs:
        print '\tlw \t'+reg+', '+str(x)+'('+p+')\t# loading register '+reg
        x = x + 4
    print '\taddi \t'+p+', '+p+', '+ str(size)+'\t# add/restore stackpointer'
def print_grid_data(grid_length):
    box_array = {}
    mult = 300 / grid_length
    row_length = 20 * grid_length
    array_size = row_length * grid_length
    count = 0
    string = 'map_grid:'
    for y in range(0, grid_length):
        print '\t\t###### New Row ######'
        for x in range(0, grid_length):
            string += '\t.word '+str(y * mult)
            string += ', '+str((y * mult) + (mult - 1))
            string += ', '+str(x * mult)
            string += ', '+str((x * mult) + (mult - 1))
            string += ', 0,'
            string += '\t # this is '+str(count+1)+'th element, grid location is '+str(count * 20)+'(map_grid)'
            box_array[count+1] = string
            print string
            count = count+1
            string = '\t'
    return box_array
def sort_grid_data(grid):
    data = []
    length = int(len(grid) ** .5)
    half_length =  length / 2 + length % 2
    middle_key = ((half_length - 1) * length) + half_length
    key = middle_key
    for x in range(2, length + 2, 2):
        key, r_data = walk(key, length, x, grid)
        key -= (length + 1)
        for item in r_data:
            data.append(item)
    print 'sorted_map_grid:\t'
    for string in data:
        print string
def walk(key, length, distance, grid):
    data = []
    o_key = key
    for x in range(1, distance):
        key = key + length
        data.append(grid[key])
    for x in range(1, distance):
        key = key + 1
        data.append(grid[key])
    for x in range(1, distance):
        key = key - length
        data.append(grid[key])
    for x in range(1, distance):
        key = key - 1
        data.append(grid[key])
    return o_key, data

def print_grid(length):
    for x in range(0,length):
        string = '\t'
        for y in range(1,length+1):
            string += str(length * x + y)+','
        print string

# ll_regs = print_all_registers()
# print_load_save_register(['$t0','$t1','$t2','$ra','$a0','$v0'],True)
# sort_grid_data(print_grid_data(10))
print_grid(10)



        
