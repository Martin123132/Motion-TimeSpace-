from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_AT = datetime.now(timezone.utc)
RUN_UTC = RUN_STARTED_AT.isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3101"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3101-Y5-R2FR-single-public-metric-or-finite-coupling-parent-action-choice-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3101_00_3100_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3100_NEXT_TARGET.csv",
        "needles": ["NEXT3100_0_primary", "single-public-metric"],
        "role": "3100 selects the zero-route versus finite-coupling parent-action fork.",
    },
    "SRC3101_01_3100_doc": {
        "path": ROOT / "3100-Y5-R2FR-parent-Hessian-and-tauPPN-extraction-for-cg-under-AX1090.md",
        "needles": ["no source-backed numeric parent inputs", "single-public-metric"],
        "role": "3100 says the finite coefficient route lacks parent-owned inputs and points to the fork.",
    },
    "SRC3101_02_1030_doc": {
        "path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "needles": ["quotient naturality", "terminal public metric", "c_g=0"],
        "role": "1030 isolates the strongest no-shadow-frame route.",
    },
    "SRC3101_03_1030_contract": {
        "path": RESIDUALS / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
        "needles": ["SPM1030_2_no_shadow_frame_slot", "EXACT_CLOSURE_CLAUSE_NOT_DERIVED"],
        "role": "1030 machine-readable public-metric/no-shadow contract.",
    },
    "SRC3101_04_3098_derivation": {
        "path": RESIDUALS / "P8_Y5_R2FR_3098_COMMON_FRAME_DERIVATION.csv",
        "needles": ["A_g(Xhat)", "DER3098_4_cg_translation"],
        "role": "3098 finite common-frame coupling ansatz.",
    },
    "SRC3101_05_3099_canonical": {
        "path": RESIDUALS / "P8_Y5_R2FR_3099_CANONICAL_X_NORMALIZATION_DERIVATION.csv",
        "needles": ["CN3099_3_alpha_eff_definition", "CN3099_4_rescaling_guard"],
        "role": "3099 canonical normalization and invariant-coupling formula.",
    },
    "SRC3101_06_3100_contract": {
        "path": RESIDUALS / "P8_Y5_R2FR_3100_PARENT_ACTION_CONTRACT_REQUIRED.csv",
        "needles": ["PAC3100_2_matter_frame_choice", "CHOICE_NOT_PARENT_SIGNED"],
        "role": "3100 parent-action contract requiring matter-frame choice.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3101_SOURCE_REGISTER.csv",
    "ansatz": RESIDUALS / "P8_Y5_R2FR_3101_PARENT_ACTION_ANSATZ_FORK.csv",
    "zero_theorem": RESIDUALS / "P8_Y5_R2FR_3101_VERTICAL_DESCENT_ZERO_THEOREM.csv",
    "finite_fork": RESIDUALS / "P8_Y5_R2FR_3101_FINITE_COUPLING_FORK_REQUIREMENTS.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3101_COUNTERMODEL_AUDIT.csv",
    "branch_verdict": RESIDUALS / "P8_Y5_R2FR_3101_BRANCH_VERDICT.csv",
    "claim_gate": RESIDUALS / "P8_Y5_R2FR_3101_CLAIM_GATE.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3101_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_R2FR_3101_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3101_VALIDATION.csv",
}

BRANCH_COPIES = {
    OUTPUTS["zero_theorem"]: PARENT_ACTION / "vertical_descent_cg_zero_theorem_3101_CONDITIONAL.csv",
    OUTPUTS["finite_fork"]: PARENT_ACTION / "finite_cg_parent_action_requirements_3101_NOT_SIGNED.csv",
    OUTPUTS["branch_verdict"]: LOCAL_BOUNDS / "cg_zero_or_finite_fork_verdict_3101_NONCLAIM.csv",
    OUTPUTS["next"]: RAB_QUEUE / "JR3101_verify_Xhat_verticality_and_matter_descent_NEXT_NONCLAIM.csv",
}


def base_row() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def with_base(row: dict[str, Any]) -> dict[str, Any]:
    merged = base_row()
    merged.update(row)
    return merged


