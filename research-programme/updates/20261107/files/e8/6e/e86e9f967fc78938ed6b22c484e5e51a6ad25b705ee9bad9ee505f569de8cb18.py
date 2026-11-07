from source_pair_common import *
import replay_coefficients as replay


def main():
    assert '--variant' not in sys.argv
    sys.argv.extend(['--variant','balanced'])
    replay.ROOT=ROOT
    replay.ancestors=ancestors
    replay.verify_source=verify_source
    def recorded_finish(folder,report,script,extra=()):
        report.update(pairing='source-adjoint',reused_evolution_equations=str(Path(replay.__file__).resolve()))
        finish(folder,report,__file__,[*extra,script])
    replay.finish=recorded_finish
    replay.main()


if __name__=='__main__':
    main()
