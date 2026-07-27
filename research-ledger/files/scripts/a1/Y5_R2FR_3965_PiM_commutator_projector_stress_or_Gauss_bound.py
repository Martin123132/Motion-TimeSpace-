from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3965"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3965-Y5-R2FR-PiM-commutator-projector-stress-or-Gauss-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3965_SOURCE_REGISTER.csv",
    "commutator": SRC / "P8_Y5_R2FR_3965_PIM_COMMUTATOR_ZERO_THEOREM_OR_BOUND.csv",
    "stress": SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv",
    "delta_vector": SRC / "P8_Y5_R2FR_3965_DELTAPIM_RESIDUAL_VECTOR.csv",
    "meff_feed": SRC / "P8_Y5_R2FR_3965_MEFF_FLUX_DELTAPIM_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3965_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3965_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3965_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3965_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3965_VALIDATION.csv",
}

NEXT_DOC = "3966-Y5-R2FR-Gauss-orbital-calibration-or-Delta-cal-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3966_Gauss_orbital_calibration_or_Delta_cal_bound.py"


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
        ("SRC3965_00_3964_next", SRC / "P8_Y5_R2FR_3964_NEXT_TARGET.csv", "NEXT3964_0", "3964 handoff"),
        ("SRC3965_01_product_rule", SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv", "HDI3964_3_product_rule", "PiM product-rule guard"),
        ("SRC3965_02_delta_pim", SRC / "P8_Y5_R2FR_3964_MEFF_FLUX_RESIDUAL_VECTOR.csv", "MFR3964_1_Delta_PiM", "Delta_PiM retained residual"),
        ("SRC3965_03_pv0", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV0_product_variation_included", "product variation exact gate"),
        ("SRC3965_04_pv1", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV1_topological_absolute_charge_route", "topological PiM route"),
        ("SRC3965_05_pv2", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV2_Hodge_DeWitt_metric_dependence_retained", "metric-dependent PiM route"),
        ("SRC3965_06_pv6", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV6_modified_exterior_residual_map", "projector stress observable map"),
        ("SRC3965_07_pm4", SRC / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM4_projector_algebra", "projector algebra"),
        ("SRC3965_08_pm5", SRC / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM5_projector_variation_owned", "projector variation owned"),
        ("SRC3965_09_pm6", SRC / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM6_flux_closure_requires_Ward_or_Euler", "projector algebra not enough"),
        ("SRC3965_10_3593", SRC / "P8_Y5_DeltaPiM_projector_variation_status.csv", "DELTAPIM_GAMMA_ZERO_DERIVED_TOTAL_BOUND_BRANCH_ACTIVE", "DeltaPiM partial zero status"),
        ("SRC3965_11_2524_def", SRC / "P8_Y5_NO_SHADOW_2524_PIM_ZERO_AUDIT.csv", "PIM2524_0_definition", "JPiM definition"),
        ("SRC3965_12_2524_rule", SRC / "P8_Y5_NO_SHADOW_2524_PIM_ZERO_AUDIT.csv", "PIM2524_1_product_rule", "commutator product rule"),
        ("SRC3965_13_2524_lemma", SRC / "P8_Y5_NO_SHADOW_2524_PIM_ZERO_AUDIT.csv", "PIM2524_2_fixed_chainmap_lemma", "fixed chainmap theorem"),
        ("SRC3965_14_2524_counter", SRC / "P8_Y5_NO_SHADOW_2524_PIM_ZERO_AUDIT.csv", "PIM2524_4_hodge_domain_counterroute", "Hodge/domain counterroute"),
        ("SRC3965_15_2524_bound", SRC / "P8_Y5_NO_SHADOW_2524_JPIM_BOUND_ROWS.csv", "JPIM2524_0_total", "JPiM total bound"),
        ("SRC3965_16_phcr_total", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_0_total", "PiM plus Htau residual law"),
        ("SRC3965_17_phcr_domain", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_4_C_domain", "domain/Hodge variation"),
        ("SRC3965_18_validation_3964", SRC / "P8_Y5_BRR545_3964_VALIDATION.csv", "VAL3964_18_no_pycache", "previous validation"),
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


def commutator_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PCT3965_0_obstruction_identity",
            "theorem_piece": "projected-current product rule",
            "formula": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "result": "Delta_PiM contains the chain-map commutator and cannot be erased by notation",
            "status": "EXACT_OBSTRUCTION_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCT3965_1_variation_identity",
            "theorem_piece": "projector variation product rule",
            "formula": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H",
            "result": "metric/domain/readout variation of Pi_M is a source-stress channel unless zero-owned",
            "status": "EXACT_VARIATION_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCT3965_2_zero_theorem",
            "theorem_piece": "fixed parent chain-map zero",
            "formula": "if Pi_M is parent-selected before readout, delta Pi_M=0, and d Pi_M=Pi_M d on C_H(A_ext), then [d,Pi_M]J_H=0",
            "result": "Delta_PiM commutator is zero only for a fixed parent chain-map projector",
            "status": "PROVED_CONDITIONAL_NOT_PARENT_PROMOTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCT3965_3_topological_route",
            "theorem_piece": "topological no-stress route",
            "formula": "Pi_M J=ell_M(J) omega_M_top, d omega_M_top=0, delta_g omega_M_top=0",
            "result": "topological Pi_M gives delta_g Pi_M=0 and no projector stress if parent-owned",
            "status": "TOPOLOGICAL_ZERO_ROUTE_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCT3965_4_counterroute",
            "theorem_piece": "metric/domain projector counterroute",
            "formula": "Pi_M=Pi_M[g,n_mu,G_B,chi_W,A_ext,S_link,R_A] => delta Pi_M and [d,Pi_M] need not vanish",
            "result": "Hodge/domain/readout PiM must be varied and retained as stress/residual",
            "status": "COUNTERMODEL_ACTIVE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def stress_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PSS3965_0_bulk_stress",
            "stress_piece": "bulk projector stress",
            "formula": "T_PiM^{mu nu}:=-(2/sqrt(-g)) delta_g[Pi_M J_H]/delta g_mu_nu",
            "zero_route": "delta_g Pi_M=0 for topological/metric-independent PiM",
            "if_nonzero": "feeds gamma,beta,xi,alpha_i and epsilon_Meff_flux",
            "status": "BOUND_BRANCH_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PSS3965_1_domain_variation",
            "stress_piece": "domain/worldtube/linking-surface variation",
            "formula": "D_domain Pi_M <= ||D_D Pi_M|| (||delta W_source||+||delta A_ext||+||delta S_link||)",
            "zero_route": "source worldtube and exterior annulus are parent-fixed before readout",
            "if_nonzero": "feeds frame/source support, R10 profile, and radial mass hair",
            "status": "BOUND_BRANCH_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PSS3965_2_boundary_projector",
            "stress_piece": "boundary/projector reference flux",
            "formula": "B_zero_flux := M_H_ref^-1 int_boundary dB_zero",
            "zero_route": "boundary exact term has zero compact flux with parent-fixed reference",
            "if_nonzero": "feeds boundary monopole and Delta_symp/Delta_cal",
            "status": "BOUND_BRANCH_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PSS3965_3_readout_guard",
            "stress_piece": "post-readout PiM mask",
            "formula": "delta S_parent must not contain P_read/fitted Pi_M choices",
            "zero_route": "PiM is defined before orbital/PPN/readout scoring",
            "if_nonzero": "fitted GM laundering; claim forbidden",
            "status": "POLICY_GUARD_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def delta_vector_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DPV3965_0_Icommutator", "I_commutator_abs", "M_H_ref^-1 |int_A [d,Pi_M]J_H|", "chain-map commutator", "zero if dPi_M=Pi_Md on parent source complex"),
        ("DPV3965_1_DPiM_var", "DPiM_JH", "||(delta Pi_M)J_H||", "projector variation source stress", "zero if PiM is parent-fixed/topological"),
        ("DPV3965_2_Ddomain", "Ddomain_PiM", "||D_D Pi_M||(|delta W|+|delta A|+|delta S|)", "domain/linking-surface variation", "zero if domain/worldtube fixed before readout"),
        ("DPV3965_3_projector_stress", "projector_stress_beta_equiv", "PPN-projected norm of delta_g Pi_M contribution", "metric-dependent projector stress", "zero if delta_g PiM=0 or stress theorem cancels"),
        ("DPV3965_4_Req", "R_eq_integral", "M_H_ref^-1 int_S(Pi_M J_H-J_M_top-dB_zero)", "same-object Hilbert/topological equality residual", "zero if same-object equality lands"),
        ("DPV3965_5_Bzero", "B_zero_flux", "M_H_ref^-1 int_boundary dB_zero", "boundary/reference flux leakage", "zero if exact term has no compact flux"),
        ("DPV3965_6_worldtube", "E_worldtube", "|delta W_source|+|delta support|+|linking surface drift|", "worldtube/support mismatch", "zero if source support fixed covariantly"),
        ("DPV3965_7_MHref", "E_MHref_guard", "I_not_sourced(M_H_ref,H_tau,H_ref,Q_tau,tau_source=tau_readout)", "same denominator/time generator guard", "zero if M_H_ref/tau are parent-owned same-frame"),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "score_term": score_term,
            "meaning": meaning,
            "zero_route": zero_route,
            "feeds": "Delta_PiM; epsilon_Meff_flux; PPN/source-normalization",
            "status": "RETAINED_SYMBOLIC_RESIDUAL",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, symbol, score_term, meaning, zero_route in rows
    ]


def meff_feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DPMF3965_0_DeltaPiM_bound",
            "target": "Delta_PiM",
            "update_formula": "Delta_PiM <= I_commutator_abs + DPiM_JH + Ddomain_PiM + projector_stress_beta_equiv + R_eq_integral + B_zero_flux + E_worldtube + E_MHref_guard",
            "meaning": "3964 Delta_PiM is now decomposed into projector commutator/stress/source-denominator components",
            "feeds": "epsilon_Meff_flux",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DPMF3965_1_Gauss_guard",
            "target": "Delta_cal / Gauss calibration",
            "update_formula": "if Delta_PiM=0 but Gauss/orbital calibration is unsigned, Delta_cal remains active",
            "meaning": "even a clean PiM source current does not by itself prove orbital inverse-square readout",
            "feeds": "next Gauss/orbital calibration gate",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3965_0_zero_route",
            "decision": "retain the fixed parent chain-map/topological PiM route as the clean zero theorem",
            "basis": "if PiM is parent-selected, metric-independent, domain-fixed, and a chain map, commutator and projector stress vanish",
            "effect": "Delta_PiM can be theorem-zero only under explicit parent-owned conditions",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3965_1_counterroute",
            "decision": "retain Hodge/domain/readout PiM as an active residual branch",
            "basis": "metric/domain-dependent projectors generate delta PiM, commutator, and stress terms",
            "effect": "no Newton/local-GR claim can use a fitted or readout-selected mass projector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3965_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "after Delta_PiM decomposition, the next source-denominator leak is Delta_cal: Gauss/orbital calibration",
            "effect": "test whether closed source mass becomes measured inverse-square orbital GM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3965_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3965_1_commutator", "PiM commutator theorem", "fixed parent chain-map PiM on same Hilbert-current complex", "CONDITIONAL_ONLY"),
        ("CLG3965_2_projector_stress", "projector stress", "topological/metric-independent PiM or stress bound", "BOUND_OR_CONDITIONAL"),
        ("CLG3965_3_delta_vector", "Delta_PiM vector", "all PiM failure components zero or score-ready", "PASS_SYMBOLIC_NONCLAIM"),
        ("CLG3965_4_Newton_claim", "Newton/local GR source denominator", "Delta_PiM=0 plus flux/Gauss/PPN gates", "BLOCKED_NONCLAIM"),
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
            "row_id": "NEXT3965_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or bound Delta_cal: show the closed Hilbert/PiM mass charge calibrates to the Gauss surface integral and slow-orbital inverse-square readout in the same observed frame, or retain calibration/radial/fifth-force residuals",
            "success_condition": "Delta_cal is theorem-zero under Gauss/orbital calibration, or becomes a finite residual feeding epsilon_Meff_flux and epsilon_Newton_source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_DELTAPIM_DECOMPOSITION",
            "summary": "3965 decomposes Delta_PiM into commutator, projector variation, domain, stress, same-object equality, boundary flux, worldtube, and MHref/tau guard terms; zero route is conditional on parent chain-map/topological PiM, while Hodge/domain/readout PiM remains bounded.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3965 - PiM Commutator Projector Stress Or Gauss Bound

Timestamp: `{timestamp}`

## Result

3965 decomposes the sharpest 3964 source-denominator leak:

`d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H`

and

`delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H`.

So `Pi_M` is safe only if it is a parent-selected chain-map projector before readout.

Clean zero route:

- `Pi_M` is parent-selected before readout;
- `delta Pi_M=0`;
- `d Pi_M=Pi_M d` on the Hilbert-current exterior complex;
- domain/worldtube/linking surfaces are fixed before readout;
- same-object Hilbert/topological equality and boundary reference flux close.

If not, the retained residual is:

`Delta_PiM <= I_commutator_abs + DPiM_JH + Ddomain_PiM + projector_stress_beta_equiv + R_eq_integral + B_zero_flux + E_worldtube + E_MHref_guard`.

## Meaning

This blocks a very common cheat: choosing `Pi_M` after the fact to match observed GM. The projector is either parent-owned, topological, and metric-independent, or it becomes a source-normalization residual.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- Commutator theorem: `source-intake\\mts_residuals\\P8_Y5_R2FR_3965_PIM_COMMUTATOR_ZERO_THEOREM_OR_BOUND.csv`
- Projector stress split: `source-intake\\mts_residuals\\P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv`
- DeltaPiM vector: `source-intake\\mts_residuals\\P8_Y5_R2FR_3965_DELTAPIM_RESIDUAL_VECTOR.csv`
- Meff feed update: `source-intake\\mts_residuals\\P8_Y5_R2FR_3965_MEFF_FLUX_DELTAPIM_FEED_UPDATE.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3965_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3965 - PiM Commutator And Projector-Stress Split

Timestamp: `{timestamp}`

- Decomposes `Delta_PiM` into commutator, variation, domain, projector-stress, equality, boundary, worldtube, and denominator/time-generator guard terms.
- Clean zero route is fixed parent chain-map/topological `Pi_M`.
- Hodge/domain/readout-selected `Pi_M` remains a bounded residual branch.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3965 - PiM Commutator And Projector-Stress Split"
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
    commutator = commutator_rows(timestamp)
    stress = stress_rows(timestamp)
    delta_vector = delta_vector_rows(timestamp)
    feed = meff_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    comm_statuses = {row["status"] for row in commutator}
    stress_statuses = {row["status"] for row in stress}
    vector_symbols = {row["symbol"] for row in delta_vector}
    feed_targets = {row["target"] for row in feed}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = commutator + stress + delta_vector + feed + decisions + claims + next_target

    checks = [
        ("VAL3965_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3965_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3965_02_commutator_identity", "EXACT_OBSTRUCTION_IDENTITY" in comm_statuses and "EXACT_VARIATION_IDENTITY" in comm_statuses, "PiM commutator and variation identities written"),
        ("VAL3965_03_zero_route", "PROVED_CONDITIONAL_NOT_PARENT_PROMOTED" in comm_statuses and "TOPOLOGICAL_ZERO_ROUTE_CONDITIONAL" in comm_statuses, "conditional PiM zero routes written"),
        ("VAL3965_04_counterroute", "COUNTERMODEL_ACTIVE_BOUND_REQUIRED" in comm_statuses, "Hodge/domain/readout counterroute retained"),
        ("VAL3965_05_stress_split", "BOUND_BRANCH_RETAINED" in stress_statuses and "POLICY_GUARD_NO_NUMERIC_CLAIM" in stress_statuses, "projector stress split and readout guard written"),
        ("VAL3965_06_delta_vector", {"I_commutator_abs", "DPiM_JH", "Ddomain_PiM", "projector_stress_beta_equiv", "R_eq_integral", "B_zero_flux", "E_worldtube", "E_MHref_guard"}.issubset(vector_symbols), "DeltaPiM residual vector complete"),
        ("VAL3965_07_feed", {"Delta_PiM", "Delta_cal / Gauss calibration"}.issubset(feed_targets), "Meff feed and next Gauss guard present"),
        ("VAL3965_08_decision", "fixed parent chain-map" in decision_text and "Hodge/domain/readout PiM" in decision_text, "decision records zero route and retained counterroute"),
        ("VAL3965_09_claim_gate", "CONDITIONAL_ONLY" in claim_statuses and "BOUND_OR_CONDITIONAL" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses, "claim gate blocks Newton/local-GR promotion"),
        ("VAL3965_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to Gauss/orbital calibration"),
        ("VAL3965_11_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3965_12_score_ready", all(row["score_ready"] for row in delta_vector), "DeltaPiM residual rows are score-ready symbolics"),
        ("VAL3965_13_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3965_14_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3965_15_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3965_16_spine_updated", SPINE_PATH.exists() and "3965 - PiM Commutator And Projector-Stress Split" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3965_17_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3965_18_script_compile", True, "script compiled before validation write"),
        ("VAL3965_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    commutator = commutator_rows(timestamp)
    stress = stress_rows(timestamp)
    delta_vector = delta_vector_rows(timestamp)
    feed = meff_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["commutator"], commutator)
    write_csv(OUTPUTS["stress"], stress)
    write_csv(OUTPUTS["delta_vector"], delta_vector)
    write_csv(OUTPUTS["meff_feed"], feed)
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
        raise SystemExit(f"3965 validation failed: {failed}")

    print(f"3965 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Delta_PiM commutator/projector-stress split assembled")


if __name__ == "__main__":
    run()
