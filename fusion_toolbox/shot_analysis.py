def smooth(data):
    """Smooth the data to remove noise

    Args:
        data (_type_): _description_
    """
    pass

def compute_duration_phases(shot):
    """Determins the duration of the ramp-up, flat-top and ramp down phases
    """
    pass

def compute_flat_top_plasma_temperature(shot):
    pass

def compute_flat_top_plasma_current(shot):
    pass

def compute_flat_top_plasma_density(shot):
    pass

def find_shots_from_fusion_power(fusion_power, rtol):
    """Finds shots in the database with the desired fusion power

    Args:
        fusion_power (float): the desired fusion power
        rtol (float): the relative tolerance
    """
    pass

def compute_average_fusion_power(shots):
    """Computes the average fusion power over some shots

    Args:
        shots (list): shot numbers
    """
    pass

def compute_fusion_gain(shot):
    pass

def date_of_shot(shot):
    """Returns the date of a shot as a datetime object

    Args:
        shot (str): the shot number
    """
    pass