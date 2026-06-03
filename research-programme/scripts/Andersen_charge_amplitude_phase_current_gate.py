from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Andersen-charge-amplitude-phase-current-gate"
CHECKPOINT_DOC = "459B-Andersen-charge-amplitude-phase-current-gate.md"
STATUS = "Andersen_charge_amplitude_phase_current_gate_written_dimensional_hazard_found_phase_current_route_live_no_EM_Newton_or_local_GR_pass"
CLAIM_CEILING = "external_charge_clue_only_no_priority_claim_no_EM_derivation_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "phase-current-charge-conservation-gate or return to 469-fill-or-zero-highest-pressure-mu-extra-row.md"

PAPER_PATH = Path("[external-paper]/emergent-electromagnetism-from-high-frequency-gravitational-relics.pdf")
IMAGE_ONE_PATH = Path("[external-image]/ea326bb9-a1bf-46f3-b47d-19e3942cf197.png")
IMAGE_TWO_PATH = Path("[external-image]/c7f0378f-66d7-4634-9346-d5a96dee749a.png")
EXTRACTED_TEXT_PATH = Path("source-intake/external_andersen_emergent_em_from_kerr_relics_extracted.txt")

SOURCE_REGISTER_PATH = Path("source-intake/external_papers/Andersen_2026_charge_amplitude_SOURCE_REGISTER.csv")
DIMENSIONAL_GATE_PATH = Path("source-intake/external_papers/Andersen_2026_charge_amplitude_DIMENSIONAL_GATE.csv")
PHASE_CURRENT_CONTRACT_PATH = Path("source-intake/external_papers/Andersen_2026_phase_current_CHARGE_CONTRACT.csv")
DECISION_PATH = Path("source-intake/external_papers/Andersen_2026_charge_phase_DECISION.csv")


CONSTANTS = {
    "G": 6.67430e-11,
    "c": 299_792_458.0,
    "e": 1.602176634e-19,
    "epsilon0": 8.8541878128e-12,
    "m_e": 9.1093837139e-31,
    "hbar": 1.054571817e-34,
}


def fmt(value: float) -> str:
    return f"{value:.6e}"


