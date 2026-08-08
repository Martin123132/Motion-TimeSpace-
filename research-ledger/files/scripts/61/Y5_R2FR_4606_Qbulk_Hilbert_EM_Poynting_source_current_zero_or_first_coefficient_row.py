from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4606"
CLAIM_ID = "L-448"
BRANCH_ID = "MTS_R2FR_Y5_QBULK_HILBERT_EM_POYNTING_GATE_4606"
MARKER = "PPC4161_QBULK_HILBERT_EM_POYNTING_SOURCE_CURRENT_ZERO_OR_FIRST_COEFFICIENT_ROW_4606"
PACKET_MARKER = "PPC4161_PACKET_QBULK_HILBERT_EM_POYNTING_GATE_4606"
DECISION = "QBULK_HILBERT_EM_POYNTING_ZERO_OR_COEFFICIENT_SCHEMA_READY_NONCLAIM"
NEXT_TARGET = "4607-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"

DOC_PATH = POST / "4606-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
FORMAL_PATH = FORMAL / "622-PPC4161-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4606_SOURCE_REGISTER.csv"
QBULK_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_SOURCE_CURRENT_THEOREM.csv"
HILBERT_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_HILBERT_ROWS.csv"
EM_POYNTING_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_EM_POYNTING_ROWS.csv"
RETAINED_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_RETAINED_ROWS.csv"
QBULK_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_UPDATE_ROWS.csv"
QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_QBARXH_BULK_UPDATE_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4606_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4606_VALIDATION.csv"

