from decimal import Decimal
import numpy as np


def source_hinge_image(engine,edges,source):
    native = edges[engine.native_edges]
    kernel = np.full(len(native)-3,Decimal(0),dtype=object)
    for index in range(len(kernel)):
        points = native[index:index+4]
        if not (points[0]<source<points[-1]) or not engine.enabled:
            continue
        width,coefficients = engine.stencil(points)
        kernel[index] = sum((coefficient*max(point-source,Decimal(0))
            for coefficient,point in zip(coefficients,points)),Decimal(0))/width.sqrt()
    return engine.apply('template',kernel)

