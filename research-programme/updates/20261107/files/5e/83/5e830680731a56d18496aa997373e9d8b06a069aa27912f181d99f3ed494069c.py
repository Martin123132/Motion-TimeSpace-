from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_compensated_acceleration_polynomial_v2_20261001 import CompensatedPolynomial,cheb_product,paired_cheb,decimal_values
from annular_resolved_acceleration_channels_20261001 import directions,channel_geometry
from decimal import Decimal,localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Cannot pin one core')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+1200

    def progress(stage):
        evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
        evidence.save()
        print(json.dumps(evidence.report['progress']),flush=True)
        if perf_counter()>deadline:
            raise RuntimeError('Safe polynomial probe boundary')

    def save(name,**values):
        path = evidence.output/(name+'.npz')
        if path.exists():
            raise FileExistsError(path)
        np.savez_compressed(path,**values)
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-compensated-acceleration-polynomial.md')
        evidence.own(evidence.root/'scripts/annular_compensated_acceleration_polynomial_v2_20261001.py')
        evidence.own(evidence.root/'DERIVATION-20261001-compensated-source-binding.md')
        evidence.report.update(branch=args.branch,level='third',github_action=False,subagents_used=False,
            same_quadrature_required=True,source_variants_separate=True,valid_for_claim=False)
        local,width,change0,change1,change2,map0,map1,field1,field2 = sp.symbols('x width d0 d1 d2 w0 w1 q1 q2')
        numerator = width*(change0+local*(change1+local*change2))-(map0+map1*local)*(field1+2*local*field2)
        constructed = width*change0-map0*field1+local*(width*change1-2*map0*field2-map1*field1
            +local*(width*change2-2*map1*field2))
        evidence.check('exact_numerator_identity',sp.expand(numerator-constructed)==0)
        with localcontext() as context:
            context.prec = 80
            first = np.array([[Decimal('1.000000000000000000000000000001'),Decimal(0)]],dtype=object)
            unit = np.array([[Decimal(1),Decimal(0)]],dtype=object)
            difference = cheb_product(unit,first)-cheb_product(unit,unit)
            evidence.check('manufactured_nonzero_remainder',difference[0,0]==Decimal('1e-30') and np.all(difference[0,1:]==0))
            evidence.check('rounded_subtraction_negative_control',float(first[0,0])-1==0 and float(difference[0,0])!=0)
            evidence.check('incompatible_map_not_zero',(difference[0,0]-Decimal('1e-20'))!=0)
            arguments = np.array([Decimal(index)/10 for index in range(-9,10)],dtype=object)
            left = np.tile(np.array([Decimal(2),Decimal(-3),Decimal(1)],dtype=object),(len(arguments),1))
            right = np.tile(np.array([Decimal(1),Decimal(4)],dtype=object),(len(arguments),1))
            product = paired_cheb(cheb_product(left,right),arguments)
            direct = paired_cheb(left,arguments)*paired_cheb(right,arguments)
            evidence.check('Chebyshev_product_algebra',max(abs(product-direct))<Decimal('1e-70'))
            progress('restore-sourced-third-grid')
            restored = restore(evidence,args.branch,'third',deadline)
            evaluator,read,report = [restored[key] for key in ['evaluator','read','report']]
            live = next(row for row in report('annular-live-support-acceleration-attempt01')['cases']
                if row['branch']==args.branch and row['level']=='third')
            direction = read(live['direction_path'])
            correction = read(live['paths']['projection'])['correction']
            progress('construct-compensated-coefficients')
            parent_fields = restored['setup']['loads'].coordinates[:,:-1].T
            evidence.check('parent_common_nodal_shape',parent_fields.shape==(len(evaluator.action.mesh['nodes']),len(evaluator.action.source)))
            polynomial = CompensatedPolynomial(evaluator,direction,correction,parent_fields)
            cells = np.linspace(0,len(evaluator.widths)-1,96).astype(int)
            labels = np.tile([-.47,-.33,-.11,.03,.17,.29,.37,.47],12)
            local = np.tile([.13,.47,.83],32)
            lower = evaluator.geometry.geometry(evaluator.edges[cells],labels)[0]
            upper = evaluator.geometry.geometry(evaluator.edges[cells+1],labels)[0]
            offsets = lower+(upper-lower)*local
            packet,active = evaluator.packet(labels,offsets)
            cells = polynomial.cells(evaluator,labels,offsets)
            evidence.check('all_actual_points_active',active.all())
            acceleration,movement = directions(packet,'C2')
            values = evaluator.metric.evaluate(offsets,evaluator.metric.cells(offsets))[0]
            geometry = channel_geometry(packet,evaluator.anchor+offsets,values)
            old = acceleration-movement*geometry[3]
            diagnostics = {}
            for variant in polynomial.coefficients:
                oracle = polynomial.oracle(variant,cells,labels,packet['local'])
                evidence.check(variant+':exact_identity',oracle['exact_relative']<1e-55,oracle['exact_relative'])
                evidence.check(variant+':binary_arithmetic_budget',oracle['within_arithmetic_budget'],
                    dict(relative=oracle['binary_relative'],maximum_budget_ratio=float(np.max(oracle['arithmetic_error']/oracle['arithmetic_budget']))))
                evidence.check(variant+':finite_nonzero',np.isfinite(oracle['binary']).all() and np.any(oracle['binary']!=0))
                old_difference = old-oracle['direct']
                source = polynomial.exact[variant]
                path = save(variant+'-probe',**{key:value for key,value in oracle.items() if isinstance(value,np.ndarray)},
                    old=old,old_difference=old_difference,labels=labels,offsets=offsets,cells=cells,local=packet['local'])
                diagnostics[variant] = dict(identity_relative=oracle['exact_relative'],binary_relative=oracle['binary_relative'],
                    maximum_old_difference=float(np.max(abs(old_difference))),path=path)
                save(variant+'-coefficients',numerator=polynomial.coefficients[variant],denominator=polynomial.denominator,
                    exact_numerator=source['numerator'].astype(str),exact_denominator=polynomial.exact_denominator.astype(str),
                    degree=polynomial.degree,widths=polynomial.widths)
            difference = polynomial.evaluate('parent_nodal',cells,labels,packet['local'])-polynomial.evaluate('rounded_coefficients',cells,labels,packet['local'])
            evidence.report.update(point_diagnostics=diagnostics,parent_rounding_maximum=float(np.max(abs(difference))),
                cells=len(polynomial.widths),layer_degree=polynomial.degree,actual_points=len(cells),
                polynomial_constructed=True,integrated_ablation_complete=False,seconds=perf_counter()-started)
            evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
