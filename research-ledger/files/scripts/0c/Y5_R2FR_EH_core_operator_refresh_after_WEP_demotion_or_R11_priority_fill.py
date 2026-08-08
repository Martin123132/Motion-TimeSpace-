from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1708"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1708-Y5-R2FR-EH-core-operator-refresh-after-WEP-demotion-or-R11-priority-fill.md"

SOURCE_FILES = {
    "1707_doc": ROOT / "1707-Y5-R2FR-local-GR-remaining-gates-rollup-after-WEP-demotion.md",
    "1707_validation": OUT / "P8_Y5_BRR545_1707_VALIDATION.csv",
    "1707_next": OUT / "P8_Y5_PARENT_QLOC_1707_NEXT_TARGET.csv",
    "1707_gate_rollup": OUT / "P8_Y5_PARENT_QLOC_1707_LOCAL_GR_GATE_ROLLUP.csv",
    "958_doc": ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
    "958_validation": OUT / "P8_Y5_BRR545_958_VALIDATION.csv",
    "1512_doc": ROOT / "1512-Y5-parent-EH-operator-selection-theorem-or-nonEH-residual-vector.md",
    "1512_validation": OUT / "P8_Y5_BRR545_1512_VALIDATION.csv",
    "1512_premises": OUT / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
    "1512_vector": OUT / "P8_Y5_PARENT_EH_1512_NON_EH_RESIDUAL_VECTOR.csv",
    "1692_doc": ROOT / "1692-Y5-R2FR-EH-source-owner-or-R11-beta-vector-current-branch.md",
    "1692_validation": OUT / "P8_Y5_BRR545_1692_VALIDATION.csv",
    "1692_owner": OUT / "P8_Y5_PARENT_QLOC_1692_EH_SOURCE_OWNER_GATE.csv",
    "1692_r11_gate": OUT / "P8_Y5_PARENT_QLOC_1692_R11_BETA_LEAKAGE_GATE.csv",
    "1692_cr2_bridge": OUT / "P8_Y5_PARENT_QLOC_1692_CR2_QNORM_COEFFICIENT_BRIDGE.csv",
}

