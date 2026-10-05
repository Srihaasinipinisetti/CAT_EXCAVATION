# CAT Excavation Control System

### Autonomous Excavation, Adaptive Digging, Load Detection & Safety Control

A modular control framework for an autonomous **four-wheeled excavation robot** developed for the **Caterpillar Autonomy Challenge**.

The system is designed around a **Raspberry Pi high-level control computer** and an **Arduino real-time motor/sensor controller**. It combines actuator control, sensor fusion, excavation-state management, current-based soil interaction detection, reachability analysis, slip/stall detection, load estimation, power management, and safety supervision into a single autonomous excavation pipeline.

---

## 🚜 Project Overview

The objective of this project is to enable an excavation robot to autonomously perform a complete digging cycle:

```text
                 ┌──────────────────────────┐
                 │       Mission Start      │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │       Self Check         │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │   Approach Dig Zone      │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │  Reachability Analysis   │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │        Alignment         │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │    Bucket Positioning    │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │      Soil Contact        │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │ Adaptive Penetration     │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │        Scoop             │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │     Load Verification    │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │          Lift            │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │       Transport          │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │     Dump Positioning     │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │          Dump            │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │    Empty Verification    │
                 └────────────┬─────────────┘
                              ↓
                 ┌──────────────────────────┐
                 │      Reset / Next        │
                 └──────────────────────────┘
```

The controller is designed to continuously monitor the robot and transition into **recovery, fault, or emergency-stop states** whenever unsafe or abnormal conditions are detected.

---

# 🧠 System Architecture

```text
                         ┌───────────────────────┐
                         │     Mission Logic     │
                         │   Excavation FSM      │
                         └───────────┬───────────┘
                                     │
                                     ↓
                         ┌───────────────────────┐
                         │    Control Layer      │
                         │ Penetration / Scoop   │
                         │ Power Management      │
                         └───────────┬───────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  │                                     │
                  ↓                                     ↓
        ┌───────────────────┐                 ┌───────────────────┐
        │   Sensor Fusion   │                 │  Safety Supervisor│
        │                   │                 │                   │
        │ Current           │                 │ Overcurrent       │
        │ Encoders          │                 │ Undervoltage      │
        │ IMU               │                 │ Stall             │
        │ Battery           │                 │ Slip              │
        └─────────┬─────────┘                 │ IMU Tip           │
                  │                           │ Communication     │
                  │                           └─────────┬─────────┘
                  ↓                                     │
        ┌───────────────────┐                            │
        │ Raspberry Pi      │◄───────────────────────────┘
        │ High-Level Logic  │
        └─────────┬─────────┘
                  │
             Serial 115200
                  │
                  ↓
        ┌───────────────────┐
        │   Arduino Mega    │
        │ Real-Time Control │
        └─────────┬─────────┘
                  │
       ┌──────────┼───────────┐
       ↓          ↓           ↓
   Wheel Motors  Boom       Clamshell
                 Actuator    Actuator
```

---

# 🖥️ Computing Architecture

## Raspberry Pi

The Raspberry Pi is responsible for high-level intelligence and supervision.

### Responsibilities

- Mission/state-machine management
- Sensor fusion
- LiDAR processing
- Camera interface
- Reachability analysis
- Excavation control
- Soil-contact detection
- Penetration resistance estimation
- Load estimation
- Slip detection
- Stall detection
- Power management
- Safety supervision
- Arduino communication

---

## Arduino

The Arduino handles real-time low-level interaction with the robot.

### Responsibilities

- Wheel motor commands
- Linear actuator commands
- Encoder acquisition
- Current telemetry
- Actuator feedback
- Real-time hardware interface

Communication between the Raspberry Pi and Arduino uses a serial protocol at:

```text
115200 baud
```

---

# 📡 Sensor System

The software supports multiple sensor sources.

| Sensor | Purpose |
|---|---|
| Wheel Encoders | Odometry and wheel-motion estimation |
| Current Sensors | Motor/actuator load monitoring |
| IMU | Pitch, roll and angular-motion monitoring |
| Battery Monitor | Voltage/current/power monitoring |
| LiDAR | Obstacle and excavation-face detection |
| Camera | Visual telemetry / optional alignment |
| Actuator Feedback | Boom and clamshell position monitoring |

