from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_live_P2_current_20260918 import LayerCurrent, P2Material
from annular_cut_initial_data_20260915 import compatible_initial_state
from derive_annular_P2_broken_traction_identity_20260918 import broken_traction
import numpy as np


class AnalyticMetric:
    def __init__(self, time):
        self.time = time
        self.edges = np.linspace(5.18,6.82,13)

    def metric(self, radius):
        radius = np.asarray(radius)
        root = np.sqrt(1-2*(.7+.001*self.time)/radius)
        lapse = root*np.exp(.004*self.time*(radius-6))
        return lapse,root


class ManufacturedTangent:
    def __init__(self, count, gram):
        self.system = PrimitiveP2System(count,gram,layer_degree=2,action_order=32)
        values,rates,unused = compatible_initial_state(self.system.model,0.)
        values[-1] += .003
        rates[:-1] += .0003*np.sin(self.system.model.radii*2.3)
        acceleration = np.append(.02*np.cos(self.system.model.radii*1.7),.005)
        self.coordinates = np.tile(values,(len(self.system.labels),1))
        self.coordinates[:,-1] += self.system.width*self.system.labels
        self.rates = np.tile(rates,(len(self.system.labels),1))
        self.acceleration = acceleration
        self.geometry = AnalyticMetric(0.)

    def layer_data(self,label):
        interpolation = P2Material(self.system,self.coordinates).interpolation([label])[0]
        return LayerCurrent(self.system.layer(label,self.geometry),
            self.system.layer(label,AnalyticMetric(1j*1e-24)),
            interpolation@self.coordinates,interpolation@self.rates,self.acceleration)


def main():
    evidence = EvidenceRun('annular-P2-broken-traction-offshell-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_forward_evolution=True,
            manufactured_metric_not_a_solution_of_matter_constraints=True,
            arbitrary_acceleration_not_using_equations_of_motion=True,
            temporal_metric_derivative_is_analytic=True,
            full_live_P2_force_convergence_proven=False)
        for count in [17,33]:
            for gram in [False,True]:
                tangent = ManufacturedTangent(count,gram)
                current = tangent.layer_data(0.)
                row = broken_traction(tangent)
                row.update(branch='MTS' if gram else 'reference',base_count=count)
                raw = current.layer.source_covector(0.,current.coordinates,current.rates,wave=True)
                row['wrong_raw_wave_covector_error'] = abs(raw-row['trace_pressure']-row['derived_defect'])
                row['omitted_edge_error'] = abs(row['actual_defect']-row['derived_defect']+row['internal_moving_edge_work'])
                row['omitted_Gram_error'] = abs(row['actual_defect']-row['derived_defect']+row['explicit_Gram_shape_force'])
                evidence.report['cases'].append(row)
                evidence.save()
                key=row['branch']+str(count)
                evidence.check(key+'_offshell_identity',row['identity_error']<2e-10,row)
                evidence.check(key+'_raw_covector_negative_control',row['wrong_raw_wave_covector_error']>1e-8)
                evidence.check(key+'_moving_internal_edge_negative_control',row['omitted_edge_error']>1e-8)
                if gram:
                    evidence.check(key+'_Gram_shape_negative_control',row['omitted_Gram_error']>1e-9)
                print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
