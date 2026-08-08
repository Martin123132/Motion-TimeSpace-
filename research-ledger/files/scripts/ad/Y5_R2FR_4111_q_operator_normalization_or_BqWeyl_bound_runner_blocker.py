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
DOC_PATH = ROOT / "4111-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_Q_OPERATOR_FORK_4111"
CHECKPOINT_ID = "4111"
DECISION = (
    "Q_OPERATOR_NORMAL_FORM_AND_NO_POLE_THEOREM_IMPORTED_PI_MTS_MAP_BUILT_"
    "ZQ_LAMBDAQ_XIQ_EXTRACTION_ADVANCED"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4111_00_4110_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4110_NEXT_TARGET.csv",
        "4111-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md",
        "4110 selects q-operator normalization as the next shared Weyl bottleneck.",
    ),
    "SRC4111_01_3608_route": (
        SOURCE_DIR / "P8_Y5_R2FR_3608_Q_OPERATOR_ROUTE_AUDIT.csv",
        "QROUTE3608_5_decision",
        "3608 audits q deletion, q-X bridge and independent Hessian routes.",
    ),
    "SRC4111_02_3608_inputs": (
        SOURCE_DIR / "P8_Y5_R2FR_3608_Q_OPERATOR_INPUT_ROWS.csv",
        "QIN3608_0_Zq",
        "3608 lists q operator inputs required for finite Weyl scoring.",
    ),
    "SRC4111_03_3608_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3608_STATUS.csv",
        "Q_OPERATOR_NORMAL_FORM_DERIVED_BUT_NOT_OWNED",
        "3608 status pins the q operator normal form but blocks scoring.",
    ),
    "SRC4111_04_3609_no_pole": (
        SOURCE_DIR / "P8_Y5_R2FR_3609_NO_POLE_HESSIAN_PROOF.csv",
        "QNP3609_2_hessian_row",
        "3609 proves the conditional no-pole Hessian row theorem.",
    ),
    "SRC4111_05_3609_certificate": (
        SOURCE_DIR / "P8_Y5_R2FR_3609_PARENT_ACTION_CERTIFICATE.csv",
        "QCERT3609_8_activation",
        "3609 audits the MTS certificate needed to activate q deletion.",
    ),
    "SRC4111_06_3609_hessian": (
        SOURCE_DIR / "P8_Y5_R2FR_3609_INDEPENDENT_HESSIAN_FILL_ROWS.csv",
        "QHESS3609_9_runner_law",
        "3609 defines independent Hessian fill rows if q is physical.",
    ),
    "SRC4111_07_3609_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3609_STATUS.csv",
        "NO_POLE_THEOREM_PROVED_CONDITIONALLY_MTS_CERTIFICATE_UNSIGNED_HESSIAN_ROWS_FILLED",
        "3609 status makes the q quotient-vs-physical fork clean.",
    ),
    "SRC4111_08_3610_pi": (
        SOURCE_DIR / "P8_Y5_R2FR_3610_PARENT_PI_SYMBOL_MAP.csv",
        "PI3610_0_pi_definition",
        "3610 builds concrete pi_MTS over actual MTS symbols.",
    ),
    "SRC4111_09_3610_dpi": (
        SOURCE_DIR / "P8_Y5_R2FR_3610_DPI_VQ_CERTIFICATE.csv",
        "DPI3610_8_verdict",
        "3610 audits Dpi[v_q] component zeros.",
    ),
    "SRC4111_10_3610_zqjq": (
        SOURCE_DIR / "P8_Y5_R2FR_3610_ZQ_JQ_EXTRACTION_ROWS.csv",
        "EX3610_2_lambda",
        "3610 extracts conditional Zq/Mq/lambda/Jq rows.",
    ),
    "SRC4111_11_3610_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3610_STATUS.csv",
        "PI_MTS_MAP_BUILT_VQ_UNSIGNED_ZQ_JQ_CONDITIONAL_EXTRACTION_ADVANCED",
        "3610 status upgrades the q fallback to xi_q/Hessian/Jq envelope.",
    ),
    "SRC4111_12_3610_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3610_NEXT_TARGET.csv",
        "3611-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md",
        "3610 selects xi_q/positive Hessian or first Jq component bound as next target.",
    ),
    "SRC4111_13_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4111_q_operator_normalization_or_BqWeyl_bound_runner_blocker.py",
        "Reproducible generator for this 4111 checkpoint.",
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


