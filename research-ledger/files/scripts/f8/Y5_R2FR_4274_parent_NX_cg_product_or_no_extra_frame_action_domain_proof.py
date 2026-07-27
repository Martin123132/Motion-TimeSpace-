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

CHECKPOINT = "4274"
CLAIM_ID = "L-115"
BRANCH = "MTS_R2FR_Y5_PARENT_NX_CG_PRODUCT_OR_NO_EXTRA_FRAME_ACTION_DOMAIN_PROOF_4274"
DECISION = "NX_CG_PRODUCT_REDUCED_TO_CG_OVER_SQRT_ZX_PARENT_CG_ZX_TAILS_STILL_BLOCK_NONCLAIM"
MARKER = "PPC4161_PARENT_NX_CG_PRODUCT_OR_NO_EXTRA_FRAME_ACTION_DOMAIN_PROOF_4274"
PACKET_MARKER = "PPC4161_PACKET_PARENT_NX_CG_PRODUCT_OR_NO_EXTRA_FRAME_ACTION_DOMAIN_PROOF_4274"
NEXT_TARGET = "4275-Y5-R2FR-parent-cg-zero-theorem-or-ZX-cg-source-row.md"

FORMAL_PATH = FORMAL / "290-PPC4161-parent-NX-cg-product-or-no-extra-frame-action-domain-proof.md"
DOC_PATH = POST / "4274-Y5-R2FR-parent-NX-cg-product-or-no-extra-frame-action-domain-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4274_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4274_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CORE_BOUND_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4274_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"

ALPHA_EFF_BOUND = 0.00578792
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
    "SRC4274_00_4273_formal": (
        FORMAL / "289-PPC4161-cg-bdis-projection-input-fill-or-parent-no-extra-frame-action-signature.md",
        "N_X c_g",
        "4273 handoff: product N_X*c_g is the first c_g-side object to derive.",
    ),
    "SRC4274_01_4273_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4273_FIRST_SCOREABLE_PROJECTION_CONTRACT.csv",
        "CON4273_0_unit_ppn_cg_contract",
        "Unit PPN projection contract for abs(N_X*c_g).",
    ),
    "SRC4274_02_1029_theorem": (
        SOURCE_DIR / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
        "NST1029_5_matter_variation_trace",
        "Older c_g theorem audit defining finite c_g as matter-frame trace coupling.",
    ),
    "SRC4274_03_1030_provenance": (
        SOURCE_DIR / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
        "CPG1030_1_finite_cg_value",
        "Provenance gate requiring numeric c_g and source path before scoring.",
    ),
    "SRC4274_04_1022_branch": (
        SOURCE_DIR / "P8_Y5_R10_1022_BRANCH_DECISION_MATRIX.csv",
        "BDM1022_2_scalar_positive_nohair",
        "Scalar-like X fallback supplies Z_X/M_X^2 normalization obligations.",
    ),
    "SRC4274_05_1018_lx": (
        POST / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "O_X X=-nabla_i(Z_X nabla^i X)+M_X^2 X",
        "Local X operator normal form containing Z_X and M_X^2.",
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


def no_extra_frame_retry_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "NEF4274_0_chain_rule_zero",
            "A_g=Abar(q(Phi)) and Dq[v_X]=0",
            "c_g=Lie_vX ln A_g=0",
            "CONDITIONAL_THEOREM_VALID",
            "parent-signed q-kernel and A_g factorization through q",
        ),
        (
            "NEF4274_1_action_domain_zero",
            "Allowed[S_matter]=Sbar[Psi,e_obs(q(Phi)),omega[e_obs],theta(q)] excluding A_g(Xhat)e_obs and B_dis(Xhat)",
            "c_g=b_dis=0 by absence of independent ordinary matter frame variables",
            "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "single-public-metric/no-extra-frame parent action domain",
        ),
        (
            "NEF4274_2_4274_verdict",
            "No-extra-frame remains the cleanest route.",
            "would bypass finite c_g/Z_X scoring",
            "ZERO_ROUTE_STILL_UNSIGNED",
            "continue finite product contract",
        ),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "premise": premise,
            "consequence": consequence,
            "status": status,
            "missing_for_claim": missing,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, premise, consequence, status, missing in raw
    ]


