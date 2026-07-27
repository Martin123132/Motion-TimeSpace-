from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3256-Y5-R2FR-material-EM-binding-projection-or-toy-charged-shell-smoke-input-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3256_SOURCE_REGISTER.csv",
    "projection": OUT / "P8_Y5_R2FR_3256_MATERIAL_EM_BINDING_PROJECTION.csv",
    "shell_match": OUT / "P8_Y5_R2FR_3256_COULOMB_SHELL_ENERGY_MATCH.csv",
    "toy_input": OUT / "P8_Y5_R2FR_3256_TOY_CHARGED_SHELL_SMOKE_INPUT_NONCLAIM.csv",
    "acceptance": OUT / "P8_Y5_R2FR_3256_MATERIAL_ACCEPTANCE_GATES.csv",
    "gram_update": OUT / "P8_Y5_R2FR_3256_GJ_EM_EM_MATERIAL_UPDATE.csv",
    "guards": OUT / "P8_Y5_R2FR_3256_NEUTRALITY_AND_DOUBLE_COUNT_GUARDS.csv",
    "gates": OUT / "P8_Y5_R2FR_3256_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3256_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3256_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3256_VALIDATION.csv",
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
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:240]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


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
            "SRC3256_3255_handoff",
            ROOT / "3255-Y5-R2FR-EM-Gram-row-input-pack-or-static-Coulomb-stress-envelope-under-AX1090.md",
            "3255 selected material EM binding projection or toy shell smoke input",
            ["NEXT3255_0_3256", "material binding", "G_J[EM,EM]"],
        ),
        (
            "SRC3256_3255_envelope",
            OUT / "P8_Y5_R2FR_3255_STATIC_COULOMB_STRESS_ENVELOPE.csv",
            "static Coulomb shell energy and Gram formula",
            ["CSE3255_2_L1_energy_shell", "CSE3255_3_L2_energy_current_shell"],
        ),
        (
            "SRC3256_3255_inputs",
            OUT / "P8_Y5_R2FR_3255_GJ_EM_EM_INPUT_REQUIREMENTS.csv",
            "Q_eff/cutoff/screening input requirements",
            ["IN3255_0_Q_eff", "IN3255_5_screening_neutrality"],
        ),
        (
            "SRC3256_1232_formula",
            OUT / "P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv",
            "component-fraction formula ledger",
            ["FORM1232_0_alloy_average", "FORM1232_2_delta_w_prediction"],
        ),
        (
            "SRC3256_1233_schema",
            OUT / "P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "component fraction acceptance schema",
            ["component_id", "fraction_value"],
        ),
        (
            "SRC3256_1328_routes",
            OUT / "P8_Y5_R10_1328_COMPONENT_SOURCE_ROUTE_MATRIX.csv",
            "source routes for EM_Coulomb material fraction",
            ["ROUTE1328_TA6V_EM_Coulomb", "ROUTE1328_PtRh10_EM_Coulomb"],
        ),
        (
            "SRC3256_1394_composition",
            OUT / "P8_Y5_R10_1394_BULK_MATERIAL_COMPOSITION_MAP.csv",
            "bulk material composition and binding interface",
            ["EM_Coulomb", "binding"],
        ),
        (
            "SRC3256_1395_binding_pack",
            OUT / "P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv",
            "binding sector beta source pack",
            ["binding", "EM"],
        ),
        (
            "SRC3256_1909_blockers",
            OUT / "P8_Y5_PARENT_QLOC_1909_MATERIAL_BINDING_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv",
            "Ti/Pt material binding projection blockers",
            ["EM_Coulomb", "binding"],
        ),
        (
            "SRC3256_1910_contract",
            OUT / "P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv",
            "exact mass-defect tensor contract",
            ["MDT1910_3_EM_Coulomb_binding", "DeltaR_AB"],
        ),
        (
            "SRC3256_3129_binding_pressure",
            ROOT / "3129-Y5-R2FR-Earth-source-calibration-smoke-and-binding-pressure-channel-under-AX1090.md",
            "binding pressure/source channel guard",
            ["Binding Pressure Channel", "Q_surface_binding"],
        ),
        (
            "SRC3256_3130_boundary_suppression",
            ROOT / "3130-Y5-R2FR-binding-boundary-suppression-or-profile-fill-under-AX1090.md",
            "boundary suppression/profile fork",
            ["surface/binding term", "rho_surf"],
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


def projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "MEP3256_0_material_energy_split",
            "object": "material EM binding energy",
            "formula": "E_EM,A := f_EM,A M_A c^2",
            "derivation": "use the existing component-fraction basis: EM/Coulomb is an internal material energy fraction, not an external net charge",
            "required_inputs": "f_EM,A;M_A;c;basis convention;source path",
            "current_status": "PROJECTION_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "MEP3256_1_alpha_response",
            "object": "material EM response",
            "formula": "gamma_EM,A := partial ln M_A / partial ln alpha_EM = (alpha_EM/M_A c^2) partial_alpha E_EM,A",
            "derivation": "if E_EM,A scales linearly with alpha in the chosen convention, gamma_EM,A approx f_EM,A; otherwise retain gamma_EM,A as sourced derivative",
            "required_inputs": "alpha-scaling convention or sourced derivative;no double-counting with nuclear surface/binding rows",
            "current_status": "CONDITIONAL_APPROX_OR_DERIVATIVE_ROW_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "MEP3256_2_differential_material_projection",
            "object": "Ti/Pt or body-pair EM projection",
            "formula": "DeltaR_AB^EM = gamma_EM,A - gamma_EM,B",
            "derivation": "inherits the 1910 response law DeltaR_AB^X=sum_c(f_Ac-f_Bc)gamma_cX when EM is the selected component",
            "required_inputs": "gamma_EM or f_EM rows for both bodies;material alloy/isotope convention;tau/source kernel",
            "current_status": "PAIR_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "MEP3256_3_no_external_neutrality_shortcut",
            "object": "neutral material handling",
            "formula": "Q_net,A=0 does not imply E_EM,A=0 or f_EM,A=0",
            "derivation": "internal Coulomb/binding stress remains a material response even if the external field is screened",
            "required_inputs": "material binding projection rather than external Q_eff alone",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": "false",
        },
    ]


