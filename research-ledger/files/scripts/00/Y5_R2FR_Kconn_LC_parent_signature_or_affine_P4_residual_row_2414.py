from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_KCONN_LC_PARENT_SIGNATURE_OR_AFFINE_P4_RESIDUAL_ROW_2414"
CHECKPOINT_ID = "2414"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2414-Y5-R2FR-Kconn-LC-parent-signature-or-affine-P4-residual-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2414_SOURCE_REGISTER.csv",
    "lc_gate": OUT / "P8_Y5_PARENT_QLOC_2414_LC_PARENT_SIGNATURE_GATE.csv",
    "gamma_slot_import": OUT / "P8_Y5_PARENT_QLOC_2414_GAMMA_SLOT_SECTOR_AUDIT_IMPORT.csv",
    "affine_p4": OUT / "P8_Y5_PARENT_QLOC_2414_AFFINE_P4_RESIDUAL_ROW.csv",
    "impact": OUT / "P8_Y5_PARENT_QLOC_2414_KCONN_IMPACT_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2414_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2414_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2414_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2414_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2414_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2414_KCONN_LC_SIGNATURE_GATE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2414_AFFINE_P4_RESIDUAL_ROW_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_KCONN_DECISION_2414_NONCLAIM.csv",
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


def formalization_has_2414_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2414-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2414*",
        "*P8_Y5_BRR545_2414*",
        "*Y5_R2FR_Kconn_LC_parent_signature_or_affine_P4_residual_row_2414*",
        "*JR2414*",
        "*PARENT_QLOC_KCONN_DECISION_2414*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2413_handoff",
            ROOT / "2413-Y5-R2FR-CDB-principal-symbol-extraction-or-algebraic-residual-map.md",
            ["CDO2413_0_K_conn", "BD2413_3_Kconn_priority", "NEXT2413_0_selected", "VAL2413_OVERALL"],
            "current handoff: K_conn is the high-leverage CDB head after CDB failed to source-sign Z_AB.",
        ),
        (
            "2113_lc_parent_signature",
            ROOT / "2113-Y5-R2FR-metric-coframe-LC-parent-signature-or-affine-P4-bound.md",
            ["LCS2113_0_contract", "LCS2113_8_Kconn_result_if_signed", "LCS2113_9_verdict", "VAL2113_OVERALL"],
            "exact conditional LC theorem plus unsigned parent-signature verdict.",
        ),
        (
            "2113_lc_gate_csv",
            OUT / "P8_Y5_PARENT_QLOC_2113_LC_PARENT_SIGNATURE_CONTRACT.csv",
            ["LCS2113_0_contract", "LCS2113_8_Kconn_result_if_signed", "FAIL_CURRENT_CLAIM"],
            "machine-readable LC parent-signature gate.",
        ),
        (
            "2113_affine_fallback_csv",
            OUT / "P8_Y5_PARENT_QLOC_2113_AFFINE_P4_FALLBACK_ROWS.csv",
            ["AFF2113_0_C_MTS", "AFF2113_5_Kconn_bound", "AFF2113_6_no_cancellation"],
            "machine-readable affine/P4 fallback from first K_conn pass.",
        ),
        (
            "2333_nohypermomentum",
            ROOT / "2333-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md",
            ["NHL2333_0_target", "P4R2333_0_hypermomentum_total", "NEXT2333_0", "VAL2333_OVERALL"],
            "no-hypermomentum/LC source connection audit; not promoted.",
        ),
        (
            "2336_srng_private",
            ROOT / "2336-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
            ["OFC2336_5_status", "ADM2336_3_decision", "P4A2336_0_SRNG_effect", "VAL2336_OVERALL"],
            "private SRNG/OFC branch switches off source/readout Gamma leakage internally, not publicly.",
        ),
        (
            "2347_srng_scope",
            ROOT / "2347-Y5-R2FR-noGamma-SRNG-adoption-or-P4-hypermomentum-component-row.md",
            ["SRNG2347_0_private_scope", "P4H2347_0_total_public", "SPIN2347_0_target", "VAL2347_OVERALL"],
            "private/public SRNG scope split and spin-connection residual handoff.",
        ),
        (
            "2412_rank_zero",
            ROOT / "2412-Y5-R2FR-principal-symbol-ZAB-or-rank-zero-source-current-identity.md",
            ["SSL2412_0_fixed_L0_branch", "RZI2412_0_euler_normal_form", "VAL2412_OVERALL"],
            "strict fixed-L0 branch is rank-zero/algebraic, so K_conn must not be recast as R10 without source-signed kinetic data.",
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


def lc_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="LCS2414_0_exact_conditional_theorem",
            theorem_component="K_conn_norm",
            condition="Conf_ord^local is metric/coframe-only; Gamma_MTS:=LC[g_obs]; omega_obs:=omega_LC[e_obs]; no independent Gamma argument appears in matter, source worldtube, clocks, lightcone, orbit readout, boundary or non-Hilbert improvement terms.",
            consequence="T_MTS=0, Q_MTS=0, Delta_lambda^{mu nu}=0, projective trace is silent, and K_conn_norm=0.",
            status="EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            public_claim_status="blocked",
            missing_signature="sector-by-sector parent object language excluding independent affine Gamma",
        ),
        base_row(
            row_id="LCS2414_1_no_independent_Gamma_inventory",
            theorem_component="field_inventory",
            condition="Gamma_MTS is absent, derived, or pure LC/coframe connection rather than an independent field.",
            consequence="no affine kinetic owner and no connection hypermomentum source",
            status="UNSIGNED_GLOBAL_INVENTORY",
            public_claim_status="blocked",
            missing_signature="parent variable list across ordinary matter, spin, EM/gauge, sources, readouts and boundaries",
        ),
        base_row(
            row_id="LCS2414_2_spin_connection_clause",
            theorem_component="omega_obs",
            condition="spin connection is coframe-owned and torsion-free: omega_obs=omega_LC[e_obs]",
            consequence="spin/torsion part of Delta_abs collapses",
            status="TARGET_SHARP_BUT_NOT_CLOSED",
            public_claim_status="blocked",
            missing_signature="spin sector proof selected by 2347 remains unfinished",
        ),
        base_row(
            row_id="LCS2414_3_private_SRNG_source_readout_clause",
            theorem_component="Delta_source+Delta_clock+Delta_light+Delta_orbit",
            condition="private SRNG/OFC branch treats readouts as downstream q-natural maps, not action variables",
            consequence="source/readout Gamma leakage is zero inside the private nonclaim branch",
            status="PRIVATE_WORKING_CLAUSE_ONLY",
            public_claim_status="blocked",
            missing_signature="public parent-observation theorem or explicit P4 source/readout component rows",
        ),
        base_row(
            row_id="LCS2414_4_boundary_projective_clause",
            theorem_component="Delta_boundary+Delta_projective",
            condition="proper boundary collar, fixed reference, projective policy and no improvement leakage",
            consequence="boundary/projective connection current would vanish or become bounded",
            status="LIVE_RESIDUAL_NOT_CLOSED_BY_SRNG",
            public_claim_status="blocked",
            missing_signature="Bzero boundary certificate plus projective trace policy",
        ),
        base_row(
            row_id="LCS2414_5_verdict",
            theorem_component="LC_parent_signature",
            condition="all LCS2414 clauses parent-signed",
            consequence="K_conn_norm=0 can be carried as a derivation step toward local GR/Newton",
            status="FAIL_CURRENT_PUBLIC_CLAIM_KEEP_AFFINE_P4_ROW",
            public_claim_status="blocked",
            missing_signature="at least spin, boundary/projective and public source/readout clauses remain unsigned",
        ),
    ]


