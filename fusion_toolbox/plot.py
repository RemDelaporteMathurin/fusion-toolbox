import numpy as np
import matplotlib.pyplot as plt


def plot_shot(shot_number):
    # Read data from the CSV file using numpy.genfromtxt
    data = np.genfromtxt(f'shots/shot_{shot_number}.csv', delimiter=',',
                        names=True, dtype=None, encoding=None)

    # Extract data columns
    time_points = data['Time']
    plasma_current_points = data['Plasma_Current_A']
    plasma_density_points = data['Plasma_Density_particlesm3']
    plasma_temperature_points = data['Plasma_Temperature_K']
    fusion_power_points = data['Fusion_Power_W']
    icrh_power_points = data['ICRH_Power_W']
    radiation_power_points = data['Radiation_Power_W']
    lhcd_power_points = data['LHCD_Power_W']
    nbi_power_points = data['NBI_Power_W']
    total_heating_power_points = data['Total_Heating_Power_W']
    injection_rate_points = data['Injection_Rate']

    # Create a figure with 5 subplots
    fig, axs = plt.subplots(5, 1, figsize=(10, 12), sharex=True)
    fig.suptitle('Fusion Plasma Data Over Time', fontsize=16)

    # Subplot 1: Plasma Current
    axs[0].plot(time_points, plasma_current_points, label='Plasma Current (A)', color='tab:blue')
    axs[0].set_ylabel('Plasma Current (A)')
    axs[0].legend(loc='upper left')

    # Subplot 2: Plasma Density
    axs[1].plot(time_points, plasma_density_points, label='Plasma Density (particles/m^3)', color='tab:orange')
    axs[1].set_ylabel('Plasma Density (particles/m^3)')
    axs[1].legend(loc='upper left')

    # Subplot 3: Plasma Temperature
    axs[2].plot(time_points, plasma_temperature_points, label='Plasma Temperature (K)', color='tab:green')
    axs[2].set_ylabel('Plasma Temperature (K)')
    axs[2].legend(loc='upper left')

    # Subplot 4: Fusion Power and Radiation Power
    axs[3].plot(time_points, fusion_power_points, label='Fusion Power (W)', color='tab:red')
    axs[3].plot(time_points, radiation_power_points, label='Radiation Power (W)', linestyle='--', color='tab:purple')
    axs[3].set_ylabel('Power (W)')
    axs[3].legend(loc='upper left')

    # Subplot 5: NBI, ICRH, and LHCD Power
    axs[4].plot(time_points, nbi_power_points, label='NBI Power (W)')
    axs[4].plot(time_points, icrh_power_points, label='ICRH Power (W)')
    axs[4].plot(time_points, lhcd_power_points, label='LHCD Power (W)')
    axs[4].plot(time_points, total_heating_power_points, label='Total')
    axs[4].set_xlabel('Time')
    axs[4].set_ylabel('Power (W)')
    axs[4].legend(loc='upper left')


if __name__ == "__main__":
    plot_shot('674546')

    # Adjust subplot spacing
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    # Show the plot
    plt.show()
