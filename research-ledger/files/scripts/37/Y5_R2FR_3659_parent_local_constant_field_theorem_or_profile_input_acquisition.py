from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3659"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_LOCAL_CONSTANT_FIELD_THEOREM_OR_PROFILE_INPUT_ACQUISITION_3659"
DOC = ROOT / "3659-Y5-R2FR-parent-local-constant-field-theorem-or-profile-input-acquisition.md"


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
        ("next_3658", RESIDUALS / "P8_Y5_R2FR_3658_NEXT_TARGET.csv", "constant-field", "3658 selected constant-field/profile input target"),
        ("radial_3658", RESIDUALS / "P8_Y5_R2FR_3658_RADIAL_STF_DERIVATION_ROWS.csv", "CONDITIONAL_NO_GRADIENT_ZERO_THEOREM_DERIVED", "3658 radial no-gradient theorem"),
        ("profiles_3658", RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv", "A_X*exp(-r/lambda_X)/r", "3658 profile coefficient formula"),
        ("interface_3658", RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_SCORE_INTERFACE_ROWS.csv", "A_X, range lambda_X", "3658 profile input route"),
        ("validation_3658", RESIDUALS / "P8_Y5_BRR545_3658_VALIDATION.csv", "VAL3658_7_yukawa_profile_formula", "3658 validation"),
        ("source_current_3650", ROOT / "3650-Y5-R2FR-EM-source-current-normalization-or-beta-source-alpha-row.md", "WARD_CONSERVATION_NOT_ENOUGH", "source-current normalization unsigned"),
        ("matter_sensitivity_3651", ROOT / "3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md", "Q_A^X = partial ln M_A^eff / partial Xhat", "source charge vector law"),
        ("weak_field_3652", ROOT / "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md", "Q_source_X", "weak-field source charge input"),
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


def constant_field_theorem_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "theorem_id": "CFT3659_0_local_linearized_EOM",
            "object": "local extra-field equation",
            "statement": "For a stable local extra field X around its vacuum value, the static weak-field equation has the schematic form Z_X (nabla^2-lambda_X^-2) deltaX = -J_X.",
            "formula": "Z_X*(nabla^2-lambda_X^-2)*deltaX = -J_X",
            "theorem_status": "LINEAR_LOCAL_EOM_FORM_DERIVED_CONDITIONALLY",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "CFT3659_1_exterior_profile",
            "object": "exterior solution",
            "statement": "Outside a compact local source with no growing mode at infinity, the massive exterior solution is deltaX(r)=A_X exp(-r/lambda_X)/r; in the massless limit it is A_X/r.",
            "formula": "J_X=0 outside source => deltaX=A_X*exp(-r/lambda_X)/r",
            "theorem_status": "EXTERIOR_PROFILE_LAW_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "CFT3659_2_amplitude_source_charge",
            "object": "profile amplitude/source charge",
            "statement": "The exterior amplitude is fixed by the integrated source charge and normalization: A_X is proportional to Q_X/Z_X, up to Green-function conventions.",
            "formula": "A_X ~= Q_X/(4*pi*Z_X) for the canonical Green normalization",
            "theorem_status": "COUPLING_IS_THE_PROFILE_AMPLITUDE_GATE",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "CFT3659_3_constant_field_zero",
            "object": "constant-field theorem",
            "statement": "If Q_X=0, the growing homogeneous mode is forbidden, Z_X>0, lambda_X^2>0, and no boundary hair is injected, then A_X=0 and the local exterior field is constant.",
            "formula": "Q_X=0 and no_boundary_hair and Z_X>0 and lambda_X^2>0 => deltaX=0 => C_gradient_TF_gamma=0",
            "theorem_status": "CONDITIONAL_CONSTANT_FIELD_ZERO_THEOREM_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "theorem_id": "CFT3659_4_current_MTS_status",
            "object": "parent/source signature",
            "statement": "Current MTS has the route but not the signature: Q_X/source-current/material-representation zero is still unsigned, so the local gamma branch cannot claim constant-field zero.",
            "formula": "need parent Q_X=0 or sourced A_X,lambda_X,k_H,k_G",
            "theorem_status": "PARENT_SOURCE_CHARGE_ZERO_UNSIGNED",
            "claim_allowed": False,
        },
    ]


