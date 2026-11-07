from derive_annular_source_gravity_20260914 import EvidenceRun
from decimal import Decimal
import numpy as np


ZERO = Decimal(0)


def atoms(engine,edges,field):
    widths = np.diff(edges)
    values = np.full(engine.indices.shape+(field.shape[1],),ZERO,dtype=object)
    selected = engine.indices>=0
    values[selected] = field[engine.indices[selected]]
    left,middle,right = values.transpose(1,0,2)
    first = (-3*left+4*middle-right)/widths[:,None]
    last = (left-4*middle+3*right)/widths[:,None]
    second = 4*(left-2*middle+right)/widths[:,None]**2
    jump = first[1:]-last[:-1]
    jump[engine.anchor-1] = ZERO
    return widths,first,last,second,jump,second[1:]-second[:-1]


def transport(engine,edges,field,movement):
    widths,first,last,unused,unused2,unused3 = atoms(engine,edges,field)
    gradient = np.full(field.shape,ZERO,dtype=object)
    displacement = np.full((engine.count,movement.shape[1]),ZERO,dtype=object)
    counts = np.zeros(engine.count,dtype=int)
    for local,slopes,velocities in [(0,first,movement[:-1]),(1,(first+last)/2,(movement[:-1]+movement[1:])/2),(2,last,movement[1:])]:
        selected = engine.indices[:,local]>=0
        indices = engine.indices[selected,local]
        np.add.at(gradient,indices,slopes[selected])
        np.add.at(displacement,indices,velocities[selected])
        np.add.at(counts,indices,1)
    return displacement[:,:,None]*gradient[:,None,:]/counts[:,None,None]**2


def image_and_tangent(engine,edges,field,movement,field_rate):
    widths,first,last,second,jump,curvature = atoms(engine,edges,field)
    tests,basis = movement.shape[1],field.shape[1]
    unused,rate_first,rate_last,rate_second,unused2,unused3 = atoms(engine,edges,field_rate.reshape(engine.count,-1))
    stretch = np.diff(movement,axis=0)/widths[:,None]
    rate_first = rate_first.reshape(len(widths),tests,basis)-stretch[:,:,None]*first[:,None,:]
    rate_last = rate_last.reshape(len(widths),tests,basis)-stretch[:,:,None]*last[:,None,:]
    rate_second = rate_second.reshape(len(widths),tests,basis)-2*stretch[:,:,None]*second[:,None,:]
    rate_jump = rate_first[1:]-rate_last[:-1]
    rate_jump[engine.anchor-1] = ZERO
    rate_curvature = rate_second[1:]-rate_second[:-1]
    native,native_rate = edges[engine.native_edges],movement[engine.native_edges]
    kernels = np.full((len(native)-3,basis),ZERO,dtype=object)
    derivatives = np.full((len(native)-3,tests,basis),ZERO,dtype=object)
    if engine.enabled:
        for index in range(len(kernels)):
            points,velocities = native[index:index+4],native_rate[index:index+4]
            width,coefficients = engine.stencil(points)
            delta_width = (velocities[-1]-velocities[0])/3
            changed = []
            for local in range(4):
                logarithm = 3*delta_width/width
                for other in range(4):
                    if local!=other:
                        logarithm -= (velocities[local]-velocities[other])/(points[local]-points[other])
                changed.append(coefficients[local]*logarithm)
            value = np.full(basis,ZERO,dtype=object)
            rate = np.full((tests,basis),ZERO,dtype=object)
            for face in range(engine.native_edges[index]+1,engine.native_edges[index+3]):
                hinges = [max(point-edges[face],ZERO) for point in points]
                hinge_rates = [velocities[local]-movement[face] if point>edges[face] else np.full(tests,ZERO,dtype=object)
                    for local,point in enumerate(points)]
                response = sum((coefficient*hinge for coefficient,hinge in zip(coefficients,hinges)),ZERO)
                twice = sum((coefficient*hinge**2/2 for coefficient,hinge in zip(coefficients,hinges)),ZERO)
                delta = sum((change*hinge+coefficient*hinge_rate for change,hinge,coefficient,hinge_rate
                    in zip(changed,hinges,coefficients,hinge_rates)),np.full(tests,ZERO,dtype=object))
                delta_twice = sum((change*hinge**2/2+coefficient*hinge*hinge_rate for change,hinge,coefficient,hinge_rate
                    in zip(changed,hinges,coefficients,hinge_rates)),np.full(tests,ZERO,dtype=object))
                value += jump[face-1]*response+curvature[face-1]*twice
                rate += rate_jump[face-1]*response+delta[:,None]*jump[face-1]
                rate += rate_curvature[face-1]*twice+delta_twice[:,None]*curvature[face-1]
            kernels[index] = value/width.sqrt()
            derivatives[index] = (rate-delta_width[:,None]*value/(2*width))/width.sqrt()
    rows,columns,coefficients,shape = engine.maps['template']
    image = np.full((shape[0],basis),ZERO,dtype=object)
    tangent = np.full((shape[0],tests,basis),ZERO,dtype=object)
    np.add.at(image,rows,coefficients[:,None]*kernels[columns])
    np.add.at(tangent,rows,coefficients[:,None,None]*derivatives[columns])
    return image,tangent