def gamma_slot_import_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="GSI2414_0_gravity_metric_coframe", sector="gravity_metric_coframe", imported_status="CONDITIONAL_LC_IF_NO_AFFINE_SLOT", current_residual="K_LC_mismatch", evidence="2113 LC parent signature contract", next_action="pin parent local ordinary variable list"),
        base_row(row_id="GSI2414_1_matter_spin", sector="matter_spin", imported_status="LIVE_GAMMA_SLOT_AUDIT_REQUIRED", current_residual="Delta_spin + axial_torsion", evidence="2347 spin connection next proof obligation", next_action="prove coframe-owned spin connection or keep axial-torsion/P4 row"),
        base_row(row_id="GSI2414_2_em_gauge", sector="em_gauge", imported_status="AUDIT_REQUIRED", current_residual="possible metric/coframe versus affine coupling ambiguity", evidence="sector not globally signed in 2113/2333", next_action="show EM/gauge uses exterior derivative/g_obs only, or define affine response row"),
        base_row(row_id="GSI2414_3_source_worldtube", sector="source_worldtube", imported_status="PRIVATE_SRNG_ZERO_ONLY", current_residual="Delta_source_public", evidence="2336 and 2347 private SRNG scope", next_action="derive public q-natural source selector or retain P4 source row"),
        base_row(row_id="GSI2414_4_clock_readout", sector="clocks", imported_status="PRIVATE_SRNG_ZERO_ONLY", current_residual="Delta_clock_public", evidence="2336 observation functor contract", next_action="derive public clock readout separation"),
        base_row(row_id="GSI2414_5_lightcone_readout", sector="lightcone", imported_status="PRIVATE_SRNG_ZERO_ONLY", current_residual="Delta_light_public", evidence="2336/2347 readout clauses", next_action="derive public lightcone readout separation without importing GR"),
        base_row(row_id="GSI2414_6_orbital_readout", sector="orbital_readout", imported_status="PRIVATE_SRNG_ZERO_ONLY", current_residual="Delta_orbit_public", evidence="2336 orbit readout limitation", next_action="derive test-body/orbit q-natural readout or keep P4 row"),
        base_row(row_id="GSI2414_7_boundary_nonhilbert", sector="boundary_nonhilbert", imported_status="LIVE_RESIDUAL", current_residual="Delta_boundary + improvement currents", evidence="2336/2347 boundary limits", next_action="Bzero boundary certificate or finite bound row"),
        base_row(row_id="GSI2414_8_projective_trace", sector="projective_trace", imported_status="LIVE_POLICY_REQUIRED", current_residual="Delta_projective", evidence="2113/2336 projective silence conditional only", next_action="projective trace certificate or residual policy"),
        base_row(row_id="GSI2414_9_sector_sum_verdict", sector="sector_sum", imported_status="NO_PUBLIC_NO_GAMMA_SUM_YET", current_residual="Delta_abs_public", evidence="2333 and 2347 claim gates block public no-Gamma theorem", next_action="2415 sector Gamma-slot audit and private SRNG adoption lock"),
    ]