---

# ⚙️ Actuator System

## Four-Wheel Skid-Steer Drive

The robot uses four driven wheels.

The control system accepts:

```text
Forward command
+
Turn command
```

and converts them into left/right wheel commands:

```text
Left  = Forward + Turn
Right = Forward - Turn
```

Commands are constrained to:

```text
-255 ... +255
```

---

## Boom Linear Actuator

Configured as a:

```text
12 V
100 mm nominal stroke
```

### Current configuration

| Parameter | Value |
|---|---:|
| Closed Length | 205 mm |
| Open Length | 305 mm |
| Stroke | 100 mm |
| Soft Minimum | 210 mm |
| Soft Maximum | 300 mm |
| Rated Current | 1.5 A |

The software automatically clamps commands to the configured soft limits.

---

## Clamshell Actuator

Configured as a:

```text
12 V
50 mm stroke
```

### Current configuration

| Parameter | Value |
|---|---:|
| Stroke | 50 mm |
| Soft Minimum | 2 mm |
| Soft Maximum | 48 mm |
| Rated Current | 1.5 A |

The clamshell controller supports:

- Open
- Close
- Position control
- Current-based slowdown
- Current-based stopping

---

# ⛏️ Adaptive Excavation

The excavation controller does not simply drive the boom at a fixed speed.

Instead, it estimates the resistance of the material using actuator current.

### Resistance Classification

```text
Boom Current
     │
     ├── < 0.70 A ─────── LOW
     │
     ├── 0.70–1.10 A ──── MEDIUM
     │
     ├── 1.10–1.28 A ──── HIGH
     │
     └── ≥ 1.28 A ─────── CRITICAL
```

The penetration velocity is automatically reduced as resistance increases.

```text
LOW       → 100% penetration speed
MEDIUM    → 50%
HIGH      → 20%
CRITICAL  → STOP + RETRACT
```

This allows the excavation mechanism to adapt to changing digging resistance instead of relying on a fixed motion profile.

---

# 📏 Penetration Depth Estimation

The system estimates penetration depth from boom actuator displacement after soil contact.

The configured target depth is:

```text
25 mm
```

The relationship is calibrated using:

```text
Depth ≈ Boom Stroke / K_DEPTH
```

where the current configuration uses:

```text
K_DEPTH = 1.2
```

> The value is a calibration parameter and should be experimentally tuned on the physical robot.

---

# 🌱 Soil Contact Detection

Soil contact is detected using multiple signals rather than position alone.

The controller considers:

- Boom actuator current
- Commanded actuator velocity
- Actual actuator velocity
- Current increase relative to idle
- Mechanical soft-limit status

Possible results:

```text
NONE
SOIL
OBSTACLE
MECHANICAL LIMIT
```

A sustained reduction in actuator motion combined with increased current indicates contact.

This allows the robot to distinguish normal actuator movement from interaction with the excavation material.

---

# 🪣 Scoop Control

After sufficient penetration:

1. The clamshell is commanded to close.
2. Clamshell current is monitored.
3. Closing speed is reduced when current becomes high.
4. The actuator stops when the bucket reaches the closed region or excessive current is detected.

This prevents unnecessary actuator loading during the scooping phase.

---

# 📦 Load Detection

The system estimates whether material has actually been collected using a **current-based lift test**.

The boom current during lifting is compared against an empty-bucket baseline.

The result is classified as:

```text
LOAD_PRESENT
LOAD_PARTIAL
LOAD_EMPTY
LOAD_UNCERTAIN
```

This provides feedback after the scoop instead of assuming that every scoop was successful.

---

# 🛞 Wheel Slip Detection

Wheel slip is estimated by comparing:

```text
Encoder-derived velocity
            vs.
IMU-derived velocity
```

The slip ratio is:

```text
Slip Ratio =
|V_encoder - V_IMU|
--------------------
max(|V_encoder|, ε)
```

The controller classifies slip as:

```text
NORMAL
WARN
CRIT
EMERG
```

Thresholds are configurable in:

```text
config/thresholds.py
```