def shell_match_rows() -> list[dict[str, Any]]:
    return [
        {
            "match_id": "CSM3256_0_energy_match",
            "object": "replace Q_eff by E_EM,A",
            "formula": "U_EM_shell = Q_eff^2/(8*pi*epsilon0)*(1/R_in-1/R_out) = E_EM,A",
            "result": "Q_eff^2 = 8*pi*epsilon0*E_EM,A/(R_in^-1-R_out^-1)",
            "derivation": "solve the 3255 shell energy formula for Q_eff^2",
            "valid_for_claim": "false",
        },
        {
            "match_id": "CSM3256_1_material_Gram_self",
            "object": "G_J[EM,EM]_A material shell surrogate",
            "formula": "G_J[EM,EM]_A = C_frame^2/(20*pi) * E_EM,A^2 * (R_in^-5-R_out^-5)/(R_in^-1-R_out^-1)^2",
            "result": "substitute CSM3256_0 into the 3255 Q_eff^4 shell Gram formula",
            "derivation": "epsilon0 cancels; the remaining dependence is material EM energy squared times shell-shape factor",
            "valid_for_claim": "false",
        },
        {
            "match_id": "CSM3256_2_fraction_form",
            "object": "G_J[EM,EM]_A in component fraction variables",
            "formula": "G_J[EM,EM]_A = C_frame^2/(20*pi) * (f_EM,A M_A c^2)^2 * K_shell(R_in,R_out)",
            "result": "K_shell := (R_in^-5-R_out^-5)/(R_in^-1-R_out^-1)^2",
            "derivation": "use E_EM,A=f_EM,A M_A c^2",
            "valid_for_claim": "false",
        },
        {
            "match_id": "CSM3256_3_distribution_generalization",
            "object": "non-shell material distribution",
            "formula": "G_J[EM,EM]_A = integral_A w_J u_EM,A(x)^2 dV_eobs",
            "result": "shell formula is a surrogate when u_EM,A(x) is replaced by an energy-matched shell profile",
            "derivation": "keeps the true target as a stress-current norm, not a forced spherical model",
            "valid_for_claim": "false",
        },
    ]


