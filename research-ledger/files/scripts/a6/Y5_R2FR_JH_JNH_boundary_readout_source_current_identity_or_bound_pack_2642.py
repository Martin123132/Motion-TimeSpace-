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
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2642-Y5-R2FR-JH-JNH-boundary-readout-source-current-identity-or-bound-pack.md"

CHECKPOINT = "2642"
BRANCH_ID = "Y5_R2FR_JH_JNH_BOUNDARY_READOUT_SOURCE_CURRENT_IDENTITY_2642"
PREFIX = "P8_Y5_SOURCE_CURRENT_IDENTITY_2642"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "proof_attempt": RESIDUALS / f"{PREFIX}_PROOF_ATTEMPT.csv",
    "component_bound": RESIDUALS / f"{PREFIX}_COMPONENT_BOUND_PACK.csv",
    "arena_projection": RESIDUALS / f"{PREFIX}_ARENA_PROJECTION_SKELETON.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2642_SOURCE_CURRENT_IDENTITY_COMPONENT_BOUND_PACK_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "R10_2642_RANK_ZERO_SOURCE_CURRENT_RESIDUAL_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2642_SOURCE_CURRENT_IDENTITY_WEP_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2642_00_2641",
        "role": "immediate readout-tail-aware identity handoff",
        "path": ROOT / "2641-Y5-R2FR-readout-tail-aware-principal-symbol-ZAB-or-rank-zero-source-current-identity.md",
        "needles": ["NEXT2641_0_selected", "RZI2641_7_verdict", "VAL2641_OVERALL"],
    },
    {
        "source_id": "SRC2642_01_2412",
        "role": "rank-zero normal form and algebraic residual bridge",
        "path": ROOT / "2412-Y5-R2FR-principal-symbol-ZAB-or-rank-zero-source-current-identity.md",
        "needles": ["RZI2412_0_euler_normal_form", "ARB2412_0_rank_zero_residual", "VAL2412_OVERALL"],
    },
    {
        "source_id": "SRC2642_02_2413",
        "role": "CDB residual classification and Qcdb map",
        "path": ROOT / "2413-Y5-R2FR-CDB-principal-symbol-extraction-or-algebraic-residual-map.md",
        "needles": ["CDO2413_5_verdict", "CRM2413_0_total_Qcdb", "VAL2413_OVERALL"],
    },
    {
        "source_id": "SRC2642_03_2346",
        "role": "non-Hilbert source component pack",
        "path": ROOT / "2346-Y5-R2FR-nonHilbert-source-projection-zero-or-component-bound-pack.md",
        "needles": ["NHZ2346_5_verdict", "NHC2346_0_total", "VAL2346_OVERALL"],
    },
    {
        "source_id": "SRC2642_04_2638",
        "role": "readout tail component failure and no-cancellation envelope",
        "path": ROOT / "2638-Y5-R2FR-readout-residual-component-zero-or-source-bound-pack.md",
        "needles": ["READOUT_COMPONENT_ZERO_ATTEMPTS_DO_NOT_CLOSE", "RB2638_6_Delta_readout_abs", "VAL2638_OVERALL"],
    },
    {
        "source_id": "SRC2642_05_1039",
        "role": "proper compact boundary zero sublemma",
        "path": ROOT / "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
        "needles": ["QK1039_6_verdict", "QKG1039_0_proper_compact_sublemma", "V1039_SUMMARY"],
    },
    {
        "source_id": "SRC2642_06_1040",
        "role": "explicit B_X/Q_X source-boundary formula contract",
        "path": ROOT / "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
        "needles": ["BX1040_4_verdict", "A3P1040_0_formula", "V1040_SUMMARY"],
    },
    {
        "source_id": "SRC2642_07_1038",
        "role": "no-pole vertical generator obstruction",
        "path": ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
        "needles": ["ODC1038_8_verdict", "CGATE1038_0_no_pole", "V1038_SUMMARY"],
    },
    {
        "source_id": "SRC2642_08_2409",
        "role": "Khat/Gamma metric-response defect",
        "path": ROOT / "2409-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
        "needles": ["KHAT_IDENTITY_NOT_MATCHED_FIRST_RESPONSE_ROUTE_ACTIVE", "KMR2409_2_Khat_identity", "VAL2409_OVERALL"],
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
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2642_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2642-Y5-R2FR*",
        "*P8_Y5_SOURCE_CURRENT_IDENTITY_2642*",
        "*P8_Y5_BRR545_2642*",
        "*Y5_R2FR_JH_JNH_boundary_readout_source_current_identity_or_bound_pack_2642*",
        "*JR2642*",
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


def proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            proof_id="SCI2642_0_master_identity",
            component="S_Z total source-current stack",
            attempted_derivation="Project the rank-zero Euler equation along the eliminated coordinate: S_Z,A := P_Z[J_H,A + J_NH,A + B_A + J_readout,A + CDB_A + R_projector,A].",
            current_result="IDENTITY_CONTRACT_DERIVED_COMPONENTS_UNSIGNED",
            condition_for_zero="Every component projection vanishes in the same parent branch and Dq_Z=0 for observed variables.",
            obstruction="components are individually sharpened but not all theorem-zero or source-backed",
            residual_if_not_zero="Z^A = (M^-1)^{AB} S_Z,B, then R_obs^I = L^I_A Z^A + E_DqZ^I",
            passes_now="False",
        ),
        base_row(
            proof_id="SCI2642_1_JH_descent",
            component="J_H ordinary Hilbert/common-matter leg",
            attempted_derivation="If S_matter = Sbar[q(Phi), psi, theta], v_Z is in ker(Dq), theta carries no representative marker, and variation is before readout, then delta_vZ S_matter = 0 and P_Z[J_H]=0.",
            current_result="CONDITIONAL_DESCENT_LEMMA_CLEAN_NOT_PARENT_SIGNED",
            condition_for_zero="parent signs common source-blind matter action, no pre-action species/source weights, no representative marker, and Dq(v_Z)=0",
            obstruction="common matter syntax, theta/no-marker rule and Dq_Z are not yet source-signed together",
            residual_if_not_zero="epsilon_JH_Z_abs := ||P_Z J_H|| / ||J_H_ref||",
            passes_now="False",
        ),
        base_row(
            proof_id="SCI2642_2_JNH_channels",
            component="J_NH spin/torsion/improvement/shadow/projector leg",
            attempted_derivation="Use 2346 trident: either all non-Hilbert channels vanish by parent field grammar, or retain absolute component envelope.",
            current_result="ZERO_NOT_DERIVED_COMPONENT_PACK_REQUIRED",
            condition_for_zero="metric/coframe-only LC branch, no hypermomentum/torsion/nonmetricity/projective source, no improvement/shadow/projector leakage",
            obstruction="2346 total zero failed and component values remain missing",
            residual_if_not_zero="epsilon_JNH_abs <= E_spin + E_boundary + E_readout + E_shadow + E_projector",
            passes_now="False",
        ),
        base_row(
            proof_id="SCI2642_3_boundary",
            component="B_A boundary/corner/source-worldtube leg",
            attempted_derivation="Import 1039 proper compact collar lemma for representative transformations, then use 1040 B_X/Q_X formula for non-proper/source boundaries.",
            current_result="NARROW_PROPER_ZERO_IMPORT_FULL_BOUNDARY_OPEN",
            condition_for_zero="proper compact representative generator and finite jets vanish on boundary collar, plus source-worldtube/reference/corner terms absent or exact",
            obstruction="1040 B_X formula is explicit but L_X/Theta_X/P_X/boundary class/reference projector are not parent-owned",
            residual_if_not_zero="epsilon_B_abs := ||Pi_A int_partialSigma epsilon.B_X|| / M_H_ref, with alpha3 edge row held nonclaim",
            passes_now="False",
        ),
        base_row(
            proof_id="SCI2642_4_readout",
            component="J_readout and Delta_readout_abs",
            attempted_derivation="If readout/projectors are post-solution maps absent from S_parent and S_red is forbidden, then P_Z[J_readout]=0.",
            current_result="ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING",
            condition_for_zero="P_read/P_loc metric-independent or postprocess-only; no marker readout; no apparatus/source backreaction; variation-before-readout",
            obstruction="2638 component-zero attempts do not close and Delta_readout_abs values are missing",
            residual_if_not_zero="Delta_readout_abs_A = abs(E_readout_total)+abs(projector_norm)+abs(marker_readout)+...",
            passes_now="False",
        ),
        base_row(
            proof_id="SCI2642_5_CDB",
            component="CDB_A derivative/domain/boundary/commutator leg",
            attempted_derivation="Use 2413: CDB does not source-sign Z_AB now, so it feeds the algebraic residual as Q_cdb unless each component zeroes.",
            current_result="NO_ZAB_REOPENING_QCDB_RETAINED",
            condition_for_zero="K_conn LC parent signature or affine coefficients zero; K_domain zero; full K_boundary source terms zero; K_comm/projector terms zero; Delta_K live zero",
            obstruction="K_conn, domain/support/readout, source boundary, projector commutator and live Khat mismatch remain unsigned",
            residual_if_not_zero="Q_cdb <= A_ref^-1 N_div(K_conn_norm+K_domain_norm+K_boundary_norm+K_comm_norm+Delta_K_live_norm)",
            passes_now="False",
        ),
        base_row(
            proof_id="SCI2642_6_DqZ",
            component="observed descent Dq_Z",
            attempted_derivation="If the quotient map q and all observed metric/coframe/measure/source/readout maps are insensitive to Z after constraint solving, E_DqZ^I=0.",
            current_result="OBSERVED_DESCENT_NOT_CLOSED",
            condition_for_zero="q, metric/coframe readout, source normalization, clock/EM/orbital observables and matter constants all factor through the quotient without Z marker",
            obstruction="Dq_Z has not been proved for all observed arenas; this is the difference between algebraic silence and physical silence",
            residual_if_not_zero="E_DqZ^I is an additive arena residual independent of S_Z cancellation",
            passes_now="False",
        ),
        base_row(
            proof_id="SCI2642_7_verdict",
            component="local GR/Newton source-current identity",
            attempted_derivation="Close SCI2642_1 through SCI2642_6 together and then prove M_AB lock/invertible-or-gauge handling.",
            current_result="NOT_CLOSED_BOUND_PACK_INSTALLED",
            condition_for_zero="single parent branch signs descent, current silence, boundary silence, readout silence, CDB silence and observed descent",
            obstruction="too many unsigned clauses remain for a claim, but each is now a named component rather than a fog bank",
            residual_if_not_zero="R_master^I <= ||L^I M^-1||*(epsilon_JH+epsilon_JNH+epsilon_B+Delta_readout_abs+Q_cdb+epsilon_projector)+E_DqZ^I",
            passes_now="False",
        ),
    ]


