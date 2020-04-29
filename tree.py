# coding=utf-8
###
import numpy as np
import random
import time
names = locals()
leaves = {}


class Branch:
    """表示一个树枝"""

    def __init__(self, situation, name, father_name="tree", wins=0, matchs=0):
        """sdad """
        self.name = name
        self.father = father_name
        self.situation = situation
        self.name_subbranch = []
        self.num_subbranch = 0
        self.leaf = 0
        if sum(sum(self.situation)) == 0:
            self.leaf = 1
        self.wins = wins
        self.matchs = matchs
        self.current_player = 1  # 1表示当前player,-1表示对手

    def creat_subbranch(self):
        if self.leaf:
            return 0
        self.num_subbranch = 0
        self.name_subbranch = []
        for len in range(4):  # line
            for i in range(4):
                for j in range(4-len):
                    if sum(self.situation[i, j:j+len+1]) == len+1:

                        self.num_subbranch += 1
                        new_situation = self.situation.copy()
                        new_situation[i, j:j+len+1] = np.zeros([1, len+1])

                        sub_name = self.name+'_'+str(self.num_subbranch)
                        # 创建分支
                        if sub_name not in names:
                            names[sub_name] = Branch(
                                new_situation, sub_name, self.name)
                        names[sub_name].current_player = self.current_player * \
                            (-1)
                        if sum(sum(new_situation)) == 0:  # 遇见叶
                            names[sub_name].leaf = 1
                            names[sub_name].matchs = 1
                            leaves[sub_name] = names[sub_name].current_player
                        self.name_subbranch.append(sub_name)

        for len in [1, 2, 3]:  # raw
            for i in range(4-len):
                for j in range(4):
                    if sum(self.situation[i:i+len+1, j]) == len+1:
                        self.num_subbranch += 1
                        new_situation = self.situation.copy()
                        new_situation[i:i+len+1, j] = np.zeros(len+1)
                        sub_name = self.name+'_'+str(self.num_subbranch)
                        if sub_name not in names:
                            names[sub_name] = Branch(
                                new_situation, sub_name, self.name)
                        names[sub_name].current_player = self.current_player * \
                            (-1)
                        if sum(sum(new_situation)) == 0:
                            names[sub_name].leaf = 1
                            names[sub_name].matchs = 1
                            leaves[sub_name] = names[sub_name].current_player
                        self.name_subbranch.append(sub_name)
        return self.num_subbranch-1

    def compare_branch(self, situation):  # 输入局势,与子节点对比,返回子节点名称
        for name in self.name_subbranch:
            if (names[name].situation == situation).all():
                print("=====")
                print(names[name].situation)
                print(situation)
                return name
        return False

    def sata(self):  # 计算胜场和总场数,返回[wins,matchs]
        if self.leaf == 1:
            return [0, 1]
        else:
            temp = [0, 0]
            for name in self.name_subbranch:
                temp[0] = temp[0]+names[name].sata()[1]-names[name].sata()[0]
                temp[1] = temp[1]+names[name].sata()[1]
            return temp

    def sata1(self):
        temp = [0, 0]
        for name, player in leaves.items():
            if self.name in name:
                temp[1] += 1
                temp[0] += 1-player*self.current_player
        temp[0] = temp[0]/2
        return temp

    def expend1(self):
        if self.creat_subbranch():
            temp0 = self
            while(temp0.creat_subbranch()):
                while 1:
                    temp1 = temp0.name_subbranch[random.randint(
                        1, temp0.num_subbranch)-1]
                    if(names[temp1].leaf == 0):
                        break
                temp0 = names[temp1]
            # print(self.num_subbranch)
            # print(random.randint(1,self.num_subbranch))
            # temp = self.name_subbranch[random.randint(1, self.num_subbranch)-1]
            # while(names[temp].leaf):
            #     temp = self.name_subbranch[random.randint(
            #         1, self.num_subbranch)-1]

            # while(names[temp].creat_subbranch()):
            #     temp = names[temp].name_subbranch[random.randint(
            #         1, names[temp].num_subbranch)-1]
            #     while(names[temp].leaf):
            #         print(temp)
            #         print(names[temp].num_subbranch)
            #         temp = names[temp].name_subbranch[random.randint(
            #             1, names[temp].num_subbranch)-1]

    def play_input(self):
        ary = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [
                       9, 10, 11, 12], [13, 14, 15, 16]], dtype=int)
        while 1:
            print()
            print("The situation now :")
            print(ary*self.situation)
            print("Enter your move :")
            nums = [int(n) for n in input().split()]
            new_situation = self.situation.copy()
            for num in nums:
                new_situation[(num-1)//4][(num-1) % 4] = 0
            
            for name in self.name_subbranch:
                if (names[name].situation == new_situation).all():
                    return name
            print()
            print('Invid input !!!')
            print('Invid input !!!')


C = 0.7
a = np.ones([4, 4], dtype=np.int8)
# a[2:,2:]=np.ones([2,2])
# a[2][2]=1

tree = Branch(a, 'tree')

current_branch = tree
while 1:

    current_branch.creat_subbranch()
    for name in current_branch.name_subbranch:
        for i in range(10):
            names[name].expend1()

    win_matchs = {}
    UCB = {}
    num_match = 0
    for sub_branch in current_branch.name_subbranch:
        win_matchs[sub_branch] = names[sub_branch].sata1()
        num_match += win_matchs[sub_branch][1]
    for sub_branch in current_branch.name_subbranch:
        # print(win_matchs[sub_branch][1])
        # print(num_match)
        UCB[sub_branch] = win_matchs[sub_branch][0]/win_matchs[sub_branch][1] + \
            C*np.sqrt(np.log(num_match/win_matchs[sub_branch][1]))
    temp = -100
    for sub_branch, ucb in UCB.items():
        if temp < ucb:
            temp = ucb
            current_branch = names[sub_branch]
   

    if current_branch.leaf:
        print('------------------')
        print('-----YOU WIN------')
        print('------------------')
        break

    your_branch = current_branch.play_input()
    if names[your_branch].leaf:
        print('------------------')
        print('-----YOU LOSS-----')
        print('------------------')
        break
    current_branch = names[your_branch]


# zsd = names.copy()
# for name in zsd:
#     if str(name)[0:4] == 'tree':
#         print(str(name))
#         if names[name].name_subbranch:

#             print(names[name].name_subbranch)
