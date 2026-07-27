from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3905"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3905-Y5-R2FR-parent-product-chart-adoption-and-inheritance-stack-or-linear-coefficient-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3905_SOURCE_REGISTER.csv",
    "normal_form": SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv",
    "inheritance": SRC / "P8_Y5_R2FR_3905_INHERITANCE_STACK_ADOPTION_GATE.csv",
    "reduction": SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv",
    "zeros": SRC / "P8_Y5_R2FR_3905_LINEAR_COEFFICIENT_ZERO_ROWS.csv",
    "gate": SRC / "P8_Y5_R2FR_3905_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3905_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3905_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3905_VALIDATION.csv",
}

NORMAL_FORM = (
    "S_parent = S_EH[Q;G_*,Lambda_*] + S_vis[Psi,E(Q),theta(Q),c_vis(Q)] "
    "+ S_Y[Q,Y_loc] + S_H[Q,H_priv] + S_int^{>=2}[Q,Y_loc,H_priv] + S_B[Q]"
)
SY_FORM = (
    "S_Y=-1/2 int sqrt(-g_Q) [A_AB^{mu nu}(Q) nabla_mu Y^A nabla_nu Y^B "
    "+ M_AB^2(Q) Y^A Y^B]"
)
GR_REDUCTION = (
    "delta_Q S_parent|_{Y=H=0}=delta_Q S_EH+delta_Q S_vis+delta_Q S_B, "
    "so G_mu_nu+Lambda_* g_mu_nu=8*pi*G_* T^vis_mu_nu"
)
NEWTON_LIMIT = "weak-field slow-motion limit gives nabla^2 Phi=4*pi*G_* rho and d2x/dt2=-nabla Phi"


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
        ("SRC3905_00_next", SRC / "P8_Y5_R2FR_3904_NEXT_TARGET.csv", "NEXT3904_0", "3904 selected product-chart adoption target"),
        ("SRC3905_01_product", SRC / "P8_Y5_R2FR_3904_PRODUCT_CHART_VERTICALITY_THEOREM.csv", "PCH3904_1_Dq", "product chart Dq memory theorem"),
        ("SRC3905_02_dq_matrix", SRC / "P8_Y5_R2FR_3904_DQ_MEMORY_VERTICALITY_MATRIX.csv", "DQM3904_6_verdict", "whole q-vector memory verdict"),
        ("SRC3905_03_dobs", SRC / "P8_Y5_R2FR_3904_DOBS_E_MEMORY_READOUT_TEST.csv", "DOBS3904_3_linear_gamma_bound", "DObs/linear gamma branch"),
        ("SRC3905_04_coeff", SRC / "P8_Y5_R2FR_3904_DIRECT_DISFORMAL_SCALAR_INPUT_ROWS.csv", "COEF3904_7_K_gamma_linear", "linear coefficient fallback rows"),
        ("SRC3905_05_validation", SRC / "P8_Y5_BRR545_3904_VALIDATION.csv", "VAL3904_14_next_target", "3904 validation"),
        ("SRC3905_06_memory", SRC / "P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv", "OWN3894_1_action", "quadratic memory action"),
        ("SRC3905_07_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "boundary certificate"),
        ("SRC3905_08_coframe", SRC / "P8_Y5_R2FR_3900_SINGLE_COFRAME_LOCK_ATTEMPT.csv", "COF3900_1_single_frame", "visible single coframe branch"),
        ("SRC3905_09_response", SRC / "P8_Y5_R2FR_3901_NO_DISFORMAL_RESPONSE_EQUATION.csv", "RESP3901_1_EH_traceless", "GR no-slip response equation"),
        ("SRC3905_10_gdot", SRC / "P8_Y5_R2FR_3902_GDOT_STATIONARY_CALIBRATION_GATE.csv", "GD3902_2_bound", "Gdot/calibration branch"),
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


def normal_form_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NF3905_0_action",
            "piece": "parent normal-form action",
            "formula": NORMAL_FORM,
            "derivation_role": "adopts the 3904 product chart as an action-domain split rather than a closure slogan",
            "status": "NORMAL_FORM_CONSTRUCTED_PARENT_UNSIGNED",
            "remaining_failure": "must be accepted as the MTS local parent branch or derived from a deeper MTS action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NF3905_1_memory_quadratic",
            "piece": "memory/residual sector",
            "formula": SY_FORM,
            "derivation_role": "makes X_mem a Y_loc fibre coordinate with no linear visible stress at Y=0",
            "status": "QUADRATIC_SECTOR_READY",
            "remaining_failure": "coercivity/gap and global adoption remain separate inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NF3905_2_interactions",
            "piece": "allowed residual interactions",
            "formula": "S_int^{>=2} has no term linear in Y_loc or H_priv that couples to S_vis, E(Q), tau(Q), constants, boundary or projectors",
            "derivation_role": "forbids the hidden/disformal/source-prefactor channels that reopened local PPN leaks",
            "status": "NO_LINEAR_VISIBLE_SHADOW_RULE",
            "remaining_failure": "requires parent grammar adoption; otherwise use COEF3904 fallback rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NF3905_3_boundary",
            "piece": "boundary/reference class",
            "formula": "S_B=S_B[Q] with fixed relative class; delta_Y S_B=0 and P_loc delta_Y B_ref=0",
            "derivation_role": "closes the linear boundary anisotropy route if parent-signed",
            "status": "BOUNDARY_INHERITANCE_CLAUSE_READY",
            "remaining_failure": "3892 certificate not globally parent-owned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NF3905_4_constants",
            "piece": "visible constants and G owner",
            "formula": "G_*, Lambda_*, masses, charges, alpha and c_vis are parent coefficient slots or Q_pub-basic functions, not Y_loc readouts",
            "derivation_role": "prevents memory from hiding in fitted GM, clocks, alpha or source normalization",
            "status": "COEFFICIENT_OWNER_CLAUSE_READY",
            "remaining_failure": "G_* numerical origin is not derived; this is ownership, not calculation of its value",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def inheritance_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "INH3905_0_q_projection",
            "inheritance_clause": "q_parent(Q,Y,H)=Q",
            "zero_if_adopted": "Dq[X_mem]=0",
            "status": "ADOPTED_INSIDE_NORMAL_FORM_ONLY",
            "fallback_symbol": "C_Dq_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "INH3905_1_coframe",
            "inheritance_clause": "e_obs=E(Q), Gamma=Gamma[E(Q)], omega=omega[E(Q)]",
            "zero_if_adopted": "C_E_mem=0 and no direct disformal readout",
            "status": "ADOPTED_INSIDE_NORMAL_FORM_ONLY",
            "fallback_symbol": "C_E_mem;C_disformal_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "INH3905_2_tau_clock",
            "inheritance_clause": "tau_source=tau_charge=tau_clock=tau_readout=tau(Q)",
            "zero_if_adopted": "C_tau_mem=0",
            "status": "ADOPTED_INSIDE_NORMAL_FORM_ONLY",
            "fallback_symbol": "C_tau_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "INH3905_3_matter_constants",
            "inheritance_clause": "S_vis uses only Psi,E(Q),theta(Q),c_vis(Q)",
            "zero_if_adopted": "C_coupling_mem=0 for visible masses/charges/source scales",
            "status": "ADOPTED_INSIDE_NORMAL_FORM_ONLY",
            "fallback_symbol": "C_coupling_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "INH3905_4_boundary_projector",
            "inheritance_clause": "S_B and Pi_M/P_loc are fixed Q-domain structures before Y variation",
            "zero_if_adopted": "C_boundary_TF_linear=C_projector_TF_linear=0",
            "status": "ADOPTED_INSIDE_NORMAL_FORM_ONLY",
            "fallback_symbol": "C_boundary_TF_linear;C_projector_TF_linear",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def reduction_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RED3905_0_Y_variation",
            "claim_piece": "residual stress silence at branch",
            "equation": "delta_Q S_Y|_{Y=0,nablaY=0}=0 and delta_Q S_int^{>=2}|_{Y=H=0}=0",
            "derived_result": "memory/residual sector does not source the local metric equation on the branch",
            "status": "DERIVED_FROM_NORMAL_FORM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RED3905_1_GR_equation",
            "claim_piece": "Einstein equation reduction",
            "equation": GR_REDUCTION,
            "derived_result": "local field equation is exactly GR with parent-owned G_* and Lambda_*",
            "status": "CONDITIONAL_GR_REDUCTION_THEOREM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RED3905_2_conservation",
            "claim_piece": "conservation",
            "equation": "Diff_Q invariance of S_EH+S_vis gives nabla_mu T_vis^{mu nu}=0 when visible matter equations hold",
            "derived_result": "Bianchi/conservation gate closes inside the normal-form branch",
            "status": "CONDITIONAL_CONSERVATION_PASS",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RED3905_3_Newton",
            "claim_piece": "Newtonian limit",
            "equation": NEWTON_LIMIT,
            "derived_result": "Newtonian mechanics follows as the ordinary GR weak-field limit with G_*",
            "status": "CONDITIONAL_NEWTON_LIMIT_PASS",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RED3905_4_G_constant",
            "claim_piece": "Newton constant status",
            "equation": "G_* is a parent coupling in S_EH unless a deeper MTS normalization derives G_*=F(kappa_MTS,ell_J,...)",
            "derived_result": "not deriving numerical G is not worse than GR, but MTS needs an owner or derivation before public claim",
            "status": "G_OWNER_IDENTIFIED_VALUE_NOT_DERIVED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_rows(timestamp: str) -> list[dict[str, Any]]:
    symbols = [
        ("ZERO3905_0", "C_Dq_mem", "Dq_parent[partial_Xmem]", "q_parent(Q,Y,H)=Q"),
        ("ZERO3905_1", "C_E_mem", "DObs_e[partial_Xmem]", "e_obs=E(Q)"),
        ("ZERO3905_2", "C_tau_mem", "D_Xmem tau/clock mismatch", "tau=tau(Q)"),
        ("ZERO3905_3", "C_disformal_mem", "direct hidden/disformal X_mem coframe coefficient", "no E(Q,X), A(X)tau_tau or B(X)h slot"),
        ("ZERO3905_4", "C_boundary_TF_linear", "linear boundary traceless anisotropy", "S_B=S_B[Q] fixed relative boundary class"),
        ("ZERO3905_5", "C_projector_TF_linear", "linear projector/readout-order traceless leak", "Pi_M/P_loc fixed on Q-domain before Y variation"),
        ("ZERO3905_6", "C_coupling_mem", "D_Xmem visible coefficients/source scales", "coefficients are parent slots or Q-basic functions"),
        ("ZERO3905_7", "K_gamma_linear", "linear PPN gamma residual", "all preceding linear coefficients vanish"),
    ]
    return [
        {
            "zero_id": zero_id,
            "symbol": symbol,
            "quantity_zeroed": quantity,
            "normal_form_clause": clause,
            "status": "ZERO_IF_NORMAL_FORM_PARENT_SIGNED",
            "runner_effect": "set to zero in product-chart branch; otherwise use 3904 fallback coefficient row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for zero_id, symbol, quantity, clause in symbols
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "GATE3905_0_normal_form", "gate": "parent normal form constructed", "result": "yes, exact branch written", "status": "PASS_CONDITIONAL", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3905_1_GR_reduction", "gate": "local GR equation follows", "result": "yes inside normal-form branch at Y=H=0", "status": "PASS_CONDITIONAL", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3905_2_Newton", "gate": "Newtonian mechanics follows", "result": "yes as weak-field GR limit with G_*", "status": "PASS_CONDITIONAL", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3905_3_parent_adoption", "gate": "global MTS adopts normal form", "result": "not yet; still a candidate branch", "status": "BLOCKED_PARENT_ADOPTION", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3905_4_G_owner", "gate": "G_* value/owner derived", "result": "owner slot identified, numerical/deeper derivation open", "status": "BLOCKED_GSTAR_DERIVATION", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3905_5_local_GR_claim", "gate": "public local-GR/Newton claim", "result": "not allowed until normal form is parent-adopted and G/source normalization owner closes", "status": "BLOCKED_NO_CLAIM", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3905_0",
            "target_checkpoint": "3906-Y5-R2FR-EH-origin-and-Gstar-owner-or-low-energy-GR-branch-contract.md",
            "script": "scripts/Y5_R2FR_3906_EH_origin_and_Gstar_owner_or_low_energy_GR_branch_contract.py",
            "objective": "try to derive or own the Einstein-Hilbert/G_* sector from MTS parent scales; if not, mark local GR as a low-energy branch contract and keep G_* as measured parent coupling",
            "why_next": "3905 conditionally gets GR/Newton from the product-chart normal form; the remaining serious hinge is whether MTS derives the EH/G coupling or merely owns it",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_CONDITIONAL_LOCAL_GR_NEWTON_NORMAL_FORM_CONSTRUCTED",
            "claim": "NO_PUBLIC_LOCAL_GR_CLAIM",
            "summary": "constructed a parent product-chart normal form where memory is vertical, visible readouts inherit from Q_pub, and GR/Newton follow on Y=H=0; global adoption and G_* origin remain open",
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
    normal_form: list[dict[str, Any]],
    inheritance: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3905 - Parent Product-Chart Adoption and Inheritance Stack or Linear Coefficient Runner

Generated: `{timestamp}`

## Result

3905 constructs the candidate parent-action normal form that makes the 3904 product chart do real work:

`{NORMAL_FORM}`

with:

`{SY_FORM}`

On the local branch `Y_loc=0`, `H_priv=0`, the residual/memory stress vanishes at linear order, visible matter sees only the public geometry, and the field equation reduces to:

`{GR_REDUCTION}`

Then the usual weak-field limit gives:

`{NEWTON_LIMIT}`

So: yes, there is now a clean conditional route from MTS structure to local GR/Newton. It is not a public claim yet because this normal form is not globally adopted by the full corpus, and `G_*` is owned but not derived.

## Parent Action Normal Form

{markdown_table(normal_form, ["row_id", "piece", "formula", "status", "remaining_failure"])}

## Inheritance Stack Adoption Gate

{markdown_table(inheritance, ["row_id", "inheritance_clause", "zero_if_adopted", "status", "fallback_symbol"])}

## Local GR / Newton Reduction Theorem

{markdown_table(reduction, ["row_id", "claim_piece", "equation", "derived_result", "status"])}

## Linear Coefficient Zero Rows

{markdown_table(zeros, ["zero_id", "symbol", "quantity_zeroed", "normal_form_clause", "status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is the most useful version of the local-GR route so far:

1. `X_mem` is vertical because it is a `Y_loc` coordinate in a product chart.
2. Visible matter, clocks, constants, boundary data and projectors inherit from `Q_pub`.
3. Quadratic residual action makes memory stress vanish on the local branch.
4. GR follows conditionally; Newton follows as the standard weak-field limit.
5. The next hard question is not "is a coupling missing?" but whether MTS derives/owns the Einstein-Hilbert coupling `G_*`.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3905 CONDITIONAL LOCAL GR NEWTON NORMAL FORM -->
## 3905 Conditional Local GR/Newton Normal Form

Timestamp: `{timestamp}`

Parent normal form:
`{NORMAL_FORM}`

Memory sector:
`{SY_FORM}`

Reduction:
`{GR_REDUCTION}`

Newton limit:
`{NEWTON_LIMIT}`

Decision: this is a conditional local-GR/Newton derivation branch, not a public claim. Next hinge is EH/G_* ownership or derivation.
<!-- END 3905 CONDITIONAL LOCAL GR NEWTON NORMAL FORM -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3905 CONDITIONAL LOCAL GR NEWTON NORMAL FORM -->"
    end = "<!-- END 3905 CONDITIONAL LOCAL GR NEWTON NORMAL FORM -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    inheritance: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3905_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3905_1_normal_form", "parent normal form emitted", any(row["row_id"] == "NF3905_0_action" and "S_EH" in str(row["formula"]) for row in normal_form), "NF3905_0"))
    checks.append(("VAL3905_2_quadratic_memory", "quadratic memory sector emitted", any(row["row_id"] == "NF3905_1_memory_quadratic" for row in normal_form), "NF3905_1"))
    checks.append(("VAL3905_3_inheritance", "inheritance stack covers q/coframe/tau/constants/boundary", len(inheritance) >= 5, f"{len(inheritance)} rows"))
    checks.append(("VAL3905_4_GR", "GR reduction theorem present", any(row["row_id"] == "RED3905_1_GR_equation" and "Einstein" in str(row["claim_piece"]) for row in reduction), "RED3905_1"))
    checks.append(("VAL3905_5_Newton", "Newton limit row present", any(row["row_id"] == "RED3905_3_Newton" for row in reduction), "RED3905_3"))
    checks.append(("VAL3905_6_G_owner", "G owner/value distinction retained", any(row["row_id"] == "RED3905_4_G_constant" and "VALUE_NOT_DERIVED" in str(row["status"]) for row in reduction), "RED3905_4"))
    required_symbols = {"C_Dq_mem", "C_E_mem", "C_tau_mem", "C_disformal_mem", "C_boundary_TF_linear", "C_projector_TF_linear", "C_coupling_mem", "K_gamma_linear"}
    checks.append(("VAL3905_7_zero_rows", "all linear coefficients have conditional zero rows", required_symbols.issubset({str(row["symbol"]) for row in zeros}), f"{len(zeros)} rows"))
    checks.append(("VAL3905_8_no_claim", "local GR claim remains blocked", any(row["gate_id"] == "GATE3905_5_local_GR_claim" and "BLOCKED" in str(row["status"]) for row in gate), "GATE3905_5"))
    checks.append(("VAL3905_9_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [normal_form, inheritance, reduction, zeros, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3905_10_doc", "markdown checkpoint exists with normal form", DOC_PATH.exists() and NORMAL_FORM in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3905_11_spine", "spine updated with 3905 block", SPINE_PATH.exists() and "BEGIN 3905 CONDITIONAL LOCAL GR NEWTON NORMAL FORM" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3905_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3905*")
            if path.is_file() and ("3905-Y5" in path.name or "P8_Y5_R2FR_3905" in path.name or "P8_Y5_BRR545_3905" in path.name)
        ]
    checks.append(("VAL3905_13_formalization_untouched", "no generated 3905 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3905_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3905_15_next_target", "next target is EH/Gstar owner", any("Gstar-owner" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3906 EH/Gstar"))
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
    normal_form = normal_form_rows(timestamp)
    inheritance = inheritance_rows(timestamp)
    reduction = reduction_rows(timestamp)
    zeros = zero_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["normal_form"], normal_form)
    write_csv(OUTPUTS["inheritance"], inheritance)
    write_csv(OUTPUTS["reduction"], reduction)
    write_csv(OUTPUTS["zeros"], zeros)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, normal_form, inheritance, reduction, zeros, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, normal_form, inheritance, reduction, zeros, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_CONDITIONAL_LOCAL_GR_NEWTON_NORMAL_FORM_CONSTRUCTED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
