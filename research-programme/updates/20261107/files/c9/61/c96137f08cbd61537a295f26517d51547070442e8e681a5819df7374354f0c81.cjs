"use strict";

function fraction(result){
  const table=result.rows.map(row=>{
    const kepler=1/row.fraction;
    const sectors=row.sectors.map(sector=>{
      const bound=(ceiling)=>{
        if(!(row.target<kepler && ceiling<=kepler*(1+1e-10)))throw Error("mass positivity");
        if(ceiling>=row.target)return 1;
        return Math.min(1,Math.max(0,(kepler-row.target)/(kepler-ceiling)));
      };
      return {ell:sector.ell,maxAtTwoFlat:bound(sector.deficitRatioCeilingIfTwoFlat),
        maxAtFourFlat:bound(sector.deficitRatioCeilingIfFourFlat)};
    });
    return {name:row.name,sectors};
  });
  const summary=[0,1].map(ell=>Object.fromEntries(["maxAtTwoFlat","maxAtFourFlat"].map(key=>{
    const bounds=table.map(row=>({name:row.name,value:row.sectors[ell][key]})).sort((a,b)=>a.value-b.value);
    return [key,{belowOne:bounds.filter(item=>item.value<1).length,belowHalf:bounds.filter(item=>item.value<.5).length,strongest:bounds[0]}];
  })));
  return {summary,rows:table,scope:"Upper limits on fraction of the outer residual force, conditional on exterior circular speed cap and a positive spherical remainder. Not a cosmological abundance."};
}
module.exports={fraction};
if(require.main===module){
  const fs=require("node:fs"),path=require("node:path");
  const result=JSON.parse(fs.readFileSync(path.join(__dirname,"force-result.json"),"utf8"));
  process.stdout.write(JSON.stringify(fraction(result),null,2)+"\n");
}