def normalization_derivation_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "ND4274_0_define_cg",
            "c_g := Lie_vX ln A_g",
            "finite common Weyl-frame derivative along the local X/vertical direction",
            "1029 theorem audit",
            "DEFINITION_IMPORTED",
            "does not itself supply numeric c_g",
        ),
        (
            "ND4274_1_quadratic_X_operator",
            "S_X^(2)=1/2 int sqrt(h) [ Z_X |grad delta Xhat|^2 + M_X^2 delta Xhat^2 ]",
            "Z_X is the parent kinetic Hessian/normalization of the retained X coordinate",
            "1018/1022 scalar-like local branch",
            "NORMAL_FORM_IMPORTED",
            "Z_X is not parent-sourced as a positive numeric value",
        ),
        (
            "ND4274_2_canonical_field",
            "phi_X = sqrt(Z_X) delta Xhat",
            "canonical unit kinetic normalization in the local scalar-like branch",
            "standard Hessian normalization from ND4274_1",
            "DERIVED_CONDITIONAL",
            "requires Z_X>0 and a declared Xhat convention",
        ),
        (
            "ND4274_3_NX_law",
            "N_X = d Xhat / d phi_X = 1/sqrt(Z_X)",
            "alpha_eff = |N_X c_g| = |c_g|/sqrt(Z_X)",
            "4273 product contract plus ND4274_2",
            "PRODUCT_REDUCED",
            "missing numeric c_g and Z_X or zero theorem",
        ),
        (
            "ND4274_4_bound_law",
            "|c_g| <= alpha_eff_bound sqrt(Z_X)",
            "with alpha_eff_bound=0.00578792, Y_gamma=R_gamma=1 and no-cancellation tails closed",
            "4273 PPN projection contract",
            "CG_BOUND_FORM_DERIVED",
            "claim blocked until c_g/Z_X/tails are sourced",
        ),
    ]
    return [
        {
            **common(),
            "derivation_id": derivation_id,
            "statement": statement,
            "meaning": meaning,
            "source_anchor": source_anchor,
            "status": status,
            "remaining_caveat": caveat,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for derivation_id, statement, meaning, source_anchor, status, caveat in raw
    ]


def product_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "contract_id": "PC4274_0_cg_zx_canonical_product",
            "quantity": "alpha_eff",
            "formula": "alpha_eff=abs(c_g)/sqrt(Z_X)",
            "equivalent_bound": "abs(c_g)<=0.00578792*sqrt(Z_X)",
            "required_inputs": "c_g;Z_X;Z_X>0;tail_guard;source_path;valid_for_claim",
            "filled_inputs": "N_X law from canonical Hessian normalization",
            "missing_inputs": "parent numeric c_g or zero theorem; parent positive Z_X; tail theorem-zero or absolute-sum guard",
            "status": "PRODUCT_LAW_DERIVED_NOT_SCORED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "contract_id": "PC4274_1_direct_alpha_escape_hatch",
            "quantity": "alpha_eff",
            "formula": "score direct parent alpha_eff only if the parent supplies it with source path and tail ledger",
            "equivalent_bound": "alpha_eff<=0.00578792",
            "required_inputs": "alpha_eff;tail_guard;source_path;valid_for_claim",
            "filled_inputs": "bound inherited from 4273",
            "missing_inputs": "direct parent alpha_eff row",
            "status": "DIRECT_ALPHA_ALLOWED_BUT_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_input_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "row_id": "RUN4274_0_live_missing_cg_zx",
            "row_type": "cg_zx_contract",
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
            "row_id": "RUN4274_1_zero_theorem_unsigned",
            "row_type": "zero_theorem",
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
            "row_id": "CTRL4274_0_cg_zx_toy_pass",
            "row_type": "cg_zx_contract",
            "c_g": "0.001",
            "Z_X": "1.0",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4274_1_cg_zx_toy_fail",
            "row_type": "cg_zx_contract",
            "c_g": "0.01",
            "Z_X": "1.0",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "source_path": str(FORMAL_PATH),
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "row_id": "CTRL4274_2_zx_normalization_toy_pass",
            "row_type": "cg_zx_contract",
            "c_g": "0.01",
            "Z_X": "4.0",
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
    out["N_X"] = ""
    out["computed_alpha_eff"] = ""
    out["derived_abs_cg_bound"] = ""
    out["passed_bound"] = "False"
    out["score_ready"] = "False"
    out["failure_modes"] = ""
    out["verdict"] = "REFUSED"

    if row["row_type"] == "zero_theorem":
        out["computed_alpha_eff"] = "0.0"
        out["failure_modes"] = "ZERO_THEOREM_UNSIGNED"
        out["verdict"] = "ZERO_ROUTE_BLOCKED_NONCLAIM"
        return out

    if row["row_type"] != "cg_zx_contract":
        out["failure_modes"] = "UNKNOWN_ROW_TYPE"
        return out

    bound = row.get("alpha_eff_bound", "")
    cg = row.get("c_g", "")
    zx = row.get("Z_X", "")
    missing = []
    if not is_number(cg):
        missing.append("MISSING_NUMERIC_CG_OR_ZERO_THEOREM")
    if not is_number(zx):
        missing.append("MISSING_NUMERIC_ZX")
    if not is_number(bound):
        missing.append("MISSING_ALPHA_BOUND")
    if missing:
        out["failure_modes"] = ";".join(missing + ["MISSING_TAIL_GUARD"])
        out["verdict"] = "PRODUCT_LAW_DERIVED_LIVE_ROW_BLOCKED"
        return out

    cg_value = float(cg)
    zx_value = float(zx)
    bound_value = float(bound)
    if zx_value <= 0.0:
        out["failure_modes"] = "NONPOSITIVE_ZX_REJECTED"
        out["verdict"] = "INVALID_NORMALIZATION"
        return out
    if bound_value <= 0.0:
        out["failure_modes"] = "NONPOSITIVE_BOUND_REJECTED"
        return out

    n_x = 1.0 / math.sqrt(zx_value)
    alpha_eff = abs(cg_value) * n_x
    cg_bound = bound_value * math.sqrt(zx_value)
    out["N_X"] = f"{n_x:.8g}"
    out["computed_alpha_eff"] = f"{alpha_eff:.8g}"
    out["derived_abs_cg_bound"] = f"{cg_bound:.8g}"
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


def bound_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_CG_ZX_CANONICAL_PRODUCT_4274",
            "target_component": "Dq_geom",
            "norm_or_bound": "alpha_eff=abs(c_g)/sqrt(Z_X); abs(c_g)<=0.00578792*sqrt(Z_X)",
            "numeric_bound": "requires_Z_X",
            "units": "dimensionless_if_cg_dimensionless_and_ZX_declared",
            "filled_inputs": "N_X=1/sqrt(Z_X) conditional canonical product law",
            "missing": "parent c_g or no-extra-frame theorem; positive Z_X; tail guard; b_dis projection/zero",
            "source_path": str(FORMAL_PATH),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def later_4275_geom_override() -> Dict[str, str]:
    candidates = [
        (
            SOURCE_DIR / "P8_Y5_R2FR_4277_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "0.0",
        ),
        (
            SOURCE_DIR / "P8_Y5_R2FR_4276_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW",
        ),
        (
            SOURCE_DIR / "P8_Y5_R2FR_4275_DQ_COMPONENT_VALUES_CANDIDATE.csv",
            "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE",
        ),
    ]
    for path, expected in candidates:
        for row in csv_rows(path):
            if row.get("probe_id") == "Dq_geom" and row.get("epsilon") == expected:
                return row
    return {}


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    later_geom = later_4275_geom_override()
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
                updated["epsilon"] = "MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE"
                updated["epsilon_C1"] = "MISSING_C1_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE"
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
                else "MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE"
                if probe == "Dq_geom"
                else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": later_geom["epsilon_C1"]
                if probe == "Dq_geom" and later_geom
                else "MISSING_C1_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE"
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
            "DEC4274_0_product_law",
            "Use the scalar-Hessian normalization to reduce N_X*c_g to c_g/sqrt(Z_X).",
            "This removes N_X as a free symbol if the retained X branch is scalar-like and Z_X>0.",
            "derive/source c_g and Z_X",
        ),
        (
            "DEC4274_1_zero_route",
            "The no-extra-frame action-domain theorem remains cleaner than scoring a finite coupling.",
            "If signed, c_g and b_dis vanish by action-domain exclusion.",
            "try parent no-extra-frame proof in parallel with c_g/Z_X source row",
        ),
        (
            "DEC4274_2_claim_status",
            "No local-GR/PPN claim follows from the product law alone.",
            "c_g, Z_X, b_dis route, and no-cancellation tails remain unsourced.",
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
        ("FW4274_0_no_free_NX", "N_X cannot remain a free fit symbol in the scalar-like branch; use N_X=1/sqrt(Z_X) or source a different canonical map."),
        ("FW4274_1_positive_ZX", "Z_X<=0 rejects the local scalar branch instead of weakening the bound."),
        ("FW4274_2_no_cg_claim", "A product law is not a parent c_g value; c_g still needs zero theorem or source path."),
        ("FW4274_3_no_tail_cancellation", "b_dis, source, gauge, readout, and boundary tails must be theorem-zero or absolute-summed."),
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
            "status_id": "STATUS4274",
            "current_status": "N_X*c_g product reduced to c_g/sqrt(Z_X); parent c_g/Z_X/tails remain missing",
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
            "why": "4274 removed N_X as an independent fog coefficient in the scalar-like branch; the next missing objects are c_g=0/public no-extra-frame or finite c_g plus positive Z_X.",
            "success_condition": "prove c_g=0 from no-extra-frame, or provide a sourced parent row for c_g and Z_X>0 plus tail guard.",
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
            "4274 reduces the 4273 product N_X*c_g using the scalar-like local Hessian: for S_X^(2)=1/2 int sqrt(h)[Z_X|grad Xhat|^2+M_X^2 Xhat^2], the canonical field is "
            "phi_X=sqrt(Z_X) Xhat, so N_X=1/sqrt(Z_X) and alpha_eff=|c_g|/sqrt(Z_X). The live PPN contract is therefore |c_g|<=0.00578792 sqrt(Z_X), but no claim is allowed "
            "until c_g or the no-extra-frame theorem, positive Z_X, b_dis routing, and tails are parent-sourced."
        ),
        "current_evidence": (
            "4274 source register, no-extra-frame retry, normalization derivation rows, product contract, runner results, updated Dq_geom candidate, decision and firewall."
        ),
        "status": "private_NX_cg_product_reduced_to_cg_over_sqrt_ZX_nonclaim",
        "next_test": "Prove c_g=0 by public no-extra-frame action-domain theorem, or source finite c_g and positive Z_X with tail guards.",
        "key_risk": "Treating N_X=1/sqrt(Z_X) as a c_g value, allowing Z_X<=0, or ignoring b_dis/source/gauge/readout tails.",
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
# 290 - PPC4161 parent N_X c_g product or no-extra-frame action-domain proof

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4274 does not claim local GR, PPN, R10, WEP, clock, orbital, Newtonian, or EM closure.

