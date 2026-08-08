from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DD_TEX = ROOT / "source-intake" / "external-sources" / "damour_donoghue_1007.2792_source" / "DamourDonoghueEPfinal.tex"

DOC = ROOT / "3259-Y5-R2FR-parent-alpha-map-owner-or-DD-comparator-demotion-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3259_SOURCE_REGISTER.csv",
    "dd_evidence": OUT / "P8_Y5_R2FR_3259_DD_SOURCE_EVIDENCE_LINES.csv",
    "pullback": OUT / "P8_Y5_R2FR_3259_PARENT_ALPHA_PULLBACK_THEOREM.csv",
    "branch_split": OUT / "P8_Y5_R2FR_3259_FIXED_EM_VS_DD_BRANCH_SPLIT.csv",
    "residual_vector": OUT / "P8_Y5_R2FR_3259_DD_CALIBRATED_EM_RESIDUAL_VECTOR_NONCLAIM.csv",
    "bound_formula": OUT / "P8_Y5_R2FR_3259_EM_BRANCH_BOUND_INVERSION_FORMULA_NONCLAIM.csv",
    "parent_audit": OUT / "P8_Y5_R2FR_3259_PARENT_ALPHA_OWNER_AUDIT.csv",
    "gates": OUT / "P8_Y5_R2FR_3259_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3259_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3259_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3259_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:260]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def line_hit(path: Path, needle: str) -> tuple[int | None, str]:
    if not path.exists():
        return None, "MISSING_SOURCE"
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            if needle in line:
                return line_number, " ".join(line.strip().split())
    return None, "NO_MATCH"


