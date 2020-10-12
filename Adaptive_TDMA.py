import matplotlib.pyplot as plt

print("TDMA implementation\n")

print("Step1:Select the largest frame structure of two hop neighbour nodes in an vehicular network\n")
print("Step2:If the ratio of number of nodes and number of slots pre-configured is greater than threshold_max,then double up the size of binary tree\n")
print("If the ratio of number of nodes and number of slots pre-configured is lesser  than threshold_min,then shorten up the size of binary tree\n")
print("Step3:Broadcast the frame length to every neighbouring nodes in vehicular network\n")


class newNode:
    def __init__(self, data):
        self.val = data
        self.left = None
        self.right = None


def doubleTree(root):

    if root is None:
        return

    doubleTree(root.left)
    doubleTree(root.right)

    oldleft = root.left
    root.left = newNode(root.val)
    root.left.left = oldleft


def insertLevelOrder(arr, root, i, n):

    
    if i < n:
        temp = newNode(arr[i])
        root = temp

        # insert left child
        root.left = insertLevelOrder(arr, root.left,
                                     2 * i + 1, n)

        # insert right child
        root.right = insertLevelOrder(arr, root.right,
                                      2 * i + 2, n)
    return root


def printKDistant(maintree, k):

    if maintree is None:
        return
    if k == 0:
        print(maintree.val,)
    else:
        printKDistant(maintree.left, k-1)
        printKDistant(maintree.right, k-1)


def removeShortPathNodesUtil(root, level, k):


    if (root == None):
        return None


    root.left = removeShortPathNodesUtil(root.left,
                                         level + 1, k)
    root.right = removeShortPathNodesUtil(root.right,
                                          level + 1, k)


    if (root.left == None and
            root.right == None and level < k):
        return None

    
    return root




def removeShortPathNodes(root, k):
    pathLen = 0
    return removeShortPathNodesUtil(root, 1, k)




def printLevelOrder(root):

    
    if root is None:
        return

    q = []

    
    q.append(root)
    max_of_slots = 1
    while q:
        count = len(q)
        no_of_slots = 0
        
        while count > 0:
            temp = q.pop(0)
            print(temp.val, end=' ')
            print("|___|", end=' ')

            if temp.left:
                q.append(temp.left)
            if temp.right:
                q.append(temp.right)
            if no_of_slots >= max_of_slots:
                max_of_slots = no_of_slots

            count -= 1
            no_of_slots += 1
        print("No of slots found in each time-frame:", no_of_slots)
        print(' ')
    print("Printing the largest number of time slots frame structure in the network:")
    print(max_of_slots+1)


def leafDelete(root):
    if root == None:
        return None
    if root.left == None and root.right == None:
        return None
    root.left = leafDelete(root.left)
    root.right = leafDelete(root.right)

    return root



fig1=plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.grid(True)
ax1.set_xlim([0,550])
ax1.ticklabel_format(useOffset=False)


k = int(input("Enter the number of Vehicle slots pre-allocated for nodes:\n"))
array=[]
for i in range(0,k):
    array.append(i)
roots=None
result=insertLevelOrder(array,roots,0,k)
printLevelOrder(result)
n = int(input("Enter the number of Vehicle nodes that can enter the network:\n"))

arr = []
threshold_max = 1
threshold_min = 0.5
for i in range(0, n):
    ele = int(input())
    arr.append(ele)
print("Vehicle id's are:", arr)


root = None
root = insertLevelOrder(arr, root, 0, n)

print("Printing TWO HOP NEIGHBOURS of all Vehicle nodes in the network\n")
printKDistant(root, 2)

print("Printing each level of Vehicle nodes in binary tree implementation\n")
printLevelOrder(root)
t = int(input("Enter the path level:\n"))
if n/k >= threshold_max:
    print("Double up the binary tree")
    doubleTree(root)
    printLevelOrder(root)

elif n/k <= threshold_min:
    print("Shorten up the slot structure")
    res = removeShortPathNodes(result,t)
    printLevelOrder(res)
    ld=leafDelete(result)
    printLevelOrder(ld)
    
else:
    printLevelOrder(root)


N=list(range(10,50,10))
K=list(range(20,100,20))
ax1.set_title('Proportion of nodes acquiring the slots')
ax1.set_xlabel('Number of nodes')
ax1.set_ylabel('Number of slots')
ax1.scatter(N,K)
ax1.plot(N,K,label='number of neighbors')
legend = ax1.legend(loc='upper center', shadow=True)

N=list(range(20,100,20))
K=list(range(10,50,10))
ax1.set_title('Proportion of nodes acquiring the slots')
ax1.set_xlabel('Number of nodes')
ax1.set_ylabel('Number of slots')
ax1.scatter(N,K)
ax1.plot(N,K,label='number of neighbors')
legend = ax1.legend(loc='upper center', shadow=True)


plt.show()
print('Probability that the node successfully occupied a slot')
S=pow(1-1/n,k-1)
print("Probability is",S)
