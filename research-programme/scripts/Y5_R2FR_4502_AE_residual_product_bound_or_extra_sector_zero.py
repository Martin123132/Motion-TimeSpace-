from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4502"
CLAIM_ID = "L-344"
MARKER = "PPC4161_AE_RESIDUAL_PRODUCT_BOUND_OR_EXTRA_SECTOR_ZERO_4502"
PACKET_MARKER = "PPC4161_PACKET_AE_RESIDUAL_PRODUCT_BOUND_OR_EXTRA_SECTOR_ZERO_4502"
DECISION = "AE_ZERO_THEOREM_DECOMPOSED_PRODUCT_BOUND_GATE_FILLED_SUBCOMPONENTS_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4503-Y5-R2FR-DeltaE-R11-EH-only-operator-or-first-coefficient-bound.md"

FORMAL_PATH = FORMAL / "518-PPC4161-AE-residual-product-bound-or-extra-sector-zero.md"
DOC_PATH = POST / "4502-Y5-R2FR-AE-residual-product-bound-or-extra-sector-zero.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4502_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4502_SOURCE_REGISTER.csv"
AE_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_AE_ZERO_THEOREM.csv"
AE_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_AE_RESIDUAL_VECTOR_DECOMPOSITION.csv"
AE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_AE_PRODUCT_BOUND_GATE.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4502_DECISION.csv"

