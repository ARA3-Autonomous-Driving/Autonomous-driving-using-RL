import os
import numpy as np
from schola.core.protocols.protobuf.grpc_protocol import GrpcProtocol
from schola.core.simulators.unreal import UnrealEditor
from schola.sb3.env import VecEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecMonitor, VecEnvWrapper
from stable_baselines3.common.callbacks import BaseCallback


class SmoothRacingWrapper(VecEnvWrapper):
    def __init__(self, venv, fixed_throttle=0.60):
        super().__init__(venv)
        self.fixed_throttle = fixed_throttle
        self.last_steer = None
        self.prev_steer = None
        self.ep_steps = None

    def reset(self):
        obs = self.venv.reset()
        self.prev_steer = np.zeros(self.num_envs, dtype=np.float32)
        self.ep_steps = np.zeros(self.num_envs, dtype=np.int32)
        return obs

    def step_async(self, actions):
        locked_actions = actions.copy()
        locked_actions[:, 0] = self.fixed_throttle
        self.last_steer = np.clip(locked_actions[:, 1], -1.0, 1.0)
        self.venv.step_async(locked_actions)

    def step_wait(self):
        obs, rewards, dones, infos = self.venv.step_wait()
        self.ep_steps += 1

        # Prevent stray teleport collision on step 1 from poisoning training
        dones = np.where(self.ep_steps <= 1, False, dones)
        rewards = np.where(self.ep_steps <= 1, 0.1, rewards)

        left_ray, center_ray, right_ray = obs[:, 0], obs[:, 1], obs[:, 2]

        # Guide steering toward whichever side has more open space
        open_direction = right_ray - left_ray
        directional_alignment = self.last_steer * open_direction

        # Stronger steering incentive when approaching a corner (center_ray < 0.40)
        corner_bonus = np.where(center_ray < 0.40, 0.35 * directional_alignment, 0.15 * directional_alignment)
        # Penalize violent steering jitter so the car drives smooth arcs
        steer_jitter_penalty = -0.05 * np.abs(self.last_steer - self.prev_steer)
        # Early warning penalty before touching walls
        wall_penalty = np.where((left_ray < 0.12) | (right_ray < 0.12) | (center_ray < 0.12), -0.3, 0.0)

        shaped_rewards = np.where(
            dones,
            rewards,
            rewards + corner_bonus + steer_jitter_penalty + wall_penalty
        )

        self.prev_steer = np.where(dones, 0.0, self.last_steer)
        self.ep_steps = np.where(dones, 0, self.ep_steps)
        return obs, shaped_rewards, dones, infos


class BestModelCallback(BaseCallback):
    def __init__(self, save_dir="./checkpoints"):
        super().__init__()
        self.save_dir = save_dir
        self.best_reward = -np.inf
        os.makedirs(save_dir, exist_ok=True)

    def _on_step(self) -> bool:
        return True

    def _on_rollout_end(self) -> None:
        if len(self.model.ep_info_buffer) >= 5:
            mean_rew = float(np.mean([ep["r"] for ep in self.model.ep_info_buffer]))
            mean_len = float(np.mean([ep["l"] for ep in self.model.ep_info_buffer]))
            if mean_rew > self.best_reward:
                self.best_reward = mean_rew
                self.model.save(os.path.join(self.save_dir, "best_racing_agent_v2"))
                print(f"[Saved Best v2] Reward: {mean_rew:.2f} | Avg Steps: {mean_len:.1f}")


def linear_schedule(initial_value: float, final_value: float):
    def func(progress_remaining: float) -> float:
        return final_value + progress_remaining * (initial_value - final_value)
    return func


protocol = GrpcProtocol(url="127.0.0.1", port=8000)
simulator = UnrealEditor()
env = VecEnv(protocol=protocol, simulator=simulator)
env = SmoothRacingWrapper(env, fixed_throttle=0.60)
env = VecMonitor(env)

model = PPO(
    policy="MlpPolicy",
    env=env,
    learning_rate=linear_schedule(2.5e-4, 5e-5),
    n_steps=512,
    batch_size=64,
    n_epochs=8,
    gamma=0.99,
    ent_coef=0.008,
    max_grad_norm=0.5,
    policy_kwargs=dict(log_std_init=-0.25),
    verbose=1,
)

print("Starting fresh PPO training run on updated track (throttle=0.60, smooth steering)...")
model.learn(total_timesteps=75_000, callback=BestModelCallback())
model.save("racing_agent_v2_final")
print("Training finished! Saved to racing_agent_v2_final.zip")
env.close()
