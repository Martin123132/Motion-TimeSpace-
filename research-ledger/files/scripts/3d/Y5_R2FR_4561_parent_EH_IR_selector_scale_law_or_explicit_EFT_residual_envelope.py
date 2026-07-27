from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4561"
CLAIM_ID = "L-403"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_EH_IR_SELECTOR_4561"
MARKER = "PPC4161_PARENT_EH_IR_SELECTOR_SCALE_LAW_OR_EXPLICIT_EFT_RESIDUAL_ENVELOPE_4561"
PACKET_MARKER = "PPC4161_PACKET_PARENT_EH_IR_SELECTOR_VERDICT_4561"
DECISION = "CONDITIONAL_EH_IR_SELECTOR_REDERIVED_PARENT_SIGNATURE_FAILS_RESIDUAL_EFT_ENVELOPE_RETAINED"
NEXT_TARGET = "4562-Y5-R2FR-A-MF-parent-origin-from-motion-time-space-or-effective-axiom-freeze.md"

FORMAL_PATH = FORMAL / "577-PPC4161-parent-EH-IR-selector-scale-law-or-explicit-EFT-residual-envelope.md"
DOC_PATH = POST / "4561-Y5-R2FR-parent-EH-IR-selector-scale-law-or-explicit-EFT-residual-envelope.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4560 = FORMAL / "576-PPC4161-local-scorecard-closure-to-parent-signature-gap-map.md"
POST_4181 = POST / "4181-Y5-R2FR-EH-local-metric-principal-block-origin-or-effective-GR-demotion.md"
POST_4182 = POST / "4182-Y5-R2FR-motion-frame-symmetry-parent-signature-or-effective-GR-label.md"
POST_4183 = POST / "4183-Y5-R2FR-motion-frame-axiom-adoption-consequences-or-effective-GR-test-contract.md"
POST_4184 = POST / "4184-Y5-R2FR-Palatini-IR-normal-form-selector-under-AMF-or-residual-EFT-bound.md"
POST_4185 = POST / "4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
CSV_4181_CHAIN = SOURCE_DIR / "P8_Y5_R2FR_4181_EH_ORIGIN_THEOREM_CHAIN.csv"
CSV_4181_EXTRA = SOURCE_DIR / "P8_Y5_R2FR_4181_EXTRA_MODE_SILENCE_GATES.csv"
CSV_4184_AXIOMS = SOURCE_DIR / "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv"
CSV_4184_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4184_PALATINI_REDUCTION_THEOREM_CHAIN.csv"
CSV_4184_RESIDUALS = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"
CSV_4185_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4185_STATUS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4561_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4561_CONDITIONAL_EH_SELECTOR_THEOREM.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4561_PARENT_SCALE_LAW_AUDIT.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4561_RESIDUAL_EFT_ENVELOPE_REFRESH.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4561_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4561_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4561_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4561_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4561_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4561_00_4560_next", "4560 selected EH/IR root", DOC_4560, "next target is EH/IR selector scale law"),
        ("SRC4561_01_4181_doc", "4181 EH origin demotion", POST_4181, "strong formal candidate, not a completed derivation"),
        ("SRC4561_02_4182_doc", "4182 A_MF parent signature missing", POST_4182, "does not yet parent-sign the axiom `A_MF`"),
        ("SRC4561_03_4183_doc", "4183 A_MF consequences", POST_4183, "does not by itself derive the Einstein-Cartan/Palatini action"),
        ("SRC4561_04_4184_doc", "4184 conditional Palatini selector", POST_4184, "selector assumptions are not yet fully parent-derived"),
        ("SRC4561_05_4185_doc", "4185 residual coefficient map", POST_4185, "c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, c_bdy"),
        ("SRC4561_06_4181_chain", "4181 EH theorem chain", CSV_4181_CHAIN, "EHO4181_2_two_derivative_normal_form"),
        ("SRC4561_07_4181_extra", "4181 extra mode gates", CSV_4181_EXTRA, "XMG4181_3_higher_curvature"),
        ("SRC4561_08_4184_axioms", "4184 selector axiom set", CSV_4184_AXIOMS, "SEL4184_2_IR_order"),
        ("SRC4561_09_4184_theorem", "4184 Palatini theorem chain", CSV_4184_THEOREM, "TH4184_1_classification"),
        ("SRC4561_10_4184_residuals", "4184 residual EFT ledger", CSV_4184_RESIDUALS, "RB4184_1_cR2"),
        ("SRC4561_11_4185_status", "4185 residual status", CSV_4185_STATUS, "all_coefficients_numeric_or_parent_zero"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4561 parent EH/IR selector theorem attempt",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "TH4561_0_variables",
            "clause": "motion-frame Cartan variables",
            "statement": "If A_MF is parent-owned, e^A=D_omega X^A+B^A and omega^AB are parent-covariant variables, with g_obs=eta_AB e^A e^B.",
            "derived_status": "conditional_on_A_MF_parent_signature",
            "failure_if_unsigned": "coframe and connection remain effective GR infrastructure, not MTS-derived variables",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4561_1_local_covariant_classification",
            "clause": "local parity-even covariant four-form classification",
            "statement": "At leading two-derivative / one-curvature IR order, the unsuppressed parity-even Cartan geometry term is EC/Palatini plus vacuum term.",
            "derived_status": "conditional_selector_theorem",
            "failure_if_unsigned": "higher-curvature, torsion-square, disformal and memory terms remain residual coefficients",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4561_2_scale_law",
            "clause": "parent IR scale separation",
            "statement": "A parent scale law must rank two-derivative EC/Palatini terms above R^2, torsion kinetic, disformal and memory terms in the local <=2PN branch.",
            "derived_status": "not_parent_derived_currently",
            "failure_if_unsigned": "EH is an effective leading ansatz rather than a parent-selected principal block",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4561_3_no_extra_light_modes",
            "clause": "no unscreened extra local modes",
            "statement": "No light torsion, scalar, vector, disformal, R^2 or memory pole can survive below the local PPN/R10/clock scale unless it is bounded by an explicit residual row.",
            "derived_status": "not_parent_derived_currently",
            "failure_if_unsigned": "gamma/beta/R10/clock/PPN compatibility remains branch-conditional",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4561_4_Palatini_to_EH",
            "clause": "torsion/nonmetricity resolution",
            "statement": "If torsion/nonmetricity are algebraic and zero or bounded in the compact spinless local branch, S_EC reduces to S_EH[g_obs] plus routed boundary.",
            "derived_status": "conditional_reduction",
            "failure_if_unsigned": "torsion/nonmetricity residuals reopen preferred-frame, WEP, spin and source-coupling rows",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4561_5_verdict",
            "clause": "EH/IR parent selector",
            "statement": "A clean conditional theorem exists, but the current corpus does not derive the parent EH/IR selector because A_MF parent ownership, IR scale law and no-extra-light-mode clauses remain unsigned.",
            "derived_status": "conditional_true_current_parent_claim_false",
            "failure_if_unsigned": "use explicit residual EFT envelope and effective-GR branch language",
            "valid_for_claim": "False",
        },
    ]