def component_bound_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            bound_id="SCB2642_0_master",
            quantity="Delta_rankzero_source_abs_A",
            formula="Delta_A <= ||L_A M^-1||*(eps_JH_Z_abs + eps_JNH_abs + eps_B_abs + Delta_readout_abs_A + Q_cdb_abs + eps_projector_abs) + E_DqZ_A",
            units="arena-normalized dimensionless after M_AB/source normalization",
            needed_inputs="M_AB rank/sign/units; L_A projection; all component zeros or numeric source rows; DqZ map",
            arenas="Newton;PPN;R10;WEP;clock;orbital;EM",
            status="MASTER_BOUND_FORM_READY_VALUES_MISSING",
            score_ready="False",
        ),
        base_row(
            bound_id="SCB2642_1_eps_JH_Z_abs",
            quantity="Hilbert source descent residual",
            formula="eps_JH_Z_abs := ||P_Z J_H|| / ||J_H_ref||",
            units="dimensionless source-normalized",
            needed_inputs="common matter action; no-marker theta; Dq(v_Z)=0; source weights absent; J_H_ref",
            arenas="Newton;PPN;WEP;R10;clock;orbital",
            status="CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
            score_ready="False",
        ),
        base_row(
            bound_id="SCB2642_2_eps_JNH_abs",
            quantity="non-Hilbert source residual",
            formula="eps_JNH_abs <= E_spin + E_boundary + E_readout + E_shadow + E_projector",
            units="dimensionless after source normalization",
            needed_inputs="2346 component theorem-zeroes or numeric source-backed values",
            arenas="local_GR;Newton;PPN;WEP;R10;clock;orbital",
            status="COMPONENT_VALUES_MISSING",
            score_ready="False",
        ),
        base_row(
            bound_id="SCB2642_3_eps_B_abs",
            quantity="boundary/source-worldtube residual",
            formula="eps_B_abs := ||Pi_A int_partialSigma epsilon_nu B_X^nu dS|| / M_H_ref",
            units="source-normalized boundary flux",
            needed_inputs="B_X owner; boundary class; reference subtraction; Pi_M/Pi_EH; M_H_ref; source-worldtube convention",
            arenas="PPN_alpha3;R10_edge;orbital;clock;Newton_GM",
            status="PROPER_ZERO_IMPORTED_SOURCE_BOUNDARY_OPEN",
            score_ready="False",
        ),
        base_row(
            bound_id="SCB2642_4_Delta_readout_abs_A",
            quantity="readout/projector residual",
            formula="Delta_readout_abs_A = sum_i |epsilon_readout_i,A|",
            units="arena-normalized dimensionless or operator-normalized",
            needed_inputs="2638/2640 component values or theorem-zero proofs",
            arenas="PPN;WEP;R10;clock;orbital;Newton",
            status="SCHEMA_READY_VALUES_MISSING",
            score_ready="False",
        ),
        base_row(
            bound_id="SCB2642_5_Q_cdb_abs",
            quantity="CDB residual",
            formula="Q_cdb <= A_ref^-1 N_div(K_conn_norm+K_domain_norm+K_boundary_norm+K_comm_norm+Delta_K_live_norm)",
            units="q_loc/source-normalized residual after A_ref and N_div",
            needed_inputs="2413 component norms; LC/Kconn decision; domain/support/readout constants; boundary and commutator rows",
            arenas="Newton;PPN;R10;WEP;clock;orbital",
            status="SYMBOLIC_COMPONENT_SUM_READY_VALUES_MISSING",
            score_ready="False",
        ),
        base_row(
            bound_id="SCB2642_6_E_DqZ_A",
            quantity="observed descent leak",
            formula="E_DqZ_A := ||Pi_A Dq_Z Z|| or theorem-zero if q and observables factor through the quotient",
            units="arena residual units",
            needed_inputs="quotient map q; observable map; metric/coframe/source/readout projection; units",
            arenas="Newton;PPN;R10;WEP;clock;orbital;EM",
            status="OBSERVED_DESCENT_MAP_MISSING",
            score_ready="False",
        ),
        base_row(
            bound_id="SCB2642_7_no_cancellation_policy",
            quantity="absolute-sum guard",
            formula="No claim may use cancellation among eps_JH, eps_JNH, eps_B, Delta_readout_abs, Q_cdb, eps_projector or E_DqZ.",
            units="policy",
            needed_inputs="each component independently zeroed or bounded",
            arenas="all local arenas",
            status="GUARD_ACTIVE",
            score_ready="False",
        ),
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            arena_id="ARENA2642_0_Newton_orbital",
            arena="Newton/orbital/GM",
            projection_formula="Delta_GM_orb <= Pi_GM[Delta_rankzero_source_abs] with fitted-GM guard",
            must_not_do="absorb source/boundary/readout residual into measured GM without common-mode theorem",
            missing_inputs="Pi_GM; orbital response kernel; M_AB normalization; source transfer convention",
            status="PROJECTION_SCHEMA_READY_VALUES_MISSING",
        ),
        base_row(
            arena_id="ARENA2642_1_PPN",
            arena="PPN gamma/beta/preferred-frame",
            projection_formula="Delta_PPN_vec <= Pi_PPN[Delta_rankzero_source_abs] + boundary alpha3 row",
            must_not_do="gamma-only pass or alpha3 cancellation",
            missing_inputs="Pi_PPN; alpha3 K_boundary/Phi coefficients; beta/nonlinear source response",
            status="PROJECTION_SCHEMA_READY_VALUES_MISSING",
        ),
        base_row(
            arena_id="ARENA2642_2_R10",
            arena="R10 short-range",
            projection_formula="strict branch has no alpha(lambda); only CDB finite-range reopening or edge/contact residual bound is legal",
            must_not_do="infer lambda from M_AB or run alpha score without Z_AB/source-test/readout-tail join",
            missing_inputs="finite Z_AB if reopened, or contact/edge residual projection; real bound curve; source/test charges",
            status="FINITE_RANGE_REJECTED_CONTACT_OR_EDGE_BOUND_ONLY",
        ),
        base_row(
            arena_id="ARENA2642_3_WEP",
            arena="WEP/composition",
            projection_formula="eta_AB <= Pi_WEP[eps_JH marker leak + eps_JNH + Delta_readout_abs + E_DqZ]",
            must_not_do="declare universality from conservation alone",
            missing_inputs="composition marker/no-marker theorem; material source map; MICROSCOPE-style projection",
            status="PROJECTION_SCHEMA_READY_VALUES_MISSING",
        ),
        base_row(
            arena_id="ARENA2642_4_clocks_EM",
            arena="clocks/time/EM",
            projection_formula="clock drift or alpha_EM drift <= Pi_clock/EM[Delta_rankzero_source_abs] + E_DqZ",
            must_not_do="hide observed descent leaks inside unit conventions",
            missing_inputs="clock observable map; EM/fine-structure readout map; DqZ projection",
            status="OBSERVED_DESCENT_VALUES_MISSING",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2642_0_source_current_identity",
            claim="P_Z[J_H + J_NH + B + J_readout + CDB + R_projector]=0",
            allowed="False",
            blocker="JH descent, JNH, boundary, readout, CDB/projector and DqZ are not all parent-signed",
        ),
        base_row(
            gate_id="CG2642_1_JH_zero",
            claim="ordinary Hilbert matter cannot source the eliminated branch",
            allowed="False",
            blocker="conditional descent lemma is clean but common matter/no-marker/Dq_Z are not parent-signed",
        ),
        base_row(
            gate_id="CG2642_2_boundary_zero",
            claim="boundary/source-worldtube terms vanish",
            allowed="False",
            blocker="proper compact representative zero is narrow; source/reference/corner boundary formula is not parent-owned",
        ),
        base_row(
            gate_id="CG2642_3_readout_zero",
            claim="readout/projector tail can be dropped",
            allowed="False",
            blocker="2638 zero attempts failed and component values are missing",
        ),
        base_row(
            gate_id="CG2642_4_local_GR_Newton",
            claim="MTS derives local GR/Newton",
            allowed="False",
            blocker="master residual vector has symbolic components only; no arena projection is score-ready",
        ),
        base_row(
            gate_id="CG2642_5_R10",
            claim="R10 short-range pass",
            allowed="False",
            blocker="strict branch has no lambda and CDB finite-range is not reopened",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2642_0_main_result",
            decision="SOURCE_CURRENT_IDENTITY_NOT_CLOSED_BOUND_PACK_INSTALLED",
            rationale="The conditional J_H descent lemma is real and useful, but the full identity still needs J_NH, boundary, readout, CDB/projector and DqZ clauses to close together.",
            consequence="local GR/Newton remains unclaimed; the retained object is Delta_rankzero_source_abs_A.",
        ),
        base_row(
            decision_id="DEC2642_1_best_gain",
            decision="JH_DESCENT_PLUS_DQZ_IS_NEXT_LEVER",
            rationale="If ordinary Hilbert matter descends and observables do not see Z, the biggest source leg is killed by theorem rather than by fitting; remaining tails become smaller explicit residuals.",
            consequence="next target should parent-sign common matter/no-marker descent or write the observed leak row.",
        ),
        base_row(
            decision_id="DEC2642_2_boundary_status",
            decision="BOUNDARY_HAS_NARROW_REAL_ZERO_BUT_NOT_FULL_SILENCE",
            rationale="1039 proper compact zero is genuine hygiene, while 1040 source-boundary formula keeps physical edge/source charges honest.",
            consequence="import proper zero only as a sublemma; retain epsilon_B_abs for source/test boundaries.",
        ),
        base_row(
            decision_id="DEC2642_3_R10_status",
            decision="STRICT_R10_STILL_REJECTED",
            rationale="The strict rank-zero branch has no lambda; R10 can return only through a future CDB finite-range operator or a contact/edge residual projection.",
            consequence="do not score alpha(lambda) from this branch.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2642_0_selected",
            next_doc="2643-Y5-R2FR-common-matter-descent-DqZ-zero-or-observed-leak-bound.md",
            next_script="scripts/Y5_R2FR_common_matter_descent_DqZ_zero_or_observed_leak_bound_2643.py",
            objective="Try to parent-sign the conditional theorem that S_matter=Sbar[q(Phi),psi,theta], v_Z in ker(Dq), and no-marker/variation-before-readout imply P_Z[J_H]=0 and E_DqZ=0; if not, write eps_JH_Z_abs and E_DqZ_A source-bound rows.",
            include="common matter action syntax; theta/no-marker rule; source-blind constants; quotient map q; Dq(v_Z); metric/coframe/source/readout observed maps; variation-before-readout",
            exclude="non-Hilbert/component cancellation; invented matter descent; empirical scoring; local GR/Newton claim; GitHub action; formalization-workbench edits",
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
                contents="2642 master source-current component-bound pack, nonclaim",
            )
        )
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    proof_rows = rows_by_name["proof_attempt"]
    bound_rows = rows_by_name["component_bound"]
    arena_rows = rows_by_name["arena_projection"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        (
            "VAL2642_00_sources",
            all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2642_01_identity_attempt",
            any(row["proof_id"] == "SCI2642_0_master_identity" and "S_Z" in row["component"] for row in proof_rows),
            "master source-current identity is written",
        ),
        (
            "VAL2642_02_conditional_JH_lemma",
            any(row["proof_id"] == "SCI2642_1_JH_descent" and row["current_result"] == "CONDITIONAL_DESCENT_LEMMA_CLEAN_NOT_PARENT_SIGNED" for row in proof_rows),
            "conditional Hilbert descent lemma is recorded but not promoted",
        ),
        (
            "VAL2642_03_all_components_visible",
            all(
                token in ";".join(row["component"] for row in proof_rows)
                for token in ["J_H", "J_NH", "boundary", "readout", "CDB", "Dq_Z"]
            ),
            "JH, JNH, boundary, readout, CDB and DqZ clauses are visible",
        ),
        (
            "VAL2642_04_bound_pack",
            any(row["bound_id"] == "SCB2642_0_master" and "Delta_rankzero_source_abs_A" in row["quantity"] for row in bound_rows),
            "master nonclaim residual bound pack is present",
        ),
        (
            "VAL2642_05_arena_coverage",
            all(token in ";".join(row["arena"] for row in arena_rows) for token in ["Newton", "PPN", "R10", "WEP", "clocks"]),
            "local arena projection skeleton covers Newton, PPN, R10, WEP and clocks",
        ),
        (
            "VAL2642_06_claim_gates_false",
            all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows),
            "all claim gates remain blocked",
        ),
        (
            "VAL2642_07_decision_next_lever",
            any(row["decision"] == "JH_DESCENT_PLUS_DQZ_IS_NEXT_LEVER" for row in decision_rows_),
            "next leverage point is JH descent plus DqZ",
        ),
        (
            "VAL2642_08_next_target",
            any(row["next_doc"].startswith("2643-Y5-R2FR-common-matter-descent") for row in next_rows),
            "2643 common-matter descent/DqZ target selected",
        ),
        (
            "VAL2642_09_branch_copies",
            all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch copies exist and parse",
        ),
        (
            "VAL2642_10_csv_parse",
            all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"),
            "all generated CSVs parse cleanly",
        ),
        (
            "VAL2642_11_formalization_untouched",
            not formalization_has_2642_artifacts(),
            "no 2642 outputs are written under formalization-workbench",
        ),
        (
            "VAL2642_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        base_row(
            validation_id=check_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
        )
        for check_id, passed, detail in checks
    ]
    rows.append(
        base_row(
            validation_id="VAL2642_OVERALL",
            status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            detail="2642 attempts the local source-current identity, installs a master nonclaim residual bound pack, and selects JH descent/DqZ as the next derivation lever",
        )
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2642 - Y5/R2FR JH/JNH Boundary Readout Source-Current Identity Or Bound Pack",
                "**Status:** source-current identity attempted. The clean theorem we can write is conditional: if ordinary matter descends through the quotient and `v_Z in ker(Dq)`, then the Hilbert source leg vanishes along the eliminated coordinate. The full local-GR identity still does not close because non-Hilbert, boundary, readout, CDB/projector and observed-descent clauses remain unsigned.",
                "**Main result:** the retained local object is now the explicit nonclaim master bound `Delta_rankzero_source_abs_A`, not a vague coupling. This is progress: the local GR/Newton problem has been turned into component zeros or component bounds.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Proof attempt",
                md_table(rows_by_name["proof_attempt"], ["proof_id", "component", "current_result", "attempted_derivation", "condition_for_zero", "obstruction", "residual_if_not_zero", "passes_now", "valid_for_claim"]),
                "## Component bound pack",
                md_table(rows_by_name["component_bound"], ["bound_id", "quantity", "formula", "units", "needed_inputs", "arenas", "status", "score_ready", "valid_for_claim"]),
                "## Arena projection skeleton",
                md_table(rows_by_name["arena_projection"], ["arena_id", "arena", "projection_formula", "must_not_do", "missing_inputs", "status", "valid_for_claim"]),
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
    for directory in (RESIDUALS, QUEUE, LOCAL_BOUNDS, MICROSCOPE):
        directory.mkdir(parents=True, exist_ok=True)
    remove_pycache()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "proof_attempt": proof_attempt_rows(),
        "component_bound": component_bound_rows(),
        "arena_projection": arena_projection_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["component_bound"])

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
