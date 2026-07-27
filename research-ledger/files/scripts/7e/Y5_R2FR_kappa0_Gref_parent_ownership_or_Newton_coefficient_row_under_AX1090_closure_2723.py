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

DOC = ROOT / "2723-Y5-R2FR-kappa0-Gref-parent-ownership-or-Newton-coefficient-row-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2723_SOURCE_REGISTER.csv",
    "ownership_audit": RESIDUALS / "P8_Y5_R2FR_2723_KAPPA_GREF_OWNERSHIP_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_2723_KAPPA_GREF_THEOREM_ATTEMPT.csv",
    "guardrails": RESIDUALS / "P8_Y5_R2FR_2723_COUPLING_GUARDRAILS.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2723_FINITE_KAPPA_GREF_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2723_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2723_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2723_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2723_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2723_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2723_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2723_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2723_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "kappa0_Gref_parent_ownership_rows_2723_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "kappa0_Gref_EJeff_update_2723_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2723_EH_LEFT_HAND_WEAK_FIELD_OPERATOR_NEXT.csv",
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
        "source_id": "SRC2723_0_2722",
        "label": "2722 kappa handoff",
        "path": ROOT / "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md",
        "needles": [
            "CMAP2722_0_metric_coupling",
            "FPG2722_0_E_kappa_bridge",
            "NEXT2722_0_selected",
            "VAL2722_OVERALL",
        ],
        "use": "direct handoff selecting kappa0/G_ref parent ownership",
    },
    {
        "source_id": "SRC2723_1_1009",
        "label": "1009 EH core not total parent",
        "path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": [
            "PCS1009_0_EH_core",
            "SVR1009_0_EH_anchor_only",
            "MISSING_PARENT_SIGNED_FIXED_BEFORE_READOUT_CERTIFICATE",
        ],
        "use": "EH core exists as anchor but is refused as total parent action",
    },
    {
        "source_id": "SRC2723_2_1339",
        "label": "1339 EH-left-hand and Newton transfer gates",
        "path": ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
        "needles": [
            "EHGate1339_1_metric_only_local_4D",
            "EHGate1339_6_source_GM_transfer",
            "LOV1339_1_weak_field_algebra",
            "VAL1339_5_Newton_blocked",
        ],
        "use": "weak-field Newton algebra is conditional while EH-left-hand and GM transfer remain blocked",
    },
    {
        "source_id": "SRC2723_3_2464",
        "label": "2464 parent action skeleton",
        "path": ROOT / "2464-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-and-source-bridge.md",
        "needles": [
            "FLD2464_0_metric",
            "VAR2464_3_delta_metric",
            "GATE2464_4_local_GR_Newton_PPN",
            "VAL2464_OVERALL",
        ],
        "use": "candidate parent route includes metric variation but does not yet own full local GR/Newton branch",
    },
    {
        "source_id": "SRC2723_4_2465",
        "label": "2465 stress/source blockers",
        "path": ROOT / "2465-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md",
        "needles": [
            "STR2465_0_metric_variation_exists",
            "STR2465_4_GR_limit_gate",
            "PV2465_5_overall",
            "VAL2465_OVERALL",
        ],
        "use": "metric stress exposure prevents treating kappa as the full effective local coupling",
    },
    {
        "source_id": "SRC2723_5_2466",
        "label": "2466 source bridge",
        "path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": [
            "CUR2466_A_Hilbert_energy_current",
            "WT2466_1_mass_readout",
            "WT2466_4_no_orbital_GM",
            "VAL2466_05_worldtube_guardrail",
        ],
        "use": "source current is Hilbert/worldtube, not fitted orbital GM",
    },
    {
        "source_id": "SRC2723_6_2469",
        "label": "2469 local metric equation gate",
        "path": ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
        "needles": [
            "MET2469_0_parent_metric_equation",
            "MET2469_3_current_corpus",
            "PPN2469_0_residual_source",
            "VAL2469_OVERALL",
        ],
        "use": "extra-sector stress can renormalize or source the local metric equation",
    },
    {
        "source_id": "SRC2723_7_2470",
        "label": "2470 no-hair/stress bound",
        "path": ROOT / "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
        "needles": [
            "NH2470_5_stress_zero",
            "BND2470_2_metric_bound",
            "MET2470_2_bound_route",
            "VAL2470_OVERALL",
        ],
        "use": "stress silence remains conditional, so kappa is not yet the only effective Newton coupling",
    },
    {
        "source_id": "SRC2723_8_1006",
        "label": "1006 anti-circular denominator warning",
        "path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": [
            "MHA1006_5_anti_circularity",
            "MHS1006_2_anti_circularity",
            "CG1006_1_orbital_GM_substitution",
            "V1006_9_MHref_gate_written",
        ],
        "use": "G_ref cannot be filled from orbital GM before the bridge is derived",
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


def ownership_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "KAP2723_0_EH_anchor",
            "target": "kappa0 appears as parent EH coefficient",
            "attempt": "use S_EH[g_obs;kappa0,Lambda0] as the coupling source",
            "verdict": "ANCHOR_EXISTS_NOT_TOTAL_PARENT",
            "reason": "1009 explicitly keeps EH as a baseline anchor and refuses EH-anchor-only promotion because sector certificates are missing",
            "claim_allowed": False,
            "next_requirement": "parent-signed total local action or a fixed EH-left-hand sector certificate",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "KAP2723_1_field_equation_convention",
            "target": "kappa0 maps to Newton constant",
            "attempt": "declare field-equation convention G_{mu nu}=kappa0 T_{mu nu}",
            "verdict": "CONVENTION_CONDITIONAL",
            "reason": "2722 derived G_N=kappa0*c^4/(8*pi) only after weak-field EH and Hilbert-source assumptions",
            "claim_allowed": False,
            "next_requirement": "units/source row for kappa0 and fixed c/G_ref convention",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "KAP2723_2_fixed_before_readout",
            "target": "G_ref is fixed before fitting",
            "attempt": "identify G_ref with kappa0*c^4/(8*pi) before orbital data",
            "verdict": "GOOD_PROTOCOL_NOT_SOURCED",
            "reason": "the anti-circular rule is correct, but kappa0 itself still lacks a parent-owned numeric/source convention",
            "claim_allowed": False,
            "next_requirement": "fixed-before-readout certificate and source path",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "KAP2723_3_same_frame",
            "target": "same metric/coframe for matter, photons, clocks and source",
            "attempt": "use g_obs/e_obs as common readout frame",
            "verdict": "FRAME_NOT_FULLY_SIGNED",
            "reason": "1339 labels observed-frame closure as not full PPN signed; 2464 keeps clock/coframe conditional",
            "claim_allowed": False,
            "next_requirement": "observed-frame/tau/coframe lock or finite frame residual row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "KAP2723_4_extra_sector_renorm",
            "target": "kappa0 is the only local gravitational coupling",
            "attempt": "assume GK/tau/boundary sectors are silent or absorbed",
            "verdict": "REJECTED_AS_UNSIGNED",
            "reason": "2469/2470 show extra stress may alter the local metric equation unless no-hair or stress-bound clauses close",
            "claim_allowed": False,
            "next_requirement": "stress silence/no-hair or finite coupling-renormalization row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "KAP2723_5_verdict",
            "target": "parent-owned kappa0/G_ref",
            "attempt": "combine EH anchor, field-equation convention, fixed-before-readout, same-frame source and stress silence",
            "verdict": "KAPPA0_GREF_PARENT_OWNERSHIP_NOT_PROVED",
            "reason": "the coupling bridge is structurally clean but remains unsigned because EH anchor, metric operator, source frame and extra-sector silence are incomplete",
            "claim_allowed": False,
            "next_requirement": "finite kappa/G_ref rows plus EH-left-hand weak-field operator gate",
            "timestamp_utc": ts(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2723_0_statement",
            "statement": "If the parent local action contains a fixed EH metric sector with field-equation convention G_{mu nu}+Lambda g_{mu nu}=kappa0 T_Hilbert_{mu nu}, all matter/readout uses one observed metric/coframe, extra-sector stress is zero or separately retained, and no observed GM enters before readout, then G_ref is parent-owned by G_ref=kappa0*c^4/(8*pi).",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_clause": "total parent action sector certificate; fixed coefficient source path; same-frame readout lock; stress silence; fixed-before-readout certificate",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2723_1_EH_anchor",
            "statement": "The corpus contains an EH anchor S_EH[g_obs;kappa0,Lambda0], but that anchor is not enough to sign the total parent local coupling.",
            "status": "ANCHOR_ONLY_NONCLAIM",
            "missing_clause": "MTS residual sector and hidden-stress certificates",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2723_2_no_fit_rule",
            "statement": "G_ref may be set equal to kappa0*c^4/(8*pi) only from parent action convention, not from measured orbital GM or PPN fit.",
            "status": "ANTI_CIRCULAR_GUARDRAIL_EXACT",
            "missing_clause": "parent source value for kappa0",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2723_3_extra_sector",
            "statement": "If extra-sector stress contributes to the local metric equation, the effective Newton coupling is kappa0 plus a residual response, not a clean parent-owned G_ref.",
            "status": "STRESS_RENORMALIZATION_OPEN",
            "missing_clause": "GK/tau/boundary stress no-hair or finite bound",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def guardrail_rows() -> list[dict[str, Any]]:
    return [
        {
            "guardrail_id": "GKD2723_0_no_observed_G",
            "rule": "Do not set kappa0 or G_ref from observed orbital GM, local PPN fit, R10 limits, or cosmology fits.",
            "allowed_use": "downstream comparison only",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GKD2723_1_field_equation_convention",
            "rule": "Every use of kappa0 must declare whether it is an action coefficient or a field-equation coefficient.",
            "allowed_use": "field-equation convention for 2722 coefficient map",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GKD2723_2_same_source_frame",
            "rule": "The same observed metric/coframe/tau/source measure must define matter stress, clocks, photons and orbit readout.",
            "allowed_use": "conditional theorem or finite frame residual",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GKD2723_3_extra_stress_separate",
            "rule": "Do not absorb GK/tau/boundary stress into G_ref unless a parent renormalization theorem is signed.",
            "allowed_use": "separate E_kappa_sector_renorm row",
            "active": True,
            "claim_credit": False,
        },
        {
            "guardrail_id": "GKD2723_4_fixed_before_readout",
            "rule": "The coupling and reference convention must be fixed before local-test residuals are computed.",
            "allowed_use": "pre-fit protocol row with source path",
            "active": True,
            "claim_credit": False,
        },
    ]


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FKG2723_0_E_kappa_source",
            "quantity": "E_kappa_source",
            "definition": "E_kappa_source := missing_or_uncertain(parent source path and equation convention for kappa0)",
            "feeds": "E_kappa_bridge and Newton coefficient gate",
            "source_path": str(ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"),
            "units_need": "field-equation coupling units compatible with G_ref/c^4",
            "missing": "parent-signed coefficient source; action-vs-field-equation convention; units",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FKG2723_1_E_Gref_definition",
            "quantity": "E_Gref_definition",
            "definition": "E_Gref_definition := |G_ref - kappa0*c^4/(8*pi)|/G_ref under fixed field-equation convention",
            "feeds": "E_kappa_bridge",
            "source_path": str(ROOT / "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md"),
            "units_need": "dimensionless coupling mismatch",
            "missing": "fixed G_ref declaration before readout; no observed-GM import certificate",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FKG2723_2_E_kappa_running",
            "quantity": "E_kappa_running",
            "definition": "E_kappa_running := sup_local |partial_mu kappa_eff|/kappa0 or |Delta kappa_eff|/kappa0",
            "feeds": "E_norm_kappa and clock/orbital stability",
            "source_path": str(ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"),
            "units_need": "dimensionless or per-length coupling drift with declared scale",
            "missing": "constant-coupling theorem or running-coupling bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FKG2723_3_E_frame_coupling",
            "quantity": "E_frame_coupling",
            "definition": "E_frame_coupling := ||G_ref(source frame)-G_ref(readout frame)||/G_ref",
            "feeds": "same-frame source normalization and PPN readout",
            "source_path": str(ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"),
            "units_need": "dimensionless frame/readout coupling mismatch",
            "missing": "common observed metric/coframe/tau lock",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FKG2723_4_E_sector_renorm",
            "quantity": "E_sector_renorm",
            "definition": "E_sector_renorm := ||Delta G_eff from GK/tau/boundary stress||/G_ref",
            "feeds": "E_extra_stress_Newton and local metric residual",
            "source_path": str(ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md"),
            "units_need": "dimensionless effective-coupling shift",
            "missing": "extra-sector stress no-hair, renormalization theorem, or finite stress bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FKG2723_5_E_reference_absorption",
            "quantity": "E_reference_absorption",
            "definition": "E_reference_absorption := |Delta G_ref_fit + Delta H_ref_fit + Delta counterterm_fit|/G_ref",
            "feeds": "no-absorption guard and E_norm_reference",
            "source_path": str(ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
            "units_need": "dimensionless fitted-reference/coupling absorption residual",
            "missing": "fixed-before-readout certificate and reference convention",
            "status": "REQUIRED_GUARD_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FKG2723_6_E_unit_convention",
            "quantity": "E_unit_convention",
            "definition": "E_unit_convention := mismatch between action coefficient, field-equation coefficient, c powers and stress-energy units",
            "feeds": "coefficient-map validation",
            "source_path": str(ROOT / "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md"),
            "units_need": "declared SI/natural-unit conversion for kappa0, c and T_00",
            "missing": "unit convention source row",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2723_0_previous",
            "formula": "E_Newton_bridge includes E_kappa_bridge + E_Poisson_residual + E_Gauss_flux + E_mu_transfer + E_extra_stress_Newton + E_gauge_domain",
            "status": "INHERITED_FROM_2722",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2723_1_kappa_split",
            "formula": "E_kappa_bridge := E_kappa_source + E_Gref_definition + E_kappa_running + E_frame_coupling + E_sector_renorm + E_reference_absorption + E_unit_convention",
            "status": "REFINED_NONCLAIM_VECTOR",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2723_2_newton_feed",
            "formula": "E_Newton_bridge := E_kappa_bridge + E_Poisson_residual + E_Gauss_flux + E_mu_transfer + E_extra_stress_Newton + E_gauge_domain",
            "status": "FORMAL_GREEN_INTERFACE_ONLY",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2723_3_zero_condition",
            "formula": "E_kappa_bridge=0 only if kappa0 source, G_ref definition, constant-coupling, same-frame, sector-renorm, reference and unit clauses all close",
            "status": "ZERO_CONDITION_NOT_MET",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2723_0_kappa_owned",
            "claim": "kappa0/G_ref is parent-owned",
            "status": "BLOCKED",
            "required_before_claim": "parent-signed EH coefficient source and field-equation convention",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2723_1_Newton_coefficient",
            "claim": "G_ref=kappa0*c^4/(8*pi) is claim-ready",
            "status": "BLOCKED",
            "required_before_claim": "fixed-before-readout G_ref convention, unit row and no observed-GM import",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2723_2_effective_coupling",
            "claim": "extra sectors do not renormalize local G",
            "status": "BLOCKED",
            "required_before_claim": "stress no-hair/positivity or finite coupling-renormalization bound",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2723_3_local_GR_Newton",
            "claim": "local GR/Newton branch passes",
            "status": "BLOCKED",
            "required_before_claim": "kappa ownership plus EH-left-hand operator, source, stress, gauge and readout gates",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2723_4_public",
            "claim": "public/GitHub output",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim audit",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2723_0_EH_anchor_only",
            "missing_item": "EH coefficient is anchor-only, not total parent local action",
            "effect": "kappa0 may be a baseline convention rather than the full MTS local coupling",
            "best_next_attack": "EH-left-hand weak-field operator and sector certificate",
            "claim_blocked": "kappa ownership; Newton coefficient",
        },
        {
            "blocker_id": "BLK2723_1_convention_units",
            "missing_item": "action-vs-field-equation coefficient and c-power units",
            "effect": "G_ref map can be off by convention even if algebra shape is right",
            "best_next_attack": "unit/source row for kappa0 and G_ref",
            "claim_blocked": "coefficient map",
        },
        {
            "blocker_id": "BLK2723_2_same_frame",
            "missing_item": "common observed metric/coframe/tau/source frame",
            "effect": "source G and readout G can drift apart",
            "best_next_attack": "frame lock or finite frame-coupling row",
            "claim_blocked": "PPN/orbital comparison",
        },
        {
            "blocker_id": "BLK2723_3_sector_renorm",
            "missing_item": "extra-sector stress/no-hair or renormalization theorem",
            "effect": "local effective G can receive GK/tau/boundary response",
            "best_next_attack": "stress no-hair or E_sector_renorm bound",
            "claim_blocked": "local GR/Newton",
        },
        {
            "blocker_id": "BLK2723_4_fixed_reference",
            "missing_item": "fixed-before-readout G_ref/H_ref/counterterm protocol",
            "effect": "coupling can be tuned to absorb local residuals",
            "best_next_attack": "fixed-reference certificate",
            "claim_blocked": "robust local tests",
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2723_0_no_kappa_claim",
            "decision": "do not claim kappa0/G_ref parent ownership",
            "rationale": "EH anchor exists but is not total parent action and fixed-before-readout/source certificates remain unsigned",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2723_1_keep_coefficient_map",
            "decision": "keep G_ref=kappa0*c^4/(8*pi) as conditional coefficient map",
            "rationale": "the algebra is correct under field-equation convention and useful as the target contract",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2723_2_finite_rows",
            "decision": "install finite kappa/G_ref residual rows",
            "rationale": "coupling uncertainty must be explicit rather than absorbed into GM or readout constants",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2723_3_next",
            "decision": "move next to EH-left-hand weak-field operator/gauge-domain",
            "rationale": "the coefficient cannot be trusted until the local operator is actually the EH weak-field operator plus controlled residuals",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2723_0_selected",
            "status": "selected_primary",
            "target_doc": "2724-Y5-R2FR-EH-left-hand-weak-field-operator-gauge-domain-or-Poisson-residual-row-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_EH_left_hand_weak_field_operator_gauge_domain_or_Poisson_residual_row_under_AX1090_closure_2724.py",
            "mission": "prove the local weak-field left-hand operator really reduces to the EH G_00 Poisson operator in the same gauge/domain, or keep E_Poisson_residual/E_gauge_domain rows explicit",
            "acceptance": "EH-left-hand operator/gauge/domain contract with all missing residuals named, or a nonclaim Poisson residual ledger",
            "forbidden": "use observed orbital GM; claim Newton/local GR/PPN; hide extra stress; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2723_0_status",
            "sector": "coupling/Newton bridge",
            "state": "kappa0-to-G_ref map is conditionally clean but parent ownership is not signed",
            "confidence": "strong algebra, weak provenance",
            "next_need": "EH-left-hand weak-field operator and source/unit convention",
        },
        {
            "snapshot_id": "SNAP2723_1_best_route",
            "sector": "derivation",
            "state": "keep G_ref as a parent coefficient target, never a fitted orbital-GM import",
            "confidence": "high as anti-circular method",
            "next_need": "metric operator/gauge/domain proof",
        },
        {
            "snapshot_id": "SNAP2723_2_risk",
            "sector": "local tests",
            "state": "extra sectors or frame drift can still shift the effective coupling seen by PPN/orbits",
            "confidence": "high blocker visibility",
            "next_need": "stress no-hair/bound and same-frame lock",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2723_0_local_bounds",
            "source_table": OUTPUTS["finite_rows"].name,
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "quarantine kappa/G_ref rows as nonclaim",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2723_1_source_weight",
            "source_table": OUTPUTS["ejeff_update"].name,
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "quarantine kappa/G_ref E_Jeff update vector as nonclaim",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2723_2_next_queue",
            "source_table": OUTPUTS["next_target"].name,
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2724 without touching formalization-workbench",
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
    guardrails: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_kappa_source",
        "E_Gref_definition",
        "E_kappa_running",
        "E_frame_coupling",
        "E_sector_renorm",
        "E_reference_absorption",
        "E_unit_convention",
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
    guardrails_active = all(row["active"] is True and row["claim_credit"] is False for row in guardrails)
    finite_nonclaim = (
        {row["quantity"] for row in finite} == required_quantities
        and all(row["valid_for_claim"] is False for row in finite)
    )
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {
            "validation_id": "VAL2723_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_2_csv_parse",
            "passed": all(result[0] for result in parse_results),
            "detail": parse_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_3_theorem_nonclaim",
            "passed": theorem_nonclaim,
            "detail": "kappa0/G_ref theorem remains conditional and no coupling ownership is promoted",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_4_guardrails_active",
            "passed": guardrails_active,
            "detail": "no-observed-G, convention, same-frame, extra-stress and fixed-before-readout guardrails are active",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_5_finite_rows_complete_nonclaim",
            "passed": finite_nonclaim,
            "detail": "finite rows include source,Gref,running,frame,sector,reference,unit components and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_6_ejeff_update_nonclaim",
            "passed": ejeff_nonclaim,
            "detail": "kappa/G_ref E_Jeff update vector remains formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_7_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no kappa/Newton/PPN/local-GR/public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_8_branch_copies",
            "passed": branch_paths_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_9_no_formalization_recent_changes",
            "passed": formalization_recent_changed_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2723_10_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2723_OVERALL",
            "passed": overall,
            "detail": "2723 keeps kappa0/G_ref parent ownership conditional, installs finite coupling rows, and selects EH-left-hand weak-field operator next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2723 - Y5/R2FR kappa0-Gref Parent Ownership Or Newton Coefficient Row Under AX1090 Closure

## Private Verdict

2723 answers the coupling question honestly: `kappa0` is present as an EH anchor, and the conditional coefficient map from 2722 is clean, but `kappa0/G_ref` is **not yet parent-owned at claim level**.

The reason is precise, not vague. The corpus has an `S_EH[g_obs;kappa0,Lambda0]` anchor, but 1009 refuses EH-anchor-only promotion because the total parent action, hidden stress, source bridge, tau/coframe, boundary and fixed-before-readout certificates are incomplete. So the correct status is:

`G_ref = kappa0*c^4/(8*pi)` is the target contract, not yet a sourced claim.

The useful progress is the coupling leak vector: `E_kappa_source`, `E_Gref_definition`, `E_kappa_running`, `E_frame_coupling`, `E_sector_renorm`, `E_reference_absorption`, and `E_unit_convention`.

## Claim Ceiling

- No parent-owned `kappa0/G_ref`, Newton coefficient, Newtonian mechanics, local-GR/Newton, R10, PPN, clock, orbital, WEP, or public/GitHub claim is opened.
- Observed orbital `GM` remains downstream only; it cannot define `G_ref`, `kappa0`, `M_source`, or any denominator.
- Coupling rows are source-ready schemas only and remain `valid_for_claim=false`.
- No `formalization-workbench` edits are allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## kappa0-Gref Ownership Audit

{markdown_table(rows["ownership_audit"], ["audit_id", "target", "attempt", "verdict", "reason", "claim_allowed", "next_requirement"])}

## Conditional Theorem Attempt

{markdown_table(rows["theorem_attempt"], ["theorem_id", "statement", "status", "missing_clause", "claim_allowed"])}

## Coupling Guardrails

{markdown_table(rows["guardrails"], ["guardrail_id", "rule", "allowed_use", "active", "claim_credit"])}

## Finite kappa0-Gref Rows

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

This is the coupling gate, and it did not fold. We did not get to claim the coupling, but we did pin down exactly what “owning the coupling” means. No fitted `GM`, no fitted `G`, no hidden sector stress pretending to be Newton. The next move is the left-hand operator: prove the actual local weak-field equation really has the EH `G_00` Poisson operator, or carry the Poisson/gauge residual explicitly.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    ownership_rows = ownership_audit_rows()
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
        "ownership_audit": ownership_rows,
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
            "validation_id": "VAL2723_PRE_DOC",
            "passed": False,
            "detail": "pre-document placeholder",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(data)

    validation = validation_rows(source_rows, theorem_rows, guardrails, finite, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2723 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
