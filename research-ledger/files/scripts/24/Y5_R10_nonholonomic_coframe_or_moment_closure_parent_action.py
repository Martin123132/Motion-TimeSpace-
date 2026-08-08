from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md"
NEXT_TARGET = "789-Y5-R10-palatini-tetrad-GR-limit-with-MTS-exchange-contract.md"
STATUS = "Y5_R10_788_nonholonomic_coframe_route_gives_clean_GR_limit_contract_but_metric_ownership_not_derived"
CLAIM_CEILING = "parent_action_contract_only_no_adopted_tetrad_no_derived_metric_from_psi_no_local_GR_Newton_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_788_SOURCE_REGISTER.csv"
NONHOLONOMIC_GATE_PATH = RESIDUALS / "P8_Y5_R10_788_NONHOLONOMIC_COFRAME_GATE.csv"
MOMENT_CLOSURE_PATH = RESIDUALS / "P8_Y5_R10_788_MOMENT_CLOSURE_GATE.csv"
ACTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_788_PARENT_ACTION_CONTRACT_CANDIDATES.csv"
BRANCH_DECISION_PATH = RESIDUALS / "P8_Y5_R10_788_BRANCH_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_788_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_788_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_788_ADOPTED_NONHOLONOMIC_COFRAME.csv",
    RESIDUALS / "P8_Y5_R10_788_ADOPTED_MOMENT_CLOSURE.csv",
    RESIDUALS / "P8_Y5_R10_788_LOCAL_GR_REENTRY_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_788_NEWTON_LIMIT_PROOF.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    NONHOLONOMIC_GATE_PATH,
    MOMENT_CLOSURE_PATH,
    ACTION_CONTRACT_PATH,
    BRANCH_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "787_doc": {
        "path": POST_CHECKPOINT / "787-Y5-R10-multifield-pregeometry-rank-gate-or-independent-metric-branch-decision.md",
        "needles": ["Current result", "flat-pullback trap"],
        "role": "immediate 788 handoff",
    },
    "787_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_787_VALIDATION.csv",
        "needles": ["V787_5_N4_rank_full", "V787_9_flat_pullback_block"],
        "role": "prior validation guard",
    },
    "787_rank_gate": {
        "path": RESIDUALS / "P8_Y5_R10_787_MULTIFIELD_PREGEOMETRY_RANK_GATE.csv",
        "needles": ["MPR787_1_minimal_multifield_rank", "MPR787_5_rank_gate_verdict"],
        "role": "multifield rank gate",
    },
    "787_curvature_gate": {
        "path": RESIDUALS / "P8_Y5_R10_787_CURVATURE_INTEGRABILITY_GATE.csv",
        "needles": ["CIG787_0_flat_pullback_trap", "CIG787_1_nonholonomic_coframe"],
        "role": "curvature/integrability handoff",
    },
    "785_contract": {
        "path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_4_connection_from_coframe", "PMC785_7_GR_Newton_reduction"],
        "role": "coframe and GR/Newton contract",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["emergent or effective metric", "MTS parent theory -> effective GR"],
        "role": "unification spine and GR/Newton chain",
    },
    "postulates_18": {
        "path": FORMALIZATION / "18-sign-conventions-and-field-postulates.md",
        "needles": ["Einstein-Equation Convention", "T_total"],
        "role": "Einstein convention and exchange postulates",
    },
    "testing_145": {
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS -> GR -> Newton", "missing GR-limit theorem"],
        "role": "local GR-limit demand",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCE_SPECS.items()
    ]