def toy_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "toy_id": "TOY3256_0_charged_shell_schema",
            "allowed_use": "code/schema smoke only",
            "material_id": "toy_charged_shell",
            "Q_eff": "MISSING_TOY_VALUE",
            "R_in": "MISSING_TOY_VALUE",
            "R_out": "MISSING_TOY_VALUE",
            "C_frame": "MISSING_TOY_VALUE",
            "formula_target": "G_J[EM,EM]_shell = C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5-R_out^-5)",
            "forbidden_use": "FORBIDDEN_FOR_CLAIM: real neutral matter, WEP, local-GR, Maxwell, or source-coupling evidence",
            "valid_for_claim": "false",
        },
        {
            "toy_id": "TOY3256_1_material_surrogate_schema",
            "allowed_use": "debug material projection algebra only",
            "material_id": "toy_material_EM_fraction",
            "Q_eff": "derived_from_E_EM_not_external_charge",
            "R_in": "MISSING_TOY_VALUE",
            "R_out": "MISSING_TOY_VALUE",
            "C_frame": "MISSING_TOY_VALUE",
            "formula_target": "G_J[EM,EM]_A = C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell",
            "forbidden_use": "FORBIDDEN_FOR_CLAIM: claim-grade material response unless f_EM,A, M_A, cutoffs, and source/readout kernel are sourced",
            "valid_for_claim": "false",
        },
    ]


def acceptance_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ACC3256_0_component_fraction",
            "required_object": "f_EM,A",
            "acceptance_rule": "must be finite numeric with uncertainty, basis convention, source path/URL/DOI, and extraction method matching the 1233 schema",
            "current_status": "MISSING_ACCEPTED_EM_FRACTION_ROWS",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ACC3256_1_material_mass",
            "required_object": "M_A or mass density profile",
            "acceptance_rule": "must match the same material body, isotope/alloy convention, and source-worldtube used by the tau/readout kernel",
            "current_status": "MISSING_SAME_ARENA_MATERIAL_MASS",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ACC3256_2_shape_cutoffs",
            "required_object": "R_in/R_out or u_EM(x)",
            "acceptance_rule": "either source a real EM energy-density distribution u_EM(x), or declare shell cutoffs as a toy/surrogate envelope",
            "current_status": "MISSING_SHAPE_PROFILE_OR_TOY_LABEL",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ACC3256_3_no_double_count",
            "required_object": "component basis map",
            "acceptance_rule": "EM_Coulomb fraction must not double-count nuclear surface/asymmetry, QCD/gluon binding, electron rest mass, or readout rows",
            "current_status": "BASIS_CONVENTION_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ACC3256_4_tau_source_kernel",
            "required_object": "tau/source/readout kernel",
            "acceptance_rule": "material Gram row cannot be inserted into WEP/PPN/local-GR until the same tau/e_obs/source-worldtube convention is declared",
            "current_status": "MISSING_TAU_SOURCE_KERNEL",
            "valid_for_claim": "false",
        },
    ]


def gram_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "GJU3256_0_Qeff_to_material",
            "target": "G_J[EM,EM]",
            "previous_symbolic_value": "C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5-R_out^-5)",
            "new_symbolic_value": "C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell(R_in,R_out)",
            "gain": "external charge parameter is replaced by internal material EM binding energy",
            "valid_for_claim": "false",
        },
        {
            "update_id": "GJU3256_1_material_pair",
            "target": "material-pair EM response",
            "previous_symbolic_value": "MISSING_SCREENING_OR_BINDING_SOURCE",
            "new_symbolic_value": "DeltaR_AB^EM = gamma_EM,A - gamma_EM,B, with gamma_EM,A approx f_EM,A only under sourced linear-alpha convention",
            "gain": "connects C_Tw EM row to WEP/source coupling material-response language",
            "valid_for_claim": "false",
        },
        {
            "update_id": "GJU3256_2_CTw_status",
            "target": "C_Tw matrix",
            "previous_symbolic_value": "first diagonal EM shell formula only",
            "new_symbolic_value": "first diagonal material-surrogate formula only; cross entries and accepted material rows still required",
            "gain": "makes next missing objects precise rather than broad",
            "valid_for_claim": "false",
        },
    ]


def guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "NG3256_0_external_neutrality",
            "statement": "External Q_net=0 does not imply internal EM_Coulomb binding fraction f_EM,A=0.",
            "blocks_bad_move": "using neutral material as an EM stress zero theorem",
            "required_safe_move": "use f_EM,A or gamma_EM,A from material binding/source rows",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "NG3256_1_shell_surrogate",
            "statement": "The shell energy match is a surrogate profile unless a real u_EM,A(x) distribution is sourced.",
            "blocks_bad_move": "treating R_in/R_out as physical without source-worldtube geometry",
            "required_safe_move": "label toy shell rows or source actual material/profile geometry",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "NG3256_2_double_count",
            "statement": "EM_Coulomb, nuclear surface/asymmetry, QCD binding, electron rest mass, and readout fractions must be basis-disjoint.",
            "blocks_bad_move": "counting the same binding energy in multiple source components",
            "required_safe_move": "declare basis convention and no-double-count map before score",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "NG3256_3_DD_external_comparator",
            "statement": "Damour-Donoghue style material charges may guide extraction but do not become parent MTS coefficients by copy-paste.",
            "blocks_bad_move": "claiming MTS source coupling from external phenomenological charges alone",
            "required_safe_move": "record external basis as comparator or derive parent basis map",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3256_0_energy_match_derivation",
            "claim": "Coulomb shell energy matching to material EM binding is algebraically derived",
            "gate_pass": "true",
            "reason": "CSM3256_0 through CSM3256_2 eliminate Q_eff in favour of E_EM,A=f_EM,A M_A c^2",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3256_1_material_projection_shape",
            "claim": "material projection formula is structurally ready",
            "gate_pass": "true",
            "reason": "MEP3256 rows define f_EM,A/gamma_EM,A and DeltaR_AB^EM gates",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3256_2_material_numeric",
            "claim": "material EM binding projection is numeric/source-backed",
            "gate_pass": "false",
            "reason": "accepted f_EM,A, M_A, profile/cutoffs, tau/source kernel, and basis map are missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3256_3_toy_smoke_claim",
            "claim": "toy charged shell is evidence for real material/source coupling",
            "gate_pass": "false",
            "reason": "toy rows are schema/debug only and explicitly forbidden for claims",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3256_4_local_GR_Newton_Maxwell",
            "claim": "local GR/Newton/Maxwell source branch is derived or bounded enough to claim",
            "gate_pass": "false",
            "reason": "only symbolic material projection is derived; numeric rows/cross terms/theorem-zero branch remain open",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3256_0_progress",
            "decision": "Use energy matching to turn Q_eff shell language into material EM binding language",
            "because": "this removes the most misleading toy parameter and connects the Gram row to real material fractions",
            "next_action": "source accepted f_EM,A rows or build an explicitly toy charged-shell smoke input",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3256_1_best_next",
            "decision": "Prioritize accepted EM_Coulomb fraction rows over numeric toy shell values",
            "because": "real local-GR/source coupling needs neutral material binding, not external net charge",
            "next_action": "fill 1233-style rows for TA6V/PtRh10 or an Earth/source material with basis/source/provenance",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3256_2_no_claim",
            "decision": "Keep all outputs private nonclaim",
            "because": "deriving the bridge equation is progress but not evidence until inputs are sourced",
            "next_action": "carry no-claim gates to 3257",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3256_0_3257",
            "selection": "selected_primary",
            "next_checkpoint": "3257-Y5-R2FR-first-accepted-EM-Coulomb-fraction-row-or-toy-shell-runner-dryrun-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3257_first_accepted_EM_Coulomb_fraction_row_or_toy_shell_runner_dryrun.py",
            "objective": "Either fill the first 1233-schema EM_Coulomb material fraction row with source/provenance, or run a clearly labelled toy-shell dry-run that cannot be mistaken for evidence.",
            "guardrail": "No local-GR/Newton/Maxwell/WEP claim from toy rows or unsourced material fractions.",
            "valid_for_claim": "false",
        }
    ]