NEEDLES = {
    "1707_doc": ["EH/operator selection or executable R11/nonEH residual vector", "NEXT1707_0_primary"],
    "1707_validation": ["VAL1707_OVERALL", "PASS"],
    "1707_next": ["1708-Y5-R2FR-EH-core-operator-refresh-after-WEP-demotion-or-R11-priority-fill.md", "selected"],
    "1707_gate_rollup": ["LGG1707_3_EH_operator", "NOT_PARENT_DERIVED_HIGHEST_UPSTREAM"],
    "958_doc": ["EH-core operator selection theorem", "not_parent_derived_current_corpus"],
    "958_validation": ["V958_8_next_target_selected", "pass"],
    "1512_doc": ["PRE1512_2_second_order", "NON_EH_VECTOR_REQUIRED"],
    "1512_validation": ["VAL1512_11_overall", "PASS"],
    "1512_premises": ["PRE1512_2_second_order", "CENTRAL_BLOCKER_NOT_DERIVED"],
    "1512_vector": ["R2_fR_scalar_mode", "RETAINED_NON_EH_RESIDUAL"],
    "1692_doc": ["FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED", "fixed-L0 double-zero"],
    "1692_validation": ["VAL1692_OVERALL", "PASS"],
    "1692_owner": ["OWNG1692_5_verdict", "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED"],
    "1692_r11_gate": ["R11G1692_1_R2FR", "FIRST_COMPONENT_OPEN"],
    "1692_cr2_bridge": ["CBR1692_0_effective_cR2", "Q_norm"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1708_SOURCE_REGISTER.csv"
EH_PREMISE_REFRESH = OUT / "P8_Y5_PARENT_QLOC_1708_EH_PARENT_PREMISE_REFRESH.csv"
EH_THEOREM_RESULT = OUT / "P8_Y5_PARENT_QLOC_1708_EH_THEOREM_RESULT.csv"
R11_FILL_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1708_R11_PRIORITY_FILL_CONTRACT.csv"
WEP_DEMOTION_IMPACT = OUT / "P8_Y5_PARENT_QLOC_1708_WEP_DEMOTION_IMPACT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1708_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1708_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1708_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1708_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    EH_PREMISE_REFRESH,
    EH_THEOREM_RESULT,
    R11_FILL_CONTRACT,
    WEP_DEMOTION_IMPACT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    EH_PREMISE_REFRESH,
    EH_THEOREM_RESULT,
    R11_FILL_CONTRACT,
    WEP_DEMOTION_IMPACT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    EH_PREMISE_REFRESH: [
        QUARANTINE / "EH_PARENT_PREMISE_REFRESH.csv",
        BRANCH_RESIDUALS / "R2FR_EH_parent_premise_refresh_1708.csv",
        QUEUE / "JR1708_EH_PARENT_PREMISE_REFRESH.csv",
    ],
    EH_THEOREM_RESULT: [
        QUARANTINE / "EH_THEOREM_RESULT.csv",
        BRANCH_RESIDUALS / "R2FR_EH_theorem_result_1708.csv",
        QUEUE / "JR1708_EH_THEOREM_RESULT.csv",
    ],
    R11_FILL_CONTRACT: [
        QUARANTINE / "R11_PRIORITY_FILL_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_R11_priority_fill_contract_1708.csv",
        QUEUE / "JR1708_R11_PRIORITY_FILL_CONTRACT.csv",
    ],
    WEP_DEMOTION_IMPACT: [
        QUARANTINE / "WEP_DEMOTION_IMPACT.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_demotion_impact_1708.csv",
        QUEUE / "JR1708_WEP_DEMOTION_IMPACT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1708.csv",
        QUEUE / "JR1708_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1708.csv",
        QUEUE / "JR1708_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _field in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1708_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1708": "EH/operator refresh after WEP split demotion and R11 priority fill selection",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def eh_premise_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EHP1708_0_local_4D",
            "local 4D compact exterior branch",
            "STRUCTURAL_TARGET_NOT_PARENT_SIGNED",
            "no change from WEP demotion",
            "parent must define the exterior reduction domain before Lovelock-style reasoning applies",
            8,
        ),
        (
            "EHP1708_1_metric_only",
            "metric-only observed exterior action",
            "NOT_PARENT_DERIVED",
            "no change from WEP demotion",
            "exclude or residualize scalar, vector, domain, projector, memory, coframe and connection carriers",
            12,
        ),
        (
            "EHP1708_2_second_order",
            "second-order metric equations through local tested scales",
            "CENTRAL_BLOCKER_NOT_DERIVED",
            "no change from WEP demotion",
            "prove no higher-derivative tower or fill R2/fR and Ricci/Weyl residual coefficients",
            13,
        ),
        (
            "EHP1708_3_Levi_Civita",
            "observed connection is Levi-Civita and universal",
            "NOT_PARENT_DERIVED",
            "no change from WEP demotion",
            "prove torsion/nonmetricity silence or fill connection-response residual rows",
            12,
        ),
        (
            "EHP1708_4_no_extra_fields",
            "no extra local stress/charge carriers",
            "ACTIVE_PRIMARY_OBSTRUCTION",
            "no change from WEP demotion",
            "prove gauge/topological/no-hair silence or retain finite residual rows",
            13,
        ),
        (
            "EHP1708_5_boundary_harmless",
            "boundary/topological terms carry no local stress, flux, radial hair or preferred-location signal",
            "CONDITIONAL_NOT_DERIVED",
            "no change from WEP demotion",
            "prove no-flux/topological harmlessness or fill boundary residual coefficients",
            10,
        ),
        (
            "EHP1708_6_parent_minimality",
            "primitive no-natural-marker/no-extension/no-higher-derivative minimality",
            "THEOREM_NOT_PROVEN",
            "now selected as highest theorem attempt",
            "one theorem could remove R2/fR, Ricci/Weyl, marker and integrated-out tower leakage at once",
            14,
        ),
        (
            "EHP1708_7_acceptance",
            "EH operator claim",
            "BLOCKED",
            "still blocked after WEP split demotion",
            "all premises must be parent-signed or each failed premise must be residualized with source-backed rows",
            15,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "premise_id": premise_id,
            "premise": premise,
            "current_status": status,
            "wep_demotion_effect": effect,
            "required_to_promote": required,
            "priority_score": priority,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for premise_id, premise, status, effect, required, priority in rows
    ]


def eh_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EHT1708_0_conditional_lovelock_route",
            "If the local exterior branch is 4D, local, diffeomorphism-invariant, metric-only, Levi-Civita and second-order, then the surviving operator is EH plus Lambda/topological boundary.",
            "EXACT_CONDITIONAL_ROUTE",
            "PREMISES_NOT_PARENT_SIGNED",
            "keep as theorem target, not current evidence",
        ),
        (
            "EHT1708_1_wep_demotion_guard",
            "Demoting the WEP split route removes a source-side shortcut but does not damage the left-hand EH theorem route.",
            "ROUTE_CLEANUP",
            "LEFT_HAND_OPERATOR_STILL_OPEN",
            "do not use WEP to promote or reject EH",
        ),
        (
            "EHT1708_2_owner_gate",
            "A single parent action must own the EH-like operator, matter coupling, boundary policy, source normalization and all residual sectors.",
            "OWNER_CONTRACT_REQUIRED",
            "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "avoid importing GR as an MTS proof",
        ),
        (
            "EHT1708_3_verdict",
            "EH operator selection remains mathematically plausible but not derived; R11/non-EH residuals stay live.",
            "NO_EH_CLAIM",
            "R11_PRIORITY_FILL_REQUIRED_IF_THEOREM_FAILS",
            "next attack primitive minimality/no-higher-derivative or first executable R11 component",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "result": result,
            "current_parent_status": status,
            "next_action": next_action,
            "theorem_proven": False,
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, result, status, next_action in rows
    ]


def r11_fill_rows() -> list[dict[str, Any]]:
    required_fields = ";".join(
        [
            "coefficient_symbol",
            "coefficient_value_or_zero_theorem",
            "units",
            "normalization",
            "parent_source_path",
            "weak_field_map",
            "observable_response_map",
            "arena_bound_source",
            "no_cancellation_guard",
            "valid_for_claim_false_until_checked",
        ]
    )
    rows = [
        (
            "R11F1708_0_R2_fR",
            "R2_fR_scalar_mode",
            "c_R2_eff or f_RR",
            "HIGHEST_FIRST",
            "prove primitive no-higher-derivative/minimality or fill finite scalar-mode coefficient row",
            "PPN_gamma_beta;R10_alpha_lambda;clock_orbital_range_terms",
            "1512_vector;1692_cr2_bridge",
        ),
        (
            "R11F1708_1_torsion_nonmetricity",
            "torsion_nonmetricity",
            "c_T or c_Q",
            "HIGHEST_FIRST",
            "prove Levi-Civita observed connection or fill torsion/nonmetricity response row",
            "WEP;clocks;light_cone;PPN_preferred_frame;spin_source",
            "1512_vector;958_doc",
        ),
        (
            "R11F1708_2_Ricci_Weyl",
            "Ricci_Weyl_squared",
            "c_Ricci or c_Weyl",
            "HIGH",
            "prove topological safe case or fill weak-field response coefficient row",
            "PPN_beta_gamma;wave_sector;preferred_location",
            "1512_vector;1692_r11_gate",
        ),
        (
            "R11F1708_3_boundary",
            "boundary_topological_terms",
            "c_boundary or c_GB",
            "HIGH",
            "prove no-flux/topological harmlessness or fill boundary charge/stress row",
            "mass_charge;PPN_alpha3_xi;radial_hair;Gdot",
            "1512_vector;958_doc",
        ),
        (
            "R11F1708_4_source_normalization",
            "source_normalization_operator",
            "epsilon_SN or c_domain_source_normalization",
            "HIGH",
            "prove constant source normalization and measured-GM lock or fill finite source denominator row",
            "Newton_GM;WEP;PPN_beta;orbital",
            "1512_vector;1692_owner",
        ),
        (
            "R11F1708_5_qnorm_projector_domain",
            "projector_domain_stress_and_q_loc_Qnorm",
            "Q_norm components",
            "HIGH",
            "close Gamma/Khat/Ploc owner bundle or fill Q_alg/Q_cdb/Q_mem/Q_bdy/Q_trans/Q_proj rows",
            "Cassini_gamma;PPN;local_GR_residual",
            "1692_cr2_bridge;1707_gate_rollup",
        ),
        (
            "R11F1708_6_vector_preferred_frame",
            "vector_preferred_frame",
            "c_domain_vector or selector_marker",
            "MEDIUM_HIGH",
            "prove no preferred-frame vector survives or fill alpha1/alpha2/alpha3 response row",
            "PPN_alpha_i;xi;clock_orbital",
            "1512_vector;958_doc",
        ),
        (
            "R11F1708_7_nonlocal_memory",
            "nonlocal_memory_kernel",
            "c_nonlocal or K_norm",
            "MEDIUM",
            "prove compact local memory silence or fill kernel norm/source row",
            "PPN;clocks;orbital;R10_range",
            "1512_vector;1692_cr2_bridge",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": fill_id,
            "operator_family": family,
            "coefficient_symbol": coefficient,
            "priority": priority,
            "first_required_action": action,
            "arena_links": arenas,
            "source_cluster": source_cluster,
            "required_fields": required_fields,
            "current_status": "CONTRACT_READY_NONCLAIM",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for fill_id, family, coefficient, priority, action, arenas, source_cluster in rows
    ]


def wep_impact_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WDI1708_0_split_removed",
            "Delta_w_TiPt*tau_WEP split route",
            "DEMOTED_TO_DIAGNOSTIC_ONLY",
            "removes a weak shortcut; does not affect EH theorem premises",
        ),
        (
            "WDI1708_1_direct_product_retained",
            "P_WEP_source_weight direct product",
            "LIVE_NONCLAIM_EXTERNAL_OR_PARENT_INPUTS_BLOCKED",
            "keeps WEP as empirical/source-side pillar, not left-hand GR proof",
        ),
        (
            "WDI1708_2_operator_priority",
            "EH/operator route",
            "UNCHANGED_HIGHEST_UPSTREAM",
            "EH/R11 remains best route because Newton/PPN/GM depend on operator ownership",
        ),
        (
            "WDI1708_3_public_posture",
            "claim posture",
            "NO_CLAIM",
            "source-side cleanup is progress, but no local-GR/Newton claim is promoted",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": impact_id,
            "object": obj,
            "post_1706_status": status,
            "effect_on_1708": effect,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for impact_id, obj, status, effect in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1708_0_EH_claim",
            "claim EH operator selected",
            "REJECT_EH_CLAIM",
            "premises remain parent-unsigned after 1707/1512/1692",
        ),
        (
            "RUN1708_1_local_GR",
            "claim derived local GR/Newton",
            "BLOCKED_NO_CLAIM",
            "EH, extra-sector silence, source normalization, measured-GM and PPN vector gates remain open",
        ),
        (
            "RUN1708_2_R11_score",
            "score R11/non-EH residual vector",
            "REJECT_R11_SCORE",
            "priority rows are contracts only; coefficient values, units, response maps and source bounds are not filled",
        ),
        (
            "RUN1708_3_WEP_shortcut",
            "use WEP split demotion as EH evidence",
            "REJECT_ROUTE_MIXING",
            "WEP is source/empirical branch; left-hand operator proof must stand independently",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "score_emitted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT1708_0_primary",
            "1709-Y5-R2FR-primitive-minimality-no-higher-derivative-or-first-R11-component-fill.md",
            "scripts/Y5_R2FR_primitive_minimality_no_higher_derivative_or_first_R11_component_fill.py",
            "try to prove primitive no-natural-marker/no-extension/no-higher-derivative minimality; if it fails, fill the first executable R2/fR and torsion/nonmetricity residual component rows",
            "selected",
        ),
        (
            "NEXT1708_1_parallel_Qnorm",
            "1709b-Y5-R2FR-Qnorm-projector-domain-component-fill.md",
            "scripts/Y5_R2FR_Qnorm_projector_domain_component_fill.py",
            "fill Q_norm/projector/domain components if the operator theorem route stalls",
            "held_parallel",
        ),
        (
            "NEXT1708_2_empirical_R10",
            "1709c-Y5-R2FR-R10-alpha-lambda-projection-fill-after-EH-refresh.md",
            "scripts/Y5_R2FR_R10_alpha_lambda_projection_fill_after_EH_refresh.py",
            "return to R10 empirical projection only after the operator/residual branch has a component to test",
            "held_empirical_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "success_condition": "theorem closes with parent-signed premises or first R11 component rows become source-backed nonclaim inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CG1708_0_EH",
            "MTS parent selects EH+Lambda exterior operator",
            "BLOCKED_NO_CLAIM",
            "metric-only, second-order, Levi-Civita, no-extra-field and no-flux premises remain unsigned",
        ),
        (
            "CG1708_1_R11_zero",
            "R11/non-EH vector theorem-zeros",
            "BLOCKED_NO_CLAIM",
            "minimality/no-higher-derivative theorem not proven and first component rows are not source-backed",
        ),
        (
            "CG1708_2_Newton",
            "Newtonian mechanics derived locally",
            "BLOCKED_NO_CLAIM",
            "measured-GM/worldtube and source-normalization remain downstream of EH/operator ownership",
        ),
        (
            "CG1708_3_PPN",
            "PPN vector reaches GR",
            "BLOCKED_NO_CLAIM",
            "response/tail split and R11/Qnorm components remain open",
        ),
        (
            "CG1708_4_WEP",
            "WEP branch passes",
            "BLOCKED_NO_CLAIM",
            "split route demoted; direct product retained but data/parent inputs are absent",
        ),
        (
            "CG1708_5_local_GR",
            "derived local GR/Newton reduction",
            "BLOCKED_NO_CLAIM",
            "operator, source, GM, PPN and finite residual branches are not closed together",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def parse_all(paths: list[Path]) -> bool:
    for path in paths:
        read_csv(path)
    return True


def claim_flags_false(paths: list[Path]) -> bool:
    allowed_truthy_keys = {"exists", "needles_present"}
    checked_keys = {
        "accepted_for_scoring",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "theorem_proven",
        "gate_pass",
        "score_emitted",
        "parent_signed",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in allowed_truthy_keys:
                    continue
                if key in checked_keys and truthy(value):
                    return False
    return True


def formalization_1708_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [
        path
        for path in FORMALIZATION.rglob("*1708*")
        if path.is_file() and ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    source_rows: list[dict[str, Any]],
    premise_rows_: list[dict[str, Any]],
    theorem_rows_: list[dict[str, Any]],
    r11_rows: list[dict[str, Any]],
    wep_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    remove_pycache()
    checks = [
        (
            "VAL1708_0_sources_exist",
            all(row["exists"] for row in source_rows),
            "all cited source paths exist",
        ),
        (
            "VAL1708_1_needles_present",
            all(row["needles_present"] for row in source_rows),
            "required source needles are present",
        ),
        (
            "VAL1708_2_premise_refresh_complete",
            len(premise_rows_) >= 8 and any(row["premise_id"] == "EHP1708_2_second_order" for row in premise_rows_),
            "EH parent premise refresh includes second-order/no-extra-field gates",
        ),
        (
            "VAL1708_3_EH_not_claimed",
            any(row["theorem_id"] == "EHT1708_3_verdict" and row["result"] == "NO_EH_CLAIM" for row in theorem_rows_),
            "EH theorem remains conditional/nonclaim",
        ),
        (
            "VAL1708_4_R11_contract_prioritized",
            len(r11_rows) >= 8
            and r11_rows[0]["operator_family"] == "R2_fR_scalar_mode"
            and r11_rows[1]["operator_family"] == "torsion_nonmetricity",
            "R11 fill contract prioritizes R2/fR and torsion/nonmetricity first",
        ),
        (
            "VAL1708_5_WEP_integrated_as_guard",
            any(row["impact_id"] == "WDI1708_2_operator_priority" for row in wep_rows),
            "WEP demotion impact recorded without route mixing",
        ),
        (
            "VAL1708_6_runner_blocks",
            all("CLAIM" in row["status"] or "REJECT" in row["status"] for row in runner_rows),
            "runner refuses EH/local-GR/R11/WEP shortcut scoring",
        ),
        (
            "VAL1708_7_next_selected",
            any(row["route_id"] == "NEXT1708_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects primitive minimality or first R11 component fill",
        ),
        (
            "VAL1708_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows),
            "all claim gates remain blocked",
        ),
        (
            "VAL1708_9_csv_parse",
            parse_all(GENERATED_CSVS),
            "all generated 1708 CSVs parse",
        ),
        (
            "VAL1708_10_no_claim_flags",
            claim_flags_false(CLAIM_CHECKED_CSVS),
            "all generated scoring and claim flags remain false",
        ),
        (
            "VAL1708_11_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets),
            "branch/quarantine/queue copies exist",
        ),
        (
            "VAL1708_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1708_13_formalization_untouched",
            not formalization_1708_hits(),
            "no 1708 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1708_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1708 EH refresh after WEP demotion and R11 priority fill contract validation",
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    premise_rows_: list[dict[str, Any]],
    theorem_rows_: list[dict[str, Any]],
    r11_rows: list[dict[str, Any]],
    wep_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    content = "\n\n".join(
        [
            "# 1708 - EH Core Operator Refresh After WEP Demotion Or R11 Priority Fill",
            "## Verdict\n"
            "- 1708 reopens the left-hand GR bridge after the WEP split route was demoted.\n"
            "- The result is not grim, but it is strict: EH is still a real conditional route, not a derived MTS theorem.\n"
            "- WEP cleanup does not hurt the theory; it simply stops a source-side shortcut from masquerading as an operator proof.\n"
            "- The best next move is primitive minimality/no-higher-derivative/no-natural-marker. If that fails, fill the first executable R11 rows.\n"
            "- No EH, Newton, PPN, R10, WEP or local-GR claim is made.",
            "## Source Register\n"
            + table(
                source_rows,
                ["source_id", "source_key", "source_path", "exists", "needles_present"],
            ),
            "## EH Parent Premise Refresh\n"
            + table(
                premise_rows_,
                [
                    "premise_id",
                    "premise",
                    "current_status",
                    "wep_demotion_effect",
                    "required_to_promote",
                    "priority_score",
                ],
            ),
            "## EH Theorem Result\n"
            + table(
                theorem_rows_,
                ["theorem_id", "statement", "result", "current_parent_status", "next_action"],
            ),
            "## R11 Priority Fill Contract\n"
            + table(
                r11_rows,
                [
                    "fill_id",
                    "operator_family",
                    "coefficient_symbol",
                    "priority",
                    "first_required_action",
                    "arena_links",
                    "current_status",
                ],
            ),
            "## WEP Demotion Impact\n"
            + table(wep_rows, ["impact_id", "object", "post_1706_status", "effect_on_1708"]),
            "## Runner Refusal\n"
            + table(runner_rows, ["runner_id", "case", "status", "reason"]),
            "## Next Target\n"
            + table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status"]),
            "## Claim Gates\n" + table(claim_rows, ["claim_id", "claim", "status", "reason"]),
            "## Validation\n" + table(validation_rows_, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "We have not got local GR yet, but the fog has thinned. The theory now has a sharp fork: either the parent action earns EH by minimality/second-order/no-extra-field clauses, or MTS becomes a finite-residual competitor with explicit R11 coefficients. That is a serious route, not waffle, but it is still a route under construction.",
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    premise_rows_ = eh_premise_rows()
    theorem_rows_ = eh_theorem_rows()
    r11_rows = r11_fill_rows()
    wep_rows = wep_impact_rows()
    runner_rows = runner_refusal_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(EH_PREMISE_REFRESH, premise_rows_)
    write_csv(EH_THEOREM_RESULT, theorem_rows_)
    write_csv(R11_FILL_CONTRACT, r11_rows)
    write_csv(WEP_DEMOTION_IMPACT, wep_rows)
    write_csv(RUNNER_REFUSAL, runner_rows)
    write_csv(NEXT_TARGET, next_rows)
    write_csv(CLAIM_GATE, claim_rows)
    copy_outputs()

    validation_rows_ = validation_rows(
        source_rows,
        premise_rows_,
        theorem_rows_,
        r11_rows,
        wep_rows,
        runner_rows,
        next_rows,
        claim_rows,
    )
    write_csv(VALIDATION, validation_rows_)
    write_doc(
        source_rows,
        premise_rows_,
        theorem_rows_,
        r11_rows,
        wep_rows,
        runner_rows,
        next_rows,
        claim_rows,
        validation_rows_,
    )

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"1708 validation {validation_rows_[-1]['result']}")


if __name__ == "__main__":
    main()
