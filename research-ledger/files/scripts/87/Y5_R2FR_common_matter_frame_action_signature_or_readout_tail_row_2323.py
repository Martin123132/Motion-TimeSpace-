from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_COMMON_MATTER_FRAME_OR_READOUT_TAIL_2323"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2323-Y5-R2FR-common-matter-frame-action-signature-or-readout-tail-row.md"

PATHS = {
    "2322_doc": ROOT / "2322-Y5-R2FR-tau-PPN-or-common-frame-parent-signature.md",
    "2322_validation": OUT / "P8_Y5_BRR545_2322_VALIDATION.csv",
    "2322_signature": OUT / "P8_Y5_PARENT_QLOC_2322_PARENT_SIGNATURE_CLAUSE_LEDGER.csv",
    "2322_tau": OUT / "P8_Y5_PARENT_QLOC_2322_CONDITIONAL_TAU_NORMALIZATION_ROWS.csv",
    "2122_owner": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
    "2122_comm": OUT / "P8_Y5_PARENT_QLOC_2122_COMMUTATOR_OBSTRUCTION_LEDGER.csv",
    "2123_pi": OUT / "P8_Y5_PARENT_QLOC_2123_PI_SPLIT_THEOREM.csv",
    "2123_zero": OUT / "P8_Y5_PARENT_QLOC_2123_COMMUTATOR_ZERO_CONDITIONS.csv",
    "2124_chain": OUT / "P8_Y5_PARENT_QLOC_2124_SOURCE_FEEDBACK_CHAIN_RULE.csv",
    "2124_gm": OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv",
    "2125_common": OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv",
    "2125_refusal": OUT / "P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv",
    "2159_moms": OUT / "P8_Y5_PARENT_QLOC_2159_MOMS_SIGNATURE_ATTEMPT.csv",
    "2159_translation": OUT / "P8_Y5_PARENT_QLOC_2159_CG_PPN_TRANSLATION_GATE.csv",
    "2203_fixed": OUT / "P8_Y5_PARENT_QLOC_2203_FIXED_BEFORE_READOUT_MAP_ATTEMPT.csv",
    "2203_readout": OUT / "P8_Y5_PARENT_QLOC_2203_ALPHA_READOUT_ROW.csv",
    "2203_gm": OUT / "P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "2208_blockers": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_BLOCKER_LEDGER.csv",
    "2318_functor": OUT / "P8_Y5_PARENT_QLOC_2318_PARENT_COEFFICIENT_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
    "2318_obligations": OUT / "P8_Y5_PARENT_QLOC_2318_FUNCTOR_PROOF_OBLIGATION_LEDGER.csv",
}

