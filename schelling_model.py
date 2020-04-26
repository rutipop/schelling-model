import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import copy

SIZE = 30


class schelling:
    def __init__(self, y_percent, b_percent, y_threshold, b_threshold):

        self.empty_percent = 1-y_percent-b_percent
        self.y_threshold = y_threshold
        self.b_threshold = b_threshold
        self.y_percent = y_percent
        self.b_percent = b_percent
        self.empty_list = []
        self.yellow_list = []
        self.blue_list = []
        self.cur_num_yellow = 0
        self.cur_num_blue = 0
        self.cur_segregation =0
        self.num_of_citizens = (y_percent+b_percent)*SIZE*SIZE

    def create_city(self):

        city = list(itertools.product(range(SIZE), range(SIZE)))
        random.shuffle(city)
        num_emptys = int(SIZE * SIZE * self.empty_percent)
        num_yellows = int(SIZE * SIZE * self.y_percent)
        num_blues = int(SIZE * SIZE * self.b_percent)
        self.empty_list = city[:num_emptys]
        self.yellow_list = city[num_emptys:num_emptys + num_yellows]
        self.blue_list = city[num_emptys + num_yellows:num_emptys + num_yellows + num_blues]

    def is_in_limit(self, i, j):
        return i > -1 and j > -1 and i < SIZE and j < SIZE

    def check_cell(self, cur_i, cur_j):
        if (not self.is_in_limit(cur_i, cur_j)):
            return

        if ((cur_i, cur_j) in self.yellow_list):
            self.cur_num_yellow = self.cur_num_yellow + 1
        elif ((cur_i, cur_j) in self.blue_list):
            self.cur_num_blue = self.cur_num_blue + 1;

    def is_cell_happy(self, i, j, is_yellow):
        self.cur_num_yellow = 0
        self.cur_num_blue = 0

        self.check_cell(i - 1, j + 1)
        self.check_cell(i, j + 1)
        self.check_cell(i + 1, j + 1)
        self.check_cell(i + 1, j)
        self.check_cell(i + 1, j - 1)
        self.check_cell(i, j - 1)
        self.check_cell(i - 1, j - 1)
        self.check_cell(i - 1, j)

        sum = (self.cur_num_blue + self.cur_num_yellow)
        if(sum == 0):
            self.cur_segregation = (self.cur_segregation)+(1/self.num_of_citizens)
            return True
        if (is_yellow):
            if(self.cur_num_blue == 0):
                self.cur_segregation = (self.cur_segregation) + (1 / self.num_of_citizens)
            return (self.cur_num_yellow / sum) >= self.y_threshold
        else:
            if (self.cur_num_yellow == 0):
                self.cur_segregation = (self.cur_segregation) + (1 / self.num_of_citizens)
            return (self.cur_num_blue / sum) >= self.b_threshold

    def plot_city(self, name):
        fig, axes = plt.subplots()
        for cell in self.yellow_list:
            axes.scatter(cell[0] + 0.5, cell[1] + 0.5, color='y')
        for cell in self.blue_list:
            axes.scatter(cell[0] + 0.5, cell[1] + 0.5, color='b')

        axes.set_title(name, fontsize=15)
        axes.set_xlim([0, 30])
        axes.set_ylim([0, 30])
        axes.set_xticks([])
        axes.set_yticks([])
        plt.savefig(name + ".png")

    def move_to_empty(self,i,j,is_yellow):
        random_val=random.randint(0,len(self.empty_list)-1)
        coor = self.empty_list.pop(random_val)
        self.empty_list.append((i,j))

        if(is_yellow):
            self.yellow_list.remove((i,j))
            self.yellow_list.append(coor)
        else:
            self.blue_list.remove((i,j))
            self.blue_list.append(coor)



    def checkup (self):
        is_moved=False
        yellow_copy = copy.deepcopy(self.yellow_list)
        blue_copy = copy.deepcopy(self.blue_list)

        for yellow_cell in yellow_copy:
            if(not self.is_cell_happy(yellow_cell[0],yellow_cell[1],True)):
                self.move_to_empty(yellow_cell[0],yellow_cell[1],True)
                is_moved = True
                break
        for blue_cell in blue_copy:
            if(not self.is_cell_happy(blue_cell[0],blue_cell[1],False)):
                self.move_to_empty(blue_cell[0],blue_cell[1],False)
                is_moved = True
                break
        return is_moved

    def plot_segregation(self,seg,time):
        plt.clf()
        plt.plot(np.arange(time),seg)
        plt.xlabel('time')
        plt.ylabel('segregation')
        plt.title('seg where the yellow threshold is 0.2 and blue threshold is 0.6.png')
        plt.savefig("seg")

    def segregate(self):
        time =0
        segregation_values=list()
        while True:
            segregation_values.append(self.cur_segregation)
            self.cur_segregation = 0
            time = time+1
            if not self.checkup():
                break
        self.plot_segregation(segregation_values,time)




model = schelling( 0.3, 0.3, 0.2, 0.6)
model.create_city()
model.plot_city("initial town where 0.3% are yellow and 0.3% are blue ")
model.segregate()
model.plot_city("segregated town where the yellow threshold is 0.2 and blue threshold is 0.2")
