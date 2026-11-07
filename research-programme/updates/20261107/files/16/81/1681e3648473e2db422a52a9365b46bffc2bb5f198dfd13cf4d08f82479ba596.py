from paired_redistribution import *
import compute_resolved as runner


if __name__=='__main__':
    runner.integrate_resolved=integrate_paired
    def local_finish(folder,report,script,extra=()):
        report.update(paired_representation=True,identical_incoming_absorption_photons_ordered=True,
                      forward_inverse_symmetry_factor=.5)
        finish(folder,report,__file__,[Path(script),ROOT/'paired_redistribution.py',*extra])
    runner.finish=local_finish
    runner.main()
