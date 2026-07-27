from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_QV_SECTOR_PIECE_LEDGER_OR_REAL_BALPHA_BG_SOURCE_ACQUISITION_2436"
CHECKPOINT_ID = "2436"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2436-Y5-R2FR-Qv-sector-piece-ledger-or-real-balpha-bg-source-acquisition.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2436_SOURCE_REGISTER.csv",
    "qv_live_sector_ledger": OUT / "P8_Y5_PARENT_QLOC_2436_QV_LIVE_SECTOR_LEDGER.csv",
    "zero_or_bound_decision": OUT / "P8_Y5_PARENT_QLOC_2436_ZERO_OR_BOUND_DECISION.csv",
    "balpha_bg_readiness": OUT / "P8_Y5_PARENT_QLOC_2436_BALPHA_BG_ACQUISITION_READINESS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2436_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2436_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2436_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2436_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2436_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_qv_live": QUEUE / "JR2436_QV_LIVE_SECTOR_LEDGER_NONCLAIM.csv",
    "queue_balpha_bg": QUEUE / "JR2436_BALPHA_BG_ACQUISITION_READINESS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "qv_live_sector_and_coefficient_readiness_2436.csv",
    "beta_docs": BETA_DOCS / "QV_BALPHA_BG_READINESS_2436_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2436_00_2435_handoff",
        "source_path": ROOT / "2435-Y5-R2FR-vertical-Noether-charge-Qv-and-typed-target-exclusion-or-balpha-bg-source-row.md",
        "needles": ["NEXT2435_0_selected", "QV2435_5_verdict", "SRCROW2435_3_verdict", "VAL2435_OVERALL"],
        "role": "fresh handoff: Q_v sector ledger or real b_alpha/b_g source acquisition",
    },
    {
        "source_id": "SRC2436_01_2394_sector_split",
        "source_path": ROOT / "2394-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md",
        "needles": ["SVL2394_6_total", "epsilon_Qv_total", "VAL2394_OVERALL"],
        "role": "original Q_v sector-piece split into EH, matter, extra, projector, boundary, coupling",
    },
    {
        "source_id": "SRC2436_02_2395_EH",
        "source_path": ROOT / "2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md",
        "needles": ["EHK2395_6_verdict", "EHC2395_5_EH_conditional_ready", "VAL2395_OVERALL"],
        "role": "EH pure-vertical kernel-zero conditional theorem",
    },
    {
        "source_id": "SRC2436_03_2396_matter",
        "source_path": ROOT / "2396-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md",
        "needles": ["MSL2396_7_verdict", "MSC2396_7_matter_zero_ready", "VAL2396_OVERALL"],
        "role": "matter/source vertical-zero conditional theorem and no-direct-slot bottleneck",
    },
    {
        "source_id": "SRC2436_04_2397_coupling",
        "source_path": ROOT / "2397-Y5-R2FR-no-direct-matter-coupling-grammar-or-coupling-charge-row.md",
        "needles": ["NDMC2397_5_verdict", "delta_w_A", "VAL2397_OVERALL"],
        "role": "direct coupling grammar and live source-prefactor countermodel",
    },
    {
        "source_id": "SRC2436_05_2399_label_forgetting",
        "source_path": ROOT / "2399-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md",
        "needles": ["SLF2399_6_current_verdict", "delta_w_block", "VAL2399_OVERALL"],
        "role": "species-prefactor narrowing to disconnected block/source-shadow residual",
    },
    {
        "source_id": "SRC2436_06_2404_first_variation",
        "source_path": ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
        "needles": ["VAL2404_OVERALL", "exact conditional Einstein/Poisson bridge", "NEXT2404_0_selected"],
        "role": "minimal candidate first variation and exact GR/Newton bridge conditions",
    },
    {
        "source_id": "SRC2436_07_2406_sector_residuals",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["VAL2406_OVERALL", "sector variation/local scaling gates", "NEXT2406_0_selected"],
        "role": "sector residual/local scaling gate consolidation",
    },
    {
        "source_id": "SRC2436_08_2407_projector",
        "source_path": ROOT / "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md",
        "needles": ["VAL2407_OVERALL", "Pi_M commutator", "NEXT2407_0_selected"],
        "role": "projector/source-worldtube commutator obstruction",
    },
    {
        "source_id": "SRC2436_09_2415_gamma",
        "source_path": ROOT / "2415-Y5-R2FR-sector-Gamma-slot-audit-and-private-SRNG-lock.md",
        "needles": ["VAL2415_OVERALL", "sector Gamma-slot audit", "NEXT2415_0_selected"],
        "role": "connection/affine slot audit and public/private residual split",
    },
    {
        "source_id": "SRC2436_10_2419_readout",
        "source_path": ROOT / "2419-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md",
        "needles": ["VAL2419_OVERALL", "source-worldtube/projector chain-map", "NEXT2419_0_selected"],
        "role": "source-worldtube/projector chain-map antecedents",
    },
    {
        "source_id": "SRC2436_11_2430_nohair",
        "source_path": ROOT / "2430-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md",
        "needles": ["NH2430_4_zero_theorem", "NH2430_5_nonzero_source_bound", "VAL2430_OVERALL"],
        "role": "conditional positive q no-hair identity and source/boundary residual fork",
    },
    {
        "source_id": "SRC2436_12_2431_Jq",
        "source_path": ROOT / "2431-Y5-R2FR-Jq-source-leg-zero-theorem-or-component-bound-vector.md",
        "needles": ["JZT2431_5_total_verdict", "JQC2431_9_total_abs", "VAL2431_OVERALL"],
        "role": "J_q descent theorem and live component-bound vector",
    },
    {
        "source_id": "SRC2436_13_2434_typed_basis",
        "source_path": ROOT / "2434-Y5-R2FR-parent-typed-object-language-and-vertical-basis-certificate-or-balpha-bg-bound-row.md",
        "needles": ["TOL2434_7_verdict", "VBC2434_6_verdict", "VAL2434_OVERALL"],
        "role": "typed object-language and vertical-basis certificate gate",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def qv_live_sector_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "sector_id": "QVSL2436_0_EH_observed_geometry",
            "sector": "EH / observed local geometry",
            "latest_evidence": "2395",
            "current_result": "CONDITIONAL_ZERO_THEOREM_AVAILABLE_NOT_SIGNED",
            "best_formula": "If e_obs=Obs_e(q(Phi)) and Dq(v_k)=0 for a pure vertical k, then delta_v e_obs=0, Theta_EH(v_k)=0, and Q_v^EH=0 up to fixed compact boundary class.",
            "missing_parent_inputs": "q/Obs_e ownership; basic coframe proof; pure-vertical/horizontal-diffeomorphism split; compact zero-flux boundary class; positive same-frame M_H_ref",
            "residual_if_unsigned": "epsilon_Qv_EH_kernel_split",
            "next_action": "do not redo EH; sign its prerequisites or keep residual row",
            "rank": 4,
        },
        {
            "sector_id": "QVSL2436_1_matter_source",
            "sector": "ordinary matter / Hilbert source / worldtube",
            "latest_evidence": "2396",
            "current_result": "CONDITIONAL_ZERO_THEOREM_AVAILABLE_NOT_SIGNED",
            "best_formula": "If matter is an observed-frame quotient functor with no independent residual/source/worldtube slot, then geometry, lift, constant, support and boundary variations vanish or are constraints, so Q_v^matter=0.",
            "missing_parent_inputs": "explicit L_m densities; q/e_obs/connection descent; matter lift/no-marker proof; no-direct-slot grammar; support/tail theorem; M_H_ref",
            "residual_if_unsigned": "epsilon_Qv_matter_source; epsilon_hidden_source_slot",
            "next_action": "coupling/no-direct-slot and source-shadow gates must close before matter zero promotes",
            "rank": 2,
        },
        {
            "sector_id": "QVSL2436_2_coupling_source_shadow",
            "sector": "nonminimal coupling / source-prefactor / b_alpha / b_g",
            "latest_evidence": "2397-2399, 2431-2435",
            "current_result": "MAIN_OPEN_WOUND_REFINED_NOT_CLOSED",
            "best_formula": "Common calibration can be harmless, species weights narrow to exchange-block/source-shadow weights, and visible coefficient drift vanishes only if the parent typed target excludes hidden/source/readout coefficient maps.",
            "missing_parent_inputs": "parent object-language inventory; no source-shadow functional; exchange graph connectivity; no-hidden-return theorem; typed target exclusion; vertical basis certificate; actual b_alpha/b_g or delta_w bounds if theorem fails",
            "residual_if_unsigned": "delta_w_block; source_shadow; epsilon_nonminimal_coupling_slot; b_alpha; b_g; J_q component vector",
            "next_action": "attack this first: either prove coupling/source-shadow zero or acquire first real coefficient-bound row",
            "rank": 1,
        },
        {
            "sector_id": "QVSL2436_3_projector_readout",
            "sector": "projector / Pi_M / source-worldtube / readout selector",
            "latest_evidence": "2407, 2418-2419",
            "current_result": "CHAINMAP_ZERO_CONDITIONAL_NOT_SIGNED",
            "best_formula": "Projector/readout is silent only if source-worldtube/projector is a fixed chain map before readout and [d,Pi_W]J_H=0 with no field-dependent reentry.",
            "missing_parent_inputs": "fixed W_source owner; Pi_W chain-map theorem; [d,Pi_W]J_H zero; variation-before-readout separation; source-current equality; no selector GM import",
            "residual_if_unsigned": "epsilon_Qv_projector; E_projector_worldtube; E_source_worldtube; epsilon_selector_GM",
            "next_action": "second-line target after coupling, because it can fake source normalization",
            "rank": 3,
        },
        {
            "sector_id": "QVSL2436_4_boundary_q_charge",
            "sector": "boundary / reference / q-boundary charge",
            "latest_evidence": "2427-2429",
            "current_result": "COMPACT_PROPER_SUBLEMMA_ONLY",
            "best_formula": "A q-boundary contribution is harmless if Q_q/K_boundary is exact/proper/zero under a parent Theta_q/P_q and fixed boundary class; otherwise it is a real edge coefficient.",
            "missing_parent_inputs": "Theta_q; P_q; B_q surface density; fixed finite-jet boundary order; Phi_boundary_local_q=0; no alpha3 edge projection leakage",
            "residual_if_unsigned": "epsilon_Qv_boundary; K_boundary_alpha3_q; Phi_boundary_local_q; Qbar_edge_qH",
            "next_action": "keep as nonclaim unless coupling closes and boundary remains the largest blocker",
            "rank": 5,
        },
        {
            "sector_id": "QVSL2436_5_extra_q_residual",
            "sector": "motion/time/domain/memory/range/q residual sector",
            "latest_evidence": "2420-2430",
            "current_result": "NOHAIR_CONDITIONAL_REQUIRES_SOURCE_AND_BOUNDARY_ZERO",
            "best_formula": "For coercive positive q operator, J_q=0 and Phi_boundary_q=0 imply q=0; nonzero source/boundary gives a finite residual bound, not local GR.",
            "missing_parent_inputs": "Z_q>0; M_q^2>0; source leg J_q=0; boundary Phi_q=0; first-class owner alternative; q residual operator normalization",
            "residual_if_unsigned": "q_R; beta_source; beta_test; alpha3; J_q component vector",
            "next_action": "use after coupling/source legs are settled; no-hair is ready but its premises are not",
            "rank": 6,
        },
        {
            "sector_id": "QVSL2436_6_connection_affine",
            "sector": "connection / affine / P4 / private SRNG",
            "latest_evidence": "2413-2416",
            "current_result": "PUBLIC_LC_ROUTE_CONDITIONAL_PRIVATE_SWITCH_LOCKED",
            "best_formula": "Connection reduces to Levi-Civita only if the parent action variables exclude independent affine Gamma in each public sector; otherwise P4 torsion/nonmetricity/projective/hypermomentum rows remain.",
            "missing_parent_inputs": "sector Arg(S_i) signatures; no independent Gamma slot; coframe-owned connection; public derivation of any private SRNG switch",
            "residual_if_unsigned": "P4_affine_residual; torsion; nonmetricity; projective trace; hypermomentum",
            "next_action": "do not use GR notation as proof; leave as public residual stack until source/coupling gates narrow",
            "rank": 7,
        },
        {
            "sector_id": "QVSL2436_7_total_Qv",
            "sector": "total vertical parent charge",
            "latest_evidence": "2394, 2435",
            "current_result": "TOTAL_QV_NOT_EXTRACTED",
            "best_formula": "Q_v=sum_s Q_v^s only after each sector current has been derived as J_v^s=dQ_v^s+C_v^s+leak_s and every leak is zeroed or bounded.",
            "missing_parent_inputs": "Theta_parent; all-field vertical generator; mu_v; sector Q_v split; zero compact flux certificate; all sector closures above",
            "residual_if_unsigned": "epsilon_kernel_charge; epsilon_theta_piece_missing; epsilon_Qv_piece_missing",
            "next_action": "ledger, then close or source the rank-1 coupling/source-shadow sector",
            "rank": 0,
        },
    ]
    return [base_row(**row, theorem_zero=False, source_backed=False, score_ready=False) for row in rows]


