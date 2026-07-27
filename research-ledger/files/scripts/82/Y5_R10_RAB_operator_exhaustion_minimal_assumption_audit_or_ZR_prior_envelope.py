from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1262"
TITLE = "1262-Y5-R10-RAB-operator-exhaustion-minimal-assumption-audit-or-ZR-prior-envelope"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS_DIR = ROOT / "source-intake" / "rab-sector" / "docs"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
MINIMAL_ASSUMPTION_PATH = OUT_DIR / f"{PACK_ID}_MINIMAL_ASSUMPTION_AUDIT.csv"
THEOREM_CANDIDATE_PATH = OUT_DIR / f"{PACK_ID}_VERTICAL_NULL_THEOREM_CANDIDATE.csv"
CLOSURE_SMUGGLING_PATH = OUT_DIR / f"{PACK_ID}_CLOSURE_SMUGGLING_AUDIT.csv"
COUNTERMODEL_PATH = OUT_DIR / f"{PACK_ID}_LEGAL_COUNTERMODEL_AUDIT.csv"
PRIOR_ENVELOPE_PATH = OUT_DIR / f"{PACK_ID}_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1262_VALIDATION.csv"
ZR1262_TEMPLATE_PATH = RAB_DOCS_DIR / "ZR1262_RAB_PRIOR_ENVELOPE_TEMPLATE_NONCLAIM.csv"


