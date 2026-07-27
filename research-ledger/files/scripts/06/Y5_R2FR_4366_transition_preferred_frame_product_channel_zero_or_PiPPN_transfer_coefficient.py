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

CHECKPOINT = "4366"
CLAIM_ID = "L-207"
BRANCH = "MTS_R2FR_Y5_TRANSITION_PREFERRED_FRAME_PRODUCT_CHANNEL_ZERO_OR_PIPPN_TRANSFER_COEFFICIENT_4366"
MARKER = "PPC4161_TRANSITION_PREFERRED_FRAME_PRODUCT_CHANNEL_ZERO_OR_PIPPN_TRANSFER_COEFFICIENT_4366"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PREFERRED_FRAME_PRODUCT_CHANNEL_ZERO_OR_PIPPN_TRANSFER_COEFFICIENT_4366"
DECISION = "PREFERRED_FRAME_PRODUCT_CHANNEL_ZERO_THEOREM_DERIVED_CONDITIONAL_PARENT_SIGNATURES_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4367-Y5-R2FR-transition-scalar-source-normalization-gamma-beta-transfer-or-WEP-only-quarantine.md"

FORMAL_PATH = FORMAL / "382-PPC4161-transition-preferred-frame-product-channel-zero-or-PiPPN-transfer-coefficient.md"
DOC_PATH = POST / "4366-Y5-R2FR-transition-preferred-frame-product-channel-zero-or-PiPPN-transfer-coefficient.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4366_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4366_00_4365_formal": (
        FORMAL / "381-PPC4161-transition-first-product-transfer-norm-or-PiPPN-source-to-metric-row.md",
        "T_alpha3=0",
        "4365 selects preferred-frame zero or transfer coefficient as next target.",
    ),
    "SRC4366_01_4365_thresholds": (
        SOURCE_DIR / "P8_Y5_R2FR_4365_CRITICAL_TRANSFER_THRESHOLDS.csv",
        "CT4365_R7_alpha3",
        "alpha3 critical transfer threshold from WEP product bound.",
    ),
    "SRC4366_02_4365_requirements": (
        SOURCE_DIR / "P8_Y5_R2FR_4365_TRANSFER_NORM_REQUIREMENTS.csv",
        "REQ4365_2_preferred_frame_zero",
        "preferred-frame product-channel silence requirement.",
    ),
    "SRC4366_03_ppn_readout": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "alpha1 = alpha2 = alpha3 = 0",
        "private PPN readout gives zero preferred-frame rows when same-metric EH/Hilbert conservation holds.",
    ),
    "SRC4366_04_no_vector_readout": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "g_0i = GR vector-potential terms only",
        "preferred-frame PPN rows reopen if an independent vector/frame channel exists.",
    ),
    "SRC4366_05_quotient_naturality": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "source normalization",
        "source-normalization hidden dependence is already a named quotient-naturality risk.",
    ),
    "SRC4366_06_4178_reactivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_3_hidden_source_constants",
        "hidden source constants/source labels reopen source-normalization rows.",
    ),
    "SRC4366_07_4181_extra_modes": (
        SOURCE_DIR / "P8_Y5_R2FR_4181_EXTRA_MODE_SILENCE_GATES.csv",
        "XMG4181_4_disformal_scalar",
        "extra vector/disformal/shadow-frame modes reopen preferred-frame or source rows.",
    ),
    "SRC4366_08_alpha3_prior_evaluator": (
        SOURCE_DIR / "P8_ALPHA3_BOUND_PRODUCT_INPUT.csv",
        "A3_total",
        "older alpha3 product evaluator discipline: no promotion without channel zero or numeric products.",
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


def threshold_lookup() -> Dict[str, Dict[str, str]]:
    rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4365_CRITICAL_TRANSFER_THRESHOLDS.csv")
    return {row["observable"]: row for row in rows}


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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4366_0_slot_classification",
            "statement": "A source-coupling product channel can feed preferred-frame PPN rows only through a vector/frame/disformal/torsion/nonmetricity slot or through nonconserved momentum flux.",
            "proof_sketch": "The PPN preferred-frame structures are carried by independent frame vectors, non-GR g_0i potentials, anisotropic momentum flux, or conservation violation. A scalar density normalization has no free spatial/frame index.",
            "consequence": "If the product channel is scalar source-normalization only, preferred-frame transfer coefficients vanish.",
            "proof_status": "EXACT_CONDITIONAL_SLOT_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4366_1_preferred_frame_zero",
            "statement": "Under the scalar stationary Hilbert-source branch, T_alpha1_product=T_alpha2_product=T_alpha3_product=0.",
            "proof_sketch": "Same-metric EH readout gives only GR g_0i vector-potential terms; Hilbert source descent plus Bianchi conservation eliminates anomalous momentum/preferred-frame terms. The scalar product p can rescale a source density but cannot introduce a preferred-frame vector.",
            "consequence": "alpha3 bottleneck is killed on this branch before comparing to its 1.428571e-5 transfer threshold.",
            "proof_status": "CONDITIONAL_THEOREM_DERIVED_PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4366_2_stationary_Gdot_side",
            "statement": "If the product source-normalization p is branch-stationary, T_Gdot_product=0.",
            "proof_sketch": "Gdot/G receives time-dependent calibrated source/coupling drift. A fixed scalar product with D_tau p=0 has no Gdot leg; kappa_* or source-measure drift would reopen the row.",
            "consequence": "Gdot transfer can be killed by stationarity, but this is separate from preferred-frame silence.",
            "proof_status": "CONDITIONAL_SIDE_THEOREM_DERIVED_PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4366_3_not_gamma_beta",
            "statement": "Preferred-frame zero does not determine gamma or beta product transfer.",
            "proof_sketch": "A scalar source normalization can still affect scalar metric potentials or source calibration unless absorbed into a common calibrated Hilbert source. Those scalar lanes need a separate gamma/beta/source-normalization theorem.",
            "consequence": "4367 must attack scalar gamma/beta transfer or quarantine the product route to WEP-only.",
            "proof_status": "LIMIT_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def premise_rows() -> List[Dict[str, str]]:
    return [
        {
            "premise_id": "PF4366_0_scalar_slot",
            "premise": "p_WEP enters only as scalar source-normalization/rest-density factor",
            "current_status": "TARGET_SHARPENED_UNSIGNED",
            "if_missing": "Delta_w/source-label dependence can enter nonfactorized or material channels",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "PF4366_1_no_vector_frame_slot",
            "premise": "no independent vector, shadow coframe, torsion, nonmetricity or preferred frame couples to the product channel",
            "current_status": "PRIVATE_PACKET_CONDITIONAL_NOT_GLOBAL",
            "if_missing": "alpha1/alpha2/alpha3 transfer reopens",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "PF4366_2_Hilbert_conservation",
            "premise": "product channel remains inside conserved Hilbert stress/source descent",
            "current_status": "PRIVATE_PACKET_CONDITIONAL_NOT_GLOBAL",
            "if_missing": "alpha3/zeta/momentum-conservation rows reopen",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "PF4366_3_stationarity",
            "premise": "D_tau p_WEP=0 before readout and comparison",
            "current_status": "UNSIGNED",
            "if_missing": "Gdot/clock/source-drift rows reopen",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
        {
            "premise_id": "PF4366_4_no_boundary_projector_reentry",
            "premise": "boundary/projector/readout maps do not reintroduce a vector or frame label",
            "current_status": "UNSIGNED",
            "if_missing": "boundary alpha3/domain alpha3 evaluators remain live",
            "parent_signed": "False",
            "valid_for_claim": "False",
        },
    ]


def transfer_rows(thresholds: Dict[str, Dict[str, str]]) -> List[Dict[str, str]]:
    def threshold(observable: str) -> str:
        return thresholds[observable]["critical_transfer_norm"]

    return [
        {
            "transfer_id": "PI4366_alpha1_product",
            "observable": "alpha1",
            "transfer_coefficient": "T_alpha1_product",
            "conditional_value": "0",
            "critical_transfer_norm": threshold("alpha1"),
            "condition_set": "PF4366_0-2 and PF4366_4",
            "status": "CONDITIONAL_ZERO_ROW_DERIVED_NOT_PARENT_ACTIVATED",
            "actual_transfer_norm_present": "conditional_zero_only",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4366_alpha2_product",
            "observable": "alpha2",
            "transfer_coefficient": "T_alpha2_product",
            "conditional_value": "0",
            "critical_transfer_norm": threshold("alpha2"),
            "condition_set": "PF4366_0-2 and PF4366_4",
            "status": "CONDITIONAL_ZERO_ROW_DERIVED_NOT_PARENT_ACTIVATED",
            "actual_transfer_norm_present": "conditional_zero_only",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4366_alpha3_product",
            "observable": "alpha3",
            "transfer_coefficient": "T_alpha3_product",
            "conditional_value": "0",
            "critical_transfer_norm": threshold("alpha3"),
            "condition_set": "PF4366_0-2 and PF4366_4",
            "status": "CONDITIONAL_ZERO_ROW_DERIVED_NOT_PARENT_ACTIVATED",
            "actual_transfer_norm_present": "conditional_zero_only",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4366_Gdot_product",
            "observable": "Gdot_over_G",
            "transfer_coefficient": "T_Gdot_product",
            "conditional_value": "0",
            "critical_transfer_norm": threshold("Gdot_over_G"),
            "condition_set": "PF4366_0, PF4366_2, PF4366_3",
            "status": "CONDITIONAL_ZERO_ROW_DERIVED_NOT_PARENT_ACTIVATED",
            "actual_transfer_norm_present": "conditional_zero_only",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4366_gamma_product",
            "observable": "gamma_minus_1",
            "transfer_coefficient": "T_gamma_product",
            "conditional_value": "OPEN",
            "critical_transfer_norm": threshold("gamma_minus_1"),
            "condition_set": "requires scalar source-normalization absorption or explicit metric transfer",
            "status": "NOT_CLOSED_BY_PREFERRED_FRAME_THEOREM",
            "actual_transfer_norm_present": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "transfer_id": "PI4366_beta_product",
            "observable": "beta_minus_1",
            "transfer_coefficient": "T_beta_product",
            "conditional_value": "OPEN",
            "critical_transfer_norm": threshold("beta_minus_1"),
            "condition_set": "requires scalar source-normalization absorption or explicit metric self-interaction transfer",
            "status": "NOT_CLOSED_BY_PREFERRED_FRAME_THEOREM",
            "actual_transfer_norm_present": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def failure_rows() -> List[Dict[str, str]]:
    return [
        {
            "failure_id": "FAIL4366_0_vector_slot",
            "failure_mode": "product channel couples to a vector/preferred frame u^mu",
            "effect": "alpha1/alpha2/alpha3 transfer rows reopen",
            "required_response": "derive zero vector slot or fill numeric transfer coefficients below thresholds",
            "claim_allowed": "False",
        },
        {
            "failure_id": "FAIL4366_1_shadow_disformal",
            "failure_mode": "product channel enters shadow coframe, disformal scalar, torsion or nonmetricity",
            "effect": "preferred-frame and same-frame source gates reopen",
            "required_response": "parent-sign no-extra-frame action-domain clause or score finite coefficients",
            "claim_allowed": "False",
        },
        {
            "failure_id": "FAIL4366_2_nonconserved_flux",
            "failure_mode": "product channel carries nonconserved momentum or boundary flux",
            "effect": "alpha3/zeta/conservation rows reopen",
            "required_response": "prove Hilbert conservation/no-flux or fill alpha3 product evaluator rows",
            "claim_allowed": "False",
        },
        {
            "failure_id": "FAIL4366_3_time_drift",
            "failure_mode": "D_tau p_WEP != 0",
            "effect": "Gdot/clock/source-drift transfer rows reopen",
            "required_response": "prove stationarity or bound T_Gdot_product",
            "claim_allowed": "False",
        },
        {
            "failure_id": "FAIL4366_4_scalar_metric_open",
            "failure_mode": "product channel is scalar but changes gamma/beta source potentials",
            "effect": "preferred-frame zero survives but local GR/PPN still not closed",
            "required_response": "derive scalar source-normalization absorption or explicit gamma/beta transfer",
            "claim_allowed": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "run_id": "RUN4366_0_preferred_frame_zero",
            "operation": "apply scalar stationary Hilbert-source branch",
            "result": "T_alpha1=T_alpha2=T_alpha3=0 conditionally",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_ACTIVATED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4366_1_Gdot_zero",
            "operation": "apply stationarity side condition",
            "result": "T_Gdot=0 conditionally",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_ACTIVATED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4366_2_gamma_beta",
            "operation": "test whether preferred-frame theorem closes gamma/beta",
            "result": "NO",
            "status": "SCALAR_METRIC_TRANSFER_REMAINS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "run_id": "RUN4366_3_public_claim",
            "operation": "score local GR/PPN",
            "result": "NOT_SCORED",
            "status": "PARENT_SIGNATURES_AND_GAMMA_BETA_TRANSFER_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4366_0_theorem",
            "gate": "preferred-frame zero theorem",
            "requirement": "scalar stationary same-metric Hilbert source branch",
            "current_result": "PASS_CONDITIONAL_THEOREM",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4366_1_activation",
            "gate": "activate preferred-frame zero row",
            "requirement": "PF4366 premise set parent-signed",
            "current_result": "BLOCKED_UNSIGNED_PREMISES",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4366_2_gamma_beta",
            "gate": "close scalar gamma/beta transfer",
            "requirement": "source-normalization absorption or explicit T_gamma/T_beta",
            "current_result": "MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4366_3_public_claim",
            "gate": "claim PPN/local-GR pass",
            "requirement": "activated preferred-frame zero, gamma/beta transfer, conservation/Bianchi and source normalization",
            "current_result": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4366_0",
            "decision": DECISION,
            "rationale": "4366 derives the preferred-frame product-channel zero theorem: if the WEP product enters only as a stationary scalar Hilbert source-normalization and no vector/shadow/disformal/torsion/boundary/readout slot survives, then the product channel has no preferred-frame tensor structure and T_alpha1=T_alpha2=T_alpha3=0. This kills the 4365 alpha3/alpha2 bottleneck only on that branch. The premise set is not parent-signed in the current corpus, and gamma/beta scalar metric transfer remains open.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4366_0",
            "item": "preferred-frame theorem",
            "status": "DERIVED_CONDITIONAL",
            "detail": "scalar stationary Hilbert source-normalization gives T_alpha1=T_alpha2=T_alpha3=0.",
        },
        {
            "status_id": "STAT4366_1",
            "item": "parent activation",
            "status": "UNSIGNED",
            "detail": "current corpus has not parent-signed the scalar/no-vector/no-reentry premise set.",
        },
        {
            "status_id": "STAT4366_2",
            "item": "gamma beta",
            "status": "OPEN",
            "detail": "preferred-frame zero does not determine scalar metric transfer.",
        },
        {
            "status_id": "STAT4366_3",
            "item": "next target",
            "status": "SCALAR_SOURCE_NORMALIZATION_TRANSFER",
            "detail": NEXT_TARGET,
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "target_id": "NT4366_0",
            "next_target": NEXT_TARGET,
            "question": "Does the scalar WEP product source-normalization absorb into calibrated Hilbert mass/G_cal for gamma/beta, or must it be quarantined as WEP-only?",
            "preferred_route": "derive common scalar source-normalization absorption with T_gamma=T_beta=0 or below thresholds",
            "alternate_route": "fill explicit T_gamma/T_beta product-transfer coefficients",
            "fallback_route": "quarantine WEP product row from local-GR/PPN and continue via parent owner/no-wA theorem",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    premises: List[Dict[str, str]],
    transfers: List[Dict[str, str]],
    failures: List[Dict[str, str]],
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

    transfer_by_obs = {row["observable"]: row for row in transfers}
    add("VAL4366_00_sources_exist", "all cited local source paths exist", all(row["path_exists"] == "True" for row in sources), "source register path_exists flags")
    add("VAL4366_01_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needle_found flags")
    add("VAL4366_02_theorem_present", "preferred-frame zero theorem present", any(row["theorem_id"] == "TH4366_1_preferred_frame_zero" for row in theorems), "TH4366_1")
    add("VAL4366_03_alpha3_zero_row", "alpha3 conditional zero row present", transfer_by_obs["alpha3"]["conditional_value"] == "0", "PI4366_alpha3_product")
    add("VAL4366_04_alpha2_zero_row", "alpha2 conditional zero row present", transfer_by_obs["alpha2"]["conditional_value"] == "0", "PI4366_alpha2_product")
    add("VAL4366_05_gamma_beta_open", "gamma and beta remain open", transfer_by_obs["gamma_minus_1"]["conditional_value"] == "OPEN" and transfer_by_obs["beta_minus_1"]["conditional_value"] == "OPEN", "gamma/beta")
    add("VAL4366_06_premises_unsigned", "premises not parent activated", all(row["parent_signed"] == "False" for row in premises), "premise parent_signed flags")
    add("VAL4366_07_failure_modes", "vector/disformal/conservation/time/scalar failures covered", len(failures) >= 5, f"failures={len(failures)}")
    add("VAL4366_08_runner_nonclaim", "runner rows remain nonclaim", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in runner), "runner flags")
    add("VAL4366_09_activation_blocked", "activation gate blocked", any(row["gate_id"] == "GATE4366_1_activation" and row["current_result"] == "BLOCKED_UNSIGNED_PREMISES" for row in gates), "activation gate")
    add("VAL4366_10_public_claim_forbidden", "public claim forbidden", any(row["gate_id"] == "GATE4366_3_public_claim" and row["current_result"] == "FORBIDDEN" for row in gates), "claim gate")
    add("VAL4366_11_decision_nonclaim", "decision nonclaim", decisions[0]["decision"] == DECISION and decisions[0]["claim_allowed"] == "False", DECISION)
    add("VAL4366_12_next_selected", "next target selected", next_targets[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4366_13_formal_marker", "formal marker written", MARKER in read_text(FORMAL_PATH), str(FORMAL_PATH))
    add("VAL4366_14_post_doc_marker", "post doc marker written", MARKER in read_text(DOC_PATH), str(DOC_PATH))
    add("VAL4366_15_spine_marker", "spine marker appended", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4366_16_packet_marker", "packet marker appended", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4366_17_claim_register", "claim register updated", f"\n{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    return rows


def write_docs(
    sources: List[Dict[str, str]],
    theorems: List[Dict[str, str]],
    premises: List[Dict[str, str]],
    transfers: List[Dict[str, str]],
    failures: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    formal = f"""# PPC4161 transition: preferred-frame product-channel zero or PiPPN transfer coefficient

Marker: `{MARKER}`

Generated: {STAMP}

## Purpose

4365 showed that preferred-frame/momentum PPN rows are the dangerous product-transfer lanes. 4366 attacks that directly. The clean route is not a tiny fitted coefficient; it is a theorem: a scalar, stationary, same-metric Hilbert source-normalization has no independent preferred-frame vector/tensor slot.

## Conditional theorem

If the WEP product channel `p_WEP=Delta_w_TiPt tau_WEP` enters only as a scalar source-normalization/rest-density factor, remains inside conserved Hilbert stress, is stationary before readout, and no vector/shadow/disformal/torsion/boundary/readout slot survives, then:

`T_alpha1_product = T_alpha2_product = T_alpha3_product = 0`.

This kills the `alpha3` and `alpha2` bottlenecks only on that branch. It does not close gamma/beta scalar metric transfer.

## Theorem rows

{md_table(theorems, ["theorem_id", "statement", "proof_sketch", "consequence", "proof_status", "valid_for_claim"])}

## Premise audit

{md_table(premises, ["premise_id", "premise", "current_status", "if_missing", "parent_signed", "valid_for_claim"])}

## PiPPN product-transfer rows

{md_table(transfers, ["transfer_id", "observable", "transfer_coefficient", "conditional_value", "critical_transfer_norm", "condition_set", "status", "claim_allowed"])}

## Failure modes

{md_table(failures, ["failure_id", "failure_mode", "effect", "required_response", "claim_allowed"])}

## Runner

{md_table(runner, ["run_id", "operation", "result", "status", "claim_allowed"])}

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

    post_doc = f"""# 4366 - preferred-frame product-channel zero or PiPPN transfer coefficient

Marker: `{MARKER}`

Generated: {STAMP}

## Result

- Derived conditional preferred-frame zero theorem: scalar stationary Hilbert source-normalization gives `T_alpha1=T_alpha2=T_alpha3=0`.
- This kills the `alpha3/alpha2` bottleneck only if the premise set is parent-signed.
- Current corpus does not activate the theorem globally; all premise rows remain nonclaim.
- Gamma/beta scalar transfer remains open.

## Why this matters

This is the right kind of leap: not “hope alpha3 is small”, but “prove there is no preferred-frame slot”. If the branch signs, the nastiest PPN lane vanishes exactly.

## Files

- Formal checkpoint: `{FORMAL_PATH}`
- Transfer rows: `{SOURCE_DIR / "P8_Y5_R2FR_4366_PREFERRED_FRAME_TRANSFER_ROWS.csv"}`
- Premise audit: `{SOURCE_DIR / "P8_Y5_R2FR_4366_PREMISE_AUDIT.csv"}`
- Validation: `{VALIDATION_PATH}`

## Next

{NEXT_TARGET}
"""
    DOC_PATH.write_text(post_doc, encoding="utf-8")


def update_rollups() -> None:
    spine_block = f"""

## 4366 Transition preferred-frame product-channel zero theorem

Marker: `{MARKER}`

4366 attacks the `alpha3/alpha2` bottleneck from 4365. It derives the conditional slot theorem: if `p_WEP=Delta_w_TiPt tau_WEP` enters only as a scalar, stationary, same-metric Hilbert source-normalization with no vector/shadow/disformal/torsion/boundary/readout reentry, then it has no preferred-frame PPN tensor/vector slot and `T_alpha1_product=T_alpha2_product=T_alpha3_product=0`. This is the right zero route for the brutal alpha3 threshold.

The theorem is not globally activated because the scalar/no-vector/Hilbert-conservation/stationarity/no-reentry premises are not parent-signed in the current corpus. Gamma/beta scalar metric transfer also remains open. Next target: `{NEXT_TARGET}`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""

## 4366 packet update: preferred-frame product-channel zero theorem

Marker: `{PACKET_MARKER}`

Packet update: the WEP product channel no longer needs a tiny fitted alpha3 coefficient if it is parent-signed as scalar stationary Hilbert source-normalization. On that branch `T_alpha1=T_alpha2=T_alpha3=0` exactly. If any vector/frame/disformal/torsion/boundary/readout slot survives, the alpha rows reopen and must use the 4365 thresholds. Gamma/beta still need the scalar source-normalization transfer law.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)

    append_claim_once(
        FORMAL / "02-claims-register.csv",
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4366 derives the conditional preferred-frame product-channel zero theorem. If p_WEP=Delta_w_TiPt*tau_WEP enters only as a scalar, stationary, same-metric Hilbert source-normalization, remains conserved, and no vector/shadow/disformal/torsion/boundary/readout slot survives, then T_alpha1_product=T_alpha2_product=T_alpha3_product=0. This would kill the 4365 alpha3/alpha2 bottleneck exactly on that branch. The premise set is not parent-signed in the current corpus and gamma/beta scalar metric transfer remains open, so no PPN/local-GR claim fires.",
            "4366 source register, theorem rows, premise audit, preferred-frame transfer rows, failure modes, runner, claim gates, decision, status, next target and validation CSV.",
            "preferred_frame_product_channel_zero_theorem_conditional_parent_unsigned_nonclaim",
            "Derive scalar source-normalization gamma/beta transfer or quarantine the WEP product row from local-GR/PPN.",
            "Treating conditional preferred-frame zero as globally parent-signed; hiding vector/frame/disformal reentry; claiming gamma/beta/local-GR from alpha-row silence.",
        ],
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    thresholds = threshold_lookup()
    sources = source_rows()
    theorems = theorem_rows()
    premises = premise_rows()
    transfers = transfer_rows(thresholds)
    failures = failure_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_SOURCE_REGISTER.csv", sources)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_PREFERRED_FRAME_THEOREM_ROWS.csv", theorems)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_PREMISE_AUDIT.csv", premises)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_PREFERRED_FRAME_TRANSFER_ROWS.csv", transfers)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_FAILURE_MODES.csv", failures)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_RUNNER.csv", runner)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_CLAIM_GATES.csv", gates)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_DECISION.csv", decisions)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_STATUS.csv", statuses)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4366_NEXT_TARGET.csv", next_targets)

    write_docs(sources, theorems, premises, transfers, failures, runner, gates, decisions, statuses, next_targets)
    update_rollups()

    validations = validation_rows(sources, theorems, premises, transfers, failures, runner, gates, decisions, statuses, next_targets)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"4366 validation failed: {details}")

    print(f"{CHECKPOINT} generated: {DECISION}")
    print(f"formal={FORMAL_PATH}")
    print(f"validation={VALIDATION_PATH}")


if __name__ == "__main__":
    main()
