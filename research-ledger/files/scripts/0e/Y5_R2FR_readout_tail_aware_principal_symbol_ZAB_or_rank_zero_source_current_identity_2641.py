from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2641-Y5-R2FR-readout-tail-aware-principal-symbol-ZAB-or-rank-zero-source-current-identity.md"

CHECKPOINT = "2641"
BRANCH_ID = "Y5_R2FR_READOUT_TAIL_AWARE_ZAB_OR_RANK_ZERO_SOURCE_CURRENT_IDENTITY_2641"
PREFIX = "P8_Y5_READOUT_TAIL_ZAB_RANKZERO_2641"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "principal_symbol": RESIDUALS / f"{PREFIX}_PRINCIPAL_SYMBOL_AUDIT.csv",
    "rank_zero_identity": RESIDUALS / f"{PREFIX}_RANK_ZERO_SOURCE_IDENTITY_GATE.csv",
    "readout_tail": RESIDUALS / f"{PREFIX}_READOUT_TAIL_IMPORT.csv",
    "finite_range": RESIDUALS / f"{PREFIX}_FINITE_RANGE_DEMOTION.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue_identity": QUEUE / "JR2641_JH_JNH_BOUNDARY_READOUT_SOURCE_IDENTITY_OR_BOUND_PACK_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "R10_2641_READOUT_TAIL_AWARE_ZAB_RANKZERO_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2641_00_2640",
        "role": "immediate Z/M/J/readout-tail handoff",
        "path": ROOT / "2640-Y5-R2FR-parent-ZM-J-owner-with-readout-tail-or-R10-alpha-refusal-runner.md",
        "needles": ["NO_SINGLE_BRANCH_OWNER", "BD2640_1_rank_zero_constraint_GR_route", "VAL2640_OVERALL"],
    },
    {
        "source_id": "SRC2641_01_2411",
        "role": "parent Z/M/J fork and rank-zero route lemma",
        "path": ROOT / "2411-Y5-R2FR-parent-ZM-and-J-current-owner-or-constraint-branch.md",
        "needles": ["ZMJ2411_1_Z_principal_symbol", "LEM2411_2_rank_zero_route", "VAL2411_OVERALL"],
    },
    {
        "source_id": "SRC2641_02_2412",
        "role": "prior strict-L0 principal-symbol/rank-zero identity contract",
        "path": ROOT / "2412-Y5-R2FR-principal-symbol-ZAB-or-rank-zero-source-current-identity.md",
        "needles": ["STRICT_RANK_ZERO_IMPORT_CONFIRMED", "CDB_SYMBOL_OR_RESIDUAL_SPLIT_REQUIRED", "VAL2412_OVERALL"],
    },
    {
        "source_id": "SRC2641_03_2409",
        "role": "Gamma_eff/Khat response defect and q_loc scaffold",
        "path": ROOT / "2409-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
        "needles": ["KHAT_IDENTITY_NOT_MATCHED_FIRST_RESPONSE_ROUTE_ACTIVE", "KMR2409_2_Khat_identity", "VAL2409_OVERALL"],
    },
    {
        "source_id": "SRC2641_04_2638",
        "role": "readout component-zero failure and absolute tail envelope",
        "path": ROOT / "2638-Y5-R2FR-readout-residual-component-zero-or-source-bound-pack.md",
        "needles": ["READOUT_COMPONENT_ZERO_ATTEMPTS_DO_NOT_CLOSE", "RB2638_6_Delta_readout_abs", "VAL2638_OVERALL"],
    },
    {
        "source_id": "SRC2641_05_1037",
        "role": "no-pole failure and source/test beta-tail guard",
        "path": ROOT / "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md",
        "needles": ["FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED", "TAIL1037_0_alpha_envelope", "V1037_3_beta_rows_complete"],
    },
    {
        "source_id": "SRC2641_06_1038",
        "role": "Omega/DCX vertical-generator no-pole obstruction",
        "path": ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
        "needles": ["FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED", "ODC1038_2_Omega_flat_map", "CGATE1038_0_no_pole"],
    },
    {
        "source_id": "SRC2641_07_2346",
        "role": "non-Hilbert source projection component-bound pack",
        "path": ROOT / "2346-Y5-R2FR-nonHilbert-source-projection-zero-or-component-bound-pack.md",
        "needles": ["NHZ2346_5_verdict", "NHC2346_0_total", "VAL2346_OVERALL"],
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join(["---"] * len(columns)) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
                for row in rows
            ],
        ]
    )


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2641_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2641-Y5-R2FR*",
        "*P8_Y5_READOUT_TAIL_ZAB_RANKZERO_2641*",
        "*P8_Y5_BRR545_2641*",
        "*Y5_R2FR_readout_tail_aware_principal_symbol_ZAB_or_rank_zero_source_current_identity_2641*",
        "*JR2641*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        found = [needle for needle in source["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                role=source["role"],
                source_path=str(source["path"]),
                path_exists=str(source["path"].exists()),
                required_needles=";".join(source["needles"]),
                found_needles=";".join(found),
                needles_present=str(source["path"].exists() and len(found) == len(source["needles"])),
            )
        )
    return rows


