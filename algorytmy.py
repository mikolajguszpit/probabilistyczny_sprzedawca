import numpy as np
import math
import time
import csv
taken_bruteforce = np.array([])
taken_greedy = np.array([])
taken_dynamic = np.array([])
def removeRange(array,point):
    x = len(array)
    while(x!=point):
        array = np.delete(array,len(array)-1)
        x = len(array)
    return array

def bruteforce(dataset,what_to_maximize,W,n):
    global taken_bruteforce
    if(n==0 or W==0):
        return 0
    elif(dataset[n-1][1]>W):
        return bruteforce(dataset,what_to_maximize,W,n-1)
    else:
        preTookSize = len(taken_bruteforce)
        x = (dataset[n-1][what_to_maximize] + bruteforce(dataset,what_to_maximize,W-dataset[n-1][1],n-1))

        preLeftSize = len(taken_bruteforce)
        y = bruteforce(dataset,what_to_maximize,W,n-1)
        if(x > y):
            if(len(taken_bruteforce) > preLeftSize):
                taken_bruteforce = removeRange(taken_bruteforce,preLeftSize)
            taken_bruteforce = np.append(taken_bruteforce,n-1)
            return x
        else:
            if(preLeftSize > preTookSize):
                for i in range(preLeftSize-preTookSize):
                    taken_bruteforce = np.delete(taken_bruteforce,preTookSize)
            return y


def greedy(dataset,what_to_maximize,W):
    global taken_greedy
    ratio = np.empty([len(dataset),2])
    for i in range (len(dataset)):
        ratio[i][0] = i
        ratio[i][1] = dataset[i][what_to_maximize]/dataset[i][1]
    ratio = ratio[np.argsort(ratio[:, 1])]
    ratio = ratio[::-1]
    value = 0
    curW = 0
    for i in range (len(ratio)):
        if(curW + dataset[int(ratio[i][0])][1] <= W):
            curW += dataset[int(ratio[i][0])][1]
            value += dataset[int(ratio[i][0])][what_to_maximize]
            taken_greedy = np.append(taken_greedy,ratio[i][0])
    return value


def dynamic(dataset,what_to_maximize,W,n):
    global taken_dynamic
    K = np.zeros([n+1,W+1])
    for i in range (n+1):
        for w in range (W+1):
            K[i][w] = K[i-1][w]
            if(i == 0 or w == 0):
                K[i][w] = 0
            elif((w >= dataset[i-1][1]) and (K[i][w] < K[i-1][w-int(dataset[i-1][1])] + dataset[i-1][what_to_maximize])):
                K[i][w] = K[i-1][w - int(dataset[i-1][1])] + dataset[i-1][what_to_maximize]
    res = K[n][W]
    w = W
    for i in range(n, 0, -1):
        if (res <= 0):
            break
        elif (res == K[i - 1][int(w)]):
            continue
        else:
            taken_dynamic = np.append(taken_dynamic,i-1)
            res = res - dataset[i-1][what_to_maximize]
            w = w - dataset[i-1][1]

    return K[n][W]

dataset1 = np.genfromtxt("produkty_10.csv", dtype="U20,f8,f8,f8,f8", delimiter=",")
dataset2 = np.genfromtxt("produkty_20.csv", dtype="U20,f8,f8,f8,f8", delimiter=",")
dataset3 = np.genfromtxt("produkty_30.csv", dtype="U20,f8,f8,f8,f8", delimiter=",")
dataset4 = np.genfromtxt("produkty_40.csv", dtype="U20,f8,f8,f8,f8", delimiter=",")

print("Na jakim zestawie danych chcesz przeprowadzić test?")
print("[1] - produkty_10.csv, [2] - produkty_20.csv, [3] - produkty_30.csv, [4] - produkty_40.csv")

choice = int(input())

if(choice == 1):
    selected_dataset = dataset1
elif(choice == 2):
    selected_dataset = dataset2
elif(choice == 3):
    selected_dataset = dataset3
elif(choice == 4):
    selected_dataset = dataset4
else:
    print("Błąd")

print("Jaki parametr chcesz maksymalizować?")
print("[1] - cena, [2] - prawdopodobieństwo, [3] - połączenie obu")

choice = int(input())

if(choice == 1):
    selected_maximialization = 2
elif(choice == 2):
    selected_maximialization = 3
elif(choice == 3):
    selected_maximialization = 4
else:
    print("Błąd")

print("Podaj maksymalną nośność wozu sprzedawcy: ")

maxWeight = int(input())

print("Jaki algorytm chcesz przetestować?")
print("[1] - bruteforce, [2] - algorytm zachłanny, [3] - programowanie dynamiczne")

choice = int(input())

if(choice == 1):
    start = time.process_time()
    x = bruteforce(selected_dataset,selected_maximialization,maxWeight,len(selected_dataset))
    stop = time.process_time() - start
    print("Algorytm wykonał się w czasie: " + str(stop) + "s")
    print("Zmaksymalizowana wartość: "+str(x))
    print("Jeżeli sprzedawca weźmie ze sobą: ")
    for i in range(len(taken_bruteforce)):
        print(selected_dataset[int(taken_bruteforce[i])][0])
elif(choice == 2):
    start = time.process_time()
    x = greedy(selected_dataset,selected_maximialization,maxWeight)
    stop = time.process_time() - start
    print("Algorytm wykonał się w czasie: " + str(stop) + "s")
    print("Zmaksymalizowana wartość: "+str(x))
    print("Jeżeli sprzedawca weźmie ze sobą: ")
    for i in range(len(taken_greedy)):
        print(selected_dataset[int(taken_greedy[i])][0])
elif(choice == 3):
    start = time.process_time()
    x = dynamic(selected_dataset,selected_maximialization,maxWeight,len(selected_dataset))
    stop = time.process_time() - start
    print("Algorytm wykonał się w czasie: " + str(stop) + "s")
    print("Zmaksymalizowana wartość: "+str(x))
    print("Jeżeli sprzedawca weźmie ze sobą: ")
    for i in range(len(taken_dynamic)):
        print(selected_dataset[int(taken_dynamic[i])][0])
else:
    print("Błąd")