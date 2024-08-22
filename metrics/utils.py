import math


def degrees_to_vector(degrees):
    """
    Convert a direction in degrees to a vector (x, y).
    
    Args:
    degrees (float): The direction in degrees.
    
    Returns:
    tuple: A tuple representing the vector (x, y).
    """
    radians = math.radians(degrees)
    x = math.cos(radians)
    y = math.sin(radians)
    return (x, y)



def is_angle_greater_than_90(x1, y1, x2, y2):
    """
    Determine if the angle between two vectors (x1, y1) and (x2, y2) is greater than 90 degrees.
    
    Args:
    x1, y1: Coordinates of the first vector.
    x2, y2: Coordinates of the second vector.
    
    Returns:
    bool: True if the angle is greater than 90 degrees, False otherwise.
    """
    dot_product = x1 * x2 + y1 * y2
    return dot_product < 0