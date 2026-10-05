"""
Numerical thresholds — SAMPLE VALUES. Tune via calibration experiments.
"""

# --- Wheel motor current (OG555 @ 12 V) ---
I_WHEEL_NO_LOAD_A = 0.5
I_WHEEL_RATED_A = 3.38
I_WHEEL_WARN_A = 2.87
I_WHEEL_CRIT_A = 3.21

# --- Linear actuator current (1.5 A rated, Cytron FD04A-class) ---
I_LA_RATED_A = 1.5
I_LA_WARN_A = 1.28
I_LA_CRIT_A = 1.43
I_LA_EMERG_A = 2.25
I_LA_WARN_OFF_A = 1.15
I_LA_CRIT_OFF_A = 1.35

# --- Battery (3S LiPo) ---
V_BAT_WARN_V = 10.8
V_BAT_CRIT_V = 10.2
V_BAT_EMERG_V = 9.6
I_BAT_CONT_A = 15.0
I_BAT_WARN_FRAC = 0.70
I_BAT_CRIT_FRAC = 0.85

# --- Stall detection ---
STALL_LA_DELTA_S_MM = 1.0
STALL_LA_TIME_BOOM_S = 0.4
STALL_LA_TIME_CLAM_S = 0.35
STALL_WHEEL_MIN_COUNTS = 3
STALL_WHEEL_WINDOW_S = 0.3
STALL_WHEEL_I_MIN_A = 2.0
STALL_WHEEL_TIME_S = 0.8
V_CMD_MIN_LA_MM_S = 2.0

# --- Slip ---
SLIP_WARN = 0.15
SLIP_CRIT = 0.28
SLIP_EMERG = 0.45
SLIP_V_EPS_M_S = 0.05

# --- Soil contact ---
I_BOOM_CONTACT_DELTA_A = 0.35
V_BOOM_CONTACT_FRAC = 0.3
CONTACT_CONFIRM_TIME_S = 0.15

# --- Penetration resistance (boom current bands) ---
I_PEN_LOW_A = 0.7
I_PEN_MED_A = 1.1
I_PEN_HIGH_A = 1.28
PEN_RETRACT_MM = 8.0

# --- Load sensing (lift segment) ---
LIFT_DELTA_S_BOOM_MM = 12.0
LIFT_SPEED_MM_S = 5.0
DI_LIFT_FULL_MIN_A = 0.45
DI_LIFT_PARTIAL_MIN_A = 0.20

# --- Reachability ---
REACH_TOL_MM = 40.0
REACH_MAX_RETRIES = 3

# --- IMU tip safety ---
PITCH_WARN_DEG = 12.0
PITCH_CRIT_DEG = 18.0
ROLL_WARN_DEG = 10.0
ROLL_CRIT_DEG = 15.0

# --- Sensor timeouts ---
ENCODER_STALE_MS = 200
IMU_STALE_MS = 100
TELEM_STALE_MS = 500
COMM_TIMEOUT_S = 5.0

# --- State timeouts (seconds) ---
T_SELF_CHECK = 45.0
T_ALIGN = 60.0
T_POSITION = 35.0
T_CONTACT = 20.0
T_PENETRATION = 25.0
T_SCOOP = 15.0
T_LIFT = 20.0
T_LOAD_CHECK = 8.0
T_DUMP = 12.0
T_RESET = 30.0

# --- Recovery ---
MAX_RETRY_STALL = 1
MAX_RETRY_SCOOP = 2
MAX_RETRY_REACH = 3

# --- Power filter ---
CURRENT_EMA_TAU_S = 0.5
I_HIGH_HOLD_S = 0.2
I_CRIT_HOLD_S = 0.15