SOURCES = [
    ("SRC2323_00_2322_doc", "2322_doc", PATHS["2322_doc"], ["NEXT2322_0", "common-matter-frame-action-signature"], "2322 handoff"),
    ("SRC2323_01_2322_validation", "2322_validation", PATHS["2322_validation"], ["VAL2322_OVERALL", "PASS"], "2322 validation"),
    ("SRC2323_02_2322_signature", "2322_signature", PATHS["2322_signature"], ["SIG2322_5_verdict", "COMMON_FRAME_SIGNATURE_NOT_DERIVED"], "parent signature blockers"),
    ("SRC2323_03_2322_tau", "2322_tau", PATHS["2322_tau"], ["CTN2322_0_canonical_alpha", "tau_PPN=1"], "conditional tau row"),
    ("SRC2323_04_2122_owner", "2122_owner", PATHS["2122_owner"], ["SRO2122_0_exact_conditional", "CONDITIONAL_PROOF_VALID"], "source/readout owner lemma"),
    ("SRC2323_05_2122_comm", "2122_comm", PATHS["2122_comm"], ["COM2122_1_when_zero", "CONDITIONAL_ZERO_ROUTE"], "commutator obstruction"),
    ("SRC2323_06_2123_pi", "2123_pi", PATHS["2123_pi"], ["PIS2123_2_q_descended_projector", "CONDITIONAL_ZERO_VALID"], "Pi split theorem"),
    ("SRC2323_07_2123_zero", "2123_zero", PATHS["2123_zero"], ["ZC2123_5_no_cancellation", "RETAINED"], "zero conditions"),
    ("SRC2323_08_2124_chain", "2124_chain", PATHS["2124_chain"], ["CR2124_4_verdict", "NORMAL_FORM_CLOSED_NUMERIC_BOUND_OPEN"], "source feedback chain rule"),
    ("SRC2323_09_2124_gm", "2124_gm", PATHS["2124_gm"], ["GM2124_3_verdict", "GUARD_NORMAL_FORM_CLOSED_DATA_OPEN"], "GM guard descent"),
    ("SRC2323_10_2125_common", "2125_common", PATHS["2125_common"], ["CMD2125_4_verdict", "THEOREM_TARGET_SHARPENED_NOT_CLOSED"], "common-mode descent"),
    ("SRC2323_11_2125_refusal", "2125_refusal", PATHS["2125_refusal"], ["REF2125_1_measured_G_hiding", "REFUSED"], "GM absorption refusal"),
    ("SRC2323_12_2159_moms", "2159_moms", PATHS["2159_moms"], ["MOM2159_7_verdict", "FAIL_CURRENT_CLAIM"], "MOMS signature"),
    ("SRC2323_13_2159_translation", "2159_translation", PATHS["2159_translation"], ["CGT2159_0_universal_common_frame", "NOT_PARENT_SIGNED"], "common-frame translation gate"),
    ("SRC2323_14_2203_fixed", "2203_fixed", PATHS["2203_fixed"], ["FBR2203_7_verdict", "source identity exists only as residual/obstruction vector"], "fixed-before-readout attempt"),
    ("SRC2323_15_2203_readout", "2203_readout", PATHS["2203_readout"], ["ARW2203_0_alpha_readout", "MISSING_FIXED_READOUT_FUNCTOR"], "alpha_readout row"),
    ("SRC2323_16_2203_gm", "2203_gm", PATHS["2203_gm"], ["MGV2203_7_calibration_PPN_tail", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL"], "measured-GM obstruction"),
    ("SRC2323_17_2208_blockers", "2208_blockers", PATHS["2208_blockers"], ["PPNB2208_3_PPN_gauge", "MISSING_PPN_GAUGE_TRANSFORM"], "PPN blockers"),
    ("SRC2323_18_2318_functor", "2318_functor", PATHS["2318_functor"], ["PCF2318_5_verdict", "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED"], "coefficient functor"),
    ("SRC2323_19_2318_obligations", "2318_obligations", PATHS["2318_obligations"], ["OBL2318_4_readout_closure", "RADIATIVE_READOUT_CLOSURE_UNSIGNED"], "readout closure obligation"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2323_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_2323_COMMON_FRAME_THEOREM_ATTEMPT.csv",
    "readout_tail": OUT / "P8_Y5_PARENT_QLOC_2323_ALPHA_READOUT_TAIL_ROW.csv",
    "commutator": OUT / "P8_Y5_PARENT_QLOC_2323_SOURCE_FEEDBACK_COMMUTATOR_BRIDGE.csv",
    "score_update": OUT / "P8_Y5_PARENT_QLOC_2323_PPN_SCORE_OBJECT_UPDATE.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2323_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2323_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2323_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2323_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2323_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2323_0_theorem", OUTPUTS["theorem"], BETA_DOCS / "COMMON_FRAME_THEOREM_ATTEMPT_2323_NONCLAIM.csv"),
    ("COPY2323_1_readout_tail", OUTPUTS["readout_tail"], MICRO_RESIDUALS / "alpha_readout_tail_row_nonclaim_2323.csv"),
    ("COPY2323_2_commutator", OUTPUTS["commutator"], RAB_QUEUE / "JR2323_SOURCE_FEEDBACK_COMMUTATOR_BRIDGE_NONCLAIM.csv"),
    ("COPY2323_3_score_update", OUTPUTS["score_update"], RAB_QUEUE / "JR2323_PPN_SCORE_OBJECT_UPDATE_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFT2323_0_candidate_theorem",
            "clause": "common matter-frame/readout theorem",
            "formal_statement": "If S_matter=Sbar[Psi,e_obs(q(Phi)),theta] and every source/readout projector used before scoring descends through (q,e_obs,theta), then vertical hidden variations do not change the matter metric, source current, or PPN readout.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_gap": "parent action has not signed the descent/functor/projector clauses",
            "closes_if_signed": "common frame; tau_PPN=1 branch; alpha_readout=0; source-feedback commutator zero",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFT2323_1_matter_action",
            "clause": "one ordinary matter action",
            "formal_statement": "one parent-selected matter action defines the metric/coframe seen by all ordinary matter before calibration and fitting",
            "proof_status": "SCHEMA_AVAILABLE_NOT_DERIVED",
            "current_gap": "MOMS action object and parent coefficient functor remain unsigned",
            "closes_if_signed": "prevents species/shadow metric split in alpha_cg",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFT2323_2_projector_support",
            "clause": "projector/support descent",
            "formal_statement": "Pi_A and source support sigma_A are q/e_obs-descended or fixed external protocol before variation",
            "proof_status": "CONDITIONAL_ZERO_WITH_COUNTERMODEL",
            "current_gap": "source worldtube, boundary/support, and projector descent certificates are missing",
            "closes_if_signed": "kills (delta Pi)J and support-domain readout tails",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFT2323_3_GM_PPN",
            "clause": "measured-GM and PPN-gauge guard",
            "formal_statement": "G_ref, source mass, PPN gauge transform, and Cassini/orbital readout are fixed before residual scoring",
            "proof_status": "GUARD_NORMAL_FORM_CLOSED_DATA_OPEN",
            "current_gap": "calibration equation, source-weight basis, and PPN gauge transform are not parent-owned",
            "closes_if_signed": "prevents post-fit absorption/cancellation of alpha_cg or alpha_readout",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CFT2323_4_verdict",
            "clause": "common matter-frame signature closes now",
            "formal_statement": "CFT2323_0 through CFT2323_3 are all parent-signed in the active branch",
            "proof_status": "NOT_DERIVED_RETAIN_ALPHA_READOUT",
            "current_gap": "the exact theorem exists, but the active branch lacks the signature certificates",
            "closes_if_signed": "not closed; retain explicit PPN readout component",
            "valid_for_claim": "false",
        },
    ]


def build_readout_tail_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ART2323_0_alpha_readout",
            "component": "alpha_readout",
            "formula": "alpha_readout = Pi_gamma[Delta_cal + Delta_PPN + C_feedback + C_protocol]",
            "source_basis": "ARW2203_0_alpha_readout;MGV2203_7_calibration_PPN_tail;CR2124_4_verdict",
            "current_status": "RETAINED_NONCLAIM_COMPONENT",
            "missing_for_bound": "numeric/source-backed Delta_cal, Delta_PPN, C_feedback, C_protocol or theorem-zero certificates",
            "observable_link": "Cassini gamma/Shapiro; beta/gamma; measured GM; orbital calibration",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ART2323_1_source_feedback",
            "component": "C_feedback",
            "formula": "D_v(Pi_A J_A)=[D_sigma Pi_A[J_A]+Pi_A D_sigma J_A]D_v sigma_A",
            "source_basis": "CR2124_1_vertical_variation;COM2122_0_identity",
            "current_status": "NORMAL_FORM_DERIVED_VALUES_MISSING",
            "missing_for_bound": "Lipschitz/operator norm and epsilon_sigma_A for relevant source/readout channel",
            "observable_link": "WEP; PPN; R10; source-normalization",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ART2323_2_protocol_tail",
            "component": "C_protocol",
            "formula": "C_protocol=0 only if masks/support/orbit windows/boundary transport are fixed external protocol or q/e_obs descendants",
            "source_basis": "PIS2123_3_external_protocol;ZC2123_2_fixed_protocol",
            "current_status": "CLOSURE_OR_SOURCE_REQUIRED",
            "missing_for_bound": "parent declaration or source path for protocol plus finite bound if not theorem-zero",
            "observable_link": "PPN gauge; support/domain; finite source",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ART2323_3_no_cancellation",
            "component": "absolute PPN readout envelope",
            "formula": "abs(alpha_PPN_total) <= abs(alpha_cg)+abs(alpha_dis)+abs(alpha_nonH)+abs(alpha_support)+abs(alpha_boundary)+abs(alpha_readout)",
            "source_basis": "ARW2203_1_no_cancellation_guard;ZC2123_5_no_cancellation",
            "current_status": "ENVELOPE_ACTIVE_VALUES_MISSING",
            "missing_for_bound": "all component values or theorem-zero rows",
            "observable_link": "local-GR/PPN acceptance gate",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_commutator_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2323_0_zero_route",
            "object": "source/readout commutator",
            "mathematical_statement": "If Pi_A=Pi_bar_A(q,e_obs,theta) and J_A=Jbar_A(q,e_obs,theta), then D_v(Pi_A J_A)=0 for v in ker(Dq).",
            "status": "EXACT_CONDITIONAL_ZERO",
            "active_branch_status": "UNSIGNED_FOR_SOURCE_FEEDBACK",
            "next_evidence": "sector descent certificates for support, weights, boundary, GM and readout",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2323_1_bound_route",
            "object": "finite readout/source feedback kernel",
            "mathematical_statement": "||D_v K_A|| <= (||D_sigma Pi_A||||J_A||+||Pi_A||||D_sigma J_A||)||D_v sigma_A||",
            "status": "FINITE_BOUND_NORMAL_FORM_DERIVED",
            "active_branch_status": "NUMERIC_BOUND_OPEN",
            "next_evidence": "operator norms and protocol-leakage epsilon_sigma_A",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFC2323_2_countermodel",
            "object": "representative/protocol-dependent support",
            "mathematical_statement": "If sigma_A or Pi_A depends on representative/source/mask data not fixed by q/e_obs, then (delta Pi_A)J_A can be nonzero.",
            "status": "COUNTERMODEL_RETAINED",
            "active_branch_status": "BLOCKS_THEOREM_PROMOTION",
            "next_evidence": "parent object-language exclusion or source-backed bound",
            "valid_for_claim": "false",
        },
    ]


