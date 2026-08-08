from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4508"
CLAIM_ID = "L-350"
MARKER = "PPC4161_MEMORY_WEYL_RESPONSE_TAIL_OR_BMEM_FINITE_BOUND_ROW_4508"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_WEYL_RESPONSE_TAIL_OR_BMEM_FINITE_BOUND_ROW_4508"
DECISION = "THETAWM_DECOMPOSED_SOURCE_ROOT_AND_NO_SPURION_ZERO_ROUTES_OR_FINITE_BWEYL_BOUND_NONCLAIM"
NEXT_TARGET = "4509-Y5-R2FR-source-root-no-spurion-combined-gate-or-BWeyl-numeric-row.md"

FORMAL_PATH = FORMAL / "524-PPC4161-memory-Weyl-response-tail-or-Bmem-finite-bound-row.md"
DOC_PATH = POST / "4508-Y5-R2FR-memory-Weyl-response-tail-or-Bmem-finite-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4508_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4508_SOURCE_REGISTER.csv"
WEYL_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4508_WEYL_OPERATOR_DERIVATION.csv"
THETAW_DECOMP = SOURCE_DIR / "P8_Y5_R2FR_4508_THETAWM_DECOMPOSITION.csv"
ZERO_GATE = SOURCE_DIR / "P8_Y5_R2FR_4508_THETAWM_ZERO_GATE.csv"
FINITE_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4508_BWEYL_FINITE_BOUND_ROW.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4508_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4508_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4508_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4508_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4508_DECISION.csv"

FORMAL_523 = FORMAL / "523-PPC4161-memory-trace-projection-lock-or-finite-Bmem-source-row.md"
POST_4507 = POST / "4507-Y5-R2FR-memory-trace-projection-lock-or-finite-Bmem-source-row.md"
SCRIPT_4507 = SCRIPT_DIR / "Y5_R2FR_4507_memory_trace_projection_lock_or_finite_Bmem_source_row.py"
STATUS_4507 = SOURCE_DIR / "P8_Y5_R2FR_4507_STATUS.csv"
FORMULA_4507 = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv"
FINITE_4507 = SOURCE_DIR / "P8_Y5_R2FR_4507_FINITE_BMEM_SOURCE_ROW.csv"

