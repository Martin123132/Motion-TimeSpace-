from annular_source_flat_native_20261002 import NativeFlatLoads,flat_basis,trial_norm
from annular_nested_physical_refinement_v3_20260922 import RefinedLoads
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_candidate_midpoint_20260921 import CommonCoordinateAction
from annular_physical_native_kernel_20260928 import NativeKernel,decimals
from annular_native_trial_matrix_20261001 import atoms
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from decimal import Decimal,localcontext
import numpy as np


ZERO = Decimal(0)


def physical_edges(engine,source,label,width):
    reference = np.array(engine.references,dtype=object)
    anchor = reference[engine.anchor]
    lower = reference[0]+Decimal.from_float(float(width))*Decimal.from_float(float(label))
    upper = reference[-1]+Decimal.from_float(float(width))*Decimal.from_float(float(label))
    fractions = np.array([(point-reference[0])/(anchor-reference[0]) if point<=anchor
        else (reference[-1]-point)/(reference[-1]-anchor) for point in reference],dtype=object)
    return np.array([lower+(source-lower)*fraction if point<=anchor else upper+(source-upper)*fraction
        for point,fraction in zip(reference,fractions)],dtype=object)


def core_basis(owner,engine,source,ratios):
    reference = np.array([Decimal(value.numerator)/Decimal(value.denominator) for value in owner.model.radii_exact],dtype=object) if hasattr(owner.model,'radii_exact') else decimals(owner.model.radii)
    anchor = engine.references[engine.anchor]
    lower,upper = engine.references[0],engine.references[-1]
    fraction = np.array([abs((point-anchor)/((lower if point<anchor else upper)-anchor)) for point in reference],dtype=object)
    taper = np.full(len(reference),ZERO,dtype=object)
    for index,value in enumerate(fraction):
        if value<=Decimal('.18'):
            taper[index] = Decimal(1)
        elif value<Decimal('.82'):
            coordinate = (value-Decimal('.18'))/Decimal('.64')
            taper[index] = 1-35*coordinate**4+84*coordinate**5-70*coordinate**6+20*coordinate**7
    interior = decimals(flat_basis(owner.model.radii,float(anchor),float(lower),float(upper)))
    basis = np.full((len(reference),len(source),26),ZERO,dtype=object)
    for index,label in enumerate(owner.layer_rule.points/2):
        edges = physical_edges(engine,source[index],label,owner.width)
        offset = nodal_radii(engine,edges)-source[index]
        quadratic = offset**2*taper/2
        basis[:,index,0] = offset*taper+Decimal.from_float(float(ratios[index]))*quadratic
        basis[:,index,1] = quadratic
        basis[:,index,2:] = interior
    return basis


