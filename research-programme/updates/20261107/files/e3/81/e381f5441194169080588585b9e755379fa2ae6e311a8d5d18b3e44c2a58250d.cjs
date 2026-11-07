"use strict";

const requireCondition = (ok, name) => { if (!ok) throw Error(name); };
const total = values => values.reduce((left, right) => left + right, 0);
const median = values => {
  if (!values.length) return null;
  const sorted = [...values].sort((left, right) => left - right);
  return (sorted[(sorted.length - 1) >> 1] + sorted[sorted.length >> 1]) / 2;
};

function solve(ell, box, step) {
  const count = Math.round(box / step) - 1;
  const make = fn => Float64Array.from({length: count}, (_, index) => fn(index));
  const radius = make(index => (index + 1) * step);
  const kinetic = 1 / step ** 2, off = -kinetic / 2;
  const centrifugal = make(index => ell * (ell + 1) / (2 * radius[index] ** 2));
  let phi = make(index => -1 / Math.hypot(ell ? 8 : 3, radius[index]));
  function ground(diagonal) {
    function negativeCount(energy) {
      let neg = 0, pivot = 0;
      for (let index = 0; index < count; index++) {
        pivot = diagonal[index] - energy - (index ? off ** 2 / pivot : 0);
        if (Math.abs(pivot) < 1e-18) pivot = -1e-18;
        neg += pivot < 0;
      }
      return neg;
    }
    let low = Math.min(...phi) - 1, high = 0;
    requireCondition(negativeCount(high) > 0 && !negativeCount(low), "unbracketed bound state");
    for (let iter = 0; iter < 44; iter++) {
      const mid = (low + high) / 2;
      if (negativeCount(mid)) high = mid; else low = mid;
    }
    const energy = (low + high) / 2, shift = low - 1e-8;
    let wave = make(index => radius[index] ** (ell + 1) * Math.exp(-radius[index] / (ell ? 7 : 3)));
    const pivot = make(() => 0);
    for (let iter = 0; iter < 2; iter++) {
      for (let index = 0; index < count; index++) {
        const ratio = index ? off / pivot[index - 1] : 0;
        pivot[index] = diagonal[index] - shift - ratio * off;
        wave[index] -= index ? ratio * wave[index - 1] : 0;
      }
      for (let index = count - 1; index >= 0; index--) {
        wave[index] = (wave[index] - (index + 1 < count ? off * wave[index + 1] : 0)) / pivot[index];
      }
      const norm = Math.sqrt(total(wave.map(value => value * value)) * step);
      wave = wave.map(value => value / norm);
    }
    return {wave, energy};
  }
  for (let iter = 1; iter <= 380; iter++) {
    const diagonal = make(index => kinetic + centrifugal[index] + phi[index]);
    const {wave, energy} = ground(diagonal);
    const shell = wave.map(value => value ** 2 * step);
    const enclosed = make(() => 0), potential = make(() => 0);
    let interior = 0, outerPotential = 0;
    for (let index = 0; index < count; index++) {
      enclosed[index] = interior + shell[index] / 2;
      interior += shell[index];
      potential[index] = -interior / radius[index];
    }
    for (let index = count - 1; index >= 0; index--) {
      potential[index] -= outerPotential;
      outerPotential += shell[index] / radius[index];
    }
    const mismatch = Math.max(...phi.map((value, index) => Math.abs(value - potential[index])));
    if (mismatch > 2e-11) {
      phi = phi.map((value, index) => .45 * value + .55 * potential[index]);
      continue;
    }
    const cumulative = distance => {
      if (distance <= step) return enclosed[0] * Math.max(0, distance / step) ** (2 * ell + 3);
      if (distance >= box) return 1;
      const left = Math.min(count - 1, Math.floor(distance / step) - 1);
      const fraction = distance / step - left - 1;
      return enclosed[left] + fraction * ((left + 1 < count ? enclosed[left + 1] : 1) - enclosed[left]);
    };
    const halfMass = bisect(0, box, value => cumulative(value) - .5);
    const gradient = make(index => (wave[index] - (index ? wave[index - 1] : 0)) / step);
    const kineticEnergy = step * total(gradient.map(value => value ** 2 / 2)) +
      wave[count - 1] ** 2 / (2 * step) + total(shell.map((value, index) => value * centrifugal[index]));
    const gravEnergy = total(shell.map((value, index) => .5 * value * potential[index]));
    const virial = (2 * kineticEnergy + gravEnergy) / Math.abs(gravEnergy);
    const eigError = Math.sqrt(step * total(wave.map((value, index) =>
      ((kinetic + centrifugal[index] + potential[index] - energy) * value +
       off * ((index ? wave[index - 1] : 0) + (index + 1 < count ? wave[index + 1] : 0))) ** 2)));
    const anisot = make(index => {
      const rad = radius[index], angular = ell * (ell + 1);
      const prev = index ? wave[index - 1] : 0;
      const next = index + 1 < count ? wave[index + 1] : 0;
      const radialGrad = ((next - prev) / (2 * step) - wave[index] / rad) / rad;
      return (radialGrad ** 2 - angular * (wave[index] / rad ** 2) ** 2 / 2) / (4 * Math.PI);
    });
    const peakIndex = enclosed.reduce((idx, mass, index) => mass / radius[index] > enclosed[idx] / radius[idx] ? index : idx, 0);
    const summary = {ell, box, step, iterations: iter, energy, mass: interior, halfMass, kineticEnergy, gravEnergy,
      virial, eigError, mismatch, peakRadius: radius[peakIndex], peakAngularMomentum: Math.sqrt(radius[peakIndex] * enclosed[peakIndex]),
      gradientStressNearHalfMass: anisot[Math.round(halfMass / step) - 1], maxGradientStress: Math.max(...anisot),
      minGradientStress: Math.min(...anisot), massBeyondHalfBox: 1 - cumulative(box / 2)};
    requireCondition(energy < 0 && Math.abs(interior - 1) < 1e-10 && Math.abs(virial) < .002 && eigError < 1e-7 &&
      Math.min(...wave) > -1e-12 && Math.max(...anisot) > 0, "invalid stationary state: " + JSON.stringify(summary));
    return {summary, cumulative};
  }
  throw Error("Poisson self-consistency did not converge");
}

