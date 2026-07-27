from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4275"
CLAIM_ID = "L-116"
BRANCH = "MTS_R2FR_Y5_PARENT_CG_ZERO_THEOREM_OR_ZX_CG_SOURCE_ROW_4275"
DECISION = "RAW_CG_ZX_REPLACED_BY_CANONICAL_GX_INVARIANT_COUPLING_PARENT_GX_OR_ZERO_THEOREM_STILL_BLOCKED"
MARKER = "PPC4161_PARENT_CG_ZERO_THEOREM_OR_ZX_CG_SOURCE_ROW_4275"
PACKET_MARKER = "PPC4161_PACKET_PARENT_CG_ZERO_THEOREM_OR_ZX_CG_SOURCE_ROW_4275"
NEXT_TARGET = "4276-Y5-R2FR-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md"

FORMAL_PATH = FORMAL / "291-PPC4161-parent-cg-zero-theorem-or-ZX-cg-source-row.md"
DOC_PATH = POST / "4275-Y5-R2FR-parent-cg-zero-theorem-or-ZX-cg-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4275_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4275_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CORE_BOUND_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4275_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"

ALPHA_EFF_BOUND = 0.00578792
LATER_4276_BLOCKER = "MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW"
LATER_4276_BLOCKER_C1 = "MISSING_C1_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW"
LATER_4277_FORMAL_PATH = FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

PROBE_ORDER = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)

