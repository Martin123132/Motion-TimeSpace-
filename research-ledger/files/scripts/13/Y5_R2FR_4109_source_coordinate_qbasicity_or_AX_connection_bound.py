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
DOC_PATH = ROOT / "4109-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_COORDINATE_QBASIC_DQ_GATE_4109"
CHECKPOINT_ID = "4109"
DECISION = (
    "QBASIC_AX_CHAIN_RULE_DERIVED_ACTUAL_DQ_VERTICAL_MATRIX_UNSIGNED_"
    "VQ_FIRST_CLASS_SOURCE_SILENCE_GATE_NEXT"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4109_00_4108_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4108_NEXT_TARGET.csv",
        "4109-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md",
        "4108 selects source-coordinate q-basicity / A_X connection as the next gate.",
    ),
    "SRC4109_01_3603_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3603_QBASIC_AX_THEOREM.csv",
        "AX3603_3_bundle_zero_theorem",
        "3603 derives the q-basic source-coordinate chain-rule zero theorem.",
    ),
    "SRC4109_02_3603_obstruction": (
        SOURCE_DIR / "P8_Y5_R2FR_3603_AX_OBSTRUCTION_LAW.csv",
        "AXR3603_0_A_X_total",
        "3603 decomposes A_X obstruction terms.",
    ),
    "SRC4109_03_3603_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3603_AX_BOUND_ROWS.csv",
        "AXB3603_12_C_M_Cshape_transfer",
        "3603 gives A_X and C_M/C_shape transfer bound rows.",
    ),
    "SRC4109_04_3603_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3603_STATUS.csv",
        "SOURCE_COORDINATE_QBASIC_AX_THEOREM_DERIVED_DQ_MATRIX_NEXT",
        "3603 status selects actual Dq matrix certification as the next target.",
    ),
    "SRC4109_05_3604_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3604_QMAP_VERTICAL_THEOREM.csv",
        "DQV3604_1_vertical_criterion",
        "3604 turns verticality into an explicit Dq matrix criterion.",
    ),
    "SRC4109_06_3604_matrix": (
        SOURCE_DIR / "P8_Y5_R2FR_3604_DIRECTION_DQ_MATRIX_AUDIT.csv",
        "DQM3604_4_v_RAB",
        "3604 audits candidate directions against the Dq matrix.",
    ),
    "SRC4109_07_3604_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3604_DQ_LEAK_BOUND_ROWS.csv",
        "DQB3604_8_Ax_transfer",
        "3604 gives Dq leak rows that feed the A_X bound.",
    ),
    "SRC4109_08_3604_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3604_STATUS.csv",
        "ACTUAL_QMAP_VERTICAL_BASIS_UNSIGNED_DQ_LEAK_BOUNDS_INSTALLED",
        "3604 status keeps q-basic theorems conditional and selects v_q as first target.",
    ),
    "SRC4109_09_3604_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3604_NEXT_TARGET.csv",
        "3605-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md",
        "3604 selects v_q first-class/source-vector silence as next target.",
    ),
    "SRC4109_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4109_source_coordinate_qbasicity_or_AX_connection_bound.py",
        "Reproducible generator for this 4109 checkpoint.",
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


