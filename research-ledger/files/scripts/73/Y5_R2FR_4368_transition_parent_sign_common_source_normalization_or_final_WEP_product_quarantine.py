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

CHECKPOINT = "4368"
CLAIM_ID = "L-209"
BRANCH = "MTS_R2FR_Y5_TRANSITION_PARENT_SIGN_COMMON_SOURCE_NORMALIZATION_OR_FINAL_WEP_PRODUCT_QUARANTINE_4368"
MARKER = "PPC4161_TRANSITION_PARENT_SIGN_COMMON_SOURCE_NORMALIZATION_OR_FINAL_WEP_PRODUCT_QUARANTINE_4368"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PARENT_SIGN_COMMON_SOURCE_NORMALIZATION_OR_FINAL_WEP_PRODUCT_QUARANTINE_4368"
DECISION = "PARENT_COMMON_SOURCE_NORMALIZATION_NOT_SIGNED_WEP_PRODUCT_FINAL_QUARANTINE_NONPRODUCT_CSRC_ROUTE_SELECTED_NONCLAIM"
NEXT_TARGET = "4369-Y5-R2FR-transition-nonproduct-Csrc-source-normalization-row-or-owner-no-wA-activation.md"

FORMAL_PATH = FORMAL / "384-PPC4161-transition-parent-sign-common-source-normalization-or-final-WEP-product-quarantine.md"
DOC_PATH = POST / "4368-Y5-R2FR-transition-parent-sign-common-source-normalization-or-final-WEP-product-quarantine.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4368_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4368_00_4367_formal": (
        FORMAL / "383-PPC4161-transition-scalar-source-normalization-gamma-beta-transfer-or-WEP-only-quarantine.md",
        "T_gamma_product=T_beta_product=0",
        "4367 conditional common-scalar gamma/beta theorem.",
    ),
    "SRC4368_01_4367_premise_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4367_PREMISE_AUDIT.csv",
        "SN4367_0_common_multiplier",
        "4367 premise audit: common multiplier is sharpened but unsigned.",
    ),
    "SRC4368_02_4367_quarantine": (
        SOURCE_DIR / "P8_Y5_R2FR_4367_WEP_ONLY_QUARANTINE.csv",
        "Q4367_0_relative_material",
        "4367 quarantine rows for relative material/source/readout WEP product.",
    ),
    "SRC4368_03_4367_transfer": (
        SOURCE_DIR / "P8_Y5_R2FR_4367_GAMMA_BETA_TRANSFER_ROWS.csv",
        "PI4367_relative_WEP_product",
        "4367 transfer table explicitly routes the relative product to WEP-only.",
    ),
    "SRC4368_04_4363_wep_product": (
        SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv",
        "PI4363_WEP_product",
        "actual source-backed product row: |Delta_w_TiPt tau_WEP| <= 2.8e-15.",
    ),
    "SRC4368_05_4178_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN.csv",
        "KGL4178_1_source_measure",
        "private source-measure normalization branch, not a global parent signature.",
    ),
    "SRC4368_06_4178_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS.csv",
        "AC4178_2_no_source_label_absorption",
        "guard forbids absorbing source labels into G.",
    ),
    "SRC4368_07_4178_reactivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_1_ZH_leak",
        "source-measure leak reopens WEP/source-normalization rows.",
    ),
    "SRC4368_08_4362_csrc_basis": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_VECTOR_BASIS.csv",
        "CSRC4362_3_epsilon_Gsrc_open",
        "non-product source/coupling drift remains an open C_src component.",
    ),
    "SRC4368_09_4362_arena_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_ARENA_PROJECTION_CONTRACT.csv",
        "ARENA4362_7_local_GR",
        "local-GR arena still requires parent graph, projections, and Bianchi/conservation closure.",
    ),
    "SRC4368_10_formal_194": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "same EH block, same Hilbert source",
        "structural GR reduction uses same EH block/Hilbert source, not hidden source labels.",
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


