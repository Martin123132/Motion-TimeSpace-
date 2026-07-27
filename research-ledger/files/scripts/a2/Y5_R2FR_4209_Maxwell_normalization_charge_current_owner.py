from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4209"
CLAIM_ID = "L-050"
BRANCH_ID = "MTS_R2FR_Y5_MAXWELL_NORMALIZATION_OWNER_4209"
DECISION = (
    "MAXWELL_NORMALIZATION_CHARGE_CURRENT_OWNER_CONTRACT_WRITTEN_"
    "CLASSICAL_U1_NO_GO_FOR_ABSOLUTE_ALPHA_VISIBLE_EM_CALIBRATION_ALLOWED_"
    "BALPHA_AND_F2_BOUND_ROWS_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md"
DOC_PATH = POST / "4209-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-alpha-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_MAXWELL_NORMALIZATION_OWNER_4209"
PACKET_MARKER = "PPC4161_PACKET_MAXWELL_NORMALIZATION_OWNER_4209"
NEXT_TARGET = "4210-Y5-R2FR-standard-visible-matter-import-contract-or-alpha-residual-bound-runner.md"

SOURCES = {
    "SRC4209_00_4208_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4208_DECISION.csv",
        "charge_current_scale_owned",
        "4208 handoff says charge-current scale ownership remains unsigned.",
    ),
    "SRC4209_01_224_formal": (
        FORMAL / "224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md",
        "Z_Q, mu0, charge/current normalization, alpha_EM",
        "4208 formal scale guard.",
    ),
    "SRC4209_02_3464_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
        "CLASSIFICATION_EXACT",
        "EM alpha/charge owner audit.",
    ),
    "SRC4209_03_4083_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4083_CHARGE_CURRENT_NORMALIZATION_THEOREM.csv",
        "EXACT_NO_GO_FOR_ABSOLUTE_ALPHA_FROM_U1_NOETHER_ALONE",
        "Charge/current normalization theorem and no-go.",
    ),
    "SRC4209_04_764_gate": (
        SOURCE_DIR / "P8_Y5_R10_764_CHARGE_NORMALIZATION_DESCENT_GATE.csv",
        "CNG764_2_Maxwell_kinetic_owner",
        "Charge normalization descent gate.",
    ),
    "SRC4209_05_3507_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_3507_ALPHA_COUPLING_IDENTITY.csv",
        "alpha_eff proportional to g_eff^2 = g_J^2/lambda_A",
        "Alpha coupling identity.",
    ),
    "SRC4209_06_current_bound": (
        SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "EMB3503_3_C_JQ",
        "Maxwell current owner bound vector.",
    ),
    "SRC4209_07_3862_handoff": (
        SOURCE_DIR / "P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv",
        "NEXT_GATE_IS_MAXWELL_NORMALIZATION_AND_CHARGE_CURRENT_OWNER",
        "Hodge zero theorem handoff to Maxwell normalization.",
    ),
    "SRC4209_08_notation": (
        FORMAL / "09-canonical-notation-and-units.md",
        "`α_EM`",
        "Canonical notation reserves alpha_EM for fine-structure constant.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def normalization_identity_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NI4209_0_action",
            "S_EM = -lambda_A/4 int F^2 + g_J int A.J",
            "separates kinetic normalization and source-current coupling",
            "definition",
        ),
        (
            "NI4209_1_canonical_field",
            "A_c = sqrt(lambda_A) A",
            "local canonical normalization moves coupling into the source term",
            "exact_local_identity",
        ),
        (
            "NI4209_2_effective_charge",
            "g_eff = g_J/sqrt(lambda_A)",
            "physical measured charge after canonical normalization",
            "exact_local_identity",
        ),
        (
            "NI4209_3_alpha_ratio",
            "alpha_eff proportional to g_J^2/lambda_A",
            "invariant ratio; neither g_J nor lambda_A alone is the physical coupling",
            "exact_local_identity",
        ),
        (
            "NI4209_4_vertical_residual",
            "b_alpha = D_X ln alpha_eff = 2 D_X ln g_J - D_X ln lambda_A",
            "single EM coupling leak seen by clocks, WEP, R10, binding and source normalization",
            "derived_residual_law",
        ),
        (
            "NI4209_5_derivative_lambda",
            "F(A_c/sqrt(lambda_A)) contains dln(lambda_A) wedge A_c terms if lambda_A varies",
            "field convention cannot erase derivative interactions",
            "derivative_residual_guard",
        ),
    ]
    return [
        {
            **common(),
            "identity_id": identity_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for identity_id, formula, meaning, status in rows
    ]


def owner_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "OC4209_0_compact_U1",
            "observed EM is a parent-owned compact U(1) connection descending through q",
            "relative charge labels become lattice-owned, not continuous source knobs",
            "conditional_available",
        ),
        (
            "OC4209_1_integer_reps",
            "matter charges are fixed integer representation weights n_A",
            "Lie_v n_A=0 inside a fixed representation sector",
            "conditional_relative_charge_silence",
        ),
        (
            "OC4209_2_kinetic_owner",
            "lambda_A or g_EM^2 is fixed by one parent fibre metric, level, generator norm or calibration",
            "prevents hidden f_X(Phi)F^2 or w_EM source multiplier",
            "not_parent_signed",
        ),
        (
            "OC4209_3_current_owner",
            "g_J and J_Q are normalized by the same parent object as A_Q and F_Q^2",
            "prevents source-only current multipliers and charge/readout drift",
            "not_parent_signed",
        ),
        (
            "OC4209_4_readout_constants",
            "hbar, c, clock/spectroscopy readout and alpha_EM markers descend through q or are calibrated constants",
            "prevents alpha readout from becoming a hidden clock/material marker",
            "not_parent_signed",
        ),
        (
            "OC4209_5_absolute_alpha_no_go",
            "classical compact U(1) plus Noether conservation does not determine numeric alpha_EM",
            "blocks fake prediction of fine-structure constant without extra parent scale law",
            "derived_no_go",
        ),
        (
            "OC4209_6_visible_EM_import",
            "standard visible Maxwell/charged matter with calibrated alpha_EM may be imported as the observed matter sector",
            "keeps GR/Newton reduction alive while marking alpha not predicted by MTS",
            "allowed_baseline_nonclaim",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "clause": clause,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, clause, effect, status in rows
    ]


