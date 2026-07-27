from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NON_EGK_RESIDUAL_ZERO_CERTIFICATES_2567"
CHECKPOINT_ID = "2567"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2567-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-local-norm.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NON_EGK_ZERO_2567_SOURCE_REGISTER.csv",
    "zero_certificate": OUT / "P8_Y5_NON_EGK_ZERO_2567_ZERO_CERTIFICATE_ATTEMPT.csv",
    "extended_norm": OUT / "P8_Y5_NON_EGK_ZERO_2567_EXTENDED_LOCAL_NORM_VECTOR.csv",
    "slot_decision": OUT / "P8_Y5_NON_EGK_ZERO_2567_SLOT_DECISION_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_NON_EGK_ZERO_2567_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NON_EGK_ZERO_2567_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NON_EGK_ZERO_2567_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NON_EGK_ZERO_2567_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2567_VALIDATION.csv",
}

COPY_TARGETS = {
    "zero_certificate": LOCAL_BOUNDS / "Non_EGK_zero_certificate_attempt_2567_NONCLAIM.csv",
    "extended_norm": LOCAL_BOUNDS / "Extended_local_residual_norm_vector_2567_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2567_HILBERT_WORLDTUBE_SOURCE_NORMALIZATION_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2567_00_2566_doc",
        "source_path": ROOT / "2566-Y5-R2FR-R10-kernel-Cmetric-EGK-derivation-or-blocker.md",
        "needles": ["NEXT2566_0_selected", "EGK2566_1_HD", "VAL2566_OVERALL"],
        "role": "handoff selecting non-EGK residual zero certificates or extended local norm",
    },
    {
        "source_id": "SRC2567_01_2566_bridge_csv",
        "source_path": LOCAL_BOUNDS / "R10_Cmetric_EGK_bridge_verdict_2566_NONCLAIM.csv",
        "needles": ["DER2566_3_EGK_current_basis", "INSUFFICIENT_FOR_FULL_SRES", "DER2566_4_bridge_shape"],
        "role": "current R10/local bridge and proof that E_GK_bound alone is too narrow",
    },
    {
        "source_id": "SRC2567_02_2566_factor_csv",
        "source_path": LOCAL_BOUNDS / "Cmetric_factor_chain_2566_NONCLAIM.csv",
        "needles": ["FAC2566_1_Cres", "FAC2566_6_Elocal", "EXTENDED_NORM_OR_ZERO_CERTIFICATE_REQUIRED"],
        "role": "C_metric factor chain and E_local_res blocker",
    },
    {
        "source_id": "SRC2567_03_2479_residual_map",
        "source_path": LOCAL_BOUNDS / "Residual_sector_to_EGK_norm_map_2479_NONCLAIM.csv",
        "needles": ["COEF2479_C_HD", "COEF2479_C_norm", "MISSING_ELLJ_WORLDTUBE_SURFACE_INDEPENDENCE_NO_FITTED_GM"],
        "role": "residual-sector coefficient map naming the non-EGK slots",
    },
    {
        "source_id": "SRC2567_04_2405_shortcuts",
        "source_path": ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
        "needles": ["constraint equation like `C=0`", "DeltaE_MTS", "OPB2405_1_c_HD"],
        "role": "rejection of constraint zero shortcuts and higher-derivative/operator residual inventory",
    },
    {
        "source_id": "SRC2567_05_2406_sector_audit",
        "source_path": ROOT / "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["SVC2406_0_higher_derivative", "SVC2406_1_constraint_auxiliary", "SVC2406_5_q_source_vector"],
        "role": "sector-by-sector zero/silence obstruction ledger",
    },
    {
        "source_id": "SRC2567_06_2466_source_norm",
        "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": ["J_M^nu = ell_J", "WT2466_2_surface_independence", "Do not define M_source by observed GM"],
        "role": "Hilbert current, worldtube bridge and no-fitted-GM source normalization guardrail",
    },
    {
        "source_id": "SRC2567_07_2480_precedent",
        "source_path": ROOT / "2480-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-norm-vector.md",
        "needles": ["ZERO2480_e_norm", "E_local_res = E_GK_bound", "VAL2480_OVERALL"],
        "role": "earlier zero-certificate precedent now aligned with 2566 bridge language",
    },
    {
        "source_id": "SRC2567_08_2566_validation",
        "source_path": OUT / "P8_Y5_BRR545_2566_VALIDATION.csv",
        "needles": ["VAL2566_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def zero_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "slot_id": "ZERO2567_e_HD",
            "slot": "e_HD_curvature_operator",
            "zero_route": "parent action normal form excludes local higher-derivative curvature operators, or retained higher-curvature terms are topological/silent in the local branch",
            "attempt_result": "NOT_ZEROED_CURRENT_CORPUS",
            "reason": "2406 records the higher-derivative template as known, but parent adoption/exclusion and coefficient bounds are still unsigned.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_HD",
            "claim_impact": "higher-derivative leakage remains in E_local_res until a parent grammar or bound closes it",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2567_e_aux",
            "slot": "e_aux_constraint_stress",
            "zero_route": "first-class zero-boundary generator, or algebraic second-class elimination with provably zero metric stress",
            "attempt_result": "ZERO_SHORTCUT_REJECTED",
            "reason": "The existing corpus explicitly rejects the shortcut C=0 -> zero stress; multiplier and auxiliary-elimination tails can survive metric variation.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_aux",
            "claim_impact": "constraint/auxiliary stress must remain visible rather than hidden inside the GK norm",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2567_e_tau",
            "slot": "e_tau_clock_frame_leak",
            "zero_route": "terminal public coframe, current-chain vertical silence and tau_source=tau_charge=tau_clock=tau_readout compatibility make frame residual vanish",
            "attempt_result": "CONDITIONAL_NOT_SIGNED",
            "reason": "The tau/current-chain identity is useful, but it is not yet a parent theorem with clock conservation and exchange terms closed.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_tau",
            "claim_impact": "preferred-frame/clock residuals remain a PPN and clock-test blocker",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2567_e_qspur",
            "slot": "e_q_weyl_spurion",
            "zero_route": "q is first-class/removed, has no Weyl/Ricci spurion, and exterior q/body charges vanish",
            "attempt_result": "NOT_ZEROED_WEYL_TAIL_DANGER",
            "reason": "The q first-class/no-spurion route is not parent-signed, and 2406 keeps Weyl/Ricci/source-vector tails as live residuals.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_qspur",
            "claim_impact": "q/Weyl spurion effects remain outside E_GK_bound unless independently zeroed or bounded",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2567_e_shadow",
            "slot": "e_species_shadow_or_zero",
            "zero_route": "universal Hilbert coupling makes non-Hilbert/source-shadow and species-dependent current exactly vanish",
            "attempt_result": "PROMISING_BUT_UNSIGNED",
            "reason": "The Hilbert branch is the right WEP-shaped direction, but matter descent has not yet proved every shadow/source species channel is zero.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_shadow",
            "claim_impact": "WEP/local-source universality remains plausible but not claimable",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2567_e_norm",
            "slot": "e_source_norm_gap",
            "zero_route": "ell_J, kappa0/G_ref and Hilbert worldtube charge define the same source before orbital fitting",
            "attempt_result": "CORE_BLOCKER",
            "reason": "The parent scale ell_J, worldtube surface independence and no-fitted-GM source equivalence remain open.",
            "retain_or_zero": "RETAIN",
            "extended_norm_slot": "E_norm",
            "claim_impact": "Newton reduction cannot be claimed until source normalization is derived rather than fitted",
            "valid_for_claim": False,
        },
        {
            "slot_id": "ZERO2567_e_background",
            "slot": "e_background_subtraction",
            "zero_route": "declare a local reference/background solution satisfying the Lambda/background field equation, then solve perturbations around it",
            "attempt_result": "CONDITIONAL_ZERO_IF_REFERENCE_DECLARED",
            "reason": "This route is mathematically clean, but the local reference/background subtraction convention still needs its own certificate.",
            "retain_or_zero": "CONDITIONAL_ZERO_OR_RETAIN",
            "extended_norm_slot": "E_bg",
            "claim_impact": "background leakage can probably be made harmless, but it is not counted as closed here",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def extended_norm_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "norm_id": "ENORM2567_0_current_EGK",
            "norm_symbol": "E_GK_bound",
            "definition": "C_B*boundary_flux + C_S*source_tail + C_X*negative_mode_defect + C_H*topology_hair_amplitude + C_P*projector_leak",
            "role": "existing GK stress-bound basis from the local arena projection branch",
            "status": "RETAIN_BASE_NONCLAIM",
            "needed_for_claim": "source-backed coefficients and proof that no non-EGK residuals survive",
            "valid_for_claim": False,
        },
        {
            "norm_id": "ENORM2567_1_extended",
            "norm_symbol": "E_local_res",
            "definition": "E_GK_bound + E_HD + E_aux + E_tau + E_qspur + E_shadow + E_norm + E_bg",
            "role": "minimal honest local residual norm after failed zero-certificate sweep",
            "status": "PROPOSED_EXTENDED_NORM_NONCLAIM",
            "needed_for_claim": "each added slot must be zeroed or supplied with units, coefficients and local arena bounds",
            "valid_for_claim": False,
        },
        {
            "norm_id": "ENORM2567_2_Cres_ext",
            "norm_symbol": "C_res_ext",
            "definition": "||S_res||_dual <= C_res_ext*E_local_res",
            "role": "replacement for the invalid full-source claim ||S_res|| <= C_res*E_GK_bound",
            "status": "FORMAL_ONLY_UNTIL_SLOT_COEFFICIENTS_SOURCED",
            "needed_for_claim": "operator norms for every retained slot in the same weak-field/local frame",
            "valid_for_claim": False,
        },
        {
            "norm_id": "ENORM2567_3_Cmetric_ext",
            "norm_symbol": "C_metric_ext",
            "definition": "C_metric_ext=(2/c^2)*C_obs*C_Green*C_res_ext",
            "role": "future local-test bridge once E_local_res and C_res_ext are sourced",
            "status": "DOWNSTREAM_NONCLAIM",
            "needed_for_claim": "C_obs, C_Green, C_res_ext and arena kernels must be numeric/source-backed",
            "valid_for_claim": False,
        },
        {
            "norm_id": "ENORM2567_4_zero_route_limit",
            "norm_symbol": "E_local_res -> E_GK_bound",
            "definition": "if E_HD=E_aux=E_tau=E_qspur=E_shadow=E_norm=E_bg=0, then the 2566 bridge reduces to the GK-only route",
            "role": "clean derivation target, not a current result",
            "status": "DESIRED_LIMIT_UNSIGNED",
            "needed_for_claim": "parent-signed zero certificate for every added slot",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def slot_decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "SDEC2567_0_all_zero_test",
            "question": "Can all non-EGK residual slots be zeroed now?",
            "answer": "NO",
            "evidence": "six retained slots plus one conditional-background slot remain unsigned after the zero attempt",
            "effect": "local-GR/Newton proof remains blocked; use extended norm only as a nonclaim scaffold",
            "valid_for_claim": False,
        },
        {
            "decision_id": "SDEC2567_1_background",
            "question": "Can e_background be treated as a clean convention rather than a physical failure?",
            "answer": "YES_CONDITIONALLY",
            "evidence": "a local reference solution can absorb Lambda/background terms if declared before readout",
            "effect": "write a background-reference certificate later; do not count it as a closed local-GR proof",
            "valid_for_claim": False,
        },
        {
            "decision_id": "SDEC2567_2_priority",
            "question": "Which retained slot should be attacked next?",
            "answer": "e_source_norm_gap",
            "evidence": "source normalization is the bridge from the parent field equation to Newtonian mass and cannot be replaced by fitted orbital GM",
            "effect": "2568 should target Hilbert/worldtube source normalization before arena kernels",
            "valid_for_claim": False,
        },
        {
            "decision_id": "SDEC2567_3_derivation_vs_bounds",
            "question": "Should the next move be empirical local bounds or derivation?",
            "answer": "DERIVATION_FIRST",
            "evidence": "R10/PPN bounds cannot rescue a circular source normalization; the parent source has to be owned first",
            "effect": "keep R10/PPN as downstream tests, not as a substitute for source closure",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2567_0_zero_sweep_done",
            "claim": "All non-EGK residual slots were audited for zero certificates.",
            "gate_status": "PASS_STRUCTURE_NONCLAIM",
            "reason": "e_HD,e_aux,e_tau,e_qspur,e_shadow,e_norm,e_background each has a zero/retain decision.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2567_1_all_zero",
            "claim": "All non-EGK slots are zero.",
            "gate_status": "BLOCKED",
            "reason": "No retained slot has a parent-signed zero theorem.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2567_2_extended_norm_source_backing",
            "claim": "Extended E_local_res is source-backed and usable for local predictions.",
            "gate_status": "BLOCKED",
            "reason": "The norm vector is formally defined, but slot coefficients, units and same-frame operator bounds are unsourced.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2567_3_source_norm",
            "claim": "The source normalization gap is closed.",
            "gate_status": "BLOCKED",
            "reason": "ell_J, kappa0/G_ref, Hilbert worldtube charge, surface independence and no-fitted-GM equivalence remain open.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2567_4_Newton_GR",
            "claim": "Newton/local-GR limit is derived.",
            "gate_status": "BLOCKED",
            "reason": "Residual slots are retained and C_res_ext is still formal.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2567_5_R10_PPN_clocks_orbits",
            "claim": "R10/PPN/clock/orbital local-test predictions can be treated as MTS predictions.",
            "gate_status": "BLOCKED",
            "reason": "C_metric_ext, C_Green, C_obs and arena kernels remain nonnumeric, and source normalization is unresolved.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2567_6_no_shortcuts",
            "claim": "No GR shortcut, fitted GM, M_H_ref laundering, plateau axiom or GitHub/public step is used.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "All shortcut routes remain explicit blockers and outputs stay in post-checkpoint-work.",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2567_0_gain",
            "decision": "Accept the zero-certificate audit as derivation progress, not a claim.",
            "reason": "It turns the vague 'extra residuals' problem into a finite list of named slots.",
            "effect": "The local-GR route is sharper because every surviving obstruction has a label and next action.",
        },
        {
            "decision_id": "DEC2567_1_extend_norm",
            "decision": "Define E_local_res as the nonclaim fallback norm.",
            "reason": "The all-zero proof fails in the current corpus, so hiding survivors under E_GK_bound would be dishonest.",
            "effect": "Future local tests must either source the extended norm or prove the added slots zero.",
        },
        {
            "decision_id": "DEC2567_2_next_source_norm",
            "decision": "Attack e_source_norm_gap next.",
            "reason": "Without a parent-owned source normalization, Newton's mass source would be fitted rather than derived.",
            "effect": "2568 selected as Hilbert/worldtube source-normalization zero-certificate attempt.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2567_0_selected",
            "selection_status": "selected",
            "target_file": "2568-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
            "target_script": "scripts/Y5_R2FR_Hilbert_worldtube_source_normalization_zero_certificate_or_Enorm_row_2568.py",
            "task": "derive or block e_source_norm_gap=0 by closing ell_J, kappa0/G_ref, Hilbert worldtube charge, surface independence, and no fitted-GM source equivalence",
            "acceptance_target": "source-normalization theorem attempt, worldtube Gauss/surface-independence gate, no-fitted-GM guardrail, E_norm retained if unsigned",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "zero_certificate": OUTPUTS["zero_certificate"],
        "extended_norm": OUTPUTS["extended_norm"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2567_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    required_slots = {
        "e_HD_curvature_operator",
        "e_aux_constraint_stress",
        "e_tau_clock_frame_leak",
        "e_q_weyl_spurion",
        "e_species_shadow_or_zero",
        "e_source_norm_gap",
        "e_background_subtraction",
    }
    found_slots = {row["slot"] for row in data["zeros"]}

    add("VAL2567_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add("VAL2567_01_required_slots", required_slots <= found_slots, "all non-EGK residual slots have zero/retain rows", ";".join(sorted(found_slots)))
    add(
        "VAL2567_02_no_false_zero",
        not any(row["retain_or_zero"] == "ZERO" or row["valid_for_claim"] is True for row in data["zeros"]),
        "no retained slot is promoted to claim-ready zero",
    )
    add(
        "VAL2567_03_extended_norm_written",
        any(row["norm_symbol"] == "E_local_res" for row in data["norms"]),
        "extended local residual norm vector is written",
    )
    add(
        "VAL2567_04_source_norm_priority",
        any(row["route_id"] == "NEXT2567_0_selected" for row in data["next"]),
        "2568 source-normalization target selected",
    )
    add("VAL2567_05_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no gate allows Newton/local-GR/R10/PPN claim")
    add(
        "VAL2567_06_zero_route_still_blocked",
        any(row["gate_id"] == "GATE2567_1_all_zero" and row["gate_status"] == "BLOCKED" for row in data["gates"]),
        "all-zero route remains blocked unless parent-signed later",
    )
    add(
        "VAL2567_07_no_fitted_GM_shortcut",
        any("fitted GM" in row.get("reason", "") or "fitted GM" in row.get("guardrails", "") for row in [*data["gates"], *data["next"]]),
        "no-fitted-GM guardrail is explicitly carried forward",
    )
    add("VAL2567_08_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2567*", "*P8_Y5_NON_EGK_ZERO_2567*", "*JR2567*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2567_09_no_formalization_artifacts", not formalization_artifacts, "no 2567 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2567_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2567_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2567_OVERALL",
        overall,
        "2567 audits non-EGK zero certificates against the 2566 bridge, retains unsigned slots in E_local_res, and selects source-normalization closure next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2567 Y5 R2FR Non-EGK Residual Zero Certificates Or Extended Local Norm",
        "",
        "**Status:** zero-certificate sweep completed against the 2566 local bridge, but no zero theorem is promoted. `E_GK_bound` remains useful but insufficient for the full residual source, so every surviving non-EGK term is carried explicitly.",
        "",
        "**Main result:** the clean all-zero route does not yet close. The honest local residual basis is now `E_local_res = E_GK_bound + E_HD + E_aux + E_tau + E_qspur + E_shadow + E_norm + E_bg`. The next best derivation target is `E_norm`, because source normalization is where the parent field equation must become Newtonian mass without fitted orbital `GM`.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Zero Certificate Attempt",
        markdown_table(data["zeros"], ["slot_id", "slot", "zero_route", "attempt_result", "reason", "retain_or_zero", "extended_norm_slot", "claim_impact", "valid_for_claim"]),
        "",
        "## Extended Local Norm Vector",
        markdown_table(data["norms"], ["norm_id", "norm_symbol", "definition", "role", "status", "needed_for_claim", "valid_for_claim"]),
        "",
        "## Slot Decision Ledger",
        markdown_table(data["slots"], ["decision_id", "question", "answer", "evidence", "effect", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "zeros": zero_certificate_rows(),
        "norms": extended_norm_rows(),
        "slots": slot_decision_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["zero_certificate"], data["zeros"])
    write_csv(OUTPUTS["extended_norm"], data["norms"])
    write_csv(OUTPUTS["slot_decision"], data["slots"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