def activation_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "CS4368_0_parent_common_multiplier",
            "required_clause": "p_WEP is inserted before readout as one common scalar multiplier of every relevant Hilbert source density, Hamiltonian mass and PPN U definition.",
            "evidence_found": "4367 derives this as a conditional theorem only; 4367 premise audit marks the common multiplier unsigned.",
            "current_result": "BLOCKED_UNSIGNED_PARENT_CLAUSE",
            "parent_signed": "False",
            "activates_common_scalar_route": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CS4368_1_same_source_charge",
            "required_clause": "the same M_Hdress/Hilbert source charge defines Poisson U, PPN U and orbital readout without GM laundering.",
            "evidence_found": "4178/194 provide a private calibrated-source selector, but not a global parent-owned proof for the WEP product row.",
            "current_result": "PRIVATE_PACKET_CONDITIONAL_NOT_PRODUCT_ACTIVATION",
            "parent_signed": "False",
            "activates_common_scalar_route": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CS4368_2_no_relative_labels",
            "required_clause": "no material, source, test-body, species, readout or boundary/projector labels survive in p_WEP.",
            "evidence_found": "the actual 4363 row is Ti/Pt WEP product data and 4367 quarantine labels it relative/material/source/readout unless reclassified by a parent theorem.",
            "current_result": "FAILED_ON_CURRENT_PRODUCT_ROW",
            "parent_signed": "False",
            "activates_common_scalar_route": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CS4368_3_no_readout_only_origin",
            "required_clause": "p_WEP is not merely a MICROSCOPE/readout comparator product; it is carried by the parent source functional itself.",
            "evidence_found": "4363 gives a source-backed product comparator, not a parent functional that renormalizes all Hilbert sources.",
            "current_result": "BLOCKED_BY_COMPARATOR_ORIGIN",
            "parent_signed": "False",
            "activates_common_scalar_route": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CS4368_4_conservation_bianchi",
            "required_clause": "the renormalized source remains a conserved Hilbert stress compatible with the Bianchi identity.",
            "evidence_found": "4367 and 188 keep this as a private/conditional packet clause; 4362 local-GR arena still lists Bianchi/conservation closure as missing.",
            "current_result": "BLOCKED_CONSERVATION_NOT_GLOBAL",
            "parent_signed": "False",
            "activates_common_scalar_route": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "CS4368_5_nonproduct_Csrc_closed",
            "required_clause": "Xi_open, epsilon_Gsrc_open and T_open do not carry independent local-GR/PPN/Newton residuals.",
            "evidence_found": "4362 C_src basis and arena contract keep these non-product rows open.",
            "current_result": "FAILED_OPEN_NONPRODUCT_ROWS",
            "parent_signed": "False",
            "activates_common_scalar_route": "False",
            "valid_for_claim": "False",
        },
    ]


def router_rows() -> List[Dict[str, str]]:
    return [
        {
            "route_id": "ROUTE4368_common_scalar",
            "input_row": "p_WEP_TiPt reclassified as universal common Hilbert-source multiplier",
            "activation_test": "all CS4368 common-source clauses parent_signed=True",
            "current_status": "BLOCKED_UNSIGNED_AND_LABEL_CONFLICT",
            "allowed_exports_if_active": "gamma/beta zero; preferred-frame zero; Newton shape preservation",
            "forbidden_exports_now": "local-GR/PPN/Newton/source-mass claim",
            "route_active": "False",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4368_WEP_only",
            "input_row": "PI4363_WEP_product",
            "activation_test": "source-backed product comparator exists and common-source export is not parent-signed",
            "current_status": "ACTIVE_NONCLAIM",
            "allowed_exports_if_active": "WEP/source-composition product bound |Delta_w_TiPt tau_WEP| <= 2.8e-15",
            "forbidden_exports_now": "gamma/beta/alpha_i/Newton/local-GR source normalization",
            "route_active": "True",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4368_nonproduct_Csrc",
            "input_row": "Xi_open; epsilon_Gsrc_open; T_open; Delta_w_component_vector outside product comparator",
            "activation_test": "move next derivation to non-product source-normalization or owner/no-wA activation",
            "current_status": "SELECTED_NEXT_WORK",
            "allowed_exports_if_active": "explicit source-backed projection rows only after matrices/components are fixed",
            "forbidden_exports_now": "cancelling open tails with the WEP product row",
            "route_active": "True",
            "valid_for_claim": "False",
        },
        {
            "route_id": "ROUTE4368_public_claim",
            "input_row": "full local-GR/PPN/Newton pass",
            "activation_test": "common-source activation plus preferred-frame zero plus all non-product C_src/T_open closure",
            "current_status": "FORBIDDEN",
            "allowed_exports_if_active": "none in current checkpoint",
            "forbidden_exports_now": "public local-GR, PPN, WEP, Newton, clock, orbital or R10 pass",
            "route_active": "False",
            "valid_for_claim": "False",
        },
    ]


