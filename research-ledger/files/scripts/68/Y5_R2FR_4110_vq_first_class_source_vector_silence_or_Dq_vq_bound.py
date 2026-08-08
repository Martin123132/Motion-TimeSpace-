from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4110-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_VQ_BQWEYL_GATE_4110"
CHECKPOINT_ID = "4110"
DECISION = (
    "VQ_SOURCE_VECTOR_DECOMPOSED_BQWEYL_INDEX_THEOREM_CONDITIONAL_"
    "FINITE_PACK_STAGED_Q_OPERATOR_NORMALIZATION_NEXT"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4110_00_4109_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4109_NEXT_TARGET.csv",
        "4110-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md",
        "4109 selects v_q first-class/source-vector silence as the next gate.",
    ),
    "SRC4110_01_3605_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3605_VQ_FIRST_CLASS_SOURCE_SILENCE_THEOREM.csv",
        "VQ3605_4_source_silence_bound_law",
        "3605 derives the v_q source-vector decomposition and bound law.",
    ),
    "SRC4110_02_3605_decomposition": (
        SOURCE_DIR / "P8_Y5_R2FR_3605_VQ_SOURCE_VECTOR_DECOMPOSITION.csv",
        "VQR3605_3_E_BqWeyl",
        "3605 identifies BqWeyl as the first dangerous v_q source-vector component.",
    ),
    "SRC4110_03_3605_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3605_DQ_VQ_BOUND_ROWS.csv",
        "VQB3605_11_Ax_transfer",
        "3605 gives v_q leak rows feeding A_X.",
    ),
    "SRC4110_04_3605_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3605_STATUS.csv",
        "VQ_FIRST_CLASS_SOURCE_SILENCE_NOT_LIVE_BQWEYL_NEXT",
        "3605 status keeps v_q active and selects BqWeyl.",
    ),
    "SRC4110_05_3606_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_NO_SPURION_THEOREM.csv",
        "BQW3606_3_spurion_necessity",
        "3606 proves the one-Weyl index lemma and spurion necessity.",
    ),
    "SRC4110_06_3606_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_BOUND_ROWS.csv",
        "BQB3606_8_E_BqWeyl_total",
        "3606 gives the finite BqWeyl bound law.",
    ),
    "SRC4110_07_3606_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_COUNTERMODEL_GUARDS.csv",
        "BQG3606_3_quadratic_weyl",
        "3606 records spurion/projector/hidden-frame/quadratic Weyl guards.",
    ),
    "SRC4110_08_3607_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_3607_BQWEYL_PARENT_SIGNATURE_AUDIT.csv",
        "PSA3607_7_verdict",
        "3607 audits and rejects current parent-signing of no-Weyl-spurion route.",
    ),
    "SRC4110_09_3607_acquisition": (
        SOURCE_DIR / "P8_Y5_R2FR_3607_BQWEYL_FINITE_ACQUISITION_ROWS.csv",
        "BACQ3607_11_acceptance_rule",
        "3607 stages the finite BqWeyl acquisition pack.",
    ),
    "SRC4110_10_3607_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3607_STATUS.csv",
        "BQWEYL_PARENT_SIGNATURE_FAILED_FINITE_INPUT_PACK_STAGED",
        "3607 status identifies q-operator normalization as shared bottleneck.",
    ),
    "SRC4110_11_3607_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3607_NEXT_TARGET.csv",
        "3608-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md",
        "3607 selects q-operator normalization as next target.",
    ),
    "SRC4110_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4110_vq_first_class_source_vector_silence_or_Dq_vq_bound.py",
        "Reproducible generator for this 4110 checkpoint.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def row_base() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def source_register_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "source_id": source_id,
            "source_type": "local_checkpoint_or_generator",
            "path_or_url": str(path),
            "needle": needle,
            "role": role,
            "exists": bool_string(path.exists()),
            "contains_needle": bool_string(path.exists() and needle in read_text(path)),
            "valid_for_claim": "False",
        }
        for source_id, (path, needle, role) in LOCAL_SOURCES.items()
    ]


