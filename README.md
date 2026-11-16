# Autonomous Driving Using Reinforcement Learning

Youtube Project DEMO - https://youtu.be/8ehvsa4cbtk

An Unreal Engine-based autonomous driving simulation that uses raycast-based environment perception and Reinforcement Learning (RL) to train an autonomous vehicle to navigate its environment.

## Overview

This project explores autonomous vehicle navigation using Reinforcement Learning within an Unreal Engine simulation environment.

The vehicle interacts with its surroundings through raycast-based perception. Distance measurements from the environment are used as observations for the RL agent, which learns driving behaviour through interaction with the simulation.

## Key Features

- **Unreal Engine Simulation:** Vehicle simulation in a 3D environment.
- **Raycast-Based Perception:** Centre, left and right raycasts for detecting surrounding obstacles.
- **Environment Observations:** Distance extraction and observation-space integration.
- **Reinforcement Learning:** Training an autonomous driving agent using the Schola framework.
- **Reward-Based Learning:** Reward and environment logic for training the agent.
- **Model Evaluation:** Evaluation of trained agents.
- **Demo Execution:** Run the trained model in the simulation.

## Technology Stack

| Component | Technology |
|---|---|
| Simulation Engine | Unreal Engine |
| Programming | C++, Python, Blueprints |
| Reinforcement Learning Integration | Schola |
| Environment Perception | Raycasts |
| Model Training | Python |
| Version Control | Git, GitHub |

## Repository Structure

```text
Autonomous-driving-using-RL/
│
├── Config/                  # Unreal Engine configuration
├── Content/                 # Maps, materials and simulation assets
├── Source/                  # C++ source code
├── final_model/             # Selected trained model
│   └── best_racing_agent_v2.zip
│
├── MyProject.uproject       # Unreal Engine project file
├── train.py                 # RL training script
├── eval.py                  # Model evaluation script
├── demo.py                  # Model demonstration script
├── .gitignore
└── README.md
```

## Prerequisites

Before running the project, install:

 Unreal Engine — 5.7.4
• Python: 3.11 
• Schola: 2.1.0 
• Stable-Baselines3: 2.9.2
• PyTorch: 2.15.0
• Gymnasium: 1.2.2
• gRPC (grpcio): 1.85.1




**Note:** The Schola plugin is excluded from this repository. Install and configure the compatible plugin separately before opening the project.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ARA3-Autonomous-Driving/Autonomous-driving-using-RL.git

cd Autonomous-driving-using-RL
```

### 2. Configure Unreal Engine

- Install the required Unreal Engine version.
- Install the compatible Schola plugin.
- Configure the plugin according to its installation instructions.
- Open `MyProject.uproject`.

### 3. Configure Python

Create and activate a Python virtual environment if required by your setup.

Install the project's Python dependencies:

```bash
pip install -r requirements.txt
```

> A `requirements.txt` file must be added to the repository once the project's actual dependencies are finalized.

### 4. Run Training

```bash
python train.py
```

### 5. Evaluate the Model

```bash
python eval.py
```

### 6. Run the Demo

```bash
python demo.py
```

**Important:** Training, evaluation and demo scripts may require the Unreal Engine simulation and Schola environment to be running and configured correctly.

## Trained Model

The repository includes a selected trained model:

```text
final_model/best_racing_agent_v2.zip
```

This model can be used for evaluation and demonstration, subject to the compatible environment and model configuration.

## Current Development Scope

The project focuses on:

- Vehicle environment implementation.
- Raycast-based obstacle detection.
- Distance extraction and observation generation.
- Reinforcement Learning environment integration.
- Reward implementation and agent training.
- Evaluation and demonstration of the trained agent.

## Future Improvements

- Improve obstacle detection and environment perception.
- Optimize training speed and agent convergence.
- Improve navigation around sharp turns.
- Enhance vehicle control and collision avoidance.
- Expand simulation environments and evaluation scenarios.

## Contributors

**ARA3 – Autonomous Driving Team**

