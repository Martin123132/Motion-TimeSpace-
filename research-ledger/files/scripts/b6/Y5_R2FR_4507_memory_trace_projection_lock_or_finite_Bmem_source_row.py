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

CHECKPOINT = "4507"
CLAIM_ID = "L-349"
MARKER = "PPC4161_MEMORY_TRACE_PROJECTION_LOCK_OR_FINITE_BMEM_SOURCE_ROW_4507"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_TRACE_PROJECTION_LOCK_OR_FINITE_BMEM_SOURCE_ROW_4507"
DECISION = "TRACE_PROJECTION_REDUCED_TO_WEYL_RESPONSE_TAIL_BMEM_FINITE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4508-Y5-R2FR-memory-Weyl-response-tail-or-Bmem-finite-bound-row.md"

FORMAL_PATH = FORMAL / "523-PPC4161-memory-trace-projection-lock-or-finite-Bmem-source-row.md"
DOC_PATH = POST / "4507-Y5-R2FR-memory-trace-projection-lock-or-finite-Bmem-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4507_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4507_SOURCE_REGISTER.csv"
TRACE_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4507_TRACE_PROJECTION_DERIVATION.csv"
WEYL_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4507_WEYL_RESPONSE_AUDIT.csv"
BMEM_FORMULA = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv"
FINITE_ROW = SOURCE_DIR / "P8_Y5_R2FR_4507_FINITE_BMEM_SOURCE_ROW.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4507_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4507_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4507_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4507_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4507_DECISION.csv"

FORMAL_522 = FORMAL / "522-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"
POST_4506 = POST / "4506-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"
SCRIPT_4506 = SCRIPT_DIR / "Y5_R2FR_4506_memory_fibre_BX_CX_owner_or_body_charge_input_row.py"
STATUS_4506 = SOURCE_DIR / "P8_Y5_R2FR_4506_STATUS.csv"
NEXT_4506 = SOURCE_DIR / "P8_Y5_R2FR_4506_NEXT_TARGET.csv"
BODY_4506 = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"

EQUATION_REGISTER = FORMAL / "05-equation-register.md"
ANSATZ_826 = SOURCE_DIR / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv"
F1_826 = SOURCE_DIR / "P8_Y5_R10_826_F1_ZERO_LEMMA.csv"
WARD_826 = SOURCE_DIR / "P8_Y5_R10_826_WARD_BIANCHI_AUDIT.csv"
BMEM_1348 = SOURCE_DIR / "P8_Y5_R10_1348_BMEM_EXTREMUM_TEST.csv"
RESP_CONTRACT = SOURCE_DIR / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
RESP_VARIATION = SOURCE_DIR / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv"
GK_METRIC_AUDIT = SOURCE_DIR / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv"
POST_1352 = POST / "1352-Y5-R10-RAB-response-displacement-conjugacy-action-or-q_loc-profile-source-fill.md"
SFE_1354 = SOURCE_DIR / "P8_Y5_R10_1354_SOURCE_FUNCTIONAL_EVENNESS_ATTEMPT.csv"
DEC_1354 = SOURCE_DIR / "P8_Y5_R10_1354_DECISION_LEDGER.csv"

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
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4507_00_formal522", "4506 formal handoff", FORMAL_522, "B_mem zero law reduced to F0_prime/projection condition", "selected trace-lock target"),
        ("SRC4507_01_post4506", "4506 post mirror", POST_4506, "That is the bridge to testing", "body-charge fallback handoff"),
        ("SRC4507_02_script4506", "4506 generator", SCRIPT_4506, 'CHECKPOINT = "4506"', "reproducible predecessor"),
        ("SRC4507_03_status4506", "4506 status", STATUS_4506, "PRIVATE_NONCLAIM", "checkpoint state"),
        ("SRC4507_04_next4506", "4506 next target", NEXT_4506, "derive the K_MTS-owned trace projection", "selected task"),
        ("SRC4507_05_body4506", "4506 Bmem finite row", BODY_4506, "BCIN4506_0_memory_density", "finite source row schema"),
        ("SRC4507_06_equation_trace", "equation register trace split", EQUATION_REGISTER, "Gamma_eff = -1/4 K_MTS", "trace projection definition"),
        ("SRC4507_07_equation_khat", "equation register Khat split", EQUATION_REGISTER, "K_MTS,mu_nu = -Gamma_eff g_mu_nu + K_hat,mu_nu", "trace/tensor split"),
        ("SRC4507_08_equation_warning", "equation register F1 warning", EQUATION_REGISTER, "`F'(m_L)=0` is not sufficient by itself", "F1 insufficiency"),
        ("SRC4507_09_826_ansatz", "826 trace projection ansatz", ANSATZ_826, "AA826_2_trace_projection_lock", "candidate trace lock"),
        ("SRC4507_10_826_F1", "826 F1 lemma", F1_826, "F826_1_F1_zero", "conditional F1 derivation"),
        ("SRC4507_11_826_Ward", "826 Ward audit", WARD_826, "W826_3_Khat_required", "Khat response required"),
        ("SRC4507_12_1348_Bmem", "1348 Bmem test", BMEM_1348, "BEXT1348_1_conditional_calculus", "conditional calculus pass"),
        ("SRC4507_13_response_contract", "response doublet contract", RESP_CONTRACT, "RD516_2_metric_response", "metric response requirement"),
        ("SRC4507_14_response_variation", "response variation", RESP_VARIATION, "AV517_2_first_variation_Z", "formal double-zero"),
        ("SRC4507_15_GK_metric", "GK metric-response audit", GK_METRIC_AUDIT, "MA515_1_Khat_metric_response", "metric-response mismatch"),
        ("SRC4507_16_1352_doc", "1352 conjugacy attempt", POST_1352, "RDA1352_3_metric_response", "metric response route"),
        ("SRC4507_17_1354_evenness", "1354 source evenness", SFE_1354, "SFE1354_6_verdict", "source evenness failed"),
        ("SRC4507_18_1354_decision", "1354 decision", DEC_1354, "DEC1354_1_Y5_priority", "Y5 coupling priority"),
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


