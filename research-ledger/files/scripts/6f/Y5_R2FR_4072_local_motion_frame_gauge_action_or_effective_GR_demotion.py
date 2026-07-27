from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md"

DECISION = "LOCAL_MOTION_FRAME_GAUGE_ACTION_WRITTEN_AS_FORMAL_CANDIDATE_NOT_CURRENT_MTS_DERIVED_EFFECTIVE_GR_DEMOTION_ACTIVE"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4072_00_4071_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_NEXT_TARGET.csv",
        "local-motion-frame-gauge-action-or-effective-GR-demotion",
        "4071 selected the gauge-action-or-demotion target.",
    ),
    "SRC4072_01_4071_origin": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_CARTAN_ORIGIN_THEOREM_ATTEMPT.csv",
        "ORG4071_0_gauge_compensator",
        "4071 proves the conditional compensator theorem.",
    ),
    "SRC4072_02_4071_gauge": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_LOCAL_MOTION_FRAME_GAUGE_TEST.csv",
        "MFG4071_2_local_translation",
        "4071 shows local translations force B^A conditionally.",
    ),
    "SRC4072_03_4071_uplift": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_MTS_TO_CARTAN_UPLIFT_MAP.csv",
        "UP4071_2_memory",
        "4071 requires Gamma/memory uplift to Cartan field-strength invariants.",
    ),
    "SRC4072_04_primitives": (
        FORMALIZATION / "03-unified-field-theory-programme.md",
        "Candidate MTS primitives:",
        "formal programme lists current primitive vocabulary.",
    ),
    "SRC4072_05_spine": (
        FORMALIZATION / "07-unification-spine.md",
        "a motion/curvature-memory field theory",
        "spine defines broad MTS target language.",
    ),
    "SRC4072_06_solder_obstruction": (
        FORMALIZATION / "142-owner-spacetime-solder-map-theorem.md",
        "bulk hybrid owner-connection route = fails as derivation",
        "older formalization warns that unsourced solder maps fail as derivations.",
    ),
    "SRC4072_07_observer_coframe": (
        ROOT / "10-observer-map-symplectic-contract.md",
        "The local observer coframe must be defined",
        "observer coframe is required before PPN claims.",
    ),
    "SRC4072_08_local_blocks": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "A511_0_EH_core",
        "minimal local GR action blocks supply EH/core comparison.",
    ),
    "SRC4072_09_derived_chain": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
        "DC511_2",
        "older derived chain states local metric equation reduction is conditional.",
    ),
    "SRC4072_10_kappa_top": (
        SOURCE_DIR / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
        "K508_0_field_content",
        "constant kappa can be topological if adopted.",
    ),
    "SRC4072_11_torsion": (
        SOURCE_DIR / "P8_Y5_axial_torsion_stiffness_status.csv",
        "axial_torsion_stiffness_and_response",
        "torsion status is symbolic nonclaim.",
    ),
    "SRC4072_12_EM_Hodge": (
        SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "DHB3504_0_Delta_Hodge_EM",
        "EM/Hodge coframe mismatch remains a bound-or-zero issue.",
    ),
    "SRC4072_13_observed_flow": (
        SOURCE_DIR / "P8_local_GR_observed_flow_stationary_branch_status.csv",
        "STAT3538_0_flow",
        "observed flow/coframe is conditional same-stack owner.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4072_SOURCE_REGISTER.csv",
    "action_candidate": SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
    "gauge_variation": SOURCE_DIR / "P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv",
    "reduction_chain": SOURCE_DIR / "P8_Y5_R2FR_4072_EH_NEWTON_PPN_REDUCTION_CONTRACT.csv",
    "demotion_matrix": SOURCE_DIR / "P8_Y5_R2FR_4072_EFFECTIVE_GR_DEMOTION_MATRIX.csv",
    "residual_interface": SOURCE_DIR / "P8_Y5_R2FR_4072_RESIDUAL_INTERFACE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4072_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4072_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4072_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4072_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4072_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def action_candidate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "block_id": "LGA4072_0_field_space",
            "action_block": "Q_4072 = {X^A=L_* Psi^A, B^A, omega^AB, eta_AB, kappa_eff, A_3, matter, EM, auxiliary silence fields}",
            "role": "minimum local motion-frame gauge parent field space",
            "variation_owner": "all geometry/readout fields are varied or constrained before PPN/Newton readout",
            "MTS_status": "FORMAL_CANDIDATE_NOT_CURRENT_MTS_DERIVED",
            "if_rejected": "Cartan coframe is an effective-GR branch input",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "LGA4072_1_solder",
            "action_block": "e^A = D_omega X^A + B^A; g_obs = eta_AB e^A e^B",
            "role": "covariant solder map avoiding exact-gradient flatness",
            "variation_owner": "B^A and omega^AB are independent parent variables or gauge fields",
            "MTS_status": "REQUIRED_FOR_ROUTE",
            "if_rejected": "4070 exact-gradient obstruction blocks derived curved GR",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "LGA4072_2_gravity",
            "action_block": "S_EC = (4 kappa_eff)^-1 int epsilon_ABCD e^A wedge e^B wedge R^CD[omega] - (Lambda_eff/12 kappa_eff) int epsilon_ABCD e^A wedge e^B wedge e^C wedge e^D",
            "role": "Einstein-Cartan/Palatini two-derivative normal form",
            "variation_owner": "delta_e gives tetrad Einstein equation; delta_omega gives torsion/spin equation",
            "MTS_status": "STANDARD_GR_FORM_IMPORTED_UNLESS_SYMMETRY_AND_IR_NORMAL_FORM_ARE_PARENT_SIGNED",
            "if_rejected": "EH remains assumed effective branch",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "LGA4072_3_torsion_gate",
            "action_block": "S_T = int lambda_A wedge T^A or S_T = int a_T T^A wedge *T_A with positive stiffness",
            "role": "torsion/nonmetricity/preferred-frame gate for local PPN safety",
            "variation_owner": "T^A = D_omega e^A is constrained to zero or bounded",
            "MTS_status": "GATE_REQUIRED_NOT_PARENT_SIGNED",
            "if_rejected": "torsion residual vector must be scored",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "LGA4072_4_kappa",
            "action_block": "S_kappa_top = int kappa_eff dA_3",
            "role": "keeps kappa_eff/G_N local constant without claiming a numerical G derivation",
            "variation_owner": "delta_A3 S gives d kappa_eff=0 on connected local domains",
            "MTS_status": "CONDITIONAL_TOPOLOGICAL_ROUTE",
            "if_rejected": "G_N remains measured and kappa drift residuals stay live",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "LGA4072_5_matter_EM",
            "action_block": "S_matter[Psi_m,e,omega_LC_or_omega] + S_EM[A,e] with one observed coframe and no shadow frame",
            "role": "same-source matter/EM/stress/clock/readout coupling",
            "variation_owner": "coframe Hilbert stress is the source of local Newton/PPN readout",
            "MTS_status": "CARRIES_FORWARD_SAME_COFRAME_GATE",
            "if_rejected": "WEP, EM-Hodge, source-frame and PPN residuals must be bounded",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "LGA4072_6_memory",
            "action_block": "S_MTS_memory = int sqrt|g| F_MTS(Gamma_mem - I_R[R,T], chi, tau, ...)",
            "role": "maps MTS memory scalars to invariants/projections of Cartan curvature/torsion",
            "variation_owner": "Gamma_mem is not the connection; it is a scalar invariant/readout or constrained projection",
            "MTS_status": "UPLIFT_REQUIRED",
            "if_rejected": "Gamma_mem cannot own the local GR coframe/connection route",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def gauge_variation_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "variation_id": "GV4072_0_transform",
            "object": "local motion-frame transformation",
            "formula": "X' = Lambda X + a; omega' = Lambda omega Lambda^-1 - dLambda Lambda^-1; B' = Lambda B - D' a",
            "result": "e' = Lambda e and g_obs' = g_obs",
            "status": "GAUGE_COVARIANCE_CHECK_PASSES_FORMALLY",
            "timestamp_utc": current_timestamp,
        },
        {
            "variation_id": "GV4072_1_field_strengths",
            "object": "Cartan field strengths",
            "formula": "R^AB = d omega^AB + omega^A_C wedge omega^CB; T^A = D_omega e^A = D_omega B^A + R^A_B X^B",
            "result": "Gamma/memory may be scalar invariants of R/T but not a replacement for omega/B",
            "status": "FIELD_STRENGTHS_DEFINED",
            "timestamp_utc": current_timestamp,
        },
        {
            "variation_id": "GV4072_2_delta_omega",
            "object": "spin connection variation",
            "formula": "delta_omega S_EC gives torsion/spin equation; spinless/torsion-constrained branch gives omega=omega_LC[e]",
            "result": "EH reduction possible only after torsion gate closes",
            "status": "CONDITIONAL_PALATINI_REDUCTION",
            "timestamp_utc": current_timestamp,
        },
        {
            "variation_id": "GV4072_3_delta_B_or_e",
            "object": "coframe/solder variation",
            "formula": "delta_e S_EC + delta_e S_matter + delta_e S_EM = 0",
            "result": "tetrad Einstein equation with one coframe Hilbert source if matter/EM gate closes",
            "status": "CONDITIONAL_EINSTEIN_EQUATION",
            "timestamp_utc": current_timestamp,
        },
        {
            "variation_id": "GV4072_4_delta_A3",
            "object": "topological kappa variation",
            "formula": "delta_A3 int kappa_eff dA_3 = - int d kappa_eff wedge delta A_3",
            "result": "d kappa_eff=0 locally if boundary/topological premises hold",
            "status": "CONDITIONAL_CONSTANT_G",
            "timestamp_utc": current_timestamp,
        },
    ]


