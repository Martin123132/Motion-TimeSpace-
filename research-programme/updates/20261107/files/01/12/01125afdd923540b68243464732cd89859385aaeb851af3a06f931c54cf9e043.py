from stage167_common import *
from fractions import Fraction


def resolution_pair_exact(fine,coarse):
    arrays={}
    maximum_rounding=Fraction(0)
    epsilon=Fraction.from_float(float(np.finfo(float).eps))
    for key in ['potential','energy']:
        corrected,defects=[],[]
        for fine_row,coarse_row in zip(np.atleast_2d(fine[key]),np.atleast_2d(coarse[key])):
            corrected_row,defect_row=[],[]
            for join in range(2):
                baseline_fine=Fraction.from_float(float(fine_row[0]))
                baseline_coarse=Fraction.from_float(float(coarse_row[0]))
                mts_fine=Fraction.from_float(float(fine_row[3+join]))
                mts_coarse=Fraction.from_float(float(coarse_row[3+join]))
                total_fine=Fraction.from_float(float(fine_row[7+join]))
                total_coarse=Fraction.from_float(float(coarse_row[7+join]))
                fine_rounding=total_fine-baseline_fine-mts_fine
                coarse_rounding=total_coarse-baseline_coarse-mts_coarse
                direct=baseline_fine-baseline_coarse+mts_fine-mts_coarse
                defect=fine_rounding-coarse_rounding
                assert total_fine-total_coarse-direct-defect==0
                for rounding,baseline,mts in [(fine_rounding,baseline_fine,mts_fine),(coarse_rounding,baseline_coarse,mts_coarse)]:
                    scale=epsilon*(abs(baseline)+abs(mts))
                    if scale:
                        maximum_rounding=max(maximum_rounding,abs(rounding)/scale)
                    else:
                        assert rounding==0
                corrected_row.append(float(direct))
                defect_row.append(float(defect))
            corrected.append(corrected_row)
            defects.append(defect_row)
        arrays[key]=np.array(corrected) if key=='potential' else np.array(corrected)[0]
        arrays[key+'_rounding']=np.array(defects) if key=='potential' else np.array(defects)[0]
    return arrays,float(maximum_rounding)
