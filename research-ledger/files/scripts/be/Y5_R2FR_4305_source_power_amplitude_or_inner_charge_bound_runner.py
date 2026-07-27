from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4305"
CLAIM_ID = "L-146"
BRANCH = "MTS_R2FR_Y5_SOURCE_POWER_AMPLITUDE_OR_INNER_CHARGE_BOUND_RUNNER_4305"
DECISION = "A_SRC_CONDITIONALLY_ZEROED_STANDARD_BRANCH_NINNER_DOMAIN_SPLIT_NEM_SELECTOR_ZERO_OR_DELTAJ_BOUND_NONCLAIM"
MARKER = "PPC4161_SOURCE_POWER_AMPLITUDE_INNER_CHARGE_EM_REDUCTION_4305"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_POWER_AMPLITUDE_INNER_CHARGE_EM_REDUCTION_4305"
NEXT_TARGET = "4306-Y5-R2FR-inner-domain-certificate-or-QmH-bound.md"

FORMAL_PATH = FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md"
DOC_PATH = POST / "4305-Y5-R2FR-source-power-amplitude-or-inner-charge-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4305_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
U_B2_STRONG = "1.4413864308717837e-13"
DELTA_J_SMOKE_BOUND = "7.035851579866459e-13"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4305_00_4304_formal": (
        FORMAL / "320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md",
        "Next target: `4305-Y5-R2FR-source-power-amplitude-or-inner-charge-bound-runner.md`.",
        "4304 handoff to A_src, inner charge and N_EM reduction.",
    ),
    "SRC4305_01_4304_norms": (
        SOURCE_DIR / "P8_Y5_R2FR_4304_FIRST_NORM_VALUE_ROWS.csv",
        "FN4304_2_Nsrc_power_anchor",
        "N_src strong source-support anchor.",
    ),
    "SRC4305_02_4280_AJ": (
        SOURCE_DIR / "P8_Y5_R2FR_4280_AJ_COEFFICIENT_REDUCTION.csv",
        "AJR4280_4_A_src_zero",
        "conditional A_src zero from Dq/Hperp closure.",
    ),
    "SRC4305_03_4280_Hperp": (
        SOURCE_DIR / "P8_Y5_R2FR_4280_HPERP_ZERO_IMPORT.csv",
        "HPZ4280_8_conclusion",
        "Hperp=0 import inside standard Dq-closed branch.",
    ),
    "SRC4305_04_4280_routing": (
        SOURCE_DIR / "P8_Y5_R2FR_4280_M2_TRANSPORT_BGRAD_ROUTING_GATE.csv",
        "M2R4280_3_finite_route",
        "remaining AJ transport/B-gradient residuals.",
    ),
    "SRC4305_05_1538_inner": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv",
        "NINNER1538_4_finite_bound",
        "inner compact-source bound row.",
    ),
    "SRC4305_06_319_boundary": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "CM4303_3_inner_charge",
        "4303 inner charge and boundary route.",
    ),
    "SRC4305_07_4207_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv",
        "PO4207_2_Poynting_identification",
        "Poynting is Hilbert EM stress, not a second source.",
    ),
    "SRC4305_08_4208_hodge": (
        SOURCE_DIR / "P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv",
        "HZ4208_2_visible_EM_action_domain",
        "Hodge deformation zero requires visible EM action-domain exclusion.",
    ),
    "SRC4305_09_4209_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4209_OWNER_CONTRACT.csv",
        "OC4209_6_visible_EM_import",
        "calibrated visible EM import branch.",
    ),
    "SRC4305_10_4218_EM": (
        SOURCE_DIR / "P8_Y5_R2FR_4218_VISIBLE_EM_THEOREM.csv",
        "VEM4218_7_curl_zero",
        "conditional visible EM residual zero theorem.",
    ),
    "SRC4305_11_4218_EM_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_4218_VISIBLE_EM_RESIDUAL_COMPONENTS.csv",
        "R_rad_Poynting",
        "visible EM residual component envelope.",
    ),
    "SRC4305_12_3124_deltaJ": (
        SOURCE_DIR / "P8_Y5_R2FR_3124_DELTAJ_BRANCH_SELECTION_OUTPUT.csv",
        "FINITE_BEFORE_VARIATION_PROJECTS_BOTH",
        "strict default live delta_J branch.",
    ),
    "SRC4305_13_3127_deltaJ_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv",
        "WGT3127_2",
        "one-channel delta_J smoke envelope from Hilbert EM weight measure.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4305 reduces the 4304 source-pair problem instead of restating it. The standard Dq/Hperp branch "
            "imports the 4280 result A_src=0, so the private source-support anchor N_src,strong<=U_B^2 A_src "
            "collapses to N_src,strong=0 on that branch. EM/Poynting also has a clean selector-zero route through "
            "Maxwell-Hodge Hilbert stress, with a fallback N_EM envelope and a nonclaim one-channel delta_J smoke "
            "bound |delta_J|<=7.035851579866459e-13. The remaining hard blocker is inner compact-source charge: "
            "N_inner is exactly zero only on a smooth no-excision or parent no-flux/no-memory-charge domain, otherwise "
            "N_inner<=C_inner |Q_m^H| remains unfilled."
        ),
        (
            "4305 source register, A_src closure import, inner-domain split, N_EM reduction, updated Npair runner, "
            "branch scorecard, decision, firewall, status, next-target and validation CSV."
        ),
        "private_Asrc_standard_branch_zero_Ninner_domain_split_NEM_selector_nonclaim",
        (
            "Derive the inner-domain certificate or source finite C_inner and Q_m^H; then feed the updated N_pair "
            "into lambda_m and C4302_DVGAMMA_QUAD."
        ),
        (
            "Treating conditional A_src=0 as a global source theorem, using no-excision language for point/excision "
            "sources, counting Poynting twice, promoting the delta_J smoke bound to claim evidence, or claiming local GR."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def asrc_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "ASRC4305_0_4304_start",
            "N_src,strong <= U_B^2 A_src",
            U_B2_STRONG,
            "4304 source-power anchor",
            "STARTING_ANCHOR",
            "A_src missing in 4304.",
        ),
        (
            "ASRC4305_1_source_split",
            "A_src = |S_A H_L^A| scale; S_A H_L^A = S_A H_perp^A after q-basic source orthogonality",
            "",
            "4237/4239/4280",
            "SOURCE_COEFFICIENT_REDUCED",
            "q-basic source piece is not the obstruction.",
        ),
        (
            "ASRC4305_2_standard_zero",
            "all Dq_i[H_L]=0 => Hperp=0 => S_A Hperp^A=0 => A_src=0",
            "0",
            "4280 AJR4280_4_A_src_zero and HPZ4280_8_conclusion",
            "CONDITIONAL_STANDARD_BRANCH_ZERO",
            "This is the real closure lever imported into the 4305 N_pair runner.",
        ),
        (
            "ASRC4305_3_Nsrc_standard",
            "N_src,strong_standard <= U_B^2 * 0 = 0",
            "0",
            "4304 plus 4280",
            "N_SRC_STANDARD_BRANCH_ZERO",
            "Only for the standard Dq/Hperp-closed branch; transition or non-Hilbert branches do not inherit it.",
        ),
        (
            "ASRC4305_4_general_fallback",
            "N_src,general <= U_B^2 A_src_general",
            "",
            "4304 fallback",
            "GENERAL_BRANCH_STILL_NEEDS_A_SRC",
            "If Dq/Hperp closure is not admitted, A_src remains a source/profile input.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, formula, value_numeric, source_basis, status, note in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": "A_src/N_src",
                "formula": formula,
                "value_numeric": value_numeric,
                "source_basis": source_basis,
                "status": status,
                "note": note,
                "parent_signed_global": "False",
                "standard_branch_zero": str(value_numeric == "0"),
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def inner_domain_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "IN4305_0_definition",
            "N_inner = ||B_inner||_{boundary-dual}",
            "DEFINITION",
            "1538",
            "Exact boundary norm; no cancellation with N_src or EM residuals.",
        ),
        (
            "IN4305_1_smooth_no_excision_zero",
            "if partial D_inner is empty in the chosen smooth-source local domain, B_inner=0 and N_inner=0",
            "EXACT_DOMAIN_IDENTITY_CONDITIONAL",
            "new domain split using 1538 boundary definition",
            "Legitimate for a smooth-source/no-excision branch only; not valid for point/excision exterior domains.",
        ),
        (
            "IN4305_2_Hilbert_no_memory_charge",
            "if compact matter has no independent m-charge and all source variation is Hilbert/q-owned, Q_m^H=0 and N_inner=0",
            "EXACT_ZERO_ROUTE_UNSIGNED",
            "4303/1538 visible source silence route",
            "Still needs parent source-charge theorem; cannot be assumed from exterior vacuum language.",
        ),
        (
            "IN4305_3_no_flux_zero",
            "if parent local domain signs no inner memory flux, B_inner=0 and N_inner=0",
            "BOUNDARY_CERTIFICATE_REQUIRED",
            "1538 no-flux route",
            "Blocked for excision domains until boundary/zero-mode certificate is signed.",
        ),
        (
            "IN4305_4_finite_bound",
            "N_inner <= C_inner |Q_m^H|",
            "FORMULA_ONLY_INPUTS_MISSING",
            "1538 finite bound",
            "Needs C_inner, Q_m^H, boundary-dual norm and excision/domain convention.",
        ),
        (
            "IN4305_5_decision",
            "standard source branch can set N_src=0, so N_inner is now the first hard source-pair blocker",
            "NEXT_PROOF_TARGET",
            "4305 reduction",
            "Attack the domain certificate or source Q_m^H/C_inner next.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, formula, status, source_basis, note in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": "N_inner",
                "formula": formula,
                "status": status,
                "source_basis": source_basis,
                "note": note,
                "exact_zero_claimable_now": "False",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def nem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "NEM4305_0_selector_zero",
            "N_EM=0 if EM action is the same Maxwell-Hodge Hilbert action, Hodge/current/normalization are q-owned or calibrated constants, and unresolved collar Poynting flux is absent/routed",
            "",
            "191/4207/4208/4209/4218",
            "CONDITIONAL_SELECTOR_ZERO",
            "Poynting is T_EM flux; not a second force in the m-lock source.",
        ),
        (
            "NEM4305_1_residual_envelope",
            "N_EM <= |delta_w_EM| ||T_EM|| + |C_XF2 projection_XF2| + |C_JQ projection_JQ| + |b_alpha sensitivity_alpha| + ||Delta_Hodge_EM|| + |Phi_EM_rad| + |Delta_exchange|",
            "",
            "4218 residual components plus 4208/4209",
            "BOUND_ENVELOPE_READY_VALUES_MISSING",
            "Absolute no-cancellation EM residual envelope.",
        ),
        (
            "NEM4305_2_deltaJ_smoke",
            "|delta_J| <= 7.035851579866459e-13 in the one-channel material Coulomb smoke envelope",
            DELTA_J_SMOKE_BOUND,
            "3127 WGT3127_2",
            "FINITE_SMOKE_BOUND_NONCLAIM",
            "Useful scale only; not full N_EM and not claim-grade source-GM evidence.",
        ),
        (
            "NEM4305_3_hodge_zero",
            "Delta_Hodge_EM=0 if observed coframe/orientation fixes *_obs and no independent chi_EM/constitutive tensor survives",
            "",
            "4208 Hodge zero contract",
            "CONDITIONAL_ZERO_UNSIGNED_ACTION_DOMAIN",
            "Mathematical uniqueness is not enough without parent EM action-domain exclusion.",
        ),
        (
            "NEM4305_4_poynting_guard",
            "radiative Poynting flux crosses boundary => boundary/Hamiltonian flux row, not hidden static bulk source",
            "",
            "4207 and 3127",
            "ROUTE_OR_BOUND_REQUIRED",
            "Lets the Poynting intuition remain useful without double-counting it.",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, formula, value_numeric, source_basis, status, note in specs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": "N_EM",
                "formula": formula,
                "value_numeric": value_numeric,
                "source_basis": source_basis,
                "status": status,
                "note": note,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4305_0_standard_source",
            "standard Dq/Hperp source branch",
            "N_src=0, so N_pair <= N_inner + N_EM + N_rest",
            "This is the immediate improvement over 4304: A_src no longer blocks the standard branch.",
            "PARTIAL_BRANCH_REDUCTION",
        ),
        (
            "RUN4305_1_smooth_selector",
            "smooth no-excision plus EM-owner branch",
            "if partial D_inner=empty, N_EM=0, N_rest=0 then N_pair=0",
            "Exact source-pair closure is now a domain/source certificate problem, not an A_src problem.",
            "EXACT_ROUTE_CONDITIONAL_NOT_CLAIMED",
        ),
        (
            "RUN4305_2_excision_fallback",
            "compact source exterior/excision branch",
            "N_pair <= C_inner |Q_m^H| + N_EM_envelope + N_rest",
            "This is the hard realistic exterior-body branch until Q_m^H or no-flux is derived.",
            "BOUND_ROUTE_READY_INPUTS_MISSING",
        ),
        (
            "RUN4305_3_general_nonstandard",
            "general non-Hilbert branch",
            "N_pair <= U_B^2 A_src_general + C_inner |Q_m^H| + N_EM_envelope + N_rest",
            "Keeps the nonstandard branch honest instead of borrowing standard-branch A_src=0.",
            "GENERAL_FALLBACK",
        ),
        (
            "RUN4305_4_to_C4302",
            "m-lock/Gamma handoff",
            "Delta_m <= (N_pair+N_N)/lambda_m; insert into C4302_DVGAMMA_QUAD",
            "4305 reduces N_pair before the same 4302 quadratic Gamma runner.",
            "HANDOFF_READY_NOT_SCORE_READY",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, branch_name, formula, role, status in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "branch_name": branch_name,
                "formula": formula,
                "role": role,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def scorecard_rows() -> List[Dict[str, str]]:
    specs = [
        ("SC4305_0_A_src", "A_src", "CLOSED_CONDITIONAL_STANDARD_BRANCH", "4280 gives A_src=0 if standard Dq/Hperp closure is admitted."),
        ("SC4305_1_Nsrc", "N_src", "ZERO_ON_STANDARD_BRANCH", "N_src,strong <= U_B^2 A_src collapses to zero on that branch."),
        ("SC4305_2_NEM", "N_EM", "ZERO_OR_BOUND_BRANCH", "selector zero exists; residual envelope and delta_J smoke bound remain nonclaim fallback."),
        ("SC4305_3_Ninner", "N_inner", "MAIN_BLOCKER", "smooth no-excision route is exact conditional; excision branch still needs Q_m^H/C_inner."),
        ("SC4305_4_Npair", "N_pair", "PARTIALLY_REDUCED", "standard branch now N_pair <= N_inner+N_EM+N_rest."),
        ("SC4305_5_local_GR", "local GR/PPN/R10", "NOT_CLAIMED", "lambda_m, inner charge/domain, EM residuals, Khat/connection/projection still gate the result."),
    ]
    rows: List[Dict[str, str]] = []
    for score_id, item, status, note in specs:
        row = base_row()
        row.update({"score_id": score_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4305_0_gain",
            "A_SRC_REMOVED_FROM_STANDARD_BRANCH",
            "4280's Dq/Hperp result makes A_src=0 in the standard branch, so 4304's U_B^2 A_src source-support anchor collapses to zero there.",
            "Do not keep chasing A_src inside the standard branch; move pressure to N_inner/N_EM/rest.",
        ),
        (
            "DEC4305_1_EM",
            "NEM_HAS_SELECTOR_ZERO_AND_BOUND_FALLBACK",
            "Maxwell-Hodge/Poynting owner rows allow N_EM=0 only under the visible EM selector; otherwise the residual envelope and delta_J smoke bound are retained.",
            "Use Poynting as Hilbert flux or a boundary flux, never both.",
        ),
        (
            "DEC4305_2_inner",
            "INNER_CHARGE_IS_NOW_FIRST_SOURCE_PAIR_BLOCKER",
            "For smooth no-excision domains N_inner=0 by boundary identity, but exterior/excision sources still need Q_m^H/C_inner or a no-flux theorem.",
            "4306 should derive the domain certificate or source Q_m^H/C_inner.",
        ),
        (
            "DEC4305_3_next",
            "INNER_DOMAIN_CERTIFICATE_OR_QMH_BOUND_NEXT",
            "The shortest route to the local-GR source gate is now proving which local source domain MTS owns.",
            NEXT_TARGET,
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not export A_src=0 outside the standard Dq/Hperp-closed branch.",
        "Do not use the smooth no-excision N_inner=0 identity for point/excision exterior source domains.",
        "Do not promote the one-channel delta_J smoke bound to a full N_EM or local-GR claim.",
        "Do not double-count Poynting: Hilbert EM flux when owned, boundary residual when open.",
        "Do not score C4302 until N_inner, N_EM/rest, lambda_m and projection constants are all source-backed or theorem-zero.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4305_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4305_0_A_src", "A_src", "CLOSED_CONDITIONAL_STANDARD_BRANCH", "not global; transition/non-Hilbert branches still need profiles"),
        ("STAT4305_1_Nsrc", "N_src", "ZERO_ON_STANDARD_BRANCH", "derived by U_B^2 A_src with A_src=0"),
        ("STAT4305_2_Ninner", "N_inner", "MAIN_BLOCKER", "domain certificate or Q_m^H/C_inner still needed"),
        ("STAT4305_3_NEM", "N_EM", "SELECTOR_ZERO_OR_BOUND", "delta_J smoke bound imported as nonclaim component only"),
        ("STAT4305_4_Npair", "N_pair", "REDUCED_NOT_CLOSED", "standard branch N_pair <= N_inner+N_EM+N_rest"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4305_0",
            "next_target": NEXT_TARGET,
            "target_question": "Which inner source domain does the parent local branch own: smooth no-excision, no-flux excision, or finite Q_m^H?",
            "preferred_route": "derive smooth-source/no-excision or parent no-flux/no-memory-charge certificate so N_inner=0",
            "fallback_route": "source finite C_inner, Q_m^H and boundary-dual convention for N_inner <= C_inner |Q_m^H|",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 321 PPC4161 source amplitude, inner charge, and EM residual reduction

Marker: `{MARKER}`

## Decision

`{DECISION}`

4305 makes the source-pair branch sharper:

```text
4304: N_src,strong <= U_B^2 A_src
4280: A_src=0 on the standard Dq/Hperp-closed branch
therefore: N_src,strong_standard = 0.
```

This is not a global source theorem. It means the standard local branch no longer has `A_src` as its first blocker. The live standard-branch source gate is now:

```text
N_pair <= N_inner + N_EM + N_rest.
```

## A_src Closure Import

{md_table(tables["asrc"], ["row_id", "formula", "value_numeric", "status", "note"])}

## Inner Domain Split

{md_table(tables["inner"], ["row_id", "formula", "status", "note"])}

## N_EM Reduction

{md_table(tables["nem"], ["row_id", "formula", "value_numeric", "status", "note"])}

## Updated Npair Runner

{md_table(tables["runner"], ["runner_id", "branch_name", "formula", "status"])}

## Branch Scorecard

{md_table(tables["scorecard"], ["score_id", "item", "status", "note"])}

## Result

The local-GR source route is closer but still gated: `A_src` is conditionally removed in the standard branch; `N_EM` has a selector-zero route plus residual fallback; `N_inner` is now the main hard source-pair target.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4305 - source-power amplitude or inner-charge bound runner

## Verdict
- Imported the 4280 standard-branch result `A_src=0`, so the 4304 source-support term collapses to `N_src,strong_standard=0`.
- Split `N_inner` into a true smooth no-excision zero identity versus the still-open exterior/excision `C_inner |Q_m^H|` branch.
- Reduced `N_EM` to selector zero or an explicit residual envelope; imported the `|delta_J| <= {DELTA_J_SMOKE_BOUND}` smoke scale as nonclaim only.
- Updated the runner: standard branch now has `N_pair <= N_inner + N_EM + N_rest`, so the next serious target is the inner-domain certificate.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## A_src Closure Import
{md_table(tables["asrc"], ["row_id", "formula", "value_numeric", "source_basis", "status", "note"])}

## Inner Domain Split
{md_table(tables["inner"], ["row_id", "formula", "status", "source_basis", "note"])}

## N_EM Reduction
{md_table(tables["nem"], ["row_id", "formula", "value_numeric", "source_basis", "status", "note"])}

## Updated Npair Runner
{md_table(tables["runner"], ["runner_id", "branch_name", "formula", "role", "status"])}

## Branch Scorecard
{md_table(tables["scorecard"], ["score_id", "item", "status", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4305_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4305_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add(
        "VAL4305_2_Asrc_zero",
        "A_src standard-branch zero imported",
        any(row["row_id"] == "ASRC4305_2_standard_zero" and row["value_numeric"] == "0" for row in tables["asrc"]),
        "asrc_rows",
    )
    add(
        "VAL4305_3_Nsrc_zero",
        "N_src standard branch collapses to zero",
        any(row["row_id"] == "ASRC4305_3_Nsrc_standard" and row["value_numeric"] == "0" for row in tables["asrc"]),
        "asrc_rows",
    )
    add(
        "VAL4305_4_inner_split",
        "inner smooth/no-excision and finite QmH routes both exist",
        any(row["row_id"] == "IN4305_1_smooth_no_excision_zero" for row in tables["inner"])
        and any(row["row_id"] == "IN4305_4_finite_bound" for row in tables["inner"]),
        "inner_rows",
    )
    add(
        "VAL4305_5_NEM_routes",
        "N_EM selector zero and residual fallback exist",
        any(row["row_id"] == "NEM4305_0_selector_zero" for row in tables["nem"])
        and any(row["row_id"] == "NEM4305_1_residual_envelope" for row in tables["nem"]),
        "nem_rows",
    )
    add(
        "VAL4305_6_deltaJ_smoke",
        "delta_J smoke bound imported as nonclaim scale",
        any(row["row_id"] == "NEM4305_2_deltaJ_smoke" and row["value_numeric"] == DELTA_J_SMOKE_BOUND for row in tables["nem"]),
        "nem_rows",
    )
    add(
        "VAL4305_7_runner_reduced",
        "standard runner has N_pair <= N_inner + N_EM + N_rest",
        any(row["runner_id"] == "RUN4305_0_standard_source" and "N_inner + N_EM + N_rest" in row["formula"] for row in tables["runner"]),
        "runner_rows",
    )
    add(
        "VAL4305_8_claim_flags_false",
        "all generated rows keep claim flags false",
        all(
            row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False"
            for table in tables.values()
            for row in table
        ),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4305_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4305_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4305_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4305_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4305_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4305_SOURCE_REGISTER.csv",
        "asrc": SOURCE_DIR / "P8_Y5_R2FR_4305_ASRC_CLOSURE_IMPORT.csv",
        "inner": SOURCE_DIR / "P8_Y5_R2FR_4305_INNER_CHARGE_DOMAIN_SPLIT.csv",
        "nem": SOURCE_DIR / "P8_Y5_R2FR_4305_NEM_RESIDUAL_REDUCTION.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4305_NPAIR_UPDATED_RUNNER.csv",
        "scorecard": SOURCE_DIR / "P8_Y5_R2FR_4305_BRANCH_SCORECARD.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4305_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4305_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4305_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4305_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "asrc": asrc_rows(),
        "inner": inner_domain_rows(),
        "nem": nem_rows(),
        "runner": runner_rows(),
        "scorecard": scorecard_rows(),
        "decision": decision_rows(),
        "firewall": firewall_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4305 source amplitude, inner charge, and EM residual reduction

Marker: `{MARKER}`

4305 removes `A_src` as the first standard-branch blocker by importing the 4280 Dq/Hperp closure: `A_src=0`, hence `N_src,strong_standard=0`. The standard source-pair runner is now `N_pair <= N_inner + N_EM + N_rest`. EM/Poynting has a selector-zero route or residual envelope; the hard remaining source-pair target is the inner source-domain certificate or finite `C_inner |Q_m^H|` bound.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4305 packet source-pair reduction

Marker: `{PACKET_MARKER}`

Packet update: inside the standard Dq/Hperp branch, the source-support side is no longer `U_B^2 A_src`; it is zero. The remaining source-pair obstruction is domain/inner-charge plus EM residual ownership. No local-GR, PPN, R10, or global Maxwell claim fires.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
