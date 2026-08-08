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

DOC = ROOT / "3267-Y5-R2FR-parent-source-map-signature-for-DD-coordinates-under-AX1090.md"
DOC_3266 = ROOT / "3266-Y5-R2FR-source-convention-lock-or-two-channel-bound-promotion-under-AX1090.md"
DD_TEX = ROOT / "source-intake" / "external-sources" / "damour_donoghue_1007.2792_source" / "DamourDonoghueEPfinal.tex"
GRAMMAR_3007 = OUT / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv"
MATTER_2970 = OUT / "P8_Y5_R2FR_2970_BASIC_MATTER_ACTION_AUDIT.csv"
PTD_2788 = OUT / "P8_Y5_R2FR_2788_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv"
DCR_2788 = OUT / "P8_Y5_R2FR_2788_DD_CHAIN_RULE_MAP_CONTRACT.csv"
PDD_2787 = OUT / "P8_Y5_R2FR_2787_PARENT_TO_DD_GATE.csv"
CRIT_3214 = OUT / "P8_Y5_R2FR_3214_INVARIANT_COUPLING_CRITERION.csv"
GAINS_3266 = OUT / "P8_Y5_R2FR_3266_MATRIX_INVERSE_AND_RESIDUAL_GAINS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3267_SOURCE_REGISTER.csv",
    "dd_evidence": OUT / "P8_Y5_R2FR_3267_DD_SOURCE_MAP_EVIDENCE.csv",
    "signature": OUT / "P8_Y5_R2FR_3267_PARENT_DD_SIGNATURE_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3267_CURRENT_MTS_SIGNATURE_AUDIT.csv",
    "scale_law": OUT / "P8_Y5_R2FR_3267_ARENA_SCALE_RESIDUAL_LAW.csv",
    "projection": OUT / "P8_Y5_R2FR_3267_OPERATOR_PROJECTION_TARGETS.csv",
    "gates": OUT / "P8_Y5_R2FR_3267_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3267_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3267_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3267_VALIDATION.csv",
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
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def line_hit(path: Path, needles: list[str]) -> tuple[int | None, str]:
    if not path.exists():
        return None, "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if all(needle in lowered_line for needle in lowered_needles):
                return line_number, " ".join(line.strip().split())
    return None, "NO_MATCH"


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
            "SRC3267_3266_contract",
            DOC_3266,
            "3266 exact eta=A D+epsilon contract",
            ["CON3266_0_parent_action_signature", "D=A^-1", "LOCK3266_0_common_field"],
        ),
        (
            "SRC3267_DD_tex",
            DD_TEX,
            "DD source-map and two-charge body-coupling convention",
            ["d_e, d_g", "chain rule", "approxalphaA"],
        ),
        (
            "SRC3267_3007_parent_grammar",
            GRAMMAR_3007,
            "current minimal parent action grammar",
            ["G3007_2_universal_matter_worldtube", "G3007_10_verdict"],
        ),
        (
            "SRC3267_2970_matter_audit",
            MATTER_2970,
            "q-basic matter action and Hilbert-current status",
            ["MAT2970_0_chain_rule", "MAT2970_7_verdict"],
        ),
        (
            "SRC3267_2788_parent_to_DD",
            PTD_2788,
            "previous parent-to-DD coefficient-map attempt",
            ["PTD2788_1_chain_rule_form", "PTD2788_6_verdict"],
        ),
        (
            "SRC3267_2788_chain_rule_contract",
            DCR_2788,
            "DD chain-rule map contract",
            ["DCR2788_0_parent_coordinates", "DCR2788_5_claim_rule"],
        ),
        (
            "SRC3267_2787_parent_gate",
            PDD_2787,
            "parent-to-DD gate from finite WEP smoke branch",
            ["PDD2787_0_parent_basis", "PDD2787_5_readout_kernel"],
        ),
        (
            "SRC3267_3214_invariant_criterion",
            CRIT_3214,
            "invariant coupling criterion for visible coefficients",
            ["CRIT3214_0_vertical_derivative_decomposition", "CRIT3214_4_finite_fallback_condition"],
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


def dd_evidence_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DDE3267_0_interaction_lagrangian",
            ["cal l", "int", "phi"],
            "DD starts from a universal scalar interaction Lagrangian with five low-energy coefficients.",
        ),
        (
            "DDE3267_1_chain_rule",
            ["chain rule"],
            "DD explicitly permits computing body couplings by chain rule through low-energy constants.",
        ),
        (
            "DDE3267_2_constants",
            ["alpha", "lambda_3", "m_e"],
            "DD identifies the relevant constants whose parent variation must be owned.",
        ),
        (
            "DDE3267_3_approx_alpha",
            ["alpha", "d_g^*", "q'_{\\hat m}"],
            "DD reduced body coupling has universal d_g* plus material terms.",
        ),
        (
            "DDE3267_4_qhatm",
            ["q'_{\\hat m}", "0.036"],
            "DD Q'_hatm charge formula.",
        ),
        (
            "DDE3267_5_qe",
            ["q'_{e}", "7.7"],
            "DD Q'_e charge formula.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for evidence_id, needles, role in specs:
        line_number, text = line_hit(DD_TEX, needles)
        rows.append(
            {
                "evidence_id": evidence_id,
                "source_path": str(DD_TEX),
                "source_url": "https://arxiv.org/abs/1007.2792",
                "line_number": line_number if line_number is not None else "NO_MATCH",
                "text_excerpt": text,
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def signature_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SIG3267_0_parent_low_energy_vector",
            "statement": "If one MTS parent generator X varies the low-energy constants by arena-independent coefficients C_g,C_hatm,C_e, then DD coordinates are MTS-owned.",
            "math": "L_X ln Lambda_3=C_g; L_X ln hatm=C_hatm; L_X ln alpha_EM=C_e; D_hatm=C_hatm-C_g; D_e=C_e.",
            "proof_status": "CONDITIONAL_EXACT_CHAIN_RULE",
            "what_is_derived": "the exact parent-to-DD coefficient map once the parent generator and coefficients are supplied",
            "what_is_not_derived": "the current corpus does not sign C_g,C_hatm,C_e from a single parent action",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SIG3267_1_universal_piece_cancels",
            "statement": "The DD universal piece d_g* cannot generate WEP composition dependence between two test bodies.",
            "math": "alpha_A=d_g*+D_hatm Qhatm_A+D_e Qe_A; alpha_A-alpha_B=D_hatm DeltaQhatm_AB+D_e DeltaQe_AB.",
            "proof_status": "DERIVED_FROM_DD_REDUCED_FORM",
            "what_is_derived": "the two-channel row is the complete dominant composition-dependent part under DD approximations",
            "what_is_not_derived": "MTS ownership of D_hatm,D_e and omitted-channel residual silence",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SIG3267_2_arena_independence_condition",
            "statement": "MICROSCOPE and Eot-Wash share one D vector iff the same C_g,C_hatm,C_e feed both material rows before readout/source modelling.",
            "math": "D_i^k=D_i for every arena k; any arena-specific factor is moved to s_k or epsilon_k.",
            "proof_status": "EXACT_DEFINITIONAL_LOCK",
            "what_is_derived": "a precise test for the parent source-map signature",
            "what_is_not_derived": "no current parent-action row signs s_k=1 and epsilon_k=0",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SIG3267_3_failure_normal_form",
            "statement": "If the parent map is not signed, the honest normal form is eta_k=s_k DeltaQ_k dot D + epsilon_k, not eta_k=DeltaQ_k dot D.",
            "math": "unknown positive s_k rescales row k; unknown epsilon_k adds residual budget from omitted channels/readout/source profile.",
            "proof_status": "DERIVED_NO_SMUGGLING_NORMAL_FORM",
            "what_is_derived": "all missing parent-source-map content has a place in the bound law",
            "what_is_not_derived": "numeric s_min or epsilon budgets",
            "valid_for_claim": "false",
        },
    ]


def audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "AUD3267_0_parent_grammar",
            "needed_signature": "one varied local parent action with universal matter/worldtube source block",
            "current_evidence": "3007 selects a grammar and keeps matter/source/worldtube as required core",
            "status": "STAGED_NOT_PARENT_SIGNED",
            "source_path": str(GRAMMAR_3007),
            "blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "AUD3267_1_matter_descent",
            "needed_signature": "ordinary matter descends through observed q-pulled geometry with no source-only prefactor",
            "current_evidence": "2970 has conditional chain rule and Hilbert-current subtheorem, but verdict remains not derived",
            "status": "CONDITIONAL_THEOREM_NOT_SIGNATURE",
            "source_path": str(MATTER_2970),
            "blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "AUD3267_2_parent_to_DD_chain_rule",
            "needed_signature": "parent generators eps_I and operator pullback D_iI into DD coordinates",
            "current_evidence": "2788 already derived the formal chain-rule map but marked parent generators/operator pullback missing",
            "status": "FORMAL_MAP_EXISTS_PARENT_OBJECTS_MISSING",
            "source_path": str(DCR_2788),
            "blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "AUD3267_3_no_hidden_visible_coefficient_slot",
            "needed_signature": "visible low-energy coefficients have no explicit hidden/source/readout slot beyond parent constants",
            "current_evidence": "3214 gives exact derivative criterion and finite fallback, but parent-owned invariant list/coefficient grammar remain required",
            "status": "CRITERION_DERIVED_NOT_CLOSED",
            "source_path": str(CRIT_3214),
            "blocks_claim": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "AUD3267_4_current_verdict",
            "needed_signature": "D_hatm,D_e are arena-independent MTS coordinates",
            "current_evidence": "3267 derives the exact signature conditions, but current sources do not satisfy all of them",
            "status": "SIGNATURE_CONTRACT_DERIVED_CURRENT_CLAIM_FAILS",
            "source_path": str(DOC),
            "blocks_claim": "true",
            "valid_for_claim": "false",
        },
    ]