def build_score_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSU2323_0_current_ppn_vector",
            "score_object": "absolute PPN residual vector",
            "formula": "alpha_total_abs >= abs(alpha_cg)+abs(alpha_readout)+other live components",
            "update": "alpha_readout is now explicitly retained unless common-frame/readout descent theorem closes",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSU2323_1_tau_activation_rule",
            "score_object": "tau_PPN=1 activation",
            "formula": "allowed only if common matter-frame signature and readout/source descent rows pass",
            "update": "2323 supplies the exact signature clauses needed to activate 2322 conditional tau",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSU2323_2_local_gr_status",
            "score_object": "local GR/Newton recovery",
            "formula": "requires alpha_cg, alpha_readout, source-normalization, support, boundary, and nonEH tails theorem-zero or bounded",
            "update": "common-frame proof not closed; local-GR claim remains blocked but target is sharper",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2323_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2323_1_conditional_theorem",
            "gate": "common-frame/readout theorem exact conditionally",
            "passed": "true",
            "claim_effect": "the proof shape is valid if premises are signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2323_2_parent_signature",
            "gate": "active parent common-frame signature signed",
            "passed": "false",
            "claim_effect": "cannot activate tau_PPN=1 or alpha_readout=0",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2323_3_readout_tail_bound",
            "gate": "alpha_readout theorem-zero or numerically bounded",
            "passed": "false",
            "claim_effect": "PPN vector still not score-ready",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2323_4_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still a target, not a result",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2323_0_alpha_readout_zero",
            "claim": "alpha_readout=0 in active branch",
            "allowed": "false",
            "reason": "zero requires q/e_obs descent of source/readout projectors and fixed-before-readout certificates; these are unsigned",
            "blocking_rows": "CFT2323_2_projector_support;ART2323_0_alpha_readout;SFC2323_2_countermodel",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2323_1_tau_activation",
            "claim": "activate tau_PPN=1 from 2322",
            "allowed": "false",
            "reason": "2323 does not close the common matter-frame signature; tau_PPN=1 remains conditional",
            "blocking_rows": "CFT2323_4_verdict;PSU2323_1_tau_activation_rule",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2323_2_measured_G_hiding",
            "claim": "measured GM can absorb readout/source tails",
            "allowed": "false",
            "reason": "only universal common-mode calibration can be absorbed; relative/source-feedback tails remain live",
            "blocking_rows": "CMD2125_3_measured_G_guard;REF2125_1_measured_G_hiding;ART2323_0_alpha_readout",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2323_3_local_GR",
            "claim": "2323 derives local GR/Newton",
            "allowed": "false",
            "reason": "2323 sharpens the theorem/retained-tail split but does not complete the residual vector",
            "blocking_rows": "CG2323_4_local_GR_Newton;PSU2323_2_local_gr_status",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2323_0",
            "next_target": "2324-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md",
            "why": "2323 retains alpha_readout as the active obstruction; next either prove projector/support/readout descent enough to set it zero, or fill the first source-backed bound row for the readout tail.",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2323_1",
            "next_target": "2324b-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-syntax-proof.md",
            "why": "parallel cleaner route: prove the missing object-language clause that forbids relative source weights before they become readout tails.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    add("VAL2323_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2323_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    theorem_rows = read_csv_rows(OUTPUTS["theorem"])
    add("VAL2323_02_conditional_theorem", any(row.get("row_id") == "CFT2323_0_candidate_theorem" and row.get("proof_status") == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows), "conditional common-frame/readout theorem row exists")
    add("VAL2323_03_parent_signature_not_promoted", any(row.get("row_id") == "CFT2323_4_verdict" and row.get("proof_status") == "NOT_DERIVED_RETAIN_ALPHA_READOUT" for row in theorem_rows), "active parent signature remains unpromoted")
    readout_rows = read_csv_rows(OUTPUTS["readout_tail"])
    add("VAL2323_04_alpha_readout_retained", any(row.get("row_id") == "ART2323_0_alpha_readout" and row.get("current_status") == "RETAINED_NONCLAIM_COMPONENT" for row in readout_rows), "alpha_readout retained as explicit nonclaim component")
    score_rows = read_csv_rows(OUTPUTS["score_update"])
    add("VAL2323_05_score_objects_nonready", all(row.get("score_ready") == "false" for row in score_rows), "score object updates remain non-score-ready")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2323_06_claim_gates_block", any(row.get("row_id") == "CG2323_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2323_07_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks premature readout/local-GR claims")
    add("VAL2323_08_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 1, "next target selected")
    add("VAL2323_09_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2323_10_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2323*.csv", "*2323-Y5*.md", "*COMMON_MATTER_FRAME*2323*", "*MTS_R2FR_COMMON_MATTER_FRAME_OR_READOUT_TAIL_2323*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2323_11_formalization_untouched_by_2323", not formalization_hits, "no 2323 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2323_OVERALL", all(row["status"] == "PASS" for row in rows), "2323 proves the common-frame/readout theorem only conditionally, keeps the active parent signature unsigned, retains alpha_readout as an explicit PPN component, and blocks local-GR/Newton claims.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    readout_tail_rows: list[dict[str, Any]],
    commutator_rows: list[dict[str, Any]],
    score_update_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2323 - Common Matter Frame Action Signature Or Readout Tail Row

## Summary

2323 lands the exact conditional theorem we wanted, but does not promote it to a claim. If the parent action selects one
ordinary matter frame `e_obs(q(Phi))`, and every source/readout projector used before PPN scoring descends through that
same `(q,e_obs)` data, then vertical hidden variations do not move the matter metric, source current, or readout map.
In that signed branch, `alpha_readout=0` and the 2322 `tau_PPN=1` conditional can activate.

The active branch is not there yet. Projector/support descent, source worldtube ownership, fixed-before-readout GM
calibration, PPN gauge transformation, and the no-source-only-species-slot clause remain unsigned. Therefore 2323 keeps
`alpha_readout` as a live PPN component instead of pretending the readout tail vanished.

This is a useful tightening: the path to local GR is no longer "hope the readout behaves"; it is now a finite theorem-or-bound
choice for `alpha_readout`.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Common Frame Theorem Attempt

{markdown_table(theorem_rows, ["row_id", "clause", "formal_statement", "proof_status", "current_gap", "closes_if_signed", "valid_for_claim"])}

## alpha_readout Tail Row

{markdown_table(readout_tail_rows, ["row_id", "component", "formula", "current_status", "missing_for_bound", "observable_link", "score_ready", "valid_for_claim"])}

## Source Feedback Commutator Bridge

{markdown_table(commutator_rows, ["row_id", "object", "mathematical_statement", "status", "active_branch_status", "next_evidence", "valid_for_claim"])}

## PPN Score Object Update

{markdown_table(score_update_rows, ["row_id", "score_object", "formula", "update", "score_ready", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "theorem": build_theorem_rows(),
        "readout_tail": build_readout_tail_rows(),
        "commutator": build_commutator_rows(),
        "score_update": build_score_update_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["theorem"],
        rows_by_output["readout_tail"],
        rows_by_output["commutator"],
        rows_by_output["score_update"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2323 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