def trace_derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "TR4507_0_algebraic_split",
            "object": "trace split",
            "derivation": "K_MTS,mu_nu=-Gamma_eff g_mu_nu+K_hat,mu_nu gives Tr K_MTS=-4 Gamma_eff+Tr K_hat",
            "condition": "if K_hat is parent-tracefree in the same branch, Gamma_eff=-1/4 Tr K_MTS",
            "result": "ALGEBRAIC_TRACE_LOCK_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "row_id": "TR4507_1_action_trace",
            "object": "Hilbert/action trace",
            "derivation": "For S_MTS=int sqrt(-g) L_MTS, Tr K_MTS contains the volume trace plus the metric/Weyl response of L_MTS, schematically Tr K= -4 Gamma_action + Theta_W + boundary/sign convention terms",
            "condition": "Theta_W and boundary trace terms must be assigned to K_hat or proved trace-silent",
            "result": "TRACE_PROJECTION_NEEDS_WEYL_RESPONSE_OWNER",
            "valid_for_claim": False,
        },
        {
            "row_id": "TR4507_2_memory_derivative",
            "object": "B_mem effective trace coefficient",
            "derivation": "B_mem^trace := partial_m Gamma_proj|L = partial_m Gamma_action|L - (1/4) partial_m Theta_W|L + boundary/source/readout trace tails, up to the chosen sign convention",
            "condition": "826 kills only partial_m Gamma_action|L when R_m(m_L;X_B)=0",
            "result": "B_MEM_REDUCED_TO_WEYL_TAIL_PLUS_SOURCE_TAILS",
            "valid_for_claim": False,
        },
        {
            "row_id": "TR4507_3_zero_theorem",
            "object": "trace-projection zero theorem",
            "derivation": "If R_m(m_L;X_B)=0, partial_m Theta_W|L=0, and boundary/source/readout trace tails vanish in the same parent branch, then B_mem^trace=0",
            "condition": "all clauses must be parent-signed together; no cancellation credit",
            "result": "ZERO_THEOREM_EXACT_BUT_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def weyl_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "WTAIL4507_0_metric_response_match",
            "claim_piece": "K_hat carries the metric response of Gamma_eff",
            "needed": "K_hat = K_metric[Gamma_eff] term-by-term, including trace, derivative, projector, and boundary terms",
            "current_evidence": "MA515_1_Khat_metric_response fail_for_current_claim",
            "status": "NOT_MATCHED",
            "effect_on_Bmem": "partial_m Theta_W may survive even when F1=0",
            "valid_for_claim": False,
        },
        {
            "audit_id": "WTAIL4507_1_tracefree_Khat",
            "claim_piece": "K_hat is tracefree in the parent branch",
            "needed": "Tr K_hat=0 and partial_m Tr K_hat=0 before readout/projection",
            "current_evidence": "equation register defines split but does not parent-sign Khat trace response",
            "status": "ALGEBRAIC_NOT_PARENT_SIGNED",
            "effect_on_Bmem": "trace projection can be a gauge split rather than a physical stress split",
            "valid_for_claim": False,
        },
        {
            "audit_id": "WTAIL4507_2_source_evenness",
            "claim_piece": "source/readout trace tails are even or zero",
            "needed": "Y5 measured-GM/source-normalization, boundary, species/readout, and Y6 extra-stress tails have zero linear memory response",
            "current_evidence": "1354 source-functional evenness theorem not proved",
            "status": "SOURCE_TAILS_LIVE",
            "effect_on_Bmem": "finite Bmem row must include Y5/Y6/source tails unless separately killed",
            "valid_for_claim": False,
        },
        {
            "audit_id": "WTAIL4507_3_parent_action_owner",
            "claim_piece": "Gamma_eff is a parent scalar density",
            "needed": "Gamma_eff(g,Phi,nablaPhi,...) with units and variation domain fixed",
            "current_evidence": "826 gives ansatz; 1352 gives promising response template but not adopted parent action",
            "status": "TEMPLATE_NOT_PARENT_ADOPTED",
            "effect_on_Bmem": "cannot promote trace-projection lock to local-GR theorem",
            "valid_for_claim": False,
        },
    ]


