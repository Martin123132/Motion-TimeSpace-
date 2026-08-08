from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_821_SOURCE_REGISTER.csv"
CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_821_CONTROL_SCALAR_CANDIDATES.csv"
GATE_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_821_GATE_MATRIX.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_821_SELECTION_DECISION.csv"
OBLIGATIONS_PATH = RESIDUALS / "P8_Y5_R10_821_OPEN_PROOF_OBLIGATIONS.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_821_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_821_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_821_VALIDATION.csv"

STATUS = "Y5_R10_821_parent_control_scalar_hunt_primary_candidate_selected_nonclaim"
CLAIM_CEILING = "candidate_parent_control_scalar_selected_no_parent_derivation_no_data_run"
PRIMARY_CANDIDATE = "X821_0_coherent_load_exposure_IM"
SECONDARY_CANDIDATE = "X821_1_XB_firewall_wrapper"
NEXT_TARGET = "822-Y5-R10-C2A-coherent-load-tensor-parent-map-attempt.md"

SOURCE_SPECS = [
    {
        "source_id": "820_doc",
        "path": POST_CHECKPOINT / "820-Y5-R10-C2A-source-axiom-algebraic-stress-test.md",
        "needles": [
            "C2A_TS1 survives as useful algebra",
            "can reproduce any monotone target history",
            "821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md",
        ],
        "role": "immediate stress-test source selecting the parent-X hunt",
    },
    {
        "source_id": "820_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_820_VALIDATION.csv",
        "needles": [
            "V820_3_arbitrary_fit_inversion_flagged,pass",
            "V820_6_survival_conditions_complete,pass",
            "V820_8_next_target_selected,pass,821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "139_hazard_theorem",
        "path": POST_CHECKPOINT / "139-density-law-hazard-theorem-attempt.md",
        "needles": [
            "I_M = det(Q)",
            "Q^i_j = X delta^i_j",
            "additive exposure + survival composition -> exponential saturation.",
            "Q^i_j parent action;",
        ],
        "role": "coherent-load exposure and additive-hazard source",
    },
    {
        "source_id": "138_pressure_kernel",
        "path": POST_CHECKPOINT / "138-coherent-volume-pressure-kernel-theorem.md",
        "needles": [
            "N_D must be a real coherent-domain volume variable,",
            "the parent domain selector D;",
            "density law from parent | fail",
        ],
        "role": "coherent-volume pressure and domain-owner warning",
    },
    {
        "source_id": "143_domain_selector",
        "path": POST_CHECKPOINT / "143-domain-selector-variational-action-attempt.md",
        "needles": [
            "Q can be owned by coherent-volume load if D and u3 are derived.",
            "C_coh[D] =",
            "domain_selector_formal_action_not_parent_derived",
        ],
        "role": "domain selector and boundary-current obstruction",
    },
    {
        "source_id": "85_XB_bundle",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "If `X_B` is arbitrary",
            "X_B = {",
            "source-power closure open.",
        ],
        "role": "universal invariant/firewall candidate",
    },
    {
        "source_id": "12_parent_skeleton",
        "path": FORMALIZATION / "12-minimal-parent-theory-sketch.md",
        "needles": [
            "There exists a memory/exchange field:",
            "source(invariants of",
            "open-system memory dynamics",
        ],
        "role": "parent sketch source-law target",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check_needles(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_path"
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "X821_0_coherent_load_exposure_IM",
            "candidate_expression": "X_source = I_M = det(Q_coh); in isotropic FLRW Q^i_j = X_load delta^i_j so I_M = X_load^3",
            "source_paths": "139-density-law-hazard-theorem-attempt.md; 138-coherent-volume-pressure-kernel-theorem.md; 143-domain-selector-variational-action-attempt.md",
            "strength": "directly matches additive-hazard survival law and can explain p_source=3 conditionally",
            "blocker": "Q_coh, domain D, boundary current J_rel, u3, and B_mem are not parent-derived",
            "leakage_risk": "medium_without_D_and_local_firewall",
            "rank": "1_primary_candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "X821_1_XB_firewall_wrapper",
            "candidate_expression": "X_firewall = X_B bundle or a derived scalar function of {A_curv,E_theta,...,I_dotB,L_cg H_bg/c}",
            "source_paths": "85-coarse-graining-invariants-XB.md",
            "strength": "universal invariant framework for local/cosmology routing and anti-sector-tuning",
            "blocker": "L_cg, weights, thresholds, D_L factorization, and source powers remain open",
            "leakage_risk": "low_if_universal_high_if_retuned",
            "rank": "2_firewall_wrapper_not_primary_source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "X821_2_coherent_volume_time_ND",
            "candidate_expression": "X_source = N_D/u3 with N_D=(1/3)ln(V_D0/V_D)",
            "source_paths": "138-coherent-volume-pressure-kernel-theorem.md; 139-density-law-hazard-theorem-attempt.md",
            "strength": "simple monotone activation variable if coherent domain D is real; gives clean volume-pressure kernel",
            "blocker": "D selection and u3 normalization are not derived; time orientation/sign must be fixed",
            "leakage_risk": "medium",
            "rank": "3_component_of_primary_candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "X821_3_additive_hazard_integral",
            "candidate_expression": "X_source = integral h_parent dN, with F=1-exp(-X_source)",
            "source_paths": "139-density-law-hazard-theorem-attempt.md",
            "strength": "mathematically clean survival composition law",
            "blocker": "hazard density h_parent is arbitrary unless derived from Q_coh/domain/source invariants",
            "leakage_risk": "high_if_h_free",
            "rank": "4_formal_wrapper_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "X821_4_parent_invariant_source_scalar",
            "candidate_expression": "X_source = normalized functional of invariants of psi, T_matter, and curvature",
            "source_paths": "12-minimal-parent-theory-sketch.md",
            "strength": "closest to parent sketch language",
            "blocker": "not explicit, not signed, not monotone, and too broad to block fit inversion",
            "leakage_risk": "high_until_formula_exists",
            "rank": "5_require_formula_before_use",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "X821_5_Gamma_mem_self",
            "candidate_expression": "X_source = Gamma_mem or Delta Gamma_mem",
            "source_paths": "12-minimal-parent-theory-sketch.md",
            "strength": "available memory variable",
            "blocker": "circular as a source law for Gamma_mem unless a separate production functional is derived",
            "leakage_risk": "high_circularity",
            "rank": "6_reject_as_primary",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gate_matrix_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    gates = {
        "parent_formula": "explicit formula from parent/coarse-grained variables",
        "monotone_sign": "X>=0 and dX/dN>=0 on the intended branch",
        "endpoint_budget": "endpoint law supports honest total-budget interpretation",
        "shape_owner": "p_source or exponent follows from geometry rather than data",
        "local_firewall": "does not leak into local PPN/local-GR claims",
        "anti_fit_inversion": "cannot encode arbitrary monotone F_fit after seeing data",
    }
    scores = {
        "X821_0_coherent_load_exposure_IM": {
            "parent_formula": "partial",
            "monotone_sign": "open",
            "endpoint_budget": "open",
            "shape_owner": "partial",
            "local_firewall": "open",
            "anti_fit_inversion": "best_if_Q_and_D_predeclared",
        },
        "X821_1_XB_firewall_wrapper": {
            "parent_formula": "partial",
            "monotone_sign": "open",
            "endpoint_budget": "not_primary",
            "shape_owner": "open",
            "local_firewall": "best_candidate",
            "anti_fit_inversion": "good_if_universal_no_retuning",
        },
        "X821_2_coherent_volume_time_ND": {
            "parent_formula": "partial",
            "monotone_sign": "orientation_dependent",
            "endpoint_budget": "partial",
            "shape_owner": "partial_if_u3_derived",
            "local_firewall": "open",
            "anti_fit_inversion": "good_if_D_predeclared",
        },
        "X821_3_additive_hazard_integral": {
            "parent_formula": "missing_hazard_density",
            "monotone_sign": "by_definition_if_h_nonnegative",
            "endpoint_budget": "partial",
            "shape_owner": "missing",
            "local_firewall": "open",
            "anti_fit_inversion": "bad_if_h_free",
        },
        "X821_4_parent_invariant_source_scalar": {
            "parent_formula": "too_broad",
            "monotone_sign": "missing",
            "endpoint_budget": "missing",
            "shape_owner": "missing",
            "local_firewall": "missing",
            "anti_fit_inversion": "bad_until_formula_predeclared",
        },
        "X821_5_Gamma_mem_self": {
            "parent_formula": "circular",
            "monotone_sign": "unknown",
            "endpoint_budget": "unknown",
            "shape_owner": "circular",
            "local_firewall": "unknown",
            "anti_fit_inversion": "bad_circular",
        },
    }
    for candidate_id, gate_scores in scores.items():
        for gate_id, description in gates.items():
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "gate_id": gate_id,
                    "gate_description": description,
                    "gate_result": gate_scores[gate_id],
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )
    return rows


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D821_0",
            "decision": "select I_M=det(Q_coh) as the primary C2A source-control candidate",
            "primary_candidate": PRIMARY_CANDIDATE,
            "secondary_candidate": SECONDARY_CANDIDATE,
            "reason": "it is the only route that connects additive hazard, determinant shape, coherent volume pressure, and p_source=3 without immediately becoming an arbitrary F_fit inversion",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D821_1",
            "decision": "use X_B as the firewall/routing wrapper, not as the primary cosmology source",
            "primary_candidate": PRIMARY_CANDIDATE,
            "secondary_candidate": SECONDARY_CANDIDATE,
            "reason": "X_B is better suited to universal local/cosmology routing, while I_M owns the activation exposure if Q and D can be derived",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def obligation_rows(generated_utc: str) -> list[dict[str, object]]:
    obligations = [
        ("O821_0_Q_parent_action", "derive Q_coh or Q^i_j from parent MTS variables before FLRW reduction", "blocks determinant exposure from being an inserted tensor"),
        ("O821_1_domain_selector_D", "derive or predeclare the coherent domain D without outcome tuning", "prevents N_D and I_M from becoming fitted labels"),
        ("O821_2_boundary_current", "derive safe boundary/relative current J_rel or equivalent", "prevents moving-domain wall stress and local PPN hair"),
        ("O821_3_u3_cell_normalization", "derive u3=1/4 or keep it symbolic/stress-only", "prevents reusing the old locked shape constant as theorem"),
        ("O821_4_monotonicity_endpoints", "prove I_M>=0, dI_M/dN>=0, and endpoint budget conditions", "needed for positive normalized source"),
        ("O821_5_Bmem_budget", "derive, bound, or quarantine B_mem", "hazard law fixes shape, not amplitude"),
        ("O821_6_local_silence", "prove local N_D=0 and delta N_D=0 or equivalent local firewall", "needed before any R10/PPN/local-GR promotion"),
        ("O821_7_perturbation_action", "derive perturbation owner: sound speed/slip/source/growth response", "needed before CMB/growth claims"),
        ("O821_8_XB_wrapper", "map I_M branch through universal X_B routing without retuning", "keeps cosmology activation compatible with local screening discipline"),
    ]
    return [
        {
            "obligation_id": obligation_id,
            "requirement": requirement,
            "why_needed": why_needed,
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for obligation_id, requirement, why_needed in obligations
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "attempt the parent map Q_coh -> I_M -> FLRW X_source and list the exact clauses that fail",
            "allowed_work": "symbolic derivation, source audit, local/FLRW reduction clauses, no data",
            "forbidden_work": "SN/BAO/CMB/growth fitting, parent-derived claim, local-GR claim",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "primary_candidate": PRIMARY_CANDIDATE,
            "secondary_candidate": SECONDARY_CANDIDATE,
            "claim_ceiling": CLAIM_CEILING,
            "verdict": "best route is coherent-load exposure I_M as source control plus X_B as firewall wrapper",
            "missing": "Q parent action, domain selector, boundary current, u3, endpoints, B_mem, local silence, perturbations",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    candidates: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    obligations: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V821_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_820, clean_820_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_820_VALIDATION.csv")
    add("V821_1_prior_820_clean", clean_820, clean_820_detail)
    candidate_ids = {row["candidate_id"] for row in candidates}
    add(
        "V821_2_candidate_set_complete",
        {PRIMARY_CANDIDATE, SECONDARY_CANDIDATE, "X821_5_Gamma_mem_self"}.issubset(candidate_ids) and len(candidates) >= 6,
        "candidate ledger includes primary, firewall, and rejected circular option",
    )
    add(
        "V821_3_primary_selected",
        any(row["primary_candidate"] == PRIMARY_CANDIDATE for row in decisions),
        PRIMARY_CANDIDATE,
    )
    add(
        "V821_4_XB_secondary_wrapper_selected",
        any(row["secondary_candidate"] == SECONDARY_CANDIDATE for row in decisions),
        SECONDARY_CANDIDATE,
    )
    add(
        "V821_5_anti_fit_gate_recorded",
        any(row["gate_id"] == "anti_fit_inversion" and row["candidate_id"] == PRIMARY_CANDIDATE for row in gate_rows),
        "anti-fit inversion gate recorded for primary candidate",
    )
    required_obligations = {
        "O821_0_Q_parent_action",
        "O821_1_domain_selector_D",
        "O821_2_boundary_current",
        "O821_3_u3_cell_normalization",
        "O821_4_monotonicity_endpoints",
        "O821_5_Bmem_budget",
        "O821_6_local_silence",
        "O821_7_perturbation_action",
        "O821_8_XB_wrapper",
    }
    add(
        "V821_6_obligations_complete",
        required_obligations.issubset({row["obligation_id"] for row in obligations}),
        "proof obligations cover parent action, local firewall, amplitude, and perturbations",
    )
    add(
        "V821_7_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "selection remains non-runnable",
    )
    add(
        "V821_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + candidates + gate_rows + decisions + obligations + next_rows + summary
    add(
        "V821_9_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V821_10_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V821_11_validation_rows_ready", True, "validation table constructed")
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    candidates: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    obligations: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 821 - Y5 R10 C2A Parent Control-Scalar Candidate Hunt",
            (
                "Current result: **the best next source-control candidate is coherent-load exposure `I_M=det(Q_coh)`, with `X_B` retained as the universal firewall wrapper**. "
                "This does not derive the parent law. It narrows the next theorem target to the load tensor/domain map rather than letting `X(N)` float."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "primary_candidate", "secondary_candidate", "claim_ceiling", "verdict", "missing", "next_target", "valid_for_claim"]),
            "## Candidate Ledger\n\n" + markdown_table(candidates, ["candidate_id", "candidate_expression", "strength", "blocker", "leakage_risk", "rank", "valid_for_claim"]),
            "## Gate Matrix\n\n" + markdown_table(gate_rows, ["candidate_id", "gate_id", "gate_result", "valid_for_claim"]),
            "## Selection Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "primary_candidate", "secondary_candidate", "reason", "runnable", "next_target", "valid_for_claim"]),
            "## Open Proof Obligations\n\n" + markdown_table(obligations, ["obligation_id", "requirement", "why_needed", "status", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is a useful narrowing. We are no longer hunting every possible source scalar. The route to try next is specific: derive or reject the parent map `Q_coh -> I_M -> FLRW X_source`, while keeping `X_B` as the local/cosmology firewall wrapper. If that parent map fails, C2A remains closure-only.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    candidates = candidate_rows(generated_utc)
    gate_rows = gate_matrix_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    obligations = obligation_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, candidates, gate_rows, decisions, obligations, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CANDIDATES_PATH, candidates, ["candidate_id", "candidate_expression", "source_paths", "strength", "blocker", "leakage_risk", "rank", "valid_for_claim", "generated_utc"])
    write_csv(GATE_MATRIX_PATH, gate_rows, ["candidate_id", "gate_id", "gate_description", "gate_result", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "primary_candidate", "secondary_candidate", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OBLIGATIONS_PATH, obligations, ["obligation_id", "requirement", "why_needed", "status", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "primary_candidate", "secondary_candidate", "claim_ceiling", "verdict", "missing", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, candidates, gate_rows, decisions, obligations, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"821 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
