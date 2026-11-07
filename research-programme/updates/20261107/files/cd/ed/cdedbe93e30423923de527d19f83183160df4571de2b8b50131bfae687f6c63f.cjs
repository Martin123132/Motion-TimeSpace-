"use strict";
const {ratio,floorFor}=require("./force.cjs");

function coupling(result,background){
  const {speed,field,hubble,mu,omegaMatter,fraction}=background;
  const roll=Math.abs(speed/hubble), lightForce=Math.abs((mu/hubble)**2*field);
  if(!(roll>0 && lightForce>0 && fraction===.5 && omegaMatter>0 && omegaMatter<1))throw Error("rolling background");
  const rows=result.rows.map(row=>{
    const sectors=row.sectors.map(sector=>{
      const ell=sector.ell,radius=sector.outerTotalSphericalMassUpper*4.30091727e-6/sector.outerTotalSpeedUpper**2;
      const alpha=(radius*sector.outerTotalSpeedUpper/result.unitsKpcKmS)**2/(ell+1);
      return [2,4].map(cap=>{
        const beta=cap*row.flat*radius/result.unitsKpcKmS;
        const roots=[256,512].map(steps=>floorFor(strength=>
          ratio(ell,row.fraction,(1+strength)*alpha,Math.sqrt(1+strength)*beta,steps),row.target));
        if(Math.abs(roots[1]-roots[0])>2e-4*Math.max(1e-12,roots[1]))throw Error("mediator floor resolution");
        const coupling=Math.sqrt(roots[1]/2);
        return {ell,cap,forceStrengthFloor:roots[1],dimensionlessMassSensitivityFloor:coupling,
          absLogMassDriftPerEFoldFloor:coupling*roll,cosmicHeavySourceOverBareLightForceFloor:coupling*3*fraction*omegaMatter/lightForce};
      });
    });
    return {name:row.name,sectors};
  });
  const limits=[0,1].map(ell=>[0,1].map(index=>{
    const sample=rows.map(row=>({name:row.name,...row.sectors[ell][index]})).sort((a,b)=>b.forceStrengthFloor-a.forceStrengthFloor);
    return {ell,cap:sample[0].cap,positive:sample.filter(row=>row.forceStrengthFloor>0).length,strongest:sample[0]};
  }));
  return {background,limits,rows,scope:"Necessary same-pole unscreened strength. The inherited zero-coupling fixture is a consistency test, not a refit or a bound on a screened or subdominant carrier."};
}
module.exports={coupling};
if(require.main===module){
  const fs=require("node:fs"),path=require("node:path"),dir=__dirname;
  const result=JSON.parse(fs.readFileSync(path.join(dir,"force-result.json"),"utf8"));
  const fixture=JSON.parse(fs.readFileSync(path.join(dir,"coupling-fixture.json"),"utf8"));
  process.stdout.write(JSON.stringify(coupling(result,fixture),null,2)+"\n");
}
