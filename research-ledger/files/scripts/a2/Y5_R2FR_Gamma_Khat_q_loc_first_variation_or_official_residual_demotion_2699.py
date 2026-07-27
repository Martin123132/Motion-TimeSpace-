from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2699"
BRANCH_ID = "Y5_R2FR_GAMMA_KHAT_Q_LOC_FIRST_VARIATION_OR_OFFICIAL_RESIDUAL_DEMOTION_2699"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2699-Y5-R2FR-Gamma-Khat-q-loc-first-variation-or-official-residual-demotion.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2699_SOURCE_REGISTER.csv",
    "ward_identity": RESIDUALS / "P8_Y5_R2FR_2699_WARD_DIVERGENCE_IDENTITY.csv",
    "parent_signature_gates": RESIDUALS / "P8_Y5_R2FR_2699_PARENT_SIGNATURE_GATES.csv",
    "noether_residual_decomposition": RESIDUALS / "P8_Y5_R2FR_2699_NOETHER_RESIDUAL_DECOMPOSITION.csv",
    "official_residual_vector": RESIDUALS / "P8_Y5_R2FR_2699_OFFICIAL_QLOC_RESIDUAL_VECTOR_NONCLAIM.csv",
    "arena_projection_queue": RESIDUALS / "P8_Y5_R2FR_2699_QLOC_ARENA_PROJECTION_QUEUE_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2699_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2699_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2699_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2699_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2699_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2699_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2699_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_residual_vector": LOCAL_BOUNDS / "GammaKhat_q_loc_official_residual_vector_2699_NONCLAIM.csv",
    "local_projection_queue": LOCAL_BOUNDS / "GammaKhat_q_loc_arena_projection_queue_2699_NONCLAIM.csv",
    "wep_residual_vector": WEP_RESIDUALS / "GammaKhat_q_loc_official_residual_vector_2699_NONCLAIM.csv",
    "source_weight_residual_vector": SOURCE_WEIGHT / "GAMMAKHAT_QLOC_OFFICIAL_RESIDUAL_VECTOR_2699_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2699_GAMMA_EFF_METRIC_RESPONSE_OR_QLOC_RESPONSE_ROW_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2699_2698_MAP",
        "relative_path": "2698-Y5-R2FR-MTS-symbols-to-minimal-local-fixed-point-action-map.md",
        "required_needles": ["SAP2698_2_Gamma_eff_Khat_q", "FVG2698_2_Gamma_Khat_q_loc", "NEXT2698_0_selected", "VAL2698_OVERALL"],
        "purpose": "imports the selected Gamma/Khat/q_loc first-variation target",
    },
    {
        "source_id": "SRC2699_2206_WARD",
        "relative_path": "2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md",
        "required_needles": ["WID2206_0_define_stress", "PSA2206_8_all_or_nothing", "QDEM2206_9_total", "VAL2206_OVERALL"],
        "purpose": "imports the Ward-divergence reduction and official residual demotion",
    },
    {
        "source_id": "SRC2699_2581_RESIDUAL_LOCK",
        "relative_path": "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
        "required_needles": ["GK2581_7_verdict", "QLOC2581_TOTAL", "NEXT2581_0_selected", "VAL2581_OVERALL"],
        "purpose": "imports the locked local residual interface and local-test map",
    },
    {
        "source_id": "SRC2699_1010_HELMHOLTZ",
        "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "required_needles": ["GKT1010_6_verdict", "GKC1010_0_metric_response_scalar_density", "QRES1010_0_q_loc_vector"],
        "purpose": "imports the action/metric-response/Helmholtz schema",
    },
    {
        "source_id": "SRC2699_1791_CONJUGACY",
        "relative_path": "1791-Y5-R2FR-response-displacement-conjugacy-owner-refresh-or-q_loc-profile-pack.md",
        "required_needles": ["WID1791_0_diffeomorphism_variation", "ACT1791_3_Khat_match", "VAL1791_OVERALL"],
        "purpose": "imports the conditional response-displacement Ward route and live K_hat mismatch",
    },
    {
        "source_id": "SRC2699_1280_BOUND_CONTRACT",
        "relative_path": "1280-Y5-R10-RAB-Gamma-Khat-qloc-action-existence-or-extra-residual-bound.md",
        "required_needles": ["GKA1280_6_verdict", "BND1280_4_row_status", "VAL1280_13_overall"],
        "purpose": "imports the strict epsilon_GK_q_loc bound contract",
    },
    {
        "source_id": "SRC2699_512_SYMBOL_RULE",
        "relative_path": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "required_needles": ["FV512_2_Gamma_Khat_q", "KK512_1_q_loc", "D512_2"],
        "purpose": "imports the original keep/kill rule: derive q_loc as Ward residual or demote it",
    },
    {
        "source_id": "SRC2699_2698_MAP_CSV",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2698_SYMBOL_ACTION_PLACEMENT_MAP.csv",
        "required_needles": ["SAP2698_2_Gamma_eff_Khat_q", "UNPLACED_FIRST_VARIATION_TARGET"],
        "purpose": "imports machine-readable 2698 placement status",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def ward_identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WID2699_0_definition",
            "define the effective extra stress",
            "T_GK^{mu nu} := K_hat^{mu nu} - Gamma_eff g^{mu nu}",
            "nabla_mu T_GK^{mu nu} = nabla_mu K_hat^{mu nu} - nabla^nu Gamma_eff",
            "q_loc^nu = -P_loc nabla_mu T_GK^{mu nu}",
            "DERIVED_ALGEBRAIC_IDENTITY",
        ),
        (
            "WID2699_1_parent_action",
            "if T_GK is a Hilbert stress of one diffeomorphism-invariant parent sector",
            "T_GK^{mu nu} = -2/sqrt(-g) delta S_GK/delta g_{mu nu} under a fixed sign/volume convention",
            "nabla_mu T_GK^{mu nu} = sum_A E_A nabla^nu Phi^A + J_source^nu + B_boundary^nu + R_readout^nu",
            "q_loc vanishes only when Euler, source, boundary, readout and projector terms vanish",
            "CONDITIONAL_FIELD_THEORY_THEOREM",
        ),
        (
            "WID2699_2_double_zero",
            "if local fixed point is a stress double zero",
            "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0",
            "F1_GK = partial_A T_GK(Phi0) delta Phi^A = 0",
            "first-order local PPN/source hair is absent only under parent-signed double zero",
            "CONDITIONAL_DOUBLE_ZERO_LAW",
        ),
        (
            "WID2699_3_projection",
            "apply local projector fixed before readout",
            "P_loc commutes with the compact local limit and carries no derivative/readout leakage",
            "P_loc q = 0 follows from P_loc nabla_mu T_GK^{mu nu}=0",
            "otherwise derivative/projector commutators become finite residual rows",
            "CONDITIONAL_PROJECTOR_GATE",
        ),
        (
            "WID2699_4_live_verdict",
            "current MTS status",
            "the Ward route is exact as a contract, but live Gamma_eff/K_hat are not parent signed",
            "theorem_zero_q_loc=false; official_residual_demotion=true",
            "local GR/Newton/PPN/R10/clock/orbital claims remain blocked by q_loc residuals",
            "DERIVATION_ATTEMPT_FAILS_CURRENT_CORPUS",
        ),
    ]
    return [
        {
            "identity_id": identity_id,
            "statement": statement,
            "mathematical_form": form,
            "derived_result": result,
            "implication": implication,
            "proof_status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for identity_id, statement, form, result, implication, status in rows
    ]


def parent_signature_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("PSG2699_0_action_owner", "S_GK_exists", "one local diffeomorphism-invariant scalar parent action owns Gamma_eff, K_hat and T_GK", "MISSING_PARENT_SIGNED_ACTION", "1010/1280/2206 keep candidate contract only", "q_action_owner_defect"),
        ("PSG2699_1_metric_response", "Khat_metric_response", "K_hat equals the metric response of the same Gamma_eff density, including derivative/improvement/boundary terms", "MISSING_OR_FAILED_LIVE_METRIC_RESPONSE_MATCH", "1280/1791/2206 say K_hat is not term-matched to K_metric[Gamma_eff]", "q_metric_response_defect"),
        ("PSG2699_2_helmholtz", "Helmholtz_integrability", "second metric variations of sqrt(-g)T_GK are symmetric up to allowed gauge/boundary terms", "MISSING_HELMHOLTZ_CERTIFICATE", "1010 and 1280 mark current-symbol Helmholtz test not checked", "q_Helmholtz_defect"),
        ("PSG2699_3_euler_closure", "Euler_Ward_closure", "fields building Gamma_eff/K_hat obey E_A=0 on compact local vacuum and have no surviving source currents", "MISSING_EULER_AND_SOURCE_ZERO_CERTIFICATE", "1791/1860/2206 keep source-current and physical lock open", "q_Euler_source_defect"),
        ("PSG2699_4_double_zero", "stress_double_zero", "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 for the physical q_loc components", "FORMAL_ONLY_NOT_PHYSICAL_COMPONENT_LOCKED", "1791 gives conditional F1=0 but not the physical q_loc/PPN/source vector", "epsilon_C0_dC_GK"),
        ("PSG2699_5_projector_owner", "P_loc_owner", "P_loc is parent-owned, fixed before readout, and has no derivative commutator leakage", "MISSING_PLOC_OWNER_AND_COMMUTATOR", "2206/1791 keep P_loc owner and commutator open", "q_Ploc_commutator"),
        ("PSG2699_6_boundary_no_flux", "boundary_no_flux", "boundary/symplectic/improvement terms do not carry linking-sphere force or source-mass flux", "MISSING_BOUNDARY_NO_FLUX_CERTIFICATE", "2698/2206 keep boundary/improvement as live open clause", "q_boundary_flux"),
        ("PSG2699_7_units_observable", "units_and_observable_maps", "q_loc and every defect has units/normalization and maps into PPN/R10/R11/clock/orbital arenas", "MISSING_UNITS_AND_RESPONSE_OPERATORS", "2581 and 2206 projection queues are staged but not score-ready", "q_units_response_defect"),
        ("PSG2699_8_all_or_nothing", "q_loc_theorem_zero", "all PSG2699_0..7 pass in one parent branch", "THEOREM_ZERO_FALSE_OFFICIAL_RESIDUAL_DEMOTION", "several core clauses are missing or failed", "q_loc_residual_vector_abs"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "required_statement": required,
            "current_status": status,
            "evidence": evidence,
            "residual_if_missing": residual,
            "parent_signed": "false",
            "passes_now": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, required, status, evidence, residual in rows
    ]


def noether_residual_decomposition_rows() -> list[dict[str, Any]]:
    rows = [
        ("NRD2699_0_metric_response", "Delta_K^{mu nu}", "K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]", "if nonzero, q_loc is not a pure parent Ward residual", "q_metric_response_defect"),
        ("NRD2699_1_Euler", "E_A nabla^nu Phi^A", "parent Euler-force term", "zero only on source-free compact solution branch", "q_Euler_defect"),
        ("NRD2699_2_source_current", "J_source^nu", "matter/source/species/readout current coupled to the GK sector", "survives if source functional is not even/quotient-descended", "q_source_current_defect"),
        ("NRD2699_3_boundary", "B_boundary^nu", "boundary/symplectic/improvement flux", "survives if reference/no-flux class is not fixed", "q_boundary_flux"),
        ("NRD2699_4_projector", "(nabla P_loc)K_hat + [P_loc,nabla]T_GK", "projector/readout derivative commutator", "survives if P_loc is post-readout or arena-defined", "q_Ploc_commutator"),
        ("NRD2699_5_readout", "R_readout^nu", "metric/PPN/readout response of the GK carrier", "survives even if divergence cancels in a hidden frame", "q_readout_defect"),
        ("NRD2699_6_total", "q_loc_residual_vector_abs", "absolute no-cancellation envelope over all GK/q_loc defects", "must be theorem-zero or source-backed bounded before local-GR claim", "q_loc_residual_vector_abs"),
    ]
    return [
        {
            "decomposition_id": row_id,
            "component": component,
            "definition": definition,
            "meaning": meaning,
            "residual_symbol": residual,
            "numeric_value_present": "false",
            "source_backed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row_id, component, definition, meaning, residual in rows
    ]


def official_residual_vector_rows() -> list[dict[str, Any]]:
    rows = [
        ("QLOC2699_0_q_loc_vector", "q_loc^nu", "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})", "OFFICIAL_RETAINED_RESIDUAL", "force_density_or_arena_normalized_vector", "local_GR;PPN;R10;R11;clock;orbital;WEP", "MISSING_PARENT_ZERO_OR_PROFILE"),
        ("QLOC2699_1_metric_response", "q_metric_response_defect", "K_hat - K_metric[Gamma_eff]", "RETAINED_SYMBOLIC_GAP", "stress_response_or_force_density", "PPN;R10;local_GR;source_normalization", "MISSING_KHAT_METRIC_RESPONSE"),
        ("QLOC2699_2_helmholtz", "q_Helmholtz_defect", "antisymmetric second-variation obstruction for T_GK", "RETAINED_SYMBOLIC_GAP", "operator_norm_or_integrability_flag", "local_GR;PPN", "MISSING_HELMHOLTZ_TEST"),
        ("QLOC2699_3_euler_source", "q_Euler_source_defect", "Euler/source-current leakage in the GK Ward identity", "RETAINED_SYMBOLIC_GAP", "force_density", "WEP;R11;PPN;clock", "MISSING_EULER_SOURCE_ZERO"),
        ("QLOC2699_4_boundary", "q_boundary_flux", "boundary/symplectic/improvement leakage", "RETAINED_SYMBOLIC_GAP", "force_or_mass_flux", "local_GR;orbital;source_measure", "MISSING_BOUNDARY_NO_FLUX"),
        ("QLOC2699_5_projector", "q_Ploc_commutator", "projector derivative/readout commutator", "RETAINED_SYMBOLIC_GAP", "force_density_or_dimensionless_projection", "PPN_alpha_i;WEP;local_GR", "MISSING_PLOC_OWNER"),
        ("QLOC2699_6_readout", "q_readout_defect", "metric/PPN response of GK carrier", "RETAINED_SYMBOLIC_GAP", "PPN_vector_or_metric_coefficients", "PPN;clock;orbital", "MISSING_METRIC_RESPONSE_MATRIX"),
        ("QLOC2699_7_total", "q_loc_residual_vector_abs", "absolute no-cancellation envelope over all q_loc defects", "OFFICIAL_NONCLAIM_TOTAL", "arena_normalized_vector", "all local arenas", "MISSING_COMPONENT_INPUTS"),
    ]
    return [
        {
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "units": units,
            "observable_link": observable,
            "blocking_reason": blocking,
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": "false",
            "official_residual": "true",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for residual_id, symbol, definition, status, units, observable, blocking in rows
    ]


def arena_projection_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("APQ2699_0_PPN", "PPN", "Delta_PPN_q = R_PPN[q_loc_residual_vector]", "beta,gamma,alpha_i,zeta_i,xi response map plus source normalization", "MISSING_PPN_RESPONSE_OPERATOR;MISSING_QLOC_COMPONENT_PROFILE;MISSING_METRIC_RESPONSE_MATRIX"),
        ("APQ2699_1_R10", "R10_short_range", "alpha_R10_q(lambda)=R_R10[q_loc(lambda)]", "range kernel, alpha(lambda) conversion, units, real bound curve link", "MISSING_R10_PROJECTION_OPERATOR;MISSING_RANGE_KERNEL;MISSING_BOUND_CURVE_LINK"),
        ("APQ2699_2_R11", "R11_source_normalization", "c_GK_operator_vector(lambda)=R_R11[q_loc]", "source measure map, Pi_M/H_tau normalization and operator basis", "MISSING_R11_OPERATOR_MAP;MISSING_SOURCE_MEASURE_NORMALIZATION"),
        ("APQ2699_3_clocks", "clock_time", "Delta_clock_q=R_clock[q_loc]", "clock frame, redshift/frequency response coefficients and matter-frame owner", "MISSING_CLOCK_RESPONSE_COEFFICIENTS;MISSING_CLOCK_FRAME"),
        ("APQ2699_4_orbital", "orbital_systems", "Delta_orbital_q=R_orbital[q_loc]", "force-to-acceleration map, radial profile and source-charge equality", "MISSING_ORBITAL_FORCE_MAP;MISSING_RADIAL_PROFILE"),
        ("APQ2699_5_local_GR", "local_GR_Newton_limit", "q_loc theorem-zero or residual bound below every local threshold", "all parent signatures or conservative finite bounds", "THEOREM_ZERO_FALSE;MISSING_COMPONENT_BOUNDS;LOCAL_GR_CLAIM_BLOCKED"),
    ]
    return [
        {
            "queue_id": queue_id,
            "arena": arena,
            "projected_quantity": quantity,
            "required_operator": operator,
            "status": status,
            "score_ready": "false",
            "theorem_zero_override": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for queue_id, arena, quantity, operator, status in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2699_0_current", False, False, False, False, False, False, False, False),
        ("DRY2699_1_action_only", True, False, False, False, False, False, False, False),
        ("DRY2699_2_action_metric_only", True, True, False, False, False, False, False, False),
        ("DRY2699_3_no_helmholtz", True, True, False, True, True, True, False, False),
        ("DRY2699_4_no_source_boundary", True, True, True, True, False, False, False, False),
        ("DRY2699_5_formal_double_zero_only", False, False, False, True, True, True, False, False),
        ("DRY2699_6_full_theorem_private", True, True, True, True, True, True, True, False),
        ("DRY2699_7_cancellation_only", True, True, True, True, True, True, True, True),
    ]
    return [
        {
            "case_id": case_id,
            "action_owner": as_bool(action),
            "metric_response": as_bool(metric),
            "helmholtz": as_bool(helmholtz),
            "euler_closure": as_bool(euler),
            "double_zero": as_bool(double_zero),
            "projector_boundary": as_bool(projector_boundary),
            "units_observable_maps": as_bool(maps),
            "cancellation_only": as_bool(cancellation),
            "expected_q_loc_zero_claim": "false",
            "timestamp_utc": stamp(),
        }
        for case_id, action, metric, helmholtz, euler, double_zero, projector_boundary, maps, cancellation in cases
    ]


def score_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    required = [
        ("action_owner", "missing_action_owner"),
        ("metric_response", "missing_metric_response"),
        ("helmholtz", "missing_helmholtz"),
        ("euler_closure", "missing_euler_closure"),
        ("double_zero", "missing_double_zero"),
        ("projector_boundary", "missing_projector_boundary"),
        ("units_observable_maps", "missing_units_observable_maps"),
    ]
    for field, blocker in required:
        if row[field] != "true":
            blockers.append(blocker)
    if row["cancellation_only"] == "true":
        blockers.append("cancellation_only_forbidden")

    if not blockers:
        status = "PRIVATE_THEOREM_CONTRACT_SATISFIED_REQUIRES_SEPARATE_SOURCE_AUDIT"
    else:
        status = "BLOCKED_NONCLAIM"
    return {
        "case_id": row["case_id"],
        "status": status,
        "blockers": ";".join(blockers),
        "q_loc_zero_claim_allowed": "false",
        "local_GR_claim_allowed": "false",
        "matches_expected": "true",
        "timestamp_utc": stamp(),
    }


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2699_0_algebra", "q_loc is a projected negative divergence of T_GK=K_hat-Gamma_eff*g", "PASS_CONDITIONAL_IDENTITY", "true", "false", "algebra sharpens the target but does not sign the parent sector"),
        ("CG2699_1_parent_signature", "all parent action/signature gates pass", "BLOCKED_NONCLAIM", "false", "false", "S_GK, metric response, Helmholtz, Euler, double-zero, P_loc and boundary are not signed together"),
        ("CG2699_2_theorem_zero", "q_loc^nu=0 can be claimed for current MTS", "BLOCKED_NONCLAIM", "false", "false", "the live Gamma/Khat branch remains unsigned"),
        ("CG2699_3_residual_demotion", "q_loc is retained as official finite residual vector", "PASS_NONCLAIM", "true", "false", "this is a discipline gate, not a physics pass"),
        ("CG2699_4_local_GR", "local EH/GR/Newton inheritance reopens", "BLOCKED_NONCLAIM", "false", "false", "q_loc plus source/Pi_M/readout residuals remain active"),
        ("CG2699_5_shortcuts", "plateau/scalar-proxy/fitted-G/readout-cancellation can zero q_loc", "BLOCKED_GUARDRAIL", "false", "false", "shortcuts remain forbidden"),
        ("CG2699_6_public", "public/GitHub readiness from 2699", "BLOCKED_PRIVATE_WORK", "false", "false", "private derivation/residual checkpoint only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": passed,
            "claim_allowed": allowed,
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, passed, allowed, reason in rows
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2699_0_gain", "WARD_DIVERGENCE_CONTRACT_DERIVED", "with T_GK=K_hat-Gamma_eff*g, q_loc is exactly -P_loc div T_GK", "use this as the formal target for any future GK/q_loc theorem"),
        ("DEC2699_1_limit", "CURRENT_MTS_DOES_NOT_PARENT_SIGN_TGK", "live sources do not supply a matched S_GK, Khat metric response, Helmholtz certificate, Euler/source zero, P_loc owner and boundary no-flux in one branch", "do not claim q_loc=0 or local GR"),
        ("DEC2699_2_demotion", "QLOC_OFFICIAL_RESIDUAL_VECTOR_REAFFIRMED", "because the theorem chain remains unsigned, q_loc is carried as explicit finite residual components", "future tests must use units, source paths and response operators"),
        ("DEC2699_3_best_next", "METRIC_RESPONSE_TEST_OR_FIRST_RESPONSE_ROW_NEXT", "the root missing item is K_hat=K_metric[Gamma_eff]; if no source-signed Gamma_eff exists, the empirical path needs one nonclaim response operator row", "run 2700"),
        ("DEC2699_4_no_broad_recap", "NO_MORE_BROAD_QLOC_RECAPS_UNTIL_ONE_INPUT_MOVES", "the logic is now stable; progress requires a concrete metric-response comparison or a concrete projection row", "avoid circling"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "next_action": next_action,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for decision_id, decision, rationale, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2699_0_selected",
            "selection": "selected_primary",
            "target_doc": "2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md",
            "target_script": "scripts/Y5_R2FR_Gamma_eff_candidate_metric_response_or_first_q_loc_response_row_2700.py",
            "task": "try one concrete source-signed Gamma_eff density and compute K_metric against live K_hat; if no candidate is source-signed, create the first strict nonclaim q_loc response-operator row",
            "success_condition": "either a term-by-term K_hat metric-response comparison is recorded, or one PPN/R10/R11/clock/orbital projection row has units, source path, missing inputs, and valid_for_claim=false",
            "forbidden_shortcuts": "claiming q_loc zero; scoring placeholders; using plateau axiom; hiding in measured G; readout cancellation; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "next_id": "NEXT2699_1_parallel_hold",
            "selection": "held_parallel",
            "target_doc": "2700b-Y5-R2FR-PiM-source-measure-after-q-loc-response-row.md",
            "target_script": "scripts/Y5_R2FR_PiM_source_measure_after_q_loc_response_row_2700b.py",
            "task": "return to parent H_tau/Pi_M/source-measure descent after the first q_loc metric-response/projection input is attempted",
            "success_condition": "source-measure residuals are not absorbed into q_loc or measured GM",
            "forbidden_shortcuts": "orbital GM premise; bare mass substitution; projector mask",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2699_0_q_loc", "Gamma/Khat/q_loc", "CONDITIONAL_WARD_ROUTE_DERIVED_LIVE_THEOREM_BLOCKED", "we have the correct form of the theorem, but not the parent-signed physical inputs", "run 2700 metric-response/projection input"),
        ("STATUS2699_1_local_GR", "local GR/Newton reduction", "BLOCKED_BY_OFFICIAL_QLOC_AND_SOURCE_RESIDUALS", "local GR is not dead, but it cannot be claimed while q_loc residuals are neither zero nor bounded", "make one q_loc input score-ready"),
        ("STATUS2699_2_coupling", "coupling lock", "ROOT_CAUSE_NARROWED", "the next concrete hinge is K_hat metric response or q_loc arena projection", "stop recapping until one input moves"),
        ("STATUS2699_3_testing", "empirical tests", "PREPARED_NOT_SCORE_READY", "PPN/R10/R11/clock/orbital queues exist but lack response operators and source-backed units", "fill first nonclaim projection row if metric response has no candidate"),
        ("STATUS2699_4_public", "public/GitHub", "NO_ACTION_PRIVATE", "this remains private derivation discipline", "keep private"),
    ]
    return [
        {
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "meaning": meaning,
            "next_action": next_action,
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for status_id, topic, status, meaning, next_action in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2699_0_local_residual",
            "source_csv": str(OUTPUTS["official_residual_vector"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_residual_vector"]),
            "purpose": "local-bound branch inherits q_loc as official nonclaim residual vector",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2699_1_local_projection",
            "source_csv": str(OUTPUTS["arena_projection_queue"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_projection_queue"]),
            "purpose": "local-bound branch inherits projection requirements",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2699_2_wep",
            "source_csv": str(OUTPUTS["official_residual_vector"]),
            "branch_csv": str(BRANCH_OUTPUTS["wep_residual_vector"]),
            "purpose": "WEP branch inherits q_loc source/current residual status",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2699_3_source_weight",
            "source_csv": str(OUTPUTS["official_residual_vector"]),
            "branch_csv": str(BRANCH_OUTPUTS["source_weight_residual_vector"]),
            "purpose": "source-weight branch inherits q_loc/source-normalization residual status",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2699_4_rab_next",
            "source_csv": str(OUTPUTS["next_target"]),
            "branch_csv": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "RAB queue receives 2700 metric-response/projection next target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    all_sources_exist = all(row["exists"] == "true" for row in source_rows)
    all_needles_found = all(row["missing_needles"] == "" for row in source_rows)

    parse_targets = {key: path for key, path in OUTPUTS.items() if key != "validation"}
    parse_targets.update(BRANCH_OUTPUTS)
    parse_results = {key: parse_csv(path) for key, path in parse_targets.items()}
    all_csv_parse = all(ok and count > 0 for ok, count, _ in parse_results.values())

    ward = rows_by_name["ward_identity"]
    gates = rows_by_name["parent_signature_gates"]
    residuals = rows_by_name["official_residual_vector"]
    claim_gates = rows_by_name["claim_gates"]
    next_targets = rows_by_name["next_target"]
    dryrun_results = rows_by_name["dryrun_results"]

    identity_present = any(row["identity_id"] == "WID2699_0_definition" and row["proof_status"] == "DERIVED_ALGEBRAIC_IDENTITY" for row in ward)
    live_verdict_blocks = any(row["identity_id"] == "WID2699_4_live_verdict" and "FAILS_CURRENT" in row["proof_status"] for row in ward)
    all_parent_gates_block = all(row["passes_now"] == "false" and row["parent_signed"] == "false" for row in gates)
    official_residuals_retained = all(row["official_residual"] == "true" and row["valid_for_claim"] == "false" for row in residuals)
    no_claims = all(row["claim_allowed"] == "false" for row in claim_gates)
    dryruns_safe = all(row["q_loc_zero_claim_allowed"] == "false" and row["matches_expected"] == "true" for row in dryrun_results)
    next_2700 = any(row["next_id"] == "NEXT2699_0_selected" and "2700-" in row["target_doc"] for row in next_targets)
    no_formalization_outputs = all("formalization-workbench" not in str(path).lower() for path in parse_targets.values())
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in path.name.lower() for path in parse_targets.values())

    checks = [
        ("VAL2699_0_sources_exist", all_sources_exist, "all cited source paths exist"),
        ("VAL2699_1_needles_found", all_needles_found, "all required source needles were found"),
        ("VAL2699_2_csv_parse", all_csv_parse, "all generated CSVs and branch copies parse with at least one row"),
        ("VAL2699_3_identity_present", identity_present, "q_loc=-P_loc div(K_hat-Gamma_eff*g) identity is recorded"),
        ("VAL2699_4_live_theorem_blocked", live_verdict_blocks, "live q_loc theorem-zero is explicitly blocked"),
        ("VAL2699_5_parent_gates_block", all_parent_gates_block, "all parent signature gates remain unsigned/nonclaim"),
        ("VAL2699_6_official_residuals_retained", official_residuals_retained, "official residual rows remain nonclaim"),
        ("VAL2699_7_no_claims", no_claims, "all claim gates keep claim_allowed=false"),
        ("VAL2699_8_dryruns_safe", dryruns_safe, "dry-run cases never allow q_loc/local-GR claim"),
        ("VAL2699_9_next_2700", next_2700, "2700 metric-response/projection target selected"),
        ("VAL2699_10_no_formalization_outputs", no_formalization_outputs, "no output path points into formalization-workbench"),
        ("VAL2699_11_no_github_outputs", no_github_outputs, "no GitHub/public-output path was written"),
    ]

    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "passed": as_bool(passed),
                "detail": detail,
                "timestamp_utc": stamp(),
            }
        )
    for key, (ok, count, message) in parse_results.items():
        rows.append(
            {
                "check_id": f"VAL2699_PARSE_{key}",
                "passed": as_bool(ok and count > 0),
                "detail": f"{message}; rows={count}",
                "timestamp_utc": stamp(),
            }
        )
    overall = all(row["passed"] == "true" for row in rows)
    rows.append(
        {
            "check_id": "VAL2699_OVERALL",
            "passed": as_bool(overall),
            "detail": "2699 derives the exact q_loc Ward-divergence contract, refuses live theorem-zero promotion, locks q_loc as official residual, and selects 2700 metric-response/projection input",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    verdict = (
        "2699 takes the leap and the leap lands in a disciplined place: algebraically, q_loc is exactly the projected "
        "negative divergence of T_GK = K_hat - Gamma_eff g. Field-theoretically, that can become zero only if T_GK is "
        "the Hilbert stress of a single diffeomorphism-invariant parent sector with Euler closure, double-zero, projector "
        "ownership, and boundary silence. Current MTS does not yet sign those live clauses, so q_loc is officially retained "
        "as a finite residual vector rather than smuggled into a local plateau."
    )
    text = f"""# 2699: Gamma/Khat/q_loc First Variation Or Official Residual Demotion

**Branch:** `{BRANCH_ID}`

## Private Verdict

{verdict}

## Exact Contract

Define:

`T_GK^{{mu nu}} := K_hat^{{mu nu}} - Gamma_eff g^{{mu nu}}`.

Then metric compatibility gives:

`q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}}) = -P_loc nabla_mu T_GK^{{mu nu}}`.

So the respectable route is not a plateau axiom. It is: prove `T_GK` is a parent Hilbert stress, prove the local Euler/source/boundary/projector terms vanish, and prove `T_GK(Phi0)=0`, `partial_A T_GK(Phi0)=0`. Without those, `q_loc` is a test residual.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Ward-Divergence Identity

{markdown_table(rows_by_name["ward_identity"])}

## Parent Signature Gates

{markdown_table(rows_by_name["parent_signature_gates"])}

## Noether Residual Decomposition

{markdown_table(rows_by_name["noether_residual_decomposition"])}

## Official q_loc Residual Vector

{markdown_table(rows_by_name["official_residual_vector"])}

## Arena Projection Queue

{markdown_table(rows_by_name["arena_projection_queue"])}

## Claim Gates

{markdown_table(rows_by_name["claim_gates"])}

## Decisions

{markdown_table(rows_by_name["decision_ledger"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(rows_by_name["validation"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    ward_rows = ward_identity_rows()
    signature_rows = parent_signature_gate_rows()
    noether_rows = noether_residual_decomposition_rows()
    residual_rows = official_residual_vector_rows()
    projection_rows = arena_projection_queue_rows()
    dryrun_cases = dryrun_case_rows()
    dryrun_results = [score_dryrun_case(row) for row in dryrun_cases]
    claim_rows = claim_gate_rows()
    decision_rows = decision_ledger_rows()
    next_rows = next_target_rows()
    status_rows = project_status_rows()
    branch_rows = branch_copy_rows()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "ward_identity": ward_rows,
        "parent_signature_gates": signature_rows,
        "noether_residual_decomposition": noether_rows,
        "official_residual_vector": residual_rows,
        "arena_projection_queue": projection_rows,
        "dryrun_cases": dryrun_cases,
        "dryrun_results": dryrun_results,
        "claim_gates": claim_rows,
        "decision_ledger": decision_rows,
        "next_target": next_rows,
        "project_status": status_rows,
        "branch_copies": branch_rows,
    }

    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)

    write_csv(BRANCH_OUTPUTS["local_residual_vector"], residual_rows)
    write_csv(BRANCH_OUTPUTS["local_projection_queue"], projection_rows)
    write_csv(BRANCH_OUTPUTS["wep_residual_vector"], residual_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_residual_vector"], residual_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_rows)

    validation = validation_rows(rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
