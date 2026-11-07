import predict_turnover as runner
import turnover_common as common
from turnover_common import *


if __name__=='__main__':
    variant=os.environ.get('MTS_INTERPOLATION','invariant')
    assert variant in ['invariant','invariant-half']
    bank_status=ROOT/'results/invariant-banks/status.json'
    manifest=json.loads(bank_status.read_text())
    assert manifest['all_checks_passed']
    for path,sha in manifest['files'].items():
        assert digest(path)==sha,path
    original_verify=runner.verify_source
    def verify_input(path,chain):
        path=Path(path).resolve()
        if path.is_relative_to(ROOT):
            assert str(path) in manifest['files'],path
            assert digest(path)==manifest['files'][str(path)],path
        else:
            original_verify(path,chain)
    common.TAIL=ROOT/(variant+'-banks')
    time_refinement=int(os.environ.get('MTS_TIME_REFINEMENT','1'))
    assert time_refinement in [1,2]
    suffix='-prediction' if time_refinement==1 else '-time2-prediction'
    runner.ROOT=ROOT/(variant+suffix)
    runner.verify_source=verify_input
    original_reconstruct=runner.reconstruct
    def reconstruct_with_time(basis,model,baseline,window,settings):
        settings['steps']*=time_refinement
        return original_reconstruct(basis,model,baseline,window,settings)
    runner.reconstruct=reconstruct_with_time
    original_finish=runner.finish
    def finish_with_bank(folder,report,script,extra=()):
        report['interpolation']=variant
        original_finish(folder,report,script,[*extra,bank_status,ROOT/'INVARIANT-INTERPOLATION.md'])
    runner.finish=finish_with_bank
    runner.main()
