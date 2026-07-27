from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4334"
CLAIM_ID = "L-175"
BRANCH = "MTS_R2FR_Y5_LOCAL_TEST_PROJECTION_MATRIX_SOURCE_CONTRACT_OR_R10_PPN_SMOKE_4334"
DECISION = "LOCAL_TEST_PROJECTION_MATRIX_SOURCE_CONTRACT_BUILT_R10_PPN_SMOKE_BLOCKED_UNTIL_NUMERIC_SOURCE_ROWS_NONCLAIM"
MARKER = "PPC4161_LOCAL_TEST_PROJECTION_MATRIX_SOURCE_CONTRACT_OR_R10_PPN_SMOKE_4334"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_TEST_PROJECTION_MATRIX_SOURCE_CONTRACT_OR_R10_PPN_SMOKE_4334"
NEXT_TARGET = "4335-Y5-R2FR-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md"

FORMAL_PATH = FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md"
DOC_PATH = POST / "4334-Y5-R2FR-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4334_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4334_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4333_NEXT_TARGET.csv",
        "projection matrices",
        "4333 handoff selecting source-backed local projection matrices before scoring.",
    ),
    (
        "SRC4334_01_4333_projection",
        FORMAL / "349-PPC4161-standard-branch-source-readout-rollup-or-open-tail-test-pack.md",
        "R_arena <= Pi_arena^Xi",
        "4333 arena residual projection contract.",
    ),
    (
        "SRC4334_02_4333_pack",
        FORMAL / "349-PPC4161-standard-branch-source-readout-rollup-or-open-tail-test-pack.md",
        "TP4333_0_R10",
        "4333 open-tail local-test pack.",
    ),
    (
        "SRC4334_03_982_matrix",
        POST / "982-Y5-R10-coupling-bound-projection-matrix-skeleton-and-screening-runner.md",
        "observable_vector = ProjectionMatrix * MTS_residual_coefficient_vector",
        "Earlier projection-matrix discipline for local screening.",
    ),
    (
        "SRC4334_04_982_R10",
        SOURCE_DIR / "P8_Y5_R10_982_PROJECTION_MATRIX_SKELETON.csv",
        "PMAT982_4_R10_alpha_lambda",
        "Existing R10 alpha(lambda) projection skeleton.",
    ),
    (
        "SRC4334_05_983_WEP",
        POST / "983-Y5-R10-WEP-source-charge-projection-matrix-MICROSCOPE-TiPt.md",
        "eta_TiPt ~= DeltaQ_source dot C_source",
        "Existing WEP source-charge projection attempt.",
    ),
    (
        "SRC4334_06_PPN_vector",
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "PPN readout vector definition for local test projection.",
    ),
    (
        "SRC4334_07_PPN_framework",
        FORMAL / "59-local-ppn-branch-framework.md",
        "This is not a pass. It is the minimum metric-observable contract",
        "Older local PPN framework warning against small-source shortcuts.",
    ),
    (
        "SRC4334_08_shared_bound",
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "epsilon_mu_tr -> (Y_WEP",
        "Earlier shared local bound runner showing why projection coefficients matter.",
    ),
    (
        "SRC4334_09_Xi_open",
        FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md",
        "Xi_open <= C_w",
        "Xi open-tail source-label bound.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                "4334 converts the 4333 open-tail test pack into an explicit projection-matrix source contract. The local test residual vector is now R_arena = Pi_arena T_open, where T_open contains Xi_open, epsilon_EM_open_boundary, epsilon_coeff_open, epsilon_projection_open, tail_guard_sum, epsilon_tau_open, epsilon_boundary_projector_open and ordinary_matter_shadow_open. Pi_R10, Pi_PPN, Pi_clock, Pi_orbital, Pi_EM and Pi_WEP must be source-backed numeric matrices fixed before scoring. The built-in R10/PPN smoke runner deliberately blocks claims because the current rows are placeholders or inherited skeletons with missing transfer constants. No local GR/R10/PPN/clock/orbital/WEP claim fires.",
                "4334 source register, open-tail vector basis, projection matrix source contract, placeholder input rows, R10/PPN smoke rows, formulas, runner, firewall, decision, status, next-target and validation CSV.",
                "private_projection_matrix_source_contract_with_R10_PPN_smoke_blocked_nonclaim",
                "Fill the first source-backed projection row, prioritizing Pi_PPN gamma/beta or R10 alpha(lambda) depending on available parent coefficients and bound curves.",
                "Treating experimental bounds as direct MTS coefficient bounds; using identity projection as physics; fitting Pi matrices after residuals; scoring R10/PPN with MISSING_* rows; or promoting a blocked smoke runner to local-GR evidence.",
            ]
        )


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, path, needle, role in SOURCES:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "line_number": find_line(path, needle),
                "role": role,
            }
        )
    return rows