---

# 🔧 Stall Detection

The system detects three major types of stalls:

```text
BOOM_STALL
CLAM_STALL
WHEEL_STALL
```

### Boom / Clamshell Stall

A stall is detected when:

- Actuator command is active
- Position change is very small
- Current is elevated
- The condition persists beyond the configured time

### Wheel Stall

A wheel stall is detected when:

- Wheel command is active
- Encoder counts remain very low
- Wheel current is high
- The condition persists for the configured duration

---

# 🔋 Power Management

The power manager continuously monitors battery current and voltage.

Battery voltage thresholds:

| State | Voltage |
|---|---:|
| Normal | ≥ 10.8 V |
| Warning | < 10.8 V |
| Critical | < 10.2 V |
| Emergency | < 9.6 V |

The system also uses an exponential moving average to prevent instantaneous current spikes from unnecessarily triggering protection.

During high power consumption, the controller can:

- Disable penetration
- Restrict clamshell operation
- Reduce wheel torque
- Enter a critical power state

---

# 🛡️ Safety Supervisor

Safety is handled independently from normal excavation control.

The safety supervisor checks:

- Emergency-stop input
- Communication loss
- Boom overcurrent
- Clamshell overcurrent
- Wheel overcurrent
- Battery undervoltage
- Actuator stall
- Wheel slip
- Excessive pitch
- Excessive roll

Fault conditions are converted into explicit fault codes.

### Fault Codes

```text
OVERCURRENT_BOOM
OVERCURRENT_CLAM
OVERCURRENT_WHEEL
UNDERVOLTAGE
STALL
SLIP
IMU_TIP
COMM_LOSS
TIMEOUT
EMERGENCY_STOP
```

---

# 🚨 Emergency Stop

The Arduino communication layer supports an explicit emergency-stop command:

```text
X
```

The safety system can therefore force the robot into:

```text
EMERGENCY_STOP
```

whenever a critical condition is detected.

---

# 🔄 Excavation State Machine

The complete mission is represented using a finite-state machine.

### Main states

```text
IDLE
 ↓
SELF_CHECK
 ↓
APPROACH_DIG_ZONE
 ↓
DIG_ZONE_REACHABILITY_CHECK
 ↓
ALIGN
 ↓
BUCKET_POSITIONING
 ↓
SOIL_CONTACT
 ↓
PENETRATION
 ↓
SCOOP
 ↓
LOAD_VERIFICATION
 ↓
LIFT
 ↓
LOAD_RECHECK
 ↓
TRANSPORT
 ↓
DUMP_POSITIONING
 ↓
DUMP
 ↓
EMPTY_VERIFICATION
 ↓
RESET
 ↓
NEXT_SCOOP
```

Additional states provide abnormal-condition handling:

```text
RECOVERY
FAULT
EMERGENCY_STOP
```

---

# 📐 Reachability Analysis

Before excavation, the controller checks whether the desired digging point can be reached by the boom mechanism.

The current geometry model uses:

```text
Minimum reach ≈ 250.8 mm
Maximum reach ≈ 616 mm
```

The controller searches possible boom actuator positions and selects the configuration producing the smallest distance to the target.

The configured reachability tolerance is:

```text
±40 mm
```

If the target cannot be reached within this tolerance, the system reports:

```text
DIG_UNREACHABLE
```

---

# 📡 Raspberry Pi ↔ Arduino Protocol

The communication interface uses a lightweight text-based serial protocol.

## Motor Command

```text
M <left> <right>
```

Example:

```text
M 100 100
```

---

## Boom Command

```text
B <length_mm> <velocity_mm_s>
```

Example:

```text
B 270.0 5.0
```

---

## Clamshell Command

```text
C <stroke_mm> <velocity_mm_s>
```

Example:

```text
C 45.0 5.0
```

---

## Emergency Stop

```text
X
```

---

## Telemetry

Arduino sends telemetry using:

```text
T <v_bat> <i_bat> <i_boom> <i_clam>
  <i_fl> <i_fr> <i_rl> <i_rr>
  <boom_mm> <clam_mm>
  <enc_fl> <enc_fr> <enc_rl> <enc_rr>
  <pitch> <roll>
```