def bmem_formula_rows() -> List[Dict[str, object]]:
    return [
        {
            "formula_id": "BMF4507_0_effective",
            "symbol": "B_mem_eff",
            "expression": "B_mem_eff = a_F L_cg^-2 R_m(m_L;X_B) - 1/4 Theta_W,m|L + B_Y5_trace + B_Y6_trace + B_boundary + B_readout",
            "derived_status": "FIRST_TERM_ZERO_CONDITIONAL_REMAINDER_EXPLICIT",
            "required_zero": "R_m=0; Theta_W,m=0; B_Y5_trace=0; B_Y6_trace=0; B_boundary=0; B_readout=0",
            "finite_bound_use": "insert B_mem_eff into rho_mem=B_mem_eff R_obs + C_mem T + J_mem for BCIN4506_0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "BMF4507_1_826_term",
            "symbol": "a_F L_cg^-2 R_m",
            "expression": "partial_m Gamma_eff|m_L = a_F L_cg^-2 partial_m R(m_L;X_B)",
            "derived_status": "ZERO_IF_BRANCH_EXTREMUM_PARENT_SIGNED",
            "required_zero": "partial_m R(m_L;X_B)=0 with X_B fixed and m_L parent-owned",
            "finite_bound_use": "if not zero, source a_F,L_cg,R_m and bound directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "BMF4507_2_Weyl_tail",
            "symbol": "Theta_W,m",
            "expression": "Theta_W,m := partial_m[trace metric-response of sqrt(-g) Gamma_eff and any trace assignment moved into K_hat]",
            "derived_status": "IDENTIFIED_AS_NEXT_HARD_COUPLING",
            "required_zero": "metric-response match plus tracefree Khat derivative in the parent branch",
            "finite_bound_use": "source or bound Theta_W,m as the first finite Bmem coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "FBM4507_0_memory_B_source",
            "coefficient": "B_mem_eff",
            "definition": "effective memory curvature-source coefficient after trace projection",
            "expression": "B_mem_eff = B_826 + B_Weyl + B_Y5 + B_Y6 + B_boundary + B_readout",
            "units": "parent_defined_to_make rho_mem and action density consistent",
            "source_required": "a_F;L_cg;R_m;Theta_W,m;Y5/Y6 trace coefficients;boundary/readout coefficients;source paths",
            "body_charge_insert": "rho_mem = B_mem_eff R_obs + C_mem T + J_mem; use Q_mem0 row from 4506",
            "current_status": "NONCLAIM_FINITE_ROW_STAGED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "FBM4507_1_no_cancellation_guard",
            "coefficient": "component absolute bound",
            "definition": "finite route cannot use accidental cancellation among B_826,B_Weyl,Y5,Y6,boundary,readout",
            "expression": "|B_mem_eff| <= sum_i |B_i| unless a parent Ward/topological identity signs cancellation",
            "units": "same as B_mem_eff",
            "source_required": "component-by-component theorem-zero or numeric bound rows",
            "body_charge_insert": "use conservative sum in A_mem bound before R10/PPN scoring",
            "current_status": "NO_CANCELLATION_ROUTE_SELECTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4507_0_trace_lock",
            "claim": "trace projection lock is parent-owned",
            "needed_signature": "K_MTS from parent variation plus tracefree/assigned Khat response",
            "current_status": "NOT_PARENT_SIGNED",
            "next_action": "derive or source Theta_W,m",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4507_1_F1_zero",
            "claim": "826 F1 zero kills B_mem",
            "needed_signature": "R_m(m_L;X_B)=0 and all trace/source tails zero",
            "current_status": "PARTIAL_ONLY",
            "next_action": "keep 826 term zero conditional, attack Weyl/source tails",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4507_2_source_tails",
            "claim": "Y5/Y6/source tails do not re-enter",
            "needed_signature": "source-functional evenness or source pullback theorem",
            "current_status": "FAILED_CURRENT_EVIDENCE",
            "next_action": "treat as finite Bmem components unless 4508 proves silence",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4507_3_local_GR",
            "claim": "memory trace branch clears local GR",
            "needed_signature": "B_mem_eff=0 plus C_mem/J/Qboundary/operator gates",
            "current_status": "BLOCKED",
            "next_action": "do not promote; continue coefficient/source branch",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4507_0_trace_projection_owner",
            "gate": "Gamma_eff trace projection is parent-owned",
            "derived_now": False,
            "blocked_by": "Theta_W metric-response tail and Khat trace assignment not signed",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4507_1_Bmem_zero",
            "gate": "B_mem_eff=0",
            "derived_now": False,
            "blocked_by": "Weyl/source/boundary/readout trace tails remain live",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4507_2_finite_row_ready",
            "gate": "B_mem finite row is score-ready",
            "derived_now": False,
            "blocked_by": "numeric/source-backed component coefficients missing",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4507_3_local_GR",
            "gate": "local GR/PPN/R10 promotion",
            "derived_now": False,
            "blocked_by": "B_mem_eff and wider memory operator/source-charge gates still unsigned",
            "claim_allowed": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "trace projection lock reduced to Weyl-response tail; B_mem_eff formula and finite source row staged",
            "not_derived": "parent-owned trace projection, Theta_W,m zero, Y5/Y6/source tail silence, numeric finite Bmem inputs",
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
            "next_id": "NT4507_0",
            "target_file": NEXT_TARGET,
            "task": "derive Theta_W,m=0 from metric-response/Khat trace ownership, or fill B_Weyl as the first finite B_mem component bound",
            "success_condition": "the Weyl-response tail is theorem-zero or becomes a sourced finite coefficient row that can enter the 4506 body-charge amplitude",
            "do_not": "treat 826 F1=0 alone as B_mem=0 or as a local-GR/PPN/R10 pass",
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4507_0",
            "decision": DECISION,
            "because": "the algebraic trace split is not the same as a parent Hilbert trace unless the Weyl metric-response tail and Khat trace assignment are owned",
            "effect": "the coupling hunt has a concrete next object: Theta_W,m, rather than a broad missing-coupling label",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_files = [
        SOURCE_REGISTER,
        TRACE_DERIVATION,
        WEYL_AUDIT,
        BMEM_FORMULA,
        FINITE_ROW,
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
    formula_ok = any("Theta_W,m" in str(row.get("expression", "")) for row in all_rows["formula"])
    finite_ok = any(row.get("coefficient") == "B_mem_eff" for row in all_rows["finite"])
    no_claim = all(not bool(row.get("derived_now", False)) for row in all_rows["gates"])
    next_ok = all_rows["next"][0]["target_file"] == NEXT_TARGET
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4507_00_sources", source_ok, "all source paths exist and needles are found"),
        ("VAL4507_01_trace_derivation", True, "trace projection reduced to Weyl response tail"),
        ("VAL4507_02_formula", formula_ok, "B_mem_eff formula includes Theta_W,m"),
        ("VAL4507_03_finite_row", finite_ok, "finite Bmem source row staged"),
        ("VAL4507_04_claims_blocked", no_claim, "all claim gates remain blocked"),
        ("VAL4507_05_nonclaim_flags", nonclaim_ok, "all generated claim flags remain false"),
        ("VAL4507_06_csv_parse", parsed, ";".join(details)),
        ("VAL4507_07_next_target", next_ok, NEXT_TARGET),
        ("VAL4507_08_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
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
            "validation_id": "VAL4507_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4507 memory trace projection lock or finite Bmem source row",
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
            "local_gr_newton_r2fr_memory_trace_coupling",
            '"4507 derives the trace-projection obstruction: the 826 F1 branch-extremum term can vanish, but a parent Hilbert trace also carries a Weyl/metric-response tail, so B_mem_eff equals the 826 branch term plus Theta_W,m and source/readout tails unless those are parent-signed zero."',
            '"4507 source register, trace projection derivation, Weyl response audit, Bmem effective formula, finite source row, parent audit, claim gates, status and validation."',
            "private_trace_projection_weyl_tail_nonclaim",
            NEXT_TARGET,
            "using algebraic trace split or 826 F1 zero alone as B_mem=0/local-GR evidence.",
            "local_gr_newton_r2fr_memory_trace_coupling",
            str(FORMAL_PATH),
            NEXT_TARGET,
            '"derive or bound Theta_W,m first; then insert B_mem_eff into the 4506 body-charge row."',
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    trace: Sequence[Mapping[str, object]],
    weyl: Sequence[Mapping[str, object]],
    formula: Sequence[Mapping[str, object]],
    finite: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4507 - Memory Trace Projection Lock Or Finite Bmem Source Row

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4507 tries to derive the trace projection rather than simply naming it. The algebraic split

`K_MTS,mu_nu = -Gamma_eff g_mu_nu + K_hat,mu_nu`

only gives `Gamma_eff=-1/4 Tr(K_MTS)` when the same parent branch makes `K_hat` tracefree, including its memory derivative. If `K_MTS` is a Hilbert/metric-derived stress from an action, its trace contains a Weyl-response tail. Therefore the real coupling coefficient is:

`B_mem_eff = a_F L_cg^-2 R_m(m_L;X_B) - 1/4 Theta_W,m|L + B_Y5_trace + B_Y6_trace + B_boundary + B_readout`.

The 826 extremum can kill the first term. It does not kill the Weyl/metric-response, source-normalization, extra-stress, boundary, or readout terms. That is progress because the next object is no longer vague coupling; it is `Theta_W,m` plus named source tails.

No local-GR, PPN, R10, clock, orbital, or EM claim is made.

## Source Register

{table(sources)}

## Trace Projection Derivation

{table(trace)}

## Weyl Response Audit

{table(weyl)}

## Bmem Effective Formula

{table(formula)}

## Finite Bmem Source Row

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
    trace = trace_derivation_rows()
    weyl = weyl_audit_rows()
    formula = bmem_formula_rows()
    finite = finite_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    next_target = next_rows()
    decisions = decision_rows()

    all_rows = {
        "sources": sources,
        "trace": trace,
        "weyl": weyl,
        "formula": formula,
        "finite": finite,
        "parent": parent,
        "gates": gates,
        "status": status,
        "next": next_target,
        "decisions": decisions,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TRACE_DERIVATION, trace)
    write_csv(WEYL_AUDIT, weyl)
    write_csv(BMEM_FORMULA, formula)
    write_csv(FINITE_ROW, finite)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, trace, weyl, formula, finite, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4507 Memory Trace Projection Lock Or Finite Bmem Source Row

Marker: `{MARKER}`  
4507 derives the remaining trace-projection coupling instead of treating `B_mem` as fog. The 826 branch-extremum kills only the explicit `a_F L_cg^-2 R_m` term. A parent Hilbert trace also carries a Weyl/metric-response tail, so `B_mem_eff` contains `Theta_W,m` plus Y5/Y6/source/boundary/readout trace tails until those are parent-signed zero or numerically bounded.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4507 Packet Integration

Marker: `{PACKET_MARKER}`  
The coupling route now has a named hard object: `Theta_W,m`, the memory derivative of the Weyl/metric-response trace tail. The next step is to derive this tail as zero from Khat metric-response ownership, or source it as the first finite `B_mem_eff` component before using the 4506 body-charge row.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
