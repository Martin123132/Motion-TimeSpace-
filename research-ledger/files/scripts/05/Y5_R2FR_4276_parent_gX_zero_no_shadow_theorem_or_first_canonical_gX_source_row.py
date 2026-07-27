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

CHECKPOINT = "4276"
CLAIM_ID = "L-117"
BRANCH = "MTS_R2FR_Y5_PARENT_GX_ZERO_NO_SHADOW_THEOREM_OR_FIRST_CANONICAL_GX_SOURCE_ROW_4276"
DECISION = "TERMINAL_METRIC_ALONE_REJECTED_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW_REQUIRED"
MARKER = "PPC4161_PARENT_GX_ZERO_NO_SHADOW_THEOREM_OR_FIRST_CANONICAL_GX_SOURCE_ROW_4276"
PACKET_MARKER = "PPC4161_PACKET_PARENT_GX_ZERO_NO_SHADOW_THEOREM_OR_FIRST_CANONICAL_GX_SOURCE_ROW_4276"
NEXT_TARGET = "4277-Y5-R2FR-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"

FORMAL_PATH = FORMAL / "292-PPC4161-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md"
DOC_PATH = POST / "4276-Y5-R2FR-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4276_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4276_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CORE_BOUND_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4276_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"

ALPHA_EFF_BOUND = 0.00578792
LIVE_BLOCKER = "MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW"
LIVE_BLOCKER_C1 = "MISSING_C1_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW"
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
    "SRC4276_00_4275_formal": (
        FORMAL / "291-PPC4161-parent-cg-zero-theorem-or-ZX-cg-source-row.md",
        "MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE",
        "4275 handoff: canonical g_X is the finite invariant local coupling.",
    ),
    "SRC4276_01_4275_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4275_CANONICAL_GX_CONTRACT.csv",
        "GC4275_0_canonical_gX_contract",
        "4275 canonical g_X scoring contract.",
    ),
    "SRC4276_02_1029_chain_rule": (
        SOURCE_DIR / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
        "NST1029_1_chain_rule_zero",
        "Conditional q-factorized chain-rule zero theorem.",
    ),
    "SRC4276_03_1029_no_slot": (
        SOURCE_DIR / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
        "NST1029_2_no_extra_frame_slot",
        "No independent A_g frame slot contract.",
    ),
    "SRC4276_04_1030_matter_domain": (
        SOURCE_DIR / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
        "SPM1030_1_matter_functor_domain",
        "Matter action must have quotient/public-interface domain.",
    ),
    "SRC4276_05_1030_shadow_slot": (
        SOURCE_DIR / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
        "SPM1030_2_no_shadow_frame_slot",
        "No A_g, B_g, or vector shadow-frame slot.",
    ),
    "SRC4276_06_1031_terminal_gap": (
        SOURCE_DIR / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv",
        "TPM1031_5_terminality_insufficiency",
        "Terminal public metric alone is not an action-domain theorem.",
    ),
    "SRC4276_07_1031_verdict": (
        SOURCE_DIR / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv",
        "TPM1031_6_verdict",
        "Existing corpus has closure contract but not parent derivation.",
    ),
    "SRC4276_08_1031_counterexamples": (
        SOURCE_DIR / "P8_Y5_R10_1031_TERMINALITY_INSUFFICIENCY_COUNTEREXAMPLES.csv",
        "TC1031_0_terminal_but_functor_uses_E",
        "Counterexample blocks terminality-only proof.",
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


def theorem_gate_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "GX4276_0_define_target",
            "Canonical local geometry coupling",
            "g_X := d ln A_g/dphi_X = c_g/sqrt(Z_X)",
            "GIVEN_FROM_4275",
            "not needed",
            "False",
        ),
        (
            "GX4276_1_parent_q_kernel",
            "Parent quotient owns the vertical representative direction",
            "Dq[v_X]=0 and v_X is not an ordinary observable variation",
            "MISSING_PARENT_SIGNATURE",
            "source-backed q-kernel certificate",
            "False",
        ),
        (
            "GX4276_2_terminal_public_metric",
            "A public metric/coframe object exists",
            "e_pub=e_pub(q(Phi)) represents rods, clocks, light, free fall, and source readout",
            "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "parent ordinary-interface object class",
            "False",
        ),
        (
            "GX4276_3_matter_interface_action_domain",
            "Ordinary matter action factors through terminal public evaluation only",
            "S_matter=Sbar[Psi,Eval(e_pub(q(Phi))),theta(q)] and not Sbar[Psi,E(q),extra labels]",
            "KEY_UNSIGNED_CLAUSE",
            "parent matter-interface action-domain theorem",
            "False",
        ),
        (
            "GX4276_4_no_shadow_slots",
            "No independent Weyl/disformal/vector shadow-frame slot",
            "Allowed action excludes A_g(Xhat)e_pub, B_dis(Xhat)dX dX, and U_mu representative slots",
            "EXACT_CLOSURE_CLAUSE_NOT_DERIVED",
            "no-shadow-frame theorem or explicit source row",
            "False",
        ),
        (
            "GX4276_5_field_rename_guard",
            "No hiding g_X in constants, active source, clocks, or support shifts",
            "theta_A, alpha_EM, G_eff, T_total, support, and readout are q-owned or retained",
            "REQUIRED_GUARD_UNSIGNED",
            "constant/source/readout tail theorem or finite residual rows",
            "False",
        ),
        (
            "GX4276_6_chain_rule_zero",
            "If the signed clauses hold, the coupling vanishes",
            "Lie_vX ln A_g = D ln Abar[Dq(v_X)] = 0, or A_g is absent from the action domain",
            "CONDITIONAL_THEOREM_VALID",
            "all previous unsigned clauses",
            "False",
        ),
        (
            "GX4276_7_verdict",
            "No-shadow g_X zero theorem is not yet parent-owned",
            "terminal public metric plus matter-interface domain plus field-rename guard plus q-kernel would imply g_X=0",
            "FAIL_CURRENT_CLAIM",
            LIVE_BLOCKER,
            "False",
        ),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "clause": clause,
            "mathematical_form": mathematical_form,
            "status": status,
            "missing_for_claim": missing_for_claim,
            "parent_signed": parent_signed,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, clause, mathematical_form, status, missing_for_claim, parent_signed in raw
    ]


