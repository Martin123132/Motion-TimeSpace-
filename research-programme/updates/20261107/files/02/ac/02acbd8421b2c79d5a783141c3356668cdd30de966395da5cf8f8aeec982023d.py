import ctypes
from ctypes import wintypes
import sys
import run228


def windows_modest():
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.SetPriorityClass.restype = wintypes.BOOL
    if not kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x4000):
        raise ctypes.WinError(ctypes.get_last_error())


if __name__ == '__main__':
    path = run228.ROOT / 'runtime-repair.json'
    identity = dict(launcher_sha256=run228.digest(__file__),
                    notes_sha256=run228.digest(run228.ROOT / 'RUNTIME-REPAIR.md'),
                    configuration_sha256=run228.digest(run228.ROOT / 'configuration.json'))
    if sys.argv[1] == 'freeze':
        assert not path.exists()
        run228.write(path, identity)
        print('Runtime-only repair frozen; numerical protocol unchanged', flush=True)
    else:
        assert run228.read(path) == identity
        run228.modest = windows_modest
        if sys.argv[1] == 'evaluate':
            run228.evaluate()
        elif sys.argv[1] == 'gravity':
            import gravity228
            gravity228.main()
        else:
            raise ValueError(sys.argv[1])
