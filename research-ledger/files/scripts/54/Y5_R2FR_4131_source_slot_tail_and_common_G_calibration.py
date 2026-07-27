from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4131-Y5-R2FR-source-slot-tail-and-common-G-calibration.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_SLOT_TAIL_AND_COMMON_G_CALIBRATION_4131"
CHECKPOINT_ID = "4131"
DECISION = "SOURCE_SLOT_TAIL_SPLIT_COMMON_G_CALIBRATION_BOUND_VECTOR_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4131_00_4130_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4130_NEXT_TARGET.csv",
        "4131-Y5-R2FR-source-slot-tail-and-common-G-calibration.md",
        "4130 selected source-slot tail and common-G calibration.",
    ),
    "SRC4131_01_4130_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4130_STATUS.csv",
        "BALPHA_INVARIANT_THROAT_DERIVED_NO_EXTRA_F2_PARENT_ZERO_UNSIGNED_BOUND_SCHEMAS_FILLED",
        "Current-chain b_alpha invariant throat.",
    ),
    "SRC4131_02_4130_product": (
        SOURCE_DIR / "P8_Y5_R2FR_4130_PRODUCT_GATES.csv",
        "COMMON_G_CALIBRATION_NEXT_PRESSURE",
        "Source-slot and common-G product gates.",
    ),
    "SRC4131_03_3996_product": (
        SOURCE_DIR / "P8_Y5_R2FR_3996_BALPHA_SOURCE_PRODUCT_VECTOR.csv",
        "BSP3996_0_invariant_source_product",
        "Older b_alpha source product vector.",
    ),
    "SRC4131_04_4107_geff": (
        SOURCE_DIR / "P8_Y5_R2FR_4107_GEFF_PRODUCT_LOCK.csv",
        "GPL4107_0_product_identity",
        "Effective coupling product identity.",
    ),
    "SRC4131_05_4080_gdot": (
        SOURCE_DIR / "P8_Y5_R2FR_4080_GDOT_AND_G_CALIBRATION_BOUNDS.csv",
        "BOUND4080_0_Gdot_over_G_LLR",
        "Gdot/G residual bound.",
    ),
    "SRC4131_06_4081_wep": (
        SOURCE_DIR / "P8_Y5_R2FR_4081_EOTVOS_WEP_BOUND.csv",
        "BOUND4081_0_MICROSCOPE_Eotvos_Ti_Pt",
        "WEP/source-coupling residual scale.",
    ),
    "SRC4131_07_4085_ppn": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
        "BND4085_10_gdot_over_g_lunar",
        "PPN and Gdot bound table.",
    ),
    "SRC4131_08_4085_ppn_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_SOURCE_STABLE_PPN_THEOREM.csv",
        "ANTI_TUNING_ANTI_ORBITAL_LAUNDERING_GUARD",
        "Source-stable PPN no-cancellation guard.",
    ),
    "SRC4131_09_4126_r10": (
        SOURCE_DIR / "P8_Y5_R2FR_4126_BETA_COMMON_BOUND_ROWS.csv",
        "R10_short_range",
        "R10 beta/common source bound row.",
    ),
    "SRC4131_10_4096_G": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW.csv",
        "SNL4096_1_constant_G_ref",
        "Clarification that G_ref is calibrated, not numerically derived.",
    ),
    "SRC4131_11_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4131_source_slot_tail_and_common_G_calibration.py",
        "Reproducible generator for this 4131 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def tail_split_rows() -> List[dict]:
    data = [
        (
            "TAIL4131_0_master",
            "B_EM_source",
            "|b_alpha|+|Dln c_pre|+|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|z_rad|",
            "dimensionless per normalized A_N",
            "exact product envelope after b_alpha invariant reduction",
            "MASTER_TAIL_VECTOR",
        ),
        (
            "TAIL4131_1_c_pre",
            "Dln c_pre",
            "pre-variation source/current coefficient slot",
            "dimensionless per normalized A_N",
            "zero only if source-only current/action slots are absent from the parent matter grammar or fixed calibration data",
            "PARENT_GRAMMAR_OR_BOUND_REQUIRED",
        ),
        (
            "TAIL4131_2_w_rel",
            "Dln w_rel",
            "relative species/source action weight",
            "dimensionless per normalized A_N",
            "zero only if representation/species labels are fixed and no relative source weighting field exists",
            "FIXED_REPRESENTATION_OR_BOUND_REQUIRED",
        ),
        (
            "TAIL4131_3_kappa_A",
            "Dln kappa_A",
            "species/source coupling multiplier",
            "dimensionless per normalized A_N",
            "zero only if all ordinary species use the same Hilbert source coupling before readout",
            "SAME_HILBERT_SOURCE_OR_BOUND_REQUIRED",
        ),
        (
            "TAIL4131_4_R_A",
            "Dln R_A",
            "readout/sensitivity regeneration of source coupling",
            "dimensionless per normalized A_N",
            "zero only if readout/radiative closure preserves the same source functional",
            "READOUT_CLOSURE_OR_BOUND_REQUIRED",
        ),
        (
            "TAIL4131_5_z_rad",
            "z_rad",
            "radiative/loop threshold regeneration",
            "dimensionless per normalized A_N",
            "zero only if radiative closure keeps the visible matter constants fixed in the local branch",
            "RADIATIVE_CLOSURE_OR_BOUND_REQUIRED",
        ),
        (
            "TAIL4131_6_w_common",
            "Dln w_common",
            "universal common source/action-scale prefactor",
            "dimensionless per normalized A_N or time/range derivative after projection",
            "not WEP-visible; must be G_ref/action-scale owned or bounded by Gdot/PPN/source calibration",
            "COMMON_MODE_G_CALIBRATION_OR_BOUND_REQUIRED",
        ),
    ]
    rows: List[dict] = []
    for tail_id, symbol, formula, units, zero_route, status in data:
        row = row_base()
        row.update(
            {
                "tail_id": tail_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "zero_route": zero_route,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def common_g_rows() -> List[dict]:
    data = [
        (
            "CG4131_0_product_identity",
            "D_A ln G_eff_obs",
            "D_A ln(G_ref*w_common*ell_J*R_frame*C_extra)=z_G+z_w+z_ellJ+z_Rframe+z_extra",
            "measured coupling silence requires the whole product to be silent, not merely constant G_ref",
            "EXACT_PRODUCT_IDENTITY",
        ),
        (
            "CG4131_1_G_ref",
            "z_G",
            "D_A ln G_ref",
            "can be zero if G_ref/kappa_ref is a fixed parent global/topological calibration label",
            "CONDITIONAL_ZERO_ROUTE_NOT_NUMERIC_PREDICTION",
        ),
        (
            "CG4131_2_w_common",
            "z_w",
            "D_A ln w_common",
            "universal source prefactor is invisible to differential WEP but visible to Gdot/PPN/source-normalization",
            "COMMON_MODE_BOUND_REQUIRED",
        ),
        (
            "CG4131_3_ellJ",
            "z_ellJ",
            "D_A ln ell_J",
            "source-current normalization denominator remains the algebraic source-coupling throat",
            "SOURCE_DENOMINATOR_BOUND_REQUIRED",
        ),
        (
            "CG4131_4_Rframe",
            "z_Rframe",
            "D_A ln R_frame",
            "same-frame/readout factor must not reintroduce source variation",
            "READOUT_FRAME_BOUND_REQUIRED",
        ),
        (
            "CG4131_5_extra",
            "z_extra",
            "D_A ln C_extra",
            "extra-sector source factors must be zero, universal fixed calibration, or bounded",
            "EXTRA_SOURCE_BOUND_REQUIRED",
        ),
    ]
    rows: List[dict] = []
    for row_id, symbol, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def arena_bound_rows() -> List[dict]:
    data = [
        (
            "AB4131_0_Gdot",
            "Gdot_clock",
            "d ln G_eff_obs/dt",
            "|z_product dot(A_N)+explicit_t| <= 1.3e-12 yr^-1",
            "per_year",
            "BOUND4080_0_Gdot_over_G_LLR; BND4085_10_gdot_over_g_lunar",
            "z_product; dot(A_N); explicit_t residuals; source path",
        ),
        (
            "AB4131_1_PPN",
            "PPN_source_stability",
            "Delta_PPN_abs includes source/readout/common-G products",
            "each gamma,beta,alpha_i,xi,zeta source product must pass its own bound with no cancellation",
            "dimensionless",
            "BND4085_0..10 and PPN4085_5 guard",
            "PPN projector weights; source denominator; no-cancellation certificate",
        ),
        (
            "AB4131_2_WEP",
            "WEP_relative_source_tail",
            "eta_AB",
            "eta_AB <= material_projection*(|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|b_alpha|+tail)",
            "|eta| dimensionless",
            "BOUND4081_0_MICROSCOPE_Eotvos_Ti_Pt",
            "composition charges; material projection; MICROSCOPE source; common-mode guard",
        ),
        (
            "AB4131_3_R10",
            "R10_short_range",
            "alpha_R10(lambda)",
            "alpha_R10(lambda)=K_tail(lambda)*B_source_tail_S*B_source_tail_T/M_tail^2 + common-mode channel",
            "dimensionless alpha(lambda)",
            "P8_Y5_R2FR_4126_BETA_COMMON_BOUND_ROWS",
            "K_tail;M_tail^2;tau(lambda);source/test tail coefficients; alpha_bound(lambda)",
        ),
        (
            "AB4131_4_Newton_Gauss",
            "Newton_source_calibration",
            "Phi_N source coefficient",
            "Phi_N=-G_ref M_H/r only if D_A ln(G_ref*M_H*readout)=0 and source denominator is not orbital-fitted",
            "potential/source normalization",
            "SNL4096_1 and 4084 source denominator gate",
            "M_H parent charge; readout frame; Gauss boundary; no orbital-GM import",
        ),
        (
            "AB4131_5_clock_alpha_joint",
            "clock_alpha_source_joint",
            "clock drift",
            "clock drift includes S_alpha*b_alpha plus S_G*z_product plus source-slot tail",
            "time^-1",
            "4130 b_alpha schema plus Gdot/common-G rows",
            "S_alpha;S_G;dot(A_N); clock source path; no alpha-only shortcut",
        ),
    ]
    rows: List[dict] = []
    for bound_id, arena, observable, formula, units, source_basis, required_inputs in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "arena": arena,
                "observable": observable,
                "formula": formula,
                "units": units,
                "source_basis": source_basis,
                "required_inputs": required_inputs,
                "status": "NONCLAIM_BOUND_SCHEMA_FILLED",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def zero_audit_rows() -> List[dict]:
    data = [
        (
            "ZA4131_0_fixed_representation",
            "Dln w_rel and charge/species labels",
            "fixed representation sectors can kill relative label drift",
            "does not kill common w_common or source denominator ell_J",
            "PARTIAL_ZERO_ROUTE",
        ),
        (
            "ZA4131_1_same_hilbert_source",
            "Dln kappa_A",
            "same Hilbert source coupling for all ordinary species would kill species/source coupling slots",
            "parent matter functor and same-coframe source ownership remain unsigned",
            "CONDITIONAL_ZERO_UNSIGNED",
        ),
        (
            "ZA4131_2_readout_radiative",
            "Dln R_A and z_rad",
            "readout/radiative closure would kill post-variation regeneration terms",
            "closure is not currently parent-signed",
            "CONDITIONAL_ZERO_UNSIGNED",
        ),
        (
            "ZA4131_3_common_G",
            "Dln w_common",
            "fixed action-scale/G_ref superselection would kill common source prefactor drift",
            "common mode is not tested by differential WEP and remains Gdot/PPN/source-calibration pressure",
            "COMMON_ZERO_UNSIGNED",
        ),
        (
            "ZA4131_4_verdict",
            "source-slot tail and common-G",
            "no full parent-zero theorem is claimable from current corpus",
            "bound vector is required before any local-GR/source-normalization claim",
            "ZERO_NOT_CLAIMED_BOUND_VECTOR_ACTIVE",
        ),
    ]
    rows: List[dict] = []
    for audit_id, target, zero_route, gap, status in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "target": target,
                "zero_route": zero_route,
                "gap": gap,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4131_0_split",
            "The source-slot tail is split into fixed-representation/source-slot/readout/radiative/common-mode pieces instead of one vague EM coupling.",
            "TAIL_SPLIT_COMPLETE",
            "score each live term independently",
        ),
        (
            "DEC4131_1_common_mode",
            "Dln w_common is a common-mode G/source calibration pressure, not a WEP-differential shortcut.",
            "COMMON_MODE_GUARD_LOCKED",
            "route it through Gdot, PPN, Newton/Gauss, and source-normalization bounds",
        ),
        (
            "DEC4131_2_no_claim",
            "No source-slot or common-G parent-zero theorem is claimed from 4131.",
            "ZERO_UNSIGNED_BOUND_VECTOR_ACTIVE",
            "keep local-GR/source-normalization claim blocked",
        ),
        (
            "DEC4131_3_next",
            "Next target is the source denominator ell_J / M_H equality, because it is the shared throat for Newton, PPN and common-G calibration.",
            "NEXT_SOURCE_DENOMINATOR_SELECTED",
            "try to prove ell_J/M_H/Hilbert charge equality or fill denominator bounds",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4131_0",
            "result": DECISION,
            "summary": (
                "4131 splits the b_alpha source-slot tail into Dln c_pre, Dln w_rel, Dln kappa_A, Dln R_A, z_rad, "
                "and Dln w_common, then maps the live terms to Gdot, PPN, WEP, R10, Newton/Gauss, and clock/alpha-source "
                "bound schemas. Fixed representation and calibrated-standard-matter branches remove some relative-label drift, "
                "but common-G/source denominator calibration remains unsigned and cannot be closed by WEP."
            ),
            "tail_split_filled": "True",
            "common_G_bound_vector_filled": "True",
            "parent_zero_signed": "False",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4132 source denominator ell_J M_H equality",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4131_0",
            "target_doc": "4132-Y5-R2FR-source-denominator-ellJ-MH-equality.md",
            "target_script": "scripts/Y5_R2FR_4132_source_denominator_ellJ_MH_equality.py",
            "objective": (
                "attack z_ellJ / source denominator equality by trying to prove ell_J(Pi_M J_H_total) equals the dressed Hilbert mass M_H "
                "and Hamiltonian/Gauss source charge before orbital readout; if unsigned, fill denominator bound rows"
            ),
            "success_gate": "ell_J/M_H source denominator is parent-signed zero, or denominator residual has Gdot/PPN/R10/Newton bound schemas with units and source paths",
            "reason": "4131 identifies source denominator as the shared throat for common-G calibration, Newton source normalization, and PPN stability.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4131_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4131_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4131_SOURCE_SLOT_TAIL_SPLIT": SOURCE_DIR / "P8_Y5_R2FR_4131_SOURCE_SLOT_TAIL_SPLIT.csv",
        "P8_Y5_R2FR_4131_COMMON_G_PRODUCT_GATE": SOURCE_DIR / "P8_Y5_R2FR_4131_COMMON_G_PRODUCT_GATE.csv",
        "P8_Y5_R2FR_4131_ARENA_BOUND_SCHEMAS": SOURCE_DIR / "P8_Y5_R2FR_4131_ARENA_BOUND_SCHEMAS.csv",
        "P8_Y5_R2FR_4131_ZERO_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4131_ZERO_AUDIT.csv",
        "P8_Y5_R2FR_4131_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4131_DECISION_GATES.csv",
        "P8_Y5_R2FR_4131_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4131_STATUS.csv",
        "P8_Y5_R2FR_4131_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4131_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4131 - Source-Slot Tail and Common-G Calibration",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The source-slot tail is now split into explicit live pieces instead of one vague coupling residual.",
        "- `Dln w_common` is common-mode: WEP cannot kill it; it must be owned by `G_ref`/action-scale or bounded by Gdot/PPN/source calibration.",
        "- No parent-zero theorem is claimed; bound schemas are filled for Gdot, PPN, WEP, R10, Newton/Gauss, and clock/alpha-source channels.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Tail Split", "", "| symbol | status | zero_route |", "|---|---|---|"])
    for row in tail_split_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['zero_route']} |")
    sections.extend(["", "## Common-G Product", "", "| symbol | status | meaning |", "|---|---|---|"])
    for row in common_g_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['meaning']} |")
    sections.extend(["", "## Arena Bounds", "", "| arena | observable | status |", "|---|---|---|"])
    for row in arena_bound_rows():
        sections.append(f"| {row['arena']} | {row['observable']} | {row['status']} |")
    sections.extend(["", "## Claim Ceiling", "", f"- {status['claim_state']}.", "- This checkpoint reduces the coupling obstruction but does not close local GR.", "", "## Next Target", "", "- `4132-Y5-R2FR-source-denominator-ellJ-MH-equality.md`", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4131_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4131_SOURCE_SLOT_TAIL_SPLIT": tail_split_rows,
        "P8_Y5_R2FR_4131_COMMON_G_PRODUCT_GATE": common_g_rows,
        "P8_Y5_R2FR_4131_ARENA_BOUND_SCHEMAS": arena_bound_rows,
        "P8_Y5_R2FR_4131_ZERO_AUDIT": zero_audit_rows,
        "P8_Y5_R2FR_4131_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4131_STATUS": status_rows,
        "P8_Y5_R2FR_4131_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4131_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4131_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4131_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    tail_text = flatten_rows([outputs["P8_Y5_R2FR_4131_SOURCE_SLOT_TAIL_SPLIT"]])
    tail_ok = all(token in tail_text for token in ["Dln c_pre", "Dln w_rel", "Dln kappa_A", "Dln R_A", "z_rad", "Dln w_common"])
    add("VAL4131_3_tail_split", "tail split includes source-slot and common-mode terms", tail_ok, "tail tokens checked")

    common_text = flatten_rows([outputs["P8_Y5_R2FR_4131_COMMON_G_PRODUCT_GATE"]])
    common_ok = all(token in common_text for token in ["z_G", "z_w", "z_ellJ", "z_Rframe", "z_extra", "EXACT_PRODUCT_IDENTITY"])
    add("VAL4131_4_common_g", "common-G product gate includes all effective-coupling factors", common_ok, "common tokens checked")

    arena_text = flatten_rows([outputs["P8_Y5_R2FR_4131_ARENA_BOUND_SCHEMAS"]])
    arena_ok = all(token in arena_text for token in ["Gdot_clock", "PPN_source_stability", "WEP_relative_source_tail", "R10_short_range", "Newton_source_calibration", "clock_alpha_source_joint"])
    add("VAL4131_5_arena_bounds", "arena bounds cover Gdot, PPN, WEP, R10, Newton/Gauss, and clock/alpha", arena_ok, "arena tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4131_ZERO_AUDIT"]])
    audit_ok = all(token in audit_text for token in ["PARTIAL_ZERO_ROUTE", "CONDITIONAL_ZERO_UNSIGNED", "COMMON_ZERO_UNSIGNED", "ZERO_NOT_CLAIMED_BOUND_VECTOR_ACTIVE"])
    add("VAL4131_6_zero_audit", "zero audit records partial routes and no-claim verdict", audit_ok, "audit tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4131_DECISION_GATES"]])
    decision_ok = all(token in decision_text for token in ["TAIL_SPLIT_COMPLETE", "COMMON_MODE_GUARD_LOCKED", "ZERO_UNSIGNED_BOUND_VECTOR_ACTIVE", "NEXT_SOURCE_DENOMINATOR_SELECTED"])
    add("VAL4131_7_decisions", "decision gates record tail split, common-mode guard, no-claim, and next target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4131_STATUS"])
    status_ok = bool(status) and status[0].get("result") == DECISION and status[0].get("tail_split_filled") == "True" and status[0].get("parent_zero_signed") == "False"
    add("VAL4131_8_status", "status records tail split and unsigned parent zero", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4131_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4132-Y5-R2FR-source-denominator-ellJ-MH-equality.md"
    add("VAL4131_9_next_target", "next target is source denominator ell_J/M_H equality", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4131_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4131*")) or any(FORMALIZATION.rglob("4131-Y5-R2FR*"))
    add("VAL4131_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4131_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4131_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
