"use strict";

function tidal(data) {
  const kpc = 3.0856775814913673e19, hbarEV = 6.582119569509067e-16;
  const freqHz = data.massEV / (Math.PI * hbarEV);
  const rows = data.profiles.map(row => {
    const meanTrace = 3 * row.outerDeficit * 1e6 / (row.outerRadius * kpc) ** 2;
    if (!(meanTrace > 0)) throw Error("missing positive aperture mass");
    return {galaxy: row.name, meanHeavyApertureTracePerSecond2: meanTrace, coherentAmplitudeCeilingPerSecond2: 3 * meanTrace};
  });
  const values = rows.map(row => row.coherentAmplitudeCeilingPerSecond2).sort((left, right) => left-right);
  const checks = [];
  const state = phases => {
    const real = phases.reduce((sum, phase) => sum + Math.cos(2 * phase), 0) / phases.length;
    const imag = phases.reduce((sum, phase) => sum + Math.sin(2 * phase), 0) / phases.length;
    return Math.hypot(real, imag);
  };
  for (const [name, phases, expected] of [["standing", [.37], 1], ["phase-balanced", [.37,.37 + Math.PI / 2], 0]]) {
    const amplitude = state(phases);
    const sample = Array.from({length:128}, (_, index) => {
      const time = 2 * Math.PI * index / 128;
      return phases.reduce((sum, phase) => sum + 2 * Math.sin(time + phase) ** 2 -
        Math.cos(time + phase) ** 2, 0) / phases.length * 2;
    });
    const mean = sample.reduce((sum, item) => sum + item / sample.length, 0);
    const fourier = [Math.cos, Math.sin].map(fn => 2 * sample.reduce((sum, item, index) =>
      sum + (item - mean) * fn(4 * Math.PI * index / sample.length) / sample.length, 0));
    const traceAmplitude = Math.hypot(...fourier);
    if (Math.abs(mean - 1) > 1e-12 || Math.abs(amplitude - expected) > 1e-12 ||
        Math.abs(traceAmplitude - 3 * amplitude) > 1e-12) throw Error("stress trace control");
    checks.push({name, coherence: amplitude, meanTrace: mean, traceAmplitude});
  }
  return {freqHz, periodJulianYears: 1 / (freqHz * 365.25 * 86400), checks, rows,
    coherentApertureCeiling: {min:values[0],median:(values[25]+values[26])/2,max:values.at(-1)},
    scope:"Time-dependent heavy Ricci source, volume averaged inside the calibration radius; not a local or line-of-sight clock measurement."};
}
module.exports = {tidal};
if (require.main === module) {
  const data = JSON.parse(require("node:fs").readFileSync(0, "utf8").replace(/^\uFEFF/, ""));
  process.stdout.write(JSON.stringify(tidal(data), null, 2) + "\n");
}