def zero_or_bound_decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "ZBD2436_0_do_not_repeat_EH",
            "question": "Should the next work redo the EH kernel-zero proof?",
            "answer": "NO",
            "reason": "2395 already gives the narrow conditional theorem; repeating it does not close q/Obs_e, boundary or M_H_ref signatures.",
            "next_effect": "EH stays conditional; effort moves to live coupling/source channels.",
        },
        {
            "decision_id": "ZBD2436_1_do_not_score_balpha_bg_yet",
            "question": "Should b_alpha/b_g be numerically scored now?",
            "answer": "NO",
            "reason": "2435 has only source-row skeletons and the live sector ledger still lacks q normalization, coefficient owner, projection matrix, and no-cancellation group.",
            "next_effect": "prepare acquisition readiness, but do not fill numeric coefficient values.",
        },
        {
            "decision_id": "ZBD2436_2_best_derivation_target",
            "question": "Which theorem has the best leverage now?",
            "answer": "COUPLING_SOURCE_SHADOW_ZERO",
            "reason": "It simultaneously feeds matter Q_v, J_q source legs, visible coefficients, source normalization, clocks/WEP/R10/PPN, and the b_alpha/b_g rows.",
            "next_effect": "2437 should attack coupling-sector Q_v/source-shadow zero or stage real coefficient-bound pack.",
        },
        {
            "decision_id": "ZBD2436_3_if_derivation_fails",
            "question": "What if coupling/source-shadow zero does not close?",
            "answer": "BOUND_PACK",
            "reason": "Then the honest route is finite residual accounting: delta_w_block, b_alpha, b_g, source_shadow, and projector/source-worldtube coefficients with sourced units and no-cancellation policy.",
            "next_effect": "no local-GR/R10/PPN/WEP claim until rows are source-backed and pass arena gates.",
        },
        {
            "decision_id": "ZBD2436_4_public_status",
            "question": "Is this GitHub/public-ready as a claim?",
            "answer": "NO",
            "reason": "This is a private spine ledger and route selector; it strengthens the framework but keeps every claim gate false.",
            "next_effect": "continue private goal work.",
        },
    ]
    return [base_row(**row) for row in rows]