def markdown_doc(
    sources: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    shell_match: list[dict[str, Any]],
    toy_input: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    gram_update: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3256 - Material EM binding projection or toy charged-shell smoke input under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.",
            "## Summary\n"
            "- `3256` converts the `3255` Coulomb-shell toy parameter into material EM-binding language.\n"
            "- Key bridge: match the shell energy to internal EM binding, `U_EM_shell = E_EM,A = f_EM,A M_A c^2`.\n"
            "- This gives `Q_eff^2 = 8*pi*epsilon0*E_EM,A/(R_in^-1-R_out^-1)` and removes fake external net-charge dependence.\n"
            "- The material surrogate self-entry is now `G_J[EM,EM]_A = C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell(R_in,R_out)`.\n"
            "- `K_shell=(R_in^-5-R_out^-5)/(R_in^-1-R_out^-1)^2`.\n"
            "- This is still nonclaim: accepted `f_EM,A`, material mass, profile/cutoffs, tau/source kernel, and no-double-count basis are missing.",
            "## Material EM Binding Projection",
            md_table(
                projection,
                ["projection_id", "object", "formula", "derivation", "required_inputs", "current_status", "valid_for_claim"],
            ),
            "## Coulomb Shell Energy Match",
            md_table(
                shell_match,
                ["match_id", "object", "formula", "result", "derivation", "valid_for_claim"],
            ),
            "## Toy Charged Shell Smoke Input",
            md_table(
                toy_input,
                ["toy_id", "allowed_use", "material_id", "Q_eff", "R_in", "R_out", "C_frame", "formula_target", "forbidden_use", "valid_for_claim"],
            ),
            "## Material Acceptance Gates",
            md_table(
                acceptance,
                ["gate_id", "required_object", "acceptance_rule", "current_status", "valid_for_claim"],
            ),
            "## GJ EM EM Material Update",
            md_table(
                gram_update,
                ["update_id", "target", "previous_symbolic_value", "new_symbolic_value", "gain", "valid_for_claim"],
            ),
            "## Neutrality And Double Count Guards",
            md_table(
                guards,
                ["guard_id", "statement", "blocks_bad_move", "required_safe_move", "valid_for_claim"],
            ),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decisions",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(
                next_target,
                ["next_id", "selection", "next_checkpoint", "next_script", "objective", "guardrail", "valid_for_claim"],
            ),
            "## Source Register",
            md_table(
                sources,
                ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"],
            ),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Working Verdict\n"
            "`3256` is a useful leap because the EM Gram row is no longer tied to an unphysical external `Q_eff` for neutral matter. It now has a bridge to the real material quantity: internal EM/Coulomb binding energy fraction. The next practical move is to fill one accepted `EM_Coulomb` fraction row, or run a toy shell only as a labelled code smoke.",
        ]
    ) + "\n"


