from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_CDB_PRINCIPAL_SYMBOL_EXTRACTION_OR_ALGEBRAIC_RESIDUAL_MAP_2413"
CHECKPOINT_ID = "2413"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2413-Y5-R2FR-CDB-principal-symbol-extraction-or-algebraic-residual-map.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2413_SOURCE_REGISTER.csv",
    "derivative_order": OUT / "P8_Y5_PARENT_QLOC_2413_CDB_DERIVATIVE_ORDER_TABLE.csv",
    "residual_map": OUT / "P8_Y5_PARENT_QLOC_2413_CDB_TO_ALGEBRAIC_RESIDUAL_MAP.csv",
    "sublemmas": OUT / "P8_Y5_PARENT_QLOC_2413_CDB_IMPORTABLE_SUBLEMMAS.csv",
    "branch_decision": OUT / "P8_Y5_PARENT_QLOC_2413_BRANCH_DECISION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2413_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2413_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2413_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2413_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2413_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2413_CDB_DERIVATIVE_ORDER_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2413_CDB_RESIDUAL_MAP_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_CDB_BRANCH_DECISION_2413_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2413_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2413-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2413*",
        "*P8_Y5_BRR545_2413*",
        "*Y5_R2FR_CDB_principal_symbol_extraction_or_algebraic_residual_map_2413*",
        "*JR2413*",
        "*PARENT_QLOC_CDB_BRANCH_DECISION_2413*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2412_handoff",
            ROOT / "2412-Y5-R2FR-principal-symbol-ZAB-or-rank-zero-source-current-identity.md",
            ["NEXT2412_0_selected", "CDB2412_4_verdict", "VAL2412_OVERALL"],
            "current handoff: CDB is the only remaining possible Z_AB hiding place.",
        ),
        (
            "2112_cdb_doc",
            ROOT / "2112-Y5-R2FR-CDB-component-zero-or-bound-Kconn-Kdomain-Kboundary.md",
            ["CZG2112_9_verdict", "CDB2112_0_total", "VAL2112_OVERALL"],
            "CDB zero theorem fails; component bounds and K_conn-first route installed.",
        ),
        (
            "2112_zero_gates_csv",
            OUT / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_ZERO_GATES.csv",
            ["CZG2112_1_Kconn_metric_only", "CZG2112_7_Kcomm_projector", "FAIL_CURRENT_CLAIM"],
            "machine-readable zero gates for CDB channels.",
        ),
        (
            "2112_bound_rows_csv",
            OUT / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_BOUND_ROWS.csv",
            ["CDB2112_1_Kconn_norm", "CDB2112_4_Kcomm_norm", "CLAIM_BLOCKED_COMPONENT_INPUTS_MISSING"],
            "machine-readable component-bound formulas.",
        ),
        (
            "2212_cdb_queue_csv",
            OUT / "P8_Y5_PARENT_QLOC_2212_CDB_PRINCIPAL_SYMBOL_QUEUE.csv",
            ["CPS2212_0_K_conn", "CPS2212_4_live_verdict", "FINITE_RANGE_STATUS_HELD_OPEN_BY_CDB"],
            "principal-symbol queue from strict rank-zero decision.",
        ),
        (
            "2337_boundary_projective",
            ROOT / "2337-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md",
            ["RSL2337_4_verdict", "BND2337_0_B_zero_flux", "VAL2337_OVERALL"],
            "private SRNG narrows projective channel; boundary remains live.",
        ),
        (
            "2338_bzero_bound",
            ROOT / "2338-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md",
            ["BZT2338_6_verdict", "BZR2338_0_first_row", "VAL2338_OVERALL"],
            "boundary no-flux zero fails; Bzero first bound row staged.",
        ),
        (
            "2346_nonhilbert_pack",
            OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_COMPONENT_BOUND_PACK.csv",
            ["NHC2346_0_total", "E_spin", "absolute_sum_policy"],
            "non-Hilbert trident component envelope feeding CDB/source residuals.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def derivative_order_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="CDO2413_0_K_conn",
            component="K_conn",
            derivative_order_status="POSSIBLE_CONNECTION_KINETIC_OWNER_NOT_SOURCE_SIGNED",
            extraction_result="No parent-signed Z_AB is extracted. Metric-only LC would collapse K_conn; independent affine/Palatini route must retain torsion/nonmetricity/projective/hypermomentum residuals.",
            kinetic_ZAB_now=False,
            residual_class="affine_or_P4_connection_residual",
            required_next="LC parent grammar/no independent Gamma/no hypermomentum or finite affine-P4 coefficient rows",
            score_ready=False,
        ),
        base_row(
            row_id="CDO2413_1_K_domain",
            component="K_domain",
            derivative_order_status="DOMAIN_SUPPORT_LEAKAGE_NOT_ZAB_OWNER",
            extraction_result="Current evidence gives domain/window/support/readout variation, not a parent-owned elliptic principal symbol.",
            kinetic_ZAB_now=False,
            residual_class="domain_support_readout_residual",
            required_next="parent domain selector or finite delta_g domain/support/readout norm",
            score_ready=False,
        ),
        base_row(
            row_id="CDO2413_2_K_boundary",
            component="K_boundary",
            derivative_order_status="BOUNDARY_DOMAIN_OR_SOURCE_CHARGE_NOT_BULK_ZAB",
            extraction_result="Proper collar zero imports narrowly, but source worldtube/corner/reference/improvement terms remain boundary residuals.",
            kinetic_ZAB_now=False,
            residual_class="B_A_boundary_flux_residual",
            required_next="B_zero_flux theorem or epsilon_Bzero_abs numerator/denominator rows",
            score_ready=False,
        ),
        base_row(
            row_id="CDO2413_3_K_comm",
            component="K_comm/P_loc",
            derivative_order_status="PROJECTOR_COMMUTATOR_RESIDUAL_NOT_ZAB_OWNER",
            extraction_result="Pure postprocess readout can be zero conditionally; projector/source-worldtube commutators survive as q_loc/residual feed.",
            kinetic_ZAB_now=False,
            residual_class="projector_readout_commutator_residual",
            required_next="P_loc commutator theorem or K_comm_norm finite row",
            score_ready=False,
        ),
        base_row(
            row_id="CDO2413_4_DeltaK_live",
            component="Delta_K_live",
            derivative_order_status="LIVE_KHAT_METRIC_RESPONSE_MISMATCH",
            extraction_result="Live Khat tensor mismatch remains a metric-response residual, not a signed kinetic operator.",
            kinetic_ZAB_now=False,
            residual_class="Delta_K_live_norm",
            required_next="live Khat tensor definition, units, and local norm",
            score_ready=False,
        ),
        base_row(
            row_id="CDO2413_5_verdict",
            component="CDB total",
            derivative_order_status="NO_SOURCE_SIGNED_ZAB_FOUND_FINITE_RANGE_NOT_REOPENED",
            extraction_result="Current CDB evidence does not source-sign a physical Z_AB. CDB is carried as algebraic/source/boundary/projector residual machinery until K_conn/LC or affine-P4 route closes.",
            kinetic_ZAB_now=False,
            residual_class="Q_cdb_component_envelope",
            required_next="attack K_conn LC parent signature first",
            score_ready=False,
        ),
    ]