LCG_1520 = SOURCE_DIR / "P8_Y5_PARENT_LCG_1520_METRIC_SILENCE_THEOREM.csv"
LCG_1369 = SOURCE_DIR / "P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv"
LCG_2734 = SOURCE_DIR / "P8_Y5_R2FR_2734_LCG_METRIC_SILENCE_AUDIT.csv"
GMV_2409 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2409_GAMMA_EFF_METRIC_VARIATION_MERGE.csv"
MRD_3627 = SOURCE_DIR / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv"
KMC_3628 = SOURCE_DIR / "P8_Y5_R2FR_3628_KMETRIC_KHAT_COMPARISON.csv"
KMC_4115 = SOURCE_DIR / "P8_Y5_R2FR_4115_KMETRIC_KHAT_COMPARISON.csv"
WEYL_3606 = SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_NO_SPURION_THEOREM.csv"
WEYL_BOUND_3606 = SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_BOUND_ROWS.csv"
WEYL_ACQ_3607 = SOURCE_DIR / "P8_Y5_R2FR_3607_BQWEYL_FINITE_ACQUISITION_ROWS.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4508_00_formal523", "4507 formal handoff", FORMAL_523, "B_mem_eff = a_F L_cg^-2 R_m", "Bmem effective formula"),
        ("SRC4508_01_post4507", "4507 post mirror", POST_4507, "Theta_W,m", "named Weyl tail"),
        ("SRC4508_02_script4507", "4507 generator", SCRIPT_4507, 'CHECKPOINT = "4507"', "reproducible predecessor"),
        ("SRC4508_03_status4507", "4507 status", STATUS_4507, "PRIVATE_NONCLAIM", "checkpoint status"),
        ("SRC4508_04_formula4507", "4507 formula csv", FORMULA_4507, "BMF4507_2_Weyl_tail", "ThetaW row"),
        ("SRC4508_05_finite4507", "4507 finite row", FINITE_4507, "FBM4507_0_memory_B_source", "Bmem finite row"),
        ("SRC4508_06_lcg1520", "1520 Lcg metric silence theorem", LCG_1520, "ML1520_2_chain_term", "Lcg chain term"),
        ("SRC4508_07_lcg1369", "1369 Lcg metric response", LCG_1369, "ML1369_3_chain_zero_gate_update", "chain zero gate"),
        ("SRC4508_08_lcg2734", "2734 Lcg metric silence audit", LCG_2734, "LCGMS2734_3_source_root_coefficient_kill", "source root route"),
        ("SRC4508_09_gmv2409", "2409 Gamma metric variation", GMV_2409, "GMV2409_0_response_doublet", "formal metric variation"),
        ("SRC4508_10_mrd3627", "3627 Gamma/Khat metric response", MRD_3627, "MRD3627_1_metric_response", "Kmetric definition"),
        ("SRC4508_11_kmc3628", "3628 Kmetric/Khat comparison", KMC_3628, "KMC3628_5_verdict", "Khat match missing"),
        ("SRC4508_12_kmc4115", "4115 current spine Kmetric comparison", KMC_4115, "KMC4115_5_verdict", "latest Khat residual"),
        ("SRC4508_13_weyl3606_index", "3606 one-Weyl index lemma", WEYL_3606, "BQW3606_1_metric_trace_index_lemma", "metric-only linear Weyl zero"),
        ("SRC4508_14_weyl3606_spurion", "3606 spurion necessity", WEYL_3606, "BQW3606_3_spurion_necessity", "linear Weyl needs spurion"),
        ("SRC4508_15_weyl3606_bound", "3606 finite Weyl bound", WEYL_3606, "BQW3606_5_finite_bound_law", "finite bound law"),
        ("SRC4508_16_weylbound3606", "3606 Weyl bound rows", WEYL_BOUND_3606, "BQB3606_1_BqWeyl", "BqWeyl finite coefficient"),
        ("SRC4508_17_weylacq3607", "3607 Weyl acquisition rows", WEYL_ACQ_3607, "BACQ3607_11_acceptance_rule", "acceptance gate"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def weyl_operator_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "WOP4508_0_define",
            "object": "unit Weyl generator",
            "formula": "W_g[X] := d/dsigma X[e^{2sigma}g]|sigma=0 at fixed non-metric parent fields before readout",
            "result": "defines the trace metric-response tail without choosing a PPN gauge",
            "status": "DERIVED_OPERATOR_DEFINITION",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "WOP4508_1_gamma_product",
            "object": "Gamma_eff=L_cg^-2 F",
            "formula": "W_g[Gamma_eff] = -2 L_cg^-3 F W_g[L_cg] + L_cg^-2 W_g[F] + W_boundary/domain",
            "result": "Theta_W splits into Lcg-chain, F-metric, and boundary/domain pieces",
            "status": "DERIVED_PRODUCT_RULE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "WOP4508_2_memory_derivative",
            "object": "Theta_W,m at m_L",
            "formula": "Theta_W,m = -2 L_cg^-3(F_m W_L + F W_L,m) + L_cg^-2 W_F,m + W_boundary,m + W_domain,m",
            "result": "826 F_m=0 kills only the first Lcg-chain term; F W_L,m and W_F,m can survive",
            "status": "DERIVED_TAIL_FORMULA",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "WOP4508_3_BWeyl_relation",
            "object": "B_Weyl component of B_mem_eff",
            "formula": "B_Weyl := -1/4 Theta_W,m",
            "result": "the 4507 finite Bmem row now has a concrete first component",
            "status": "FINITE_COMPONENT_DEFINED",
            "valid_for_claim": False,
        },
    ]