def principal_symbol_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            audit_id="ZAB2641_0_M_not_Z",
            object="M_AB / H_AB Hessian",
            attempted_proof="Use Gamma_eff quadratic response to infer a finite-range kinetic residue.",
            result="REJECTED_HESSIAN_NOT_PRINCIPAL_SYMBOL",
            reasoning="M_AB enters the algebraic curvature of the eliminated coordinate. A Yukawa range needs the coefficient of a differential operator such as -Z_AB Delta plus M_AB. M_AB alone is not a pole residue.",
            readout_tail_status="tail irrelevant to this rejection but must remain in any source equation",
            missing_to_close="physical quotient kinetic/principal-symbol Z_AB with units, sign, rank and branch owner",
            passes_now="False",
        ),
        base_row(
            audit_id="ZAB2641_1_ZAB_owner",
            object="Z_AB physical quotient principal symbol",
            attempted_proof="Extract Z_AB from the live Gamma_eff/Khat/CDB parent branch with readout-aware domain terms.",
            result="NOT_SOURCE_SIGNED",
            reasoning="2411 says Z_AB is not signed; 2409 says Khat is not matched to the live metric response; 2412 says CDB is the only remaining hiding place for derivative order.",
            readout_tail_status="readout/projector/domain terms may masquerade as derivative leakage and cannot be ignored",
            missing_to_close="parent action branch; Khat identity; CDB split by derivative order; domain/boundary/projector descent",
            passes_now="False",
        ),
        base_row(
            audit_id="ZAB2641_2_strict_rank_zero_import",
            object="strict fixed-L0 branch",
            attempted_proof="Import the 2412 strict-rank-zero result as the clean branch classification.",
            result="CONDITIONAL_RANK_ZERO_IMPORT_CONFIRMED",
            reasoning="On the strict fixed-L0 subbranch, no parent-owned -Z_AB Delta term is available; the branch is algebraic/constraint-like unless CDB reopens derivative order.",
            readout_tail_status="rank-zero does not silence J_readout; it only changes the problem from Yukawa suppression to source-current identity",
            missing_to_close="CDB no-derivative proof or component residual split; parent rank/sign/units for M_AB",
            passes_now="False",
        ),
        base_row(
            audit_id="ZAB2641_3_no_pole_certificate",
            object="no physical local X pole / vertical generator route",
            attempted_proof="Identify the eliminated direction as a pure gauge/vertical generator.",
            result="NOT_PROVED",
            reasoning="1037 and 1038 still miss parent Omega, DCX, all-field vertical action, boundary charge/cocycle, degree count and matter descent.",
            readout_tail_status="matter/readout descent remains one of the no-pole blockers",
            missing_to_close="Omega_Y; D C_X; v_X on all MTS sectors; Q_X/K_boundary; degree count; matter/no-marker descent",
            passes_now="False",
        ),
        base_row(
            audit_id="ZAB2641_4_verdict",
            object="readout-tail-aware principal-symbol route",
            attempted_proof="Close either physical Z_AB or rank-zero/no-pole from current corpus.",
            result="NO_ZAB_OWNER_OR_RANK_ZERO_SOURCE_IDENTITY_PROOF_YET",
            reasoning="The finite-range branch remains demoted. The best route is now a readout-tail-aware source-current identity for the rank-zero/algebraic branch, with CDB treated as the only derivative-order escape hatch.",
            readout_tail_status="must appear explicitly as J_readout and Delta_readout_abs, not as a post-hoc nuisance",
            missing_to_close="J_H/J_NH/boundary/readout/CDB/DqZ identity or sourced component-bound pack",
            passes_now="False",
        ),
    ]