def float_or_none(value: Any) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3259_3258_handoff",
            ROOT / "3258-Y5-R2FR-source-backed-EM-Coulomb-coefficient-or-parent-alpha-map-owner-under-AX1090.md",
            "3258 selected parent alpha-map owner or DD demotion",
            ["NEXT3258_0_3259", "Q'_e", "PARENT_ALPHA_MAP_UNSIGNED"],
        ),
        (
            "SRC3259_3258_dd_rows",
            OUT / "P8_Y5_R2FR_3258_DD_EM_CHARGE_EXTERNAL_COMPARATOR_NONCLAIM.csv",
            "numeric DD external EM charge rows",
            ["DD3258_TA6V_minus_PtRh10_Qe_prime", "Qe_prime_DD"],
        ),
        (
            "SRC3259_1055_parent_contract",
            OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "parent action fixed EM owner candidate",
            ["PAC1055_1_EM_owner", "no f(Xhat)F_Q^2"],
        ),
        (
            "SRC3259_1065_charge_norm",
            OUT / "P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv",
            "charge/current normalization audit",
            ["CIN1065_4_verdict", "CONDITIONAL_NOT_PARENT_SIGNED"],
        ),
        (
            "SRC3259_1234_em_owner",
            OUT / "P8_Y5_R10_1234_EM_OWNER_UNIQUENESS_PROOF_ATTEMPT.csv",
            "EM owner uniqueness attempt",
            ["EMU1234_2_unique_F2", "EMU1234_6_verdict"],
        ),
        (
            "SRC3259_1397_unique_F2",
            OUT / "P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
            "unique Maxwell F2 theorem audit",
            ["UMF1397_6_exact_conditional_theorem", "UMF1397_7_current_verdict"],
        ),
        (
            "SRC3259_1400_em_residual",
            OUT / "P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv",
            "finite EM local residual vector and b_alpha product",
            ["REM1400_3_b_alpha_EM", "REM1400_6_WEP"],
        ),
        (
            "SRC3259_1910_response_contract",
            OUT / "P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv",
            "exact material response tensor contract",
            ["MDT1910_3_EM_Coulomb_binding", "DeltaR_AB"],
        ),
        (
            "SRC3259_DD_tex",
            DD_TEX,
            "downloaded arXiv source for DD alpha chain and Q'_e formula",
            ["Q'_{e}", "7.7 \\times 10^{-4}", "alpha_A"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def dd_source_evidence_rows() -> list[dict[str, Any]]:
    specs = [
        ("DD3259_alpha_A_definition", "\\alpha_A =  \\frac{\\partial \\ln[\\kappa m_A(\\varphi)] }{\\partial \\varphi}", "body scalar coupling is derivative of log mass along scalar path"),
        ("DD3259_alpha_variation", "\\alpha(\\varphi) &=   &(1 + d_e \\varphi)  \\alpha", "fine-structure constant varies with d_e in DD parameterization"),
        ("DD3259_mass_chain_rule", "\\bar{\\alpha}_A \\equiv \\frac{\\partial \\ln M_A}{ \\partial \\varphi}", "composition-dependent part is mass-response derivative"),
        ("DD3259_alpha_chain_sum", "= \\frac{1}{M_A}\\left[ \\sum_{a=u,d,e} (d_{m_a}-d_g)\\frac{\\partial M_A}{\\partial \\ln k_a}+ d_e \\frac{\\partial M_A}{ \\partial \\ln \\alpha}\\right].", "chain rule isolates alpha derivative"),
        ("DD3259_Qe_formula", "Q'_{e} =  + 7.7 \\times 10^{-4} \\frac{Z(Z-1)}{A^{4/3}}", "DD approximate electromagnetic charge formula"),
        ("DD3259_WEP_formula", "\\left( \\frac{\\Delta a}{a} \\right)_{BC} = (\\alpha_B- \\alpha_C)\\alpha_E", "DD WEP signal is differential coupling times source coupling"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, needle, role in specs:
        line_number, text = line_hit(DD_TEX, needle)
        rows.append(
            {
                "evidence_id": row_id,
                "source_path": str(DD_TEX),
                "line_number": line_number if line_number is not None else "NO_MATCH",
                "text_excerpt": text,
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def dd_external_values() -> dict[str, float]:
    path = OUT / "P8_Y5_R2FR_3258_DD_EM_CHARGE_EXTERNAL_COMPARATOR_NONCLAIM.csv"
    values: dict[str, float] = {}
    for row in read_csv(path):
        value = float_or_none(row.get("Qe_prime_DD"))
        if value is not None:
            values[row["material_id"]] = value
    return values


def pullback_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PB3259_0_parent_path",
            "statement": "Let Phi(s) be an allowed parent path and alpha_EM(Phi) the observed dimensionless EM coupling after quotient/readout.",
            "formula": "b_alpha^P := d_s ln alpha_EM(Phi(s))",
            "derivation_status": "DEFINITION_READY",
            "claim_effect": "turns vague alpha drift into a single parent pullback coefficient",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PB3259_1_chain_rule",
            "statement": "If the only retained material dependence along Phi(s) is the alpha/Coulomb channel, the material response is the DD alpha charge times the parent alpha pullback plus a residual.",
            "formula": "d_s ln M_A|EM = Q'_e,A b_alpha^P + r_A^EM",
            "derivation_status": "EXACT_CHAIN_RULE_WITH_RESIDUAL",
            "claim_effect": "DD becomes a calibrated residual vector only after parent alpha map is signed",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PB3259_2_pair_difference",
            "statement": "For a material pair, common-mode terms cancel and the differential EM residual is controlled by the DD charge difference.",
            "formula": "DeltaR_AB^EM = b_alpha^P DeltaQ'_e,AB + Delta r_AB^EM",
            "derivation_status": "EXACT_PAIR_PULLBACK_LAW",
            "claim_effect": "source coupling is now a scalar product coefficient times a known composition vector",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PB3259_3_fixed_EM_zero",
            "statement": "If the parent action signs fixed EM representation/norm, no hidden F_Q^2 slot, and quotient-fixed readout, then alpha_EM is constant on local vertical paths.",
            "formula": "Lie_v alpha_EM=0 => b_alpha^P=0 => DeltaR_AB^EM=Delta r_AB^EM; if no extra EM matter vertex, Delta r_AB^EM=0",
            "derivation_status": "CONDITIONAL_ZERO_THEOREM_READY",
            "claim_effect": "this is the clean local-GR route: kill EM composition drift by parent ownership, not by fitting",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PB3259_4_controlled_DD_branch",
            "statement": "If alpha_EM is not parent-fixed, DD is demoted/promoted only to a finite residual input with source/readout product still required.",
            "formula": "eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res, B_alpha^MTS:=beta_source_alpha b_alpha_EM tau_WEP",
            "derivation_status": "FINITE_BOUND_BRANCH_READY",
            "claim_effect": "lets future tests bound the coupling rather than hiding it",
            "valid_for_claim": "false",
        },
    ]


def branch_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BR3259_FIXED_EM",
            "branch_name": "fixed parent EM representation",
            "premise": "PAC1055_1, EMU1234, and UMF1397 clauses are parent-signed: EM norm/readout is fixed and no hidden alpha/F_Q^2 coefficient survives",
            "result": "b_alpha^P=0 and DD EM branch contributes zero to local WEP/PPN/source composition residuals",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "why_useful": "best route for reducing to GR/Newton: source coupling is eliminated by action ownership",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3259_DD_BOUND",
            "branch_name": "controlled alpha residual",
            "premise": "parent action permits or fails to exclude alpha_EM pullback",
            "result": "retain eta_AB^EM=DeltaQ'_e,AB B_alpha^MTS and bound B_alpha^MTS with WEP/clock/orbital data",
            "current_status": "NUMERIC_COMPOSITION_VECTOR_READY_SOURCE_PRODUCT_MISSING",
            "why_useful": "prevents alpha coupling from being a ghost parameter; it becomes one finite tested product",
            "valid_for_claim": "false",
        },
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    values = dd_external_values()
    delta = values.get("TA6V_minus_PtRh10")
    abs_delta = abs(delta) if delta is not None else None
    rows: list[dict[str, Any]] = []
    for material_id in ["PtRh10", "TA6V", "TA6V_minus_PtRh10"]:
        value = values.get(material_id)
        rows.append(
            {
                "residual_id": f"RV3259_{material_id}_EM",
                "material_id": material_id,
                "Qe_prime_DD": f"{value:.12e}" if value is not None else "MISSING",
                "parent_pullback_formula": "R_A^EM = Q'_e,A b_alpha^P + r_A^EM",
                "source_observable_formula": "eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res",
                "status": "NUMERIC_EXTERNAL_VECTOR_PARENT_PRODUCT_MISSING",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "residual_id": "RV3259_TA6V_minus_PtRh10_unit_product",
            "material_id": "TA6V_minus_PtRh10",
            "Qe_prime_DD": f"{delta:.12e}" if delta is not None else "MISSING",
            "parent_pullback_formula": "DeltaR_TA6V-PtRh10^EM = (-1.982376296670e-3) b_alpha^P + Delta r_EM",
            "source_observable_formula": "eta_TA6V-PtRh10^EM = (-1.982376296670e-3) B_alpha^MTS + Delta eta_res",
            "status": f"ABS_DELTA_QE={abs_delta:.12e}" if abs_delta is not None else "MISSING_DELTA",
            "valid_for_claim": "false",
        }
    )
    return rows


def bound_formula_rows() -> list[dict[str, Any]]:
    values = dd_external_values()
    delta = values.get("TA6V_minus_PtRh10")
    abs_delta = abs(delta) if delta is not None else None
    return [
        {
            "bound_id": "BOUND3259_0_symbolic_WEP",
            "observable": "eta_TA6V_minus_PtRh10",
            "formula": "|B_alpha^MTS| <= (eta_bound_abs + |Delta eta_res|)/|DeltaQ'_e|",
            "numeric_denominator": f"{abs_delta:.12e}" if abs_delta is not None else "MISSING_DELTA_QE",
            "input_needed": "real eta_bound_abs for the selected WEP branch plus source/readout/tau convention",
            "status": "BOUND_FORMULA_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BOUND3259_1_clock_crosscheck",
            "observable": "clock/fine-structure residual",
            "formula": "C_clock_EM=K_alpha b_alpha_EM tau_clock; compare against same b_alpha_EM used in WEP product",
            "numeric_denominator": "not_applicable",
            "input_needed": "clock sensitivity K_alpha, tau_clock, and same parent alpha pullback b_alpha_EM",
            "status": "CROSSCHECK_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BOUND3259_2_fixed_zero",
            "observable": "all alpha/Coulomb local residuals",
            "formula": "if fixed-EM branch signs b_alpha^P=0 and Delta r_EM=0, no WEP/clock alpha residual remains",
            "numeric_denominator": "zero_theorem_branch",
            "input_needed": "parent-signed fixed EM owner/no-counterterm/readout descent clauses",
            "status": "ZERO_BRANCH_READY_BUT_UNSIGNED",
            "valid_for_claim": "false",
        },
    ]


def parent_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "AUD3259_0_EM_owner",
            "needed_clause": "observed EM connection and kinetic normalization are parent-owned fixed representation/topological data",
            "source_anchor": "PAC1055_1_EM_owner",
            "current_status": "CANDIDATE_CLAUSE_PRESENT_NOT_PARENT_SIGNED",
            "effect_if_signed": "b_alpha^P=0 on local vertical paths unless a separate allowed alpha deformation is declared",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "AUD3259_1_no_counterterm",
            "needed_clause": "no independent lambda_A F_Q^2 or hidden f(X)F_Q^2 slot",
            "source_anchor": "EMU1234_2_unique_F2;UMF1397_7_current_verdict",
            "current_status": "CURRENT_CORPUS_FAILS_TO_EXCLUDE_COUNTERTERM",
            "effect_if_signed": "removes standalone alpha drift branch",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "AUD3259_2_readout_descent",
            "needed_clause": "Hodge/coframe/hbar*c/readout factors are quotient-fixed",
            "source_anchor": "EMU1234_4_readout_descent;REM1400_2_readout",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect_if_signed": "prevents fake alpha drift through unit/readout changes",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "AUD3259_3_no_extra_matter_vertex",
            "needed_clause": "no hidden alpha/mass/binding vertex after quotient",
            "source_anchor": "EMU1234_5_no_alpha_vertex;MDT1910_3_EM_Coulomb_binding",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect_if_signed": "sets Delta r_AB^EM=0 after b_alpha^P=0",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3259_0_pullback_theorem",
            "gate": "parent alpha pullback law written",
            "passed": "true",
            "reason": "exact chain-rule form d_s ln M_A=Q'_e,A b_alpha^P+r_A^EM is recorded",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3259_1_fixed_zero_claim",
            "gate": "fixed-EM zero theorem parent-signed",
            "passed": "false",
            "reason": "EM owner/no-counterterm/readout/no-vertex clauses remain conditional or failed in current corpus",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3259_2_DD_residual_claim",
            "gate": "DD comparator promoted to MTS source-coupling evidence",
            "passed": "false",
            "reason": "numeric DD vector exists but B_alpha^MTS and parent alpha map are not signed",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3259_3_local_GR",
            "gate": "local GR/Newton/Maxwell reduction from EM branch",
            "passed": "false",
            "reason": "requires either fixed-EM zero branch or bounded residual branch with source/readout/tau product",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3259_0",
            "verdict": "ALPHA_BRANCH_SPLIT_DERIVED_NOT_CLOSED",
            "what_moved": "DD is no longer a loose external number: it is the finite composition vector in DeltaR_AB^EM=b_alpha^P DeltaQ'_e+Delta r_EM",
            "best_route": "try fixed-EM parent owner first because it gives b_alpha^P=0 and the cleanest GR/Newton reduction",
            "fallback_route": "if fixed-EM cannot be signed, use DD vector to bound B_alpha^MTS against WEP/clock data",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3259_0_3260",
            "selected": "primary",
            "target_doc": "3260-Y5-R2FR-fixed-EM-owner-zero-theorem-or-DD-WEP-bound-runner-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3260_fixed_EM_owner_zero_theorem_or_DD_WEP_bound_runner.py",
            "objective": "Try to sign the fixed-EM owner/no-counterterm/readout/no-vertex chain; if it fails, run the DD residual vector through a WEP bound formula with real eta/tau inputs.",
            "guardrail": "No MTS local-GR claim unless b_alpha^P=0 is parent-signed or the finite residual product is empirically bounded below the local gate.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = source_register()
    dd_evidence = dd_source_evidence_rows()
    residual_rows = residual_vector_rows()
    delta_row = next(row for row in residual_rows if row["residual_id"] == "RV3259_TA6V_minus_PtRh10_unit_product")
    validations = [
        {
            "check_id": "VAL3259_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3259_1_sources_parse",
            "check": "all cited source CSV/MD/TEX paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3259_2_DD_lines_found",
            "check": "DD source evidence lines are found",
            "passed": bool_str(all(row["line_number"] != "NO_MATCH" for row in dd_evidence)),
            "detail": ";".join(f"{row['evidence_id']}:{row['line_number']}" for row in dd_evidence),
        },
        {
            "check_id": "VAL3259_3_outputs_parse",
            "check": "all 3259 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3259_4_delta_vector_numeric",
            "check": "TA6V_minus_PtRh10 DD EM differential vector is finite numeric",
            "passed": bool_str(float_or_none(delta_row["Qe_prime_DD"]) is not None and math.isfinite(float(delta_row["Qe_prime_DD"]))),
            "detail": delta_row["Qe_prime_DD"],
        },
        {
            "check_id": "VAL3259_5_claim_gates_false",
            "check": "no 3259 claim gate allows local-GR/WEP/Maxwell promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3259_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3259_7_overall",
            "check": "3259 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3259_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    dd_evidence = dd_source_evidence_rows()
    pullback = pullback_rows()
    branch_split = branch_split_rows()
    residual = residual_vector_rows()
    bounds = bound_formula_rows()
    parent_audit = parent_audit_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3259 - Parent alpha-map owner or DD comparator demotion under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3259` derives the exact parent-alpha pullback law: `d_s ln M_A|EM = Q'_e,A b_alpha^P + r_A^EM`.
- This is a real fork, not a ledger loop: if the parent action fixes EM/readout, `b_alpha^P=0`; if it does not, the DD vector is the finite residual to bound.
- For the Ti/Pt branch, `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3`, so `eta_EM = -1.982376296670e-3 B_alpha^MTS + residual`.
- No claim is promoted because the fixed-EM owner chain is still unsigned and the finite residual product still lacks source/readout/tau input.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## DD Source Evidence Lines
{md_table(dd_evidence, ["evidence_id", "line_number", "text_excerpt", "role", "valid_for_claim"])}

## Parent Alpha Pullback Theorem
{md_table(pullback, ["theorem_id", "statement", "formula", "derivation_status", "claim_effect", "valid_for_claim"])}

## Branch Split
{md_table(branch_split, ["branch_id", "branch_name", "premise", "result", "current_status", "why_useful", "valid_for_claim"])}

## DD-Calibrated EM Residual Vector
{md_table(residual, ["residual_id", "material_id", "Qe_prime_DD", "parent_pullback_formula", "source_observable_formula", "status", "valid_for_claim"])}

## Bound Inversion Formula
{md_table(bounds, ["bound_id", "observable", "formula", "numeric_denominator", "input_needed", "status", "valid_for_claim"])}

## Parent Alpha Owner Audit
{md_table(parent_audit, ["audit_id", "needed_clause", "source_anchor", "current_status", "effect_if_signed", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_route", "fallback_route", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_key = {
        "sources": source_register(),
        "dd_evidence": dd_source_evidence_rows(),
        "pullback": pullback_rows(),
        "branch_split": branch_split_rows(),
        "residual_vector": residual_vector_rows(),
        "bound_formula": bound_formula_rows(),
        "parent_audit": parent_audit_rows(),
        "gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
