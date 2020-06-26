import re
import os
import math
from collections import defaultdict
import numpy as np
import random 
from random import choice, sample
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sympy
import subprocess
from sympy.logic import SOPform
from sympy import *
from sympy.logic.boolalg import to_cnf, to_dnf
from datetime import datetime
random.seed(5)

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def uniqify_data(listA, listB):
    checked = []
    dupl = []

    for ele in listA:
        if ele not in checked and listA.count(ele) > 1: 
            dupl = list_duplicates_of(listA, ele)
            checked.append(ele)
            if not(all(x==listB[0] for x in dupl)): # checking whether multiple minterms have different labels
                listA = np.delete(listA, dupl).tolist()
            else:
                listA = np.delete(listA, dupl[1:]).to_list()

def fetch_data(filepath):
    inputs = 0
    outputs = 0
    features = []
    labels = []
    with open(filepath,'r') as f:
        for line in f.readlines():
            if line.startswith('.i '):
                inputs = int(line.split(" ")[1])
            elif line.startswith('.o '):
                outputs = int(line.split(" ")[1])
            elif line[0] in ['0','1']:
                x, y = tuple(line.split(" "))
                uniqify_data(x,y)
                features.append([int(ch) for ch in x])
                labels.append(int(y))
    return inputs, outputs, np.array(features), np.array(labels)



class Table:
    def __init__(self, inputs):
        self.inputs = inputs
        self.inputs.sort()
        self.table_size = 2**len(inputs) 
        self.pos = defaultdict(int)
        self.negs = defaultdict(int)
    
    def indexing(self, vec):
        ind = 0
        pos = 1
        try:
            vec_sel = [vec[i] for i in self.inputs]
            for bit in vec_sel[::-1]:
                if bit:
                    ind += pos
                pos *= 2
        except:
            print(self.inputs,vec)
            raise Exception
        return ind
    
    def train(self, X, y):
        for i in range(len(y)):
            x = X[i]
            label = y[i]
            ind = self.indexing(x)
            if label == 1:
                self.pos[ind] += 1
            else:    
                self.negs[ind] += 1
    
    def predict(self, x):
        ind = self.indexing(x)
        if self.pos[ind] > self.negs[ind]:
            return 1
        else:
            return 0
    
    def minterms(self):
        terms = []
        for term in self.pos.keys():
            if self.pos[term] > self.negs[term]:
                bits = [int(b) for b in list(bin(term)[2:].zfill(len(self.inputs)))]
                terms.append(bits)
        return terms
    
    def dont_cares(self):
        terms = []
        for term in range(self.table_size):
            if self.pos[term] == self.negs[term]:
                bits = [int(b) for b in list(bin(term)[2:].zfill(len(self.inputs)))]
                terms.append(bits)
        return terms

class Network:
    def __init__(self, inputs, nodes, connections, flow = 'random'):
        self.inputs = inputs
        self.nodes = nodes
        self.connections = connections
        
        self.layerranges = [inputs] + nodes
        self.layers = [None]*len(nodes)
        
        positions = [set() for _ in range(len(nodes)+1)]
        positions[-1].add(nodes[-1]-1)
        
        for ll in range(len(nodes)-1,-1,-1):
            self.layers[ll] = [None for _ in range(nodes[ll])]
            for tt in range(len(self.layers[ll])):
                if tt in positions[ll+1]:
                    if (flow != 'random'):
                        available_inputs = list(range(self.layerranges[ll]))
                        #if ll == 0:
                        available_inputs = list(set(available_inputs) - positions[ll])
                        if len(available_inputs) > connections[ll]:
                            randinputs = sample(available_inputs,connections[ll])
                    else:
                        randinputs = sample(range(self.layerranges[ll]),connections[ll])
                    for x in randinputs:
                        positions[ll].add(x)
                    self.layers[ll][tt] = Table(randinputs)
        
    def train(self, X, y):
        X_ = X
        prev_y = {}
        next_y = {}
        for i,layer in enumerate(self.layers):
            for tt in range(len(layer)):
                if layer[tt] is not None:
                    if X_ is None:
                        temp_X = np.ones((len(X),self.layerranges[i]), dtype= bool)*-1
                        for conn in layer[tt].inputs:
                            temp_X[:,conn] = np.array(prev_y[conn])
                        X_ = temp_X.tolist()
                    layer[tt].train(X_, y)
                    next_y[tt] = [layer[tt].predict(x) for x in X_]
            X_ = None
            prev_y = next_y
            next_y = {}
            print("{} layer trained".format(i))
    
    def predict(self, X):
        X_ = X
        prev_y = {}
        next_y = {}
        for i,layer in enumerate(self.layers):
            for tt in range(len(layer)):
                if layer[tt] is not None:
                    if X_ is None:
                        temp_X = np.ones((len(X),self.layerranges[i]))*-1
                        for conn in layer[tt].inputs:
                            temp_X[:,conn] = np.array(prev_y[conn])
                        X_ = temp_X.tolist()
                    next_y[tt] = [layer[tt].predict(x) for x in X_]
            X_ = None
            prev_y = next_y
            next_y = {}
        return prev_y[0]
    
