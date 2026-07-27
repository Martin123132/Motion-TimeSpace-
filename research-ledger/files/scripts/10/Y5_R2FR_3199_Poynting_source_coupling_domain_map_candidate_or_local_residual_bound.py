from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3199-Y5-R2FR-Poynting-source-coupling-domain-map-candidate-or-local-residual-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3199_INPUTS.csv"
CANDIDATE = OUT / "P8_Y5_R2FR_3199_STRESS_FLUX_DOMAIN_CANDIDATE.csv"
POYNTING = OUT / "P8_Y5_R2FR_3199_POYNTING_MAXWELL_DESCENT_AUDIT.csv"
RANK_GATE = OUT / "P8_Y5_R2FR_3199_RANK_POSITIVITY_AND_COUPLING_GATE.csv"
BOUND_SCHEMA = OUT / "P8_Y5_R2FR_3199_LOCAL_RESIDUAL_BOUND_SCHEMA.csv"
DECISION = OUT / "P8_Y5_R2FR_3199_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3199_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "formalization":
        return FW / relative_path
    if location == "post_checkpoint":
        return ROOT / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lower_terms = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lower_terms):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def b(value: bool) -> str:
    return "true" if value else "false"


SOURCES = [
    {
        "input_id": "SRC3199_00",
        "location": "post_checkpoint",
        "relative_path": "3198-Y5-R2FR-parent-domain-map-extraction-or-local-closure-demotion-under-AX1090.md",
        "role": "3198 stress-flux/Poynting next-route seed",
        "terms": ["stress-flux", "Poynting", "C^nu", "NO_PARENT_DOMAIN_TRIPLE"],
    },
    {
        "input_id": "SRC3199_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3198_CONSTRUCTIVE_SEED_LEDGER.csv",
        "role": "machine-readable 3198 constructive seeds",
        "terms": ["Poynting", "C^nu", "tau_em"],
    },
    {
        "input_id": "SRC3199_02",
        "location": "formalization",
        "relative_path": "15-conservation-to-effective-gamma.md",
        "role": "total stress-energy and exchange-current framework",
        "terms": ["∇_μ(T_matter", "Q^ν", "T_MTS", "T_flux"],
    },
    {
        "input_id": "SRC3199_03",
        "location": "formalization",
        "relative_path": "18-sign-conventions-and-field-postulates.md",
        "role": "stress-energy sign and conservation convention",
        "terms": ["Stress-Energy", "∇_μ", "Q^ν", "T_MTS"],
    },
    {
        "input_id": "SRC3199_04",
        "location": "formalization",
        "relative_path": "19-proof-obligations.md",
        "role": "GR and Maxwell proof obligations",
        "terms": ["T_MTS", "Maxwell", "Gauge field", "conserved current"],
    },
    {
        "input_id": "SRC3199_05",
        "location": "formalization",
        "relative_path": "29-em-maxwell-gate-audit.md",
        "role": "EM/Maxwell gate and Poynting/stress status",
        "terms": ["Maxwell recovery", "Poynting", "EM stress-energy", "radiation pressure"],
    },
    {
        "input_id": "SRC3199_06",
        "location": "formalization",
        "relative_path": "75-projected-source-laws.md",
        "role": "conditional source projection and boundary source law",
        "terms": ["conditional_not_parent_derived", "source-support", "K_perp", "boundary"],
    },
    {
        "input_id": "SRC3199_07",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "parent source tensor and sector routing gates",
        "terms": ["source tensor", "K_hat", "flux", "not parent-derived"],
    },
    {
        "input_id": "SRC3199_08",
        "location": "post_checkpoint",
        "relative_path": "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
        "role": "observed reduced boundary/source/projector flux decomposition",
        "terms": ["B_obs", "source_measure", "projector", "no-flux"],
    },
    {
        "input_id": "SRC3199_09",
        "location": "post_checkpoint",
        "relative_path": "1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
        "role": "fallback observed-boundary-flux component schema",
        "terms": ["B_obs", "boundary", "source_measure", "M_H_ref"],
    },
    {
        "input_id": "SRC3199_10",
        "location": "post_checkpoint",
        "relative_path": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
        "role": "parent-owner failure and Bobs source acquisition pivot",
        "terms": ["parent-owner", "Bobs", "source", "flux"],
    },
]


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        rows.append(
            {
                "input_id": source["input_id"],
                "source_path": rel(path),
                "exists": b(path.exists()),
                "role": source["role"],
                "evidence": evidence(path, source["terms"]),
                "generated_utc": now,
            }
        )
    return rows