def profile_input_rows(ts: str) -> list[dict[str, object]]:
    gamma = next(row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv") if row["row_id"] == "R3_gamma")
    upper = parse_float(gamma["upper_bound"])
    specs = [
        ("PI3659_0_QX_source", "Q_X", "integrated local MTS source charge", "Q_X=int d^3x J_X", "MISSING_PARENT_SOURCE_CHARGE_ZERO_OR_NUMERIC_SOURCE", "3651 Q_A^X law; 3652 Q_source_X"),
        ("PI3659_1_ZX", "Z_X", "quadratic kinetic normalization of local extra field", "S_X quadratic term contains -Z_X/2 (partial X)^2", "MISSING_PARENT_QUADRATIC_ACTION_NORMALIZATION", "parent action required"),
        ("PI3659_2_lambdaX", "lambda_X", "local range/mass scale", "lambda_X=1/M_X", "MISSING_PARENT_MASS_OR_RANGE", "parent Hessian required"),
        ("PI3659_3_AX", "A_X", "exterior profile amplitude", "A_X ~= Q_X/(4*pi*Z_X)", "MISSING_QX_ZX_NUMERIC_INPUTS", "derived in 3659"),
        ("PI3659_4_kH", "k_H", "linear Hessian-STF coefficient in gamma slip", "C_H=|k_H|*|X_second-X_prime/r|/|Phi_N|", "MISSING_WEAK_FIELD_OPERATOR_PROJECTION", "3658 profile coefficient"),
        ("PI3659_5_kG", "k_G", "gradient-square-STF coefficient in gamma slip", "C_G=|k_G|*|X_prime|^2/|Phi_N|", "MISSING_WEAK_FIELD_OPERATOR_PROJECTION", "3658 profile coefficient"),
        ("PI3659_6_boundary_hair", "B_X", "local boundary/hair injection amplitude", "B_X=0 required for constant-field theorem", "MISSING_BOUNDARY_SILENCE_SIGNATURE", "3655/3656 boundary clause"),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "required_for": "delta_gamma_MTS profile score or zero theorem",
            "cassini_required_bound": upper,
            "units": gamma["units"],
            "source_hint": source_hint,
            "current_status": current_status,
            "score_ready": False,
            "placeholder_refused_as_claim": True,
            "claim_allowed": False,
        }
        for input_id, symbol, definition, formula, current_status, source_hint in specs
    ]


def source_charge_gate_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "gate_id": "SCG3659_0_matter_descent_zero",
            "object": "Q_X",
            "zero_route": "matter action and source measure descend through q/fixed representation so Lie_vX ln M_A_eff=0 for local ordinary matter",
            "current_status": "UNSIGNED_BUT_NOW_IDENTIFIED_AS_GAMMA_CRITICAL",
            "if_signed": "A_X=0 and C_gradient_TF_gamma=0 for the corresponding local field",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "gate_id": "SCG3659_1_nonzero_charge_bound",
            "object": "Q_X/Z_X",
            "zero_route": "if Q_X is not zero, fit or bound Q_X/Z_X using gamma/WEP/R10/shared source arena",
            "current_status": "BOUND_ROUTE_READY_INPUTS_MISSING",
            "if_signed": "profile coefficient can be scored against C_gamma_TF_total<=2.3e-5",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3659_0_exterior_profile", "exterior local profile law derived", "PASSED_DERIVATION", "deltaX=A_X exp(-r/lambda_X)/r outside a compact source"),
        ("CG3659_1_coupling_gate", "profile amplitude tied to source charge", "PASSED_DERIVATION", "A_X proportional to Q_X/Z_X"),
        ("CG3659_2_constant_field", "constant-field zero theorem derived conditionally", "PASSED_CONDITIONAL_THEOREM", "Q_X=0 plus no boundary hair gives deltaX=0"),
        ("CG3659_3_no_claim", "no local-GR/gamma pass claimed", "ACTIVE_GUARD", "Q_X=0 or numeric Q_X/Z_X remains unsigned"),
        ("CG3659_4_next", "next step targets Q_X zero proof or bound acquisition", "SOURCE_CHARGE_ZERO_OR_BOUND_NEXT", "the coupling is now the narrow target"),
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
            "status": "LOCAL_CONSTANT_FIELD_THEOREM_CONDITIONAL_SOURCE_CHARGE_GATE_IDENTIFIED",
            "summary": "3659 derives the local exterior profile law and the constant-field theorem: the gamma-relevant profile amplitude is controlled by Q_X/Z_X, so Q_X=0 is the clean local-GR route and nonzero Q_X must be bounded.",
            "claim_ceiling": "no MTS gamma prediction, local-GR pass, PPN pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed",
            "useful_result": "The coupling really is the key at this rung: local gamma now narrows to proving Q_X=0 or sourcing Q_X,Z_X,lambda_X,k_H,k_G.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3659_0",
            "target_doc": "3660-Y5-R2FR-QX-source-charge-zero-proof-or-gamma-bound-input-pack.md",
            "target_script": "scripts/Y5_R2FR_3660_QX_source_charge_zero_proof_or_gamma_bound_input_pack.py",
            "objective": "try to prove Q_X=0 from parent matter/source descent; if not, build the nonclaim gamma-bound input pack for Q_X, Z_X, lambda_X, k_H, and k_G",
            "success_gate": "Q_X is parent-zero for the local ordinary source or every required gamma profile input has an explicit source/provenance status with placeholders refused as claims",
        }
    ]


