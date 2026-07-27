from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4107-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_CONSTANT_GEFF_GATE_4107"
CHECKPOINT_ID = "4107"
DECISION = (
    "MEASURED_GM_DERIVATIVE_IDENTITY_AND_GEFF_PRODUCT_LOCK_IMPORTED_"
    "ELLJ_SOURCE_CURRENT_NORMALIZATION_GATE_NEXT"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4107_00_4106_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4106_NEXT_TARGET.csv",
        "4107-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md",
        "4106 selects constant G_eff/radial-time hair as the current gate.",
    ),
    "SRC4107_01_3599_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3599_CONSTANT_GEFF_RADIAL_TIME_NOHAIR_THEOREM.csv",
        "NH3599_1_master_identity",
        "3599 derives the measured-GM derivative identity.",
    ),
    "SRC4107_02_3599_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3599_DERIVATIVE_HAIR_RESIDUALS.csv",
        "DHR3599_8_partial_r_mu_obs",
        "3599 lists derivative-hair residual channels.",
    ),
    "SRC4107_03_3599_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3599_DERIVATIVE_HAIR_BOUND_ROWS.csv",
        "DHB3599_11_derivative_hair_total",
        "3599 gives source-ready derivative-hair bound rows.",
    ),
    "SRC4107_04_3599_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3599_STATUS.csv",
        "CONSTANT_GEFF_RADIAL_TIME_HAIR_IDENTITY_DERIVED_BOUNDS_ACTIVE",
        "3599 status keeps derivative hair active and selects product lock.",
    ),
    "SRC4107_05_3600_product_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3600_GEFF_PRODUCT_LOCK_THEOREM.csv",
        "GPL3600_1_product_identity",
        "3600 derives the effective coupling product identity.",
    ),
    "SRC4107_06_3600_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3600_GEFF_PRODUCT_RESIDUALS.csv",
        "GPR3600_",
        "3600 decomposes product-lock residuals.",
    ),
    "SRC4107_07_3600_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv",
        "GPB3600_",
        "3600 gives source-ready product factor bound rows.",
    ),
    "SRC4107_08_3600_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3600_STATUS.csv",
        "GEFF_PRODUCT_LOCK_IDENTITY_DERIVED_PRODUCT_BOUNDS_ACTIVE",
        "3600 status identifies ell_J as the next largest denominator.",
    ),
    "SRC4107_09_3600_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3600_NEXT_TARGET.csv",
        "3601-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md",
        "3600 selects ell_J source-current normalization as next target.",
    ),
    "SRC4107_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4107_constant_Geff_radial_time_hair_zero_or_bound.py",
        "Reproducible generator for this 4107 checkpoint.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def row_base() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def source_register_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "source_id": source_id,
            "source_type": "local_checkpoint_or_generator",
            "path_or_url": str(path),
            "needle": needle,
            "role": role,
            "exists": bool_string(path.exists()),
            "contains_needle": bool_string(path.exists() and needle in read_text(path)),
            "valid_for_claim": "False",
        }
        for source_id, (path, needle, role) in LOCAL_SOURCES.items()
    ]


