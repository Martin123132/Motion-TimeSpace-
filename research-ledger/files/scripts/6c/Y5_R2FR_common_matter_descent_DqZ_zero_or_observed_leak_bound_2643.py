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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2643-Y5-R2FR-common-matter-descent-DqZ-zero-or-observed-leak-bound.md"

CHECKPOINT = "2643"
BRANCH_ID = "Y5_R2FR_COMMON_MATTER_DESCENT_DQZ_ZERO_OR_LEAK_BOUND_2643"
PREFIX = "P8_Y5_COMMON_DESCENT_DQZ_2643"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "theorem_gate": RESIDUALS / f"{PREFIX}_PARENT_SIGNATURE_THEOREM_GATE.csv",
    "dqz_leak": RESIDUALS / f"{PREFIX}_DQZ_JH_LEAK_BOUND_ROWS.csv",
    "arena_map": RESIDUALS / f"{PREFIX}_ARENA_LEAK_MAP.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2643_QVIS_OBJECT_LANGUAGE_OR_JH_DQZ_LEAK_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "DqZ_JH_common_matter_descent_2643_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "QVIS_NO_SOURCE_SLOT_JH_DQZ_2643_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2643_00_2642",
        "role": "immediate JH/DqZ source-current handoff",
        "path": ROOT / "2642-Y5-R2FR-JH-JNH-boundary-readout-source-current-identity-or-bound-pack.md",
        "needles": ["SCI2642_1_JH_descent", "SCB2642_6_E_DqZ_A", "VAL2642_OVERALL"],
    },
    {
        "source_id": "SRC2643_01_2214",
        "role": "exact chain-rule descent formula and algebraic leak map",
        "path": ROOT / "2214-Y5-R2FR-algebraic-residual-coefficient-map-or-DqZ-source-descent-proof.md",
        "needles": ["DSD2214_0_exact_chain_rule", "CM2214_5_E_DqZ", "VAL2214_OVERALL"],
    },
    {
        "source_id": "SRC2643_02_1674",
        "role": "visible quotient ansatz and Dq_Z component matrix",
        "path": ROOT / "1674-Y5-R2FR-parent-q-Z-basis-minimal-ansatz-and-Dq-computation.md",
        "needles": ["QANS1674_1_visible_quotient", "DQM1674_0_coframe_metric", "VAL1674_OVERALL"],
    },
    {
        "source_id": "SRC2643_03_1673",
        "role": "Dq_Z zero theorem blocker and first factor value row",
        "path": ROOT / "1673-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill.md",
        "needles": ["ZTA1673_3_verdict", "DQZVAL1673_0_first_factor_value", "VAL1673_OVERALL"],
    },
    {
        "source_id": "SRC2643_04_1628",
        "role": "Hilbert source owner conditional subtheorem",
        "path": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
        "needles": ["SOC1628_1_hilbert_owner", "SOC1628_6_verdict", "VAL1628_OVERALL"],
    },
    {
        "source_id": "SRC2643_05_1886",
        "role": "common matter no-source-only slot bottleneck",
        "path": ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
        "needles": ["CG1886_0_conditional_no_slot", "DEC1886_0_no_slot_not_derived", "VAL1886_OVERALL"],
    },
    {
        "source_id": "SRC2643_06_2602",
        "role": "observed coframe/current descent and b_g leak bridge",
        "path": ROOT / "2602-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
        "needles": ["DGR2602_2_coframe_kernel", "RUN2602_0_current_descent", "VAL2602_OVERALL"],
    },
    {
        "source_id": "SRC2643_07_1038",
        "role": "matter/no-marker descent still blocks no-pole route",
        "path": ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
        "needles": ["ODC1038_7_matter_readout", "MISSING_MATTER_QUOTIENT", "V1038_SUMMARY"],
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


def formalization_has_2643_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2643-Y5-R2FR*",
        "*P8_Y5_COMMON_DESCENT_DQZ_2643*",
        "*P8_Y5_BRR545_2643*",
        "*Y5_R2FR_common_matter_descent_DqZ_zero_or_observed_leak_bound_2643*",
        "*JR2643*",
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


def theorem_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="QVIS2643_0_chain_rule_theorem",
            clause="exact common-matter descent theorem",
            theorem_or_contract="delta_vZ S_matter = D Sbar[Dq(v_Z)] + J_theta Lie_vZ(theta) + J_direct[Z] + delta_vZ B_matter. If all four terms vanish, P_Z[J_H]=0.",
            current_status="EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            needed_to_close="Dq(v_Z)=0; Lie_vZ(theta)=0; no direct Z/source-only slot; matter boundary/projector silence",
            failure_if_open="ordinary Hilbert source leg survives as eps_JH_Z_abs",
            passes_now="False",
        ),
        base_row(
            gate_id="QVIS2643_1_visible_quotient",
            clause="visible quotient Q_vis",
            theorem_or_contract="Q_vis=(e_obs,g_obs,mu_m,D_m,source/readout data,theta_owned,A_owned) and ordinary matter/readouts depend on Phi only through Q_vis.",
            current_status="MINIMAL_ANSATZ_WRITTEN_NOT_PARENT_SIGNED",
            needed_to_close="parent field chart; q(Phi); ker(Dq) basis; exclusion of Z/R_phys/phi/Gamma_mem/chi/g(z) from ordinary matter arguments",
            failure_if_open="Dq_Z and direct source/readout leaks remain legal",
            passes_now="False",
        ),
        base_row(
            gate_id="QVIS2643_2_kernel_membership",
            clause="v_Z in ker(Dq)",
            theorem_or_contract="For eliminated Z directions, Dq(v_Z)=0 with declared q/Z norms and source/readout/boundary columns.",
            current_status="DqZ_ZERO_NOT_PROVED",
            needed_to_close="computable Dq matrix, selected Z basis, operator norm convention, constraint-first elimination signature",
            failure_if_open="Dq_Z_norm remains MISSING_NUMERIC_OR_THEOREM_ZERO",
            passes_now="False",
        ),
        base_row(
            gate_id="QVIS2643_3_no_marker_theta",
            clause="theta/no-marker silence",
            theorem_or_contract="theta constants, clock standards, EM readouts and material labels are quotient/superselection data, not representative-Z fields.",
            current_status="NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            needed_to_close="theta ownership; hidden-frame ban; material marker/source-only frame exclusion; readout-before/after variation rule",
            failure_if_open="J_theta Lie_vZ(theta), clock/EM drift, and WEP marker residuals remain",
            passes_now="False",
        ),
        base_row(
            gate_id="QVIS2643_4_no_source_only_slot",
            clause="no direct Z/pre-action source-only slot",
            theorem_or_contract="ordinary matter object language forbids S_matter=sum_i w_i(Z) S_i, direct F(Z) matter vertices, and source-only representative labels.",
            current_status="SOURCE_WEIGHT_SEAM_OPEN",
            needed_to_close="parent object-language typing/action-scale normalization theorem, or finite w_R/beta_w/Delta_w vector",
            failure_if_open="classical EOM may look universal while Hilbert source weights differ",
            passes_now="False",
        ),
        base_row(
            gate_id="QVIS2643_5_observed_descent",
            clause="DObs/DqZ observed descent",
            theorem_or_contract="If Obs_A=Obs_A(Q_vis), then DObs_A(v_Z)=DObs_A Dq(v_Z)=0; otherwise E_DqZ_A is additive.",
            current_status="CHAIN_RULE_EXACT_OBSERVED_MAP_UNSIGNED",
            needed_to_close="coframe functor; source/current map; readout map; boundary/projector map; tau/current projectability",
            failure_if_open="E_DqZ_A and b_g/common-frame derivative bridge survive",
            passes_now="False",
        ),
        base_row(
            gate_id="QVIS2643_6_verdict",
            clause="J_H=0 and E_DqZ=0 parent signature",
            theorem_or_contract="All QVIS2643_0..5 close in one parent branch before any local empirical scoring.",
            current_status="NOT_CLOSED_FINITE_LEAK_ROWS_REQUIRED",
            needed_to_close="Q_vis object-language parent signature or finite eps_JH/E_DqZ vector",
            failure_if_open="2642 master residual keeps eps_JH_Z_abs and E_DqZ_A",
            passes_now="False",
        ),
    ]