def nonholonomic_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NHC788_0_exact_gradient_rejected",
            "object": "e^a_mu = partial_mu psi^a",
            "result": "rejected_as_full_GR_route",
            "reason": "with constant internal metric and invertible map it is locally a flat pullback, so curvature is not generic",
            "requirement_to_repair": "add nonholonomic coframe component, moment covariance, or independent tetrad",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "NHC788_1_nonholonomic_ansatz",
            "object": "e^a_mu = partial_mu X^a + A^a_mu",
            "result": "viable_contract",
            "reason": "A^a_mu with de^a != 0 can carry anholonomy and allow curved geometry rather than a coordinate pullback",
            "requirement_to_repair": "derive A^a_mu from MTS parent fields or declare it as independent tetrad distortion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "NHC788_2_torsion_gate",
            "object": "T^a = de^a + omega^a_b wedge e^b",
            "result": "must_be_owned",
            "reason": "nonholonomy is not automatically torsion in a spin-connection theory, but torsion must be zero, sourced, or bounded",
            "requirement_to_repair": "Palatini/Einstein-Cartan connection equation or torsion residual bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "NHC788_3_GR_limit_contract",
            "object": "S[e,omega,Phi_MTS,Psi]",
            "result": "cleanest_next_contract",
            "reason": "Palatini/tetrad action can recover GR if omega becomes Levi-Civita and MTS stress/exchange vanishes or is controlled",
            "requirement_to_repair": "write explicit local GR limit theorem with variation and exchange conditions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "NHC788_4_ownership_warning",
            "object": "e^a_mu",
            "result": "not_derived_from_psi",
            "reason": "a nonholonomic coframe solves curvature but risks becoming an independent metric in disguise",
            "requirement_to_repair": "parent derivation of e or accept independent metric/tetrad fallback honestly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def moment_closure_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MCG788_0_moment_metric",
            "object": "M_mu_nu = H_AB <D_mu psi^A D_nu psi^B>_cg",
            "result": "viable_but_unsigned",
            "reason": "a coarse-grained covariance can avoid exact-gradient flatness if it has independent evolution",
            "missing": "covariant averaging kernel, closure equation, positivity/signature rule, and stress tensor",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MCG788_1_closure_dynamics",
            "object": "D_t M_mu_nu or covariant moment equation",
            "result": "missing",
            "reason": "without dynamics the moment metric is another fitted tensor field",
            "missing": "parent kinetic equation or variational principle for moments",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MCG788_2_signature_control",
            "object": "Lorentzian domain of g=eta+L_*^2 M or g=e^T eta e",
            "result": "open",
            "reason": "moment covariance alone does not automatically give stable Lorentzian signature",
            "missing": "signature theorem or tetrad factorization with internal Lorentz metric",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MCG788_3_Bianchi_conservation",
            "object": "nabla_mu(T_matter+T_MTS)^mu_nu=0 or controlled Q_nu",
            "result": "missing",
            "reason": "a moment closure must respect Bianchi identities if it is to reduce to GR",
            "missing": "Ward identity/exchange current from covariant parent action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MCG788_4_verdict",
            "object": "moment closure route",
            "result": "promising_but_slower",
            "reason": "it preserves the motion-flow idea but needs more parent machinery than the tetrad GR-limit contract",
            "missing": "use after Palatini/tetrad local limit contract is written",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def action_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PAC788_0_palatini_tetrad_contract",
            "candidate_action": "S = (1/2 kappa) integral epsilon_abcd e^a e^b R^cd[omega] + S_MTS[e,omega,Phi] + S_matter[e,omega,Psi]",
            "GR_limit_condition": "delta_omega S sets torsion/nonmetricity to zero; delta_e S gives Einstein equation with total stress",
            "strength": "least_suspicious_local_GR_route",
            "weakness": "e is not derived from scalar psi; this is independent/effective tetrad unless parent derives it",
            "status": "next_contract_selected",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC788_1_distortion_owned_contract",
            "candidate_action": "e^a = dX^a + A^a with A^a sourced by MTS motion/memory variables",
            "GR_limit_condition": "A^a dynamics must produce allowed tetrad variations and reduce to Levi-Civita GR locally",
            "strength": "keeps motion/time/space ancestry",
            "weakness": "A^a source law and gauge symmetry are not written",
            "status": "candidate_not_adopted",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC788_2_moment_metric_contract",
            "candidate_action": "g_mu_nu = eta_mu_nu + L_*^2 M_mu_nu with M constrained to covariant MTS moments",
            "GR_limit_condition": "moment equations must induce EH-like dynamics or be constrained to standard metric sector",
            "strength": "closest to original gradient/motion intuition",
            "weakness": "closure and EH dynamics are not derived",
            "status": "candidate_not_adopted",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC788_3_independent_metric_contract",
            "candidate_action": "standard metric/tetrad GR sector plus MTS stress, memory, and exchange terms",
            "GR_limit_condition": "T_MTS and exchange residuals vanish/suppress in local regime, giving GR then Newton",
            "strength": "most defensible route under scrutiny",
            "weakness": "weakens claim that metric is fully derived from motion field",
            "status": "fallback_retained",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D788_0_reject_exact_gradient",
            "decision": "reject exact-gradient coframe as full GR route",
            "reason": "flat pullback trap blocks generic curvature",
            "result": "rejected_for_GR_ownership",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D788_1_select_palatini_contract",
            "decision": "write Palatini/tetrad GR-limit contract next",
            "reason": "it gives the cleanest exact route to GR/Newton while keeping MTS residuals explicit",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D788_2_keep_moment_route",
            "decision": "keep moment closure as a later derivation route",
            "reason": "it may preserve the original motion-flow intuition but needs a parent kinetic/closure theorem",
            "result": "retained_not_primary",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D788_3_no_adoption",
            "decision": "do not adopt any branch as proved",
            "reason": "none yet derives e/g from parent MTS fields and proves matter-frame blindness",
            "result": "not_adopted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "nonholonomic coframe/tetrad route is the cleanest way to carry curvature and recover GR, but unless the coframe is derived from MTS it is an independent/effective metric sector",
            "hard_blocker": "derive e or A from parent motion/time/space variables, or honestly use Palatini/tetrad GR sector plus explicit MTS exchange residuals",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    nonholonomic: list[dict[str, Any]],
    moment: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_787_clean = all(validation_clean(number) for number in range(665, 788))
    nonholonomic_complete = len(nonholonomic) == 5
    exact_gradient_rejected = any(row["gate_id"] == "NHC788_0_exact_gradient_rejected" and row["result"] == "rejected_as_full_GR_route" for row in nonholonomic)
    palatini_selected = any(row["gate_id"] == "NHC788_3_GR_limit_contract" and row["result"] == "cleanest_next_contract" for row in nonholonomic)
    ownership_warning = any(row["gate_id"] == "NHC788_4_ownership_warning" and row["result"] == "not_derived_from_psi" for row in nonholonomic)
    moment_complete = len(moment) == 5
    moment_missing_dynamics = any(row["gate_id"] == "MCG788_1_closure_dynamics" and row["result"] == "missing" for row in moment)
    contracts_complete = len(contracts) == 4
    next_contract_selected = any(row["contract_id"] == "PAC788_0_palatini_tetrad_contract" and row["status"] == "next_contract_selected" for row in contracts)
    no_adoption = any(row["decision_id"] == "D788_3_no_adoption" and row["result"] == "not_adopted" for row in decisions)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D788_1_select_palatini_contract" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, nonholonomic, moment, contracts, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V788_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V788_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V788_2_prior_665_787_clean", prior_665_787_clean, "665-787 validation rows have no failures"),
        ("V788_3_nonholonomic_complete", nonholonomic_complete, "nonholonomic coframe rows complete"),
        ("V788_4_exact_gradient_rejected", exact_gradient_rejected, "exact-gradient coframe rejected as full GR route"),
        ("V788_5_palatini_selected", palatini_selected, "Palatini/tetrad contract selected as next derivation"),
        ("V788_6_ownership_warning", ownership_warning, "coframe ownership warning recorded"),
        ("V788_7_moment_complete", moment_complete, "moment closure rows complete"),
        ("V788_8_moment_missing_dynamics", moment_missing_dynamics, "moment closure dynamics missing"),
        ("V788_9_contracts_complete", contracts_complete, "parent action contract candidate rows complete"),
        ("V788_10_next_contract_selected", next_contract_selected, "Palatini/tetrad candidate selected"),
        ("V788_11_no_adoption", no_adoption, "no branch adopted as proved"),
        ("V788_12_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V788_13_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V788_14_claim_artifacts_absent", claim_artifacts_absent, "no adopted-coframe/moment/local-GR/Newton claim artifact fabricated"),
        ("V788_15_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V788_16_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V788_17_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    nonholonomic: list[dict[str, Any]],
    moment: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 788 - Y5 R10 Nonholonomic Coframe Or Moment Closure Parent Action

Current result: **the exact-gradient route is rejected as a full GR derivation, but the nonholonomic coframe route gives a clean local-GR contract**. The honest price is that the coframe becomes an independent/effective metric object unless the parent MTS theory derives it. The moment-closure route keeps more of the original motion-flow intuition, but it needs a real covariant closure equation before it can compete.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Nonholonomic Coframe Gate

{markdown_table(nonholonomic, ["gate_id", "object", "result", "reason", "requirement_to_repair", "valid_for_claim"])}

## Moment Closure Gate

{markdown_table(moment, ["gate_id", "object", "result", "reason", "missing", "valid_for_claim"])}

## Parent Action Contract Candidates

{markdown_table(contracts, ["contract_id", "candidate_action", "GR_limit_condition", "strength", "weakness", "status", "valid_for_claim"])}

## Branch Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

The best route now is not to pretend the scalar gradient metric has magically become GR. The serious route is to write the Palatini/tetrad local-limit theorem: if the coframe and connection obey the standard variational equations and the MTS residual stress/exchange switches off locally, GR and then Newton follow. That does not finish the deeper derivation of the coframe from MTS, but it gives the exact contract the parent action must satisfy.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    nonholonomic = nonholonomic_gate_rows(generated_utc)
    moment = moment_closure_rows(generated_utc)
    contracts = action_contract_rows(generated_utc)
    decisions = branch_decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, nonholonomic, moment, contracts, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(NONHOLONOMIC_GATE_PATH, nonholonomic, ["gate_id", "object", "result", "reason", "requirement_to_repair", "valid_for_claim", "generated_utc"])
    write_csv(MOMENT_CLOSURE_PATH, moment, ["gate_id", "object", "result", "reason", "missing", "valid_for_claim", "generated_utc"])
    write_csv(ACTION_CONTRACT_PATH, contracts, ["contract_id", "candidate_action", "GR_limit_condition", "strength", "weakness", "status", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, nonholonomic, moment, contracts, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"788 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