SOURCES = {
    "SRC4275_00_4274_formal": (
        FORMAL / "290-PPC4161-parent-NX-cg-product-or-no-extra-frame-action-domain-proof.md",
        "alpha_eff = |N_X c_g| = |c_g|/sqrt(Z_X)",
        "4274 handoff: c_g/Z_X product law.",
    ),
    "SRC4275_01_4274_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4274_PRODUCT_CONTRACT.csv",
        "PC4274_0_cg_zx_canonical_product",
        "4274 contract for alpha_eff=abs(c_g)/sqrt(Z_X).",
    ),
    "SRC4275_02_4273_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4273_FIRST_SCOREABLE_PROJECTION_CONTRACT.csv",
        "CON4273_0_unit_ppn_cg_contract",
        "4273 unit PPN alpha_eff bound.",
    ),
    "SRC4275_03_1029_theorem": (
        SOURCE_DIR / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
        "NST1029_1_chain_rule_zero",
        "Older no-shadow chain-rule zero theorem route.",
    ),
    "SRC4275_04_1030_provenance": (
        SOURCE_DIR / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
        "CPG1030_1_finite_cg_value",
        "Older finite c_g provenance gate.",
    ),
    "SRC4275_05_1026_metric_lock": (
        POST / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
        "parent metric route remains unowned",
        "Older warning that raw Z_X metric lock is not parent-owned.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_number(value: str) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
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


def invariant_derivation_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "INV4275_0_raw_quantities",
            "c_g := d ln A_g/dXhat and S_X^(2)=1/2 int sqrt(h) Z_X |grad Xhat|^2 + ...",
            "raw c_g and Z_X depend on the Xhat coordinate convention",
            "4274 product law",
            "RAW_PAIR_NOT_OBSERVABLE_ALONE",
        ),
        (
            "INV4275_1_reparam_test",
            "Xprime=a Xhat gives c_gprime=c_g/a and Z_Xprime=Z_X/a^2",
            "|c_gprime|/sqrt(Z_Xprime)=|c_g|/sqrt(Z_X)",
            "direct chain-rule calculation",
            "INVARIANCE_PROVED",
        ),
        (
            "INV4275_2_define_gX",
            "phi_X=sqrt(Z_X) Xhat and g_X:=d ln A_g/dphi_X",
            "g_X=c_g/sqrt(Z_X)=N_X c_g up to orientation sign",
            "canonical Hessian normalization",
            "CANONICAL_COUPLING_DEFINED",
        ),
        (
            "INV4275_3_ppn_contract",
            "alpha_eff=|g_X| under the 4273 unit PPN response contract",
            "|g_X|<=0.00578792 before tails",
            "4273/4274 alpha_eff bound",
            "INVARIANT_BOUND_CONTRACT_DERIVED",
        ),
        (
            "INV4275_4_zero_route",
            "If A_g factors through q or no A_g/B_dis action slot exists, g_X=0",
            "no-extra-frame theorem kills the invariant coupling directly",
            "1029 chain-rule zero route",
            "ZERO_ROUTE_STILL_UNSIGNED",
        ),
    ]
    return [
        {
            **common(),
            "derivation_id": derivation_id,
            "statement": statement,
            "consequence": consequence,
            "source_anchor": source_anchor,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for derivation_id, statement, consequence, source_anchor, status in raw
    ]


def canonical_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "contract_id": "GC4275_0_canonical_gX_contract",
            "quantity": "g_X",
            "definition": "g_X := d ln A_g / d phi_X = c_g/sqrt(Z_X)",
            "score_formula": "abs(g_X) <= alpha_eff_bound",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "replaces": "raw c_g plus Z_X product scoring",
            "required_inputs": "parent g_X or no-extra-frame zero theorem; tail_guard; b_dis route; source_path; valid_for_claim",
            "status": "CANONICAL_INVARIANT_CONTRACT_DERIVED_NOT_SCORED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "contract_id": "GC4275_1_raw_cg_zx_demoted",
            "quantity": "c_g;Z_X",
            "definition": "raw coordinate pair allowed only as one way to compute g_X",
            "score_formula": "compute g_X=c_g/sqrt(Z_X), then score abs(g_X)",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "replaces": "separate c_g and Z_X target",
            "required_inputs": "numeric c_g; positive Z_X; same Xhat convention; source_path; valid_for_claim",
            "status": "RAW_PAIR_DEMOTED_TO_INPUT_ROUTE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_input_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "row_id": "RUN4275_0_live_missing_gX",
            "row_type": "canonical_gx",
            "g_X": "MISSING_PARENT_CANONICAL_GX_OR_ZERO_THEOREM",
            "c_g": "",
            "Z_X": "",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "MISSING_TAIL_THEOREM_ZERO_OR_ABSOLUTE_SUM",
            "source_path": str(FORMAL_PATH),
            "control_only": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "RUN4275_1_live_raw_pair_missing",
            "row_type": "raw_cg_zx_to_gx",
            "g_X": "",
            "c_g": "MISSING_PARENT_CG_OR_ZERO_THEOREM",
            "Z_X": "MISSING_PARENT_POSITIVE_ZX",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "MISSING_TAIL_THEOREM_ZERO_OR_ABSOLUTE_SUM",
            "source_path": str(FORMAL_PATH),
            "control_only": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "RUN4275_2_zero_theorem_unsigned",
            "row_type": "zero_theorem",
            "g_X": "0.0",
            "c_g": "0.0",
            "Z_X": "not_applicable",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "MISSING_PUBLIC_PARENT_NO_EXTRA_FRAME_SIGNATURE",
            "source_path": str(FORMAL_PATH),
            "control_only": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4275_0_gx_toy_pass",
            "row_type": "canonical_gx",
            "g_X": "0.001",
            "c_g": "",
            "Z_X": "",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4275_1_gx_toy_fail",
            "row_type": "canonical_gx",
            "g_X": "0.01",
            "c_g": "",
            "Z_X": "",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4275_2_raw_pair_toy_pass",
            "row_type": "raw_cg_zx_to_gx",
            "g_X": "",
            "c_g": "0.01",
            "Z_X": "4.0",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4275_3_reparam_invariance",
            "row_type": "raw_cg_zx_to_gx",
            "g_X": "",
            "c_g": "0.005",
            "Z_X": "1.0",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def score_row(row: Dict[str, str]) -> Dict[str, str]:
    out = dict(row)
    out["computed_g_X"] = ""
    out["computed_alpha_eff"] = ""
    out["passed_bound"] = "False"
    out["score_ready"] = "False"
    out["failure_modes"] = ""
    out["verdict"] = "REFUSED"

    bound = row.get("alpha_eff_bound", "")
    if not is_number(bound) or float(bound) <= 0.0:
        out["failure_modes"] = "MISSING_OR_NONPOSITIVE_ALPHA_BOUND"
        return out
    bound_value = float(bound)

    if row["row_type"] == "zero_theorem":
        out["computed_g_X"] = "0.0"
        out["computed_alpha_eff"] = "0.0"
        out["failure_modes"] = "ZERO_THEOREM_UNSIGNED"
        out["verdict"] = "ZERO_ROUTE_BLOCKED_NONCLAIM"
        return out

    if row["row_type"] == "canonical_gx":
        gx = row.get("g_X", "")
        if not is_number(gx):
            out["failure_modes"] = "MISSING_PARENT_CANONICAL_GX_OR_ZERO_THEOREM;MISSING_TAIL_GUARD"
            out["verdict"] = "CANONICAL_CONTRACT_DERIVED_LIVE_ROW_BLOCKED"
            return out
        g_value = float(gx)
    elif row["row_type"] == "raw_cg_zx_to_gx":
        cg = row.get("c_g", "")
        zx = row.get("Z_X", "")
        missing = []
        if not is_number(cg):
            missing.append("MISSING_NUMERIC_CG")
        if not is_number(zx):
            missing.append("MISSING_NUMERIC_ZX")
        if missing:
            out["failure_modes"] = ";".join(missing + ["RAW_PAIR_ROUTE_BLOCKED"])
            out["verdict"] = "RAW_PAIR_TO_GX_BLOCKED"
            return out
        zx_value = float(zx)
        if zx_value <= 0.0:
            out["failure_modes"] = "NONPOSITIVE_ZX_REJECTED"
            out["verdict"] = "INVALID_NORMALIZATION"
            return out
        g_value = float(cg) / math.sqrt(zx_value)
    else:
        out["failure_modes"] = "UNKNOWN_ROW_TYPE"
        return out

    alpha_eff = abs(g_value)
    out["computed_g_X"] = f"{g_value:.8g}"
    out["computed_alpha_eff"] = f"{alpha_eff:.8g}"
    out["passed_bound"] = str(alpha_eff <= bound_value)

    if row.get("control_only") == "True":
        out["failure_modes"] = "CONTROL_ONLY"
        out["verdict"] = "CONTROL_PASS_NONCLAIM" if alpha_eff <= bound_value else "CONTROL_FAIL_NONCLAIM"
        return out

    if row.get("tail_guard_status") != "THEOREM_ZERO" or row.get("valid_for_claim") != "True":
        out["failure_modes"] = "TAIL_GUARD_NOT_CLOSED_OR_VALID_FOR_CLAIM_FALSE"
        out["verdict"] = "NUMERIC_BUT_NONCLAIM" if alpha_eff <= bound_value else "NUMERIC_FAIL_NONCLAIM"
        return out

    out["score_ready"] = "True"
    out["verdict"] = "PASS_CLAIM_READY" if alpha_eff <= bound_value else "FAIL_CLAIM_READY"
    return out


def runner_rows() -> List[Dict[str, str]]:
    return [score_row(row) for row in runner_input_rows()]


def invariance_smoke_rows() -> List[Dict[str, str]]:
    base_cg = 0.01
    base_zx = 4.0
    scale = 2.0
    scaled_cg = base_cg / scale
    scaled_zx = base_zx / (scale * scale)
    base_gx = base_cg / math.sqrt(base_zx)
    scaled_gx = scaled_cg / math.sqrt(scaled_zx)
    return [
        {
            **common(),
            "smoke_id": "INVSMOKE4275_0_reparam",
            "base_cg": f"{base_cg:.8g}",
            "base_Z_X": f"{base_zx:.8g}",
            "scale_a": f"{scale:.8g}",
            "scaled_cg": f"{scaled_cg:.8g}",
            "scaled_Z_X": f"{scaled_zx:.8g}",
            "base_g_X_abs": f"{abs(base_gx):.8g}",
            "scaled_g_X_abs": f"{abs(scaled_gx):.8g}",
            "invariant": str(math.isclose(abs(base_gx), abs(scaled_gx), rel_tol=0.0, abs_tol=1e-14)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def bound_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_CANONICAL_GX_CONTRACT_4275",
            "target_component": "Dq_geom",
            "norm_or_bound": "alpha_eff=abs(g_X); abs(g_X)<=0.00578792",
            "numeric_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "units": "dimensionless canonical coupling",
            "filled_inputs": "normalization-invariant g_X definition; reparametrization guard",
            "missing": "parent canonical g_X or no-extra-frame theorem; tail guard; b_dis projection/zero",
            "source_path": str(FORMAL_PATH),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def later_4276_geom_override() -> Dict[str, str]:
    candidates = [
        (
            SOURCE_DIR / "P8_Y5_R2FR_4277_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "0.0",
        ),
        (
            SOURCE_DIR / "P8_Y5_R2FR_4276_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            LATER_4276_BLOCKER,
        ),
    ]
    for path, expected in candidates:
        for row in csv_rows(path):
            if row.get("probe_id") == "Dq_geom" and row.get("epsilon") == expected:
                return row
    return {}


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    later_geom = later_4276_geom_override()
    rows: List[Dict[str, str]] = []
    seen = set()
    for row in previous:
        probe = row.get("probe_id", "")
        if not probe:
            continue
        updated = dict(row)
        updated.update(common())
        if probe == "Dq_geom":
            if later_geom:
                updated["epsilon"] = later_geom["epsilon"]
                updated["epsilon_C1"] = later_geom["epsilon_C1"]
                updated["source_path"] = later_geom["source_path"]
            else:
                updated["epsilon"] = "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE"
                updated["epsilon_C1"] = "MISSING_C1_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE"
                updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        rows.append(updated)
        seen.add(probe)
    for probe in PROBE_ORDER:
        if probe in seen:
            continue
        rows.append(
            {
                **common(),
                "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": later_geom["epsilon"]
                if probe == "Dq_geom" and later_geom
                else "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE"
                if probe == "Dq_geom"
                else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": later_geom["epsilon_C1"]
                if probe == "Dq_geom" and later_geom
                else "MISSING_C1_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE"
                if probe == "Dq_geom"
                else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": later_geom["source_path"] if probe == "Dq_geom" and later_geom else str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4275_0_invariant_target",
            "Promote canonical g_X as the finite coefficient target.",
            "Raw c_g and Z_X are coordinate-convention dependent; g_X=c_g/sqrt(Z_X) is the invariant product.",
            "derive/source parent g_X",
        ),
        (
            "DEC4275_1_raw_pair_route",
            "Keep raw c_g,Z_X only as an input route to g_X.",
            "This prevents unit-rescaling or X-coordinate games from changing the apparent bound.",
            "require same convention and Z_X>0 if raw pair is used",
        ),
        (
            "DEC4275_2_zero_route",
            "The no-extra-frame theorem remains the cleanest closure.",
            "If the parent action excludes/factors A_g and B_dis, g_X=0 and b_dis=0.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4275_0_no_raw_rescaling", "Do not score raw c_g without Z_X and a shared Xhat convention."),
        ("FW4275_1_invariant_only", "Finite local PPN scoring uses canonical g_X or direct alpha_eff, not separate raw coefficients."),
        ("FW4275_2_zero_theorem_unsigned", "g_X=0 needs public no-extra-frame/factor-through-q theorem, not WEP/covariance alone."),
        ("FW4275_3_tail_guard", "b_dis, q_nonH, source, readout, gauge, boundary, and EM tails remain theorem-zero or absolute-sum obligations."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4275",
            "current_status": "canonical invariant g_X contract derived; parent g_X or no-extra-frame theorem still missing",
            "local_gr_claim": "False",
            "ppn_claim": "False",
            "newton_claim": "False",
            "em_claim": "False",
            "next_best_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4275 removes raw normalization ambiguity; the remaining finite target is parent canonical g_X, or theorem-zero no-shadow action domain.",
            "success_condition": "derive g_X=0 by no-extra-frame/factor-through-q theorem, or provide a source-backed canonical g_X row with tail guards.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4275 replaces the raw c_g,Z_X target with the canonical invariant coupling g_X:=d ln A_g/dphi_X=c_g/sqrt(Z_X). Under Xhat rescalings, c_g and Z_X change but |g_X| does not, "
            "so the finite PPN contract is |g_X|<=0.00578792 before tails. This is not a local-GR claim: parent g_X or the no-extra-frame theorem, b_dis routing, and tail guards remain missing."
        ),
        "current_evidence": (
            "4275 source register, invariant derivation rows, canonical g_X contract, invariance smoke row, runner results, updated Dq_geom candidate, decision and firewall."
        ),
        "status": "private_canonical_gX_invariant_contract_derived_nonclaim",
        "next_test": "Prove g_X=0 from no-extra-frame/factor-through-q parent action, or source a finite canonical g_X row with tail guards.",
        "key_risk": "Unit-rescaling raw c_g/Z_X, claiming g_X=0 from WEP/covariance alone, or ignoring b_dis and source/readout/gauge tails.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def append_unique_block(path: Path, marker: str, title: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n", encoding="utf-8")


def formal_doc() -> str:
    return f"""
# 291 - PPC4161 parent c_g zero theorem or Z_X c_g source row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4275 does not claim local GR, PPN, R10, WEP, clock, orbital, Newtonian, or EM closure.

It sharpens the live blocker:

```text
old 4274 blocker: MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE
new 4275 blocker: MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE
```

## Invariant coupling

4274 derived:

```text
alpha_eff = |c_g|/sqrt(Z_X).
```

But raw `c_g` and `Z_X` separately depend on the chosen `Xhat` coordinate. If:

```text
Xprime = a Xhat,
```

then:

```text
c_gprime = c_g/a,
Z_Xprime = Z_X/a^2,
|c_gprime|/sqrt(Z_Xprime)=|c_g|/sqrt(Z_X).
```

So define the canonical coupling:

```text
phi_X = sqrt(Z_X) Xhat,
g_X := d ln A_g/d phi_X = c_g/sqrt(Z_X).
```

The finite PPN contract is now:

```text
|g_X| <= 0.00578792
```

before tails.

## Zero route

If the parent signs:

```text
A_g=Abar(q(Phi)), Dq[v_X]=0
```

or excludes independent `A_g/B_dis` ordinary-frame action slots, then:

```text
g_X=0,
b_dis=0.
```

That remains unsigned in the current public parent corpus.

## Next target

`{NEXT_TARGET}` should either prove the no-shadow/no-extra-frame theorem for `g_X=0`, or provide the first source-backed canonical `g_X` row.
"""


def checkpoint_doc() -> str:
    return f"""
# 4275 - parent c_g zero theorem or Z_X c_g source row

Marker: `{MARKER}`

Decision: `{DECISION}`

4275 does the normalization cleanup that the local branch needed:

```text
g_X := d ln A_g/dphi_X = c_g/sqrt(Z_X).
```

The live bound becomes:

```text
|g_X| <= 0.00578792
```

Raw `c_g,Z_X` rows are now only an input route to `g_X`, not the promoted target.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    derivations = csv_rows(paths["invariant_derivation"])
    contracts = csv_rows(paths["canonical_contract"])
    runners = csv_rows(paths["runner"])
    smoke = csv_rows(paths["invariance_smoke"])
    components = csv_rows(paths["local_candidate"])
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + derivations
        + contracts
        + csv_rows(paths["runner_inputs"])
        + runners
        + smoke
        + csv_rows(paths["core_bound"])
        + components
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4275_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4275_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4275_2_invariant_derivation",
            any(row["derivation_id"] == "INV4275_2_define_gX" and row["status"] == "CANONICAL_COUPLING_DEFINED" for row in derivations),
            "canonical g_X is defined",
        ),
        (
            "VAL4275_3_contract_written",
            any(row["contract_id"] == "GC4275_0_canonical_gX_contract" and row["alpha_eff_bound"] == f"{ALPHA_EFF_BOUND:.8f}" for row in contracts),
            "canonical g_X contract written",
        ),
        (
            "VAL4275_4_live_blocked",
            any(row["row_id"] == "RUN4275_0_live_missing_gX" and row["verdict"] == "CANONICAL_CONTRACT_DERIVED_LIVE_ROW_BLOCKED" for row in runners),
            "live canonical row blocked by missing parent g_X",
        ),
        (
            "VAL4275_5_controls_compute",
            any(row["row_id"] == "CTRL4275_0_gx_toy_pass" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in runners)
            and any(row["row_id"] == "CTRL4275_1_gx_toy_fail" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in runners)
            and any(row["row_id"] == "CTRL4275_2_raw_pair_toy_pass" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in runners),
            "toy controls verify g_X and raw-pair-to-g_X arithmetic",
        ),
        (
            "VAL4275_6_reparam_smoke",
            any(row["smoke_id"] == "INVSMOKE4275_0_reparam" and row["invariant"] == "True" for row in smoke),
            "rescaling smoke confirms |g_X| invariant",
        ),
        (
            "VAL4275_7_live_4254_updated",
            any(
                row.get("probe_id") == "Dq_geom"
                and row.get("epsilon") in {"MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE", LATER_4276_BLOCKER, "0.0"}
                and row.get("epsilon_C1") in {"MISSING_C1_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE", LATER_4276_BLOCKER_C1, "0.0"}
                and row.get("source_path") in {str(FORMAL_PATH), str(FORMAL / "292-PPC4161-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md"), str(LATER_4277_FORMAL_PATH)}
                for row in components
            ),
            "live Dq_geom candidate sharpened",
        ),
        ("VAL4275_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4275_9_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4275_10_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4275_11_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4275_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4275_SOURCE_REGISTER.csv",
        "invariant_derivation": SOURCE_DIR / "P8_Y5_R2FR_4275_CANONICAL_GX_INVARIANT_DERIVATION.csv",
        "canonical_contract": SOURCE_DIR / "P8_Y5_R2FR_4275_CANONICAL_GX_CONTRACT.csv",
        "runner_inputs": SOURCE_DIR / "P8_Y5_R2FR_4275_BOUND_RUNNER_INPUTS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4275_BOUND_RUNNER_RESULTS.csv",
        "invariance_smoke": SOURCE_DIR / "P8_Y5_R2FR_4275_REPARAM_INVARIANCE_SMOKE.csv",
        "core_bound": CORE_BOUND_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4275_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4275_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4275_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4275_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["invariant_derivation"], invariant_derivation_rows())
    write_csv(paths["canonical_contract"], canonical_contract_rows())
    write_csv(paths["runner_inputs"], runner_input_rows())
    write_csv(paths["runner"], runner_rows())
    write_csv(paths["invariance_smoke"], invariance_smoke_rows())
    write_csv(paths["core_bound"], bound_candidate_rows())
    component_candidate = component_candidate_rows()
    write_csv(paths["local_candidate"], component_candidate)
    write_csv(LIVE_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4275 canonical g_X invariant coupling",
        "4275 replaces raw `c_g,Z_X` scoring with the canonical invariant coupling `g_X=d ln A_g/dphi_X=c_g/sqrt(Z_X)`. The finite local PPN contract is now `|g_X|<=0.00578792` before tails; the next target is parent `g_X=0` or a source-backed finite `g_X` row.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4275 packet canonical g_X invariant coupling",
        "Packet update: `Dq_geom` is now blocked by parent canonical `g_X` or the public no-extra-frame theorem, not by raw coordinate-normalization choices.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