def countermodel_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CM4276_0_terminal_but_E_visible",
            "A terminal e_pub exists, but S_matter is evaluated on E(q) before the unique map E -> e_pub.",
            "Terminating the metric object does not force the action to forget non-terminal ordinary frames.",
            "GX4276_3_matter_interface_action_domain",
        ),
        (
            "CM4276_1_terminal_with_labels",
            "Objects carry labels or natural transformations that map to terminal labels, while S_matter depends on the labels.",
            "Source weights, constants, or marker couplings can survive terminality.",
            "GX4276_5_field_rename_guard",
        ),
        (
            "CM4276_2_frame_rename",
            "Choose e_pub as terminal and move A_g(Xhat) into masses, alpha_EM, measured G, or source normalization.",
            "A zero metric derivative can reappear as b_A, b_alpha, q_nonH, or calibration residual.",
            "GX4276_5_field_rename_guard",
        ),
        (
            "CM4276_3_kernel_not_owned",
            "The public metric is selected, but Dq-kernel directions are physical or boundary-active.",
            "Vertical representative motion can still source finite local coupling.",
            "GX4276_1_parent_q_kernel",
        ),
    ]
    return [
        {
            **common(),
            "countermodel_id": countermodel_id,
            "construction": construction,
            "what_breaks": what_breaks,
            "required_repair_gate": required_repair_gate,
            "blocks_terminality_only_proof": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for countermodel_id, construction, what_breaks, required_repair_gate in raw
    ]


def canonical_gx_schema_rows() -> List[Dict[str, str]]:
    required = [
        ("g_X", "dimensionless numeric canonical coupling", "required for finite-source route"),
        ("definition", "d ln A_g/dphi_X with phi_X canonically normalized", "prevents raw Xhat rescaling games"),
        ("units", "dimensionless", "required"),
        ("source_path", "local source file or paper path", "must exist"),
        ("source_row_id", "row/equation/theorem anchor", "must be exact"),
        ("derivation_status", "parent_signed_zero, parent_numeric, or retained_residual", "must not be placeholder"),
        ("tail_guard_status", "THEOREM_ZERO or absolute residual budget", "must close b_dis/source/readout tails"),
        ("valid_for_claim", "True only if all parent inputs are real", "False by default"),
    ]
    return [
        {
            **common(),
            "field": field,
            "meaning": meaning,
            "claim_gate": claim_gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for field, meaning, claim_gate in required
    ]


def canonical_gx_source_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "source_row_id": "GXSR4276_0_live_missing_parent_gX",
            "row_type": "canonical_gx",
            "g_X": "MISSING_PARENT_CANONICAL_GX",
            "definition": "d ln A_g/dphi_X",
            "units": "dimensionless",
            "source_path": str(FORMAL_PATH),
            "source_anchor": LIVE_BLOCKER,
            "derivation_status": "MISSING_PARENT_NUMERIC_OR_ZERO_THEOREM",
            "tail_guard_status": "MISSING_TAIL_THEOREM_ZERO_OR_ABSOLUTE_SUM",
            "control_only": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_row_id": "GXSR4276_1_zero_theorem_unsigned",
            "row_type": "zero_theorem",
            "g_X": "0.0",
            "definition": "g_X=0 if action domain excludes/factors A_g through q",
            "units": "dimensionless",
            "source_path": str(FORMAL_PATH),
            "source_anchor": "GX4276_3_matter_interface_action_domain",
            "derivation_status": "ZERO_THEOREM_UNSIGNED",
            "tail_guard_status": "MISSING_MATTER_INTERFACE_ACTION_DOMAIN",
            "control_only": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_row_id": "CTRL4276_0_gx_small_pass",
            "row_type": "canonical_gx",
            "g_X": "0.001",
            "definition": "toy canonical g_X",
            "units": "dimensionless",
            "source_path": str(FORMAL_PATH),
            "source_anchor": "control",
            "derivation_status": "CONTROL_ONLY",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_row_id": "CTRL4276_1_gx_large_fail",
            "row_type": "canonical_gx",
            "g_X": "0.01",
            "definition": "toy canonical g_X",
            "units": "dimensionless",
            "source_path": str(FORMAL_PATH),
            "source_anchor": "control",
            "derivation_status": "CONTROL_ONLY",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "source_row_id": "CTRL4276_2_zero_theorem_signed_control",
            "row_type": "zero_theorem",
            "g_X": "0.0",
            "definition": "toy signed zero theorem",
            "units": "dimensionless",
            "source_path": str(FORMAL_PATH),
            "source_anchor": "control",
            "derivation_status": "PARENT_SIGNED_ZERO_CONTROL",
            "tail_guard_status": "THEOREM_ZERO_CONTROL",
            "control_only": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def score_gx_row(row: Dict[str, str]) -> Dict[str, str]:
    out = dict(row)
    out["alpha_eff_bound"] = f"{ALPHA_EFF_BOUND:.8f}"
    out["computed_alpha_eff"] = ""
    out["passed_bound"] = "False"
    out["score_ready"] = "False"
    out["failure_modes"] = ""
    out["verdict"] = "REFUSED"

    if row.get("row_type") == "zero_theorem":
        out["computed_alpha_eff"] = "0.0"
        out["passed_bound"] = "True"
        if row.get("control_only") == "True":
            out["failure_modes"] = "CONTROL_ONLY"
            out["verdict"] = "CONTROL_ZERO_PASS_NONCLAIM"
        else:
            out["failure_modes"] = "ZERO_THEOREM_UNSIGNED"
            out["verdict"] = "ZERO_ROUTE_BLOCKED_NONCLAIM"
        return out

    gx = row.get("g_X", "")
    if not is_number(gx):
        out["failure_modes"] = "MISSING_PARENT_CANONICAL_GX_OR_ZERO_THEOREM;MISSING_TAIL_GUARD"
        out["verdict"] = "CANONICAL_GX_SOURCE_ROW_BLOCKED"
        return out

    alpha_eff = abs(float(gx))
    out["computed_alpha_eff"] = f"{alpha_eff:.8g}"
    out["passed_bound"] = str(alpha_eff <= ALPHA_EFF_BOUND)

    if row.get("control_only") == "True":
        out["failure_modes"] = "CONTROL_ONLY"
        out["verdict"] = "CONTROL_PASS_NONCLAIM" if alpha_eff <= ALPHA_EFF_BOUND else "CONTROL_FAIL_NONCLAIM"
        return out

    if row.get("tail_guard_status") != "THEOREM_ZERO" or row.get("valid_for_claim") != "True":
        out["failure_modes"] = "TAIL_GUARD_NOT_CLOSED_OR_VALID_FOR_CLAIM_FALSE"
        out["verdict"] = "NUMERIC_BUT_NONCLAIM" if alpha_eff <= ALPHA_EFF_BOUND else "NUMERIC_FAIL_NONCLAIM"
        return out

    out["score_ready"] = "True"
    out["verdict"] = "PASS_CLAIM_READY" if alpha_eff <= ALPHA_EFF_BOUND else "FAIL_CLAIM_READY"
    return out


def runner_rows() -> List[Dict[str, str]]:
    return [score_gx_row(row) for row in canonical_gx_source_rows()]


def bound_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_MATTER_INTERFACE_OR_GX_SOURCE_4276",
            "target_component": "Dq_geom",
            "norm_or_bound": "alpha_eff=abs(g_X); abs(g_X)<=0.00578792 if tail guards close",
            "numeric_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "units": "dimensionless canonical coupling",
            "filled_inputs": "terminality-only proof rejected; exact matter-interface action-domain theorem target identified",
            "missing": LIVE_BLOCKER + "; MISSING_TAIL_GUARD",
            "source_path": str(FORMAL_PATH),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def later_4277_geom_override() -> Dict[str, str]:
    path = SOURCE_DIR / "P8_Y5_R2FR_4277_DQ_COMPONENT_VALUES_CANDIDATE.csv"
    for row in csv_rows(path):
        if row.get("probe_id") == "Dq_geom" and row.get("epsilon") == "0.0" and row.get("source_path") == str(LATER_4277_FORMAL_PATH):
            return row
    return {}


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    later_geom = later_4277_geom_override()
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
                updated["epsilon"] = LIVE_BLOCKER
                updated["epsilon_C1"] = LIVE_BLOCKER_C1
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
                else LIVE_BLOCKER
                if probe == "Dq_geom"
                else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": later_geom["epsilon_C1"]
                if probe == "Dq_geom" and later_geom
                else LIVE_BLOCKER_C1
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
            "DEC4276_0_terminality_rejected",
            "Reject terminal public metric alone as a proof of g_X=0.",
            "Countermodels allow S_matter to use non-terminal frames or labels before mapping to e_pub.",
            "do not claim no-shadow theorem from terminality alone",
        ),
        (
            "DEC4276_1_real_zero_theorem_contract",
            "The real zero theorem must sign the ordinary matter-interface action domain.",
            "If S_matter factors only through Eval(e_pub(q(Phi))) and theta(q), then vertical representative motion cannot generate g_X.",
            NEXT_TARGET,
        ),
        (
            "DEC4276_2_source_row_fallback",
            "If the theorem cannot be signed, the fallback is a numeric canonical g_X source row.",
            "The source row must be parent-owned and must include b_dis/source/readout tail guards before local evidence can fire.",
            "fill canonical g_X source row or prove tail-zero theorem",
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
        ("FW4276_0_no_terminality_shortcut", "Terminal e_pub is not enough; the matter action must forget non-public frame data before evaluation."),
        ("FW4276_1_no_field_rename_escape", "A_g cannot be hidden in masses, alpha_EM, measured G, clock constants, support shifts, or source normalization."),
        ("FW4276_2_no_numeric_placeholder", "No finite g_X row may score unless the source path, source anchor, units, parent coefficient, and tail guards are real."),
        ("FW4276_3_no_local_claim", "R10, PPN, WEP, clock, orbital, Newton, EM, and local-GR claims remain false until the action-domain theorem or source row closes."),
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
            "status_id": "STATUS4276",
            "current_status": "terminality-only route rejected; exact matter-interface action-domain theorem or canonical g_X source row required",
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
            "why": "4276 proves that terminal public metric is only useful if paired with matter-interface action-domain descent; otherwise source a finite canonical g_X row.",
            "success_condition": "parent-sign S_matter=Sbar[Psi,Eval(e_pub(q(Phi))),theta(q)] with field-rename/tail guards, or provide a source-backed numeric canonical g_X row.",
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
            "4276 rejects the terminal-public-metric shortcut as a standalone g_X=0 proof. The route that survives is sharper: parent q-kernel ownership plus an ordinary matter-interface action domain "
            "S_matter=Sbar[Psi,Eval(e_pub(q(Phi))),theta(q)], no A_g/B_dis shadow slots, and no field-rename/tail escape. Without that theorem, the fallback is a source-backed canonical g_X row."
        ),
        "current_evidence": (
            "4276 source register, theorem gate, terminality countermodel audit, canonical g_X source schema and rows, runner results, updated Dq_geom candidate, decision and firewall."
        ),
        "status": "private_terminality_shortcut_rejected_matter_interface_or_gX_source_required_nonclaim",
        "next_test": "Prove the matter-interface action-domain descent with q-kernel and field-rename/tail guards, or source a finite canonical g_X row.",
        "key_risk": "Claiming g_X=0 from terminality, WEP, or covariance alone, or hiding the same coupling in constants/source/readout tails.",
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
# 292 - PPC4161 parent g_X zero no-shadow theorem or first canonical g_X source row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4276 does not claim local GR, PPN, R10, WEP, clock, orbital, Newtonian, or EM closure.

It sharpens the live blocker:

```text
old 4275 blocker: MISSING_PARENT_CANONICAL_GX_OR_NO_EXTRA_FRAME_SIGNATURE
new 4276 blocker: {LIVE_BLOCKER}
```

## What was actually derived

4275 already made the finite local target invariant:

```text
g_X := d ln A_g/dphi_X = c_g/sqrt(Z_X),
|g_X| <= 0.00578792
```

4276 tests the tempting shortcut:

```text
terminal public metric/coframe object e_pub exists
therefore no shadow frame exists
therefore g_X = 0
```

That shortcut fails. Terminality is a universal morphism property; it is not automatically an action-domain exclusion.

## Countermodel

A category can have a terminal public metric/coframe `e_pub` while ordinary matter is still evaluated as:

```text
S_A[Psi_A, E_A(q), theta_A]
```

before the unique map:

```text
E_A(q) -> e_pub
```

is applied. Then matter can still see species/readout frame data, labels, constants, support shifts, or source normalization. This permits a finite shadow coupling even though a terminal public object exists.

## Surviving theorem contract

The clean zero theorem is:

```text
Dq[v_X] = 0,
S_matter = Sbar[Psi, Eval(e_pub(q(Phi))), theta(q)],
no independent A_g(Xhat), B_dis(Xhat), U_mu shadow-frame slot,
no field-rename escape into masses, alpha_EM, G_eff, clocks, or active source,
```

then:

```text
Lie_vX ln A_g = 0,
g_X = 0,
b_dis = 0
```

up to separately signed tail guards.

This is a real derivation route, but the decisive parent clause is still unsigned:

```text
ordinary matter-interface action-domain descent.
```

## Fallback source-row route

If the theorem cannot be parent-signed, the next admissible route is a numeric canonical source row:

```text
g_X, units, definition, source_path, source_anchor, derivation_status, tail_guard_status, valid_for_claim.
```

No such claim-ready row exists in the current local corpus.

## Next target

`{NEXT_TARGET}` should attack the missing matter-interface action-domain proof directly, or fill the first source-backed canonical `g_X` row.
"""


def checkpoint_doc() -> str:
    return f"""
# 4276 - parent g_X zero no-shadow theorem or first canonical g_X source row

Marker: `{MARKER}`

Decision: `{DECISION}`

4276 rejects the lazy route:

```text
terminal metric exists => g_X=0
```

The route that survives is stronger and more precise:

```text
S_matter = Sbar[Psi, Eval(e_pub(q(Phi))), theta(q)]
```

with q-kernel ownership, no shadow-frame slots, and no field-rename/tail escape. Until that is parent-signed, `Dq_geom` is blocked by:

```text
{LIVE_BLOCKER}
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    gates = csv_rows(paths["theorem_gate"])
    countermodels = csv_rows(paths["countermodels"])
    schema = csv_rows(paths["schema"])
    source_candidates = csv_rows(paths["source_rows"])
    runners = csv_rows(paths["runner"])
    components = csv_rows(paths["local_candidate"])
    live_components = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + gates
        + countermodels
        + schema
        + source_candidates
        + runners
        + csv_rows(paths["core_bound"])
        + components
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    live_geom = [row for row in live_components if row.get("probe_id") == "Dq_geom"]
    validations = [
        ("VAL4276_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4276_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4276_2_terminality_countermodel",
            any(row["countermodel_id"] == "CM4276_0_terminal_but_E_visible" and row["blocks_terminality_only_proof"] == "True" for row in countermodels),
            "terminality-only route is explicitly countermodeled",
        ),
        (
            "VAL4276_3_key_clause_unsigned",
            any(row["gate_id"] == "GX4276_3_matter_interface_action_domain" and row["status"] == "KEY_UNSIGNED_CLAUSE" for row in gates),
            "matter-interface action-domain clause identified as key missing theorem",
        ),
        (
            "VAL4276_4_verdict_blocked",
            any(row["gate_id"] == "GX4276_7_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates),
            "no-shadow g_X zero theorem remains blocked",
        ),
        (
            "VAL4276_5_schema_written",
            any(row["field"] == "g_X" for row in schema)
            and any(row["field"] == "tail_guard_status" for row in schema),
            "canonical g_X source schema written",
        ),
        (
            "VAL4276_6_live_source_row_blocked",
            any(row["source_row_id"] == "GXSR4276_0_live_missing_parent_gX" and row["verdict"] == "CANONICAL_GX_SOURCE_ROW_BLOCKED" for row in runners),
            "live g_X source row remains blocked",
        ),
        (
            "VAL4276_7_controls_compute",
            any(row["source_row_id"] == "CTRL4276_0_gx_small_pass" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in runners)
            and any(row["source_row_id"] == "CTRL4276_1_gx_large_fail" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in runners)
            and any(row["source_row_id"] == "CTRL4276_2_zero_theorem_signed_control" and row["verdict"] == "CONTROL_ZERO_PASS_NONCLAIM" for row in runners),
            "toy controls verify bound arithmetic and zero route",
        ),
        (
            "VAL4276_8_live_4254_updated",
            bool(live_geom)
            and (
                (
                    live_geom[0].get("epsilon") == LIVE_BLOCKER
                    and live_geom[0].get("epsilon_C1") == LIVE_BLOCKER_C1
                    and live_geom[0].get("source_path") == str(FORMAL_PATH)
                )
                or (
                    live_geom[0].get("epsilon") == "0.0"
                    and live_geom[0].get("epsilon_C1") == "0.0"
                    and live_geom[0].get("source_path") == str(LATER_4277_FORMAL_PATH)
                )
            ),
            "live Dq_geom blocker sharpened to matter-interface-or-g_X-source row",
        ),
        ("VAL4276_9_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4276_10_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4276_11_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4276_12_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
        ("VAL4276_13_no_placeholder_source_claim", all(row.get("valid_for_claim", "False") == "False" for row in source_candidates), "no g_X candidate is claim-ready"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4276_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4276_SOURCE_REGISTER.csv",
        "theorem_gate": SOURCE_DIR / "P8_Y5_R2FR_4276_GX_ZERO_THEOREM_GATE.csv",
        "countermodels": SOURCE_DIR / "P8_Y5_R2FR_4276_TERMINALITY_COUNTERMODEL_AUDIT.csv",
        "schema": SOURCE_DIR / "P8_Y5_R2FR_4276_CANONICAL_GX_SOURCE_SCHEMA.csv",
        "source_rows": SOURCE_DIR / "P8_Y5_R2FR_4276_CANONICAL_GX_SOURCE_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4276_BOUND_RUNNER_RESULTS.csv",
        "core_bound": CORE_BOUND_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4276_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4276_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4276_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4276_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["theorem_gate"], theorem_gate_rows())
    write_csv(paths["countermodels"], countermodel_rows())
    write_csv(paths["schema"], canonical_gx_schema_rows())
    write_csv(paths["source_rows"], canonical_gx_source_rows())
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
        "PPC4161 4276 terminality shortcut rejected",
        "4276 rejects terminal public metric alone as a proof of `g_X=0`. The surviving route is parent matter-interface action-domain descent: `S_matter=Sbar[Psi,Eval(e_pub(q(Phi))),theta(q)]`, with q-kernel ownership, no shadow slots, and no field-rename/tail escape; otherwise a source-backed canonical `g_X` row is required.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4276 packet matter-interface action-domain gate",
        "Packet update: `Dq_geom` is now blocked by the matter-interface action-domain theorem or a source-backed canonical `g_X` row. Terminality alone is explicitly rejected as insufficient.",
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