def ensure_dirs() -> None:
    for path in [RESIDUALS, PARENT_ACTION, LOCAL_BOUNDS, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        resolved = PYCACHE.resolve()
        if str(resolved).startswith(str(ROOT.resolve())):
            shutil.rmtree(resolved)


def sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        csv_rows(path)
    except Exception:
        return False
    return True


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCES.items():
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        parses = csv_parses(path) if exists and path.suffix.lower() == ".csv" else exists
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            with_base(
                {
                    "source_id": source_id,
                    "path": str(path),
                    "exists": exists,
                    "parseable": parses,
                    "needles_found": not missing,
                    "missing_needles": ";".join(missing),
                    "sha256": sha256(path),
                    "role": spec["role"],
                }
            )
        )
    return rows


def ansatz_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "ansatz_id": "ANS3101_0_parent_configuration",
            "object": "parent configuration and observable quotient",
            "construction": "Phi in P, q:P->Q_obs, public geometry e_pub=e_pub(q(Phi))",
            "meaning": "ordinary observables are functions of the quotient geometry, not arbitrary representatives",
            "status": "CONSTRUCTIVE_DOMAIN_SPLIT",
        },
        {
            "ansatz_id": "ANS3101_1_vertical_mode",
            "object": "local residual direction Xhat",
            "construction": "v_X := partial/Phi along Xhat with Dq[v_X]=0",
            "meaning": "Xhat is pure representative/vertical if this clause is signed",
            "status": "ZERO_ROUTE_KEY_CLAUSE",
        },
        {
            "ansatz_id": "ANS3101_2_zero_route_action",
            "object": "single-public-metric matter action",
            "construction": "S_matter = Sbar[psi, e_pub(q(Phi)), omega[e_pub], theta(q(Phi))]",
            "meaning": "ordinary matter has no independent A_g(Xhat), B_g(Xhat), marker, or shadow-frame argument",
            "status": "CONSTRUCTIVE_ZERO_ROUTE",
        },
        {
            "ansatz_id": "ANS3101_3_finite_route_action",
            "object": "finite common-frame coupling action",
            "construction": "S_matter = Sbar[psi, A_g(Xhat)^2 e_pub(q(Phi)), theta(q(Phi),Xhat)]",
            "meaning": "if this slot is allowed, c_g=d ln A_g/dXhat|0 is a real coupling and must be bounded",
            "status": "CONSTRUCTIVE_FINITE_ROUTE",
        },
        {
            "ansatz_id": "ANS3101_4_fork_rule",
            "object": "no middle fog rule",
            "construction": "Either vertical descent excludes Xhat from S_matter, giving c_g=0, or finite route owns Z_X,M_X^2,tau,S and c_g source rows.",
            "meaning": "the project cannot claim local GR while retaining an unowned shadow matter frame",
            "status": "ADOPTED_FOR_NEXT_DERIVATION",
        },
    ]
    return [with_base(row) for row in rows]


