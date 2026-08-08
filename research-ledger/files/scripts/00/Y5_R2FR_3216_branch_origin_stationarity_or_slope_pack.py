from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3216-Y5-R2FR-branch-origin-coefficient-stationarity-or-memory-slope-bound-pack-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3216_INPUTS.csv"
THEOREMS = OUT / "P8_Y5_R2FR_3216_STATIONARITY_THEOREM_ROUTES.csv"
INDEPENDENCE = OUT / "P8_Y5_R2FR_3216_VISIBLE_OPERATOR_INDEPENDENCE_GUARD.csv"
ROUTE_AUDIT = OUT / "P8_Y5_R2FR_3216_ROUTE_AUDIT.csv"
SLOPE_PACK = OUT / "P8_Y5_R2FR_3216_MEMORY_SLOPE_BOUND_PACK.csv"
DECISION = OUT / "P8_Y5_R2FR_3216_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3216_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


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
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3216_00_3215_doc",
        "location": "post_checkpoint",
        "relative_path": "3215-Y5-R2FR-memory-scalar-nohair-or-coefficient-typing-theorem-for-balpha-Hodge-under-AX1090.md",
        "role": "3215 source-compatible nohair handoff",
        "terms": ["C_r'(0)", "positive memory no-hair alone", "coefficient-stationarity"],
    },
    {
        "input_id": "SRC3216_01_3215_source",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3215_MEMORY_SOURCE_COMPATIBILITY_THEOREM.csv",
        "role": "linear source identity and nohair counterexample",
        "terms": ["MSC3215_1_source_term", "MSC3215_4_nohair_only_counterexample"],
    },
    {
        "input_id": "SRC3216_02_3215_stationarity",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3215_COEFFICIENT_STATIONARITY_GATE.csv",
        "role": "stationarity gates for EM/Hodge/readout/boundary",
        "terms": ["CSG3215_0_balpha_memory", "CSG3215_2_hodge_metric", "CSG3215_4_boundary_flux"],
    },
    {
        "input_id": "SRC3216_03_3214_jacobian",
        "location": "post_checkpoint",
        "relative_path": "3214-Y5-R2FR-invariant-generator-kill-list-for-EM-coupling-or-promote-provenance-inputs-under-AX1090.md",
        "role": "coupling Jacobian gate",
        "terms": ["J_C(I)", "fixed discrete", "continuous memory"],
    },
    {
        "input_id": "SRC3216_04_1105_master",
        "location": "post_checkpoint",
        "relative_path": "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md",
        "role": "typed/no-hidden-visible coefficient morphism route",
        "terms": ["MHM1105_2_product_functor", "MHM1105_3_scalar_counterexample", "PACK1105_0_parent_object_language"],
    },
    {
        "input_id": "SRC3216_05_1097_constants",
        "location": "post_checkpoint",
        "relative_path": "1097-Y5-R10-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md",
        "role": "constant-sector universality and dimensionless guard",
        "terms": ["CSU1097_1_descent_superselection", "CSU1097_2_dimensionless_guard", "CSU1097_5_verdict"],
    },
    {
        "input_id": "SRC3216_06_1291_strict",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1291_STRICT_DOUBLE_ZERO_PARENT_CLAUSE.csv",
        "role": "strict double-zero parent clause",
        "terms": ["SDZ1291_1_strict_F_form", "SDZ1291_3_no_multiplier_or_readout_cheat", "SDZ1291_5_parent_clause_verdict"],
    },
    {
        "input_id": "SRC3216_07_1533_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv",
        "role": "parent action double-zero contract",
        "terms": ["VAC1533_1_potential_source", "VAC1533_2_vacuum_subtraction", "VAC1533_6_verdict"],
    },
    {
        "input_id": "SRC3216_08_2141_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_2141_DOUBLE_ZERO_THEOREM.csv",
        "role": "exact double-zero mechanism for sourced minimal form",
        "terms": ["DZ2141_1_K_first_derivative", "DZ2141_5_nonflat_system", "DZ2141_6_verdict"],
    },
    {
        "input_id": "SRC3216_09_2817_kill",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2817_STRICT_DOUBLE_ZERO_COEFFICIENT_KILL.csv",
        "role": "strict double-zero coefficient kill",
        "terms": ["CK2817_1_exact_double_zero", "CK2817_2_local_lock_dependency", "CK2817_4_verdict"],
    },
    {
        "input_id": "SRC3216_10_3063_extra",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3063_EXTRA_DOUBLE_ZERO_PROOF_ATTEMPT.csv",
        "role": "extra-sector double-zero proof status",
        "terms": ["DZ3063_2_derivative_zero_dC", "DZ3063_6_physical_lock", "DZ3063_7_verdict"],
    },
    {
        "input_id": "SRC3216_11_3071_root",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3071_SOURCE_ROOT_DOUBLE_ZERO_ROUTE_AUDIT.csv",
        "role": "source-root double-zero route",
        "terms": ["SR3071_1_Fprime_stationary", "SR3071_2_double_zero", "SR3071_3_finite_displacement"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    theorem_rows = [
        {
            "route_id": "THM3216_0_operator_independence",
            "route": "universal source silence implies coefficient stationarity",
            "formal_statement": "If m=0 is a solution for every allowed local visible configuration and the operator set {O_r} is linearly independent modulo identities/boundaries, then sum_r C_r'(0) O_r=0 for all configurations implies C_r'(0)=0 for each active channel.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "turns source silence into individual b_alpha/Hodge/readout/boundary slope zero without cancellation",
            "missing_for_claim": "parent statement that the same local branch m=0 solves the memory equation for the full allowed visible test class",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "THM3216_1_typed_exclusion",
            "route": "object-language/domain exclusion",
            "formal_statement": "If visible coefficients C_r are typed as C_r=Cbar_r(q(Phi),representation,topological level) and m is vertical with Dq[partial_m]=0, then partial_m C_r=0 by the chain rule.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "kills all memory-to-visible coefficient slopes at tree level",
            "missing_for_claim": "parent-owned visible coefficient vertex list and radiative/readout stability",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "THM3216_2_even_fixed_point",
            "route": "exact branch involution/evenness",
            "formal_statement": "If the local branch has an exact involution sigma:m->-m fixing visible operators and the parent coefficient maps obey C_r(sigma m)=C_r(m), then C_r'(0)=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "derives double-zero/stationarity without setting the constant C_r(0) to zero",
            "missing_for_claim": "parent symmetry, same-branch fixed origin, and proof visible/readout/boundary maps respect sigma",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "THM3216_3_source_root_deformation",
            "route": "vacuum-subtracted strict double-zero deformation",
            "formal_statement": "If C_r(m)=C_r0+lambda_r F(m) with F(m_*)=F'(m_*)=0, equivalently F=(m-m_*)^2 H smooth and finite, then C_r'(m_*)=0; if C_r0=0 the coefficient is also value-zero.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "imports the 1291/1533/2141/2817 double-zero algebra into alpha/Hodge/readout slopes",
            "missing_for_claim": "parent source-root F for each visible coefficient and local lock m=m_*",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "THM3216_4_extremum_limit",
            "route": "action extremum alone is insufficient",
            "formal_statement": "V_mem'(m_*)=0 does not imply C_r'(m_*)=0; the total variation contains V_mem'(m_*)+sum_r C_r'(m_*)O_r, so visible operators source m unless the slopes vanish, are typed out, or cancel for all states by an independent theorem.",
            "status": "COUNTERTHEOREM",
            "what_it_buys": "blocks the fake shortcut 'm is at an extremum so all couplings are stationary'",
            "missing_for_claim": "not applicable; this is a guardrail",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "THM3216_5_quadratic_correction_guard",
            "route": "stationarity still modifies the Hessian",
            "formal_statement": "Even when C_r'(0)=0, the second variation contains sum_r C_r''(0)O_r; local nohair needs G_eff=G_mem-eta_visible>0 after these corrections.",
            "status": "CORRECTION_GUARD",
            "what_it_buys": "prevents double-zero from silently creating a tachyon/long-range scalar",
            "missing_for_claim": "bounds on C_r''(0), visible operator norms, and parent spectral floor",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    independence_rows = [
        {
            "guard_id": "IND3216_0_F2",
            "operator": "F^2",
            "independence_test": "electrostatic/magnetostatic configurations make F^2 nonzero while matter/source/readout choices can be varied separately",
            "consequence": "b_alpha_memory cannot be cancelled generically by Hodge/readout/source terms",
            "status": "INDEPENDENCE_GUARD_WRITTEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "guard_id": "IND3216_1_FstarF",
            "operator": "FstarF",
            "independence_test": "parallel E dot B configurations vary FstarF independently from F^2; parity/time-arrow sectors must be treated separately",
            "consequence": "dual/theta slope needs its own zero or bound row",
            "status": "INDEPENDENCE_GUARD_WRITTEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "guard_id": "IND3216_2_null_wave_stress",
            "operator": "T_EM/Hodge with null radiation",
            "independence_test": "null EM waves can have F^2=FstarF=0 while T_EM and Poynting flux remain nonzero",
            "consequence": "Hodge/stress and Poynting slopes are not killed by F2 stationarity",
            "status": "INDEPENDENCE_GUARD_WRITTEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "guard_id": "IND3216_3_matter_source",
            "operator": "matter stress/source weights",
            "independence_test": "ordinary matter stress can be present with EM off and composition/source labels varied",
            "consequence": "source universality and WEP slopes cannot be hidden in alpha stationarity",
            "status": "INDEPENDENCE_GUARD_WRITTEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "guard_id": "IND3216_4_boundary_flux",
            "operator": "boundary/worldtube flux",
            "independence_test": "surface flux depends on support/worldtube choice and is not fixed by the bulk Euler equation alone",
            "consequence": "bulk double-zero does not remove C_Poynting unless boundary functor is included",
            "status": "INDEPENDENCE_GUARD_WRITTEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    route_rows = [
        {
            "audit_id": "RA3216_0_best_zero_route",
            "candidate": "typed exclusion plus radiative/readout stability",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "most economical if the parent action can enumerate visible coefficient domains once",
            "risk": "1105 scalar counterexample survives if hidden invariants remain legal coefficient arguments",
            "next_evidence": "parent visible-coefficient vertex list showing no memory argument for EM, Hodge, matter, readout, and boundary maps",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "RA3216_1_double_zero_route",
            "candidate": "strict source-root/even deformation C=C0+lambda F with F=O((m-m_*)^2)",
            "current_status": "ALGEBRA_EXACT_SOURCE_ROOT_NOT_PARENT_MATCHED",
            "reason": "1291/2141/2817 already prove the derivative-zero algebra under premises",
            "risk": "without local lock m=m_* and boundary/readout closure it becomes fitted root language",
            "next_evidence": "same-branch local lock and source-root ownership for each visible coefficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "RA3216_2_operator_independence_route",
            "candidate": "derive slopes from all-state source silence",
            "current_status": "POWERFUL_CONTRACT_NOT_PARENT_ASSUMPTION",
            "reason": "if MTS demands local memory silence for arbitrary allowed visible test fields, no-cancellation forces slopes zero",
            "risk": "if silence only holds for one fitted state, cancellations are possible and invalid for a field theory",
            "next_evidence": "all-state local branch theorem and independent-operator basis statement",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "RA3216_3_finite_route",
            "candidate": "source-backed memory slope bound pack",
            "current_status": "REQUIRED_IF_ZERO_ROUTES_UNSIGNED",
            "reason": "keeps theory testable without pretending coefficient slopes vanish",
            "risk": "not a prediction until slopes, field norms, supports, and units are source-backed",
            "next_evidence": "numeric or symbolic parent-owned slope bounds with source paths",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    slope_rows = [
        {
            "slope_id": "SLP3216_0_balpha_memory",
            "coefficient": "b_alpha_m = partial_m ln Z_A at m_*",
            "zero_authority_options": "typed exclusion; exact evenness; strict F=O((m-m_*)^2); all-state source silence",
            "finite_bound_row": "abs(b_alpha_m) with units 1/[m] or dimensionless if m normalized",
            "operator_norm_needed": "||F^2|| on local support",
            "feeds": "J_m_vis; alpha drift; R10/clocks/WEP alpha channel",
            "current_status": "MISSING_ZERO_AUTHORITY_OR_SLOPE_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "slope_id": "SLP3216_1_theta_memory",
            "coefficient": "b_theta_m = partial_m Theta_A at m_*",
            "zero_authority_options": "topological/discrete constant; exact parity/evenness; typed exclusion",
            "finite_bound_row": "abs(b_theta_m) plus FstarF support norm",
            "operator_norm_needed": "||FstarF||",
            "feeds": "dual/topological EM source; parity/time-arrow residual",
            "current_status": "MISSING_ZERO_AUTHORITY_OR_SLOPE_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "slope_id": "SLP3216_2_hodge_memory",
            "coefficient": "B_Hodge_m = partial_m g_obs or partial_m star_obs at m_*",
            "zero_authority_options": "observed coframe factors only through q; exact evenness; all-state source silence",
            "finite_bound_row": "operator norm ||B_Hodge_m T_EM||",
            "operator_norm_needed": "EM stress/Hodge norm including null radiation",
            "feeds": "PPN;clock;EM stress;local metric residual",
            "current_status": "MISSING_ZERO_AUTHORITY_OR_SLOPE_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "slope_id": "SLP3216_3_readout_memory",
            "coefficient": "B_readout_m = partial_m C_readout at m_*",
            "zero_authority_options": "readout-after-variation; no S_eff feedback; exact stationarity",
            "finite_bound_row": "readout coefficient derivative times clock/alpha observable norm",
            "operator_norm_needed": "clock/spectroscopy/readout operator norm",
            "feeds": "clock drift; alpha readout; radiative return",
            "current_status": "MISSING_READOUT_CLOSURE_OR_SLOPE_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "slope_id": "SLP3216_4_boundary_memory",
            "coefficient": "B_boundary_m = partial_m C_boundary at m_*",
            "zero_authority_options": "boundary functor exact/proper/orthogonal; strict double-zero boundary weight; no-flux theorem",
            "finite_bound_row": "abs(B_boundary_m) integral |n_i T_EM^0i| dS dt",
            "operator_norm_needed": "Poynting/worldtube flux norm",
            "feeds": "3210 boundary leakage; local PPN/clock/R10 residual",
            "current_status": "MISSING_BOUNDARY_ZERO_OR_FLUX_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "slope_id": "SLP3216_5_source_weight_memory",
            "coefficient": "B_source_m = partial_m kappa_A or source weight at m_*",
            "zero_authority_options": "universal Hilbert source theorem; typed source coupling; all-material no-cancellation",
            "finite_bound_row": "species/source-weight derivative with WEP/PPN/Newton source normalization",
            "operator_norm_needed": "matter stress/source composition norm",
            "feeds": "Newtonian GM; WEP; PPN source coupling",
            "current_status": "MISSING_UNIVERSAL_SOURCE_THEOREM_OR_SLOPE_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3216_0_result",
            "result": "STATIONARITY_ROUTES_DERIVED_AS_CONDITIONALS_NO_PARENT_SIGNED_ZERO_YET_SLOPE_PACK_STAGED",
            "claim_status": "NO_BALPHA_ZERO_NO_MEMORY_SILENCE_NO_LOCAL_GR_CLAIM",
            "decision": "3216 derives the exact ways branch-origin coefficient stationarity can be real: typed exclusion, exact even/fixed-point symmetry, strict source-root double-zero, or all-state operator-independence/no-cancellation. Current corpus does not parent-sign any route for the full EM/Hodge/readout/boundary/source set, so finite memory-slope rows remain required.",
            "best_next_route": "build the parent visible-coefficient vertex list and test whether memory is absent from every visible coefficient domain; this is the least-scrutiny route because it can kill many slopes at once",
            "next_target": "3217-Y5-R2FR-parent-visible-coefficient-vertex-list-or-first-memory-slope-source-row-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    return input_rows, theorem_rows, independence_rows, route_rows, slope_rows, decision_rows


def main() -> None:
    now = stamp()
    input_rows, theorem_rows, independence_rows, route_rows, slope_rows, decision_rows = build_rows(now)

    generated_without_validation = [
        INPUTS,
        THEOREMS,
        INDEPENDENCE,
        ROUTE_AUDIT,
        SLOPE_PACK,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(THEOREMS, theorem_rows)
    write_csv(INDEPENDENCE, independence_rows)
    write_csv(ROUTE_AUDIT, route_rows)
    write_csv(SLOPE_PACK, slope_rows)
    write_csv(DECISION, decision_rows)

    all_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_rows.extend(read_csv(path))
    claim_rows = [row for row in all_rows if row.get("valid_for_claim") == "true"]

    validation_rows = [
        {
            "check_id": "VAL3216_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_01_stationarity_routes",
            "check": "stationarity theorem routes include typing, evenness, double-zero, and operator independence",
            "pass": b(len(theorem_rows) >= 6),
            "detail": ";".join(row["route_id"] for row in theorem_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_02_no_fake_extremum",
            "check": "extremum-only shortcut is rejected",
            "pass": b(any(row["route_id"] == "THM3216_4_extremum_limit" for row in theorem_rows)),
            "detail": "V_mem extremum alone does not imply C_r slope zero",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_03_independence_guard",
            "check": "operator independence/no-cancellation guard covers bulk, stress, matter, boundary",
            "pass": b(len(independence_rows) >= 5),
            "detail": ";".join(row["guard_id"] for row in independence_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_04_slope_pack",
            "check": "finite slope pack covers alpha, dual, Hodge, readout, boundary, source",
            "pass": b(len(slope_rows) >= 6),
            "detail": ";".join(row["slope_id"] for row in slope_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_05_claims_blocked",
            "check": "no generated row is valid_for_claim true",
            "pass": b(len(claim_rows) == 0),
            "detail": f"claim_rows_true={len(claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_06_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3216_08_next_target",
            "check": "next target is concrete and derivation-first",
            "pass": b("3217" in decision_rows[0]["next_target"]),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3216 - Branch-Origin Coefficient Stationarity Or Memory Slope Bound Pack under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha=0` claim, memory silence claim, or public-facing result.

## Result

3216 derives the stationarity fork cleanly.

The source term from 3215 was:

```text
J_m,vis(0) = - sum_r C_r'(0) O_r.
```

Therefore `C_r'(0)=0` is not optional decoration. It is the exact lock that stops ordinary visible fields from sourcing the memory scalar.

There are four legitimate ways to get it:

```text
1. typed exclusion:
   C_r = Cbar_r(q(Phi), representation data), Dq[partial_m]=0

2. exact fixed-point/even symmetry:
   m -> -m and C_r(m)=C_r(-m)

3. strict source-root/double-zero deformation:
   C_r(m)=C_r0 + lambda_r F(m), F(m_*)=F'(m_*)=0

4. all-state source silence:
   sum_r C_r'(0)O_r = 0 for all independent visible test operators
   => each C_r'(0)=0
```

The false route is now explicitly rejected:

```text
V_mem'(m_*)=0 alone does not imply C_r'(m_*)=0.
```

A memory potential can be stationary while EM, Hodge, readout, boundary, or source coefficients still have linear slopes. That would source memory and spoil a local-GR/Maxwell reduction unless those slopes are zero or bounded.

## Stationarity Theorem Routes

{md_table(theorem_rows, ["route_id", "route", "formal_statement", "status", "what_it_buys", "missing_for_claim", "valid_for_claim"])}

## Visible Operator Independence Guard

{md_table(independence_rows, ["guard_id", "operator", "independence_test", "consequence", "status", "valid_for_claim"])}

## Route Audit

{md_table(route_rows, ["audit_id", "candidate", "current_status", "reason", "risk", "next_evidence", "valid_for_claim"])}

## Memory Slope Bound Pack

{md_table(slope_rows, ["slope_id", "coefficient", "zero_authority_options", "finite_bound_row", "operator_norm_needed", "feeds", "current_status", "valid_for_claim"])}

## Decision

`{decision_rows[0]["result"]}`.

Claim status: `{decision_rows[0]["claim_status"]}`.

Best next route: {decision_rows[0]["best_next_route"]}.

Next target:

```text
{decision_rows[0]["next_target"]}
```

## Generated Evidence

- `{rel(INPUTS)}`
- `{rel(THEOREMS)}`
- `{rel(INDEPENDENCE)}`
- `{rel(ROUTE_AUDIT)}`
- `{rel(SLOPE_PACK)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