def build_sympy_expr(net, ip):
    ip_vars = ['ip_{}'.format(i) for i in range(ip)]
    ip_syms = symbols(" ".join(ip_vars))
    syms = {i:x for i,x in enumerate(ip_syms)}
    for i, layer in enumerate(net.layers):
        expr = dict()
        for j, neuron in enumerate(layer):
            if neuron is not None:
                reqd_syms = [syms[ip_num] for ip_num in neuron.inputs]
                expr[j] = SOPform(reqd_syms,neuron.minterms(), neuron.dont_cares())
        syms = expr
    return ip_vars, ip_syms, syms[0]

def sympy_acc(ip_syms, sp_expr, X, y):
    y_pred = []
    for i in range(X.shape[0]):
        if i%1000 == 0:
            print("Evaluated {} vectors".format(i))
        x = list(X[i] == 1)
        sp_inputs = {ip_sym:x[j] for j,ip_sym in enumerate(ip_syms)}
        y_sp = int(bool(sp_expr.subs(sp_inputs)))
        y_pred.append(y_sp)
    return accuracy_score(y, y_pred)

def remove_dont_care_elements( wire ): 
    literal = wire.split("&")
    tmp = []
    for i,term in enumerate(literal):
        if '~' in term: 
            without_tilda = term.replace('~','')
            if term in literal:
                if without_tilda in literal:
                    wire = [] 
                    return False
    return True
                             