DOC_4605 = POST / "4605-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
FORMAL_621 = FORMAL / "621-PPC4161-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
CSV_4605_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4605_NEXT_TARGET.csv"
CSV_4605_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4605_SOURCE_NUMERATOR_THEOREM.csv"
CSV_4605_BULK = SOURCE_DIR / "P8_Y5_R2FR_4605_QBULK_COMPONENT_ROWS.csv"
CSV_4605_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4605_QBARXH_NUMERATOR_UPDATE_ROWS.csv"
CSV_4520_SILENCE = SOURCE_DIR / "P8_Y5_R2FR_4520_RANK_ZERO_SOURCE_CURRENT_SILENCE_THEOREM.csv"
CSV_4530_DESCENT = SOURCE_DIR / "P8_Y5_R2FR_4530_SOURCE_CURRENT_DESCENT_IDENTITY.csv"
CSV_4587_DENSITY = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv"
CSV_4587_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_POYNTING_RESIDUAL_VECTOR.csv"
CSV_4587_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4587_POYNTING_OWNER_LOCK.csv"
CSV_4588_REYNOLDS = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv"
CSV_WARD_CONTRACT = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
CSV_WARD_BRIDGE = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv"
CSV_EM_ELLJ = SOURCE_DIR / "P8_EM_ellJ_source_current_owner_residual_law.csv"
CSV_2642_PROOF = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv"
CSV_2642_BOUND = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv"
CSV_2617_IDENTITY = SOURCE_DIR / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv"
CSV_4514_TAILS = SOURCE_DIR / "P8_Y5_R2FR_4514_REMAINING_SOURCE_TAIL_LEDGER.csv"
CSV_4440_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_CHARGE_CLOSURE_OUTPUT.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ").replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4606 sharpens the Q_bulk source-current numerator: ordinary Hilbert matter and Maxwell/EM Poynting stress vanish as independent bulk sources only on one q-basic, same-coframe, no-marker, no-source-weight, no-flux parent branch; otherwise explicit Hilbert, EM/Poynting and retained source coefficient rows feed Q_bulk_abs.",
        "current_evidence": "Generated Q_bulk theorem rows, Hilbert rows, EM/Poynting rows, retained-source rows, Q_bulk update, Qbar_XH update, blockers, controls and validation.",
        "status": "Qbulk_Hilbert_EM_Poynting_zero_or_coefficient_schema_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Double-counting Poynting as a new source after it is already Hilbert EM stress, or erasing radiative/nonminimal EM wall flux without a no-flux/Hodge theorem.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until Hilbert/EM/retained bulk rows, edge/shadow rows, denominator/projector, qbar_XT and arena kernels are zero or source-backed.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4606_00_4605_doc", DOC_4605, "4606-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md", "4605 selected Q_bulk target."),
        ("SRC4606_01_621_formal", FORMAL_621, "Q_bulk=0 on the same q-basic ordinary-source plus EM/Poynting branch", "formal bulk handoff."),
        ("SRC4606_02_4605_next", CSV_4605_NEXT, "4606-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md", "machine next target."),
        ("SRC4606_03_4605_theorem", CSV_4605_THEOREM, "NUM4605_1_bulk_zero", "bulk zero theorem handoff."),
        ("SRC4606_04_4605_bulk_hilbert", CSV_4605_BULK, "QB4605_0_Hilbert", "Q_bulk Hilbert row."),
        ("SRC4606_05_4605_bulk_em", CSV_4605_BULK, "QB4605_1_EM_Poynting", "Q_bulk EM/Poynting row."),
        ("SRC4606_06_4605_bulk_total", CSV_4605_BULK, "QB4605_TOTAL", "Q_bulk total row."),
        ("SRC4606_07_4605_qbar", CSV_4605_QBAR, "QU4605_1_Qbar_insert", "Qbar update from numerator."),
        ("SRC4606_08_4520_hilbert", CSV_4520_SILENCE, "RZSC4520_2_hilbert_matter", "Hilbert matter silence."),
        ("SRC4606_09_4520_poynting", CSV_4520_SILENCE, "RZSC4520_3_poynting", "EM/Poynting silence."),
        ("SRC4606_10_4520_retained", CSV_4520_SILENCE, "RZSC4520_4_retained", "retained exception."),
        ("SRC4606_11_4530_chain", CSV_4530_DESCENT, "J4530_0_full_variation_decomposition", "full chain-rule identity."),
        ("SRC4606_12_4530_weights", CSV_4530_DESCENT, "J4530_2_pre_action_weight_counterterm", "source-weight countermodel."),
        ("SRC4606_13_4587_density", CSV_4587_DENSITY, "DQT4587_1_qbasic_density_zero", "density q-basic theorem."),
        ("SRC4606_14_4587_residual", CSV_4587_RESIDUAL, "DRV4587_4_E_Poynting_boundary", "Poynting residual component."),
        ("SRC4606_15_4587_once", CSV_4587_POYNTING, "POY4587_1_once_only", "once-only Poynting lock."),
        ("SRC4606_16_4587_flux", CSV_4587_POYNTING, "POY4587_2_flux_boundary", "Poynting flux boundary row."),
        ("SRC4606_17_4588_shell", CSV_4588_REYNOLDS, "RST4588_2_shell_bound", "support shell handoff."),
        ("SRC4606_18_Ward_source", CSV_WARD_CONTRACT, "SC1_Hilbert_source_definition", "Hilbert source definition contract."),
        ("SRC4606_19_Ward_nonH", CSV_WARD_CONTRACT, "SC4_no_nonHilbert_source_current", "no non-Hilbert source current contract."),
        ("SRC4606_20_Ward_bridge", CSV_WARD_BRIDGE, "WB520_2_stationary_mass_generator", "stationary mass generator context."),
        ("SRC4606_21_EM_ellJ", CSV_EM_ELLJ, "EJR3513_1_R_md", "matter descent/source multiplier residual."),
        ("SRC4606_22_2642_JH", CSV_2642_PROOF, "SCI2642_1_JH_descent", "Hilbert source descent residual."),
        ("SRC4606_23_2642_bound", CSV_2642_BOUND, "SCB2642_1_eps_JH_Z_abs", "Hilbert source bound row."),
        ("SRC4606_24_2617_identity", CSV_2617_IDENTITY, "SMI2617_1_identity_source_map", "identity source-map theorem."),
        ("SRC4606_25_4514_Jmem", CSV_4514_TAILS, "STL4514_3_Jmem", "retained J_mem source current."),
        ("SRC4606_26_4440_source", CSV_4440_SOURCE, "SOURCE_CHARGE_REDUCED_TO_ACTION_MEASURE_CURRENT_CONTRACT", "source charge action-current context."),
        ("SRC4606_27_claim_447", CLAIMS_PATH, "L-447", "claim-register handoff from 4605."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": bool(line),
                "line_number": line,
                "role": role,
                "generated_utc": now,
                "valid_for_claim": False,
            }
        )
    return rows