The Raspberry Pi parses this information and creates a unified robot state using the sensor-fusion layer.

---

# 🗂️ Project Structure

```text
excavation_control/
│
├── blocks/
│   │
│   ├── actuators/
│   │   ├── clamshell_actuator.py
│   │   ├── linear_actuator.py
│   │   └── wheel_drive.py
│   │
│   ├── control/
│   │   ├── penetration_control.py
│   │   ├── power_manager.py
│   │   └── scoop_control.py
│   │
│   ├── detection/
│   │   ├── load_sensing.py
│   │   ├── reachability.py
│   │   ├── slip_detection.py
│   │   ├── soil_contact.py
│   │   └── stall_detection.py
│   │
│   ├── safety/
│   │   └── safety_supervisor.py
│   │
│   └── sensors/
│       ├── battery_monitor.py
│       ├── camera_sensor.py
│       ├── current_sensor.py
│       ├── encoder_sensor.py
│       ├── imu_sensor.py
│       ├── lidar_sensor.py
│       └── sensor_fusion.py
│
├── comm/
│   └── arduino_serial.py
│
├── config/
│   ├── hardware.py
│   └── thresholds.py
│
└── state_machine/
    └── states.py
```

---

# ⚙️ Configuration

Robot-specific parameters are centralized in:

```text
config/hardware.py
```

Important parameters include:

```python
BOOM_LA_LENGTH_CLOSED_MM
BOOM_LA_LENGTH_OPEN_MM
BOOM_LA_SOFT_MIN_MM
BOOM_LA_SOFT_MAX_MM

CLAM_LA_STROKE_MM

PENETRATION_DEPTH_TARGET_MM

WHEEL_DIAMETER_MM
WHEEL_GEAR_RATIO
TRACK_WIDTH_MM

SERIAL_PORT
SERIAL_BAUD

LIDAR_PORT
LIDAR_BAUD

CAMERA_WIDTH
CAMERA_HEIGHT
```

Control and safety thresholds are centralized in:

```text
config/thresholds.py
```

This makes the software easier to calibrate without modifying the main control algorithms.

---

# 🧪 Simulation Mode

The project includes a simulation mode that allows parts of the control system to be tested without the physical robot.

In:

```text
config/hardware.py
```

set:

```python
SIMULATION_MODE = True
```

In simulation mode, the system can generate sample:

- Arduino telemetry
- Battery readings
- Actuator feedback
- Current readings
- LiDAR scans

This enables software development and algorithm testing before connecting the physical robot.

---

# 🔌 Hardware Configuration

The current software configuration is intended around the following architecture:

### Computing

- Raspberry Pi
- Arduino Mega-class controller

### Drive

- 4 × OG555 geared motors
- OE-37 encoder feedback
- 4 × BTS7960 motor drivers

### Excavation

- Boom linear actuator
- Clamshell linear actuator

### Sensors

- Wheel encoders
- Current sensors
- IMU
- Battery voltage/current sensing
- LiDAR
- Camera

