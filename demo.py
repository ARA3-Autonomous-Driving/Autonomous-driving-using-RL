import time
import numpy as np
from schola.core.protocols.protobuf.grpc_protocol import GrpcProtocol
from schola.core.simulators.unreal import UnrealEditor
from schola.sb3.env import VecEnv
from stable_baselines3 import PPO

protocol = GrpcProtocol(url="127.0.0.1", port=8000)
simulator = UnrealEditor()
env = VecEnv(protocol=protocol, simulator=simulator)
model = PPO.load("./checkpoints/best_racing_agent_v2")

obs = env.reset()
total_crashes = 0
ep_steps = 0
print("=== LIVE AUTONOMOUS AGENT TELEMETRY ^(DETERMINISTIC POLICY^) ===")

for step in range(5000):
    action, _ = model.predict(obs, deterministic=True)
    action[:, 0] = 0.60
    steer = float(action[0, 1])
    obs, rewards, dones, infos = env.step(action)
    ep_steps += 1

    if step %% 10 == 0:
        l_ray, c_ray, r_ray = obs[0]
        direction = "LEFT " if steer < -0.1 else ("RIGHT" if steer > 0.1 else "STRAIGHT")
        print(f"Step: {ep_steps:04d} | LiDAR [L:{l_ray:.2f} C:{c_ray:.2f} R:{r_ray:.2f}] | Steer: {steer:+.2f} ^({direction}^) | Crashes: {total_crashes}")

    if dones[0]:
        total_crashes += 1
        print(f"--- Reset triggered at step {ep_steps} ---")
        ep_steps = 0

env.close()
