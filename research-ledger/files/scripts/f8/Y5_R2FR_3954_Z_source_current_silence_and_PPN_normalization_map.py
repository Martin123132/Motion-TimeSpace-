from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3954"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3954-Y5-R2FR-Z-source-current-silence-and-PPN-normalization-map.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3954_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv",
    "ppn": SRC / "P8_Y5_R2FR_3954_PPN_SOURCE_NORMALIZATION_RESIDUAL_MAP.csv",
    "coupling": SRC / "P8_Y5_R2FR_3954_LOCAL_COUPLING_PRODUCT_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3954_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3954_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3954_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3954_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3954_VALIDATION.csv",
}

NEXT_DOC = "3955-Y5-R2FR-observable-metric-Z-linear-coefficient-or-source-current-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3955_observable_metric_Z_linear_coefficient_or_source_current_bound.py"


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
        ("SRC3954_00_3953_next", SRC / "P8_Y5_R2FR_3953_NEXT_TARGET.csv", "NEXT3953_0", "3953 source-current handoff"),
        ("SRC3954_01_3953_double_zero", SRC / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv", "MGV3953_3_double_zero", "double-zero source leakage condition"),
        ("SRC3954_02_3953_nohair", SRC / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv", "MGV3953_4_positive_operator_condition", "positive operator needs zero J_A"),
        ("SRC3954_03_3953_ppn", SRC / "P8_Y5_R2FR_3953_KHAT_COMPARISON_REQUIREMENTS.csv", "KCR3953_4_PPN_source_normalization", "PPN source-normalization gap"),
        ("SRC3954_04_3953_linear", SRC / "P8_Y5_R2FR_3953_DELTAK_COMPONENT_TEMPLATE.csv", "DCT3953_4_source_linear", "linear source-current component"),
        ("SRC3954_05_CGM_species", SRC / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM3_species_source_charge", "species source-charge gate"),
        ("SRC3954_06_CGM_radial", SRC / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv", "CGM2_radial_hair", "radial source-hair gate"),
        ("SRC3954_07_runner_species", SRC / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "P8_species_source_charge", "source-charge residual row"),
        ("SRC3954_08_runner_frame", SRC / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "P8_frame_calibration_split", "frame calibration residual row"),
        ("SRC3954_09_Gauss", SRC / "P8_charge_current_equality_DIRECT_ATTEMPT.csv", "CC7_closed_flux_and_Gauss_calibration", "Gauss/GM source calibration"),
        ("SRC3954_10_matter_descent", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_1_R_md", "matter descent/source-only multiplier residual"),
        ("SRC3954_11_units", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_8_R_units", "source unit normalization residual"),
        ("SRC3954_12_stack_owner", SRC / "P8_EM_observed_stack_charge_lattice_owner_status.csv", "STAT3524_0_composite_theorem", "shared owner source-coupling route"),
        ("SRC3954_13_Geff_product", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_4_Geff_product", "local coupling product gate"),
        ("SRC3954_14_validation_3953", SRC / "P8_Y5_BRR545_3953_VALIDATION.csv", "VAL3953_18_no_pycache", "previous validation"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SCT3954_0_define_JA",
            "theorem_piece": "source-current definition",
            "formula": "J_A := (1/sqrt(-g)) delta S_matter / delta Z^A",
            "derived_statement": "Z^A is source-silent iff J_A=0 on the local branch, modulo boundary/support residuals.",
            "zero_condition": "matter action has no independent Z^A dependence and observable fields do not vary linearly with Z^A",
            "feeds": "R_source; DeltaK_linear_or_J_A; PPN source normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCT3954_1_chain_rule",
            "theorem_piece": "matter chain rule through observable metric",
            "formula": "J_A = 1/2 T_obs^{mu nu} C_{A mu nu} + J_A^direct + J_A^measure + J_A^support, with C_{A mu nu}:=partial g_obs_{mu nu}/partial Z^A",
            "derived_statement": "If matter descends only through g_obs, all Z-source coupling is controlled by the linear observable-metric coefficient C_A plus measure/support terms.",
            "zero_condition": "C_A|local=0, J_A^direct=0, J_A^measure=0, J_A^support=0",
            "feeds": "eta_source_AB; delta_frame_source; partial_r_ln_mu_obs",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCT3954_2_silence_theorem",
            "theorem_piece": "source-current silence theorem",
            "formula": "S_matter = Sbar_matter[psi,g_obs,theta], partial_Z g_obs|0=0, partial_Z theta|0=0, no source-only weights => J_A|0=0",
            "derived_statement": "The constructed Gamma branch plus matter descent gives local source silence without imposing a plateau axiom.",
            "zero_condition": "observable-metric descent, material-label descent, no source-only multiplier, and fixed support/worldtube",
            "feeds": "positive-operator no-hair condition in 3953",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCT3954_3_bound_if_leaky",
            "theorem_piece": "finite source-current bound",
            "formula": "|J_A| <= 1/2 ||T_obs|| ||C_A|| + |J_A^direct| + |J_A^measure| + |J_A^support|",
            "derived_statement": "If source silence fails, the failure is a bounded residual, not a hidden closure assumption.",
            "zero_condition": "not required; each term needs sourced coefficient/bound rows",
            "feeds": "P8_species_source_charge; P8_frame_calibration_split; radial/range source hair",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCT3954_4_Newton_calibration",
            "theorem_piece": "Newton/source calibration law",
            "formula": "mu_obs = G_eff M_eff; D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)",
            "derived_statement": "A constant universal coupling can be calibrated, but time/radius/species/frame/range dependence cannot be absorbed into measured GM.",
            "zero_condition": "D_X ln(G_ref w_common ell_J R_frame)=0 plus closed source flux and no derivative hair",
            "feeds": "Gdot; Newton_GM; PPN; R10; WEP source charge",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCT3954_5_GR_Newton_constant_status",
            "theorem_piece": "what can be derived about Newton G",
            "formula": "G_N is fixed by the EH/source-coupling product convention, e.g. G_eff ~ [M_EH w_common ell_J R_frame]^{-1} up to units",
            "derived_statement": "This framework can derive constancy/universality conditions for the measured coupling; its absolute value still needs parent scale or calibration unless a deeper unit theorem fixes M_EH and source normalization.",
            "zero_condition": "parent-fixed M_EH, w_common, ell_J, R_frame and no derivative/source dependence",
            "feeds": "local GR and Newtonian mechanics limit",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ppn_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PPN3954_0_C_A", "C_A := partial_Z g_obs|0", "linear observable-metric leakage", "0 if observable metric has double-zero in Z", "gamma_minus_1; eta_WEP_direct_geometry; source charge", "MISSING_C_A_COEFFICIENT", "dimensionless_or_metric_units"),
        ("PPN3954_1_J_direct", "J_A^direct", "direct matter/source dependence on Z", "0 if S_matter has no independent Z or source-only weights", "eta_source_AB; R10 source composition", "MISSING_DIRECT_SOURCE_WEIGHT_AUDIT", "source_current_units"),
        ("PPN3954_2_J_measure", "J_A^measure", "measure/coframe/material-label dependence on Z", "0 if measure/coframe/material labels descend through g_obs only", "frame calibration; clocks; WEP", "MISSING_MEASURE_DESCENT_AUDIT", "source_current_units"),
        ("PPN3954_3_J_support", "J_A^support", "worldtube/support/domain dependence on Z", "0 if source support is parent-owned and fixed before readout", "radial hair; range hair; R10", "MISSING_SUPPORT_DESCENT_AUDIT", "source_current_units"),
        ("PPN3954_4_eta_source_AB", "eta_source_AB", "species/source composition dependence", "0 if source action is selector-blind", "WEP source charge", "RETAINED_UNFILLED_NO_CLAIM", "dimensionless"),
        ("PPN3954_5_delta_frame_source", "delta_frame_source", "source variation and matter readout frame mismatch", "0 if same parent frame controls source and readout", "clock redshift; WEP; local GR", "RETAINED_UNFILLED_NO_CLAIM", "dimensionless"),
        ("PPN3954_6_partial_r_mu", "partial_r_ln_mu_obs", "radial source hair", "0 if no radial G_eff/M_eff/epsilon_mu leakage outside compact support", "Newton inverse-square; R10", "RETAINED_UNFILLED_NO_CLAIM", "inverse_length_or_envelope"),
        ("PPN3954_7_Geff_product", "D_X ln(G_ref w_common ell_J R_frame)", "local coupling product drift", "0 if all product factors are parent-constant without tuning", "Gdot; Newton; PPN; clocks", "RETAINED_PRODUCT_GATE", "derivative_units"),
        ("PPN3954_8_total_source_norm", "epsilon_source_norm_total", "sum/envelope of C_A,J_direct,J_measure,J_support,eta_source,frame,radial,range,Geff_product", "0 only if every component is theorem-zero", "local_GR; Newton; PPN", "COMPONENT_VALUES_MISSING", "dimensionless_or_vector"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "meaning": meaning,
            "zero_route": zero_route,
            "observable_links": observable_links,
            "current_status": status,
            "units": units,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, meaning, zero_route, observable_links, status, units in data
    ]


def coupling_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LCG3954_0_M_EH", "M_EH", "EH/source stress coefficient", "sets the gravitational response scale with the source product", "parent-fixed positive coefficient or calibration"),
        ("LCG3954_1_w_common", "w_common", "ordinary matter action-density line scale", "universal rescaling can be calibrated; derivatives/source dependence cannot", "single common matter scale"),
        ("LCG3954_2_ell_J", "ell_J", "Hilbert/source-current normalization", "links matter/EM source current to gravitational source", "same parent Hilbert current owner"),
        ("LCG3954_3_R_frame", "R_frame", "source/readout frame factor", "same-frame lock between source variation and observed readout", "one observed parent frame or bounded split"),
        ("LCG3954_4_Geff_product", "G_ref*w_common*ell_J*R_frame", "effective local coupling product", "D_X ln product must vanish for constant Newton/PPN source coupling", "parent identity or independent zero of every factor"),
        ("LCG3954_5_measured_GM", "mu_obs=G_eff M_eff", "measured orbital source product", "constant offset can be calibrated; derivative hair cannot", "closed flux, constant coupling, no range/species/frame drift"),
    ]
    return [
        {
            "row_id": row_id,
            "factor": factor,
            "definition": definition,
            "local_coupling_role": role,
            "zero_or_bound_requirement": requirement,
            "status": "CONDITIONAL_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, factor, definition, role, requirement in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3954_0_theorem",
            "decision": "source-current silence is derivable if matter descends through an observable metric with no first-order Z leakage",
            "basis": "J_A chain rule gives 1/2 T_obs C_A plus direct/measure/support terms",
            "effect": "the coupling gap is now a coefficient problem, not a vague missing assumption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3954_1_no_claim",
            "decision": "do not claim local Newton/GR source coupling yet",
            "basis": "C_A, direct source weights, measure descent, support descent, and coupling product constancy are not signed",
            "effect": "PPN/source-normalization residual vector remains active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3954_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the next concrete coefficient is C_A=partial_Z g_obs|0",
            "effect": "derive observable-metric double-zero or fill the source-current bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3954_0_sources", "source-backed coupling checkpoint", "all source paths and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3954_1_chain_rule", "J_A chain rule", "source current decomposed into C_A/direct/measure/support terms", "PASS_THEOREM_NONCLAIM"),
        ("CG3954_2_silence", "J_A silence", "C_A and all direct/measure/support terms are zero", "BLOCKED_COEFFICIENTS_MISSING"),
        ("CG3954_3_Geff", "coupling product constancy", "D_X ln(G_ref w_common ell_J R_frame)=0", "BLOCKED_PRODUCT_FACTORS_UNSIGNED"),
        ("CG3954_4_PPN", "source-normalized PPN/Newton", "species/frame/radius/range residuals zero or bounded", "BLOCKED_RESIDUAL_VECTOR_UNFILLED"),
        ("CG3954_5_local_GR", "local-GR/source-coupling promotion", "source current, Khat, DeltaK, and coupling product all close", "BLOCKED_NONCLAIM"),
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
        for row_id, gate, requirement, status in data
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3954_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or bound C_A = partial g_obs / partial Z at the local branch; if C_A=0, source-current silence advances, otherwise fill the finite source-current/PPN residual row",
            "success_condition": "C_A is either theorem-zero from observable-metric double-zero/descent, or represented as a sourced finite coefficient feeding eta_source_AB, frame split, and PPN/source-normalization rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3954 derives the Z-source-current chain rule, states exact silence conditions, and maps leaks into PPN/source-normalization residuals and the local coupling product gate.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3954 - Z Source-Current Silence And PPN Normalization Map

Timestamp: `{timestamp}`

## Result

3954 derives the source-current chain rule for the constructed `Z^A` branch:

`J_A := (1/sqrt(-g)) delta S_matter / delta Z^A`.

If matter descends through the observable metric, then:

`J_A = 1/2 T_obs^mu_nu C_A_mu_nu + J_A^direct + J_A^measure + J_A^support`

where:

`C_A_mu_nu := partial g_obs_mu_nu / partial Z^A`.

## Silence Condition

`J_A=0` follows if:

- `partial_Z g_obs|0=0`;
- no direct `Z` matter/source weights exist;
- measure, coframe, material labels and source support descend through the same observable structure;
- boundary/support terms are fixed before readout.

So the coupling problem is now concrete: derive or bound `C_A`.

## Newton / G Status

The framework can derive constancy and universality conditions for the measured coupling:

`D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)`.

A universal constant offset can be calibrated. Time/radius/species/frame/range dependence cannot be hidden inside measured `GM`.

The absolute value of `G_N` still needs a parent-fixed `M_EH` / source-normalization scale or external calibration.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3954_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3954_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3954 - Z Source-Current Silence And Coupling Map

Timestamp: `{timestamp}`

- Derived `J_A := (1/sqrt(-g)) delta S_matter/delta Z^A`.
- Chain rule: `J_A = 1/2 T_obs^{{mu nu}} C_A_mu_nu + J_A^direct + J_A^measure + J_A^support`.
- Exact silence route: `C_A=0`, no direct source weights, measure/coframe/material/support descent.
- Mapped leakage into source-charge, frame split, radial/range hair, and `D_X ln(G_ref w_common ell_J R_frame)`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3954 - Z Source-Current Silence And Coupling Map"
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
    theorem = theorem_rows(timestamp)
    ppn = ppn_rows(timestamp)
    coupling = coupling_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    theorem_ids = {row["row_id"] for row in theorem}
    ppn_symbols = {row["symbol"] for row in ppn}
    coupling_factors = {row["factor"] for row in coupling}
    gate_statuses = {row["status"] for row in claim_gate}
    nonclaim_groups = (theorem, ppn, coupling, decisions, claim_gate, next_target)
    checks = [
        ("VAL3954_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3954_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3954_02_JA_defined", "SCT3954_0_define_JA" in theorem_ids, "J_A definition emitted"),
        ("VAL3954_03_chain_rule", "SCT3954_1_chain_rule" in theorem_ids, "matter chain-rule source current emitted"),
        ("VAL3954_04_silence_theorem", "SCT3954_2_silence_theorem" in theorem_ids, "source-current silence theorem emitted"),
        ("VAL3954_05_Newton_calibration", "SCT3954_4_Newton_calibration" in theorem_ids and "SCT3954_5_GR_Newton_constant_status" in theorem_ids, "Newton/G calibration status emitted"),
        ("VAL3954_06_ppn_residuals", {"C_A := partial_Z g_obs|0", "J_A^direct", "J_A^measure", "J_A^support", "eta_source_AB", "delta_frame_source", "partial_r_ln_mu_obs", "D_X ln(G_ref w_common ell_J R_frame)", "epsilon_source_norm_total"}.issubset(ppn_symbols), "PPN/source-normalization residual map emitted"),
        ("VAL3954_07_coupling_product", {"M_EH", "w_common", "ell_J", "R_frame", "G_ref*w_common*ell_J*R_frame", "mu_obs=G_eff M_eff"}.issubset(coupling_factors), "local coupling product factors emitted"),
        ("VAL3954_08_claim_gate_blocks", "PASS_THEOREM_NONCLAIM" in gate_statuses and "BLOCKED_COEFFICIENTS_MISSING" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate blocks promotion while keeping theorem"),
        ("VAL3954_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to observable-metric Z coefficient"),
        ("VAL3954_10_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3954_11_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3954_12_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3954_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3954_14_spine_updated", SPINE_PATH.exists() and "3954 - Z Source-Current Silence And Coupling Map" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3954_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3954_16_script_compile", True, "script compiled before validation write"),
        ("VAL3954_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    source_rows = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    ppn = ppn_rows(timestamp)
    coupling = coupling_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["ppn"], ppn)
    write_csv(OUTPUTS["coupling"], coupling)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3954 validation failed: {failed}")

    print(f"3954 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("source-current theorem emitted; next target is C_A = partial_Z g_obs")


if __name__ == "__main__":
    run()
