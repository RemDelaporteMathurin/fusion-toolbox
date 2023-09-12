import csv
import random
import numpy as np
import os

def generate_multiple_shots(num_shots=10):
    # Create a directory to store the CSV files
    if not os.path.exists("shots"):
        os.makedirs("shots")

    for shot_number in range(1, num_shots + 1):

        # Generate a unique 6-digit shot number for each shot
        unique_shot_number = ''.join(str(random.randint(0, 9)) for _ in range(6))

        # Specify the start, plateau, and end values for each quantity
        start_current = 0
        plateau_current = random.uniform(start_current, 1500)
        end_current = 0

        start_density = 0
        plateau_density = random.uniform(start_density, 1e19)
        end_density = 0

        start_temperature = 0
        plateau_temperature = random.uniform(start_temperature, 40e6)
        end_temperature = 0

        start_fusion_power = 0
        plateau_fusion_power = random.uniform(start_fusion_power, 2e6)
        end_fusion_power = 0

        start_icrh_power = 0
        plateau_icrh_power = random.uniform(start_icrh_power, 1e6)
        end_icrh_power = 0

        start_radiation_power = 0
        plateau_radiation_power = random.uniform(0, 1) * plateau_fusion_power
        end_radiation_power = 0

        start_lhcd_power = 0
        plateau_lhcd_power = random.uniform(start_lhcd_power, 4e5)
        end_lhcd_power = 0

        start_nbi_power = 0
        plateau_nbi_power = random.uniform(start_nbi_power, 1e6)
        end_nbi_power = 0

        start_injection_rate = 0
        plateau_injection_rate = random.uniform(start_injection_rate, 20e19)
        end_injection_rate = 0

        # Specify the durations for ramp-up, plateau, and ramp-down phases
        duration_rampup = random.uniform(0.1, 0.4)  # Example: Random duration between 0.1 and 0.4
        duration_plateau = random.uniform(0.2, 0.4)  # Example: Random duration between 0.2 and 0.4
        duration_rampdown = 1.0 - (duration_rampup + duration_plateau)

        # Generate data for the shot
        data = generate_data(num_time_points=10000, start_current=start_current, plateau_current=plateau_current, end_current=end_current,
                            start_density=start_density, plateau_density=plateau_density, end_density=end_density,
                            start_temperature=start_temperature, plateau_temperature=plateau_temperature, end_temperature=end_temperature,
                            start_fusion_power=start_fusion_power, plateau_fusion_power=plateau_fusion_power, end_fusion_power=end_fusion_power,
                            start_icrh_power=start_icrh_power, plateau_icrh_power=plateau_icrh_power, end_icrh_power=end_icrh_power,
                            start_radiation_power=start_radiation_power, plateau_radiation_power=plateau_radiation_power, end_radiation_power=end_radiation_power,
                            start_lhcd_power=start_lhcd_power, plateau_lhcd_power=plateau_lhcd_power, end_lhcd_power=end_lhcd_power,
                            start_nbi_power=start_nbi_power, plateau_nbi_power=plateau_nbi_power, end_nbi_power=end_nbi_power,
                            start_injection_rate=start_injection_rate, plateau_injection_rate=plateau_injection_rate, end_injection_rate=end_injection_rate,
                            duration_rampup=duration_rampup, duration_plateau=duration_plateau, duration_rampdown=duration_rampdown)

        # Define the filename with the shot number
        filename = f"shots/shot_{unique_shot_number}.csv"

        # Write data to CSV file
        write_to_csv(data, filename)

        print(f"Data for Shot {unique_shot_number} has been generated and saved as '{filename}'.")


