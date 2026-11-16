# Adaptive Reinforcement Learning-Based Autonomous Driving in Unreal Engine 5

<p align="center">
  <strong>TEAM ARA3 · Autonomous Driving · Reinforcement Learning</strong>
</p>

A research and development project exploring an adaptive autonomous-driving agent in an Unreal Engine 5 simulation. The agent learns driving decisions from a compact numerical representation of its environment and produces continuous vehicle-control actions.

> **Project status:** The repository contains the Unreal Engine project, Python training/evaluation/demo scripts, a `final_model/` directory, and recorded PPO training checkpoints. The metrics below are the values visible in the team's training screenshots; they are not a claim of real-road validation.

---

## Overview

Traditional rule-based driving logic can be difficult to extend to situations that were not anticipated during development. Autonomous driving also involves more than reaching a destination: the vehicle should consider lane position, obstacle handling, route progress, collision avoidance, and smooth control.

This project investigates that problem in a controlled simulation using Reinforcement Learning (RL). The initial project concept describes observations such as vehicle velocity, lane offset/cross-track error, and obstacle distances. The policy is intended to output continuous steering, throttle, and braking actions.

### Project goals

- Build a repeatable autonomous-driving simulation in Unreal Engine 5.
- Represent nearby driving conditions using a compact, 3-channel LiDAR approximation.
- Exchange observation and action data between the simulation and the Python agent.
- Train a driving policy using Proximal Policy Optimization (PPO).
- Evaluate navigation behaviour and monitor training stability.
- Track defects and validation work through the team's Jira project.

## System concept

```text
┌───────────────────────────────────────┐
│          Unreal Engine 5              │
│                                       │
│  Driving track + vehicle pawn         │
│  3-channel LiDAR approximation        │
│  Observation/state extraction         │
└──────────────────┬────────────────────┘
                   │ observations
                   ▼
┌───────────────────────────────────────┐
│       Simulation ↔ Python bridge      │
│          Schola integration           │
└──────────────────┬────────────────────┘
                   │
                   ▼
┌───────────────────────────────────────┐
│           Python RL agent             │
│                                       │
│       PPO policy (training)           │
│       Action selection / evaluation   │
└──────────────────┬────────────────────┘
                   │ steering / throttle / brake
                   └───────────────► Unreal Engine 5
```

The repository's GitHub description identifies a Kinematic Pawn and a real-time UDP/TCP telemetry bridge via Schola. The project reports describe Unreal Engine 5, Python, reinforcement learning, and the use of Schola for simulation-agent integration. Refer to the actual project configuration and source code for the precise communication settings and vehicle implementation.

![GitHub repository structure](docs/images/github-repository-structure.png)

## Technology stack

| Component | Role in the project |
|---|---|
| Unreal Engine 5 | 3D driving simulation |
| C++ | Unreal project source and simulation-side logic |
| Python | Training, evaluation, and demonstration scripts |
| Proximal Policy Optimization (PPO) | Reinforcement-learning algorithm |
| Stable-Baselines3 | Python RL framework identified in the project report |
| Schola | Unreal-to-Python reinforcement-learning integration |
| LiDAR approximation | Compact environmental perception |
| GitHub | Source-code collaboration and version control |
| Jira | Agile backlog, sprint tracking, and bug management |

## Repository structure

The repository currently shows the following top-level structure:

```text
Autonomous-driving-using-RL/
├── Config/
├── Content/
├── Source/
├── final_model/
├── .gitignore
├── .vsconfig
├── MyProject.uproject
├── README.md
├── demo.py
├── eval.py
└── train.py
```

| Path | Purpose |
|---|---|
| `Config/` | Unreal Engine project configuration |
| `Content/` | Unreal assets and simulation content |
| `Source/` | C++ source code |
| `final_model/` | Directory for the trained model artifacts |
| `MyProject.uproject` | Unreal Engine project descriptor |
| `train.py` | Training entry-point script |
| `eval.py` | Evaluation entry-point script |
| `demo.py` | Demonstration entry-point script |

## Training results

The following values were transcribed from the team's four training-stage screenshots. They are checkpoint snapshots, not a smoothed learning curve.

| Checkpoint | Iterations | Timesteps | Mean episode reward | Mean episode length | FPS |
|---|---:|---:|---:|---:|---:|
| Start | 12 | 6,144 | -4.34 | 41.0 | 40 |
| Mid | 35 | 17,920 | 3.89 | 142.4 | 58 |
| High | 70 | 35,840 | -5.74 | 35.8 | 16 |
| Ready | 98 | 50,176 | 14.31 | 179.1 | 20 |

### Interpretation

- **Start:** The recorded mean episode reward was negative (-4.34), with an average episode length of 41.
- **Mid:** The recorded reward became positive (3.89), and the average episode length increased to 142.4.
- **High:** This checkpoint showed a regression: mean reward was -5.74 and mean episode length was 35.8.
- **Ready:** The best of the four supplied snapshots, with a mean reward of 14.31 and average episode length of 179.1.

