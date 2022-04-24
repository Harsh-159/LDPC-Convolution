import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message
import random
import matplotlib.pyplot as plt
from datetime import datetime
from guppy import hpy
import networkx as nx

h = hpy()

def send_over_BSC(code,prob):
    code=list(code)
    for i in range(len(code)):
        num=random.randint(0,100)
        if num<prob*100:
            if code[i]==-1:
                code[i]=1
            else:
                code[i]=-1
    return np.array(code)

def rand_code(length):
    key1 = []
    for i in range(length):
        temp = random.randint(0, 1)
        key1.append(temp)
    return np.array(key1)

def difference(c1,c2):
    different=0
    for i in range(len(c1)):
        if c1[i]!=c2[i]:
            different+=1
    return different

startTime = datetime.now().timestamp()

n = 2000
d_v = 2
d_c = 4
snr = 2000
H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
ori_H=H
ori_G=G
print(G)
k = G.shape[1]
ori_k=k
#after making matrices v is taken with fixed length
x_axis=[]
noted_error=[]
memory_bits=[]
time_taken_in_this=[]
for i in range(0,200,2):
    p=i/1000
    x_axis.append(p)
    k=ori_k
    G=ori_G
    H=ori_H
    v = rand_code(k)
    y = encode(G, v, snr)
    print(y)
    y=send_over_BSC(y,p)
    print(y)

    d = decode(H, y, snr)
    print(d)
    x = get_message(G, d)
    #assert abs(x - v).sum() == 0
    diff=difference(v,x)
    print("Number of different bits is: ", diff)
    per=diff/n
    noted_error.append(per)

    time_taken = datetime.now().timestamp() - startTime
    time_taken_in_this.append(time_taken)
    print("Time taken is: ", time_taken)

    x = h.heap()
    num_nodes = 1000
    num_edges = 5000
    G = nx.gnm_random_graph(num_nodes, num_edges)
    m_con = x.size
    memory_bits.append(m_con)
    print("Memory consumed is: ", m_con, "bits")

plt.subplot(1, 3, 1)
plt.plot(x_axis,noted_error)
plt.xlabel("Actual error probability")
plt.ylabel("Noted error probability")

plt.subplot(1, 3, 2)
plt.plot(x_axis, memory_bits)
plt.xlabel("Actual error probability")
plt.ylabel("Memory bits consumed")

plt.subplot(1, 3, 3)
plt.plot(x_axis, time_taken_in_this)
plt.xlabel("Actual error probability")
plt.ylabel("Time taken")
plt.show()
