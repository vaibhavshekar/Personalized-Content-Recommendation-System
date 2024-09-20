import random
import warnings
from typing import List
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
import seaborn as sn


class Node:
    def __init__(self, funny, drama, music, sadness, time_spent):
        self.funny = funny
        self.drama = drama
        self.music = music
        self.sadness = sadness
        self.time_spent = time_spent
        self.next = None


class LinkedList:
    def __init__(self, name: str):
        self.head = None
        self.name = name.lower()
        self.score_ = None
        self.model = RandomForestClassifier()
        self.df = None
        self.xtrain = None
        self.xtest = None
        self.ytrain = None
        self.ytest = None

    def append(self, funny, drama, music, sadness, time_spent):
        new_node = Node(funny, drama, music, sadness, time_spent)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def initalize(self):
        data = []
        current = self.head
        while current:
            data.append([current.funny, current.drama, current.music, current.sadness, current.time_spent])
            current = current.next
        self.df = pd.DataFrame(data, columns=['Funny', 'Drama', 'Music', 'Sadness', 'TimeSpent'])
        self.xtrain, self.xtest, self.ytrain, self.ytest = train_test_split(self.df.drop('TimeSpent', axis='columns'),
                                                                            self.df.TimeSpent,
                                                                            test_size=0.2,
                                                                            random_state=1)
        self.model.fit(self.xtrain, self.ytrain)

    def predict(self, value):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            return self.model.predict(value) == 1

    def get_score(self):
        self.score_ = self.model.score(self.xtest, self.ytest)
        return self.score_

    def confusion_matrix(self):
        predicted = self.model.predict(self.xtest)
        cm = confusion_matrix(self.ytest, predicted)
        plt.figure(figsize=(10, 7))
        sn.heatmap(cm, annot=True)
        plt.xlabel("Predicted")
        plt.ylabel("Truth")
        plt.show()


def generate_random_data():
    funny = random.randint(0, 1)
    drama = random.randint(0, 1)
    music = random.randint(0, 1)
    sadness = random.randint(0, 1)
    time_spent = random.randint(0, 1)
    return funny, drama, music, sadness, time_spent


sarath = LinkedList('Sarath')
rohit = LinkedList('Rohit')

for i in range(100):
    funny, drama, music, sadness, time_spent = generate_random_data()
    sarath.append(funny, drama, music, sadness, time_spent)

for i in range(100):
    funny, drama, music, sadness, time_spent = generate_random_data()
    rohit.append(funny, drama, music, sadness, time_spent)


# sarath.initalize()
# value, score = sarath.predict([[1, 0, 0, 1]])
# print(value, score)


class Stack:
    def __init__(self):
        self.list: List[LinkedList] = []
        self.sz = 0

    def push(self, linkedlist: LinkedList):
        self.list.append(linkedlist)
        linkedlist.initalize()
        self.sz += 1

    def pop(self):
        self.list.pop()
        self.sz -= 1

    def predict(self, name: str, value):
        for element in self.list:
            if element.name == name.lower():
                return element.predict([value])
        print("No user found")
        return

    def get_score(self, name: str):
        for element in self.list:
            if element.name == name.lower():
                return element.get_score()
        print("No user found")
        return False

    def confusion_metirx(self, name: str):
        for element in self.list:
            if element.name == name.lower():
                element.confusion_matrix()
                return
        print("No user found")
        return False


mystack = Stack()
mystack.push(sarath)
mystack.push(rohit)
mystack.get_score('rohit')
mystack.get_score('sarath')


while True:
    funny, drama, music, sadness, time_spent = generate_random_data()
    print("1 : To predict reel will be liked by user\n2 : To print the score\n3 : Get confusion matrix\n4 : Quit")
    choice = int(input("Enter choice :"))
    if choice == 1:
        user = input("Enter username: ")
        print(f"Reel Configuration : funny:{funny} ,drama:{drama} ,music:{music} sadness:{sadness}")
        print(mystack.predict(user, [funny, drama, music, sadness]))
    elif choice == 2:
        user = input("Enter username: ")
        print("Socre is :", mystack.get_score(user))
    elif choice == 3:
        user = input("Enter username: ")
        mystack.confusion_metirx(user)
    else:
        break
