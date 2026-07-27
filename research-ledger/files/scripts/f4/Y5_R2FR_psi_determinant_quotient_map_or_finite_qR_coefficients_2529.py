from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_PSI_DETERMINANT_QUOTIENT_OR_QR_FINITE_2529"
CHECKPOINT_ID = "2529"
DOC = ROOT / "2529-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_SOURCE_REGISTER.csv",
    "determinant_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_PSI_DETERMINANT_QUOTIENT_GATE.csv",
    "psi_lift_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_PSI_LIFT_AND_CARRIER_AUDIT.csv",
    "finite_qr_contract": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_FINITE_QR_COEFFICIENT_CONTRACT.csv",
    "q_source_vector_import": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_Q_SOURCE_VECTOR_IMPORT.csv",
    "first_dangerous_row": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_FIRST_DANGEROUS_BQWEYL_ROW.csv",
    "claim_gates": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_CLAIM_GATES.csv",
    "refusal_runner": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_REFUSAL_RUNNER.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2529_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2529_VALIDATION.csv",
}

BRANCH_COPIES = {
    "determinant_gate": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Psi_determinant_quotient_gate_2529_NONCLAIM.csv",
    "finite_qr_contract": ROOT
    / "source-intake"
    / "local_bounds"
    / "Finite_qR_coefficient_contract_2529_NONCLAIM.csv",
    "first_dangerous_row": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "BQWEYL2529_FIRST_DANGEROUS_ROW_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "BQWEYL2529_NEXT_TARGET_NONCLAIM.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
        **row,
    }


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
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


