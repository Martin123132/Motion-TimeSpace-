from common import *
from source_adapter import dense_values
from extend import make_rhs
from thermal_candidate import Thermal
from phase_math import symbolic
import numpy as np
import sympy as sp
import ast
import csv


def independent_algebra():
    position,velocity,omega,hubble=sp.symbols('x v omega H',real=True,nonzero=True)
    position_rate=position+omega*velocity/hubble
    velocity_rate=-2*velocity-omega*position/hubble
    energy=(position**2+velocity**2)/2
    energy_rate=sp.expand(sp.diff(energy,position)*position_rate+sp.diff(energy,velocity)*velocity_rate)
    second=sp.expand(sp.diff(energy_rate,position)*position_rate+sp.diff(energy_rate,velocity)*velocity_rate)
    polar=(-position*velocity_rate+velocity*position_rate)/(position**2+velocity**2)
    checks=dict(canonical_energy=sp.simplify(energy_rate-(position**2-2*velocity**2)),
                canonical_second=sp.simplify(second-(2*position**2+8*velocity**2+6*omega*position*velocity/hubble)),
                polar_angle=sp.simplify(polar-(omega/hubble+3*position*velocity/(position**2+velocity**2))))
    for sign in (-1,1):
        checks['orthogonal_product_'+str(sign)]=sp.expand((position**2+velocity**2)/2-sign*position*velocity-(position-sign*velocity)**2/2)
    require(all(value==0 for value in checks.values()),'independent canonical/comparison algebra')
    return {name:str(value) for name,value in checks.items()}


def comparison_samples():
    generator=np.random.default_rng(24420261107)
    rows=[]
    rotation=np.array([[0.,1.],[-1.,0.]])
    damping=np.diag([1.,-2.])
    for index in range(512):
        external,heavy,omega=np.exp(generator.uniform(-3,3,3))
        logarithmic_width=float(np.exp(generator.uniform(-12,-1)))
        mean=generator.normal(size=2)*np.exp(generator.uniform(-3,3))
        error=generator.normal(size=2)*np.exp(generator.uniform(-12,1))
        radius=np.linalg.norm(error)
        amplitude=np.linalg.norm(mean)
        true_heavy=heavy*np.exp(generator.uniform(-logarithmic_width,logarithmic_width))
        mean_hubble=np.sqrt((external+heavy+np.dot(mean,mean)/2)/3)
        true_hubble=np.sqrt((external+true_heavy+np.dot(mean+error,mean+error)/2)/3)
        lower=np.sqrt((external+heavy*np.exp(-logarithmic_width)+max(amplitude-radius,0)**2/2)/3)
        difference_rate=damping@error+omega/true_hubble*rotation@error+omega*(1/true_hubble-1/mean_hubble)*rotation@mean
        actual=float(np.dot(error,difference_rate)/radius)
        density_error=heavy*np.expm1(logarithmic_width)
        coefficient=omega/(3*lower*mean_hubble*(lower+mean_hubble))
        bound=radius+coefficient*(amplitude*density_error+.5*amplitude**2*radius+.5*amplitude*radius**2)
        excess=(actual-bound)/max(abs(actual),bound,1e-100)
        require(excess<=ALGEBRA and lower<=true_hubble*(1+ALGEBRA),'independent comparison inequality')
        rows.append(dict(index=index,relative_excess=float(excess)))
    return dict(cases=len(rows),max_relative_excess=max(item['relative_excess'] for item in rows),scope='dimensionless inequality checks, not invented physical histories')


