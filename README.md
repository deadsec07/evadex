# 🎯 EvadeX: Autonomous Missile Evasion Simulator

**EvadeX** is a next-generation missile simulation system that demonstrates AI-driven, autonomous evasive maneuvers against incoming interceptors. Inspired by obstacle-avoiding drones like DJI, this prototype simulates how smart missiles can detect threats mid-flight and dynamically avoid interception using onboard intelligence.

---

## 🚀 Features

| Module            | Description |
|-------------------|-------------|
| 🔁 Real-Time Evasion Logic | Dynamically adjusts trajectory to avoid incoming interceptors. |
| 🧠 AI Integration | PPO (Reinforcement Learning) policy training included. |
| 🎥 Live Animation | Visualize all missile and interceptor paths in real-time. |
| 📡 Sensor Simulation | Simulates noisy IR-based interceptor tracking. |
| 💾 Telemetry Logging | All flight data recorded in CSV for replay, training, or analysis. |
| ☄️ Multi-Target Threats | Supports multiple interceptors and multiple friendly missiles. |

---

## 🧠 Technologies Used

- Python 3.10+
- Matplotlib (visualization + animation)
- NumPy (vector math)
- Gym (`stable-baselines3`) – for AI training
- CSV – for telemetry output
- Optional: Pygame / PyQt for future real-time GUI

---

## 📦 Project Structure

evadex-sim/
├── main.py # Main simulation loop
├── missile.py # Missile movement & turning constraints
├── interceptor.py # Seeker missile logic
├── evasion_ai.py # Threat-avoidance logic
├── rl_agent.py # Placeholder RL evader (pluggable)
├── missile_env.py # Gym-compatible AI training environment
├── telemetry.csv # Flight log
└── README.md # You're reading this!

---

## 📊 Example Output

- Blue lines = friendly missile(s)
- Red/Orange/Purple dashed lines = interceptor(s)
- Heatmap = threat zones (hotter = more dangerous)
- Animation = live evasive maneuvering over time

---

## 🔬 How It Works

1. Missile is launched with a target heading.
2. Interceptors are launched to pursue it.
3. Missile constantly monitors threat vectors.
4. If a threat is close, it turns evasively using AI logic.
5. Uses either:
   - Basic heuristic logic (manual evasion)
   - RL agent (learns to avoid threats through training)

---

## 🧪 AI Training (Optional)

```bash
# Install RL dependencies
pip install stable-baselines3 gym

# Train agent
python train_rl_agent.py  # internally calls PPO with MissileEvasionEnv

## 🧪 Project Setup

1. chmod +x setup.sh
2. ./setup.sh
3. when done use, 'deactivate' to Exit venv

