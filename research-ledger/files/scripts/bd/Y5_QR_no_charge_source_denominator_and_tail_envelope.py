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
QUARANTINE = MICROSCOPE / "quarantine" / "1582"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1582-Y5-QR-no-charge-source-denominator-and-tail-envelope.md"

SOURCE_FILES = {
    "1581_doc": ROOT / "1581-Y5-RAB-qRhat-profile-and-Cassini-bound-row-or-no-charge-return.md",
    "1581_validation": OUT / "P8_Y5_BRR545_1581_VALIDATION.csv",
    "1581_profile": OUT / "P8_Y5_PARENT_QLOC_1581_QRHAT_PROFILE_DERIVATION.csv",
    "1581_bound": OUT / "P8_Y5_PARENT_QLOC_1581_CASSINI_QR_BOUND_ROW_NONCLAIM.csv",
    "1581_nocharge": OUT / "P8_Y5_PARENT_QLOC_1581_NO_CHARGE_RETURN_AUDIT.csv",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "1577_nocharge": OUT / "P8_Y5_PARENT_QLOC_1577_QR_NO_CHARGE_THEOREM_AUDIT.csv",
    "1575_matter_descent": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1581_doc": ["NEXT_1582_QR_NO_CHARGE_SOURCE_DENOMINATOR_AND_TAIL_ENVELOPE", "Q_R=0/tails=0"],
    "1581_validation": ["VAL1581_OVERALL", "PASS"],
    "1581_profile": ["PROF1581_3_ppn_ratio", "DERIVED_CONDITIONAL_BOUND_TARGET"],
    "1581_bound": ["CB1581_0_qRhat", "4.6e-05"],
    "1581_nocharge": ["NCR1581_4_verdict", "NEXT_ROUTE"],
    "06_source_neutrality": ["delta S_boundary = [W R_AB' + Pi_R] delta R_AB|_surface.", "Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1."],
    "1577_nocharge": ["NCA1577_4_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1575_matter_descent": ["MDS1575_4_boundary", "OPEN"],
    "10_observer": ["gamma - 1 = 0 after R_AB=0.", "Bianchi-like consistency identity"],
    "local_bound_claims": ["Cassini_Shapiro_gamma_2003", "gamma_minus_1", "2.3e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1582_SOURCE_REGISTER.csv"
NO_CHARGE_SIGNATURE = OUT / "P8_Y5_PARENT_QLOC_1582_NO_CHARGE_SIGNATURE_AUDIT.csv"
SOURCE_DENOMINATOR = OUT / "P8_Y5_PARENT_QLOC_1582_SOURCE_DENOMINATOR_CONTRACT.csv"
TAIL_ENVELOPE = OUT / "P8_Y5_PARENT_QLOC_1582_PPN_TAIL_ENVELOPE.csv"
CASSINI_READINESS = OUT / "P8_Y5_PARENT_QLOC_1582_CASSINI_READINESS_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1582_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1582_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1582_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1582_VALIDATION.csv"

COPY_TARGETS = {
    NO_CHARGE_SIGNATURE: [
        QUARANTINE / "NO_CHARGE_SIGNATURE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "QR_no_charge_signature_audit_nonclaim_1582.csv",
    ],
    SOURCE_DENOMINATOR: [
        QUARANTINE / "SOURCE_DENOMINATOR_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "source_denominator_contract_nonclaim_1582.csv",
    ],
    TAIL_ENVELOPE: [
        QUARANTINE / "PPN_TAIL_ENVELOPE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "PPN_tail_envelope_nonclaim_1582.csv",
    ],
    CASSINI_READINESS: [
        QUARANTINE / "CASSINI_READINESS_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "Cassini_readiness_runner_nonclaim_1582.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "QR_nocharge_tail_decision_nonclaim_1582.csv",
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
                "source_id": f"SRC1582_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "Q_R no-charge source denominator and PPN tail envelope",
                **flags(),
            }
        )
    return rows


def no_charge_signature_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NCS1582_0_boundary_variation",
            "source-boundary stationarity",
            "delta S_boundary=[W R_AB' + Pi_R] delta R_AB|_surface",
            "natural boundary gives Q_R=-Pi_R",
            "FORMAL_INPUT",
            "does not set Pi_R=0",
        ),
        (
            "NCS1582_1_matter_descent",
            "ordinary matter/source descent through observed quotient geometry",
            "delta_{R_AB} S_matter_boundary=0",
            "Pi_R=0 if no hidden reciprocal source momentum exists",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "1575 boundary/descent clauses remain open",
        ),
        (
            "NCS1582_2_no_marker",
            "no source-only reciprocal marker or disformal/conformal readout term",
            "partial S_source/partial R_AB=0 at the boundary",
            "prevents fitted source charge from regenerating Q_R",
            "CONTRACT_WRITTEN_NOT_DERIVED",
            "no parent action rule forbids marker terms yet",
        ),
        (
            "NCS1582_3_proper_boundary",
            "proper/free/exact source boundary class",
            "Pi_R=0 or exact/proper term with no exterior contribution",
            "would imply Q_R=0",
            "OPEN_NOT_SIGNED",
            "source boundary class is not derived",
        ),
        (
            "NCS1582_4_verdict",
            "Q_R=0 no-charge theorem",
            "Pi_R=0 plus boundary silence -> Q_R=0 -> q_R_hat=0",
            "sufficient for gamma channel if tails vanish",
            "FAIL_CURRENT_CLAIM_NOT_PARENT_SIGNED",
            "Pi_R=0 and tail silence are not parent-signed",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "signature_id": signature_id,
            "clause": clause,
            "equation": equation,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for signature_id, clause, equation, effect_if_signed, status, blocking_gap in rows
    ]


def source_denominator_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SD1582_0_QR",
            "Q_R",
            "reciprocal charge/hair amplitude",
            "parent no-charge theorem or numeric source-backed exterior charge",
            "MISSING_QR_VALUE_OR_ZERO_THEOREM",
            "needed for q_R_hat=-Q_R/(2 kappa_W G M)",
        ),
        (
            "SD1582_1_kappaW",
            "kappa_W",
            "asymptotic radial weight normalization W=kappa_W r^2",
            "parent radial-cell normalization in same units as Q_R",
            "MISSING_WEIGHT_NORMALIZATION",
            "cannot translate Q_R into q_R_hat without it",
        ),
        (
            "SD1582_2_GM",
            "G M_source",
            "Newtonian denominator U_N=GM/r",
            "same-frame source mass and gravitational constant convention",
            "MISSING_SOURCE_DENOMINATOR_CONVENTION",
            "prevents a clean Q_R/(GM) row",
        ),
        (
            "SD1582_3_sigma",
            "sigma_Q",
            "sign convention between exterior integration and PPN gamma",
            "observer gauge and radial orientation convention",
            "MISSING_SIGN_CONVENTION",
            "irrelevant for absolute bound but required for prediction sign",
        ),
        (
            "SD1582_4_radius_domain",
            "PPN weak-field domain",
            "r outside source and U_N<<1",
            "domain map from source boundary to Cassini light-propagation path",
            "MISSING_DOMAIN_MAP",
            "Cassini cannot score without path/domain compatibility",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "denominator_id": denominator_id,
            "symbol": symbol,
            "role": role,
            "required_source": required_source,
            "current_status": current_status,
            "why_needed": why_needed,
            **flags(),
        }
        for denominator_id, symbol, role, required_source, current_status, why_needed in rows
    ]