def qbulk_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QBH4606_0_bulk_decomposition",
            "statement": "The bulk numerator splits into ordinary Hilbert, EM/Poynting, and retained/direct source pieces.",
            "formula": "Q_bulk = Q_Hilbert + Q_EM/Poynting + Q_retained",
            "derivation": "Refines 4605's Q_bulk row using 4520, 4530 and 4587 source-current splits.",
            "consequence": "The bulk source problem now has three named inputs instead of one undifferentiated coupling.",
            "status": "QBULK_SPLIT_DERIVED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QBH4606_1_Hilbert_zero",
            "statement": "Ordinary Hilbert bulk source vanishes along X only when the source action descends through the parent quotient before readout.",
            "formula": "D_v S_src = <delta Sbar_src/delta q,Dq[v]> + sum_A J_theta_A Lie_v theta_A + J_direct[v] + delta_v B; zero if all terms vanish",
            "derivation": "Direct chain-rule identity: q-basic source action plus Dq[v]=0 kills the quotient term; no-marker/no-direct/source-weight conditions kill the rest.",
            "consequence": "Dq verticality alone is not enough; source weights, constants and direct source slots remain live if unsigned.",
            "status": "EXACT_CONDITIONAL_HILBERT_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QBH4606_2_EM_Poynting_once_only",
            "statement": "Maxwell/Poynting is counted once as Hilbert EM stress if the EM action uses the public observed Hodge/coframe.",
            "formula": "S_EM=-1/(4 mu0) int sqrt(-g_obs) F^2; T_EM=Hilbert variation; S_Poynting^i=-T_EM^i_nu tau^nu",
            "derivation": "The Poynting vector is an energy-flux component of the same Hilbert stress tensor, not an extra independent source current.",
            "consequence": "An added background/Poynting source after T_EM would double-count unless it is a separate boundary/nonminimal residual row.",
            "status": "ONCE_ONLY_EM_SOURCE_LOCK_DERIVED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QBH4606_3_EM_Poynting_zero_or_flux",
            "statement": "EM/Poynting contributes no independent bulk source on a q-basic public-Maxwell no-flux worldtube; otherwise its contribution is a wall/Hodge/nonminimal coefficient.",
            "formula": "Q_EM=0 if D_v Hodge_obs=0, D_v theta_EM=0, no nonminimal source multiplier, and int_boundary T_EM(tau,n) dSigma dt=0",
            "derivation": "Combine 4520 Poynting silence with 4587 public-Hodge, once-only and boundary-flux rows.",
            "consequence": "The Poynting instinct is preserved but disciplined: it is either Hilbert flux, or an explicit coefficient to bound.",
            "status": "CONDITIONAL_EM_ZERO_OR_FLUX_BOUND_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QBH4606_4_absolute_bulk_bound",
            "statement": "If any bulk zero premise is unsigned, the bulk source current uses a no-cancellation coefficient envelope.",
            "formula": "|Q_bulk| <= |Q_Hilbert|_abs + |Q_EM/Poynting|_abs + |Q_retained|_abs",
            "derivation": "Triangle inequality; no cancellation between ordinary matter, EM/Poynting and retained source tails is credited.",
            "consequence": "Q_bulk is ready for first coefficient-row filling without pretending local GR is derived.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def hilbert_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "H4606_0_qbasic_action",
            "quantity": "epsilon_action_vertical",
            "zero_condition": "S_src=Sbar_src[q(Phi),Psi,theta] and Dq[v_X]=0 before readout",
            "bound_formula": "|Q_H_action| <= W_lambda_max M_ref |epsilon_action_vertical|",
            "required_inputs": "parent source action; quotient map; vertical generator; W_lambda_max; M_ref",
            "current_status": "ZERO_CONDITION_DEFINED_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "H4606_1_constants_markers",
            "quantity": "epsilon_constant_marker",
            "zero_condition": "Lie_v theta_A=0 for masses, alpha_EM, material/source labels and source scale",
            "bound_formula": "|Q_H_marker| <= W_lambda_max M_ref |epsilon_constant_marker|",
            "required_inputs": "no-marker theorem or source-backed marker sensitivities",
            "current_status": "ZERO_CONDITION_DEFINED_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "H4606_2_source_weights",
            "quantity": "epsilon_source_weight",
            "zero_condition": "no pre-action species/source weights w_A or source-only multipliers inside S_matter",
            "bound_formula": "|Q_H_weight| <= W_lambda_max sum_A |delta w_A| |S_A|",
            "required_inputs": "object-language source-weight ban or numeric w_A bounds",
            "current_status": "SOURCE_WEIGHT_ZERO_OR_BOUND_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "H4606_TOTAL",
            "quantity": "Q_bulk_Hilbert_abs",
            "zero_condition": "all Hilbert source action, marker and source-weight rows vanish in the same parent branch",
            "bound_formula": "|Q_bulk_Hilbert| <= W_lambda_max M_ref (|epsilon_action_vertical|+|epsilon_constant_marker|+|epsilon_source_weight|+|epsilon_matter_lift|)",
            "required_inputs": "all component zeros or source-backed values with units",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def em_poynting_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4606_0_public_Hodge",
            "quantity": "epsilon_Hodge_EM",
            "zero_condition": "EM action uses the public observed Hodge/coframe already varied in T_EM",
            "bound_formula": "|Q_EM_Hodge| <= W_lambda_max M_ref |epsilon_Hodge_EM|",
            "required_inputs": "same-Hodge theorem; no hidden second frame; EM units",
            "current_status": "PUBLIC_HODGE_ZERO_CONDITIONAL_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4606_1_once_only",
            "quantity": "c_Poynt_extra",
            "zero_condition": "T_total already includes T_EM and no extra background/Poynting source is added after variation",
            "bound_formula": "|Q_EM_extra| <= |c_Poynt_extra| |int_boundary S dot n|",
            "required_inputs": "single source functional branch or numeric extra-flux coefficient",
            "current_status": "ONCE_ONLY_ZERO_CONDITIONAL_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4606_2_wall_flux",
            "quantity": "Phi_wall_Poynting",
            "zero_condition": "stationary/no-flux source collar: int_boundary T_EM(tau,n_boundary) dSigma dt=0",
            "bound_formula": "|Q_EM_flux| <= W_lambda_max |int_boundary T_EM(tau,n_boundary) dSigma dt|",
            "required_inputs": "source collar; tau; boundary normal; EM stress flux; time window",
            "current_status": "WALL_FLUX_ZERO_OR_NUMERIC_BOUND_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4606_3_nonminimal",
            "quantity": "epsilon_nonminimal_EM",
            "zero_condition": "no nonminimal EM/current coupling creates an independent source weight",
            "bound_formula": "|Q_EM_nonminimal| <= W_lambda_max M_ref |epsilon_nonminimal_EM|",
            "required_inputs": "unique Maxwell block theorem or coefficient row for F^2/source multiplier",
            "current_status": "NONMINIMAL_EM_ZERO_OR_BOUND_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4606_TOTAL",
            "quantity": "Q_bulk_EM_Poynting_abs",
            "zero_condition": "public Hodge, once-only source functional, no wall flux and no nonminimal EM route in one branch",
            "bound_formula": "|Q_bulk_EM/Poynting| <= W_lambda_max (M_ref|epsilon_Hodge_EM| + |c_Poynt_extra Phi_wall| + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|)",
            "required_inputs": "all EM/Poynting component zeros or source-backed coefficient rows",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def retained_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R4606_0_direct",
            "quantity": "J_direct_abs",
            "zero_condition": "no direct retained source current or material source marker outside the Hilbert action",
            "bound_formula": "|Q_direct| <= W_lambda_max |J_direct_abs|",
            "required_inputs": "direct source inventory or no-direct-source theorem",
            "current_status": "DIRECT_RETAINED_SOURCE_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R4606_1_memory",
            "quantity": "J_mem_abs",
            "zero_condition": "memory kernel has no direct source slot in the local branch",
            "bound_formula": "|Q_mem| <= W_lambda_max |J_mem_abs|",
            "required_inputs": "memory source-current owner theorem or coefficient row",
            "current_status": "JMEM_ZERO_OR_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R4606_2_readout",
            "quantity": "J_readout_abs",
            "zero_condition": "readout is post-solution and fixed before variation with no source backreaction",
            "bound_formula": "|Q_readout| <= W_lambda_max |J_readout_abs|",
            "required_inputs": "variation-before-readout proof or readout coefficient row",
            "current_status": "READOUT_SOURCE_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "R4606_TOTAL",
            "quantity": "Q_bulk_retained_abs",
            "zero_condition": "all retained/direct/memory/readout bulk source rows vanish in one parent branch",
            "bound_formula": "|Q_bulk_retained| <= W_lambda_max(|J_direct_abs|+|J_mem_abs|+|J_marker_abs|+|J_readout_abs|)",
            "required_inputs": "all retained source zeros or coefficient rows",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbulk_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BU4606_0_zero_route",
            "quantity": "Q_bulk",
            "formula": "Q_bulk=0 if Q_bulk_Hilbert=Q_bulk_EM/Poynting=Q_bulk_retained=0 in the same parent branch",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BU4606_1_absolute_bound",
            "quantity": "Q_bulk_abs",
            "formula": "|Q_bulk| <= |Q_bulk_Hilbert| + |Q_bulk_EM/Poynting| + |Q_bulk_retained|",
            "current_status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbar_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBU4606_0_Qbar_bulk_insert",
            "quantity": "Qbar_XH_abs",
            "formula": "|Qbar_XH| <= (||Pi_M||(|Q_bulk_Hilbert|+|Q_bulk_EM/Poynting|+|Q_bulk_retained|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "current_status": "QBAR_SCHEMA_REFINED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        }
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4606_0_Hilbert",
            "missing_object": "ordinary Hilbert source q-basic/no-marker/no-source-weight proof or coefficients",
            "why_it_matters": "without this, ordinary matter can carry the X source current",
            "best_next_action": "fill or prove Hilbert action, marker and source-weight rows",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4606_1_EM_Poynting",
            "missing_object": "public Maxwell-Hodge, once-only source functional, wall flux and nonminimal EM rows",
            "why_it_matters": "this decides whether Poynting is already Hilbert stress or a live wall/source residual",
            "best_next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4606_2_retained",
            "missing_object": "direct, memory, marker and readout retained source rows",
            "why_it_matters": "these are the legal ways bulk source current can survive after Hilbert/EM descent",
            "best_next_action": "source retained current inventory after EM/Poynting wall flux is settled",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4606_3_downstream",
            "missing_object": "Q_edge/Q_shadow, M_lower/Pi_M, qbar_XT and arena kernels",
            "why_it_matters": "Q_bulk alone is still not an empirical local-GR/R10 pass",
            "best_next_action": "defer until bulk coefficient rows are live",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4606_0_once_only_Poynting",
            "control": "If T_total already includes T_EM, no extra Poynting source is added unless it is declared as a boundary/nonminimal residual.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4606_1_no_verticality_shortcut",
            "control": "Dq[v_X]=0 does not zero Hilbert source unless marker constants, source weights, direct slots and boundary terms also vanish.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4606_2_no_cancellation",
            "control": "Hilbert, EM/Poynting and retained bulk pieces are absolute-summed.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4606_3_no_claim_from_schema",
            "control": "Bulk coefficient schemas do not imply local-GR, R10, PPN, clock or orbital success.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4606_0_Hilbert",
            "promotion_requirement": "Hilbert action, marker/source constants and source weights are zero or bounded.",
            "current_status": "FAIL_HILBERT_COMPONENT_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4606_1_EM",
            "promotion_requirement": "Public Maxwell-Hodge, once-only Poynting and wall flux/nonminimal rows are zero or bounded.",
            "current_status": "FAIL_EM_POYNTING_COMPONENT_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4606_2_retained",
            "promotion_requirement": "retained/direct/memory/readout source rows are zero or bounded.",
            "current_status": "FAIL_RETAINED_COMPONENT_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4606_3_empirical",
            "promotion_requirement": "Q_bulk_abs joins Q_edge/Q_shadow and downstream source/test/arena rows to form claim-grade I_X^ST.",
            "current_status": "FAIL_DOWNSTREAM_INPUTS_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "decision": DECISION,
            "reason": "Q_bulk now has explicit Hilbert, EM/Poynting and retained-source zero/bound routes; the EM/Poynting question is isolated as the sharpest next coefficient row.",
            "claim": "no R10/PPN/local-GR pass",
            "next_target": NEXT_TARGET,
            "generated_utc": now,
            "valid_for_claim": False,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "status": DECISION,
            "what_moved": "Poynting/EM is now formally either once-only Hilbert stress or a named wall/Hodge/nonminimal coefficient, not loose intuition.",
            "what_did_not_move": "No numeric bulk source amplitude, R10 alpha, PPN residual or local-GR pass is claimed.",
            "generated_utc": now,
            "valid_for_claim": False,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The cleanest next fork is Maxwell/Poynting: prove same-Hodge/no-wall-flux once-only ownership, or fill the wall-flux coefficient.",
            "derive_first": "derive public Maxwell-Hodge and no Poynting wall flux in the same source-worldtube branch",
            "fallback": "fill epsilon_Hodge_EM, c_Poynt_extra, Phi_wall_Poynting and epsilon_nonminimal_EM as nonclaim coefficient rows",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4606 - Y5 R2FR Qbulk Hilbert/EM/Poynting Source-Current Zero Or First Coefficient Row