def vq_source_rows() -> List[dict]:
    entries = [
        (
            "VQ4110_0_first_class",
            "first-class v_q route",
            "Dq[v_q]=0 if v_q is generated by a differentiable first-class G_q with proper charge, bracket closure, degree count and matter/readout descent",
            "strong route but not parent-owned",
            "CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "SRC4110_01_3605_theorem",
        ),
        (
            "VQ4110_1_constraint_first",
            "constraint-first elimination route",
            "Dq[v_q]=0 if q_private is eliminated by parent constraint/auxiliary equation before q, matter and readout are formed",
            "would remove v_q as a physical source direction",
            "CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "SRC4110_01_3605_theorem",
        ),
        (
            "VQ4110_2_source_vector",
            "q source-vector normal form",
            "E_q=L_q q+B_qRic R_Ricci+B_qW C_Weyl+C_qT T_H+epsilon_q_source sigma_source+Q_q_body delta_body+Pi_q delta_boundary+tail_q",
            "all v_q source-silence channels are explicit",
            "EXACT_SOURCE_VECTOR_DECOMPOSITION",
            "SRC4110_01_3605_theorem",
        ),
        (
            "VQ4110_3_bound_law",
            "epsilon_Dq_vq",
            "epsilon_Dq_vq <= E_first_class + E_BqWeyl + E_CqT + E_q_source + E_body + E_boundary + E_readout + E_tail + E_norm",
            "failed verticality becomes a no-cancellation bound vector",
            "EXACT_BOUND_LAW_NONCLAIM",
            "SRC4110_03_3605_bounds",
        ),
        (
            "VQ4110_4_BqWeyl_priority",
            "E_BqWeyl",
            "first dangerous v_q component because Weyl/tidal curvature survives local exterior vacuum",
            "this is the correct first source-vector row to attack",
            "FIRST_DANGEROUS_COMPONENT",
            "SRC4110_04_3605_status",
        ),
        (
            "VQ4110_5_AX_transfer",
            "epsilon_AX_from_vq",
            "||dYbar|| epsilon_Dq_vq + E_Y",
            "v_q leakage feeds A_X, then C_M/C_shape, ell_J and G_eff",
            "TRANSFER_ROW_NONCLAIM",
            "SRC4110_03_3605_bounds",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "piece": piece,
            "formula_or_condition": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, piece, formula, meaning, status, source_key in entries
    ]


def bqweyl_rows() -> List[dict]:
    entries = [
        (
            "BQW4110_0_metric_trace",
            "one-Weyl metric trace lemma",
            "any scalar linear in C_abcd formed only from metric contractions vanishes because Weyl is trace-free",
            "strong algebraic zero for metric-only one-Weyl terms",
            "PASS_EXACT_LEMMA",
            "SRC4110_05_3606_theorem",
        ),
        (
            "BQW4110_1_epsilon_trace",
            "one-Weyl epsilon lemma",
            "epsilon^{abcd}C_abcd also vanishes; parity-odd scalar curvature begins at quadratic order C*Cdual",
            "no single-Weyl pseudoscalar loophole",
            "PASS_EXACT_LEMMA",
            "SRC4110_05_3606_theorem",
        ),
        (
            "BQW4110_2_spurion_necessity",
            "linear Weyl countermodel",
            "nonzero linear Weyl scalar requires q P^{abcd} C_abcd, with P a Weyl-type spurion/projector/readout tensor",
            "BqWeyl is zero only if the parent object language forbids P^{abcd}",
            "EXACT_CONDITIONAL_THEOREM",
            "SRC4110_05_3606_theorem",
        ),
        (
            "BQW4110_3_parent_signature",
            "Z_BqWeyl_linear",
            "no-Weyl-spurion route is not parent-signed: typed grammar, object-language exhaustion, q representation, hidden-frame and curvature-morphism exclusions are missing",
            "do not promote BqWeyl=0",
            "ZERO_THEOREM_NOT_ACTIVATED",
            "SRC4110_08_3607_signature",
        ),
        (
            "BQW4110_4_finite_law",
            "E_BqWeyl",
            "E_BqWeyl[arena] <= tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl|| plus boundary/source tails",
            "finite route exists but input pack is incomplete",
            "FINITE_BOUND_LAW_READY_INPUTS_MISSING",
            "SRC4110_06_3606_bounds",
        ),
        (
            "BQW4110_5_quadratic_guard",
            "D_qWeyl2",
            "linear BqWeyl zero does not kill q C_abcd C^abcd, q C*Cdual or hidden curvature towers",
            "quadratic Weyl remains separate guard",
            "PASS_GUARD",
            "SRC4110_07_3606_guards",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "piece": piece,
            "formula_or_condition": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, piece, formula, meaning, status, source_key in entries
    ]


def acquisition_rows() -> List[dict]:
    entries = [
        ("ACQ4110_0_Z_linear", "Z_BqWeyl_linear", "zero switch for linear BqWeyl absence", "ZERO_SWITCH_NOT_LIVE", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_1_BqWeyl", "B_qWeyl", "parent coefficient for q P*C or equivalent q-Weyl mixing", "REQUIRED_FIRST_DANGEROUS", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_2_Zq", "Z_q_or_G_q", "q kinetic/operator normalization or Green response", "REQUIRED_SHARED_Q_OPERATOR", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_3_Mq", "M_q^2_or_lambda_q", "q range/mass gap for local/Yukawa response", "REQUIRED_IF_NOT_MASSLESS", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_4_CWeyl", "C_Weyl_local_profile", "local Weyl/tidal curvature profile entering G_q C_Weyl", "REQUIRED_PROFILE_INPUT", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_5_tau_R10", "tau_BqWeyl_R10", "projection into R10/short-range branch", "REQUIRED_ARENA_PROJECTION", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_6_tau_PPN", "tau_BqWeyl_PPN", "projection into PPN residuals", "REQUIRED_ARENA_PROJECTION", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_7_tau_clock", "tau_BqWeyl_clock", "projection into clock/redshift drift", "REQUIRED_ARENA_PROJECTION", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_8_tau_orbital", "tau_BqWeyl_orbital", "projection into orbital/source-GM residual", "REQUIRED_ARENA_PROJECTION", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_9_DqWeyl2", "D_qWeyl2", "quadratic Weyl/higher-curvature guard", "SEPARATE_GUARD_REQUIRED", "SRC4110_09_3607_acquisition"),
        ("ACQ4110_10_acceptance", "E_BqWeyl_acceptance", "E_BqWeyl can leave epsilon_Dq_vq only by zero switch or complete finite row pack", "ACCEPTANCE_GATE", "SRC4110_09_3607_acquisition"),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, definition, status, source_key in entries
    ]


def promotion_gate_rows() -> List[dict]:
    entries = [
        ("PROM4110_0_vq_route", "v_q first-class/constraint route", "PASS_CONDITIONAL_THEOREM", "would prove Dq[v_q]=0 if parent-owned"),
        ("PROM4110_1_vq_claim", "current Dq[v_q]=0 claim", "FAIL_CURRENT_CLAIM", "first-class/source-silence package is not live"),
        ("PROM4110_2_index_lemma", "one-Weyl index theorem", "PASS_EXACT_LEMMA", "metric/epsilon-only single Weyl scalar vanishes"),
        ("PROM4110_3_BqWeyl_zero", "BqWeyl zero claim", "FAIL_CURRENT_CLAIM", "no-spurion parent signature is unsigned"),
        ("PROM4110_4_finite_pack", "finite BqWeyl scoring", "FAIL_CURRENT_CLAIM", "BqWeyl, Z_q/G_q, C_Weyl profile and arena projections are missing"),
        ("PROM4110_5_DqWeyl2", "quadratic Weyl guard", "PASS_GUARD", "linear theorem does not remove D_qWeyl2"),
        ("PROM4110_6_local_vacuum", "local vacuum shortcut", "PASS_GUARD", "Weyl/tidal curvature survives exterior vacuum"),
        ("PROM4110_7_Newton_GR", "local-GR/Newton promotion", "FAIL_CURRENT_CLAIM", "epsilon_Dq_vq and E_BqWeyl remain active"),
        ("PROM4110_8_next", "q operator normalization", "PASS_ROUTE_SELECTED", "Z_q/G_q is shared by BqWeyl and D_qWeyl2 finite routes"),
    ]
    return [
        {
            **row_base(),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status, detail in entries
    ]


def decision_rows() -> List[dict]:
    entries = [
        (
            "DEC4110_0_vq",
            "keep v_q as highest-priority vertical candidate",
            "it is the first q-map direction feeding A_X and source coupling, but not certified vertical",
            "epsilon_Dq_vq remains active",
            "VQ_CANDIDATE_RETAINED_NONCLAIM",
            "SRC4110_04_3605_status",
        ),
        (
            "DEC4110_1_BqWeyl",
            "retain BqWeyl index theorem but block zero claim",
            "the single-Weyl algebra is strong, but no-spurion parent signature is missing",
            "Z_BqWeyl_linear is a conditional zero switch only",
            "BQWEYL_ZERO_CONDITIONAL_ONLY",
            "SRC4110_08_3607_signature",
        ),
        (
            "DEC4110_2_finite",
            "stage finite BqWeyl pack without scoring",
            "BqWeyl, q operator, Weyl profile and arena projections are not sourced",
            "finite Weyl runner stays blocked",
            "FINITE_PACK_STAGED_NONCLAIM",
            "SRC4110_09_3607_acquisition",
        ),
        (
            "DEC4110_3_next",
            "attack q-operator normalization next",
            "Z_q/G_q is shared by linear BqWeyl and quadratic DqWeyl2 finite routes",
            "4111 targets q operator/domain/norm or runner blocker",
            "NEXT_TARGET_SELECTED",
            "SRC4110_11_3607_next",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, consequence, status, source_key in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4110_0",
            "target_doc": "4111-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md",
            "target_script": "scripts/Y5_R2FR_4111_q_operator_normalization_or_BqWeyl_bound_runner_blocker.py",
            "objective": "derive or source Z_q/G_q and the q operator domain/norm shared by BqWeyl and D_qWeyl2; if not, keep the finite Weyl bound runner blocked with exact missing inputs",
            "success_gate": "finite BqWeyl or D_qWeyl2 scoring cannot start until q operator normalization, domain, boundary condition and norm convention are parent-owned or source-backed",
            "reason": "4110 keeps v_q and BqWeyl alive but shows the shared finite-route bottleneck is q operator normalization",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4110_0",
            "decision": DECISION,
            "strongest_result": "4110 consolidates the v_q route through BqWeyl: Dq[v_q]=0 would require a live first-class/constraint-first package or termwise source-vector silence; BqWeyl is the first dangerous component; a metric/epsilon-only one-Weyl scalar vanishes, so nonzero linear BqWeyl requires a Weyl spurion/projector/readout tensor. Current corpus does not parent-sign no-spurion grammar, so zero is conditional and the finite pack remains staged.",
            "what_moved_forward": "the dangerous Weyl branch is no longer vague: it is either no-spurion parent signature or finite BqWeyl acquisition, with Z_q/G_q as shared bottleneck",
            "still_missing": "parent first-class G_q/constraint route, no-spurion typed grammar, q representation, BqWeyl coefficient, Z_q/G_q, M_q/lambda_q, C_Weyl profile, arena projections, D_qWeyl2 guard and q norm/domain",
            "public_status": "no vq_vertical_BqWeyl_qbasic_ellJ_Newton_local_GR_PPN claim",
            "next_target": "4111 q operator normalization or BqWeyl runner blocker",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4110_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4110_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4110_VQ_SOURCE_GATE": SOURCE_DIR / "P8_Y5_R2FR_4110_VQ_SOURCE_GATE.csv",
        "P8_Y5_R2FR_4110_BQWEYL_INDEX_SIGNATURE_GATE": SOURCE_DIR / "P8_Y5_R2FR_4110_BQWEYL_INDEX_SIGNATURE_GATE.csv",
        "P8_Y5_R2FR_4110_BQWEYL_ACQUISITION_PACK": SOURCE_DIR / "P8_Y5_R2FR_4110_BQWEYL_ACQUISITION_PACK.csv",
        "P8_Y5_R2FR_4110_PROMOTION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4110_PROMOTION_GATES.csv",
        "P8_Y5_R2FR_4110_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4110_DECISION_GATE.csv",
        "P8_Y5_R2FR_4110_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4110_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4110_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4110_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4110 - vq first-class source-vector silence or Dq_vq bound",
        "",
        "## Verdict",
        "4110 keeps `v_q` as the best vertical candidate, but refuses to certify it without the missing first-class/source-silence package.",
        "",
        "The live bound is:",
        "",
        "`epsilon_Dq_vq <= E_first_class + E_BqWeyl + E_CqT + E_q_source + E_body + E_boundary + E_readout + E_tail + E_norm`.",
        "",
        "The important algebraic advance is on `B_qWeyl`: a scalar linear in one Weyl tensor vanishes unless the parent language supplies a Weyl-type spurion/projector/readout tensor `P^{abcd}`. That is a good zero route, but not a live claim because the no-spurion grammar is not parent-signed.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Concrete Advances",
        "- `v_q` source silence is a component vector, not a slogan.",
        "- `B_qWeyl` is identified as the first dangerous component because exterior vacuum still has Weyl curvature.",
        "- One-Weyl metric/epsilon index lemmas give a real conditional zero theorem.",
        "- Finite BqWeyl acquisition rows are staged but not score-ready.",
        "- `Z_q/G_q` is now the shared bottleneck for linear and quadratic Weyl finite routes.",
        "",
        "## Still Not Claimed",
        "- `Dq[v_q]=0`.",
        "- `B_qWeyl=0`.",
        "- finite Weyl scoring.",
        "- q-basic/local-GR/Newton/PPN promotion.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4110_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4110_VQ_SOURCE_GATE.csv`",
        "- `P8_Y5_R2FR_4110_BQWEYL_INDEX_SIGNATURE_GATE.csv`",
        "- `P8_Y5_R2FR_4110_BQWEYL_ACQUISITION_PACK.csv`",
        "- `P8_Y5_R2FR_4110_PROMOTION_GATES.csv`",
        "- `P8_Y5_R2FR_4110_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4110_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4110_STATUS.csv`",
        "- `P8_Y5_BRR545_4110_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4111-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md`",
        "- Objective: derive/source `Z_q/G_q`, q operator domain, boundary condition and norm convention, or keep finite Weyl scoring blocked.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4110_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4110_VQ_SOURCE_GATE"], vq_source_rows())
    write_csv(outputs["P8_Y5_R2FR_4110_BQWEYL_INDEX_SIGNATURE_GATE"], bqweyl_rows())
    write_csv(outputs["P8_Y5_R2FR_4110_BQWEYL_ACQUISITION_PACK"], acquisition_rows())
    write_csv(outputs["P8_Y5_R2FR_4110_PROMOTION_GATES"], promotion_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4110_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4110_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4110_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **row_base(),
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "valid_for_claim": "False",
            }
        )

    source_rows = source_register_rows()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "True"]
    missing_needles = [row["source_id"] for row in source_rows if row["contains_needle"] != "True"]
    add("VAL4110_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4110_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_counts = {}
    parse_ok = True
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[name] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_counts[name] = f"ERROR:{exc}"
            parse_ok = False
    add("VAL4110_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    vq_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4110_VQ_SOURCE_GATE"]))
    vq_tokens = ["epsilon_Dq_vq", "E_first_class", "E_BqWeyl", "E_CqT", "epsilon_AX_from_vq"]
    missing_vq = [token for token in vq_tokens if token not in vq_text]
    add("VAL4110_3_vq_gate", "v_q source gate includes bound vector and A_X transfer", not missing_vq, ";".join(missing_vq) or "vq tokens present")

    bq_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4110_BQWEYL_INDEX_SIGNATURE_GATE"]))
    bq_tokens = ["one-Weyl", "P^{abcd}", "Z_BqWeyl_linear", "E_BqWeyl", "D_qWeyl2"]
    missing_bq = [token for token in bq_tokens if token not in bq_text]
    add("VAL4110_4_BqWeyl_gate", "BqWeyl gate includes index lemma, spurion need, finite law and quadratic guard", not missing_bq, ";".join(missing_bq) or "BqWeyl tokens present")

    acq_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4110_BQWEYL_ACQUISITION_PACK"]))
    acq_tokens = ["B_qWeyl", "Z_q_or_G_q", "C_Weyl_local_profile", "tau_BqWeyl_R10", "tau_BqWeyl_PPN", "D_qWeyl2", "E_BqWeyl_acceptance"]
    missing_acq = [token for token in acq_tokens if token not in acq_text]
    add("VAL4110_5_acquisition_pack", "finite BqWeyl acquisition pack includes required inputs", not missing_acq, ";".join(missing_acq) or "acquisition tokens present")

    gates = parse_csv(outputs["P8_Y5_R2FR_4110_PROMOTION_GATES"])
    no_claim = all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in gates)
    blocked = any(row.get("status") == "FAIL_CURRENT_CLAIM" and "BqWeyl zero" in row.get("gate", "") for row in gates)
    next_gate = any(row.get("status") == "PASS_ROUTE_SELECTED" and "q operator" in row.get("gate", "") for row in gates)
    add("VAL4110_6_gates", "promotion gates block BqWeyl zero and select q operator", no_claim and blocked and next_gate, f"no_claim={no_claim}; blocked={blocked}; next={next_gate}")

    decisions = parse_csv(outputs["P8_Y5_R2FR_4110_DECISION_GATE"])
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" and "q-operator" in row.get("decision", "") for row in decisions)
    add("VAL4110_7_decisions", "decision gate selects q-operator normalization", next_decision, str(decisions))

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4110_NEXT_TARGET"])
    next_ok = any("4111-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4110_8_next_target", "next target is q operator normalization / BqWeyl runner blocker", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4110_STATUS"])
    status_text = " ".join(" ".join(row.values()) for row in status_rows_local)
    status_ok = DECISION in status_text and "no vq_vertical_BqWeyl_qbasic_ellJ_Newton_local_GR_PPN claim" in status_text
    add("VAL4110_9_status", "status records decision and no-claim state", status_ok, "status row checked")

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4110*")) or any(
            FORMALIZATION.rglob("4110-Y5-R2FR*")
        )
    add("VAL4110_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4110_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4110_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