def tail_envelope_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TAIL1582_0_core",
            "core reciprocal hair",
            "|Q_R|/(2 |kappa_W| G M)",
            "MISSING_QR_KAPPA_GM",
            "must be zero-proved or bounded directly",
        ),
        (
            "TAIL1582_1_gauge",
            "delta_gauge",
            "PPN radial-gauge/observer-map mismatch",
            "MISSING_GAUGE_ZERO_OR_BOUND",
            "cannot be cancelled against Q_R",
        ),
        (
            "TAIL1582_2_source",
            "delta_source",
            "source denominator and interior matching residual",
            "MISSING_SOURCE_TAIL_ZERO_OR_BOUND",
            "contains hidden reciprocal source momentum risk",
        ),
        (
            "TAIL1582_3_boundary",
            "delta_boundary",
            "boundary/worldtube/corner term",
            "MISSING_BOUNDARY_TAIL_ZERO_OR_BOUND",
            "must include Pi_R/B_R contribution absolutely",
        ),
        (
            "TAIL1582_4_readout",
            "delta_readout",
            "matter/readout/coframe projection tail",
            "MISSING_READOUT_TAIL_ZERO_OR_BOUND",
            "matter descent/no-marker clauses remain unsigned",
        ),
        (
            "TAIL1582_5_higher_order",
            "O(U_N) PPN correction",
            "post-linear beta/conservation tail",
            "MISSING_SECOND_ORDER_CONTROL",
            "gamma alone does not prove full GR reduction",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "tail_id": tail_id,
            "tail_component": tail_component,
            "absolute_envelope_term": absolute_envelope_term,
            "current_status": current_status,
            "claim_rule": claim_rule,
            "no_cancellation": True,
            **flags(),
        }
        for tail_id, tail_component, absolute_envelope_term, current_status, claim_rule in rows
    ]