def validation_rows(
    sources: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    shell_match: list[dict[str, Any]],
    toy_input: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    gram_update: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, requirement: str, evidence_text: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "passed": bool_str(passed),
                "requirement": requirement,
                "evidence": evidence_text,
            }
        )

    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" and row["evidence_hits"] != "NO_MATCH" for row in sources)
    add("VAL3256_0_sources_exist_parse_hit", source_ok, "every cited source exists, parses, and has evidence hits", str(source_ok))

    outputs_parse = all(csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")
    add("VAL3256_1_output_csvs_parse", outputs_parse, "all 3256 output CSVs parse before validation write", str(outputs_parse))

    energy_split = any(row["projection_id"] == "MEP3256_0_material_energy_split" and "f_EM,A" in row["formula"] for row in projection)
    add("VAL3256_2_material_energy_split", energy_split, "material EM binding energy split exists", str(energy_split))

    q_eliminated = any(row["match_id"] == "CSM3256_0_energy_match" and "Q_eff^2" in row["result"] for row in shell_match)
    material_gj = any(row["match_id"] == "CSM3256_2_fraction_form" and "f_EM,A M_A c^2" in row["formula"] for row in shell_match)
    add("VAL3256_3_shell_match", q_eliminated and material_gj, "Q_eff elimination and material GJ formula are present", f"q={q_eliminated} material={material_gj}")

    toy_nonclaim = all(row["valid_for_claim"] == "false" and "forbidden" in row["forbidden_use"].lower() for row in toy_input)
    add("VAL3256_4_toy_quarantined", toy_nonclaim, "toy shell rows are nonclaim and forbidden for evidence", str(toy_nonclaim))

    acceptance_missing = all("MISSING_" in row["current_status"] or "REQUIRED" in row["current_status"] for row in acceptance)
    add("VAL3256_5_acceptance_missing", acceptance_missing, "acceptance gates preserve missing/required status", str(acceptance_missing))

    gram_updated = any(row["update_id"] == "GJU3256_0_Qeff_to_material" and "f_EM,A" in row["new_symbolic_value"] for row in gram_update)
    add("VAL3256_6_gram_material_update", gram_updated, "GJ EM self-entry updated to material binding variables", str(gram_updated))

    guards_present = any("Q_net=0" in row["statement"] for row in guards) and any("double-count" in row["required_safe_move"] or "basis" in row["required_safe_move"] for row in guards)
    add("VAL3256_7_guards_present", guards_present, "neutrality and double-count guards are present", str(guards_present))

    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [projection, shell_match, toy_input, acceptance, gram_update, guards]
        for row in collection
    )
    claims_blocked = all(row["claim_allowed"] == "false" for row in gates) and any(row["claim_gate_id"] == "CG3256_4_local_GR_Newton_Maxwell" and row["gate_pass"] == "false" for row in gates)
    add("VAL3256_8_nonclaim_claims_blocked", all_nonclaim and claims_blocked, "all rows nonclaim and local-GR/Newton/Maxwell gate blocked", f"nonclaim={all_nonclaim} claims={claims_blocked}")

    output_scope_ok = all(str(path).startswith(str(ROOT)) for path in [DOC, *OUTPUTS.values()])
    add("VAL3256_9_output_scope", output_scope_ok, "all generated files stay in post-checkpoint-work", str(output_scope_ok))

    formalization_3256_files = []
    if FW.exists():
        formalization_3256_files = [path for path in FW.rglob("*3256*") if path.is_file()]
    add("VAL3256_10_formalization_untouched", not formalization_3256_files, "no 3256 files are written under formalization-workbench", f"file_count={len(formalization_3256_files)}")

    add("VAL3256_11_next_target", bool(next_rows()), "3257 next target is selected", str(bool(next_rows())))

    overall = all(row["passed"] == "true" for row in rows)
    add("VAL3256_OVERALL", overall, "3256 validation overall", "all required validation rows passed" if overall else "one or more validation rows failed")
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    projection = projection_rows()
    shell_match = shell_match_rows()
    toy_input = toy_input_rows()
    acceptance = acceptance_rows()
    gram_update = gram_update_rows()
    guards = guard_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["projection"], projection)
    write_csv(OUTPUTS["shell_match"], shell_match)
    write_csv(OUTPUTS["toy_input"], toy_input)
    write_csv(OUTPUTS["acceptance"], acceptance)
    write_csv(OUTPUTS["gram_update"], gram_update)
    write_csv(OUTPUTS["guards"], guards)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    validation = validation_rows(sources, projection, shell_match, toy_input, acceptance, gram_update, guards, gates)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        markdown_doc(sources, projection, shell_match, toy_input, acceptance, gram_update, guards, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3256_OVERALL")
    print(f"{overall['validation_id']}={overall['passed']}")
    print(DOC)
    for name, path in OUTPUTS.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