def balpha_bg_readiness_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "BBR2436_0_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative of EM/gauge kinetic or fine-structure coefficient along retained q/source-shadow direction",
            "units": "dimensionless_or_per_parent_q_unit",
            "required_before_numeric": "parent coefficient owner; q normalization; vertical basis; projection to clocks/WEP/R10/EM; source path; extraction method; no-cancellation group",
            "current_status": "ACQUISITION_NOT_READY_NO_PARENT_OWNER",
            "source_backed": False,
            "score_ready": False,
        },
        {
            "row_id": "BBR2436_1_b_g",
            "symbol": "b_g",
            "definition": "universal Weyl/shadow-frame slope or coframe response coefficient in the observed metric/clock/readout branch",
            "units": "dimensionless_or_per_parent_q_unit",
            "required_before_numeric": "coframe/connection owner; no-shadow-frame theorem failure mode; projection to PPN/R10/clock/WEP; source path; product-law source/test split",
            "current_status": "ACQUISITION_NOT_READY_NO_FRAME_OWNER",
            "source_backed": False,
            "score_ready": False,
        },
        {
            "row_id": "BBR2436_2_delta_w_block",
            "symbol": "delta_w_block",
            "definition": "relative active-source weight over disconnected ordinary exchange blocks or source-shadow components",
            "units": "dimensionless",
            "required_before_numeric": "ordinary exchange graph; source-shadow owner; material projection basis; WEP/R10/PPN/clock/source-normalization bounds; source path",
            "current_status": "BETTER_FIRST_COUPLING_BOUND_THAN_RAW_BALPHA_BG",
            "source_backed": False,
            "score_ready": False,
        },
        {
            "row_id": "BBR2436_3_source_shadow",
            "symbol": "source_shadow",
            "definition": "non-Hilbert or hidden source functional returning after apparent total-Hilbert source formation",
            "units": "arena_dependent",
            "required_before_numeric": "parent action normal form owner; no-shadow theorem failure; projection operator; arena units; source path",
            "current_status": "PRIMARY_THEOREM_OR_BOUND_TARGET",
            "source_backed": False,
            "score_ready": False,
        },
        {
            "row_id": "BBR2436_4_verdict",
            "symbol": "coefficient_acquisition_verdict",
            "definition": "real numeric acquisition is deferred until the parent coupling/source-shadow owner is either proved impossible or made into an explicit residual basis",
            "units": "n/a",
            "required_before_numeric": "2437 coupling-sector theorem/bound split",
            "current_status": "NONCLAIM_DEFER_NUMERIC_FILL",
            "source_backed": False,
            "score_ready": False,
        },
    ]
    return [base_row(**row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2436_0_total_Qv", "total vertical Q_v extracted and zero", "BLOCKED", "sector pieces are named but not all derived/zeroed/bounded"),
        ("CG2436_1_matter_Qv", "matter/source Q_v zero", "BLOCKED", "coupling/source-shadow/no-direct-slot owner remains unsigned"),
        ("CG2436_2_coefficients", "b_alpha/b_g/delta_w coefficients theorem-zero or source-backed", "BLOCKED", "no parent coefficient owner or numeric source-backed projection row yet"),
        ("CG2436_3_projector", "projector/worldtube/readout chain-map silence", "BLOCKED", "conditional chain-map antecedents remain unsigned"),
        ("CG2436_4_q_nohair", "q=0 local branch from no-hair", "BLOCKED", "J_q=0 and boundary zero remain unproved"),
        ("CG2436_5_local_GR", "local GR/Newton/PPN/WEP/R10 pass", "BLOCKED", "requires all upstream sector and coefficient gates"),
    ]
    return [base_row(claim_id=claim_id, claim=claim, gate_status=status, reason=reason, gate_pass=False) for claim_id, claim, status, reason in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2436_0_current_state", "CURRENT_STATE_IS_NOT_CIRCLE", "The chain has narrowed free coupling from species weights to block/source-shadow/visible-coefficient channels and has conditional zero theorems for EH, matter, q no-hair, and projector silence.", "continue deriving, but stop repeating already-narrow conditionals"),
        ("DEC2436_1_rank1", "COUPLING_SOURCE_SHADOW_IS_RANK1", "It blocks matter Q_v, J_q, observed coefficients, source normalization and local tests simultaneously.", "2437 should attack coupling/source-shadow zero or bound pack"),
        ("DEC2436_2_no_public_claim", "NO_GITHUB_OR_PUBLIC_CLAIM", "Every claim gate is false and rows are nonclaim.", "stay private"),
        ("DEC2436_3_no_numeric_fill", "NO_PLACEHOLDER_COEFFICIENTS", "b_alpha/b_g/delta_w values without owner, units, source path and projection would be fake precision.", "defer numeric acquisition until residual basis is fixed"),
        ("DEC2436_4_next", "SELECT_2437_COUPLING_SECTOR_QV_SHADOW_SLOT", "This is the cleanest route with the least wasted abstraction and the highest chance of unlocking local GR reduction.", "write parent coupling-sector zero theorem or first real coefficient-bound pack"),
    ]
    return [base_row(decision_id=row_id, decision=decision, rationale=rationale, consequence=consequence) for row_id, decision, rationale, consequence in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2436_0_selected",
            selection_status="selected",
            target_file="2437-Y5-R2FR-coupling-sector-Qv-shadow-slot-zero-or-first-real-coefficient-bound-pack.md",
            target_script="scripts/Y5_R2FR_coupling_sector_Qv_shadow_slot_zero_or_first_real_coefficient_bound_pack_2437.py",
            task="prove the coupling/source-shadow sector contributes no vertical Q_v/J_q/visible-coefficient source leg from the parent action grammar; if it cannot close, define the first real residual basis for delta_w_block, source_shadow, b_alpha, and b_g acquisition",
            acceptance_target="either a parent-signed coupling-sector zero theorem, or a source-ready nonclaim coefficient-bound pack with units, projection maps, provenance fields, and no-cancellation guards",
            guardrails="do not invent coefficient values, do not use projection-by-declaration, do not cancel tails, do not claim local GR/R10/PPN/WEP/clock/orbital pass, do not edit formalization-workbench, and do not push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_qv_live", OUTPUTS["qv_live_sector_ledger"], COPY_TARGETS["queue_qv_live"], "live Q_v sector ledger nonclaim queue"),
        ("queue_balpha_bg", OUTPUTS["balpha_bg_readiness"], COPY_TARGETS["queue_balpha_bg"], "b_alpha/b_g/delta_w acquisition readiness nonclaim queue"),
        ("branch_wep", OUTPUTS["zero_or_bound_decision"], COPY_TARGETS["branch_wep"], "ranked Q_v/coupling decision for local WEP branch"),
        ("beta_docs", OUTPUTS["balpha_bg_readiness"], COPY_TARGETS["beta_docs"], "coefficient acquisition readiness for beta docs"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=note,
            )
        )
    return rows


