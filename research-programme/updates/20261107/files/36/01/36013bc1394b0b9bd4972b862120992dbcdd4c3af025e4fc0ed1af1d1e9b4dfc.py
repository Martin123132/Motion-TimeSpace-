from __future__ import annotations

from seed_common import *
import sympy as sp
import urllib.request


def main():
    modest()
    folder=ROOT/'results/covariant-check'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def identity(name,expression):
        residual=sp.simplify(expression)
        checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
        assert residual==0,(name,residual)
    first,second,third=sp.symbols('first second third',real=True)
    coordinates=[first,second,third]
    zeta=sp.Function('zeta')(*coordinates)
    gradient=sp.Matrix([sp.diff(zeta,coordinate) for coordinate in coordinates])
    hessian=sp.hessian(zeta,coordinates)
    laplacian=sp.trace(hessian)
    gradient2=gradient.dot(gradient)
    curvature=sp.exp(-2*zeta)*(-4*laplacian-2*gradient2)
    tracefree=sp.exp(-2*zeta)*(-hessian+gradient*gradient.T+sp.eye(3)*(laplacian-gradient2)/3)
    identity('full three-dimensional curvature tracefree identity',sp.trace(tracefree))
    for component in range(3):
        divergence=sum(sp.diff(tracefree[index,component],coordinates[index])+
            3*gradient[index]*tracefree[index,component] for index in range(3))
        identity('covariant contracted spatial Bianchi component '+str(component),
            divergence-sp.diff(curvature,coordinates[component])/6)
    angle=sp.symbols('angle',real=True)
    fourth=sp.integrate(sp.cos(angle)**4*sp.sin(angle),(angle,0,sp.pi))/2
    second_moment=sp.integrate(sp.cos(angle)**2*sp.sin(angle),(angle,0,sp.pi))/2
    cross=sp.integrate(sp.sin(angle)**5,(angle,0,sp.pi))/16
    identity('massless angular fourth diagonal moment',fourth-sp.Rational(1,5))
    identity('massless angular fourth offdiagonal moment',cross-sp.Rational(1,15))
    identity('collisionless stress shear response coefficient',4*(fourth-cross)-sp.Rational(8,15))
    identity('isotropic angular second moment',second_moment-sp.Rational(1,3))
    sources=ROOT/'sources'
    sources.mkdir(exist_ok=False)
    records=[]
    for filename,url in [
        ('ma-bertschinger-initial-data.html','https://arxiv.org/html/astro-ph/9506072v1'),
        ('anisotropic-separate-universe.html','https://arxiv.org/html/2101.05707v1')]:
        request=urllib.request.Request(url,headers={'User-Agent':'MTS-private-research/1.0'})
        with urllib.request.urlopen(request,timeout=30) as response:
            content=response.read(8_000_001)
            assert len(content)<=8_000_000
            final_url=response.url
        path=sources/filename
        path.write_bytes(content)
        records.append(dict(url=url,final_url=final_url,path=str(path),sha256=digest(path),bytes=len(content),
            role='Primary convention/method reference; the displayed local identities are checked independently.'))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,source_records=records),
        __file__,[Path(row['path']) for row in records])
    print(json.dumps(dict(state='complete',identities=len(checks))))


if __name__=='__main__':
    main()
