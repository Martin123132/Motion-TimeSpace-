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
DOC_PATH = ROOT / "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md"

DECISION = "PURE_GRADIENT_COFRAME_FLATNESS_OBSTRUCTION_FOUND_CARTAN_SOLDER_PARENT_ROUTE_CONSTRUCTED_CONDITIONALLY"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4070_00_4069_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4069_NEXT_TARGET.csv",
        "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate",
        "4069 selected the psi-packet/coframe parent-action gate.",
    ),
    "SRC4070_01_4069_coframe": (
        SOURCE_DIR / "P8_Y5_R2FR_4069_PSI_PACKET_COFRAME_REPAIR_THEOREM.csv",
        "COF4069_0_metric_induction",
        "4069 proves conditional Lorentzian metric induction from a rank-four packet coframe.",
    ),
    "SRC4070_02_4069_extra_modes": (
        SOURCE_DIR / "P8_Y5_R2FR_4069_EH_NORMAL_FORM_GATE.csv",
        "EHNF4069_1_extra_mode_silence",
        "4069 makes torsion/extra-mode silence an EH gate.",
    ),
    "SRC4070_03_4069_norm_req": (
        SOURCE_DIR / "P8_Y5_R2FR_4069_PARENT_REQUIREMENTS.csv",
        "REQ4069_2_normalization",
        "4069 marks normalization as a P0 parent requirement.",
    ),
    "SRC4070_04_units_Lstar": (
        FORMALIZATION / "09-canonical-notation-and-units.md",
        "Metric covariance normalization",
        "canonical notation already introduced L_* as the metric normalization length.",
    ),
    "SRC4070_05_observer_coframe": (
        ROOT / "10-observer-map-symplectic-contract.md",
        "The local observer coframe must be defined",
        "observer map contract requires coframe definition before PPN claims.",
    ),
    "SRC4070_06_covariant_frame": (
        ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "CFA1003_1_quotient_coframe_descent",
        "1003 records conditional coframe descent and frame leak gates.",
    ),
    "SRC4070_07_owner_connection": (
        FORMALIZATION / "141-doubled-owner-connection-current-primitive.md",
        "independent_owner_connection",
        "141 identifies independent owner connection as a useful primitive.",
    ),
    "SRC4070_08_solder_gate": (
        FORMALIZATION / "142-owner-spacetime-solder-map-theorem.md",
        "owner_spacetime_solder_map_bulk_hybrid_fails_boundary_topological_backup_open",
        "142 shows solder/projection is the obstruction for prior owner-connection routes.",
    ),
    "SRC4070_09_independent_coframe_solder": (
        FORMALIZATION / "142-owner-spacetime-solder-map-theorem.md",
        "Independent coframe solder",
        "142 separately audits independent coframe solder.",
    ),
    "SRC4070_10_EH_core": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "A511_0_EH_core",
        "minimal local GR parent blocks contain the EH core.",
    ),
    "SRC4070_11_kappa_top": (
        SOURCE_DIR / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
        "T508_1_topological_zeroform",
        "constant kappa can be topological if parent-owned.",
    ),
    "SRC4070_12_torsion": (
        SOURCE_DIR / "P8_Y5_axial_torsion_stiffness_status.csv",
        "axial_torsion_stiffness_and_response",
        "axial torsion stiffness remains symbolic nonclaim.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4070_SOURCE_REGISTER.csv",
    "gradient_obstruction": SOURCE_DIR / "P8_Y5_R2FR_4070_EXACT_GRADIENT_FLATNESS_OBSTRUCTION.csv",
    "cartan_action": SOURCE_DIR / "P8_Y5_R2FR_4070_CARTAN_SOLDER_PARENT_ACTION.csv",
    "normalization_gate": SOURCE_DIR / "P8_Y5_R2FR_4070_NORMALIZATION_GATE.csv",
    "torsion_gate": SOURCE_DIR / "P8_Y5_R2FR_4070_TORSION_EXTRA_MODE_GATE.csv",
    "eh_chain": SOURCE_DIR / "P8_Y5_R2FR_4070_EH_REDUCTION_CHAIN.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4070_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4070_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4070_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4070_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4070_VALIDATION.csv",
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


def gradient_obstruction_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "test_id": "GFO4070_0_exact_scalar_coframe",
            "candidate": "e^A = dX^A with X^A = L_* Psi^A and det(dX) != 0",
            "result": "FAILS_CURVED_GR",
            "proof": "If dX is invertible, X^A are local coordinates and g = eta_AB dX^A dX^B is the pullback of flat eta_AB; therefore Riemann[g]=0 locally.",
            "impact": "rank/signature are repaired, but curvature/EH dynamics are killed if the coframe is only exact scalar gradients.",
            "required_repair": "add a genuine solder/translation connection or independent coframe sector; do not claim curved GR from exact gradients alone",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "GFO4070_1_covariant_derivative_without_translation",
            "candidate": "e^A = D_omega X^A = dX^A + omega^A_B X^B",
            "result": "INCOMPLETE_AND_TORSION_RISK",
            "proof": "D_omega e^A = R^A_B[omega] X^B, so nontrivial curvature enters through the spin connection, but torsion/connection equations must be owned and constrained.",
            "impact": "connection can avoid flatness, but without an action it is a new unowned geometry sector",
            "required_repair": "write parent Palatini/Cartan action and torsion gate",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "GFO4070_2_background_eta",
            "candidate": "g_mu_nu = eta_mu_nu + L_*^2 <partial_mu psi partial_nu psi>",
            "result": "WEAK_FIELD_ANSATZ_ONLY",
            "proof": "The fixed eta_mu_nu supplies causal structure and cannot be the full background-independent observed metric; it remains useful only as a local tangent/weak-field expansion.",
            "impact": "old notation must be rewritten as internal eta_AB plus a coframe if the route is retained",
            "required_repair": "use g_obs = eta_AB e^A e^B with eta_AB internal, not a fixed spacetime metric",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def cartan_action_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "block_id": "CSA4070_0_field_content",
            "parent_block": "Phi_parent^4070 = (X^A=L_* Psi^A, B^A, omega^AB, kappa_eff, matter/EM, auxiliary silence fields)",
            "role": "minimal Cartan/solder parent candidate for the 4069 psi-packet route",
            "variation_or_identity": "e^A := D_omega X^A + B^A; g_obs := eta_AB e^A e^B",
            "status": "CONSTRUCTED_AS_CONDITIONAL_PARENT_CANDIDATE",
            "remaining_gap": "B^A/omega^AB must be justified as MTS motion-connection infrastructure, not arbitrary imported tetrad GR",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "CSA4070_1_solder_connection",
            "parent_block": "B^A translational/solder one-form",
            "role": "breaks exact-gradient flatness while preserving the psi packet as clock/motion coordinate data",
            "variation_or_identity": "in unitary gauge X^A=0, e^A=B^A; outside that gauge e^A is covariant under internal frame transformations",
            "status": "NECESSARY_REPAIR_IDENTIFIED",
            "remaining_gap": "must derive or motivate B^A from MTS flow/transport variables",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "CSA4070_2_gravity_action",
            "parent_block": "S_EC[e,omega;kappa] = (1/4 kappa_eff) int epsilon_ABCD e^A wedge e^B wedge R^CD[omega]",
            "role": "Palatini/Einstein-Cartan parent form that reduces to EH if torsion is constrained or spinless",
            "variation_or_identity": "delta_omega gives torsion equation; delta_e gives Einstein equation in tetrad form after torsion resolution",
            "status": "STANDARD_GR_REDUCTION_ROUTE_CONDITIONAL",
            "remaining_gap": "MTS must own why this is the IR normal form rather than merely importing GR",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "CSA4070_3_torsion_constraint",
            "parent_block": "S_T = int lambda_A wedge T^A or torsion mass/stiffness sector",
            "role": "prevents unbounded torsion/PPN/preferred-frame leakage in the local branch",
            "variation_or_identity": "T^A := D_omega e^A = 0 or T^A suppressed by positive stiffness",
            "status": "GATE_REQUIRED_NOT_CLAIMED",
            "remaining_gap": "axial torsion stiffness is symbolic only; parent coefficients must be signed or torsion set to zero by constraint",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "block_id": "CSA4070_4_matter",
            "parent_block": "S_matter[Psi_matter,e,omega_or_LC[e]] + S_EM[A,e]",
            "role": "same observed coframe for matter, EM, clocks, PPN, and orbital readouts",
            "variation_or_identity": "Hilbert/coframe stress is the same source used in local Newton/PPN branch",
            "status": "CARRIES_FORWARD_SAME_COFRAME_GATE",
            "remaining_gap": "no shadow coframe/frame/source prefactor theorem remains unsigned",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def normalization_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "norm_id": "N4070_0_X_length",
            "quantity": "X^A = L_* Psi^A",
            "dimension_rule": "Psi^A dimensionless phase/strain; L_* has length; X^A has length",
            "status": "DIMENSIONALLY_CLEAN",
            "claim_limit": "L_* is not numerically derived",
            "acceptance_test": "parent action must derive, topologically fix, or explicitly calibrate L_* without species/source labels",
            "timestamp_utc": current_timestamp,
        },
        {
            "norm_id": "N4070_1_coframe",
            "quantity": "e^A_mu = D_mu X^A + B^A_mu",
            "dimension_rule": "e^A_mu is dimensionless if coordinate x^mu has length and B^A_mu is dimensionless in the same convention",
            "status": "CONVENTION_READY",
            "claim_limit": "normalization convention must be declared before comparing PPN/clock/orbital sectors",
            "acceptance_test": "all matter/EM/readout terms use the same e^A_mu normalization",
            "timestamp_utc": current_timestamp,
        },
        {
            "norm_id": "N4070_2_kappa",
            "quantity": "kappa_eff and G_N = c^4 kappa_eff/(8*pi)",
            "dimension_rule": "kappa_eff is the EH coefficient; G_N remains calibrated unless parent scale theorem derives it",
            "status": "CALIBRATION_FIREWALL_RETAINED",
            "claim_limit": "no numerical Newton-G prediction",
            "acceptance_test": "close topological/superselection kappa route or keep G_N as measured input",
            "timestamp_utc": current_timestamp,
        },
        {
            "norm_id": "N4070_3_planck_scale",
            "quantity": "induced EH coefficient from integrating out psi packet modes",
            "dimension_rule": "would require a real heat-kernel/induced-gravity coefficient or parent normal-form theorem",
            "status": "NOT_DERIVED",
            "claim_limit": "cannot claim induced Planck scale from 4070",
            "acceptance_test": "derive coefficient from parent spectrum/cutoff/gap, or explicitly demote to calibrated GR branch",
            "timestamp_utc": current_timestamp,
        },
    ]


