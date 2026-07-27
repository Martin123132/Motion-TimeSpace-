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

DOC = ROOT / "2721-Y5-R2FR-source-normalization-no-fitted-GM-or-finite-EJeff-vector-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2721_SOURCE_REGISTER.csv",
    "normalization_audit": RESIDUALS / "P8_Y5_R2FR_2721_SOURCE_NORMALIZATION_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_2721_NO_FITTED_GM_THEOREM_ATTEMPT.csv",
    "guardrails": RESIDUALS / "P8_Y5_R2FR_2721_NO_ABSORPTION_GUARDRAILS.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2721_FINITE_ENORM_ESHADOW_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2721_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2721_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2721_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2721_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2721_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2721_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2721_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2721_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "source_normalization_Enorm_Eshadow_rows_2721_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "Enorm_Eshadow_EJeff_update_2721_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2721_POISSON_GAUSS_NEWTON_COEFFICIENT_NEXT.csv",
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
        "source_id": "SRC2721_0_2720",
        "label": "2720 no-absorption handoff",
        "path": ROOT / "2720-Y5-R2FR-readout-stability-or-finite-Jreadout-bound-under-AX1090-closure.md",
        "needles": [
            "FJR2720_5_E_no_absorption_guard",
            "BLK2720_3_no_absorption",
            "NEXT2720_0_selected",
            "VAL2720_OVERALL",
        ],
        "use": "direct handoff selecting source normalization/no-fitted-GM as the next local-GR bridge gate",
    },
    {
        "source_id": "SRC2721_1_2480",
        "label": "2480 E_norm priority",
        "path": ROOT / "2480-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-norm-vector.md",
        "needles": [
            "ZERO2480_e_norm",
            "ENORM2480_1_extended",
            "NEXT2480_0_selected",
            "VAL2480_OVERALL",
        ],
        "use": "shows source normalization is the highest-value retained non-EGK slot",
    },
    {
        "source_id": "SRC2721_2_2466",
        "label": "2466 Hilbert/worldtube source bridge",
        "path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": [
            "CUR2466_A_Hilbert_energy_current",
            "WT2466_1_mass_readout",
            "WT2466_4_no_orbital_GM",
            "VAL2466_05_worldtube_guardrail",
        ],
        "use": "identifies Hilbert source current and rejects fitted orbital GM as source definition",
    },
    {
        "source_id": "SRC2721_3_2467",
        "label": "2467 Hilbert-current conservation and scale",
        "path": ROOT / "2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
        "needles": [
            "DIV2467_1_full_divergence",
            "SCL2467_1_mass_readout_cancels",
            "SCL2467_4_empirical_fit_forbidden",
            "VAL2467_OVERALL",
        ],
        "use": "gives the exact current divergence and parent-scale/non-fit warning",
    },
    {
        "source_id": "SRC2721_4_2468",
        "label": "2468 stationary source theorem",
        "path": ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
        "needles": [
            "EXT2468_3_surface_mass",
            "DYN2468_1_exchange_required",
            "GATE2468_0_stationary_q_zero",
            "VAL2468_OVERALL",
        ],
        "use": "provides the conditional stationary source-mass theorem but keeps dynamic exchange blocked",
    },
    {
        "source_id": "SRC2721_5_2469",
        "label": "2469 local metric/stress gate",
        "path": ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
        "needles": [
            "MET2469_0_parent_metric_equation",
            "MET2469_3_current_corpus",
            "PPN2469_0_residual_source",
            "VAL2469_OVERALL",
        ],
        "use": "prevents source normalization from becoming a local-GR claim while extra stress remains open",
    },
    {
        "source_id": "SRC2721_6_2208",
        "label": "2208 PPN/source-normalization blocker",
        "path": ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md",
        "needles": [
            "PPNL2208_3_source_normalization",
            "measured-GM no-absorption rule",
            "VAL2208_OVERALL",
        ],
        "use": "connects dimensionless PPN residuals to fixed source normalization",
    },
    {
        "source_id": "SRC2721_7_2479",
        "label": "2479 C_norm/C_shadow coefficient blocker",
        "path": ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md",
        "needles": [
            "COEF2479_C_shadow",
            "COEF2479_C_norm",
            "CRES2479_0_current_formula",
            "GATE2479_5_no_shortcuts",
            "VAL2479_OVERALL",
        ],
        "use": "maps normalization and source-shadow gaps into residual coefficients",
    },
    {
        "source_id": "SRC2721_8_1006",
        "label": "1006 M_H_ref anti-circularity",
        "path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": [
            "MHA1006_5_anti_circularity",
            "MHA1006_6_theorem_verdict",
            "MHS1006_2_anti_circularity",
            "V1006_9_MHref_gate_written",
        ],
        "use": "blocks reuse of orbital GM or an unsourced denominator as the source normalizer",
    },
    {
        "source_id": "SRC2721_9_1361",
        "label": "1361 observed coframe/source-frame lock",
        "path": ROOT / "1361-Y5-R10-RAB-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
        "needles": [
            "CTL1361_6_Hilbert_current_before_readout",
            "CTL1361_7_positive_MHref_denominator",
            "MHR1361_0_M_H_ref_first_row",
            "MHR1361_1_acceptance_requirements",
        ],
        "use": "requires same observed coframe/tau/source frame before any denominator or source charge is promoted",
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


def normalization_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SN2721_0_Hilbert_source",
            "target": "source mass before orbital readout",
            "attempt": "define M_source[W]=int_{Sigma cap W} T_matter^{mu nu} tau_nu dSigma_mu in a fixed observed coframe",
            "verdict": "BEST_CONTRACT_CONDITIONAL",
            "reason": "2466/2468 make this the least circular source bridge; it matches GR stress-energy sourcing and rejects fitted orbital GM",
            "claim_allowed": False,
            "next_requirement": "same coframe/tau lock, parent matter descent, and stationary/worldtube support conditions",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "SN2721_1_kappa_Gref",
            "target": "gravitational coupling normalization",
            "attempt": "use fixed EH/weak-field coefficient kappa0 or G_ref before tests",
            "verdict": "CONDITIONAL_STANDARD_BRIDGE",
            "reason": "linearized EH would fix Newtonian coupling once kappa0 and source stress are parent-owned, but current corpus has not signed the full metric equation and extra-sector silence",
            "claim_allowed": False,
            "next_requirement": "Poisson/Gauss bridge from parent metric equation with fixed kappa0/G_ref",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "SN2721_2_no_fitted_GM",
            "target": "forbid residual absorption into GM/G_ref/source charge",
            "attempt": "declare observed orbital GM as downstream readout, not a normalizer",
            "verdict": "GUARDRAIL_PASSES_NOT_THEOREM",
            "reason": "2466, 1006 and 2208 all reject orbital-GM substitution; this blocks a cheat but does not supply the missing source coefficients",
            "claim_allowed": False,
            "next_requirement": "no-absorption row plus a downstream comparison protocol",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "SN2721_3_surface_independence",
            "target": "worldtube source charge is surface-independent",
            "attempt": "use stationary compact-source theorem",
            "verdict": "CONDITIONAL_LOCAL_THEOREM_ONLY",
            "reason": "2468 closes surface mass only under stationary compact-source hypotheses; dynamic clock exchange remains missing",
            "claim_allowed": False,
            "next_requirement": "dynamic exchange current or restrict local theorem to stationary collars",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "SN2721_4_extra_stress",
            "target": "source normalization implies local metric/GR normalization",
            "attempt": "let Hilbert source alone fix Newton limit",
            "verdict": "REJECTED_AS_INCOMPLETE",
            "reason": "2469 shows q_loc/source silence does not silence T_GK, boundary, tau/projector or vacuum stress",
            "claim_allowed": False,
            "next_requirement": "stress-silence/no-hair or explicit residual stress bound",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "SN2721_5_verdict",
            "target": "E_norm=0 and no-fitted-GM local bridge",
            "attempt": "combine Hilbert source, fixed kappa0/G_ref, stationary surface mass, no absorption, and stress silence",
            "verdict": "SOURCE_NORMALIZATION_ZERO_NOT_DERIVED_FINITE_ROWS_REQUIRED",
            "reason": "the route is promising and sharper, but kappa/G_ref, dynamic exchange, Poisson/Gauss bridge, and extra-sector stress remain unsigned",
            "claim_allowed": False,
            "next_requirement": "finite E_norm/E_shadow rows plus Poisson-Gauss Newton coefficient gate",
            "timestamp_utc": ts(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2721_0_statement",
            "statement": "If the parent action fixes the EH/weak-field coefficient kappa0, matter descends universally to a Hilbert stress tensor in one observed coframe, the stationary worldtube Hilbert charge M_source is surface-independent, extra-sector stress is zero or explicitly retained, and observed GM is used only after the Poisson/Gauss readout, then source normalization is fixed and E_norm=0.",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_clause": "kappa0/G_ref parent convention; Poisson/Gauss bridge; dynamic exchange or stationary-domain restriction; extra-sector stress silence; same-frame coframe/tau/source lock",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2721_1_Hilbert_mass",
            "statement": "M_source[W]=int_{Sigma cap W} T_matter^{mu nu} tau_nu dSigma_mu is the non-circular mass/energy source candidate; orbital GM cannot define it.",
            "status": "CONDITIONAL_ON_DESCENT_AND_SURFACE_INDEPENDENCE",
            "missing_clause": "same-frame coframe/tau lock and dynamic worldtube exchange",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2721_2_standard_linearized_bridge",
            "statement": "For an EH metric equation with fixed kappa0 and no extra stress, the weak-field slow-source limit gives a Poisson/Gauss law where the Newtonian coefficient is read from kappa0 and the Hilbert source, not fitted afterwards.",
            "status": "STANDARD_BRIDGE_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_clause": "parent metric equation, gauge/domain rule, stress silence, and kappa0-to-G_ref convention",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2721_3_no_absorption",
            "statement": "A local residual is claim-testable only after G_ref, source charge and reference/counterterm convention are fixed before residual fitting; otherwise Delta(GM) is an absorption channel.",
            "status": "GUARDRAIL_EXACT_AS_PROTOCOL",
            "missing_clause": "numerical/source-backed fixed reference row and arena comparison protocol",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2721_4_shadow_coupling",
            "statement": "E_shadow=0 only if every non-Hilbert, species, vertical, disformal or source-shadow current reduces to the same Hilbert source or is independently bounded.",
            "status": "UNSIGNED_SOURCE_SHADOW_ZERO",
            "missing_clause": "universal coupling theorem for A/Gamma/tau/matter constants",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def guardrail_rows() -> list[dict[str, Any]]:
    return [
        {
            "guardrail_id": "GUARD2721_0_no_orbital_GM_input",
            "rule": "Observed orbital GM cannot be used to define M_source, M_H_ref, G_ref, or any residual normalizer.",
            "allowed_use": "downstream observable after parent source and coupling are fixed",
            "violation_effect": "circular Newton/PPN claim",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GUARD2721_1_fixed_before_fit",
            "rule": "G_ref, kappa0, H_ref/counterterms, source charge and tau/coframe frame must be declared before fitting local residuals.",
            "allowed_use": "pre-fit protocol row only",
            "violation_effect": "residual absorption into constants",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GUARD2721_2_one_source_measure",
            "rule": "R10, PPN, clocks and orbital tests must use the same parent source measure unless a sourced conversion row exists.",
            "allowed_use": "arena projection after common source normalization",
            "violation_effect": "incompatible wins across arenas",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GUARD2721_3_no_reference_cancellation",
            "rule": "H_ref/background/counterterm choices cannot be tuned to cancel the tested residual.",
            "allowed_use": "fixed reference convention with source path",
            "violation_effect": "fake local-GR pass",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GUARD2721_4_no_shadow_hiding",
            "rule": "Non-Hilbert source-shadow and species-dependent currents cannot be hidden in E_norm.",
            "allowed_use": "separate E_shadow row or zero theorem",
            "violation_effect": "WEP/composition leakage hidden as normalization",
            "active": True,
            "claim_credit": False,
        },
    ]


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FSN2721_0_E_norm_kappa",
            "quantity": "E_norm_kappa",
            "definition": "E_norm_kappa := C_kappa * |Delta kappa0/kappa0 or Delta G_ref/G_ref| under fixed parent metric coefficient",
            "feeds": "E_norm and E_Jeff",
            "source_path": str(ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md"),
            "units_need": "dimensionless coupling normalization residual",
            "missing": "parent kappa0/G_ref convention; Poisson/Gauss bridge; source path",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FSN2721_1_E_norm_source_charge",
            "quantity": "E_norm_source_charge",
            "definition": "E_norm_source_charge := C_Q * |M_source(parent Hilbert charge) - M_source(readout convention)|/M_source",
            "feeds": "E_norm and Newton/PPN source normalization",
            "source_path": str(ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md"),
            "units_need": "dimensionless source-charge mismatch in one observed coframe",
            "missing": "same-frame e_obs/tau; Hilbert source integral; matter descent; source path",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FSN2721_2_E_norm_surface_drift",
            "quantity": "E_norm_surface_drift",
            "definition": "E_norm_surface_drift := C_surface * |Q_M[Sigma_2]-Q_M[Sigma_1]|/M_source",
            "feeds": "E_norm and worldtube surface-independence gate",
            "source_path": str(ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md"),
            "units_need": "dimensionless worldtube charge drift",
            "missing": "dynamic exchange current or explicit stationary-domain restriction; side-flux bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FSN2721_3_E_norm_reference",
            "quantity": "E_norm_reference",
            "definition": "E_norm_reference := C_ref * |Delta H_ref + Delta boundary_counterterm|/M_source under fixed reference convention",
            "feeds": "E_norm and no-reference-cancellation guard",
            "source_path": str(ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
            "units_need": "dimensionless reference/counterterm normalization residual",
            "missing": "H_ref/counterterm convention; positivity; fixed-before-readout certificate",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FSN2721_4_E_norm_absorption",
            "quantity": "E_norm_absorption",
            "definition": "E_norm_absorption := C_abs * |Delta(GM)_fit + Delta(source_charge)_fit|/M_source with all fitted-normalizer routes forbidden",
            "feeds": "E_norm and claim gate",
            "source_path": str(ROOT / "2720-Y5-R2FR-readout-stability-or-finite-Jreadout-bound-under-AX1090-closure.md"),
            "units_need": "dimensionless absorption-attempt residual flag or bound",
            "missing": "comparison protocol proving normalizers were fixed before fit",
            "status": "REQUIRED_GUARD_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FSN2721_5_E_norm_extra_stress",
            "quantity": "E_norm_extra_stress",
            "definition": "E_norm_extra_stress := C_stress * ||T_GK + T_tau/P + boundary||/||T_matter_source||",
            "feeds": "E_norm, E_Jeff and local metric residual",
            "source_path": str(ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md"),
            "units_need": "dimensionless stress residual relative to Hilbert source scale",
            "missing": "GK stress silence/no-hair or explicit stress norm bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FSN2721_6_E_shadow_species",
            "quantity": "E_shadow_species",
            "definition": "E_shadow_species := C_shadow * ||J_nonHilbert + J_species + J_disformal||/||J_Hilbert||",
            "feeds": "E_shadow and WEP/source-shadow branch",
            "source_path": str(ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md"),
            "units_need": "dimensionless source-shadow/species-current residual",
            "missing": "universal coupling theorem or source-backed composition bounds",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2721_0_previous",
            "formula": "E_nonmatter = E_boundary + E_harmonic + E_readout + E_shadow + E_norm",
            "status": "INHERITED_FROM_2718",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2721_1_norm_split",
            "formula": "E_norm := E_norm_kappa + E_norm_source_charge + E_norm_surface_drift + E_norm_reference + E_norm_absorption + E_norm_extra_stress",
            "status": "REFINED_NONCLAIM_VECTOR",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2721_2_shadow_split",
            "formula": "E_shadow := E_shadow_species + any retained non-Hilbert source-current tail",
            "status": "REFINED_NONCLAIM_VECTOR",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2721_3_green_feed",
            "formula": "||R_AB|| <= ||G_R||*(E_matter + E_boundary_hair + E_readout + E_shadow + E_norm)",
            "status": "FORMAL_GREEN_INTERFACE_ONLY",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2721_4_zero_condition",
            "formula": "E_norm=E_shadow=0 only if source charge, kappa/G_ref, reference, surface-independence, no-absorption and species-shadow clauses all close",
            "status": "ZERO_CONDITION_NOT_MET",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2721_0_Enorm_zero",
            "claim": "E_norm=0",
            "status": "BLOCKED",
            "required_before_claim": "fixed kappa/G_ref, Hilbert source charge, surface-independence, fixed reference and no absorption",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2721_1_Eshadow_zero",
            "claim": "E_shadow=0",
            "status": "BLOCKED",
            "required_before_claim": "universal matter/source coupling or bounded non-Hilbert/species currents",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2721_2_Newton_source",
            "claim": "Newton source normalization is derived",
            "status": "BLOCKED",
            "required_before_claim": "Poisson/Gauss bridge from parent metric equation with fixed coupling and stress silence",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2721_3_PPN_local_GR",
            "claim": "PPN/local-GR branch passes",
            "status": "BLOCKED",
            "required_before_claim": "E_Jeff source vector zero/bounded plus readout and source normalization fixed",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2721_4_public",
            "claim": "public/GitHub output",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim audit",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2721_0_kappa_Gref",
            "missing_item": "parent-owned kappa0/G_ref and Poisson/Gauss normalization",
            "effect": "Hilbert source cannot yet set Newtonian coefficient without a fit",
            "best_next_attack": "derive linearized parent metric equation to Poisson law",
            "claim_blocked": "Newton source; PPN",
        },
        {
            "blocker_id": "BLK2721_1_worldtube_dynamic",
            "missing_item": "dynamic exchange current or strict stationary-domain restriction",
            "effect": "source charge can drift between hypersurfaces outside stationary collars",
            "best_next_attack": "derive exchange identity or keep E_norm_surface_drift finite",
            "claim_blocked": "global source normalization",
        },
        {
            "blocker_id": "BLK2721_2_extra_stress",
            "missing_item": "T_GK/tau/boundary stress silence",
            "effect": "even correct Hilbert source does not guarantee GR metric equation",
            "best_next_attack": "GK no-hair/positivity or stress-bound row",
            "claim_blocked": "local GR; PPN",
        },
        {
            "blocker_id": "BLK2721_3_reference",
            "missing_item": "fixed H_ref/background/counterterm convention",
            "effect": "residuals can be cancelled by a moving reference",
            "best_next_attack": "fixed-reference certificate tied to parent action",
            "claim_blocked": "source-normalized residual scoring",
        },
        {
            "blocker_id": "BLK2721_4_shadow_species",
            "missing_item": "universal source-coupling theorem",
            "effect": "composition/species charge can reappear as source-shadow rather than Hilbert stress",
            "best_next_attack": "prove all matter/source couplings descend through Hilbert stress or bound E_shadow_species",
            "claim_blocked": "WEP-safe local branch",
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2721_0_no_Enorm_zero_claim",
            "decision": "do not claim E_norm=0",
            "rationale": "source normalization has a strong conditional path but kappa/G_ref, surface drift, reference and stress clauses remain unsigned",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2721_1_accept_Hilbert_contract",
            "decision": "keep Hilbert source mass as primary non-circular source contract",
            "rationale": "it is the only route that looks like GR/Newton rather than a fitted orbital normalization",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2721_2_finite_rows",
            "decision": "install E_norm/E_shadow component rows",
            "rationale": "every source-normalization leak must be a named residual rather than hidden in readout or constants",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2721_3_next",
            "decision": "move next to Poisson-Gauss Newton coefficient bridge",
            "rationale": "the next decisive derivation is showing parent Hilbert source and kappa0 produce Newton's Poisson law without fitted GM",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2721_0_selected",
            "status": "selected_primary",
            "target_doc": "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_Poisson_Gauss_Newton_coefficient_bridge_or_Enorm_bound_under_AX1090_closure_2722.py",
            "mission": "derive the weak-field Poisson/Gauss bridge from parent metric coefficient and Hilbert source to Newtonian GM, or keep E_norm_kappa/source_charge as explicit finite nonclaim rows",
            "acceptance": "conditional Newton coefficient theorem with all hypotheses explicit, or a blocker ledger proving source normalization remains finite-bound only",
            "forbidden": "use observed orbital GM as input; claim local GR/PPN; hide extra stress; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2721_0_status",
            "sector": "local GR/Newton bridge",
            "state": "source normalization is now a named theorem target and finite residual vector, not a vague objection",
            "confidence": "good structural progress, still nonclaim",
            "next_need": "Poisson/Gauss Newton coefficient bridge",
        },
        {
            "snapshot_id": "SNAP2721_1_best_route",
            "sector": "derivation",
            "state": "Hilbert source mass plus fixed EH coupling is the cleanest route; fitted orbital GM is forbidden",
            "confidence": "high as strategy",
            "next_need": "parent metric equation and fixed kappa0/G_ref",
        },
        {
            "snapshot_id": "SNAP2721_2_risk",
            "sector": "claim risk",
            "state": "extra stress and species-shadow can still ruin local GR even if source mass is correct",
            "confidence": "high blocker visibility",
            "next_need": "stress silence/no-hair or explicit stress bound",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2721_0_local_bounds",
            "source_table": OUTPUTS["finite_rows"].name,
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "quarantine source-normalization rows as nonclaim",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2721_1_source_weight",
            "source_table": OUTPUTS["ejeff_update"].name,
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "quarantine E_norm/E_shadow/E_Jeff update vector as nonclaim",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2721_2_next_queue",
            "source_table": OUTPUTS["next_target"].name,
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2722 without touching formalization-workbench",
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
    guardrails: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_norm_kappa",
        "E_norm_source_charge",
        "E_norm_surface_drift",
        "E_norm_reference",
        "E_norm_absorption",
        "E_norm_extra_stress",
        "E_shadow_species",
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
    guardrails_active = all(row["active"] is True and row["claim_credit"] is False for row in guardrails)
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {
            "validation_id": "VAL2721_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_2_csv_parse",
            "passed": all(result[0] for result in parse_results),
            "detail": parse_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_3_theorem_nonclaim",
            "passed": theorem_nonclaim,
            "detail": "source-normalization theorem remains conditional and no E_norm zero is promoted",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_4_guardrails_active",
            "passed": guardrails_active,
            "detail": "no-fitted-GM, fixed-before-fit, one-source-measure, no-reference-cancellation and no-shadow-hiding guardrails are active",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_5_finite_rows_complete_nonclaim",
            "passed": finite_nonclaim,
            "detail": "finite E_norm/E_shadow rows include kappa,source_charge,surface,reference,absorption,extra_stress,species components and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_6_ejeff_update_nonclaim",
            "passed": ejeff_nonclaim,
            "detail": "E_norm/E_shadow/E_Jeff update vector remains formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_7_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no source-normalization/Newton/PPN/local-GR/public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_8_branch_copies",
            "passed": branch_paths_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_9_no_formalization_recent_changes",
            "passed": formalization_recent_changed_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2721_10_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2721_OVERALL",
            "passed": overall,
            "detail": "2721 fixes the no-fitted-GM protocol as a guardrail, refines E_norm/E_shadow rows, and selects Poisson-Gauss Newton coefficient bridge next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2721 - Y5/R2FR Source Normalization No-fitted-GM Or Finite E_Jeff Vector Under AX1090 Closure

## Private Verdict

2721 attacks the normalization cheat-door. It does **not** prove `E_norm=0`, and it does not claim Newton/GR. But it does lock the protocol: observed orbital `GM`, fitted `G_ref`, fitted source charge, and moving reference constants cannot be used to define the source normalizer. They are downstream readouts only.

The clean route is now explicit: parent Hilbert source mass plus a fixed parent metric coupling must produce the Newtonian Poisson/Gauss coefficient before any local residuals are scored. That is the right GR-like path. Current MTS has a strong conditional scaffold, especially the stationary worldtube/Hilbert-source theorem, but the `kappa0/G_ref` convention, Poisson/Gauss bridge, dynamic exchange, fixed reference, source-shadow, and extra-stress silence are not yet parent-signed.

The useful progress is a sharper `E_norm/E_shadow` split. Any future local-GR or PPN test has to carry these rows or prove them zero.

## Claim Ceiling

- No `E_norm=0`, `E_shadow=0`, Newton-source, local-GR/Newton, R10, PPN, clock, orbital, WEP, or public/GitHub claim is opened.
- No observed orbital `GM`, fitted `G_ref`, fitted source charge, moving `H_ref`, or reference cancellation is allowed as an input normalizer.
- Source-normalization rows are source-ready schemas only and remain `valid_for_claim=false`.
- No `formalization-workbench` edits are allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## Source Normalization Audit

{markdown_table(rows["normalization_audit"], ["audit_id", "target", "attempt", "verdict", "reason", "claim_allowed", "next_requirement"])}

## Conditional Theorem Attempt

{markdown_table(rows["theorem_attempt"], ["theorem_id", "statement", "status", "missing_clause", "claim_allowed"])}

## No-absorption Guardrails

{markdown_table(rows["guardrails"], ["guardrail_id", "rule", "allowed_use", "violation_effect", "active", "claim_credit"])}

## Finite E_norm/E_shadow Rows

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

This is a useful anti-cheat checkpoint. We did not magically get Newton, but we did box off the thing that would make Newton fake: normalizing by the very `GM` we are supposed to derive. The next move is the real one: derive the Poisson/Gauss bridge from the parent metric equation and Hilbert source. If that bridge closes, the local branch gets much more serious. If not, `E_norm` stays as an explicit residual row rather than a hidden fitted constant.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    normalization_rows = normalization_audit_rows()
    theorem_rows = theorem_attempt_rows()
    guardrails = guardrail_rows()
    finite = finite_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "normalization_audit": normalization_rows,
        "theorem_attempt": theorem_rows,
        "guardrails": guardrails,
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
            "validation_id": "VAL2721_PRE_DOC",
            "passed": False,
            "detail": "pre-document placeholder",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(data)

    validation = validation_rows(source_rows, theorem_rows, finite, guardrails, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2721 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
