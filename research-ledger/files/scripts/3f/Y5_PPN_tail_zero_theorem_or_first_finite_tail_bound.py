from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1583"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1583-Y5-PPN-tail-zero-theorem-or-first-finite-tail-bound.md"

SOURCE_FILES = {
    "1582_doc": ROOT / "1582-Y5-QR-no-charge-source-denominator-and-tail-envelope.md",
    "1582_validation": OUT / "P8_Y5_BRR545_1582_VALIDATION.csv",
    "1582_tail_envelope": OUT / "P8_Y5_PARENT_QLOC_1582_PPN_TAIL_ENVELOPE.csv",
    "1582_readiness": OUT / "P8_Y5_PARENT_QLOC_1582_CASSINI_READINESS_RUNNER.csv",
    "1575_matter_descent": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
    "1519_coframe_tau": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
    "1519_local_status": OUT / "P8_Y5_PARENT_FRAME_1519_LOCAL_GR_NEWTON_STATUS.csv",
    "boundary_noflux": OUT / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1582_doc": ["NEXT_1583_PPN_TAIL_ZERO_THEOREM_OR_FIRST_FINITE_TAIL_BOUND", "delta_gauge"],
    "1582_validation": ["VAL1582_OVERALL", "PASS"],
    "1582_tail_envelope": ["TAIL1582_5_higher_order", "MISSING_SECOND_ORDER_CONTROL"],
    "1582_readiness": ["CR1582_1_absolute_bound", "NOT_RUN_COMPONENTS_MISSING"],
    "1575_matter_descent": ["MDS1575_4_boundary", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    "1519_coframe_tau": ["OCF1519_4_tau_lock", "MISSING_TAU_LOCK"],
    "1519_local_status": ["LOCAL1519_2_PPN", "NOT_CLAIMED"],
    "boundary_noflux": ["T5_parent_owner_audit", "fail_not_parent_owned"],
    "10_observer": ["beta - 1 = 0", "Bianchi-like consistency identity"],
    "local_bound_claims": ["Cassini_Shapiro_gamma_2003", "gamma_minus_1", "2.3e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1583_SOURCE_REGISTER.csv"
TAIL_ZERO_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1583_PPN_TAIL_ZERO_THEOREM_ATTEMPT.csv"
FINITE_TAIL_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1583_FIRST_FINITE_TAIL_BOUND_LEDGER.csv"
GR_COMPLETION = OUT / "P8_Y5_PARENT_QLOC_1583_GR_COMPLETION_GATE.csv"
CASSINI_TAIL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1583_CASSINI_TAIL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1583_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1583_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1583_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1583_VALIDATION.csv"

COPY_TARGETS = {
    TAIL_ZERO_ATTEMPT: [
        QUARANTINE / "PPN_TAIL_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "PPN_tail_zero_theorem_attempt_nonclaim_1583.csv",
    ],
    FINITE_TAIL_LEDGER: [
        QUARANTINE / "FIRST_FINITE_TAIL_BOUND_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "first_finite_tail_bound_ledger_nonclaim_1583.csv",
    ],
    GR_COMPLETION: [
        QUARANTINE / "GR_COMPLETION_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "GR_completion_gate_nonclaim_1583.csv",
    ],
    CASSINI_TAIL_RUNNER: [
        QUARANTINE / "CASSINI_TAIL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "Cassini_tail_runner_nonclaim_1583.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "PPN_tail_zero_decision_nonclaim_1583.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1583_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "PPN tail-zero theorem or first finite absolute tail-bound row",
                **flags(),
            }
        )
    return rows


def tail_zero_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TZ1583_0_gauge",
            "delta_gauge",
            "observed coframe and PPN radial gauge are fixed before readout; A=T^2 and B=S in same source frame",
            "delta_gauge=0",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "q/Obs_e/coframe tau lock remains not parent-signed",
        ),
        (
            "TZ1583_1_source",
            "delta_source",
            "same-frame Newtonian source denominator GM, no hidden source reciprocal momentum, source boundary matched",
            "delta_source=0",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "Q_R/Pi_R, kappa_W, GM convention and domain map are missing",
        ),
        (
            "TZ1583_2_boundary",
            "delta_boundary",
            "scalar-only stationary boundary collar with no vector/shear/normal flux and full Ward flux closure",
            "delta_boundary=0",
            "CONDITIONAL_LEMMA_PARENT_OWNER_MISSING",
            "boundary noflux theorem is conditional and not parent-owned",
        ),
        (
            "TZ1583_3_readout",
            "delta_readout",
            "ordinary matter/constants/readout descend through one observed coframe; no marker, Weyl, disformal or shadow frame",
            "delta_readout=0",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "matter descent, constants, no-marker and tau lock remain unsigned",
        ),
        (
            "TZ1583_4_higher_order",
            "O(U_N) PPN correction",
            "beta-1=0, Bianchi-like conservation identity, and common matter coupling close the post-linear tail",
            "higher-order tail=0",
            "NOT_DERIVED",
            "PPN beta, conservation and common matter coupling remain open",
        ),
        (
            "TZ1583_5_verdict",
            "all PPN tails zero",
            "TZ1583_0 through TZ1583_4 all parent-signed",
            "Cassini gamma channel can score only then",
            "FAIL_CURRENT_CLAIM_TAIL_ZERO_NOT_DERIVED",
            "at least gauge/source/boundary/readout/second-order clauses remain unsigned",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "tail_zero_id": tail_zero_id,
            "tail_component": tail_component,
            "zero_condition": zero_condition,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for tail_zero_id, tail_component, zero_condition, effect_if_signed, status, blocking_gap in rows
    ]


def finite_tail_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FTB1583_0_gauge",
            "delta_gauge",
            "absolute dimensionless PPN-gamma contribution",
            "source path for gauge map, observer coframe, PPN radial coordinate, and value/bound",
            "MISSING_GAUGE_BOUND_OR_ZERO",
        ),
        (
            "FTB1583_1_source",
            "delta_source",
            "absolute source-denominator/interior-matching contribution",
            "Q_R/Pi_R source row, kappa_W, GM convention and domain map",
            "MISSING_SOURCE_BOUND_OR_ZERO",
        ),
        (
            "FTB1583_2_boundary",
            "delta_boundary",
            "absolute boundary/worldtube/corner contribution",
            "boundary noflux theorem or numeric boundary tail bound with units/source path",
            "MISSING_BOUNDARY_BOUND_OR_ZERO",
        ),
        (
            "FTB1583_3_readout",
            "delta_readout",
            "absolute matter/readout/shadow-frame contribution",
            "matter descent/no-marker/tau-lock theorem or numeric readout bound",
            "MISSING_READOUT_BOUND_OR_ZERO",
        ),
        (
            "FTB1583_4_higher_order",
            "O(U_N) PPN correction",
            "absolute post-linear beta/conservation contribution",
            "PPN beta/conservation/common coupling derivation or numeric finite bound",
            "MISSING_SECOND_ORDER_BOUND_OR_ZERO",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "finite_tail_id": finite_tail_id,
            "tail_component": tail_component,
            "required_units": required_units,
            "required_source_form": required_source_form,
            "current_status": current_status,
            "no_cancellation": True,
            **flags(),
        }
        for finite_tail_id, tail_component, required_units, required_source_form, current_status in rows
    ]


