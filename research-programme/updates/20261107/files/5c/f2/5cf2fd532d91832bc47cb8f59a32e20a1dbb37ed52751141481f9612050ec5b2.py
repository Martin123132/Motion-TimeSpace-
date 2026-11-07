from __future__ import annotations

from streaming_common import *


def main():
    modest()
    folder=ROOT/'results/pair-streaming'
    folder.mkdir(parents=True,exist_ok=False)
    fits=json.loads((PARENT/'results/velocity-fits/status.json').read_text())
    branches=[]
    for label in ['heavy','cold','lcdm']:
        central=correlations(label)
        variants={name:correlations(label,**options) for name,options in [
            ('refined',dict(nodes=65537)),('coarse',dict(nodes=16385)),
            ('pchip',dict(method='pchip')),('cut_q3',dict(upper=3.))]}
        comparison={}
        for name,variant in variants.items():
            comparison[name]={key:max(abs(base[key]-other[key]) for base,other in zip(central['rows'],variant['rows'])
                if 10<=base['separation_Mpc_over_h']<=200)
                for key in ['xi_cb','cross_Mpc_over_h','pair_variance_Mpc_over_h_squared']}
        biases=[('cb_density',1.)]+[(cap,next(row['fit']['bias'] for row in fits['rows']
            if row['branch']==label and row['family']=='gaussian' and row['cap']==cap and row['kmax']==.1 and row['ells']==[0,2])) for cap in ['NGC','SGC']]
        weighted=[]
        conversion=survey.geometry(label)['model_H_km_s_Mpc']/(1+survey.REDSHIFT)/HUNIT
        for sample,bias in biases:
            for row in central['rows']:
                correlation=bias*bias*row['xi_cb'];cross=bias*row['cross_Mpc_over_h'];variance=row['pair_variance_Mpc_over_h_squared']
                moments=weighted_moments(correlation,cross,variance)
                covariance=np.array([[bias*bias*central['variance_density'],correlation,cross],
                    [correlation,bias*bias*central['variance_density'],cross],[cross,cross,variance]])
                weighted.append(dict(sample=sample,bias=bias,separation_Mpc_over_h=row['separation_Mpc_over_h'],LOS_cosine=row['LOS_cosine'],
                    xi_tracer=correlation,cross_Mpc_over_h=cross,unweighted_pair_variance=variance,
                    **moments,mean_velocity_km_s=conversion*moments['mean'],
                    covariance_min_eigenvalue=float(min(linalg.eigvalsh(covariance))),
                    one_point_negative_density_probability=float(special.ndtr(-1/(bias*math.sqrt(central['variance_density'])))),
                    positivity=positivity(correlation,cross,variance)))
        branch=dict(branch=label,central=central,variants=variants,primary_numerical_differences=comparison,
            weighted=weighted,biases=dict(biases),velocity_conversion=conversion,
            new_parameters_fitted=0,nonlinear_parent_distribution_derived=False)
        branches.append(branch)
        write_json(folder/(label+'.json'),branch)
        primary=[row for row in weighted if row['LOS_cosine']==1 and row['sample']=='cb_density' and row['separation_Mpc_over_h'] in [10,30,50,100,150,200]]
        print(label,json.dumps(primary),flush=True)
    finish(folder,dict(branches=branches,actual_survey_refit=False,
        scope='Pair weighting of the retained Gaussian linear fields. Signed-density obstruction is tested rather than clipped.'),
        __file__,[PARENT/'results/velocity-fits/status.json',PARENT/'results/derived-moments/status.json',
            *[SPECTRUM/'results/spectrum'/(label+'.npz') for label in ['heavy','cold','lcdm']],*folder.glob('*.json')])


if __name__=='__main__':
    main()
