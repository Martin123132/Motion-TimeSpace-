from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4714"
CLAIM_ID = "L-556"
MARKER = "PPC4161_EM_STRESS_POYNTING_CURRENT_OWNER_OR_SIDECHANNEL_BOUND_4714"
PACKET_MARKER = "PPC4161_PACKET_EM_STRESS_POYNTING_CURRENT_OWNER_OR_SIDECHANNEL_BOUND_4714"
DECISION = "MAXWELL_HODGE_POYNTING_REBASED_TO_CURRENT_BRANCH_SAME_CURRENT_AND_SIDECHANNEL_BOUNDS_RETAINED_NONCLAIM"
NEXT_TARGET = "4715-Y5-R2FR-same-current-charge-lattice-owner-or-source-test-bound.md"

DOC_PATH = POST / "4714-Y5-R2FR-EM-stress-Poynting-current-owner-or-sidechannel-bound.md"
FORMAL_PATH = FORMAL / "730-PPC4161-EM-stress-Poynting-current-owner-or-sidechannel-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4713_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4713_NEXT_TARGET.csv"
CSV_4713_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4713_NO_LINEAR_OWNER_THEOREM_ROWS.csv"
CSV_4713_LLINEAR = SOURCE_DIR / "P8_Y5_R2FR_4713_LLINEAR_BOUND_ROWS.csv"
CSV_4713_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4713_VALIDATION.csv"
DOC_4175 = POST / "4175-Y5-R2FR-Maxwell-Hodge-Poynting-stress-owner-theorem-or-EM-side-channel-bound.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
CSV_4175_ACTION = SOURCE_DIR / "P8_Y5_R2FR_4175_MAXWELL_HODGE_ACTION_VARIATION.csv"
CSV_4175_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4175_POYNTING_STRESS_IDENTIFICATION.csv"
CSV_4175_CONSERVATION = SOURCE_DIR / "P8_Y5_R2FR_4175_TOTAL_CONSERVATION_AND_LORENTZ_EXCHANGE.csv"
CSV_4175_SIDE = SOURCE_DIR / "P8_Y5_R2FR_4175_EM_SIDE_CHANNEL_CLOSE_OR_REACTIVATE.csv"
CSV_4175_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4175_BRANCH_DECISION.csv"
CSV_4694_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_SOURCE_CURRENT_THEOREM.csv"
CSV_4694_EM = SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_EM_POYNTING_ROWS.csv"
CSV_4695_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4695_EM_POYNTING_HODGE_FLUX_THEOREM.csv"
CSV_4695_HODGE = SOURCE_DIR / "P8_Y5_R2FR_4695_HODGE_OWNER_ROWS.csv"
CSV_4695_FLUX = SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv"
CSV_4696_RETAINED = SOURCE_DIR / "P8_Y5_R2FR_4696_RETAINED_BULK_SOURCE_CURRENT_THEOREM.csv"
CSV_4696_JMEM_EM = SOURCE_DIR / "P8_Y5_R2FR_4696_JMEM_EM_4695_INSERTION_ROWS.csv"
CSV_4696_JREADOUT = SOURCE_DIR / "P8_Y5_R2FR_4696_JREADOUT_ROWS.csv"
CSV_3222_GUARDS = SOURCE_DIR / "P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv"
CSV_765_MKI = SOURCE_DIR / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
CSV_765_RESCALE = SOURCE_DIR / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
CSV_988_EMLOCK = SOURCE_DIR / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv"
CSV_4702_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4702_GAUGE_OWNER_CLAUSES.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4714_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv"
CURRENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_CURRENT_CONSERVATION_EXCHANGE_ROWS.csv"
SIDECHANNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_SIDECHANNEL_BOUND_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4714_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4714_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once(timestamp: str) -> None:
    existing = text(CLAIMS_PATH)
    if existing.startswith(CLAIM_ID + ",") or f"\n{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4714 rebases the Maxwell-Hodge/Poynting stress theorem onto the current local branch and retains side-channel bounds for Hodge, current, boundary flux and nonminimal EM sources.",
        "current_evidence": "Generated source register, EM stress theorem rows, conservation/current rows, side-channel bound rows, gates, firewalls, decision, status, next target and validation.",
        "status": "em_stress_poynting_current_owner_conditional_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Counting Poynting twice, or treating scalar F_Q^2 coefficient silence as full EM stress/current/source-coupling closure.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "EM stress Poynting current owner or sidechannel bound",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or list(row)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writerow({field: row.get(field, "") for field in fields})


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4714_00_4713_next", CSV_4713_NEXT, "NT4713_0", "4713 handoff to EM stress/Poynting/current owner"),
        ("SRC4714_01_4713_same_branch", CSV_4713_THEOREM, "NLO4713_4_same_branch_clock_closure", "same-branch closure requires owner consistency"),
        ("SRC4714_02_4713_Llinear_arena", CSV_4713_LLINEAR, "LL4713_3_arena_transfer_bound", "arena transfer needs current/source maps"),
        ("SRC4714_03_4713_validation", CSV_4713_VALIDATION, "VAL4713_OVERALL", "4713 validation"),
        ("SRC4714_04_4175_doc", DOC_4175, "Poynting flux is already owned", "older Maxwell-Hodge/Poynting theorem"),
        ("SRC4714_05_191_formal", FORMAL_191, "Poynting vector is not a separate background field", "formal 191 theorem"),
        ("SRC4714_06_4175_action", CSV_4175_ACTION, "MH4175_2_Hilbert_stress", "Hilbert EM stress variation"),
        ("SRC4714_07_4175_poynting", CSV_4175_POYNTING, "PNT4175_2_flux", "Poynting identity"),
        ("SRC4714_08_4175_conservation", CSV_4175_CONSERVATION, "CONS4175_3_total", "total matter+EM conservation"),
        ("SRC4714_09_4175_boundary", CSV_4175_SIDE, "EMSC4175_4_boundary_flux", "radiative boundary flux routed, not zeroed"),
        ("SRC4714_10_4175_decision", CSV_4175_DECISION, "DEC4175_1_no_global", "private selector not global adoption"),
        ("SRC4714_11_4694_once", CSV_4694_THEOREM, "QBH4694_2_EM_Poynting_once_only", "Poynting counted once"),
        ("SRC4714_12_4694_zero_flux", CSV_4694_THEOREM, "QBH4694_3_EM_Poynting_zero_or_flux", "EM zero or flux bound"),
        ("SRC4714_13_4694_bound", CSV_4694_THEOREM, "QBH4694_4_absolute_bulk_bound", "bulk no-cancellation bound"),
        ("SRC4714_14_4694_em_total", CSV_4694_EM, "EM4694_TOTAL", "EM/Poynting total side-channel row"),
        ("SRC4714_15_4695_once", CSV_4695_THEOREM, "EMF4695_0_once_only", "once-only theorem"),
        ("SRC4714_16_4695_hodge", CSV_4695_THEOREM, "EMF4695_1_same_Hodge", "same-Hodge condition"),
        ("SRC4714_17_4695_flux", CSV_4695_THEOREM, "EMF4695_2_no_wall_flux", "wall flux condition"),
        ("SRC4714_18_4695_bound", CSV_4695_THEOREM, "EMF4695_3_finite_EM_bound", "finite EM bound"),
        ("SRC4714_19_4695_hodge_envelope", CSV_4695_HODGE, "HG4695_1_Hodge_envelope", "Hodge/constitutive envelope"),
        ("SRC4714_20_4695_wall_bound", CSV_4695_FLUX, "FX4695_1_wall_flux_bound", "Poynting wall flux bound"),
        ("SRC4714_21_4696_memory", CSV_4696_RETAINED, "RET4696_2_memory", "memory current EM open branch"),
        ("SRC4714_22_4696_bulk", CSV_4696_RETAINED, "RET4696_5_bulk_update", "bulk retained update"),
        ("SRC4714_23_4696_insertion", CSV_4696_JMEM_EM, "JME4696_0_4695_insertion", "4695 EM insertion into memory current"),
        ("SRC4714_24_4696_double", CSV_4696_JMEM_EM, "JME4696_1_no_double_count", "no double-counting control"),
        ("SRC4714_25_4696_readout", CSV_4696_JREADOUT, "JR4696_0_total", "readout re-entry current"),
        ("SRC4714_26_3222_null", CSV_3222_GUARDS, "SPG3222_0_null_wave_guard", "F^2 silence not Poynting silence"),
        ("SRC4714_27_3222_current", CSV_3222_GUARDS, "SPG3222_2_current_normalization", "current normalization guard"),
        ("SRC4714_28_765_same_current", CSV_765_MKI, "MKI765_3_same_current", "same current owner gate"),
        ("SRC4714_29_765_counter", CSV_765_RESCALE, "RCE765_2_current_rescale", "current rescaling counterexample"),
        ("SRC4714_30_988_current", CSV_988_EMLOCK, "EMLOCK988_2_current_owner", "EM lock current owner"),
        ("SRC4714_31_4702_same_current", CSV_4702_OWNER, "OWN4702_4_same_current", "4702 same current owner"),
        ("SRC4714_32_4702_readout", CSV_4702_OWNER, "OWN4702_5_readout_radiative", "readout/radiative guard"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMP4714_0_rebase",
            "claim_piece": "4175 theorem rebased onto current branch",
            "statement": "The 4175 Maxwell-Hodge/Poynting result is retained only as an exact conditional theorem: it applies when the same observed Hodge/coframe, Maxwell kinetic owner and matter current owner are all clauses of one parent branch.",
            "derivation": "4175 proved the Hilbert-stress identity, while 4694-4696 and 4713 show the same branch must also carry Hodge, wall-flux, current, readout and no-linear coefficient gates.",
            "result": "Poynting is not a new field on the same-owner Maxwell-Hodge branch, but the current branch is not promoted.",
            "current_status": "REBASED_EXACT_CONDITIONAL_NONCLAIM",
            "missing_for_claim": "same-Hodge parent signature, same-current charge lattice owner, boundary flux zero/bound and no nonminimal EM source multiplier",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMP4714_1_Hilbert_stress",
            "claim_piece": "EM Hilbert stress owner",
            "statement": "If S_EM=-1/4 int sqrt(-g_obs) Z_Q F_{mu nu}F^{mu nu} uses the same observed metric/Hodge and Z_Q is fixed or quotient-owned for the metric variation, then the source contribution is T_EM^{mu nu}=Z_Q(F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu}F^2), plus only explicitly retained constitutive/nonminimal residuals.",
            "derivation": "Metric variation of the Maxwell-Hodge action gives the standard symmetric Hilbert tensor. Any metric-dependent constitutive tensor, hidden coefficient or source multiplier is not erased; it is moved to the side-channel envelope.",
            "result": "ordinary EM energy density, pressure, stress and momentum flux are counted once in T_total",
            "current_status": "EXACT_CONDITIONAL_THEOREM_RESIDUALS_RETAINED",
            "missing_for_claim": "prove Delta_Hodge_EM=0 and epsilon_nonminimal_EM=0 or source-bound them",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMP4714_2_Poynting_identity",
            "claim_piece": "Poynting vector is stress flux",
            "statement": "For local observer n and spatial triad e_i, rho_EM=T_EM(n,n) and S_i=-T_EM(n,e_i); in an orthonormal Maxwell branch this is the usual E x B flux up to the chosen unit normalization.",
            "derivation": "Decompose the same Hilbert tensor relative to the observer frame. The flux component is not a second source current and cannot be added after variation without double counting.",
            "result": "c_Poynt_extra=0 on the single-source-functional branch",
            "current_status": "EXACT_IDENTITY_ON_SAME_HODGE_BRANCH",
            "missing_for_claim": "same-Hodge/current branch and boundary flux routing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMP4714_3_null_wave_guard",
            "claim_piece": "F2 silence is not stress silence",
            "statement": "A null EM wave can satisfy F_{mu nu}F^{mu nu}=0 while T_EM and the Poynting flux are nonzero.",
            "derivation": "The scalar invariant F^2 and the quadratic stress tensor are different contractions. Therefore the 4713 scalar kinetic coefficient/root route cannot by itself close EM stress, Poynting or source coupling.",
            "result": "full local-GR transfer needs T_EM/Hodge/current ownership, not only scalar F2 coefficient safety",
            "current_status": "NO_CHEAT_GUARD_DERIVED",
            "missing_for_claim": "none; this is a firewall",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMP4714_4_no_double_count",
            "claim_piece": "Poynting placement control",
            "statement": "Ordinary Maxwell Poynting flux is counted either as Hilbert EM stress in Q_bulk_EM or as a separately introduced nonminimal/source-tail flux, never both.",
            "derivation": "If it is produced by S_EM, it is already inside T_EM. If a distinct background/source Poynting term is introduced, it is a new term in the action or reduced source map and must be bounded as epsilon_nonminimal_EM or c_Poynt_extra.",
            "result": "the background-field intuition is preserved as stress flow, not as a free extra force",
            "current_status": "CONTROL_DERIVED",
            "missing_for_claim": "single source functional branch or finite side-channel coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def current_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CUR4714_0_same_current_identity",
            "quantity": "R_EM_current^nu",
            "definition": "R_EM_current^nu := nabla_mu T_EM^{mu nu} + F^nu_lambda J_Q^lambda",
            "zero_condition": "Maxwell equation, Hodge operator and matter current J_Q are derived from the same T_Q/charge-lattice owner",
            "finite_bound": "||R_EM_current|| <= E_Hodge_current + E_J_owner + E_charge_lattice + E_readout_current",
            "current_status": "IDENTITY_DERIVED_OWNER_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CUR4714_1_lorentz_exchange",
            "quantity": "matter-EM exchange",
            "definition": "nabla_mu T_EM^{mu nu}=-F^nu_lambda J_Q^lambda and nabla_mu T_matter+binding^{mu nu}=F^nu_lambda J_Q^lambda",
            "zero_condition": "same current and complete binding/interactions included in matter stress",
            "finite_bound": "||nabla_mu T_total^{mu nu}|| <= ||R_EM_current|| + ||R_matter_exchange|| + ||R_binding_omitted||",
            "current_status": "EXCHANGE_LAW_CONDITIONAL_BINDING_CURRENT_ROWS_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CUR4714_2_total_conservation",
            "quantity": "total EM+matter conservation residual",
            "definition": "R_total_EM^nu := nabla_mu(T_EM^{mu nu}+T_matter+binding^{mu nu})",
            "zero_condition": "R_EM_current=0, matter exchange uses the same J_Q, no boundary flux through local collar, and no readout/source tail re-enters",
            "finite_bound": "||R_total_EM|| <= ||R_EM_current|| + |Phi_wall_Poynting|/L_collar + ||J_readout|| + ||J_mem^EM_open||",
            "current_status": "FINITE_RESIDUAL_LAW_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CUR4714_3_arena_source_coupling",
            "quantity": "arena EM/source residual",
            "definition": "B_arena,EMstress <= |K_arena_EMstress| * (side-channel envelope + current residual + boundary flux)",
            "zero_condition": "same-current owner plus arena source/test charge maps and compact no-flux collar",
            "finite_bound": "B_arena,EMstress <= |K_arena_EMstress|(E_EM_side + ||R_EM_current|| + |Phi_wall_Poynting|/M_ref)",
            "current_status": "ARENA_TRANSFER_SCHEMA_READY_MAPS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def sidechannel_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SC4714_0_Delta_Hodge_EM",
            "quantity": "Delta_Hodge_EM",
            "meaning": "second Hodge, constitutive tensor, hidden EM metric or orientation/readout leak",
            "zero_condition": "Maxwell action uses only *_obs[e_obs(q)] and fixed orientation/units",
            "bound_formula": "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "status": "BOUND_IMPORTED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SC4714_1_current_owner",
            "quantity": "E_J_owner",
            "meaning": "matter current normalization is not the same T_Q owner as the Maxwell kinetic/Hodge block",
            "zero_condition": "J_Q is the Noether current of the same fixed charge lattice/generator owner",
            "bound_formula": "E_J_owner >= ||J_Maxwell - J_matter_Noether|| plus charge-lattice/current-weight residuals",
            "status": "NEXT_TARGET_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SC4714_2_wall_flux",
            "quantity": "Phi_wall_Poynting",
            "meaning": "EM radiative or apparatus flux crossing the local collar",
            "zero_condition": "stationary isolated local collar with no incoming/background radiation and no current crossing the wall",
            "bound_formula": "|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV| + |Phi_incoming| + |Phi_apparatus|",
            "status": "BOUND_IMPORTED_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SC4714_3_nonminimal_EM",
            "quantity": "epsilon_nonminimal_EM",
            "meaning": "independent EM/source multiplier, second EM metric, hidden current coupling or non-Hilbert Poynting term",
            "zero_condition": "parent object language has one Maxwell-Hodge source functional and no hidden/source EM weights",
            "bound_formula": "|Q_EM_nonminimal| <= W_lambda_max M_ref |epsilon_nonminimal_EM|",
            "status": "ZERO_OR_BOUND_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SC4714_4_readout_memory",
            "quantity": "J_mem^EM_open + J_readout_EM",
            "meaning": "EM flux or readout re-enters source variation after solving the bare action",
            "zero_condition": "variation-before-readout plus source-kernel silence and EM no-wall-flux",
            "bound_formula": "|J_mem^EM_open| <= C_EM_source/M_H_ref * |Q_bulk_EM/Poynting|; J_readout <= J_PiM_comm+...+J_boundary_endpoint",
            "status": "REDUCED_TO_4696_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SC4714_5_total_sidechannel",
            "quantity": "E_EM_side",
            "meaning": "no-cancellation EM stress/Poynting/current side-channel envelope",
            "zero_condition": "all side-channel rows zero on one parent branch",
            "bound_formula": "E_EM_side <= W_H||Delta_Hodge_EM|| + W_J E_J_owner + W_flux |Phi_wall_Poynting|/M_ref + W_nonmin|epsilon_nonminimal_EM| + W_R|J_mem^EM_open+J_readout_EM|",
            "status": "TOTAL_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("GATE4714_0_same_hodge", "same observed Hodge/coframe", "S_EM uses *_obs[e_obs(q)] with no hidden constitutive tensor", "UNSIGNED"),
        ("GATE4714_1_single_source", "single Hilbert source owner", "T_EM counted once in T_total and no standalone Poynting/background source", "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"),
        ("GATE4714_2_same_current", "same current/charge owner", "J_Q is the Noether current of the same T_Q/charge-lattice owner", "NEXT_TARGET"),
        ("GATE4714_3_boundary_flux", "boundary/wall flux handled", "Phi_wall_Poynting=0 or source-backed and routed through Hamiltonian boundary charge", "VALUE_MISSING"),
        ("GATE4714_4_readout_memory", "readout/memory no re-entry", "no reduced EFT/readout/source-kernel tail regenerates EM source coupling", "UNSIGNED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "required_condition": required,
            "current_status": status,
            "passes": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, required, status in gates
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4714_0_no_F2_to_TEM",
            "rule": "Do not infer T_EM/Poynting silence from F_Q^2 coefficient silence; null EM can have F_Q^2=0 and nonzero stress flux.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4714_1_no_double_count",
            "rule": "Do not add a separate Poynting/background source after T_EM is already in T_total; if added, it becomes epsilon_nonminimal_EM or c_Poynt_extra with a bound row.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4714_2_no_current_shortcut",
            "rule": "Do not transfer Maxwell-Hodge stress closure to WEP/R10/PPN/orbital tests until the same-current charge-lattice owner and source/test maps are derived or bounded.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4714_3_no_boundary_erasure",
            "rule": "Radiative EM wall flux is routed or bounded, not silently set to zero outside a stationary isolated collar theorem.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4714_0_main",
            "decision": DECISION,
            "meaning": "Poynting is handled correctly as Hilbert EM stress on the same-owner branch; current/local-GR claims remain blocked by same-current, Hodge, boundary and side-channel inputs.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4714_1_next",
            "decision": "ATTACK_SAME_CURRENT_CHARGE_LATTICE_NEXT",
            "meaning": "The dominant remaining EM/local source-coupling blocker is whether the current sourcing Maxwell is the same current carried by matter/source/test bodies.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4714_0",
            "status": "PRIVATE_NONCLAIM",
            "summary": "Maxwell-Hodge/Poynting theorem is rebased into the current branch; side-channel and same-current rows remain nonclaim.",
            "poynting_as_extra_background_force": False,
            "local_gr_claim": False,
            "r10_wep_ppn_orbital_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4714_0",
            "target": NEXT_TARGET,
            "reason": "Stress/Poynting is now a same-owner theorem/bound; the next fork is whether Maxwell current, matter charge and source/test response descend from the same charge-lattice owner.",
            "derive_first": "prove T_Q/charge-lattice/same-current owner and rule out current rescaling",
            "fallback": "stage source/test current mismatch rows for R10, WEP, PPN, clocks and orbital systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_body(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], currents: list[dict[str, Any]], sidechannels: list[dict[str, Any]], gates: list[dict[str, Any]], firewalls: list[dict[str, Any]]) -> str:
    return f"""# 4714 - EM Stress, Poynting and Current Owner or Side-Channel Bound

Generated: {timestamp}

Scope: local/private framework work only. No GitHub action.

## Result

This checkpoint rebases the older 4175 Maxwell-Hodge/Poynting theorem onto the newer 4694-4713 current branch.

The good news:

```text
Poynting is not a mysterious extra background force if it is generated by the same Maxwell-Hodge action.
```

The no-cheat version:

```text
S_EM = -1/4 int sqrt(-g_obs) Z_Q F_{{mu nu}}F^{{mu nu}}
=> T_EM^{{mu nu}}=Z_Q(F^{{mu alpha}}F^nu_alpha - 1/4 g_obs^{{mu nu}}F^2)
```

and for observer `n` with spatial triad `e_i`,

```text
S_i = -T_EM(n,e_i) ~ (E x B)_i.
```

So ordinary Poynting flow is a component of Hilbert EM stress. It is counted once in `T_total`, not added again as an independent background field.

## The Catch

This does **not** mean scalar `F_Q^2` coefficient silence is full EM/local-GR silence. A null EM wave can have `F_Q^2=0` while `T_EM` and Poynting flux are nonzero.

The current branch still needs:

```text
same Hodge + same current + no nonminimal EM source + boundary flux routed/zeroed + readout/memory no re-entry.
```

## Current Residual

```text
R_EM_current^nu := nabla_mu T_EM^{{mu nu}} + F^nu_lambda J_Q^lambda.
```

It vanishes only when the Maxwell equation, Hodge operator and matter current use the same parent owner.

## Side-Channel Envelope

```text
E_EM_side <= W_H||Delta_Hodge_EM||
           + W_J E_J_owner
           + W_flux |Phi_wall_Poynting|/M_ref
           + W_nonmin |epsilon_nonminimal_EM|
           + W_R |J_mem^EM_open + J_readout_EM|.
```

## Theorem Rows

{table(theorem)}

## Current / Conservation Rows

{table(currents)}

## Side-Channel Rows

{table(sidechannels)}

## Promotion Gates

{table(gates)}

## Firewalls

{table(firewalls)}

## Source Register

{table(sources)}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`.
"""


def formal_body(timestamp: str) -> str:
    return f"""# PPC4161 4714 - EM Stress/Poynting/Current Owner or Side-Channel Bound

Generated: {timestamp}

Private nonclaim checkpoint.

Core result:

```text
S_EM = -1/4 int sqrt(-g_obs) Z_Q F^2
=> T_EM^{{mu nu}}=Z_Q(F^{{mu alpha}}F^nu_alpha - 1/4 g_obs^{{mu nu}}F^2).
```

For local observer `n`,

```text
S_i = -T_EM(n,e_i).
```

Thus ordinary Poynting flux is EM Hilbert stress, not a separate background force, provided the same Maxwell-Hodge-current owner is used.

Retained residual:

```text
R_EM_current^nu := nabla_mu T_EM^{{mu nu}} + F^nu_lambda J_Q^lambda.
```

Total side-channel envelope:

```text
E_EM_side <= W_H||Delta_Hodge_EM|| + W_J E_J_owner
           + W_flux |Phi_wall_Poynting|/M_ref
           + W_nonmin |epsilon_nonminimal_EM|
           + W_R |J_mem^EM_open + J_readout_EM|.
```

No local-GR/R10/WEP/PPN claim is allowed until same-current, boundary and side-channel inputs close.

Validation: `{VALIDATION_CSV}`.
Next: `{NEXT_TARGET}`.
"""


def write_resume(timestamp: str) -> None:
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: {timestamp}

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4714-Y5-R2FR-EM-stress-Poynting-current-owner-or-sidechannel-bound.md`

## What Changed

The older Maxwell-Hodge/Poynting theorem has been rebased onto the current local branch:

```text
Poynting flux = spatial flux component of T_EM
```

but only if the same Maxwell-Hodge-current owner is used.

Retained current residual:

```text
R_EM_current^nu := nabla_mu T_EM^{{mu nu}} + F^nu_lambda J_Q^lambda.
```

Retained side-channel envelope:

```text
E_EM_side <= W_H||Delta_Hodge_EM|| + W_J E_J_owner
           + W_flux |Phi_wall_Poynting|/M_ref
           + W_nonmin |epsilon_nonminimal_EM|
           + W_R |J_mem^EM_open + J_readout_EM|.
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not infer full EM stress silence from scalar `F_Q^2` silence.
- Do not double-count Poynting as both `T_EM` and an extra background force.
- Do not transfer EM closure into R10/WEP/PPN/orbital tests before same-current/source-test maps are owned or bounded.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, sources: list[dict[str, Any]], theorem: list[dict[str, Any]], currents: list[dict[str, Any]], sidechannels: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4714_sources_exist", all(row["path_exists"] for row in sources), "all cited local source paths exist"),
        ("VAL4714_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4714_poynting_identity", any(row["theorem_id"] == "EMP4714_2_Poynting_identity" for row in theorem), "Poynting identity row present"),
        ("VAL4714_null_guard", any(row["theorem_id"] == "EMP4714_3_null_wave_guard" for row in theorem), "F2-to-TEM firewall row present"),
        ("VAL4714_current_residual", any(row["row_id"] == "CUR4714_0_same_current_identity" for row in currents), "same-current residual row present"),
        ("VAL4714_side_total", any(row["row_id"] == "SC4714_5_total_sidechannel" for row in sidechannels), "total side-channel envelope present"),
        ("VAL4714_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in theorem + currents + sidechannels), "no row allows a claim"),
        ("VAL4714_gates_not_passing", not all(bool(row["passes"]) for row in gates), "promotion gates not all passing"),
        ("VAL4714_doc_written", DOC_PATH.exists(), "checkpoint document written"),
        ("VAL4714_formal_written", FORMAL_PATH.exists(), "formal packet document written"),
        ("VAL4714_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4714_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "4714 artifacts validate as private nonclaim checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows(timestamp)
    theorem = theorem_rows(timestamp)
    currents = current_rows(timestamp)
    sidechannels = sidechannel_rows(timestamp)
    gates = promotion_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(CURRENT_CSV, currents)
    write_csv(SIDECHANNEL_CSV, sidechannels)
    write_csv(PROMOTION_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    DOC_PATH.write_text(doc_body(timestamp, sources, theorem, currents, sidechannels, gates, firewalls), encoding="utf-8")
    FORMAL_PATH.write_text(formal_body(timestamp), encoding="utf-8")
    append_claim_once(timestamp)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: Maxwell-Hodge/Poynting has been rebased onto the current branch; ordinary Poynting is `T_EM` flux if the same Maxwell-Hodge-current owner is used.
- Retained residual: `R_EM_current^nu := nabla_mu T_EM^{{mu nu}} + F^nu_lambda J_Q^lambda`.
- Side-channel envelope: `E_EM_side <= W_H||Delta_Hodge_EM|| + W_J E_J_owner + W_flux |Phi_wall_Poynting|/M_ref + W_nonmin|epsilon_nonminimal_EM| + W_R|J_mem^EM_open+J_readout_EM|`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts the EM stress/Poynting issue into a same-owner theorem plus explicit Hodge/current/wall/nonminimal/readout side-channel rows.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_resume(timestamp)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    validation = validation_rows(timestamp, sources, theorem, currents, sidechannels, gates)
    write_csv(VALIDATION_CSV, validation)


if __name__ == "__main__":
    main()
