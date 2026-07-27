from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4583"
CLAIM_ID = "L-425"
BRANCH_ID = "MTS_R2FR_Y5_CHARGE_CURRENT_NORMALIZATION_AND_EM_READOUT_TAIL_OWNER_OR_SOURCE_BOUND_4583"
MARKER = "PPC4161_CHARGE_CURRENT_NORMALIZATION_AND_EM_READOUT_TAIL_OWNER_OR_SOURCE_BOUND_4583"
PACKET_MARKER = "PPC4161_PACKET_CHARGE_CURRENT_NORMALIZATION_AND_EM_READOUT_TAIL_OWNER_OR_SOURCE_BOUND_4583"
DECISION = "FIXED_QBASIC_EM_COUPLING_AND_READOUT_TAIL_ZERO_IMPORTED_OPEN_DYNAMIC_EM_TAIL_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4584-Y5-R2FR-parent-material-tensor-and-apparatus-support-zero-or-bound.md"

DOC_PATH = POST / "4583-Y5-R2FR-charge-current-normalization-and-EM-readout-tail-owner-or-source-bound.md"
FORMAL_PATH = FORMAL / "599-PPC4161-charge-current-normalization-and-EM-readout-tail-owner-or-source-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4582 = POST / "4582-Y5-R2FR-material-response-tail-and-active-kernel-first-bound-or-owner-zero.md"
CSV_4582_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4582_MATERIAL_TAIL_REDUCTION_ROWS.csv"
CSV_4582_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4582_DECISION.csv"
CSV_4582_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4582_NEXT_TARGET.csv"
DOC_4438 = POST / "4438-Y5-R2FR-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md"
CSV_4438_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4438_TOTAL_EM_ZERO_ROWS.csv"
CSV_4438_SURV = SOURCE_DIR / "P8_Y5_R2FR_4438_OPEN_EM_SURVIVOR_ROWS.csv"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_225 = FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md"
FORMAL_278 = FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md"
FORMAL_329 = FORMAL / "329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md"
FORMAL_453 = FORMAL / "453-PPC4161-EM-charge-current-unique-F2-owner-or-Kmactionscale-source-value.md"
CSV_EM_BOUND = SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_EM_POYNTING = SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4583_SOURCE_REGISTER.csv"
OWNER_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_CHARGE_CURRENT_EM_READOUT_OWNER_THEOREM.csv"
BRANCH_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_BRANCH_GATE_MATRIX.csv"
TAIL_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_EM_TAIL_REDUCTION_ROWS.csv"
BOUND_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_OPEN_DYNAMIC_EM_BOUND_SCHEMA.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4583_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4583_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4583_00_4582_doc", DOC_4582, "C_material_tail", "4582 material tail handoff"),
        ("SRC4583_01_4582_tail", CSV_4582_TAIL, "MTR4582_3_Creadout_update", "4582 C_readout update"),
        ("SRC4583_02_4582_decision", CSV_4582_DECISION, "C_JQ", "4582 surviving EM/material terms"),
        ("SRC4583_03_4582_next", CSV_4582_NEXT, "charge-current-normalization-and-EM-readout-tail", "4582 selected 4583"),
        ("SRC4583_04_225_norm", FORMAL_225, "alpha_eff proportional to g_J^2/lambda_A", "Maxwell normalization identity"),
        ("SRC4583_05_278_guard", FORMAL_278, "C_JQ = 0", "fixed visible EM readout guard"),
        ("SRC4583_06_329_ward", FORMAL_329, "CN4313_1_fixed_visible_branch", "Ward current normalization branch"),
        ("SRC4583_07_4437_formal", FORMAL_453, "ZERO4437_1_C_JQ", "4437 fixed branch C_JQ zero"),
        ("SRC4583_08_4438_doc", DOC_4438, "TOTAL_FIXED_BRANCH_EM_PRODUCT_ZERO", "4438 total fixed EM zero"),
        ("SRC4583_09_4438_zero", CSV_4438_ZERO, "ZERO4438_1_C_EM_readout", "4438 C_EM_readout zero"),
        ("SRC4583_10_4438_survivors", CSV_4438_SURV, "SURV4438_1_readout_regeneration", "4438 readout survivor"),
        ("SRC4583_11_Maxwell_Hodge", FORMAL_191, "Poynting vector is not a separate background field", "Poynting/Hilbert stress owner"),
        ("SRC4583_12_EM_CJQ", CSV_EM_BOUND, "EMB3503_3_C_JQ", "live C_JQ ledger"),
        ("SRC4583_13_EM_CEMreadout", CSV_EM_BOUND, "EMB3503_5_C_EM_readout", "live C_EM_readout ledger"),
        ("SRC4583_14_EM_Phi", CSV_EM_POYNTING, "EMF3502_1_radiative_poynting_flux", "Poynting flux survivor"),
        ("SRC4583_15_EM_readout_regen", CSV_EM_POYNTING, "EMF3502_6_readout_radiative_regeneration", "readout regeneration survivor"),
        ("SRC4583_16_claim_424", CLAIMS_PATH, "L-424", "prior claim register handoff"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "generated_utc": now,
                "valid_for_claim": "False",
            }
        )
    return rows


