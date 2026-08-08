from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3527-Y5-R2FR-charge-generator-level-current-owner-or-alpha-ratio-countermodel-kill.md"
CANONICAL_STATUS = OUT / "P8_EM_alpha_level_current_owner_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3527": {"path": Path(__file__).resolve(), "role": "3527 generator"},
    "doc_3526": {
        "path": ROOT / "3526-Y5-R2FR-scalar-gauge-coupling-owner-DXlambda-zero-or-alpha-bound-runner.md",
        "role": "3526 ratio identity and scalar-coupling handoff",
    },
    "next_3526": {
        "path": OUT / "P8_Y5_R2FR_3526_NEXT_TARGET.csv",
        "role": "3526-selected level/current owner target",
    },
    "status_3526": {
        "path": OUT / "P8_EM_scalar_gauge_coupling_owner_status.csv",
        "role": "3526 canonical scalar coupling status",
    },
    "theorem_642": {
        "path": OUT / "P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv",
        "role": "compact U(1), integer labels and Maxwell action attempt",
    },
    "verdict_642": {
        "path": OUT / "P8_Y5_R10_642_ZERO_VERDICT.csv",
        "role": "642 compact U(1) does not fix alpha verdict",
    },
    "vgn_765": {
        "path": OUT / "P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv",
        "role": "765 vertical generator norm theorem attempt",
    },
    "rescale_765": {
        "path": OUT / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "role": "765 generator/current/readout counterexamples",
    },
    "maxwell_gate_765": {
        "path": OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "role": "765 Maxwell kinetic inheritance gates",
    },
    "level_audit_1056": {
        "path": OUT / "P8_Y5_R10_1056_TOPOLOGICAL_LEVEL_INDEX_ROUTE_AUDIT.csv",
        "role": "1056 topological level/index route audit",
    },
    "norm_audit_1056": {
        "path": OUT / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "role": "1056 generator norm derivation audit",
    },
    "rescale_1056": {
        "path": OUT / "P8_Y5_R10_1056_RESCALING_DEGENERACY_LEDGER.csv",
        "role": "1056 rescaling/counterterm/current/readout degeneracy ledger",
    },
    "tq_signature_1100": {
        "path": OUT / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
        "role": "1100 T_Q signature clauses",
    },
    "unique_f2_1057": {
        "path": OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "role": "1057 unique Maxwell subblock attempt",
    },
    "operator_domain_1058": {
        "path": OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "role": "1058 visible operator-domain exhaustion attempt",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def no_go_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NG3527_0_compact_U1_success",
            "claim_piece": "compact U(1) fixes relative charge labels",
            "statement": "If the visible charge fibre is a parent compact U(1), then matter representations carry integer labels and F_Q=dA_Q gives dF_Q=0.",
            "derivation": "Single-valued representation phases exp(i n theta_Q) require integer n. A connection on the U(1) bundle has curvature F_Q=dA_Q locally, so the Bianchi identity follows.",
            "result": "relative charge labels and homogeneous Maxwell kinematics have structural support",
            "blocker_or_limit": "the base charge unit Q_* and the Maxwell kinetic coefficient are not fixed by this alone",
            "status": "PARTIAL_DERIVATION_SUCCESS",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NG3527_1_continuous_coupling_no_go",
            "claim_piece": "compact U(1) plus Noether current does not fix alpha",
            "statement": "For a 4D U(1) gauge field on a fixed observed geometry, the family S_g=-1/(4g^2) int F_Q wedge *_obs F_Q + int A_Q wedge J_Q is gauge invariant and current-conserving for every positive real g.",
            "derivation": "Gauge invariance only requires dJ_Q=0 and F_Q=dA_Q. The coefficient g^{-2} multiplies a gauge-invariant local operator. Changing g changes the strength in d*_obs F_Q=g^2 *_obs J_Q but violates neither compactness nor the Ward identity.",
            "result": "ordinary compact U(1) and Noether current cannot derive a numeric or vertical-silent alpha by themselves",
            "blocker_or_limit": "an extra parent norm/level/domain principle is required",
            "status": "DERIVED_NO_GO_FOR_COMPACT_U1_ONLY",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NG3527_2_same_current_is_necessary_not_sufficient",
            "claim_piece": "same current owner kills one countermodel but not the F2 coefficient",
            "statement": "If J_Q is the Noether current of T_Q and Q_* is fixed, current rescaling is blocked, but an independent F_Q^2 coefficient remains legal unless the operator domain is exhausted.",
            "derivation": "The interaction normalization and current conservation can be owned by representation data. However lambda_A F_Q^2 contains no current and is still a local gauge-invariant scalar operator.",
            "result": "same-current owner is necessary for WEP/R10/source tests but insufficient for C_XF2=0",
            "blocker_or_limit": "unique F2/no independent counterterm theorem still required",
            "status": "DERIVED_NECESSITY_NOT_SUFFICIENCY",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NG3527_3_topological_level_limit",
            "claim_piece": "topology can fix levels but not automatically the Maxwell kinetic term",
            "statement": "BF/Chern-Simons/index/monopole data can quantize charge or topological response coefficients, but the 4D Maxwell F_Q^2 coefficient is fixed only if a parent inheritance theorem ties it to that level.",
            "derivation": "The F_Q wedge *_obs F_Q term uses the metric/Hodge structure and is not itself a topological period. Quantized flux or charge labels do not determine its real prefactor without an extra metric/fibre norm or duality condition.",
            "result": "topological routes are possible but not present as a current parent theorem",
            "blocker_or_limit": "no source signs BF/CS/index/monopole-to-F2 inheritance",
            "status": "EXTRA_PRINCIPLE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NG3527_4_live_verdict",
            "claim_piece": "C_XF2 zero from charge-generator level/current owner",
            "statement": "The live corpus cannot derive C_XF2=0 from compact U(1), charge lattice and Noether current alone.",
            "derivation": "642 supplies compact labels, 765/1056 identify the correct parent norm/current theorem shape, but 1057/1058 keep independent F_Q^2 and operator-domain counterterms legal.",
            "result": "alpha/source coupling remains either an explicit calibrated constant or a finite residual bound branch",
            "blocker_or_limit": "unique parent curvature norm plus no-extra-F2 domain is the remaining non-circular derivation route",
            "status": "ZERO_REJECTED_FOR_COMPACT_U1_ONLY",
            "valid_for_claim": "False",
        },
    ]


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RA3527_0_compact_U1",
            "candidate_owner": "compact U(1) charge fibre",
            "owns": "integer relative charges; connection period; dF=0",
            "does_not_own": "continuous Maxwell kinetic coefficient g^{-2}; base charge unit as measured alpha",
            "current_evidence": "642 and 1056",
            "verdict": "SUPPORT_ONLY_NOT_ALPHA_OWNER",
            "source_path": str(SOURCES["theorem_642"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "route_id": "RA3527_1_parent_norm",
            "candidate_owner": "fixed parent generator norm N_Q",
            "owns": "T_Q scale if a parent metric/symplectic/lattice form signs it",
            "does_not_own": "independent lambda_A F_Q^2 unless unique F2 domain closes",
            "current_evidence": "765 and 1056 mark this as the right theorem shape but unsigned",
            "verdict": "RIGHT_SHAPE_NOT_SIGNED",
            "source_path": str(SOURCES["vgn_765"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "route_id": "RA3527_2_same_current",
            "candidate_owner": "Noether/Ward current of T_Q",
            "owns": "current conservation and source/test charge normalization if signed",
            "does_not_own": "vacuum F2 coefficient",
            "current_evidence": "765/1100 retain current owner as unsigned",
            "verdict": "NECESSARY_FOR_SOURCE_TESTS_NOT_SUFFICIENT",
            "source_path": str(SOURCES["tq_signature_1100"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "route_id": "RA3527_3_topological_level",
            "candidate_owner": "BF/CS/index/monopole/topological level",
            "owns": "integer levels or charge/topological response coefficients",
            "does_not_own": "4D metric Maxwell coefficient without an inheritance theorem",
            "current_evidence": "1056 says possible but not present",
            "verdict": "EXTRA_PRINCIPLE_NOT_IN_CURRENT_CORPUS",
            "source_path": str(SOURCES["level_audit_1056"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "route_id": "RA3527_4_operator_domain",
            "candidate_owner": "visible operator-domain exhaustion / unique F2",
            "owns": "exclusion of lambda_A and f_X F_Q^2 if parent-signed",
            "does_not_own": "base current/source normalization unless paired with T_Q/J_Q",
            "current_evidence": "1057/1058 keep this as the hard remaining gate",
            "verdict": "BEST_NEXT_DERIVATION_ROUTE",
            "source_path": str(SOURCES["operator_domain_1058"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def countermodel_kill_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CK3527_0_generator_rescale",
            "countermodel": "T_Q/A_Q/current normalization rescale",
            "killed_by_3527": "partially",
            "reason": "a fixed compact representation lattice plus fixed parent norm would kill pure generator rescaling, but that norm is not signed",
            "still_alive": "True",
            "needed_to_kill": "nonrescalable parent norm and fixed base charge unit",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CK3527_1_independent_F2",
            "countermodel": "independent lambda_A F_Q^2",
            "killed_by_3527": "no",
            "reason": "the no-go theorem shows compact U(1) and Noether current allow a continuous F2 coefficient",
            "still_alive": "True",
            "needed_to_kill": "unique F2 / visible operator-domain exhaustion theorem",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CK3527_2_current_rescale",
            "countermodel": "J_A -> c_A(X)J_A source/test charge drift",
            "killed_by_3527": "conditionally",
            "reason": "same Noether current owner would kill it, but current/source denominator ownership is unsigned",
            "still_alive": "True",
            "needed_to_kill": "same current owner across matter, source, test, clocks and readout",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CK3527_3_topological_shortcut",
            "countermodel": "claim topology fixes alpha directly",
            "killed_by_3527": "yes",
            "reason": "topological charge/level data do not automatically fix the 4D metric F2 coefficient",
            "still_alive": "False_as_shortcut",
            "needed_to_kill": "not applicable; shortcut rejected, only a real inheritance theorem could work",
            "valid_for_claim": "False",
        },
    ]


def requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "REQ3527_0_parent_curvature_norm",
            "required_object": "parent curvature norm",
            "mathematical_contract": "S_parent contains -C_P/4 int <F_parent,F_parent>_P and A_parent=A_Q T_Q + A_perp with fixed N_Q=<T_Q,T_Q>_P",
            "why_needed": "supplies lambda_A=C_P N_Q from parent data",
            "current_status": "CONDITIONAL_TEMPLATE",
            "if_missing": "lambda_A remains a free visible coefficient",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3527_1_no_extra_F2",
            "required_object": "operator-domain exhaustion",
            "mathematical_contract": "Allowed[S_vis] has no independent lambda_A F_Q^2, f_X F_Q^2 or radiative/readout F2 term outside parent generation",
            "why_needed": "kills the continuous-coupling no-go counterfamily",
            "current_status": "HARD_GATE_UNSIGNED",
            "if_missing": "C_XF2 bound branch mandatory",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3527_2_same_current_source",
            "required_object": "same T_Q Noether current and source denominator",
            "mathematical_contract": "J_Q=delta S_matter/delta A_Q with fixed Q_* and no c_A(X) current weights for source/test bodies",
            "why_needed": "turns alpha owner into WEP/R10/source-normalization owner",
            "current_status": "UNSIGNED",
            "if_missing": "vacuum alpha silence would not imply source-coupling silence",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3527_3_readout_radiative",
            "required_object": "readout/radiative preservation",
            "mathematical_contract": "observed alpha, clock/spectroscopy ratios and effective thresholds remain generated by the same parent owner",
            "why_needed": "protects measured alpha after reduction",
            "current_status": "UNSIGNED",
            "if_missing": "clock/spectroscopy alpha pressure can re-enter",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3527_4_calibrated_constant_fallback",
            "required_object": "explicit calibrated constant policy",
            "mathematical_contract": "if REQ3527_0..3 cannot be derived, alpha_EM is an explicit universal measured constant with C_XF2=0 adopted as a closure input, not a theorem",
            "why_needed": "GR itself uses calibrated constants; this keeps MTS testable without pretending all constants are derived",
            "current_status": "AVAILABLE_AS_NONDERIVED_FALLBACK",
            "if_missing": "project keeps circling alpha instead of testing local GR/source coupling",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3527_0_compact_U1",
            "quantity": "compact_U1_charge_lattice",
            "value": "partial_success",
            "meaning": "relative charge labels and dF=0 can be structurally supported",
            "claim_effect": "not enough to own alpha",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3527_1_no_go",
            "quantity": "compact_U1_plus_Noether_fixes_alpha",
            "value": "rejected",
            "meaning": "4D Maxwell admits a continuous gauge kinetic coefficient for every compact U(1) and conserved current",
            "claim_effect": "C_XF2 zero cannot come from this route alone",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3527_2_remaining_route",
            "quantity": "best_remaining_derivation_route",
            "value": "parent_curvature_norm_plus_unique_F2_domain",
            "meaning": "only a parent inheritance theorem plus no-extra-F2 domain can still derive the ratio rather than calibrate it",
            "claim_effect": "sets the next proof target cleanly",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3527_3_fallback",
            "quantity": "calibrated_constant_option",
            "value": "explicit_nonclaim_fallback",
            "meaning": "alpha may be carried as a universal measured constant like G in GR if derivation stalls, but must be labelled as closure/calibration",
            "claim_effect": "keeps the broader local GR/Newton derivation route alive without pretending alpha is derived",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3527_0_stop_compact_U1_loop",
            "decision": "stop using compact U(1) alone as an alpha derivation route",
            "rationale": "it fixes relative labels but leaves the 4D Maxwell kinetic coefficient continuous",
            "effect": "prevents another loop through the same coupling argument",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3527_1_focus_unique_F2_or_calibrate",
            "decision": "next either prove unique F2 parent-domain inheritance or make alpha an explicit calibrated constant",
            "rationale": "those are the only honest routes left after the no-go theorem",
            "effect": "keeps derivation-first pressure while acknowledging GR-style constants are legitimate if labelled",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3527_2_source_tests_wait",
            "decision": "do not score WEP/R10/clock as MTS predictions yet",
            "rationale": "source/current/readout projections still need C_XF2 transfer kernels or a theorem-zero owner",
            "effect": "finite bound branch stays ready but nonclaim",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3528-Y5-R2FR-unique-F2-parent-domain-inheritance-or-calibrated-alpha-constant-contract.md",
            "next_script": "scripts/Y5_R2FR_3528_unique_F2_parent_domain_inheritance_or_calibrated_alpha_constant_contract.py",
            "objective": "Try the last non-circular derivation route for alpha: prove parent curvature-norm inheritance with no independent F_Q^2 operator; if that cannot close, write the explicit calibrated-alpha constant contract so the local GR/Newton source programme can move without smuggling a theorem.",
            "success_gate": "Either independent F_Q^2 is parent-forbidden by a source-backed domain theorem, or alpha_EM is labelled as a measured universal closure constant with bound tests for any drift.",
            "why_next": "3527 rejects compact U(1)-only alpha derivation; only unique F2 inheritance or explicit calibration remains honest.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3527_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_1_compact_U1_partial_success", "passed": bool_text(any(row["theorem_id"] == "NG3527_0_compact_U1_success" and row["status"] == "PARTIAL_DERIVATION_SUCCESS" for row in no_go)), "detail": "compact U(1) support is retained, not dismissed", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_2_no_go_present", "passed": bool_text(any(row["theorem_id"] == "NG3527_1_continuous_coupling_no_go" and row["status"] == "DERIVED_NO_GO_FOR_COMPACT_U1_ONLY" for row in no_go) and any(row["quantity"] == "compact_U1_plus_Noether_fixes_alpha" and row["value"] == "rejected" for row in status)), "detail": "compact U(1)+Noether alpha derivation is rejected by explicit counterfamily", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_3_unique_F2_selected", "passed": bool_text(any(row["route_id"] == "RA3527_4_operator_domain" and row["verdict"] == "BEST_NEXT_DERIVATION_ROUTE" for row in routes)), "detail": "unique F2/domain inheritance selected as only remaining derivation route", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_4_countermodel_shortcut_killed", "passed": bool_text(any(row["countermodel_id"] == "CK3527_3_topological_shortcut" and row["still_alive"] == "False_as_shortcut" for row in countermodels) and any(row["countermodel_id"] == "CK3527_1_independent_F2" and row["still_alive"] == "True" for row in countermodels)), "detail": "topological shortcut rejected while independent F2 remains live", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_5_calibrated_fallback_declared", "passed": bool_text(any(row["requirement_id"] == "REQ3527_4_calibrated_constant_fallback" for row in requirements)), "detail": "calibrated-constant fallback is explicit rather than smuggled", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_6_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + no_go + routes + countermodels + requirements + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no alpha/local-GR/source-coupling claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3528-Y5-R2FR-unique-F2-parent-domain")), "detail": "3528 unique-F2-or-calibrated-alpha target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3527_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3527_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3527_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3527 - Charge Generator Level/Current Owner Or Alpha-Ratio Countermodel Kill

## Summary
- **Good news:** compact `U(1)` is useful. It supports relative integer charge labels and `F_Q=dA_Q`, so the EM structure is not arbitrary.
- **Hard result:** compact `U(1)` plus a conserved Noether current does **not** fix the 4D Maxwell kinetic coefficient. There is a continuous family of allowed `g_EM`.
- **Meaning:** the alpha/coupling owner cannot be derived from charge quantization alone. The missing piece is either a parent curvature norm plus no-extra-`F_Q^2` domain theorem, or an explicit calibrated-constant policy.
- **Countermodel killed:** the lazy shortcut “topology fixes alpha” is rejected. Real topology could help only if it inherits into the metric Maxwell `F_Q^2` term.
- **No claim:** `C_XF2=0` is still not live. The project now has a cleaner fork: prove unique F2 inheritance, or carry alpha as a measured universal constant like GR carries `G`.

## No-Go Core
For every positive real `g`,

`S_g = -1/(4g^2) int F_Q wedge *_obs F_Q + int A_Q wedge J_Q`

is gauge invariant when `dJ_Q=0`. Compactness quantizes representation labels, not the real coefficient `g^{-2}`. That is the coupling throat in one line.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## No-Go Theorem
{markdown_table(no_go, ["theorem_id", "claim_piece", "statement", "derivation", "result", "blocker_or_limit", "status", "valid_for_claim"])}

## Route Audit
{markdown_table(routes, ["route_id", "candidate_owner", "owns", "does_not_own", "current_evidence", "verdict", "source_path", "valid_for_claim"])}

## Countermodel Kill Matrix
{markdown_table(countermodels, ["countermodel_id", "countermodel", "killed_by_3527", "reason", "still_alive", "needed_to_kill", "valid_for_claim"])}

## Parent Principle Requirements
{markdown_table(requirements, ["requirement_id", "required_object", "mathematical_contract", "why_needed", "current_status", "if_missing", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    no_go = no_go_theorem_rows()
    routes = route_audit_rows()
    countermodels = countermodel_kill_rows()
    requirements = requirement_rows()
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3527_SOURCE_REGISTER.csv",
        "no_go_theorem": OUT / "P8_Y5_R2FR_3527_LEVEL_CURRENT_NO_GO_THEOREM.csv",
        "route_audit": OUT / "P8_Y5_R2FR_3527_ROUTE_AUDIT.csv",
        "countermodel_kill": OUT / "P8_Y5_R2FR_3527_COUNTERMODEL_KILL_MATRIX.csv",
        "requirements": OUT / "P8_Y5_R2FR_3527_PARENT_PRINCIPLE_REQUIREMENTS.csv",
        "status": OUT / "P8_Y5_R2FR_3527_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3527_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3527_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3527_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["no_go_theorem"], no_go, ["theorem_id", "claim_piece", "statement", "derivation", "result", "blocker_or_limit", "status", "valid_for_claim"])
    write_csv(outputs["route_audit"], routes, ["route_id", "candidate_owner", "owns", "does_not_own", "current_evidence", "verdict", "source_path", "valid_for_claim"])
    write_csv(outputs["countermodel_kill"], countermodels, ["countermodel_id", "countermodel", "killed_by_3527", "reason", "still_alive", "needed_to_kill", "valid_for_claim"])
    write_csv(outputs["requirements"], requirements, ["requirement_id", "required_object", "mathematical_contract", "why_needed", "current_status", "if_missing", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, no_go, routes, countermodels, requirements, status, decisions, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, no_go, routes, countermodels, requirements, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