def source_exists(path: Path) -> bool:
    if path.is_absolute():
        return path.exists()
    return (ROOT / path).exists()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns = list(rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_source_register() -> list[dict[str, Any]]:
    sources = [
        {
            "source_file": str(PAPER_PATH),
            "exists": source_exists(PAPER_PATH),
            "role": "primary external paper for HFGW/Kerr relic EM clue audit",
        },
        {
            "source_file": str(IMAGE_ONE_PATH),
            "exists": source_exists(IMAGE_ONE_PATH),
            "role": "public-post screenshot context only; not physics evidence",
        },
        {
            "source_file": str(IMAGE_TWO_PATH),
            "exists": source_exists(IMAGE_TWO_PATH),
            "role": "profile/follow screenshot context only; not physics evidence",
        },
        {
            "source_file": str(EXTRACTED_TEXT_PATH),
            "exists": source_exists(EXTRACTED_TEXT_PATH),
            "role": "private extracted PDF text used for equation intake",
        },
        {
            "source_file": "459A-Andersen-HFGW-EM-charge-relevance-audit.md",
            "exists": source_exists(Path("459A-Andersen-HFGW-EM-charge-relevance-audit.md")),
            "role": "first-pass Andersen charge-sector intake",
        },
        {
            "source_file": "287-boundary-current-charge-owner-attempt.md",
            "exists": source_exists(Path("287-boundary-current-charge-owner-attempt.md")),
            "role": "MTS boundary-current charge-unit obstruction",
        },
        {
            "source_file": "source-intake/mts_residuals/P8_charge_current_equality_STATUS.csv",
            "exists": source_exists(Path("source-intake/mts_residuals/P8_charge_current_equality_STATUS.csv")),
            "role": "current no-promotion status for charge-current equality",
        },
        {
            "source_file": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
            "exists": source_exists(Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv")),
            "role": "PG gate that external EM analogies must not bypass",
        },
    ]
    return sources


def build_dimensional_gate() -> list[dict[str, Any]]:
    G = CONSTANTS["G"]
    c = CONSTANTS["c"]
    e = CONSTANTS["e"]
    epsilon0 = CONSTANTS["epsilon0"]
    m_e = CONSTANTS["m_e"]
    hbar = CONSTANTS["hbar"]

    schwarzschild_radius = 2.0 * G * m_e / c**2
    omega_s = c / schwarzschild_radius
    sigma_rs2 = schwarzschild_radius**2
    kerr_radius = hbar / (2.0 * m_e * c)

    h0_length = math.sqrt(e**2 * 16.0 * G / (epsilon0 * c**2 * omega_s**2 * sigma_rs2))
    strain_at_kerr_radius = h0_length / kerr_radius
    strain_at_one_metre = h0_length
    sigma_needed_for_h_1e_minus_83 = e**2 * 16.0 * G / (epsilon0 * c**2 * omega_s**2 * (1e-83) ** 2)

    return [
        {
            "row_id": "D0_paper_force_formula",
            "quantity": "F = c^2 omega_s^2 h0^2 sigma_abs / (64 pi G d^2)",
            "value": "symbolic",
            "units": "N only if h = h0/r and h0 carries length",
            "gate": "dimensional_condition",
            "result": "conditional_pass_with_length_h0",
            "implication_for_MTS": "any MTS import must declare whether amplitude is a length-normalized envelope or a dimensionless strain at a named radius",
        },
        {
            "row_id": "D1_schwarzschild_radius",
            "quantity": "R_s = 2 G m_e / c^2",
            "value": fmt(schwarzschild_radius),
            "units": "m",
            "gate": "electron_scale_input",
            "result": "computed",
            "implication_for_MTS": "carrier frequency becomes extreme only because the electron gravitational radius is tiny",
        },
        {
            "row_id": "D2_relic_frequency",
            "quantity": "omega_s = c / R_s",
            "value": fmt(omega_s),
            "units": "s^-1",
            "gate": "frequency_input",
            "result": "computed",
            "implication_for_MTS": "frequency must be parent-derived; otherwise charge strength is a scale choice",
        },
        {
            "row_id": "D3_sigma_abs_Rs_squared",
            "quantity": "sigma_abs = R_s^2",
            "value": fmt(sigma_rs2),
            "units": "m^2",
            "gate": "cross_section_assumption",
            "result": "assumption_not_derived",
            "implication_for_MTS": "cross-section is the biggest hidden lever; it cannot be accepted without a source/scattering theorem",
        },
        {
            "row_id": "D4_h0_needed_if_sigma_Rs2",
            "quantity": "h0 solving Coulomb strength with sigma_abs = R_s^2",
            "value": fmt(h0_length),
            "units": "m",
            "gate": "amplitude_solution",
            "result": "length_amplitude_not_dimensionless_strain",
            "implication_for_MTS": "the quoted tiny dimensionless strain is not directly obtained unless an extra radius/reference convention is supplied",
        },
        {
            "row_id": "D5_strain_at_kerr_ring",
            "quantity": "h0 / a where a = hbar/(2 m_e c)",
            "value": fmt(strain_at_kerr_radius),
            "units": "dimensionless",
            "gate": "local_strain_readout",
            "result": "near_LIGO_scale_if_read_at_Kerr_radius",
            "implication_for_MTS": "the amplitude readout is radius-dependent; this is a serious normalization hazard, not a fatal theorem-killer",
        },
        {
            "row_id": "D6_strain_at_one_metre",
            "quantity": "h0 / 1 m",
            "value": fmt(strain_at_one_metre),
            "units": "dimensionless",
            "gate": "macroscopic_strain_readout",
            "result": "tiny_but_not_1e-83",
            "implication_for_MTS": "MTS must state the observer radius or envelope normalization before making amplitude claims",
        },
        {
            "row_id": "D7_cross_section_needed_for_h_1e_minus_83",
            "quantity": "sigma_abs needed if h = 1e-83 is inserted as dimensionless",
            "value": fmt(sigma_needed_for_h_1e_minus_83),
            "units": "m^2",
            "gate": "paper_claim_tension_check",
            "result": "requires_nanometre_scale_effective_cross_section_or_missing_reference_length",
            "implication_for_MTS": "do not inherit the 1e-83 number as a derived MTS fact",
        },
        {
            "row_id": "D8_amplitude_degeneracy",
            "quantity": "e^2 fixes omega_s^2 sigma_abs h0^2 only",
            "value": "one constraint on three physical ingredients",
            "units": "mixed",
            "gate": "noncircularity",
            "result": "open",
            "implication_for_MTS": "the useful route is a parent-derived carrier plus cross-section plus phase current, not a fitted charge product",
        },
    ]


def build_phase_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PC0_parent_phase_variable",
            "candidate_identity": "theta_Q is a compact carrier phase of the motion-time-space state",
            "would_close": "charge sign becomes a phase orientation rather than an inserted +/- label",
            "required_proof": "theta_Q appears in the parent action with a real shift/compact symmetry",
            "current_status": "not_derived",
            "fallback": "phase polarity remains analogy only",
        },
        {
            "contract_id": "PC1_conserved_current",
            "candidate_identity": "nabla_mu J_Q^mu = 0",
            "would_close": "charge conservation",
            "required_proof": "Noether/Ward identity or topological current from the same parent variables",
            "current_status": "not_derived",
            "fallback": "positive/negative charge is renamed, not explained",
        },
        {
            "contract_id": "PC2_quantized_charge_unit",
            "candidate_identity": "Q/e = n or Q/Q_star = n/k",
            "would_close": "electron charge unit and charge discreteness",
            "required_proof": "winding, level, index, or boundary-current theorem fixing the unit",
            "current_status": "open_from_287",
            "fallback": "charge amplitude remains empirical closure",
        },
        {
            "contract_id": "PC3_force_sign_from_stress",
            "candidate_identity": "F_12 derives from averaged cross-term T_eff[h1,h2] with sign fixed by Delta theta",
            "would_close": "attraction and repulsion from one stress/action rule",
            "required_proof": "radiation-pressure and vacuum-depletion signs follow from one covariant stress tensor",
            "current_status": "not_derived",
            "fallback": "relative phase is just a sign convention",
        },
        {
            "contract_id": "PC4_Maxwell_limit",
            "candidate_identity": "coarse-grained carrier equations reduce to Maxwell equations",
            "would_close": "EM field law rather than only Coulomb pair force",
            "required_proof": "Gauss, no-monopole, Faraday, and Ampere-Maxwell equations in one observed frame",
            "current_status": "not_derived",
            "fallback": "paper clue cannot be called electromagnetism",
        },
        {
            "contract_id": "PC5_Lorentz_force_readout",
            "candidate_identity": "matter sees q(E + v x B) from the same observed coframe",
            "would_close": "particle coupling/readout",
            "required_proof": "geodesic/frame-dragging or gauge-coupling derivation with source normalization",
            "current_status": "not_derived",
            "fallback": "magnetism/frame-dragging remains formal analogy",
        },
        {
            "contract_id": "PC6_regular_source",
            "candidate_identity": "carrier source is finite, topological, or otherwise regularized",
            "would_close": "no hidden singular-source cheat",
            "required_proof": "replace or control naked Kerr ring divergences in MTS variables",
            "current_status": "not_derived",
            "fallback": "source model is speculative only",
        },
        {
            "contract_id": "PC7_no_GR_gate_bypass",
            "candidate_identity": "EM/charge branch stays separate from measured-GM PG closure",
            "would_close": "discipline boundary",
            "required_proof": "none; policy gate",
            "current_status": "pass_policy",
            "fallback": "do not use charge clue to promote Newton, PPN, or local GR",
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "Q0_usefulness",
            "status": "useful_clue",
            "meaning": "the paper points at charge as carrier phase/coherence/flux, which is relevant to the MTS charge branch",
            "next_action": "keep Andersen citation if this clue is used",
        },
        {
            "decision_id": "Q1_dimensional_status",
            "status": "hazard_found",
            "meaning": "the charge-amplitude formula needs an explicit amplitude length/reference-radius convention",
            "next_action": "do not import h ~ 1e-83 as a derived fact",
        },
        {
            "decision_id": "Q2_best_MTS_route",
            "status": "phase_current_route",
            "meaning": "turn charge into a conserved compact phase current rather than a primitive U(1) field or a pure fitted amplitude",
            "next_action": "attempt PC0-PC3 before claiming any EM branch",
        },
        {
            "decision_id": "Q3_Maxwell_status",
            "status": "not_derived",
            "meaning": "Coulomb-like inverse-square force is not enough; full Maxwell and Lorentz-force limits remain missing",
            "next_action": "defer EM promotion",
        },
        {
            "decision_id": "Q4_GR_Newton_status",
            "status": "not_closed",
            "meaning": "external EM clue does not close measured-GM, Poisson-Gauss, PPN, or local-GR gates",
            "next_action": "return to 469 alpha3/mu-extra local pressure gate if the main local-GR route remains priority",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def build_doc(timestamp: str, run_dir: Path) -> str:
    source_register = read_csv(SOURCE_REGISTER_PATH)
    dimensional_gate = read_csv(DIMENSIONAL_GATE_PATH)
    phase_contract = read_csv(PHASE_CURRENT_CONTRACT_PATH)
    decision = read_csv(DECISION_PATH)

    return f"""# 459B - Andersen Charge-Amplitude / Phase-Current Gate

Private external-paper charge-sector deepening. This is not a public MTS priority, authorship, plagiarism, EM derivation, measured-GM, Newtonian-limit, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint `459A` answered whether Andersen's HFGW/Kerr relic paper is relevant. It is.

This checkpoint asks the sharper question:

```text
Can the paper help us get charge over the line?
```

Short answer:

```text
It gives a useful route, not a derivation.
```

The useful route is:

```text
charge = conserved compact phase/current of an underlying geometric carrier
```

not:

```text
copy the 1e-83 amplitude or declare Coulomb solved.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Andersen_charge_amplitude_phase_current_gate.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Dimensional gate | `{DIMENSIONAL_GATE_PATH}` |
| Phase-current contract | `{PHASE_CURRENT_CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. What The Paper Gives Us

The paper's best MTS clue is not the Kerr singularity itself. The best clue is the pattern:

```text
high-frequency geometric carrier
-> coarse-grained stress/flux
-> inverse-square envelope
-> sign from relative phase
-> magnetic sector from spin/vorticity/frame-dragging
```

That is very compatible with the post-checkpoint simplification idea:

```text
do not add a mysterious extra charge substance if motion-time-space phase/current can carry the observable.
```

But compatibility is not a theorem.

## 5. Dimensional / Normalization Gate

{markdown_table(dimensional_gate)}

Main red-team result:

```text
The formula can be dimensionally sane only if h0 in h ~ h0/r is treated as a length amplitude,
or if an explicit reference radius is supplied.
```

With the paper-style assumption `sigma_abs = R_s^2`, the Coulomb-strength solution is:

```text
h0 ~= 1.96e-35 m
```

and the strain read at the Kerr ring radius is roughly:

```text
h0/a ~= 1.01e-22.
```

So the quoted `1e-83` amplitude is not something we can import as a clean derived MTS value. It may depend on a different hidden normalization/cross-section convention. That does not kill the clue, but it absolutely blocks promotion.

## 6. MTS Phase-Current Contract

If this clue is useful, the MTS version should look like this:

{markdown_table(phase_contract)}

The key route is:

```text
theta_Q compact phase
J_Q^mu derived current
nabla_mu J_Q^mu = 0
Q/Q_* quantized
force sign from averaged stress cross-term
Maxwell/Lorentz limits after coarse-graining
```

This would be a real field-theory route. Without those steps, it is just a nice analogy wearing boxing gloves.

## 7. Attribution Policy

Use rule:

```text
If MTS uses carrier-flux charge, phase-polarity charge, or frame-dragging magnetism, cite Andersen 2026.
```

Boundary rule:

```text
Do not claim influence, copying, or priority from follows/likes/screenshots.
```

Physics rule:

```text
Only equations, derivations, and tests count inside the audit.
```

## 8. Decision

{markdown_table(decision)}

Plain-English decision:

```text
Yes, this paper can help, but as a route-finder.
It suggests the next MTS charge move should be a phase-current conservation/quantization gate.
It does not close charge, EM, Newton, or local GR by itself.
```

## 9. Claim Ceiling

Allowed:

```text
Andersen 2026 is a useful external speculative parallel for an emergent geometric charge route.
```

Allowed:

```text
The strongest MTS-relevant clue is charge sign as carrier phase plus charge strength as a coarse-grained flux/cross-section law.
```

Forbidden:

```text
MTS derives charge from Andersen's paper.
```

Forbidden:

```text
The 1e-83 amplitude is a verified MTS prediction.
```

Forbidden:

```text
This closes Maxwell, measured-GM, Newton, PPN, or local GR.
```

## 10. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `phase-current-charge-conservation-gate` | Best way to use the Andersen clue without importing speculation |
| 2 | `charge-amplitude-dimensional-ledger` | Needed if we ever use a flux/cross-section law for elementary charge |
| 3 | `469-fill-or-zero-highest-pressure-mu-extra-row.md` | Main local-GR route still needs the alpha3/mu-extra pressure row handled |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    write_csv(SOURCE_REGISTER_PATH, build_source_register())
    write_csv(DIMENSIONAL_GATE_PATH, build_dimensional_gate())
    write_csv(PHASE_CURRENT_CONTRACT_PATH, build_phase_contract())
    write_csv(DECISION_PATH, build_decision())

    for source_path in [SOURCE_REGISTER_PATH, DIMENSIONAL_GATE_PATH, PHASE_CURRENT_CONTRACT_PATH, DECISION_PATH]:
        rows = read_csv(source_path)
        write_csv(Path(results_dir.relative_to(ROOT)) / source_path.name.lower(), rows)

    doc = build_doc(timestamp, run_dir)
    (ROOT / CHECKPOINT_DOC).write_text(doc, encoding="utf-8")

    source_register = read_csv(SOURCE_REGISTER_PATH)
    dimensional_gate = read_csv(DIMENSIONAL_GATE_PATH)
    phase_contract = read_csv(PHASE_CURRENT_CONTRACT_PATH)
    decision = read_csv(DECISION_PATH)

    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "dimensional_gate": str(ROOT / DIMENSIONAL_GATE_PATH),
        "phase_current_contract": str(ROOT / PHASE_CURRENT_CONTRACT_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_register),
        "missing_source_paths": sum(1 for row in source_register if row["exists"].lower() != "true"),
        "dimensional_gate_rows": len(dimensional_gate),
        "phase_contract_rows": len(phase_contract),
        "decision_rows": len(decision),
        "dimensional_hazard_found": True,
        "phase_current_route_live": True,
        "andersen_priority_claim_allowed": False,
        "andersen_theorem_import_allowed": False,
        "EM_branch_promoted": False,
        "measured_GM_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    status = write_run(args.timestamp)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
