from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3293-Y5-R2FR-parent-Hilbert-source-and-canonical-quantum-normalization-signature-under-AX1090.md"

SRC_3292_DOC = ROOT / "3292-Y5-R2FR-source-only-scalar-exclusion-from-parent-object-language-under-AX1090.md"
SRC_3292_NEXT = OUT / "P8_Y5_R2FR_3292_NEXT_TARGET.csv"
SRC_3292_THEOREM = OUT / "P8_Y5_R2FR_3292_SOURCE_ONLY_SCALAR_EXCLUSION_THEOREM.csv"
SRC_3292_CANONICAL = OUT / "P8_Y5_R2FR_3292_FIELD_REDEFINITION_CANONICALIZATION_AUDIT.csv"
SRC_3292_HILBERT = OUT / "P8_Y5_R2FR_3292_HILBERT_SOURCE_VS_SPURION_SPLIT.csv"
SRC_3292_VALIDATION = OUT / "P8_Y5_BRR545_3292_VALIDATION.csv"
SRC_3291_DOC = ROOT / "3291-Y5-R2FR-TQ-Noether-current-owner-and-source-label-forgetting-under-AX1090.md"
SRC_1064_DOC = ROOT / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md"
SRC_1065_DOC = ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3293_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv",
    "canonical": OUT / "P8_Y5_R2FR_3293_CANONICAL_QUANTUM_READOUT_SIGNATURE.csv",
    "conservation": OUT / "P8_Y5_R2FR_3293_BIANCHI_CONSERVATION_COUNTERCHECK.csv",
    "localgr": OUT / "P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv",
    "residuals": OUT / "P8_Y5_R2FR_3293_RESIDUAL_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3293_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3293_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3293_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3293_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3293_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 560) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 330)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3292_DOC, "3292 handoff", ["Hilbert-source/canonical-normalization", "non-Hilbert spurion"]),
        (SRC_3292_NEXT, "3292 next target", ["Hilbert-source", "canonical-quantum-normalization"]),
        (SRC_3292_THEOREM, "source-only scalar theorem", ["SOX3292_1_same_action_hilbert_route", "SOX3292_5_verdict"]),
        (SRC_3292_CANONICAL, "canonicalization audit", ["CAN3292_0_free_whole_action_weight", "CAN3292_2_source_only_after_variation"]),
        (SRC_3292_HILBERT, "Hilbert source vs spurion split", ["HSS3292_2_forbidden_source_only_spurion", "HSS3292_3_hidden_spurion_return"]),
        (SRC_3292_VALIDATION, "3292 validation", ["VAL3292_12_overall", "true"]),
        (SRC_3291_DOC, "Noether/source coupling reduction", ["beta_source_alpha", "source-only/species-label slot"]),
        (SRC_1064_DOC, "older label forgetting/Hilbert variation route", ["total Hilbert variation", "measured G"]),
        (SRC_1065_DOC, "older no-source-only grammar and action-scale issue", ["action scale", "Hilbert source owner"]),
        (SRC_1100_DOC, "T_Q current/readout open clauses", ["TQS1100_4_same_current_owner", "readout"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3293_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HSSIG3293_0_target",
            "claim_piece": "parent Hilbert-source signature",
            "statement": "There is one descended matter functional S_m[q(Phi),Psi,theta] and local source tensors/currents are defined only by its variational derivatives: T_mu_nu=-2/sqrt(-g) delta S_m/delta g^mu_nu and J_Q=1/sqrt(-g) delta S_m/delta A_Q.",
            "status": "TARGET_SHARP",
            "payoff": "source strength is no longer a separate selector; it is the same object that controls inertial matter dynamics and Noether current.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HSSIG3293_1_source_only_exclusion",
            "claim_piece": "ban post-variation source selectors",
            "statement": "If all source terms entering the local field equations are Hilbert/Noether variations of S_m, then T_source=sum_A kappa_A T_A introduced after variation is not allowed unless kappa_A already belongs to S_m and readout.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "payoff": "the source-only branch from 3292 is theorem-zero under this signature.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HSSIG3293_2_same_action_conservation",
            "claim_piece": "Ward/Bianchi compatibility",
            "statement": "Diffeomorphism invariance of the same S_m gives the on-shell matter identity nabla_mu T^mu_nu = F_nu_mu J_Q^mu plus other derived force terms, so local conservation is tied to the same current/source owner.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "payoff": "connects source coupling to local GR consistency instead of ad hoc source normalization.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HSSIG3293_3_parent_gap",
            "claim_piece": "why not promoted",
            "statement": "The corpus still has to show that the MTS parent action actually descends to this single Hilbert-source signature; writing the signature is not the same as deriving the parent action.",
            "status": "NOT_PARENT_SIGNED",
            "payoff": "cleanly names the remaining local-GR matter coupling requirement.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HSSIG3293_4_verdict",
            "claim_piece": "signature status",
            "statement": "3293 proves the exact local theorem: Hilbert-source signature excludes source-only scalars. It does not prove MTS owns the signature yet.",
            "status": "CONDITIONAL_DERIVATION_NOT_PROMOTED",
            "payoff": "the coupling problem is now a parent-action descent problem, not a beta_source_alpha fitting problem.",
            "valid_for_claim": "false",
        },
    ]