def generate_data(num_time_points, start_current, plateau_current, end_current,
                  start_density, plateau_density, end_density,
                  start_temperature, plateau_temperature, end_temperature,
                  start_fusion_power, plateau_fusion_power, end_fusion_power,
                  start_icrh_power, plateau_icrh_power, end_icrh_power,
                  start_radiation_power, plateau_radiation_power, end_radiation_power,
                  start_lhcd_power, plateau_lhcd_power, end_lhcd_power,
                  start_nbi_power, plateau_nbi_power, end_nbi_power,
                  start_injection_rate, plateau_injection_rate, end_injection_rate,
                  duration_rampup, duration_plateau, duration_rampdown,
                  noise_stddev=0.1):
    # Define the time points
    time_points = list(range(1, num_time_points + 1))

    # Calculate the phase end points based on durations
    phase1_end = int(num_time_points * duration_rampup)
    phase2_end = int(num_time_points * (duration_rampup + duration_plateau))
    phase3_end = int(num_time_points * (duration_rampup + duration_plateau + duration_rampdown))
    # Generate data for all quantities
    plasma_current = np.concatenate([
        np.linspace(start_current, plateau_current, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_current),  # Phase 2: Constant
        np.linspace(plateau_current, end_current, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points) * plateau_current/10  # Add noise

    plasma_density = np.concatenate([
        np.linspace(start_density, plateau_density, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_density),  # Phase 2: Constant
        np.linspace(plateau_density, end_density, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points) * plateau_density/10  # Add noise

    plasma_temperature = np.concatenate([
        np.linspace(start_temperature, plateau_temperature, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_temperature),  # Phase 2: Constant
        np.linspace(plateau_temperature, end_temperature, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points) * plateau_temperature/10  # Add noise

    fusion_power = np.concatenate([
        np.linspace(start_fusion_power, plateau_fusion_power, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_fusion_power),  # Phase 2: Constant
        np.linspace(plateau_fusion_power, end_fusion_power, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points)* plateau_fusion_power/10   # Add noise

    icrh_power = np.concatenate([
        np.linspace(start_icrh_power, plateau_icrh_power, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_icrh_power),  # Phase 2: Constant
        np.linspace(plateau_icrh_power, end_icrh_power, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points)* plateau_icrh_power/10  # Add noise

    radiation_power = np.concatenate([
        np.linspace(start_radiation_power, plateau_radiation_power, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_radiation_power),  # Phase 2: Constant
        np.linspace(plateau_radiation_power, end_radiation_power, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points)* plateau_radiation_power/10  # Add noise

    lhcd_power = np.concatenate([
        np.linspace(start_lhcd_power, plateau_lhcd_power, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_lhcd_power),  # Phase 2: Constant
        np.linspace(plateau_lhcd_power, end_lhcd_power, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points)* plateau_lhcd_power/10  # Add noise

    nbi_power = np.concatenate([
        np.linspace(start_nbi_power, plateau_nbi_power, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_nbi_power),  # Phase 2: Constant
        np.linspace(plateau_nbi_power, end_nbi_power, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points)* plateau_nbi_power/10  # Add noise

    total_heating_power = lhcd_power + nbi_power + icrh_power

    injection_rate = np.concatenate([
        np.linspace(start_injection_rate, plateau_injection_rate, phase1_end),  # Phase 1: Ramp-up
        np.full(phase2_end - phase1_end, plateau_injection_rate),  # Phase 2: Constant
        np.linspace(plateau_injection_rate, end_injection_rate, phase3_end - phase2_end),  # Phase 3: Ramp-down
    ])+ np.random.normal(0, noise_stddev, num_time_points)  # Add noise

    # Return data as dictionaries
    data = {
        'Time': time_points,
        'Plasma_Current (A)': plasma_current,
        'Plasma_Density (particlesm3)': plasma_density,
        'Plasma_Temperature (K)': plasma_temperature,
        'Fusion_Power (W)': fusion_power,
        'ICRH_Power (W)': icrh_power,
        'Radiation_Power (W)': radiation_power,
        'LHCD_Power (W)': lhcd_power,
        'NBI_Power (W)': nbi_power,
        'Total_Heating_Power (W)': total_heating_power,
        'Injection_Rate': injection_rate
    }

    return data

def write_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Plasma_Current (A)', 'Plasma_Density (particlesm3)', 'Plasma_Temperature (K)',
                         'Fusion_Power (W)', 'ICRH_Power (W)', 'Radiation_Power (W)', 'LHCD_Power (W)', 'NBI_Power (W)',
                         'Total_Heating_Power (W)', 'Injection_Rate'])
        for i in range(len(data['Time'])):
            row = []
            for key in ['Time', 'Plasma_Current (A)', 'Plasma_Density (particlesm3)', 'Plasma_Temperature (K)',
                        'Fusion_Power (W)', 'ICRH_Power (W)', 'Radiation_Power (W)', 'LHCD_Power (W)', 'NBI_Power (W)',
                        'Total_Heating_Power (W)', 'Injection_Rate']:
                row.append(data[key][i])
            writer.writerow(row)


if __name__ == "__main__":
    generate_multiple_shots(num_shots=10)