def compensated_shapes(engine,edges,field,movement=None):
    widths,left,right,curvature,unused,unused2 = atoms(engine,edges,field)
    jump = left[engine.anchor]-right[engine.anchor-1]
    native = edges[engine.native_edges]
    source = edges[engine.anchor]
    indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
    hinge = np.maximum(native-source,ZERO)
    values = field[indices]-hinge[:,None]*jump
    gradients = np.vstack([left[:1],(right[:-1]+left[1:])/2,right[-1:]])
    if movement is not None:
        if np.any(movement[engine.anchor]):
            raise ValueError('Fast tangent requires source-pinned generators')
        native_rate = movement[engine.native_edges]
        delta_values = native_rate[:,:,None]*gradients[engine.native_edges,None,:]
        source_left,source_right = engine.anchor-1,engine.anchor
        left_rate = movement[source_left,:,None]*gradients[source_left,None,:]
        left_middle_rate = (movement[source_left]+movement[source_left+1])[:,None]*(left[source_left]+right[source_left])[None,:]/4
        right_rate = movement[source_right+1,:,None]*gradients[source_right+1,None,:]
        right_middle_rate = (movement[source_right]+movement[source_right+1])[:,None]*(left[source_right]+right[source_right])[None,:]/4
        delta_left_slope = (left_rate-4*left_middle_rate)/widths[source_left]
        delta_left_slope -= ((movement[source_left+1]-movement[source_left])/widths[source_left])[:,None]*right[source_left]
        delta_right_slope = (4*right_middle_rate-right_rate)/widths[source_right]
        delta_right_slope -= ((movement[source_right+1]-movement[source_right])/widths[source_right])[:,None]*left[source_right]
        delta_jump = delta_right_slope-delta_left_slope
        delta_values -= hinge[:,None,None]*delta_jump[None,:,:]
        delta_values -= np.where((native>source)[:,None],native_rate,ZERO)[:,:,None]*jump[None,None,:]
        derivatives = np.full((len(native)-3,movement.shape[1],field.shape[1]),ZERO,dtype=object)
    kernels = np.full((len(native)-3,field.shape[1]),ZERO,dtype=object)
    for index in range(len(kernels)):
        points = native[index:index+4]
        width,coefficient = engine.stencil(points)
        coefficient = np.array(coefficient,dtype=object)*int(engine.enabled)/width.sqrt()
        kernels[index] = np.sum(coefficient[:,None]*values[index:index+4],axis=0)
        if movement is not None:
            velocities = native_rate[index:index+4]
            delta_width = (velocities[-1]-velocities[0])/3
            for local in range(4):
                logarithm = Decimal('2.5')*delta_width/width
                for other in range(4):
                    if local!=other:
                        logarithm -= (velocities[local]-velocities[other])/(points[local]-points[other])
                derivatives[index] += coefficient[local]*(logarithm[:,None]*values[index+local]+delta_values[index+local])
    rows,columns,coefficient,shape = engine.maps['template']
    image = np.full((shape[0],field.shape[1]),ZERO,dtype=object)
    np.add.at(image,rows,coefficient[:,None]*kernels[columns])
    if movement is None:
        return image
    tangent = np.full((shape[0],movement.shape[1],field.shape[1]),ZERO,dtype=object)
    np.add.at(tangent,rows,coefficient[:,None,None]*derivatives[columns])
    return image,tangent,jump,delta_jump


def core_forms(engine,data,field,movement):
    image,tangent,jump,delta_jump = compensated_shapes(engine,data['edges'],field,movement)
    coefficient = np.asarray(engine.apply('sampling',data['beta']),float)
    changed = engine.sampling@np.asarray(data['beta_radial'][:,None]*movement[engine.native_edges],float)
    image_float,tangent_float = np.asarray(image,float),np.asarray(tangent,float)
    product = np.einsum('ai,a,akj->kij',image_float,coefficient,tangent_float)
    forms = (product+product.transpose(0,2,1))/2+np.einsum('ai,ak,aj->kij',image_float,changed,image_float)/2
    potential = (image_float.T*coefficient)@image_float/2
    return forms,potential,image,tangent,jump,delta_jump


class NativeCoreLoads(NativeFlatLoads):
    def __init__(self,owner,coordinates,rates,mesh,packet,extension,deadline):
        RefinedLoads.__init__(self,owner,coordinates,rates,mesh,packet,extension,deadline)
        engine = NativeKernel(mesh,packet['gram_support'],extension!='reference')
        self.native_engine = engine
        self.native_references = np.array([float(engine.references[index]) for index in engine.native_edges])
        self.native_sampling = engine.sampling.tocsc()
        factors = []
        with localcontext() as context:
            context.prec = 64
            for index,label in enumerate(owner.layer_rule.points/2):
                edges = physical_edges(engine,coordinates[index,-1],label,owner.width)
                factors.append(np.asarray(compensated_shapes(engine,edges,coordinates[index,:-1,None])[:,0],float))
        self.native_factor_vertices = np.array(factors)
        self.native_factor_coefficients = owner.layer_rule.inverse@self.native_factor_vertices


def live_core(owner,coordinates,rates,mesh,packet,extension,deadline):
    loads = NativeCoreLoads(owner,coordinates,rates,mesh,packet,extension,deadline)
    solver = CandidateRadialSolve(loads,22,28,[extension])
    solution = solver.solve(extension)
    action = CommonCoordinateAction(owner,coordinates,rates,mesh,loads,solver,solution,64)
    return loads,action


def source_geometry(action,labels):
    cardinal = np.array([np.asarray(action.cardinal(label)).ravel() for label in labels])
    radii = cardinal@action.source
    values,derivatives = action.solver.values(action.solution,radii)
    metric = 1-2*values[0]/radii
    metric_radial = -2*derivatives[0]/radii+2*values[0]/radii**2
    speed_square = np.exp(2*values[1])*metric
    drift = speed_square*(2/radii+derivatives[1]+metric_radial/(2*metric))
    return cardinal,speed_square,drift