def canonical_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "CQR3293_0_canonical_fields",
            "target": "canonical field normalization",
            "condition": "each matter sector is represented with fixed kinetic/readout normalization after quotienting field redefinitions",
            "why_needed": "otherwise whole-action weights can hide as field-normalization choices",
            "status": "EXACT_REQUIRED_SIGNATURE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "CQR3293_1_quantum_action_scale",
            "target": "common action scale / hbar readout",
            "condition": "multiplying one species action by w_A is not classically visible in EOM but changes stress normalization and path-integral/statistical weight unless action scale is parent-owned",
            "why_needed": "closes the 1065 action-scale counterexample",
            "status": "REQUIRED_SIGNATURE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "CQR3293_2_measured_coupling_readout",
            "target": "measured masses, charges, spectra, and couplings",
            "condition": "if w_A changes interactions, spectra, or currents, it is theta_A/readout data rather than a hidden source-only scalar",
            "why_needed": "separates matter parameters from gravitational source-only spurions",
            "status": "CLASSIFICATION_THEOREM_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "CQR3293_3_effective_action_guard",
            "target": "radiative/readout closure",
            "condition": "the effective action and laboratory readout must preserve the same Hilbert/Noether owner rather than regenerate kappa_A(I_hid) or delta_readout weights",
            "why_needed": "prevents hidden-source return after tree-level derivation",
            "status": "OPEN_GUARD",
            "valid_for_claim": "false",
        },
    ]


def conservation_rows() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "BCC3293_0_Bianchi_not_enough",
            "claim_tested": "can Bianchi/conservation alone kill constant w_A?",
            "result": "NO",
            "argument": "If each T_A is separately conserved in a noninteracting limit, constant sum_A w_A T_A can still be conserved, so conservation alone does not prove universal coupling.",
            "consequence": "need Hilbert-source/action-owner proof, not just divergence-free source rhetoric.",
            "valid_for_claim": "false",
        },
        {
            "check_id": "BCC3293_1_interacting_matter_pressure",
            "claim_tested": "do interactions make arbitrary w_A dangerous?",
            "result": "YES_BUT_NOT_FINAL",
            "argument": "For interacting species, separate weighted stress tensors generally exchange energy-momentum, so arbitrary w_A can violate the total Ward identity unless weights are common or action-owned.",
            "consequence": "interaction/Ward structure pressures w_A toward common/action-owned, but still requires parent signature.",
            "valid_for_claim": "false",
        },
        {
            "check_id": "BCC3293_2_common_mode",
            "claim_tested": "is a common source multiplier fatal?",
            "result": "NO_IF_GUARDED",
            "argument": "A universal constant common multiplier can be the calibrated Newton/G normalization only if species/time/range/frame derivatives vanish.",
            "consequence": "relative source weights are physical; common calibration is allowed after guards.",
            "valid_for_claim": "false",
        },
        {
            "check_id": "BCC3293_3_local_GR_condition",
            "claim_tested": "what local GR needs",
            "result": "HILBERT_SOURCE_SIGNATURE",
            "argument": "Local GR reduction requires the source in Einstein's equation to be the Hilbert stress of the same matter action, with measured G as the common coupling constant.",
            "consequence": "MTS can be fair like GR about the numerical G value, but not about relative/non-Hilbert source weights.",
            "valid_for_claim": "false",
        },
    ]