Generated: `{now}`

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Claim register row: `{CLAIM_ID}`
Previous target: `{DOC_4605}`

## Result

4606 sharpens the bulk numerator:

```text
Q_bulk = Q_bulk_Hilbert + Q_bulk_EM/Poynting + Q_bulk_retained.
```

The strict zero route is:

```text
Q_bulk_Hilbert = 0
Q_bulk_EM/Poynting = 0
Q_bulk_retained = 0
    => Q_bulk = 0.
```

The important physical clause is:

```text
S_EM = -1/(4 mu0) int sqrt(-g_obs) F^2
T_EM = Hilbert variation of S_EM
S_Poynting^i = -T_EM^i_nu tau^nu
```

So Poynting is not a second hidden source when the public Maxwell-Hodge branch is active. It is already inside `T_EM`. If radiation/nonminimal EM flux crosses the source collar, it becomes an explicit wall/Hodge/nonminimal coefficient instead:

```text
|Q_bulk_EM/Poynting| <= W_lambda_max (
    M_ref |epsilon_Hodge_EM|
    + |c_Poynt_extra Phi_wall|
    + |Phi_wall_Poynting|
    + M_ref |epsilon_nonminimal_EM|
).
```

The bulk fallback is:

```text
|Q_bulk| <= |Q_bulk_Hilbert| + |Q_bulk_EM/Poynting| + |Q_bulk_retained|.
```

