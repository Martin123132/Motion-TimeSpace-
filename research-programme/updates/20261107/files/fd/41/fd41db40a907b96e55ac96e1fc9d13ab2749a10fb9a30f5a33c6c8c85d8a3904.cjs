"use strict";

function germ(){
  const cases=[];
  for(const residue of [.02,.4,.98]) for(const field of [-.06,.04,.2]) for(const cubic of [-1.2,1.2]){
    const light=.3, heavy=2, proj=1-residue, alpha=cubic*residue*Math.sqrt(proj)*field/heavy**2;
    const val=-1+Math.sqrt(1+2*alpha);
    const coord=val*heavy**2/(cubic*residue);
    const h=cubic*Math.sqrt(residue)*coord**2/(2*heavy**2);
    const residual=h*heavy**2-cubic*Math.sqrt(residue)*(Math.sqrt(proj)*field-Math.sqrt(residue)*h)**2/2;
    const force=light**2*field+Math.sqrt(proj)*cubic*coord**2/2;
    const curvature=light**2+proj/residue*heavy**2*val/(1+val);
    const pathMetric=1+proj/residue*(val/(1+val))**2;
    const entry=cubic*coord, aa=light**2+proj*entry, off=-Math.sqrt(proj*residue)*entry, bb=heavy**2+residue*entry;
    const check=Math.max(Math.abs(residual),Math.abs(aa-off**2/bb-curvature),
      Math.abs((aa-light**2)*(bb-light**2)-off**2-proj*(heavy**2-light**2)*entry),
      Math.abs(1+(off/bb)**2-pathMetric));
    if(check>1e-11)throw Error("trough/Hessian mismatch");
    cases.push({residue,field,cubic,force,curvature,pathMetric,check});
  }
  return {cases,scope:"Dimensionless algebra controls. These are not MTS coefficient estimates."};
}
module.exports={germ};
if(require.main===module)process.stdout.write(JSON.stringify(germ(),null,2)+"\n");