def zero_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "ZTH3101_0_assume_descent",
            "statement": "Assume ordinary matter action descends through the observable quotient.",
            "equation": "S_matter[Phi,psi]=Sbar[q(Phi),psi,theta(q(Phi))]",
            "derivation_status": "ASSUMPTION_TO_VERIFY_IN_CURRENT_CORPUS",
            "claim_effect": "removes representative variables from ordinary matter by domain",
        },
        {
            "step_id": "ZTH3101_1_vertical_direction",
            "statement": "Assume Xhat is a vertical representative direction.",
            "equation": "Dq[v_X]=0",
            "derivation_status": "ASSUMPTION_TO_VERIFY_IN_CURRENT_CORPUS",
            "claim_effect": "Xhat changes representative data without changing public geometry",
        },
        {
            "step_id": "ZTH3101_2_variation_zero",
            "statement": "Vary the descended matter action along the vertical direction.",
            "equation": "delta_X S_matter = D Sbar[q(Phi)] . Dq[v_X] = 0",
            "derivation_status": "EXACT_CONDITIONAL_PROOF_STEP",
            "claim_effect": "ordinary Hilbert source has no Xhat matter current",
        },
        {
            "step_id": "ZTH3101_3_shadow_frame_exclusion",
            "statement": "A shadow conformal frame is not quotient-natural unless it is constant along fibres.",
            "equation": "A_g(Xhat)^2 e_pub(q(Phi)) descends only if v_X[ln A_g]=0",
            "derivation_status": "EXACT_CONDITIONAL_PROOF_STEP",
            "claim_effect": "forbids common scalar fifth-force slot in ordinary matter",
        },
        {
            "step_id": "ZTH3101_4_cg_zero",
            "statement": "The finite common-frame coefficient vanishes on the descended matter domain.",
            "equation": "c_g := partial_X ln A_g|_0 = 0",
            "derivation_status": "DERIVED_IF_DESCENT_AND_VERTICALITY_SIGNED",
            "claim_effect": "silences PPN common scalar charge without needing a numeric c_g bound",
        },
        {
            "step_id": "ZTH3101_5_tau_zero",
            "statement": "If c_g is zero by action-domain exclusion, the c_g component of PPN response is zero.",
            "equation": "alpha_eff_PPN,cg = tau_PPN c_g S_PPN/sqrt(Z_X)=0",
            "derivation_status": "EXACT_CONDITIONAL_COROLLARY",
            "claim_effect": "Cassini no longer constrains this component; remaining residual vector still must close",
        },
        {
            "step_id": "ZTH3101_6_limit",
            "statement": "This proves only the right-hand matter-frame/common-scalar piece, not full GR/Newton.",
            "equation": "local_GR requires left-hand EH/Newton limit + conservation + hidden residual silence",
            "derivation_status": "SCOPE_GUARD",
            "claim_effect": "prevents overclaiming from c_g=0 alone",
        },
    ]
    return [with_base(row) for row in rows]


def finite_fork_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "req_id": "FIN3101_0_allowed_shadow_slot",
            "finite_route_requirement": "parent action explicitly allows A_g(Xhat)^2 e_pub in ordinary matter",
            "needed_formula": "A_g(Xhat)=exp(c_g Xhat+O(Xhat^2))",
            "current_status": "NOT_PARENT_SIGNED",
            "why_needed": "otherwise c_g is excluded by descent rather than bounded",
        },
        {
            "req_id": "FIN3101_1_canonical_block",
            "finite_route_requirement": "same parent action supplies Z_X and M_X^2",
            "needed_formula": "phi=M_Pl sqrt(Z_X) Xhat; lambda_X=sqrt(Z_X/M_X^2)",
            "current_status": "MISSING_ZX_MX2",
            "why_needed": "fixes normalization and arena",
        },
        {
            "req_id": "FIN3101_2_ppn_projection",
            "finite_route_requirement": "linearized response matrix supplies tau_PPN and no-cancellation envelope",
            "needed_formula": "delta gamma = tau_PPN c_g S_PPN/sqrt(Z_X)+sum residual_i",
            "current_status": "MISSING_TAUPPN_VECTOR",
            "why_needed": "turns Cassini into an MTS component statement",
        },
        {
            "req_id": "FIN3101_3_range_transfer",
            "finite_route_requirement": "S_PPN or R10/orbital transfer function is derived from lambda_X",
            "needed_formula": "S_A(lambda_X,environment) for arena A",
            "current_status": "MISSING_RANGE_TRANSFER",
            "why_needed": "prevents applying the wrong experiment to the wrong range",
        },
        {
            "req_id": "FIN3101_4_source_policy",
            "finite_route_requirement": "finite route remains nonclaim until all rows above are source-backed",
            "needed_formula": "valid_for_claim = all(FIN3101_0..FIN3101_3)",
            "current_status": "CLOSURE_ONLY_CURRENTLY",
            "why_needed": "stops coupling from becoming a free dial",
        },
    ]
    return [with_base(row) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "counter_id": "CM3101_0_covariant_Jordan_frame",
            "countermodel": "S_matter[psi,A_g(Xhat)^2 e_pub]",
            "what_it_preserves": "diffeomorphism covariance and universal WEP quietness",
            "what_it_breaks": "quotient descent / no-shadow-frame domain",
            "lesson": "covariance and WEP alone cannot prove c_g=0",
        },
        {
            "counter_id": "CM3101_1_constants_rename",
            "countermodel": "remove A_g from metric but put Xhat into masses/clocks/constants",
            "what_it_preserves": "formal single metric notation",
            "what_it_breaks": "quotient-owned constants and clock/readout silence",
            "lesson": "single metric must include constants/no-marker clauses",
        },
        {
            "counter_id": "CM3101_2_disformal_shadow",
            "countermodel": "g_m=A_g^2 e_pub + B_g(Xhat) U_mu U_nu",
            "what_it_preserves": "zero c_g possible",
            "what_it_breaks": "PPN residual silence through b_dis",
            "lesson": "c_g=0 is not enough unless shadow disformal slots are excluded or bounded",
        },
        {
            "counter_id": "CM3101_3_source_only_tail",
            "countermodel": "matter descends but non-Hilbert/support/boundary source tails remain",
            "what_it_preserves": "ordinary metric coupling",
            "what_it_breaks": "source-side GR/Newton reduction",
            "lesson": "right-hand matter descent must be paired with hidden residual cleanup",
        },
    ]
    return [with_base(row) for row in rows]