def scale_law_rows() -> list[dict[str, Any]]:
    zero = next(row for row in read_csv(GAINS_3266) if row["scenario"] == "zero_residual")
    ten = next(row for row in read_csv(GAINS_3266) if row["scenario"] == "ten_percent_eta_residual")
    eta_sized = next(row for row in read_csv(GAINS_3266) if row["scenario"] == "eta_sized_residual")
    return [
        {
            "law_id": "SCALE3267_0_exact_scaled_normal_form",
            "case": "unknown_arena_scale",
            "formula": "eta_k = s_k DeltaQ_k dot D + epsilon_k",
            "Dhatm_bound": "unbounded if any |s_k| can approach 0",
            "De_bound": "unbounded if any |s_k| can approach 0",
            "interpretation": "rank-two matrix does not save the claim if source/readout normalization is allowed to vanish or flip by arena",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SCALE3267_1_positive_scale_lower_bound",
            "case": "0<s_min_k<=|s_k|",
            "formula": "|D_j| <= sum_k |A^-1_jk| (b_k+e_k)/s_min_k",
            "Dhatm_bound": "use 3266 inverse gains divided rowwise by supplied s_min_k",
            "De_bound": "use 3266 inverse gains divided rowwise by supplied s_min_k",
            "interpretation": "a future source-normalization proof can be weaker than s_k=1; a positive lower bound is enough for boundedness",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SCALE3267_2_zero_residual_s_equal_1",
            "case": "s_MICROSCOPE=s_EOTWASH=1; epsilon=0",
            "formula": "3266 zero-residual special case",
            "Dhatm_bound": zero["Dhatm_bound"],
            "De_bound": zero["De_bound"],
            "interpretation": "conditional best-case bridge if the parent signature closes exactly",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SCALE3267_3_ten_percent_residual_s_equal_1",
            "case": "s=1; epsilon_k=0.1 eta_bound_k",
            "formula": "3266 residual-gain law",
            "Dhatm_bound": ten["Dhatm_bound"],
            "De_bound": ten["De_bound"],
            "interpretation": "shows residual budgets degrade bounds linearly, not catastrophically, once source scale is locked",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SCALE3267_4_eta_sized_residual_s_equal_1",
            "case": "s=1; epsilon_k=eta_bound_k",
            "formula": "3266 residual-gain law",
            "Dhatm_bound": eta_sized["Dhatm_bound"],
            "De_bound": eta_sized["De_bound"],
            "interpretation": "even eta-sized residuals remain finite, but this is still nonclaim without sourced epsilons",
            "valid_for_claim": "false",
        },
    ]


def projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "PROJ3267_0_gluon_universal",
            "parent_operator": "O_g = beta_3/(2g_3) F_A^2 + gamma_m sum_i m_i psi_i_bar psi_i",
            "DD_coordinate": "d_g and d_g* universal part",
            "pair_effect": "cancels in alpha_A-alpha_B except through D_hatm=C_hatm-C_g",
            "needed_parent_input": "coefficient C_g from variation of one parent matter action",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3267_1_light_quark_mass",
            "parent_operator": "O_hatm = hatm (u_bar u + d_bar d) in low-energy matter action",
            "DD_coordinate": "Q'_hatm with D_hatm=C_hatm-C_g",
            "pair_effect": "material-dependent nuclear/surface response",
            "needed_parent_input": "signed parent generator for hatm/Lambda_3 response",
            "current_status": "MISSING_OPERATOR_PULLBACK",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3267_2_electromagnetic",
            "parent_operator": "O_e = F_munu F^munu / 4e^2 or alpha_EM response",
            "DD_coordinate": "Q'_e with D_e=C_e",
            "pair_effect": "material-dependent Coulomb response",
            "needed_parent_input": "signed parent generator for alpha_EM/EM stress response",
            "current_status": "MISSING_OPERATOR_PULLBACK",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3267_3_omitted_channels",
            "parent_operator": "electron mass, delta m, finite-size/binding tensor, readout/source-profile terms",
            "DD_coordinate": "epsilon_k residual",
            "pair_effect": "does not vanish unless theorem-zero or numeric budget is supplied",
            "needed_parent_input": "epsilon_MICROSCOPE and epsilon_EOTWASH source rows or zero theorems",
            "current_status": "RESIDUALIZED",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3267_0_signature_theorem",
            "gate": "parent-to-DD signature theorem written",
            "passed": "true",
            "reason": "3267 derives the exact C_g,C_hatm,C_e -> D_hatm,D_e map and failure normal form",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3267_1_current_parent_coefficients",
            "gate": "current MTS supplies C_g,C_hatm,C_e from one parent action",
            "passed": "false",
            "reason": "3007/2970/2788 stage the conditions but do not parent-sign the coefficients",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3267_2_arena_scale_lock",
            "gate": "source/readout scale s_k fixed or lower-bounded",
            "passed": "false",
            "reason": "3267 derives the scaled law but no numeric s_min rows exist",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3267_3_residual_budget",
            "gate": "omitted-channel epsilons sourced or theorem-zero",
            "passed": "false",
            "reason": "electron/delta-m/binding/readout/source-profile residuals remain explicit",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3267_4_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "source-coupling map is sharpened but local parent action and residual-sector silence remain unsigned",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3267_0",
            "verdict": "PARENT_DD_SIGNATURE_DERIVED_AS_CONTRACT_NOT_CURRENTLY_SIGNED",
            "what_moved": "The parent-source-map question is now C_g,C_hatm,C_e ownership plus s_k/epsilon_k rows, not a vague coupling worry.",
            "best_next": "try to derive the ordinary-matter low-energy coefficient vector C_g,C_hatm,C_e from the MTS parent matter/action grammar",
            "fallback_next": "source positive s_min and epsilon budgets and keep DD matrix as a bounded external-comparator branch",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3267_0_3268",
            "selected": "primary",
            "target_doc": "3268-Y5-R2FR-parent-low-energy-coefficient-vector-or-explicit-residual-basis-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3268_parent_low_energy_coefficient_vector_or_explicit_residual_basis.py",
            "objective": "Attempt to derive C_g,C_hatm,C_e from the parent matter action; if not derivable, instantiate the explicit residual/coefficient basis required by 3267.",
            "guardrail": "Do not call DD coefficients MTS-derived unless the parent operator pullback and coefficient normalization are signed.",
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
    sources = source_register()
    dd_rows = dd_evidence_rows()
    all_dd_found = all(row["line_number"] != "NO_MATCH" for row in dd_rows)
    all_claim_false = all(row["claim_allowed"] == "false" for row in claim_gate_rows())
    scale_rows_ok = all(row["valid_for_claim"] == "false" for row in scale_law_rows())
    theorem_rows_ok = any(row["proof_status"] == "CONDITIONAL_EXACT_CHAIN_RULE" for row in signature_theorem_rows())
    validations = [
        {
            "check_id": "VAL3267_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3267_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3267_2_DD_evidence_found",
            "check": "DD source-map evidence lines are found",
            "passed": bool_str(all_dd_found),
            "detail": ";".join(f"{row['evidence_id']}:{row['line_number']}" for row in dd_rows),
        },
        {
            "check_id": "VAL3267_3_outputs_parse",
            "check": "all 3267 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3267_4_signature_theorem_present",
            "check": "parent-to-DD conditional theorem is present",
            "passed": bool_str(theorem_rows_ok),
            "detail": "C_g,C_hatm,C_e -> D_hatm,D_e map recorded",
        },
        {
            "check_id": "VAL3267_5_scale_law_nonclaim",
            "check": "arena-scale and residual laws remain nonclaim",
            "passed": bool_str(scale_rows_ok),
            "detail": "all scale law rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3267_6_claim_gates_false",
            "check": "no 3267 claim gate allows WEP/local-GR promotion",
            "passed": bool_str(all_claim_false),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3267_7_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3267_8_overall",
            "check": "3267 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3267_8_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    dd = dd_evidence_rows()
    signature = signature_theorem_rows()
    audit = audit_rows()
    scale = scale_law_rows()
    projection = projection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3267 - Parent source-map signature for DD coordinates under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3267` derives the exact signature a future MTS parent action must satisfy to make the DD two-channel vector genuinely MTS-owned.
- The target is now sharp: one parent generator must supply arena-independent `C_g`, `C_hatm`, and `C_e`, giving `D_hatm=C_hatm-C_g` and `D_e=C_e`.
- The universal DD piece cancels in material differences, so the two-channel matrix from `3265/3266` is the right algebraic object once that parent signature is signed.
- Current MTS does **not** yet sign the parent coefficient vector; the honest failure normal form is `eta_k=s_k DeltaQ_k dot D + epsilon_k`.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## DD Source-Map Evidence
{md_table(dd, ["evidence_id", "line_number", "text_excerpt", "role", "source_url", "valid_for_claim"])}

## Parent-DD Signature Theorem
{md_table(signature, ["theorem_id", "statement", "math", "proof_status", "what_is_derived", "what_is_not_derived", "valid_for_claim"])}

## Current MTS Signature Audit
{md_table(audit, ["audit_id", "needed_signature", "current_evidence", "status", "source_path", "blocks_claim", "valid_for_claim"])}

## Arena Scale and Residual Law
{md_table(scale, ["law_id", "case", "formula", "Dhatm_bound", "De_bound", "interpretation", "valid_for_claim"])}

## Operator Projection Targets
{md_table(projection, ["projection_id", "parent_operator", "DD_coordinate", "pair_effect", "needed_parent_input", "current_status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register())
    write_csv(OUTPUTS["dd_evidence"], dd_evidence_rows())
    write_csv(OUTPUTS["signature"], signature_theorem_rows())
    write_csv(OUTPUTS["audit"], audit_rows())
    write_csv(OUTPUTS["scale_law"], scale_law_rows())
    write_csv(OUTPUTS["projection"], projection_rows())
    write_csv(OUTPUTS["gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
