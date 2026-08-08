from __future__ import annotations

import csv
import math
from pathlib import Path


PACK_ID = "P8_Y5_R10_1335"
TITLE = "1335-Y5-R10-RAB-WEP-product-normalization-for-electron-residual-or-readout-waitstate"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PRODUCT_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_WEP_PRODUCT_NORMALIZATION_CONTRACT.csv"
WAITSTATE_PATH = OUT_DIR / f"{PACK_ID}_READOUT_SOURCE_WAITSTATE.csv"
BOUND_RESCALING_PATH = OUT_DIR / f"{PACK_ID}_EPSILON_E_BOUND_RESCALING_TABLE.csv"
INPUT_MANIFEST_PATH = OUT_DIR / f"{PACK_ID}_OFFICIAL_INPUT_REQUEST_MANIFEST.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1335_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not is_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not is_false(row.get("claim_allowed", False)):
                return False
    return True


def finite_positive(value: object) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number > 0.0


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1335*") if path.is_file()]


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1335_0_1334_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1334_NEXT_TARGET.csv",
            "needle": "NEXT1334_0_1335",
            "role": "selected 1335 target",
        },
        {
            "source_id": "SRC1335_1_1334_epsilon",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1334_ELECTRON_COEFFICIENT_SOURCE_ACQUISITION.csv",
            "needle": "EPS1334_0_existing_proxy_bound",
            "role": "epsilon_e proxy bound source",
        },
        {
            "source_id": "SRC1335_2_1334_same_branch",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1334_SAME_BRANCH_WEP_PRODUCT_REQUIREMENTS.csv",
            "needle": "SBR1334_0_tau_WEP",
            "role": "same-branch blockers",
        },
        {
            "source_id": "SRC1335_3_1330_delta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1330_AUDITED_ELECTRON_DELTA_VECTOR.csv",
            "needle": "DELTA1330_0_TA6V_minus_PtRh10_electron",
            "role": "audited electron material contrast",
        },
        {
            "source_id": "SRC1335_4_1080_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_WEP_BOUND_IMPORT.csv",
            "needle": "BOUND1080_0_MICROSCOPE_WEP_source_charge",
            "role": "MICROSCOPE eta bound anchor",
        },
        {
            "source_id": "SRC1335_5_1066_tau_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
            "needle": "TWP1066_7_verdict",
            "role": "tau_WEP projection contract",
        },
        {
            "source_id": "SRC1335_6_1083_source_caveat",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "needle": "SCG1083_0_profile_weighting",
            "role": "source-worldtube/profile caveat",
        },
        {
            "source_id": "SRC1335_7_1084_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle": "RIG1084_0_CMSM_arrays",
            "role": "official MICROSCOPE readout import gate",
        },
        {
            "source_id": "SRC1335_8_1224_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
            "needle": "FSW1224_2_tau_WEP",
            "role": "finite source-weight input contract",
        },
        {
            "source_id": "SRC1335_9_1225_acquisition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
            "needle": "ACQ1225_0_official_readout_arrays",
            "role": "tau/readout/source acquisition table",
        },
        {
            "source_id": "SRC1335_10_1334_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1334_VALIDATION.csv",
            "needle": "VAL1334_10_overall",
            "role": "1334 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    epsilon_row = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1334_ELECTRON_COEFFICIENT_SOURCE_ACQUISITION.csv"))[0]
    delta_row = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1330_AUDITED_ELECTRON_DELTA_VECTOR.csv"))[0]
    bound_row = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1080_WEP_BOUND_IMPORT.csv"))[0]
    epsilon_proxy = float(epsilon_row["value_or_bound"])
    delta_f = float(delta_row["abs_delta_fraction"])
    eta_bound = float(bound_row["bound_value"])

    product_contract = [
        {
            "contract_id": "WPN1335_0_symbolic_product",
            "formula": "|eta_TiPt| = |K_readout * S_source * O_orbit * epsilon_e * DeltaF_e|",
            "known_inputs": "DeltaF_e; eta_bound; unit-kernel epsilon_e proxy",
            "missing_inputs": "K_readout; S_source; O_orbit; same-branch parent classifier",
            "current_status": "SYMBOLIC_ONLY",
            "claim_effect": "cannot score WEP or promote epsilon_e bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "WPN1335_1_tau_eff_definition",
            "formula": "tau_eff_e := K_readout * S_source * O_orbit in the same observed coframe/readout convention",
            "known_inputs": "none numeric",
            "missing_inputs": "official arrays; source worldtube; orbit average; readout normalization",
            "current_status": "TAU_EFF_NOT_FILLED",
            "claim_effect": "unit tau_eff=1 remains a smoke convention only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "WPN1335_2_bound_formula",
            "formula": "|epsilon_e| <= eta_bound / (|DeltaF_e| * |tau_eff_e|)",
            "known_inputs": f"eta_bound={fmt(eta_bound)};DeltaF_e={fmt(delta_f)}",
            "missing_inputs": "tau_eff_e",
            "current_status": "BOUND_FORMULA_READY_TAU_MISSING",
            "claim_effect": "rescaling table can be written but no claim row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    waitstate = [
        {
            "wait_id": "WAIT1335_0_official_arrays",
            "object": "official MICROSCOPE CMSM/export arrays",
            "required_content": "time; segment/session id; gx/gz; Sxx/Sxz; masks; calibration flags; attitude/orbit convention",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "source": "RIG1084_0_CMSM_arrays;ACQ1225_0_official_readout_arrays",
            "effect": "K_readout and tau_eff_e cannot be physical",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "wait_id": "WAIT1335_1_product_convention",
            "object": "eta_AB product normalization",
            "required_content": "map from source response x material response x readout kernel to reported Eotvos eta",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source": "RIG1084_1_product_convention;ACQ1225_1_product_convention",
            "effect": "unit-kernel bound cannot become same-branch epsilon_e bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "wait_id": "WAIT1335_2_source_worldtube",
            "object": "Earth/source stress worldtube",
            "required_content": "profile-weighted source stress/current seen along MICROSCOPE orbit in observed local frame",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source": "SCG1083_0_profile_weighting;ACQ1225_2_source_worldtube",
            "effect": "source leg S_source remains absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "wait_id": "WAIT1335_3_orbit_average",
            "object": "MICROSCOPE orbit/session average",
            "required_content": "time/orbit average matched to reported eta_AB channel and masks",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source": "TWP1066_1_orbit_average;ACQ1225_3_orbit_average",
            "effect": "O_orbit remains absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "wait_id": "WAIT1335_4_parent_branch",
            "object": "same parent branch classifier",
            "required_content": "branch id linking epsilon_e, DeltaF_e, source worldtube, readout kernel, and eta bound",
            "current_status": "MISSING_BRANCH_CLASSIFIER",
            "source": "P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv:TPL1317_16",
            "effect": "branch mixing remains forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    tau_scenarios = [
        ("TAU1335_0_unit_kernel_smoke", 1.0, "UNIT_KERNEL_SMOKE_ONLY"),
        ("TAU1335_1_tau_eff_0p1_sensitivity", 0.1, "SENSITIVITY_ONLY_NOT_SOURCE_BACKED"),
        ("TAU1335_2_tau_eff_10_sensitivity", 10.0, "SENSITIVITY_ONLY_NOT_SOURCE_BACKED"),
    ]
    rescaling = [
        {
            "row_id": row_id,
            "tau_eff_assumption": fmt(tau_eff),
            "eta_bound": fmt(eta_bound),
            "delta_F_e_abs": fmt(delta_f),
            "epsilon_e_required_abs_max": fmt(eta_bound / (delta_f * abs(tau_eff))),
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, tau_eff, status in tau_scenarios
    ]

    manifest = [
        {
            "manifest_id": "MAN1335_0_readout_arrays",
            "path_or_source_needed": "source-intake/microscope/official_readout/",
            "file_expectation": "official/exported arrays with gx,gz,Sxx,Sxz,time,masks,calibration/orbit metadata",
            "used_for": "K_readout and eta product convention",
            "priority": "P0",
            "status": "WAITING_FOR_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "manifest_id": "MAN1335_1_source_worldtube",
            "path_or_source_needed": "source-intake/microscope/source_worldtube/",
            "file_expectation": "Earth/source stress profile and orbit shell weighting in observed local frame",
            "used_for": "S_source",
            "priority": "P0",
            "status": "WAITING_FOR_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "manifest_id": "MAN1335_2_product_convention",
            "path_or_source_needed": "source-intake/microscope/product_convention/",
            "file_expectation": "explicit convention mapping source/material/readout product to reported eta_TiPt",
            "used_for": "tau_eff_e normalization and units/sign",
            "priority": "P0",
            "status": "WAITING_FOR_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "manifest_id": "MAN1335_3_branch_classifier",
            "path_or_source_needed": "source-intake/mts_residuals/future_parent_branch_classifier.csv",
            "file_expectation": "same branch id for epsilon_e, DeltaF_e, tau_eff_e, and MICROSCOPE eta bound",
            "used_for": "anti-branch-mixing gate",
            "priority": "P0",
            "status": "WAITING_FOR_PARENT_OR_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1335_0_same_branch_normalization",
            "target": "same-branch WEP product for epsilon_e",
            "input_status": "TAU_EFF_MISSING",
            "runner_status": "WAITSTATE_NOT_SCOREABLE",
            "reason": "official readout arrays, product convention, source worldtube, orbit averaging, and branch classifier are missing",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1335_1_epsilon_e_bound_rescaling",
            "target": "epsilon_e bound as function of tau_eff_e",
            "input_status": "SYMBOLIC_RESCALING_READY",
            "runner_status": "NONCLAIM_SENSITIVITY_ONLY",
            "reason": "rescaling table is useful for planning but no tau_eff_e value is sourced",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1335_0_no_unit_tau_claim",
            "shortcut": "set tau_eff_e=1 and claim a physical bound",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1335_1_no_surrogate_readout_claim",
            "shortcut": "use surrogate/readout smoke rows as official MICROSCOPE readout",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1335_2_no_branch_mixing",
            "shortcut": "mix epsilon_e, material contrast, source profile, and readout from different parent branches",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1335_3_no_WEP_or_local_GR_claim",
            "shortcut": "claim WEP/local-GR pass from waitstate or sensitivity table",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1335_0_normalization_result",
            "decision": "epsilon_e cannot be normalized into a physical WEP product yet",
            "because": "tau_eff_e is not sourced and official readout/source inputs remain absent",
            "effect": "unit-kernel bound remains planning pressure only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1335_1_next_route",
            "decision": "write an official MICROSCOPE/readout/source acquisition manifest before any WEP scoring",
            "because": "the blocker is no longer algebraic; it is missing readout/source/product convention evidence",
            "effect": "future run can either import official data or explicitly pivot back to parent common-mode theory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1335_0_1336",
            "target_file": "1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot.md",
            "target_script": "scripts/Y5_R10_RAB_official_MICROSCOPE_readout_source_manifest_or_common_mode_pivot.py",
            "task": "build the official MICROSCOPE/readout/source acquisition manifest and decide whether to pursue data intake or pivot back to the parent common-mode proof",
            "success_condition": "readout/source/product convention inputs become acquisition-ready with exact paths/schemas, or the finite electron branch is paused while theory common-mode work resumes",
            "do_not": "do not score WEP from sensitivity rows, do not use surrogate arrays as official data, do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        product_contract,
        waitstate,
        rescaling,
        manifest,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    symbolic_formula_ready = any(row["contract_id"] == "WPN1335_2_bound_formula" and row["current_status"] == "BOUND_FORMULA_READY_TAU_MISSING" for row in product_contract)
    waitstate_complete = len(waitstate) == 5 and all(row["current_status"] != "FILLED" for row in waitstate)
    rescaling_finite = all(finite_positive(row["epsilon_e_required_abs_max"]) for row in rescaling)
    manifest_waiting = len(manifest) == 4 and all(str(row["status"]).startswith("WAITING") for row in manifest)
    runner_waitstate = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1336 = next_target[0]["target_file"].startswith("1336-")

    validations = [
        validation_row(
            "VAL1335_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1335_1_symbolic_formula_ready",
            "epsilon_e WEP product formula is symbolic-ready with tau missing",
            symbolic_formula_ready,
            "WPN1335_2_bound_formula=BOUND_FORMULA_READY_TAU_MISSING",
        ),
        validation_row(
            "VAL1335_2_waitstate_complete",
            "readout/source waitstate lists all required blockers",
            waitstate_complete,
            ";".join(f"{row['wait_id']}={row['current_status']}" for row in waitstate),
        ),
        validation_row(
            "VAL1335_3_rescaling_finite",
            "tau_eff sensitivity rescaling rows are finite numeric and nonclaim",
            rescaling_finite,
            ";".join(f"{row['row_id']}={row['epsilon_e_required_abs_max']}" for row in rescaling),
        ),
        validation_row(
            "VAL1335_4_manifest_waiting",
            "official input manifest remains waiting for source/readout data",
            manifest_waiting,
            ";".join(f"{row['manifest_id']}={row['status']}" for row in manifest),
        ),
        validation_row(
            "VAL1335_5_runner_waitstate",
            "runners refuse WEP/local-GR scoring",
            runner_waitstate,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1335_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1335_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1335_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1335_9_next_target_1336",
            "next target routes to official MICROSCOPE manifest or common-mode pivot",
            next_is_1336,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1335_10_overall",
            "overall 1335 validation",
            all(row["status"] == "PASS" for row in validations),
            "1335 puts epsilon_e WEP normalization into readout/source waitstate and blocks unit-kernel scoring",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PRODUCT_CONTRACT_PATH, product_contract)
    write_csv(WAITSTATE_PATH, waitstate)
    write_csv(BOUND_RESCALING_PATH, rescaling)
    write_csv(INPUT_MANIFEST_PATH, manifest)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1335 cannot convert the `epsilon_e` electron residual bound into a claim-grade WEP product. The correct product is symbolic, but the effective readout/source normalization `tau_eff_e` is not sourced.

**Main progress:** the unit-kernel bound is now quarantined as planning pressure only. The exact missing objects are official MICROSCOPE arrays, eta product convention, source-worldtube weighting, orbit averaging, and a same-parent-branch classifier.

**Decision:** no WEP, `epsilon_e`, or local-GR claim. Next work should either acquire/manifest the official MICROSCOPE/readout/source inputs or pivot back to the parent common-mode theorem route.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Electron WEP Product Normalization Contract
{markdown_table(product_contract, ["contract_id", "formula", "known_inputs", "missing_inputs", "current_status", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Readout Source Waitstate
{markdown_table(waitstate, ["wait_id", "object", "required_content", "current_status", "source", "effect", "valid_for_claim", "claim_allowed"])}

## Epsilon-e Bound Rescaling Table
{markdown_table(rescaling, ["row_id", "tau_eff_assumption", "eta_bound", "delta_F_e_abs", "epsilon_e_required_abs_max", "status", "valid_for_claim", "claim_allowed"])}

## Official Input Request Manifest
{markdown_table(manifest, ["manifest_id", "path_or_source_needed", "file_expectation", "used_for", "priority", "status", "valid_for_claim", "claim_allowed"])}

## Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "runner_status", "reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