def candidate_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "candidate_id": "SFD3199_00",
            "object": "stress_flux_domain_map",
            "candidate_equation": "C^nu = n_mu(T_MTS^{mu nu} - tau_m T_matter^{mu nu} - tau_EM T_EM^{mu nu})|_layer",
            "derivation_status": "FORMALLY_ADMISSIBLE_NOT_PARENT_SIGNED",
            "reason": "a diffeomorphism-invariant parent action would naturally generate normal stress-flux matching, but current MTS has no parent-owned tau_m/tau_EM or complete T_MTS/T_EM descent",
            "owns_C_phi": "candidate_only",
            "owns_J": "no",
            "owns_G_N": "no",
            "rank_claim": "no",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SFD3199_01",
            "object": "Poynting_component",
            "candidate_equation": "T_EM^{0i} = S^i/c in SI conventions, or T_EM^{0i}=S^i in c=1 units, with S = E x H",
            "derivation_status": "STANDARD_MAXWELL_IF_MAXWELL_GATE_PASSED",
            "reason": "Poynting is the correct energy-flux/momentum-density object inside Maxwell stress-energy; it is not a substitute for deriving Maxwell/gauge/current structure",
            "owns_C_phi": "helper_only",
            "owns_J": "no",
            "owns_G_N": "no",
            "rank_claim": "no",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SFD3199_02",
            "object": "local_static_limit",
            "candidate_equation": "C^nu_static = n_mu(T_MTS^{mu nu} - tau_m T_matter^{mu nu}) + O(S_EM/c)",
            "derivation_status": "BOUND_ROUTE_NOT_DERIVATION",
            "reason": "quiet local vacuum/solar-system tests require EM flux/Poynting residuals to be zero or bounded; a large unsuppressed Poynting source would damage local GR safety",
            "owns_C_phi": "closure_bound",
            "owns_J": "no",
            "owns_G_N": "no",
            "rank_claim": "no",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def poynting_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "PMG3199_00",
            "gate": "gauge_or_equivalent_A_mu",
            "required_for": "Maxwell stress-energy and Poynting identification",
            "current_status": "open",
            "source_path": "formalization-workbench/29-em-maxwell-gate-audit.md",
            "evidence": "current EM audit says no gauge field or equivalent object is introduced",
            "effect_on_3199": "Poynting may be used as a target structure, not a derived MTS object",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "PMG3199_01",
            "gate": "homogeneous_Maxwell_or_geometric_Bianchi",
            "required_for": "F=dA or equivalent two-form flux conservation",
            "current_status": "open",
            "source_path": "formalization-workbench/19-proof-obligations.md",
            "evidence": "Maxwell proof obligations require homogeneous Maxwell equations or a geometric equivalent",
            "effect_on_3199": "without this, EM flux can only be a phenomenological/pre-Maxwell residual channel",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "PMG3199_02",
            "gate": "conserved_current_and_charge",
            "required_for": "source coupling tau_EM and Coulomb/radiation-pressure consistency",
            "current_status": "open",
            "source_path": "formalization-workbench/29-em-maxwell-gate-audit.md",
            "evidence": "audit lists Coulomb force and radiation pressure as failed/open for classical EM",
            "effect_on_3199": "tau_EM cannot be claimed parent-owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "PMG3199_03",
            "gate": "standard_or_parent_derived_T_EM",
            "required_for": "normal flux C^nu_EM = n_mu T_EM^{mu nu}",
            "current_status": "partial_open",
            "source_path": "formalization-workbench/29-em-maxwell-gate-audit.md",
            "evidence": "energy diagnostics exist but are not yet Maxwell T_EM",
            "effect_on_3199": "can define a source-ready bound row, not a Maxwell derivation claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def rank_gate_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "RPG3199_00",
            "object": "C^nu normal stress-flux map",
            "needed_statement": "C^nu is obtained by varying a parent action with an interface/layer domain, not imposed as an external junction rule",
            "current_status": "unproven",
            "failure_mode": "if imposed by hand, 3199 collapses back to 3198 closure",
            "next_action": "derive boundary term from parent variational principle",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "RPG3199_01",
            "object": "J_Aa = partial C_A / partial z^a",
            "needed_statement": "rank(J)=4 for z=(Delta F_L, Delta F'_L, Delta F_R, Delta F'_R)",
            "current_status": "unproven",
            "failure_mode": "static/spherically symmetric flux generally supplies too few independent channels; Poynting is zero in quiet electrostatic/no-radiation limits",
            "next_action": "extract or source four independent response coefficients from parent stress/source equations",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "RPG3199_02",
            "object": "G_flux positive norm",
            "needed_statement": "positive normal metric on flux codomain comes from parent hyperbolic energy or observer-split positive energy norm",
            "current_status": "unproven",
            "failure_mode": "raw Lorentzian stress-flux contractions are not automatically positive definite",
            "next_action": "derive an observer-frame positive energy norm or domain Hessian",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "RPG3199_03",
            "object": "tau_m and tau_EM",
            "needed_statement": "source coupling coefficients are fixed by parent normalization/units rather than tuned owner couplings",
            "current_status": "unproven",
            "failure_mode": "fitted couplings repeat the transition-owner failure recorded in 95",
            "next_action": "tie tau coefficients to stress tensor normalization, Newton G, charge/current normalization, or mark as nuisance bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "component_id": "BR3199_00",
            "residual_component": "B_obs_EM_Poynting_over_MH",
            "definition": "abs(P_loc n_mu tau_EM T_EM^{mu nu})/M_H_ref",
            "needed_columns": "system_id;surface_id;E_field;B_or_H_field;Poynting_flux;normal_projection;tau_EM;M_H_ref;units;source_path;valid_for_claim",
            "claim_gate": "all numeric/source-backed, tau_EM parent-owned or explicit nuisance, no MISSING markers",
            "current_status": "schema_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "BR3199_01",
            "residual_component": "B_obs_matter_source_flux_over_MH",
            "definition": "abs(P_loc n_mu tau_m T_matter^{mu nu})/M_H_ref",
            "needed_columns": "system_id;surface_id;density;pressure;velocity_flux;normal_projection;tau_m;M_H_ref;units;source_path;valid_for_claim",
            "claim_gate": "source-backed matter flux or theorem-zero source silence",
            "current_status": "schema_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "BR3199_02",
            "residual_component": "B_obs_MTS_stress_flux_over_MH",
            "definition": "abs(P_loc n_mu T_MTS^{mu nu})/M_H_ref",
            "needed_columns": "system_id;surface_id;T_MTS_component;normal_projection;parent_field_values;M_H_ref;units;source_path;valid_for_claim",
            "claim_gate": "T_MTS derived from parent action or finite source-backed component row",
            "current_status": "schema_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "BR3199_03",
            "residual_component": "B_obs_total_flux_no_cancellation_over_MH",
            "definition": "sum of BR3199_00..BR3199_02 absolute components with no cancellation credit",
            "needed_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "claim_gate": "each component zero/bounded with positive M_H_ref and compatible units",
            "current_status": "schema_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3199_00",
            "result": "STRESS_FLUX_DOMAIN_MAP_CANDIDATE_BUILT_NOT_CLOSED",
            "claim_status": "NO_LOCAL_GR_MAXWELL_OR_PPN_CLAIM",
            "decision": "Poynting/source flux is a legitimate candidate ingredient only through stress-energy; current corpus lacks Maxwell descent, parent-owned couplings, positive flux metric, and rank-four Jacobian",
            "best_next_route": "derive or source the four response coefficients J_Aa for C^nu, starting with whether quiet local Poynting flux is theorem-zero or finite-bounded",
            "next_target": "3200-Y5-R2FR-stress-flux-rank-coefficient-extractor-or-Poynting-residual-bound-runner-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    candidates: list[dict[str, object]],
    poynting: list[dict[str, object]],
    rank_gates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, CANDIDATE, POYNTING, RANK_GATE, BOUND_SCHEMA, DECISION]
    return [
        {
            "check_id": "VAL3199_00_inputs_exist",
            "check": "all cited sources exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3199_01_candidate_equation_recorded",
            "check": "stress-flux C^nu candidate is recorded",
            "pass": b(any("C^nu" in row["candidate_equation"] and "T_EM" in row["candidate_equation"] for row in candidates)),
            "detail": "C^nu normal stress-flux map present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3199_02_poynting_not_overclaimed",
            "check": "Poynting route remains blocked by Maxwell/descent gates",
            "pass": b(all(row["valid_for_claim"] == "false" for row in poynting)),
            "detail": ";".join(f"{row['gate_id']}={row['current_status']}" for row in poynting),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3199_03_rank_and_positive_metric_unproven",
            "check": "rank-four and positive-metric gates are not claimed",
            "pass": b(all(row["current_status"] == "unproven" and row["valid_for_claim"] == "false" for row in rank_gates)),
            "detail": "rank(J), positive G_flux, parent variation, and tau ownership remain open",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3199_04_residual_schema_has_poynting_component",
            "check": "local residual fallback includes EM/Poynting flux row",
            "pass": b(any(row["residual_component"] == "B_obs_EM_Poynting_over_MH" for row in bounds)),
            "detail": "Poynting bound schema staged without numeric claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3199_05_no_claim_leak",
            "check": "all generated rows remain valid_for_claim=false",
            "pass": b(
                all(row.get("valid_for_claim") == "false" for table in [candidates, poynting, rank_gates, bounds, decisions] for row in table)
            ),
            "detail": "no local-GR, Maxwell, PPN, or coupling claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3199_06_decision_names_extractor",
            "check": "decision names coefficient extractor/bound runner as next target",
            "pass": b("rank-coefficient" in decisions[0]["next_target"] and decisions[0]["claim_status"] == "NO_LOCAL_GR_MAXWELL_OR_PPN_CLAIM"),
            "detail": decisions[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3199_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    candidates: list[dict[str, object]],
    poynting: list[dict[str, object]],
    rank_gates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3199 - Poynting Source Coupling Domain Map Candidate Or Local Residual Bound Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, Maxwell derivation, EM unification claim, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3199 takes the constructive route rather than only circling missing inputs.",
        "",
        "The candidate parent-domain map is:",
        "",
        "```text",
        "C^nu = n_mu(T_MTS^{mu nu} - tau_m T_matter^{mu nu} - tau_EM T_EM^{mu nu})|_layer.",
        "```",
        "",
        "This is the right shape because parent-owned local gluing should be a normal stress-flux balance. In that language the Poynting vector is not decorative: it is the EM energy-flux/momentum-density part of `T_EM^{mu nu}`.",
        "",
        "Tiny goblin verdict: useful route, not closed.",
        "",
        "## What This Derives",
        "",
        "If a parent action supplies `T_MTS`, matter/EM descent, source couplings, and the layer variation, then the 3197 stiffness theorem can be fed by a flux map:",
        "",
        "```text",
        "J_Aa = partial C_A / partial z^a,",
        "K0 = J^T G_flux J.",
        "```",
        "",
        "This is a real derivation target, not a vibes target.",
        "",
        "## Why Poynting Helps But Does Not Save The Branch Alone",
        "",
    ]
    for row in poynting:
        lines.append(f"- `{row['gate_id']}`: `{row['current_status']}` - {row['effect_on_3199']}")
    lines.extend(
        [
            "",
            "A large unsuppressed local Poynting flux would hurt the local-GR branch, not rescue it. In quiet/static local tests the EM flux contribution must either theorem-zero or enter the residual-bound ledger.",
            "",
            "## Hard Gates",
            "",
        ]
    )
    for row in rank_gates:
        lines.append(f"- `{row['gate_id']}`: {row['needed_statement']} Status: `{row['current_status']}`.")
    lines.extend(
        [
            "",
            "## Residual Bound Fallback",
            "",
            "If the flux map is not parent-derived, the honest fallback is to bound each absolute component without cancellation credit.",
            "",
        ]
    )
    for row in bounds:
        lines.append(f"- `{row['component_id']}`: `{row['residual_component']}` - {row['definition']}")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"`{decisions[0]['result']}`.",
            "",
            f"Claim status: `{decisions[0]['claim_status']}`.",
            "",
            f"Decision: {decisions[0]['decision']}",
            "",
            f"Best next route: {decisions[0]['best_next_route']}",
            "",
            "Next target:",
            "",
            "```text",
            str(decisions[0]["next_target"]),
            "```",
            "",
            "## Generated Evidence",
            "",
            f"- `{rel(INPUTS)}`",
            f"- `{rel(CANDIDATE)}`",
            f"- `{rel(POYNTING)}`",
            f"- `{rel(RANK_GATE)}`",
            f"- `{rel(BOUND_SCHEMA)}`",
            f"- `{rel(DECISION)}`",
            f"- `{rel(VALIDATION)}`",
            "",
            "## Validation",
            "",
        ]
    )
    for row in validations:
        lines.append(f"- `{row['check_id']}`: `{row['pass']}` - {row['detail']}")
    lines.extend(["", "All generated rows remain `valid_for_claim=false`.", ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = input_rows()
    candidates = candidate_rows()
    poynting = poynting_rows()
    rank_gates = rank_gate_rows()
    bounds = bound_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(CANDIDATE, candidates)
    write_csv(POYNTING, poynting)
    write_csv(RANK_GATE, rank_gates)
    write_csv(BOUND_SCHEMA, bounds)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, candidates, poynting, rank_gates, bounds, decisions)
    write_csv(VALIDATION, validations)
    write_doc(candidates, poynting, rank_gates, bounds, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3199 validation failed: {detail}")
    print(f"3199 generated {DOC}")


if __name__ == "__main__":
    main()