def rank_zero_identity_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="RZI2641_0_normal_form",
            clause="rank-zero Euler normal form",
            contract="With Z_AB=0 on the strict physical quotient, the local eliminated equation must reduce to M_AB Z^B = J_H,A + J_NH,A + B_A + J_readout,A + CDB_A + R_projector,A.",
            current_status="CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            missing_input="parent rank/sign/units for M_AB; CDB split; source-current rows",
            failure_mode="algebraic source residual survives and projects into Newton/PPN/R10/WEP/clock/orbital arenas",
            passes_now="False",
        ),
        base_row(
            gate_id="RZI2641_1_JH",
            clause="Hilbert/common-matter source leg",
            contract="P_Z[J_H]=0 or universal Hilbert source descent along the eliminated coordinate from one source-blind matter action.",
            current_status="PARTIAL_CONDITIONAL_THEOREM_ONLY",
            missing_input="common matter action syntax; source-blind object language; variation-before-readout domain lock",
            failure_mode="ordinary matter sources Z through a retained algebraic residual",
            passes_now="False",
        ),
        base_row(
            gate_id="RZI2641_2_JNH",
            clause="non-Hilbert source channels",
            contract="P_Z[J_spin/torsion + J_improvement + J_shadow + J_projector]=0 or absolute component bounds exist.",
            current_status="COMPONENT_BOUND_PACK_REQUIRED",
            missing_input="2346 component values or theorem-zero proofs for each non-Hilbert channel",
            failure_mode="a conserved but non-Hilbert source survives; Bianchi/Ward is not enough",
            passes_now="False",
        ),
        base_row(
            gate_id="RZI2641_3_boundary",
            clause="boundary, corner and support terms",
            contract="P_Z[B_A]=0 for proper compact local variations, or Q_X/K_boundary/corner flux is bounded arena-by-arena.",
            current_status="OPEN",
            missing_input="boundary differentiability; Q_X; K_boundary cocycle; source-worldtube/support convention",
            failure_mode="edge charge behaves like an effective source or beta leg",
            passes_now="False",
        ),
        base_row(
            gate_id="RZI2641_4_readout",
            clause="readout/projector tail",
            contract="P_Z[J_readout]=0 or Delta_readout_abs_A is carried as an additive no-cancellation envelope in every local arena.",
            current_status="ZERO_NOT_PROVED_BOUNDS_MISSING",
            missing_input="E_readout_total; projector_norm; marker_readout; section/apparatus/projector-stress rows with values or zero proofs",
            failure_mode="a readout-induced metric/source response is hidden inside fitted GM, gamma-only scoring, or cancellation",
            passes_now="False",
        ),
        base_row(
            gate_id="RZI2641_5_CDB",
            clause="CDB derivative/source split",
            contract="CDB_A contains no physical principal-symbol term or is split into derivative, boundary, projector and source components.",
            current_status="ONLY_REMAINING_ZAB_HIDING_PLACE",
            missing_input="K_conn; K_domain; K_boundary; K_comm extraction with derivative order and units",
            failure_mode="finite-range branch reopens but without source-signed Z/M/J/tails",
            passes_now="False",
        ),
        base_row(
            gate_id="RZI2641_6_DqZ",
            clause="observed descent",
            contract="Dq_Z=0 for metric/coframe/measure/source/readout maps, or the observed residual vector E_DqZ is bounded.",
            current_status="DESCENT_NOT_CLOSED",
            missing_input="quotient map q; observed coframe/metric projection; source/test readout descent",
            failure_mode="constraint variable is invisible in equations but visible in observables",
            passes_now="False",
        ),
        base_row(
            gate_id="RZI2641_7_verdict",
            clause="local GR/Newton reduction by rank-zero source-current identity",
            contract="All RZI2641_1..6 close in one parent branch, producing S_A=0 and Dq_Z=0 before any empirical scoring.",
            current_status="NOT_CLOSED_BUT_NOW_EXACTLY_TARGETED",
            missing_input="component-by-component proof or source-bound pack",
            failure_mode="local branch remains closure-only, not a derivation of GR/Newton",
            passes_now="False",
        ),
    ]