## Private Decision

`{DECISION}`

No R10, PPN, clock, orbital, EM, Newton or local-GR pass is claimed. The immediate best target is `{NEXT_TARGET}`.

## Source Register

{markdown_table(tables["sources"])}

## Qbulk Source-Current Theorem

{markdown_table(tables["theorem"])}

## Hilbert Rows

{markdown_table(tables["hilbert"])}

## EM/Poynting Rows

{markdown_table(tables["em_poynting"])}

## Retained Rows

{markdown_table(tables["retained"])}

## Qbulk Update Rows

{markdown_table(tables["qbulk_update"])}

## QbarXH Bulk Update Rows

{markdown_table(tables["qbar_update"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Controls

{markdown_table(tables["controls"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

{markdown_table(tables["next"])}
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 622 - Qbulk Hilbert/EM/Poynting Source-Current Zero Or First Coefficient Row

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

The bulk source numerator is:

```text
Q_bulk = Q_bulk_Hilbert + Q_bulk_EM/Poynting + Q_bulk_retained.
```

Ordinary Hilbert zero:

```text
D_v S_src = 0
```

only when the source action descends through `q`, `Dq[v_X]=0`, marker constants are vertical-silent, and no source-only weights/direct source slots survive.

EM/Poynting once-only lock:

```text
S_EM=-1/(4 mu0) int sqrt(-g_obs) F^2,
T_EM=Hilbert variation,
S_Poynting^i=-T_EM^i_nu tau^nu.
```

Therefore Poynting is already counted in the Hilbert EM stress on the public Maxwell-Hodge branch. If wall flux or nonminimal EM survives:

```text
|Q_bulk_EM/Poynting| <= W_lambda_max(M_ref|epsilon_Hodge_EM|+|c_Poynt_extra Phi_wall|+|Phi_wall_Poynting|+M_ref|epsilon_nonminimal_EM|).
```

Bulk bound:

```text
|Q_bulk| <= |Q_bulk_Hilbert| + |Q_bulk_EM/Poynting| + |Q_bulk_retained|.
```

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4606_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4606_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")

    csv_paths = [SOURCE_REGISTER, QBULK_THEOREM_CSV, HILBERT_ROWS_CSV, EM_POYNTING_ROWS_CSV, RETAINED_ROWS_CSV, QBULK_UPDATE_CSV, QBAR_UPDATE_CSV, BLOCKERS_CSV, CONTROL_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4606_02_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    hilbert_text = "\n".join(str(row) for row in tables["hilbert"])
    em_text = "\n".join(str(row) for row in tables["em_poynting"])
    retained_text = "\n".join(str(row) for row in tables["retained"])
    add("VAL4606_03_qbulk_split", "Q_bulk = Q_Hilbert + Q_EM/Poynting + Q_retained" in theorem_text, "Qbulk split present")
    add("VAL4606_04_hilbert_conditions", "epsilon_source_weight" in hilbert_text and "epsilon_constant_marker" in hilbert_text, "Hilbert source conditions present")
    add("VAL4606_05_em_once_only", "c_Poynt_extra" in em_text and "Phi_wall_Poynting" in em_text and "ONCE_ONLY" in theorem_text, "EM/Poynting once-only and wall-flux rows present")
    add("VAL4606_06_retained_rows", "J_mem_abs" in retained_text and "J_readout_abs" in retained_text, "retained rows present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "numeric_value_present"} and value is True:
                    all_false = False
    add("VAL4606_07_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4606_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4606_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4606_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4606_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4606_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4606_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4606_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4606_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4606_OVERALL", all(row["status"] == "PASS" for row in rows), "4606 Qbulk Hilbert/EM/Poynting gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": qbulk_theorem_rows(now),
        "hilbert": hilbert_rows(now),
        "em_poynting": em_poynting_rows(now),
        "retained": retained_rows(now),
        "qbulk_update": qbulk_update_rows(now),
        "qbar_update": qbar_update_rows(now),
        "blockers": blocker_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(QBULK_THEOREM_CSV, tables["theorem"])
    write_csv(HILBERT_ROWS_CSV, tables["hilbert"])
    write_csv(EM_POYNTING_ROWS_CSV, tables["em_poynting"])
    write_csv(RETAINED_ROWS_CSV, tables["retained"])
    write_csv(QBULK_UPDATE_CSV, tables["qbulk_update"])
    write_csv(QBAR_UPDATE_CSV, tables["qbar_update"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])

    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - Qbulk Hilbert/EM/Poynting Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The bulk source-current numerator now splits into ordinary Hilbert source, Maxwell/EM Poynting stress, and retained source tails. Poynting is once-only Hilbert EM stress on the public Maxwell-Hodge branch; otherwise wall flux, Hodge leakage, extra Poynting coefficient and nonminimal EM source coupling are explicit nonclaim rows.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Qbulk Hilbert/EM/Poynting Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now routes `Q_bulk` through Hilbert, EM/Poynting and retained-source coefficient rows. The next target is the public Maxwell-Hodge/no-wall-flux fork rather than vague coupling language.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4606 validation failed: {failed}")
    print(f"4606 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