def tail_vector_rows() -> List[Dict[str, str]]:
    return [
        {
            "tail_id": "T4334_0_Xi",
            "symbol": "Xi_open",
            "meaning": "open hidden source-label/source-prefactor tail",
            "source_checkpoint": "4332",
            "units": "dimensionless envelope unless projected",
            "status": "MATRIX_INPUT",
        },
        {
            "tail_id": "T4334_1_EM",
            "symbol": "epsilon_EM_open_boundary",
            "meaning": "open radiation/constitutive EM collar tail",
            "source_checkpoint": "4329",
            "units": "dimensionless envelope unless projected",
            "status": "MATRIX_INPUT",
        },
        {
            "tail_id": "T4334_2_coeff",
            "symbol": "epsilon_coeff_open",
            "meaning": "dynamic coefficient/source-measure/calibration drift tail",
            "source_checkpoint": "4330",
            "units": "dimensionless or log-derivative by component",
            "status": "MATRIX_INPUT",
        },
        {
            "tail_id": "T4334_3_projection",
            "symbol": "epsilon_projection_open",
            "meaning": "post-action readout/projector/arena projection tail",
            "source_checkpoint": "4331",
            "units": "arena dependent",
            "status": "MATRIX_INPUT",
        },
        {
            "tail_id": "T4334_4_guard",
            "symbol": "tail_guard_sum",
            "meaning": "remaining unsourced nonstandard local residual guard",
            "source_checkpoint": "4328-4333",
            "units": "arena dependent",
            "status": "MATRIX_INPUT",
        },
        {
            "tail_id": "T4334_5_tau",
            "symbol": "epsilon_tau_open",
            "meaning": "clock/reference/orbital tau reopen tail",
            "source_checkpoint": "4325",
            "units": "clock/orbit dependent",
            "status": "MATRIX_INPUT",
        },
        {
            "tail_id": "T4334_6_domain",
            "symbol": "epsilon_boundary_projector_open",
            "meaning": "domain/projector/no-flux boundary reopen tail",
            "source_checkpoint": "4326",
            "units": "domain dependent",
            "status": "MATRIX_INPUT",
        },
        {
            "tail_id": "T4334_7_matter_shadow",
            "symbol": "ordinary_matter_shadow_open",
            "meaning": "ordinary matter shadow-frame tail outside action-domain descent branch",
            "source_checkpoint": "4328",
            "units": "composition/frame dependent",
            "status": "MATRIX_INPUT",
        },
    ]


