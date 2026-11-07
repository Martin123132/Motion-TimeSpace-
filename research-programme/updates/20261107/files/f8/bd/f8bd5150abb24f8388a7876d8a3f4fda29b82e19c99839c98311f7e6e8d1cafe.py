from derive_annular_source_gravity_20260914 import EvidenceRun
from bisect import bisect_right
from fractions import Fraction


def native_mesh(model):
    edges = [Fraction.from_float(float(value)) for value in model.edges]
    nodes = [None]*model.count
    elements = [list(map(int, row)) for row in model.element_indices]
    for number, indices in enumerate(elements):
        locations = [edges[number], (edges[number]+edges[number+1])/2, edges[number+1]]
        for index, location in zip(indices, locations):
            if index >= 0:
                if nodes[index] is not None and nodes[index] != location:
                    raise ValueError('Inconsistent canonical native node.')
                nodes[index] = location
    if any(value is None for value in nodes):
        raise ValueError('Native coefficient has no node.')
    return dict(edges=edges, nodes=nodes, elements=elements, count=len(nodes),
        anchor=Fraction.from_float(float(model.anchor)))


def common_mesh(first, last):
    if first['anchor'] != last['anchor'] or first['edges'][0] != last['edges'][0] or first['edges'][-1] != last['edges'][-1]:
        raise ValueError('Common interval and source trace required.')
    edges = sorted(set(first['edges']) | set(last['edges']))
    all_nodes = sorted(edges+[(lower+upper)/2 for lower, upper in zip(edges[:-1], edges[1:])])
    nodes = [value for value in all_nodes if value != first['anchor']]
    indices = {value:index for index, value in enumerate(nodes)}
    elements = [[indices.get(lower, -1), indices[(lower+upper)/2], indices.get(upper, -1)]
        for lower, upper in zip(edges[:-1], edges[1:])]
    return dict(edges=edges, nodes=nodes, elements=elements, count=len(nodes), anchor=first['anchor'])


def evaluation_row(mesh, location):
    element = min(max(bisect_right(mesh['edges'], location)-1, 0), len(mesh['edges'])-2)
    lower, upper = mesh['edges'][element:element+2]
    fraction = (location-lower)/(upper-lower)
    shapes = [(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)]
    return {index:value for index, value in zip(mesh['elements'][element], shapes) if index >= 0 and value}


def evaluation_rows(mesh, locations):
    return [evaluation_row(mesh, location) for location in locations]


def apply_rows(rows, values):
    return [sum((value*values[column] for column, value in row.items()), Fraction(0)) for row in rows]


def compose_rows(first, last):
    answer = []
    for row in first:
        result = {}
        for inner, factor in row.items():
            for column, value in last[inner].items():
                result[column] = result.get(column, Fraction(0))+factor*value
        answer.append({column:value for column, value in result.items() if value})
    return answer


def forms(mesh, values):
    mass, stiffness = Fraction(0), Fraction(0)
    for element, indices in enumerate(mesh['elements']):
        left, middle, right = [values[index] if index >= 0 else Fraction(0) for index in indices]
        length = mesh['edges'][element+1]-mesh['edges'][element]
        mass += length*(4*left**2+16*middle**2+4*right**2+4*left*middle-2*left*right+4*middle*right)/30
        stiffness += (7*left**2+16*middle**2+7*right**2-16*left*middle+2*left*right-16*middle*right)/(3*length)
    return mass, stiffness


def serialize_mesh(mesh):
    return dict(edges=list(map(str, mesh['edges'])), nodes=list(map(str, mesh['nodes'])),
        elements=mesh['elements'], count=mesh['count'], anchor=str(mesh['anchor']))


def serialize_rows(rows):
    return [{str(column):str(value) for column, value in row.items()} for row in rows]
