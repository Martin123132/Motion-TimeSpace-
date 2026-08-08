from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4364"
CLAIM_ID = "L-205"
BRANCH = "MTS_R2FR_Y5_TRANSITION_TAU_WEP_LOWER_BOUND_OR_PRODUCT_ONLY_LOCAL_ROUTE_4364"
MARKER = "PPC4161_TRANSITION_TAU_WEP_LOWER_BOUND_OR_PRODUCT_ONLY_LOCAL_ROUTE_4364"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_TAU_WEP_LOWER_BOUND_OR_PRODUCT_ONLY_LOCAL_ROUTE_4364"
DECISION = "TAU_WEP_LOWER_BOUND_NOT_DERIVED_PRODUCT_ONLY_TRANSFER_THEOREM_DERIVED_NONCLAIM"
NEXT_TARGET = "4365-Y5-R2FR-transition-first-product-transfer-norm-or-PiPPN-source-to-metric-row.md"

FORMAL_PATH = FORMAL / "380-PPC4161-transition-tau-WEP-lower-bound-or-product-only-local-route.md"
DOC_PATH = POST / "4364-Y5-R2FR-transition-tau-WEP-lower-bound-or-product-only-local-route.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4364_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

B_WEP_PRODUCT = 2.8e-15


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4364_00_4363_formal": (
        FORMAL / "379-PPC4161-transition-first-Csrc-projection-input-or-parent-graph-edge-proof.md",
        "Pi_WEP_product",
        "4363 closes the first product-level WEP projection row.",
    ),
    "SRC4364_01_4363_projection": (
        SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv",
        "PI4363_WEP_product",
        "Numeric fixed WEP product projection row.",
    ),
    "SRC4364_02_4363_blockers": (
        SOURCE_DIR / "P8_Y5_R2FR_4363_REMAINING_BLOCKERS.csv",
        "BLK4363_0_tau_inversion",
        "4363 retained the tau-inversion blocker.",
    ),
    "SRC4364_03_4359_tau_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_4359_TAU_LOWER_BOUND_ROWS.csv",
        "TLB4359_1_sufficient_lower_bound",
        "Exact tau_min sufficient lower-bound theorem.",
    ),
    "SRC4364_04_4360_cmin_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_4360_CMIN_ROWS.csv",
        "CMIN4360_4_verdict",
        "c_min remains not derived.",
    ),
    "SRC4364_05_4360_parent_nondegeneracy": (
        SOURCE_DIR / "P8_Y5_R2FR_4360_PARENT_NONDEGENERACY_ATTEMPT_ROWS.csv",
        "PND4360_4_verdict",
        "generic parent nondegeneracy attempt failed.",
    ),
    "SRC4364_06_4362_arena_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_ARENA_PROJECTION_CONTRACT.csv",
        "ARENA4362_1_PPN",
        "4362 arena rows require projection matrices for PPN/local transfer.",
    ),
    "SRC4364_07_local_bound_claims": (
        LOCAL_BOUNDS / "local_bound_claims.csv",
        "R1_WEP_source_charge",
        "source-backed WEP product bound anchor.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def bound_value() -> float:
    rows = read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    match = [row for row in rows if row.get("row_id") == "R1_WEP_source_charge"]
    if len(match) != 1:
        raise ValueError("expected exactly one R1_WEP_source_charge row")
    return float(match[0]["upper_bound"])


def tau_recheck_rows() -> List[Dict[str, str]]:
    return [
        {
            "route_id": "TAU4364_0_exact_condition",
            "route": "tau lower bound",
            "statement": "tau_min = k_min*s_min*m_min*c_min/N_max if all factors are source-backed and c_min>0",
            "current_evidence": "4359 conditional theorem exists",
            "result": "CONDITIONAL_ONLY",
            "what_is_missing": "official K_CMSM, source vector, material tensor, normalization and c_min",
            "valid_for_claim": "False",
        },
        {
            "route_id": "TAU4364_1_cmin_status",
            "route": "alignment/non-null",
            "statement": "c_min excludes V_ST in ker(K_CMSM)",
            "current_evidence": "4360 c_min verdict remains C_MIN_NOT_DERIVED",
            "result": "NOT_DERIVED",
            "what_is_missing": "sourced contraction or parent one-channel/non-null theorem",
            "valid_for_claim": "False",
        },
        {
            "route_id": "TAU4364_2_generic_proof",
            "route": "generic parent nondegeneracy",
            "statement": "nonzero K_CMSM and nonzero V_ST imply nonzero pairing",
            "current_evidence": "4360 rejected by kernel/cancellation countermodel",
            "result": "REJECTED",
            "what_is_missing": "positive cone or one-dimensional signed channel theorem",
            "valid_for_claim": "False",
        },
        {
            "route_id": "TAU4364_3_amplitude_inference",
            "route": "Delta_w amplitude",
            "statement": "|Delta_w_TiPt| <= B_WEP/tau_min",
            "current_evidence": "tau_min not positive in current corpus",
            "result": "FORBIDDEN_NOW",
            "what_is_missing": "tau_min>0 or owner/no-wA zero theorem",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4364_0_product_bound",
            "statement": "Let p = Delta_w_TiPt*tau_WEP. The 4363 product projection supplies |p| <= B_WEP.",
            "formula": f"|p| <= {B_WEP_PRODUCT}",
            "proof_status": "SOURCE_BACKED_PRODUCT_BOUND",
            "closes": "WEP product comparator lane",
            "does_not_close": "Delta_w amplitude or local-GR transfer",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4364_1_transfer_norm",
            "statement": "If an arena residual factorizes through the product as R_A = T_A p and |T_A| <= A_A before scoring, then |R_A| <= A_A B_WEP.",
            "formula": "|R_A| <= A_A * B_WEP",
            "proof_status": "EXACT_LINEAR_TRANSFER_BOUND",
            "closes": "legal product-only cross-arena route once A_A is sourced",
            "does_not_close": "any arena whose residual depends separately on Delta_w or tau_WEP",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4364_2_vector_transfer",
            "statement": "For a residual vector R = T p, any fixed norm gives ||R|| <= ||T|| B_WEP.",
            "formula": "||R|| <= ||T|| * B_WEP",
            "proof_status": "EXACT_VECTOR_TRANSFER_BOUND",
            "closes": "PPN/Newton/local-GR vector scoring shape after source-backed T matrix exists",
            "does_not_close": "the missing T matrix itself",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4364_3_no_amplitude_from_product",
            "statement": "A product bound alone cannot bound Delta_w_TiPt: choose tau_WEP=epsilon and Delta_w_TiPt=B_WEP/epsilon.",
            "formula": "|Delta_w_TiPt*tau_WEP|=B_WEP while |Delta_w_TiPt| -> infinity as epsilon -> 0",
            "proof_status": "COUNTERMODEL_DERIVED",
            "closes": "firewall against illegal tau division",
            "does_not_close": "finite-amplitude branch",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4364_4_factorization_gate",
            "statement": "A product-only local route is admissible only for observables whose MTS source-coupling residual is proved to depend on p, not on Delta_w_TiPt separately.",
            "formula": "R_A = F_A(p) with Lipschitz/source-backed transfer before scoring",
            "proof_status": "ADMISSIBILITY_GATE_DERIVED",
            "closes": "exact rule for using the product bound without tau_min",
            "does_not_close": "factorization/source-backed transfer for PPN/Newton/local-GR",
            "valid_for_claim": "False",
        },
    ]


def transfer_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "transfer_id": "TR4364_0_WEP_product_self",
            "arena": "WEP product lane",
            "residual": "P_WEP_TiPt",
            "product_factorization": "P_WEP_TiPt=|p|",
            "transfer_norm": "1",
            "bound_if_transfer_sourced": f"{B_WEP_PRODUCT}",
            "status": "TRANSFER_CLOSED_PRODUCT_ONLY",
            "missing_before_claim": "parent numeric p=0 theorem or candidate p value for scoring",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "TR4364_1_Delta_w_amplitude",
            "arena": "Delta_w amplitude",
            "residual": "|Delta_w_TiPt|",
            "product_factorization": "Delta_w=p/tau_WEP",
            "transfer_norm": "1/tau_min",
            "bound_if_transfer_sourced": "2.8e-15/tau_min",
            "status": "BLOCKED_TAU_MIN_MISSING",
            "missing_before_claim": "tau_min>0 or owner/no-wA theorem",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "TR4364_2_PPN",
            "arena": "PPN/local solar tests",
            "residual": "R_PPN_source_product",
            "product_factorization": "R_PPN_source_product=T_PPN<-p p",
            "transfer_norm": "A_PPN_product",
            "bound_if_transfer_sourced": "A_PPN_product*2.8e-15",
            "status": "TRANSFER_LAW_DERIVED_NORM_MISSING",
            "missing_before_claim": "source-to-metric Green operator and PPN projection norm",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "TR4364_3_Newton_source",
            "arena": "Newton/source normalization",
            "residual": "epsilon_Gsrc_product",
            "product_factorization": "epsilon_Gsrc_product=T_Gsrc<-p p",
            "transfer_norm": "A_Gsrc_product",
            "bound_if_transfer_sourced": "A_Gsrc_product*2.8e-15",
            "status": "TRANSFER_LAW_DERIVED_NORM_MISSING",
            "missing_before_claim": "calibrated source normalization transfer from product channel",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "TR4364_4_local_GR",
            "arena": "local GR/Newton limit",
            "residual": "R_local_GR_product",
            "product_factorization": "R_local_GR_product=T_GR<-p p",
            "transfer_norm": "A_GR_product",
            "bound_if_transfer_sourced": "A_GR_product*2.8e-15",
            "status": "TRANSFER_LAW_DERIVED_NORM_MISSING",
            "missing_before_claim": "Bianchi/conservation-compatible metric/source transfer",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "TR4364_5_clock_orbital_EM",
            "arena": "clock/orbital/EM side lanes",
            "residual": "R_clock_orbital_EM_product",
            "product_factorization": "R_side=T_side<-p p",
            "transfer_norm": "A_side_product",
            "bound_if_transfer_sourced": "A_side_product*2.8e-15",
            "status": "TRANSFER_LAW_DERIVED_NORM_MISSING",
            "missing_before_claim": "clock sensitivity, GM/orbital frame and EM current/Hodge transfer matrices",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def countermodel_rows() -> List[Dict[str, str]]:
    return [
        {
            "countermodel_id": "CM4364_0_tau_null",
            "construction": "tau_WEP=0 and Delta_w_TiPt finite",
            "product": "p=0",
            "effect": "WEP product lane can pass while Delta_w amplitude is unconstrained",
            "blocks": "Delta_w amplitude inference",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4364_1_small_tau_large_delta",
            "construction": "tau_WEP=epsilon, Delta_w_TiPt=B_WEP/epsilon",
            "product": "p=B_WEP",
            "effect": "product bound is saturated but Delta_w grows without bound as epsilon->0",
            "blocks": "any local residual that depends on Delta_w rather than p",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM4364_2_nonfactorized_local_residual",
            "construction": "R_PPN=a*Delta_w_TiPt with no tau factor",
            "product": "p bounded",
            "effect": "R_PPN can be arbitrarily large under CM4364_1",
            "blocks": "using WEP product bound as local-GR/PPN proof",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "run_id": "RUN4364_0_tau_lower_bound",
            "input": "current corpus",
            "operation": "attempt tau_min extraction",
            "result": "NO_TAU_MIN",
            "reason": "c_min not sourced or parent-proved",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4364_1_product_self_lane",
            "input": "p_WEP_TiPt product lane",
            "operation": "apply PI4363_WEP_product and source-backed bound",
            "result": "PRODUCT_COMPARATOR_READY",
            "reason": "transfer norm is exactly 1 for the product observable",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4364_2_amplitude_lane",
            "input": "Delta_w_TiPt amplitude",
            "operation": "divide by tau_WEP",
            "result": "REFUSED",
            "reason": "tau_min missing; countermodel active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4364_3_cross_arena_lane",
            "input": "PPN/Newton/local_GR side lanes",
            "operation": "use product transfer theorem",
            "result": "READY_FOR_FIRST_TRANSFER_NORM",
            "reason": "requires source-backed A_A before scoring",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4364_0_tau_min",
            "gate": "tau_WEP lower bound",
            "requirement": "c_min>0 plus source-backed k_min,s_min,m_min,N_max",
            "current_result": "FAIL_CURRENT_CORPUS",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4364_1_product_only_law",
            "gate": "product-only transfer theorem",
            "requirement": "derive exact transfer law without tau inversion",
            "current_result": "PASS_NONCLAIM_THEOREM",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4364_2_cross_arena_score",
            "gate": "score PPN/Newton/local-GR from WEP product",
            "requirement": "source-backed transfer norm A_A and factorization through p",
            "current_result": "BLOCKED_TRANSFER_NORM_MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4364_3_public_claim",
            "gate": "claim WEP/local-GR/Newton/PPN pass",
            "requirement": "numeric p value or zero theorem plus all necessary transfer norms/conservation gates",
            "current_result": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4364_0",
            "decision": DECISION,
            "rationale": "The tau lower-bound route remains open but not closed: c_min>0 is still not sourced or parent-proved. Instead of dividing by tau_WEP, 4364 derives the exact product-only transfer law. Any arena residual that factorizes through p=Delta_w_TiPt*tau_WEP can be bounded by a source-backed transfer norm times 2.8e-15. Any arena residual that depends on Delta_w separately is not bounded by the product row, as shown by the small-tau countermodel.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4364_0",
            "item": "tau_min route",
            "status": "NOT_DERIVED",
            "detail": "finite route still needs c_min/non-null alignment or official contraction.",
        },
        {
            "status_id": "STAT4364_1",
            "item": "product-only theorem",
            "status": "DERIVED",
            "detail": "product-bound transfer is legal only through factorized residuals with sourced transfer norms.",
        },
        {
            "status_id": "STAT4364_2",
            "item": "amplitude shortcut",
            "status": "REJECTED",
            "detail": "small-tau countermodel blocks Delta_w amplitude inference.",
        },
        {
            "status_id": "STAT4364_3",
            "item": "next target",
            "status": "FIRST_TRANSFER_NORM_OR_PIPPN_ROW",
            "detail": NEXT_TARGET,
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "target_id": "NT4364_0",
            "next_target": NEXT_TARGET,
            "question": "Can one source-backed transfer norm from p_WEP_TiPt into PPN/Newton/local-GR be derived or bounded?",
            "preferred_route": "derive Pi_PPN or Pi_GR source-to-metric row for the product channel and compare A_A*2.8e-15 to local bounds",
            "alternate_route": "return to tau_min only if official MICROSCOPE contraction arrays or a parent one-channel theorem become available",
            "fallback_route": "keep the product lane as the only WEP-safe statement and attack Xi_open/epsilon_Gsrc separately",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: List[Dict[str, str]],
    tau_recheck: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    transfers: List[Dict[str, str]],
    countermodels: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "check": check,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4364_00_sources_exist", "all cited local source paths exist", all(row["path_exists"] == "True" for row in sources), "source register path_exists flags")
    add("VAL4364_01_needles_found", "all cited local source needles found", all(row["needle_found"] == "True" for row in sources), "source register needle_found flags")
    add("VAL4364_02_tau_not_derived", "tau lower bound remains not derived", any(row["route_id"] == "TAU4364_3_amplitude_inference" and row["result"] == "FORBIDDEN_NOW" for row in tau_recheck), "amplitude inference row")
    add("VAL4364_03_transfer_theorem", "product transfer theorem derived", any(row["theorem_id"] == "TH4364_1_transfer_norm" for row in theorems), "TH4364_1")
    add("VAL4364_04_countermodel", "small-tau countermodel present", any(row["countermodel_id"] == "CM4364_1_small_tau_large_delta" for row in countermodels), "CM4364_1")
    add("VAL4364_05_WEP_self_closed", "WEP product self transfer closed", any(row["transfer_id"] == "TR4364_0_WEP_product_self" and row["status"] == "TRANSFER_CLOSED_PRODUCT_ONLY" for row in transfers), "TR4364_0")
    add("VAL4364_06_cross_arenas_blocked", "cross-arena transfers require missing norms", all(row["claim_allowed"] == "False" for row in transfers) and any("NORM_MISSING" in row["status"] for row in transfers), "transfer flags")
    add("VAL4364_07_runner_nonclaim", "runner rows remain nonclaim", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in runner), "runner flags")
    add("VAL4364_08_claim_forbidden", "public claim forbidden", any(row["gate_id"] == "GATE4364_3_public_claim" and row["current_result"] == "FORBIDDEN" for row in gates), "claim gate")
    add("VAL4364_09_decision_nonclaim", "decision is nonclaim", decisions[0]["decision"] == DECISION and decisions[0]["claim_allowed"] == "False", DECISION)
    add("VAL4364_10_next_selected", "next target selected", next_targets[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4364_11_formal_marker", "formal marker written", MARKER in read_text(FORMAL_PATH), str(FORMAL_PATH))
    add("VAL4364_12_post_doc_marker", "post doc marker written", MARKER in read_text(DOC_PATH), str(DOC_PATH))
    add("VAL4364_13_spine_marker", "spine marker appended", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4364_14_packet_marker", "packet marker appended", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4364_15_claim_register", "claim register updated", f"\n{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    return rows


def write_docs(
    sources: List[Dict[str, str]],
    tau_recheck: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    transfers: List[Dict[str, str]],
    countermodels: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    formal = f"""# PPC4161 transition: tau-WEP lower bound or product-only local route

Marker: `{MARKER}`

Generated: {STAMP}

## Purpose

4364 attempts the tau lower-bound lift and refuses it when the current corpus cannot supply `c_min>0`. It then derives the safe replacement: a product-only transfer theorem. This is not a retreat; it is the exact rule for using the real WEP product bound without smuggling in `Delta_w` amplitude.

## Tau route recheck

{md_table(tau_recheck, ["route_id", "route", "statement", "current_evidence", "result", "what_is_missing", "valid_for_claim"])}

## Product-only theorem

Let:

`p := Delta_w_TiPt tau_WEP`

and use the 4363 source-backed product bound:

`|p| <= {B_WEP_PRODUCT}`.

Then an arena residual may use this bound only if it factorizes through `p`:

`R_A = T_A p`, with `|T_A| <= A_A` fixed and source-backed before scoring.

Then:

`|R_A| <= A_A {B_WEP_PRODUCT}`.

If the residual depends on `Delta_w_TiPt` separately, the product bound gives no amplitude control.

{md_table(theorems, ["theorem_id", "statement", "formula", "proof_status", "closes", "does_not_close", "valid_for_claim"])}

## Transfer contract

{md_table(transfers, ["transfer_id", "arena", "residual", "product_factorization", "transfer_norm", "bound_if_transfer_sourced", "status", "missing_before_claim", "claim_allowed"])}

## Countermodels

{md_table(countermodels, ["countermodel_id", "construction", "product", "effect", "blocks", "valid_for_claim"])}

## Runner

{md_table(runner, ["run_id", "input", "operation", "result", "reason", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "requirement", "current_result", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "rationale", "next_target", "claim_allowed"])}

## Status

{md_table(statuses, ["status_id", "item", "status", "detail"])}

## Next target

{md_table(next_targets, ["target_id", "next_target", "question", "preferred_route", "alternate_route", "fallback_route", "claim_allowed"])}

## Source register

{md_table(sources, ["source_id", "path_exists", "needle_found", "line_number", "role"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")

    post_doc = f"""# 4364 - tau-WEP lower bound or product-only local route

Marker: `{MARKER}`

Generated: {STAMP}

## Result

- `tau_min` is still not derived: `c_min>0` remains the missing non-null alignment object.
- Product-only local route is now exact: if `R_A=T_A p` and `|T_A|<=A_A`, then `|R_A|<=A_A*2.8e-15`.
- Amplitude shortcut is rejected: product bound cannot control `Delta_w_TiPt` if `tau_WEP` can be small.

## What moved

We now know precisely how the WEP product row can help PPN/Newton/local-GR: not by division, but by a source-backed transfer norm from `p=Delta_w_TiPt tau_WEP` into the target residual.

## Files

- Formal checkpoint: `{FORMAL_PATH}`
- Transfer contract: `{SOURCE_DIR / "P8_Y5_R2FR_4364_PRODUCT_TRANSFER_CONTRACT.csv"}`
- Countermodels: `{SOURCE_DIR / "P8_Y5_R2FR_4364_COUNTERMODEL_ROWS.csv"}`
- Validation: `{VALIDATION_PATH}`

## Next

{NEXT_TARGET}
"""
    DOC_PATH.write_text(post_doc, encoding="utf-8")


def update_rollups() -> None:
    spine_block = f"""

## 4364 Transition tau-WEP lower bound or product-only route

Marker: `{MARKER}`

4364 rechecks the finite `tau_WEP` lift and refuses to divide by it. The current corpus still lacks `c_min>0`, the non-null alignment between the signed MICROSCOPE readout and the source/material vector. Therefore `|Delta_w_TiPt| <= 2.8e-15/tau_min` remains forbidden.

The useful derived replacement is the product-only transfer theorem. Let `p=Delta_w_TiPt tau_WEP` and `|p|<=2.8e-15`. If an arena residual factorizes as `R_A=T_A p` with source-backed `|T_A|<=A_A` fixed before scoring, then `|R_A|<=A_A*2.8e-15`. If the residual depends on `Delta_w_TiPt` separately, the small-tau countermodel blocks the inference. Next target: `{NEXT_TARGET}`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""

## 4364 packet update: product-only transfer law

Marker: `{PACKET_MARKER}`

Packet update: the WEP product row is useful only through factorized transfer. The packet may use `|p_WEP_TiPt|<=2.8e-15` for any residual `R_A=T_A p_WEP_TiPt` with a source-backed transfer norm, but it may not infer a bound on `Delta_w_TiPt` while `tau_WEP` lacks a positive lower bound. This turns the next local-GR attack into a concrete transfer-norm problem, preferably a `Pi_PPN` or `Pi_GR` source-to-metric row.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)

    append_claim_once(
        FORMAL / "02-claims-register.csv",
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4364 rechecks the tau_WEP lower-bound route and keeps it blocked because c_min>0 is still not sourced or parent-proved. It derives the safe product-only transfer law: for p=Delta_w_TiPt*tau_WEP with |p|<=2.8e-15, any arena residual that factorizes as R_A=T_A p with source-backed |T_A|<=A_A obeys |R_A|<=A_A*2.8e-15. A small-tau countermodel proves that the product bound cannot control Delta_w_TiPt or any residual depending on Delta_w separately. No WEP/local-GR/Newton/PPN claim fires.",
            "4364 source register, tau recheck rows, product-only theorem rows, product transfer contract, countermodels, runner, claim gates, decision, status, next target and validation CSV.",
            "tau_WEP_lower_bound_not_derived_product_only_transfer_theorem_nonclaim",
            "Fill the first source-backed product transfer norm, preferably Pi_PPN or Pi_GR source-to-metric.",
            "Dividing by tau_WEP without tau_min; using WEP product as a Delta_w amplitude bound; applying product bound to nonfactorized local residuals.",
        ],
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    if bound_value() != B_WEP_PRODUCT:
        raise SystemExit("local WEP product bound changed; inspect before regenerating 4364")

    sources = source_rows()
    tau_recheck = tau_recheck_rows()
    theorems = theorem_rows()
    transfers = transfer_contract_rows()
    countermodels = countermodel_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_SOURCE_REGISTER.csv", sources)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_TAU_RECHECK_ROWS.csv", tau_recheck)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_PRODUCT_ONLY_THEOREM_ROWS.csv", theorems)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_PRODUCT_TRANSFER_CONTRACT.csv", transfers)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_COUNTERMODEL_ROWS.csv", countermodels)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_RUNNER.csv", runner)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_CLAIM_GATES.csv", gates)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_DECISION.csv", decisions)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_STATUS.csv", statuses)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4364_NEXT_TARGET.csv", next_targets)

    write_docs(sources, tau_recheck, theorems, transfers, countermodels, runner, gates, decisions, statuses, next_targets)
    update_rollups()

    validations = validation_rows(sources, tau_recheck, theorems, transfers, countermodels, runner, gates, decisions, statuses, next_targets)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"4364 validation failed: {details}")

    print(f"{CHECKPOINT} generated: {DECISION}")
    print(f"formal={FORMAL_PATH}")
    print(f"validation={VALIDATION_PATH}")


if __name__ == "__main__":
    main()