It reduces the live blocker:

```text
old 4273 blocker: MISSING_NX_CG_PRODUCT_AND_TAIL_GUARDS_FOR_CG_BDIS_FRAME_VECTOR
new 4274 blocker: MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE
```

## Product derivation

The retained finite common-frame coefficient is:

```text
c_g := Lie_vX ln A_g.
```

For a scalar-like retained `X` branch, the local quadratic Hessian has the normal form:

```text
S_X^(2)=1/2 int sqrt(h) [ Z_X |grad delta Xhat|^2 + M_X^2 delta Xhat^2 ].
```

The canonical local scalar coordinate is therefore:

```text
phi_X = sqrt(Z_X) delta Xhat,
N_X = d Xhat/d phi_X = 1/sqrt(Z_X).
```

So the 4273 product is:

```text
alpha_eff = |N_X c_g| = |c_g|/sqrt(Z_X).
```

With the 4273 unit PPN response contract:

```text
|c_g| <= 0.00578792 sqrt(Z_X).
```

This is only a contract. It is not an MTS prediction until `c_g` and positive `Z_X` are parent-owned, and tails are theorem-zero or absolute-summed.

## Zero route

The cleaner route remains:

```text
A_g=Abar(q(Phi)), Dq[v_X]=0
or
no independent A_g/B_dis ordinary-frame action slot
```

