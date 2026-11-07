from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy import linalg, sparse
from scipy.sparse.linalg import splu
from scipy.special import eval_jacobi

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'interior-storage-20261006'
sys.path.insert(0, str(BRANCH/'radial-gravity-stability-20261003'))
from test_radial_energy import Profile


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)


def dependencies(profile=None):
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.add(PARENT/'results/stage-integrity.json')
    if profile is not None:
        paths.add(profile.path)
        paths.add(BRANCH/'self-gravity-20261003/results/fine/status.json')
    return {str(path): digest(path) for path in sorted(paths)}


def save(name, script, report, arrays=None):
    directory = ROOT/'results'/name
    directory.mkdir(parents=True, exist_ok=False)
    outputs = {}
    if arrays is not None:
        np.savez_compressed(directory/'forms.npz', **arrays)
        outputs['forms.npz'] = digest(directory/'forms.npz')
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), output_hashes=outputs, **report)
    write_json(directory/'status.json', report)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


class Background:
    def __init__(self, nominal=.03):
        self.profile = Profile(20., nominal)
        self.alpha = self.profile.alpha
        self.radius = self.profile.radius
        self.mass = self.alpha*self.profile.mass
        self.frequency = self.profile.frequency

    def values(self, position):
        field, gradient, energy, force, second = [np.zeros_like(position) for _ in range(5)]
        metric = 1-2*self.mass/position
        lapse = np.sqrt(np.maximum(metric, 1e-100))
        interior = position < self.radius
        field[interior], gradient[interior], _, metric[interior], xi, _ = self.profile.values(position[interior])
        lapse[interior] = xi*np.sqrt(metric[interior])
        energy[interior] = 3*field[interior]**(4/3)/8+field[interior]**4/8
        force[interior] = field[interior]**(1/3)/2+field[interior]**3/2
        second[interior] = field[interior]**(-2/3)/6+1.5*field[interior]**2
        rotation2 = self.frequency**2/lapse**2
        pressure = (metric*gradient**2+rotation2*field**2)/2-energy
        metric_prime = (1-metric)/position-self.alpha*position*(metric*gradient**2+rotation2*field**2+2*energy)
        log_lapse_prime = ((1-metric)/2+self.alpha*position**2*pressure)/(position*metric)
        gradient_prime = (force-rotation2*field)/metric-(2/position+log_lapse_prime+metric_prime/(2*metric))*gradient
        return dict(field=field, gradient=gradient, second_gradient=gradient_prime, metric=metric,
                    lapse=lapse, energy=energy, force=force, second=second, rotation2=rotation2,
                    metric_prime=metric_prime, log_lapse_prime=log_lapse_prime)


def quadrature(edges, order=8):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    width = np.diff(edges)
    positions = ((edges[1:]+edges[:-1])[:, None]/2+width[:, None]*nodes/2).ravel()
    factors = (width[:, None]*weights/2).ravel()
    cells = np.repeat(np.arange(len(width)), order)
    shape_left = np.tile((1-nodes)/2, len(width))
    shape_right = 1-shape_left
    return positions, factors, cells, shape_left, shape_right


def basis(position, radius, count, power):
    coordinate = position/radius
    inside = coordinate < 1
    selected = coordinate[inside]
    envelope = selected**power*(1-selected)**power
    first_envelope = power*(selected**(power-1)*(1-selected)**power-selected**power*(1-selected)**(power-1))
    second_envelope = power*(power-1)*(selected**(power-2)*(1-selected)**power+selected**power*(1-selected)**(power-2))-2*power**2*selected**(power-1)*(1-selected)**(power-1)
    values, first, second = [np.zeros((len(position), count)) for _ in range(3)]
    jacobi_left, jacobi_right = 2*power, 2*power+2
    for degree in range(count):
        polynomial = eval_jacobi(degree, jacobi_left, jacobi_right, 2*selected-1)
        derivative = (degree+jacobi_left+jacobi_right+1)*eval_jacobi(degree-1, jacobi_left+1, jacobi_right+1, 2*selected-1) if degree else np.zeros_like(selected)
        curvature = (degree+jacobi_left+jacobi_right+1)*(degree+jacobi_left+jacobi_right+2)*eval_jacobi(degree-2, jacobi_left+2, jacobi_right+2, 2*selected-1) if degree > 1 else np.zeros_like(selected)
        values[inside, degree] = envelope*polynomial
        first[inside, degree] = (first_envelope*polynomial+envelope*derivative)/radius
        second[inside, degree] = (second_envelope*polynomial+2*first_envelope*derivative+envelope*curvature)/radius**2
    return values, first, second


def tail(position, mass, normalization_radius):
    def raw(points):
        discriminant = np.sqrt(points*(points-2*mass))
        isotropic = (points-mass+discriminant)/2
        isotropic_prime = (1+(points-mass)/discriminant)/2
        conformal = 1+mass/(2*isotropic)
        value = isotropic**(-3)/conformal
        logarithm = (-3/isotropic+mass/(2*isotropic**2*conformal))*isotropic_prime
        return value, value*logarithm
    value, derivative = raw(position)
    normalization = raw(np.asarray(normalization_radius))[0]
    return value/normalization, derivative/normalization