def matrix_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "matrix_id": "PI4334_0_R10",
            "arena": "R10 short-range fifth-force",
            "projection_symbol": "Pi_R10(lambda)",
            "residual_vector": "R_R10(lambda)",
            "formula": "R_R10(lambda)=Pi_R10(lambda) dot T_open; alpha_pred(lambda)=K_X Qbar_XH(lambda) P_A qbarXT_vec plus open-tail terms",
            "required_numeric_inputs": "K_X; Qbar_XH(lambda); P_A qbarXT_vec; lambda_X; alpha_bound(lambda); lab composition support",
            "current_basis": "982 has PMAT982_4_R10_alpha_lambda skeleton",
            "missing_marker": "MISSING_R10_PARENT_COEFFICIENTS_AND_BOUND_CURVE",
            "valid_for_claim": "False",
        },
        {
            "matrix_id": "PI4334_1_PPN",
            "arena": "PPN/Cassini/local solar tests",
            "projection_symbol": "Pi_PPN",
            "residual_vector": "R_PPN=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G)",
            "formula": "R_PPN=Pi_PPN dot T_open plus solved metric response from K_tr,loc",
            "required_numeric_inputs": "metric Green operator; gamma/beta transfer; preferred-frame map; Gdot clock/orbital convention; range/profile",
            "current_basis": "188 defines PPN vector; 59/60 require metric closure",
            "missing_marker": "MISSING_LOCAL_METRIC_TRANSFER_MATRIX",
            "valid_for_claim": "False",
        },
        {
            "matrix_id": "PI4334_2_clock",
            "arena": "clock/redshift/atomic standards",
            "projection_symbol": "Pi_clock",
            "residual_vector": "R_clock",
            "formula": "R_clock=Pi_clock dot T_open with species sensitivities to alpha_EM, mass ratios, tau reference and EM collar tails",
            "required_numeric_inputs": "clock species map; alpha/mass sensitivity coefficients; tau reference convention; EM source normalization",
            "current_basis": "4325/4330 identify tau and coefficient reopen tails",
            "missing_marker": "MISSING_CLOCK_SPECIES_TRANSFER_MATRIX",
            "valid_for_claim": "False",
        },
        {
            "matrix_id": "PI4334_3_orbital",
            "arena": "orbital/ephemeris/binary dynamics",
            "projection_symbol": "Pi_orbital",
            "residual_vector": "R_orbital",
            "formula": "R_orbital=Pi_orbital dot T_open with GM convention, time-reference and source-support terms",
            "required_numeric_inputs": "GM convention; orbital frame; range/time transfer; source support; no-flux domain map",
            "current_basis": "4325 and 4326 identify orbital/tau/domain reopen tails",
            "missing_marker": "MISSING_ORBITAL_FRAME_AND_GM_TRANSFER_MATRIX",
            "valid_for_claim": "False",
        },
        {
            "matrix_id": "PI4334_4_EM",
            "arena": "EM/stress/Poynting/radiation",
            "projection_symbol": "Pi_EM",
            "residual_vector": "R_EM",
            "formula": "R_EM=Pi_EM dot T_open separating Hilbert EM flux from extra force/open radiation tails",
            "required_numeric_inputs": "open radiation flux; constitutive deformation; source current normalization; Hodge ownership map",
            "current_basis": "4329 separates same-Hodge zero from open radiation/constitutive branch",
            "missing_marker": "MISSING_EM_FLUX_CONSTITUTIVE_TRANSFER_MATRIX",
            "valid_for_claim": "False",
        },
        {
            "matrix_id": "PI4334_5_WEP",
            "arena": "WEP/source-composition",
            "projection_symbol": "Pi_WEP",
            "residual_vector": "R_WEP",
            "formula": "R_WEP=Pi_WEP dot T_open; eta_TiPt ~= DeltaQ_source dot C_source + marker/theta/source terms",
            "required_numeric_inputs": "composition charge basis; material sensitivity matrix; source-normalization map; marker/theta coupling map",
            "current_basis": "983 has MICROSCOPE alloy proxy deltas but no MTS source-charge basis",
            "missing_marker": "MISSING_SOURCE_CHARGE_PROJECTION",
            "valid_for_claim": "False",
        },
    ]


def placeholder_rows() -> List[Dict[str, str]]:
    rows = []
    for matrix in matrix_contract_rows():
        rows.append(
            {
                "input_id": matrix["matrix_id"].replace("PI4334", "PIN4334"),
                "projection_symbol": matrix["projection_symbol"],
                "arena": matrix["arena"],
                "numeric_matrix_present": "False",
                "source_path": "MISSING_SOURCE_PATH",
                "source_status": "MISSING_SOURCE_NUMERIC_MATRIX",
                "missing_marker": matrix["missing_marker"],
                "valid_for_claim": "False",
            }
        )
    return rows


