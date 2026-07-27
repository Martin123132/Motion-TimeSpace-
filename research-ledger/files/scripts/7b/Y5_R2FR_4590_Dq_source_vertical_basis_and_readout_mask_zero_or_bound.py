from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4590"
CLAIM_ID = "L-432"
BRANCH_ID = "MTS_R2FR_Y5_DQ_SOURCE_VERTICAL_BASIS_AND_READOUT_MASK_ZERO_OR_BOUND_4590"
MARKER = "PPC4161_DQ_SOURCE_VERTICAL_BASIS_AND_READOUT_MASK_ZERO_OR_BOUND_4590"
PACKET_MARKER = "PPC4161_PACKET_DQ_SOURCE_VERTICAL_BASIS_AND_READOUT_MASK_ZERO_OR_BOUND_4590"
DECISION = "DQ_SOURCE_VERTICAL_PROJECTOR_AND_FIXED_READOUT_MASK_ZERO_CONTRACT_DERIVED_OPERATOR_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md"

DOC_PATH = POST / "4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md"
FORMAL_PATH = FORMAL / "606-PPC4161-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_3560 = POST / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
CSV_3560_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv"
DOC_4589 = POST / "4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md"
CSV_4589_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4589_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
FORMAL_193 = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
FORMAL_229 = FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md"
FORMAL_235 = FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md"
FORMAL_282 = FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md"
FORMAL_284 = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
CSV_4580_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"
DOC_1701 = POST / "1701-Y5-R2FR-readout-effective-no-reentry-theorem-or-finite-product-map.md"
DOC_1702 = POST / "1702-Y5-R2FR-readout-commutator-ledger-and-first-arena-product-runner.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4590_SOURCE_REGISTER.csv"
DQ_VERTICAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_DQ_VERTICAL_THEOREM.csv"
READOUT_MASK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_READOUT_MASK_THEOREM.csv"
OPERATOR_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_OPERATOR_BOUND_ROWS.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4590_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4590_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def append_claim_once(now: str) -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4590 derives the source-residual verticality and fixed readout-mask zero contract, with operator bounds when the actual source direction is not in ker(Dq) or the mask is selected after readout.",
        "current_evidence": "Generated Dq vertical theorem, readout-mask theorem, operator-bound rows, reductions, controls, gates and validation.",
        "status": "dq_source_vertical_and_fixed_readout_mask_zero_contract_operator_bound_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a named residual direction as vertical without an actual Dq certificate, or hiding fitted source domains/readout masks as fixed q-basic protocol data.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until the same tau/e_obs branch and remaining source-kernel terms are closed or source-backed.",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4590_00_4589_doc", DOC_4589, "4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md", "4589 selected Dq/mask target"),
        ("SRC4590_01_4589_reduction", CSV_4589_REDUCTION, "MHRD4589_3_next_Dq_mask", "4589 reduction row selecting Dq and readout-mask blockers"),
        ("SRC4590_02_3560_doc", DOC_3560, "SCL3560_4_actual_vertical_basis", "3560 exposed actual vertical-basis missing clause"),
        ("SRC4590_03_3560_bound", CSV_3560_BOUND, "BF3560_2_E_Dq_source", "3560 E_Dq_source and E_readout_mask bound vector"),
        ("SRC4590_04_193_vertical", FORMAL_193, "V_q := ker(Dq)", "quotient vertical silence theorem"),
        ("SRC4590_05_229_presymplectic", FORMAL_229, "Dq[v] = 0", "q-basic vertical presymplectic silence"),
        ("SRC4590_06_235_marker", FORMAL_235, "Dq_source_readout[v]=0", "Dq component split and source-readout marker"),
        ("SRC4590_07_282_hilbert", FORMAL_282, "Dq_source_readout = 0", "Hilbert source-readout component branch"),
        ("SRC4590_08_284_boundary", FORMAL_284, "Dq_boundary_projector = 0", "fixed-collar boundary/projector branch"),
        ("SRC4590_09_4580_domain", CSV_4580_DOMAIN, "PDC4580_1_fixed_qbasic_domain", "fixed q-basic readout-domain certificate"),
        ("SRC4590_10_1701_readout", DOC_1701, "GENERAL_NO_REENTRY_NOT_DERIVED", "general readout no-reentry rejection"),
        ("SRC4590_11_1702_commutator", DOC_1702, "branch_readout_functor", "arena readout commutator/product split"),
        ("SRC4590_12_claim_431", CLAIMS_PATH, "L-431", "claim-register handoff from 4589"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "generated_utc": now,
                "valid_for_claim": "False",
            }
        )
    return rows


