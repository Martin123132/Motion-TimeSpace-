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

DOC = ROOT / "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2722_SOURCE_REGISTER.csv",
    "poisson_audit": RESIDUALS / "P8_Y5_R2FR_2722_POISSON_GAUSS_BRIDGE_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_2722_NEWTON_COEFFICIENT_THEOREM_ATTEMPT.csv",
    "coefficient_map": RESIDUALS / "P8_Y5_R2FR_2722_COEFFICIENT_MAP_NONCLAIM.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2722_FINITE_NEWTON_ENORM_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2722_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2722_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2722_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2722_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2722_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2722_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2722_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2722_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "Poisson_Gauss_Newton_Enorm_rows_2722_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "Newton_coefficient_EJeff_update_2722_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2722_KAPPA0_GREF_PARENT_OWNERSHIP_NEXT.csv",
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
        "source_id": "SRC2722_0_2721",
        "label": "2721 Poisson/Gauss handoff",
        "path": ROOT / "2721-Y5-R2FR-source-normalization-no-fitted-GM-or-finite-EJeff-vector-under-AX1090-closure.md",
        "needles": [
            "FSN2721_0_E_norm_kappa",
            "FSN2721_1_E_norm_source_charge",
            "NEXT2721_0_selected",
            "VAL2721_OVERALL",
        ],
        "use": "direct handoff selecting the Poisson/Gauss Newton coefficient bridge",
    },
    {
        "source_id": "SRC2722_1_2466",
        "label": "2466 Hilbert source and no orbital GM",
        "path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
        "needles": [
            "CUR2466_A_Hilbert_energy_current",
            "WT2466_1_mass_readout",
            "WT2466_4_no_orbital_GM",
            "PV2466_2_Newton_source",
        ],
        "use": "source mass must come from Hilbert/worldtube current before orbital readout",
    },
    {
        "source_id": "SRC2722_2_2468",
        "label": "2468 stationary Hilbert worldtube theorem",
        "path": ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
        "needles": [
            "EXT2468_3_surface_mass",
            "DYN2468_1_exchange_required",
            "GATE2468_0_stationary_q_zero",
            "VAL2468_OVERALL",
        ],
        "use": "conditional surface-independent source mass and dynamic exchange blocker",
    },
    {
        "source_id": "SRC2722_3_2469",
        "label": "2469 parent metric equation and stress blocker",
        "path": ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md",
        "needles": [
            "MET2469_0_parent_metric_equation",
            "MET2469_2_stealth_reduction",
            "MET2469_3_current_corpus",
            "PPN2469_0_residual_source",
            "VAL2469_OVERALL",
        ],
        "use": "metric equation only reduces to GR/Newton if extra stress is silent or retained",
    },
    {
        "source_id": "SRC2722_4_2470",
        "label": "2470 GK no-hair and stress-bound fallback",
        "path": ROOT / "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
        "needles": [
            "NH2470_5_stress_zero",
            "BND2470_2_metric_bound",
            "MET2470_0_if_nohair",
            "VAL2470_OVERALL",
        ],
        "use": "extra stress silence remains conditional; finite stress-to-metric bound is fallback",
    },
    {
        "source_id": "SRC2722_5_2208",
        "label": "2208 PPN source normalization",
        "path": ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md",
        "needles": [
            "PPNL2208_0_operator_factorization",
            "PPNL2208_3_source_normalization",
            "measured-GM no-absorption rule",
            "VAL2208_OVERALL",
        ],
        "use": "PPN coefficients require fixed source normalization and residual stress map",
    },
    {
        "source_id": "SRC2722_6_2478",
        "label": "2478 metric Green/source residual",
        "path": ROOT / "2478-Y5-R2FR-residual-source-norm-and-Green-bound-certificate.md",
        "needles": [
            "RES2478_0_definition",
            "CMET2478_0_formal_metric_bound",
            "BLK2478_3_source_normalization",
            "VAL2478_OVERALL",
        ],
        "use": "finite residual metric-bound path if Newton bridge remains unsourced",
    },
    {
        "source_id": "SRC2722_7_2479",
        "label": "2479 C_norm/C_shadow coefficient blocker",
        "path": ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md",
        "needles": [
            "COEF2479_C_norm",
            "COEF2479_C_shadow",
            "CRES2479_0_current_formula",
            "GATE2479_5_no_shortcuts",
            "VAL2479_OVERALL",
        ],
        "use": "normalization and shadow coefficients are still symbolic blockers",
    },
    {
        "source_id": "SRC2722_8_1339",
        "label": "1339 EH-left-hand and Newton transfer gate",
        "path": ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
        "needles": [
            "EHGate1339_6_source_GM_transfer",
            "LOV1339_1_weak_field_algebra",
            "NEW1339_2_GM_calibration",
            "VAL1339_8_shortcuts_enforced",
        ],
        "use": "Poisson-looking algebra is not Newton until source-to-GM transfer is derived",
    },
    {
        "source_id": "SRC2722_9_1009",
        "label": "1009 EH core and worldtube glue contract",
        "path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": [
            "PCS1009_0_EH_core",
            "PCS1009_8_worldtube_source_glue",
            "SVR1009_0_EH_anchor_only",
            "SVR1009_4_worldtube_glue_conditional",
        ],
        "use": "EH core cannot be treated as total parent action without sector/source certificates",
    },
    {
        "source_id": "SRC2722_10_1006",
        "label": "1006 anti-circular Poisson/Gauss warning",
        "path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": [
            "MHA1006_5_anti_circularity",
            "MHS1006_2_anti_circularity",
            "CG1006_1_orbital_GM_substitution",
            "V1006_9_MHref_gate_written",
        ],
        "use": "orbital GM cannot fill source denominator before Poisson/Gauss bridge",
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


def poisson_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PG2722_0_metric_equation",
            "target": "parent metric equation has EH weak-field coefficient",
            "attempt": "start from G_{mu nu}+Lambda g_{mu nu}=kappa0 T_Hilbert_{mu nu}+residual_stress",
            "verdict": "CONDITIONAL_STANDARD_FORM",
            "reason": "2469 and 1339 allow the EH/GR-looking bridge only when extra-sector stress and EH-left-hand premises are signed",
            "claim_allowed": False,
            "next_requirement": "parent kappa0/G_ref ownership and stress-silence/bound certificate",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PG2722_1_weak_field_coefficient",
            "target": "derive Newtonian Poisson coefficient",
            "attempt": "use g_00=-(1+2Phi/c^2), T_00≈rho_H c^2 and G_00^lin≈2 nabla^2 Phi/c^2",
            "verdict": "ALGEBRA_DERIVED_CONDITIONAL",
            "reason": "the algebra gives nabla^2 Phi=(kappa0 c^4/2) rho_H, hence G_N=kappa0 c^4/(8*pi), only if the weak-field/gauge/source assumptions hold",
            "claim_allowed": False,
            "next_requirement": "fix kappa0 and gauge/domain convention before tests",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PG2722_2_gauss_flux",
            "target": "same source gives exterior inverse-square law",
            "attempt": "integrate Poisson equation over a linking volume and use Gauss theorem",
            "verdict": "CONDITIONAL_GAUSS_TRANSFER",
            "reason": "gives surface flux 4*pi*G_N*M_source only if M_source is the Hilbert/worldtube source and boundary/falloff terms are controlled",
            "claim_allowed": False,
            "next_requirement": "worldtube surface theorem or finite surface-drift row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PG2722_3_orbital_readout",
            "target": "connect parent mu=G_N M_source to measured orbital GM",
            "attempt": "treat GM_orbit as downstream readout of parent mu",
            "verdict": "DOWNSTREAM_ONLY_NOT_INPUT",
            "reason": "1006/2466/2721 forbid using observed orbital GM to define the source or coupling; it can only test the derived mu",
            "claim_allowed": False,
            "next_requirement": "orbit/readout map and residual vector after parent mu is fixed",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PG2722_4_extra_stress",
            "target": "Newton bridge not spoiled by MTS stress",
            "attempt": "set residual_stress=0 in local stationary exterior",
            "verdict": "STRESS_SILENCE_UNSIGNED",
            "reason": "2470 gives the no-hair route but not the proof; finite stress metric bounds remain fallback",
            "claim_allowed": False,
            "next_requirement": "stress no-hair/positivity or finite residual stress-to-Phi row",
            "timestamp_utc": ts(),
        },
        {
            "audit_id": "PG2722_5_verdict",
            "target": "Newton coefficient bridge",
            "attempt": "combine EH coefficient, Hilbert source, Gauss flux, no-absorption and stress silence",
            "verdict": "NEWTON_COEFFICIENT_THEOREM_CONDITIONAL_NOT_CLAIMED",
            "reason": "the algebraic bridge is clean, but parent kappa0/G_ref ownership, stress silence, boundary/gauge and orbital readout are not signed",
            "claim_allowed": False,
            "next_requirement": "kappa0-G_ref parent ownership or finite E_Newton coefficient rows",
            "timestamp_utc": ts(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2722_0_statement",
            "statement": "If the parent local metric equation reduces in a stationary weak-field source collar to G_{mu nu}^{lin}=kappa0 T_Hilbert_{mu nu}, with g_00=-(1+2Phi/c^2), T_00≈rho_H c^2, controlled gauge/domain terms, no extra stress, and parent Hilbert source M_source, then nabla^2 Phi=4*pi*G_N*rho_H with G_N=kappa0*c^4/(8*pi), and the exterior Gauss flux gives mu_parent=G_N*M_source.",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_clause": "parent kappa0/G_ref convention; EH-left-hand premises; stress silence; gauge/domain/falloff; same-frame Hilbert source; orbital readout map",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2722_1_linearized_00",
            "statement": "Using the stated weak-field convention, G_00^{lin}≈2*nabla^2 Phi/c^2 and T_00≈rho_H c^2 imply nabla^2 Phi=(kappa0*c^4/2)*rho_H.",
            "status": "ALGEBRA_DERIVED_CONDITIONAL",
            "missing_clause": "weak-field gauge convention and parent EH-left-hand ownership",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2722_2_newton_constant",
            "statement": "Matching nabla^2 Phi=(kappa0*c^4/2)*rho_H to nabla^2 Phi=4*pi*G_N*rho_H gives G_N=kappa0*c^4/(8*pi).",
            "status": "COEFFICIENT_MAP_DERIVED_CONDITIONAL",
            "missing_clause": "kappa0 must be parent-fixed before local tests and not backfilled from observed GM",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2722_3_gauss_transfer",
            "statement": "Integrating over a source-linking volume gives integral_boundary grad(Phi).n dS=4*pi*G_N*M_source plus explicit boundary/support/stress residuals.",
            "status": "GAUSS_FORM_DERIVED_CONDITIONAL",
            "missing_clause": "falloff/domain package, surface-independent M_source, and residual-stress flux bounds",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
        {
            "theorem_id": "THM2722_4_orbit_not_input",
            "statement": "The observed orbital GM is a comparison to mu_parent=G_N*M_source after the theorem, never an input to define G_N or M_source.",
            "status": "ANTI_CIRCULAR_PROTOCOL_EXACT",
            "missing_clause": "downstream orbital/readout residual protocol",
            "claim_allowed": False,
            "timestamp_utc": ts(),
        },
    ]


def coefficient_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "CMAP2722_0_metric_coupling",
            "input": "kappa0",
            "derived_quantity": "G_N",
            "formula": "G_N = kappa0*c^4/(8*pi)",
            "status": "CONDITIONAL_MAP_NOT_SOURCE",
            "missing": "parent-fixed kappa0/G_ref convention",
            "valid_for_claim": False,
        },
        {
            "map_id": "CMAP2722_1_source_density",
            "input": "T_00≈rho_H*c^2",
            "derived_quantity": "rho_H",
            "formula": "rho_H = T_00/c^2 in the local observed coframe",
            "status": "CONDITIONAL_SOURCE_READOUT",
            "missing": "same-frame Hilbert matter descent and tau/coframe lock",
            "valid_for_claim": False,
        },
        {
            "map_id": "CMAP2722_2_poisson",
            "input": "G_00^lin=kappa0*T_00",
            "derived_quantity": "nabla^2 Phi",
            "formula": "nabla^2 Phi = 4*pi*G_N*rho_H + residual_Phi",
            "status": "CONDITIONAL_WEAK_FIELD_FORM",
            "missing": "gauge/domain/residual-stress package",
            "valid_for_claim": False,
        },
        {
            "map_id": "CMAP2722_3_gauss",
            "input": "Poisson equation plus boundary/falloff",
            "derived_quantity": "mu_parent",
            "formula": "mu_parent = G_N*M_source",
            "status": "CONDITIONAL_GAUSS_FORM",
            "missing": "surface-independent M_source and boundary flux control",
            "valid_for_claim": False,
        },
        {
            "map_id": "CMAP2722_4_orbital_comparison",
            "input": "mu_parent",
            "derived_quantity": "Delta_mu_orbit",
            "formula": "Delta_mu_orbit = (GM_orbit - mu_parent)/mu_parent",
            "status": "DOWNSTREAM_TEST_ONLY",
            "missing": "orbital/readout protocol after mu_parent is fixed",
            "valid_for_claim": False,
        },
    ]