def dqz_leak_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            leak_id="LEAK2643_0_eps_JH_Z_abs",
            quantity="ordinary Hilbert source leak",
            formula="eps_JH_Z_abs <= C_matter*Dq_Z_norm + eps_theta_marker + eps_direct_Z + eps_source_weight + eps_matter_boundary",
            units="dimensionless source-normalized",
            blockers="MISSING_DQZ_ZERO_OR_VALUE;MISSING_THETA_NO_MARKER;MISSING_NO_SOURCE_ONLY_SLOT;MISSING_MATTER_BOUNDARY_SILENCE",
            arenas="Newton;PPN;R10;WEP;clock;orbital;EM",
            status="BOUND_FORM_READY_VALUES_MISSING",
            score_ready="False",
        ),
        base_row(
            leak_id="LEAK2643_1_Dq_Z_norm",
            quantity="quotient vertical leakage",
            formula="Dq_Z_norm := ||Dq[v_Z]||_q / ||v_Z||_Z",
            units="operator norm after q/Z norm declaration",
            blockers="MISSING_COMPUTABLE_Q_MAP;MISSING_Z_BASIS;MISSING_Q_Z_NORMS;MISSING_SOURCE_READOUT_DESCENT",
            arenas="all local observed arenas",
            status="MISSING_NUMERIC_OR_THEOREM_ZERO",
            score_ready="False",
        ),
        base_row(
            leak_id="LEAK2643_2_E_DqZ_A",
            quantity="observed arena descent leak",
            formula="E_DqZ_A <= C_A_obs*Dq_Z_norm*N_Z + E_theta_A + E_readout_A + E_boundary_projector_A",
            units="arena residual units",
            blockers="MISSING_OBSERVED_COFRAME_FUNCTOR;MISSING_SOURCE_MAP;MISSING_READOUT_DESCENT;MISSING_BOUNDARY_PROJECTOR_MAP",
            arenas="Newton;PPN;R10;WEP;clock;orbital;EM",
            status="ARENA_MAP_READY_VALUES_MISSING",
            score_ready="False",
        ),
        base_row(
            leak_id="LEAK2643_3_source_weight_seam",
            quantity="pre-action source-only weight",
            formula="Delta_w_abs := max_ij |w_i-w_j| or beta_w product leg if source weights are legal",
            units="dimensionless relative source weight",
            blockers="PARENT_OBJECT_LANGUAGE_NO_SOURCE_SLOT_UNSIGNED",
            arenas="WEP;Newton_GM;PPN;R10_source_test",
            status="COUNTEREXAMPLE_RETAINED",
            score_ready="False",
        ),
        base_row(
            leak_id="LEAK2643_4_theta_marker",
            quantity="theta/material marker leak",
            formula="eps_theta_marker <= ||J_theta Lie_vZ(theta)||/||J_ref|| + marker/source-label readout terms",
            units="source-normalized or arena-specific",
            blockers="NO_MARKER_THEOREM_NOT_PARENT_SIGNED;HIDDEN_FRAME_BAN_UNSIGNED",
            arenas="WEP;clock;EM;R10;PPN",
            status="BOUND_ROW_REQUIRED",
            score_ready="False",
        ),
        base_row(
            leak_id="LEAK2643_5_bg_bridge",
            quantity="observed coframe/common-frame metric leak",
            formula="for g_obs=e^(2 sigma_X)g_GR with sigma_X=s_X U/c^2, gamma_eff=(1+s_X)/(1-s_X); b_g path remains nonclaim until b_g,x_U and no-other-channel proof exist",
            units="PPN gamma response coefficient",
            blockers="MISSING_BG;MISSING_X_U;MISSING_NO_OTHER_CHANNEL_PROOF;MISSING_DQ_TAU_PROJECTABILITY",
            arenas="PPN_gamma;R10_bridge;clock/WEP via observed frame",
            status="SOURCE_BACKED_FORM_NONCLAIM",
            score_ready="False",
        ),
        base_row(
            leak_id="LEAK2643_6_master_policy",
            quantity="no-cancellation policy",
            formula="eps_JH_Z_abs and E_DqZ_A enter 2642 master residual additively; no cancellation with J_NH, CDB, boundary or readout tails is allowed.",
            units="policy",
            blockers="component theorem-zero or numeric rows required independently",
            arenas="all local arenas",
            status="GUARD_ACTIVE",
            score_ready="False",
        ),
    ]


