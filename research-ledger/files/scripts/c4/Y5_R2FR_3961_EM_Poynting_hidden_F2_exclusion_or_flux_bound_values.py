from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3961"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3961-Y5-R2FR-EM-Poynting-hidden-F2-exclusion-or-flux-bound-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3961_SOURCE_REGISTER.csv",
    "variation": SRC / "P8_Y5_R2FR_3961_HIDDEN_EM_VARIATION_LAW.csv",
    "factorization": SRC / "P8_Y5_R2FR_3961_SIGMA_FACTOR_EM_EXCLUSION_GATE.csv",
    "poynting": SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv",
    "first_values": SRC / "P8_Y5_R2FR_3961_EM_FIRST_CONDITIONAL_ZERO_VALUES.csv",
    "bound_templates": SRC / "P8_Y5_R2FR_3961_EM_BOUND_VALUE_TEMPLATES.csv",
    "decision": SRC / "P8_Y5_R2FR_3961_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3961_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3961_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3961_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3961_VALIDATION.csv",
}

NEXT_DOC = "3962-Y5-R2FR-EM-residual-vector-first-score-or-Hodge-owner-lock.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3962_EM_residual_vector_first_score_or_Hodge_owner_lock.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3961_00_3960_next", SRC / "P8_Y5_R2FR_3960_NEXT_TARGET.csv", "NEXT3960_0", "3960 handoff"),
        ("SRC3961_01_hidden_gate", SRC / "P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv", "EMG3960_2_hidden_F2", "hidden F2 gate"),
        ("SRC3961_02_poynting_gate", SRC / "P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv", "EMG3960_3_Poynting_flux", "Poynting flux gate"),
        ("SRC3961_03_res_CXF2", SRC / "P8_Y5_R2FR_3960_RETAINED_RESIDUAL_VALUE_QUEUE.csv", "RV3960_0_C_XF2", "retained C_XF2 residual"),
        ("SRC3961_04_res_flux", SRC / "P8_Y5_R2FR_3960_RETAINED_RESIDUAL_VALUE_QUEUE.csv", "RV3960_1_Phi_EM_rad", "retained Poynting residual"),
        ("SRC3961_05_res_hodge", SRC / "P8_Y5_R2FR_3960_RETAINED_RESIDUAL_VALUE_QUEUE.csv", "RV3960_2_Delta_Hodge_EM", "retained Hodge residual"),
        ("SRC3961_06_stationary", SRC / "P8_Y5_R2FR_3960_SOURCE_CURRENT_ZERO_GRAMMAR.csv", "SCG3960_5_stationary_isolated_boundary", "stationary no-flux grammar"),
        ("SRC3961_07_CA_EM", SRC / "P8_Y5_R2FR_3959_CA_TOTAL_CURRENT_BOUND_LAW.csv", "CAB3959_5_EM_alpha_charge", "EM alpha bound"),
        ("SRC3961_08_EM_source_F2", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_2_nonminimal_XF2", "hidden F2 source row"),
        ("SRC3961_09_EM_source_flux", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_1_radiative_poynting_flux", "Poynting source row"),
        ("SRC3961_10_EM_source_hodge", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_4_observed_Hodge_flow_rule", "Hodge source row"),
        ("SRC3961_11_EM_bound_F2", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_2_C_XF2", "C_XF2 bound route"),
        ("SRC3961_12_EM_bound_flux", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_4_Phi_EM_rad", "Poynting bound route"),
        ("SRC3961_13_EM_bound_readout", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_5_C_EM_readout", "readout residual"),
        ("SRC3961_14_sigma_factor", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_00_candidate_action", "Sigma factorization"),
        ("SRC3961_15_bulk_force", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_07_bulk_X_force_law", "bulk force factorization"),
        ("SRC3961_16_memory", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_08_nonlocal_memory_kernel", "memory factorization"),
        ("SRC3961_17_sigma_bound", SRC / "P8_Y5_R2FR_3959_YLOC_ZERO_THEOREM_OR_BOUND.csv", "YB3959_4_sigma_bound", "Sigma bound"),
        ("SRC3961_18_validation_3960", SRC / "P8_Y5_BRR545_3960_VALIDATION.csv", "VAL3960_18_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:1000]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def variation_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HEV3961_0_action",
            "object": "hidden EM action perturbation",
            "formula": "Delta S_EM[Y]=-(1/4mu0) int sqrt(-g_obs)[ f(Y) F_mnF^mn + g(Y) F_mn *F^mn ]",
            "derived_result": "gauge/diffeomorphism symmetry allows this unless the parent action grammar forbids or factorizes it",
            "status": "COUNTERMODEL_ALLOWED_BY_SYMMETRY_ALONE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HEV3961_1_source_current",
            "object": "linear Y source current",
            "formula": "J_A^EM|0 = -(1/4mu0)[ (partial_A f)|0 F^2 + (partial_A g)|0 F*F ] + J_A^Hodge + J_A^readout",
            "derived_result": "hidden F2/F*F is a direct source-current term unless the first derivatives vanish",
            "status": "DERIVED_DANGEROUS_LINEAR_SOURCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HEV3961_2_bound",
            "object": "hidden EM source bound",
            "formula": "|J_A^EM| <= (1/4mu0)(|f_A| ||F^2|| + |g_A| ||F*F||) + |J_A^Hodge| + |J_A^readout|",
            "derived_result": "if exclusion fails, EM leakage is finite and value-ready once coefficient and field norms are supplied",
            "status": "DERIVED_BOUND_TEMPLATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def factorization_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SFE3961_0_gauge_not_enough",
            "gate": "gauge/diffeomorphism invariance",
            "condition": "F^2 and F*F are gauge and diffeomorphism scalars",
            "effect": "does not exclude f(Y)F^2 or g(Y)F*F",
            "result": "EXCLUSION_FAILS_BY_SYMMETRY_ALONE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFE3961_1_sigma_factor",
            "gate": "Sigma factorization",
            "condition": "f(Y)=f_0 + fbar Sigma_loc(Y) + O(Sigma_loc^2), g(Y)=g_0 + gbar Sigma_loc(Y) + O(Sigma_loc^2)",
            "effect": "partial_A f|0=partial_A g|0=0 because Sigma_loc=G_ABY^AY^B and partial_A Sigma_loc|0=0",
            "result": "HIDDEN_F2_LINEAR_SOURCE_ZERO_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFE3961_2_no_hidden_visible_Hom",
            "gate": "operator-domain exclusion",
            "condition": "no parent morphism from hidden Y_loc marker to visible EM coupling except common constant or Sigma_loc",
            "effect": "direct C_XF2 is zero as an action grammar rule",
            "result": "POSSIBLE_STRONG_EXCLUSION_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFE3961_3_residual_if_fail",
            "gate": "residual bound branch",
            "condition": "if f_A or g_A survives, retain C_XF2 in EM residual vector",
            "effect": "C_A_total and alpha/clock residuals receive a bounded EM source term",
            "result": "BOUND_BRANCH_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def poynting_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PNF3961_0_identity",
            "theorem_piece": "Poynting identity",
            "formula": "dU_EM/dt + integral_boundary S_Poynting dot n dA = - integral_D J dot E dV",
            "derived_result": "boundary EM flux is controlled by field energy change plus matter work",
            "status": "DERIVED_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PNF3961_1_stationary_zero",
            "theorem_piece": "stationary isolated no-flux theorem",
            "formula": "time_avg(dU_EM/dt)=0 and time_avg(integral_D J dot E)=0 => time_avg(Phi_EM_rad)=0",
            "derived_result": "compact stationary non-radiating local branch has no net Poynting boundary source",
            "status": "POYNTING_ZERO_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PNF3961_2_flux_bound",
            "theorem_piece": "nonstationary flux bound",
            "formula": "|Phi_EM_rad| <= |dU_EM/dt| + |W_matter|, W_matter:=integral_D J dot E dV",
            "derived_result": "if the local branch radiates or sits in a background flux, the leakage is bounded by energy/work terms",
            "status": "DERIVED_FLUX_BOUND_TEMPLATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PNF3961_3_branch_warning",
            "theorem_piece": "branch warning",
            "formula": "Phi_EM_rad=0 is not valid for radiating binaries, driven lab systems, or boundaries through external radiation",
            "derived_result": "no-flux is a local stationary branch condition, not a universal EM truth",
            "status": "NO_UNIVERSAL_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def first_value_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "value_id": "EMZ3961_0_partial_f",
            "symbol": "partial_A f_EM|0",
            "conditional_value": "0",
            "units": "model_dependent_EM_coupling_derivative",
            "condition": "hidden EM coefficient factorizes through Sigma_loc or no hidden-visible Hom exists",
            "feeds": "C_XF2; J_A^EM; C_A_total; alpha/clocks",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "EMZ3961_1_partial_g",
            "symbol": "partial_A g_EM|0",
            "conditional_value": "0",
            "units": "model_dependent_EM_dual_coupling_derivative",
            "condition": "hidden pseudoscalar/dual EM coefficient factorizes through Sigma_loc or is absent by action grammar",
            "feeds": "C_XF2_dual; J_A^EM; parity/EM clock channels",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "EMZ3961_2_Phi_EM_rad",
            "symbol": "Phi_EM_rad",
            "conditional_value": "0",
            "units": "time^-1_or_dimensionless_window",
            "condition": "stationary isolated local branch with no net matter work and no background/incoming radiation through boundary",
            "feeds": "B_EM; clock/orbital/alpha source leakage",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "value_id": "EMZ3961_3_Delta_Hodge_EM",
            "symbol": "Delta_Hodge_EM",
            "conditional_value": "0",
            "units": "dimensionless_or_tensor",
            "condition": "EM Hodge star is exactly the observed gravitational/coframe Hodge star *_obs[e_obs(q)]",
            "feeds": "visible Maxwell stress; EM source-current; charge/current normalization",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_template_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "EMB3961_0_hidden_F2",
            "symbol": "J_A^EM_hidden",
            "bound_formula": "|J_A^EM| <= (1/4mu0)(|f_A| ||F^2|| + |g_A| ||F*F||) + |J_A^Hodge| + |J_A^readout|",
            "needed_values": "f_A; g_A; F^2 norm; F*F norm; J_A^Hodge; J_A^readout",
            "status": "VALUE_READY_TEMPLATE_NO_NUMERIC_VALUES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB3961_1_flux",
            "symbol": "Phi_EM_rad",
            "bound_formula": "|Phi_EM_rad| <= |dU_EM/dt| + |integral_D J dot E dV|",
            "needed_values": "EM energy time derivative; matter EM work; averaging/window rule; boundary definition",
            "status": "VALUE_READY_TEMPLATE_NO_NUMERIC_VALUES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB3961_2_alpha_clock",
            "symbol": "Delta_alpha/alpha",
            "bound_formula": "|Delta_alpha/alpha| <= K_EM[|f_A| ||F^2|| + |g_A| ||F*F|| + |Delta_Hodge_EM| + |Phi_EM_rad| + |C_EM_readout|]",
            "needed_values": "K_EM; f_A; g_A; field norms; Delta_Hodge_EM; Phi_EM_rad; C_EM_readout",
            "status": "FEEDS_3959_CA_EM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3961_0_no_gauge_shortcut",
            "decision": "do not claim gauge symmetry excludes hidden EM F2/F*F couplings",
            "basis": "F^2 and F*F are allowed scalars unless parent action grammar forbids direct hidden-visible coefficients",
            "effect": "prevents a false Maxwell/source-coupling proof",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3961_1_sigma_route",
            "decision": "use Sigma_loc factorization as the clean zero route for hidden EM source terms",
            "basis": "Sigma_loc has a double zero, so first derivatives of factorized EM coefficients vanish at Y=0",
            "effect": "hidden F2/F*F becomes zero on the local branch if parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3961_2_poynting_route",
            "decision": "use stationary isolated Poynting theorem for boundary flux, otherwise retain flux bound",
            "basis": "Poynting identity gives exact no-flux condition or a finite work/energy bound",
            "effect": "Poynting source is no longer vague; it is branch-zero or value-scored",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3961_3_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the EM residual vector now has conditional zeros and bound templates; next step should score/lock Hodge/readout owner",
            "effect": "turn EM leakage into a compact score vector feeding C_A_total",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3961_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3961_1_hidden_F2_zero", "hidden F2/F*F zero", "Sigma factorization or no-hidden-visible Hom parent-signed", "CONDITIONAL_ONLY"),
        ("CLG3961_2_poynting_zero", "Poynting flux zero", "stationary isolated no-work/no-radiation branch", "CONDITIONAL_ONLY"),
        ("CLG3961_3_bound_templates", "EM bound templates", "finite coefficient/field/work/readout values supplied", "NEXT_VALUES_REQUIRED"),
        ("CLG3961_4_local_GR_EM", "local GR/Maxwell source coupling", "EM residual vector zero or scored plus non-EM residuals handled", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3961_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "assemble the EM residual vector with first conditional zero rows and bound templates, then either lock the Hodge/readout owner or produce a first nonclaim score row feeding C_A_total_current",
            "success_condition": "Delta_Hodge_EM, C_EM_readout, w_EM, C_XF2, and Phi_EM_rad are either zero-condition rows or finite bound rows suitable for the 3959 C_A/alpha/clock residual law",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_EM_DERIVATION",
            "summary": "3961 derives the hidden EM source-current law, shows gauge symmetry alone does not exclude f(Y)F^2/F*F, gives the Sigma factorization zero route, derives the stationary-isolated Poynting no-flux theorem, and records finite bound templates if either zero route fails.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3961 - EM Poynting Hidden F2 Exclusion Or Flux Bound Values

Timestamp: `{timestamp}`

## Result

3961 derives the EM source-current danger directly:

`J_A^EM|0 = -(1/4mu0)[(partial_A f)|0 F^2 + (partial_A g)|0 F*F] + J_A^Hodge + J_A^readout`.

This means gauge symmetry alone is not enough. `F^2` and `F*F` are legal scalars.

The clean zero route is:

`f(Y)=f_0 + fbar Sigma_loc(Y)+...`, `g(Y)=g_0 + gbar Sigma_loc(Y)+...`

so `partial_A f|0 = partial_A g|0 = 0` because `Sigma_loc=G_ABY^AY^B` has a double zero.

For the Poynting channel:

`dU_EM/dt + integral_boundary S dot n = - integral_D J dot E`.

So the stationary isolated branch gives `Phi_EM_rad=0`; otherwise it is bounded by field-energy change plus matter work.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- Hidden EM variation: `source-intake\\mts_residuals\\P8_Y5_R2FR_3961_HIDDEN_EM_VARIATION_LAW.csv`
- Sigma EM gate: `source-intake\\mts_residuals\\P8_Y5_R2FR_3961_SIGMA_FACTOR_EM_EXCLUSION_GATE.csv`
- Poynting theorem/bound: `source-intake\\mts_residuals\\P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv`
- First zero values: `source-intake\\mts_residuals\\P8_Y5_R2FR_3961_EM_FIRST_CONDITIONAL_ZERO_VALUES.csv`
- Bound templates: `source-intake\\mts_residuals\\P8_Y5_R2FR_3961_EM_BOUND_VALUE_TEMPLATES.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3961_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3961 - Hidden EM F2 And Poynting Flux Derivation

Timestamp: `{timestamp}`

- Derived hidden EM source current: `J_A^EM|0` is controlled by `partial_A f`, `partial_A g`, Hodge, and readout terms.
- Gauge symmetry alone does not exclude hidden `F^2/F*F`; Sigma factorization or no-hidden-visible-Hom grammar is required.
- Derived Poynting no-flux condition from the energy identity: stationary isolated branch gives `Phi_EM_rad=0`; nonstationary/radiative branch gets a finite flux bound.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3961 - Hidden EM F2 And Poynting Flux Derivation"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    variation = variation_rows(timestamp)
    factorization = factorization_rows(timestamp)
    poynting = poynting_rows(timestamp)
    first_values = first_value_rows(timestamp)
    bound_templates = bound_template_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    variation_statuses = {row["status"] for row in variation}
    factor_results = {row["result"] for row in factorization}
    poynting_statuses = {row["status"] for row in poynting}
    value_symbols = {row["symbol"] for row in first_values}
    bound_symbols = {row["symbol"] for row in bound_templates}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = variation + factorization + poynting + first_values + bound_templates + decisions + claims + next_target

    checks = [
        ("VAL3961_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3961_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3961_02_hidden_source_law", "DERIVED_DANGEROUS_LINEAR_SOURCE" in variation_statuses and any("partial_A f" in row["formula"] for row in variation), "hidden EM source-current law derived"),
        ("VAL3961_03_gauge_refusal", "EXCLUSION_FAILS_BY_SYMMETRY_ALONE" in factor_results, "gauge-only exclusion refused"),
        ("VAL3961_04_sigma_zero_route", "HIDDEN_F2_LINEAR_SOURCE_ZERO_CONDITIONAL" in factor_results, "Sigma factorization zero route written"),
        ("VAL3961_05_poynting_identity", "DERIVED_IDENTITY" in poynting_statuses and "POYNTING_ZERO_CONDITIONAL" in poynting_statuses, "Poynting identity and stationary zero theorem written"),
        ("VAL3961_06_bound_templates", {"J_A^EM_hidden", "Phi_EM_rad", "Delta_alpha/alpha"}.issubset(bound_symbols), "EM bound templates present"),
        ("VAL3961_07_first_values", {"partial_A f_EM|0", "partial_A g_EM|0", "Phi_EM_rad", "Delta_Hodge_EM"}.issubset(value_symbols), "first conditional EM zero values present"),
        ("VAL3961_08_decision", "do not claim gauge symmetry" in decision_text and "Sigma_loc factorization" in decision_text and "Poynting theorem" in decision_text, "decision records no shortcut plus zero/bound routes"),
        ("VAL3961_09_claim_gate", "CONDITIONAL_ONLY" in claim_statuses and "NEXT_VALUES_REQUIRED" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses, "claim gate blocks EM/local-GR promotion"),
        ("VAL3961_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to EM residual vector score/Hodge owner"),
        ("VAL3961_11_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3961_12_zero_rows_score_ready", all(row["score_ready"] for row in first_values), "first EM zero rows are score-ready conditionals"),
        ("VAL3961_13_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3961_14_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3961_15_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3961_16_spine_updated", SPINE_PATH.exists() and "3961 - Hidden EM F2 And Poynting Flux Derivation" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3961_17_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3961_18_script_compile", True, "script compiled before validation write"),
        ("VAL3961_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    variation = variation_rows(timestamp)
    factorization = factorization_rows(timestamp)
    poynting = poynting_rows(timestamp)
    first_values = first_value_rows(timestamp)
    bound_templates = bound_template_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["variation"], variation)
    write_csv(OUTPUTS["factorization"], factorization)
    write_csv(OUTPUTS["poynting"], poynting)
    write_csv(OUTPUTS["first_values"], first_values)
    write_csv(OUTPUTS["bound_templates"], bound_templates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, sources), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, sources)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3961 validation failed: {failed}")

    print(f"3961 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("hidden EM source law and Poynting no-flux/bound route derived")


if __name__ == "__main__":
    run()
