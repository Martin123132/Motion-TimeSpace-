"use strict";

const insist=(ok,msg)=>{if(!ok)throw Error(msg);};
function integrate(fix,charge,law,zEnd,steps){
  const field0=fix.field, mass=fix.mu/fix.hubble, dz=zEnd/steps;
  let state=[field0,fix.speed/fix.hubble,fix.omegaMatter*fix.fraction,fix.omegaMatter*(1-fix.fraction),.00009,1,0];
  const rates=(z,[field,speed,heavy,other,radiation,hubble])=>{
    const argument=charge*(field-field0), denom=law==="mass" ? 1+argument : 1+2*argument;
    insist(denom>0 && heavy>0 && hubble>0,"nonpositive fluctuation state");
    const eff=charge/denom, conversion=-1/((1+z)*hubble);
    return [speed,-3*hubble*speed-mass**2*field-3*eff*heavy,(-3*hubble+eff*speed)*heavy,
      -3*hubble*other,-4*hubble*radiation,-(speed**2)/2-1.5*(heavy+other)-2*radiation]
      .map(rate=>rate*conversion).concat(1/hubble);
  };
  const shifted=(values,rate,offset)=>values.map((v,i)=>v+rate[i]*offset);
  for(let index=0;index<steps;index++){
    const z=index*dz,k1=rates(z,state),k2=rates(z+dz/2,shifted(state,k1,dz/2));
    const k3=rates(z+dz/2,shifted(state,k2,dz/2)),k4=rates(z+dz,shifted(state,k3,dz));
    state=state.map((v,i)=>v+dz*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6);
  }
  const [field,speed,heavy,other,radiation,hubble,comoving]=state;
  const constraint=hubble**2-(heavy+other+radiation+speed**2/6+mass**2*field**2/6);
  insist(Math.abs(constraint)<1e-10,"Friedmann constraint");
  return {hubble,comoving,luminosity:(1+zEnd)*comoving,constraint};
}
function jerk(coupling,reference){
  const fixture=coupling.background;
  const test=integrate(fixture,0,"mass",.1,160);
  insist(reference.z===.1 && Math.abs(test.hubble/reference.E-1)<1e-6 &&
    Math.abs(test.comoving/reference.dimensionless_comoving_integral-1)<1e-6,"5193 regression");
  const checks=[];
  for(const ell of [0,1]) for(const item of coupling.limits[ell]) for(const sign of [-1,1]){
    const charge=sign*item.strongest.dimensionlessMassSensitivityFloor;
    const expected=1.5*fixture.fraction*fixture.omegaMatter*fixture.speed/fixture.hubble*charge;
    for(const law of ["mass","massSquared"]) {
      const rows=[.004,.002,.001].map(scale=>{
        const changes=[-scale,scale].map(z=>{
          const baseline=integrate(fixture,0,law,z,32),model=integrate(fixture,charge,law,z,32);
          return [model.hubble-baseline.hubble,model.luminosity-baseline.luminosity];
        });
        const viaH=(changes[1][0]+changes[0][0])/scale**2;
        const viaDistance=-3*(changes[1][1]-changes[0][1])/scale**3;
        return {scale,viaH,viaDistance};
      });
      insist(Math.abs(rows[2].viaH/expected-1)<.001 && Math.abs(rows[2].viaDistance/expected-1)<.001,"jerk or distance coefficient");
      checks.push({ell,exteriorCapFactor:item.cap,sign,law,expectedDeltaJerk:expected,rows});
    }
  }
  return {reference,baselineAtZPointOne:test,checks,scope:"Instantaneous matched-state comparison of cold number-conserving heavy matter with unchanged scalar potential and fixed local metric. The two mass laws only verify the local jet; neither is claimed as the parent continuation."};
}
module.exports={jerk};
if(require.main===module){
  const fs=require("node:fs"),path=require("node:path"),dir=__dirname;
  const read=name=>JSON.parse(fs.readFileSync(path.join(dir,name),"utf8"));
  const reference=read("../cosmology-lab-handoff-20261020/reference-cases.json").cases.find(obj=>obj.model==="ParentScalar_Lambda_zero").predictions.find(row=>row.z===.1);
  process.stdout.write(JSON.stringify(jerk(read("coupling-result.json"),reference),null,2)+"\n");
}