def smoke_rows() -> List[Dict[str, str]]:
    rows = []
    for matrix in matrix_contract_rows():
        focus = "R10_PPN_FOCUS" if matrix["matrix_id"] in {"PI4334_0_R10", "PI4334_1_PPN"} else "SUPPORTING_ARENA"
        rows.append(
            {
                "smoke_id": matrix["matrix_id"].replace("PI4334", "SMOKE4334"),
                "arena": matrix["arena"],
                "focus": focus,
                "bound_input_complete": "False",
                "projection_matrix_complete": "False",
                "tail_vector_numeric": "False",
                "score_attempted": "False",
                "smoke_result": "blocked_missing_projection_matrix",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4334_0_tail_vector",
            "name": "open-tail vector",
            "formula": "T_open := (Xi_open, epsilon_EM_open_boundary, epsilon_coeff_open, epsilon_projection_open, tail_guard_sum, epsilon_tau_open, epsilon_boundary_projector_open, ordinary_matter_shadow_open)",
            "status": "DEFINED",
        },
        {
            "formula_id": "F4334_1_matrix_contract",
            "name": "projection matrix contract",
            "formula": "R_arena = Pi_arena T_open, with Pi_arena source-backed numeric and fixed before scoring",
            "status": "SOURCE_MATRIX_REQUIRED",
        },
        {
            "formula_id": "F4334_2_R10_smoke_gate",
            "name": "R10 smoke gate",
            "formula": "score_R10 only if K_X, Qbar_XH(lambda), P_A qbarXT_vec, lambda_X, Pi_R10(lambda), and alpha_bound(lambda) are numeric/source-backed",
            "status": "BLOCKED_CURRENTLY",
        },
        {
            "formula_id": "F4334_3_PPN_smoke_gate",
            "name": "PPN smoke gate",
            "formula": "score_PPN only if Pi_PPN maps T_open into (gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G) with metric-transfer provenance",
            "status": "BLOCKED_CURRENTLY",
        },
        {
            "formula_id": "F4334_4_claim_gate",
            "name": "claim gate",
            "formula": "claim_allowed=False unless every used Pi_arena row has numeric_matrix_present=True, source_status=SOURCE_BACKED_NUMERIC_MATRIX, and no MISSING_* marker",
            "status": "CLAIM_BLOCKED",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4334_0_source_backed_matrix",
            "branch_input": "all required Pi_arena rows numeric and source-backed before scoring",
            "action": "ALLOW_NONCLAIM_NUMERIC_SMOKE",
            "output": "compute R_arena and compare to sourced bound",
            "claim_policy": "still nonclaim until full arena validation passes",
        },
        {
            "runner_id": "RUN4334_1_current_placeholders",
            "branch_input": "current Pi rows contain MISSING_* or source_path=MISSING_SOURCE_PATH",
            "action": "BLOCK_SCORE",
            "output": "blocked_missing_projection_matrix",
            "claim_policy": "no local claim",
        },
        {
            "runner_id": "RUN4334_2_identity_projection",
            "branch_input": "identity Pi assumed for debugging",
            "action": "DEBUG_ONLY_REJECT_CLAIM",
            "output": "identity bounds allowed only as sanity rows",
            "claim_policy": "valid_for_claim=false",
        },
        {
            "runner_id": "RUN4334_3_postfit_matrix",
            "branch_input": "Pi chosen after residual inspection",
            "action": "REJECT_POSTFIT_PROJECTION",
            "output": "projection invalid",
            "claim_policy": "firewall",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4334_0_bound_direct",
            "forbidden_shortcut": "treat experimental bound as direct MTS coefficient bound",
            "reason": "982 already shows observable_vector requires ProjectionMatrix times MTS residual vector",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4334_1_identity",
            "forbidden_shortcut": "use identity projection as physics",
            "reason": "identity rows are debug-only and cannot replace source-backed Pi matrices",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4334_2_postfit",
            "forbidden_shortcut": "fit Pi_R10 or Pi_PPN after seeing residuals",
            "reason": "projection matrices must be frozen before scoring",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4334_3_missing_marker",
            "forbidden_shortcut": "score rows with MISSING_* markers",
            "reason": "smoke runner blocks any missing parent coefficient, bound curve or transfer matrix",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4334_4_local_claim",
            "forbidden_shortcut": "promote blocked R10/PPN smoke to local-GR evidence",
            "reason": "current 4334 rows are source-contract infrastructure only",
            "status": "BLOCK",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "summary": "The local-test bridge is now executable as a contract: define T_open, require source-backed Pi_arena matrices, and refuse R10/PPN scores while matrices or bound inputs are placeholders.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4334_0_contract",
            "item": "projection matrix source contract",
            "status": "BUILT",
            "notes": "Pi_R10, Pi_PPN, Pi_clock, Pi_orbital, Pi_EM and Pi_WEP rows defined",
        },
        {
            "status_id": "STAT4334_1_smoke",
            "item": "R10/PPN smoke runner",
            "status": "BLOCKED_BY_DESIGN",
            "notes": "current rows lack numeric source-backed matrices and bound inputs",
        },
        {
            "status_id": "STAT4334_2_testing",
            "item": "testing readiness",
            "status": "SCHEMA_READY_DATA_NOT_READY",
            "notes": "next step is filling one real projection row, not adding more gates",
        },
        {
            "status_id": "STAT4334_3_next",
            "item": "first projection row",
            "status": "NEXT_TARGET",
            "notes": "try Pi_PPN gamma/beta or R10 alpha(lambda) first",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4334_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can one projection row be made source-backed enough to run a genuine nonclaim smoke score?",
            "preferred_route": "try Pi_PPN gamma/beta from the local metric-transfer contract; if blocked, try R10 alpha(lambda) using 982/563-style K_X Qbar_XH lambda rows and a real bound curve",
            "fallback_route": "if no row can be sourced, demote current local-testing branch to closure-contract-only until parent coefficients or transfer matrices are derived",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 350 - PPC4161 local-test projection matrix source contract or R10/PPN smoke runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4334 does **not** prove public local GR, Newtonian mechanics, R10, PPN, WEP, clock safety, orbital safety, Maxwell/QED, charge normalization, or a numerical value of `G_N`.

It builds the missing bridge to testing:

```text
T_open := (Xi_open,
           epsilon_EM_open_boundary,
           epsilon_coeff_open,
           epsilon_projection_open,
           tail_guard_sum,
           epsilon_tau_open,
           epsilon_boundary_projector_open,
           ordinary_matter_shadow_open)

R_arena = Pi_arena T_open.
```

The R10/PPN smoke runner is intentionally conservative: it refuses to score until `Pi_arena` is numeric, source-backed and fixed before residuals are inspected.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Open-Tail Vector Basis

{md_table(tables["tail_vector"], ["tail_id", "symbol", "meaning", "source_checkpoint", "units", "status"])}

## Projection Matrix Contract

{md_table(tables["matrix_contract"], ["matrix_id", "arena", "projection_symbol", "residual_vector", "formula", "required_numeric_inputs", "current_basis", "missing_marker", "valid_for_claim"])}

## Placeholder Input Rows

{md_table(tables["placeholders"], ["input_id", "projection_symbol", "arena", "numeric_matrix_present", "source_path", "source_status", "missing_marker", "valid_for_claim"])}

## Smoke Runner

{md_table(tables["smoke"], ["smoke_id", "arena", "focus", "bound_input_complete", "projection_matrix_complete", "tail_vector_numeric", "score_attempted", "smoke_result", "claim_allowed", "valid_for_claim"])}

## Formula Gates

{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Runner Modes

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4334 Y5-R2FR local-test projection matrix source contract or R10/PPN smoke runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

The testing bridge is now explicit: `R_arena = Pi_arena T_open`. The R10/PPN smoke runner exists as a claim-blocking schema and refuses to score placeholders.

## Projection Contract

{md_table(tables["matrix_contract"], ["arena", "projection_symbol", "required_numeric_inputs", "missing_marker", "valid_for_claim"])}

## Smoke Status

{md_table(tables["smoke"], ["arena", "focus", "score_attempted", "smoke_result", "claim_allowed"])}

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4334_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4334_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4334_tail_vector_complete", "tail vector contains required open tails", {"Xi_open", "epsilon_EM_open_boundary", "epsilon_coeff_open", "epsilon_projection_open", "tail_guard_sum", "epsilon_tau_open", "epsilon_boundary_projector_open", "ordinary_matter_shadow_open"}.issubset({r["symbol"] for r in tables["tail_vector"]}), "tail_vector")
    add("VAL4334_matrix_symbols", "all arena matrices defined", {"Pi_R10(lambda)", "Pi_PPN", "Pi_clock", "Pi_orbital", "Pi_EM", "Pi_WEP"}.issubset({r["projection_symbol"] for r in tables["matrix_contract"]}), "matrix_contract")
    add("VAL4334_R10_contract", "R10 row requires alpha lambda inputs", any("alpha_bound(lambda)" in r["required_numeric_inputs"] and "K_X" in r["required_numeric_inputs"] for r in tables["matrix_contract"]), "matrix_contract")
    add("VAL4334_PPN_contract", "PPN row maps to full PPN vector", any("gamma-1" in r["residual_vector"] and "metric" in r["required_numeric_inputs"] for r in tables["matrix_contract"]), "matrix_contract")
    add("VAL4334_placeholders_block", "all placeholder rows block claim", all(r["numeric_matrix_present"] == "False" and r["valid_for_claim"] == "False" and "MISSING" in r["missing_marker"] for r in tables["placeholders"]), "placeholders")
    add("VAL4334_smoke_blocks", "all smoke rows are blocked and not attempted", all(r["score_attempted"] == "False" and r["claim_allowed"] == "False" and r["smoke_result"] == "blocked_missing_projection_matrix" for r in tables["smoke"]), "smoke")
    add("VAL4334_R10_PPN_focus", "R10 and PPN smoke rows are focus rows", {"R10 short-range fifth-force", "PPN/Cassini/local solar tests"}.issubset({r["arena"] for r in tables["smoke"] if r["focus"] == "R10_PPN_FOCUS"}), "smoke")
    add("VAL4334_formula_matrix", "projection matrix formula defined", any("R_arena = Pi_arena T_open" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4334_claim_gate", "claim gate requires no MISSING markers", any("no MISSING_* marker" in r["formula"] and "claim_allowed=False" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4334_runner_modes", "runner has source-backed, placeholder, identity and postfit modes", {"ALLOW_NONCLAIM_NUMERIC_SMOKE", "BLOCK_SCORE", "DEBUG_ONLY_REJECT_CLAIM", "REJECT_POSTFIT_PROJECTION"}.issubset({r["action"] for r in tables["runner"]}), "runner")
    add("VAL4334_firewall_direct_bound", "direct experimental-bound shortcut blocked", any("experimental bound" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4334_firewall_missing", "MISSING marker scoring blocked", any("MISSING_*" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4334_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4334_next_first_row", "next target fills first source-backed projection row", any("first-source-backed" in r["next_target"] and "genuine nonclaim smoke score" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4334_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4334_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4334_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4334_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4334_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4334_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4334_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4334_SOURCE_REGISTER.csv",
        "tail_vector": SOURCE_DIR / "P8_Y5_R2FR_4334_OPEN_TAIL_VECTOR_BASIS.csv",
        "matrix_contract": SOURCE_DIR / "P8_Y5_R2FR_4334_PROJECTION_MATRIX_SOURCE_CONTRACT.csv",
        "placeholders": SOURCE_DIR / "P8_Y5_R2FR_4334_PROJECTION_MATRIX_PLACEHOLDER_INPUTS.csv",
        "smoke": SOURCE_DIR / "P8_Y5_R2FR_4334_R10_PPN_SMOKE_RUNNER.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4334_FORMULA_GATES.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4334_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4334_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4334_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4334_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4334_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "tail_vector": tail_vector_rows(),
        "matrix_contract": matrix_contract_rows(),
        "placeholders": placeholder_rows(),
        "smoke": smoke_rows(),
        "formulas": formula_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
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
## PPC4161 4334 local-test projection matrix source contract

Marker: `{MARKER}`

4334 converts the open-tail local-test pack into a scoreable contract without pretending it is already scoreable. The open-tail vector is `T_open=(Xi_open, epsilon_EM_open_boundary, epsilon_coeff_open, epsilon_projection_open, tail_guard_sum, epsilon_tau_open, epsilon_boundary_projector_open, ordinary_matter_shadow_open)`, and every local arena must use `R_arena=Pi_arena T_open` with `Pi_arena` numeric, source-backed and fixed before scoring. Current `Pi_R10`, `Pi_PPN`, `Pi_clock`, `Pi_orbital`, `Pi_EM` and `Pi_WEP` rows are placeholders or inherited skeletons, so the R10/PPN smoke runner blocks claims by design.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4334 packet projection-matrix source contract

Marker: `{PACKET_MARKER}`

Packet update: the bridge from local closure to empirical testing is now `R_arena=Pi_arena T_open`. The next non-circling move is to source one real `Pi` row, preferably PPN gamma/beta or R10 alpha(lambda), then run a nonclaim smoke score.
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
