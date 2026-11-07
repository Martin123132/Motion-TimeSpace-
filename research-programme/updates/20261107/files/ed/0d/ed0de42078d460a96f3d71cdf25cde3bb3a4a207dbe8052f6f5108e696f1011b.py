from stage167_common import *


def resolution_pair(fine,coarse):
    arrays={}
    maximum_identity=Decimal(0)
    maximum_rounding=Decimal(0)
    with localcontext() as context:
        context.prec=60
        epsilon=Decimal.from_float(float(np.finfo(float).eps))
        for key in ['potential','energy']:
            fine_rows=np.atleast_2d(fine[key])
            coarse_rows=np.atleast_2d(coarse[key])
            corrected,defects=[],[]
            for fine_row,coarse_row in zip(fine_rows,coarse_rows):
                corrected_row,defect_row=[],[]
                for join in range(2):
                    baseline_fine=Decimal.from_float(float(fine_row[0]))
                    baseline_coarse=Decimal.from_float(float(coarse_row[0]))
                    mts_fine=Decimal.from_float(float(fine_row[3+join]))
                    mts_coarse=Decimal.from_float(float(coarse_row[3+join]))
                    total_fine=Decimal.from_float(float(fine_row[7+join]))
                    total_coarse=Decimal.from_float(float(coarse_row[7+join]))
                    fine_rounding=total_fine-baseline_fine-mts_fine
                    coarse_rounding=total_coarse-baseline_coarse-mts_coarse
                    direct=baseline_fine-baseline_coarse+mts_fine-mts_coarse
                    defect=fine_rounding-coarse_rounding
                    raw=total_fine-total_coarse
                    maximum_identity=max(maximum_identity,abs(raw-direct-defect)/max(abs(raw),Decimal('1e-300')))
                    for rounding,baseline,mts in [(fine_rounding,baseline_fine,mts_fine),(coarse_rounding,baseline_coarse,mts_coarse)]:
                        maximum_rounding=max(maximum_rounding,abs(rounding)/max(epsilon*(abs(baseline)+abs(mts)),Decimal('1e-300')))
                    corrected_row.append(float(direct))
                    defect_row.append(float(defect))
                corrected.append(corrected_row)
                defects.append(defect_row)
            arrays[key]=np.array(corrected) if key=='potential' else np.array(corrected)[0]
            arrays[key+'_rounding']=np.array(defects) if key=='potential' else np.array(defects)[0]
    return arrays,float(maximum_identity),float(maximum_rounding)
