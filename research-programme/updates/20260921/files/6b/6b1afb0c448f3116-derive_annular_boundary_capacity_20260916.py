from derive_annular_source_gravity_20260914 import EvidenceRun
import json
import numpy as np
import sympy as sp


def capacity(first_fraction,splits=1,degree=2):
    tail = np.sqrt(2)/12 if degree == 2 else np.sqrt(3)/6
    length = first_fraction/splits
    diagonal,off = (length/8,length/24) if degree == 2 else (length/3,length/6)
    for index in range(splits):
        tail = diagonal-off**2/(diagonal+tail)
    return tail


def main():
    evidence = EvidenceRun('annular-boundary-capacity-attempt01',__file__)
    try:
        coordinate = sp.symbols('s',real=True)
        basis = sp.Matrix([(1-coordinate)*(1-2*coordinate),4*coordinate*(1-coordinate),coordinate*(2*coordinate-1)])
        mass = sp.integrate(basis*basis.T,(coordinate,0,1))
        condensed = mass.extract([0,2],[0,2])-mass.extract([0,2],[1])*mass.extract([1],[0,2])/mass[1,1]
        evidence.check('exact_quadratic_midpoint_condensation',condensed == sp.Matrix([[3,-1],[-1,3]])/24)
        tail = sp.sqrt(2)/12
        evidence.check('positive_half_line_capacity_fixed_point',sp.simplify(sp.Rational(1,8)-sp.Rational(1,24)**2/(sp.Rational(1,8)+tail)-tail)==0)
        decay = 3-2*sp.sqrt(2)
        evidence.check('decaying_vertex_boundary_kernel',sp.simplify(decay**2-6*decay+1)==0 and 0 < float(decay) < 1)
        path = evidence.root/'source-intake/navier-stokes/20260914/annular-boundary-inertia-attempt01/status.json'
        previous = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('kinetic_complement_identity_qualified',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        for row in previous['cases']:
            count,degree = row['count'],row['degree']
            vertices = np.linspace(5.2,6.8,count)
            cell = np.searchsorted(vertices,6.03)-1
            spacing = vertices[1]-vertices[0]
            fraction = (6.03-vertices[cell])/spacing
            leading_capacity = capacity(fraction,degree=degree)+capacity(1-fraction,degree=degree)
            predicted_mass = 6.03**2*.01**2*spacing*leading_capacity
            predicted_force = -2/6.03*predicted_mass*row['material_inertia']/(row['material_inertia']+predicted_mass)
            evidence.report['cases'].append(dict(degree=degree,count=count,branch=row['branch'],source_fraction=float(fraction),
                measured_added_mass=row['added_mass'],leading_added_mass=float(predicted_mass),
                predicted_initial_force=float(predicted_force),measured_initial_force=row['mechanical_force'],
                force_relative_error=float(abs(predicted_force-row['mechanical_force'])/abs(row['mechanical_force']))))
        decisions = []
        for count in [257,513]:
            vertices = np.linspace(5.2,6.8,count)
            cell = np.searchsorted(vertices,6.03)-1
            spacing = vertices[1]-vertices[0]
            fraction = (6.03-vertices[cell])/spacing
            for splits in [1,2,4,8,16]:
                predicted_mass = 6.03**2*.01**2*spacing*(capacity(fraction,splits)+capacity(1-fraction,splits))
                predicted_force = 2*predicted_mass/6.03
                if predicted_force < 1.5e-7:
                    decisions.append(dict(count=count,source_splits=splits,predicted_absolute_initial_force=float(predicted_force)))
                    break
        evidence.report.update(local_refinement_decisions=decisions,selection_rule='First dyadic source subdivision with leading initial-force estimate below 1.5e-7; numerical design budget, not a new physics coefficient or acceptance threshold.',
            scope='Analytic frozen-weight boundary-capacity law and derived numerical refinement choices; not an exact varying-weight or evolved-force bound.',
            half_line_capacity=str(tail),decay=str(decay),frozen_weight_leading_law_not_exact=True,
            live_quadratic_geometry_qualified=False,uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
