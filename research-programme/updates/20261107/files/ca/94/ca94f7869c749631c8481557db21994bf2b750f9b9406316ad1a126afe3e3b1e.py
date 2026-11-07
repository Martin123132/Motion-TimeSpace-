from thermal_insertions import *


def ordered_cut(initial,first,second,first_pol,second_pol,shifted):
    middle,final=initial+first,initial+first+second
    propagator=spin.propagator(middle)
    first_vertex,second_vertex=spin.slash(first_pol),spin.slash(second_pol)
    shift_initial,shift_middle,shift_final=[shifted(momentum) for momentum in [initial,middle,final]]
    return (second_vertex*propagator*contracted_chain(shift_middle)*propagator*first_vertex
            +second_vertex*propagator*contracted_chain(shift_middle*first_vertex*shift_initial)
            +contracted_chain(shift_final*second_vertex*shift_middle)*propagator*first_vertex
            +contracted_chain(shift_final*second_vertex*shift_middle*first_vertex*shift_initial))


def radial_decomposition(initial,incoming,outgoing,incoming_pol,outgoing_pol,direction):
    null=spin.photon(mp.mpf(1),direction)
    final=initial+incoming-outgoing
    if abs(spin.dot(initial,initial)-1)>mp.mpf('1e-40') or abs(spin.dot(final,final)-1)>mp.mpf('1e-40'):
        raise ValueError('Radial decomposition requires bare on-shell external electrons')
    constant,soft=mp.zeros(4),mp.zeros(4)
    poles=[]
    transfers,polarizations=[incoming,-outgoing],[incoming_pol,outgoing_pol]
    for first,second in [(0,1),(1,0)]:
        middle=initial+transfers[first]
        defect=spin.dot(middle,middle)-1
        projection=spin.dot(middle,null)
        location=abs(defect/(2*projection))
        sign=mp.sign(defect/projection)
        residue=(spin.slash(middle-sign*location*null)+mp.eye(4))/(-2*sign*projection)
        def shifted(momentum):
            if mp.norm(momentum-middle)<mp.mpf('1e-45'):
                return residue
            return spin.propagator(momentum-sign*location*null)
        pole_residue=ordered_cut(initial,transfers[first],transfers[second],polarizations[first],polarizations[second],shifted)
        poles.append(dict(location=location,coefficient=2*location*pole_residue,
                          denominator_slope_sign=mp.sign(-2*sign*projection),order=(first,second)))
        constant+=2*ordered_cut(initial,transfers[first],transfers[second],polarizations[first],polarizations[second],
                               lambda momentum:spin.slash(null)/(2*spin.dot(momentum,null)))
        soft+=contracted_chain((spin.slash(final)+mp.eye(4))*spin.slash(polarizations[second])
                               *spin.propagator(middle)*spin.slash(polarizations[first])
                               *(spin.slash(initial)+mp.eye(4)))/(2*spin.dot(initial,null)*spin.dot(final,null))
    return dict(constant=constant,soft=soft,poles=poles)


def reconstruct(coefficients,energy):
    return coefficients['constant']+coefficients['soft']/energy**2+sum(
        (pole['coefficient']/(energy**2-pole['location']**2) for pole in coefficients['poles']),mp.zeros(4))


def planck_moment(value):
    return mp.mpf(1) if value==0 else value/mp.expm1(value)


def thermal_hilbert(location):
    location=mp.mpf(location)
    if location<=0:
        raise ValueError('A strictly positive interior pole is required')
    end=max(2*location,mp.mpf(1))
    at_pole=planck_moment(location)
    def subtracted(value):
        if abs(value-location)<mp.mpf('1e-25'):
            return mp.diff(planck_moment,location)
        return (planck_moment(value)-at_pole)/(value-location)
    positive=mp.quad(subtracted,[0,location,end])+at_pole*mp.log((end-location)/location)
    positive+=mp.quad(lambda value:planck_moment(value)/(value-location),[end,mp.inf])
    negative=mp.quad(lambda value:planck_moment(value)/(value+location),[0,1,mp.inf])
    return (positive-negative)/(2*location)


def finite_radial(coefficients,temperature):
    result=coefficients['constant']*temperature**2*mp.pi**2/6
    for pole in coefficients['poles']:
        scaled=pole['location']/temperature
        kernel=thermal_hilbert(scaled)-mp.j*mp.pi*pole['denominator_slope_sign']/(2*mp.expm1(scaled))
        result+=pole['coefficient']*kernel
    return result