SOURCE_SPECS = [
    {
        "source_id": "SRC2529_0_2528_doc",
        "source_path": "2528-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md",
        "needle": "NEXT2528_0_selected",
        "role": "current handoff selecting psi determinant / quotient route",
    },
    {
        "source_id": "SRC2529_1_2528_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2528_VALIDATION.csv",
        "needle": "VAL2528_OVERALL,PASS",
        "role": "2528 validation anchor",
    },
    {
        "source_id": "SRC2529_2_2362_doc",
        "source_path": "2362-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md",
        "needle": "DQG2362_6_verdict",
        "role": "psi determinant quotient precedent",
    },
    {
        "source_id": "SRC2529_3_2362_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2362_VALIDATION.csv",
        "needle": "VAL2362_OVERALL,PASS",
        "role": "2362 validation anchor",
    },
    {
        "source_id": "SRC2529_4_2363_doc",
        "source_path": "2363-Y5-R2FR-finite-qR-coefficient-source-pack-or-selector-reentry.md",
        "needle": "CSP2363_8_verdict",
        "role": "finite q_R coefficient/source-pack precedent",
    },
    {
        "source_id": "SRC2529_5_2363_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2363_VALIDATION.csv",
        "needle": "VAL2363_OVERALL,PASS",
        "role": "2363 validation anchor",
    },
    {
        "source_id": "SRC2529_6_2364_doc",
        "source_path": "2364-Y5-R2FR-q-source-vector-normal-form-or-first-finite-bound-row.md",
        "needle": "SLOT2364_6_verdict",
        "role": "q source-vector normal form and B_qWeyl selection",
    },
    {
        "source_id": "SRC2529_7_2364_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2364_VALIDATION.csv",
        "needle": "VAL2364_OVERALL,PASS",
        "role": "2364 validation anchor",
    },
    {
        "source_id": "SRC2529_8_2364_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2364_NEXT_TARGET.csv",
        "needle": "NEXT2364_0_selected",
        "role": "B_qWeyl next target precedent",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["source_path"]
        rows.append(
            stamp(
                {
                    **spec,
                    "path_exists": str(path.exists()),
                    "needle_found": str(contains(path, spec["needle"])),
                    "status": "SOURCE_OK" if path.exists() and contains(path, spec["needle"]) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def determinant_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DQG2529_0_channel_definition",
            "object": "psi covariance to local q-channel map",
            "statement": "psi channel can define a temporal/radial covariance mismatch variable q",
            "status": "EXACT_FORMAL_MAP_RETAINED",
            "why_it_matters": "turns the vague residual into a determinate scalar/channel target",
        },
        {
            "row_id": "DQG2529_1_q_zero_surface",
            "object": "determinant/reciprocity surface",
            "statement": "q=0 is the same target class as T^2 S=1 / R_AB=0 in the local branch grammar",
            "status": "EXACT_IDENTITY_RETAINED",
            "why_it_matters": "the local-GR route now has a clean algebraic surface",
        },
        {
            "row_id": "DQG2529_2_absent_q",
            "object": "q absent from psi image",
            "statement": "parent psi map lands only on q=0 configurations",
            "status": "FAIL_CURRENT_CLAIM",
            "why_it_matters": "current psi/covariance ansatz permits independent temporal/radial channels",
        },
        {
            "row_id": "DQG2529_3_vertical_q",
            "object": "q quotient-vertical",
            "statement": "q variations are representative/gauge directions with Dq_visible[q]=0",
            "status": "MISSING_QUOTIENT_MAP",
            "why_it_matters": "needs the q object/equivalence relation that 2527/2528 left unsigned",
        },
        {
            "row_id": "DQG2529_4_stationary_q",
            "object": "q=0 selected by parent action/free energy",
            "statement": "first variation drives q to zero before matter/readout",
            "status": "MISSING_PARENT_SELECTOR",
            "why_it_matters": "would avoid finite q_R coefficients if signed",
        },
        {
            "row_id": "DQG2529_5_verdict",
            "object": "psi determinant quotient verdict",
            "statement": "the determinant theorem is exact, but current MTS does not derive q=0 from psi",
            "status": "PSI_QUOTIENT_NOT_CLOSED",
            "why_it_matters": "finite q_R/source-vector branch remains required",
        },
    ]
    return [stamp(row) for row in rows]


def psi_lift_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "PLA2529_0_parent_carrier",
            "audit_item": "psi parent carrier",
            "needed": "psi must be a parent-owned field/map before readout",
            "status": "PARTIAL_CANDIDATE_ONLY",
            "failure_mode": "readout-level psi cannot select q=0 dynamically",
        },
        {
            "row_id": "PLA2529_1_determinant_relation",
            "audit_item": "determinant/volume relation",
            "needed": "det(psi) or covariance determinant must control the same q_R/R_AB channel",
            "status": "FORMAL_RELATION_RETAINED",
            "failure_mode": "identity alone does not set q=0",
        },
        {
            "row_id": "PLA2529_2_lift_exactness",
            "audit_item": "psi-gradient lift",
            "needed": "local one-form lift must be integrable on finite neighbourhoods",
            "status": "CURL_OBSTRUCTION_UNSIGNED",
            "failure_mode": "algebraic one-point map may not define a parent branch",
        },
        {
            "row_id": "PLA2529_3_matter_readout_silence",
            "audit_item": "matter/readout silence",
            "needed": "ordinary matter/readout must not regenerate q source terms",
            "status": "NOT_PARENT_SIGNED",
            "failure_mode": "finite q_R source leg survives",
        },
        {
            "row_id": "PLA2529_4_verdict",
            "audit_item": "psi lift verdict",
            "needed": "parent-owned psi map selects or quotients q before matter/readout",
            "status": "DERIVATION_ROUTE_OPEN_NOT_CLAIMED",
            "failure_mode": "move to explicit source-vector rows",
        },
    ]
    return [stamp(row) for row in rows]


def finite_qr_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "FQC2529_0_selector",
            "coefficient": "q=0 selector theorem",
            "status": "MISSING_SELECTOR_THEOREM",
            "role": "would replace finite branch with theorem-zero local q",
        },
        {
            "row_id": "FQC2529_1_Mq2",
            "coefficient": "M_q^2",
            "status": "MISSING_PARENT_HESSIAN",
            "role": "blocks q_R=j_q/M_q^2 and range lambda_q",
        },
        {
            "row_id": "FQC2529_2_Zq",
            "coefficient": "Z_q",
            "status": "MISSING_ZQ_THEOREM_OR_COEFFICIENT",
            "role": "controls gradient/range/hair branch",
        },
        {
            "row_id": "FQC2529_3_jq",
            "coefficient": "j_q/J_q",
            "status": "MISSING_JQ_SOURCE_OR_ZERO",
            "role": "sets finite q amplitude and WEP/source sensitivity",
        },
        {
            "row_id": "FQC2529_4_Pobs",
            "coefficient": "P_obs",
            "status": "PARTIAL_TRANSLATION_PARENT_VALUES_MISSING",
            "role": "blocks empirical runner translation",
        },
        {
            "row_id": "FQC2529_5_source_norm",
            "coefficient": "sourceGM/Pi_M/Hilbert normalization",
            "status": "MISSING_SOURCE_NORMALIZATION_THEOREM",
            "role": "blocks Newton derivation and fitted-GM guard",
        },
        {
            "row_id": "FQC2529_6_verdict",
            "coefficient": "finite q_R readiness",
            "status": "NOT_SCORE_READY",
            "role": "normal form required before sourcing values",
        },
    ]
    return [stamp(row) for row in rows]


