import csv
import random
import numpy as np
import os


def generate_multiple_shots(
    num_shots=10,
    shot_prefix="2023912",
    Q=1.5,
    current=1500,
    density=1e19,
    temperature=40e6,
    icrh_power=1e6,
    lhcd_power=4e5,
    nbi_power=1e6,
):
    # Create a directory to store the CSV files
    if not os.path.exists("shots"):
        os.makedirs("shots")

    for shot_number in range(1, num_shots + 1):
        # Generate a unique 6-digit shot number for each shot
        unique_shot_number = shot_prefix + f"{shot_number:02d}"

        # Specify the start, plateau, and end values for each quantity
        plateau_icrh_power = np.random.normal(icrh_power, 0.2e6)

        plateau_lhcd_power = np.random.normal(lhcd_power, 0.3e5)

        plateau_nbi_power = np.random.normal(nbi_power, 0.2e6)

        plateau_fusion_power = np.random.normal(Q, 0.2) * (
            plateau_nbi_power + plateau_lhcd_power + plateau_icrh_power
        )

        # Specify the durations for ramp-up, plateau, and ramp-down phases
        duration_rampup = random.uniform(
            100, 200
        )  # Example: Random duration between 0.1 and 0.4
        duration_plateau = random.uniform(
            300, 400
        )  # Example: Random duration between 0.2 and 0.4
        duration_rampdown = random.uniform(100, 200)

        # Generate data for the shot
        data = generate_data(
            num_time_points=10000,
            start_current=0,
            plateau_current=np.random.normal(current, 100),
            end_current=0,
            start_density=0,
            plateau_density=np.random.normal(density, 0.1e19),
            end_density=0,
            start_temperature=0,
            plateau_temperature=np.random.normal(temperature, 1e6),
            end_temperature=0,
            start_fusion_power=0,
            plateau_fusion_power=plateau_fusion_power,
            end_fusion_power=0,
            start_icrh_power=0,
            plateau_icrh_power=plateau_icrh_power,
            end_icrh_power=0,
            start_radiation_power=0,
            plateau_radiation_power=random.uniform(0, 1) * plateau_fusion_power,
            end_radiation_power=0,
            start_lhcd_power=0,
            plateau_lhcd_power=plateau_lhcd_power,
            end_lhcd_power=0,
            start_nbi_power=0,
            plateau_nbi_power=plateau_nbi_power,
            end_nbi_power=0,
            start_injection_rate=0,
            plateau_injection_rate=random.uniform(0, 20e19),
            end_injection_rate=0,
            duration_rampup=duration_rampup,
            duration_plateau=duration_plateau,
            duration_rampdown=duration_rampdown,
        )

        # Define the filename with the shot number
        filename = f"shots/shot_{unique_shot_number}.csv"

        # Write data to CSV file
        write_to_csv(data, filename)

        print(
            f"Data for Shot {unique_shot_number} has been generated and saved as '{filename}'."
        )


