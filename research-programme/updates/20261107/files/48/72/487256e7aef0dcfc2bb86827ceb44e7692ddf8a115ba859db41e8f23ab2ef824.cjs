"use strict";

const insist = (ok, label) => { if (!ok) throw Error(label); };
function widthDenom(power, corner) {
  const end = Math.min(1, corner);
  const poly = 1 - 2 * power * end / (power + 2) + power * end ** 2 / (power + 4);
  return poly * (corner > 1 ? corner ** (-power / 2) : 1);
}
function necessarySpeed(ell, fraction, ratio, unitSpeed) {
  const power = 2 * ell + 3, uniform = fraction ** (power - 1);
  if (ratio <= uniform) return 0;
  let low = 0, high = 1;
  while (widthDenom(power, high) > uniform / ratio) high *= 2;
  for (let iter = 0; iter < 70; iter++) {
    const mid = (low + high) / 2;
    if (widthDenom(power, mid) > uniform / ratio) low = mid; else high = mid;
  }
  return unitSpeed * Math.sqrt(2 * power * (low + high) / 2);
}
function deficitRange(point) {
  const signed = value => value * Math.abs(value);
  const samples = [.3,.8].flatMap(disk => [.5,1].map(bulge => signed(point[3]) + disk * signed(point[4]) + bulge * signed(point[5])));
  return [Math.max(0, point[1] - 2 * point[2]) ** 2 - Math.max(...samples),
    (point[1] + 2 * point[2]) ** 2 - Math.min(...samples)];
}
function controls() {
  const output = [];
  for (const ell of [0,1]) for (const waveR of [.2,1.4,2.9]) {
    const shape = value => {
      if (value < .001) return 1 - value ** 2 / (2 * (2 * ell + 3));
      return ell ? 3 * (Math.sin(value) - value * Math.cos(value)) / value ** 3 : Math.sin(value)/value;
    };
    const mass = rad => {
      let sum = 0;
      for (let index=0; index<4096; index++) {
        const zone = rad * (index + .5) / 4096;
        sum += zone ** (2 * ell + 2) * shape(waveR * zone) ** 2 * rad / 4096;
      }
      return sum;
    };
    const fraction = .7, ratio = mass(fraction) / (fraction * mass(1));
    const minK = necessarySpeed(ell, fraction, ratio, 1);
    insist(ratio >= fraction ** (2*ell+2) && minK <= waveR + 1e-6, "exact regular Bessel control");
    output.push({ell,waveR,ratio,minK});
  }
  return output;
}
function depth(data) {
  insist(data.profiles.length === 52, "cohort");
  const generousSpeed = 299792.458 * Math.sqrt(2e-5);
  const units = 1.973269804593025e-7 * 299792.458 / (data.massEV * 3.0856775814913673e19);
  const rows = data.profiles.map(row => {
    const points = row.points.filter(point => point[0]>0 && point[1]>0 && point[2]>0);
    const outer = points.find(point => point[0]===row.outerRadius);
    const candidates = points.filter(point => point[0]>=.5*row.outerRadius && point[0]<=.85*row.outerRadius)
      .sort((left,right) => Math.abs(left[0]-.7*row.outerRadius)-Math.abs(right[0]-.7*row.outerRadius) || right[0]-left[0]);
    if (!outer || !candidates.length) return {name:row.name,eligible:false};
    const interior = candidates[0], fraction = interior[0]/row.outerRadius;
    const [innerLo,innerHi] = deficitRange(interior), [outerLo,outerHi] = deficitRange(outer);
    const output = {name:row.name,eligible:true,radiusRatio:fraction,outerRadiusKpc:row.outerRadius,flatSpeedKmS:row.flatSpeed,
      innerRadiusKpc:interior[0],innerSquaredSpeedRange:[innerLo,innerHi],outerSquaredSpeedRange:[outerLo,outerHi]};
    if (!(outerHi>0 && innerHi>=0)) return {...output,reason:"no positive halo acceleration"};
    const min = Math.max(0,innerLo)/outerHi, max = outerLo>0 ? innerHi/outerLo : null;
    output.ratioRange=[min,max];
    if(min>1/fraction) return {...output,reason:"enclosed-mass decreases"};
    output.sectors=[0,1].map(ell => {
      if(max!==null && max<fraction**(2*ell+2)) return {ell,reason:"too steep even for nodeless density"};
      const minKmS = necessarySpeed(ell,fraction,min,units/row.outerRadius);
      return {ell,minKmS,minOverFlat:minKmS/row.flatSpeed,overGenerous:minKmS>generousSpeed};
    });
    return output;
  });
  const summary = [0,1].map(ell => {
    const ok=rows.flatMap(row => row.sectors?.[ell]?.minKmS!==undefined ? [{name:row.name,...row.sectors[ell]}] : []);
    const ordered=[...ok].sort((a,b)=>b.minKmS-a.minKmS);
    return {ell,withBounds:ok.length,sectorFailures:rows.filter(row => row.sectors?.[ell]?.reason).length,
      nonzero:ok.filter(row=>row.minKmS>0).length,aboveTwoFlat:ok.filter(row=>row.minOverFlat>2).length,
      aboveFourFlat:ok.filter(row=>row.minOverFlat>4).length,aboveGenerous:ok.filter(row=>row.overGenerous).length,
      topByKmS:ordered.slice(0,4)};
  });
  return {massEV:data.massEV,generousSpeed,eligible:rows.filter(row=>row.eligible).length,
    generalFailures:rows.filter(row=>row.reason).length,controls:controls(),summary,rows};
}

module.exports = {depth};
if (require.main === module) {
  const data = JSON.parse(require("node:fs").readFileSync(0,"utf8").replace(/^\uFEFF/,""));
  process.stdout.write(JSON.stringify(depth(data), null, 2) + "\n");
}
