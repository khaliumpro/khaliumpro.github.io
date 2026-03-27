import tkinter as tk
import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# -----------------------------
# CONFIG
# -----------------------------
GRID_SIZE = 14
WHITE_MIN = 2
WHITE_MAX = 11          # inclusive -> 10x10 white area
RED_COUNT = 5
CELL_SIZE = 40

# Choose your rule:
RESTRICT_TO_WHITE = True   # True = agent stays inside 10x10 white area
                           # False = agent can move anywhere on 14x14

MAX_STEPS_PER_EPISODE = 200

ACTIONS = {
    0: (-1, 0),  # UP
    1: (1, 0),   # DOWN
    2: (0, -1),  # LEFT
    3: (0, 1),   # RIGHT
}

# DQN hyperparams
GAMMA = 0.99
LR = 1e-3

REPLAY_CAPACITY = 50_000
BATCH_SIZE = 64
LEARN_START = 1_000

TARGET_UPDATE_EVERY = 500       # steps
TRAIN_EVERY = 1                 # steps

EPS_START = 1.0
EPS_END = 0.05
EPS_DECAY_STEPS = 25_000        # bigger = slower decay

DEVICE = torch.device("cpu")    # keep simple


# -----------------------------
# Q NETWORK
# -----------------------------
class QNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 4)
        )

    def forward(self, x):
        return self.net(x)


# -----------------------------
# REPLAY BUFFER
# -----------------------------
class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = deque(maxlen=capacity)

    def push(self, s, a, r, ns, done):
        self.buf.append((s, a, r, ns, done))

    def sample(self, batch_size):
        batch = random.sample(self.buf, batch_size)
        s, a, r, ns, done = zip(*batch)
        return (
            torch.tensor(np.array(s), dtype=torch.float32, device=DEVICE),
            torch.tensor(a, dtype=torch.int64, device=DEVICE),
            torch.tensor(r, dtype=torch.float32, device=DEVICE),
            torch.tensor(np.array(ns), dtype=torch.float32, device=DEVICE),
            torch.tensor(done, dtype=torch.float32, device=DEVICE),
        )

    def __len__(self):
        return len(self.buf)


# -----------------------------
# ENVIRONMENT
# -----------------------------
class GameEnv:
    def reset(self):
        self.steps = 0

        # agent starts in white area (you can change this if you want)
        self.agent = [
            random.randint(WHITE_MIN, WHITE_MAX),
            random.randint(WHITE_MIN, WHITE_MAX)
        ]

        self.current_target = 1
        self.reds = {}
        positions = set()

        # reds strictly inside white 10x10
        for i in range(1, RED_COUNT + 1):
            while True:
                x = random.randint(WHITE_MIN, WHITE_MAX)
                y = random.randint(WHITE_MIN, WHITE_MAX)
                if (x, y) not in positions:
                    positions.add((x, y))
                    self.reds[(x, y)] = i
                    break

        return self.get_state()

    def get_next_target_pos(self):
        for (x, y), num in self.reds.items():
            if num == self.current_target:
                return x, y
        return self.agent[0], self.agent[1]

    def get_state(self):
        ax, ay = self.agent
        tx, ty = self.get_next_target_pos()

        # Normalize to [0,1] so learning is easier
        ax_n = ax / (GRID_SIZE - 1)
        ay_n = ay / (GRID_SIZE - 1)
        tx_n = tx / (GRID_SIZE - 1)
        ty_n = ty / (GRID_SIZE - 1)
        tgt_n = self.current_target / RED_COUNT

        return np.array([ax_n, ay_n, tx_n, ty_n, tgt_n], dtype=np.float32)

    def step(self, action):
        self.steps += 1
        dx, dy = ACTIONS[action]
        nx = self.agent[0] + dx
        ny = self.agent[1] + dy

        # default small step penalty
        reward = -0.02

        if RESTRICT_TO_WHITE:
            # movement restricted to white area only
            if WHITE_MIN <= nx <= WHITE_MAX and WHITE_MIN <= ny <= WHITE_MAX:
                self.agent = [nx, ny]
        else:
            # movement allowed anywhere on board (clamped)
            nx = max(0, min(GRID_SIZE - 1, nx))
            ny = max(0, min(GRID_SIZE - 1, ny))
            self.agent = [nx, ny]

        pos = tuple(self.agent)

        # correct red square
        if pos in self.reds and self.reds[pos] == self.current_target:
            reward = 10.0
            del self.reds[pos]
            self.current_target += 1

        # wrong red square
        elif pos in self.reds:
            reward = -5.0

        done = False
        if self.current_target > RED_COUNT:
            reward += 20.0  # finish bonus
            done = True

        # stop episode if too long
        if self.steps >= MAX_STEPS_PER_EPISODE:
            done = True

        return self.get_state(), reward, done


# -----------------------------
# TKINTER UI
# -----------------------------
root = tk.Tk()
root.title("Improved DQN Grid (14x14)")

canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()

info_label = tk.Label(root, text="", font=("Arial", 14))
info_label.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=6)

# -----------------------------
# DRAW
# -----------------------------
def draw(env, episode, eps, steps_total, last_reward):
    canvas.delete("all")

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

            if WHITE_MIN <= i <= WHITE_MAX and WHITE_MIN <= j <= WHITE_MAX:
                color = "white"
            else:
                color = "black"

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # reds
    for (x, y), num in env.reds.items():
        canvas.create_rectangle(
            y * CELL_SIZE,
            x * CELL_SIZE,
            (y + 1) * CELL_SIZE,
            (x + 1) * CELL_SIZE,
            fill="red"
        )
        canvas.create_text(
            y * CELL_SIZE + CELL_SIZE // 2,
            x * CELL_SIZE + CELL_SIZE // 2,
            text=str(num),
            fill="white",
            font=("Arial", 16, "bold")
        )

    # blue agent
    ax, ay = env.agent
    canvas.create_rectangle(
        ay * CELL_SIZE,
        ax * CELL_SIZE,
        (ay + 1) * CELL_SIZE,
        (ax + 1) * CELL_SIZE,
        fill="blue"
    )

    tx, ty = env.get_next_target_pos()
    info_label.config(
        text=(
            f"Episode: {episode} | Steps: {env.steps}/{MAX_STEPS_PER_EPISODE} | TotalSteps: {steps_total}\n"
            f"Epsilon: {eps:.3f} | Current target: {env.current_target} | Next: ({tx},{ty}) | Last reward: {last_reward:.2f}\n"
            f"Restricted to white: {RESTRICT_TO_WHITE}"
        )
    )


# -----------------------------
# TRAINER (DQN)
# -----------------------------
q = QNet().to(DEVICE)
q_target = QNet().to(DEVICE)
q_target.load_state_dict(q.state_dict())
q_target.eval()

optimizer = optim.Adam(q.parameters(), lr=LR)
loss_fn = nn.SmoothL1Loss()

rb = ReplayBuffer(REPLAY_CAPACITY)

global_step = 0
episode = 0

env = GameEnv()
state = env.reset()
ep_return = 0.0
last_reward = 0.0
running = False


def epsilon_by_step(step):
    # linear decay
    if step >= EPS_DECAY_STEPS:
        return EPS_END
    frac = step / EPS_DECAY_STEPS
    return EPS_START + frac * (EPS_END - EPS_START)


def choose_action(s, eps):
    if random.random() < eps:
        return random.randint(0, 3)
    with torch.no_grad():
        x = torch.tensor(s, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        return int(torch.argmax(q(x), dim=1).item())


def train_batch():
    if len(rb) < LEARN_START:
        return 0.0

    s, a, r, ns, done = rb.sample(BATCH_SIZE)

    # Q(s,a)
    qvals = q(s)
    q_sa = qvals.gather(1, a.unsqueeze(1)).squeeze(1)

    with torch.no_grad():
        # target = r + gamma * max_a' Q_target(ns, a') * (1-done)
        max_next = q_target(ns).max(dim=1).values
        target = r + GAMMA * (1.0 - done) * max_next

    loss = loss_fn(q_sa, target)
    optimizer.zero_grad()
    loss.backward()
    nn.utils.clip_grad_norm_(q.parameters(), 5.0)
    optimizer.step()

    return float(loss.item())


def loop():
    global running, global_step, episode, state, ep_return, last_reward

    if not running:
        return

    eps = epsilon_by_step(global_step)
    action = choose_action(state, eps)

    next_state, reward, done = env.step(action)
    last_reward = reward
    ep_return += reward

    rb.push(state, action, reward, next_state, float(done))
    state = next_state

    # train
    loss_val = 0.0
    if global_step % TRAIN_EVERY == 0:
        loss_val = train_batch()

    # update target net
    if global_step % TARGET_UPDATE_EVERY == 0:
        q_target.load_state_dict(q.state_dict())

    global_step += 1

    if done:
        episode += 1
        # print a summary occasionally
        if episode % 10 == 0:
            print(f"Episode {episode} | return {ep_return:.1f} | replay {len(rb)} | eps {eps:.3f} | last loss {loss_val:.4f}")
        state = env.reset()
        ep_return = 0.0

    draw(env, episode, eps, global_step, last_reward)
    root.after(50, loop)


def start():
    global running
    if not running:
        running = True
        loop()


def stop():
    global running
    running = False


def reset_episode():
    global state, ep_return
    state = env.reset()
    ep_return = 0.0


tk.Button(btn_frame, text="Start", width=10, command=start).pack(side="left", padx=4)
tk.Button(btn_frame, text="Stop", width=10, command=stop).pack(side="left", padx=4)
tk.Button(btn_frame, text="Reset", width=10, command=reset_episode).pack(side="left", padx=4)

draw(env, episode, epsilon_by_step(global_step), global_step, last_reward)
root.mainloop()