def torsion_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "TEX4070_0_torsion_zero",
            "mode": "torsion T^A",
            "required_condition": "T^A = D_omega e^A vanishes in local spinless branch or is suppressed below PPN/R10/clock/orbital locks",
            "route": "lambda_A wedge T^A constraint, Palatini spinless solution, or positive torsion stiffness",
            "status": "REQUIRED_NOT_PARENT_SIGNED",
            "residual_if_open": "epsilon_torsion_PPN; epsilon_axial_torsion_spin; preferred_frame_leak",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "TEX4070_1_nonmetricity",
            "mode": "nonmetricity Q_AB = -D_omega eta_AB",
            "required_condition": "D_omega eta_AB = 0 or nonmetricity is heavy/silent",
            "route": "internal Lorentz connection omega^AB=-omega^BA",
            "status": "CLOSABLE_BY_ANTISYMMETRIC_SPIN_CONNECTION_IF_PARENT_SIGNED",
            "residual_if_open": "clock/EM/PPN frame drift",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "TEX4070_2_extra_packet_modes",
            "mode": "packet amplitude/orientation/noise modes not contained in e^A",
            "required_condition": "extra modes are vertical q_parent fibres, massive, or residualized",
            "route": "quotient chain rule plus positive Hessian/gap",
            "status": "OPEN_BUT_TYPED",
            "residual_if_open": "fifth-force/source-normalization/local metric leakage",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "TEX4070_3_higher_curvature",
            "mode": "R^2, Ricci^2, Weyl^2, boundary/topological curvature terms",
            "required_condition": "coefficients vanish/double-zero, are topological, or are bounded below empirical locks",
            "route": "normal-form truncation plus R11 operator gate",
            "status": "OPEN_RESIDUAL_GATE",
            "residual_if_open": "R10/PPN/orbital deviations",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def eh_chain_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "step_id": "CHAIN4070_0",
            "premise": "rank-four psi packet plus Cartan solder field",
            "derivation": "e^A = D_omega X^A + B^A; g_obs = eta_AB e^A e^B",
            "result": "nondegenerate Lorentzian observed metric if det(e)!=0",
            "status": "CONDITIONAL_METRIC_DERIVED",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "CHAIN4070_1",
            "premise": "Einstein-Cartan/Palatini two-derivative parent normal form",
            "derivation": "S_EC[e,omega] = (1/4 kappa_eff) int epsilon e e R[omega]",
            "result": "tetrad Einstein equations after torsion/nonmetricity constraints",
            "status": "CONDITIONAL_GR_FORM",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "CHAIN4070_2",
            "premise": "torsion-free or spinless Palatini branch",
            "derivation": "omega = omega_LC[e] and S_EC[e,omega_LC] = S_EH[g_obs] plus boundary",
            "result": "EH metric action recovered",
            "status": "CONDITIONAL_EH_RECOVERY",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "CHAIN4070_3",
            "premise": "same coframe matter/EM and calibrated kappa_eff",
            "derivation": "delta_e S_matter and S_EM define the same Hilbert/coframe stress used by weak-field readout",
            "result": "routes back into 4063 Newton/PPN readout without separate source smuggling",
            "status": "CONDITIONAL_LINK_TO_4063",
            "timestamp_utc": current_timestamp,
        },
        {
            "step_id": "CHAIN4070_4",
            "premise": "parent ownership of B^A, omega^AB, L_*, kappa_eff, and silence gates",
            "derivation": "all new geometry infrastructure is owned by the MTS parent action rather than imported after the fact",
            "result": "would promote the route from effective branch to genuine MTS-to-GR derivation",
            "status": "OPEN_PROMOTION_GATE",
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision_gate": [
            {
                "decision_id": "DEC4070_0",
                "decision": DECISION,
                "summary": "4070 finds that pure exact-gradient coframes are locally flat and cannot derive curved GR, then constructs the viable Cartan solder parent route e^A=D_omega X^A+B^A with Palatini/EH reduction gates.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
            {
                "decision_id": "DEC4070_1",
                "decision": "NEXT_MUST_DERIVE_OR_DEMOTE_SOLDER_CONNECTION",
                "summary": "The GR bridge now depends on whether B^A/omega^AB/L_* can be parent-owned MTS motion-connection infrastructure rather than imported tetrad GR.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4070_0",
                "claim": "exact scalar gradients alone derive curved local GR",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "exact-gradient rank-four coframe is locally a coordinate pullback of flat eta_AB, so Riemann[g]=0",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4070_1",
                "claim": "Cartan solder parent route can conditionally connect psi packet to EH",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "requires parent-owned B^A/omega^AB/L_*, torsion/nonmetricity silence, same coframe matter, and calibrated kappa",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4070_2",
                "claim": "MTS has completed the derivation of GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "solder connection ownership and extra-mode gates remain open",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4070_3",
                "claim": "MTS predicts numerical Newton G",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "L_* and kappa_eff are not numerically derived in 4070",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4070_0",
                "next_doc": "4071-Y5-R2FR-Cartan-solder-field-origin-from-MTS-flow-or-demotion.md",
                "next_script": "scripts/Y5_R2FR_4071_Cartan_solder_field_origin_from_MTS_flow_or_demotion.py",
                "reason": "derive B^A and omega^AB from MTS motion/flow/memory variables, or demote the Cartan coframe to an explicit effective-GR branch input",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4070",
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
        {"check_id": "VAL4070_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4070_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4070_02_no_public_or_github_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4070_03_gradient_flatness_obstruction",
            "passed": "FAILS_CURVED_GR" in joined and "Riemann[g]=0" in joined,
            "detail": "pure exact-gradient coframe is rejected as a curved-GR derivation",
        },
        {
            "check_id": "VAL4070_04_cartan_route",
            "passed": "e^A := D_omega X^A + B^A" in joined and "CONSTRUCTED_AS_CONDITIONAL_PARENT_CANDIDATE" in joined,
            "detail": "Cartan solder parent route is constructed conditionally",
        },
        {
            "check_id": "VAL4070_05_torsion_gate",
            "passed": "TEX4070_0_torsion_zero" in joined and "REQUIRED_NOT_PARENT_SIGNED" in joined,
            "detail": "torsion/extra-mode gate remains explicit and nonclaim",
        },
        {
            "check_id": "VAL4070_06_next_target",
            "passed": "4071-Y5-R2FR-Cartan-solder-field-origin-from-MTS-flow-or-demotion.md" in joined,
            "detail": "next target attacks origin of Cartan solder field",
        },
        {"check_id": "VAL4070_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4070 - Psi Packet Coframe Parent Action, Normalization, And Torsion Gate

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## The Trap We Caught

The 4069 `psi`-packet coframe fixes the rank/signature problem, but the most obvious version still fails:

```text
e^A = dX^A,   g_obs = eta_AB dX^A dX^B.
```

If `det(dX) != 0`, then `X^A` are local coordinates and `g_obs` is just a pullback of flat internal Minkowski space. That gives `Riemann[g_obs]=0` locally, not curved GR.

So exact scalar gradients alone do **not** derive local GR. That old path is dead.

## Viable Repair

4070 keeps the route alive by making the needed geometry explicit:

```text
X^A = L_* Psi^A
e^A = D_omega X^A + B^A
g_obs = eta_AB e^A e^B
```

Here `B^A` is a translational/solder one-form and `omega^AB` is an internal Lorentz spin connection. This is the minimal Cartan/Palatini-style parent route that can avoid exact-gradient flatness.

## EH Reduction Chain

The conditional route is now:

```text
psi packet + Cartan solder field
-> nondegenerate Lorentzian coframe e^A
-> Einstein-Cartan / Palatini action
-> torsion-free or spinless branch
-> EH[g_obs] + boundary
-> 4063 weak-field Newton/PPN readout
```

This is not a completed MTS derivation yet. The new required derivation is sharper:

```text
derive B^A and omega^AB from MTS motion/flow/memory variables,
or demote them as effective-GR branch inputs.
```

## Hard Claim Limits

- No exact-gradient curved-GR claim.
- No public local-GR/Newton/PPN claim.
- No numerical Newton-G prediction.
- No torsion/extra-mode pass until the Cartan fields are parent-owned and constrained.

## Next

`4071` should attack the origin of the Cartan solder field: can `B^A` and `omega^AB` be derived from MTS flow/memory/transport variables, or are they imported GR infrastructure?
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    gradient_obstruction = gradient_obstruction_rows(current_timestamp)
    cartan_action = cartan_action_rows(current_timestamp)
    normalization_gate = normalization_gate_rows(current_timestamp)
    torsion_gate = torsion_gate_rows(current_timestamp)
    eh_chain = eh_chain_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["gradient_obstruction"], gradient_obstruction)
    write_csv(OUTPUTS["cartan_action"], cartan_action)
    write_csv(OUTPUTS["normalization_gate"], normalization_gate)
    write_csv(OUTPUTS["torsion_gate"], torsion_gate)
    write_csv(OUTPUTS["eh_chain"], eh_chain)
    write_csv(OUTPUTS["decision_gate"], static["decision_gate"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["gradient_obstruction"],
        OUTPUTS["cartan_action"],
        OUTPUTS["normalization_gate"],
        OUTPUTS["torsion_gate"],
        OUTPUTS["eh_chain"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        gradient_obstruction,
        cartan_action,
        normalization_gate,
        torsion_gate,
        eh_chain,
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