def residual_map_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            map_id="CRM2413_0_total_Qcdb",
            quantity="Q_cdb",
            residual_formula="Q_cdb <= A_ref^-1 N_div (K_conn_norm + K_domain_norm + K_boundary_norm + K_comm_norm + Delta_K_live_norm)",
            enters_rank_zero_as="C_A^CDB in M_AB Z^B = J_A + B_A + C_A^CDB + R_A + J_A^NH",
            needed_inputs="A_ref;N_div;component norms;no-cancellation guard;arena projections",
            status="SYMBOLIC_COMPONENT_SUM_READY_VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            map_id="CRM2413_1_connection",
            quantity="K_conn_norm",
            residual_formula="K_conn_norm <= K_LC_mismatch + |c_T_or_c_Q| + |c_A_or_S| + |c_Ttrace| + |c_Qtrace| + |c_Qshear| + |c_Delta|",
            enters_rank_zero_as="affine/P4 source contribution to C_A^CDB",
            needed_inputs="LC parent signature or affine coefficients with units/source maps",
            status="HIGHEST_LEVERAGE_VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            map_id="CRM2413_2_domain",
            quantity="K_domain_norm",
            residual_formula="K_domain_norm <= C_chi||delta_g chi_D|| + C_sup||delta_g support|| + C_read||delta_g R_readout||",
            enters_rank_zero_as="domain/support/readout source leakage",
            needed_inputs="domain selector;support variation;readout variation constants",
            status="VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            map_id="CRM2413_3_boundary",
            quantity="K_boundary_norm",
            residual_formula="K_boundary_norm <= I_not_proper(|b_C|+|outer_flux|+|corner|+|h_edge|+|Pi_R_tot|)",
            enters_rank_zero_as="B_A or boundary part of C_A^CDB",
            needed_inputs="proper-collar switch;B_zero_flux;corner/source flux;M_H_ref",
            status="NARROW_ZERO_PLUS_FINITE_SOURCE_BRANCH",
            score_ready=False,
        ),
        base_row(
            map_id="CRM2413_4_commutator",
            quantity="K_comm_norm",
            residual_formula="K_comm_norm <= ||(delta P_loc)J|| + ||[P_loc,nabla]K_res|| + ||[delta_parent,R_pre]T_H||",
            enters_rank_zero_as="projector/readout commutator feed into q_loc and arena residuals",
            needed_inputs="projector variation;source worldtube;pre-variation readout clauses",
            status="VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            map_id="CRM2413_5_q_loc_feed",
            quantity="q_loc_CDB",
            residual_formula="||P_loc nabla_mu Delta_K^{mu nu}|| <= N_div||Delta_K|| + K_comm_norm",
            enters_rank_zero_as="observed q_loc residual vector and PPN/local source feed",
            needed_inputs="N_div;P_loc commutator;Delta_K norm;component norms",
            status="FEED_READY_INPUTS_MISSING",
            score_ready=False,
        ),
    ]