def qbasic_ax_rows() -> List[dict]:
    entries = [
        (
            "QAX4109_0_qbasic_criterion",
            "Y descends through q",
            "For connected q-fibres, Y=Ybar(q(Phi)) iff dY annihilates ker(Dq) and is compatible across quotient branches",
            "q-basicity has a differential criterion, not a slogan",
            "EXACT_DIFFERENTIAL_CRITERION",
            "SRC4109_01_3603_theorem",
        ),
        (
            "QAX4109_1_AX_identity",
            "A_X_source_connection",
            "A_X^I := D_XY^I = dY^I(v_X); if Y is q-basic, A_X=dYbar(Dq(v_X))",
            "source mass/shape drift is controlled by q-map leakage plus non-q-basic defects",
            "EXACT_CHAIN_RULE_IDENTITY",
            "SRC4109_01_3603_theorem",
        ),
        (
            "QAX4109_2_bundle_zero",
            "C_M+C_shape",
            "if M_H_ref and sigma^a are q-basic and Dq(v_X)=0, then A_X=0, partial_M A_X^M=partial_M A_X^a=0, and C_M=C_shape=0",
            "this is the non-plateau derivation route",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "SRC4109_01_3603_theorem",
        ),
        (
            "QAX4109_3_shape_law",
            "sigma^a",
            "D_X sigma^a=(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref",
            "shape leakage is a Reynolds/support/density law, not a mystery coupling",
            "EXACT_REYNOLDS_TRANSPORT_LAW",
            "SRC4109_01_3603_theorem",
        ),
        (
            "QAX4109_4_nonzero_bound",
            "A_X bound",
            "||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||",
            "when verticality is unsigned, A_X becomes a bound row feeding C_M,C_shape",
            "EXACT_BOUND_LAW_NONCLAIM",
            "SRC4109_03_3603_bounds",
        ),
        (
            "QAX4109_5_current_verdict",
            "q-basic source-coordinate zero",
            "not claimable until actual Dq matrix/residual basis proves verticality and the H_tau/H_ref/density/support/EM branches descend",
            "the theorem is useful but not activated",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "SRC4109_04_3603_status",
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


def dq_matrix_rows() -> List[dict]:
    entries = [
        (
            "DQM4109_0_vertical_criterion",
            "ker(Dq)",
            "for q=(q_geom,q_tau,q_matter,q_boundary,q_coeff,q_projector,readout), v is vertical iff every Dq_a[v]=0 on the same branch",
            "all q-basic zero theorems now depend on an actual matrix gate",
            "EXACT_MATRIX_CRITERION",
            "SRC4109_05_3604_theorem",
        ),
        (
            "DQM4109_1_Dq_bound_law",
            "epsilon_Dq[v]",
            "epsilon_Dq[v] := ||Dq[v]||_q/||v|| <= sum_a epsilon_a[v]",
            "unsigned verticality becomes a source-ready leak bound",
            "EXACT_BOUND_LAW_NONCLAIM",
            "SRC4109_05_3604_theorem",
        ),
        (
            "DQM4109_2_vq",
            "v_q_private",
            "best first candidate, but vertical only if q_private is first-class/source-silent across geometry, tau, matter, boundary and readout",
            "highest-priority direction not certified",
            "CANDIDATE_HIGHEST_PRIORITY_NOT_CERTIFIED",
            "SRC4109_06_3604_matrix",
        ),
        (
            "DQM4109_3_memory_coeff_boundary",
            "v_memory_tau;v_coeff;v_boundary",
            "memory/tau, coefficient and boundary directions are conditional only and need their own q-component leak bounds",
            "secondary candidate directions remain unsigned",
            "CANDIDATE_BOUNDS_REQUIRED",
            "SRC4109_06_3604_matrix",
        ),
        (
            "DQM4109_4_RAB_guard",
            "v_RAB",
            "R_AB/lambda_R is rejected under the current observer-cell map unless the observer map is rebuilt or the field is constraint-eliminated",
            "prevents using rejected directions inside q-basic zero theorems",
            "REJECTED_CURRENT_BRANCH",
            "SRC4109_06_3604_matrix",
        ),
        (
            "DQM4109_5_projector_guard",
            "delta_projector",
            "projector/readout-kernel variation is an obstruction, not vertical, unless fixed before variation or retained separately",
            "prevents projector silence by definition",
            "OBSTRUCTION_NOT_VERTICAL",
            "SRC4109_06_3604_matrix",
        ),
        (
            "DQM4109_6_AX_transfer",
            "epsilon_AX_from_Dq",
            "||dYbar|| epsilon_Dq + E_Y feeds the A_X source-coordinate bound",
            "Dq leakage directly propagates into C_M,C_shape and ell_J",
            "TRANSFER_ROW_NONCLAIM",
            "SRC4109_07_3604_bounds",
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


def bound_rows() -> List[dict]:
    entries = [
        ("BND4109_0_A_X", "A_X_source_connection", "||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||", "BOUND_REQUIRED_CRITICAL", "SRC4109_03_3603_bounds"),
        ("BND4109_1_Dq_total", "epsilon_Dq_total", "max_i ||Dq[v_i]||_q/||v_i|| or declared q-component norm envelope", "BOUND_REQUIRED_CRITICAL", "SRC4109_07_3604_bounds"),
        ("BND4109_2_Dq_vq", "epsilon_Dq_vq", "||Dq[v_q]||_q/||v_q|| <= E_first_class+E_matter+E_boundary+E_readout", "BOUND_REQUIRED_HIGHEST_PRIORITY", "SRC4109_07_3604_bounds"),
        ("BND4109_3_Dq_memory", "epsilon_Dq_memory_tau", "memory/tau/coframe source-support q leak bound", "BOUND_REQUIRED", "SRC4109_07_3604_bounds"),
        ("BND4109_4_Dq_coeff", "epsilon_Dq_coeff", "coefficient/source-scale/clock-constant q leak bound", "BOUND_REQUIRED", "SRC4109_07_3604_bounds"),
        ("BND4109_5_Dq_boundary", "epsilon_Dq_boundary", "compact boundary/reference q leak bound", "BOUND_REQUIRED_LOCAL_ONLY", "SRC4109_07_3604_bounds"),
        ("BND4109_6_Dq_RAB", "epsilon_Dq_RAB", "rejected nonzero unless observer map rebuilt or constraint-first elimination is proved", "REJECTED_BOUND_REQUIRED_IF_REUSED", "SRC4109_07_3604_bounds"),
        ("BND4109_7_Dq_projector", "epsilon_Dq_projector", "projector/readout-kernel obstruction bound", "BOUND_REQUIRED_OBSTRUCTION", "SRC4109_07_3604_bounds"),
        ("BND4109_8_Ctransfer", "C_M_plus_C_shape", "C_M+C_shape from A_X and partial_M A_X derivative rows", "TOTAL_BOUND_BRANCH_ACTIVE", "SRC4109_03_3603_bounds"),
    ]
    return [
        {
            **row_base(),
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, symbol, definition, status, source_key in entries
    ]


def promotion_gate_rows() -> List[dict]:
    entries = [
        ("PROM4109_0_chain_rule", "A_X chain-rule identity", "PASS_EXACT_IDENTITY", "A_X=dY(v_X), and q-basic Y gives A_X=dYbar(Dq(v_X))"),
        ("PROM4109_1_bundle_zero", "A_X/C_M/C_shape zero", "PASS_CONDITIONAL_THEOREM", "q-basic Y plus Dq(v_X)=0 kills A_X, C_M and C_shape"),
        ("PROM4109_2_Dq_matrix", "actual vertical matrix criterion", "PASS_EXACT_CRITERION", "v is vertical only if every q-component derivative vanishes"),
        ("PROM4109_3_current_vertical_claim", "live vertical basis", "FAIL_CURRENT_CLAIM", "no candidate direction has source-backed Dq[v]=0"),
        ("PROM4109_4_RAB_guard", "R_AB/lambda_R direction", "PASS_GUARD", "rejected under current observer-cell map"),
        ("PROM4109_5_projector_guard", "projector/readout variation", "PASS_GUARD", "obstruction, not vertical direction"),
        ("PROM4109_6_Newton_GR", "constant G/Newton/local-GR promotion", "FAIL_CURRENT_CLAIM", "q-basic source-coordinate/H_tau/density/support zeros remain conditional"),
        ("PROM4109_7_next", "v_q first attack", "PASS_ROUTE_SELECTED", "v_q is the highest-priority direction for first-class/source-vector silence"),
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
            "DEC4109_0_AX",
            "adopt q-basic A_X chain-rule theorem",
            "it kills C_M and C_shape only through source-coordinate descent plus true verticality",
            "no plateau or measured-GM calibration is allowed for A_X=0",
            "AX_CHAIN_RULE_CANONICAL",
            "SRC4109_01_3603_theorem",
        ),
        (
            "DEC4109_1_Dq",
            "make actual Dq matrix the activation gate",
            "no q-basic theorem can activate without the same q-map and residual basis proving Dq[v]=0",
            "verticality becomes matrix evidence or leak bounds",
            "DQ_MATRIX_GATE_CANONICAL",
            "SRC4109_05_3604_theorem",
        ),
        (
            "DEC4109_2_next",
            "attack v_q first-class/source-vector silence next",
            "3604 says v_q is the best candidate and first Dq leak row feeding A_X/local closure",
            "4110 targets epsilon_Dq_vq zero or bound",
            "NEXT_TARGET_SELECTED",
            "SRC4109_09_3604_next",
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
            "next_id": "NEXT4109_0",
            "target_doc": "4110-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md",
            "target_script": "scripts/Y5_R2FR_4110_vq_first_class_source_vector_silence_or_Dq_vq_bound.py",
            "objective": "prove v_q is first-class/source-silent across geometry, tau, matter, boundary and readout q-components; if not, retain epsilon_Dq_vq with B_qW, C_qT, matter, boundary and readout tail bounds",
            "success_gate": "v_q can enter q-basic zero theorems only if Dq[v_q]=0 is parent-owned on the same q map, or if a source-backed epsilon_Dq_vq bound is available",
            "reason": "4109 shows A_X dies by chain rule only after Dq(v_X)=0; v_q is the highest-priority candidate direction and first leak bound feeding source coupling",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4109_0",
            "decision": DECISION,
            "strongest_result": "4109 imports the q-basic source-coordinate theorem and the actual Dq matrix gate. A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y, so q-basic Y and true verticality kill A_X, partial_M A_X, C_M and C_shape by chain rule. But 3604 shows no direction is currently certified vertical; v_q is only the best first candidate, while v_RAB is rejected and projector variation is an obstruction.",
            "what_moved_forward": "the q-basic route is now an explicit matrix/eigen-direction problem with Dq leak bounds that feed A_X and ell_J rather than another abstract closure phrase",
            "still_missing": "parent-owned q definition, residual basis action, actual Dq entries, Dq[v_q]=0 or epsilon_Dq_vq bound, memory/tau frame lock, coefficient descent, compact boundary/reference silence, projector fixedness, q-component norm",
            "public_status": "no qbasic_AX_ellJ_constant_Geff_Newton_local_GR_PPN claim",
            "next_target": "4110 vq first-class source-vector silence or Dq_vq bound",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4109_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4109_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4109_QBASIC_AX_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4109_QBASIC_AX_THEOREM.csv",
        "P8_Y5_R2FR_4109_DQ_MATRIX_GATE": SOURCE_DIR / "P8_Y5_R2FR_4109_DQ_MATRIX_GATE.csv",
        "P8_Y5_R2FR_4109_BOUND_INPUTS": SOURCE_DIR / "P8_Y5_R2FR_4109_BOUND_INPUTS.csv",
        "P8_Y5_R2FR_4109_PROMOTION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4109_PROMOTION_GATES.csv",
        "P8_Y5_R2FR_4109_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4109_DECISION_GATE.csv",
        "P8_Y5_R2FR_4109_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4109_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4109_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4109_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4109 - source-coordinate q-basicity or A_X connection bound",
        "",
        "## Verdict",
        "4109 gets the source-coordinate route into its honest form:",
        "",
        "`A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y`, with `Y=(M_H_ref,sigma^a)`.",
        "",
        "If `Y` is q-basic and `Dq(v_X)=0`, then `A_X=0`; therefore `partial_M A_X^M=partial_M A_X^a=0` and `C_M=C_shape=0`. That is the clean chain-rule route.",
        "",
        "But the actual `Dq` matrix is not signed yet. No residual direction currently passes the verticality gate. So the live result is a bound law, not a zero claim.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Concrete Advances",
        "- `A_X` is reduced to q-map leakage plus source-coordinate descent defects.",
        "- Shape drift has the Reynolds law, not a vague source-coupling mystery.",
        "- Verticality is now an explicit matrix criterion over `q_geom,q_tau,q_matter,q_boundary,q_coeff,q_projector,readout`.",
        "- `v_q` is the highest-priority candidate; `v_RAB` is rejected in the current observer map; projector variation is an obstruction.",
        "",
        "## Still Not Claimed",
        "- `A_X=0`.",
        "- `C_M=C_shape=0` live branch.",
        "- q-basic source-coordinate/H_tau/density/support closure.",
        "- Constant `G_eff`, Newton/local-GR/PPN.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4109_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4109_QBASIC_AX_THEOREM.csv`",
        "- `P8_Y5_R2FR_4109_DQ_MATRIX_GATE.csv`",
        "- `P8_Y5_R2FR_4109_BOUND_INPUTS.csv`",
        "- `P8_Y5_R2FR_4109_PROMOTION_GATES.csv`",
        "- `P8_Y5_R2FR_4109_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4109_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4109_STATUS.csv`",
        "- `P8_Y5_BRR545_4109_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4110-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md`",
        "- Objective: prove `Dq[v_q]=0` across geometry, tau, matter, boundary and readout components, or retain `epsilon_Dq_vq` bound rows.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4109_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4109_QBASIC_AX_THEOREM"], qbasic_ax_rows())
    write_csv(outputs["P8_Y5_R2FR_4109_DQ_MATRIX_GATE"], dq_matrix_rows())
    write_csv(outputs["P8_Y5_R2FR_4109_BOUND_INPUTS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4109_PROMOTION_GATES"], promotion_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4109_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4109_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4109_STATUS"], status_rows())
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
    add("VAL4109_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4109_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

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
    add("VAL4109_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    qbasic_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4109_QBASIC_AX_THEOREM"]))
    qbasic_tokens = ["A_X", "dYbar(Dq(v_X))", "C_M=C_shape=0", "Reynolds", "||A_X||"]
    missing_qbasic = [token for token in qbasic_tokens if token not in qbasic_text]
    add("VAL4109_3_qbasic_ax", "qbasic theorem contains chain rule, zero route, Reynolds law and bound", not missing_qbasic, ";".join(missing_qbasic) or "qbasic tokens present")

    dq_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4109_DQ_MATRIX_GATE"]))
    dq_tokens = ["q_geom", "q_tau", "q_matter", "v_q_private", "v_RAB", "delta_projector", "epsilon_AX_from_Dq"]
    missing_dq = [token for token in dq_tokens if token not in dq_text]
    add("VAL4109_4_dq_matrix", "Dq matrix gate includes q components and candidate directions", not missing_dq, ";".join(missing_dq) or "Dq tokens present")

    bound_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4109_BOUND_INPUTS"]))
    bound_tokens = ["A_X_source_connection", "epsilon_Dq_total", "epsilon_Dq_vq", "epsilon_Dq_RAB", "C_M_plus_C_shape"]
    missing_bound = [token for token in bound_tokens if token not in bound_text]
    add("VAL4109_5_bounds", "bound rows include A_X, Dq leak, vq, RAB and C transfer", not missing_bound, ";".join(missing_bound) or "bound tokens present")

    gates = parse_csv(outputs["P8_Y5_R2FR_4109_PROMOTION_GATES"])
    no_claim = all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in gates)
    vertical_blocked = any(row.get("status") == "FAIL_CURRENT_CLAIM" and "vertical" in row.get("gate", "") for row in gates)
    rab_guard = any(row.get("status") == "PASS_GUARD" and "R_AB" in row.get("gate", "") for row in gates)
    add("VAL4109_6_gates", "promotion gates block vertical claim and retain RAB guard", no_claim and vertical_blocked and rab_guard, f"no_claim={no_claim}; vertical={vertical_blocked}; rab={rab_guard}")

    decisions = parse_csv(outputs["P8_Y5_R2FR_4109_DECISION_GATE"])
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" and "v_q" in row.get("decision", "") for row in decisions)
    add("VAL4109_7_decisions", "decision gate selects v_q first attack", next_decision, str(decisions))

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4109_NEXT_TARGET"])
    next_ok = any("4110-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4109_8_next_target", "next target is vq first-class/source-vector silence", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4109_STATUS"])
    status_text = " ".join(" ".join(row.values()) for row in status_rows_local)
    status_ok = DECISION in status_text and "no qbasic_AX_ellJ_constant_Geff_Newton_local_GR_PPN claim" in status_text
    add("VAL4109_9_status", "status records decision and no-claim state", status_ok, "status row checked")

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4109*")) or any(
            FORMALIZATION.rglob("4109-Y5-R2FR*")
        )
    add("VAL4109_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4109_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4109_VALIDATION.csv"
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
