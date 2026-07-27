from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3906"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3906-Y5-R2FR-EH-origin-and-Gstar-owner-or-low-energy-GR-branch-contract.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3906_SOURCE_REGISTER.csv",
    "eh_selection": SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv",
    "gstar": SRC / "P8_Y5_R2FR_3906_GSTAR_OWNER_MATRIX.csv",
    "source_bridge": SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv",
    "contract": SRC / "P8_Y5_R2FR_3906_LOW_ENERGY_GR_BRANCH_CONTRACT.csv",
    "residuals": SRC / "P8_Y5_R2FR_3906_NON_EH_AND_GSTAR_RESIDUAL_ROWS.csv",
    "gate": SRC / "P8_Y5_R2FR_3906_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3906_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3906_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3906_VALIDATION.csv",
}

EH_SELECTOR = (
    "If Q is the only public metric/coframe, S_Q is local, diffeomorphism invariant, "
    "second-order in the metric equations, and has no independent scalar/vector/tensor "
    "operator slots on the local branch, then E_Q^{mu nu}=A_* G^{mu nu}+B_* g^{mu nu}"
)
EH_ACTION = "S_Q=(1/(2*kappa_*)) int sqrt(-Q) (R[Q]-2 Lambda_*) + S_top[Q] + S_nonEH_residual"
GSTAR_OWNER = "kappa_* = 8*pi*G_*/c^4, delta_local kappa_*=0, partial_{t,r,A,lambda,Y,H} G_*=0 on the local branch"
SOURCE_COUPLING = "E_Q^{mu nu}=kappa_* T_vis^{mu nu}[E(Q),Psi] with T_vis from the same Hilbert variation used by matter and Maxwell"
LOW_ENERGY_CONTRACT = (
    "MTS local-GR branch = product chart + EH selector + constant G_* owner + same-frame Hilbert source "
    "+ silent/bounded residual sectors"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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
        ("SRC3906_00_next", SRC / "P8_Y5_R2FR_3905_NEXT_TARGET.csv", "NEXT3905_0", "3905 selected EH/Gstar target"),
        ("SRC3906_01_reduction", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_4_G_constant", "3905 GR/Newton reduction and G owner distinction"),
        ("SRC3906_02_normal_form", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_4_constants", "3905 parent normal-form constants clause"),
        ("SRC3906_03_local_eh_attempt", SRC / "P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv", "T506_EH_plus_silent_reduction", "prior local EH reduction theorem attempt"),
        ("SRC3906_04_local_eh_requirements", SRC / "P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv", "EH505_0_operator_reduction", "prior EH reduction requirements"),
        ("SRC3906_05_local_eh_failures", SRC / "P8_LOCAL_EH_REDUCTION_FAILURE_LEDGER.csv", "F506_3_calibration_missing", "prior EH failure ledger"),
        ("SRC3906_06_kappa_contract", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU1_global_coupling_status", "constant universal coupling contract"),
        ("SRC3906_07_global_superselection", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS1_kappa_not_local_field", "global coupling superselection contract"),
        ("SRC3906_08_hilbert_calibration", SRC / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM4_constant_universal_Geff", "Hilbert monopole calibration contract"),
        ("SRC3906_09_newton_stack", SRC / "P8_source_normalized_Newton_branch_STACK.csv", "SN5_EH_to_Poisson_coefficient", "source-normalized Newton branch stack"),
        ("SRC3906_10_source_owner", SRC / "P8_source_owner_parent_action_terms_CONTRACT.csv", "A5_constant_universal_coupling", "parent source owner action terms"),
        ("SRC3906_11_source_norm", SRC / "P8_Y5_SOURCE_NORM_2568_THEOREM_ATTEMPT.csv", "THM2568_4_poisson_source_match", "Hilbert worldtube source normalization theorem attempt"),
        ("SRC3906_12_maxwell", SRC / "P8_Y5_R2FR_3900_MAXWELL_EM_STRESS_CALIBRATION_GATE.csv", "EM3900_0_minimal_Maxwell", "Maxwell Hilbert stress same-frame row"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def eh_selection_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EH3906_0_selector",
            "clause": "EH operator selector",
            "statement": EH_SELECTOR,
            "derived_result": "selects Einstein tensor plus cosmological term as the unique low-derivative public metric equation",
            "status": "CONDITIONAL_OPERATOR_SELECTION_THEOREM",
            "remaining_failure": "locality/second-order/no-extra-operator assumptions must be parent-signed or residual-scored",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EH3906_1_action",
            "clause": "EH action normal form",
            "statement": EH_ACTION,
            "derived_result": "makes the 3905 S_EH block explicit and separates topological/non-EH residuals",
            "status": "ACTION_FORM_CONSTRUCTED",
            "remaining_failure": "S_nonEH_residual coefficients are not globally zeroed yet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EH3906_2_nonEH_filter",
            "clause": "non-EH operator filter",
            "statement": "R^2, R_mn R^mn, Weyl^2, nonlocal kernels, torsion/nonmetricity, projector/domain operators must be topological, field-redefinition redundant, zero, or executable residuals",
            "derived_result": "prevents EH import by making every non-EH escape channel explicit",
            "status": "RESIDUAL_FILTER_READY",
            "remaining_failure": "not all residual coefficients are numerically bounded in current local tests",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EH3906_3_Bianchi",
            "clause": "Bianchi consistency",
            "statement": "nabla_mu(G^{mu nu}+Lambda_* g^{mu nu})=0 requires nabla_mu(kappa_* T_vis^{mu nu})=0",
            "derived_result": "constant kappa_* plus same-frame matter equations close conservation; variable kappa creates an exchange residual",
            "status": "CONSERVATION_GATE_EXPLICIT",
            "remaining_failure": "constant kappa/G owner not derived from deeper MTS scale",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gstar_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "G3906_0_definition",
            "piece": "Gstar definition",
            "formula": GSTAR_OWNER,
            "result": "G_* is the local GR coupling associated with the EH block",
            "status": "OWNER_SLOT_DEFINED",
            "open_part": "numerical value of G_* is not derived from MTS scales",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "G3906_1_not_Newton_derivation",
            "piece": "anti-circularity",
            "formula": "do not derive G_* from orbital GM, fitted Newtonian mass, H0, or post-readout calibration",
            "result": "Newtonian agreement can measure G_*, not prove its parent origin",
            "status": "ANTI_CIRCULARITY_GUARD",
            "open_part": "need kappa_MTS/ell_J/topological normalization if predicting G",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "G3906_2_constant_owner",
            "piece": "constant coupling owner",
            "formula": "G_* in K_global, not Gamma(E_local); delta_local G_*=0",
            "result": "kills local Gdot/fifth-force/source-composition leakage if parent-signed",
            "status": "CONDITIONAL_SUPERSELECTION_OWNER",
            "open_part": "global coupling sector is not derived as a theorem of the full MTS parent action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "G3906_3_derivation_target",
            "piece": "deeper MTS derivation target",
            "formula": "G_* ?= F(kappa_MTS, ell_J, cell scale, action normalization, topological charge)",
            "result": "this is the next optional ambition beyond a low-energy GR branch contract",
            "status": "DERIVATION_OPEN_TARGET",
            "open_part": "no sourced function F exists in current inspected rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_bridge_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SRCBR3906_0_Hilbert",
            "bridge": "same-frame Hilbert source",
            "formula": SOURCE_COUPLING,
            "result": "ordinary matter and EM stress source the same public geometry",
            "status": "CONDITIONAL_SAME_FRAME_SOURCE_BRIDGE",
            "remaining_failure": "same-frame/no-source-prefactor inheritance must be parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SRCBR3906_1_Maxwell",
            "bridge": "Maxwell/EM stress",
            "formula": "T_EM^{mu nu}=2/sqrt(-Q) delta S_Maxwell[A,E(Q),alpha_*]/delta Q_{mu nu}",
            "result": "Poynting/vector EM stress is not an extra force; it is part of T_vis in the EH equation",
            "status": "EM_STRESS_INHERITS_HILBERT_SOURCE",
            "remaining_failure": "alpha/clock calibration remains separate from stress sourcing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SRCBR3906_2_Poisson",
            "bridge": "Poisson coefficient",
            "formula": "weak-field 00 equation gives nabla^2 Phi = (kappa_* c^4/2) rho_H = 4*pi*G_* rho_H",
            "result": "Newtonian coefficient follows once kappa_*=8*pi G_*/c^4 and source mass is Hilbert-normalized",
            "status": "CONDITIONAL_POISSON_COEFFICIENT",
            "remaining_failure": "worldtube Hilbert mass and measured-source normalization remain parent-conditional",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SRCBR3906_3_exchange",
            "bridge": "variable coupling exchange guard",
            "formula": "if nabla_mu kappa_* != 0 then q_exchange^nu = T_vis^{mu nu} nabla_mu kappa_* / kappa_*",
            "result": "any nonconstant G branch becomes a scored residual instead of being hidden in measured GM",
            "status": "EXCHANGE_RESIDUAL_FORMULA_READY",
            "remaining_failure": "requires numeric/source rows if G_* superselection is not signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "LEGR3906_0_scope",
            "contract": LOW_ENERGY_CONTRACT,
            "meaning": "this is the honest local-GR branch contract, not a claim that full MTS has been globally derived",
            "status": "CONTRACT_WRITTEN_NONCLAIM",
            "fallback_if_missing": "keep explicit non-EH/G/source residual vector active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "LEGR3906_1_EH_origin",
            "contract": "EH shape is derived by operator-selection assumptions; EH absolute normalization is G_* owner",
            "meaning": "operator form and coupling value are deliberately separated",
            "status": "SEPARATION_OF_FIGHTS",
            "fallback_if_missing": "do not pretend deriving GR also derives numerical G",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "LEGR3906_2_public_claim_policy",
            "contract": "public wording may say conditional local-GR branch exists; it may not say MTS derives G or passes local GR",
            "meaning": "keeps GitHub/journal-facing statements disciplined",
            "status": "CLAIM_DISCIPLINE_POLICY",
            "fallback_if_missing": "overclaim risk",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RES3906_0_nonEH", "c_nonEH_operator_vector", "coefficients for R^2/Ricci^2/Weyl^2/nonlocal/torsion/projector operators", "dimensionless or length-scaled by operator", "blocks EH-only/local PPN if nonzero"),
        ("RES3906_1_Gdot", "dln_Gstar_dt", "time derivative of local gravitational coupling", "1/time", "Gdot/clock/source-coupling residual"),
        ("RES3906_2_radial", "partial_r_ln_Gstar", "radial derivative of G_* or measured source strength", "1/length", "radial fifth-force/source-normalization residual"),
        ("RES3906_3_species", "partial_A_ln_Gstar", "species/material/source-label derivative of G_* or active source coupling", "dimensionless per material coordinate", "WEP/source-charge residual"),
        ("RES3906_4_range", "alpha_Gstar_lambda", "finite-range coupling amplitude if G_* is mediated by a local scalar/range field", "dimensionless", "R10/Yukawa residual"),
        ("RES3906_5_source_norm", "epsilon_Hilbert_mass_norm", "mismatch between Hilbert worldtube mass and measured orbital source mass", "dimensionless", "Newton/GM anti-circularity residual"),
        ("RES3906_6_exchange", "q_kappa_exchange^nu", "Bianchi exchange current from nonconstant kappa_*", "force density", "conservation/source coupling residual"),
    ]
    return [
        {
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "zero_route": "G_* superselection + EH selector + Hilbert source normalization",
            "fallback_use": fallback,
            "status": "ACTIVE_UNTIL_THEOREM_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for residual_id, symbol, definition, units, fallback in rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "GATE3906_0_EH_shape", "gate": "EH operator shape", "result": "conditionally selected by local/diffeomorphic/second-order/no-extra-operator assumptions", "status": "PASS_CONDITIONAL", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3906_1_nonEH", "gate": "non-EH residuals", "result": "not globally zero; residual vector emitted", "status": "BLOCKED_RESIDUALS_ACTIVE", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3906_2_Gstar_owner", "gate": "G_* owner", "result": "owner slot and superselection route defined", "status": "PASS_CONDITIONAL_OWNER", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3906_3_Gstar_value", "gate": "numerical G_* derivation", "result": "not derived from MTS scales", "status": "BLOCKED_VALUE_NOT_DERIVED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3906_4_source_coupling", "gate": "Hilbert/Maxwell source coupling", "result": "same-frame bridge written; source normalization still conditional", "status": "PARTIAL_CONDITIONAL", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3906_5_local_GR_claim", "gate": "local GR/Newton promotion", "result": "not allowed until non-EH residuals and G/source normalization are theorem-zero or bounded", "status": "BLOCKED_NO_CLAIM", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3906_0",
            "target_checkpoint": "3907-Y5-R2FR-Gstar-from-MTS-scales-or-measured-coupling-policy-runner.md",
            "script": "scripts/Y5_R2FR_3907_Gstar_from_MTS_scales_or_measured_coupling_policy_runner.py",
            "objective": "try to derive kappa_*/G_* from MTS scales such as kappa_MTS, ell_J, cell/action normalization or topological charge; if not, lock G_* as measured superselected coupling and run residual-policy gates",
            "why_next": "3906 separates EH-shape derivation from G-value derivation; the next honest leap is to attempt the G_* scale map directly or accept a measured-coupling branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_EH_SHAPE_CONDITIONAL_GSTAR_OWNER_SEPARATED",
            "claim": "NO_LOCAL_GR_OR_G_VALUE_CLAIM",
            "summary": "EH operator shape is conditionally selected under strict local/diffeomorphic/second-order assumptions; G_* is owned as a constant parent coupling but its numerical MTS derivation remains open",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    eh_selection: list[dict[str, Any]],
    gstar: list[dict[str, Any]],
    source_bridge: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3906 - EH Origin and Gstar Owner or Low-Energy GR Branch Contract

Generated: `{timestamp}`

## Result

3906 separates two fights that must not be blurred:

1. **EH operator shape**: why the public geometry equation is Einstein-Hilbert rather than an arbitrary metric operator.
2. **`G_*` value/owner**: why the coupling is constant/universal, and whether MTS derives its numerical value.

Conditional EH selector:

`{EH_SELECTOR}`

Action branch:

`{EH_ACTION}`

Coupling owner:

`{GSTAR_OWNER}`

Same-frame source bridge:

`{SOURCE_COUPLING}`

Verdict: MTS now has a clean low-energy GR branch contract, but not a completed local-GR claim. EH shape can be conditionally selected; `G_*` is owned as a global parent coupling unless a deeper MTS normalization derives it. That is acceptable as a GR-reduction contract, but not as a claimed prediction of Newton's constant.

## EH Operator Selection Contract

{markdown_table(eh_selection, ["row_id", "clause", "statement", "status", "remaining_failure"])}

## Gstar Owner Matrix

{markdown_table(gstar, ["row_id", "piece", "formula", "result", "status", "open_part"])}

## Hilbert Source Coupling Bridge

{markdown_table(source_bridge, ["row_id", "bridge", "formula", "result", "status", "remaining_failure"])}

## Low-Energy GR Branch Contract

{markdown_table(contract, ["contract_id", "contract", "meaning", "status", "fallback_if_missing"])}

## Non-EH and Gstar Residual Rows

{markdown_table(residuals, ["residual_id", "symbol", "definition", "units", "fallback_use", "status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This improves the project because it stops asking the wrong question. GR does not normally derive the numerical value of `G`; it uses it as a measured coupling. MTS can still be stronger if it later derives `G_*` from MTS scales, but the honest local-GR route is now:

`product chart -> EH selector -> constant G_* owner -> same-frame Hilbert/Maxwell source -> bounded residual vector`.

If any arrow fails, the failure is not handwaved; it activates `c_nonEH_operator_vector`, `dln_Gstar_dt`, source-normalization, range, species, or exchange rows.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3906 EH GSTAR OWNER CONTRACT -->
## 3906 EH Shape and Gstar Owner Contract

Timestamp: `{timestamp}`

EH selector:
`{EH_SELECTOR}`

Action branch:
`{EH_ACTION}`

G owner:
`{GSTAR_OWNER}`

Source bridge:
`{SOURCE_COUPLING}`

Decision: EH shape is conditionally selected; `G_*` is a constant parent coupling unless a deeper MTS scale map is derived. No local-GR or numerical-G claim yet.
<!-- END 3906 EH GSTAR OWNER CONTRACT -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3906 EH GSTAR OWNER CONTRACT -->"
    end = "<!-- END 3906 EH GSTAR OWNER CONTRACT -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    eh_selection: list[dict[str, Any]],
    gstar: list[dict[str, Any]],
    source_bridge: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3906_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3906_1_eh_selector", "EH selector emitted", any(row["row_id"] == "EH3906_0_selector" and "Einstein" in str(row["derived_result"]) for row in eh_selection), "EH3906_0"))
    checks.append(("VAL3906_2_nonEH_filter", "non-EH residual filter present", any(row["row_id"] == "EH3906_2_nonEH_filter" for row in eh_selection), "EH3906_2"))
    checks.append(("VAL3906_3_gstar_owner", "Gstar owner slot defined", any(row["row_id"] == "G3906_0_definition" and "kappa_*" in str(row["formula"]) for row in gstar), "G3906_0"))
    checks.append(("VAL3906_4_g_value_open", "G numerical derivation kept open", any(row["row_id"] == "G3906_3_derivation_target" and "OPEN" in str(row["status"]) for row in gstar), "G3906_3"))
    checks.append(("VAL3906_5_source_bridge", "Hilbert and Maxwell source bridge present", any(row["row_id"] == "SRCBR3906_0_Hilbert" for row in source_bridge) and any(row["row_id"] == "SRCBR3906_1_Maxwell" for row in source_bridge), "Hilbert+Maxwell"))
    checks.append(("VAL3906_6_contract", "low-energy GR branch contract written", any(row["contract_id"] == "LEGR3906_0_scope" for row in contract), "LEGR3906_0"))
    required_residuals = {"c_nonEH_operator_vector", "dln_Gstar_dt", "partial_r_ln_Gstar", "partial_A_ln_Gstar", "alpha_Gstar_lambda", "epsilon_Hilbert_mass_norm", "q_kappa_exchange^nu"}
    checks.append(("VAL3906_7_residuals", "non-EH/G/source residual rows complete", required_residuals.issubset({str(row["symbol"]) for row in residuals}), f"{len(residuals)} residuals"))
    checks.append(("VAL3906_8_no_claim", "local GR claim remains blocked", any(row["gate_id"] == "GATE3906_5_local_GR_claim" and "BLOCKED" in str(row["status"]) for row in gate), "GATE3906_5"))
    checks.append(("VAL3906_9_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [eh_selection, gstar, source_bridge, contract, residuals, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3906_10_doc", "markdown checkpoint exists with EH selector", DOC_PATH.exists() and EH_SELECTOR in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3906_11_spine", "spine updated with 3906 block", SPINE_PATH.exists() and "BEGIN 3906 EH GSTAR OWNER CONTRACT" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3906_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3906*")
            if path.is_file() and ("3906-Y5" in path.name or "P8_Y5_R2FR_3906" in path.name or "P8_Y5_BRR545_3906" in path.name)
        ]
    checks.append(("VAL3906_13_formalization_untouched", "no generated 3906 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3906_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3906_15_next_target", "next target attacks Gstar scale map", any("Gstar-from-MTS-scales" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3907 Gstar scale map"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    eh_selection = eh_selection_rows(timestamp)
    gstar = gstar_rows(timestamp)
    source_bridge = source_bridge_rows(timestamp)
    contract = contract_rows(timestamp)
    residuals = residual_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["eh_selection"], eh_selection)
    write_csv(OUTPUTS["gstar"], gstar)
    write_csv(OUTPUTS["source_bridge"], source_bridge)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, eh_selection, gstar, source_bridge, contract, residuals, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, eh_selection, gstar, source_bridge, contract, residuals, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_EH_SHAPE_CONDITIONAL_GSTAR_OWNER_SEPARATED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