def generate_data(
    num_time_points,
    start_current,
    plateau_current,
    end_current,
    start_density,
    plateau_density,
    end_density,
    start_temperature,
    plateau_temperature,
    end_temperature,
    start_fusion_power,
    plateau_fusion_power,
    end_fusion_power,
    start_icrh_power,
    plateau_icrh_power,
    end_icrh_power,
    start_radiation_power,
    plateau_radiation_power,
    end_radiation_power,
    start_lhcd_power,
    plateau_lhcd_power,
    end_lhcd_power,
    start_nbi_power,
    plateau_nbi_power,
    end_nbi_power,
    start_injection_rate,
    plateau_injection_rate,
    end_injection_rate,
    duration_rampup,
    duration_plateau,
    duration_rampdown,
    noise_factor=0.01,
):
    # Calculate the phase end points based on durations
    phase1_end = duration_rampup
    phase2_end = duration_rampup + duration_plateau
    phase3_end = duration_rampup + duration_plateau + duration_rampdown

    # Define the time points
    time_precision = num_time_points / phase3_end  # point/s

    nb_phase1_pts = int(phase1_end * time_precision)
    nb_phase2_pts = int((phase2_end - phase1_end) * time_precision)
    nb_phase3_pts = num_time_points - nb_phase2_pts - nb_phase1_pts

    time_points = np.concatenate(
        [
            np.linspace(0, phase1_end, nb_phase1_pts),  # Phase 1: Ramp-up
            np.linspace(phase1_end, phase2_end, nb_phase2_pts),  # Phase 2: Constant
            np.linspace(phase2_end, phase3_end, nb_phase3_pts),  # Phase 3: Ramp-down
        ]
    )

    # Generate data for all quantities
    plasma_current = np.concatenate(
        [
            np.linspace(
                start_current, plateau_current, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_current),  # Phase 2: Constant
            np.linspace(
                plateau_current, end_current, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_current * noise_factor, num_time_points
    )  # Add noise

    plasma_density = np.concatenate(
        [
            np.linspace(
                start_density, plateau_density, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_density),  # Phase 2: Constant
            np.linspace(
                plateau_density, end_density, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_density * noise_factor, num_time_points
    )  # Add noise

    plasma_temperature = np.concatenate(
        [
            np.linspace(
                start_temperature, plateau_temperature, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_temperature),  # Phase 2: Constant
            np.linspace(
                plateau_temperature, end_temperature, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_temperature * noise_factor, num_time_points
    )  # Add noise

    fusion_power = np.concatenate(
        [
            np.linspace(
                start_fusion_power, plateau_fusion_power, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_fusion_power),  # Phase 2: Constant
            np.linspace(
                plateau_fusion_power, end_fusion_power, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_fusion_power * noise_factor, num_time_points
    )  # Add noise

    icrh_power = np.concatenate(
        [
            np.linspace(
                start_icrh_power, plateau_icrh_power, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_icrh_power),  # Phase 2: Constant
            np.linspace(
                plateau_icrh_power, end_icrh_power, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_icrh_power * noise_factor, num_time_points
    )  # Add noise

    radiation_power = np.concatenate(
        [
            np.linspace(
                start_radiation_power, plateau_radiation_power, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_radiation_power),  # Phase 2: Constant
            np.linspace(
                plateau_radiation_power, end_radiation_power, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_radiation_power * noise_factor, num_time_points
    )  # Add noise

    lhcd_power = np.concatenate(
        [
            np.linspace(
                start_lhcd_power, plateau_lhcd_power, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_lhcd_power),  # Phase 2: Constant
            np.linspace(
                plateau_lhcd_power, end_lhcd_power, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_lhcd_power * noise_factor, num_time_points
    )  # Add noise

    nbi_power = np.concatenate(
        [
            np.linspace(
                start_nbi_power, plateau_nbi_power, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_nbi_power),  # Phase 2: Constant
            np.linspace(
                plateau_nbi_power, end_nbi_power, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_nbi_power * noise_factor, num_time_points
    )  # Add noise

    total_heating_power = lhcd_power + nbi_power + icrh_power

    injection_rate = np.concatenate(
        [
            np.linspace(
                start_injection_rate, plateau_injection_rate, nb_phase1_pts
            ),  # Phase 1: Ramp-up
            np.full(nb_phase2_pts, plateau_injection_rate),  # Phase 2: Constant
            np.linspace(
                plateau_injection_rate, end_injection_rate, nb_phase3_pts
            ),  # Phase 3: Ramp-down
        ]
    ) + np.random.normal(
        0, plateau_injection_rate * noise_factor, num_time_points
    )  # Add noise

    # Return data as dictionaries
    data = {
        "Time (s)": time_points,
        "Plasma_Current (A)": plasma_current,
        "Plasma_Density (particlesm3)": plasma_density,
        "Plasma_Temperature (K)": plasma_temperature,
        "Fusion_Power (W)": fusion_power,
        "ICRH_Power (W)": icrh_power,
        "Radiation_Power (W)": radiation_power,
        "LHCD_Power (W)": lhcd_power,
        "NBI_Power (W)": nbi_power,
        "Total_Heating_Power (W)": total_heating_power,
        "Injection_Rate": injection_rate,
    }

    return data


def write_to_csv(data, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(list(data.keys()))
        nb_rows = len(data[list(data.keys())[0]])
        for i in range(nb_rows):
            row = []
            for quantity in data.values():
                row.append(quantity[i])
            writer.writerow(row)


if __name__ == "__main__":
    year = 2023
    months = [1, 2, 3, 4, 5]
    days = range(1, 10)
    for month in months:
        for day in days:
            prefix = f"{year}{month:02d}{day:02d}"
            Q = 2/max(months)*month + 1
            generate_multiple_shots(num_shots=4, shot_prefix=prefix, Q=Q)