def gr_completion_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GRC1583_0_gamma",
            "PPN gamma channel",
            "Q_R=0 or bounded q_R_hat plus tails=0/bounded",
            "FORMAL_BRIDGE_EXISTS_NOT_SCOREABLE",
            "gamma bridge exists but Q_R and tails are missing",
        ),
        (
            "GRC1583_1_beta",
            "PPN beta channel",
            "beta-1=0 in valid PPN coordinate construction",
            "MISSING_DERIVATION",
            "observer contract already says gamma=1 alone is insufficient",
        ),
        (
            "GRC1583_2_conservation",
            "Bianchi-like conservation",
            "field equations imply source-compatible conservation identity",
            "MISSING_DERIVATION",
            "needed to prevent hidden momentum/domain flux tails",
        ),
        (
            "GRC1583_3_common_matter",
            "universal matter coframe/coupling",
            "all matter sectors couple to same observed coframe with constants fixed",
            "MISSING_PARENT_SIGNATURE",
            "matter descent and tau lock are unsigned",
        ),
        (
            "GRC1583_4_newton",
            "Newtonian source-normalized limit",
            "T^2=1-2U/c^2 and correct weak-field acceleration",
            "MISSING_SOURCE_DENOMINATOR",
            "GM/MHref/source equality remains missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "completion_id": completion_id,
            "gr_requirement": gr_requirement,
            "required_statement": required_statement,
            "current_status": current_status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for completion_id, gr_requirement, required_statement, current_status, blocking_gap in rows
    ]