def theta_decomp_rows() -> List[Dict[str, object]]:
    return [
        {
            "component_id": "TW4508_0_Fm_WL",
            "component": "-2 L^-3 F_m W_L",
            "zero_route": "826 branch extremum F_m=0",
            "current_status": "CONDITIONAL_ZERO_FROM_826",
            "finite_input_if_live": "F_m;L_cg;W_L",
            "valid_for_claim": False,
        },
        {
            "component_id": "TW4508_1_F_WLm",
            "component": "-2 L^-3 F W_L,m",
            "zero_route": "source-root F(m_L)=0 or Lcg metric-silence W_L,m=0",
            "current_status": "BEST_ZERO_ROUTE_UNSIGNED",
            "finite_input_if_live": "F(m_L);partial_m W_g[L_cg]",
            "valid_for_claim": False,
        },
        {
            "component_id": "TW4508_2_WFm",
            "component": "L^-2 W_F,m",
            "zero_route": "metric/epsilon-only one-Weyl index theorem plus no Weyl spurion/projector/readout grammar",
            "current_status": "INDEX_LEMMA_DERIVED_PARENT_GRAMMAR_UNSIGNED",
            "finite_input_if_live": "B_qWeyl;G_q;C_Weyl;arena projection",
            "valid_for_claim": False,
        },
        {
            "component_id": "TW4508_3_boundary_domain",
            "component": "W_boundary,m + W_domain,m",
            "zero_route": "fixed boundary class, variation-before-readout, no source/reference flux",
            "current_status": "UNSIGNED_RETAINED_TAIL",
            "finite_input_if_live": "boundary flux coefficient;domain motion coefficient;readout source path",
            "valid_for_claim": False,
        },
        {
            "component_id": "TW4508_4_Khat_match",
            "component": "Khat trace-assignment mismatch",
            "zero_route": "K_hat=K_metric[Gamma_eff] with one sign/volume convention and tracefree residual",
            "current_status": "MATCH_MISSING_CURRENT_CORPUS",
            "finite_input_if_live": "R_K trace norm and memory derivative",
            "valid_for_claim": False,
        },
    ]