def sublemma_rows() -> list[dict[str, Any]]:
    return [
        base_row(sublemma_id="SUB2413_0_metric_only_LC", component="K_conn", import_status="CONDITIONAL_IMPORT_ONLY", statement="On metric/coframe-only configuration space, Gamma=LC[g_obs].", guard="requires parent field inventory to exclude independent Gamma and hypermomentum"),
        base_row(sublemma_id="SUB2413_1_boundary_proper_collar", component="K_boundary", import_status="NARROW_ZERO_IMPORT_ONLY", statement="Proper compact representative generators kill finite-jet local boundary cocycles.", guard="does not cover source worldtubes, reference/corner terms, or edge projectors"),
        base_row(sublemma_id="SUB2413_2_pure_postprocess", component="K_comm", import_status="CONDITIONAL_IMPORT_ONLY", statement="Readout maps absent from parent/effective variation cannot create source coefficients.", guard="does not cover field/support/source dependent projectors or pre-variation EFT readouts"),
        base_row(sublemma_id="SUB2413_3_projector_absorption", component="K_comm/K_domain", import_status="CONDITIONAL_BOUND_ONLY", statement="Small projector leakage can be absorbed if same-domain constants satisfy CK/Korn/trace inequalities.", guard="requires sourced epsilon_P, C_CK, C_trace, norm convention and units"),
        base_row(sublemma_id="SUB2413_4_boundary_Bzero", component="K_boundary", import_status="BOUND_ROW_STAGED_NOT_ZERO", statement="B_zero_flux zero theorem is exact as a target but unsigned; epsilon_Bzero_abs is the retained row.", guard="requires theta/Q_tau, fixed reference, compact support, Hilbert equality, positive M_H_ref"),
    ]