def write_ver(expression, file_num, ip, verilog_file):
    print ("Verilog conversion for expresion =", expression)
    ip_vars = ['ip_{}'.format(i) for i in range(ip)]
    wire    = []

    dest_file = open(verilog_file, 'w+')
    dest_file.write('module (')

    exp_arr = str(expression).split("|")
    
    for term in exp_arr:
        import re
        term = re.sub('[()]','', term) 
        #if (remove_dont_care_elements(term)):
        #    print("dont care not removed for ", term)
        wire.append(term)
        #else:
        #    print("dont care removed for ", term)


    print("No of wires = ", int(len(wire)))
    if (int ( len( wire )) % 100  == 99 ):
        more_wire = int(len(wire) / 100)
        print("more_wire with 99 ",more_wire)
    else: 
        more_wire = int(len(wire) / 100) + 1
        print("more_wire",more_wire)
    wire_vars = ['w_{}'.format(i) for i in range(len(wire))]
    wire_syms = symbols(", ".join(wire_vars))
    dest_file.write(",".join(ip_vars))
    dest_file.write(", o1);\n")
    dest_file.write("input " + ", ".join(ip_vars) + ";\n")
    dest_file.write("output o1;\n")
    dest_file.write("wire " + ", ".join(wire_vars) + ";\n")
    new_wire = []

    for i in range(more_wire):
        start = i*100
        stop  = ((i + 1) * 100)  if ((i + 1) * 100) < len(wire)  else len(wire)  
        if stop > start:
                term = " | ".join(wire_vars[start:stop])
        new_wire.append(term)


    dest_file.write("\n")
    if (len(str(expression).split()) == 1):
        if (str(expression).strip() == 'True'):
            dest_file.write("assign o1 = 1'b1" + ";\n" )
            dest_file.write('endmodule\n')
        elif (str(expression).strip() == 'False'):
            dest_file.write("assign o1 = 1'b0" +  ";\n" )
            dest_file.write('endmodule\n')
        else:
            dest_file.write("assign o1 = " + str(expression).strip() + ";\n" )
            dest_file.write('endmodule\n')

    else:
        if (len(wire) < 100 ):
            try:
               for i,terms in enumerate(wire):
                  dest_file.write("assign " + str(wire_syms[i]) + " = " + terms + ";\n")
            except:
               print("ex{:02d} fails due to symbol issue for len(wire) < 100 \n".format(file_num))
            o1 = " | ".join(wire_vars)
        else:
            new_wire_vars = ['nw_1{}'.format(i) for i in range(len(new_wire))]
            new_wire_syms = symbols(", ".join(new_wire_vars))
            dest_file.write("wire " + ", ".join(new_wire_vars) + ";\n")
            try:
                for i,terms in enumerate(wire):
                    dest_file.write("assign " + str(wire_syms[i]) + " = " + terms + ";\n")
                for i,terms in enumerate(new_wire):
                    dest_file.write("assign " + str(new_wire_syms[i]) + " = " + terms + ";\n")
            except:
                print("ex{:02d} fails due to symbol issue \n".format(file_num))
            o1 = " | ".join(new_wire_vars)
    
        dest_file.write("assign o1 = " + str(o1) +  ";\n" )
        dest_file.write('endmodule\n')
        dest_file.close()
        
        # Removing occurance of ~~
        with open(verilog_file) as f:
            newText=f.read().replace('~~', '') 
        with open(verilog_file, 'w+') as f:
            f.write(newText)


def call_abc(file_num, verilog_file, aig_file):
    abc_call =  "abc -q " + "\"read " + verilog_file + ";strash; fraig; balance; compress2rs;write_aiger " + aig_file + ";&read " + aig_file + "; ps;&mltest " + "validation_data/ex{:02d}.valid.pla".format(file_num) + "\""
    print(abc_call)
    c_str = "Correct = "
    n_str = "Naive"
    encoding = 'utf-8'
    import re
    try:
        cmd = subprocess.Popen(abc_call, stdout=subprocess.PIPE, shell=True)
        cmd_out, cmd_err = cmd.communicate()
        cmd_str = cmd_out.decode(encoding)
        print(cmd_str)
        result      = re.search('%s(.*)%s' % (c_str, n_str), cmd_str).group(1)
        naive       = re.search('%s(.*)' % (n_str), cmd_str).group(1)
        and_gate    = re.search('%s(.*)%s' % ("and =", "lev"), cmd_str).group(1)

        print("Correct = ", result )
        print("Naive guess = ", naive)
        print("and_gate = ", and_gate)
        print(cmd_str)
        return result, naive, and_gate
    except:
        print(cmd_str)
        result      = '---'
        naive       = '---'
        and_gate    = '---'
        return result, naive, and_gate

def call_native_abc(file_num, verilog_file, aig_file):
    abc_call =  "abc -q " + "\"read train_data/ex{:02d}.train.pla;".format(file_num) + "strash; write_aiger temp/ex{:02d}.aig;".format(file_num) + "&read temp/ex{:02d}.aig;ps;&mltest ".format(file_num) + "validation_data/ex{:02d}.valid.pla".format(file_num) + "\""
    print(abc_call)
    c_str = "Correct = "
    n_str = "Naive"
    encoding = 'utf-8'
    import re
    try:
        cmd = subprocess.Popen(abc_call, stdout=subprocess.PIPE, shell=True)
        cmd_out, cmd_err = cmd.communicate()
        cmd_str = cmd_out.decode(encoding)
        result      = re.search('%s(.*)%s' % (c_str, n_str), cmd_str).group(1)
        naive       = re.search('%s(.*)' % (n_str), cmd_str).group(1)
        and_gate    = re.search('%s(.*)%s' % ('and = ', 'lev'), cmd_str).group(1)
        print( "cmd_str", cmd_str)
        print("Correct = ", result )
        print("Naive guess = ", naive)
        print("and_gate = ", and_gate)
        return result, naive, and_gate
    except:
        print(cmd_str)
        result      = '---'
        naive       = '---'
        and_gate    = '---'
        return result, naive, and_gate