The fluctuation at the High checkpoint is important: training did not improve monotonically. A final assessment should use repeated evaluation episodes and consistent test conditions, rather than relying on a single training log snapshot.

### Training screenshots

**Start and Mid checkpoints**

![Start and Mid PPO training logs](docs/images/training-start-and-mid.jpeg)

**High and Ready checkpoints**

![High and Ready PPO training logs](docs/images/training-high-and-ready.jpeg)

## Running the project

The repository includes `train.py`, `eval.py`, and `demo.py`. Exact command-line arguments and dependency versions should be taken from those scripts and the project's environment configuration.

### 1. Clone the repository

```bash
git clone https://github.com/ARA3-Autonomous-Driving/Autonomous-driving-using-RL.git
cd Autonomous-driving-using-RL
```

### 2. Open the Unreal Engine project

Open `MyProject.uproject` using the Unreal Engine version configured for this project.

Ensure that the required plugins and project dependencies are installed and enabled. In particular, confirm the Schola version is compatible with the installed Unreal Engine version.

### 3. Set up Python

Create and activate a virtual environment:

```bash
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
.venv\Scripts\activate
```

Install the project's dependencies using its dependency file, if provided. No `requirements.txt` was visible in the repository snapshot used to prepare this README, so package names and versions are intentionally not guessed here.

### 4. Train, evaluate, or run the demo

The repository provides these entry-point scripts:

```text
train.py
eval.py
demo.py
```

Check each script's configuration and arguments before running it. The commands below are illustrative entry points; they may need arguments or environment setup specific to the implementation:

```bash
python train.py
python eval.py
python demo.py
```

The Unreal Engine environment and the Python-side integration must be configured as required by the project before running these scripts.

## Testing and known issues

The team tracks testing and defects in the Jira project **ADAPT-Drive (AD)**. The supplied Jira screenshot shows the following five issues marked **Done** at the time of capture:

| Jira issue | Description | Captured status |
|---|---|---|
| AD-44 | Raycasts Wall Failure | Done |
| AD-45 | Raycasts Not Clearly Visible | Done |
| AD-50 | Car Moving Backwards | Done |
| AD-52 | Car Crashes at First 180-Degree Left Turn | Done |
| AD-51 | Training Is Very Slow | Done |

These are issue-tracker statuses from the supplied screenshot. They should not be interpreted as proof that every possible scenario has passed final validation.

![Jira bug tracker showing the recorded issues](docs/images/jira-bug-tracker.png)

## Agile project and team

The project is managed using Agile Scrum practices, with a Jira product backlog, sprint planning, issue tracking, and review activities.

**Team ARA3**

| Team member | Role recorded in the Phase 2 report |
|---|---|
| Anmol Singh | AI intelligence, error handling, and documentation |
| Rahul Raj | QA and testing; Scrum Master |
| Aryan Sanskar Ahuja | Core AI implementation and Unreal Engine 5 |

**Project management:** [ADAPT-Drive Jira project](https://rahul2007bsbs.atlassian.net/jira/software/projects/AD/boards/202/backlog)

## Research context

The initial project submission identifies the research need as a focused, modifiable simulation experiment for adaptive driving using compact numerical observations rather than requiring the policy to process raw camera images or LiDAR point clouds. The intended policy must balance lane position, obstacle distance, route progress, and smoothness.

The submission references the following background work:

1. Dosovitskiy et al. (2017), [CARLA: An Open Urban Driving Simulator](https://arxiv.org/abs/1711.03938).
2. Shah et al. (2017), [AirSim: High-Fidelity Visual and Physical Simulation for Autonomous Vehicles](https://arxiv.org/abs/1705.05065).
3. Schulman et al. (2017), [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347).

## References and documentation

- [Unreal Engine documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/)
- [AMD Schola documentation](https://gpuopen.com/manuals/schola/)
- [AMD Schola GitHub repository](https://github.com/GPUOpen-LibrariesAndSDKs/Schola)
- [Stable-Baselines3 PPO documentation](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)

## Limitations and future work

The project is a simulation-based investigation. The supplied material does not establish real-vehicle deployment, road safety certification, or generalisation to real-world driving.

Potential next steps include:

- Run repeated evaluation episodes with fixed test scenarios and seeds.
- Report collision count, completion rate, lane deviation, route progress, and control smoothness alongside reward.
- Investigate the reward and episode-length regression visible in the High checkpoint.
- Document the exact observation vector, action bounds, reward function, and termination conditions.
- Record Unreal Engine, Schola, Python, and package versions.
- Add a reproducible dependency file and exact run commands.

---

<p align="center">
  <strong>TEAM ARA3</strong><br>
  Adaptive Reinforcement Learning-Based Autonomous Driving in Unreal Engine 5
</p>
