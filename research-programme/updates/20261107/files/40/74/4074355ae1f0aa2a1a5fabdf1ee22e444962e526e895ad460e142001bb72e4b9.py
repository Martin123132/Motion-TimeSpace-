from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_physical_native_kernel_20260928 import NativeKernel,decimals,maximum
from annular_native_trial_matrix_20261001 import atoms,transport
from annular_nested_physical_refinement_v3_20260922 import RefinedLoads
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_candidate_midpoint_20260921 import CommonCoordinateAction
from annular_live_P2_canonical_v2_20260918 import material_weight
from search_annular_nonzero_shape_constraint_v3_20261001 import profiles
from decimal import Decimal,localcontext
import numpy as np


ZERO = Decimal(0)


def flat_basis(knots,anchor,lower,upper,count=24):
    knots = np.asarray(knots,float)
    left = knots<anchor
    fraction = np.where(left,(anchor-knots)/(anchor-lower),(knots-anchor)/(upper-anchor))
    coordinate = (fraction-.5)/.32
    envelope = np.maximum(1-coordinate**2,0)**4
    polynomial = np.polynomial.legendre.legvander(coordinate,count//2-1)
    values = polynomial*envelope[:,None]
    result = np.zeros((len(knots),count))
    result[:,0] = values[:,0]
    result[:,1] = np.where(left,values[:,0],-values[:,0])
    for degree in range(1,count//2):
        result[:,2*degree] = np.where(left,values[:,degree],0)
        result[:,2*degree+1] = np.where(left,0,values[:,degree])
    return result


def movements(engine,edges,source,count=33):
    radius = np.asarray(edges,float)
    fraction = np.where(radius<=float(source),(radius-radius[0])/(float(source)-radius[0]),
        (radius[-1]-radius)/(radius[-1]-float(source)))
    value = profiles(radius,count)[0]
    boundary = np.where((radius<=float(source))[:,None],value[:1],value[-1:])
    result = value-fraction[:,None]*profiles(float(source),count)[0]-(1-fraction[:,None])*boundary
    result[[0,engine.anchor,-1]] = 0.
    return decimals(result)


def native_values(engine,field):
    indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
    if np.any(indices<0):
        raise ValueError('Native support must not contain pinned source')
    return field[indices],indices


def divided_image(engine,edges,field):
    native = edges[engine.native_edges]
    values,indices = native_values(engine,field)
    scalar = field.ndim==1
    if scalar:
        values = values[:,None]
    kernel = np.full((len(native)-3,values.shape[1]),ZERO,dtype=object)
    coefficients = []
    for index in range(len(kernel)):
        width,row = engine.stencil(native[index:index+4])
        row = np.array(row,dtype=object)/width.sqrt()*int(engine.enabled)
        coefficients.append(row)
        kernel[index] = np.sum(row[:,None]*values[index:index+4],axis=0)
    rows,columns,weights,shape = engine.maps['template']
    image = np.full((shape[0],values.shape[1]),ZERO,dtype=object)
    np.add.at(image,rows,weights[:,None]*kernel[columns])
    return (image[:,0] if scalar else image),kernel,np.array(coefficients),indices


def flat_image_and_tangent(engine,edges,field,movement):
    image,kernel,coefficients,indices = divided_image(engine,edges,field)
    unused,left,right,unused2,unused3,unused4 = atoms(engine,edges,field)
    gradients = np.vstack([left[:1],(right[:-1]+left[1:])/2,right[-1:]])[engine.native_edges]
    field_rate = movement[engine.native_edges,:,None]*gradients[:,None,:]
    native,native_rate = edges[engine.native_edges],movement[engine.native_edges]
    values = field[indices]
    derivatives = np.full((len(kernel),movement.shape[1],field.shape[1]),ZERO,dtype=object)
    for index in range(len(kernel)):
        points = native[index:index+4]
        speeds = native_rate[index:index+4]
        width = (points[-1]-points[0])/3
        delta_width = (speeds[-1]-speeds[0])/3
        for local in range(4):
            logarithm = Decimal('2.5')*delta_width/width
            for other in range(4):
                if other!=local:
                    logarithm -= (speeds[local]-speeds[other])/(points[local]-points[other])
            derivatives[index] += coefficients[index,local]*(logarithm[:,None]*values[index+local]
                +field_rate[index+local])
    rows,columns,weights,shape = engine.maps['template']
    tangent = np.full((shape[0],movement.shape[1],field.shape[1]),ZERO,dtype=object)
    np.add.at(tangent,rows,weights[:,None,None]*derivatives[columns])
    return image,tangent,field_rate


def shape_forms(engine,data,field,movement):
    image,tangent,field_rate = flat_image_and_tangent(engine,data['edges'],field,movement)
    coefficient = np.asarray(engine.apply('sampling',data['beta']),float)
    changed = engine.sampling@np.asarray(data['beta_radial'][:,None]*movement[engine.native_edges],float)
    image_float,tangent_float = np.asarray(image,float),np.asarray(tangent,float)
    work = np.einsum('ai,a,akj->kij',image_float,coefficient,tangent_float)
    forms = (work+work.transpose(0,2,1))/2+np.einsum('ai,ak,aj->kij',image_float,changed,image_float)/2
    potential = (image_float.T*coefficient)@image_float/2
    return forms,potential,image,tangent,field_rate


class NativeFlatLoads(RefinedLoads):
    def __init__(self,owner,coordinates,rates,mesh,packet,extension,deadline):
        super().__init__(owner,coordinates,rates,mesh,packet,extension,deadline)
        self.native_engine = NativeKernel(mesh,packet['gram_support'],extension!='reference')
        engine = self.native_engine
        self.native_references = np.array([float(engine.references[index]) for index in engine.native_edges])
        self.native_sampling = engine.sampling.tocsc()
        factors = []
        with localcontext() as context:
            context.prec = 64
            reference = np.array(engine.references,dtype=object)
            anchor = reference[engine.anchor]
            fractions = np.array([(point-reference[0])/(anchor-reference[0]) if point<=anchor
                else (reference[-1]-point)/(reference[-1]-anchor) for point in reference],dtype=object)
            for label_index,label in enumerate(owner.layer_rule.points/2):
                source = coordinates[label_index,-1]
                lower = reference[0]+Decimal.from_float(float(owner.width))*Decimal.from_float(float(label))
                upper = reference[-1]+Decimal.from_float(float(owner.width))*Decimal.from_float(float(label))
                edges = np.array([lower+(source-lower)*fraction if point<=anchor else upper+(source-upper)*fraction
                    for point,fraction in zip(reference,fractions)],dtype=object)
                field = coordinates[label_index,:-1]
                atom = engine.atoms(edges,field)
                if maximum(atom['slope_left'][engine.anchor:engine.anchor+1])!=0 or maximum(atom['slope_right'][engine.anchor-1:engine.anchor])!=0:
                    raise ValueError('NativeFlatLoads requires exactly source-flat field')
                image = divided_image(engine,edges,field)[0] if extension!='reference' else np.zeros(engine.template.shape[0])
                factors.append(np.asarray(image,float))
        self.native_factor_vertices = np.array(factors)
        self.native_factor_coefficients = owner.layer_rule.inverse@self.native_factor_vertices

    def native_node_load(self,labels,index,extension):
        if extension=='reference':
            return np.zeros_like(labels)
        start,end = self.native_sampling.indptr[index:index+2]
        indices = self.native_sampling.indices[start:end]
        weights = self.native_sampling.data[start:end]
        images = np.polynomial.chebyshev.chebval(2*labels,self.native_factor_coefficients[:,indices])
        return np.sum(weights[:,None]*images**2,axis=0)/2

    def gram_density(self,radius,extension,omit_spatial_jacobian=False,omit_label_jacobian=False):
        answer = np.zeros_like(radius)
        if extension=='reference':
            return answer
        for index,reference in enumerate(self.native_references):
            lower,upper = self.material.node_geometry(reference,np.array([-.5,.5]))[0]
            selected = (radius>=lower)&(radius<=upper)
            if not np.any(selected):
                continue
            labels = self.material.inverse_node(radius[selected],reference)
            unused,unused2,label_jacobian = self.material.node_geometry(reference,labels)
            answer[selected] += material_weight(labels)*self.native_node_load(labels,index,extension)/label_jacobian
        return answer


def live_native_flat(owner,coordinates,rates,mesh,packet,extension,deadline):
    loads = NativeFlatLoads(owner,coordinates,rates,mesh,packet,extension,deadline)
    solver = CandidateRadialSolve(loads,22,28,[extension])
    solution = solver.solve(extension)
    action = CommonCoordinateAction(owner,coordinates,rates,mesh,loads,solver,solution,64)
    return loads,action


def trial_norm(action,field,order=8,label=0.):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source = float(cardinal@action.source)
    quad = action.quadrature(label,source,order)
    local = quad['local']
    shape = np.array([(1-local)*(1-2*local),4*local*(1-local),local*(2*local-1)]).T
    indices = np.array(action.mesh['elements'])[quad['cells']]
    shape *= indices>=0
    collocation = np.einsum('qv,qvb->qb',shape,np.asarray(field,float)[np.maximum(indices,0)])
    geometry = action.geometry(quad['reference'],source,label)
    weighted = collocation*np.sqrt(quad['measure']*geometry['kinetic'])[:,None]
    return weighted.T@weighted,weighted