def residual_rows() -> List[Dict[str, str]]:
    rows = [
        ("RB4209_0_w_EM", "w_EM", "independent multiplier of observed Maxwell stress", "WEP;clock;source_normalization;EM_binding", "MISSING_UNIQUE_F2_OWNER"),
        ("RB4209_1_C_XF2", "C_XF2", "hidden/motion/time field coupling to F^2 or F wedge F", "alpha_EM;clock;WEP;R10;PPN", "MISSING_OPERATOR_DOMAIN_EXCLUSION"),
        ("RB4209_2_C_JQ", "C_JQ", "charge/current normalization not fixed by same parent object", "Lorentz_force;source_charge;WEP;EM_stress_scale", "MISSING_CURRENT_OWNER"),
        ("RB4209_3_b_alpha", "b_alpha", "D_X ln(g_J^2/lambda_A)", "clock;WEP;R10;alpha_EM_drift;binding_energy", "MISSING_ALPHA_OWNER"),
        ("RB4209_4_dlnlambda", "dlnlambda_derivative", "derivative coupling from spacetime/vertical variation of lambda_A", "dispersion;current_leak;Poynting_anomaly", "MISSING_CONSTANT_KINETIC_NORM"),
        ("RB4209_5_b_marker", "b_A/b_alpha material markers", "EM/material constants do not descend through q", "composition;clock;spectroscopy;WEP", "MISSING_NO_MARKER_THEOREM"),
        ("RB4209_6_visible_calibration", "alpha_EM_calibrated", "standard visible matter constants imported but not predicted", "baseline_local_GR_matter_sector", "CALIBRATED_BASELINE_NOT_MTS_PREDICTION"),
    ]
    return [
        {
            **common(),
            "residual_id": residual_id,
            "coefficient": coefficient,
            "definition": definition,
            "observable_links": observable_links,
            "current_status": current_status,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, coefficient, definition, observable_links, current_status in rows
    ]


def route_matrix_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RM4209_0_parent_prediction",
            "parent predicts alpha_EM",
            "requires fixed parent fibre metric/level/generator norm, current owner, hbar/c/readout owner and no counterterm",
            "not_available_current_corpus",
        ),
        (
            "RM4209_1_calibrated_visible_EM",
            "standard visible EM imported with calibrated alpha_EM",
            "acceptable for local GR/Newton reduction, same as GR imports matter constants",
            "recommended_baseline",
        ),
        (
            "RM4209_2_deviation_bound",
            "MTS-specific F2/current/readout deviation retained",
            "score w_EM, C_XF2, C_JQ, b_alpha and derivative lambda rows against clocks/WEP/R10/PPN",
            "fallback_bound_route",
        ),
        (
            "RM4209_3_forbidden_shortcut",
            "set lambda_A=1 and declare alpha derived",
            "field convention only moves coupling; invariant ratio g_J^2/lambda_A remains",
            "rejected",
        ),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "requirement_or_effect": requirement_or_effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, route, requirement_or_effect, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "normalization_identity_written": "True",
            "b_alpha_residual_law_written": "True",
            "absolute_alpha_predicted": "False",
            "classical_U1_no_go_imported": "True",
            "visible_EM_calibration_allowed": "True",
            "unique_F2_parent_signed": "False",
            "charge_current_parent_signed": "False",
            "residual_bound_rows_retained": "True",
            "public_local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4209_0_no_alpha_prediction", "Do not claim numerical fine-structure alpha from classical U(1), Noether current, or field convention alone."),
        ("FW4209_1_no_lambda_convention_win", "Setting lambda_A=1 is not a proof unless g_J, current, matter readout and source normalization are fixed together."),
        ("FW4209_2_no_F2_counterterm_silence", "Any independent f_X(Phi)F^2 or w_EM term is a physical residual unless parent-forbidden."),
        ("FW4209_3_no_CJQ_silence", "Charge/current normalization drift C_JQ remains active without the same parent owner for A_Q, J_Q and q_star."),
        ("FW4209_4_visible_EM_import_label", "Standard EM import is allowed only as calibrated visible matter, not as MTS prediction of alpha_EM."),
        ("FW4209_5_no_hidden_marker", "Material, clock and EM constants must descend through q or be retained as b_A/b_alpha rows."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4209 locks the Maxwell normalization identity: alpha_eff is the invariant ratio g_J^2/lambda_A, b_alpha is its derivative residual, classical U1 does not predict absolute alpha, and calibrated visible EM is allowed as a nonclaim baseline while F2/current residual rows stay retained.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "Local GR can proceed with calibrated visible matter, but any MTS deviation from standard EM must now be either theorem-zero or empirically bounded.",
            "route_A": "write standard visible matter import contract with calibrated EM constants and no MTS alpha claim",
            "route_B": "build alpha residual bound runner for w_EM, C_XF2, C_JQ, b_alpha and material markers",
            "route_C": "only later revisit speculative alpha_EM prediction if a parent scale law exists",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4209_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4209_NORMALIZATION_IDENTITIES.csv": normalization_identity_rows(),
        "P8_Y5_R2FR_4209_OWNER_CONTRACT.csv": owner_contract_rows(),
        "P8_Y5_R2FR_4209_RESIDUAL_BOUND_ROWS.csv": residual_rows(),
        "P8_Y5_R2FR_4209_ROUTE_MATRIX.csv": route_matrix_rows(),
        "P8_Y5_R2FR_4209_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4209_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4209_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4209_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 225 - PPC4161 Maxwell Normalization Charge-Current Owner

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint locks the Maxwell normalization/charge-current fork after the Hodge gate.

## Normalization Identity

Write the local EM source sector as:

```text
S_EM = -lambda_A/4 int F^2 + g_J int A.J.
```

Canonical normalization:

```text
A_c = sqrt(lambda_A) A
```

gives:

```text
g_eff = g_J/sqrt(lambda_A),
alpha_eff proportional to g_J^2/lambda_A.
```

Therefore the real EM coupling residual is:

```text
b_alpha = D_X ln alpha_eff
        = 2 D_X ln g_J - D_X ln lambda_A.
```

No field convention can remove this unless the parent action also fixes the current, matter readout, source normalization and clock/spectroscopy convention.

## No-Go And Baseline

Compact U(1) and Noether conservation can own relative charge labels, but they do not determine the absolute gauge kinetic coefficient or numerical `alpha_EM`.

So there are only three honest routes:

```text
parent scale law predicts alpha_EM;
standard visible EM is imported with calibrated alpha_EM;
or deviations w_EM, C_XF2, C_JQ, b_alpha are bounded.
```

The current safe route for local GR is calibrated visible EM, not an MTS prediction of the fine-structure constant.
"""
    checkpoint = f"""# 4209 - Y5 R2FR Maxwell Normalization Charge-Current Owner Or Alpha Bound

Decision: `{DECISION}`

4209 locks the coupling identity:

```text
alpha_eff proportional to g_J^2/lambda_A,
b_alpha = 2 D_X ln g_J - D_X ln lambda_A.
```

This blocks the shortcut of setting one coefficient to one by convention and calling alpha derived.

Current status:

```text
absolute alpha_EM predicted = false;
calibrated visible EM baseline allowed = true;
w_EM, C_XF2, C_JQ, b_alpha rows retained = true.
```
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},em_local_gr,"The Maxwell normalization/charge-current owner contract is written: alpha_eff is the invariant ratio g_J^2/lambda_A and b_alpha=2D ln g_J-D ln lambda_A; classical U(1) does not predict absolute alpha_EM, calibrated visible EM is allowed as a nonclaim baseline, and w_EM/C_XF2/C_JQ/b_alpha rows remain retained.",'
        f'"4209 source audit, normalization identities, owner contract, residual bound rows, route matrix, decision row and firewall.",'
        f'private_Maxwell_normalization_nonclaim_alpha_no_go_visible_EM_calibrated,'
        f'"Write the standard visible matter import contract or build alpha residual bound runner for F2/current/material marker rows.",'
        f'"This prevents fake alpha derivations by field convention while preserving the GR-style calibrated visible matter route."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Maxwell Normalization Owner - 4209

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4209 locks the physical EM normalization invariant:

