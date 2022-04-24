from pip._vendor.distlib.compat import raw_input
import matplotlib.pyplot as plt
from datetime import datetime
from guppy import hpy
import networkx as nx
import random

h = hpy()

def rand_code(length):
    key1 = ""
    for i in range(length):
        temp = str(random.randint(0, 1))
        key1 += temp
    return (key1)

def send_over_BSC(code,prob):
    code=list(code)
    for i in range(len(code)):
        num=random.randint(0,100)
        if num<prob*100:
            if code[i]=='0':
                code[i]='1'
            else:
                code[i]='0'
    recieved = ''
    for i in code:
        recieved += i
    return recieved

def difference(c1,c2):
    different=0
    for i in range(len(c1)):
        if c1[i]!=c2[i]:
            different+=1
    return different

class Convolutional:
    def moveOnMachine(self, state, input):
        nextState = 0
        output = ""
        if (state == 0 and input == "0"):
            nextState = 0
            output = "00"
        elif (state == 0 and input == "1"):
            nextState = 2
            output = "11"
        elif (state == 1 and input == "0"):
            nextState = 0
            output = "10"
        elif (state == 1 and input == "1"):
            nextState = 2
            output = "01"
        elif (state == 2 and input == "0"):
            nextState = 1
            output = "11"
        elif (state == 2 and input == "1"):
            nextState = 3
            output = "00"
        elif (state == 3 and input == "0"):
            nextState = 1
            output = "01"
        else:
            nextState = 3
            output = "10"
        return (nextState, output)

    def encode(self, input):
        i = 0
        state = 0
        ans = ''
        while (i < len(input)):
            state, output = self.moveOnMachine(state, input[i])
            ans = ans + output
            i = i + 1
        return ans

    def constructPath(self, path, index):
        code = ""
        length = len(path[0])
        thisState = index
        for i in range(length - 1, -1, -1):
            if (thisState == 0):
                code = code + "0"
            elif (thisState == 1):
                code = code + "0"
            elif (thisState == 2):
                code = code + "1"
            else:
                code = code + "1"
            if (i == -1):
                thisState = 0
            else:
                thisState = path[thisState][i]

        return (code[::-1])

    def decode(self, input):
        currentPM = [None] * 4
        nextPM = [None] * 4
        path = [[0 for x in range(int(len(input) / 2))] for y in range(4)]
        currentPM[0] = 0
        currentPM[1] = float("inf")
        currentPM[2] = float("inf")
        currentPM[3] = float("inf")

        i = 0
        while (i < len(input)):
            str = input[i: i + 2]
            half=int(i/2)
            if (str == '00'):
                if (currentPM[0] < currentPM[1] + 1):
                    nextPM[0] = currentPM[0]
                    path[0][half] = 0
                else:
                    nextPM[0] = currentPM[1] + 1
                    path[0][half] = 1

                if (currentPM[2] + 2 < currentPM[3] + 1):
                    nextPM[1] = currentPM[2] + 2
                    path[1][half] = 2
                else:
                    nextPM[1] = currentPM[3] + 1
                    path[1][half] = 3

                if (currentPM[0] + 2 < currentPM[1] + 1):
                    nextPM[2] = currentPM[0] + 2
                    path[2][half] = 0
                else:
                    nextPM[2] = currentPM[1] + 1
                    path[2][half] = 1

                if (currentPM[2] < currentPM[3] + 1):
                    nextPM[3] = currentPM[2]
                    path[3][half] = 2
                else:
                    nextPM[3] = currentPM[3] + 1
                    path[3][half] = 3
            ###############################

            elif (str == '01'):
                if (currentPM[0] + 1 < currentPM[1] + 2):
                    nextPM[0] = currentPM[0] + 1
                    path[0][half] = 0
                else:
                    nextPM[0] = currentPM[1] + 2
                    path[0][half] = 1

                if (currentPM[2] + 1 < currentPM[3]):
                    nextPM[1] = currentPM[2] + 1
                    path[1][half] = 2
                else:
                    nextPM[1] = currentPM[3]
                    path[1][half] = 3

                if (currentPM[0] + 1 < currentPM[1]):
                    nextPM[2] = currentPM[0] + 1
                    path[2][half] = 0
                else:
                    nextPM[2] = currentPM[1]
                    path[2][half] = 1

                if (currentPM[2] + 1 < currentPM[3] + 2):
                    nextPM[3] = currentPM[2] + 1
                    path[3][half] = 2
                else:
                    nextPM[3] = currentPM[3] + 2
                    path[3][half] = 3
            ###############################

            elif (str == '10'):
                if (currentPM[0] + 1 < currentPM[1]):
                    nextPM[0] = currentPM[0] + 1
                    path[0][half] = 0
                else:
                    nextPM[0] = currentPM[1]
                    path[0][half] = 1

                if (currentPM[2] + 1 < currentPM[3] + 2):
                    nextPM[1] = currentPM[2] + 1
                    path[1][half] = 2
                else:
                    nextPM[1] = currentPM[3] + 2
                    path[1][half] = 3

                if (currentPM[0] + 1 < currentPM[1] + 2):
                    nextPM[2] = currentPM[0] + 1
                    path[2][half] = 0
                else:
                    nextPM[2] = currentPM[1] + 2
                    path[2][half] = 1

                if (currentPM[2] + 1 < currentPM[3]):
                    nextPM[3] = currentPM[2] + 1
                    path[3][half] = 2
                else:
                    nextPM[3] = currentPM[3]
                    path[3][half] = 3
            #########################################
            elif (str == "11"):
                if (currentPM[0] + 2 < currentPM[1] + 1):
                    nextPM[0] = currentPM[0] + 2
                    path[0][half] = 0
                else:
                    nextPM[0] = currentPM[1] + 1
                    path[0][half] = 1

                if (currentPM[2] < currentPM[3] + 1):
                    nextPM[1] = currentPM[2]
                    path[1][half] = 2
                else:
                    nextPM[1] = currentPM[3] + 1
                    path[1][half] = 3

                if (currentPM[0] < currentPM[1] + 1):
                    nextPM[2] = currentPM[0]
                    path[2][half] = 0
                else:
                    nextPM[2] = currentPM[1] + 1
                    path[2][half] = 1

                if (currentPM[2] + 2 < currentPM[3] + 1):
                    nextPM[3] = currentPM[2] + 2
                    path[3][half] = 2
                else:
                    nextPM[3] = currentPM[3] + 1
                    path[3][half] = 3

            i = i + 2
            currentPM = nextPM[:]

        index = currentPM.index(min(currentPM))
        #print("Index is ",index)
        #print("path is",path)
        #print('min error = ', min(currentPM))
        return (self.constructPath(path, index))


