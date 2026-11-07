"use strict";

const check = (test,message) => {if(!test)throw Error(message);};
function ratio(ell,fraction,alpha,beta,steps) {
  const scale=Math.max(1,2*alpha,Math.sqrt(beta)), power=2*ell+2;
  const rate=2*alpha/scale, square=beta/scale**2;
  function integral(begin,end) {
    const start=Math.min(scale*begin,64), width=(Math.min(scale*end,64)-start)/steps;
    let sum=0;
    for(let index=0;index<=steps;index++){
      const x=start+index*width;
      sum+=(index===0||index===steps?1:index%2?4:2)*x**power*Math.exp(-rate*x-square*x*x);
    }
    return sum*width/3;
  }
  const interior=integral(0,fraction);
  return interior/(interior+integral(fraction,1))/fraction;
}
function floorFor(fn,target) {
  if(fn(0)>=target)return 0;
  let low=0,high=1;
  while(fn(high)<target && high<2**40)high*=2;
  check(fn(high)>=target,"finite comparison root not bracketed");
  for(let iter=0;iter<54;iter++){
    const mid=(low+high)/2;
    if(fn(mid)<target)low=mid;else high=mid;
  }
  return (high+low)/2;
}
function references(){
  const fraction=.7, positive=.8, checks=[];
  const expMass=(radius,rate,power)=>{
    const arg=radius*rate;
    let term=1,sum=1;
    for(let index=1;index<=power;index++){term*=arg/index;sum+=term;}
    return 1-Math.exp(-arg)*sum;
  };
  const gaussMass=(radius,beta,power)=>{
    let sum=0,term=1;
    for(let index=0;index<35;index++){sum+=term/(power+2*index+1);term*=-beta*radius**2/(index+1);}
    return radius**(power+1)*sum;
  };
  for(const ell of [0,1]){
    const power=2*ell+2;
    for(const [name,alpha,beta,ref] of [
      ["uniform",0,0,fraction**power],
      ["Coulomb",positive,0,expMass(fraction,2*positive,power)/expMass(1,2*positive,power)/fraction],
      ["oscillator",0,positive,gaussMass(fraction,positive,power)/gaussMass(1,positive,power)/fraction]
    ]){
      const difference=Math.abs(ratio(ell,fraction,alpha,beta,512)-ref);
      check(difference<1e-8,"quadrature reference "+name);
      checks.push({ell,name,difference});
    }
  }
  return checks;
}
function force(data,depth) {
  const units=1.973269804593025e-7*299792.458/(data.massEV*3.0856775814913673e19), grav=4.30091727e-6;
  check(depth.massEV===data.massEV && depth.eligible===51 && data.profiles.length===52,"depth input");
  const checks=references(), rows=[];
  for(const entry of depth.rows){
    if(!entry.eligible || entry.reason)continue;
    const profile=data.profiles.find(row=>row.name===entry.name);
    const outer=profile.points.find(point=>point[0]===entry.outerRadiusKpc);
    const speedHigh=outer[1]+2*outer[2], radius=outer[0], fraction=entry.radiusRatio, target=entry.ratioRange[0];
    check(target<1/fraction && target>=0,"enclosed mass");
    const sectors=[0,1].map(ell=>{
      const alphaMeasured=(radius*speedHigh/units)**2/(ell+1);
      const both=[256,512].map(steps=>({
        beta:floorFor(beta=>ratio(ell,fraction,alphaMeasured,beta,steps),target),
        alpha:floorFor(alpha=>ratio(ell,fraction,alpha,0,steps),target)
      }));
      for(const key of ["alpha","beta"]){
        check(Math.abs(both[0][key]-both[1][key])<=2e-4*Math.max(1e-12,both[1][key]),"resolution: "+key);
      }
      const exteriorSpeed=both[1].beta*units/radius, mass=(ell+1)*units**2*both[1].alpha/(grav*radius);
      return {ell,outerTotalSpeedUpper:speedHigh,outerTotalSphericalMassUpper:radius*speedHigh**2/grav,
        minExteriorSupKmS:exteriorSpeed,minSupOverFlat:exteriorSpeed/profile.flatSpeed,
        totalGravitatingMassFloorSolar:mass,minTotalOverOuterUpper:both[1].alpha/alphaMeasured,
        deficitRatioCeilingIfTwoFlat:ratio(ell,fraction,alphaMeasured,2*profile.flatSpeed*radius/units,512),
        deficitRatioCeilingIfFourFlat:ratio(ell,fraction,alphaMeasured,4*profile.flatSpeed*radius/units,512)};
    });
    rows.push({name:profile.name,fraction,target,flat:profile.flatSpeed,sectors});
  }
  const summary=[0,1].map(ell=>{
    const cases=rows.map(row=>({name:row.name,...row.sectors[ell]}));
    return {ell,galaxies:cases.length,requireExteriorGt2Flat:cases.filter(row=>row.minSupOverFlat>2).length,
      requireExteriorGt4Flat:cases.filter(row=>row.minSupOverFlat>4).length,
      totalFloorGtOuterUpper:cases.filter(row=>row.minTotalOverOuterUpper>1).length,
      topByExteriorKmS:[...cases].sort((left,right)=>right.minExteriorSupKmS-left.minExteriorSupKmS).slice(0,3)};
  });
  return {massEV:data.massEV,unitsKpcKmS:units,checks,summary,rows};
}
module.exports={force,ratio,floorFor};
if(require.main===module){
  const fs=require("node:fs"),path=require("node:path");
  const data=JSON.parse(fs.readFileSync(0,"utf8").replace(/^\uFEFF/,""));
  const depth=JSON.parse(fs.readFileSync(path.join(__dirname,"depth-result.json"),"utf8"));
  process.stdout.write(JSON.stringify(force(data,depth),null,2)+"\n");
}