def branch_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "verdict_id": "BV3101_0_constructive_progress",
            "subject": "c_g zero route",
            "verdict": "CONDITIONAL_THEOREM_CONSTRUCTED",
            "meaning": "if Xhat is vertical and matter action descends through q, c_g=0 follows by chain rule/action-domain exclusion",
            "claim_allowed_now": False,
        },
        {
            "verdict_id": "BV3101_1_current_corpus_status",
            "subject": "current AX1090 branch",
            "verdict": "NEEDS_VERTICALITY_AND_DESCENT_VERIFICATION",
            "meaning": "the theorem is now sharper than a missing ledger, but the active corpus must prove Dq[v_X]=0 and S_matter=Sbar[q(Phi)]",
            "claim_allowed_now": False,
        },
        {
            "verdict_id": "BV3101_2_finite_route",
            "subject": "finite c_g route",
            "verdict": "DEMANDED_IF_DESCENT_FAILS",
            "meaning": "if A_g(Xhat) is physically allowed, the theory must own Z_X/M_X^2/tau/range rows and face PPN/R10/orbital tests",
            "claim_allowed_now": False,
        },
    ]
    return [with_base(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "claim_id": "CG3101_0_conditional_zero_theorem",
            "claim": "vertical quotient descent implies c_g=0",
            "allowed": True,
            "claim_allowed_for_physics": False,
            "reason": "mathematical conditional theorem only; current branch verification still required",
        },
        {
            "claim_id": "CG3101_1_current_cg_zero",
            "claim": "current MTS has c_g=0",
            "allowed": False,
            "claim_allowed_for_physics": False,
            "reason": "Xhat verticality and matter descent not yet verified in active parent action",
        },
        {
            "claim_id": "CG3101_2_finite_cg_bound",
            "claim": "current MTS has a finite bounded c_g",
            "allowed": False,
            "claim_allowed_for_physics": False,
            "reason": "finite route lacks Z_X/M_X^2/tau/range/source rows",
        },
        {
            "claim_id": "CG3101_3_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "allowed": False,
            "claim_allowed_for_physics": False,
            "reason": "c_g route is only one right-hand matter-frame gate; EH/Newton and hidden residual gates remain",
        },
    ]
    return [with_base(row) for row in rows]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT3101_0_primary",
            "next_checkpoint": "3102-Y5-R2FR-verify-Xhat-verticality-and-matter-descent-under-AX1090.md",
            "script": "scripts/Y5_R2FR_verify_Xhat_verticality_and_matter_descent_under_AX1090_3102.py",
            "objective": "inspect the active parent/spine documents for q, Xhat, e_pub, matter action, constants, and hidden source tails to see whether ZTH3101 clauses are actually signed",
            "selection_status": "selected",
            "success_condition": "current branch gets c_g=0 as parent-signed, or finite coupling route becomes mandatory with explicit source rows",
        },
        {
            "route_id": "NEXT3101_1_parallel",
            "next_checkpoint": "3102b-Y5-R2FR-hidden-residual-vector-after-cg-zero-under-AX1090.md",
            "script": "scripts/Y5_R2FR_hidden_residual_vector_after_cg_zero_under_AX1090_3102b.py",
            "objective": "if c_g zero route survives, build the residual vector for b_dis, q_nonH, support, boundary, constants and source tails",
            "selection_status": "held",
            "success_condition": "local GR/Newton right-hand side has no untracked residual hiding behind c_g=0",
        },
    ]
    return [with_base(row) for row in rows]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            with_base(
                {
                    "copy_id": f"COPY3101_{len(rows)}",
                    "source": str(source),
                    "target": str(target),
                    "target_exists": target.exists(),
                    "target_sha256": sha256(target),
                    "purpose": "constructive zero-or-finite fork handoff",
                }
            )
        )
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return lines


