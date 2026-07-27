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

DOC = ROOT / "2718-Y5-R2FR-Jeff-source-norm-split-or-ZR-theorem-zero-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2718_SOURCE_REGISTER.csv",
    "zr_theorem_audit": RESIDUALS / "P8_Y5_R2FR_2718_ZR_THEOREM_ZERO_AUDIT.csv",
    "jeff_split": RESIDUALS / "P8_Y5_R2FR_2718_JEFF_SOURCE_NORM_SPLIT.csv",
    "matter_exterior": RESIDUALS / "P8_Y5_R2FR_2718_MATTER_EXTERIOR_ZERO_CONTRACT.csv",
    "bound_vector": RESIDUALS / "P8_Y5_R2FR_2718_JEFF_BOUND_VECTOR_NONCLAIM.csv",
    "green_interface": RESIDUALS / "P8_Y5_R2FR_2718_GREEN_BOUND_INTERFACE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2718_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2718_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2718_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2718_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2718_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2718_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2718_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "Jeff_source_norm_split_2718_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "Jeff_bound_vector_2718_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2718_BOUNDARY_HARMONIC_NOCHARGE_OR_FINITE_NORM_NEXT.csv",
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
        "source_id": "SRC2718_0_2717",
        "label": "2717 finite R_AB Green kernel",
        "path": ROOT / "2717-Y5-R2FR-finite-RAB-green-kernel-normalization-or-parent-coefficient-zero-under-AX1090-closure.md",
        "needles": [
            "NORM2717_1_operator",
            "GRN2717_0_flat_yukawa_kernel",
            "NEXT2717_0_selected",
            "VAL2717_OVERALL",
        ],
        "use": "operator and Green-bound interface receiving J_eff",
    },
    {
        "source_id": "SRC2718_1_1567",
        "label": "1567 parent protection clauses",
        "path": ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "needles": [
            "CON1567_2_matter_functor",
            "CON1567_3_boundary_functor",
            "CON1567_4_readout_closure",
            "CON1567_5_operator_exclusion",
            "ACQ1567_3_JR",
        ],
        "use": "zero-theorem clauses for Z_R, J_R, boundary, and readout",
    },
    {
        "source_id": "SRC2718_2_1867",
        "label": "1867 finite Z_R/J_R intake",
        "path": ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
        "needles": [
            "OLA1867_2_derivative_exclusion",
            "OLA1867_3_source_exclusion",
            "CMA1867_1_source_scalar",
            "FINT1867_5_SR_total",
        ],
        "use": "surviving countermodel and source total split target",
    },
    {
        "source_id": "SRC2718_3_2466",
        "label": "2466 Hilbert-current source bridge",
        "path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": [
            "CUR2466_A_Hilbert_energy_current",
            "CON2466_1_local_inertial_limit",
            "WT2466_2_surface_independence",
            "VAC2466_0_exact_vacuum",
            "VAL2466_OVERALL",
        ],
        "use": "least-circular matter source route and exterior-vacuum conditional zero",
    },
    {
        "source_id": "SRC2718_4_2478",
        "label": "2478 Green-bound source blockers",
        "path": ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
        "needles": [
            "RES2478_2_boundary",
            "RES2478_3_shadow",
            "BLK2478_0_Cres_coefficients",
            "GATE2478_2_Cres",
        ],
        "use": "source norm and boundary/shadow blocker template",
    },
    {
        "source_id": "SRC2718_5_2479",
        "label": "2479 residual-sector coefficient map",
        "path": ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md",
        "needles": [
            "COEF2479_C_boundary",
            "COEF2479_C_shadow",
            "COEF2479_C_norm",
            "BAS2479_1_minimal_extension",
            "VAL2479_OVERALL",
        ],
        "use": "extended residual source slots and no-fitted-GM normalization guard",
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


def zr_theorem_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ZRA2718_0_operator_exclusion",
            "target": "Z_R=0",
            "attempt": "use no D R_AB / no vertical Sobolev constructor grammar",
            "result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_closed": "operator exclusion is still a proposed parent grammar clause, not derived from MTS primitives",
            "kept_as": "zero route remains preferred if parent grammar closes",
            "valid_for_claim": False,
            "source_anchor": "1567 CON1567_5; 1867 OLA1867_2; 2717 ZERO2717_0",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "ZRA2718_1_vertical_null",
            "target": "Z_R=0",
            "attempt": "argue R_AB is presymplectic-null/auxiliary so kinetic stiffness contradicts its type",
            "result": "CONTRADICTION_SHAPE_NOT_PARENT_PROVED",
            "why_not_closed": "nullness, boundary charge silence, and readout stability are not jointly signed",
            "kept_as": "conditional contradiction check",
            "valid_for_claim": False,
            "source_anchor": "2716 PPC2716_3; 1567 THM1567_0",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "ZRA2718_2_finite_fallback",
            "target": "finite Z_R",
            "attempt": "if theorem-zero fails, keep Z_R positive and source-normalized",
            "result": "FALLBACK_STILL_REQUIRED",
            "why_not_closed": "no numeric parent coefficient, no units, no positive operator certificate",
            "kept_as": "finite Green kernel branch",
            "valid_for_claim": False,
            "source_anchor": "2717 NORM2717_1; 2717 GRN2717_0",
            "timestamp_utc": ts(),
        },
    ]


