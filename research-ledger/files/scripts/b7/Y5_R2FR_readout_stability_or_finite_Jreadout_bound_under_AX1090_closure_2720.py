from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2720-Y5-R2FR-readout-stability-or-finite-Jreadout-bound-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2720_SOURCE_REGISTER.csv",
    "readout_audit": RESIDUALS / "P8_Y5_R2FR_2720_READOUT_STABILITY_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_2720_READOUT_THEOREM_ATTEMPT.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2720_FINITE_JREADOUT_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2720_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2720_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2720_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2720_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2720_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2720_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2720_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2720_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "readout_Jreadout_rows_2720_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "Ereadout_EJeff_update_2720_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2720_SOURCE_NORMALIZATION_NO_FITTED_GM_OR_EJEFF_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def md_escape(value: Any) -> str:
    return normalize(value).replace("|", "\\|").replace("\n", "<br>")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: normalize(row.get(key, "")) for key in fieldnames})


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


SOURCE_SPECS = [
    {
        "source_id": "SRC2720_0_2719",
        "label": "2719 readout handoff",
        "path": ROOT / "2719-Y5-R2FR-boundary-harmonic-nocharge-or-finite-Jeff-bound-under-AX1090-closure.md",
        "needles": [
            "BLK2719_3_readout_next",
            "NEXT2719_0_selected",
            "VAL2719_OVERALL",
        ],
        "use": "hands off the remaining readout-regeneration source after boundary/harmonic rows are explicit",
    },
    {
        "source_id": "SRC2720_1_2718",
        "label": "2718 J_readout source split",
        "path": ROOT / "2718-Y5-R2FR-Jeff-source-norm-split-or-ZR-theorem-zero-under-AX1090-closure.md",
        "needles": [
            "JEFF2718_4_readout",
            "BND2718_2_remaining_local_vacuum",
            "VAL2718_OVERALL",
        ],
        "use": "defines J_readout as post-reduction/readout regeneration feeding E_Jeff",
    },
    {
        "source_id": "SRC2720_2_2717",
        "label": "2717 arena projection blockers",
        "path": ROOT / "2717-Y5-R2FR-finite-RAB-green-kernel-normalization-or-parent-coefficient-zero-under-AX1090-closure.md",
        "needles": [
            "ARENA2717_1_PPN",
            "ARENA2717_2_clock",
            "ARENA2717_3_orbital",
            "NF2717_4_TAU",
            "VAL2717_OVERALL",
        ],
        "use": "connects R_AB profile to PPN, clock and orbital observables only through missing arena kernels",
    },
    {
        "source_id": "SRC2720_3_1567",
        "label": "1567 readout/tau contract",
        "path": ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "needles": [
            "CON1567_4_readout_closure",
            "AUD1567_2_readout",
            "ACQ1567_6_tau_PPN",
            "ACQ1567_7_tau_clock",
            "ACQ1567_8_tau_orbital",
            "VAL1567_OVERALL",
        ],
        "use": "records the unsigned readout-closure clause and missing tau projection rows",
    },
    {
        "source_id": "SRC2720_4_1873",
        "label": "1873 hidden/readout tail warning",
        "path": ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md",
        "needles": [
            "BSC1873_6_hidden_tail_silence",
            "UNS1873_3_boundary",
            "RCD1873_0_current_status",
            "VAL1873_OVERALL",
        ],
        "use": "prevents readout/EFT tails being silently hidden behind boundary or local projection language",
    },
    {
        "source_id": "SRC2720_5_2478",
        "label": "2478 observable projection coefficient",
        "path": ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
        "needles": [
            "C_obs",
            "BLK2478_4_Cobs_Karena",
            "VAL2478_OVERALL",
        ],
        "use": "keeps observable projection C_obs/K_arena symbolic until sourced",
    },
    {
        "source_id": "SRC2720_6_2208",
        "label": "2208 source normalization and no-absorption",
        "path": ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md",
        "needles": [
            "PPNL2208_0_operator_factorization",
            "PPNL2208_3_source_normalization",
            "measured-GM no-absorption rule",
            "VAL2208_OVERALL",
        ],
        "use": "shows PPN residuals require a fixed source normalization, not a hidden fitted-GM absorption",
    },
    {
        "source_id": "SRC2720_7_10_observer",
        "label": "10 observer-map symplectic contract",
        "path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": [
            "gamma - 1 = 0 after R_AB=0.",
            "all matter sectors couple to the same observer coframe.",
            "derive R_AB=0 from the parent theory",
        ],
        "use": "ties local GR/PPN readout to observer coframe and derived R_AB silence",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": path.exists(),
                "required_needles_found": not missing,
                "missing_needles": ";".join(missing),
                "use": spec["use"],
                "claim_credit": False,
                "timestamp_utc": ts(),
            }
        )
    return rows