def quarantine_rows() -> List[Dict[str, str]]:
    return [
        {
            "rule_id": "Q4368_0_relative_product_default",
            "trigger": "a WEP product row carries material/source/readout labels and no parent theorem reclassifies it as common source normalization",
            "rule": "route it to WEP/source-composition only",
            "release_condition": "parent signs common scalar Hilbert-source multiplier before readout or owner/no-wA kills the row",
            "current_status": "ACTIVE",
            "claim_allowed": "False",
        },
        {
            "rule_id": "Q4368_1_no_PPN_export",
            "trigger": "attempt to use PI4363_WEP_product as gamma/beta/alpha_i transfer input",
            "rule": "reject export unless route ROUTE4368_common_scalar is activated or a source-backed T_j coefficient is supplied",
            "release_condition": "parent-signed common-source route or numeric Pi_PPN product transfer fixed before scoring",
            "current_status": "ACTIVE",
            "claim_allowed": "False",
        },
        {
            "rule_id": "Q4368_2_no_Newton_G_export",
            "trigger": "attempt to absorb relative WEP product into G_cal, M_Hdress, rho_H or U",
            "rule": "reject absorption as hidden source-label/readout dependence",
            "release_condition": "same-source-charge theorem with no labels plus calibrated coupling lock",
            "current_status": "ACTIVE",
            "claim_allowed": "False",
        },
        {
            "rule_id": "Q4368_3_no_tau_division",
            "trigger": "attempt to infer Delta_w_TiPt from |Delta_w_TiPt tau_WEP|",
            "rule": "forbid division until tau_min>0 or the source-weight row is theorem-zero",
            "release_condition": "source-backed tau_min lower bound or parent owner/no-wA zero theorem",
            "current_status": "ACTIVE",
            "claim_allowed": "False",
        },
        {
            "rule_id": "Q4368_4_no_open_tail_cancellation",
            "trigger": "attempt to use the WEP product row to cancel Xi_open, epsilon_Gsrc_open or T_open",
            "rule": "require separate projection/bound/zero row for each non-product component",
            "release_condition": "source-backed projection matrices/components or parent graph/measure/no-reentry theorem",
            "current_status": "ACTIVE",
            "claim_allowed": "False",
        },
    ]


