from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3620"
BRANCH_ID = "MTS_R2FR_Y5_EM_SOURCE_COUPLING_OWNER_OR_F2_COEFFICIENT_BOUND_3620"
DOC = ROOT / "3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3620_SOURCE_REGISTER.csv",
        "owner_theorem": RESIDUALS / "P8_Y5_R2FR_3620_EM_SOURCE_OWNER_THEOREM_ATTEMPT.csv",
        "calibration_gate": RESIDUALS / "P8_Y5_R2FR_3620_MAXWELL_SOURCE_CALIBRATION_GATE.csv",
        "finite_coefficients": RESIDUALS / "P8_Y5_R2FR_3620_FINITE_F2_SOURCE_COEFFICIENT_ROWS.csv",
        "source_current_closure": RESIDUALS / "P8_Y5_R2FR_3620_EM_TOTAL_SOURCE_CURRENT_CLOSURE.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3620_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3620_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3620_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_EM_source_coupling_owner_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3620_VALIDATION.csv",
    }


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3619": (
            RESIDUALS / "P8_Y5_R2FR_3619_NEXT_TARGET.csv",
            "3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md",
        ),
        "domain_3619": (
            RESIDUALS / "P8_Y5_R2FR_3619_VISIBLE_EM_DOMAIN_EXHAUSTION_THEOREM.csv",
            "EXACT_CONDITIONAL_THEOREM_PLUS_NONZERO_ROWS",
        ),
        "kinetic_765": (
            RESIDUALS / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
            "MKI765_5_total",
        ),
        "alpha_1812": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
            "ALO1812_5_verdict",
        ),
        "current_1814": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv",
            "VCC1814_0_target",
        ),
        "charge_spine_2340": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
            "PCS2340_6_MHref",
        ),
        "observed_hodge_3503": (
            RESIDUALS / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
            "OHM3503_2_charge_current_owner",
        ),
        "poynting_3463": (
            RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
            "EM3463_4_multiplier_obstruction",
        ),
        "f2_gates_3212": (
            RESIDUALS / "P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv",
            "F2G3212_5_total_EM_zero",
        ),
        "unique_f2_1235": (
            RESIDUALS / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
            "UF21235_7_verdict",
        ),
        "no_hidden_visible_2659": (
            RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
            "ODT2659_6_verdict",
        ),
    }


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for source_id, source_data in source_map().items():
        source_path, needle = source_data
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def owner_theorem_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "ESO3620_0_parent_connection_projection",
            "claim_piece": "visible EM connection projection",
            "statement": "A_Q must be the projection of a parent connection along a fixed generator T_Q before readout, not an appended Maxwell field.",
            "formula": "A_parent = A_Q T_Q + A_perp; F_parent contains F_Q T_Q",
            "if_signed": "visible EM is tied to the parent field space and cannot be independently normalized after the fact",
            "current_status": "CONDITIONAL_TEMPLATE_ONLY",
            "source_path": str(sources["kinetic_765"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "ESO3620_1_fixed_TQ_norm",
            "claim_piece": "fixed gauge-generator norm",
            "statement": "The parent norm of T_Q must be fixed by representation/lattice/fibre metric data so the Maxwell kinetic coefficient cannot be rescaled independently.",
            "formula": "Z_Q = C_P <T_Q,T_Q>_P = C_P N_Q; D_v N_Q=0",
            "if_signed": "lambda_F2 and b_alpha from gauge-norm drift vanish structurally",
            "current_status": "NORM_ROUTE_CONDITIONAL_NOT_SIGNED",
            "source_path": str(sources["alpha_1812"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "ESO3620_2_unique_F2",
            "claim_piece": "unique Maxwell F2 owner",
            "statement": "No independent lambda_A F_Q^2 or hidden f_X F_Q^2 term is allowed beyond the parent curvature norm.",
            "formula": "Allowed[S] excludes DeltaS=-1/4 int lambda_F2(Phi) F_Q wedge *_obs F_Q",
            "if_signed": "EM stress/Poynting strength cannot be tuned independently of the parent charge generator",
            "current_status": "UNIQUE_F2_NOT_CLOSED",
            "source_path": str(sources["unique_f2_1235"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "ESO3620_3_same_current_owner",
            "claim_piece": "charge/current normalization",
            "statement": "The same T_Q owner must define matter charge labels, the Noether/Ward current, and source/test current readout.",
            "formula": "J_Q := delta S_matter/delta A_Q with charges as fixed T_Q representation weights",
            "if_signed": "current rescalings J->c_J J and source-label kappa_A maps are ill-typed",
            "current_status": "CONNECTION_CURRENT_OWNER_CONTRACT_NOT_CURRENT_PROOF",
            "source_path": str(sources["current_1814"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "ESO3620_4_Hilbert_source",
            "claim_piece": "EM Hilbert stress source",
            "statement": "Once the observed Hodge and kinetic/current owner are fixed together, EM energy, pressure and Poynting flux source gravity through the same Hilbert stress slot as matter.",
            "formula": "T_EM^{mu nu}=2/sqrt(-g_obs) delta S_EM/delta g_obs; T_EM^{0i}=S_Poynting^i/c^2",
            "if_signed": "Poynting flow becomes source-current flow, not an extra fitted force",
            "current_status": "EXACT_CONDITIONAL_ON_OWNER_PACKAGE",
            "source_path": str(sources["poynting_3463"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "ESO3620_5_total_current_closure",
            "claim_piece": "matter plus EM total current",
            "statement": "Local force exchange between matter and EM cancels only in the total Hilbert current, so the source mass/current must use T_total rather than matter alone.",
            "formula": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda; nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda; nabla_mu T_total^{mu nu}=0",
            "if_signed": "charged internal exchange is bookkeeping inside the total source, while radiative boundary flux remains explicit",
            "current_status": "CONDITIONAL_TOTAL_CURRENT_CLOSURE",
            "source_path": str(sources["observed_hodge_3503"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "ESO3620_6_verdict",
            "claim_piece": "EM source coupling owner verdict",
            "statement": "The source-coupling theorem is exact conditionally, but the current corpus does not jointly sign projection, norm, unique F2, current owner and readout/radiative closure.",
            "formula": "ESO3620_0..ESO3620_5 signed together => lambda_F2=b_alpha=kappa_J=w_EM=0",
            "if_signed": "local EM/GR source coupling becomes structurally calibrated",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PLUS_FINITE_ROWS",
            "source_path": str(sources["kinetic_765"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def calibration_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MCG3620_0_projection",
            "owner_clause": "A_Q projection from parent connection",
            "required_condition": "A_parent=A_Q T_Q + A_perp before readout",
            "current_status": "template_only",
            "failure_mode": "appended Maxwell field can carry independent normalization",
            "source_path": str(sources["kinetic_765"][0]),
            "passes_now": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MCG3620_1_norm",
            "owner_clause": "fixed T_Q norm / fixed alpha level",
            "required_condition": "<T_Q,T_Q>_P=N_Q fixed; alpha_EM=alpha_*(ell_EM,g_*)",
            "current_status": "not_signed",
            "failure_mode": "g_EM normalization and alpha drift become finite coefficients",
            "source_path": str(sources["alpha_1812"][0]),
            "passes_now": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MCG3620_2_unique_F2",
            "owner_clause": "no independent F2",
            "required_condition": "no lambda_A F_Q^2 or f_X F_Q^2 beyond parent curvature norm",
            "current_status": "failed_current_corpus",
            "failure_mode": "EM stress source strength can drift independently",
            "source_path": str(sources["f2_gates_3212"][0]),
            "passes_now": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MCG3620_3_same_current",
            "owner_clause": "same current owner",
            "required_condition": "J_Q is Noether/Ward current of the same T_Q connection and source/test readout has no c_J/kappa_A",
            "current_status": "contract_not_current_proof",
            "failure_mode": "source/test current rescaling reopens WEP/R10/local-GR residuals",
            "source_path": str(sources["current_1814"][0]),
            "passes_now": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "MCG3620_4_readout_radiative",
            "owner_clause": "readout/radiative preservation",
            "required_condition": "effective alpha and EM source readout factor only through q or fixed representation data",
            "current_status": "unsigned",
            "failure_mode": "clock/spectroscopy/EFT thresholds regenerate alpha/source markers",
            "source_path": str(sources["alpha_1812"][0]),
            "passes_now": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def finite_coefficient_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "FSC3620_0_lambda_F2",
            "coefficient": "lambda_F2",
            "meaning": "independent Maxwell kinetic multiplier beyond parent curvature norm",
            "formula": "S_EM=-(Z_Q/4) int F_Q wedge *_obs F_Q; Z_Q=C_P N_Q + lambda_F2",
            "observable_links": "alpha_EM; clocks; spectroscopy; WEP; R10; source normalization",
            "required_for_zero": "unique parent curvature norm and no independent F2 slot",
            "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "source_path": str(sources["unique_f2_1235"][0]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "FSC3620_1_b_alpha",
            "coefficient": "b_alpha",
            "meaning": "vertical/readout derivative of the measured fine-structure level",
            "formula": "b_alpha := D_v ln alpha_EM",
            "observable_links": "atomic clocks; Oklo/meteorites; WEP composition response; spectroscopy",
            "required_for_zero": "fixed alpha level plus readout/radiative closure",
            "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "source_path": str(sources["alpha_1812"][0]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "FSC3620_2_kappa_J",
            "coefficient": "kappa_J",
            "meaning": "source/test current normalization or species/source-label current rescaling",
            "formula": "J_Q^readout=(1+kappa_J) J_Q^Noether",
            "observable_links": "WEP; Lorentz force calibration; source/test charge; local EM stress exchange",
            "required_for_zero": "same T_Q Noether current owner and no current morphism",
            "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "source_path": str(sources["current_1814"][0]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "FSC3620_3_w_EM",
            "coefficient": "w_EM",
            "meaning": "EM Hilbert stress/source weight relative to matter/source mass",
            "formula": "T_EM^source=(1+w_EM) T_EM^Hilbert",
            "observable_links": "Newtonian source mass; PPN; orbital GM; radiation pressure; Poynting flux",
            "required_for_zero": "same observed Hodge, unique F2 and Hilbert source current owner",
            "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "source_path": str(sources["poynting_3463"][0]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "FSC3620_4_Phi_EM_boundary",
            "coefficient": "Phi_EM_boundary",
            "meaning": "radiative/boundary Poynting flux not included in stationary source charge",
            "formula": "Phi_EM_boundary := int_boundary S_Poynting dot n dA",
            "observable_links": "stationary source charge; orbital energy loss; local conservation; H_tau flux",
            "required_for_zero": "closed stationary worldtube or explicit radiation flux accounting",
            "current_value": "MISSING_BOUNDARY_ZERO_OR_NUMERIC_FLUX",
            "source_path": str(sources["poynting_3463"][0]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_current_closure_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "closure_id": "SCC3620_0_total_stress_identity",
            "target": "matter plus EM total Hilbert current",
            "identity": "nabla_mu T_total^{mu nu}=0 with T_total=T_matter+T_EM",
            "meaning": "internal Lorentz exchange cancels only in the total current",
            "status": "EXACT_CONDITIONAL_IMPORTED",
            "source_path": str(sources["observed_hodge_3503"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "closure_id": "SCC3620_1_source_mass_projection",
            "target": "projected stationary source charge",
            "identity": "d(Pi_M J_H_total)=Pi_M dJ_H_total + [d,Pi_M]J_H_total",
            "meaning": "local Newtonian source mass is stable only if total current closure, projector naturality and boundary flux clauses close together",
            "status": "CONDITIONAL_CHAIN_NOT_FULLY_SIGNED",
            "source_path": str(sources["observed_hodge_3503"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": timestamp and BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "closure_id": "SCC3620_2_reference_mass_guard",
            "target": "M_H_ref / H_tau denominator",
            "identity": "M_H_ref=H_tau[S_outer]-H_ref",
            "meaning": "EM source coupling must feed the same H_tau/source denominator rather than borrowing orbital GM",
            "status": "FIRST_ROW_READY_VALUES_MISSING",
            "source_path": str(sources["charge_spine_2340"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3620_0_owner_theorem",
            "decision": "The EM source-coupling owner theorem is exact conditionally: projection, fixed T_Q norm, unique F2, same current and Hilbert source must close together.",
            "status": "PASS_CONDITIONAL_NOT_PARENT_SIGNED",
            "next_action": "attempt joint parent signature rather than separate patch fixes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3620_1_finite_rows",
            "decision": "Because the owner theorem is not jointly signed, finite rows are emitted for lambda_F2, b_alpha, kappa_J, w_EM and Phi_EM_boundary.",
            "status": "PASS_FINITE_ROWS_VALUES_MISSING",
            "next_action": "source bounds or prove zeros for these rows before any local-GR/Newton claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3620_2_best_next_route",
            "decision": "Best next route is a single joint parent-owner packet for T_Q, N_Q, J_Q and F2, because closing only one of them leaves rescaling loopholes.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3621-Y5-R2FR-joint-TQ-NQ-JQ-owner-packet-or-finite-bound-runner.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3620_0",
            "result": "EM_SOURCE_OWNER_CONDITIONAL_THEOREM_PLUS_FINITE_COEFFICIENT_ROWS",
            "summary": "3620 derives the joint EM source-coupling owner theorem conditionally and emits finite rows for the live normalization/source coefficients because the parent owner packet is not jointly signed.",
            "owner_theorem_promoted": False,
            "finite_coefficients_written": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3620_0",
            "target_doc": "3621-Y5-R2FR-joint-TQ-NQ-JQ-owner-packet-or-finite-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_3621_joint_TQ_NQ_JQ_owner_packet_or_finite_bound_runner.py",
            "objective": "attempt a joint parent-owner packet for the visible charge generator T_Q, fixed norm N_Q, Noether current J_Q, unique F2 and EM Hilbert source weight; if it cannot be signed, prepare finite bound-runner rows for lambda_F2, b_alpha, kappa_J and w_EM",
            "success_gate": "either the joint owner packet closes all EM source-coupling rescalings at once, or the finite rows become runner-ready with units, arenas and source paths",
            "reason": "3620 shows piecemeal closure is insufficient; source coupling needs one shared owner or finite empirical bounds.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "EM_source_owner": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "live_coefficients": "lambda_F2;b_alpha;kappa_J;w_EM;Phi_EM_boundary",
            "local_GR_Newton_pressure_point": "calibrated source coupling",
            "claim_status": "NO_CLAIM",
            "valid_for_claim": False,
        }
    ]


def write_markdown() -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3620 Y5 R2FR: EM source-coupling owner or F2 coefficient bound",
                "",
                "## Verdict",
                "- The EM/source coupling throat is now explicit.",
                "- Local Maxwell light-cone success is not enough: `A_Q`, `F_Q^2`, `J_Q`, `alpha_EM`, Poynting/Hilbert stress and source mass must share one parent owner.",
                "- The owner theorem is exact conditionally, but not parent-signed in the current corpus.",
                "- Therefore finite source-coupling coefficient rows are retained.",
                "",
                "## Conditional owner theorem",
                "- `A_parent = A_Q T_Q + A_perp` must define the visible connection before readout.",
                "- `Z_Q = C_P <T_Q,T_Q>_P = C_P N_Q` must be fixed by parent representation/norm data.",
                "- No independent `lambda_F2 F_Q^2` or hidden `f_X F_Q^2` may exist.",
                "- `J_Q := delta S_matter/delta A_Q` must be the same `T_Q` Noether/Ward current used by source/test readout.",
                "- `T_EM` must be the Hilbert stress from the same observed-Hodge Maxwell action.",
                "- If all close together: `lambda_F2=b_alpha=kappa_J=w_EM=0`.",
                "",
                "## Live finite rows",
                "- `lambda_F2`: independent Maxwell kinetic multiplier.",
                "- `b_alpha`: vertical/readout drift of measured fine-structure level.",
                "- `kappa_J`: source/test current normalization rescaling.",
                "- `w_EM`: EM Hilbert stress/source weight relative to matter/source mass.",
                "- `Phi_EM_boundary`: radiative Poynting boundary flux not included in stationary source charge.",
                "",
                "## Practical read",
                "- The theory is not dead here; this is a clean engineering throat.",
                "- But this must close as one packet. Closing only `F2` while leaving current normalization free just moves the knob.",
                "- This is directly connected to Newton/GR reduction because it controls what counts as source mass/energy.",
                "",
                "## Next target",
                "- `3621-Y5-R2FR-joint-TQ-NQ-JQ-owner-packet-or-finite-bound-runner.md`.",
                "- Aim: one parent owner packet for `T_Q`, `N_Q`, `J_Q`, unique `F2`, and EM Hilbert source weight; otherwise prepare finite empirical bound rows.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: exact conditional theorem plus finite coefficient rows.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    results: list[tuple[str, bool, str]] = []

    sources = source_map()
    sources_exist = all(source_path.exists() for source_path, _needle in sources.values())
    needles_found = all(source_path.exists() and contains(source_path, needle) for source_path, needle in sources.values())
    results.append(("VAL3620_0_sources_exist", sources_exist, "all required 3620 source paths exist"))
    results.append(("VAL3620_1_needles_found", needles_found, "all selected 3620 source anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3620_2_outputs_exist", outputs_exist, "all pre-validation 3620 outputs written"))

    parse_details: list[str] = []
    csv_parse_pass = True
    for name, path in paths.items():
        if name == "validation":
            continue
        try:
            parse_details.append(f"{name}:{len(read_csv(path))}")
        except Exception as exception:
            csv_parse_pass = False
            parse_details.append(f"{name}:ERROR:{exception}")
    results.append(("VAL3620_3_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    theorem_rows = read_csv(paths["owner_theorem"]) if paths["owner_theorem"].exists() else []
    theorem_has_joint_zero = any("lambda_F2=b_alpha=kappa_J=w_EM=0" in row["formula"] for row in theorem_rows)
    theorem_not_promoted = bool(theorem_rows) and all(row["parent_signed"] == "False" for row in theorem_rows)
    results.append(("VAL3620_4_joint_zero_formula_written", theorem_has_joint_zero, "joint zero formula written"))
    results.append(("VAL3620_5_theorem_not_promoted", theorem_not_promoted, "owner theorem remains conditional/nonclaim"))

    coefficient_rows = read_csv(paths["finite_coefficients"]) if paths["finite_coefficients"].exists() else []
    expected = {"lambda_F2", "b_alpha", "kappa_J", "w_EM", "Phi_EM_boundary"}
    found = {row["coefficient"] for row in coefficient_rows}
    coeff_nonclaim = bool(coefficient_rows) and all(
        row["score_ready"] == "False" and row["claim_allowed"] == "False" and row["valid_for_claim"] == "False"
        for row in coefficient_rows
    )
    results.append(("VAL3620_6_finite_coefficients_present", expected.issubset(found), "all finite source-coupling coefficients present"))
    results.append(("VAL3620_7_coefficients_nonclaim", coeff_nonclaim, "finite coefficient rows remain nonclaim/not score-ready"))

    gate_rows = read_csv(paths["calibration_gate"]) if paths["calibration_gate"].exists() else []
    gates_blocked = bool(gate_rows) and all(row["passes_now"] == "False" for row in gate_rows)
    results.append(("VAL3620_8_calibration_gates_blocked", gates_blocked, "calibration gates correctly remain blocked"))

    closure_rows = read_csv(paths["source_current_closure"]) if paths["source_current_closure"].exists() else []
    total_current_written = any("T_total" in row["identity"] for row in closure_rows)
    results.append(("VAL3620_9_total_current_identity_written", total_current_written, "total matter+EM current closure identity written"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3620_10_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3620*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3620 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3620_11_no_formalization_leak", formalization_clean, formalization_detail))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["owner_theorem"], owner_theorem_rows())
    write_csv(paths["calibration_gate"], calibration_gate_rows())
    write_csv(paths["finite_coefficients"], finite_coefficient_rows())
    write_csv(paths["source_current_closure"], source_current_closure_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3620 validation failed: {failed}")
    print(f"wrote 3620 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