def reduction_chain_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "step_id": "RED4072_0_metric",
            "premise": "rank-four psi packet plus B/omega gauge compensators",
            "derivation": "e^A = D X^A + B^A; g_obs=eta_AB e^A e^B",
            "result": "non-flat Lorentzian observed geometry becomes possible",
            "status": "FORMAL_ROUTE",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "RED4072_1_EH",
            "premise": "S_EC action plus torsion/nonmetricity gate",
            "derivation": "omega -> omega_LC[e]; S_EC -> S_EH[g_obs] plus boundary",
            "result": "EH form inherited conditionally",
            "status": "CONDITIONAL_ON_TORSION_GATE",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "RED4072_2_source",
            "premise": "same observed coframe in matter, EM, clocks and source readouts",
            "derivation": "coframe Hilbert variation defines T_H and T_EM",
            "result": "source coupling can feed 4063 weak-field Newton/PPN branch",
            "status": "CONDITIONAL_ON_NO_SHADOW_FRAME",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "RED4072_3_Newton",
            "premise": "EH same-source branch and calibrated kappa_eff",
            "derivation": "G_00^(1) = kappa_eff T_00^H gives nabla^2 Phi_N = 4*pi G_N rho_H",
            "result": "Newtonian limit inherited from the guarded 4063 readout",
            "status": "CONDITIONAL_LINK_TO_4063",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "RED4072_4_PPN",
            "premise": "torsion, nonmetricity, shadow frames, EM-Hodge mismatch and extra modes are zero or bounded",
            "derivation": "PPN vector equals GR plus explicit residual interface",
            "result": "local tests become empirical residual locks rather than closure assumptions",
            "status": "NOT_CLAIMED_RESIDUAL_INTERFACE_REQUIRED",
            "timestamp_utc": current_timestamp,
        },
    ]