def arena_map_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            arena_id="AM2643_0_Newton",
            arena="Newton/GM/orbital",
            leak_path="Delta_GM <= Pi_GM(eps_JH_Z_abs + E_DqZ_GM + source_weight + boundary/readout tails)",
            current_status="FITTED_GM_GUARD_ACTIVE",
            missing_inputs="common-mode GM theorem; source map; DqZ norm; orbital projection",
        ),
        base_row(
            arena_id="AM2643_1_PPN",
            arena="PPN gamma/beta/preferred-frame",
            leak_path="Delta_PPN <= Pi_PPN(eps_JH_Z_abs + E_DqZ_PPN) plus b_g/sigma_X bridge and alpha3 boundary row",
            current_status="SCHEMA_READY_VALUES_MISSING",
            missing_inputs="b_g,x_U,no-other-channel proof, PPN vector projection",
        ),
        base_row(
            arena_id="AM2643_2_WEP",
            arena="WEP/composition",
            leak_path="eta_AB <= Pi_WEP(Delta_w_abs + eps_theta_marker + E_DqZ_WEP + readout marker tail)",
            current_status="NO_MARKER_AND_NO_SOURCE_SLOT_UNSIGNED",
            missing_inputs="object-language no-source-slot theorem or finite Delta_w vector; material marker map",
        ),
        base_row(
            arena_id="AM2643_3_R10",
            arena="R10/contact or source-test branch",
            leak_path="strict branch has no lambda; DqZ/source leak can only feed contact/edge/CDB-reopened finite-range rows",
            current_status="STRICT_ALPHA_LAMBDA_REJECTED",
            missing_inputs="finite principal symbol if reopened, source/test charge split, real bound curve, DqZ/contact projection",
        ),
        base_row(
            arena_id="AM2643_4_clock_EM",
            arena="clock/time/EM",
            leak_path="Delta_clock/alpha_EM <= Pi_theta(eps_theta_marker + E_DqZ_clock/EM + readout standard leak)",
            current_status="THETA_MARKER_DESCENT_UNSIGNED",
            missing_inputs="theta ownership; EM/fine-structure readout map; clock standard quotient descent",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2643_0_JH_zero",
            claim="P_Z[J_H]=0 for ordinary matter",
            allowed="False",
            blocker="exact chain-rule theorem exists, but Q_vis/no-marker/no-source-slot/boundary clauses are not parent-signed",
        ),
        base_row(
            gate_id="CG2643_1_DqZ_zero",
            claim="Dq_Z=0 for all observed local arenas",
            allowed="False",
            blocker="minimal q/Z ansatz is conditional; Dq matrix, source/readout descent and norms are not parent-signed",
        ),
        base_row(
            gate_id="CG2643_2_no_source_slot",
            claim="parent ordinary matter object language forbids source-only weights",
            allowed="False",
            blocker="1886 keeps source-weight seam live until object-language/action-scale rule is derived",
        ),
        base_row(
            gate_id="CG2643_3_local_GR_Newton",
            claim="local GR/Newton reduction follows",
            allowed="False",
            blocker="eps_JH_Z_abs and E_DqZ_A remain symbolic components of the 2642 master residual",
        ),
        base_row(
            gate_id="CG2643_4_empirical_scoring",
            claim="PPN/WEP/R10/clock/orbital rows can be scored",
            allowed="False",
            blocker="no finite source-backed MTS coefficient rows yet",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2643_0_main_result",
            decision="CONDITIONAL_THEOREM_CONSOLIDATED_PARENT_SIGNATURE_NOT_CLOSED",
            rationale="The chain-rule proof is exact: quotient-invariant matter plus v_Z in ker(Dq) kills the Hilbert source and observed leak. The current corpus still lacks the parent Q_vis/object-language signature.",
            consequence="carry eps_JH_Z_abs and E_DqZ_A as explicit nonclaim leak rows.",
        ),
        base_row(
            decision_id="DEC2643_1_best_next",
            decision="QVIS_OBJECT_LANGUAGE_IS_THE_NEXT_WALL",
            rationale="DqZ, J_H, theta markers, and source weights all collapse if the parent object language says ordinary matter only sees Q_vis and has no source-only/action-weight slot.",
            consequence="attack Q_vis object-language typing before more empirical scoring.",
        ),
        base_row(
            decision_id="DEC2643_2_progress",
            decision="LOCAL_GR_ROUTE_BECOMES_A_SIGNATURE_PROBLEM",
            rationale="This is better than a loose coupling hunt: we now know exactly what the parent action must forbid or include as a finite residual.",
            consequence="the next file should either sign the grammar or write a finite JH/DqZ vector validator.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2643_0_selected",
            next_doc="2644-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-vector.md",
            next_script="scripts/Y5_R2FR_Qvis_object_language_no_source_slot_or_finite_JH_DqZ_vector_2644.py",
            objective="Try to parent-sign the object-language rule that ordinary matter/readouts are functors of Q_vis only, with no direct Z slot, no source-only weights and no theta marker; if it fails, build the finite eps_JH_Z_abs/E_DqZ_A vector validator.",
            include="Q_vis grammar; field chart; q(Phi); no direct Z/R_AB slot; no pre-action w_A; theta/no-marker; source/readout descent; finite leak-vector schema",
            exclude="empirical scoring; source-weight absorption into G_N without common-mode proof; invented no-marker axiom; local GR/Newton claim; GitHub action; formalization-workbench edits",
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
                contents="2643 Q_vis/JH/DqZ leak rows, nonclaim",
            )
        )
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["theorem_gate"]
    leak_rows = rows_by_name["dqz_leak"]
    arena_rows = rows_by_name["arena_map"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        (
            "VAL2643_00_sources",
            all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2643_01_chain_rule",
            any(row["gate_id"] == "QVIS2643_0_chain_rule_theorem" and "EXACT_CONDITIONAL" in row["current_status"] for row in theorem_rows),
            "exact conditional chain-rule theorem is recorded",
        ),
        (
            "VAL2643_02_signature_not_closed",
            any(row["gate_id"] == "QVIS2643_6_verdict" and row["current_status"] == "NOT_CLOSED_FINITE_LEAK_ROWS_REQUIRED" for row in theorem_rows),
            "parent signature gate remains nonclaim",
        ),
        (
            "VAL2643_03_leak_rows",
            all(token in ";".join(row["quantity"] for row in leak_rows) for token in ["ordinary Hilbert", "quotient vertical", "observed arena", "source-only", "theta"]),
            "JH, DqZ, observed, source-weight and theta leak rows are present",
        ),
        (
            "VAL2643_04_arena_coverage",
            all(token in ";".join(row["arena"] for row in arena_rows) for token in ["Newton", "PPN", "WEP", "R10", "clock"]),
            "arena map covers Newton, PPN, WEP, R10 and clock/EM",
        ),
        (
            "VAL2643_05_claim_gates_false",
            all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows),
            "all claim gates remain blocked",
        ),
        (
            "VAL2643_06_next_wall",
            any(row["decision"] == "QVIS_OBJECT_LANGUAGE_IS_THE_NEXT_WALL" for row in decision_rows_),
            "decision selects Qvis object-language wall",
        ),
        (
            "VAL2643_07_next_target",
            any(row["next_doc"].startswith("2644-Y5-R2FR-Qvis-object-language") for row in next_rows),
            "2644 Qvis object-language/no-source-slot target selected",
        ),
        (
            "VAL2643_08_branch_copies",
            all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch copies exist and parse",
        ),
        (
            "VAL2643_09_csv_parse",
            all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"),
            "all generated CSVs parse cleanly",
        ),
        (
            "VAL2643_10_formalization_untouched",
            not formalization_has_2643_artifacts(),
            "no 2643 outputs are written under formalization-workbench",
        ),
        (
            "VAL2643_11_pycache_absent",
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
            validation_id="VAL2643_OVERALL",
            status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            detail="2643 consolidates the common-matter/DqZ descent theorem, refuses parent-signature promotion, stages explicit leak rows, and selects Qvis object-language/no-source-slot as next target",
        )
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2643 - Y5/R2FR Common Matter Descent DqZ Zero Or Observed Leak Bound",
                "**Status:** the exact theorem is now consolidated: if ordinary matter/readouts are functors of `Q_vis=q(Phi)`, if `v_Z in ker(Dq)`, and if theta/source markers carry no representative label, then `P_Z[J_H]=0` and `E_DqZ_A=0`. Current MTS does not yet parent-sign those clauses together.",
                "**Main result:** the local-GR source side is now a parent object-language problem. Either the parent grammar forbids direct `Z`/source-only/marker slots, or the theory must carry finite `eps_JH_Z_abs` and `E_DqZ_A` leak rows into every local arena.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Parent signature theorem gate",
                md_table(rows_by_name["theorem_gate"], ["gate_id", "clause", "current_status", "theorem_or_contract", "needed_to_close", "failure_if_open", "passes_now", "valid_for_claim"]),
                "## DqZ/JH leak rows",
                md_table(rows_by_name["dqz_leak"], ["leak_id", "quantity", "formula", "units", "blockers", "arenas", "status", "score_ready", "valid_for_claim"]),
                "## Arena leak map",
                md_table(rows_by_name["arena_map"], ["arena_id", "arena", "leak_path", "current_status", "missing_inputs", "valid_for_claim"]),
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
    for directory in (RESIDUALS, QUEUE, LOCAL_BOUNDS, SOURCE_WEIGHT):
        directory.mkdir(parents=True, exist_ok=True)
    remove_pycache()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "theorem_gate": theorem_gate_rows(),
        "dqz_leak": dqz_leak_rows(),
        "arena_map": arena_map_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["dqz_leak"])

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
