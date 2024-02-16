import random
import multiprocessing as mp
import sys

# 用于模拟一次三门游戏
def play_game(change_choice):
    doors = [0, 0, 0] # 三扇门，0代表山羊，1代表汽车
    doors[random.randint(0, 2)] = 1 # 随机选一扇门放置汽车

    # 参赛者选择一扇门
    first_choice = random.randint(0, 2)

    # 主持人打开一扇有山羊的门
    open_door = -1
    for i in range(3):
        if i != first_choice and doors[i] == 0:
            open_door = i
            break

    # 参赛者选择是否更换选择
    if change_choice:
        second_choice = -1
        for i in range(3):
            if i != first_choice and i != open_door:
                second_choice = i
                break
        return doors[second_choice]
    else:
        return doors[first_choice]

# 计算函数，用于在多个进程中运行游戏模拟
def compute(wins, change_choice, n):
    for i in range(n):
        if play_game(change_choice) == 1:
            wins.value += 1
        progress_bar(i, n)

# 进度条函数，用于在控制台输出计算进度条
def progress_bar(count, total):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s\r' % (bar, percents, '%'))
    sys.stdout.flush()

# 模拟1000000次中途换门和中途不换门
if __name__ == "__main__":
    n = 1000000
    change_wins = mp.Value('i', 0)
    not_change_wins = mp.Value('i', 0)

    p1 = mp.Process(target=compute, args=(change_wins, True, n))
    p2 = mp.Process(target=compute, args=(not_change_wins, False, n))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # 输出结果
    print("\n换门获胜概率：", change_wins.value/n)
    print("不换门获胜概率：", not_change_wins.value/n)