def derivative_identity_rows() -> List[dict]:
    entries = [
        (
            "DID4107_0_master_identity",
            "measured GM identity",
            "mu_obs = G_eff*M_eff*(1+epsilon_mu); D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)",
            "every drift/profile in measured GM must be assigned to coupling, source flux, or extra-monopole residual",
            "EXACT_IDENTITY_IMPORTED",
            "SRC4107_01_3599_theorem",
        ),
        (
            "DID4107_1_time_hair",
            "time derivative hair",
            "d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + partial_t epsilon_mu/(1+epsilon_mu)",
            "local Gdot cannot be hidden in fitted GM",
            "BOUND_BRANCH_ACTIVE",
            "SRC4107_01_3599_theorem",
        ),
        (
            "DID4107_2_radial_hair",
            "radial profile hair",
            "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r epsilon_mu/(1+epsilon_mu)",
            "radial source/coupling profile cannot be treated as constant Newtonian mass",
            "BOUND_BRANCH_ACTIVE",
            "SRC4107_01_3599_theorem",
        ),
        (
            "DID4107_3_no_cancellation",
            "anti-tuning rule",
            "D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)=0 counts only if parent action gives the identity",
            "fitted radius-by-radius or epoch-by-epoch cancellation is not evidence",
            "PASS_GUARD",
            "SRC4107_01_3599_theorem",
        ),
        (
            "DID4107_4_current_verdict",
            "constant measured GM",
            "constant Newtonian GM follows only if coupling, projected source flux and epsilon_mu channels are parent-silent or independently bounded",
            "constant GM is a theorem target with active residual channels, not an assumed fit constant",
            "NO_CLAIM_BOUNDS_ACTIVE",
            "SRC4107_04_3599_status",
        ),
    ]
    return [
        {
            **row_base(),
            "identity_id": identity_id,
            "piece": piece,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for identity_id, piece, formula, meaning, status, source_key in entries
    ]


def derivative_hair_bound_rows() -> List[dict]:
    entries = [
        ("DHB4107_0_dln_Geff_dt", "dln_Geff_dt", "d ln G_eff/dt", "BOUND_REQUIRED_CRITICAL", "SRC4107_03_3599_bounds"),
        ("DHB4107_1_dln_Meff_dt", "dln_Meff_dt", "d ln M_eff/dt", "BOUND_REQUIRED_CRITICAL", "SRC4107_03_3599_bounds"),
        ("DHB4107_2_partial_t_epsilon_mu", "partial_t_epsilon_mu", "partial_t epsilon_mu/(1+epsilon_mu)", "BOUND_REQUIRED_CRITICAL", "SRC4107_03_3599_bounds"),
        ("DHB4107_3_partial_r_ln_mu_obs", "partial_r_ln_mu_obs", "partial_r ln mu_obs", "BOUND_REQUIRED_CRITICAL", "SRC4107_03_3599_bounds"),
        ("DHB4107_4_partial_r_ln_Geff", "partial_r_ln_Geff", "partial_r ln G_eff", "BOUND_REQUIRED", "SRC4107_03_3599_bounds"),
        ("DHB4107_5_partial_r_ln_Meff", "partial_r_ln_Meff", "partial_r ln M_eff", "BOUND_REQUIRED", "SRC4107_03_3599_bounds"),
        ("DHB4107_6_partial_r_epsilon_mu", "partial_r_epsilon_mu", "partial_r epsilon_mu/(1+epsilon_mu)", "BOUND_REQUIRED", "SRC4107_03_3599_bounds"),
        ("DHB4107_7_no_cancellation_identity", "C_cancel_identity", "parent identity for derivative cancellation, not fit cancellation", "GUARD_REQUIRED", "SRC4107_03_3599_bounds"),
        ("DHB4107_8_total", "epsilon_derivative_hair_total", "norm of all active time/radial/product/range/frame/species derivative-hair rows", "TOTAL_BOUND_BRANCH_ACTIVE", "SRC4107_03_3599_bounds"),
    ]
    return [
        {
            **row_base(),
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, symbol, definition, status, source_key in entries
    ]


def geff_product_lock_rows() -> List[dict]:
    entries = [
        (
            "GPL4107_0_product_identity",
            "effective coupling product",
            "D_X ln(G_ref*w_common*ell_J*R_frame*C_extra) = z_G + z_w + z_ellJ + z_Rframe + z_extra",
            "constant kappa alone is insufficient; the measured coupling product must be silent",
            "EXACT_PRODUCT_IDENTITY_IMPORTED",
            "SRC4107_05_3600_product_theorem",
        ),
        (
            "GPL4107_1_zG",
            "z_G",
            "D_X ln G_ref",
            "can be conditionally zero if kappa/G_ref is a parent global or topological superselection label",
            "CONDITIONAL_ZERO_ROUTE",
            "SRC4107_05_3600_product_theorem",
        ),
        (
            "GPL4107_2_zw",
            "z_w",
            "D_X ln w_common",
            "action-line/common scale drift must be parent-silent before readout",
            "BOUND_REQUIRED",
            "SRC4107_07_3600_bounds",
        ),
        (
            "GPL4107_3_zellJ",
            "z_ellJ",
            "D_X ln ell_J",
            "source-current normalization denominator is the largest remaining algebraic coupling gate",
            "NEXT_TARGET_SELECTED",
            "SRC4107_08_3600_status",
        ),
        (
            "GPL4107_4_zRframe",
            "z_Rframe",
            "D_X ln R_frame",
            "same-frame/readout factor must not sneak coupling variation back in",
            "BOUND_REQUIRED",
            "SRC4107_07_3600_bounds",
        ),
        (
            "GPL4107_5_zextra",
            "z_extra",
            "D_X ln C_extra",
            "extra-sector source factors must be zero, universal, or bounded",
            "BOUND_REQUIRED",
            "SRC4107_07_3600_bounds",
        ),
    ]
    return [
        {
            **row_base(),
            "product_id": product_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for product_id, symbol, formula, meaning, status, source_key in entries
    ]


def promotion_gate_rows() -> List[dict]:
    entries = [
        ("PROM4107_0_master_identity", "measured-GM derivative identity", "PASS_EXACT_IDENTITY", "mu_obs derivative split is exact"),
        ("PROM4107_1_constant_Geff", "constant G_eff claim", "FAIL_CURRENT_CLAIM", "product lock is conditional, not parent-signed"),
        ("PROM4107_2_time_hair", "time derivative hair", "FAIL_CURRENT_CLAIM", "dln_Geff_dt/dln_Meff_dt/partial_t epsilon_mu remain active"),
        ("PROM4107_3_radial_hair", "radial profile hair", "FAIL_CURRENT_CLAIM", "partial_r ln mu_obs remains active"),
        ("PROM4107_4_product_lock", "full effective coupling product", "PASS_CONDITIONAL_THEOREM", "D_X ln product identity is imported, but factors remain open"),
        ("PROM4107_5_no_fit_cancellation", "no fitted cancellation", "PASS_GUARD", "cancellation requires parent identity"),
        ("PROM4107_6_Newton_GR", "Newton/local-GR promotion", "FAIL_CURRENT_CLAIM", "ell_J and PPN stability remain downstream"),
    ]
    return [
        {
            **row_base(),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status, detail in entries
    ]


def decision_rows() -> List[dict]:
    entries = [
        (
            "DEC4107_0_identity",
            "adopt measured-GM derivative identity as canonical",
            "it forces all local GM drift/profile into G_eff, M_eff or epsilon_mu channels",
            "derivative hair can no longer be hidden in fitted GM",
            "DERIVATIVE_IDENTITY_CANONICAL",
            "SRC4107_01_3599_theorem",
        ),
        (
            "DEC4107_1_product_lock",
            "adopt effective coupling product lock",
            "constant kappa alone is not enough; G_ref*w_common*ell_J*R_frame*C_extra must be silent",
            "constant measured coupling remains conditional",
            "PRODUCT_LOCK_CANONICAL",
            "SRC4107_05_3600_product_theorem",
        ),
        (
            "DEC4107_2_next",
            "attack ell_J source-current normalization next",
            "3600 identifies z_ellJ as the largest remaining algebraic denominator in the coupling product",
            "4108 targets ell_J zero or source-ready component bounds",
            "NEXT_TARGET_SELECTED",
            "SRC4107_09_3600_next",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, consequence, status, source_key in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4107_0",
            "target_doc": "4108-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_4108_ellJ_source_current_normalization_zero_or_bound.py",
            "objective": "prove z_ellJ=D_X ln ell_J=0 by closing matter descent, Ward projection, Pi_M/H_tau, reference, support, frame and unit factors, or retain z_ellJ component bound rows",
            "success_gate": "the effective coupling product can advance only if the source-current normalization denominator is parent-owned before readout, not calibrated from observed GM",
            "reason": "4107 imports the product lock and identifies ell_J as the sharpest remaining denominator in constant measured coupling",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4107_0",
            "decision": DECISION,
            "strongest_result": "4107 imports the exact measured-GM derivative identity and the effective-coupling product lock. Constant Newtonian GM now has a precise condition: D_X ln G_eff, D_X ln M_eff and D_X ln(1+epsilon_mu) must vanish or be independently bounded, and G_eff itself means the full product G_ref*w_common*ell_J*R_frame*C_extra, not just a declared kappa.",
            "what_moved_forward": "the next coupling problem is reduced from 'derive G' to the concrete source-current normalization denominator ell_J and its Ward/PiM/H_tau/unit owners",
            "still_missing": "z_ellJ source-current normalization owner; w_common action-line silence; same-frame R_frame silence; extra-sector product silence; Pi_M flux conservation; mu_extra zero/universal theorem; radial/time derivative bounds; PPN source stability",
            "public_status": "no constant_Geff_Newton_local_GR_PPN claim",
            "next_target": "4108 ellJ source-current normalization zero or bound",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4107_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4107_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4107_DERIVATIVE_IDENTITY": SOURCE_DIR / "P8_Y5_R2FR_4107_DERIVATIVE_IDENTITY.csv",
        "P8_Y5_R2FR_4107_DERIVATIVE_HAIR_BOUNDS": SOURCE_DIR / "P8_Y5_R2FR_4107_DERIVATIVE_HAIR_BOUNDS.csv",
        "P8_Y5_R2FR_4107_GEFF_PRODUCT_LOCK": SOURCE_DIR / "P8_Y5_R2FR_4107_GEFF_PRODUCT_LOCK.csv",
        "P8_Y5_R2FR_4107_PROMOTION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4107_PROMOTION_GATES.csv",
        "P8_Y5_R2FR_4107_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4107_DECISION_GATE.csv",
        "P8_Y5_R2FR_4107_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4107_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4107_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4107_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4107 - Constant G_eff radial/time hair zero or bound",
        "",
        "## Verdict",
        "4107 moves the Newton-coupling route one notch tighter. Constant measured `GM` is now governed by an exact identity, not taste:",
        "",
        "`mu_obs = G_eff M_eff (1+epsilon_mu)` and `D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)`.",
        "",
        "Then 3600 sharpens `G_eff`: it is not one magic constant. It is the product `G_ref*w_common*ell_J*R_frame*C_extra`. Constant `kappa` alone does not close the gate.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Concrete Advances",
        "- Time drift and radial profile hair are exact residual channels, not fitted away.",
        "- Fitted cancellation is rejected unless the parent action supplies an identity.",
        "- The measured coupling product is split into `z_G`, `z_w`, `z_ellJ`, `z_Rframe`, and `z_extra`.",
        "- `z_ellJ = D_X ln ell_J` is now the sharpest next denominator to attack.",
        "",
        "## Still Not Claimed",
        "- Constant universal `G_eff`.",
        "- Constant Newtonian `GM`.",
        "- Local GR/PPN source stability.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4107_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4107_DERIVATIVE_IDENTITY.csv`",
        "- `P8_Y5_R2FR_4107_DERIVATIVE_HAIR_BOUNDS.csv`",
        "- `P8_Y5_R2FR_4107_GEFF_PRODUCT_LOCK.csv`",
        "- `P8_Y5_R2FR_4107_PROMOTION_GATES.csv`",
        "- `P8_Y5_R2FR_4107_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4107_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4107_STATUS.csv`",
        "- `P8_Y5_BRR545_4107_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4108-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md`",
        "- Objective: prove `z_ellJ=D_X ln ell_J=0` through matter descent/Ward/PiM/H_tau/unit ownership, or retain source-ready `z_ellJ` bound rows.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4107_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4107_DERIVATIVE_IDENTITY"], derivative_identity_rows())
    write_csv(outputs["P8_Y5_R2FR_4107_DERIVATIVE_HAIR_BOUNDS"], derivative_hair_bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4107_GEFF_PRODUCT_LOCK"], geff_product_lock_rows())
    write_csv(outputs["P8_Y5_R2FR_4107_PROMOTION_GATES"], promotion_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4107_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4107_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4107_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **row_base(),
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "valid_for_claim": "False",
            }
        )

    source_rows = source_register_rows()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "True"]
    missing_needles = [row["source_id"] for row in source_rows if row["contains_needle"] != "True"]
    add("VAL4107_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4107_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_counts = {}
    parse_ok = True
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[name] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_counts[name] = f"ERROR:{exc}"
            parse_ok = False
    add("VAL4107_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    identity_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4107_DERIVATIVE_IDENTITY"]))
    identity_tokens = ["mu_obs", "G_eff", "M_eff", "epsilon_mu", "no_cancellation"]
    missing_identity = [token for token in identity_tokens if token not in identity_text]
    add("VAL4107_3_identity", "derivative identity contains measured GM split and cancellation guard", not missing_identity, ";".join(missing_identity) or "identity tokens present")

    bounds_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4107_DERIVATIVE_HAIR_BOUNDS"]))
    bounds_tokens = ["dln_Geff_dt", "dln_Meff_dt", "partial_t_epsilon_mu", "partial_r_ln_mu_obs", "epsilon_derivative_hair_total"]
    missing_bounds = [token for token in bounds_tokens if token not in bounds_text]
    add("VAL4107_4_derivative_bounds", "core derivative hair bounds are present", not missing_bounds, ";".join(missing_bounds) or "bound tokens present")

    product_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4107_GEFF_PRODUCT_LOCK"]))
    product_tokens = ["G_ref*w_common*ell_J*R_frame*C_extra", "z_G", "z_w", "z_ellJ", "z_Rframe", "z_extra"]
    missing_product = [token for token in product_tokens if token not in product_text]
    add("VAL4107_5_product_lock", "G_eff product lock includes all product factors", not missing_product, ";".join(missing_product) or "product tokens present")

    gates = parse_csv(outputs["P8_Y5_R2FR_4107_PROMOTION_GATES"])
    claim_guard = all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in gates)
    claims_blocked = any(row.get("status") == "FAIL_CURRENT_CLAIM" and "constant G_eff" in row.get("gate", "") for row in gates)
    add("VAL4107_6_promotion_gates", "promotion gates keep constant Geff/Newton claims blocked", claim_guard and claims_blocked, f"claim_guard={claim_guard}; constant_blocked={claims_blocked}")

    decisions = parse_csv(outputs["P8_Y5_R2FR_4107_DECISION_GATE"])
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" and "ell_J" in row.get("decision", "") for row in decisions)
    add("VAL4107_7_next_decision", "decision gate selects ell_J source-current normalization", next_decision, str(decisions))

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4107_NEXT_TARGET"])
    next_ok = any("4108-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4107_8_next_target", "next target is ellJ normalization zero or bound", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4107_STATUS"])
    status_text = " ".join(" ".join(row.values()) for row in status_rows_local)
    status_ok = DECISION in status_text and "no constant_Geff_Newton_local_GR_PPN claim" in status_text
    add("VAL4107_9_status", "status records decision and no-claim state", status_ok, "status row checked")

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4107*")) or any(
            FORMALIZATION.rglob("4107-Y5-R2FR*")
        )
    add("VAL4107_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4107_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4107_VALIDATION.csv"
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