```text
alpha_eff proportional to g_J^2/lambda_A,
b_alpha = 2 D_X ln g_J - D_X ln lambda_A.
```

Classical U(1) does not predict absolute `alpha_EM`; calibrated visible EM is allowed as a nonclaim baseline for local GR, while `w_EM`, `C_XF2`, `C_JQ`, `b_alpha` and marker rows stay retained for any MTS-specific deviations."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Maxwell Normalization Owner - 4209

Marker: `{PACKET_MARKER}`

The packet now prevents the alpha shortcut: field conventions can move the EM coupling around, but the invariant ratio `g_J^2/lambda_A` is physical. MTS may import calibrated visible EM for local GR, but alpha prediction remains a separate future burden."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4209_SOURCE_REGISTER.csv"]
    identities = rows_by_file["P8_Y5_R2FR_4209_NORMALIZATION_IDENTITIES.csv"]
    contract = rows_by_file["P8_Y5_R2FR_4209_OWNER_CONTRACT.csv"]
    residuals = rows_by_file["P8_Y5_R2FR_4209_RESIDUAL_BOUND_ROWS.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4209_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4209_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4209_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4209_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4209_2_identity_ratio", "normalization identities include alpha ratio and b_alpha law", {"NI4209_3_alpha_ratio", "NI4209_4_vertical_residual"}.issubset({row["identity_id"] for row in identities})),
        ("VAL4209_3_derivative_guard", "derivative lambda guard present", any(row["identity_id"] == "NI4209_5_derivative_lambda" for row in identities)),
        ("VAL4209_4_owner_contract", "owner contract includes compact U1, kinetic, current and no-go clauses", {"OC4209_0_compact_U1", "OC4209_2_kinetic_owner", "OC4209_3_current_owner", "OC4209_5_absolute_alpha_no_go"}.issubset({row["contract_id"] for row in contract})),
        ("VAL4209_5_visible_import", "visible EM calibration baseline represented", any(row["contract_id"] == "OC4209_6_visible_EM_import" for row in contract)),
        ("VAL4209_6_residual_rows", "retained rows include w_EM, C_XF2, C_JQ and b_alpha", {"w_EM", "C_XF2", "C_JQ", "b_alpha"}.issubset({row["coefficient"] for row in residuals})),
        ("VAL4209_7_residuals_missing", "residual numeric values stay missing/nonclaim", all(row["numeric_value"] == "MISSING" for row in residuals)),
        ("VAL4209_8_route_matrix", "route matrix includes parent prediction, visible import, bound route and rejected shortcut", {"RM4209_0_parent_prediction", "RM4209_1_calibrated_visible_EM", "RM4209_2_deviation_bound", "RM4209_3_forbidden_shortcut"}.issubset({row["route_id"] for row in routes})),
        ("VAL4209_9_decision_nonclaim", "decision keeps alpha not predicted and public local claim false", decision[0]["absolute_alpha_predicted"] == "False" and decision[0]["public_local_GR_claim"] == "False"),
        ("VAL4209_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4209_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4209_12_claim_register", "claim register contains L-050", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4209_13_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4209_14_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    rows_by_file = all_rows()
    write_docs()
    update_registers()
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4209_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4209 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4209_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