def affine_p4_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="P4R2414_0_C_MTS_definition",
            quantity="C_MTS^lambda_{mu nu}",
            formula="C_MTS^lambda_{mu nu}:=Gamma_MTS^lambda_{mu nu}-LC[g_obs]^lambda_{mu nu}",
            role="affine residual variable if independent Gamma survives",
            units="1/length",
            status="DEFINITION_READY_VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="P4R2414_1_Kconn_bound",
            quantity="K_conn_norm",
            formula="K_conn_norm <= K_LC_mismatch + |c_T_or_c_Q| + |c_A_or_S| + |c_Ttrace| + |c_Qtrace| + |c_Qshear| + |c_Delta|",
            role="absolute-sum upper envelope for connection residual entering Q_cdb/R_alg",
            units="arena_norm_dependent",
            status="SYMBOLIC_BOUND_READY_INPUTS_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="P4R2414_2_torsion_component",
            quantity="T_MTS^lambda_{mu nu}",
            formula="T_MTS^lambda_{mu nu}=2 C_MTS^lambda_[mu nu]",
            role="torsion component of affine branch",
            units="1/length",
            status="EXACT_COMPONENT_FORMULA_VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="P4R2414_3_nonmetricity_component",
            quantity="Q_MTS,rho mu nu",
            formula="Q_MTS,rho mu nu=-nabla^Gamma_rho g_obs,mu nu",
            role="nonmetricity component of affine branch",
            units="metric/length",
            status="EXACT_COMPONENT_FORMULA_VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="P4R2414_4_projective_component",
            quantity="A_projective",
            formula="A_projective := trace/projective part of C_MTS not fixed by metric compatibility or torsion constraints",
            role="projective trace residual if affine/projective symmetry is not parent-fixed",
            units="1/length",
            status="POLICY_REQUIRED_VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="P4R2414_5_hypermomentum_total",
            quantity="Delta_abs_public",
            formula="Delta_abs_public := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary|| + ||Delta_projective||",
            role="public hypermomentum/no-Gamma residual envelope",
            units="action_connection_variation_norm",
            status="PUBLIC_RESIDUAL_LIVE_VALUES_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="P4R2414_6_no_cancellation_guard",
            quantity="policy",
            formula="score by absolute component sums; do not cancel torsion, nonmetricity, projective and hypermomentum terms without a signed identity",
            role="prevents fake local-GR pass by tuned cancellations",
            units="dimensionless_policy",
            status="GUARD_READY",
            score_ready=False,
        ),
    ]


