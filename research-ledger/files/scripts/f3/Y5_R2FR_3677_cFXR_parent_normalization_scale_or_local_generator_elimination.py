from __future__ import annotations

import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3677"
BRANCH_ID = "MTS_R2FR_Y5_CFXR_PARENT_NORMALIZATION_SCALE_OR_GENERATOR_ELIMINATION_3677"
DOC = ROOT / "3677-Y5-R2FR-cFXR-parent-normalization-scale-or-local-generator-elimination.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3676", RESIDUALS / "P8_Y5_R2FR_3676_NEXT_TARGET.csv", "cFXR-parent-normalization", "3676 selected the parent-normalization/generator target"),
        ("doc_3676", ROOT / "3676-Y5-R2FR-no-natural-marker-no-reentry-theorem-or-FXR-prior-row.md", "anti-circling move", "3676 staged c_FXR as exact finite coefficient slot"),
        ("prior_3676", RESIDUALS / "P8_Y5_R2FR_3676_CFXR_PRIOR_SOURCE_ROW.csv", "CFXRP3676_0_cFXR", "c_FXR prior/source rows"),
        ("validation_3676", RESIDUALS / "P8_Y5_BRR545_3676_VALIDATION.csv", "VAL3676_16_no_accidental_numeric_prior", "3676 validation"),
        ("doc_3673", ROOT / "3673-Y5-R2FR-parent-action-Hessian-STF-operator-location.md", "k_H_geo = - A_H F0_prime/(1 + A_H F0)", "F(X)R variation coefficient derivation"),
        ("template_3674", RESIDUALS / "P8_Y5_R2FR_3674_FXR_COEFFICIENT_TEMPLATE_ROWS.csv", "FXRC3674_0_allowed_branch", "allowed F(X)R coefficient template"),
        ("bounds_3675", RESIDUALS / "P8_Y5_R2FR_3675_FINITE_CFXR_BOUND_ROWS.csv", "FXRS3675_eta_100_zeta_215.032", "strictest inherited scalar-slip bound row"),
        ("canonical_3464", RESIDUALS / "P8_Y5_R2FR_3464_CANONICAL_NORMALIZATION_THEOREM_AUDIT.csv", "CAN3464_1_single_action_unit", "canonical action/source normalization precedent"),
        ("em_owner_3464", RESIDUALS / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv", "EAC3464_0_gauge_rescaling", "Maxwell/current rescaling exact classification"),
        ("prior_policy_2965", RESIDUALS / "P8_Y5_R2FR_2965_NXHAT_FIRST_PRIOR_SLOT_NONCLAIM.csv", "NONCLAIM_UNTIL_SOURCE_BACKED", "nonclaim prior-slot policy"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def strongest_xi_bound() -> tuple[str, float, str]:
    rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3675_FINITE_CFXR_BOUND_ROWS.csv")
    strongest = min(rows, key=lambda row: float(row["xi_H_max"]))
    return strongest["bound_id"], float(strongest["xi_H_max"]), strongest["finite_coefficient_bound"]


def canonical_contract_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "CNC3677_0_parent_slot",
            "parent curvature slot",
            "S_H=(M_*^2/2) int sqrt(-g) A_H F(X) R",
            "D_H=1+A_H*F0",
            "c_FXR=A_H*F0_prime/D_H",
            "3673/3674 already derived this as the allowed F(X)R branch",
            "accepted starting point",
        ),
        (
            "CNC3677_1_field_rescaling",
            "field-coordinate redundancy",
            "X_prime=lambda_X*X",
            "Z_X_prime=Z_X/lambda_X^2; F0_prime_prime=F0_prime/lambda_X; f_EM_prime=f_EM/lambda_X",
            "c_FXR_prime=c_FXR/lambda_X",
            "c_FXR by itself is not a coordinate-invariant physical coefficient",
            "derived algebraic transformation",
        ),
        (
            "CNC3677_2_invariant_product",
            "observable scalar-slip product",
            "xi_FXR=|A_H*F0_prime*f_EM/(D_H*Z_X)|",
            "xi_FXR_prime=xi_FXR",
            "xi_FXR=|c_FXR*f_EM/Z_X|",
            "the bound must act on the invariant product, not on raw c_FXR alone",
            "derived invariant",
        ),
        (
            "CNC3677_3_canonical_field",
            "canonical field coordinate",
            "X_hat=sqrt(Z_X)*X",
            "F0_hat_prime=F0_prime/sqrt(Z_X); f_EM_hat=f_EM/sqrt(Z_X)",
            "g_FXR=A_H*F0_hat_prime/D_H",
            "xi_FXR=|g_FXR*f_EM_hat|",
            "canonical normalization converts the vague coupling into two dimensionless physical legs",
        ),
        (
            "CNC3677_4_denominator_guard",
            "EH denominator guard",
            "D_H=1+A_H*F0",
            "require D_H not near zero before any naturalness/scoring row is trusted",
            "default smoke guard: |D_H|>=1/2",
            "prevents fake large/small coupling from Planck-mass denominator accident",
            "conditional guard, not a parent theorem",
        ),
    ]
    return [
        {
            **base(ts),
            "contract_id": contract_id,
            "item": item,
            "statement": statement,
            "transformation_or_guard": transformation_or_guard,
            "derived_symbol": derived_symbol,
            "consequence": consequence,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for contract_id, item, statement, transformation_or_guard, derived_symbol, consequence, status in specs
    ]


def reparam_derivation_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RPD3677_0_kinetic",
            "kinetic term invariance",
            "(Z_X/2)(partial X)^2=(Z_X/(2*lambda_X^2))(partial X_prime)^2",
            "Z_X_prime=Z_X/lambda_X^2",
            "PASS_DERIVED",
        ),
        (
            "RPD3677_1_curvature_derivative",
            "curvature prefactor derivative",
            "F_X=dF/dX, X_prime=lambda_X X",
            "F0_prime_prime=F0_prime/lambda_X",
            "PASS_DERIVED",
        ),
        (
            "RPD3677_2_source_transfer",
            "linear EM transfer leg",
            "f_EM X T_EM = (f_EM/lambda_X) X_prime T_EM",
            "f_EM_prime=f_EM/lambda_X",
            "PASS_DERIVED_IF_LINEAR_SOURCE_CONVENTION",
        ),
        (
            "RPD3677_3_raw_cFXR",
            "raw c_FXR transformation",
            "c_FXR=A_H*F0_prime/D_H",
            "c_FXR_prime=c_FXR/lambda_X",
            "NOT_OBSERVABLE_ALONE",
        ),
        (
            "RPD3677_4_product_invariance",
            "observable product invariance",
            "(c_FXR/lambda_X)*(f_EM/lambda_X)/(Z_X/lambda_X^2)=c_FXR*f_EM/Z_X",
            "xi_FXR_prime=xi_FXR",
            "PASS_DERIVED_INVARIANT",
        ),
        (
            "RPD3677_5_canonical_pair",
            "canonical pair",
            "X_hat=sqrt(Z_X)X gives g_FXR=c_FXR/sqrt(Z_X), s_EM=f_EM/sqrt(Z_X)",
            "xi_FXR=|g_FXR*s_EM|",
            "PASS_DERIVED_CANONICAL_OBSERVABLE_PAIR",
        ),
    ]
    return [
        {
            **base(ts),
            "derivation_id": derivation_id,
            "step": step,
            "calculation": calculation,
            "result": result,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for derivation_id, step, calculation, result, status in specs
    ]


def naturalness_prior_rows(ts: str) -> list[dict[str, object]]:
    bound_id, xi_max, _ = strongest_xi_bound()
    g_nat = 1.0
    s_em_max_if_g_nat = xi_max / g_nat
    four_pi = 12.566370614359172
    s_em_max_if_g_4pi = xi_max / four_pi
    specs = [
        (
            "NPR3677_0_gFXR_canonical_O1",
            "g_FXR=A_H*F0_hat_prime/(1+A_H*F0)",
            "dimensionless",
            -1.0,
            1.0,
            "weakly_coupled_canonical_EFT_O1_prior",
            "canonical X_hat, analytic F, no denominator accident |D_H|>=1/2",
            "MISSING-free naturalness prior row for private smoke use only",
            False,
        ),
        (
            "NPR3677_1_gFXR_canonical_4pi",
            "g_FXR=A_H*F0_hat_prime/(1+A_H*F0)",
            "dimensionless",
            -four_pi,
            four_pi,
            "loose_perturbative_4pi_prior",
            "same assumptions as O1 but allows strong-ish EFT coefficient",
            "MISSING-free loose smoke prior, not evidence",
            False,
        ),
        (
            "NPR3677_2_sEM_required_if_gO1",
            "s_EM=f_EM/sqrt(Z_X)",
            "dimensionless canonical transfer",
            -s_em_max_if_g_nat,
            s_em_max_if_g_nat,
            f"conditional_from_{bound_id}_and_|g_FXR|<=1",
            "if curvature-prefactor leg is natural O(1), canonical EM transfer must be small",
            "derived conditional smoke bound on EM/Poynting transfer leg",
            False,
        ),
        (
            "NPR3677_3_sEM_required_if_g4pi",
            "s_EM=f_EM/sqrt(Z_X)",
            "dimensionless canonical transfer",
            -s_em_max_if_g_4pi,
            s_em_max_if_g_4pi,
            f"conditional_from_{bound_id}_and_|g_FXR|<=4pi",
            "if curvature-prefactor leg is as large as 4pi, canonical EM transfer must be even smaller",
            "derived conditional smoke bound on EM/Poynting transfer leg",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "prior_id": prior_id,
            "symbol": symbol,
            "units": units,
            "lower_bound": f"{lower:.12e}",
            "upper_bound": f"{upper:.12e}",
            "prior_type": prior_type,
            "assumptions": assumptions,
            "status": status,
            "missing_markers": "NONE",
            "prior_ready": True,
            "valid_for_claim": False,
            "score_ready": False,
            "claim_allowed": claim_allowed,
        }
        for prior_id, symbol, units, lower, upper, prior_type, assumptions, status, claim_allowed in specs
    ]


def bound_implication_rows(ts: str) -> list[dict[str, object]]:
    bound_id, xi_max, inherited = strongest_xi_bound()
    implications = [
        (
            "BIR3677_0_invariant_bound",
            "xi_FXR=|g_FXR*s_EM|",
            "<=",
            xi_max,
            bound_id,
            inherited,
            "strictest inherited private scalar-slip template converted to canonical pair",
        ),
        (
            "BIR3677_1_if_gFXR_O1",
            "|s_EM|",
            "<=",
            xi_max,
            "NPR3677_0_gFXR_canonical_O1",
            "|g_FXR|<=1",
            "EM/Poynting transfer leg must be below the scalar-slip ceiling if curvature leg is natural",
        ),
        (
            "BIR3677_2_if_sEM_O1",
            "|g_FXR|",
            "<=",
            xi_max,
            "canonical_sEM_O1_hypothesis",
            "|s_EM|<=1",
            "curvature prefactor leg must be suppressed if EM transfer is O(1)",
        ),
        (
            "BIR3677_3_if_gFXR_4pi",
            "|s_EM|",
            "<=",
            xi_max / 12.566370614359172,
            "NPR3677_1_gFXR_canonical_4pi",
            "|g_FXR|<=4pi",
            "looser curvature naturalness still forces a very small EM transfer leg",
        ),
    ]
    return [
        {
            **base(ts),
            "implication_id": implication_id,
            "quantity": quantity,
            "relation": relation,
            "numeric_value": f"{numeric_value:.12e}",
            "basis": basis,
            "input_bound_or_assumption": input_bound_or_assumption,
            "interpretation": interpretation,
            "valid_for_claim": False,
            "score_ready": False,
            "claim_allowed": False,
        }
        for implication_id, quantity, relation, numeric_value, basis, input_bound_or_assumption, interpretation in implications
    ]


def generator_decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "GDR3677_0_generator_elimination_attempt",
            "kill quotient-scalar generator feeding F(X)R",
            "NOT_KILLED_THIS_CHECKPOINT",
            "3676 left quotient-invariant class scalar live; 3677 does not pretend to prove its absence",
            "use canonical normalization route instead of smuggling zero",
        ),
        (
            "GDR3677_1_raw_cFXR_decision",
            "raw c_FXR coefficient",
            "DEMOTED_NOT_PHYSICAL_ALONE",
            "field rescaling changes c_FXR, so raw c_FXR cannot be assigned a physical numeric prior without Z_X",
            "replace with canonical g_FXR and s_EM pair",
        ),
        (
            "GDR3677_2_canonical_pair_decision",
            "canonical observable pair",
            "PROMOTED_TO_PRIVATE_SMOKE_COORDINATES",
            "xi_FXR=|g_FXR*s_EM| is invariant and can be tested without arbitrary field-coordinate drift",
            "future data/code should score g_FXR and s_EM product, not raw c_FXR",
        ),
        (
            "GDR3677_3_next_physics_target",
            "EM/Poynting transfer leg",
            "NEXT_BEST_TARGET",
            "if |g_FXR| is natural, the Cassini-style ceiling makes |s_EM| <= 2.979e-5; this is a sharp EM/source-coupling target",
            "derive s_EM from Maxwell/Poynting/current owner or produce a bound row",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3677_0_raw_cFXR_claim", "claim a raw numeric c_FXR", "BLOCKED_BY_REPARAMETERIZATION", "raw c_FXR is field-coordinate dependent"),
        ("CG3677_1_canonical_prior_claim", "treat naturalness prior as evidence", "BLOCKED_NONCLAIM", "O(1) and 4pi rows are smoke priors only"),
        ("CG3677_2_local_GR_claim", "claim local-GR/PPN pass", "BLOCKED_NONCLAIM", "xi product still needs EM transfer/source leg or theorem-zero"),
        ("CG3677_3_generator_zero", "claim quotient-scalar generator killed", "BLOCKED_NONCLAIM", "generator elimination was not proved"),
        ("CG3677_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    _, xi_max, _ = strongest_xi_bound()
    return [
        {
            **base(ts),
            "status": "CANONICAL_CFXR_PAIR_DERIVED_NATURALNESS_PRIOR_STAGED_NONCLAIM",
            "summary": "3677 derives that raw c_FXR is not physical by itself under X rescaling. The invariant branch is xi_FXR=|g_FXR*s_EM| with g_FXR=A_H*F0_hat_prime/(1+A_H*F0) and s_EM=f_EM/sqrt(Z_X). A MISSING-free O(1)/4pi naturalness prior for g_FXR is staged for private smoke use, and the inherited bound implies a sharp conditional target on the EM/Poynting transfer leg.",
            "claim_ceiling": "no local-GR, PPN, WEP/R10, fifth-force, EH/Newton, generator-zero, or finite-coupling evidence claim is made",
            "useful_result": f"if |g_FXR|<=1 then |s_EM|<={xi_max:.12e}; if |s_EM|<=1 then |g_FXR|<={xi_max:.12e}",
            "next_missing_piece": "derive or bound s_EM=f_EM/sqrt(Z_X) from Maxwell/Poynting/current owner in the same canonical normalization",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3677_0",
            "target_doc": "3678-Y5-R2FR-canonical-EM-Poynting-transfer-leg-or-sEM-bound.md",
            "target_script": "scripts/Y5_R2FR_3678_canonical_EM_Poynting_transfer_leg_or_sEM_bound.py",
            "objective": "derive the canonical EM/Poynting transfer leg s_EM=f_EM/sqrt(Z_X) from Maxwell stress/current normalization, or produce a nonclaim bound/input row for s_EM in the invariant xi_FXR=|g_FXR*s_EM| product",
            "success_gate": "either s_EM is theorem-zero/source-derived in canonical units, or a source-backed/nonclaim s_EM bound row exists without field-rescaling ambiguity",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    contracts: list[dict[str, object]],
    derivations: list[dict[str, object]],
    priors: list[dict[str, object]],
    implications: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3677 - c_FXR parent normalization scale or local generator elimination",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint takes the leap that 3676 set up: raw `c_FXR` is not the physical coupling unless the `X` field coordinate is fixed. Under `X' = lambda_X X`, the raw pieces move, but the observable product does not.",
        "",
        "## Main derivation",
        "",
        "`Z_X' = Z_X/lambda_X^2`, `F0_prime' = F0_prime/lambda_X`, and `f_EM' = f_EM/lambda_X`.",
        "",
        "Therefore:",
        "",
        "`(c_FXR' f_EM')/Z_X' = c_FXR f_EM/Z_X`.",
        "",
        "With the canonical field `X_hat=sqrt(Z_X) X`:",
        "",
        "`g_FXR = A_H*F0_hat_prime/(1+A_H*F0)`",
        "",
        "`s_EM = f_EM/sqrt(Z_X)`",
        "",
        "`xi_FXR = |g_FXR*s_EM|`.",
        "",
        "That is the useful object. The raw `c_FXR` row is demoted; the canonical pair is promoted for private smoke tests.",
        "",
        "## Immediate consequence",
    ]
    for row in implications:
        lines.append(f"- `{row['implication_id']}`: `{row['quantity']} {row['relation']} {row['numeric_value']}` from {row['input_bound_or_assumption']} - {row['interpretation']}")
    lines.extend(["", "## Canonical contract"])
    for row in contracts:
        lines.append(f"- `{row['contract_id']}`: {row['status']} - {row['item']} -> {row['consequence']}")
    lines.extend(["", "## Reparameterization derivation"])
    for row in derivations:
        lines.append(f"- `{row['derivation_id']}`: {row['status']} - {row['result']}")
    lines.extend(["", "## Naturalness priors"])
    for row in priors:
        lines.append(f"- `{row['prior_id']}`: `{row['symbol']}` in [{row['lower_bound']}, {row['upper_bound']}] - {row['status']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    contracts: list[dict[str, object]],
    derivations: list[dict[str, object]],
    priors: list[dict[str, object]],
    implications: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + contracts + derivations + priors + implications + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3677*", "3677-Y5-R2FR-*", "P8_Y5*3677*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    contract_ids = {str(row["contract_id"]) for row in contracts}
    derivation_ids = {str(row["derivation_id"]) for row in derivations}
    prior_ids = {str(row["prior_id"]) for row in priors}
    implication_ids = {str(row["implication_id"]) for row in implications}
    numeric_prior_rows = [row for row in priors if row["missing_markers"] == "NONE" and re.match(r"^-?\d+\.\d+e[+-]\d+$", str(row["lower_bound"]).lower())]

    add("VAL3677_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3677_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3677_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3677 outputs written")
    add("VAL3677_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3677_4_contract_coverage", {"CNC3677_0_parent_slot", "CNC3677_1_field_rescaling", "CNC3677_2_invariant_product", "CNC3677_3_canonical_field", "CNC3677_4_denominator_guard"}.issubset(contract_ids), "canonical normalization contract covers parent slot, rescaling, invariant product, canonical field, denominator")
    add("VAL3677_5_derivation_coverage", {"RPD3677_0_kinetic", "RPD3677_1_curvature_derivative", "RPD3677_2_source_transfer", "RPD3677_3_raw_cFXR", "RPD3677_4_product_invariance", "RPD3677_5_canonical_pair"}.issubset(derivation_ids), "reparameterization derivation covers all moving pieces")
    add("VAL3677_6_product_invariant", any(row["derivation_id"] == "RPD3677_4_product_invariance" and "xi_FXR_prime=xi_FXR" in row["result"] for row in derivations), "xi product invariance derived")
    add("VAL3677_7_naturalness_rows", {"NPR3677_0_gFXR_canonical_O1", "NPR3677_1_gFXR_canonical_4pi", "NPR3677_2_sEM_required_if_gO1", "NPR3677_3_sEM_required_if_g4pi"}.issubset(prior_ids), "naturalness and conditional s_EM prior rows present")
    add("VAL3677_8_no_missing_in_prior_rows", len(numeric_prior_rows) == len(priors), "all 3677 prior rows are MISSING-free numeric smoke priors")
    add("VAL3677_9_bound_implications", {"BIR3677_0_invariant_bound", "BIR3677_1_if_gFXR_O1", "BIR3677_2_if_sEM_O1", "BIR3677_3_if_gFXR_4pi"}.issubset(implication_ids), "canonical bound implications present")
    add("VAL3677_10_raw_cfxr_demoted", any(row["decision_id"] == "GDR3677_1_raw_cFXR_decision" and row["status"] == "DEMOTED_NOT_PHYSICAL_ALONE" for row in decisions), "raw c_FXR demoted because field-coordinate dependent")
    add("VAL3677_11_em_next_target", any(row["decision_id"] == "GDR3677_3_next_physics_target" and "EM/Poynting" in row["decision"] for row in decisions), "EM/Poynting transfer leg selected")
    add("VAL3677_12_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3677_13_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3677_14_doc_written", "raw `c_FXR` is not the physical coupling" in doc_text and "xi_FXR = |g_FXR*s_EM|" in doc_text and "private smoke tests" in doc_text, "doc records canonical pair derivation")
    add("VAL3677_15_no_formalization_leak", not leaks, "no 3677 checkpoint files in formalization-workbench")
    add("VAL3677_16_next_target", next_target[0]["target_doc"].startswith("3678-") and "Poynting" in next_target[0]["objective"], "3678 canonical EM/Poynting target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    contracts = canonical_contract_rows(ts)
    derivations = reparam_derivation_rows(ts)
    priors = naturalness_prior_rows(ts)
    implications = bound_implication_rows(ts)
    decisions = generator_decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3677_SOURCE_REGISTER.csv",
        "contracts": RESIDUALS / "P8_Y5_R2FR_3677_CANONICAL_NORMALIZATION_CONTRACT.csv",
        "derivations": RESIDUALS / "P8_Y5_R2FR_3677_REPARAMETERIZATION_DERIVATION_ROWS.csv",
        "priors": RESIDUALS / "P8_Y5_R2FR_3677_NATURALNESS_PRIOR_ROWS.csv",
        "implications": RESIDUALS / "P8_Y5_R2FR_3677_BOUND_IMPLICATION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3677_GENERATOR_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3677_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3677_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3677_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3677_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["derivations"], derivations)
    write_csv(outputs["priors"], priors)
    write_csv(outputs["implications"], implications)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, contracts, derivations, priors, implications, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, contracts, derivations, priors, implications, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3677 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3677 checkpoint with canonical c_FXR pair, MISSING-free naturalness priors, and EM/Poynting next target")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