def readout_tail_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            tail_id="RTI2641_0_E_readout_total",
            imported_from="RB2638_0 / RT2640_0",
            arena="all local arenas, especially PPN and R10",
            role_in_2641="appears as J_readout or field-equation readout response in the rank-zero source identity",
            current_status="MISSING_SOURCE_PATH_AND_NUMERIC_VALUE",
            zero_allowed_now="False",
            valid_for_claim="False",
        ),
        base_row(
            tail_id="RTI2641_1_projector_norm",
            imported_from="RB2638_1 / RT2640_1",
            arena="R10, WEP, clocks, PPN, orbital",
            role_in_2641="projector/domain commutator can become J_projector or CDB/K_comm residual",
            current_status="MISSING_PROJECTOR_NORM_AND_DOMAIN",
            zero_allowed_now="False",
            valid_for_claim="False",
        ),
        base_row(
            tail_id="RTI2641_2_marker_readout",
            imported_from="RB2638_3 / RT2640_2",
            arena="source/test composition and WEP/R10",
            role_in_2641="no-marker descent clause for J_readout and beta_s/beta_t source legs",
            current_status="BLOCKED_BY_NO_MARKER_THEOREM_MISSING",
            zero_allowed_now="False",
            valid_for_claim="False",
        ),
        base_row(
            tail_id="RTI2641_3_Delta_readout_abs",
            imported_from="RB2638_6 / RT2640_3",
            arena="PPN/WEP/R10/clock/orbital/Newton",
            role_in_2641="absolute no-cancellation envelope that must be added to any local residual vector until components zero",
            current_status="SCHEMA_READY_VALUES_MISSING",
            zero_allowed_now="False",
            valid_for_claim="False",
        ),
    ]