> Hardware values in `config/hardware.py` and `config/thresholds.py` are explicitly marked as sample/calibration values where applicable. They must be validated against the final physical robot before deployment.

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Srihaasinipinisetti/CAT_EXCAVATION.git
cd CAT_EXCAVATION
```

Create a Python environment:

```bash
python3 -m venv venv
```

Activate it:

### Linux / Raspberry Pi

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install required dependencies according to the modules enabled on the robot.

For Arduino communication:

```bash
pip install pyserial
```

For camera processing:

```bash
pip install opencv-python
```

Additional LiDAR libraries can be installed depending on the specific LiDAR hardware used.

---

# ▶️ Running in Simulation

Make sure:

```python
SIMULATION_MODE = True
```

The serial interface will then operate without requiring a physical Arduino and will generate simulated telemetry.

---

# 🔧 Preparing for the Physical Robot

Before enabling hardware operation:

### 1. Configure the serial port

For Raspberry Pi:

```python
SERIAL_PORT = "/dev/ttyACM0"
```

### 2. Verify baud rate

```python
SERIAL_BAUD = 115200
```

### 3. Calibrate actuator limits

Verify:

```text
Boom minimum
Boom maximum
Clamshell minimum
Clamshell maximum
```

### 4. Calibrate current thresholds

Measure actual:

```text
Wheel current
Boom actuator current
Clamshell actuator current
Battery current
```

### 5. Calibrate geometry

Measure:

```text
Wheel diameter
Track width
Boom linkage geometry
Actuator mounting points
Digging reach
```

### 6. Test safety systems

Verify:

- Emergency stop
- Overcurrent protection
- Undervoltage detection
- Stall detection
- Communication-loss detection
- IMU tip detection

**Do not run the excavation mechanism at full power until all safety limits have been validated.**

---

# 🎯 Design Goals

The control architecture is designed around five major goals:

### 1. Autonomous Excavation

Minimize dependence on manual intervention during the excavation cycle.

### 2. Adaptive Digging

Adjust penetration behavior according to measured excavation resistance.

### 3. Sensor-Based Decision Making

Use current, encoder, IMU, actuator and distance information instead of relying only on predefined timing.

### 4. Fault Tolerance

Detect abnormal conditions and enter recovery or fault states rather than blindly continuing the mission.

### 5. Modular Architecture

Keep sensing, control, detection, actuation and safety modules independent so individual components can be calibrated and improved without rewriting the entire system.

---

# 🧩 Key Algorithms

The current implementation includes:

- Skid-steer drive control
- Encoder-based odometry
- Sensor fusion
- Current-based resistance classification
- Adaptive penetration control
- Soil-contact detection
- Clamshell scoop control
- Current-based load estimation
- Wheel-slip detection
- Actuator stall detection
- Wheel stall detection
- Reachability analysis
- Battery monitoring
- Power arbitration
- IMU-based tip detection
- Communication-loss detection
- Emergency-stop supervision
- Finite-state excavation control

---

# 📊 Control Frequencies

Configured control rates:

```text
Main Control Loop : 50 Hz
Safety Supervisor  : 100 Hz
```

The higher safety-loop frequency allows critical conditions to be detected independently of slower mission-level decisions.

---

# 🏗️ Development Philosophy

The project follows a **modular block-based control architecture**.

Each subsystem has a defined responsibility:

```text
Sensors
   ↓
Sensor Fusion
   ↓
Detection / Estimation
   ↓
Control
   ↓
Actuation
   ↓
Physical Robot
   ↓
Telemetry
   ↺
```

Safety operates across the architecture:

```text
              ┌─────────────────┐
              │ Safety Supervisor│
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Sensors        Control       Actuators
```

This separation makes the system easier to test, debug, calibrate and extend.

---

# 🚧 Current Development Status

The repository currently contains the core software blocks for:

- Hardware abstraction
- Sensor processing
- Actuator control
- Excavation control
- Detection algorithms
- Power management
- Safety supervision
- State-machine definition
- Raspberry Pi ↔ Arduino communication
- Simulation

Some components, including physical LiDAR drivers, final Arduino firmware integration and several geometry/calibration parameters, are intended to be completed and validated against the final robot hardware.

---

# 🔮 Future Improvements

Potential future extensions include:

- Full autonomous mission executor
- CAD-derived inverse kinematics
- Real-time LiDAR-based dig-zone mapping
- Camera-based excavation alignment
- Improved soil classification
- Adaptive penetration learning
- Automatic actuator calibration
- More robust slip estimation
- Closed-loop traction control
- Data logging and telemetry visualization
- Hardware-in-the-loop testing
- Automated parameter optimization

---

# 👥 Project

**Caterpillar Autonomy Challenge**

**Project:** Autonomous Excavation Control System

**Repository:**  
`CAT_EXCAVATION`

Developed as part of an autonomous excavation robotics system focusing on **safe, adaptive and sensor-driven excavation**.

---

## ⚠️ Disclaimer

This repository contains a robotics control framework intended for development and experimentation.

Parameters marked as **SAMPLE**, calibration values, actuator limits, current thresholds, and mechanical geometry must be validated against the actual robot before deployment.

Never operate the physical excavation mechanism without independently verifying emergency-stop functionality and mechanical/electrical safety limits.