def cassini_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "CR1582_0_sufficient_zero",
            "case": "Q_R=0 and all PPN tails zero",
            "formula": "gamma_minus_1=0",
            "status": "SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED",
            "can_score": False,
            "blocker": "Pi_R=0/tail silence not parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "CR1582_1_absolute_bound",
            "case": "finite Q_R with absolute tail envelope",
            "formula": "|Q_R|/(2|kappa_W|GM)+|delta_gauge|+|delta_source|+|delta_boundary|+|delta_readout|+|O(U_N)| <= 2.3e-05",
            "status": "NOT_RUN_COMPONENTS_MISSING",
            "can_score": False,
            "blocker": "Q_R, kappa_W, source denominator and every tail bound are missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "CR1582_2_forbidden_cancellation",
            "case": "Q_R cancels a tail or gauge term",
            "formula": "signed cancellations in gamma_minus_1",
            "status": "REFUSE_PLACEHOLDER",
            "can_score": False,
            "blocker": "no-cancellation policy requires absolute envelope",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "CR1582_3_claim_readiness",
            "case": "Cassini/local-GR claim",
            "formula": "score only after Q_R/kappa_W/GM and all tails are signed or bounded",
            "status": "BLOCKED_NO_CLAIM",
            "can_score": False,
            "blocker": "no complete MTS prediction row exists",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1582_0_nocharge", "Q_R=0 no-charge theorem", "BLOCKED_NO_CLAIM", "Pi_R=0/source-boundary neutrality is sufficient but not parent-signed"),
        ("GATE1582_1_denominator", "source denominator Q_R/(kappa_W GM) is score-ready", "BLOCKED_NO_CLAIM", "Q_R, kappa_W, GM convention and domain map are missing"),
        ("GATE1582_2_tail_envelope", "PPN tail envelope complete", "BLOCKED_NO_CLAIM", "gauge/source/boundary/readout/second-order tails are missing"),
        ("GATE1582_3_Cassini", "Cassini PPN comparison can be scored", "BLOCKED_NO_CLAIM", "readiness runner blocks every case except conditional nonclaim zero"),
        ("GATE1582_4_local_GR", "derived local GR/Newton branch", "BLOCKED_NO_CLAIM", "gamma channel is not enough without beta, conservation and common matter coupling"),
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
            "DEC1582_0_nocharge_status",
            "NO_CHARGE_SUFFICIENT_BUT_UNSIGNED",
            "Pi_R=0 would kill Q_R, but current corpus does not derive Pi_R=0 from the parent source action",
            "do not claim Q_R=0 or local GR",
        ),
        (
            "DEC1582_1_envelope_status",
            "ABSOLUTE_PPN_TAIL_ENVELOPE_WRITTEN",
            "Cassini scoring now requires |Q_R|/(2|kappa_W|GM) plus absolute tails, with no cancellations",
            "finite fallback has a strict scoring contract but no values",
        ),
        (
            "DEC1582_2_next",
            "NEXT_1583_PPN_TAIL_ZERO_THEOREM_OR_FIRST_FINITE_TAIL_BOUND",
            "after Q_R, the next obstruction is tail silence; proving tails zero is the cleanest GR route, bounding them is the fallback",
            "try gauge/source/boundary/readout tail-zero theorem before finite-tail acquisition",
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
            "next_target": "1583-Y5-PPN-tail-zero-theorem-or-first-finite-tail-bound.md",
            "script": "scripts/Y5_PPN_tail_zero_theorem_or_first_finite_tail_bound.py",
            "objective": "attempt to prove gauge/source/boundary/readout PPN tails vanish from the parent observer/matter descent contracts, or stage the first finite absolute tail bound row",
            "do_not": "do not use cancellation against Q_R; do not score Cassini; do not treat gamma-channel control as full GR reduction",
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


def has_1582_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1582" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    nocharge = read_csv(NO_CHARGE_SIGNATURE)
    denominator = read_csv(SOURCE_DENOMINATOR)
    tails = read_csv(TAIL_ENVELOPE)
    readiness = read_csv(CASSINI_READINESS)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_denominators = {"Q_R", "kappa_W", "G M_source", "sigma_Q", "PPN weak-field domain"}
    required_tails = {"core reciprocal hair", "delta_gauge", "delta_source", "delta_boundary", "delta_readout", "O(U_N) PPN correction"}
    checks = [
        ("VAL1582_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1582_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1582_2_nocharge_unsigned",
            any(row["signature_id"] == "NCS1582_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_NOT_PARENT_SIGNED" for row in nocharge),
            "no-charge route remains sufficient but unsigned",
        ),
        (
            "VAL1582_3_denominator_complete_schema",
            {row["symbol"] for row in denominator} == required_denominators,
            "source denominator schema covers Q_R, kappa_W, GM, sign and domain",
        ),
        (
            "VAL1582_4_tail_envelope_complete_schema",
            {row["tail_component"] for row in tails} == required_tails and all(row["no_cancellation"] == "True" for row in tails),
            "PPN absolute tail envelope covers all required tail terms with no cancellation",
        ),
        (
            "VAL1582_5_cassini_readiness_blocked",
            all(row["can_score"] == "False" for row in readiness),
            "Cassini readiness runner blocks all scoring cases",
        ),
        (
            "VAL1582_6_claim_gates_closed",
            all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates),
            "all claim gates remain closed",
        ),
        (
            "VAL1582_7_decision_next",
            any(row["decision"] == "NEXT_1583_PPN_TAIL_ZERO_THEOREM_OR_FIRST_FINITE_TAIL_BOUND" for row in decisions),
            "decision selects PPN tail-zero/finite-tail target",
        ),
        ("VAL1582_8_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1582 CSVs parse cleanly"),
        ("VAL1582_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1582_10_no_raw_accepted", not has_1582_rows(RAB_RAW) and not has_1582_rows(RAB_ACCEPTED), "no 1582 rows written to raw/accepted finite directories"),
        ("VAL1582_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1582_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1582_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1582 paths are outside formalization-workbench; git status is clean when available"),
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
            "check_id": "VAL1582_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1582 Q_R no-charge source denominator and tail-envelope validation",
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
    nocharge: list[dict[str, Any]],
    denominator: list[dict[str, Any]],
    tails: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1582 - Q_R No-Charge Source Denominator And Tail Envelope",
                "## Verdict\n"
                "- The source-boundary route is sufficient but still unsigned: `Pi_R=0` would force `Q_R=0`, but the current parent action does not yet derive `Pi_R=0`.\n"
                "- Cassini scoring now has a strict no-cancellation contract: `|Q_R|/(2|kappa_W|GM)+|delta_gauge|+|delta_source|+|delta_boundary|+|delta_readout|+|O(U_N)| <= 2.3e-05`.\n"
                "- The finite fallback therefore needs real rows for `Q_R`, `kappa_W`, `GM`, domain matching, and every PPN tail before a score is allowed.\n"
                "- The clean GR route remains `Q_R=0` plus all PPN tails silent; this would close the gamma channel but still would not by itself prove full GR reduction.\n"
                "- No Cassini, PPN, local GR/Newton, no-charge, tail-zero, R10, WEP, clock, orbital, beta, or conservation claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## No-Charge Signature Audit",
                md_table(nocharge, ["signature_id", "clause", "equation", "effect_if_signed", "status", "blocking_gap"]),
                "## Source Denominator Contract",
                md_table(denominator, ["denominator_id", "symbol", "role", "required_source", "current_status", "why_needed"]),
                "## PPN Tail Envelope",
                md_table(tails, ["tail_id", "tail_component", "absolute_envelope_term", "current_status", "claim_rule", "no_cancellation"]),
                "## Cassini Readiness Runner",
                md_table(readiness, ["runner_id", "case", "formula", "status", "can_score", "blocker"]),
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
    nocharge = no_charge_signature_rows()
    denominator = source_denominator_rows()
    tails = tail_envelope_rows()
    readiness = cassini_readiness_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        NO_CHARGE_SIGNATURE,
        SOURCE_DENOMINATOR,
        TAIL_ENVELOPE,
        CASSINI_READINESS,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(NO_CHARGE_SIGNATURE, nocharge)
    write_csv(SOURCE_DENOMINATOR, denominator)
    write_csv(TAIL_ENVELOPE, tails)
    write_csv(CASSINI_READINESS, readiness)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, nocharge, denominator, tails, readiness, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
