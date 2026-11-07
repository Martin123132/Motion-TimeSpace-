"use strict";
function flux(data,coupling){
  const galaxy=data.profiles.find(row=>row.name==="DDO154");
  const outer=galaxy.points.find(point=>point[0]===galaxy.outerRadius);
  const nu=galaxy.outerDeficit/299792.458**2, hubble=coupling.background.hubble;
  const radius=galaxy.outerRadius*3.0856775814913673e19, inverseOrbit=radius/(1000*outer[1]);
  const witness=coupling.limits.flatMap(group=>group.map(row=>{
    const bound=row.strongest;
    if(bound.name!==galaxy.name)throw Error("unexpected controlling galaxy");
    return {ell:row.ell,cap:row.cap,strengthAtFloor:bound.forceStrengthFloor,
      dimensionlessAnisotropyAtFloor:2*bound.forceStrengthFloor*nu**2,
      anisotropyOverHaloCompactness:2*bound.forceStrengthFloor*nu,
      absoluteInstantaneousDriftTimesOrbitalPeriod:2*Math.PI*inverseOrbit*hubble*bound.absLogMassDriftPerEFoldFloor};
  }));
  const controls=[];
  for(const charge of [-2,0,2]){
    const rate=-.4;
    let error=0,poisson=0,accel=0;
    for(const r of [.2,.5,1,2,5]){
      const step=r*1e-4, field=x=>-charge/(4*Math.PI*Math.hypot(1,x));
      const grad=x=>charge*x/(4*Math.PI*Math.hypot(1,x)**3);
      const mass=r**3/Math.hypot(1,r)**3, density=3/(4*Math.PI*Math.hypot(1,r)**5);
      const numerical=(field(r+step)-field(r-step))/(2*step);
      const divergence=((r+step)**2*grad(r+step)-(r-step)**2*grad(r-step))/(2*step*r**2);
      const surface=-4*Math.PI*r**2*rate*numerical;
      error=Math.max(error,Math.abs(surface+charge*rate*mass));
      poisson=Math.max(poisson,Math.abs(divergence-charge*density));
      accel=Math.max(accel,Math.abs(charge*numerical-2*charge**2*mass/(8*Math.PI*r**2)));
    }
    if(Math.max(error,poisson,accel)>1e-7)throw Error("flux, Gauss or acceleration");
    controls.push({charge,maxSurfaceExchangeError:error,maxPoissonError:poisson,maxExtraAccelerationError:accel});
  }
  return {nu,orderNuStrength:1/(2*nu),hubbleLightCrossing:hubble*radius/299792458,witness,controls};
}
module.exports={flux};
if(require.main===module){
  const fs=require("node:fs"),path=require("node:path");
  const data=JSON.parse(fs.readFileSync(0,"utf8").replace(/^\uFEFF/,""));
  const coupling=JSON.parse(fs.readFileSync(path.join(__dirname,"coupling-result.json"),"utf8"));
  process.stdout.write(JSON.stringify(flux(data,coupling),null,2)+"\n");
}