which would give:

```text
c_g=b_dis=0.
```

Current evidence still does not public-sign that action-domain theorem.

## Next target

`{NEXT_TARGET}` should prove `c_g=0` by no-extra-frame action domain or fill a finite parent `c_g,Z_X` source row.
"""


def checkpoint_doc() -> str:
    return f"""
# 4274 - parent N_X c_g product or no-extra-frame action-domain proof

Marker: `{MARKER}`

Decision: `{DECISION}`

4274 takes the 4273 product `N_X c_g` and removes `N_X` as an independent free symbol in the scalar-like branch:

```text
N_X = 1/sqrt(Z_X),
alpha_eff = |c_g|/sqrt(Z_X).
```

The remaining obstruction is now:

```text
c_g=0 public theorem
or
finite c_g + positive Z_X + tail guards.
```

All rows remain `valid_for_claim=false`.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    derivations = csv_rows(paths["normalization"])
    contracts = csv_rows(paths["product_contract"])
    runners = csv_rows(paths["runner"])
    components = csv_rows(paths["local_candidate"])
    acceptable_geom_epsilons = {
        "MISSING_PARENT_CG_AND_POSITIVE_ZX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW",
        "0.0",
    }
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + csv_rows(paths["no_extra_frame_retry"])
        + derivations
        + contracts
        + csv_rows(paths["runner_inputs"])
        + runners
        + csv_rows(paths["core_bound"])
        + components
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4274_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4274_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4274_2_product_law",
            any(row["derivation_id"] == "ND4274_3_NX_law" and row["status"] == "PRODUCT_REDUCED" for row in derivations),
            "N_X law reduces product to c_g/sqrt(Z_X)",
        ),
        (
            "VAL4274_3_contract_written",
            any(row["contract_id"] == "PC4274_0_cg_zx_canonical_product" and "sqrt(Z_X)" in row["equivalent_bound"] for row in contracts),
            "c_g/Z_X product contract written",
        ),
        (
            "VAL4274_4_live_blocked",
            any(row["row_id"] == "RUN4274_0_live_missing_cg_zx" and row["verdict"] == "PRODUCT_LAW_DERIVED_LIVE_ROW_BLOCKED" for row in runners),
            "live row blocked by missing c_g/Z_X",
        ),
        (
            "VAL4274_5_controls_compute",
            any(row["row_id"] == "CTRL4274_0_cg_zx_toy_pass" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in runners)
            and any(row["row_id"] == "CTRL4274_1_cg_zx_toy_fail" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in runners)
            and any(row["row_id"] == "CTRL4274_2_zx_normalization_toy_pass" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in runners),
            "toy controls verify c_g/Z_X arithmetic",
        ),
        (
            "VAL4274_6_live_4254_updated",
            any(row.get("probe_id") == "Dq_geom" and row.get("epsilon") in acceptable_geom_epsilons for row in components),
            "live Dq_geom candidate sharpened or later-refined",
        ),
        ("VAL4274_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4274_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4274_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4274_10_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4274_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4274_SOURCE_REGISTER.csv",
        "no_extra_frame_retry": SOURCE_DIR / "P8_Y5_R2FR_4274_NO_EXTRA_FRAME_RETRY.csv",
        "normalization": SOURCE_DIR / "P8_Y5_R2FR_4274_NX_CG_NORMALIZATION_DERIVATION.csv",
        "product_contract": SOURCE_DIR / "P8_Y5_R2FR_4274_PRODUCT_CONTRACT.csv",
        "runner_inputs": SOURCE_DIR / "P8_Y5_R2FR_4274_BOUND_RUNNER_INPUTS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4274_BOUND_RUNNER_RESULTS.csv",
        "core_bound": CORE_BOUND_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4274_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4274_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4274_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4274_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["no_extra_frame_retry"], no_extra_frame_retry_rows())
    write_csv(paths["normalization"], normalization_derivation_rows())
    write_csv(paths["product_contract"], product_contract_rows())
    write_csv(paths["runner_inputs"], runner_input_rows())
    write_csv(paths["runner"], runner_rows())
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
        "PPC4161 4274 N_X c_g product reduction",
        "4274 reduces the 4273 product `N_X c_g` to `c_g/sqrt(Z_X)` in the scalar-like local Hessian branch. The next live target is no-extra-frame `c_g=0`, or finite parent `c_g` plus positive `Z_X` and tail guards.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4274 packet N_X c_g product reduction",
        "Packet update: `Dq_geom` is now blocked by parent `c_g` and positive `Z_X`, or by the unsigned public no-extra-frame theorem.",
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
