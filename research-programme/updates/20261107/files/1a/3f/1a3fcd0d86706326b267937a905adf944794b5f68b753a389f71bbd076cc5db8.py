from derive_annular_source_gravity_20260914 import EvidenceRun
from decimal import Decimal, localcontext
import numpy as np


def decimal_values(values):
    values = np.asarray(values)
    return np.array([value if isinstance(value,Decimal) else Decimal.from_float(float(value))
        for value in values.ravel()],dtype=object).reshape(values.shape)


def nodal_polynomials(mesh,values):
    result = []
    for indices in mesh['elements']:
        left,middle,right = [values[index] if index>=0 else np.full(values.shape[1],Decimal(0),dtype=object) for index in indices]
        result.append([left,-3*left+4*middle-right,2*left-4*middle+2*right])
    return np.array(result,dtype=object)


def cheb_product(first,second):
    shape = np.broadcast_shapes(first.shape[:-1],second.shape[:-1])
    result = np.full(shape+(first.shape[-1]+second.shape[-1]-1,),Decimal(0),dtype=object)
    for left in range(first.shape[-1]):
        for right in range(second.shape[-1]):
            value = first[...,left]*second[...,right]/2
            result[...,left+right] += value
            result[...,abs(left-right)] += value
    return result


def paired_cheb(coefficients,argument):
    argument = np.asarray(argument)
    while argument.ndim<coefficients.ndim-1:
        argument = argument[...,None]
    recent = np.zeros(coefficients.shape[:-1],dtype=coefficients.dtype)
    previous = recent.copy()
    for degree in range(coefficients.shape[-1]-1,0,-1):
        value = coefficients[...,degree]+2*argument*recent-previous
        previous,recent = recent,value
    return coefficients[...,0]+argument*recent-previous


class CompensatedPolynomial:
    def __init__(self,evaluator,directions,correction,parent_fields,precision=80):
        self.widths = evaluator.widths.copy()
        inverse = evaluator.action.owner.layer_rule.inverse
        self.degree = inverse.shape[0]-1
        if self.degree<1:
            raise ValueError('Expected nonconstant parent layer representation')
        self.exact = {}
        with localcontext() as context:
            context.prec = precision
            transform = decimal_values(inverse).T
            edges = evaluator.edges
            source = decimal_values(evaluator.action.source-evaluator.anchor)@transform
            shifted = source.copy()
            shifted[1] -= Decimal.from_float(float(evaluator.action.owner.width))/2
            side = np.array([1/(-Decimal.from_float(float(edges[0]))) if value<0
                else -1/Decimal.from_float(float(edges[-1])) for value in edges[:-1]],dtype=object)
            jacobian = side[:,None]*shifted
            jacobian[:,0] += 1
            widths = decimal_values(self.widths)
            denominator = widths[:,None]*jacobian
            displacement = np.where(edges<0,1+edges/(-edges[0]),1-edges/edges[-1])
            displacement = decimal_values(displacement)
            edge = decimal_values(evaluator.edge_vertices).T@transform
            source_change = decimal_values(evaluator.source_direction)@transform
            map_left = edge[:-1]+displacement[:-1,None]*source_change
            map_slope = edge[1:]-edge[:-1]+(displacement[1:]-displacement[:-1])[:,None]*source_change
            fields = dict(rounded_coefficients=decimal_values(evaluator.polynomials['field']),
                parent_nodal=nodal_polynomials(evaluator.action.mesh,decimal_values(parent_fields)))
            changed = dict(rounded_coefficients=decimal_values(evaluator.polynomials['field_change']),
                parent_nodal=nodal_polynomials(evaluator.action.mesh,
                    (decimal_values(directions['field_vertices'])-decimal_values(correction[:,:-1])).T))
            for variant in fields:
                field = fields[variant]@transform
                change = changed[variant]@transform
                numerator = cheb_product(denominator[:,None,:],change)
                numerator[:,0] -= cheb_product(map_left,field[:,1])
                numerator[:,1] -= 2*cheb_product(map_left,field[:,2])+cheb_product(map_slope,field[:,1])
                numerator[:,2] -= 2*cheb_product(map_slope,field[:,2])
                self.exact[variant] = dict(numerator=numerator,field=field,change=change)
            self.exact_denominator = denominator
            self.exact_map_left,self.exact_map_slope = map_left,map_slope
        self.denominator = np.asarray(denominator,float)
        self.coefficients = {name:np.asarray(data['numerator'],float) for name,data in self.exact.items()}

    def cells(self,evaluator,labels,offsets):
        source = evaluator.action.cardinal(labels)@(evaluator.action.source-evaluator.anchor)
        jacobian = np.where(offsets<source,1+(source-evaluator.action.owner.width*labels)/(-evaluator.edges[0]),
            1-(source-evaluator.action.owner.width*labels)/evaluator.edges[-1])
        reference = (offsets-source)/jacobian
        return np.clip(np.searchsorted(evaluator.edges,reference,side='right')-1,0,len(evaluator.widths)-1)

    def evaluate(self,variant,cells,labels,local):
        denominator = paired_cheb(self.denominator[cells],2*labels)
        if np.any(denominator<=0):
            raise ValueError('Nonpositive reconstructed material width')
        values = paired_cheb(self.coefficients[variant][cells],2*labels)
        return (values[:,0]+local*(values[:,1]+local*values[:,2]))/denominator

    def oracle(self,variant,cells,labels,local):
        with localcontext() as context:
            context.prec = 90
            labels,local = decimal_values(labels),decimal_values(local)
            denominator = paired_cheb(self.exact_denominator[cells],2*labels)
            data = self.exact[variant]
            field = paired_cheb(data['field'][cells],2*labels)
            change = paired_cheb(data['change'][cells],2*labels)
            movement = paired_cheb(self.exact_map_left[cells],2*labels)+local*paired_cheb(self.exact_map_slope[cells],2*labels)
            direct = change[:,0]+local*(change[:,1]+local*change[:,2])-movement*(field[:,1]+2*local*field[:,2])/denominator
            coefficient = paired_cheb(data['numerator'][cells],2*labels)
            reduced = (coefficient[:,0]+local*(coefficient[:,1]+local*coefficient[:,2]))/denominator
            binary = self.evaluate(variant,cells,np.asarray(labels,float),np.asarray(local,float))
            scale = max(float(np.max(abs(direct))),1e-300)
            basis = np.polynomial.chebyshev.chebvander(2*np.asarray(labels,float),self.coefficients[variant].shape[-1]-1)
            absolute = np.einsum('qpd,qd->qp',abs(self.coefficients[variant][cells]),abs(basis))
            powers = np.array([np.ones(len(local)),abs(np.asarray(local,float)),np.asarray(local,float)**2]).T
            absolute = np.sum(absolute*powers,axis=1)/np.asarray(denominator,float)
            error = np.asarray(abs(decimal_values(binary)-direct),float)
            bound = 128*(self.degree+1)**2*np.finfo(float).eps*np.maximum(absolute,1e-300)
            return dict(direct=np.asarray(direct,float),reduced=np.asarray(reduced,float),binary=binary,
                exact_relative=float(np.max(abs(direct-reduced)))/scale,binary_relative=float(np.max(error))/scale,
                arithmetic_error=error,arithmetic_budget=bound,within_arithmetic_budget=bool(np.all(error<=bound)))