ZR1262_TEMPLATE_FIELDS = [
    "row_id",
    "coefficient_symbol",
    "branch",
    "coefficient_value",
    "coefficient_units",
    "prior_lower",
    "prior_upper",
    "normalization_convention",
    "arena_projection",
    "source_path",
    "source_anchor",
    "status",
    "valid_for_claim",
    "claim_allowed",
    "notes",
]


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(rows: list[dict[str, object]]) -> bool:
    joined = "\n".join(str(value) for row in rows for value in row.values())
    return "MISSING" in joined or "TBD" in joined or "PLACEHOLDER" in joined


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        MINIMAL_ASSUMPTION_PATH,
        THEOREM_CANDIDATE_PATH,
        CLOSURE_SMUGGLING_PATH,
        COUNTERMODEL_PATH,
        PRIOR_ENVELOPE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        ZR1262_TEMPLATE_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAB_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1262_0_1261_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1261_NEXT_TARGET.csv",
            "needle": "NEXT1261_0_1262",
            "purpose": "handoff to minimal R_AB operator-exhaustion audit or Z_R prior envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1262_1_1261_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1261_OPERATOR_EXHAUSTION_REENTRY_AUDIT.csv",
            "needle": "ZERO_PROOF_NOT_CLOSED_RETAIN_ZR_BRANCH",
            "purpose": "previous verdict that zero proof remains unclosed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1262_2_1261_blocker",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1261_BLOCKER_LEDGER.csv",
            "needle": "minimal parent assumption audit showing no independent R_AB gradient constructor exists",
            "purpose": "explicit blocker to resolve",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1262_3_1259_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1259_OPERATOR_EXCLUSION_THEOREM_CANDIDATE.csv",
            "needle": "EXACT_IF_PARENT_SIGNED_NOT_DERIVED",
            "purpose": "conditional R_AB gradient-ban theorem candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1262_4_1259_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1259_ZR_POSITIVE_COEFFICIENT_CONTRACT.csv",
            "needle": "ZRC1259_0_ZR",
            "purpose": "fallback Z_R-positive coefficient contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1262_5_1058_exhaustion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
            "needle": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR",
            "purpose": "generic operator exhaustion not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1262_6_1107_object",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            "needle": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
            "purpose": "object-language exhaustion not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1262_7_1236_typed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
            "purpose": "typed certificate is a closure contract, not theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    minimal_assumptions = [
        {
            "assumption_id": "MIN1262_0_RAB_vertical_sort",
            "assumption": "`R_AB` is a representative/compatibility coordinate on the vertical fibre, not a quotient observable or hidden physical scalar.",
            "why_needed": "If `R_AB` is physical, the gradient term is an ordinary legal kinetic energy.",
            "mathematical_form": "for every compact local variation delta R_AB there is delta Phi in ker(Dq) with delta r_AB=delta R_AB",
            "current_status": "NOT_PARENT_DERIVED",
            "closure_risk": "medium: it must be derived from the parent quotient map, not declared after local tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "MIN1262_1_vertical_null_action",
            "assumption": "The local parent action descends through the quotient and has no density on vertical fibre directions.",
            "why_needed": "A gradient penalty is exactly an action density on representative changes.",
            "mathematical_form": "S_loc[Phi]=Sbar[q(Phi),theta,top] and delta_v S_loc=0 for compact v in ker(Dq)",
            "current_status": "MINIMAL_CORE_ASSUMPTION_NOT_SIGNED",
            "closure_risk": "high: this is the real theorem we need, otherwise it is a closure axiom",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "MIN1262_2_no_vertical_metric_connection",
            "assumption": "The parent supplies no vertical fibre metric, vertical connection, or Sobolev norm that could make |D R_AB|^2 quotient-natural.",
            "why_needed": "Without this ban, a gauge-covariant vertical gradient operator can be written consistently.",
            "mathematical_form": "no parent object G_vert and nabla_vert with G_vert(nabla r,nabla r) in the local density",
            "current_status": "NOT_PARENT_DERIVED",
            "closure_risk": "high: this is where a hidden counterterm can be smuggled back in",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "MIN1262_3_boundary_and_defect_silence",
            "assumption": "Local-vacuum source worldtubes carry no vertical boundary charge, defect current, or reference subtraction for `R_AB`.",
            "why_needed": "Boundary support can source nonzero `R_AB` hair even if bulk vertical directions are null.",
            "mathematical_form": "Pi_R^n=0 and delta B_R/delta R_AB=0 on the local exterior boundary class",
            "current_status": "NOT_PARENT_DERIVED",
            "closure_risk": "medium: requires source-worldtube/no-flux theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "MIN1262_4_radiative_readout_closure",
            "assumption": "Effective/readout reduction preserves quotient descent and does not regenerate a vertical fibre energy.",
            "why_needed": "Tree-level null directions are not enough if the readout action can create `Z_R` later.",
            "mathematical_form": "S_eff and readout maps remain in Image(ParentGenerate[q,theta,top])",
            "current_status": "UNSIGNED",
            "closure_risk": "high: inherited blocker from 1058/1107/1236",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_candidate = [
        {
            "candidate_id": "THEO1262_0_vertical_null_ban",
            "theorem_name": "vertical-fibre null ban for R_AB gradient energy",
            "statement": "If MIN1262_0 through MIN1262_4 are parent-derived, then int sqrt(h) Z_R h^{ij}D_iR_ABD_jR_AB is not an allowed local physical operator and the local branch has Z_R=0.",
            "proof_step": "The gradient term changes under arbitrary compact vertical representative variations unless the parent supplies a vertical metric/connection; quotient descent plus no vertical metric forbids such dependence.",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "claim_effect": "would close the R_AB local residual without fitting a finite Z_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "THEO1262_1_no_plateau_needed",
            "theorem_name": "no local plateau smuggling",
            "statement": "The route bans the operator itself rather than assuming D_iR_AB=0 at a local plateau.",
            "proof_step": "Variation of the operator gives a nonzero bulk equation for generic compact vertical variations, so a plateau is an equation-of-motion special case, not a derivation of Z_R=0.",
            "proof_status": "USEFUL_REJECTION_OF_PLATEAU_AXIOM",
            "claim_effect": "prevents the earlier local branch from hiding an extra axiom",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "THEO1262_2_counterterm_survival_if_physical",
            "theorem_name": "finite-Z_R survival condition",
            "statement": "If any of MIN1262_0 through MIN1262_4 fails, `Z_R` must remain as a finite residual coefficient or bounded prior.",
            "proof_step": "A physical or vertically-metrized `R_AB` has an allowed second-derivative local kinetic operator by symmetry and dimensional analysis.",
            "proof_status": "COUNTERMODEL_FORCES_NONCLAIM_FALLBACK",
            "claim_effect": "blocks local-GR/R10/PPN promotion until the residual is derived or sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_smuggling = [
        {
            "audit_id": "CS1262_0_declaring_RAB_gauge",
            "risk": "declaring `R_AB` vertical/gauge by fiat",
            "why_bad": "This would merely rename the desired result; it must come from the parent quotient map.",
            "safe_requirement": "source a parent map q and show R_AB variations lie in ker(Dq)",
            "status": "UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CS1262_1_no_vertical_metric",
            "risk": "quietly assuming no vertical fibre metric or connection",
            "why_bad": "A parent vertical metric would make the gradient term legal and give real local hair.",
            "safe_requirement": "derive absence of G_vert/nabla_vert from motion/time/space primitives",
            "status": "UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CS1262_2_boundary_silence",
            "risk": "assuming the boundary current vanishes",
            "why_bad": "Even a null bulk fibre can carry boundary charge in a source worldtube.",
            "safe_requirement": "prove Pi_R^n=0 and B_R silence for the local exterior class",
            "status": "UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CS1262_3_readout_loops",
            "risk": "tree-level proof only",
            "why_bad": "Effective/readout reduction can regenerate a counterterm unless the quotient grammar is stable.",
            "safe_requirement": "radiative/readout closure of the typed parent object language",
            "status": "UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    countermodels = [
        {
            "countermodel_id": "CM1262_0_physical_scalar_RAB",
            "allowed_if": "`R_AB` is a genuine local scalar/tensor component rather than a pure representative coordinate",
            "operator": "int sqrt(h) 1/2 Z_R h^{ij}D_iR_ABD_jR_AB",
            "lesson": "diffeomorphism/locality alone do not ban the term",
            "effect": "operator-exhaustion must be parent-derived, not assumed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1262_1_vertical_metric_exists",
            "allowed_if": "the parent includes a vertical fibre metric and compatible connection",
            "operator": "int sqrt(h) G_vert(DR_AB,DR_AB)",
            "lesson": "even representative variables can carry energy if the parent gives them a fibre norm",
            "effect": "MIN1262_2 is essential",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1262_2_boundary_defect",
            "allowed_if": "the source worldtube carries a vertical boundary charge or defect class",
            "operator": "bulk null plus nonzero B_R boundary variation",
            "lesson": "bulk Z_R=0 does not by itself prove local exterior silence",
            "effect": "boundary/no-hair proof remains separate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    prior_requirements = [
        {
            "requirement_id": "PRIOR1262_0_ZR",
            "coefficient": "Z_R",
            "requirement": "source-backed value, theorem-zero, or explicit prior interval with units and normalization",
            "relation": "feeds either finite q_Rhat branch or ell_R suppression branch",
            "current_status": "MISSING_SOURCE_BACKED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "PRIOR1262_1_MR2",
            "coefficient": "M_R^2",
            "requirement": "parent Hessian or sourced mass-gap/screening scale",
            "relation": "ell_R=sqrt(Z_R/M_R^2) after declared normalization",
            "current_status": "MISSING_SOURCE_BACKED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "PRIOR1262_2_JR",
            "coefficient": "J_R",
            "requirement": "matter descent zero theorem or finite source coupling",
            "relation": "sets Q_R and therefore q_Rhat amplitude",
            "current_status": "MISSING_SOURCE_BACKED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "PRIOR1262_3_BR",
            "coefficient": "B_R",
            "requirement": "boundary no-hair theorem or finite boundary-flux bound",
            "relation": "controls Pi_R^n and residual exterior hair",
            "current_status": "MISSING_SOURCE_BACKED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "PRIOR1262_4_arena_projection",
            "coefficient": "tau_R10/tau_PPN/tau_clock/tau_orbital",
            "requirement": "arena kernels translating coefficient envelope into observable residuals",
            "relation": "prevents a broad prior envelope from being mistaken for a local pass",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    template_rows = [
        {
            "row_id": "ZR1262_TEMPLATE_DO_NOT_SCORE",
            "coefficient_symbol": "Z_R_or_M_R2_or_J_R_or_B_R",
            "branch": "MISSING_THEOREM_ZERO_OR_FINITE_PRIOR_BRANCH",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "coefficient_units": "MISSING_UNITS",
            "prior_lower": "MISSING_PRIOR_LOWER",
            "prior_upper": "MISSING_PRIOR_UPPER",
            "normalization_convention": "MISSING_NORMALIZATION_CONVENTION",
            "arena_projection": "MISSING_R10_PPN_CLOCK_OR_ORBITAL_PROJECTION",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "status": "DOCS_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only prior-envelope template. Do not move to raw/accepted until all MISSING markers are replaced by source-backed values or theorem-zero rows.",
        }
    ]
    write_csv(ZR1262_TEMPLATE_PATH, template_rows, ZR1262_TEMPLATE_FIELDS)

    claim_gates = [
        {
            "gate_id": "GATE1262_0_theorem_not_claimed",
            "claim": "Z_R=0 by operator-exhaustion",
            "status": "BLOCKED",
            "reason": "vertical-null/no-vertical-metric/boundary/radiative clauses are exact conditional but not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1262_1_prior_not_scoreable",
            "claim": "finite Z_R prior envelope is scoreable",
            "status": "BLOCKED",
            "reason": "template contains MISSING markers and no accepted source-backed coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1262_2_local_GR_not_passed",
            "claim": "local GR/Newton/R10/PPN pass",
            "status": "BLOCKED",
            "reason": "neither theorem-zero nor finite coefficient residual is sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1262_0_minimal_assumption",
            "decision": "the minimum clean theorem route is vertical-fibre null descent plus no vertical metric/connection and boundary/readout silence",
            "because": "this bans the operator itself rather than imposing a local plateau",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "next_action": "try to derive vertical-fibre null descent from the parent presymplectic/quotient structure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1262_1_fallback",
            "decision": "if vertical-fibre null descent cannot be parent-derived, retain a finite nonclaim Z_R prior envelope",
            "because": "legal countermodels exist whenever R_AB is physical or vertically metrized",
            "status": "NONCLAIM_FALLBACK_READY_AS_TEMPLATE_ONLY",
            "next_action": "do not score until source-backed coefficient and arena projection rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1262_0_1263",
            "target_file": "1263-Y5-R10-vertical-fibre-null-from-parent-presymplectic-degeneracy-or-RAB-prior-envelope-fill.md",
            "target_script": "scripts/Y5_R10_vertical_fibre_null_from_parent_presymplectic_degeneracy_or_RAB_prior_envelope_fill.py",
            "task": "try to derive ker(Dq) as a presymplectic null/gauge fibre of the parent action, including no vertical metric and boundary silence; if not, fill only a nonclaim prior-envelope intake contract",
            "success_condition": "parent-derived vertical null proof with no closure smuggling, or explicit demotion to finite residual coefficient workflow",
            "do_not": "do not claim Z_R=0, local GR, R10, PPN, clock, or orbital pass from the conditional theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (MINIMAL_ASSUMPTION_PATH, minimal_assumptions),
        (THEOREM_CANDIDATE_PATH, theorem_candidate),
        (CLOSURE_SMUGGLING_PATH, closure_smuggling),
        (COUNTERMODEL_PATH, countermodels),
        (PRIOR_ENVELOPE_PATH, prior_requirements),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    theorem_is_conditional = theorem_candidate[0]["proof_status"] == "EXACT_CONDITIONAL_NOT_PARENT_DERIVED"
    no_claim_gates = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_main_rows_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _path, rows in generated_tables
        for row in rows
    )
    template_nonclaim = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in template_rows)
    template_has_missing = contains_missing_marker(template_rows)
    next_is_1263 = next_target[0]["target_file"].startswith("1263-")

    csv_parse_ok = True
    csv_parse_details: list[str] = []
    for path, _rows in [*generated_tables, (ZR1262_TEMPLATE_PATH, template_rows)]:
        try:
            parsed_rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAILED:{exc}")

    formalization_writes = generated_inside_formalization()

    validation_rows = [
        validation_row("VAL1262_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1262_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1262_2_minimal_assumptions", "minimal assumption audit has every required clause", len(minimal_assumptions) == 5, f"minimal_assumption_rows={len(minimal_assumptions)}"),
        validation_row("VAL1262_3_conditional_theorem", "theorem is exact conditional, not claimed", theorem_is_conditional, theorem_candidate[0]["proof_status"]),
        validation_row("VAL1262_4_countermodels", "legal countermodels are recorded", len(countermodels) == 3, f"countermodel_rows={len(countermodels)}"),
        validation_row("VAL1262_5_claim_gates", "all claim gates remain blocked", no_claim_gates, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1262_6_nonclaim_policy", "all generated rows remain nonclaim", all_main_rows_nonclaim and template_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1262_7_template_guard", "prior-envelope template is docs-only and visibly incomplete", template_nonclaim and template_has_missing, f"template={ZR1262_TEMPLATE_PATH.name}"),
        validation_row("VAL1262_8_next_target_1263", "next target is vertical-fibre null derivation", next_is_1263, next_target[0]["target_file"]),
        validation_row("VAL1262_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1262_10_formalization_untouched", "formalization-workbench untouched by generated outputs", not formalization_writes, f"formalization_generated_output_count={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1262_11_overall",
            "overall 1262 validation",
            overall,
            "1262 isolates the minimum vertical-null theorem route, rejects closure smuggling, and creates only a nonclaim finite-Z_R prior-envelope template",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1262 narrows the clean derivation route: ban `Z_R` only if `R_AB` is parent-derived as a vertical/gauge representative coordinate and the parent action has no vertical fibre energy, no vertical metric/connection, no boundary charge, and stable readout descent.

**Main progress:** this is better than a plateau axiom. The candidate theorem bans the operator itself; it does not assume `D_i R_AB = 0` locally. But it is still exact-conditional, not parent-signed.

**No-claim guard:** no `Z_R=0`, local-GR/Newton, R10, PPN, clock, orbital, finite `q_R_hat`, or suppression claim is made.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Minimal Assumption Audit
{markdown_table(minimal_assumptions, ["assumption_id", "assumption", "why_needed", "mathematical_form", "current_status", "closure_risk", "valid_for_claim", "claim_allowed"])}

## Vertical Null Theorem Candidate
{markdown_table(theorem_candidate, ["candidate_id", "theorem_name", "statement", "proof_step", "proof_status", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Closure Smuggling Audit
{markdown_table(closure_smuggling, ["audit_id", "risk", "why_bad", "safe_requirement", "status", "valid_for_claim", "claim_allowed"])}

## Legal Countermodel Audit
{markdown_table(countermodels, ["countermodel_id", "allowed_if", "operator", "lesson", "effect", "valid_for_claim", "claim_allowed"])}

## Z_R Prior Envelope Requirements
{markdown_table(prior_requirements, ["requirement_id", "coefficient", "requirement", "relation", "current_status", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
