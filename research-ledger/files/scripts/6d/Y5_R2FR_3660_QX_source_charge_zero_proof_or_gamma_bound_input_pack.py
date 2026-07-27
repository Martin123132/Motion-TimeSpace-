from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3660"
BRANCH_ID = "MTS_R2FR_Y5_QX_SOURCE_CHARGE_ZERO_PROOF_OR_GAMMA_BOUND_INPUT_PACK_3660"
DOC = ROOT / "3660-Y5-R2FR-QX-source-charge-zero-proof-or-gamma-bound-input-pack.md"


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
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3659", RESIDUALS / "P8_Y5_R2FR_3659_NEXT_TARGET.csv", "Q_X", "3659 selected QX zero/bound target"),
        ("constant_theorem_3659", RESIDUALS / "P8_Y5_R2FR_3659_CONSTANT_FIELD_THEOREM_ATTEMPT.csv", "Q_X=0", "3659 constant-field theorem"),
        ("profile_inputs_3659", RESIDUALS / "P8_Y5_R2FR_3659_PROFILE_INPUT_ACQUISITION_ROWS.csv", "PI3659_0_QX_source", "3659 profile input register"),
        ("source_gate_3659", RESIDUALS / "P8_Y5_R2FR_3659_SOURCE_CHARGE_GATE_ROWS.csv", "SCG3659_0_matter_descent_zero", "3659 source-charge gate"),
        ("validation_3659", RESIDUALS / "P8_Y5_BRR545_3659_VALIDATION.csv", "VAL3659_6_constant_field_theorem", "3659 validation"),
        ("current_3650", RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv", "WARD_CONSERVATION_NOT_ENOUGH", "source-current zero route and countermodel"),
        ("material_theorem_3651", RESIDUALS / "P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv", "Q_A^X = partial ln M_A^eff/partial Xhat", "source charge law"),
        ("material_rows_3651", RESIDUALS / "P8_Y5_R2FR_3651_MATERIAL_SENSITIVITY_ROWS.csv", "MSR3651_4_Qsource", "Q_source_X row"),
        ("gm_rows_3652", RESIDUALS / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv", "GMC3652_2_Qsource", "weak-field Q_source_X calibration"),
        ("local_bounds_R3", LOCAL_BOUNDS / "local_bound_claims.csv", "R3_gamma", "Cassini gamma bound anchor"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def qx_zero_proof_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "proof_id": "QXZ3660_0_source_definition",
            "object": "integrated local source charge",
            "statement": "The local exterior amplitude is controlled by Q_X, with Q_X obtained by integrating the matter/source current J_X over the compact local source.",
            "formula": "Q_X = int_source d^3x J_X = sum_A int_source d^3x rho_A Q_A^X",
            "proof_status": "SOURCE_CHARGE_DEFINITION_DERIVED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "QXZ3660_1_material_sensitivity_link",
            "object": "material/source sensitivity",
            "statement": "3651 gives Q_A^X as the logarithmic sensitivity of effective matter/source mass to the local extra field.",
            "formula": "Q_A^X = partial ln M_A^eff/partial Xhat",
            "proof_status": "QX_REDUCED_TO_MATERIAL_SENSITIVITY_MATRIX",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "QXZ3660_2_zero_condition",
            "object": "Q_X zero theorem",
            "statement": "If every local source constituent has Q_A^X=0, the source measure has no X-dependent normalization, and boundary hair is absent, then Q_X=0.",
            "formula": "forall A: Q_A^X=0 and b_J_source=0 and B_X=0 => Q_X=0",
            "proof_status": "CONDITIONAL_QX_ZERO_THEOREM_DERIVED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "QXZ3660_3_countermodel",
            "object": "legal nonzero Q_X branch",
            "statement": "A material marker, current rescaling, EM binding sensitivity, or source-measure factor can generate nonzero Q_A^X unless the parent matter functor forbids it.",
            "formula": "Q_A^X = beta_source_alpha,A*b_alpha + B_A^EM*f_EM + B_A^m*b_m + B_A^nuc*b_nuc + b_J_source,A + b_material_marker,A + b_boundary,A",
            "proof_status": "NONZERO_SOURCE_CHARGE_COUNTERMODEL_LIVE",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "proof_id": "QXZ3660_4_current_verdict",
            "object": "current MTS Q_X zero status",
            "statement": "The zero theorem exists, but parent representation/source-measure/material/boundary clauses remain unsigned in the current corpus.",
            "formula": "Q_X=0 not accepted; build gamma-bound input pack for Q_X/Z_X branch",
            "proof_status": "PARENT_QX_ZERO_UNSIGNED_BOUND_PACK_REQUIRED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
    ]


def qx_zero_clause_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("QZA3660_0_representation_descent", "matter representation labels fixed or quotient-owned", "3651 MSS3651_0", "UNSIGNED"),
        ("QZA3660_1_source_measure_descent", "particle/source measure and current normalization descend through q", "3650 SCT3650_2", "UNSIGNED"),
        ("QZA3660_2_no_material_marker", "no independent material marker chi_A(X_N)", "3651 MSS3651_5", "UNSIGNED"),
        ("QZA3660_3_no_binding_leak", "mass/binding pieces have no live X sensitivity or are sourced and bounded", "3651 MSS3651_1-2", "UNSIGNED"),
        ("QZA3660_4_source_hamiltonian_owner", "weak-field source Hamiltonian fixes active/inertial source map", "3652 GMC3652_2", "UNSIGNED"),
        ("QZA3660_5_boundary_no_hair", "boundary hair B_X does not inject exterior profile amplitude", "3659 PI3659_6", "UNSIGNED"),
        ("QZA3660_6_total", "all Q_X zero clauses hold together", "3660 QXZ3660_2", "NOT_SIGNED"),
    ]
    return [
        {
            **base(ts),
            "clause_id": clause_id,
            "clause": clause,
            "source_anchor": source_anchor,
            "current_status": status,
            "accepted_as_zero": False,
            "next_action": "derive parent clause or retain bound input",
            "claim_allowed": False,
        }
        for clause_id, clause, source_anchor, status in specs
    ]


def gamma_bound_input_pack_rows(ts: str) -> list[dict[str, object]]:
    gamma = next(row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv") if row["row_id"] == "R3_gamma")
    upper = parse_float(gamma["upper_bound"])
    specs = [
        ("GBI3660_0_QX", "Q_X", "integrated local source charge", "Q_X=sum_A int rho_A Q_A^X d^3x", "dimensionless source charge", "MISSING_PARENT_ZERO_OR_SOURCE_COMPOSITION"),
        ("GBI3660_1_QA", "Q_A_X", "constituent/source sensitivity vector", "Q_A^X=partial ln M_A^eff/partial Xhat", "dimensionless", "MISSING_COMPONENT_SENSITIVITIES"),
        ("GBI3660_2_ZX", "Z_X", "quadratic kinetic normalization", "quadratic action coefficient of X", "action-normalization dependent", "MISSING_PARENT_QUADRATIC_ACTION"),
        ("GBI3660_3_lambdaX", "lambda_X", "local range/mass scale", "lambda_X=1/M_X", "length", "MISSING_PARENT_HESSIAN_OR_RANGE"),
        ("GBI3660_4_AX", "A_X", "exterior profile amplitude", "A_X ~= Q_X/(4*pi*Z_X)", "field amplitude times length", "MISSING_QX_ZX_INPUTS"),
        ("GBI3660_5_kH", "k_H", "Hessian-STF gamma projection coefficient", "C_H=|k_H|*|A_X|*exp(-r/lambda_X)*(3/r^3+3/(lambda_X*r^2)+1/(lambda_X^2*r))/|Phi_N|", "projection units", "MISSING_WEAK_FIELD_PROJECTION"),
        ("GBI3660_6_kG", "k_G", "gradient-square-STF gamma projection coefficient", "C_G=|k_G|*A_X^2*exp(-2*r/lambda_X)*(1/r^2+1/(lambda_X*r))^2/|Phi_N|", "projection units", "MISSING_WEAK_FIELD_PROJECTION"),
        ("GBI3660_7_gamma_kernel", "K_gamma_profile", "Cassini/local gamma geometry kernel", "evaluate r, Phi_N(r), impact geometry, and transfer kernel for gamma test", "dimensionless kernel", "MISSING_GAMMA_GEOMETRY_KERNEL"),
        ("GBI3660_8_boundary_readout_source", "C_other_gamma", "non-profile gamma residual pieces", "|C_boundary|+|C_readout|+|C_source|+|C_nonEH_other|", "dimensionless", "MISSING_COMPONENT_BOUNDS"),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "units": units,
            "cassini_bound_row": "R3_gamma",
            "cassini_upper_bound": upper,
            "cassini_reference": gamma["reference_path_or_url"],
            "required_for": "delta_gamma_MTS profile prediction or Q_X zero proof",
            "current_status": status,
            "score_ready": False,
            "placeholder_refused_as_claim": True,
            "claim_allowed": False,
        }
        for input_id, symbol, definition, formula, units, status in specs
    ]


def gamma_bound_formula_rows(ts: str) -> list[dict[str, object]]:
    gamma = next(row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv") if row["row_id"] == "R3_gamma")
    upper = parse_float(gamma["upper_bound"])
    return [
        {
            **base(ts),
            "formula_id": "GBF3660_0_amplitude",
            "object": "profile amplitude",
            "formula": "A_X ~= Q_X/(4*pi*Z_X)",
            "bound_use": "substitute into C_gradient_TF_gamma",
            "required_inputs": "Q_X;Z_X",
            "numeric_upper_bound": upper,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "formula_id": "GBF3660_1_gamma_profile_envelope",
            "object": "gamma profile envelope",
            "formula": "|k_H|*|Q_X|/(4*pi*|Z_X|)*exp(-r/lambda_X)*(3/r^3+3/(lambda_X*r^2)+1/(lambda_X^2*r))/|Phi_N(r)| + |k_G|*(Q_X/(4*pi*Z_X))^2*exp(-2*r/lambda_X)*(1/r^2+1/(lambda_X*r))^2/|Phi_N(r)| + |C_other_gamma| <= 2.3e-05",
            "bound_use": "Cassini gamma nonclaim score formula once inputs are real",
            "required_inputs": "Q_X;Z_X;lambda_X;k_H;k_G;r;Phi_N;C_other_gamma",
            "numeric_upper_bound": upper,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "formula_id": "GBF3660_2_zero_shortcut",
            "object": "source-charge zero shortcut",
            "formula": "Q_X=0 and B_X=0 => A_X=0 => profile terms vanish before Cassini scoring",
            "bound_use": "theorem-zero route if parent signs source-charge descent",
            "required_inputs": "parent Q_X=0 theorem; boundary no-hair theorem",
            "numeric_upper_bound": upper,
            "claim_allowed": False,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "decision_id": "DEC3660_0_zero_route",
            "route": "Q_X theorem-zero",
            "status": "DERIVED_CONDITIONALLY_UNSIGNED",
            "meaning": "if parent matter/source descent signs every Q_A^X zero clause, local gamma profile amplitude vanishes",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "decision_id": "DEC3660_1_bound_route",
            "route": "Q_X/Z_X gamma-bound input pack",
            "status": "INPUT_PACK_READY_PLACEHOLDERS_REFUSED",
            "meaning": "if Q_X is nonzero or unsigned, next work must source the profile/operator inputs before any score",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3660_0_QX_definition", "Q_X source charge definition derived", "PASSED_DERIVATION", "Q_X=sum_A int rho_A Q_A^X d^3x"),
        ("CG3660_1_QX_zero", "Q_X=0 theorem derived conditionally", "PASSED_CONDITIONAL_THEOREM", "all constituent sensitivities plus source measure/boundary hair must vanish"),
        ("CG3660_2_countermodel", "nonzero Q_X branch remains legal", "ACTIVE_GUARD", "material/current/binding/source labels can leak unless parent forbids them"),
        ("CG3660_3_bound_pack", "gamma-bound input pack staged", "PASSED_INPUT_PACK", "Q_X,Z_X,lambda_X,k_H,k_G and kernel inputs registered"),
        ("CG3660_4_no_claim", "no local-GR/gamma pass claimed", "ACTIVE_GUARD", "no Q_X zero signature or numeric profile inputs yet"),
        ("CG3660_5_next", "next step decomposes Q_X or sources the profile inputs", "QX_COMPONENT_BASIS_NEXT", "coupling branch is now the narrow target"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "QX_ZERO_THEOREM_CONDITIONAL_GAMMA_BOUND_INPUT_PACK_READY_NONCLAIM",
            "summary": "3660 derives Q_X=sum_A int rho_A Q_A^X d^3x and the conditional Q_X=0 theorem, refuses the unsigned zero, and stages the gamma-bound input pack for the nonzero source-charge branch.",
            "claim_ceiling": "no MTS gamma prediction, local-GR pass, PPN pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed",
            "useful_result": "The coupling problem is now executable: either prove every Q_A^X source sensitivity vanishes, or source Q_X,Z_X,lambda_X,k_H,k_G plus gamma geometry and score the Cassini envelope.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3660_0",
            "target_doc": "3661-Y5-R2FR-QX-component-basis-decomposition-or-shared-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_3661_QX_component_basis_decomposition_or_shared_bound_runner.py",
            "objective": "decompose Q_X into beta_source_alpha, EM binding, mass/nuclear, source-measure, material-marker, and boundary components; attempt theorem-zero per component, otherwise prepare shared WEP/R10/gamma bound rows",
            "success_gate": "each Q_X component is either parent-zero, numeric/source-backed, or explicitly retained as nonclaim with its shared empirical arena and no-cancellation status",
        }
    ]


def write_doc(sources, proof, audit, inputs, formulas, decisions, gates, status_rows_, next_target) -> None:
    lines = [
        "# 3660 - QX source-charge zero proof or gamma bound input pack",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "`Q_X` is no longer just a missing coupling label. It is the integrated local source charge",
        "",
        "`Q_X = int_source d^3x J_X = sum_A int_source d^3x rho_A Q_A^X`,",
        "",
        "with `Q_A^X = partial ln M_A^eff/partial Xhat` from the material/source sensitivity law.",
        "",
        "Therefore the clean local-GR route is now exact but conditional: if every ordinary-matter constituent has `Q_A^X=0`, the source measure has no X-dependent normalization, and boundary hair is absent, then `Q_X=0`, `A_X=0`, and the local gamma profile vanishes.",
        "",
        "Current MTS does not yet sign those parent clauses, so 3660 refuses the zero claim and writes the nonclaim gamma-bound input pack. The nonzero branch must score",
        "",
        "`A_X ~= Q_X/(4*pi*Z_X)`",
        "",
        "inside the Cassini envelope for `delta_gamma_MTS`.",
        "",
        "## QX zero proof attempt",
    ]
    for row in proof:
        lines.append(f"- `{row['proof_id']}`: {row['proof_status']} - `{row['formula']}`")
    lines.extend(["", "## QX zero-clause audit"])
    for row in audit:
        lines.append(f"- `{row['clause_id']}`: {row['current_status']} - {row['clause']}")
    lines.extend(["", "## Gamma-bound input pack"])
    for row in inputs:
        lines.append(f"- `{row['input_id']}`: `{row['symbol']}` - {row['current_status']}")
    lines.extend(["", "## Bound formulas"])
    for row in formulas:
        lines.append(f"- `{row['formula_id']}`: `{row['object']}` - {row['bound_use']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['meaning']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(ts, output_paths, sources, proof, audit, inputs, formulas, decisions, gates, status_rows_, next_target) -> list[dict[str, object]]:
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

    add("VAL3660_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3660_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3660_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3660 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3660_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3660_4_QX_definition", any("sum_A int_source" in row["formula"] for row in proof), "Q_X integrated source definition recorded")
    add("VAL3660_5_QX_zero_theorem", any(row["proof_status"] == "CONDITIONAL_QX_ZERO_THEOREM_DERIVED" for row in proof), "conditional Q_X zero theorem derived")
    add("VAL3660_6_countermodel_live", any(row["proof_status"] == "NONZERO_SOURCE_CHARGE_COUNTERMODEL_LIVE" for row in proof), "nonzero source-charge countermodel retained")
    add("VAL3660_7_no_zero_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in proof + audit), "no unsigned Q_X zero accepted")
    required = {"Q_X", "Q_A_X", "Z_X", "lambda_X", "A_X", "k_H", "k_G", "K_gamma_profile", "C_other_gamma"}
    add("VAL3660_8_input_pack_complete", required.issubset({row["symbol"] for row in inputs}), "gamma bound input pack contains required symbols")
    add("VAL3660_9_placeholders_refused", all(str(row["placeholder_refused_as_claim"]).lower() == "true" and str(row["score_ready"]).lower() == "false" for row in inputs), "all input placeholders refused as claims")
    add("VAL3660_10_gamma_bound_formula", any("Q_X/(4*pi*Z_X)" in row["formula"] and parse_float(row["numeric_upper_bound"]) == 2.3e-05 for row in formulas), "gamma bound formula carries Q_X/Z_X and Cassini limit")
    add("VAL3660_11_decisions_present", {"DEC3660_0_zero_route", "DEC3660_1_bound_route"}.issubset({row["decision_id"] for row in decisions}), "zero and bound decisions present")
    add("VAL3660_12_claim_gates_present", {"CG3660_0_QX_definition", "CG3660_1_QX_zero", "CG3660_2_countermodel", "CG3660_3_bound_pack", "CG3660_4_no_claim", "CG3660_5_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + proof + audit + inputs + formulas + decisions + gates + status_rows_ + next_target
    add("VAL3660_13_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3660_14_doc_written", "Q_X = int_source" in doc_text and "Q_A^X=0" in doc_text and "A_X ~= Q_X/(4*pi*Z_X)" in doc_text, "doc records Q_X zero and bound routes")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3660*", "3660-Y5-R2FR-*", "Y5_R2FR_3660_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3660_15_no_formalization_leak", not leaks, "no 3660 checkpoint files in formalization-workbench")
    add("VAL3660_16_next_target", next_target[0]["target_doc"].startswith("3661-") and "component-basis" in next_target[0]["target_doc"], "3661 QX component-basis target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    proof = qx_zero_proof_rows(ts)
    audit = qx_zero_clause_audit_rows(ts)
    inputs = gamma_bound_input_pack_rows(ts)
    formulas = gamma_bound_formula_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3660_SOURCE_REGISTER.csv",
        "proof": RESIDUALS / "P8_Y5_R2FR_3660_QX_ZERO_PROOF_ATTEMPT.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3660_QX_ZERO_CLAUSE_AUDIT.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3660_GAMMA_BOUND_INPUT_PACK.csv",
        "formulas": RESIDUALS / "P8_Y5_R2FR_3660_GAMMA_BOUND_FORMULAS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3660_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3660_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3660_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3660_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3660_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["proof"], proof)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["inputs"], inputs)
    write_csv(outputs["formulas"], formulas)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, proof, audit, inputs, formulas, decisions, gates, status_rows_, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, proof, audit, inputs, formulas, decisions, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3660 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3660 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
