import numpy as np

def get_noisy_interceptor_position(true_pos):
    noise = np.random.normal(0, 1.0, size=2)
    return true_pos + noise

def evasive_heading(current_pos, interceptor_pos, current_heading_rad):
    direction = interceptor_pos - current_pos
    distance = np.linalg.norm(direction)

    if distance > 30:
        return current_heading_rad

    angle_to_threat = np.arctan2(direction[1], direction[0])
    evade_angle = angle_to_threat + np.pi

    # Add a slight bias to avoid mirrored patterns
    evade_angle += np.radians(np.random.uniform(-10, 10))

    new_heading = 0.4 * current_heading_rad + 0.6 * evade_angle
    return new_heading
