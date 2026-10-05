"""
Hardware geometry and actuator limits — SAMPLE VALUES (change for your robot).
"""

# --- Boom linear actuator (12 V, 100 mm stroke) ---
BOOM_LA_LENGTH_CLOSED_MM = 205.0
BOOM_LA_LENGTH_OPEN_MM = 305.0
BOOM_LA_STROKE_MM = BOOM_LA_LENGTH_OPEN_MM - BOOM_LA_LENGTH_CLOSED_MM
BOOM_LA_SOFT_MIN_MM = 210.0
BOOM_LA_SOFT_MAX_MM = 300.0
BOOM_LA_RATED_CURRENT_A = 1.5

# --- Clamshell linear actuator (12 V, 50 mm stroke) ---
CLAM_LA_STROKE_MM = 50.0
CLAM_LA_SOFT_MIN_MM = 2.0
CLAM_LA_SOFT_MAX_MM = 48.0
CLAM_LA_RATED_CURRENT_A = 1.5

# --- Clamshell assembly height proxy (mm) ---
CLAM_HEIGHT_OPEN_MM = 236.0
CLAM_HEIGHT_CLOSED_MM = 270.0

# --- Linkage (from sketch — used in reachability samples) ---
LINK_BOOM_MM = 405.0
LINKAGE_ANGLE_CLOSED_DEG = 60.0
LINKAGE_ANGLE_OPEN_DEG = 120.0

# --- Excavation mission ---
PENETRATION_DEPTH_TARGET_MM = 25.0
# mm boom stroke per mm depth — CALIBRATE; sample placeholder
K_DEPTH_MM_STROKE_PER_MM_DEPTH = 1.2

# --- Wheels (OG555 + OE-37) ---
WHEEL_DIAMETER_MM = 100.0
WHEEL_RATED_RPM = 50.0
WHEEL_GEAR_RATIO = 180
ENCODER_CPR_MOTOR_SHAFT = 7
ENCODER_CPR_WHEEL_SHAFT = ENCODER_CPR_MOTOR_SHAFT * WHEEL_GEAR_RATIO
TRACK_WIDTH_MM = 420.0  # SAMPLE — measure on robot

# --- Power ---
BATTERY_CELLS_S = 3
BATTERY_NOMINAL_V = 11.1
BATTERY_FULL_V = 12.6

# --- Serial (Pi ↔ Arduino) ---
SERIAL_PORT = "/dev/ttyACM0"
SERIAL_BAUD = 115200

# --- LiDAR / camera (Pi-side) ---
LIDAR_PORT = "/dev/ttyUSB0"
LIDAR_BAUD = 115200
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# --- Control loop ---
CONTROL_HZ = 50
SAFETY_HZ = 100

# --- Simulation (no Arduino / sensors) ---
SIMULATION_MODE = True