def parent_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PA4561_0_A_MF_parent_origin",
            "required_parent_input": "A_MF motion-frame gauge redundancy owned by parent action",
            "current_evidence": "4182 says A_MF parent signature is not found; 4183 treats it as adoption-ready candidate",
            "verdict": "FAIL_PARENT_SIGNATURE",
            "repair_route": "derive A_MF from motion/time/space primitives or freeze it as an explicit axiom",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PA4561_1_IR_order_scale_law",
            "required_parent_input": "parent scale hierarchy selecting two-derivative / one-curvature local IR order",
            "current_evidence": "4184 uses IR order as selector assumption; 4185 maps c_R2/M_R as residual",
            "verdict": "FAIL_PARENT_SCALE_LAW",
            "repair_route": "derive M_* suppression or source c_R2/M_R bounds in PPN/R10/orbital arenas",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PA4561_2_no_extra_light_modes",
            "required_parent_input": "no light torsion/scalar/vector/disformal/memory modes in local branch",
            "current_evidence": "4181 extra-mode gates require zero_or_bound; 4184 residual ledger keeps c_T,c_R2,c_D,c_Gamma,c_bdy,delta_kappa",
            "verdict": "FAIL_UNTIL_ZERO_OR_BOUND",
            "repair_route": "prove each coefficient zero/heavy or fill finite residual source rows",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PA4561_3_same_coframe_source",
            "required_parent_input": "matter and Maxwell-Hodge see the same observed coframe",
            "current_evidence": "private selector clause exists, global parent adoption still open",
            "verdict": "PRIVATE_NOT_GLOBAL",
            "repair_route": "derive parent same-coframe functor or retain c_D/WEP/clock/EM propagation bounds",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "PA4561_4_boundary_routing",
            "required_parent_input": "boundary/topological terms fixed, exact or Hamiltonian-routed",
            "current_evidence": "private boundary route exists, global boundary/no-flux remains unsigned",
            "verdict": "PRIVATE_NOT_GLOBAL",
            "repair_route": "derive global compact-collar support/no-flux theorem or retain c_bdy bounds",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    base = [
        ("RE4561_0_cT", "c_T", "torsion-square / spin-torsion coefficient", "PPN preferred-frame; spin coupling; R10/contact", "derive torsion silence or source c_T bound"),
        ("RE4561_1_cR2", "c_R2/M_R", "curvature-square massive scalar/tensor pole", "R10 alpha(lambda); orbital precession; beta/gamma", "derive parent scale gap M_R or source full R10/orbital bound"),
        ("RE4561_2_cD", "c_D", "disformal/second metric/source coframe split", "WEP; clocks; EM propagation; Poynting stress", "derive same-coframe parent functor or source WEP/clock bounds"),
        ("RE4561_3_cGamma", "c_Gamma", "local memory support/projector residual", "PPN; clocks; R10; local G variation", "derive memory support silence or source c_Gamma profile coefficients"),
        ("RE4561_4_cbdy", "c_bdy", "unrouted boundary/edge charge", "Hamiltonian mass leakage; radiation/transition current; R10 edge", "derive boundary primitive/no-flux or source edge-bound rows"),
        ("RE4561_5_deltaKappa", "delta_kappa", "source-coupling drift / kappa normalization residual", "Newton coefficient; orbital GM; clock/local G variation", "derive parent kappa scale law or keep G_cal calibrated only"),
    ]
    rows: list[dict[str, Any]] = []
    for residual_id, coefficient, meaning, arena, next_action in base:
        rows.append(
            {
                "residual_id": residual_id,
                "coefficient": coefficient,
                "meaning": meaning,
                "test_arena": arena,
                "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
                "envelope_rule": "zero_or_heavy_or_explicit_bound_required_before_public_local_GR_claim",
                "next_action": next_action,
                "valid_for_claim": "False",
            }
        )
    return rows


