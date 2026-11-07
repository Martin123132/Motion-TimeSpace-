from consistent_spectral_basis import ConsistentBasis
import extended_system

extended_system.StableBasis = ConsistentBasis


class ConsistentSystem(extended_system.ExtendedSystem):
    def __init__(self, model, count=32, maximum=8, bank=None, stride=1):
        super().__init__(model, count, maximum, bank, stride)