def main():
    startTime = datetime.now().timestamp()
    c = Convolutional()
    lengths=[1000]
    for length in lengths:
        print('Input length is:',length)
        input=rand_code(length)
        ori_i=input
        print('Input code is: ',input)

        code = c.encode(input)
        ori_enc=code
        print('Encoded code is: ', code)

        x_axis=[]
        noted_error=[]
        memory_bits=[]
        time_taken_in_this=[]
        for i in range(0,10,1):
            code=ori_enc
            input=ori_i
            i=i/100
            p=i
            x_axis.append(i)
            print("probability of error is:",p)
            code=send_over_BSC(code,p)
            print('recieved code is: ',code)

            decoded= c.decode(code)
            print('decoded code is: ', decoded)

            diff=difference(input,decoded)
            print("Number of different bits is: ",diff)
            per=diff/length
            noted_error.append(per)
            print('Percentage error is:',per)

            time_taken=datetime.now().timestamp() - startTime
            time_taken_in_this.append(time_taken)
            print("Time taken is: ",time_taken)
            x = h.heap()
            num_nodes = 1000
            num_edges = 5000
            G = nx.gnm_random_graph(num_nodes, num_edges)
            m_con=x.size
            memory_bits.append(m_con)
            print("Memory consumed is: ",m_con,"bits")

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
        plt.show()


if __name__ == "__main__":
    main()