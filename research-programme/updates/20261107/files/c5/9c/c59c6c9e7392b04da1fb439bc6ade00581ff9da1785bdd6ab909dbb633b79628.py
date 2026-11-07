from run_join import run,ROOT
import json


def main():
    for steps in [2048,4096,8192,16384]:
        run('refine_join_time.py','--steps',str(steps))
        run('check_join_time.py','--steps',str(steps))
        status=json.loads((ROOT/'results'/f'time-control-n{steps}/status.json').read_text())
        if status['all_checks_passed']:
            print('REFINEMENT GATE PASSED',steps,flush=True)
            return
    print('REFINEMENT BUDGET REACHED;RETAIN FAILED GATES',flush=True)


if __name__=='__main__':
    main()