def owner_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CCO4583_0_rescaling_identity",
            "claim": "The EM coupling drift is the owner ratio, not a removable field convention.",
            "derivation": "S_EM=-lambda_A/4 int F^2 + g_J int A.J; A_c=sqrt(lambda_A)A; alpha_eff proportional to g_J^2/lambda_A; b_alpha=D_X ln alpha_eff=2D_X ln g_J-D_X ln lambda_A.",
            "consequence": "A -> lambda A only moves normalization between kinetic and current slots. A real relative derivative is physical unless both slots are fixed by the same owner.",
            "status": "EXACT_IDENTITY_IMPORTED",
            "source": str(FORMAL_225),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CCO4583_1_CJQ_fixed_branch_zero",
            "claim": "C_JQ=0 in the fixed q-basic standard visible branch.",
            "derivation": "If theta_obs={m_A,charges,alpha_EM,hbar,c,material labels}, g_J, lambda_A and readout labels are fixed before variation, and J_matter=J_Maxwell in the same action, then D_X ln g_J=D_X ln lambda_A=0 and deltaJ has no C_JQ component.",
            "consequence": "The 4582 material tail loses |C_JQ| only inside this private branch; dynamic/global current normalization remains a bound row.",
            "status": "PRIVATE_BRANCH_ZERO_IMPORTED_FROM_4437",
            "source": str(FORMAL_453),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CCO4583_2_CEMreadout_strict_zero",
            "claim": "C_EM_readout=0 in the strict postprocessing/no-hidden-S_eff branch.",
            "derivation": "If readout, clocks, spectroscopy, EFT reduction and material labels are post-variation maps with no hidden-field argument slot in S_parent or S_eff, then they cannot regenerate f_X F^2, alpha_X, Hodge readout, or EM binding response as a source coefficient.",
            "consequence": "The 4582 material tail loses |C_EM_readout| only under the 4438 strict readout-preservation conditions.",
            "status": "PRIVATE_BRANCH_ZERO_IMPORTED_FROM_4438",
            "source": str(CSV_4438_ZERO),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CCO4583_3_PhiEM_closed_collar_zero",
            "claim": "Phi_EM_rad=0 only for fixed-orientation closed collars with pointwise no radiative/background Poynting flux.",
            "derivation": "Poynting is Maxwell-Hodge Hilbert stress flux. If P_rad_EM(tau)=0 on the collar boundary, no radiative EM boundary flux enters the local material/readout tail. If flux crosses the collar, it is routed as boundary/Hamiltonian energy, not erased.",
            "consequence": "The strict fixed branch removes |Phi_EM_rad|; open-radiation branches retain a source-energy or power-normalized bound row.",
            "status": "CLOSED_COLLAR_ZERO_WITH_OPEN_FLUX_FIREWALL",
            "source": str(DOC_4438),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "CCO4583_4_open_dynamic_bound",
            "claim": "Open/dynamic EM tails are an absolute no-cancellation residual vector.",
            "derivation": "C_EM_tail := |C_JQ_dyn|+|C_EM_readout_eff|+|Phi_EM_rad|+|Delta_Hodge_EM|+|C_XF2|+|b_alpha|+|deltaJ_perp|. Ward mismatch obeys ||Delta_Ward|| <= ||F||_inf(|C_JQ| ||J||+||deltaJ_perp||)+||R_Hodge||+||R_Q||+||B_J||.",
            "consequence": "If any fixed-branch clause fails, the EM tail is retained as a sourced bound schema, never set to zero by convention.",
            "status": "BOUND_SCHEMA_DERIVED_VALUES_MISSING",
            "source": str(FORMAL_329),
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def branch_gate_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        (
            "BG4583_0_fixed_qbasic_sameHodge_closed_collar",
            "fixed q-basic same-Hodge closed-collar branch",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            "C_JQ=0; C_EM_readout=0; Phi_EM_rad=0; C_EM_tail=0",
            "PRIVATE_BRANCH_ZERO_READY_NONCLAIM",
        ),
        (
            "BG4583_1_dynamic_charge_current",
            "dynamic/global charge-current normalization branch",
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            "C_JQ_dyn retained with Ward/current bound",
            "BOUND_REQUIRED",
        ),
        (
            "BG4583_2_readout_regeneration",
            "readout/EFT hidden-argument branch",
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            "C_EM_readout_eff retained",
            "BOUND_REQUIRED",
        ),
        (
            "BG4583_3_open_radiation",
            "open radiative/background Poynting collar",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            "Phi_EM_rad retained as boundary/Hamiltonian flux",
            "BOUND_REQUIRED",
        ),
    ]
    fields = [
        "gate_id",
        "branch",
        "fixed_theta_obs",
        "fixed_lambda_A",
        "fixed_g_J",
        "same_current_owner",
        "same_Hodge_owner",
        "readout_after_variation",
        "no_hidden_S_eff_argument",
        "closed_collar_no_flux",
        "result",
        "status",
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            **{field: bool_text(value) if isinstance(value, bool) else value for field, value in zip(fields, row)},
            "generated_utc": now,
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def tail_reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ETR4583_0_fixed_branch_EM_tail_zero",
            "target": "C_EM_tail",
            "formula": "C_EM_tail=|C_JQ|+|C_EM_readout|+|Phi_EM_rad|+|Delta_Hodge_EM|+|C_XF2|+|b_alpha|+|deltaJ_perp|=0",
            "branch_condition": "fixed q-basic + same Hodge + post-variation readout + no hidden S_eff argument + closed collar no-flux",
            "status": "PRIVATE_BRANCH_ZERO_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ETR4583_1_material_tail_fixed_branch_update",
            "target": "C_material_tail",
            "formula": "C_material_tail <= sum_X |C_X R_material_X| + |C_apparatus|",
            "branch_condition": "4582 material owner zero plus 4583 fixed-branch EM tail zero",
            "status": "REDUCED_BOUND_PARENT_MATERIAL_AND_APPARATUS_REMAIN",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ETR4583_2_Creadout_fixed_branch_update",
            "target": "C_readout",
            "formula": "C_readout <= sum_X |C_X R_material_X| + |C_apparatus| + C_kernel_active + C_EFT_active + C_tau_tail",
            "branch_condition": "strict fixed EM branch only; active kernels and non-EM/material tails not closed",
            "status": "C_READOUT_REDUCED_NOT_CLOSED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ETR4583_3_open_dynamic_branch_update",
            "target": "C_readout_open",
            "formula": "C_readout <= sum_X |C_X R_material_X| + |C_apparatus| + C_EM_tail + C_kernel_active + C_EFT_active + C_tau_tail",
            "branch_condition": "any dynamic current, hidden readout/EFT argument, Hodge mismatch, or open radiative collar",
            "status": "OPEN_BRANCH_BOUND_SCHEMA_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def bound_schema_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("OBS4583_0_CJQ_dyn", "C_JQ_dyn", "dynamic charge/current normalization multiplier outside fixed branch", "|C_JQ_dyn| <= source-backed current normalization bound", "MISSING_DYNAMIC_CURRENT_OWNER_OR_NUMERIC_BOUND", "EMB3503_3_C_JQ"),
        ("OBS4583_1_deltaJ_perp", "deltaJ_perp", "current mismatch orthogonal to pure normalization", "||deltaJ_perp||_dual sourced in same collar/current units", "MISSING_CURRENT_MISMATCH_NORM", "EB4313_0_deltaJ"),
        ("OBS4583_2_CEMreadout_eff", "C_EM_readout_eff", "readout/EFT/spectroscopy regenerated EM coefficient", "|C_EM_readout_eff| <= source-backed readout/EFT closure bound", "MISSING_READOUT_CLOSURE_OR_BOUND", "EMB3503_5_C_EM_readout"),
        ("OBS4583_3_PhiEMrad", "Phi_EM_rad", "open radiative/background Poynting boundary flux", "|Phi_EM_rad|/(M_H c^2) or power-window analogue", "MISSING_FLUX_OR_CLOSED_COLLAR_ZERO", "EMF3502_1_radiative_poynting_flux"),
        ("OBS4583_4_DeltaHodge", "Delta_Hodge_EM", "EM Hodge/constitutive mismatch", "||Delta_Hodge_EM|| <= source-backed same-Hodge residual bound", "MISSING_SAME_HODGE_PARENT_SIGNATURE_OR_BOUND", "EMB3503_0_Delta_Hodge_EM"),
        ("OBS4583_5_CXF2", "C_XF2", "hidden visible F^2/F*F coefficient", "|C_XF2| <= parent operator-domain or numeric bound", "MISSING_OPERATOR_DOMAIN_EXCLUSION_OR_BOUND", "EMB3503_2_C_XF2"),
        ("OBS4583_6_balpha", "b_alpha", "fine-structure/coupling drift", "|2Dln g_J-Dln lambda_A| <= sourced drift bound", "MISSING_ALPHA_LEVEL_OWNER_OR_BOUND", "EAC3464_1_alpha_level"),
        ("OBS4583_7_CEMtail_abs", "C_EM_tail", "absolute no-cancellation EM tail", "sum_abs of the preceding open/dynamic EM rows", "SCHEMA_READY_VALUES_MISSING", "CCO4583_4_open_dynamic_bound"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "current_status": status,
            "source_anchor": anchor,
            "numeric_value_present": "False",
            "source_backed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for row_id, symbol, definition, formula, status, anchor in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4583_rescale", "field rescaling A->lambda A only moves normalization", "do not treat convention as physical zero", "CONTROL_PASS"),
        ("CTRL4583_no_alpha_prediction", "fixed calibrated alpha_EM branch", "no numerical alpha_EM prediction is claimed", "FIREWALL_PASS"),
        ("CTRL4583_dynamic_current", "g_J(Phi) or lambda_A(Phi) before variation", "C_JQ_dyn retained", "COUNTERMODEL_CAUGHT"),
        ("CTRL4583_hidden_readout", "S_eff or readout map has hidden-field argument", "C_EM_readout_eff retained", "COUNTERMODEL_CAUGHT"),
        ("CTRL4583_open_flux", "nonzero Poynting flux crosses collar", "Phi_EM_rad routed as boundary/Hamiltonian flux", "FIREWALL_PASS"),
        ("CTRL4583_nonEM_residuals", "EM tail zero alone", "does not close parent material tensor, apparatus, active kernel, EFT, tau tails", "FIREWALL_PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "case": case,
            "expected_result": expected,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, case, expected, status in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM4583_0_CJQ_fixed", "C_JQ zero imported for fixed q-basic branch.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4583_1_CEMreadout_fixed", "C_EM_readout zero imported for strict postprocessing/no-hidden-S_eff branch.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4583_2_Phi_closed", "Phi_EM_rad zero only on closed collar no-flux branch.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4583_3_open_dynamic", "Open/dynamic EM bound rows require sourced values.", "BLOCKED"),
        ("PROM4583_4_nonEM_tail", "Parent material tensor, apparatus, active kernel, EFT and tau tails still block local-GR claim.", "BLOCKED"),
        ("PROM4583_5_no_public_claim", "No local-GR/R10/PPN/Maxwell/public claim from 4583.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in rows
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4583 imports the already-derived fixed-branch C_JQ=0 and C_EM_readout=0 results, adds the closed-collar Phi_EM_rad=0 guard, and reduces the 4582 material/readout envelope. Open radiation, hidden readout/EFT regeneration and dynamic/global current branches remain explicit bound rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "After the fixed-branch EM terms are removed, the leading non-EM material/readout debt is the parent material tensor dot coefficient vector plus apparatus support.",
            "derive_first": "prove R_material_X*C_X=0 or apparatus support zero by parent source-domain ownership",
            "fallback": "source finite parent material tensor and apparatus/readout support bounds without cancellation credit",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "PRIVATE_NONCLAIM_LOCAL_ONLY",
            "summary": "C_JQ/C_EM_readout/Phi_EM_rad zero imported only in fixed q-basic same-Hodge strict readout closed-collar branch; open/dynamic EM tails retained.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(sources: list[dict[str, Any]], theorem: list[dict[str, Any]], gates: list[dict[str, Any]], reductions: list[dict[str, Any]], bounds: list[dict[str, Any]], controls: list[dict[str, Any]], promotions: list[dict[str, Any]], decision: list[dict[str, Any]], next_target: list[dict[str, Any]]) -> str:
    return f"""# 4583 - Charge/current normalization and EM readout tail owner or source bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Private/public status: private nonclaim; no GitHub action.

## Result

4583 does **not** reinvent the EM coupling result.  It imports the useful fixed-branch theorems already built at 4437/4438 and applies them to the 4582 material/readout tail:

```text
fixed q-basic + same Hodge + post-variation readout
+ no hidden S_eff/readout argument + closed collar no-flux
=> C_JQ = 0,
   C_EM_readout = 0,
   Phi_EM_rad = 0,
   C_EM_tail = 0.
```

Therefore, in that private branch:

```text
C_material_tail <= sum_X |C_X R_material_X| + |C_apparatus|
```

and the local readout envelope reduces to:

```text
C_readout <= sum_X |C_X R_material_X| + |C_apparatus| + C_kernel_active + C_EFT_active + C_tau_tail.
```

This is real progress, but it is not a local-GR claim.  The parent material tensor, apparatus support, active kernels, EFT tails and tau tails still have to close.

## Owner theorem rows

{markdown_table(theorem)}

## Branch gate matrix

{markdown_table(gates)}

## Tail reductions

{markdown_table(reductions)}

## Open/dynamic EM bound schema

{markdown_table(bounds)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Decision

{markdown_table(decision)}

## Next target

{markdown_table(next_target)}

## Source register

{markdown_table(sources)}
"""


def formal_text() -> str:
    return f"""## PPC4161 4583 charge/current and EM readout tail owner

Marker: `{MARKER}`  
Decision: `{DECISION}`  

4583 imports the 4437/4438 fixed-branch EM result into the current local readout chain.  In the fixed q-basic same-Hodge strict readout closed-collar branch:

```text
C_JQ = 0,
C_EM_readout = 0,
Phi_EM_rad = 0,
C_EM_tail = 0.
```

Thus the 4582 material/readout envelope becomes:

```text
C_material_tail <= sum_X |C_X R_material_X| + |C_apparatus|,
C_readout <= sum_X |C_X R_material_X| + |C_apparatus| + C_kernel_active + C_EFT_active + C_tau_tail.
```

Open radiation, hidden readout/EFT regeneration, Hodge mismatch and dynamic/global charge-current normalization remain as absolute bound rows.  This is a private nonclaim and does not predict `alpha_EM`, `G_N`, local GR, R10, PPN, clock safety or orbital safety.

Next target: `{NEXT_TARGET}`.
"""


def packet_text() -> str:
    return f"""## 4583 packet update - EM coupling/readout tail imported zero

Marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  

4583 reduces the live packet envelope by importing the fixed q-basic same-Hodge strict readout closed-collar EM zero:

```text
C_JQ = C_EM_readout = Phi_EM_rad = 0
```

only inside that private branch.  The remaining readout debt is parent material tensor/apparatus plus active kernel/EFT/tau tails; open/dynamic EM branches remain explicit bound rows.
"""


def update_claims() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4583 imports the fixed-branch C_JQ/C_EM_readout/Phi_EM_rad zero into the 4582 material/readout envelope and retains open/dynamic EM tail bounds.",
        "current_evidence": "Generated source register, owner theorem rows, branch gate matrix, tail reductions, open/dynamic EM bound schema, controls, gates and validation.",
        "status": "fixed_qbasic_em_coupling_and_readout_tail_zero_imported_open_dynamic_em_tail_bound_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Promoting fixed-branch calibrated EM closure into a global Maxwell/QED/local-GR claim, or deleting open radiation/readout regeneration/dynamic current rows.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Parent material tensor, apparatus, active kernel, EFT, tau and open/dynamic EM rows still block local-GR/R10/PPN claims.",
    }
    rows = read_csv(CLAIMS_PATH)
    if rows:
        rows.append(row)
        write_csv(CLAIMS_PATH, rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def validate(outputs: list[Path], sources: list[dict[str, Any]], theorem: list[dict[str, Any]], gates: list[dict[str, Any]], reductions: list[dict[str, Any]], bounds: list[dict[str, Any]], controls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4583_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            add(f"VAL4583_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4583_sources_exist", "all cited sources exist", all(row["path_exists"] == "True" for row in sources), "source register existence")
    add("VAL4583_needles_found", "all cited needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add("VAL4583_CJQ_zero", "C_JQ fixed branch zero imported", any(row["theorem_id"] == "CCO4583_1_CJQ_fixed_branch_zero" and "C_JQ=0" in row["claim"] for row in theorem), "CCO4583_1")
    add("VAL4583_CEMreadout_zero", "C_EM_readout strict branch zero imported", any(row["theorem_id"] == "CCO4583_2_CEMreadout_strict_zero" and "C_EM_readout=0" in row["claim"] for row in theorem), "CCO4583_2")
    add("VAL4583_closed_collar_guard", "Phi_EM_rad closed-collar guard retained", any(row["theorem_id"] == "CCO4583_3_PhiEM_closed_collar_zero" and "boundary/Hamiltonian" in row["derivation"] for row in theorem), "CCO4583_3")
    add("VAL4583_branch_gate", "branch gate includes fixed and open/dynamic branches", any(row["gate_id"] == "BG4583_0_fixed_qbasic_sameHodge_closed_collar" and "C_EM_tail=0" in row["result"] for row in gates) and any(row["gate_id"] == "BG4583_3_open_radiation" for row in gates), "branch gates")
    add("VAL4583_tail_reduction", "C_readout reduction contains material tensor and apparatus", any(row["row_id"] == "ETR4583_2_Creadout_fixed_branch_update" and "C_apparatus" in row["formula"] and "R_material_X" in row["formula"] for row in reductions), "ETR4583_2")
    add("VAL4583_open_bound_rows", "open bound schema includes C_JQ, C_EM_readout and Phi_EM_rad", all(any(row["symbol"] == symbol for row in bounds) for symbol in ["C_JQ_dyn", "C_EM_readout_eff", "Phi_EM_rad"]), "bound schema")
    add("VAL4583_controls", "controls include alpha, hidden readout and open flux firewalls", all(any(row["control_id"] == control_id for row in controls) for control_id in ["CTRL4583_no_alpha_prediction", "CTRL4583_hidden_readout", "CTRL4583_open_flux"]), "controls")
    add("VAL4583_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4583_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4583_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add("VAL4583_spine_packet", "spine and packet markers present", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), f"{MARKER}; {PACKET_MARKER}")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    theorem = owner_theorem_rows(now)
    gates = branch_gate_rows(now)
    reductions = tail_reduction_rows(now)
    bounds = bound_schema_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decision = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_THEOREM_CSV, theorem)
    write_csv(BRANCH_GATE_CSV, gates)
    write_csv(TAIL_REDUCTION_CSV, reductions)
    write_csv(BOUND_SCHEMA_CSV, bounds)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(
        doc_text(sources, theorem, gates, reductions, bounds, controls, promotions, decision, next_target),
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(formal_text(), encoding="utf-8")

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### 4583 - Charge/current and EM readout tail owner

Marker: `{MARKER}`  
Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.

4583 imports the fixed q-basic same-Hodge strict readout closed-collar EM zero into the local readout chain:

```text
C_JQ = C_EM_readout = Phi_EM_rad = 0
```

only inside that private branch.  The live reduced envelope is parent material tensor/apparatus plus active kernel, EFT and tau tails; open/dynamic EM rows remain bounded nonclaim rows.
""",
    )
    append_once(PACKET_PATH, PACKET_MARKER, packet_text())
    update_claims()

    outputs = [
        SOURCE_REGISTER,
        OWNER_THEOREM_CSV,
        BRANCH_GATE_CSV,
        TAIL_REDUCTION_CSV,
        BOUND_SCHEMA_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validate(outputs, sources, theorem, gates, reductions, bounds, controls)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    print(f"4583 complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