def q_operator_route_rows() -> List[dict]:
    entries = [
        (
            "QOP4111_0_operator_form",
            "q operator normal form",
            "L_q=-Z_q Delta_branch + M_q^2 + B_q^bdry + curvature/readout terms; G_q=L_q^{-1} only after domain, boundary and norm are owned",
            "linear BqWeyl and quadratic DqWeyl2 are one operator problem",
            "DERIVED_CONDITIONAL_NORMAL_FORM",
            "SRC4111_03_3608_status",
        ),
        (
            "QOP4111_1_no_pole_route",
            "q deletion/no-pole route",
            "delete q only if parent quotient, vertical generator, action/matter/readout descent and boundary/source silence all close",
            "not activated for current MTS",
            "ROUTE_BLOCKED_CERTIFICATE_UNSIGNED",
            "SRC4111_01_3608_route",
        ),
        (
            "QOP4111_2_qx_bridge",
            "q-X bridge route",
            "borrow X operator only if q=aX, scale/units/domain/boundary/readout and X-side values are parent-owned",
            "not owned",
            "ROUTE_BLOCKED",
            "SRC4111_01_3608_route",
        ),
        (
            "QOP4111_3_independent_hessian",
            "physical q Hessian route",
            "if q is physical, fill Z_q, M_q^2/lambda_q, D(L_q), B_q boundary, J_q and P_arena in one normalization",
            "formulas filled, not numeric/source-backed",
            "ROUTE_FORMULA_READY_VALUES_MISSING",
            "SRC4111_06_3609_hessian",
        ),
        (
            "QOP4111_4_runner_blocker",
            "finite Weyl runner",
            "no finite BqWeyl or DqWeyl2 score until one q operator ownership route is activated",
            "runner remains blocked",
            "SCORING_REFUSED_CURRENT",
            "SRC4111_03_3608_status",
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


def no_pole_fork_rows() -> List[dict]:
    entries = [
        (
            "NP4111_0_hessian_theorem",
            "no-pole Hessian row",
            "if S=Sbar∘pi, v_q in ker(Dpi), and reduced equations hold, then D^2(Sbar∘pi)[v_q,w]=0 for every physical direction w",
            "q row/column vanishes from physical Hessian on the quotient",
            "PROVED_CONDITIONALLY",
            "SRC4111_04_3609_no_pole",
        ),
        (
            "NP4111_1_propagator",
            "q-basic readout propagator",
            "gauge-fixing may add representative-sector inverse, but q-basic observables have zero coupling to it",
            "no physical q pole if the certificate closes",
            "PROVED_CONDITIONALLY",
            "SRC4111_04_3609_no_pole",
        ),
        (
            "NP4111_2_certificate",
            "MTS activation certificate",
            "parent pi, v_q in ker(Dpi), first-class degree count, action/matter/coefficient/readout/boundary descent must close on one branch",
            "not signed",
            "CERTIFICATE_UNSIGNED",
            "SRC4111_05_3609_certificate",
        ),
        (
            "NP4111_3_fork",
            "q quotient-vs-physical fork",
            "either q is quotient representative and disappears from local physical propagators, or q is physical residual with explicit Hessian/source rows",
            "mathematically clean fork",
            "FORK_EXACT_NONCLAIM",
            "SRC4111_07_3609_status",
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


def pi_zq_jq_rows() -> List[dict]:
    entries = [
        (
            "PZJ4111_0_pi_MTS",
            "pi_MTS candidate",
            "public geometry/coframe, tau, matter/constants, boundary class, coupling slots, projector/readout maps, excluded q_private and Y_loc",
            "concrete candidate over actual symbols, not parent-signed",
            "CONCRETE_CANDIDATE_CONSTRUCTED_NOT_PARENT_SIGNED",
            "SRC4111_08_3610_pi",
        ),
        (
            "PZJ4111_1_Dpi_vq",
            "Dpi[v_q]",
            "component zeros across geometry, clocks, matter/constants, boundary, coefficients, projectors and local silence multiplet",
            "unsigned componentwise",
            "FAIL_CURRENT_CERTIFICATION",
            "SRC4111_09_3610_dpi",
        ),
        (
            "PZJ4111_2_Mq2",
            "M_q^2",
            "M_q^2 = n_q^A H_AB n_q^B",
            "physical q fallback uses Hessian normal direction",
            "CONDITIONAL_FORMULA_IMPORTED",
            "SRC4111_10_3610_zqjq",
        ),
        (
            "PZJ4111_3_Zq",
            "Z_q",
            "Z_q = xi_q^2 n_q^A H_AB n_q^B",
            "operator normalization tied to smoothing/correlation length",
            "CONDITIONAL_FORMULA_IMPORTED",
            "SRC4111_10_3610_zqjq",
        ),
        (
            "PZJ4111_4_lambda",
            "lambda_q",
            "lambda_q = sqrt(Z_q/M_q^2) = xi_q",
            "if q is physical in positive Hessian branch, its range is not arbitrary",
            "EXACT_CONDITIONAL_RATIO",
            "SRC4111_10_3610_zqjq",
        ),
        (
            "PZJ4111_5_Jq",
            "J_q",
            "J_q[eta] := delta_eta S_nonq projected onto the q equation; J_q^abs is component envelope over matter, frame, marker, body, boundary, projector, memory, source-normalization and curvature components",
            "source vector sharpened but values missing",
            "COMPONENT_ENVELOPE_READY_VALUES_MISSING",
            "SRC4111_10_3610_zqjq",
        ),
        (
            "PZJ4111_6_runner_law",
            "q residual bound",
            "||P_arena q|| <= ||P_arena L_q^{-1}|| (||J_q^abs|| + |B_qW| ||C_Weyl|| + |D_qWeyl2| ||C^2|| + boundary tails)",
            "finite runner law is ready but not executable",
            "BOUND_LAW_READY_NUMBERS_MISSING",
            "SRC4111_10_3610_zqjq",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "formula_or_condition": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, formula, meaning, status, source_key in entries
    ]


def promotion_gate_rows() -> List[dict]:
    entries = [
        ("PROM4111_0_operator_form", "q operator normal form", "PASS_CONDITIONAL_FORM", "L_q form is fixed, ownership missing"),
        ("PROM4111_1_no_pole_theorem", "no-pole Hessian theorem", "PASS_CONDITIONAL_THEOREM", "q row vanishes if quotient certificate closes"),
        ("PROM4111_2_q_deletion", "q deletion for MTS", "FAIL_CURRENT_CLAIM", "pi/v_q/descent/boundary certificate is unsigned"),
        ("PROM4111_3_pi_MTS", "concrete pi_MTS map", "PASS_CANDIDATE_NONCLAIM", "actual MTS symbols mapped but parent signature missing"),
        ("PROM4111_4_Zq_lambda", "Zq/Mq/lambda extraction", "PASS_CONDITIONAL_FORMULA", "lambda_q=xi_q under positive Hessian branch"),
        ("PROM4111_5_runner", "finite Weyl runner", "FAIL_CURRENT_CLAIM", "xi_q/H_AB/Jq/P_arena values are missing"),
        ("PROM4111_6_Newton_GR", "local-GR/Newton promotion", "FAIL_CURRENT_CLAIM", "q quotient or physical residual branch not closed"),
        ("PROM4111_7_next", "xi_q or J_q component", "PASS_ROUTE_SELECTED", "next target must own xi_q/H_AB or first J_q component bound"),
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
            "DEC4111_0_operator",
            "adopt q operator fork",
            "finite Weyl scoring is one q operator problem, not separate loose BqWeyl/DqWeyl2 guesses",
            "runner remains blocked until q operator ownership exists",
            "Q_OPERATOR_FORK_CANONICAL",
            "SRC4111_03_3608_status",
        ),
        (
            "DEC4111_1_no_pole",
            "retain no-pole theorem as real but conditional",
            "the Hessian proof is mathematically clean, but MTS pi/v_q certificate is unsigned",
            "do not delete q yet",
            "NO_POLE_THEOREM_CONDITIONAL_ONLY",
            "SRC4111_07_3609_status",
        ),
        (
            "DEC4111_2_physical_q",
            "advance physical-q fallback",
            "if q is physical, lambda_q=xi_q under positive Hessian branch",
            "next derivation targets xi_q/H_AB or J_q components",
            "ZQ_LAMBDAQ_EXTRACTION_ADVANCED",
            "SRC4111_11_3610_status",
        ),
        (
            "DEC4111_3_next",
            "attack xi_q positive Hessian or first J_q component",
            "3610 upgrades q from abstract missing operator to xi_q/Hessian/source-envelope problem",
            "4112 targets xi_q/H_AB source or first J_q component bound",
            "NEXT_TARGET_SELECTED",
            "SRC4111_12_3610_next",
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
            "next_id": "NEXT4111_0",
            "target_doc": "4112-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md",
            "target_script": "scripts/Y5_R2FR_4112_xi_q_positive_Hessian_source_or_Jq_first_component_bound.py",
            "objective": "derive/source xi_q and the positive Hessian branch that makes lambda_q=xi_q; if that cannot close, fill the first J_q component bound for matter/constants or body/boundary",
            "success_gate": "must produce either an owned xi_q/H_AB row or a theorem-zero/source-backed bound for at least one leading J_q component; no new target-only ledger",
            "reason": "4111 upgrades q from abstract operator ownership to a concrete xi_q/Hessian/Jq source-envelope problem",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4111_0",
            "decision": DECISION,
            "strongest_result": "4111 imports the q operator normal form, the conditional no-pole Hessian theorem, and the concrete pi_MTS/Zq/Jq extraction. The fork is now sharp: q is either a quotient representative with no physical pole if pi and v_q certificate close, or q is a physical residual with M_q^2=n_q H n_q, Z_q=xi_q^2 n_q H n_q and lambda_q=xi_q.",
            "what_moved_forward": "finite Weyl scoring is blocked for a better reason: the next missing object is xi_q/positive Hessian ownership or a first real J_q component bound, not an abstract q operator label",
            "still_missing": "parent pi signature, Dpi[v_q] component zeros, xi_q source, positive H_AB, q domain/boundary/norm, J_q component zero/bound values and arena projections",
            "public_status": "no q_deletion_q_physical_runner_BqWeyl_Newton_local_GR_PPN claim",
            "next_target": "4112 xi_q positive Hessian source or Jq first component bound",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4111_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4111_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4111_Q_OPERATOR_ROUTE_GATE": SOURCE_DIR / "P8_Y5_R2FR_4111_Q_OPERATOR_ROUTE_GATE.csv",
        "P8_Y5_R2FR_4111_NO_POLE_HESSIAN_FORK": SOURCE_DIR / "P8_Y5_R2FR_4111_NO_POLE_HESSIAN_FORK.csv",
        "P8_Y5_R2FR_4111_PI_MTS_ZQ_JQ_EXTRACTION": SOURCE_DIR / "P8_Y5_R2FR_4111_PI_MTS_ZQ_JQ_EXTRACTION.csv",
        "P8_Y5_R2FR_4111_PROMOTION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4111_PROMOTION_GATES.csv",
        "P8_Y5_R2FR_4111_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4111_DECISION_GATE.csv",
        "P8_Y5_R2FR_4111_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4111_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4111_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4111_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4111 - q operator normalization or BqWeyl bound runner blocker",
        "",
        "## Verdict",
        "4111 turns the `q` bottleneck into a clean fork instead of another missing-constant pile.",
        "",
        "The operator side is now:",
        "",
        "`L_q=-Z_q Delta_branch + M_q^2 + B_q^bdry + curvature/readout terms`.",
        "",
        "The quotient side is also sharp: if `S=Sbar∘pi`, `v_q in ker(Dpi)`, and reduced equations hold, the q Hessian row/column vanish for q-basic observables. But MTS has not signed the actual `pi/v_q` certificate.",
        "",
        "The physical-q fallback is sharper too: `M_q^2=n_q^A H_AB n_q^B`, `Z_q=xi_q^2 n_q^A H_AB n_q^B`, hence `lambda_q=xi_q` under the positive Hessian branch.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Concrete Advances",
        "- q deletion is a conditional Hessian theorem, not handwaving.",
        "- `pi_MTS` is mapped over actual MTS symbols, but still unsigned.",
        "- If q is physical, its range is tied to `xi_q`, not arbitrary.",
        "- The finite Weyl runner remains blocked until `xi_q/H_AB` or `J_q` components are owned.",
        "",
        "## Still Not Claimed",
        "- q deletion/no-pole for MTS.",
        "- finite BqWeyl/DqWeyl2 scoring.",
        "- local GR/Newton/PPN promotion.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4111_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4111_Q_OPERATOR_ROUTE_GATE.csv`",
        "- `P8_Y5_R2FR_4111_NO_POLE_HESSIAN_FORK.csv`",
        "- `P8_Y5_R2FR_4111_PI_MTS_ZQ_JQ_EXTRACTION.csv`",
        "- `P8_Y5_R2FR_4111_PROMOTION_GATES.csv`",
        "- `P8_Y5_R2FR_4111_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4111_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4111_STATUS.csv`",
        "- `P8_Y5_BRR545_4111_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4112-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md`",
        "- Objective: derive/source `xi_q` and positive `H_AB`, or fill the first theorem-zero/source-backed `J_q` component bound.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4111_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4111_Q_OPERATOR_ROUTE_GATE"], q_operator_route_rows())
    write_csv(outputs["P8_Y5_R2FR_4111_NO_POLE_HESSIAN_FORK"], no_pole_fork_rows())
    write_csv(outputs["P8_Y5_R2FR_4111_PI_MTS_ZQ_JQ_EXTRACTION"], pi_zq_jq_rows())
    write_csv(outputs["P8_Y5_R2FR_4111_PROMOTION_GATES"], promotion_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4111_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4111_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4111_STATUS"], status_rows())
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
    add("VAL4111_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4111_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

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
    add("VAL4111_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    operator_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4111_Q_OPERATOR_ROUTE_GATE"]))
    operator_tokens = ["L_q", "Z_q", "M_q", "B_q", "finite Weyl runner"]
    missing_operator = [token for token in operator_tokens if token not in operator_text]
    add("VAL4111_3_operator", "q operator route gate contains normal form and runner blocker", not missing_operator, ";".join(missing_operator) or "operator tokens present")

    no_pole_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4111_NO_POLE_HESSIAN_FORK"]))
    no_pole_tokens = ["Sbar", "Dpi", "q row", "CERTIFICATE_UNSIGNED", "q quotient-vs-physical"]
    missing_no_pole = [token for token in no_pole_tokens if token not in no_pole_text]
    add("VAL4111_4_no_pole", "no-pole fork contains Hessian theorem and unsigned certificate", not missing_no_pole, ";".join(missing_no_pole) or "no-pole tokens present")

    extraction_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4111_PI_MTS_ZQ_JQ_EXTRACTION"]))
    extraction_tokens = ["pi_MTS", "Dpi[v_q]", "M_q^2", "Z_q", "lambda_q", "xi_q", "J_q", "P_arena"]
    missing_extraction = [token for token in extraction_tokens if token not in extraction_text]
    add("VAL4111_5_extraction", "pi/Zq/Jq extraction rows include pi map, lambda=xi and runner law", not missing_extraction, ";".join(missing_extraction) or "extraction tokens present")

    gates = parse_csv(outputs["P8_Y5_R2FR_4111_PROMOTION_GATES"])
    no_claim = all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in gates)
    q_deletion_blocked = any(row.get("status") == "FAIL_CURRENT_CLAIM" and "q deletion" in row.get("gate", "") for row in gates)
    next_gate = any(row.get("status") == "PASS_ROUTE_SELECTED" and "xi_q" in row.get("detail", "") for row in gates)
    add("VAL4111_6_gates", "promotion gates block q deletion and select xi/Jq route", no_claim and q_deletion_blocked and next_gate, f"no_claim={no_claim}; q_deletion={q_deletion_blocked}; next={next_gate}")

    decisions = parse_csv(outputs["P8_Y5_R2FR_4111_DECISION_GATE"])
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" and "xi_q" in row.get("decision", "") for row in decisions)
    add("VAL4111_7_decisions", "decision gate selects xi_q/Jq next", next_decision, str(decisions))

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4111_NEXT_TARGET"])
    next_ok = any("4112-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4111_8_next_target", "next target is xi-q positive Hessian or Jq first component", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4111_STATUS"])
    status_text = " ".join(" ".join(row.values()) for row in status_rows_local)
    status_ok = DECISION in status_text and "no q_deletion_q_physical_runner_BqWeyl_Newton_local_GR_PPN claim" in status_text
    add("VAL4111_9_status", "status records decision and no-claim state", status_ok, "status row checked")

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4111*")) or any(
            FORMALIZATION.rglob("4111-Y5-R2FR*")
        )
    add("VAL4111_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4111_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4111_VALIDATION.csv"
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