def validation_rows() -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    def add(validation_id: str, check_pass: bool, detail: str, artifact: Path | str) -> None:
        validations.append(with_base({"validation_id": validation_id, "check_pass": bool(check_pass), "detail": detail, "artifact": str(artifact)}))

    sources = csv_rows(OUTPUTS["sources"])
    ansatz = csv_rows(OUTPUTS["ansatz"])
    zero_theorem = csv_rows(OUTPUTS["zero_theorem"])
    finite_fork = csv_rows(OUTPUTS["finite_fork"])
    countermodels = csv_rows(OUTPUTS["countermodels"])
    branch_verdict = csv_rows(OUTPUTS["branch_verdict"])
    claim_gate = csv_rows(OUTPUTS["claim_gate"])
    next_targets = csv_rows(OUTPUTS["next"])

    add("VAL3101_00_sources_csv", OUTPUTS["sources"].exists(), "source register exists", OUTPUTS["sources"])
    add("VAL3101_01_sources_exist", all(row["exists"] == "True" for row in sources), "every cited source path exists", OUTPUTS["sources"])
    add("VAL3101_02_sources_parse", all(row["parseable"] == "True" for row in sources), "every cited csv source parses", OUTPUTS["sources"])
    add("VAL3101_03_sources_needles", all(row["needles_found"] == "True" for row in sources), "all source needles found", OUTPUTS["sources"])
    add("VAL3101_04_doc_exists", DOC.exists(), "checkpoint doc exists", DOC)
    add("VAL3101_05_ansatz_fork", any(row["ansatz_id"] == "ANS3101_4_fork_rule" for row in ansatz), "zero-or-finite fork rule recorded", OUTPUTS["ansatz"])
    add("VAL3101_06_zero_chain_rule", any(row["step_id"] == "ZTH3101_2_variation_zero" and "Dq[v_X] = 0" in row["equation"] for row in zero_theorem), "chain-rule zero proof step recorded", OUTPUTS["zero_theorem"])
    add("VAL3101_07_cg_zero_conditional", any(row["step_id"] == "ZTH3101_4_cg_zero" and "c_g" in row["equation"] and "= 0" in row["equation"] for row in zero_theorem), "conditional c_g=0 theorem recorded", OUTPUTS["zero_theorem"])
    add("VAL3101_08_scope_guard", any(row["step_id"] == "ZTH3101_6_limit" for row in zero_theorem), "scope guard prevents local-GR overclaim", OUTPUTS["zero_theorem"])
    add("VAL3101_09_finite_requirements", len(finite_fork) >= 5 and all(row["valid_for_claim"] == "False" for row in finite_fork), "finite route requirements remain nonclaim", OUTPUTS["finite_fork"])
    add("VAL3101_10_countermodels", len(countermodels) >= 4, "countermodels included", OUTPUTS["countermodels"])
    add("VAL3101_11_branch_constructive", any(row["verdict_id"] == "BV3101_0_constructive_progress" and row["verdict"] == "CONDITIONAL_THEOREM_CONSTRUCTED" for row in branch_verdict), "constructive theorem verdict recorded", OUTPUTS["branch_verdict"])
    add("VAL3101_12_current_not_claimed", any(row["verdict_id"] == "BV3101_1_current_corpus_status" and row["claim_allowed_now"] == "False" for row in branch_verdict), "current branch not overclaimed", OUTPUTS["branch_verdict"])
    add("VAL3101_13_claim_gate_blocks_current", any(row["claim_id"] == "CG3101_1_current_cg_zero" and row["allowed"] == "False" for row in claim_gate), "current c_g=0 claim remains blocked until verified", OUTPUTS["claim_gate"])
    add("VAL3101_14_next_primary", any(row["route_id"] == "NEXT3101_0_primary" and row["selection_status"] == "selected" for row in next_targets), "primary next target selected", OUTPUTS["next"])
    add("VAL3101_15_branch_copies_exist", all(target.exists() for target in BRANCH_COPIES.values()), "all branch copies exist", OUTPUTS["copies"])
    add("VAL3101_16_branch_copies_parse", all(csv_parses(target) for target in BRANCH_COPIES.values()), "all branch copies parse", OUTPUTS["copies"])
    fw_hits = []
    if FORMALIZATION.exists():
        fw_hits = [path for path in FORMALIZATION.rglob("*3101*") if datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= RUN_STARTED_AT]
    add("VAL3101_17_formalization_untouched", len(fw_hits) == 0, "no formalization-workbench 3101 artifacts modified by this run", FORMALIZATION)
    add("VAL3101_18_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE)
    return validations


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3101 - Y5 R2FR single-public-metric or finite-coupling parent action choice under AX1090",
        "",
        "**Progress:** 3101 is constructive, not just diagnostic. It builds the parent-action fork: if ordinary matter descends through the observable quotient and `Xhat` is vertical, the common matter-frame coupling is forced to vanish; if not, MTS must own a finite fifth-force coupling with source rows.",
        "",
        "**Main conditional theorem:** `S_matter=Sbar[q(Phi)]` and `Dq[v_X]=0` imply `delta_X S_matter=0`. A shadow frame `A_g(Xhat)^2 e_pub` descends only if `partial_X ln A_g=0`, hence `c_g=0`.",
        "",
        "**Current verdict:** this is a real forward derivation route, but not yet a current-MTS claim. The next task is to verify whether the active AX1090 parent/spine actually signs quotient descent, verticality, quotient-owned constants, and hidden-source silence.",
        "",
        "## Source Register",
        *md_table(data["sources"], ["source_id", "path", "exists", "parseable", "needles_found", "missing_needles", "role"]),
        "",
        "## Parent Action Ansatz Fork",
        *md_table(data["ansatz"], ["ansatz_id", "object", "construction", "meaning", "status"]),
        "",
        "## Vertical Descent Zero Theorem",
        *md_table(data["zero_theorem"], ["step_id", "statement", "equation", "derivation_status", "claim_effect"]),
        "",
        "## Finite Coupling Fork Requirements",
        *md_table(data["finite_fork"], ["req_id", "finite_route_requirement", "needed_formula", "current_status", "why_needed"]),
        "",
        "## Countermodel Audit",
        *md_table(data["countermodels"], ["counter_id", "countermodel", "what_it_preserves", "what_it_breaks", "lesson"]),
        "",
        "## Branch Verdict",
        *md_table(data["branch_verdict"], ["verdict_id", "subject", "verdict", "meaning", "claim_allowed_now"]),
        "",
        "## Claim Gate",
        *md_table(data["claim_gate"], ["claim_id", "claim", "allowed", "claim_allowed_for_physics", "reason"]),
        "",
        "## Next Target",
        *md_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Branch Copies",
        *md_table(data["copies"], ["copy_id", "source", "target", "target_exists", "purpose"]),
        "",
        "## Validation",
        *md_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()

    data = {
        "sources": source_register(),
        "ansatz": ansatz_rows(),
        "zero_theorem": zero_theorem_rows(),
        "finite_fork": finite_fork_rows(),
        "countermodels": countermodel_rows(),
        "branch_verdict": branch_verdict_rows(),
        "claim_gate": claim_gate_rows(),
        "next": next_rows(),
    }

    write_csv(OUTPUTS["sources"], data["sources"])
    write_csv(OUTPUTS["ansatz"], data["ansatz"])
    write_csv(OUTPUTS["zero_theorem"], data["zero_theorem"])
    write_csv(OUTPUTS["finite_fork"], data["finite_fork"])
    write_csv(OUTPUTS["countermodels"], data["countermodels"])
    write_csv(OUTPUTS["branch_verdict"], data["branch_verdict"])
    write_csv(OUTPUTS["claim_gate"], data["claim_gate"])
    write_csv(OUTPUTS["next"], data["next"])

    data["copies"] = copy_rows()
    write_csv(OUTPUTS["copies"], data["copies"])

    remove_pycache()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if row["check_pass"])
    total = len(data["validation"])
    print(f"3101 constructive zero-or-finite fork written: {passed}/{total} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
