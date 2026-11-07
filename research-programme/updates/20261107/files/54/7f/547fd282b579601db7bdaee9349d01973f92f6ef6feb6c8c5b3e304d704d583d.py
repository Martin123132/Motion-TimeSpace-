from __future__ import annotations

import sympy as symbolic
from vertex_common import *


def main():
    modest()
    folder=ROOT/'results/local-gravity'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def identity(name,expression):
        entries=list(expression) if isinstance(expression,symbolic.MatrixBase) else [expression]
        residual=[symbolic.simplify(entry) for entry in entries]
        passed=all(entry==0 for entry in residual)
        checks.append(dict(name=name,passed=passed,components=len(entries)))
        assert passed,(name,residual)

    rational=symbolic.Rational
    minkowski=symbolic.diag(-1,1,1,1)
    def einstein(metric,momentum):
        raised=minkowski*momentum
        norm=(momentum.T*raised)[0]
        trace=symbolic.trace(minkowski*metric)
        contraction=metric*raised
        ricci=(-momentum*contraction.T-contraction*momentum.T+norm*metric+trace*momentum*momentum.T)/2
        return ricci-minkowski*symbolic.trace(minkowski*ricci)/2

    modes=[('massive_sum',1,[-1,0,0,0],[-rational(5,4),rational(3,4),0,0]),
        ('massive_nonparallel',1,[-rational(5,4),rational(3,4),0,0],[-rational(5,4),0,rational(3,4),0]),
        ('massive_static_beat',1,[-rational(5,4),rational(3,4),0,0],[rational(5,4),rational(3,4),0,0]),
        ('null_nonparallel',0,[-1,1,0,0],[-1,0,1,0])]
    rows=[]
    for label,mass,first,second in modes:
        momentum_p=symbolic.Matrix(first)
        momentum_q=symbolic.Matrix(second)
        momentum=momentum_p+momentum_q
        norm=(momentum.T*minkowski*momentum)[0]
        dot=(momentum_p.T*minkowski*momentum_q)[0]
        source=-(momentum_p*momentum_q.T+momentum_q*momentum_p.T)/2+minkowski*(dot-mass**2)/2
        identity(label+': both modes are on shell',symbolic.Matrix([
            (momentum_p.T*minkowski*momentum_p)[0]+mass**2,
            (momentum_q.T*minkowski*momentum_q)[0]+mass**2]))
        identity(label+': source conserved',source*minkowski*momentum)
        assert norm!=0
        reverse=2*source/norm
        metric=reverse-minkowski*symbolic.trace(minkowski*reverse)/2
        identity(label+': Lorenz constraint',reverse*minkowski*momentum)
        identity(label+': full linear Einstein response',einstein(metric,momentum)-source)
        rows.append(dict(mode=label,total_minkowski_norm=str(norm),source=[[str(entry) for entry in source.row(index)] for index in range(4)]))

    amplitude,mass,wavenumber,phase,cycle=symbolic.symbols('A m k x theta',positive=True,real=True)
    frequency2=mass**2+wavenumber**2
    phi=amplitude*symbolic.cos(wavenumber*phase)*symbolic.cos(cycle)
    kinetic=amplitude**2*frequency2*symbolic.cos(wavenumber*phase)**2*symbolic.sin(cycle)**2
    gradient=symbolic.diff(phi,phase)**2
    potential=mass**2*phi**2
    density=symbolic.integrate((kinetic+gradient+potential)/2,(cycle,0,2*symbolic.pi))/(2*symbolic.pi)
    pressure_x=symbolic.integrate((kinetic+gradient-potential)/2,(cycle,0,2*symbolic.pi))/(2*symbolic.pi)
    pressure_y=symbolic.integrate((kinetic-gradient-potential)/2,(cycle,0,2*symbolic.pi))/(2*symbolic.pi)
    identity('Cycle-averaged standing-wave density',symbolic.trigsimp(density-amplitude**2*(mass**2+wavenumber**2+mass**2*symbolic.cos(2*wavenumber*phase))/4))
    identity('Cycle-averaged longitudinal pressure',pressure_x-amplitude**2*wavenumber**2/4)
    identity('Cycle-averaged transverse pressure',symbolic.trigsimp(pressure_y-amplitude**2*wavenumber**2*symbolic.cos(2*wavenumber*phase)/4))
    total_k=2*wavenumber
    density_mode=amplitude**2*mass**2/4
    transverse_mode=amplitude**2*wavenumber**2/4
    potential_phi=-(density_mode+2*transverse_mode)/(2*total_k**2)
    potential_psi=-density_mode/(2*total_k**2)
    metric=symbolic.diag(-2*potential_phi,-2*potential_psi,-2*potential_psi,-2*potential_psi)
    source=symbolic.diag(density_mode,0,transverse_mode,transverse_mode)
    identity('Standing-wave Newtonian-gauge Einstein equations',einstein(metric,symbolic.Matrix([0,total_k,0,0]))-source)
    identity('Finite-gradient gravitational slip is fixed',potential_phi/potential_psi-1-2*wavenumber**2/mass**2)
    newton_g,physical_density=symbolic.symbols('G rho_physical',positive=True)
    identity('Restored Poisson normalization uses inherited G',(-total_k**2*potential_psi).subs(amplitude**2*mass**2,32*symbolic.pi*newton_g*physical_density)-4*symbolic.pi*newton_g*physical_density)

    retarded,advanced,transverse_x,transverse_y=symbolic.symbols('u v X Y',real=True)
    coordinates=[retarded,advanced,transverse_x,transverse_y]
    profile=symbolic.Function('F')(retarded)
    rate=symbolic.diff(profile,retarded)
    wave=-rate**2*(transverse_x**2+transverse_y**2)/2
    geometry=symbolic.Matrix([[wave,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
    inverse=geometry.inv()
    connection=[[[symbolic.simplify(sum(inverse[upper,lower]*(symbolic.diff(geometry[lower,right],coordinates[left])+symbolic.diff(geometry[lower,left],coordinates[right])-symbolic.diff(geometry[left,right],coordinates[lower])) for lower in range(4))/2) for right in range(4)] for left in range(4)] for upper in range(4)]
    ricci=symbolic.zeros(4)
    for left in range(4):
        for right in range(4):
            ricci[left,right]=symbolic.simplify(sum(symbolic.diff(connection[upper][left][right],coordinates[upper])-symbolic.diff(connection[upper][left][upper],coordinates[right])+sum(connection[upper][upper][middle]*connection[middle][left][right]-connection[upper][right][middle]*connection[middle][left][upper] for middle in range(4)) for upper in range(4)))
    field_gradient=symbolic.Matrix([rate,0,0,0])
    field_norm=(field_gradient.T*inverse*field_gradient)[0]
    scalar_stress=field_gradient*field_gradient.T-geometry*field_norm/2
    scalar_ricci=symbolic.trace(inverse*ricci)
    identity('Exact null metric determinant',geometry.det()+1)
    identity('Exact null scalar solves covariant KG',sum(symbolic.diff((inverse*field_gradient)[index],coordinates[index]) for index in range(4)))
    identity('Exact null scalar Einstein equations',ricci-geometry*scalar_ricci/2-scalar_stress)
    identity('Exact plane-wave scalar curvature is zero',scalar_ricci)
    maxwell=symbolic.zeros(4)
    maxwell[0,2]=rate
    maxwell[2,0]=-rate
    maxwell_raised=inverse*maxwell*inverse
    maxwell_norm=sum(maxwell[left,right]*maxwell_raised[left,right] for left in range(4) for right in range(4))
    maxwell_stress=maxwell*inverse*maxwell.T-geometry*maxwell_norm/4
    identity('Null Maxwell invariant',maxwell_norm)
    identity('Source-free Maxwell divergence',symbolic.Matrix([sum(symbolic.diff(maxwell_raised[left,right],coordinates[left]) for left in range(4)) for right in range(4)]))
    identity('Maxwell Bianchi identity',symbolic.Matrix([symbolic.diff(maxwell[middle,right],coordinates[left])+symbolic.diff(maxwell[right,left],coordinates[middle])+symbolic.diff(maxwell[left,middle],coordinates[right]) for left in range(4) for middle in range(left+1,4) for right in range(middle+1,4)]))
    identity('Scalar and Maxwell null energy-flux tensors match',maxwell_stress-scalar_stress)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,nonresonant_modes=rows,
        excluded_fourier_channels=['K=0 homogeneous background','K^2=0 copropagating null channel'],
        null_channel_treated_by_exact_plane_wave=True,newton_G_inherited_not_derived=True,
        standing_wave_slip='Phi/Psi=1+2*(k/m)^2',plane_wave_local_not_finite_energy=True,
        scalar_maxwell_stress_degeneracy_not_charge_derivation=True),__file__)
    print(json.dumps(dict(exact_checks=len(checks),newton_slip='1+2*(k/m)^2',null_wave='exact')),flush=True)


if __name__=='__main__':
    main()