def readout_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "READ2720_0_parent_image_stability",
            "target": "readout/effective reduction preserves Image(ParentGenerate)",
            "attempt": "demand Pi_obs o ParentGenerate = ParentGenerate_obs o Pi_parent, with no representative-dependent R_AB source",
            "verdict": "UNSIGNED_READOUT_STABILITY",
            "reason": "1567 records the exact clause but not the parent proof; 1873 keeps hidden/readout tails unsigned",
            "claim_allowed": False,
            "next_requirement": "parent readout functor or finite J_readout projection row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "READ2720_1_tree_level_silence",
            "target": "no readout regeneration from a tree-level clean action",
            "attempt": "argue that absence of explicit R_AB terms before reduction survives observation",
            "verdict": "REJECTED_AS_TOO_WEAK",
            "reason": "effective reduction, gauge fixing, normalization and observable projection can generate source terms unless the map is signed",
            "claim_allowed": False,
            "next_requirement": "closure under projection, renormalization and gauge/readout conversion",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "READ2720_2_tau_frame",
            "target": "tau_PPN, tau_clock and tau_orbital do not become new sources",
            "attempt": "treat tau rows as passive readout coefficients",
            "verdict": "MISSING_ARENA_PROJECTION_KERNELS",
            "reason": "2717 and 1567 both require explicit tau/readout kernels before PPN, clock or orbital scoring",
            "claim_allowed": False,
            "next_requirement": "source-backed tau_R10/tau_PPN/tau_clock/tau_orbital rows",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "READ2720_3_ppn_gauge",
            "target": "PPN readout does not hide R_AB residuals in coordinates or fitted constants",
            "attempt": "project weak-field metric residual directly into gamma and beta",
            "verdict": "SOURCE_NORMALIZATION_BLOCKER",
            "reason": "2208 requires inverse-divergence stress, gauge/domain choice, source normalization and measured-GM no-absorption",
            "claim_allowed": False,
            "next_requirement": "fixed G_ref/source charge and no-fitted-GM rule",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "READ2720_4_clock_species",
            "target": "clock/redshift readout is universal",
            "attempt": "use one observer coframe for all matter sectors",
            "verdict": "COFRAME_DESCENT_NOT_SIGNED",
            "reason": "the observer-map contract requires universal matter coupling, but this is not yet derived from the parent quotient action",
            "claim_allowed": False,
            "next_requirement": "matter/coframe descent theorem or finite species-dependent clock row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "READ2720_5_verdict",
            "target": "J_readout=0",
            "attempt": "combine image stability, tau silence, PPN gauge readout, clock universality and no-absorption",
            "verdict": "READOUT_ZERO_NOT_DERIVED_FINITE_ROWS_REQUIRED",
            "reason": "every honest zero route has at least one unsigned parent/readout/arena clause",
            "claim_allowed": False,
            "next_requirement": "finite J_readout rows feed E_Jeff and source-normalization becomes next target",
            "timestamp_utc": ts(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2720_0_statement",
            "statement": "If the readout map Pi_obs is a quotient functor that preserves Image(ParentGenerate), commutes with weak-field linearization, has no representative-dependent counterterms, fixes a universal observer coframe, and uses arena kernels as projections rather than sources, then J_readout=0.",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_clause": "parent readout functor; radiative/effective closure; tau kernels; PPN gauge/source normalization; clock species descent",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2720_1_image_preservation",
            "statement": "For every parent-generated local variation delta Phi, (I-P_parent) D Pi_obs[delta Phi] must vanish in the R_AB source channel.",
            "status": "EXACT_IF_PARENT_FUNCTOR_SIGNED",
            "missing_clause": "no proof that Pi_obs preserves the parent-generated image after reduction",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2720_2_effective_closure",
            "statement": "Radiative, coarse-grained and gauge-fixed effective actions must not generate representative Weyl/disformal/R_AB derivative coefficients.",
            "status": "UNSIGNED_EFFECTIVE_CLOSURE",
            "missing_clause": "counterterm basis and symmetry proof excluding R_AB readout operators",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2720_3_arena_projection",
            "statement": "tau_R10, tau_PPN, tau_clock and tau_orbital must be bounded projections of an already bounded R_AB profile, not independent fitted response terms.",
            "status": "MISSING_KERNELS",
            "missing_clause": "arena-specific projection kernels and units",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2720_4_no_absorption",
            "statement": "The observed Newtonian source normalization must be fixed before residuals are scored, so J_readout cannot be hidden by refitting GM, G_ref or source charge.",
            "status": "SOURCE_NORMALIZATION_REQUIRED",
            "missing_clause": "no-fitted-GM/source-normalization contract",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FJR2720_0_E_readout_projection",
            "quantity": "E_readout_projection",
            "definition": "E_readout_projection := C_proj * ||(I-P_parent) D Pi_obs[delta Phi]||_RAB_source",
            "feeds": "J_readout and E_Jeff",
            "source_path": str(ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"),
            "units_need": "R_AB Euler-source norm or equivalent weak-field source-density units",
            "missing": "parent image-preservation theorem; projection norm; representative-source basis",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FJR2720_1_E_tau_frame",
            "quantity": "E_tau_frame",
            "definition": "E_tau_frame := C_tau * max(|tau_R10|,|tau_PPN|,|tau_clock|,|tau_orbital|) * ||R_AB||_profile",
            "feeds": "arena readout part of J_readout",
            "source_path": str(ROOT / "2717-Y5-R2FR-finite-RAB-green-kernel-normalization-or-parent-coefficient-zero-under-AX1090-closure.md"),
            "units_need": "arena residual per dimensionless R_AB amplitude or gradient",
            "missing": "tau_R10/tau_PPN/tau_clock/tau_orbital kernels and unit conventions",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FJR2720_2_E_PPN_gauge",
            "quantity": "E_PPN_gauge",
            "definition": "E_PPN_gauge := C_PPN_gauge * ||Pi_PPN[h_res]||_(gamma,beta,light,delay)",
            "feeds": "PPN/local-GR residual vector",
            "source_path": str(ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md"),
            "units_need": "dimensionless PPN residuals after fixed gauge and source normalization",
            "missing": "I_div^{-1} boundary/gauge rule; T_GK profile; no-fitted-GM source rule",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FJR2720_3_E_metric_response",
            "quantity": "E_metric_response",
            "definition": "E_metric_response := C_obs * C_Green * C_res * E_GK_bound",
            "feeds": "observed metric residual before arena scoring",
            "source_path": str(ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md"),
            "units_need": "metric perturbation or normalized observable residual",
            "missing": "numeric/source-backed C_obs, C_Green, C_res and E_GK_bound",
            "status": "SYMBOLIC_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FJR2720_4_E_arena_kernel",
            "quantity": "E_arena_kernel",
            "definition": "E_arena_kernel := max(K_R10,K_PPN,K_clock,K_orbital) * ||R_AB||_Green_profile",
            "feeds": "R10/PPN/clock/orbital comparison rows",
            "source_path": str(ROOT / "2717-Y5-R2FR-finite-RAB-green-kernel-normalization-or-parent-coefficient-zero-under-AX1090-closure.md"),
            "units_need": "arena-specific residual units and domain/range convention",
            "missing": "K_arena values; lambda/range convention; experimental normalization",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FJR2720_5_E_no_absorption_guard",
            "quantity": "E_no_absorption_guard",
            "definition": "E_no_absorption_guard := C_absorb * ||Delta(GM)_fit or Delta(source_charge)|| under fixed reference convention",
            "feeds": "source-normalization and local-GR claim gate",
            "source_path": str(ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md"),
            "units_need": "dimensionless fractional source-normalization residual or equivalent PPN source units",
            "missing": "fixed G_ref, M_H/ref or source charge; measured-GM no-absorption rule",
            "status": "REQUIRED_GUARD_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2720_0_previous",
            "formula": "E_nonmatter = E_boundary + E_harmonic + E_readout + E_shadow + E_norm",
            "status": "INHERITED_FROM_2718",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2720_1_readout_split",
            "formula": "E_readout := E_readout_projection + E_tau_frame + E_PPN_gauge + E_metric_response + E_arena_kernel + E_no_absorption_guard",
            "status": "REFINED_NONCLAIM_VECTOR",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2720_2_green_feed",
            "formula": "||R_AB|| <= ||G_R||*(E_matter + E_boundary_hair + E_readout + E_shadow + E_norm)",
            "status": "FORMAL_GREEN_INTERFACE_ONLY",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2720_3_zero_condition",
            "formula": "E_readout=0 only if parent readout image-stability, effective closure, tau kernels, universal coframe and source-normalization all close",
            "status": "ZERO_CONDITION_NOT_MET",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2720_0_readout_zero",
            "claim": "J_readout=0",
            "status": "BLOCKED",
            "required_before_claim": "parent readout functor plus effective/counterterm closure",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2720_1_PPN",
            "claim": "PPN/local-GR residual is safe",
            "status": "BLOCKED",
            "required_before_claim": "C_obs/K_arena, PPN gauge map and no-fitted-GM source normalization",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2720_2_clock",
            "claim": "clock/redshift readout is universal and bounded",
            "status": "BLOCKED",
            "required_before_claim": "coframe/matter descent or finite species-dependent clock row",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2720_3_orbital",
            "claim": "orbital/precession residual is bounded",
            "status": "BLOCKED",
            "required_before_claim": "orbital projection kernel, gradient profile and no fitted-GM absorption",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2720_4_local_GR",
            "claim": "local GR/Newton limit",
            "status": "BLOCKED",
            "required_before_claim": "all E_Jeff pieces zero or absolutely bounded with readout/source normalization fixed",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2720_5_public",
            "claim": "public/GitHub output",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim audit",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2720_0_readout_functor",
            "missing_item": "parent readout functor/image-stability theorem",
            "effect": "post-reduction map can regenerate R_AB source or derivative terms",
            "best_next_attack": "derive quotient readout naturality or keep finite E_readout_projection row",
            "claim_blocked": "J_readout=0; local GR",
        },
        {
            "blocker_id": "BLK2720_1_tau_kernels",
            "missing_item": "tau_R10/tau_PPN/tau_clock/tau_orbital kernels",
            "effect": "R_AB amplitude cannot be converted into arena residuals cleanly",
            "best_next_attack": "source arena projection kernels or prove they are projections only",
            "claim_blocked": "R10; PPN; clocks; orbital",
        },
        {
            "blocker_id": "BLK2720_2_Cobs_Karena",
            "missing_item": "observable projection coefficient C_obs and K_arena",
            "effect": "metric residual can be symbolic but not scored",
            "best_next_attack": "factor observed metric response and arena kernels from existing Green certificate",
            "claim_blocked": "empirical local tests",
        },
        {
            "blocker_id": "BLK2720_3_no_absorption",
            "missing_item": "fixed source normalization and no-fitted-GM rule",
            "effect": "residuals can be hidden in refit constants instead of being tested",
            "best_next_attack": "write source-normalization contract and finite E_norm/E_absorb vector",
            "claim_blocked": "PPN/local-GR comparison",
        },
        {
            "blocker_id": "BLK2720_4_hidden_tails",
            "missing_item": "effective/counterterm/radiative readout-tail exclusion",
            "effect": "tree-level silence is not stable under projection",
            "best_next_attack": "counterterm basis audit under quotient symmetry",
            "claim_blocked": "readout theorem-zero",
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2720_0_no_zero_claim",
            "decision": "do not claim J_readout=0",
            "rationale": "readout stability exists as a clean theorem shape but the parent/readout/effective clauses are unsigned",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2720_1_reject_tree_silence",
            "decision": "reject tree-level readout silence as a proof",
            "rationale": "projection, gauge fixing and source normalization can generate residual response terms",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2720_2_finite_rows",
            "decision": "install finite J_readout rows into E_Jeff",
            "rationale": "if zero is not derived, every readout leak must be source-ready and nonclaim",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2720_3_next",
            "decision": "move next to source normalization and no-fitted-GM",
            "rationale": "PPN/readout cannot be judged until source normalization is fixed, especially against GR/Newton comparisons",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2720_0_selected",
            "status": "selected_primary",
            "target_doc": "2721-Y5-R2FR-source-normalization-no-fitted-GM-or-finite-EJeff-vector-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_source_normalization_no_fitted_GM_or_finite_EJeff_vector_under_AX1090_closure_2721.py",
            "mission": "fix the reference source normalization so local residuals cannot be hidden by refitting GM/G_ref/source charge, or create finite E_norm/E_absorb rows feeding E_Jeff",
            "acceptance": "either source normalization is parent-signed, or no-absorption rows become explicit nonclaim inputs for PPN/R10/local tests",
            "forbidden": "score PPN/local GR; absorb residuals into fitted GM; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2720_0_status",
            "sector": "local-GR bridge",
            "state": "finite Green branch, boundary/harmonic rows, and now readout rows exist, but no theorem-zero/local-GR claim is open",
            "confidence": "structural progress, not evidence claim",
            "next_need": "source normalization and no-fitted-GM contract",
        },
        {
            "snapshot_id": "SNAP2720_1_best_route",
            "sector": "derivation",
            "state": "the winning route is still derivation-first: kill source channels by parent contracts, otherwise bound every leak absolutely",
            "confidence": "high as methodology",
            "next_need": "parent readout functor or sourced finite kernels",
        },
        {
            "snapshot_id": "SNAP2720_2_empirical",
            "sector": "testing readiness",
            "state": "not score-ready; R10/PPN/clock/orbital rows need numeric kernels and fixed source normalization",
            "confidence": "honest blocker map",
            "next_need": "no-absorption rule and arena projection constants",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2720_0_local_bounds",
            "source_table": OUTPUTS["finite_rows"].name,
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "quarantine readout local-bound rows as nonclaim",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2720_1_source_weight",
            "source_table": OUTPUTS["ejeff_update"].name,
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "quarantine E_readout/E_Jeff update vector as nonclaim",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2720_2_next_queue",
            "source_table": OUTPUTS["next_target"].name,
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2721 without touching formalization-workbench",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"
    return True, len(rows), "parsed"


def recent_formalization_changes() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            except OSError:
                continue
            if modified >= SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_readout_projection",
        "E_tau_frame",
        "E_PPN_gauge",
        "E_metric_response",
        "E_arena_kernel",
        "E_no_absorption_guard",
    }
    csv_paths = [
        path for key, path in OUTPUTS.items() if key != "validation"
    ] + list(BRANCH_OUTPUTS.values())
    parse_results = [(*parse_csv(path), path) for path in csv_paths]
    parse_detail = "; ".join(
        f"{path.name}:{row_count}:{detail}" if passed else f"{path.name}:{detail}"
        for passed, row_count, detail, path in parse_results
    )
    branch_paths_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_recent_changed_count = recent_formalization_changes()
    source_ok = all(
        row["exists"] is True and row["required_needles_found"] is True
        for row in source_rows
    )
    theorem_nonclaim = all(row["claim_allowed"] is False for row in theorem_rows)
    finite_nonclaim = (
        {row["quantity"] for row in finite} == required_quantities
        and all(row["valid_for_claim"] is False for row in finite)
    )
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {
            "validation_id": "VAL2720_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_2_csv_parse",
            "passed": all(result[0] for result in parse_results),
            "detail": parse_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_3_theorem_nonclaim",
            "passed": theorem_nonclaim,
            "detail": "readout theorem remains conditional and no J_readout zero is promoted",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_4_finite_rows_complete_nonclaim",
            "passed": finite_nonclaim,
            "detail": "finite readout rows include projection,tau,PPN,metric,arena,no-absorption components and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_5_ejeff_update_nonclaim",
            "passed": ejeff_nonclaim,
            "detail": "E_readout/E_Jeff update vector remains formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_6_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no local-GR/R10/PPN/clock/orbital/public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_7_branch_copies",
            "passed": branch_paths_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_8_no_formalization_recent_changes",
            "passed": formalization_recent_changed_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2720_9_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2720_OVERALL",
            "passed": overall,
            "detail": "2720 keeps readout zero conditional, rejects tree-level silence, installs finite J_readout rows, and selects source normalization/no-fitted-GM next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2720 - Y5/R2FR Readout Stability Or Finite J_readout Bound Under AX1090 Closure

## Private Verdict

2720 goes after the readout leak directly. It does **not** prove `J_readout=0`. The exact theorem shape is now clear: the readout/effective map must preserve the parent-generated image, commute with weak-field linearization, forbid representative-dependent counterterms, keep arena kernels as projections, and fix the source normalization so residuals cannot be hidden in `GM`, `G_ref`, or source charge.

That theorem is still unsigned. Tree-level silence is explicitly rejected as too weak because projection, gauge fixing, coarse graining and observable normalization can regenerate an `R_AB` source after the parent action looked clean.

The useful progress is bookkeeping with teeth: `E_readout_projection`, `E_tau_frame`, `E_PPN_gauge`, `E_metric_response`, `E_arena_kernel`, and `E_no_absorption_guard` are now explicit nonclaim rows feeding `E_Jeff`.

## Claim Ceiling

- No `J_readout=0`, local-GR/Newton, R10, PPN, clock, orbital, WEP, or public/GitHub claim is opened.
- No tree-level/readout-silence shortcut is allowed.
- Readout rows are source-ready schemas only and remain `valid_for_claim=false`.
- No `formalization-workbench` edits are allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## Readout Stability Audit

{markdown_table(rows["readout_audit"], ["audit_id", "target", "attempt", "verdict", "reason", "claim_allowed", "next_requirement"])}

## Conditional Theorem Attempt

{markdown_table(rows["theorem_attempt"], ["theorem_id", "statement", "status", "missing_clause", "claim_allowed"])}

## Finite J_readout Rows

{markdown_table(rows["finite_rows"], ["row_id", "quantity", "definition", "feeds", "source_path", "units_need", "missing", "status", "valid_for_claim"])}

## E_Jeff Update

{markdown_table(rows["ejeff_update"], ["update_id", "formula", "status", "claim_allowed"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"])}

## Current Blocker Stack

{markdown_table(rows["blocker_stack"], ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"])}

## Decision Ledger

{markdown_table(rows["decision_ledger"], ["decision_id", "decision", "rationale", "allowed", "claim_credit"])}

## Next Target

{markdown_table(rows["next_target"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"])}

## Project Status Snapshot

{markdown_table(rows["project_snapshot"], ["snapshot_id", "sector", "state", "confidence", "next_need"])}

## Branch Copies

{markdown_table(rows["branch_copies"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This one is not a knockout, but it is a clean round. The readout leak is no longer a foggy “maybe”; it is a named vector. If the theory is going to reduce to GR/Newton locally, the next hard thing is source normalization: we must stop residuals from being hidden in fitted `GM` or reference constants. That is the least hand-wavy route from here.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    readout_rows = readout_audit_rows()
    theorem_rows = theorem_attempt_rows()
    finite = finite_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "readout_audit": readout_rows,
        "theorem_attempt": theorem_rows,
        "finite_rows": finite,
        "ejeff_update": ejeff,
        "claim_gates": gates,
        "blocker_stack": blockers,
        "decision_ledger": decisions,
        "next_target": next_rows,
        "project_snapshot": snapshot,
    }

    for key, rows in data.items():
        write_csv(OUTPUTS[key], rows)

    write_csv(BRANCH_OUTPUTS["local_bounds"], finite)
    write_csv(BRANCH_OUTPUTS["source_weight"], ejeff)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    copies = branch_copy_rows()
    data["branch_copies"] = copies
    write_csv(OUTPUTS["branch_copies"], copies)

    data["validation"] = [
        {
            "validation_id": "VAL2720_PRE_DOC",
            "passed": False,
            "detail": "pre-document placeholder",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(data)

    validation = validation_rows(source_rows, theorem_rows, finite, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2720 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