def zero_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "ZG4508_0_source_root",
            "zero_claim": "F(m_L)=0 and F_m(m_L)=0 kill Lcg chain response",
            "mathematical_condition": "F=0 removes F W_L,m; F_m=0 removes F_m W_L",
            "status": "EXACT_ZERO_IF_PARENT_LOCKED",
            "missing_signature": "same-branch source-root/double-zero lock, no fitted per-system root",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ZG4508_1_no_spurion",
            "zero_claim": "linear Weyl part of W_F,m vanishes",
            "mathematical_condition": "metric/epsilon-only one-Weyl scalar is zero; nonzero linear Weyl requires P^{abcd}C_abcd spurion",
            "status": "INDEX_THEOREM_DERIVED_PARENT_GRAMMAR_UNSIGNED",
            "missing_signature": "typed parent grammar excluding Weyl spurions/projectors/readout kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ZG4508_2_Khat_metric",
            "zero_claim": "trace assignment tail vanishes",
            "mathematical_condition": "K_hat=K_metric[Gamma_eff] and residual R_K has zero trace derivative",
            "status": "NOT_MATCHED",
            "missing_signature": "global parent Khat metric-response convention and tensor match",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ZG4508_3_combined",
            "zero_claim": "Theta_W,m=0",
            "mathematical_condition": "ZG4508_0, ZG4508_1, ZG4508_2 plus boundary/domain/readout silence all hold in one branch",
            "status": "COMBINED_THEOREM_NOT_CLAIMED",
            "missing_signature": "all component zeros together, with no cancellation credit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_bound_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BW4508_0_total",
            "symbol": "B_Weyl",
            "formula": "|B_Weyl| <= 1/4[2 L^-3(|F_m||W_L|+|F||W_L,m|)+L^-2|W_F,m|+|W_boundary,m|+|W_domain,m|+|R_K_trace,m|]",
            "units": "same as B_mem_eff",
            "required_inputs": "L_cg;F;F_m;W_L;W_L,m;W_F,m;boundary/domain/readout/Khat trace norms;source paths",
            "body_charge_use": "B_mem_eff = B_826 + B_Weyl + B_Y5 + B_Y6 + B_boundary + B_readout; then use 4506 Q_mem row",
            "status": "NONCLAIM_BOUND_ROW_STAGED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BW4508_1_simplified_if_source_root",
            "symbol": "B_Weyl_source_root_branch",
            "formula": "if F=F_m=0, |B_Weyl| <= 1/4[L^-2|W_F,m|+|W_boundary,m|+|W_domain,m|+|R_K_trace,m|]",
            "units": "same as B_mem_eff",
            "required_inputs": "parent source-root; no-spurion or finite W_F,m; boundary/domain/Khat rows",
            "body_charge_use": "preferred finite branch if source-root is parent-signed before no-spurion theorem closes",
            "status": "REDUCED_BOUND_TEMPLATE_NOT_SCORE_READY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BW4508_2_linear_Weyl_fallback",
            "symbol": "B_qWeyl",
            "formula": "E_BqWeyl[arena] <= tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl|| plus boundary/source tails",
            "units": "q source vector norm / arena declared",
            "required_inputs": "B_qWeyl;G_q;C_Weyl profile;tau_R10;tau_PPN;tau_clock;tau_orbital;units",
            "body_charge_use": "fallback if no-spurion grammar fails",
            "status": "IMPORT_3606_BOUND_LAW_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4508_0_derivation",
            "claim": "Theta_W,m formula derived",
            "status": "DERIVED_PRODUCT_RULE",
            "effect": "the Weyl tail is decomposed into source-root, no-spurion, Khat-match, and boundary/domain gates",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4508_1_source_root",
            "claim": "source-root/double-zero is live",
            "status": "UNSIGNED",
            "effect": "cannot yet kill F W_L,m in public/local claim",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4508_2_no_spurion",
            "claim": "linear Weyl spurion excluded",
            "status": "INDEX_LEMMA_EXACT_GRAMMAR_UNSIGNED",
            "effect": "linear Weyl zero route exists but is not parent-promoted",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4508_3_Khat",
            "claim": "Khat metric-response trace is matched",
            "status": "MATCH_MISSING",
            "effect": "R_K_trace,m remains part of B_Weyl bound",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "CG4508_0_ThetaW_zero", "gate": "Theta_W,m=0", "derived_now": False, "blocked_by": "combined source-root/no-spurion/Khat/boundary signatures unsigned", "claim_allowed": False},
        {"gate_id": "CG4508_1_BWeyl_score", "gate": "B_Weyl finite bound score-ready", "derived_now": False, "blocked_by": "no numeric/source-backed component rows", "claim_allowed": False},
        {"gate_id": "CG4508_2_Bmem", "gate": "B_mem_eff cleared", "derived_now": False, "blocked_by": "B_Weyl plus Y5/Y6/boundary/readout tails live", "claim_allowed": False},
        {"gate_id": "CG4508_3_local_GR", "gate": "local GR/PPN/R10 promotion", "derived_now": False, "blocked_by": "memory/fibre source-charge and Khat gates still open", "claim_allowed": False},
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "Theta_W,m product-rule decomposition and B_Weyl finite bound law",
            "not_derived": "combined parent source-root, no-spurion grammar, Khat trace match, boundary/domain silence, numeric bound inputs",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4508_0",
            "target_file": NEXT_TARGET,
            "task": "try to close the combined source-root plus no-Weyl-spurion gate; if not, fill the first numeric/source-backed B_Weyl component row",
            "success_condition": "B_Weyl is theorem-zero in the parent grammar or becomes a finite, source-backed coefficient bound ready for the 4506 body-charge row",
            "do_not": "claim Theta_W,m zero from the one-Weyl index lemma unless the no-spurion/readout grammar is parent-signed",
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4508_0",
            "decision": DECISION,
            "because": "the Weyl trace tail is not one object; its Lcg, F-metric, Khat-match, boundary, and source/readout pieces have different zero routes",
            "effect": "the next fork is a real theorem gate: source-root plus no-spurion plus Khat trace match, or a finite B_Weyl bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_files = [
        SOURCE_REGISTER,
        WEYL_OPERATOR,
        THETAW_DECOMP,
        ZERO_GATE,
        FINITE_BOUND,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    parsed = True
    details: List[str] = []
    for path in csv_files:
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            parsed = False
            details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    nonclaim_ok = all(
        str(value).lower() != "true"
        for rows in all_rows.values()
        for row in rows
        for key, value in row.items()
        if key in {"valid_for_claim", "claim_allowed"}
    )
    product_rule_ok = any("Theta_W,m" in str(row.get("object", "")) and "F_m" in str(row.get("formula", "")) for row in all_rows["operator"])
    bound_ok = any(row.get("symbol") == "B_Weyl" for row in all_rows["finite"])
    no_claim = all(not bool(row.get("derived_now", False)) for row in all_rows["gates"])
    next_ok = all_rows["next"][0]["target_file"] == NEXT_TARGET
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4508_00_sources", source_ok, "all source paths exist and needles are found"),
        ("VAL4508_01_product_rule", product_rule_ok, "Theta_W,m product-rule formula recorded"),
        ("VAL4508_02_finite_bound", bound_ok, "B_Weyl finite bound row staged"),
        ("VAL4508_03_claims_blocked", no_claim, "all claim gates remain blocked"),
        ("VAL4508_04_nonclaim_flags", nonclaim_ok, "all generated claim flags remain false"),
        ("VAL4508_05_csv_parse", parsed, ";".join(details)),
        ("VAL4508_06_next_target", next_ok, NEXT_TARGET),
        ("VAL4508_07_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4508_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4508 memory Weyl response tail or Bmem finite bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = ",".join(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_memory_weyl_tail",
            '"4508 derives the Theta_W,m product-rule decomposition for the memory Weyl/metric-response trace tail and stages a finite B_Weyl bound. The clean zero route requires source-root/double-zero, no Weyl-spurion grammar, Khat trace match, and boundary/domain/readout silence in one parent branch."',
            '"4508 source register, Weyl operator derivation, ThetaW decomposition, zero gate, finite B_Weyl bound row, parent audit, claim gates, status and validation."',
            "private_ThetaWm_decomposition_BWeyl_bound_nonclaim",
            NEXT_TARGET,
            "using the one-Weyl index lemma alone as a full trace-response/local-GR proof.",
            "local_gr_newton_r2fr_memory_weyl_tail",
            str(FORMAL_PATH),
            NEXT_TARGET,
            '"close source-root plus no-spurion plus Khat trace match, or source the first B_Weyl finite component."',
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    operator: Sequence[Mapping[str, object]],
    decomp: Sequence[Mapping[str, object]],
    zero: Sequence[Mapping[str, object]],
    finite: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4508 - Memory Weyl Response Tail Or Bmem Finite Bound Row

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4508 turns `Theta_W,m` into an actual formula. For the unit Weyl generator `W_g` and

`Gamma_eff = L_cg^-2 F(m,X_B,...)`,

the trace-response tail obeys

`Theta_W,m = -2 L_cg^-3(F_m W_L + F W_L,m) + L_cg^-2 W_F,m + W_boundary,m + W_domain,m`.

So the 826 branch extremum `F_m=0` only kills the first term. The remaining clean route is stronger and sharper: source-root/double-zero kills the `F W_L,m` term, the one-Weyl index theorem plus a no-spurion parent grammar kills the linear Weyl part of `W_F,m`, and Khat metric-response ownership must kill the trace-assignment mismatch. If those are not all parent-signed together, the fallback is a finite `B_Weyl=-Theta_W,m/4` bound.

This is still private/nonclaim: no local-GR, PPN, R10, clock, orbital, or EM claim fires.

## Source Register

{table(sources)}

## Weyl Operator Derivation

{table(operator)}

## ThetaWm Decomposition

{table(decomp)}

## ThetaWm Zero Gate

{table(zero)}

## B_Weyl Finite Bound Row

{table(finite)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    operator = weyl_operator_rows()
    decomp = theta_decomp_rows()
    zero = zero_gate_rows()
    finite = finite_bound_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    next_target = next_rows()
    decisions = decision_rows()

    all_rows = {
        "sources": sources,
        "operator": operator,
        "decomp": decomp,
        "zero": zero,
        "finite": finite,
        "parent": parent,
        "gates": gates,
        "status": status,
        "next": next_target,
        "decisions": decisions,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(WEYL_OPERATOR, operator)
    write_csv(THETAW_DECOMP, decomp)
    write_csv(ZERO_GATE, zero)
    write_csv(FINITE_BOUND, finite)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, operator, decomp, zero, finite, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4508 Memory Weyl Response Tail Or Bmem Finite Bound Row

Marker: `{MARKER}`  
4508 derives the product-rule decomposition of `Theta_W,m`. The 826 branch extremum kills only `F_m W_L`; source-root/double-zero is needed for `F W_L,m`; no-Weyl-spurion grammar is needed for the linear Weyl part of `W_F,m`; and Khat metric-response ownership is needed for the trace-assignment tail. Otherwise `B_Weyl=-Theta_W,m/4` enters the finite `B_mem_eff` body-charge row.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4508 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now has the exact Weyl-tail fork: close source-root plus no-spurion plus Khat trace-match in one parent branch, or source the finite `B_Weyl` bound before any local-GR/PPN/R10 scoring.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