def q_source_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "QSV2529_0_normal_form",
            "imported_from": "SLOT2364_0_q_euler",
            "statement": "E_q=L_q q+B_qRic R_Ricci+B_qW C_Weyl+C_qT T_H+epsilon_q_source sigma_source+Q_q_body delta_body+Pi_q delta_boundary+tail_q=0",
            "status": "NORMAL_FORM_ACCEPTED_NONCLAIM",
            "effect": "all source-looking q channels are explicit rather than hidden in q_R",
        },
        {
            "row_id": "QSV2529_1_absolute_residual",
            "imported_from": "SLOT2364_3_absolute_residual",
            "statement": "J_q_res is absolute-summed; no sign-cancellation policy",
            "status": "RESIDUAL_VECTOR_LOCKED",
            "effect": "each component must be theorem-zero or finite-bounded",
        },
        {
            "row_id": "QSV2529_2_local_vacuum",
            "imported_from": "SLOT2364_4_local_vacuum_condition",
            "statement": "local exterior vacuum does not kill Weyl, body/boundary, readout/history, or tail terms",
            "status": "CONDITION_WRITTEN_NOT_SATISFIED",
            "effect": "prevents circular local-GR claim",
        },
        {
            "row_id": "QSV2529_3_verdict",
            "imported_from": "SLOT2364_6_verdict",
            "statement": "source-vector normal form is ready enough to choose the first dangerous row, not enough to claim local GR/Newton",
            "status": "SOURCE_VECTOR_READY_CLAIM_BLOCKED",
            "effect": "prioritize B_qWeyl next",
        },
    ]
    return [stamp(row) for row in rows]