def aag_pipeline(file_num, layers=[16,8,1], connections=[8,4,1]): 
    ip, op, X_train, y_train = fetch_data('train_data/ex{:02d}.train.pla'.format(file_num))
    _,_, X_val, y_val = fetch_data('validation_data/ex{:02d}.valid.pla'.format(file_num))
    X_val, X_tr, y_val, y_tr = train_test_split(X_val, y_val, test_size = 0.4)

    X_train = np.vstack((X_train, X_tr))
    y_train = np.array(list(y_train) + list(y_tr))
    print("Input dimension: ",ip)

    verilog_file    = verilog_dir + '/ex{:02d}.v'.format(file_num)
    aig_file        = aig_dir     + '/ex{:02d}.aig'.format(file_num)

    small_ckt = False
    n_acc, n_naive, n_gate = call_native_abc(file_num, verilog_file, aig_file)
    if (int(n_gate) < 5000):
        print("no training needed")
        small_ckt = True
    
    layers = []
    connections = []
    if (ip > 16):
        val = 2 ** (math.ceil(math.log(ip,2)))
        #layers.append(val)
        while (int(val/8) > 32):
            val = int(val/8)
            layers.append(val)
    
    connections = [8] * len(layers)
    layers.extend([16,8,1])
    connections.extend([8,4,4])
    #connections = [4] * len(layers)
    #layers = [16,8,8,4,1]
    #layers.extend([ip, ip/2, 4, 1])
    #connections = [4] * len(layers)
    print("layers", layers)
    print("connections", connections)
    flow = 'random'
    net     = Network(ip, layers, connections, flow )

    print("Training network...", flush=True)
    net.train(X_train,y_train)

    y_pred = np.array(net.predict(X_val))
    print("Network accuracy: ",accuracy_score(y_val, y_pred))

    print("Constructing sympy expression...")
    ip_vars, ip_syms, sp_expr = build_sympy_expr(net, ip)

    write_ver(sp_expr,file_num,ip, verilog_file)

    each_ex = []
    print("ABC accuracy....", flush=True)
    acc, naive, gate = call_abc(file_num, verilog_file, aig_file)
    if (small_ckt):
        each_ex = ["ex{:02d}".format(file_num), accuracy_score(y_val, y_pred), n_acc, n_naive, n_gate, acc, naive, gate, 'small_ckt']
    else:
        each_ex = ["ex{:02d}".format(file_num), accuracy_score(y_val, y_pred), n_acc, n_naive, n_gate, acc, naive, gate]

    print(each_ex)
    final_list.append(each_ex)

now = datetime.now()
month   = now.strftime("%m")
day     = now.strftime("%d")
hour    = now.strftime("%H")
minute  = now.strftime("%M")
verilog_dir     = "verilog_data_" + hour + minute 
aig_dir         =  "aig_data_" + hour + minute 
try:
    os.mkdir(verilog_dir)
    os.mkdir(aig_dir)
except OSError:
    print ("Creation of the directory failed %s " % verilog_dir )
else:
    print ("Successfully created the directory %s " % verilog_dir )

   
final_list = []
title = ['example', 'net_cc', 'n_abc_acc', 'n_abc_naive', 'n_abc_gate_count', 'abc_acc', 'naive', 'gate_count' ]
final_list.append(title)
#for i in range(91,92):
for i in range(100):
    print("i = ", i)
    print("processing ex{:02d}".format(i))
    print("-----------")
    aag_pipeline(i) #, [32, 32, 32, 16, 16, 8, 1], [8, 8, 4, 4, 2, 2, 1] )
    print("-----------")


import csv
print(final_list)
with open("eda_output_" + day + "_" + month + hour + minute + ".csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(final_list)


