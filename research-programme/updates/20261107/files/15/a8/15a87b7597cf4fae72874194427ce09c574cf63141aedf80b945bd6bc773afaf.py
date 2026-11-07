from corrector import *
from scipy.interpolate import make_interp_spline


class HigherOrderCorrector(Corrector):
    def __init__(self, packet):
        self.support, self.vectors, self.units = packet["support"], packet["vectors"], packet["units"]
        self.splines = {name: make_interp_spline(packet["efold"], packet[name], k=5, axis=0)
                        for prefix in ("U", "V") for name in (prefix + "_A", prefix + "_B", prefix + "_C")}