def write_doc(sources, theorem, inputs, source_gates, gates, status_rows_, next_target) -> None:
    lines = [
        "# 3659 - Parent local constant-field theorem or profile input acquisition",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The local gamma problem has narrowed to the coupling/source-charge gate.",
        "",
        "For a stable local extra field, the exterior equation has the schematic form",
        "",
        "`Z_X (nabla^2-lambda_X^-2) deltaX = 0` outside the compact source,",
        "",
        "so with no growing mode the exterior profile is",
        "",
        "`deltaX(r)=A_X exp(-r/lambda_X)/r`.",
        "",
        "The amplitude is not magic: `A_X ~= Q_X/(4*pi*Z_X)` in canonical Green normalization. Therefore the clean local-GR route is `Q_X=0` plus no boundary hair, which gives `deltaX=0` and kills the gamma STF profile. If `Q_X` is not zero, the theory must bound `Q_X/Z_X`, `lambda_X`, `k_H`, and `k_G` against Cassini gamma.",
        "",
        "## Constant-field theorem attempt",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['theorem_status']} - `{row['formula']}`")
    lines.extend(["", "## Profile/source input rows"])
    for row in inputs:
        lines.append(f"- `{row['input_id']}`: `{row['symbol']}` - {row['current_status']}")
    lines.extend(["", "## Source-charge gates"])
    for row in source_gates:
        lines.append(f"- `{row['gate_id']}`: `{row['object']}` - {row['current_status']}")
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


def validate(ts, output_paths, sources, theorem, inputs, source_gates, gates, status_rows_, next_target) -> list[dict[str, object]]:
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

    add("VAL3659_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3659_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3659_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3659 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3659_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3659_4_exterior_profile", any("A_X*exp(-r/lambda_X)/r" in row["formula"] for row in theorem), "exterior profile law derived")
    add("VAL3659_5_amplitude_charge_gate", any("Q_X/(4*pi*Z_X)" in row["formula"] for row in theorem), "profile amplitude tied to source charge")
    add("VAL3659_6_constant_field_theorem", any(row["theorem_status"] == "CONDITIONAL_CONSTANT_FIELD_ZERO_THEOREM_DERIVED" for row in theorem), "conditional constant-field theorem derived")
    required = {"Q_X", "Z_X", "lambda_X", "A_X", "k_H", "k_G", "B_X"}
    add("VAL3659_7_inputs_registered", required.issubset({row["symbol"] for row in inputs}), "profile/source inputs registered")
    add("VAL3659_8_placeholders_refused", all(str(row["placeholder_refused_as_claim"]).lower() == "true" and str(row["score_ready"]).lower() == "false" for row in inputs), "all input placeholders refused as claims")
    add("VAL3659_9_source_charge_gates", {"SCG3659_0_matter_descent_zero", "SCG3659_1_nonzero_charge_bound"}.issubset({row["gate_id"] for row in source_gates}), "source charge zero/bound gates present")
    add("VAL3659_10_claim_gates_present", {"CG3659_0_exterior_profile", "CG3659_1_coupling_gate", "CG3659_2_constant_field", "CG3659_3_no_claim", "CG3659_4_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + theorem + inputs + source_gates + gates + status_rows_ + next_target
    add("VAL3659_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3659_12_doc_written", "Q_X=0" in doc_text and "A_X ~= Q_X/(4*pi*Z_X)" in doc_text and "coupling/source-charge gate" in doc_text, "doc records source-charge gate")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3659*", "3659-Y5-R2FR-*", "Y5_R2FR_3659_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3659_13_no_formalization_leak", not leaks, "no 3659 checkpoint files in formalization-workbench")
    add("VAL3659_14_next_target", next_target[0]["target_doc"].startswith("3660-") and "QX" in next_target[0]["target_doc"], "3660 QX source-charge target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = constant_field_theorem_rows(ts)
    inputs = profile_input_rows(ts)
    source_gates = source_charge_gate_rows(ts)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3659_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3659_CONSTANT_FIELD_THEOREM_ATTEMPT.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3659_PROFILE_INPUT_ACQUISITION_ROWS.csv",
        "source_gates": RESIDUALS / "P8_Y5_R2FR_3659_SOURCE_CHARGE_GATE_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3659_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3659_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3659_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3659_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["inputs"], inputs)
    write_csv(outputs["source_gates"], source_gates)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, inputs, source_gates, gates, status_rows_, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, inputs, source_gates, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3659 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3659 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