def branch_decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(branch_id_local="BD2413_0_strict_branch", branch="strict fixed-L0", decision="RANK_ZERO_RETAINED", reason="CDB extraction does not change strict branch: no strict Z_AB and no strict R10 lambda.", next_action="carry algebraic residual identity"),
        base_row(branch_id_local="BD2413_1_finite_range", branch="finite-range R10", decision="NOT_REOPENED_BY_CURRENT_CDB_EVIDENCE", reason="no CDB channel source-signs a physical kinetic Z_AB now.", next_action="do not run alpha(lambda) unless K_conn/LC or affine operator later sources Z_AB"),
        base_row(branch_id_local="BD2413_2_CDB_residual", branch="CDB residual", decision="MOVED_INTO_RALG_COMPONENT_MAP", reason="each CDB channel has a symbolic bound/residual class and no-cancellation policy.", next_action="fill component rows or prove zero sublemmas"),
        base_row(branch_id_local="BD2413_3_Kconn_priority", branch="connection channel", decision="SELECT_KCONN_FIRST", reason="K_conn is the only CDB head that could still decide geometry-vs-affine residual cleanly.", next_action="LC parent signature or affine/P4 residual row"),
        base_row(branch_id_local="BD2413_4_verdict", branch="local GR route", decision="RANK_ZERO_PLUS_CDB_RESIDUAL_DISCIPLINE", reason="strict branch is algebraic; CDB is residual/affine unless K_conn is parent-signed.", next_action="2414 Kconn LC parent signature or affine P4 residual"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2413_0_CDB_ZAB", gate="CDB source-signs physical Z_AB", status="BLOCKED_NONCLAIM", implication="finite range not reopened"),
        base_row(gate_id="CG2413_1_strict_R10", gate="strict-branch R10 alpha(lambda)", status="REJECTED_FOR_STRICT_BRANCH", implication="no strict lambda"),
        base_row(gate_id="CG2413_2_Qcdb_score", gate="Q_cdb residual score-ready", status="BLOCKED_NONCLAIM", implication="component values and source paths missing"),
        base_row(gate_id="CG2413_3_Kconn_zero", gate="K_conn zero/LC parent signature closes", status="BLOCKED_NONCLAIM", implication="affine/P4 rows still retained"),
        base_row(gate_id="CG2413_4_local_GR_Newton", gate="local GR/Newton reduction follows", status="BLOCKED_NONCLAIM", implication="CDB/source-current/boundary closure still missing"),
        base_row(gate_id="CG2413_5_GitHub", gate="public/GitHub update", status="BLOCKED_PRIVATE", implication="private derivation work only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2413_0_gain", decision="CDB_SPLIT_AS_RESIDUAL_NOT_ZAB", rationale="No current CDB channel source-signs Z_AB; each channel now has a residual class and bound route.", next_action="use Q_cdb component envelope in R_alg"),
        base_row(decision_id="DEC2413_1_strict", decision="FINITE_RANGE_NOT_REOPENED", rationale="The strict branch remains rank-zero; R10 alpha(lambda) is rejected unless future K_conn evidence sources an operator.", next_action="keep R10 data lane separate/nonclaim"),
        base_row(decision_id="DEC2413_2_priority", decision="KCONN_LC_PARENT_SIGNATURE_NEXT", rationale="Connection ownership is the highest-leverage CDB head: it decides LC geometry versus affine/P4 residuals.", next_action="derive no independent Gamma/no hypermomentum or fill affine/P4 coefficient row"),
        base_row(decision_id="DEC2413_3_no_claim", decision="NO_LOCAL_CLAIM_NO_GITHUB", rationale="Residual map improved, but no zero theorem or numeric bound closes.", next_action="all rows remain nonclaim"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2413_0_selected",
            selection_status="selected",
            target_file="2414-Y5-R2FR-Kconn-LC-parent-signature-or-affine-P4-residual-row.md",
            target_script="scripts/Y5_R2FR_Kconn_LC_parent_signature_or_affine_P4_residual_row_2414.py",
            objective="try to parent-sign metric/coframe-only Levi-Civita connection for the local source branch; if not, stage affine/P4 torsion, nonmetricity, projective and hypermomentum residual coefficients",
            success_condition="K_conn zero/LC clause becomes parent-signed nonclaim, or affine/P4 residual row is explicit with units/source paths and valid_for_claim=false",
            do_not_do="do not declare Gamma=LC by notation, ignore hypermomentum/projective trace, claim local GR/Newton, or use GitHub",
        ),
        base_row(
            route_id="NEXT2413_1_parallel",
            selection_status="held_parallel",
            target_file="2414b-Y5-R2FR-Bzero-boundary-denominator-source-row.md",
            target_script="scripts/Y5_R2FR_Bzero_boundary_denominator_source_row_2414b.py",
            objective="continue boundary denominator/Bzero row acquisition if connection route stalls",
            success_condition="epsilon_Bzero_abs numerator/denominator units and source paths are explicit nonclaim rows",
            do_not_do="do not import EH boundary charge without MTS theta/Q_tau extraction",
        ),
    ]