def impact_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="IMP2414_0_if_LC_parent_signed", object="K_conn_norm", impact="K_conn_norm=0", implication="one major CDB residual head disappears; local GR branch becomes much cleaner but still needs source-current/boundary checks"),
        base_row(row_id="IMP2414_1_current_public_status", object="K_conn_norm", impact="affine/P4 residual retained", implication="no local-GR/Newton claim; no finite-range R10 reopening"),
        base_row(row_id="IMP2414_2_private_SRNG_status", object="source/readout Gamma leakage", impact="zero only inside private nonclaim SRNG/OFC branch", implication="useful internal branch, not public evidence"),
        base_row(row_id="IMP2414_3_if_affine_survives", object="C_MTS/Delta_abs_public", impact="must be bounded or empirically constrained", implication="move to P4/source-pack route before any local arena score"),
        base_row(row_id="IMP2414_4_project_overview", object="GR/Newton reduction", impact="closer but still unsigned", implication="the work is now precise: missing item is sector Gamma-slot ownership, not vague handwaving"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2414_0_exact_LC_conditional", gate="LC theorem exact as conditional", passed=True, claim_effect="mathematical lemma available but guarded"),
        base_row(gate_id="CG2414_1_parent_LC_signature", gate="LC parent signature public", passed=False, claim_effect="K_conn zero cannot be publicly claimed"),
        base_row(gate_id="CG2414_2_private_SRNG", gate="private SRNG usable internally", passed=True, claim_effect="source/readout leakage may be set zero only inside private nonclaim branch"),
        base_row(gate_id="CG2414_3_public_noGamma_sector_sum", gate="all sectors exclude independent Gamma publicly", passed=False, claim_effect="Delta_abs_public remains live"),
        base_row(gate_id="CG2414_4_affine_P4_score_ready", gate="affine/P4 residual row score-ready", passed=False, claim_effect="values/maps/source paths missing"),
        base_row(gate_id="CG2414_5_R10_reopen", gate="finite-range R10 reopened by K_conn", passed=False, claim_effect="strict branch remains rank-zero/algebraic"),
        base_row(gate_id="CG2414_6_local_GR_Newton", gate="local GR/Newton reduction claim", passed=False, claim_effect="blocked pending sector Gamma-slot and source-current closure"),
        base_row(gate_id="CG2414_7_GitHub", gate="public/GitHub update", passed=False, claim_effect="private checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2414_0_result", decision="LC_KCONN_ZERO_IS_EXACT_CONDITIONAL", rationale="Metric/coframe-only parent language kills independent affine connection exactly.", consequence="retain as theorem schema, not public claim"),
        base_row(decision_id="DEC2414_1_no_smuggling", decision="DO_NOT_IMPORT_GR_CONNECTION", rationale="The goal is to derive GR/Newton; saying Gamma=LC because GR does is circular.", consequence="sector Gamma-slot evidence required"),
        base_row(decision_id="DEC2414_2_private_branch", decision="PRIVATE_SRNG_BRANCH_ALLOWED_NONCLAIM", rationale="SRNG/OFC is useful for internal derivation pressure but not yet public theorem.", consequence="label all source/readout zeros private"),
        base_row(decision_id="DEC2414_3_fallback", decision="AFFINE_P4_RESIDUAL_ROW_RETAINED", rationale="If any independent Gamma slot survives, C_MTS/Delta_abs_public must be bounded.", consequence="carry no-cancellation absolute-sum row"),
        base_row(decision_id="DEC2414_4_next", decision="SECTOR_GAMMA_SLOT_AUDIT_NEXT", rationale="This is now the shortest route to derived local GR rather than another detour around it.", consequence="audit gravity, matter/spin, EM/gauge, source, clocks, light, orbits, boundary and projective trace"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2414_0_selected",
            selection_status="selected",
            target_file="2415-Y5-R2FR-sector-Gamma-slot-audit-and-private-SRNG-lock.md",
            target_script="scripts/Y5_R2FR_sector_Gamma_slot_audit_and_private_SRNG_lock_2415.py",
            objective="audit every local ordinary/source/readout sector for an independent affine Gamma slot; lock private SRNG as nonclaim; either prove sector no-Gamma or assign explicit P4 residual components",
            success_condition="all sectors are either parent-signed no-Gamma/coframe-owned, private-SRNG-only nonclaim, or represented by affine/P4 residual rows with units/source paths",
            do_not_do="do not claim local GR/Newton, do not use private SRNG publicly, do not reopen R10 without sourced kinetic Z_AB, do not push GitHub",
        ),
        base_row(
            route_id="NEXT2414_1_parallel",
            selection_status="held_parallel",
            target_file="2415b-Y5-R2FR-spin-connection-coframe-owned-or-axial-torsion-P4-row.md",
            target_script="scripts/Y5_R2FR_spin_connection_coframe_owned_or_axial_torsion_P4_row_2415b.py",
            objective="if the broad sector audit is too wide, attack the spin connection first because 2347 leaves Delta_spin unchanged by SRNG",
            success_condition="omega_obs=omega_LC[e_obs] is parent-signed for spin matter, or axial-torsion/spin-current row is explicit",
            do_not_do="do not assume spinors automatically imply torsion-free LC without parent action signature",
        ),
    ]