function bisect(low, high, func) {
  requireCondition(func(low) <= 0 && func(high) >= 0, "root outside bracket");
  for (let index = 0; index < 67; index++) {
    const mid = (high + low) / 2;
    if (func(mid) > 0) high = mid; else low = mid;
  }
  return (low + high) / 2;
}

function run(profiles, massEV) {
  requireCondition(profiles.length === 52 && new Set(profiles.map(row => row.name)).size === 52, "frozen galaxy cohort changed");
  const modes = [0, 1].map(ell => [[80,.05], [80,.025], [120,.025]].map(([box, step]) => solve(ell, box, step)));
  for (const states of modes) for (const index of [0, 1]) for (const field of ["energy", "halfMass"]) {
    const ratio = states[index].summary[field] / states[index + 1].summary[field];
    requireCondition(Math.abs(ratio - 1) < .002, "resolution/box sensitivity: " + field);
  }
  const inverseLengthSpeed = massEV * 3.0856775814913673e19 * 1000 / (1.973269804593025e-7 * 299792458);
  const rows = [], shells = ["outerHalf", "innerHalf"];
  const quantities = ["baryon", "constant", "wave0", "wave1"];
  const stats = {};
  for (const {name, outerRadius, outerDeficit, flatSpeed, points} of profiles) {
    const valid = points.filter(row => row[0] > 0 && row[1] > 0 && row[2] > 0);
    const end = valid.reduce((left, right) => left[0] > right[0] ? left : right);
    const baryon = row => row[3] * Math.abs(row[3]) + .5 * row[4] * Math.abs(row[4]) + .7 * row[5] * Math.abs(row[5]);
    const deficit = end[1] ** 2 - baryon(end);
    requireCondition(end[0] === outerRadius && deficit > 0 && Math.abs(outerDeficit - deficit) < 1e-7 &&
      valid.filter(row => row[0] === outerRadius).length === 1, "outer join " + name);
    const eta = inverseLengthSpeed * outerRadius * Math.sqrt(deficit), eta2 = eta ** 2;
    const scales = modes.map(states => {
      const state = states[2], x = bisect(0, 2 * Math.max(120, eta2), value => value * state.cumulative(value) - eta2);
      requireCondition(Math.abs(x * state.cumulative(x) / eta2 - 1) < 1e-10, "outer calibration " + name);
      return {x, mass: state.cumulative(x), state};
    });
    const byShell = Object.fromEntries(shells.map(key => [key, []]));
    for (const point of valid.filter(row => row[0] < outerRadius)) {
      const radiusFraction = point[0] / outerRadius, base = baryon(point);
      const halo = scales.map(({x, mass, state}) => deficit * state.cumulative(x * radiusFraction) / (radiusFraction * mass));
      const residuals = [base, base + deficit, base + halo[0], base + halo[1]].map(value => (value - point[1] ** 2) / end[1] ** 2);
      byShell[radiusFraction >= .5 ? "outerHalf" : "innerHalf"].push(residuals);
    }
    const galaxy = {name, etaFromOuterDeficit: eta, etaFromCatalogueFlatSpeed: inverseLengthSpeed * outerRadius * flatSpeed,
      xAtOuter: scales.map(state => state.x)};
    for (const key of shells) {
      const sample = byShell[key];
      galaxy[key] = {count: sample.length, abs: quantities.map((_, index) => median(sample.map(row => Math.abs(row[index])))),
        signed: quantities.map((_, index) => median(sample.map(row => row[index])))};
    }
    rows.push(galaxy);
  }
  for (const key of shells) {
    const valid = rows.filter(row => row[key].count);
    stats[key] = {galaxies: valid.length, radii: total(valid.map(row => row[key].count)),
      medianAbs: Object.fromEntries(quantities.map((label, index) => [label, median(valid.map(row => row[key].abs[index]))])),
      medianSigned: Object.fromEntries(quantities.map((label, index) => [label, median(valid.map(row => row[key].signed[index]))])),
      betterThanConstant: Object.fromEntries([2,3].map(index => [quantities[index],valid.filter(row => row[key].abs[index] < row[key].abs[1]).length]))};
  }
  const etas = rows.map(row => row.etaFromOuterDeficit);
  return {massEV, states: modes.map(states => states.map(state => state.summary)), stats,
    eta: {min: Math.min(...etas), median: median(etas), max: Math.max(...etas), belowOne: etas.filter(value => value < 1).length,
      atLeastTen: etas.filter(value => value >= 10).length}, rows};
}

module.exports = {run};