def demotion_matrix_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "DEM4072_0_symmetry",
            "required_parent_signature": "local motion-frame Lorentz + translation gauge symmetry appears as a primitive MTS symmetry",
            "current_evidence": "flow/frame clues exist but no signed local Poincare/motion-frame principal bundle action",
            "verdict": "FAILS_CURRENT_DERIVATION",
            "if_adopted": "Cartan fields become parent infrastructure",
            "if_not_adopted": "effective_GR_branch_input",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "DEM4072_1_action_ownership",
            "required_parent_signature": "B^A, omega^AB, R^AB, and T^A are in S_parent before local-GR readout",
            "current_evidence": "4072 writes the action candidate but prior corpus did not contain it",
            "verdict": "NEW_FORMAL_CANDIDATE_NOT_DERIVED",
            "if_adopted": "route becomes a private parent-action candidate",
            "if_not_adopted": "Cartan route is imported GR scaffolding",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "DEM4072_2_MTS_uplift",
            "required_parent_signature": "psi/flow/Gamma/tau map to X/B/R,T/e0 without losing information or adding hidden knobs",
            "current_evidence": "uplift map exists but Gamma scalar cannot replace the full connection",
            "verdict": "UPLIFT_OPEN",
            "if_adopted": "Gamma becomes curvature/torsion invariant/projection",
            "if_not_adopted": "Gamma remains separate effective memory scalar",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "DEM4072_3_empirical_safety",
            "required_parent_signature": "torsion, EM-Hodge, shadow frame, kappa drift and extra modes are zero or bounded",
            "current_evidence": "existing ledgers keep these as nonclaim residual gates",
            "verdict": "RESIDUALS_LIVE",
            "if_adopted": "must run residual scorer before claims",
            "if_not_adopted": "no public local-GR claim",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def residual_interface_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "RES4072_0_torsion",
            "quantity": "epsilon_torsion",
            "source": "T^A and axial torsion stiffness",
            "zero_condition": "T^A=0 by constraint/Palatini spinless branch or positive stiffness below locks",
            "fallback": "score torsion PPN/spin/preferred-frame residual",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4072_1_nonmetricity",
            "quantity": "epsilon_nonmetricity",
            "source": "D_omega eta_AB",
            "zero_condition": "omega^AB antisymmetric internal Lorentz connection parent-signed",
            "fallback": "clock/EM/PPN frame drift bound",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4072_2_EM_Hodge",
            "quantity": "Delta_Hodge_EM",
            "source": "EM constitutive/Hodge rule vs observed coframe",
            "zero_condition": "S_EM uses only e^A/g_obs and no independent principal/skewon/axion-gradient channel",
            "fallback": "EM birefringence/light-cone/Poynting bound rows",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4072_3_kappa",
            "quantity": "D kappa_eff or G_N drift",
            "source": "kappa topological/superselection sector",
            "zero_condition": "d kappa_eff=0 from S_kappa_top or equivalent parent global sector",
            "fallback": "G_eff drift/range/source normalization residual",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "residual_id": "RES4072_4_shadow_frame",
            "quantity": "epsilon_frame_source",
            "source": "matter/EM/clocks not using same descended coframe",
            "zero_condition": "single same-coframe matter functor with no conformal/disformal/source-label shadow frame",
            "fallback": "WEP/R10/PPN/source-coupling coefficient bounds",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision_gate": [
            {
                "decision_id": "DEC4072_0",
                "decision": DECISION,
                "summary": "4072 writes the local motion-frame gauge action candidate, verifies formal gauge/reduction structure, and marks current corpus derivation as failed unless the new action is explicitly parent-signed/adopted.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
            {
                "decision_id": "DEC4072_1",
                "decision": "CARTAN_ROUTE_IS_PRIVATE_PARENT_CANDIDATE_OR_EFFECTIVE_BRANCH_NOT_PROVEN_DERIVATION",
                "summary": "This is the fork: adopt/derive the motion-frame gauge action as MTS parent infrastructure, or label Cartan/EH as effective-GR input.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4072_0",
                "claim": "MTS existing corpus already derives the local motion-frame gauge action",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "4072 writes a formal candidate, but prior corpus does not parent-sign local motion-frame gauge symmetry/action",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4072_1",
                "claim": "local motion-frame gauge action is a viable private parent-action candidate",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "formal action, gauge transformations, field strengths, and EH reduction chain are explicit",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4072_2",
                "claim": "MTS derives local GR/Newton/PPN as a completed theorem",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "adoption/derivation, torsion, nonmetricity, same-coframe matter, EM-Hodge and kappa gates remain open",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4072_3",
                "claim": "MTS predicts numerical Newton G",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "kappa_eff remains topological/calibrated unless a parent scale theorem derives it",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4072_0",
                "next_doc": "4073-Y5-R2FR-formal-adoption-or-demotion-of-motion-frame-gauge-parent.md",
                "next_script": "scripts/Y5_R2FR_4073_formal_adoption_or_demotion_of_motion_frame_gauge_parent.py",
                "reason": "decide whether to add the motion-frame gauge action as a private MTS parent candidate in the formal workbench, or explicitly demote the local GR bridge to an effective-GR branch with residual scorers",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4072",
                "status": DECISION,
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_claim", "allowed_public", "public_claim", "github_action"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public/github claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public/github false"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4072_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4072_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4072_02_no_public_or_github_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4072_03_action_written",
            "passed": "Q_4072" in joined and "S_EC" in joined and "e^A = D_omega X^A + B^A" in joined,
            "detail": "local motion-frame gauge action candidate is written",
        },
        {
            "check_id": "VAL4072_04_current_derivation_rejected",
            "passed": "FORMAL_CANDIDATE_NOT_CURRENT_MTS_DERIVED" in joined and "FAILS_CURRENT_DERIVATION" in joined,
            "detail": "current-corpus derivation is not claimed",
        },
        {
            "check_id": "VAL4072_05_demotion_fork",
            "passed": "effective_GR_branch_input" in joined and "CARTAN_ROUTE_IS_PRIVATE_PARENT_CANDIDATE_OR_EFFECTIVE_BRANCH" in joined,
            "detail": "adopt-or-demote fork is explicit",
        },
        {
            "check_id": "VAL4072_06_next_target",
            "passed": "4073-Y5-R2FR-formal-adoption-or-demotion-of-motion-frame-gauge-parent.md" in joined,
            "detail": "next target decides formal adoption or demotion",
        },
        {"check_id": "VAL4072_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4072 - Local Motion-Frame Gauge Action Or Effective-GR Demotion

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## What Was Written

4072 writes the actual parent-action candidate that 4071 demanded:

```text
Q_4072 = {{X^A=L_* Psi^A, B^A, omega^AB, eta_AB, kappa_eff, A_3, matter, EM, auxiliary fields}}

e^A = D_omega X^A + B^A
g_obs = eta_AB e^A e^B

S_EC = (4 kappa_eff)^-1 ∫ epsilon_ABCD e^A∧e^B∧R^CD[omega]
      - (Lambda_eff / 12 kappa_eff) ∫ epsilon_ABCD e^A∧e^B∧e^C∧e^D
```

with optional torsion constraint/stiffness, topological `kappa_eff`, same-coframe matter/EM, and a memory-invariant sector.

## What Closed

- The action form is now explicit.
- The gauge transformation law is explicit.
- The route from Cartan action to EH, then to 4063 Newton/PPN readout, is explicit.
- The exact-gradient flatness trap is avoided by `B^A`.

## What Did Not Close

The current MTS corpus does **not** yet derive this action. It contains motion/flow/memory/frame clues, but not a parent-signed local motion-frame gauge action.

So the honest status is:

```text
motion_frame_gauge_action = formal_private_candidate
current_MTS_derivation = false
effective_GR_demotion = active_if_not_adopted_or_derived
```

## Fork

Either:

1. adopt/derive this as MTS parent infrastructure, then continue closing torsion, EM-Hodge, same-coframe, and kappa gates; or
2. demote the Cartan/EH local branch to an effective-GR input and keep MTS as a residual/testable extension around it.

## Next

`4073` should decide formal adoption or demotion in the workbench, rather than leaving this fork vague.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    action_candidate = action_candidate_rows(current_timestamp)
    gauge_variation = gauge_variation_rows(current_timestamp)
    reduction_chain = reduction_chain_rows(current_timestamp)
    demotion_matrix = demotion_matrix_rows(current_timestamp)
    residual_interface = residual_interface_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["action_candidate"], action_candidate)
    write_csv(OUTPUTS["gauge_variation"], gauge_variation)
    write_csv(OUTPUTS["reduction_chain"], reduction_chain)
    write_csv(OUTPUTS["demotion_matrix"], demotion_matrix)
    write_csv(OUTPUTS["residual_interface"], residual_interface)
    write_csv(OUTPUTS["decision_gate"], static["decision_gate"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["action_candidate"],
        OUTPUTS["gauge_variation"],
        OUTPUTS["reduction_chain"],
        OUTPUTS["demotion_matrix"],
        OUTPUTS["residual_interface"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        action_candidate,
        gauge_variation,
        reduction_chain,
        demotion_matrix,
        residual_interface,
        static["decision_gate"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, row_groups)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