def jeff_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "JEFF2718_0_definition",
            "component": "J_eff",
            "formula": "J_eff = J_matter + J_boundary + J_harmonic + J_readout + J_shadow + J_norm",
            "norm_contract": "||J_eff||_X <= sum_i ||J_i||_X in one declared local norm X",
            "zero_route": "all components theorem-zero in exterior collar",
            "status": "SPLIT_WRITTEN_NONCLAIM",
            "units_status": "same Euler-source units conjugate to dimensionless R_AB",
            "source_path": str(ROOT / "2717-Y5-R2FR-finite-RAB-green-kernel-normalization-or-parent-coefficient-zero-under-AX1090-closure.md"),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "component_id": "JEFF2718_1_matter",
            "component": "J_matter",
            "formula": "J_matter := c_m * delta S_matter/delta R_AB, or Hilbert-current-induced reciprocal source if matter descent fails",
            "norm_contract": "||J_matter||_X <= C_matter * E_matter_tail; conditionally zero outside worldtube when T_matter=0 and matter descends",
            "zero_route": "delta S_matter/delta R_AB=0 plus exterior T_matter=0 and no species shadow",
            "status": "CONDITIONAL_EXTERIOR_ZERO_NOT_FULL_SOURCE_ZERO",
            "units_status": "requires c_m/ell_J and parent matter-current normalization",
            "source_path": str(ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md"),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "component_id": "JEFF2718_2_boundary",
            "component": "J_boundary",
            "formula": "J_boundary := boundary/corner variation contribution plus worldtube jump layer projected onto R_AB",
            "norm_contract": "||J_boundary||_X <= C_boundary * boundary_flux",
            "zero_route": "boundary functor descends through Q-boundary data and Q_R=0",
            "status": "BOUNDARY_NO_CHARGE_NOT_SIGNED",
            "units_status": "requires boundary momentum/flux units conjugate to R_AB",
            "source_path": str(ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "component_id": "JEFF2718_3_harmonic",
            "component": "J_harmonic",
            "formula": "J_harmonic := zero-mode / harmonic exterior hair contribution not captured by compact bulk source",
            "norm_contract": "||J_harmonic||_X <= C_harm * harmonic_zero_mode_amplitude",
            "zero_route": "domain plus boundary conditions remove harmonic zero mode",
            "status": "DOMAIN_BOUNDARY_PACKAGE_MISSING",
            "units_status": "same dimensionless R_AB source-equivalent norm after applying L_R",
            "source_path": str(ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md"),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "component_id": "JEFF2718_4_readout",
            "component": "J_readout",
            "formula": "J_readout := post-reduction/readout regeneration of R_AB derivative/source terms",
            "norm_contract": "||J_readout||_X <= C_readout * readout_regen_leak",
            "zero_route": "effective/readout reduction preserves ParentGenerate image",
            "status": "READOUT_STABILITY_NOT_SIGNED",
            "units_status": "requires same observed-metric/readout convention as tau_i projections",
            "source_path": str(ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "component_id": "JEFF2718_5_shadow_norm",
            "component": "J_shadow + J_norm",
            "formula": "source-shadow, species, frame, and normalization gaps including ell_J/worldtube/no-fitted-GM mismatch",
            "norm_contract": "||J_shadow+J_norm||_X <= C_shadow*source_tail + C_norm*e_source_norm_gap",
            "zero_route": "Hilbert-only universal source with parent ell_J, WEP-safe coupling, and surface-independent worldtube charge",
            "status": "SOURCE_NORMALIZATION_AND_WEP_GUARDS_OPEN",
            "units_status": "requires ell_J, kappa/G_ref convention, and worldtube charge units",
            "source_path": str(ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md"),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def matter_exterior_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "MAT2718_0_hilbert_source",
            "statement": "Use Hilbert/energy current J_M^nu=ell_J T_matter^{nu rho} tau_rho as the least-circular matter source bridge",
            "condition": "matter action metric-coupled, ell_J parent-fixed, tau parent-owned",
            "result": "best current contract retained",
            "claim_status": "NONCLAIM_CONTRACT",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "contract_id": "MAT2718_1_exterior_zero",
            "statement": "In a source-free exterior collar, T_matter=0 implies Hilbert J_M=0",
            "condition": "no matter support/tails in collar and no hidden R_AB matter coupling",
            "result": "conditional matter-piece zero",
            "claim_status": "PARTIAL_CONDITIONAL_GAIN",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "contract_id": "MAT2718_2_conservation_leak",
            "statement": "nabla_mu J_M^mu = ell_J T_matter^{mu nu} nabla_mu tau_nu plus scale-gradient/jump terms",
            "condition": "clock compatibility and worldtube jump identity not yet closed",
            "result": "surface/source leakage can survive even when bulk matter is controlled",
            "claim_status": "BLOCKER_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "contract_id": "MAT2718_3_no_fitted_GM",
            "statement": "Do not define source magnitude by observed orbital GM",
            "condition": "source must be parent/worldtube/Hilbert normalized before Newton comparisons",
            "result": "anti-circularity guard remains active",
            "claim_status": "GUARDRAIL_PASS",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def bound_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BND2718_0_total",
            "quantity": "E_Jeff",
            "definition": "E_Jeff := E_matter + E_boundary + E_harmonic + E_readout + E_shadow + E_norm",
            "feeds_green_bound": "||R_AB|| <= ||G_R|| * E_Jeff",
            "missing_before_numeric": "all C_i coefficients, units, domain, and source paths",
            "status": "EXTENDED_SOURCE_NORM_VECTOR_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "bound_id": "BND2718_1_best_partial_zero",
            "quantity": "E_matter_exterior",
            "definition": "E_matter_exterior=0 if T_matter=0, matter descends, and there are no tails/species shadows",
            "feeds_green_bound": "removes only the bulk matter source piece",
            "missing_before_numeric": "matter descent proof, ell_J, clock/worldtube closure",
            "status": "PARTIAL_ZERO_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "bound_id": "BND2718_2_remaining_local_vacuum",
            "quantity": "E_nonmatter := E_boundary + E_harmonic + E_readout + E_shadow + E_norm",
            "definition": "remaining exterior reciprocal source after bulk matter is conditionally controlled",
            "feeds_green_bound": "dominant blocker for local-vacuum plateau-free GR route",
            "missing_before_numeric": "boundary no-charge, harmonic zero-mode control, readout stability, source normalization",
            "status": "PRIMARY_BLOCKER_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def green_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "GIF2718_0_kernel_input",
            "input_to_2717": "J_eff source norm",
            "formula": "||R_AB||_L2 <= E_Jeff/M_R^2 + boundary_term",
            "what_2718_adds": "E_Jeff is now split into named source components",
            "still_missing": "numeric E_Jeff, M_R^2, boundary term, and claim-safe domain package",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "interface_id": "GIF2718_1_yukawa_input",
            "input_to_2717": "pointwise source norm and support geometry",
            "formula": "|R_AB| <= V_eff exp(-d_min/ell_R)/(4*pi Z_R d_min) * E_Jeff_inf + |R_boundary|",
            "what_2718_adds": "E_Jeff_inf must be assembled from the same component split",
            "still_missing": "V_eff,d_min,Z_R,ell_R,source support,boundary norm",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "interface_id": "GIF2718_2_local_GR_zero_condition",
            "input_to_2717": "exact source silence",
            "formula": "if E_Jeff=0 and boundary/harmonic=0, then R_AB=0 for positive operator",
            "what_2718_adds": "bulk matter exterior zero is plausible, but nonmatter pieces remain",
            "still_missing": "boundary/readout/harmonic/source-normalization zero theorems",
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2718_0_ZR_zero",
            "claim": "Z_R=0 theorem-zero",
            "status": "BLOCKED",
            "required_before_claim": "parent no-derivative grammar/action-image exhaustion signed",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2718_1_JEFF_zero",
            "claim": "J_eff=0 in local vacuum",
            "status": "BLOCKED",
            "required_before_claim": "matter descent plus boundary no-charge plus harmonic/readout/source-normalization silence",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2718_2_partial_matter_zero",
            "claim": "bulk Hilbert matter piece conditionally zeros outside source support",
            "status": "PASS_AS_CONDITIONAL_NONCLAIM_ONLY",
            "required_before_claim": "ell_J, clock compatibility, worldtube jump identity, no species shadow",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2718_3_local_GR_Newton",
            "claim": "local GR/Newton reduction",
            "status": "BLOCKED",
            "required_before_claim": "R_AB zero or fully bounded residual vector plus metric readout/gauge",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "gate_id": "GATE2718_4_public",
            "claim": "public/GitHub output",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim audit",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2718_0_boundary_harmonic",
            "missing_item": "boundary no-charge and harmonic zero-mode theorem",
            "effect": "exterior reciprocal hair survives even if bulk matter source vanishes",
            "best_next_attack": "derive boundary/harmonic silence or finite norm row",
            "claim_blocked": "local vacuum GR",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2718_1_readout",
            "missing_item": "readout stability against R_AB regeneration",
            "effect": "effective reduction can reintroduce source terms after parent elimination",
            "best_next_attack": "prove readout preserves ParentGenerate image",
            "claim_blocked": "PPN;clock;local_GR",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2718_2_source_normalization",
            "missing_item": "ell_J/worldtube/no-fitted-GM source normalization",
            "effect": "matter/source norms cannot become numeric predictions",
            "best_next_attack": "connect Hilbert current scale to parent constants",
            "claim_blocked": "Newton;R10;orbital",
            "timestamp_utc": ts(),
        },
        {
            "blocker_id": "BLK2718_3_ZR",
            "missing_item": "Z_R theorem-zero or positive numeric coefficient",
            "effect": "Green kernel remains formal",
            "best_next_attack": "operator-exclusion proof or finite coefficient source row",
            "claim_blocked": "all finite residual tests",
            "timestamp_utc": ts(),
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2718_0_ZR",
            "decision": "do not claim Z_R theorem-zero",
            "rationale": "the no-derivative grammar remains unsigned",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2718_1_source_split",
            "decision": "adopt J_eff component split as the active finite branch input",
            "rationale": "2717 kernel now needs a source norm; 2718 names the exact pieces to derive or bound",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2718_2_matter_partial",
            "decision": "record conditional exterior matter zero as partial progress only",
            "rationale": "Hilbert current gives the least-circular bulk source route, but boundary/readout/normalization remain open",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
        {
            "decision_id": "DEC2718_3_next",
            "decision": "attack boundary/harmonic no-charge next",
            "rationale": "after the bulk matter piece, exterior hair is the cleanest blocker to local-vacuum GR",
            "allowed": True,
            "claim_credit": False,
            "timestamp_utc": ts(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2718_0_selected",
            "status": "selected_primary",
            "target_doc": "2719-Y5-R2FR-boundary-harmonic-nocharge-or-finite-Jeff-bound-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_boundary_harmonic_nocharge_or_finite_Jeff_bound_under_AX1090_closure_2719.py",
            "mission": "derive boundary/corner/harmonic no-charge for the R_AB source sector, or create finite boundary/harmonic norm rows that feed E_Jeff",
            "acceptance": "boundary/harmonic source is theorem-zero, or E_boundary/E_harmonic rows become source-ready nonclaim inputs for the 2717 Green bound",
            "forbidden": "score R10/PPN; use fitted GM; hide boundary terms inside matter; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
            "timestamp_utc": ts(),
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2718_0_status",
            "sector": "local-GR bridge",
            "state": "J_eff is decomposed into named source pieces; bulk matter has a conditional exterior-zero route",
            "confidence": "real structural progress, not a claim",
            "next_need": "boundary/harmonic/readout/source-normalization closure",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2718_1_derivation",
            "sector": "derivability",
            "state": "Z_R zero still unsigned; matter descent still conditional",
            "confidence": "honest blocker",
            "next_need": "parent no-derivative grammar or finite coefficient",
            "timestamp_utc": ts(),
        },
        {
            "snapshot_id": "SNAP2718_2_testing",
            "sector": "empirical readiness",
            "state": "not ready to score; E_Jeff vector is source-ready structure only",
            "confidence": "blocked but sharpened",
            "next_need": "numeric/source-backed component norms",
            "timestamp_utc": ts(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2718_0_local_bounds",
            "source_table": "P8_Y5_R2FR_2718_JEFF_SOURCE_NORM_SPLIT.csv",
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "quarantine J_eff local-bound source split as nonclaim",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2718_1_source_weight",
            "source_table": "P8_Y5_R2FR_2718_JEFF_BOUND_VECTOR_NONCLAIM.csv",
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "quarantine E_Jeff source-weight vector as nonclaim",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
        {
            "copy_id": "COPY2718_2_next_queue",
            "source_table": "P8_Y5_R2FR_2718_NEXT_TARGET.csv",
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2719 without touching formalization-workbench",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
            "timestamp_utc": ts(),
        },
    ]


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    ok = True
    for path in paths:
        try:
            with path.open("r", newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            if not rows:
                ok = False
                details.append(f"{path.name}:0 rows")
            else:
                details.append(f"{path.name}:{len(rows)}:parsed")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def formalization_recent_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified >= SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    zr_rows: list[dict[str, Any]],
    jeff_rows: list[dict[str, Any]],
    matter_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csv_paths = [
        OUTPUTS["source_register"],
        OUTPUTS["zr_theorem_audit"],
        OUTPUTS["jeff_split"],
        OUTPUTS["matter_exterior"],
        OUTPUTS["bound_vector"],
        OUTPUTS["green_interface"],
        OUTPUTS["claim_gates"],
        OUTPUTS["blocker_stack"],
        OUTPUTS["decision_ledger"],
        OUTPUTS["next_target"],
        OUTPUTS["project_snapshot"],
        OUTPUTS["branch_copies"],
        *BRANCH_OUTPUTS.values(),
    ]
    csv_ok, csv_detail = csv_parse_details(csv_paths)
    source_ok = all(row["exists"] and row["required_needles_found"] for row in sources)
    zr_nonclaim = all(row["valid_for_claim"] is False for row in zr_rows)
    jeff_nonclaim = all(row["valid_for_claim"] is False for row in jeff_rows)
    matter_nonclaim = all(row["valid_for_claim"] is False for row in matter_rows)
    bound_nonclaim = all(row["valid_for_claim"] is False for row in bound_rows)
    green_nonclaim = all(row["valid_for_claim"] is False for row in green_rows)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    branch_ok = all(Path(row["copy_path"]).exists() and row["valid_for_claim"] is False for row in branches)
    required_components = {"J_matter", "J_boundary", "J_harmonic", "J_readout", "J_shadow + J_norm"}
    present_components = {row["component"] for row in jeff_rows}
    split_complete = required_components.issubset(present_components)
    matter_partial = any(row["claim_status"] == "PARTIAL_CONDITIONAL_GAIN" for row in matter_rows)
    formalization_count = formalization_recent_changed_count()
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in str(path).lower() for path in csv_paths)
    rows = [
        {
            "validation_id": "VAL2718_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found" if source_ok else "missing source or needle",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_2_csv_parse",
            "passed": csv_ok,
            "detail": csv_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_3_zr_nonclaim",
            "passed": zr_nonclaim,
            "detail": "Z_R theorem-zero remains unclaimed",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_4_jeff_split_complete",
            "passed": split_complete and jeff_nonclaim,
            "detail": "J_eff split includes matter,boundary,harmonic,readout,shadow/norm and remains nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_5_matter_partial_nonclaim",
            "passed": matter_partial and matter_nonclaim,
            "detail": "conditional exterior matter zero recorded as nonclaim only",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_6_bound_vector_nonclaim",
            "passed": bound_nonclaim,
            "detail": "E_Jeff bound vector remains nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_7_green_interface_nonclaim",
            "passed": green_nonclaim,
            "detail": "Green-bound interface receives E_Jeff without score claim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_8_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no local-GR/R10/PPN/public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_9_branch_copies",
            "passed": branch_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_10_no_formalization_recent_changes",
            "passed": formalization_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2718_11_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2718_OVERALL",
            "passed": overall,
            "detail": "2718 keeps Z_R theorem-zero blocked, splits J_eff into source-norm components, records conditional exterior matter zero as nonclaim, and selects boundary/harmonic no-charge next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    zr_rows: list[dict[str, Any]],
    jeff_rows: list[dict[str, Any]],
    matter_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    green_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    snapshot: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2718 - Y5/R2FR J_eff Source-norm Split Or Z_R Theorem-zero Under AX1090 Closure",
        "",
        "## Private Verdict",
        "",
        "2718 makes a useful narrowing move. The `Z_R=0` theorem-zero route is tried again and remains unsigned: no parent-owned no-derivative grammar means no theorem-zero claim. The finite branch therefore stays live.",
        "",
        "The progress is on the source side. `J_eff` is no longer a blob. It is split as `J_eff = J_matter + J_boundary + J_harmonic + J_readout + J_shadow + J_norm`, with a nonclaim norm vector `E_Jeff`. The best partial win is that the Hilbert-current route gives a conditional exterior-zero for the bulk matter piece when `T_matter=0` outside the worldtube and matter really descends. That does **not** zero the full local source, because boundary, harmonic, readout, shadow, and normalization pieces remain open.",
        "",
        "## Claim Ceiling",
        "",
        "- No `Z_R=0`, `J_eff=0`, local-GR/Newton, R10, PPN, clock, orbital, or public/GitHub claim is opened.",
        "- The exterior matter zero is partial and conditional, not a full local-vacuum proof.",
        "- All `J_eff` component rows and `E_Jeff` rows remain `valid_for_claim=false`.",
        "- No `formalization-workbench` edits are allowed from this checkpoint.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"]),
        "",
        "## Z_R Theorem-zero Audit",
        "",
        markdown_table(zr_rows, ["audit_id", "target", "attempt", "result", "why_not_closed", "kept_as", "valid_for_claim", "source_anchor"]),
        "",
        "## J_eff Source-norm Split",
        "",
        markdown_table(jeff_rows, ["component_id", "component", "formula", "norm_contract", "zero_route", "status", "units_status", "source_path", "valid_for_claim"]),
        "",
        "## Matter Exterior-zero Contract",
        "",
        markdown_table(matter_rows, ["contract_id", "statement", "condition", "result", "claim_status", "valid_for_claim"]),
        "",
        "## E_Jeff Bound Vector",
        "",
        markdown_table(bound_rows, ["bound_id", "quantity", "definition", "feeds_green_bound", "missing_before_numeric", "status", "valid_for_claim"]),
        "",
        "## Green-bound Interface",
        "",
        markdown_table(green_rows, ["interface_id", "input_to_2717", "formula", "what_2718_adds", "still_missing", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(gates, ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"]),
        "",
        "## Current Blocker Stack",
        "",
        markdown_table(blockers, ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decisions, ["decision_id", "decision", "rationale", "allowed", "claim_credit"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(snapshot, ["snapshot_id", "sector", "state", "confidence", "next_need"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(branches, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
        "## Plain-English Read",
        "",
        "This is a good step toward derived local GR because it separates the source problem into killable pieces. The bulk matter piece has a plausible Hilbert-current exterior-zero route, which is exactly the GR-compatible direction. But the theory cannot claim local vacuum yet because boundary/harmonic/readout/source-normalization pieces can still carry reciprocal hair.",
        "",
        "Next best strike: boundary and harmonic no-charge. If those die, the local branch gets materially cleaner. If they do not, they become finite source rows feeding the 2717 Green bound.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, SOURCE_WEIGHT, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    zr_rows = zr_theorem_audit_rows()
    jeff_rows = jeff_split_rows()
    matter_rows = matter_exterior_rows()
    bound_rows = bound_vector_rows()
    green_rows = green_interface_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["zr_theorem_audit"], zr_rows)
    write_csv(OUTPUTS["jeff_split"], jeff_rows)
    write_csv(OUTPUTS["matter_exterior"], matter_rows)
    write_csv(OUTPUTS["bound_vector"], bound_rows)
    write_csv(OUTPUTS["green_interface"], green_rows)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["blocker_stack"], blockers)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    write_csv(OUTPUTS["project_snapshot"], snapshot)

    write_csv(BRANCH_OUTPUTS["local_bounds"], jeff_rows)
    write_csv(BRANCH_OUTPUTS["source_weight"], bound_rows)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branches)

    pending_validation = [
        {
            "validation_id": "VAL2718_PENDING",
            "passed": False,
            "detail": "pre-validation placeholder for first doc write",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(
        sources,
        zr_rows,
        jeff_rows,
        matter_rows,
        bound_rows,
        green_rows,
        gates,
        blockers,
        decisions,
        next_rows,
        snapshot,
        branches,
        pending_validation,
    )

    validation = validation_rows(sources, zr_rows, jeff_rows, matter_rows, bound_rows, green_rows, gates, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(
        sources,
        zr_rows,
        jeff_rows,
        matter_rows,
        bound_rows,
        green_rows,
        gates,
        blockers,
        decisions,
        next_rows,
        snapshot,
        branches,
        validation,
    )

    overall = next(row for row in validation if row["validation_id"] == "VAL2718_OVERALL")
    print(f"2718 complete: {overall['passed']} - {overall['detail']}")
    print(DOC)


if __name__ == "__main__":
    main()
