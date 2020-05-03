# coding=utf-8
import numpy as np
import random
names = locals()
leaves = {}
black_branch = []


class Branch:
    """表示一个树枝"""

    def __init__(self, situation, name, father_name="tree", wins=0, matchs=0):
        """初始化"""
        self.name = name  # 节点ID
        self.father = father_name  # 父节点ID
        self.situation = situation
        self.name_subbranch = []  # 子节点ID
        self.num_subbranch = 0  # 子节点总量
        self.unexpanded_subbranch = []#未完全拓展子节点
        self.created = 0 #节点是否已创建
        self.leaf = 0  # 是否为叶
        if sum(sum(self.situation)) == 0:
            self.leaf = 1
        self.current_player = 1  # 1和-1表示两个参与者

    def creat_subbranch(self):
        """找到可行的子节点,并将子节点初始化"""
        if self.leaf:
            return 0
        if self.created:
            return 1
        self.num_subbranch = 0
        self.name_subbranch = []
        number = 0
        for len in range(4):  # 行方向
            for i in range(4):
                for j in range(4-len):
                    if sum(self.situation[i, j:j+len+1]) == len+1:
                        number += 1  # Id序号
                        sub_name = self.name+'_'+str(number)
                        if sub_name not in black_branch:
                            self.num_subbranch += 1
                            if sub_name not in names.keys():
                                new_situation = self.situation.copy()
                                new_situation[i, j:j+len +
                                              1] = np.zeros([1, len+1])
                                names[sub_name] = Branch(
                                    new_situation, sub_name, self.name)
                                names[sub_name].current_player = self.current_player * \
                                    (-1)
                                self.name_subbranch.append(sub_name)
                                self.unexpanded_subbranch.append(sub_name)
                                if sum(sum(new_situation)) == 0:  # 遇见叶
                                    names[sub_name].leaf = 1
                                    names[sub_name].matchs = 1
                                    leaves[sub_name] = names[sub_name].current_player
                                    self.unexpanded_subbranch.remove(sub_name)
                                    temp_0 = self
                                    while temp_0.unexpanded_subbranch == []:
                                        names[temp_0.father].unexpanded_subbranch.remove(
                                            temp_0.name)
                                        temp_0 = names[temp_0.father]

        for len in [1, 2, 3]:  # 列方向
            for i in range(4-len):
                for j in range(4):
                    if sum(self.situation[i:i+len+1, j]) == len+1:
                        number += 1  # Id序号
                        sub_name = self.name+'_'+str(number)
                        if sub_name not in black_branch:
                            if sub_name not in names.keys():
                                self.num_subbranch += 1
                                new_situation = self.situation.copy()
                                new_situation[i:i+len+1, j] = np.zeros(len+1)
                                names[sub_name] = Branch(
                                    new_situation, sub_name, self.name)
                                names[sub_name].current_player = self.current_player * \
                                    (-1)
                                self.name_subbranch.append(sub_name)
                                self.unexpanded_subbranch.append(sub_name)
                                if sum(sum(new_situation)) == 0:  # 遇见叶
                                    names[sub_name].leaf = 1
                                    names[sub_name].matchs = 1
                                    leaves[sub_name] = names[sub_name].current_player
                                    self.unexpanded_subbranch.remove(sub_name)
                                    temp_0 = self
                                    while temp_0.unexpanded_subbranch == []:
                                        names[temp_0.father].unexpanded_subbranch.remove(
                                            temp_0.name)
                                        temp_0 = names[temp_0.father]

        self.created = 1
        return self.num_subbranch-1

    def sata1(self):
        """统计试验结果"""
        temp = [0, 0]
        if self.num_subbranch == 0:
            return [0, 1]
        for name, player in leaves.items():
            if self.name in name:
                temp[1] += 1
                temp[0] += 1-player*self.current_player
        temp[0] = temp[0]/2
        if temp[1] == 0:
            temp[1] = 1
        return temp

    def expend1(self):
        """进行一次试验"""
        temp0 = self
        while(temp0.creat_subbranch()):
            if(temp0.unexpanded_subbranch == []):
                if temp0 == self: # self已被完全拓展
                    return 2
                return 0
            temp1 = temp0.unexpanded_subbranch[random.randint(
                1, len(temp0.unexpanded_subbranch))-1]
            temp0 = names[temp1]
        return 1

    def play_input(self):
        """用户输入"""
        ary = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [
                       9, 10, 11, 12], [13, 14, 15, 16]], dtype=int)
        while 1:
            print()
            print("The situation now :")
            print(ary*self.situation)
            print("Enter your move :")
            try:
                nums = [int(n) for n in input().split()]
            except ValueError:
                print('Invalid  input !!!')
                print('Invalid  input !!!')
                print('Invalid  input !!!')
                print("'You should enter numbers between 'space'.Here is an example :")
                print("1 5 9")
                continue
            new_situation = self.situation.copy()
            try:
                for num in nums:
                    new_situation[(num-1)//4][(num-1) % 4] = 0
            except IndexError:
                print('Invalid  input !!!')
                print('Invalid  input !!!')
                print('Invalid  input !!!')
                print("The number you enter cannot be greater than 16.")
            for name in self.name_subbranch:
                if (names[name].situation == new_situation).all():
                    return name
            print()
            print('Invalid  input !!!')
            print('Invalid  input !!!')
            print('Invalid  input !!!')

    def del_black(self):
        """剔除劣势节点"""
        change = 1
        while change:
            if self.name_subbranch == []:
                return 0
            change = 0
            leaves_copy = leaves.copy()
            for name, player in leaves_copy.items():

                if player != self.current_player and names[names[name].father].num_subbranch <= 1:
                    change += 1

                    name_pa = names[names[name].father].father
                    black_branch.append(name_pa)
                    try:
                        names[names[name_pa].father].name_subbranch.remove(
                            name_pa)
                        names[names[name_pa].father].num_subbranch -= 1
                    except ValueError:
                        a = 1
                    del leaves[name]
                    if names[names[name_pa].father].num_subbranch == 0:
                        leaves[name_pa] = player


C = 0.001
a = np.ones([4, 4], dtype=np.int8)

# a[0] = [1, 1, 0, 0]
# a[1] = [1, 1, 0, 0]
# a[2] = [0, 1, 1, 0]
# a[3] = [0, 0, 0, 0]
print(a)
tree = Branch(a, 'tree')
current_branch = tree
j = 0
while 1:
    current_branch.creat_subbranch()
    if j == 0:
        scale = 33

        print("NEW GAME".center(scale+21, '-'))
        count = 10*current_branch.num_subbranch

        for name in current_branch.name_subbranch:
            for i in range(10):
                names[name].expend1()
                j += 1
                c = 100*j//count
                a = '*'*(scale*j//count)
                b = '.'*(scale-scale*j//count)
                print(
                    "\rInitializing:[{}->{}]{:3.0f}%".format(a, b, c), end='')
        print('\n'+"Let's start the game".center(scale+21, '-'))

    else:
        times = 1200
        if current_branch.num_subbranch <= 27:
            times = 2400
            print("!!!!!!!!!!!!!")
        for name in current_branch.name_subbranch:
            for i in range(times//current_branch.num_subbranch):
                if (names[name].expend1() == 2):
                    break

    current_branch.del_black()

    if current_branch.num_subbranch == 0:
        print('----------------------------')
        print('--------AI surrender--------')
        print('----------------------------')
        break
    win_matchs = {}
    UCB = {}
    num_match = 0

    for sub_branch in current_branch.name_subbranch:

        win_matchs[sub_branch] = names[sub_branch].sata1()
        num_match += win_matchs[sub_branch][1]
    for sub_branch in current_branch.name_subbranch:
        UCB[sub_branch] = win_matchs[sub_branch][0]/win_matchs[sub_branch][1] + \
            C*np.sqrt(np.log(num_match/win_matchs[sub_branch][1]))
    temp = -100
    for sub_branch, ucb in UCB.items():
        if temp < ucb:
            temp = ucb
            current_branch = names[sub_branch]

    if current_branch.leaf:
        print('----------------------------')
        print('----------YOU WIN-----------')
        print('----------------------------')
        break

    your_branch = current_branch.play_input()
    if names[your_branch].leaf:
        print('----------------------------')
        print('----------YOU LOSS----------')
        print('----------------------------')
        break
    current_branch = names[your_branch]
