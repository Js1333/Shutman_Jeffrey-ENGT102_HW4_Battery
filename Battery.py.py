"""
ENGT-102 Homework 4: Battery Runtime Simulator
Reads an operating schedule from battery_schedule.csv, simulates battery
energy use segment by segment, reports status, and plots the results.
"""

import matplotlib
matplotlib.use("Agg")  # lets the plot be saved without needing a display
import matplotlib.pyplot as plt

# ---------------- System data ----------------
BATTERY_CAPACITY_WH = 36.0

POWER_W = {
    "standby": 3,
    "sensing": 8,
    "drive": 30,
    "transmit": 18,
}


# ---------------- Functions ----------------
def calculate_energy_used(power_w, minutes):
    """Return energy used (Wh) for a segment given power (W) and duration (min)."""
    duration_hr = minutes / 60
    return power_w * duration_hr


def get_battery_status(remaining_wh, capacity_wh):
    """Return a battery-status message based on the energy remaining."""
    if remaining_wh <= 0:
        return "BATTERY DEPLETED"
    percent = remaining_wh / capacity_wh * 100
    if percent <= 20:
        return "LOW BATTERY"
    return "NORMAL"


# ---------------- Read the schedule ----------------
schedule = []  # list of (mode, duration_min)
with open("battery_schedule.csv", "r") as file:
    next(file)  # skip header line
    for line in file:
        line = line.strip()
        if line == "":
            continue
        parts = line.split(",")
        mode = parts[0].strip()
        duration_min = float(parts[1])
        schedule.append((mode, duration_min))

# ---------------- Simulation ----------------
battery_remaining_wh = BATTERY_CAPACITY_WH
elapsed_min = 0.0
total_energy_wh = 0.0

# Lists for the plot (include initial condition)
time_list = [0.0]
battery_list = [BATTERY_CAPACITY_WH]

print("BATTERY RUNTIME SIMULATION")
print("=" * 88)
print(f"{'Seg':<4}{'Mode':<10}{'Duration (min)':>15}{'Energy Used (Wh)':>18}"
      f"{'Remaining (Wh)':>16}   Status")
print("-" * 88)

for i, (mode, duration_min) in enumerate(schedule, start=1):
    power = POWER_W[mode]
    energy_used = calculate_energy_used(power, duration_min)

    elapsed_min += duration_min
    total_energy_wh += energy_used
    battery_remaining_wh = battery_remaining_wh - energy_used

    status = get_battery_status(battery_remaining_wh, BATTERY_CAPACITY_WH)

    time_list.append(elapsed_min)
    battery_list.append(battery_remaining_wh)

    print(f"{i:<4}{mode:<10}{duration_min:>15.1f}{energy_used:>18.2f}"
          f"{battery_remaining_wh:>16.2f}   {status}")

print("=" * 88)

# ---------------- Plot ----------------
plt.figure(figsize=(9, 5.5))
plt.plot(time_list, battery_list, marker="o", linewidth=2, color="tab:blue")
plt.axhline(0.2 * BATTERY_CAPACITY_WH, color="orange", linestyle="--",
            label="20% low-battery threshold")
plt.axhline(0, color="red", linestyle="--", label="Depleted (0 Wh)")
plt.title("Battery Energy Remaining vs. Elapsed Time")
plt.xlabel("Elapsed Time (min)")
plt.ylabel("Battery Energy Remaining (Wh)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("battery_runtime.png", dpi=150)
plt.close()

# ---------------- Final summary ----------------
percent_remaining = battery_remaining_wh / BATTERY_CAPACITY_WH * 100

print("\nFINAL SIMULATION SUMMARY")
print("-" * 40)
print(f"Total operating time:          {elapsed_min:.1f} min ({elapsed_min / 60:.2f} hr)")
print(f"Total energy required:         {total_energy_wh:.2f} Wh")
print(f"Battery energy remaining:      {battery_remaining_wh:.2f} Wh")
print(f"Battery percentage remaining:  {percent_remaining:.1f}%")

if battery_remaining_wh > 0:
    print("RESULT: The battery CAN complete the full schedule.")
else:
    print("RESULT: The battery CANNOT complete the full schedule.")
print("\nPlot saved as battery_runtime.png")