def first_dangerous_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "FDQ2529_0_BqWeyl",
            "coefficient": "B_qWeyl",
            "priority": "1",
            "why_first": "Weyl/tidal curvature survives exterior vacuum, so local-vacuum arguments do not silence this channel",
            "zero_route": "parent q representation/no-Weyl-spurion/index theorem",
            "finite_route": "source-backed B_qWeyl bound row with q Green operator, Weyl profile, units, and arena projections",
            "status": "SELECT_FIRST_DANGEROUS_ROW_NONCLAIM",
        },
        {
            "row_id": "FDQ2529_1_BqRic_CqT",
            "coefficient": "B_qRic;C_qT",
            "priority": "2",
            "why_first": "bulk Ricci/matter source terms are next after Weyl because matter coupling and Newton source normalization are still open",
            "zero_route": "operator-owned LHS or matter descent theorem",
            "finite_route": "finite source-normalized q residual rows",
            "status": "QUEUE_AFTER_BQWEYL",
        },
        {
            "row_id": "FDQ2529_2_body_boundary_tail",
            "coefficient": "Q_q_body;Pi_q;tail_q",
            "priority": "3",
            "why_first": "worldtube/readout reentry can fake a source even if bulk rows are absent",
            "zero_route": "support/boundary/readout silence theorem",
            "finite_route": "finite body/boundary/tail rows with arena projections",
            "status": "QUEUE_AFTER_BULK_ROWS",
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CG2529_0_psi_selector",
            "claim": "psi determinant map derives q=0",
            "allowed": "False",
            "blocked_by": "DQG2529_2_absent_q;DQG2529_4_stationary_q;PLA2529_4_verdict",
        },
        {
            "row_id": "CG2529_1_finite_qR_score",
            "claim": "finite q_R coefficients are score-ready",
            "allowed": "False",
            "blocked_by": "FQC2529_1_Mq2;FQC2529_2_Zq;FQC2529_3_jq;FQC2529_5_source_norm",
        },
        {
            "row_id": "CG2529_2_q_source_vector_zero",
            "claim": "q source-vector residual vanishes",
            "allowed": "False",
            "blocked_by": "FDQ2529_0_BqWeyl;QSV2529_2_local_vacuum",
        },
        {
            "row_id": "CG2529_3_local_GR_Newton",
            "claim": "local GR/Newton branch derived",
            "allowed": "False",
            "blocked_by": "CG2529_0_psi_selector;CG2529_1_finite_qR_score;CG2529_2_q_source_vector_zero",
        },
        {
            "row_id": "CG2529_4_public_or_github",
            "claim": "public/GitHub update recommended from 2529",
            "allowed": "False",
            "blocked_by": "B_qWeyl and finite q_R rows remain nonclaim",
        },
    ]
    return [stamp(row) for row in rows]


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "REF2529_0_identity_as_selector",
            "shortcut": "treat determinant identity as q=0 selection",
            "verdict": "REJECT",
            "reason": "an exact surface is not a parent dynamical selector",
        },
        {
            "row_id": "REF2529_1_psi_one_point",
            "shortcut": "use a one-point psi/covariance match as branch theorem",
            "verdict": "REJECT",
            "reason": "finite-neighbourhood lift and curl/integrability remain unsigned",
        },
        {
            "row_id": "REF2529_2_vacuum_kills_weyl",
            "shortcut": "claim local vacuum kills all q sources",
            "verdict": "REJECT",
            "reason": "exterior vacuum kills Ricci/matter bulk, not Weyl/tidal curvature",
        },
        {
            "row_id": "REF2529_3_placeholder_coefficients",
            "shortcut": "score q_R with placeholder M_q^2, Z_q or j_q",
            "verdict": "REJECT",
            "reason": "finite branch needs sourced values, units, norms and no-cancellation guard",
        },
        {
            "row_id": "REF2529_4_public_claim",
            "shortcut": "present q source-vector normal form as local-GR derivation",
            "verdict": "REJECT",
            "reason": "normal form identifies residual rows; it does not zero them",
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DEC2529_0_exact_target",
            "decision": "retain psi determinant q=0 as exact target",
            "reason": "it unifies the local residual surface with the reciprocal/determinant grammar",
            "effect": "mathematical target is sharp",
            "status": "DONE_NONCLAIM",
        },
        {
            "row_id": "DEC2529_1_no_selector_claim",
            "decision": "do not claim psi derives q=0",
            "reason": "absent/vertical/stationary q routes are not parent-signed",
            "effect": "finite q_R branch remains live",
            "status": "BLOCK_CLAIM",
        },
        {
            "row_id": "DEC2529_2_source_vector",
            "decision": "import q source-vector normal form",
            "reason": "it exposes which residual components must be zeroed or bounded",
            "effect": "next target can focus on B_qWeyl instead of generic q_R",
            "status": "ACTIVE",
        },
        {
            "row_id": "DEC2529_3_BqWeyl",
            "decision": "select B_qWeyl as first dangerous row",
            "reason": "Weyl survives local exterior vacuum and can source q unless forbidden by representation/no-spurion theorem",
            "effect": "2530 attacks no-Weyl-spurion or finite B_qWeyl bound",
            "status": "SELECTED",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NEXT2529_0_selected",
            "priority": "selected",
            "next_target": "2530-Y5-R2FR-q-representation-no-Weyl-spurion-or-BqWeyl-bound-row.md",
            "script": "scripts/Y5_R2FR_q_representation_no_Weyl_spurion_or_BqWeyl_bound_row_2530.py",
            "objective": "either prove a parent q representation/no-Weyl-spurion/index theorem that forbids B_qWeyl, or fill the first source-backed nonclaim B_qWeyl bound row",
            "acceptance_gate": "q representation, allowed tensor slots, Weyl spurion ban, boundary/readout stability and arena projections are signed, or B_qWeyl remains finite nonclaim with units/source path",
            "do_not": "do not claim vacuum kills Weyl; do not set B_qWeyl=0 by taste; do not claim local GR/Newton",
        },
        {
            "row_id": "NEXT2529_1_fallback",
            "priority": "fallback_nonclaim",
            "next_target": "2530b-Y5-R2FR-BqRic-CqT-body-bound-row-queue.md",
            "script": "scripts/Y5_R2FR_BqRic_CqT_body_bound_row_queue_2530b.py",
            "objective": "queue Ricci/matter/body/boundary/tail rows after B_qWeyl is handled",
            "acceptance_gate": "each residual has a zero theorem or finite source-backed row",
            "do_not": "do not skip B_qWeyl because it is inconvenient",
        },
    ]
    return [stamp(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    copies = [
        ("determinant_gate", OUTPUTS["determinant_gate"], BRANCH_COPIES["determinant_gate"]),
        ("finite_qr_contract", OUTPUTS["finite_qr_contract"], BRANCH_COPIES["finite_qr_contract"]),
        ("first_dangerous_row", OUTPUTS["first_dangerous_row"], BRANCH_COPIES["first_dangerous_row"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    for copy_id, source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": str(source.relative_to(ROOT)),
                    "destination_path": str(destination.relative_to(ROOT)),
                    "destination_exists": str(destination.exists()),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def any_claim_enabled(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    truthy = {"true", "yes", "1", "claim_ready", "score_ready"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in {"path_exists", "needle_found", "destination_exists"}:
                    continue
                if key in {"valid_for_claim", "claim_allowed", "claim_ready", "allowed"} and str(value).strip().lower() in truthy:
                    return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    sources = rows_by_name["source_register"]
    checks.append(("VAL2529_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "every required source path exists"))
    checks.append(("VAL2529_01_source_needles", all(row["needle_found"] == "True" for row in sources), "all required source needles found"))
    checks.append(("VAL2529_02_psi_not_promoted", any(row["row_id"] == "DQG2529_5_verdict" and row["status"] == "PSI_QUOTIENT_NOT_CLOSED" for row in rows_by_name["determinant_gate"]), "psi quotient not promoted"))
    checks.append(("VAL2529_03_finite_qr_not_score_ready", any(row["row_id"] == "FQC2529_6_verdict" and row["status"] == "NOT_SCORE_READY" for row in rows_by_name["finite_qr_contract"]), "finite q_R contract remains non-score-ready"))
    checks.append(("VAL2529_04_source_vector_imported", any(row["row_id"] == "QSV2529_3_verdict" and row["status"] == "SOURCE_VECTOR_READY_CLAIM_BLOCKED" for row in rows_by_name["q_source_vector_import"]), "q source-vector normal form imported as nonclaim"))
    checks.append(("VAL2529_05_BqWeyl_selected", any(row["row_id"] == "FDQ2529_0_BqWeyl" and row["status"] == "SELECT_FIRST_DANGEROUS_ROW_NONCLAIM" for row in rows_by_name["first_dangerous_row"]), "B_qWeyl selected as first dangerous row"))
    checks.append(("VAL2529_06_claim_gates_blocked", all(row["allowed"] == "False" for row in rows_by_name["claim_gates"]), "all claim gates blocked"))
    checks.append(("VAL2529_07_refusals_cover_shortcuts", len(rows_by_name["refusal_runner"]) >= 5 and all("REJECT" in row["verdict"] for row in rows_by_name["refusal_runner"]), "shortcuts refused"))
    checks.append(("VAL2529_08_next_selected", any(row["row_id"] == "NEXT2529_0_selected" and "BqWeyl" in row["next_target"] for row in rows_by_name["next_target"]), "BqWeyl next target selected"))
    checks.append(("VAL2529_09_no_claim_flags", not any_claim_enabled(rows_by_name), "no generated row enables claim flags"))
    checks.append(("VAL2529_10_branch_copies", all(row["destination_exists"] == "True" for row in rows_by_name["branch_copies"]), "branch copies exist"))
    checks.append(("VAL2529_11_no_formalization_artifacts", not any("formalization-workbench" in str(path).lower() for path in [DOC, *OUTPUTS.values(), *BRANCH_COPIES.values()]), "no outputs target formalization-workbench"))
    checks.append(("VAL2529_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2529_CSV_{path.stem}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2529_CSV_{path.stem}", False, f"{path.name} parse failed: {exc}"))
    for copy_id, path in BRANCH_COPIES.items():
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2529_COPY_CSV_{copy_id}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2529_COPY_CSV_{copy_id}", False, f"{path.name} parse failed: {exc}"))

    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2529_OVERALL",
            overall,
            "2529 retains the exact psi determinant target, refuses to promote it as a selector, imports the q source-vector normal form, and selects B_qWeyl as the first dangerous local residual.",
        )
    )
    return [stamp({"check_id": check_id, "status": "PASS" if ok else "FAIL", "details": detail}) for check_id, ok, detail in checks]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def slim(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [{column: row.get(column, "") for column in columns} for row in rows]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2529 - Psi Determinant Quotient Map or Finite `q_R` Coefficients",
                "**Current verdict:** the `psi` determinant route gives a sharp exact target, not a local-GR theorem. It identifies the `q=0` / reciprocal surface, but current MTS does not prove that parent `psi` lands on it, quotients it, or dynamically selects it before matter/readout.",
                "**Main gain:** the finite branch is no longer vague. Importing the q source-vector normal form exposes the first dangerous residual: `B_qWeyl`. This is the right next target because exterior vacuum does not kill Weyl/tidal curvature.",
                "**Claim discipline:** no local-GR/Newton/R10/PPN/clock/orbital/GitHub claim is allowed from 2529. The result is an exact target plus a finite residual attack order.",
                "## Source Register",
                markdown_table(
                    slim(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needle_found", "status", "role"]),
                    ["source_id", "source_path", "path_exists", "needle_found", "status", "role"],
                ),
                "## Determinant / Quotient Gate",
                markdown_table(
                    slim(rows_by_name["determinant_gate"], ["row_id", "object", "statement", "status", "why_it_matters"]),
                    ["row_id", "object", "statement", "status", "why_it_matters"],
                ),
                "## Psi Lift Audit",
                markdown_table(
                    slim(rows_by_name["psi_lift_audit"], ["row_id", "audit_item", "needed", "status", "failure_mode"]),
                    ["row_id", "audit_item", "needed", "status", "failure_mode"],
                ),
                "## Finite `q_R` Coefficient Contract",
                markdown_table(
                    slim(rows_by_name["finite_qr_contract"], ["row_id", "coefficient", "status", "role"]),
                    ["row_id", "coefficient", "status", "role"],
                ),
                "## Q Source-Vector Import",
                markdown_table(
                    slim(rows_by_name["q_source_vector_import"], ["row_id", "imported_from", "statement", "status", "effect"]),
                    ["row_id", "imported_from", "statement", "status", "effect"],
                ),
                "## First Dangerous Row",
                markdown_table(
                    slim(rows_by_name["first_dangerous_row"], ["row_id", "coefficient", "priority", "why_first", "zero_route", "finite_route", "status"]),
                    ["row_id", "coefficient", "priority", "why_first", "zero_route", "finite_route", "status"],
                ),
                "## Claim Gates",
                markdown_table(
                    slim(rows_by_name["claim_gates"], ["row_id", "claim", "allowed", "blocked_by"]),
                    ["row_id", "claim", "allowed", "blocked_by"],
                ),
                "## Refusal Runner",
                markdown_table(
                    slim(rows_by_name["refusal_runner"], ["row_id", "shortcut", "verdict", "reason"]),
                    ["row_id", "shortcut", "verdict", "reason"],
                ),
                "## Decision Ledger",
                markdown_table(
                    slim(rows_by_name["decision_ledger"], ["row_id", "decision", "reason", "effect", "status"]),
                    ["row_id", "decision", "reason", "effect", "status"],
                ),
                "## Next Target",
                markdown_table(
                    slim(rows_by_name["next_target"], ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"]),
                    ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"],
                ),
                "## Branch Copies",
                markdown_table(
                    slim(rows_by_name["branch_copies"], ["copy_id", "source_path", "destination_path", "destination_exists", "status"]),
                    ["copy_id", "source_path", "destination_path", "destination_exists", "status"],
                ),
                "## Validation",
                markdown_table(
                    slim(rows_by_name["validation"], ["check_id", "status", "details"]),
                    ["check_id", "status", "details"],
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "determinant_gate": determinant_gate_rows(),
        "psi_lift_audit": psi_lift_rows(),
        "finite_qr_contract": finite_qr_rows(),
        "q_source_vector_import": q_source_vector_rows(),
        "first_dangerous_row": first_dangerous_rows(),
        "claim_gates": claim_gate_rows(),
        "refusal_runner": refusal_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