def copy_branch_rows(derivative: list[dict[str, Any]], residual: list[dict[str, Any]], branch: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["derivative_order"], BRANCH_COPIES["queue"], derivative),
        ("branch_wep", OUTPUTS["residual_map"], BRANCH_COPIES["branch_wep"], residual),
        ("beta_docs", OUTPUTS["branch_decision"], BRANCH_COPIES["beta_docs"], branch),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(base_row(copy_id=copy_id, source_path=str(source_path), target_path=str(target_path), copied=target_path.exists(), parse_ok=parse_ok, row_count=row_count, parse_detail=parse_detail))
    return rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = data["source_register"]
    rows.append(base_row(validation_id="VAL2413_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2413_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    derivative_text = " ".join(str(row) for row in data["derivative_order"])
    rows.append(base_row(validation_id="VAL2413_02_no_zab_found", status="PASS" if "NO_SOURCE_SIGNED_ZAB_FOUND_FINITE_RANGE_NOT_REOPENED" in derivative_text else "FAIL", detail="CDB derivative-order table does not promote Z_AB"))
    rows.append(base_row(validation_id="VAL2413_03_all_channels_classified", status="PASS" if all(name in derivative_text for name in ["K_conn", "K_domain", "K_boundary", "K_comm", "Delta_K_live"]) else "FAIL", detail="all CDB channels classified"))

    residual_text = " ".join(str(row) for row in data["residual_map"])
    rows.append(base_row(validation_id="VAL2413_04_residual_map", status="PASS" if "Q_cdb <=" in residual_text and "q_loc_CDB" in residual_text else "FAIL", detail="CDB residual map and q_loc feed installed"))

    sublemma_text = " ".join(str(row) for row in data["sublemmas"])
    rows.append(base_row(validation_id="VAL2413_05_sublemmas_nonclaim", status="PASS" if "CONDITIONAL_IMPORT_ONLY" in sublemma_text and "BOUND_ROW_STAGED_NOT_ZERO" in sublemma_text else "FAIL", detail="only conditional/narrow sublemmas imported"))

    branch_text = " ".join(str(row) for row in data["branch_decision"])
    rows.append(base_row(validation_id="VAL2413_06_branch_decision", status="PASS" if "NOT_REOPENED_BY_CURRENT_CDB_EVIDENCE" in branch_text and "SELECT_KCONN_FIRST" in branch_text else "FAIL", detail="finite range not reopened and Kconn selected"))

    claim = data["claim_gate"]
    rows.append(base_row(validation_id="VAL2413_07_claim_gates", status="PASS" if all(not row["valid_for_claim"] and not row["claim_allowed"] for row in claim) else "FAIL", detail="claim gates remain false"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2413_08_next_target", status="PASS" if "2414-Y5-R2FR-Kconn-LC-parent-signature-or-affine-P4-residual-row.md" in next_text else "FAIL", detail="Kconn LC parent signature route selected"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2413_09_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2413_10_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2413_11_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2413_12_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2413_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2413_OVERALL", status=overall, detail="2413 classifies CDB as residual machinery rather than a sourced Z_AB, keeps finite-range R10 closed for the strict branch, and selects K_conn LC parent signature or affine/P4 residual next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2413_OVERALL")
    lines = [
        "# 2413 - Y5/R2FR CDB Principal Symbol Extraction Or Algebraic Residual Map",
        "",
        "## Result",
        "",
        "2413 does the CDB split. Current evidence does **not** source-sign a physical `Z_AB` hiding inside CDB, so finite-range R10 is not reopened for the strict local branch.",
        "",
        "Instead, CDB becomes residual machinery feeding the rank-zero algebraic equation:",
        "",
        "`M_AB Z^B = J_A + B_A + C_A^CDB + R_A + J_A^NH`.",
        "",
        "The most important remaining CDB head is `K_conn`: if the parent branch is truly metric/coframe-only Levi-Civita, the connection residual collapses; if not, affine/P4 torsion, nonmetricity, projective and hypermomentum coefficients must be carried honestly.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## CDB Derivative-Order Table",
        "",
        md_table(data["derivative_order"], ["row_id", "component", "derivative_order_status", "extraction_result", "kinetic_ZAB_now", "residual_class", "required_next", "score_ready", "valid_for_claim"]),
        "",
        "## CDB To Algebraic Residual Map",
        "",
        md_table(data["residual_map"], ["map_id", "quantity", "residual_formula", "enters_rank_zero_as", "needed_inputs", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Importable Sublemmas",
        "",
        md_table(data["sublemmas"], ["sublemma_id", "component", "import_status", "statement", "guard", "valid_for_claim"]),
        "",
        "## Branch Decision",
        "",
        md_table(data["branch_decision"], ["branch_id_local", "branch", "decision", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(data["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(data["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Practical Status",
        "",
        "This is a strong pruning step. CDB no longer floats as a mystical maybe-range: unless `K_conn` later produces a real parent kinetic operator, it is an explicit residual envelope feeding the algebraic rank-zero branch. The next best attack is connection ownership.",
        "",
        f"Validation overall: `{overall['status']}`.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "derivative_order": derivative_order_rows(),
        "residual_map": residual_map_rows(),
        "sublemmas": sublemma_rows(),
        "branch_decision": branch_decision_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["derivative_order"], data["derivative_order"])
    write_csv(OUTPUTS["residual_map"], data["residual_map"])
    write_csv(OUTPUTS["sublemmas"], data["sublemmas"])
    write_csv(OUTPUTS["branch_decision"], data["branch_decision"])
    write_csv(OUTPUTS["claim_gate"], data["claim_gate"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["derivative_order"], data["residual_map"], data["branch_decision"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