def solve_constraint(background, edges, position, weights, cells, shape_left, shape_right, source):
    values = background.values(position)
    metric = values['metric']
    width = np.diff(edges)
    measure = position**2/np.sqrt(metric)
    potential = 6/position**2+2*background.alpha*(values['rotation2']*values['field']**2-values['energy'])
    diagonal = np.zeros(len(edges))
    offdiagonal = np.zeros(len(edges)-1)
    np.add.at(diagonal, cells, weights*(position**2*np.sqrt(metric)/width[cells]**2+measure*potential*shape_left**2))
    np.add.at(diagonal, cells+1, weights*(position**2*np.sqrt(metric)/width[cells]**2+measure*potential*shape_right**2))
    np.add.at(offdiagonal, cells, weights*(-position**2*np.sqrt(metric)/width[cells]**2+measure*potential*shape_left*shape_right))
    logarithm = tail(np.asarray(edges[-1]), background.mass, edges[-1])[1]
    diagonal[-1] -= edges[-1]**2*np.sqrt(1-2*background.mass/edges[-1])*logarithm
    operator = sparse.diags([offdiagonal[1:], diagonal[1:], offdiagonal[1:]], [-1, 0, 1], format='csc')
    right = np.zeros((len(edges), source.shape[1]))
    np.add.at(right, cells, (weights*measure*shape_left)[:, None]*source)
    np.add.at(right, cells+1, (weights*measure*shape_right)[:, None]*source)
    solution = np.vstack([np.zeros(source.shape[1]), splu(operator).solve(right[1:])])
    residual = float(np.linalg.norm(operator@solution[1:]-right[1:])/max(np.linalg.norm(right[1:]), 1e-300))
    metric_scalar = shape_left[:, None]*solution[cells]+shape_right[:, None]*solution[cells+1]
    metric_gradient = (solution[cells+1]-solution[cells])/width[cells, None]
    return metric_scalar, metric_gradient, solution[-1], residual, solution


def hessian_form(matrix, weights, coefficient, left, right=None):
    if right is None:
        matrix += 2*left.T@((weights*coefficient)[:, None]*left)
    else:
        product = left.T@((weights*coefficient)[:, None]*right)
        matrix += product+product.T


def even_form(background, position, weights, radial, angular, angular_prime, amplitude, amplitude_prime, phase_momentum):
    values = background.values(position)
    field, gradient, metric, lapse, energy, force, second, rotation2, log_lapse_prime = [values[key] for key in ['field', 'gradient', 'metric', 'lapse', 'energy', 'force', 'second', 'rotation2', 'log_lapse_prime']]
    measure = lapse*position**2/np.sqrt(metric)
    result = np.zeros((radial.shape[1], radial.shape[1]))
    hessian_form(result, weights, -lapse/(4*background.alpha*np.sqrt(metric))*(-.25+.75*metric+1.5*position*metric*log_lapse_prime), radial)
    hessian_form(result, weights, -lapse/(4*background.alpha*np.sqrt(metric))*(3-metric-2*position*metric*log_lapse_prime), radial, angular)
    hessian_form(result, weights, lapse*np.sqrt(metric)*position/(4*background.alpha)*(1+position*log_lapse_prime), radial, angular_prime)
    hessian_form(result, weights, -lapse*np.sqrt(metric)*position**2/(8*background.alpha), angular_prime)
    hessian_form(result, weights, measure*metric/2, amplitude_prime)
    hessian_form(result, weights, measure*metric*gradient, amplitude_prime, angular-radial/2)
    hessian_form(result, weights, measure*metric*gradient**2*3/16-measure*energy/8, radial)
    hessian_form(result, weights, -measure*metric*gradient**2/4+measure*energy/2, radial, angular)
    hessian_form(result, weights, measure*(3/position**2+second/2+1.5*rotation2), amplitude)
    hessian_form(result, weights, measure*(force+rotation2*field), amplitude, radial/2+angular)
    hessian_form(result, weights, measure/2, phase_momentum)
    hessian_form(result, weights, -measure*background.frequency/lapse, phase_momentum, 2*amplitude+field[:, None]*(radial/2+angular))
    hessian_form(result, weights, measure*rotation2*field**2*3/16, radial)
    hessian_form(result, weights, measure*rotation2*field**2/2, angular)
    hessian_form(result, weights, measure*rotation2*field**2/4, radial, angular)
    return result


def whiten(matrix, cholesky):
    left = linalg.solve_triangular(cholesky, matrix, lower=True)
    return linalg.solve_triangular(cholesky, left.T, lower=True).T


def spectral_data(even, odd, gram, gravity_count, matter_count):
    cholesky = linalg.cholesky(gram, lower=True)
    even_white, odd_white = whiten(even, cholesky), whiten(odd, cholesky)
    even_white, odd_white = (even_white+even_white.T)/2, (odd_white+odd_white.T)/2
    even_eigenvalues, odd_eigenvalues = linalg.eigvalsh(even_white), linalg.eigvalsh(odd_white)
    signs = np.r_[np.ones(gravity_count+matter_count), -np.ones(matter_count)]
    inverse_mass = signs[:, None]*odd_white*signs[None, :]
    mass_factor = linalg.cholesky(inverse_mass, lower=True)
    squares = linalg.eigvalsh(mass_factor.T@even_white@mass_factor)
    return dict(even_min=float(even_eigenvalues[0]), odd_min=float(odd_eigenvalues[0]),
                frequency_squares=squares.tolist(), frequencies=np.sqrt(np.maximum(squares, 0)).tolist(),
                gram_condition=float(np.linalg.cond(gram)), negative_squares=int(np.count_nonzero(squares < 0)),
                even_symmetry_error=float(np.linalg.norm(even-even.T)/np.linalg.norm(even)),
                odd_symmetry_error=float(np.linalg.norm(odd-odd.T)/np.linalg.norm(odd)))