def finite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FPG2722_0_E_kappa_bridge",
            "quantity": "E_kappa_bridge",
            "definition": "E_kappa_bridge := |G_ref - kappa0*c^4/(8*pi)|/G_ref",
            "feeds": "E_norm_kappa and Newton coefficient gate",
            "source_path": str(ROOT / "2721-Y5-R2FR-source-normalization-no-fitted-GM-or-finite-EJeff-vector-under-AX1090-closure.md"),
            "units_need": "dimensionless coupling mismatch; kappa0 units compatible with G_ref/c^4",
            "missing": "parent source for kappa0; fixed G_ref convention; source path",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FPG2722_1_E_Poisson_residual",
            "quantity": "E_Poisson_residual",
            "definition": "E_Poisson_residual := ||nabla^2 Phi - 4*pi*G_ref*rho_H||/||4*pi*G_ref*rho_H||",
            "feeds": "E_norm and weak-field residual vector",
            "source_path": str(ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"),
            "units_need": "dimensionless Poisson residual in declared weak-field gauge",
            "missing": "Phi definition; gauge/domain; rho_H source row; residual-stress subtraction",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FPG2722_2_E_Gauss_flux",
            "quantity": "E_Gauss_flux",
            "definition": "E_Gauss_flux := |integral_boundary grad(Phi).n dS - 4*pi*G_ref*M_source|/(4*pi*G_ref*M_source)",
            "feeds": "E_norm_source_charge and source/Gauss gate",
            "source_path": str(ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md"),
            "units_need": "dimensionless flux mismatch over declared linking surface",
            "missing": "surface-independent M_source; boundary/falloff; dynamic exchange or stationary restriction",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FPG2722_3_E_mu_transfer",
            "quantity": "E_mu_transfer",
            "definition": "E_mu_transfer := |GM_orbit - G_ref*M_source|/(G_ref*M_source) as downstream comparison only",
            "feeds": "orbital/readout residual after Newton coefficient is fixed",
            "source_path": str(ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
            "units_need": "dimensionless orbital calibration mismatch",
            "missing": "orbit/readout model; parent mu fixed first; no observed-GM input certificate",
            "status": "DOWNSTREAM_ONLY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FPG2722_4_E_extra_stress_Newton",
            "quantity": "E_extra_stress_Newton",
            "definition": "E_extra_stress_Newton := ||T_GK + T_tau/P + boundary||_00/||T_Hilbert||_00",
            "feeds": "E_norm_extra_stress and local metric residual",
            "source_path": str(ROOT / "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md"),
            "units_need": "dimensionless stress residual in same weak-field/source norm",
            "missing": "GK no-hair/positivity or finite stress norm; boundary term convention",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FPG2722_5_E_gauge_domain",
            "quantity": "E_gauge_domain",
            "definition": "E_gauge_domain := C_gauge*||gauge/domain/falloff correction to G_00^lin - 2*nabla^2 Phi/c^2||",
            "feeds": "Poisson residual and PPN/local-GR gate",
            "source_path": str(ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md"),
            "units_need": "dimensionless weak-field operator residual",
            "missing": "weak-field gauge; domain boundary conditions; inverse-divergence convention",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "FPG2722_6_E_shadow_source",
            "quantity": "E_shadow_source",
            "definition": "E_shadow_source := ||J_shadow_00||/(||T_Hilbert||_00) after common source normalization",
            "feeds": "E_shadow and WEP/source-normalization branch",
            "source_path": str(ROOT / "2479-Y5-R2FR-residual-sector-to-EGK-norm-map-or-coefficient-blocker.md"),
            "units_need": "dimensionless non-Hilbert source fraction",
            "missing": "universal coupling/source-shadow zero theorem or source-backed bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2722_0_previous",
            "formula": "E_norm := E_norm_kappa + E_norm_source_charge + E_norm_surface_drift + E_norm_reference + E_norm_absorption + E_norm_extra_stress",
            "status": "INHERITED_FROM_2721",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2722_1_newton_split",
            "formula": "E_Newton_bridge := E_kappa_bridge + E_Poisson_residual + E_Gauss_flux + E_mu_transfer + E_extra_stress_Newton + E_gauge_domain",
            "status": "REFINED_NONCLAIM_VECTOR",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2722_2_source_shadow",
            "formula": "E_shadow retains E_shadow_source unless all source currents reduce to Hilbert stress",
            "status": "REFINED_NONCLAIM_VECTOR",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2722_3_green_feed",
            "formula": "||R_AB|| <= ||G_R||*(E_matter + E_boundary_hair + E_readout + E_shadow + E_norm + E_Newton_bridge)",
            "status": "FORMAL_GREEN_INTERFACE_ONLY",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2722_4_zero_condition",
            "formula": "E_Newton_bridge=0 only if kappa/G_ref, Poisson algebra, Gauss flux, orbit readout, extra stress and gauge/domain clauses all close",
            "status": "ZERO_CONDITION_NOT_MET",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2722_0_coefficient_map",
            "claim": "G_N=kappa0*c^4/(8*pi) is parent-owned",
            "status": "BLOCKED",
            "required_before_claim": "kappa0/G_ref parent convention and units source",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2722_1_Poisson",
            "claim": "Poisson equation is derived for MTS local branch",
            "status": "BLOCKED",
            "required_before_claim": "EH-left-hand premises, weak-field gauge, Hilbert source and stress residual control",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2722_2_Gauss_orbit",
            "claim": "parent source produces measured inverse-square orbital GM",
            "status": "BLOCKED",
            "required_before_claim": "Gauss surface theorem, falloff, orbit/readout map and no observed-GM input",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2722_3_local_GR_PPN",
            "claim": "local GR/PPN branch passes",
            "status": "BLOCKED",
            "required_before_claim": "Newton bridge plus PPN residual vector and all E_Jeff components zero/bounded",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2722_4_public",
            "claim": "public/GitHub output",
            "status": "NOT_REQUESTED_BLOCKED_BY_PRIVATE_SCOPE",
            "required_before_claim": "explicit user request and public-safe claim audit",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2722_0_kappa_parent",
            "missing_item": "parent-fixed kappa0/G_ref convention",
            "effect": "coefficient map is algebra, not a derived physical Newton constant",
            "best_next_attack": "sign kappa0/G_ref from parent EH/weak-field action or keep E_kappa_bridge finite",
            "claim_blocked": "Newton coefficient",
        },
        {
            "blocker_id": "BLK2722_1_EH_left",
            "missing_item": "metric-only EH-left-hand premises",
            "effect": "G_00^lin≈2*nabla^2 Phi/c^2 may not be the actual MTS local operator",
            "best_next_attack": "derive weak-field operator/gauge/domain package",
            "claim_blocked": "Poisson bridge",
        },
        {
            "blocker_id": "BLK2722_2_stress",
            "missing_item": "extra-sector stress silence or finite stress norm",
            "effect": "Poisson equation receives non-Hilbert source terms",
            "best_next_attack": "GK no-hair/positivity or E_extra_stress_Newton row",
            "claim_blocked": "local GR and PPN",
        },
        {
            "blocker_id": "BLK2722_3_gauss_boundary",
            "missing_item": "boundary/falloff/domain package",
            "effect": "Poisson algebra does not yet imply exterior 1/r inverse-square law",
            "best_next_attack": "surface flux theorem or finite E_Gauss_flux row",
            "claim_blocked": "Newtonian mechanics",
        },
        {
            "blocker_id": "BLK2722_4_orbit_readout",
            "missing_item": "downstream orbital/readout residual map",
            "effect": "parent mu cannot yet be compared cleanly to measured orbital GM",
            "best_next_attack": "derive orbit readout only after parent mu is fixed",
            "claim_blocked": "measured-GM transfer",
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2722_0_accept_conditional_algebra",
            "decision": "record the standard weak-field coefficient map",
            "rationale": "under EH and Hilbert-source hypotheses the Newton coefficient is not mysterious: G_N=kappa0*c^4/(8*pi)",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2722_1_no_Newton_claim",
            "decision": "do not claim Newtonian mechanics reduction",
            "rationale": "kappa0 ownership, stress silence, boundary/Gauss and orbital readout are not signed",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2722_2_finite_rows",
            "decision": "install Newton-bridge finite residual rows",
            "rationale": "if the bridge is not fully derived, every failure mode needs a named residual row",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2722_3_next",
            "decision": "move next to kappa0/G_ref parent ownership",
            "rationale": "the algebra is now clear; the next decisive gap is whether the coupling is parent-owned rather than fitted",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2722_0_selected",
            "status": "selected_primary",
            "target_doc": "2723-Y5-R2FR-kappa0-Gref-parent-ownership-or-Newton-coefficient-row-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_kappa0_Gref_parent_ownership_or_Newton_coefficient_row_under_AX1090_closure_2723.py",
            "mission": "prove kappa0/G_ref is fixed by the parent weak-field action before tests, or keep E_kappa_bridge as a source-ready nonclaim row",
            "acceptance": "parent-owned coupling convention with units and source path, or a blocker ledger refusing Newton coefficient promotion",
            "forbidden": "set G_ref from observed orbital GM; claim Newton/local GR/PPN; hide extra stress; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2722_0_status",
            "sector": "Newton bridge",
            "state": "conditional Poisson/Gauss algebra is now explicit, but no Newton claim is opened",
            "confidence": "mathematically standard under stated hypotheses",
            "next_need": "parent-owned kappa0/G_ref and stress/gauge certificates",
        },
        {
            "snapshot_id": "SNAP2722_1_best_route",
            "sector": "derivation",
            "state": "derive G_N from kappa0 and Hilbert source before orbital GM is used",
            "confidence": "high as anti-circular route",
            "next_need": "coupling ownership, then Gauss/exterior readout",
        },
        {
            "snapshot_id": "SNAP2722_2_risk",
            "sector": "claim risk",
            "state": "Poisson-looking algebra can still fail as Newtonian mechanics if source-GM transfer or extra-stress silence fails",
            "confidence": "high blocker visibility",
            "next_need": "E_kappa_bridge, E_Gauss_flux and E_extra_stress_Newton closure",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2722_0_local_bounds",
            "source_table": OUTPUTS["finite_rows"].name,
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "quarantine Poisson/Gauss Newton residual rows as nonclaim",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2722_1_source_weight",
            "source_table": OUTPUTS["ejeff_update"].name,
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "quarantine Newton coefficient/E_Jeff update vector as nonclaim",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2722_2_next_queue",
            "source_table": OUTPUTS["next_target"].name,
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queue 2723 without touching formalization-workbench",
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
    coeff_rows: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_kappa_bridge",
        "E_Poisson_residual",
        "E_Gauss_flux",
        "E_mu_transfer",
        "E_extra_stress_Newton",
        "E_gauge_domain",
        "E_shadow_source",
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
    coeff_nonclaim = all(row["valid_for_claim"] is False for row in coeff_rows)
    finite_nonclaim = (
        {row["quantity"] for row in finite} == required_quantities
        and all(row["valid_for_claim"] is False for row in finite)
    )
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {
            "validation_id": "VAL2722_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_2_csv_parse",
            "passed": all(result[0] for result in parse_results),
            "detail": parse_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_3_theorem_nonclaim",
            "passed": theorem_nonclaim,
            "detail": "Newton coefficient theorem remains conditional and no Poisson/Gauss/Newton claim is promoted",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_4_coefficient_map_nonclaim",
            "passed": coeff_nonclaim,
            "detail": "coefficient map derives G_N=kappa0*c^4/(8*pi) only conditionally",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_5_finite_rows_complete_nonclaim",
            "passed": finite_nonclaim,
            "detail": "finite rows include kappa,Poisson,Gauss,mu,extra-stress,gauge,shadow components and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_6_ejeff_update_nonclaim",
            "passed": ejeff_nonclaim,
            "detail": "Newton bridge/E_Jeff update vector remains formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_7_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no Newton/Poisson/Gauss/PPN/local-GR/public claim gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_8_branch_copies",
            "passed": branch_paths_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_9_no_formalization_recent_changes",
            "passed": formalization_recent_changed_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2722_10_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2722_OVERALL",
            "passed": overall,
            "detail": "2722 derives the conditional Poisson/Gauss coefficient map, keeps Newton nonclaim, installs finite Newton bridge rows, and selects kappa0/G_ref ownership next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2722 - Y5/R2FR Poisson-Gauss Newton Coefficient Bridge Or E_norm Bound Under AX1090 Closure

## Private Verdict

2722 gets a real piece of the Newton bridge onto paper. Under the standard weak-field EH/Hilbert-source hypotheses, the coefficient map is clean:

`G_N = kappa0*c^4/(8*pi)`.

That means the route is not “fit `GM` and call it Newton.” The route is: parent metric coefficient `kappa0` plus parent Hilbert source `M_source` gives a Poisson/Gauss law; only after that may orbital `GM` be used as a downstream comparison.

But this is still **not** a Newton/GR claim. The bridge is conditional because the corpus has not parent-signed `kappa0/G_ref`, the EH-left-hand premises, the weak-field gauge/domain package, extra-sector stress silence, or the orbital/readout map. So the result is a strong conditional derivation shape plus finite nonclaim rows, not a pass.

## Claim Ceiling

- No Newtonian mechanics, local-GR/Newton, R10, PPN, clock, orbital, WEP, or public/GitHub claim is opened.
- Observed orbital `GM` remains downstream only; it cannot define `G_ref`, `kappa0`, `M_source`, or any denominator.
- Poisson/Gauss rows are source-ready schemas only and remain `valid_for_claim=false`.
- No `formalization-workbench` edits are allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## Poisson-Gauss Bridge Audit

{markdown_table(rows["poisson_audit"], ["audit_id", "target", "attempt", "verdict", "reason", "claim_allowed", "next_requirement"])}

## Conditional Theorem Attempt

{markdown_table(rows["theorem_attempt"], ["theorem_id", "statement", "status", "missing_clause", "claim_allowed"])}

## Coefficient Map

{markdown_table(rows["coefficient_map"], ["map_id", "input", "derived_quantity", "formula", "status", "missing", "valid_for_claim"])}

## Finite Newton Bridge Rows

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

This is a proper little win, but it is not the finish line. We now have the exact boxing combination for Newton: `kappa0` throws the jab, Hilbert source throws the cross, Gauss theorem turns it into inverse-square motion. The missing thing is whether MTS owns `kappa0/G_ref` and the local metric operator before any data fit. That is the next gate. No more circling: 2723 should go straight at coupling ownership.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    poisson_rows = poisson_audit_rows()
    theorem_rows = theorem_attempt_rows()
    coeff = coefficient_map_rows()
    finite = finite_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "poisson_audit": poisson_rows,
        "theorem_attempt": theorem_rows,
        "coefficient_map": coeff,
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
            "validation_id": "VAL2722_PRE_DOC",
            "passed": False,
            "detail": "pre-document placeholder",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(data)

    validation = validation_rows(source_rows, theorem_rows, coeff, finite, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2722 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
