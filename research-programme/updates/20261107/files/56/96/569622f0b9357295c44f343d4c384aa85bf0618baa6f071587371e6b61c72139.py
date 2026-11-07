import argparse
import run_evolution as driver
from evolution_common import *


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--name',required=True)
    parser.add_argument('--substeps',type=int,default=2)
    parser.add_argument('--maximum',type=int,default=6)
    parser.add_argument('--start',type=float,default=1e-6)
    arguments=parser.parse_args()
    original_step=driver.etd_step
    original_finish=driver.finish
    def refined(system,moment,state,step):
        result=state
        for index in range(arguments.substeps):
            result=original_step(system,moment+index*step/arguments.substeps,result,step/arguments.substeps)
        return result
    def finish_refined(folder,report,script,extra=()):
        report['substeps_per_reported_step']=arguments.substeps
        report['actual_steps']=report['steps']*arguments.substeps
        original_finish(folder,report,script,[*extra,Path(__file__)])
    driver.etd_step=refined
    driver.finish=finish_refined
    driver.run(arguments.model,arguments.name,arguments.maximum,.01,arguments.start,1e-5)


if __name__=='__main__':
    main()