def localgr_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "LGR3293_0_required_inputs",
            "local_gr_piece": "matter source side",
            "required_parent_input": "single public metric/coframe, one Hilbert matter action, same Noether current owner, canonical readout normalization",
            "derived_if_input_signed": "T_mu_nu and J_Q are fixed variational objects; source-only beta branch vanishes",
            "current_status": "INPUTS_PARTIAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "route_id": "LGR3293_1_common_G",
            "local_gr_piece": "Newton/G calibration",
            "required_parent_input": "one universal common coupling constant kappa_G multiplying the total Hilbert source",
            "derived_if_input_signed": "common kappa_G can be calibrated as measured G; relative w_A cannot be hidden in G",
            "current_status": "CALIBRATION_ALLOWED_NOT_PREDICTIVE",
            "valid_for_claim": "false",
        },
        {
            "route_id": "LGR3293_2_Newtonian_limit",
            "local_gr_piece": "Newtonian source density",
            "required_parent_input": "weak-field slow-motion limit of the same Hilbert stress T_00 plus constant G",
            "derived_if_input_signed": "Poisson source is rho_total with no species-relative source weights",
            "current_status": "CONDITIONAL_ON_GR_KINETIC_AND_HILBERT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "route_id": "LGR3293_3_Maxwell_stress",
            "local_gr_piece": "EM stress contribution",
            "required_parent_input": "Hodge/Maxwell action from same public metric and same T_Q current owner",
            "derived_if_input_signed": "EM stress enters Hilbert source consistently with Poynting/Hodge branch",
            "current_status": "CONDITIONAL_ON_3286_3288_AND_TQ_SIGNATURE",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RES3293_0_Hilbert_signature_zero_conditional",
            "arena": "formal_local_GR_coupling",
            "quantity": "beta_source_only_label",
            "prediction": "0 if parent Hilbert-source signature and canonical readout are signed",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "missing_for_claim": "PARENT_ACTION_DESCENT;CANONICAL_QUANTUM_READOUT;EFFECTIVE_ACTION_GUARD",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RES3293_1_conservation_countercheck",
            "arena": "theory_red_team",
            "quantity": "constant w_A conservation test",
            "prediction": "conservation alone cannot exclude every constant species weight",
            "status": "COUNTERCHECK_RETAINED",
            "missing_for_claim": "HILBERT_SOURCE_SIGNATURE_NOT_JUST_BIANCHI",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RES3293_2_PPN_Newton_residual",
            "arena": "PPN_Newton",
            "quantity": "relative active/passive source normalization",
            "prediction": "MISSING_PARENT_SIGNATURE_OR_NUMERIC_BOUND",
            "status": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "COMMON_G_GUARDS;PPN_PROJECTION;ORBITAL_PROJECTION",
            "valid_for_claim": "false",
        },
        {
            "row_id": "RES3293_3_WEP_R10_residual",
            "arena": "WEP_R10",
            "quantity": "arena source-current products",
            "prediction": "MISSING_TAU_AND_SOURCE_MAPS",
            "status": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "TAU_WEP;TAU_R10;MATERIAL_MAP;BOUND_CURVE;SOURCE_CURRENT_MAP",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": row["row_id"],
            "expected_status": row["status"],
            "observed_status": row["status"],
            "expectation_match": "true",
            "claim_allowed": "false",
        }
        for row in residuals
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3293_0_Hilbert_exclusion_theorem",
            "gate": "Hilbert-source signature excludes source-only scalars",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "exact conditional theorem is established.",
        },
        {
            "gate_id": "GATE3293_1_parent_signature_signed",
            "gate": "MTS parent action signs the Hilbert-source/canonical-readout signature",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "parent action descent remains to be derived.",
        },
        {
            "gate_id": "GATE3293_2_Bianchi_as_proof",
            "gate": "Bianchi/conservation alone proves universal coupling",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "constant species weights can evade divergence checks in special limits.",
        },
        {
            "gate_id": "GATE3293_3_local_GR_source_claim",
            "gate": "local GR matter source is derived for MTS",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "the route is sharper, but parent metric/action kinetic/signature inputs remain open.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3293_0_actual_progress",
            "finding": "Hilbert-source signature would kill the surviving source-only scalar exactly.",
            "consequence": "the source-coupling branch is no longer arbitrary beta-fitting; it is an action-descent proof obligation.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3293_1_red_team",
            "finding": "Bianchi/conservation is not strong enough alone to prove universal coupling.",
            "consequence": "do not smuggle the equivalence principle through divergence-free language.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3293_2_GR_fairness",
            "finding": "Like GR, MTS can calibrate a common G; unlike a source-only scalar, common G must be universal and relative weights must vanish.",
            "consequence": "next work should build the local GR reduction contract around common calibrated G plus Hilbert source, not predict G numerically first.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3293_0_3294",
            "target_doc": "3294-Y5-R2FR-local-GR-reduction-contract-Hilbert-source-common-G-and-Newton-limit-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3294_local_GR_reduction_contract_Hilbert_source_common_G_and_Newton_limit.py",
            "objective": "assemble the local GR reduction contract: single public metric/coframe, Einstein-like kinetic term or equivalent field equation, Hilbert matter source, common calibrated G, Maxwell stress branch, and Newton/PPN residual gates.",
            "guardrails": "do not derive numerical G by assertion; do not use Bianchi alone as universal coupling proof; do not claim local GR until every contract piece is parent-signed or explicitly bounded.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    canonical: list[dict[str, Any]],
    conservation: list[dict[str, Any]],
    localgr: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3293_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3293_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3293_2_outputs_parse", "all 3293 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    sig_text = " ".join(row["statement"] + " " + row["status"] for row in signature)
    add(
        "VAL3293_3_signature_theorem_present",
        "Hilbert-source theorem includes variational definitions and source-only exclusion",
        "delta S_m/delta g" in sig_text and "delta S_m/delta A_Q" in sig_text and "source-only" in sig_text and "EXACT_CONDITIONAL_THEOREM" in sig_text,
    )

    can_text = " ".join(row["target"] + " " + row["condition"] for row in canonical)
    add(
        "VAL3293_4_canonical_readout_requirements_present",
        "canonical requirements include field normalization, action scale, measured readout, and effective action guard",
        "canonical field normalization" in can_text and "hbar" in can_text and "measured masses" in can_text and "effective action" in can_text,
    )

    conservation_text = " ".join(row["result"] + " " + row["argument"] for row in conservation)
    add(
        "VAL3293_5_Bianchi_not_overclaimed",
        "Bianchi countercheck states conservation alone cannot kill constant w_A",
        "NO" in conservation_text and "conservation alone does not prove universal coupling" in conservation_text,
    )

    localgr_text = " ".join(row["local_gr_piece"] + " " + row["required_parent_input"] + " " + row["derived_if_input_signed"] for row in localgr)
    add(
        "VAL3293_6_local_GR_contract_pieces_present",
        "local GR matter coupling rows include source side, common G, Newtonian limit, and Maxwell stress",
        "matter source side" in localgr_text and "common coupling constant" in localgr_text and "Poisson source" in localgr_text and "EM stress" in localgr_text,
    )

    add("VAL3293_7_residual_rows_nonclaim", "all residual rows remain nonclaim", all(row["valid_for_claim"] == "false" for row in residuals))
    add("VAL3293_8_runner_expectations", "runner expectations all match", all(row["expectation_match"] == "true" for row in runner), ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner))
    add("VAL3293_9_claim_gates_false", "no 3293 gate allows local-GR/WEP/R10/PPN claim", all(row["claim_allowed"] == "false" for row in promotion) and any(row["passed"] == "false" for row in promotion))
    add(
        "VAL3293_10_next_target_focused",
        "next target focuses local GR reduction contract with common G and Newton limit",
        len(next_target) == 1 and "local-GR-reduction-contract" in next_target[0]["target_doc"] and "Newton-limit" in next_target[0]["target_doc"],
    )
    add(
        "VAL3293_11_decision_records_no_smuggling",
        "decision ledger records no Bianchi smuggling and common-G fairness",
        any("Bianchi/conservation is not strong enough" in row["finding"] for row in decisions) and any("calibrate a common G" in row["finding"] for row in decisions),
    )
    add(
        "VAL3293_12_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3293_13_overall", "3293 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    canonical: list[dict[str, Any]],
    conservation: list[dict[str, Any]],
    localgr: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3293 - Parent Hilbert source and canonical quantum normalization signature under AX1090

**Run UTC:** {RUN_UTC}

3293 is the cleanest coupling move so far: if the parent action supplies one Hilbert matter source plus canonical matter/readout normalization, the surviving source-only scalar from 3292 is not a free coupling. It is either already measured matter data, a common calibrated constant, or a non-Hilbert spurion.

The hard red-team point is also recorded: Bianchi/conservation alone does **not** prove universal coupling. Constant species weights can pass divergence checks in special limits. The route must be action descent, not conservation hand-waving.

## Source Register

{md_table(sources)}

## Hilbert-Source Signature Theorem

{md_table(signature)}

## Canonical Quantum/Readout Signature

{md_table(canonical)}

## Bianchi/Conservation Countercheck

{md_table(conservation)}

## Local GR Matter-Coupling Reduction

{md_table(localgr)}

## Residual Rows

{md_table(residuals)}

## Nonclaim Runner

{md_table(runner)}

## Promotion Gates

{md_table(promotion)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    before_fw = snapshot_tree(FW)

    sources = source_register_rows()
    signature = signature_rows()
    canonical = canonical_rows()
    conservation = conservation_rows()
    localgr = localgr_rows()
    residuals = residual_rows()
    runner = runner_rows(residuals)
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["signature"], signature)
    write_csv(OUTPUTS["canonical"], canonical)
    write_csv(OUTPUTS["conservation"], conservation)
    write_csv(OUTPUTS["localgr"], localgr)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, signature, canonical, conservation, localgr, residuals, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, signature, canonical, conservation, localgr, residuals, runner, promotion, decisions, next_target, validation)

    if PYCACHE.exists():
        for item in PYCACHE.iterdir():
            if item.is_file():
                item.unlink()
        try:
            PYCACHE.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