def release_rows() -> List[Dict[str, str]]:
    return [
        {
            "release_id": "REL4368_0_parent_common_scalar",
            "would_release": "ROUTE4368_common_scalar",
            "required_input": "action-level proof that p_WEP multiplies every relevant Hilbert source entry by one common scalar before readout",
            "current_evidence": "conditional theorem only; no parent source functional",
            "met_now": "False",
            "valid_for_claim": "False",
        },
        {
            "release_id": "REL4368_1_owner_no_wA",
            "would_release": "Delta_w_component_vector and Xi_open zero route",
            "required_input": "parent-owned connected ordinary-matter action graph, measure owner and readout no-reentry",
            "current_evidence": "4362 graph signature rejected in current corpus",
            "met_now": "False",
            "valid_for_claim": "False",
        },
        {
            "release_id": "REL4368_2_source_metric_transfer",
            "would_release": "finite PPN/local-GR scoring route",
            "required_input": "source-backed Pi_PPN/Pi_GR transfer matrices for product and non-product C_src components",
            "current_evidence": "4362 arena contract lists matrices/operators as missing",
            "met_now": "False",
            "valid_for_claim": "False",
        },
        {
            "release_id": "REL4368_3_tau_min",
            "would_release": "Delta_w amplitude bound from WEP product",
            "required_input": "positive tau_WEP lower bound with official/source-backed readout and non-null alignment",
            "current_evidence": "4364-4365 keep product-only theorem; no tau division",
            "met_now": "False",
            "valid_for_claim": "False",
        },
        {
            "release_id": "REL4368_4_nonproduct_Csrc_closure",
            "would_release": "local-GR/Newton/PPN claim gate",
            "required_input": "Xi_open, epsilon_Gsrc_open and T_open bounded/projected/zeroed with Bianchi and boundary closure",
            "current_evidence": "4362 local-GR arena remains blocked",
            "met_now": "False",
            "valid_for_claim": "False",
        },
    ]