def cassini_tail_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "CTR1583_0_tail_zero_import",
            "case": "all tails set to zero by theorem labels",
            "status": "REFUSE_PLACEHOLDER",
            "reason": "zero labels are conditional and not parent-signed",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "CTR1583_1_finite_tail_bound",
            "case": "finite absolute tail envelope",
            "status": "NOT_RUN_COMPONENTS_MISSING",
            "reason": "no finite tail row has numeric/source-backed bound",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "CTR1583_2_gamma_only_gr",
            "case": "use gamma channel as full local GR reduction",
            "status": "REFUSE_PLACEHOLDER",
            "reason": "beta, conservation, Newtonian source normalization and common matter coupling remain open",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1583_0_tail_zero", "all PPN tails vanish", "BLOCKED_NO_CLAIM", "tail-zero theorem has unsigned gauge/source/boundary/readout/second-order clauses"),
        ("GATE1583_1_finite_tail_bound", "finite tail envelope is score-ready", "BLOCKED_NO_CLAIM", "finite tail rows have no numeric/source-backed values"),
        ("GATE1583_2_Cassini", "Cassini gamma comparison can be scored", "BLOCKED_NO_CLAIM", "Q_R/source denominator and tails remain missing"),
        ("GATE1583_3_GR", "derived local GR/Newton branch", "BLOCKED_NO_CLAIM", "beta, Bianchi/conservation and common matter coupling remain open"),
        ("GATE1583_4_public_claim", "any local PPN claim", "BLOCKED_NO_CLAIM", "formal contracts only; no prediction row exists"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1583_0_tail_status",
            "PPN_TAIL_ZERO_THEOREM_FAILS_CURRENT_CORPUS",
            "each tail has a plausible zero condition, but at least one required parent signature is missing in every route",
            "Cassini/local gamma branch remains nonclaim",
        ),
        (
            "DEC1583_1_fallback_status",
            "FINITE_TAIL_BOUND_LEDGER_STAGED",
            "absolute no-cancellation tail rows now have required source forms",
            "finite fallback can continue only by filling numeric/source-backed tail bounds",
        ),
        (
            "DEC1583_2_next",
            "NEXT_1584_PPN_BETA_CONSERVATION_COMMON_MATTER_GATE",
            "the highest-value GR path is now beta/conservation/common coupling, because gamma-channel work alone cannot prove GR reduction",
            "derive beta=1, Bianchi-like identity and universal coframe coupling or keep local GR unclaimed",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1584-Y5-PPN-beta-conservation-common-matter-gate.md",
            "script": "scripts/Y5_PPN_beta_conservation_common_matter_gate.py",
            "objective": "map and attempt the beta=1, Bianchi-like conservation and universal observed-coframe coupling gates needed after the gamma/q_R_hat branch",
            "do_not": "do not claim GR from gamma alone; do not import Einstein equations; do not score PPN until beta/conservation/matter gates are derived or explicitly bounded",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "can_score",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    generated_paths = [Path(__file__).resolve(), DOC, *generated_csvs]
    generated_paths.extend(target for targets in COPY_TARGETS.values() for target in targets)
    if any(is_within(path, FORMALIZATION) for path in generated_paths):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1583_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1583" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    zero = read_csv(TAIL_ZERO_ATTEMPT)
    finite = read_csv(FINITE_TAIL_LEDGER)
    completion = read_csv(GR_COMPLETION)
    runner = read_csv(CASSINI_TAIL_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_tails = {"delta_gauge", "delta_source", "delta_boundary", "delta_readout", "O(U_N) PPN correction"}
    required_gr = {"PPN gamma channel", "PPN beta channel", "Bianchi-like conservation", "universal matter coframe/coupling", "Newtonian source-normalized limit"}
    checks = [
        ("VAL1583_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1583_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1583_2_tail_zero_fails",
            any(row["tail_zero_id"] == "TZ1583_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_TAIL_ZERO_NOT_DERIVED" for row in zero),
            "tail-zero theorem is not falsely promoted",
        ),
        (
            "VAL1583_3_finite_tail_schema",
            {row["tail_component"] for row in finite} == required_tails and all(row["no_cancellation"] == "True" for row in finite),
            "finite tail ledger covers all tail terms with no-cancellation policy",
        ),
        (
            "VAL1583_4_gr_completion_schema",
            {row["gr_requirement"] for row in completion} == required_gr,
            "GR completion map covers gamma, beta, conservation, matter coupling and Newtonian source limit",
        ),
        (
            "VAL1583_5_runner_blocks",
            all(row["can_score"] == "False" for row in runner),
            "Cassini tail runner blocks scoring and gamma-only GR shortcut",
        ),
        (
            "VAL1583_6_claim_gates_closed",
            all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates),
            "all claim gates remain closed",
        ),
        (
            "VAL1583_7_decision_next",
            any(row["decision"] == "NEXT_1584_PPN_BETA_CONSERVATION_COMMON_MATTER_GATE" for row in decisions),
            "decision selects beta/conservation/common matter gate",
        ),
        ("VAL1583_8_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1583 CSVs parse cleanly"),
        ("VAL1583_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1583_10_no_raw_accepted", not has_1583_rows(RAB_RAW) and not has_1583_rows(RAB_ACCEPTED), "no 1583 rows written to raw/accepted finite directories"),
        ("VAL1583_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1583_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1583_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1583 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1583_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1583 PPN tail-zero or finite-tail-bound validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    completion: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1583 - PPN Tail-Zero Theorem Or First Finite Tail Bound",
                "## Verdict\n"
                "- The PPN tail-zero theorem is now explicit but not parent-signed: gauge, source, boundary, readout and higher-order tails each have a plausible zero route, but at least one ownership clause is missing in every route.\n"
                "- A finite absolute tail-bound ledger is staged for `delta_gauge`, `delta_source`, `delta_boundary`, `delta_readout`, and the second-order PPN tail; all rows remain missing-valued nonclaims.\n"
                "- The gamma/q_R_hat branch is useful but cannot be upgraded to GR: beta, Bianchi-like conservation, common matter coupling and the Newtonian source denominator are still separate gates.\n"
                "- Cassini remains blocked because no complete MTS prediction row exists and gamma-only GR is refused.\n"
                "- No PPN, Cassini, local GR/Newton, tail-zero, finite-tail, R10, WEP, clock, orbital, beta, or conservation claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## PPN Tail-Zero Theorem Attempt",
                md_table(zero, ["tail_zero_id", "tail_component", "zero_condition", "effect_if_signed", "status", "blocking_gap"]),
                "## First Finite Tail Bound Ledger",
                md_table(finite, ["finite_tail_id", "tail_component", "required_units", "required_source_form", "current_status", "no_cancellation"]),
                "## GR Completion Gate",
                md_table(completion, ["completion_id", "gr_requirement", "required_statement", "current_status", "blocking_gap"]),
                "## Cassini Tail Runner",
                md_table(runner, ["runner_id", "case", "status", "reason", "can_score"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    zero = tail_zero_attempt_rows()
    finite = finite_tail_ledger_rows()
    completion = gr_completion_rows()
    runner = cassini_tail_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        TAIL_ZERO_ATTEMPT,
        FINITE_TAIL_LEDGER,
        GR_COMPLETION,
        CASSINI_TAIL_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(TAIL_ZERO_ATTEMPT, zero)
    write_csv(FINITE_TAIL_LEDGER, finite)
    write_csv(GR_COMPLETION, completion)
    write_csv(CASSINI_TAIL_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, zero, finite, completion, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
