import math

import numpy as np

from evadex.interceptor import Interceptor
from evadex.missile import Missile


def test_missile_heading_clamp():
    m = Missile(0, 0, 1.0, 0.0, max_turn_deg_per_step=10)
    original = m.heading
    # request a large turn (90 deg); should clamp to max_turn
    target = original + math.radians(90)
    m.update_heading(target)
    assert abs(m.heading - original) <= math.radians(10) + 1e-9


def test_interceptor_pursue_nonincreasing_distance():
    mpos = np.array([10.0, 0.0])
    ic = Interceptor(0.0, 0.0, 1.0)
    d0 = np.linalg.norm(ic.get_position() - mpos)
    ic.pursue(mpos)
    d1 = np.linalg.norm(ic.get_position() - mpos)
    assert d1 <= d0 + 1e-9