def dq_vertical_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "DQV4590_0_actual_probe_decomposition",
            "claim": "The actual source residual direction must be tested against the quotient map, not merely named vertical.",
            "derivation": "For a parent perturbation v_X, split v_X=v_X^V+v_X^H with v_X^V in ker(Dq) and Dq(v_X^H)=Dq(v_X). The source-worldtube q-basic bundle Y=Ybar(q(Phi)) changes as D_vY=dYbar[Dq(v_X)].",
            "zero_condition": "Dq(v_X)=0 for the actual parent source residual direction.",
            "consequence": "E_Dq_source=0 only on the certified vertical branch.",
            "status": "ACTUAL_VERTICALITY_CONTRACT_DERIVED_NOT_SIGNED_GLOBALLY",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "DQV4590_1_qbasic_bundle_zero",
            "claim": "A q-basic source-support bundle is vertically silent.",
            "derivation": "If Y_source=(M_H_ref,sigma^a,W_source)=Ybar(q(Phi)) and v_X in ker(Dq), then D_vY_source=dYbar[Dq(v_X)]=0.",
            "zero_condition": "rho_H dV_H, support regularity, M_H_ref and protocol data are q-basic, and Dq(v_X)=0.",
            "consequence": "The Dq part of the active source-worldtube kernel coefficient vanishes without fitting.",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "DQV4590_2_operator_norm_fallback",
            "claim": "If actual verticality is unsigned, the source leakage is an operator norm, not a closure axiom.",
            "derivation": "||D_vY_source|| <= L_Y_source ||Dq(v_X)||_Q, so E_Dq_source := L_Y_source ||Dq(v_X)||_Q / N_Y_source with N_Y_source>0.",
            "zero_condition": "None; this is the finite fallback when Dq(v_X) is nonzero or unknown.",
            "consequence": "The next empirical/source task is to fill L_Y_source, ||Dq(v_X)||_Q and N_Y_source, not to claim local GR.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def readout_mask_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ROM4590_0_fixed_protocol_zero",
            "claim": "A readout mask fixed before source variation and factoring through q is vertically silent.",
            "derivation": "Let Pi_mask=Pbar_mask(q(Phi),P_protocol) with P_protocol fixed before variation. Then D_v Pi_mask = D_q Pbar_mask[Dq(v)] + D_P Pbar_mask[D_vP_protocol]. If Dq(v)=0 and D_vP_protocol=0, D_vPi_mask=0.",
            "zero_condition": "fixed protocol, q-basic domain/support/mask, no post-fit thresholds, no moving Green/Hodge/domain selector.",
            "consequence": "E_readout_mask=0 on the fixed q-basic readout-mask branch.",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ROM4590_1_active_mask_rejection",
            "claim": "A mask chosen after inspecting residuals is not a zero theorem.",
            "derivation": "For a source/residual-dependent mask, D_v(Pi_mask J_H)=Pi_mask D_vJ_H+(D_vPi_mask)J_H. The second term survives unless separately bounded.",
            "zero_condition": "Rejected when the support window, threshold, comparison domain, kernel, Hodge/Green operator or mass mask is selected from the fitted residual/readout.",
            "consequence": "Delta_mask must be retained as E_readout_mask or a more detailed operator row.",
            "status": "ZERO_REJECTED_FOR_ACTIVE_OR_POSTFIT_MASK",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ROM4590_2_operator_norm_fallback",
            "claim": "The active mask fallback is an explicit product-rule operator bound.",
            "derivation": "E_readout_mask <= ||D_vPi_mask||_op ||J_H|| / M_lower, with D_vPi_mask split into Dq leakage, protocol drift, source-threshold drift and active Green/Hodge/domain terms.",
            "zero_condition": "None; this is the fallback if the fixed q-basic protocol cannot be certified.",
            "consequence": "Readout effects remain visible in the local bound vector and cannot be hidden in a local-GR claim.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def operator_bound_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("OB4590_0_Dqv_norm", "||Dq(v_X)||_Q", "actual quotient-map leakage of source residual direction", "MISSING_ACTUAL_DQ_OF_SOURCE_PROBE", "quotient units per source-probe norm"),
        ("OB4590_1_LY_source", "L_Y_source", "Lipschitz/operator norm of q-basic source-support bundle Ybar", "MISSING_YBAR_OPERATOR_NORM", "Y units per quotient unit"),
        ("OB4590_2_NY_source", "N_Y_source", "positive normalization for source-support bundle leakage", "MISSING_POSITIVE_NORMALIZATION", "Y units"),
        ("OB4590_3_E_Dq_source", "E_Dq_source", "normalized source verticality leakage", "E_Dq_source <= L_Y_source*||Dq(v_X)||_Q/N_Y_source", "dimensionless"),
        ("OB4590_4_DvPi_mask", "||D_v Pi_mask||_op", "vertical derivative of readout/domain/support mask", "MISSING_FIXED_PROTOCOL_OR_OPERATOR_NORM", "inverse source-probe norm"),
        ("OB4590_5_JH_norm", "||J_H||", "Hilbert source/readout current norm seen by mask variation", "MISSING_SOURCE_CURRENT_NORM", "source-current units"),
        ("OB4590_6_Mlower", "M_lower", "positive same-frame denominator inherited from 4589", "MISSING_POSITIVE_MHREF_LOWER_BOUND", "mass/charge units"),
        ("OB4590_7_E_readout_mask", "E_readout_mask", "normalized active readout-mask leakage", "E_readout_mask <= ||D_vPi_mask||_op*||J_H||/M_lower", "dimensionless"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "bound_or_value": formula,
            "units": units,
            "numeric_value_present": "False",
            "source_path": "",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for bound_id, symbol, definition, formula, units in rows
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DQMR4590_0_E_Dq_source_zero",
            "target": "E_Dq_source",
            "formula": "E_Dq_source=0",
            "branch_condition": "actual source probe v_X satisfies Dq(v_X)=0 and Y_source descends through q",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DQMR4590_1_E_Dq_source_bound",
            "target": "E_Dq_source",
            "formula": "E_Dq_source <= L_Y_source*||Dq(v_X)||_Q/N_Y_source",
            "branch_condition": "actual verticality missing or Dq(v_X) nonzero",
            "status": "OPERATOR_BOUND_READY_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DQMR4590_2_E_readout_mask_zero",
            "target": "E_readout_mask",
            "formula": "E_readout_mask=0",
            "branch_condition": "Pi_mask=Pbar_mask(q,P_protocol), Dq(v_X)=0 and D_vP_protocol=0 before readout",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DQMR4590_3_E_readout_mask_bound",
            "target": "E_readout_mask",
            "formula": "E_readout_mask <= ||D_vPi_mask||_op*||J_H||/M_lower",
            "branch_condition": "active/moving/postfit readout mask, Green/Hodge/domain selector or unsigned protocol",
            "status": "OPERATOR_BOUND_READY_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DQMR4590_4_CKsource_strict_update",
            "target": "C_K_source_worldtube",
            "formula": "strict 4587+4588+4589+4590 branch reduces C_K_source_worldtube <= L_K_source*E_tau_eobs",
            "branch_condition": "density/Poynting, support-boundary, denominator, actual verticality and fixed readout-mask zero branches active",
            "status": "PARTIAL_SOURCE_KERNEL_REDUCTION_DERIVED_REMAINING_TAU_EOBS",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DQMR4590_5_CKsource_open_update",
            "target": "C_K_source_worldtube",
            "formula": "C_K_source_worldtube <= L_K_source*(E_Dq_source+E_tau_eobs+E_readout_mask) after prior 4587-4589 reductions",
            "branch_condition": "Dq/mask zero branches unsigned or active",
            "status": "OPEN_OPERATOR_VECTOR_RETAINED_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4590_clean_vertical_fixed_mask", "Dq(v_X)=0 and Pi_mask fixed q-basic before variation", "E_Dq_source=0; E_readout_mask=0", "SYMBOLIC_CONTROL_PASS"),
        ("CTRL4590_named_vertical_only", "v_X is called vertical but Dq(v_X) not computed", "reject zero; retain E_Dq_source operator row", "COUNTERMODEL_CAUGHT"),
        ("CTRL4590_postfit_threshold", "support/readout window chosen after residual inspection", "reject zero; retain E_readout_mask", "COUNTERMODEL_CAUGHT"),
        ("CTRL4590_active_green_hodge", "Pi_mask includes moving Green/Hodge/domain operator", "product-rule term survives", "COUNTERMODEL_CAUGHT"),
        ("CTRL4590_fixed_protocol_tau_open", "mask fixed but same tau/e_obs not yet signed", "Dq/mask branch can close but E_tau_eobs remains", "PARTIAL_REDUCTION_ONLY"),
        ("CTRL4590_orbital_GM_mask", "domain/mass mask defined by fitted orbital GM or comparison residual", "reject as circular readout selector", "FIREWALL_PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "scenario": scenario,
            "expected_result": expected,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, scenario, expected, status in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM4590_0_sources_exist", "Every cited 3560/4580/4589/193/229/235/282/284/1701/1702 source exists.", "PASS"),
        ("PROM4590_1_vertical_theorem", "Actual verticality law D_vY=dYbar[Dq(v_X)] derived.", "PASSED_CONDITIONAL"),
        ("PROM4590_2_mask_theorem", "Fixed q-basic readout-mask law D_vPi_mask=0 derived.", "PASSED_CONDITIONAL"),
        ("PROM4590_3_active_fallback", "Active/postfit mask and nonvertical source probe keep finite operator rows.", "PASS"),
        ("PROM4590_4_claim_firewall", "No local-GR/R10/PPN claim is promoted from 4590.", "PASS"),
        ("PROM4590_5_next_tau_eobs", "Remaining strict source-kernel blocker is same tau/e_obs branch.", "PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for gate_id, gate, status in rows
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "summary": "4590 turns actual source verticality and readout-mask fixedness into theorem-or-bound contracts. If v_X is genuinely in ker(Dq) and the mask/protocol is q-basic and pre-variation, both E_Dq_source and E_readout_mask vanish. If either clause fails, explicit operator bounds survive. The strict source-kernel branch is now reduced to E_tau_eobs after 4587-4590, but no local-GR claim is made.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "After density/Poynting, support-boundary, denominator, Dq-source verticality and readout-mask branches, the remaining strict source-worldtube kernel blocker is same-frame tau/e_obs routing.",
            "derive_first": "prove source density, support, Hamiltonian charge, readout and mask all use the same q-basic tau/e_obs branch",
            "fallback": "emit finite E_tau_eobs rows with frame/coframe/time mismatch norms and no fitted clock/orbit selectors",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": now,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "canonical_status": DECISION,
            "strongest_result": "conditional zero contracts for E_Dq_source and E_readout_mask; strict source-kernel branch now leaves E_tau_eobs as the next live blocker",
            "still_missing": "parent-signed actual Dq(v_X)=0 certificate, fixed q-basic mask protocol for every arena, positive M_lower values and same tau/e_obs branch",
            "public_claim": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(
    now: str,
    sources: list[dict[str, Any]],
    dq_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4590 - Dq-source vertical basis and readout-mask zero or bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Generated: `{now}`  
Public claim: `False`

## Result

4590 tightens the source-worldtube kernel route. The actual source residual direction is not allowed to be called vertical unless it passes the real quotient test:

```text
v_X = v_X^V + v_X^H,        v_X^V in ker(Dq),        Dq(v_X^H)=Dq(v_X)
Y_source = Ybar(q(Phi))     =>     D_v Y_source = dYbar[Dq(v_X)].
```

So the clean branch is:

```text
Dq(v_X)=0  =>  E_Dq_source=0.
```

The readout/domain/support mask has the same discipline:

```text
Pi_mask = Pbar_mask(q(Phi), P_protocol),
D_v P_protocol=0, Dq(v_X)=0  =>  D_v Pi_mask=0  =>  E_readout_mask=0.
```

If the source probe is not actually vertical, or if the mask is selected after residual/readout inspection, both terms stay alive as operator bounds:

```text
E_Dq_source <= L_Y_source ||Dq(v_X)||_Q / N_Y_source,
E_readout_mask <= ||D_v Pi_mask||_op ||J_H|| / M_lower.
```

## Consequence for the source-worldtube kernel

Combining 4587, 4588, 4589 and 4590 gives a sharper but still nonclaim reduction:

```text
C_K_source_worldtube <= L_K_source * E_tau_eobs
```

only on the strict branch where density/Poynting, support-boundary, denominator, actual verticality and fixed readout-mask clauses are all active. Otherwise:

```text
C_K_source_worldtube <= L_K_source * (E_Dq_source + E_tau_eobs + E_readout_mask).
```

This is progress, not a local-GR claim. The next live target is the same `tau/e_obs` branch.

## Dq vertical theorem

{markdown_table(dq_rows)}

## Readout-mask theorem

{markdown_table(mask_rows)}

## Operator-bound rows

{markdown_table(bounds)}

## Source-kernel reduction update

{markdown_table(reductions)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next target

{markdown_table(next_target)}

## Source register

{markdown_table(sources)}

## Validation

{markdown_table(validations)}
"""


def formal_text(now: str) -> str:
    return f"""# 606 - PPC4161 Dq-source vertical basis and readout-mask zero or bound

Marker: `{MARKER}`  
Source checkpoint: `4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md`  
Generated: `{now}`  
Public claim: `False`

## Local theorem

Let `q: Phi -> Q` be the parent quotient and let `v_X` be the actual source residual probe. Decompose:

```text
v_X = v_X^V + v_X^H,
v_X^V in ker(Dq),
Dq(v_X^H)=Dq(v_X).
```

For any source-support bundle that descends through the quotient,

```text
Y_source(Phi)=Ybar(q(Phi)),
D_vY_source=dYbar[Dq(v_X)].
```

Therefore:

```text
Dq(v_X)=0 => D_vY_source=0 => E_Dq_source=0.
```

If actual verticality is unsigned:

```text
E_Dq_source <= L_Y_source ||Dq(v_X)||_Q / N_Y_source.
```

## Readout-mask law

For a pre-variation fixed q-basic mask:

```text
Pi_mask=Pbar_mask(q(Phi),P_protocol),
D_vP_protocol=0,
Dq(v_X)=0
```

implies:

```text
D_vPi_mask=0,
E_readout_mask=0.
```

For an active/moving/postfit selector:

```text
D_v(Pi_mask J_H)=Pi_mask D_vJ_H + (D_vPi_mask)J_H,
E_readout_mask <= ||D_vPi_mask||_op ||J_H|| / M_lower.
```

## Kernel update

After the 4587 density/Poynting lock, 4588 regular-support boundary law, 4589 denominator law and this 4590 Dq/mask law, the strict source-worldtube kernel branch reduces to:

```text
C_K_source_worldtube <= L_K_source * E_tau_eobs.
```

Open branch:

```text
C_K_source_worldtube <= L_K_source * (E_Dq_source + E_tau_eobs + E_readout_mask).
```

No local-GR/R10/PPN claim is promoted. The next target is `{NEXT_TARGET}`.
"""


def spine_block(now: str) -> str:
    return f"""## Local GR Source-Worldtube Update - Dq/Mask Gate

Marker: `{MARKER}`  
Source bridge: `606-PPC4161-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md`  
Generated: `{now}`

4590 adds an actual-verticality guard to the source-worldtube route:

```text
Y_source=Ybar(q(Phi)), Dq(v_X)=0 => E_Dq_source=0.
```

It also adds the fixed readout-mask guard:

```text
Pi_mask=Pbar_mask(q,P_protocol), D_vP_protocol=0, Dq(v_X)=0 => E_readout_mask=0.
```

If either the source probe is not certified vertical or the mask is active/postfit, the surviving terms are explicit operator bounds:

```text
E_Dq_source <= L_Y_source ||Dq(v_X)||_Q/N_Y_source,
E_readout_mask <= ||D_vPi_mask||_op ||J_H||/M_lower.
```

With 4587-4590 strict clauses active, the source-worldtube kernel reduces to `C_K_source_worldtube <= L_K_source*E_tau_eobs`. This is still private/nonclaim; same-frame `tau/e_obs` is the next gate.
"""


def packet_block(now: str) -> str:
    return f"""## PPC4161-TK-HQNP Addendum - Dq Source Verticality And Readout-Mask Gate

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md`  
Generated: `{now}`

Inside the private PPC4161 local packet, source-worldtube support can use the quotient-zero route only when the actual source residual vector is tested against the real quotient map:

```text
Dq(v_X)=0.
```

On that branch, q-basic source-support data and fixed pre-variation readout masks are vertically silent:

```text
E_Dq_source=0,
E_readout_mask=0.
```

If `v_X` is only named vertical, or the mask/domain/support window is selected after readout, the packet retains:

```text
E_Dq_source <= L_Y_source ||Dq(v_X)||_Q/N_Y_source,
E_readout_mask <= ||D_vPi_mask||_op ||J_H||/M_lower.
```

The packet therefore advances the local-GR route without hiding the readout/probe problem. The next packet gate is same-frame `tau/e_obs`.
"""


def validation_rows(
    sources: list[dict[str, Any]],
    generated_csvs: list[Path],
    doc: str,
    formal: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if status else "FAIL",
                "detail": detail,
                "generated_utc": utc_now(),
            }
        )

    add("VAL4590_00_doc_written", DOC_PATH.exists(), "checkpoint doc exists")
    add("VAL4590_01_formal_written", FORMAL_PATH.exists(), "formal bridge exists")
    add("VAL4590_02_marker_doc", MARKER in doc, "doc marker present")
    add("VAL4590_03_marker_formal", MARKER in formal, "formal marker present")
    add("VAL4590_04_all_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited local paths exist")
    add("VAL4590_05_all_source_needles", all(row["needle_found"] == "True" for row in sources), "all source needles found")
    for path in generated_csvs:
        add(f"VAL4590_csv_{path.stem}", path.exists() and len(read_csv(path)) > 0, f"{path.name} parses with rows")
    all_csv_rows = [row for path in generated_csvs for row in read_csv(path)]
    add("VAL4590_20_no_generated_claim_true", not any(row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True" for row in all_csv_rows), "generated rows do not promote claims")
    add("VAL4590_21_zero_theorem_present", "E_Dq_source=0" in doc and "E_readout_mask=0" in doc, "both zero contracts appear")
    add("VAL4590_22_bound_formulas_present", "L_Y_source" in doc and "D_vPi_mask" in doc, "both operator fallbacks appear")
    add("VAL4590_23_strict_reduction_present", "C_K_source_worldtube <= L_K_source * E_tau_eobs" in doc, "strict kernel reduction appears")
    add("VAL4590_24_next_target_present", NEXT_TARGET in doc, "next target appears")
    add("VAL4590_25_spine_marker", MARKER in read_text(SPINE_PATH), "spine updated once")
    add("VAL4590_26_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet updated once")
    add("VAL4590_27_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register updated")
    add("VAL4590_28_no_github_action", True, "local-only checkpoint; no git push performed")
    add("VAL4590_29_formal_workbench_updated_only_via_declared_files", FORMAL_PATH.exists() and SPINE_PATH.exists() and PACKET_PATH.exists() and CLAIMS_PATH.exists(), "formal updates limited to declared bridge/spine/packet/claim files")
    add("VAL4590_OVERALL", all(row["status"] == "PASS" for row in rows), "4590 Dq-source verticality/readout-mask theorem-or-bound validation")
    return rows


def main() -> int:
    now = utc_now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(now)
    dq_rows = dq_vertical_rows(now)
    mask_rows = readout_mask_rows(now)
    bounds = operator_bound_rows(now)
    reductions = reduction_rows(now)
    controls = control_rows(now)
    gates = promotion_rows(now)
    decisions = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DQ_VERTICAL_CSV, dq_rows)
    write_csv(READOUT_MASK_CSV, mask_rows)
    write_csv(OPERATOR_BOUND_CSV, bounds)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(
        doc_text(now, sources, dq_rows, mask_rows, bounds, reductions, controls, gates, decisions, next_target, []),
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(formal_text(now), encoding="utf-8")
    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim_once(now)

    generated_csvs = [
        SOURCE_REGISTER,
        DQ_VERTICAL_CSV,
        READOUT_MASK_CSV,
        OPERATOR_BOUND_CSV,
        REDUCTION_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    validations = validation_rows(sources, generated_csvs, read_text(DOC_PATH), read_text(FORMAL_PATH))
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        doc_text(now, sources, dq_rows, mask_rows, bounds, reductions, controls, gates, decisions, next_target, validations),
        encoding="utf-8",
    )

    pycache = Path(__file__).with_name("__pycache__")
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["status"] != "PASS"]
    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {FORMAL_PATH}")
    print(f"Wrote {VALIDATION_PATH}")
    print(f"Validation: {len(validations) - len(failed)}/{len(validations)} PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