def finite_range_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            demotion_id="FRD2641_0_finite_range_R10",
            branch="Z_AB finite-range Yukawa branch",
            decision="DEMOTED_TO_NONCLAIM",
            reason="No source-signed Z_AB owner, no same-branch Z/M/J/beta/readout-tail join, and no promoted external alpha_bound(lambda) curve.",
            reopen_condition="CDB or parent action supplies physical Z_AB plus M_AB, J_A, beta_s beta_t, Delta_readout_abs, units and source paths from one branch.",
            next_action="hold R10 data plumbing parallel, but do not score alpha(lambda)",
        ),
        base_row(
            demotion_id="FRD2641_1_rank_zero_route",
            branch="rank-zero/algebraic local GR route",
            decision="PROMOTED_AS_BEST_DERIVATION_ROUTE",
            reason="If the strict branch has no physical kinetic residue, GR/Newton reduction must be a source-current/descent theorem rather than a Yukawa-short-range miracle.",
            reopen_condition="J_H + J_NH + B + J_readout + CDB + projector source stack vanishes and Dq_Z=0, or every component is bounded.",
            next_action="build 2642 JH/JNH/boundary/readout source-current identity or bound pack",
        ),
        base_row(
            demotion_id="FRD2641_2_CDB_escape_hatch",
            branch="CDB derivative-order branch",
            decision="HELD_OPEN_BUT_QUARANTINED",
            reason="2412 leaves CDB as the only remaining place a principal symbol can hide; 2641 refuses to infer it from Hessian or readout artifacts.",
            reopen_condition="extract K_conn/K_domain/K_boundary/K_comm and classify each as derivative principal symbol, source leakage, boundary term or projector residual.",
            next_action="include CDB as a named component in the 2642 identity/bound pack",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2641_0_ZAB_claim",
            claim="physical principal symbol Z_AB is sourced",
            allowed="False",
            blocker="Z_AB owner not parent-signed; CDB unresolved; Khat identity missing",
            valid_for_claim="False",
        ),
        base_row(
            gate_id="CG2641_1_rank_zero_proof",
            claim="rank-zero/no-pole local branch is proved",
            allowed="False",
            blocker="Omega/DCX/vertical-generator no-pole route and source-current identity both remain incomplete",
            valid_for_claim="False",
        ),
        base_row(
            gate_id="CG2641_2_readout_tail_zero",
            claim="readout tail can be dropped",
            allowed="False",
            blocker="2638 component-zero attempts failed; Delta_readout_abs values/source paths missing",
            valid_for_claim="False",
        ),
        base_row(
            gate_id="CG2641_3_R10_alpha",
            claim="R10 alpha(lambda) can be scored",
            allowed="False",
            blocker="finite-range branch demoted; missing Z/M/J/beta/tail/external curve join",
            valid_for_claim="False",
        ),
        base_row(
            gate_id="CG2641_4_local_GR_Newton",
            claim="MTS derives local GR/Newton branch",
            allowed="False",
            blocker="source-current/descent identity not closed and observed residual vector not bounded",
            valid_for_claim="False",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2641_0_main_result",
            decision="ZAB_OR_RANK_ZERO_PROOF_NOT_CLOSED",
            rationale="The strict branch is still best read as rank-zero/algebraic, but the source-current identity is not closed once readout tails, non-Hilbert currents, boundary terms and CDB are kept explicit.",
            consequence="No local GR/Newton or R10 pass; continue derivation with a source-current identity/bound pack.",
            valid_for_claim="False",
        ),
        base_row(
            decision_id="DEC2641_1_good_news",
            decision="PROBLEM_IS_NOW_SHARP",
            rationale="We are no longer vaguely asking whether a motion field hides; the remaining local-GR route is a concrete equation: J_H + J_NH + B + J_readout + CDB + projector/source tails = 0 with Dq_Z=0.",
            consequence="The next checkpoint can attack one visible source stack rather than circle the whole theory.",
            valid_for_claim="False",
        ),
        base_row(
            decision_id="DEC2641_2_route_guard",
            decision="NO_HESSIAN_TO_RANGE_OR_READOUT_DROPPING",
            rationale="Using M_AB as a range or dropping Delta_readout_abs would be the exact laundering move this checkpoint is designed to prevent.",
            consequence="Finite-range scoring stays locked until parent coefficients exist.",
            valid_for_claim="False",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2641_0_selected",
            next_doc="2642-Y5-R2FR-JH-JNH-boundary-readout-source-current-identity-or-bound-pack.md",
            next_script="scripts/Y5_R2FR_JH_JNH_boundary_readout_source_current_identity_or_bound_pack_2642.py",
            objective="Try to prove P_Z[J_H + J_NH + B + J_readout + CDB + R_projector]=0 and Dq_Z=0 for the rank-zero local branch; if any clause fails, write the component-bound pack with arena projections.",
            include="J_H common matter descent; non-Hilbert 2346 components; boundary Q_X/K_boundary; readout tail 2638/2640; CDB derivative/source split; Dq_Z observed descent",
            exclude="R10 alpha scoring; finite-range lambda inference from M_AB; readout-tail cancellation; local GR/Newton claim; formalization-workbench edits; GitHub action",
            valid_for_claim="False",
        )
    ]


