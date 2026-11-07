from ctypes import POINTER, byref, c_double, c_int

from .baseconfig import fortran_class, np, numpy_1d
from .dark_energy import DarkEnergyModel


@fortran_class
class MTSTwoField(DarkEnergyModel):
    _fortran_class_module_ = 'MTSTwoField'
    _fortran_class_name_ = 'TMTSTwoField'
    _fields_ = [('slow_mass_mpc', c_double), ('heavy_mass_mpc', c_double),
        ('heavy_fraction', c_double), ('heavy_exact_limit', c_double),
        ('seed_scale', c_double), ('initial_time_factor', c_double)]
    _methods_ = [(name, [numpy_1d, numpy_1d, numpy_1d, POINTER(c_int)])
        for name in ['SetSlowTable', 'SetHeavyTable', 'SetHeavyBackground']]

    def set_table(self, method, loga, first, second):
        arrays = [np.ascontiguousarray(values, dtype=np.float64) for values in [loga, first, second]]
        if not all(values.ndim == 1 and np.isfinite(values).all() for values in arrays):
            raise ValueError('Tables must be finite one-dimensional arrays')
        if len({len(values) for values in arrays}) != 1 or len(arrays[0]) < 4:
            raise ValueError('Tables must have matching lengths of at least four')
        if np.any(np.diff(arrays[0]) <= 0):
            raise ValueError('Scale factors must strictly increase')
        getattr(self, 'f_' + method)(*arrays, byref(c_int(len(arrays[0]))))
        return self

    def __getstate__(self):
        raise TypeError('MTS native spline state cannot be pickled')