def main():
    modest()
    check_parent()
    destination=ROOT/'summary'
    destination.mkdir(exist_ok=False)
    for script in ROOT.glob('*.py'):
        compile(script.read_text(),str(script),'exec')
        ast.parse(script.read_text())
    require(read(ROOT/'inventory-01.end.json')['exit_code']==1,'original failure retained')
    require(not (ROOT/'inventory/result.json').exists(),'failed inventory not relabelled')
    for phase in ('diagnose-01','thermal-01','extension-01'):
        require(read(ROOT/(phase+'.end.json'))['exit_code']==0,'completed candidate phase '+phase)
    extension=read(ROOT/'extension/result.json')
    freeze=read(ROOT/'extension/freeze.json')
    qualification=read(ROOT/'thermal-qualification/result.json')
    require(extension['handoff_eligible'] and qualification['passed'],'candidate qualification')
    for source_manifest in (freeze['sources'],qualification['source_hashes']):
        for path,expected in source_manifest.items():
            require(digest(path)==expected,'changed numerical candidate source '+path)
    for path,expected in read(ROOT/'thermal-qualification/protocol.json')['source_files'].items():
        require(digest(path)==expected,'changed defining thermal source')
    symbolic_checks=dict(phase=symbolic(),independent=independent_algebra())
    inequality=comparison_samples()
    dense_reports=[]
    endpoint_rows=[]
    reports=[]
    for model in ('heavy','cold'):
        configuration=freeze['configurations'][model]
        require(digest(configuration['accepted_path'])==configuration['accepted_sha256'],'retained initial input')
        parameters=configuration['thermal_parameters']
        require(all(parameters[name]>0 for name in ('cdm','baryon','photon','massless')),'positive standard species')
        require(all(value>0 for value in parameters['masses']+parameters['coefficients']),'positive thermal components')
        thermal=Thermal(parameters)
        rhs=make_rhs(configuration,thermal)
        for label in ('base','fine','independent'):
            packet=load(ROOT/'extension'/model/(label+'-dense.npz'))
            indices=np.unique(np.linspace(0,len(packet['segment_start'])-1,97,dtype=int))
            points=packet['segment_start'][indices]+.3819660112501051*(packet['segment_end'][indices]-packet['segment_start'][indices])
            states,derivatives=dense_values(packet,points)
            predicted=np.asarray([rhs(float(point),state) for point,state in zip(points,states)])
            scales=np.maximum(np.max(abs(predicted),axis=0),1e-15)
            discrepancy=float(np.max(abs(derivatives-predicted)/scales[None,:]))
            require(discrepancy<GATE,'dense output derivative check '+model+' '+label)
            dense_reports.append(dict(model=model,label=label,off_node_points=len(points),normalized_derivative_error=discrepancy))
        packet=load(ROOT/'extension'/model/'fine.npz')
        for endpoint in ('scale_start','scale_end'):
            scale=freeze['target'][endpoint]
            index=int(np.argmin(abs(packet['a']-scale)))
            require(abs(packet['a'][index]/scale-1)<ALGEBRA,'frozen endpoint exists')
            speed_record=next(item for item in freeze['target']['models'] if item['model']==model)
            speeds=1/np.sqrt(1+(scale/np.asarray(speed_record['momentum_mass_ratio']))**2)
            require(float(speeds.max())<=.1+ALGEBRA,'five-node cold target')
            endpoint_rows.append(dict(model=model,endpoint=endpoint,a=float(packet['a'][index]),redshift=float(1/packet['a'][index]-1),
                                      conformal_hubble_Mpc_inv=float(packet['hubble'][index]),hubble_uncertainty=float(packet['hubble_error'][index]),
                                      conformal_clock_Mpc=float(packet['clock'][index]),clock_uncertainty=float(packet['clock_error'][index]),
                                      slow_coordinate_0=float(packet['slow_coordinates'][index,0]),slow_coordinate_1=float(packet['slow_coordinates'][index,1]),
                                      heavy_mean_density=float(packet['heavy_mean'][index]),heavy_log_density_width=float(packet['heavy_log_width'][index]),
                                      maximum_saved_node_speed=float(speeds.max())))
        report=read(ROOT/'extension'/model/'result.json')
        maximum_numerical=max(item['error'] for item in report['comparisons'])
        maximum_uncertainty=max(report['cold_relative_uncertainty'].values())
        require(maximum_numerical<GATE and maximum_uncertainty<GATE,'unchanged final gates')
        reports.append(dict(model=model,max_refinement_discrepancy=maximum_numerical,cold_uncertainty=report['cold_relative_uncertainty'],
                            replay=report['replay']))
    with (destination/'cold-endpoints.csv').open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(endpoint_rows[0]))
        writer.writeheader()
        writer.writerows(endpoint_rows)
    with (destination/'cold-endpoints.csv').open(newline='',encoding='utf-8') as stream:
        require(len(list(csv.DictReader(stream)))==4,'CSV round trip')
    check_parent()
    report=dict(state='validated_background_candidate',reports=reports,symbolic_checks=symbolic_checks,
                comparison_inequality=inequality,dense_output_checks=dense_reports,original_inventory_pass=False,
                parent_and_original_bank_unchanged=True,physical_ode_solves=8,new_cosmology_fits=0,
                exact_late_heavy_phase_available=False,formal_interval_arithmetic_certificate=False,
                next_target='Derive action-owned late perturbation micromotion/averaged transfer with an error bound before the frozen cold GR/Poisson physical benchmark.',
                source_hashes=frozen_sources())
    write(destination/'result.json',report)
    print(json.dumps(dict(state=report['state'],reports=reports,max_dense_error=max(item['normalized_derivative_error'] for item in dense_reports)),indent=2),flush=True)


if __name__=='__main__':
    main()