def branch_copy_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_rows: list[dict[str, Any]] = []
    for copy_id, path in BRANCH_COPIES.items():
        write_csv(path, rows)
        copy_rows.append(
            base_row(
                copy_id=copy_id,
                copy_path=str(path),
                path_exists=str(path.exists()),
                csv_parses=str(csv_parses(path)),
                contents="rank-zero source-current identity target and nonclaim branch decision",
                valid_for_claim="False",
            )
        )
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    principal_rows = rows_by_name["principal_symbol"]
    identity_rows = rows_by_name["rank_zero_identity"]
    readout_rows = rows_by_name["readout_tail"]
    finite_rows = rows_by_name["finite_range"]
    gate_rows = rows_by_name["claim_gates"]
    next_rows = rows_by_name["next_target"]
    branch_copy_rows_ = rows_by_name["branch_copies"]
    checks = [
        (
            "VAL2641_00_sources",
            all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2641_01_principal_symbol_audit",
            any(row["audit_id"] == "ZAB2641_4_verdict" and row["result"] == "NO_ZAB_OWNER_OR_RANK_ZERO_SOURCE_IDENTITY_PROOF_YET" for row in principal_rows),
            "principal-symbol audit refuses Z_AB/rank-zero proof promotion",
        ),
        (
            "VAL2641_02_rank_zero_identity_contract",
            all(needle in ";".join(row["clause"] for row in identity_rows) for needle in ["Hilbert", "non-Hilbert", "boundary", "readout", "CDB", "observed descent"]),
            "rank-zero contract includes Hilbert, non-Hilbert, boundary, readout, CDB and observed descent clauses",
        ),
        (
            "VAL2641_03_readout_tail_visible",
            any(row["tail_id"] == "RTI2641_3_Delta_readout_abs" for row in readout_rows),
            "readout tail is explicitly imported as an additive no-cancellation envelope",
        ),
        (
            "VAL2641_04_finite_range_demoted",
            any(row["demotion_id"] == "FRD2641_0_finite_range_R10" and row["decision"] == "DEMOTED_TO_NONCLAIM" for row in finite_rows),
            "finite-range R10 remains nonclaim",
        ),
        (
            "VAL2641_05_claim_gates_false",
            all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows),
            "all claim gates are blocked",
        ),
        (
            "VAL2641_06_next_target",
            any(row["next_doc"].startswith("2642-Y5-R2FR-JH-JNH-boundary-readout") for row in next_rows),
            "2642 source-current identity/bound-pack target selected",
        ),
        (
            "VAL2641_07_branch_copies",
            all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_copy_rows_),
            "branch copies exist and parse",
        ),
        (
            "VAL2641_08_csv_parse",
            all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"),
            "all generated CSVs parse cleanly",
        ),
        (
            "VAL2641_09_formalization_untouched",
            not formalization_has_2641_artifacts(),
            "no 2641 outputs are written under formalization-workbench",
        ),
        (
            "VAL2641_10_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        base_row(
            validation_id=check_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
            valid_for_claim="False",
        )
        for check_id, passed, detail in checks
    ]
    rows.append(
        base_row(
            validation_id="VAL2641_OVERALL",
            status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            detail="2641 readout-tail-aware principal-symbol/rank-zero gate keeps local claims blocked and selects 2642 source-current identity target",
            valid_for_claim="False",
        )
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2641 - Y5/R2FR Readout-Tail-Aware Principal Symbol ZAB Or Rank-Zero Source-Current Identity",
                "**Status:** readout-tail-aware ZAB/rank-zero proof attempted. The finite-range branch still has no source-signed `Z_AB`, and the strict rank-zero route is promising but not closed because the source-current identity must still kill or bound `J_H`, `J_NH`, boundary charge, CDB leakage, observed descent and `J_readout` in one parent branch.",
                "**Main result:** the best local-GR route is now exact rather than foggy: prove `P_Z[J_H + J_NH + B + J_readout + CDB + R_projector]=0` plus `Dq_Z=0`, or carry that whole stack as an arena-resolved residual vector. No R10/local-GR/Newton claim is allowed from this checkpoint.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Principal-symbol audit",
                md_table(rows_by_name["principal_symbol"], ["audit_id", "object", "result", "reasoning", "readout_tail_status", "missing_to_close", "passes_now", "valid_for_claim"]),
                "## Rank-zero source-current identity gate",
                md_table(rows_by_name["rank_zero_identity"], ["gate_id", "clause", "contract", "current_status", "missing_input", "failure_mode", "passes_now", "valid_for_claim"]),
                "## Readout tail import",
                md_table(rows_by_name["readout_tail"], ["tail_id", "imported_from", "arena", "role_in_2641", "current_status", "zero_allowed_now", "valid_for_claim"]),
                "## Finite-range demotion and route split",
                md_table(rows_by_name["finite_range"], ["demotion_id", "branch", "decision", "reason", "reopen_condition", "next_action", "valid_for_claim"]),
                "## Claim gates",
                md_table(rows_by_name["claim_gates"], ["gate_id", "claim", "allowed", "blocker", "valid_for_claim"]),
                "## Decision ledger",
                md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
                "## Next target",
                md_table(rows_by_name["next_target"], ["next_id", "next_doc", "next_script", "objective", "include", "exclude", "valid_for_claim"]),
                "## Branch copies",
                md_table(rows_by_name["branch_copies"], ["copy_id", "copy_path", "path_exists", "csv_parses", "contents", "valid_for_claim"]),
                "## Validation",
                md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    remove_pycache()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "principal_symbol": principal_symbol_rows(),
        "rank_zero_identity": rank_zero_identity_rows(),
        "readout_tail": readout_tail_rows(),
        "finite_range": finite_range_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["rank_zero_identity"])

    for name, rows in rows_by_name.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], rows)

    generated = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())
    rows_by_name["validation"] = validation_rows(generated, rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