def remaining_route_rows() -> List[Dict[str, str]]:
    return [
        {
            "route_id": "NEXT4368_0_epsilon_Gsrc",
            "live_object": "epsilon_Gsrc_open",
            "why_it_matters": "this is the non-product finite source/coupling drift that can hit Newton, PPN, orbital, clock and local-GR rows",
            "best_next_move": "derive a source-normalization projection row or parent-zero it via source-measure ownership",
            "blocked_claim": "local-GR/Newton/source normalization",
            "selected": "True",
        },
        {
            "route_id": "NEXT4368_1_Xi_open",
            "live_object": "Xi_open",
            "why_it_matters": "hidden source-label/source-prefactor tails can evade the WEP product channel",
            "best_next_move": "tie Xi_open to owner/no-wA graph signatures or bound it as its own source-tail row",
            "blocked_claim": "WEP/PPN/local-GR",
            "selected": "True",
        },
        {
            "route_id": "NEXT4368_2_T_open",
            "live_object": "T_open projection basis",
            "why_it_matters": "metric, clock, EM/Poynting, orbital and boundary tails still require arena projection matrices",
            "best_next_move": "fill one source-backed Pi_arena^T row instead of reusing the WEP product",
            "blocked_claim": "PPN/clock/orbital/EM/R10/local-GR",
            "selected": "False",
        },
        {
            "route_id": "NEXT4368_3_owner_no_wA",
            "live_object": "parent ordinary-matter graph/measure/no-reentry theorem",
            "why_it_matters": "this is the cleanest zero route if the parent action can sign it",
            "best_next_move": "try one concrete graph edge or measure-owner proof, not the whole graph at once",
            "blocked_claim": "source-coupling zero route",
            "selected": "True",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4368_0_common_scalar_activation",
            "claim_tested": "activate common scalar WEP product route",
            "required_inputs": "all CS4368 parent clauses signed",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4368_1_WEP_quarantine",
            "claim_tested": "keep PI4363_WEP_product as WEP/source-composition only",
            "required_inputs": "relative labels survive and common-source route is unsigned",
            "status": "ACTIVE_NONCLAIM",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4368_2_nonproduct_route",
            "claim_tested": "continue local-GR work through non-product C_src/source-normalization rows",
            "required_inputs": "epsilon_Gsrc/Xi/T_open projections or parent-zero theorem",
            "status": "SELECTED_NEXT_WORK",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4368_3_public_local_GR",
            "claim_tested": "public local-GR/Newton/PPN pass",
            "required_inputs": "common-source activation or finite projections plus Bianchi/conservation/boundary closure",
            "status": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4368_0",
            "decision": DECISION,
            "summary": (
                "4368 attempts to activate the common-source route and rejects it in the current corpus. "
                "The theorem from 4367 remains valid conditionally, but the actual 4363 product row is "
                "Ti/Pt/source/readout-relative and cannot be exported to PPN/Newton/local-GR without a "
                "parent action proof. The WEP product is therefore quarantined as WEP-only, and the next "
                "serious local-GR route is non-product source coupling: epsilon_Gsrc_open, Xi_open, T_open, "
                "or a concrete owner/no-wA activation proof."
            ),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4368_0",
            "object": "common scalar theorem",
            "status": "PRESERVED_CONDITIONAL",
            "note": "If parent-signed, p_WEP as common Hilbert-source normalization gives zero product transfer to gamma/beta and preferred-frame rows.",
        },
        {
            "status_id": "STAT4368_1",
            "object": "actual WEP product row",
            "status": "FINAL_CURRENT_CORPUS_QUARANTINE",
            "note": "PI4363_WEP_product is WEP/source-composition only until parent reclassification or owner/no-wA zero.",
        },
        {
            "status_id": "STAT4368_2",
            "object": "local GR route",
            "status": "MOVE_TO_NONPRODUCT_CSRC",
            "note": "Do not spend the next cycle exporting the WEP product; attack epsilon_Gsrc_open/Xi_open/T_open or owner/no-wA.",
        },
        {
            "status_id": "STAT4368_3",
            "object": "public claim",
            "status": "FORBIDDEN",
            "note": "No WEP, PPN, Newton, clock, orbital, R10 or local-GR pass fires from this checkpoint.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4368_0",
            "target": NEXT_TARGET,
            "question": "Can the local-GR route be advanced through non-product source normalization or by activating one concrete owner/no-wA parent signature?",
            "preferred_route": "derive/project epsilon_Gsrc_open into Newton/PPN/source-normalization before trying to score local GR",
            "alternate_zero_route": "parent-sign a specific ordinary-matter graph/measure/no-reentry edge that kills Xi_open or Delta_w_component_vector",
            "avoid": "re-exporting the quarantined WEP product to PPN/Newton/local-GR",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    activation: List[Dict[str, str]],
    router: List[Dict[str, str]],
    quarantine: List[Dict[str, str]],
    release: List[Dict[str, str]],
    remaining: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: parent-sign common source normalization or final WEP product quarantine

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

The common-source route is mathematically sharp but not parent-signed in the current corpus. The conditional theorem survives:

```text
if p_WEP is one common scalar Hilbert-source normalization before readout,
then T_alpha1_product=T_alpha2_product=T_alpha3_product=0
and T_gamma_product=T_beta_product=0.
```

But the actual source-backed row we have is still:

```text
PI4363_WEP_product: |p_WEP_TiPt| = |Delta_w_TiPt tau_WEP| <= 2.8e-15.
```

That row carries Ti/Pt/source/readout meaning. Without a parent theorem reclassifying it as universal common source normalization, it must stay in the WEP/source-composition box. This is not a retreat; it is a router that stops us spending more checkpoints trying to smuggle a relative product into local GR.

## Exact Fork Theorem

Let `p` be the product-channel scalar. There are only two clean routes:

1. **Common-source activation.** If the parent action inserts `p` as one common scalar multiplier of the same conserved Hilbert source density and Hamiltonian mass used to define `U`, then the product is absorbed into the calibrated source charge. PPN coefficients relative to the same `U` keep their GR values, and the product-channel transfer to preferred-frame rows is zero.
2. **Relative-product quarantine.** If `p` carries material, source-label, test-body, readout, boundary/projector or non-Hilbert meaning, then it is not a source normalization. Exporting it to `gamma`, `beta`, `alpha_i`, Newton/source mass or local GR hides source dependence in `U` or `G_cal`. It remains WEP-only until a release condition is met.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Common Source Activation Audit

{md_table(activation, ["clause_id", "required_clause", "evidence_found", "current_result", "parent_signed", "activates_common_scalar_route"])}

## WEP Product Router

{md_table(router, ["route_id", "input_row", "activation_test", "current_status", "allowed_exports_if_active", "forbidden_exports_now", "route_active"])}

## Final Quarantine Rules

{md_table(quarantine, ["rule_id", "trigger", "rule", "release_condition", "current_status", "claim_allowed"])}

## Release Conditions

{md_table(release, ["release_id", "would_release", "required_input", "current_evidence", "met_now"])}

## Remaining Local-GR Routes

{md_table(remaining, ["route_id", "live_object", "why_it_matters", "best_next_move", "blocked_claim", "selected"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "valid_for_claim"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_zero_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4368: parent-sign common source normalization or final WEP product quarantine

Marker: `{MARKER}`

## What changed

- Tried to activate the clean common-source route from 4367.
- Rejected activation in the current corpus because the actual 4363 row is still Ti/Pt/source/readout-relative.
- Locked a current-corpus quarantine: `PI4363_WEP_product` is WEP/source-composition only, not a PPN/Newton/local-GR export row.
- Selected the next real route: non-product source coupling (`epsilon_Gsrc_open`, `Xi_open`, `T_open`) or one concrete owner/no-`w_A` parent signature.

## Decision row

{md_table(decisions, ["decision_id", "decision", "summary", "next_target"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_zero_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4368 Transition parent-sign common source normalization or final WEP quarantine

Marker: `{MARKER}`

4368 closes the WEP-product export loop for the current corpus. The common-source theorem remains valuable: if a future parent action makes `p_WEP` one universal Hilbert-source multiplier before readout, then the product-channel transfer to preferred-frame and gamma/beta PPN rows is zero. But the actual sourced row is still the Ti/Pt MICROSCOPE product `|Delta_w_TiPt tau_WEP| <= 2.8e-15`, which carries relative material/source/readout meaning.

So the row is quarantined as WEP/source-composition only. Local GR now has to move through non-product source coupling (`epsilon_Gsrc_open`, `Xi_open`, `T_open`) or a concrete owner/no-`w_A` parent signature, not through repeated attempts to export the WEP product into `U` or `G_cal`. Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4368 packet update: WEP product final current-corpus quarantine

Marker: `{PACKET_MARKER}`

Packet update: the WEP product is now routed cleanly. If a future parent action signs it as universal common Hilbert-source normalization, it can re-enter the local-GR branch with zero product transfer to preferred-frame and gamma/beta rows. In the current corpus it remains a Ti/Pt/source/readout product and is WEP-only. The next packet work should attack `epsilon_Gsrc_open`, `Xi_open`, `T_open`, or one concrete owner/no-`w_A` signature.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim(decisions: List[Dict[str, str]]) -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4368 attempts to parent-sign the common scalar source-normalization route and rejects activation in the current corpus. "
                "The conditional theorem remains: if p_WEP is one universal Hilbert-source multiplier before readout, product-channel transfer to gamma/beta and preferred-frame PPN rows is zero. "
                "But the actual 4363 row is the Ti/Pt/source/readout product |Delta_w_TiPt tau_WEP|<=2.8e-15, so it is quarantined as WEP/source-composition only. "
                "No PPN, Newton, local-GR, clock, orbital, R10 or WEP pass is claimed; the next route is non-product C_src source normalization or a concrete owner/no-wA parent signature."
            ),
            "4368 source register, common-source activation audit, WEP product router, final quarantine rules, release conditions, remaining local-GR routes, claim gates, decision, status, next target and validation CSV.",
            "parent_common_source_not_signed_WEP_product_final_quarantine_nonproduct_Csrc_route_nonclaim",
            "Derive/project epsilon_Gsrc_open or Xi_open into Newton/PPN/source-normalization, or parent-sign one owner/no-wA graph/measure/no-reentry edge.",
            "Exporting the relative WEP product into PPN/Newton/local GR; hiding source labels in U or G_cal; dividing by tau_WEP without tau_min; cancelling non-product C_src tails with the WEP product.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []

    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4368_SOURCE_REGISTER.csv")
    activation = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4368_COMMON_SOURCE_ACTIVATION_AUDIT.csv")
    router = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4368_WEP_PRODUCT_ROUTER.csv")
    quarantine = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4368_FINAL_QUARANTINE_RULES.csv")
    release = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4368_RELEASE_CONDITIONS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4368_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4368_0_all_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source path exists")
    add("VAL4368_1_all_needles_found", all(row["needle_found"] == "True" for row in sources), "every source needle resolves to a line")
    add(
        "VAL4368_2_common_route_blocked",
        any(row["clause_id"] == "CS4368_0_parent_common_multiplier" and row["parent_signed"] == "False" for row in activation),
        "common scalar route remains unsigned",
    )
    add(
        "VAL4368_3_relative_label_failure_present",
        any(row["clause_id"] == "CS4368_2_no_relative_labels" and row["current_result"] == "FAILED_ON_CURRENT_PRODUCT_ROW" for row in activation),
        "actual WEP row remains relative/material/source/readout",
    )
    add(
        "VAL4368_4_wep_route_active",
        any(row["route_id"] == "ROUTE4368_WEP_only" and row["route_active"] == "True" for row in router),
        "WEP-only route is active",
    )
    add(
        "VAL4368_5_common_route_not_active",
        any(row["route_id"] == "ROUTE4368_common_scalar" and row["route_active"] == "False" for row in router),
        "common-source export route is not active",
    )
    add(
        "VAL4368_6_nonproduct_route_selected",
        any(row["route_id"] == "ROUTE4368_nonproduct_Csrc" and row["route_active"] == "True" for row in router),
        "non-product C_src route selected",
    )
    add(
        "VAL4368_7_quarantine_active",
        all(row["current_status"] == "ACTIVE" for row in quarantine),
        "all quarantine rules active",
    )
    add(
        "VAL4368_8_no_release_met",
        all(row["met_now"] == "False" for row in release),
        "no release condition is met now",
    )
    add(
        "VAL4368_9_claims_forbidden",
        all(row["claim_allowed"] == "False" for row in gates),
        "claim gates remain false",
    )
    add("VAL4368_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal document marker present")
    add("VAL4368_11_post_marker", MARKER in read_text(DOC_PATH), "post-checkpoint document marker present")
    add("VAL4368_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended")
    add("VAL4368_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended")
    add("VAL4368_14_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim register row appended")
    add(
        "VAL4368_15_no_valid_claim_rows",
        all("True" not in [row.get("valid_for_claim", ""), row.get("claim_allowed", "")] for path in csv_paths for row in read_csv(path)),
        "all generated rows remain nonclaim",
    )
    add(
        "VAL4368_16_csv_parse",
        all(len(read_csv(path)) > 0 for path in csv_paths),
        "all generated CSVs parse and have rows",
    )

    return validations


def main() -> None:
    sources = source_rows()
    activation = activation_rows()
    router = router_rows()
    quarantine = quarantine_rows()
    release = release_rows()
    remaining = remaining_route_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4368_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4368_COMMON_SOURCE_ACTIVATION_AUDIT.csv": activation,
        "P8_Y5_R2FR_4368_WEP_PRODUCT_ROUTER.csv": router,
        "P8_Y5_R2FR_4368_FINAL_QUARANTINE_RULES.csv": quarantine,
        "P8_Y5_R2FR_4368_RELEASE_CONDITIONS.csv": release,
        "P8_Y5_R2FR_4368_REMAINING_LOCAL_GR_ROUTES.csv": remaining,
        "P8_Y5_R2FR_4368_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4368_DECISION.csv": decisions,
        "P8_Y5_R2FR_4368_STATUS.csv": statuses,
        "P8_Y5_R2FR_4368_NEXT_TARGET.csv": next_targets,
    }
    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, activation, router, quarantine, release, remaining, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim(decisions)

    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