def copy_branch_rows(lc_gate: list[dict[str, Any]], affine: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["lc_gate"], BRANCH_COPIES["queue"], lc_gate),
        ("branch_wep", OUTPUTS["affine_p4"], BRANCH_COPIES["branch_wep"], affine),
        ("beta_docs", OUTPUTS["decision"], BRANCH_COPIES["beta_docs"], decision),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source_path),
                target_path=str(target_path),
                copied=target_path.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_detail=parse_detail,
            )
        )
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
    rows.append(base_row(validation_id="VAL2414_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2414_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    lc_text = " ".join(str(row) for row in data["lc_gate"])
    rows.append(base_row(validation_id="VAL2414_02_exact_conditional_lc_theorem", status="PASS" if "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED" in lc_text and "K_conn_norm=0" in lc_text else "FAIL", detail="LC/Kconn zero theorem is recorded as exact conditional"))
    rows.append(base_row(validation_id="VAL2414_03_lc_not_public_claim", status="PASS" if "FAIL_CURRENT_PUBLIC_CLAIM_KEEP_AFFINE_P4_ROW" in lc_text else "FAIL", detail="Kconn zero remains blocked publicly"))
    rows.append(base_row(validation_id="VAL2414_04_private_srng_not_public", status="PASS" if "PRIVATE_WORKING_CLAUSE_ONLY" in lc_text and "public parent-observation theorem" in lc_text else "FAIL", detail="private SRNG/OFC is not promoted"))

    import_text = " ".join(str(row) for row in data["gamma_slot_import"])
    required_sectors = ["matter_spin", "em_gauge", "source_worldtube", "clocks", "lightcone", "orbital_readout", "boundary_nonhilbert", "projective_trace"]
    rows.append(base_row(validation_id="VAL2414_05_sector_audit_import", status="PASS" if all(sector in import_text for sector in required_sectors) else "FAIL", detail="sector Gamma-slot audit imports all required local arenas"))

    affine_text = " ".join(str(row) for row in data["affine_p4"])
    rows.append(base_row(validation_id="VAL2414_06_affine_p4_row", status="PASS" if "C_MTS^lambda" in affine_text and "Delta_abs_public" in affine_text and "no_cancellation" in affine_text else "FAIL", detail="affine/P4 fallback row retained"))
    rows.append(base_row(validation_id="VAL2414_07_p4_nonready", status="PASS" if all(not row["score_ready"] for row in data["affine_p4"]) else "FAIL", detail="affine/P4 rows remain non-score-ready"))

    claim_text = " ".join(str(row) for row in data["claim_gates"])
    rows.append(base_row(validation_id="VAL2414_08_claim_gates", status="PASS" if "CG2414_6_local_GR_Newton" in claim_text and "passed': False" in claim_text else "FAIL", detail="local-GR/Newton and R10 claims blocked"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2414_09_next_target", status="PASS" if "2415-Y5-R2FR-sector-Gamma-slot-audit-and-private-SRNG-lock.md" in next_text else "FAIL", detail="sector Gamma-slot/private SRNG lock selected next"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2414_10_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2414_11_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2414_12_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2414_13_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2414_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2414_OVERALL", status=overall, detail="2414 writes the exact conditional Kconn/LC theorem, refuses public GR import, retains affine/P4 residual rows, and selects sector Gamma-slot audit/private SRNG lock next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2414_OVERALL")
    lines = [
        "# 2414 - Y5/R2FR Kconn LC Parent Signature Or Affine P4 Residual Row",
        "",
        "## Result",
        "",
        "2414 takes the clean route and refuses the tempting shortcut.",
        "",
        "The exact conditional theorem is sharp: if the local ordinary/source/readout parent branch is genuinely metric/coframe-only, with `Gamma_MTS := LC[g_obs]`, coframe-owned `omega_obs`, no independent affine `Gamma` slot, no hypermomentum, and no boundary/projective leakage, then",
        "",
        "`K_conn_norm = 0`.",
        "",
        "But that is still **not** a public MTS local-GR claim. The corpus has not yet signed the sector-by-sector parent object language. Private SRNG/OFC can switch off source/readout Gamma leakage internally, but it remains private and nonclaim. Therefore the affine/P4 residual row stays live:",
        "",
        "`C_MTS^lambda_{mu nu} := Gamma_MTS^lambda_{mu nu} - LC[g_obs]^lambda_{mu nu}`.",
        "",
        "Practical verdict: `K_conn` is no longer vague. It is either an exact LC zero after a parent-signature proof, or an explicit affine/P4 residual pack. The next attack is the sector Gamma-slot audit.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## LC Parent Signature Gate",
        "",
        md_table(data["lc_gate"], ["row_id", "theorem_component", "condition", "consequence", "status", "public_claim_status", "missing_signature", "valid_for_claim"]),
        "",
        "## Gamma Slot Sector Audit Import",
        "",
        md_table(data["gamma_slot_import"], ["row_id", "sector", "imported_status", "current_residual", "evidence", "next_action", "valid_for_claim"]),
        "",
        "## Affine P4 Residual Row",
        "",
        md_table(data["affine_p4"], ["row_id", "quantity", "formula", "role", "units", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Kconn Impact Ledger",
        "",
        md_table(data["impact"], ["row_id", "object", "impact", "implication", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gates"], ["gate_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
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
        "This is progress, but the honest kind: the local-GR route is now less foggy, not finished. The exact kill-switch for `K_conn` is known; the remaining proof debt is whether the parent theory really forbids independent affine Gamma slots in every sector that matters.",
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
        "lc_gate": lc_gate_rows(),
        "gamma_slot_import": gamma_slot_import_rows(),
        "affine_p4": affine_p4_rows(),
        "impact": impact_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["lc_gate"], data["lc_gate"])
    write_csv(OUTPUTS["gamma_slot_import"], data["gamma_slot_import"])
    write_csv(OUTPUTS["affine_p4"], data["affine_p4"])
    write_csv(OUTPUTS["impact"], data["impact"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["lc_gate"], data["affine_p4"], data["decision"])
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
