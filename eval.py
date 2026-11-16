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
print("Testing best_racing_agent_v2 with deterministic=True ^(zero exploration noise^)...")
for step in range(3000):
    action, _ = model.predict(obs, deterministic=True)
    action[:, 0] = 0.60
    obs, rewards, dones, infos = env.step(action)
    if dones:
        print(f"Episode reset at step {step}")
env.close()
