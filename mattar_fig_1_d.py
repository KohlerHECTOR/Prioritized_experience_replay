import os

import numpy as np
import matplotlib.pyplot as plt

from mazemdp.maze import build_maze, create_random_maze
from random import seed
from mazemdp import create_random_maze
from replay_sim import Agent
from utils import evaluate

from arguments import get_args


args = get_args()



def to_plot(data, label):
    mean_data = np.mean(data, axis = 0)
    std_data = np.std(data, axis = 0)
    plt.plot(mean_data, label = label)
    plt.fill_between(np.arange(len(mean_data)), mean_data + std_data, mean_data - std_data, alpha = 0.4)


mdp = create_random_maze(9, 6, 0.13)

# using e-greedy pol for all models
args.action_policy = "greedy"
#### MATTAR MODEL ####
print("WITH PRIORITIZED REPLAY")
res_train = []
res_list_Q = []
for i in range(args.simulations):
    print("#### SIM NB: {}".format(i))
    rat = Agent(mdp, args)
    data = rat.learn(args)
    res_train.append(data["train"])
    res_list_Q.append(data["list_Q"])

res_eval = []
for list_Q in res_list_Q:
    res_eval.append(evaluate(list_Q, mdp, args))

to_plot(np.array(res_eval), label = "Prioritized replay")
#### MATTAR MODEL ####

#### Dyna - Q ######
print("DYNA-Q")
args.set_all_gain_to_1 = True
args.set_all_need_to_1 = True
res_train = []
res_list_Q = []
for i in range(args.simulations):
    print("#### SIM NB: {}".format(i))
    rat = Agent(mdp, args)
    data = rat.learn(args)
    res_train.append(data["train"])
    res_list_Q.append(data["list_Q"])

res_eval = []
for list_Q in res_list_Q:
    res_eval.append(evaluate(list_Q, mdp, args))

to_plot(np.array(res_eval), label = "Dyna-Q")
#### Dyna - Q ######

#### Q-learning######
print("Q-learning")
args.set_all_gain_to_1 = True
args.set_all_need_to_1 = True
args.planning_steps = 0
res_train = []
res_list_Q = []
for i in range(args.simulations):
    print("#### SIM NB: {}".format(i))
    rat = Agent(mdp, args)
    data = rat.learn(args)
    res_train.append(data["train"])
    res_list_Q.append(data["list_Q"])

res_eval = []
for list_Q in res_list_Q:
    res_eval.append(evaluate(list_Q, mdp, args))

to_plot(np.array(res_eval), label = "Q-learning")
#### Q-learning ######




# to_plot(np.array(res_train), "train")
plt.xlabel("episode")
plt.ylabel("steps until goal")
# plt.title("Performances of Mattar's agent in training and evalutation")
plt.legend()
filename = "mattar_fig_1_d"
# for _, val in args._get_kwargs():
#     filename += "_" + str(val)
plt.savefig("results/Mattar/" + filename + ".png")