def formalization_hits() -> list[Path]:
    patterns = [
        "*2436-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2436*",
        "*P8_Y5_BRR545_2436*",
        "*JR2436*",
        "*QV_BALPHA_BG_READINESS_2436*",
    ]
    hits: list[Path] = []
    if not FORMALIZATION.exists():
        return hits
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return hits


def validation_rows(generated_outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources = generated_outputs["source_register"]
    rows.append(
        base_row(
            check_id="VAL2436_00_sources_exist",
            status="PASS" if all(row["path_exists"] == True for row in sources) else "FAIL",
            notes="all cited source paths exist" if all(row["path_exists"] == True for row in sources) else "one or more source paths missing",
        )
    )
    rows.append(
        base_row(
            check_id="VAL2436_01_source_needles",
            status="PASS" if all(row["needles_found"] == True for row in sources) else "FAIL",
            notes="all cited source needles are present" if all(row["needles_found"] == True for row in sources) else "one or more source needles missing",
        )
    )

    ledger = generated_outputs["qv_live_sector_ledger"]
    required_sectors = {
        "QVSL2436_0_EH_observed_geometry",
        "QVSL2436_1_matter_source",
        "QVSL2436_2_coupling_source_shadow",
        "QVSL2436_3_projector_readout",
        "QVSL2436_4_boundary_q_charge",
        "QVSL2436_5_extra_q_residual",
        "QVSL2436_6_connection_affine",
        "QVSL2436_7_total_Qv",
    }
    present_sectors = {row["sector_id"] for row in ledger}
    rows.append(
        base_row(
            check_id="VAL2436_02_all_live_sectors_present",
            status="PASS" if required_sectors.issubset(present_sectors) else "FAIL",
            notes="live Q_v sectors include EH, matter, coupling, projector, boundary, q residual, connection, and total",
        )
    )
    rows.append(
        base_row(
            check_id="VAL2436_03_rank1_coupling_selected",
            status="PASS" if any(row["sector_id"] == "QVSL2436_2_coupling_source_shadow" and str(row["rank"]) == "1" for row in ledger) else "FAIL",
            notes="coupling/source-shadow is selected as the highest-leverage open sector",
        )
    )
    rows.append(
        base_row(
            check_id="VAL2436_04_no_theorem_zero_claims",
            status="PASS" if all(row.get("theorem_zero") == False for row in ledger) else "FAIL",
            notes="no Q_v sector is promoted to theorem-zero in 2436",
        )
    )

    readiness = generated_outputs["balpha_bg_readiness"]
    rows.append(
        base_row(
            check_id="VAL2436_05_coefficient_rows_nonclaim",
            status="PASS" if all(row.get("source_backed") == False and row.get("score_ready") == False for row in readiness) else "FAIL",
            notes="b_alpha/b_g/delta_w acquisition rows remain nonclaim and unscored",
        )
    )

    claims = generated_outputs["claim_gates"]
    rows.append(
        base_row(
            check_id="VAL2436_06_claims_blocked",
            status="PASS" if all(row.get("gate_pass") == False and row.get("valid_for_claim") == False for row in claims) else "FAIL",
            notes="all local-GR/R10/PPN/WEP/clock/orbital claim gates remain blocked",
        )
    )

    rows.append(
        base_row(
            check_id="VAL2436_07_next_target_written",
            status="PASS" if generated_outputs["next_target"][0]["target_file"].startswith("2437-") else "FAIL",
            notes="2437 coupling-sector target selected",
        )
    )

    hits = formalization_hits()
    rows.append(
        base_row(
            check_id="VAL2436_08_no_formalization_artifacts",
            status="PASS" if not hits else "FAIL",
            notes="no 2436 artifacts were written to formalization-workbench" if not hits else "formalization-workbench contains 2436 artifacts",
            detail="; ".join(str(hit) for hit in hits),
        )
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        rows.append(
            base_row(
                check_id=f"VAL2436_CSV_{path.stem}",
                status="PASS" if ok and count > 0 else "FAIL",
                notes=f"CSV parses with {count} rows" if ok else "CSV parse failed",
                detail=detail,
            )
        )

    non_validation = [row for row in rows if row["check_id"] != "VAL2436_OVERALL"]
    overall_pass = all(row["status"] == "PASS" for row in non_validation)
    rows.append(
        base_row(
            check_id="VAL2436_OVERALL",
            status="PASS" if overall_pass else "FAIL",
            notes="2436 consolidates the live Q_v sector map, selects coupling/source-shadow as rank-1, keeps b_alpha/b_g acquisition nonclaim, and preserves all claim gates false",
        )
    )
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2436 - Y5/R2FR Qv Sector Piece Ledger Or Real b_alpha/b_g Source Acquisition",
        "",
        "## Result",
        "- 2436 consolidates the actual live `Q_v` state instead of circling the same theorem from another angle.",
        "- EH and matter/source now have useful conditional zero theorems, but neither is parent-signed.",
        "- The rank-1 open wound is the coupling/source-shadow/visible-coefficient sector: `delta_w_block`, `source_shadow`, `b_alpha`, and `b_g`.",
        "- Numeric `b_alpha/b_g` acquisition is deliberately not filled yet because the parent coefficient owner, q normalization, projection map, and no-cancellation group are not fixed.",
        "- The next best attack is 2437: prove the coupling-sector zero theorem from the parent action grammar, or build the first real nonclaim coefficient-bound pack.",
        "",
        "## Practical Status",
        "This is a useful checkpoint.  The local-GR route is not dead, but the bottleneck is no longer vague: the theory must either remove the coupling/source-shadow channels as parent-illegal objects, or carry them as finite residual coefficients into WEP, clocks, R10, PPN, orbital and EM bounds.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], outputs["source_register"]),
        "",
        "## Live Q_v Sector Ledger",
        table(["sector_id", "sector", "latest_evidence", "current_result", "missing_parent_inputs", "residual_if_unsigned", "next_action", "rank", "valid_for_claim"], outputs["qv_live_sector_ledger"]),
        "",
        "## Zero Or Bound Decisions",
        table(["decision_id", "question", "answer", "reason", "next_effect", "valid_for_claim"], outputs["zero_or_bound_decision"]),
        "",
        "## b_alpha / b_g Acquisition Readiness",
        table(["row_id", "symbol", "definition", "required_before_numeric", "current_status", "source_backed", "score_ready", "valid_for_claim"], outputs["balpha_bg_readiness"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], outputs["claim_gates"]),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "qv_live_sector_ledger": qv_live_sector_ledger_rows(),
        "zero_or_bound_decision": zero_or_bound_decision_rows(),
        "balpha_bg_readiness": balpha_bg_readiness_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in outputs.items():
        write_csv(OUTPUTS[key], rows)

    outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], outputs["branch_copies"])

    outputs["validation"] = validation_rows(outputs)
    write_csv(OUTPUTS["validation"], outputs["validation"])
    write_doc(outputs)

    print(DOC)
    print(OUTPUTS["validation"])
    overall = next(row for row in outputs["validation"] if row["check_id"] == "VAL2436_OVERALL")
    print(f"VAL2436_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