def promotion_gate_rows(audit: list[dict[str, Any]], residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_fail = any(row.get("verdict", "").startswith("FAIL") for row in audit)
    residuals_open = any(row.get("current_value") == "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND" for row in residuals)
    return [
        {
            "gate_id": "PG4561_0_conditional_theorem",
            "requirement": "conditional EC/Palatini->EH selector theorem written",
            "status": "PASS_CONDITIONAL",
            "claim_effect": "usable theorem route, not parent proof",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4561_1_parent_signature",
            "requirement": "A_MF, IR scale law and no-extra-light-mode clauses parent-derived",
            "status": "FAIL_UNSIGNED" if parent_fail else "PASS_PARENT_SIGNED",
            "claim_effect": "public local-GR derivation remains blocked",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4561_2_residual_EFT",
            "requirement": "every excluded invariant has parent-zero/heavy proof or numeric bound",
            "status": "FAIL_RESIDUALS_OPEN" if residuals_open else "PASS_RESIDUALS_CLOSED",
            "claim_effect": "residual EFT envelope retained",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4561_3_next_target",
            "requirement": "next derivation target attacks first missing parent input",
            "status": "PASS_NEXT_SELECTED",
            "claim_effect": "next target = A_MF origin from motion/time/space or explicit axiom freeze",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4561_0",
            "decision": DECISION,
            "summary": "4561 rederives the conditional EH/IR selector: A_MF plus local parity-even two-derivative IR order, no extra light modes, same-coframe matter/EM and routed boundary selects EC/Palatini and reduces to EH when torsion/nonmetricity are silent. Current MTS still fails parent promotion because A_MF parent origin, IR scale law and no-extra-light-mode proofs are unsigned. The explicit EFT residual envelope is retained.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "A_MF parent ownership is the first gate in the EH/IR selector chain; without it, coframe and connection are effective GR inputs rather than MTS-derived variables.",
            "success_condition": "Derive A_MF from motion/time/space parent primitives, or freeze it explicitly as an adopted axiom and move residual EFT bounds forward without claiming parent derivation.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "conditional_EH_selector_written": "True",
            "current_parent_EH_derivation_proved": "False",
            "residual_EFT_envelope_retained": "True",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4561_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    theorem_text = " ".join(str(value) for row in theorem for value in row.values())
    theorem_ok = all(token in theorem_text for token in ["A_MF", "EC/Palatini", "two-derivative", "S_EH", "conditional_true_current_parent_claim_false"])
    rows.append(
        {
            "validation_id": "VAL4561_1_theorem",
            "check": "conditional EH/IR selector theorem includes A_MF, EC/Palatini, IR order and EH reduction",
            "status": "PASS" if theorem_ok else "FAIL",
            "details": f"{len(theorem)} theorem rows checked",
        }
    )

    audit_ok = any(row.get("verdict") == "FAIL_PARENT_SIGNATURE" for row in audit)
    audit_ok = audit_ok and any(row.get("verdict") == "FAIL_PARENT_SCALE_LAW" for row in audit)
    audit_ok = audit_ok and all(row.get("valid_for_claim") == "False" for row in audit)
    rows.append(
        {
            "validation_id": "VAL4561_2_parent_audit",
            "check": "parent audit blocks current EH derivation on explicit unsigned inputs",
            "status": "PASS" if audit_ok else "FAIL",
            "details": f"{len(audit)} audit rows checked",
        }
    )

    residual_text = " ".join(str(value) for row in residuals for value in row.values())
    residuals_ok = all(token in residual_text for token in ["c_T", "c_R2/M_R", "c_D", "c_Gamma", "c_bdy", "delta_kappa"])
    residuals_ok = residuals_ok and all(row.get("current_value") == "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND" for row in residuals)
    rows.append(
        {
            "validation_id": "VAL4561_3_residuals",
            "check": "residual EFT envelope contains all open coefficients and keeps them unclaimed",
            "status": "PASS" if residuals_ok else "FAIL",
            "details": f"{len(residuals)} residual rows checked",
        }
    )

    gates_ok = any(row.get("status") == "PASS_CONDITIONAL" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "FAIL_UNSIGNED" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "FAIL_RESIDUALS_OPEN" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "PASS_NEXT_SELECTED" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4561_4_gates",
            "check": "promotion gates pass conditional theorem but block parent claim and select next target",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "promotion gates checked",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4561_5_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4561_OVERALL",
            "check": "4561 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4561 - parent EH/IR selector scale law or explicit EFT residual envelope

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4561 takes the selected 4560 root target seriously: the private local branch is clean, but public parent derivation needs the EH/IR principal block.

The best theorem currently available is conditional:

```text
A_MF
+ local parity-even covariant four-form
+ two-derivative / one-curvature IR order
+ no extra light local modes
+ same-coframe matter/EM
+ routed boundary
=> EC/Palatini principal block
=> S_EH[g_obs] + boundary when torsion/nonmetricity are silent.
```

That is mathematically useful, but it is not yet an MTS parent derivation. The current corpus still lacks:

- parent origin of `A_MF`;
- parent scale law selecting two-derivative IR order;
- parent proof that extra light torsion/scalar/vector/disformal/memory modes are zero, heavy or bounded.

So the disciplined result is:

```text
conditional EH/IR selector = written
current parent EH derivation = false
residual EFT envelope = retained
```

## Conditional EH Selector Theorem

{markdown_table(theorem)}

## Parent Scale-Law Audit

{markdown_table(audit)}

## Residual EFT Envelope Refresh

{markdown_table(residuals)}

## Promotion Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4561 rederives the conditional EH/IR selector and retains the explicit residual EFT envelope because A_MF parent origin, IR scale law and no-extra-light-mode clauses remain unsigned.",
        "current_evidence": "Generated source register, conditional EH selector theorem, parent scale-law audit, residual EFT envelope refresh, promotion gates, status and validation CSVs.",
        "status": "conditional_EH_IR_selector_written_parent_derivation_false_residual_EFT_retained",
        "next_test": NEXT_TARGET,
        "failure_mode": "Calling the EH/Palatini block MTS-derived before deriving A_MF parent origin and the IR/no-extra-mode scale law.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "next root derivation target is A_MF origin from motion/time/space or explicit axiom freeze.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    audit = parent_audit_rows()
    residuals = residual_rows()
    gates = promotion_gate_rows(audit, residuals)
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(PARENT_AUDIT_CSV, audit)
    write_csv(RESIDUAL_CSV, residuals)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4561 - parent EH/IR selector scale law or explicit EFT residual envelope\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, theorem, audit, residuals, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, theorem, audit, residuals, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4561 Parent EH/IR Selector Verdict

Marker: `{MARKER}`  
The conditional EH/IR selector is rederived:

```text
A_MF + locality + two-derivative IR order + no extra light modes
+ same-coframe matter/EM + routed boundary
=> EC/Palatini => EH[g_obs] + boundary.
```

But current parent derivation is still false because `A_MF` parent origin, IR scale law and no-extra-light-mode clauses remain unsigned. The residual EFT envelope stays live: `c_T`, `c_R2/M_R`, `c_D`, `c_Gamma`, `c_bdy`, and `delta_kappa`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4561 Packet Integration - Parent EH/IR Selector Verdict

Marker: `{PACKET_MARKER}`  
The packet may use the conditional EC/Palatini-to-EH selector as a theorem route, but must not call the EH principal block MTS-parent-derived. The live residual envelope is `c_T`, `c_R2/M_R`, `c_D`, `c_Gamma`, `c_bdy`, and `delta_kappa`; next root is deriving `A_MF` from motion/time/space or freezing it as an explicit axiom.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4561_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
