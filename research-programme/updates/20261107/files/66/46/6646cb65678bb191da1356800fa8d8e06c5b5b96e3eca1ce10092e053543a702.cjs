"use strict";
const fs=require("node:fs"),crypto=require("node:crypto"),path=require("node:path");
const root=__dirname;
const read=name=>JSON.parse(fs.readFileSync(path.join(root,name),"utf8").replace(/^\uFEFF/,""));
const sha=file=>crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const data=JSON.parse(fs.readFileSync(0,"utf8").replace(/^\uFEFF/,""));
const files={}, checks=[];
function verify(label,actual,saved){
  let count=0,maxScaled=0;
  function visit(value,expected){
    if(typeof value!==typeof expected)throw Error(label+" type mismatch");
    if(typeof value==="number"){
      if(!Number.isFinite(value)||!Number.isFinite(expected))throw Error(label+" nonfinite");
      count++;
      const ratio=Math.abs(value-expected)/(1+Math.abs(expected));
      maxScaled=Math.max(maxScaled,ratio);
      if(ratio>2e-8)throw Error(label+" numerical mismatch "+value+" "+expected);
    }else if(value && typeof value==="object"){
      if(!expected||Object.keys(value).sort().join("|")!==Object.keys(expected).sort().join("|"))throw Error(label+" keys");
      for(const key of Object.keys(value))visit(value[key],expected[key]);
    }else if(value!==expected)throw Error(label+" value");
  }
  visit(actual,saved);
  checks.push({label,count,maxScaled});
}
const wave=require("./wave.cjs").run(data.profiles,data.massEV);
wave.inputs=data.inputs;wave.sha256=data.sha256;
wave.code=Object.fromEntries(["wave.cjs","inputs.ps1","PROTOCOL.md"].map(name=>[name,sha(path.join(root,name))]));
verify("standing waves and all 52 calibrated profiles",wave,read("result.json"));
const depth=require("./depth.cjs").depth(data);
verify("escape depths",depth,read("depth-result.json"));
const force=require("./force.cjs").force(data,depth);
verify("exterior and total-mass floors",force,read("force-result.json"));
verify("partial heavy fraction",require("./fraction.cjs").fraction(force),read("fraction-result.json"));
verify("tidal stress",require("./tidal.cjs").tidal(data),read("tidal-result.json"));
verify("Hessian controls",require("./germ.cjs").germ(),read("germ-result.json"));
const fixture=read("coupling-fixture.json");
if(sha(fixture.rollingFile)!==fixture.rollingHash||sha(fixture.growthFile)!==fixture.growthHash)throw Error("fixture sources");
const coupling=require("./coupling.cjs").coupling(force,fixture);
verify("coupled dark force",coupling,read("coupling-result.json"));
verify("local conserved aperture flux",require("./local_flux.cjs").flux(data,coupling),read("local-flux-result.json"));
const refName="../cosmology-lab-handoff-20261020/reference-cases.json";
if(sha(path.join(root,refName))!=="a8aef6c7828f58f31431359c43dbac8f7e565195879630242e3eec22af20928b")throw Error("reference bytes");
const reference=read(refName).cases.find(obj=>obj.model==="ParentScalar_Lambda_zero").predictions.find(row=>row.z===.1);
verify("expansion and distance jerk",require("./jerk.cjs").jerk(coupling,reference),read("jerk-result.json"));
for(const name of fs.readdirSync(root).filter(name=>/\.(ps1|cjs|md|json|py)$/.test(name) &&
  !name.endsWith(".receipt.json") && !name.startsWith("validation"))){
  files[name]=sha(path.join(root,name));
}
process.stdout.write(JSON.stringify({passed:true,checks,files,pid:process.pid,node:process.version})+"\n");
