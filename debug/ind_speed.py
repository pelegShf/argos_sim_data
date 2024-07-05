from matplotlib import pyplot as plt
from metrics.speed import get_individ_speed, get_individ_speed_rolling


fig, axs = plt.subplots(2, 4, figsize=(20, 10))

robotNum = 1
for i in range(2):
    for j in range(4):
        get_individ_speed_rolling(trial=1, robotNum=robotNum, avg_over_frames=50, ax=axs[i, j])
        robotNum += 1

plt.tight_layout()
# plt.show()
plt.savefig('./visualization/graphs/pNg_rolling_robots_speed.png')