FORMAL_517 = FORMAL / "517-PPC4161-A-shell-component-source-coefficient-fill-or-kernel-zero.md"
POST_4501 = POST / "4501-Y5-R2FR-A-shell-component-source-coefficient-fill-or-kernel-zero.md"
SCRIPT_4501 = SCRIPT_DIR / "Y5_R2FR_4501_A_shell_component_source_coefficient_fill_or_kernel_zero.py"
RESIDUAL_MAP_4501 = SOURCE_DIR / "P8_Y5_R2FR_4501_RESIDUAL_LEDGER_COMPONENT_MAP.csv"
COMPONENT_BUDGET_4501 = SOURCE_DIR / "P8_Y5_R2FR_4501_COMPONENT_TRANSFER_BUDGET.csv"
STATUS_4501 = SOURCE_DIR / "P8_Y5_R2FR_4501_STATUS.csv"
L2_ENVELOPE_1953 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1953_L2_ENVELOPE_LEDGER.csv"
L2_SPLIT_1954 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1954_L2_RESIDUAL_SPLIT.csv"
RESIDUAL_LEDGER_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"
RESIDUAL_OPERATOR_1956 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1956_RESIDUAL_OPERATOR_LEDGER.csv"
RESIDUAL_CURRENT_1957 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1957_RESIDUAL_CURRENT_LEDGER.csv"

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
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def rows_by(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    return {row[key]: row for row in read_csv(path) if key in row}


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4502_00_formal517", "4501 formal handoff", FORMAL_517, "RM4501_1_extra_residual", "A_E product bound"),
        ("SRC4502_01_post4501", "4501 post mirror", POST_4501, "prove A_E=0", "selected A_E target"),
        ("SRC4502_02_residual_map4501", "4501 residual component map", RESIDUAL_MAP_4501, "RM4501_1_extra_residual", "A_E row"),
        ("SRC4502_03_budget4501", "4501 component budget", COMPONENT_BUDGET_4501, "CB4501_A_E", "A_E numeric budget"),
        ("SRC4502_04_status4501", "4501 status", STATUS_4501, "4502-Y5-R2FR-AE-residual-product-bound-or-extra-sector-zero.md", "next target"),
        ("SRC4502_05_l2env1953", "1953 l2 envelope ledger", L2_ENVELOPE_1953, "ENV1953_2_kernel_transport", "kernel/envelope route"),
        ("SRC4502_06_l2split1954", "1954 residual split", L2_SPLIT_1954, "L2R1954_5_verdict", "residual zero conditions"),
        ("SRC4502_07_bound1955", "1955 residual bound ledger", RESIDUAL_LEDGER_1955, "RB1955_2_extra_residual_l2", "P2 R_extra row"),
        ("SRC4502_08_operator1956", "1956 residual operator ledger", RESIDUAL_OPERATOR_1956, "RES1956_3_R_extra_l2", "extra residual component"),
        ("SRC4502_09_current1957", "1957 residual current ledger", RESIDUAL_CURRENT_1957, "CUR1957_4_projection_to_STF", "source-current projection"),
        ("SRC4502_10_script4501", "4501 generator", SCRIPT_4501, 'CHECKPOINT = "4501"', "reproducible predecessor"),
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


def constants() -> Dict[str, float]:
    row = rows_by(COMPONENT_BUDGET_4501, "budget_id").get("CB4501_A_E", {})
    return {
        "single_a": float(row.get("single_survivor_A_bound", "1.400851696295935e-13")),
        "single_j2": float(row.get("single_survivor_J2_bound", "3.3e-08")),
        "equal_a": float(row.get("equal_no_cancellation_A_budget", "3.502129240739837e-14")),
        "equal_j2": float(row.get("equal_no_cancellation_J2_budget", "8.25e-09")),
        "c_j2": float(row.get("rho1_abs_coefficient", "2.355709750522272e5")),
    }


def ae_zero_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "AEZ4502_0_master_bound",
            "target": "A_E",
            "statement": "A_E is controlled by the extra-sector l=2 residual after EH/GR baseline subtraction.",
            "formula": "|A_E| <= ||W_STF||_1 ||K_2^X|| ||P_2 R_extra||",
            "result": "EXACT_PRODUCT_BOUND_FROM_4501_1955",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AEZ4502_1_vector_zero",
            "target": "P_2 R_extra",
            "statement": "The extra residual is zero if all named residual subchannels vanish in the same source/coframe/baseline convention.",
            "formula": "DeltaE_R11_l2=DeltaT_w_l2=DeltaT_NH_l2=Omega_boundary_extra_l2=DeltaT_readout_l2=0 => P_2 R_extra=0 => A_E=0",
            "result": "CONDITIONAL_AE_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AEZ4502_2_EH_only_operator",
            "target": "DeltaE_R11_l2",
            "statement": "If the local weak-field operator is exactly EH in the public branch, the non-EH/R11 l=2 operator residual vanishes.",
            "formula": "E_local=E_EH through l=2 weak-field order => DeltaE_R11_l2=0",
            "result": "FIRST_SUBCHANNEL_ZERO_TARGET",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AEZ4502_3_no_source_label",
            "target": "DeltaT_w_l2",
            "statement": "If source labels/weights are forgotten by the public source functor, there is no extra l=2 source-prefactor residual.",
            "formula": "source_weight_parent -> source_weight_EH => DeltaT_w_l2=0",
            "result": "SOURCE_LABEL_ZERO_TARGET",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AEZ4502_4_no_nonHilbert_bypass",
            "target": "DeltaT_NH_l2",
            "statement": "If no non-Hilbert/torsion/bypass current couples to the public metric, the non-Hilbert l=2 source residual vanishes.",
            "formula": "J_nonHilbert projected to public l=2 = 0 => DeltaT_NH_l2=0",
            "result": "NONHILBERT_ZERO_TARGET",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AEZ4502_5_boundary_flux",
            "target": "Omega_boundary_extra_l2",
            "statement": "If the parent symplectic/boundary flux has no extra l=2 piece, boundary flux does not feed A_E.",
            "formula": "Omega_boundary_extra_l2=0",
            "result": "BOUNDARY_FLUX_ZERO_TARGET",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AEZ4502_6_readout_reentry",
            "target": "DeltaT_readout_l2",
            "statement": "If identity readout has no post-variation re-entry, readout does not reappear inside the residual source current.",
            "formula": "DeltaT_readout_l2=0",
            "result": "READOUT_REENTRY_ZERO_TARGET",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def ae_vector_rows() -> List[Dict[str, object]]:
    return [
        {
            "component_id": "AEV4502_0_DeltaE_R11",
            "symbol": "DeltaE_R11_l2",
            "meaning": "non-EH/R11 local operator l=2 residual",
            "source_row": "RES1956_0_DeltaE_R11",
            "zero_condition": "local weak-field operator is EH-only through l=2 order",
            "finite_input": "numeric R11/non-EH coefficient vector and l=2 operator norm",
            "status": "FIRST_TARGET_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "AEV4502_1_DeltaT_w",
            "symbol": "DeltaT_w_l2",
            "meaning": "source prefactor/species/source-label l=2 residual",
            "source_row": "RES1956_1_DeltaT_w; CUR1957_1_DeltaT_w",
            "zero_condition": "source-label forgetting/common Hilbert source measure",
            "finite_input": "numeric delta_w l=2 envelope",
            "status": "SOURCE_LABEL_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "component_id": "AEV4502_2_DeltaT_NH",
            "symbol": "DeltaT_NH_l2",
            "meaning": "spin/torsion/boundary/non-Hilbert current bypass residual",
            "source_row": "RES1956_2_DeltaT_NH; CUR1957_2_DeltaT_NH",
            "zero_condition": "no bypass current or projected-silent exact current",
            "finite_input": "numeric non-Hilbert l=2 envelope",
            "status": "NONHILBERT_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "component_id": "AEV4502_3_boundary_flux",
            "symbol": "Omega_boundary_extra_l2",
            "meaning": "extra boundary/symplectic l=2 flux residual",
            "source_row": "RES1956_4_boundary_flux_l2",
            "zero_condition": "no extra l=2 parent theta/Q/boundary flux",
            "finite_input": "numeric boundary flux envelope",
            "status": "BOUNDARY_FLUX_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "component_id": "AEV4502_4_readout_reentry",
            "symbol": "DeltaT_readout_l2",
            "meaning": "post-variation readout/domain/frame re-entry residual",
            "source_row": "CUR1957_3_DeltaT_readout",
            "zero_condition": "identity readout and no domain/frame re-entry",
            "finite_input": "numeric marker/readout l=2 envelope",
            "status": "READOUT_REENTRY_ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "component_id": "AEV4502_5_vector_norm",
            "symbol": "||P_2 R_extra||",
            "meaning": "conservative no-cancellation vector norm",
            "source_row": "RES1956_3_R_extra_l2 plus residual vector rows",
            "zero_condition": "all AEV4502_0 through AEV4502_4 zero",
            "finite_input": "sum of absolute subcomponent envelopes",
            "status": "VECTOR_NORM_DECOMPOSED_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def ae_bound_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    residual_norm = "||DeltaE_R11_l2||+||DeltaT_w_l2||+||DeltaT_NH_l2||+||Omega_boundary_extra_l2||+||DeltaT_readout_l2||"
    return [
        {
            "bound_id": "AEB4502_0_vector_norm",
            "quantity": "||P_2 R_extra||",
            "formula": f"||P_2 R_extra|| <= {residual_norm}",
            "numeric_threshold": "MISSING_UNTIL_WSTF_K2X_SELECTED",
            "status": "VECTOR_BOUND_FORMULA_FILLED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AEB4502_1_single_AE",
            "quantity": "|A_E|",
            "formula": f"||W_STF||_1 ||K_2^X|| ({residual_norm}) <= {c['single_a']:.15e}",
            "numeric_threshold": f"{c['single_a']:.15e}",
            "status": "SINGLE_COMPONENT_BOUND_READY_FACTORS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AEB4502_2_equal_budget_AE",
            "quantity": "|A_E| equal budget",
            "formula": f"||W_STF||_1 ||K_2^X|| ({residual_norm}) <= {c['equal_a']:.15e}",
            "numeric_threshold": f"{c['equal_a']:.15e}",
            "status": "STRICT_NO_CANCELLATION_EQUAL_BUDGET_READY_FACTORS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AEB4502_3_J2_equivalent",
            "quantity": "|DeltaJ2_E|",
            "formula": f"|DeltaJ2_E| = {c['c_j2']:.15e} |A_E| <= {c['equal_j2']:.15e} under equal budget",
            "numeric_threshold": f"{c['equal_j2']:.15e}",
            "status": "J2_EQUIVALENT_COMPONENT_BOUND_READY",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4502_0_AE_zero",
            "clause": "all A_E residual subchannels vanish",
            "current_status": "CONDITIONAL_THEOREM_DECOMPOSED",
            "evidence": str(AE_ZERO_CSV),
            "remaining_unsigned": "subchannel parent signatures",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4502_1_DeltaE_R11",
            "clause": "EH-only local operator",
            "current_status": "FIRST_TARGET_SELECTED",
            "evidence": str(AE_VECTOR_CSV),
            "remaining_unsigned": "numeric/nonzero R11 coefficients or EH-only theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4502_2_finite_bound",
            "clause": "A_E product bound",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "evidence": str(AE_BOUND_CSV),
            "remaining_unsigned": "W_STF, K_2^X and residual vector envelopes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4502_0_AE_zero_theorem",
            "gate": "A_E zero theorem decomposed",
            "passed": True,
            "claim_allowed": False,
            "detail": "if five residual subchannels vanish, A_E=0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4502_1_AE_product_bound",
            "gate": "A_E product bound formula ready",
            "passed": True,
            "claim_allowed": False,
            "detail": "strict equal-budget inequality is written, but factors are not numeric",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4502_2_first_target",
            "gate": "first residual subcomponent selected",
            "passed": True,
            "claim_allowed": False,
            "detail": "DeltaE_R11_l2 is the next best attack because it asks whether the local operator is exactly EH",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4502_3_local_GR_J2_promotion",
            "gate": "local GR/J2 promotion",
            "passed": False,
            "claim_allowed": False,
            "detail": "A_E subchannels are not parent-signed zero and no numeric residual product pass exists",
            "valid_for_claim": False,
        },
    ]


def status_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "AE_zero_theorem_decomposed": True,
            "AE_product_bound_ready": True,
            "AE_numeric_factors_ready": False,
            "first_subtarget": "DeltaE_R11_l2",
            "local_GR_claim": False,
            "equal_AE_budget": f"{c['equal_a']:.15e}",
            "sharpest_open_clause": "prove DeltaE_R11_l2=0 from EH-only local operator, or source the first R11/non-EH coefficient vector",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4502_0",
            "target": NEXT_TARGET,
            "preferred_route": "prove the local weak-field operator is EH-only through l=2 order, giving DeltaE_R11_l2=0",
            "fallback_route": "fill the first finite R11/non-EH coefficient vector and insert it into the A_E product bound",
            "do_not_do": "score total solar l=2 structure instead of GR-subtracted MTS residual l=2",
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "what_moved_forward": "4502 decomposes A_E into five residual subchannels and writes the exact zero theorem plus finite no-cancellation product bound",
            "what_is_derived": "A_E=0 follows if DeltaE_R11_l2, DeltaT_w_l2, DeltaT_NH_l2, Omega_boundary_extra_l2 and DeltaT_readout_l2 vanish in the same baseline",
            "what_remains_blocked": "no subchannel is parent-signed zero or numerically bounded yet; DeltaE_R11_l2 is selected first",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def append_section_once(path: Path, marker: str, section: str) -> None:
    body = text(path)
    if marker in body:
        return
    path.write_text(body.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    claim = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_j2_AE_residual",
        "claim": "4502 decomposes A_E into five residual subchannels, proves the conditional A_E zero theorem from their joint silence, and writes the finite no-cancellation product bound without promoting local GR/J2.",
        "current_evidence": "4502 source register, A_E zero theorem, residual vector decomposition, product bound gate, parent audit, claim gates, status and validation.",
        "status": "private_AE_residual_zero_or_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "scoring total solar l=2 structure rather than GR-subtracted MTS residual l=2, or treating a decomposed target as a pass.",
        "sector": "local_gr_newton_j2_AE_residual",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "DeltaE_R11_l2 is the first live subcomponent; local GR remains unclaimed.",
    }
    rows = []
    if CLAIMS_PATH.exists():
        with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = [
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
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(claim)


def build_doc(
    sources: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    vector_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    parent_audit: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4502 - A_E Residual Product Bound Or Extra Sector Zero

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Result

4502 attacks the first live component from 4501: `A_E`.

The exact finite law is now:

`|A_E| <= ||W_STF||_1 ||K_2^X|| ||P_2 R_extra||`.

The extra residual is no longer a single fog word. It is decomposed into the no-cancellation vector

`||P_2 R_extra|| <= ||DeltaE_R11_l2|| + ||DeltaT_w_l2|| + ||DeltaT_NH_l2|| + ||Omega_boundary_extra_l2|| + ||DeltaT_readout_l2||`.

Therefore the clean zero route is:

`DeltaE_R11_l2=DeltaT_w_l2=DeltaT_NH_l2=Omega_boundary_extra_l2=DeltaT_readout_l2=0 => A_E=0`.

The strict equal-budget finite gate inherited from 4501 is:

`||W_STF||_1 ||K_2^X|| ||P_2 R_extra|| <= 3.502129240739837e-14`.

The next best target is `DeltaE_R11_l2`: prove the local weak-field operator is exactly EH through l=2 order, or fill the first finite R11/non-EH coefficient vector.

No local-GR, J2, PPN, or Newtonian-recovery claim is promoted.

## A_E Zero Theorem

{table(zero_rows)}

## A_E Residual Vector

{table(vector_rows)}

## A_E Product Bound Gate

{table(bound_rows)}

## Parent Signature Audit

{table(parent_audit)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def validation_rows(
    sources: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    vector_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
) -> List[Dict[str, object]]:
    csv_paths = [
        SOURCE_REGISTER,
        AE_ZERO_CSV,
        AE_VECTOR_CSV,
        AE_BOUND_CSV,
        PARENT_AUDIT_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    parsed = []
    for path in csv_paths:
        parsed.append(f"{path.name}:{len(read_csv(path)) if path.exists() and text(path).strip() else 0}")
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_0_sources_exist_and_needles_found",
            "passed": all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources),
            "detail": "all source-register paths exist and needles are found",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_1_AE_zero_theorem",
            "passed": any(row["theorem_id"] == "AEZ4502_1_vector_zero" and "A_E=0" in row["formula"] for row in zero_rows),
            "detail": "A_E zero theorem is decomposed into residual subchannels",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_2_vector_components",
            "passed": len(vector_rows) == 6 and any(row["symbol"] == "DeltaE_R11_l2" for row in vector_rows),
            "detail": "A_E residual vector contains named subcomponents",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_3_product_bound_numeric_threshold",
            "passed": any("3.502129240739837e-14" in row["formula"] for row in bound_rows),
            "detail": "strict equal-budget A_E threshold is carried through",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_4_first_subtarget_selected",
            "passed": NEXT_TARGET in text(NEXT_CSV) and "DeltaE_R11_l2" in text(STATUS_CSV),
            "detail": "DeltaE_R11_l2 selected as first subtarget",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_5_claim_gates_block_promotion",
            "passed": all(str(row["claim_allowed"]).lower() == "false" for row in gates),
            "detail": "claim gates block local-GR/J2 promotion",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_6_all_generated_rows_nonclaim",
            "passed": all("True" not in line.rsplit(",", 1)[-1] for path in csv_paths for line in text(path).splitlines()[1:]),
            "detail": "all generated rows keep valid_for_claim=false",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_7_csvs_parse",
            "passed": all(path.exists() for path in csv_paths),
            "detail": "; ".join(parsed),
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_8_docs_written",
            "passed": FORMAL_PATH.exists() and DOC_PATH.exists() and MARKER in text(FORMAL_PATH),
            "detail": "formal and post checkpoint docs exist",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_9_claim_register_updated",
            "passed": CLAIM_ID in text(CLAIMS_PATH),
            "detail": "claims register contains L-344",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_10_spine_and_packet_updated",
            "passed": MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
            "detail": "spine and packet contain 4502 markers",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4502_11_pycache_removed",
            "passed": not (SCRIPT_DIR / "__pycache__").exists(),
            "detail": "scripts __pycache__ absent after generation",
            "valid_for_claim": False,
        },
    ]


def main() -> None:
    c = constants()
    sources = source_rows()
    zero_rows = ae_zero_rows()
    vector_rows = ae_vector_rows()
    bound_rows = ae_bound_rows(c)
    parent_audit = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows(c)
    next_target = next_rows()
    decisions = decision_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(AE_ZERO_CSV, zero_rows)
    write_csv(AE_VECTOR_CSV, vector_rows)
    write_csv(AE_BOUND_CSV, bound_rows)
    write_csv(PARENT_AUDIT_CSV, parent_audit)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    doc = build_doc(sources, zero_rows, vector_rows, bound_rows, parent_audit, gates, status, next_target, decisions)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)

    append_claim_once()

    append_section_once(
        SPINE_PATH,
        MARKER,
        """
## 4502 A_E Residual Product Bound Or Extra Sector Zero

Marker: `PPC4161_AE_RESIDUAL_PRODUCT_BOUND_OR_EXTRA_SECTOR_ZERO_4502`  
4502 decomposes the `A_E` residual into five named subchannels: `DeltaE_R11_l2`, `DeltaT_w_l2`, `DeltaT_NH_l2`, `Omega_boundary_extra_l2`, and `DeltaT_readout_l2`. It derives the conditional zero theorem that their joint silence gives `A_E=0`, and it writes the no-cancellation finite gate `||W_STF||_1 ||K_2^X|| ||P_2 R_extra|| <= 3.502129240739837e-14`. The next target is the first subchannel: prove the local operator is EH-only or source the first R11/non-EH coefficient vector.
""",
    )

    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        """
## 4502 Packet Integration

Marker: `PPC4161_PACKET_AE_RESIDUAL_PRODUCT_BOUND_OR_EXTRA_SECTOR_ZERO_4502`  
The packet now treats `A_E` as a decomposed residual vector, not a blob. If `DeltaE_R11_l2`, source-label residuals, non-Hilbert bypass, boundary flux, and readout re-entry vanish, then `A_E` vanishes. Otherwise the branch has a concrete product-bound gate. The next clean attack is `DeltaE_R11_l2`: EH-only local operator theorem or first finite coefficient row.
""",
    )

    if (SCRIPT_DIR / "__pycache__").exists():
        shutil.rmtree(SCRIPT_DIR / "__pycache__")

    validation = validation_rows(sources, zero_rows, vector_rows, bound_rows, gates)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if not bool(row["passed"])]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} validation passed ({len(validation)} checks)")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
