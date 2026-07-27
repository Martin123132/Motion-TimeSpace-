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

DOC = ROOT / "3255-Y5-R2FR-EM-Gram-row-input-pack-or-static-Coulomb-stress-envelope-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3255_SOURCE_REGISTER.csv",
    "arena": OUT / "P8_Y5_R2FR_3255_EM_GRAM_ARENA_NORM_UNIT_PACK.csv",
    "coulomb": OUT / "P8_Y5_R2FR_3255_STATIC_COULOMB_STRESS_ENVELOPE.csv",
    "input_pack": OUT / "P8_Y5_R2FR_3255_GJ_EM_EM_INPUT_REQUIREMENTS.csv",
    "gram_update": OUT / "P8_Y5_R2FR_3255_GJ_EM_EM_SYMBOLIC_UPDATE.csv",
    "poynting_guard": OUT / "P8_Y5_R2FR_3255_POYNTING_ZERO_STRESS_NONZERO_GUARD.csv",
    "gates": OUT / "P8_Y5_R2FR_3255_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3255_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3255_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3255_VALIDATION.csv",
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
            "SRC3255_3254_handoff",
            ROOT / "3254-Y5-R2FR-first-component-current-Gram-row-or-parent-signature-clause-lock-under-AX1090.md",
            "3254 selects static Coulomb/EM envelope as next target",
            ["NEXT3254_0_3255", "G_J[EM,EM]", "Coulomb"],
        ),
        (
            "SRC3255_3254_gram",
            OUT / "P8_Y5_R2FR_3254_EM_COMPONENT_CURRENT_GRAM_ROW.csv",
            "EM Gram self/cross row contract",
            ["GJ3254_EM_EM_SELF", "G_J[EM,EM]"],
        ),
        (
            "SRC3255_3254_bounds",
            OUT / "P8_Y5_R2FR_3254_EM_CURRENT_NORM_BOUND_ROWS.csv",
            "EM norm bounds and static Coulomb guard",
            ["EMB3254_0_L1_energy_current_bound", "EMB3254_3_static_coulomb_warning"],
        ),
        (
            "SRC3255_3116_doc",
            ROOT / "3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md",
            "public Hodge/Maxwell stress route",
            ["Hilbert Stress Derivation", "Poynting Vector Readout"],
        ),
        (
            "SRC3255_3116_lock_csv",
            OUT / "P8_Y5_R2FR_3116_PUBLIC_HODGE_MAXWELL_STRESS_LOCK.csv",
            "Maxwell action to Hilbert stress and Poynting readout rows",
            ["EMH3116_1", "EMH3116_2"],
        ),
        (
            "SRC3255_3142_doc",
            ROOT / "3142-Y5-R2FR-em-poynting-qbasic-sector-under-AX1090.md",
            "q-basic Maxwell/Poynting conditional sector",
            ["EM/Poynting q-basic sector theorem", "Hilbert EM stress tensor"],
        ),
        (
            "SRC3255_3200_doc",
            ROOT / "3200-Y5-R2FR-stress-flux-rank-coefficient-extractor-or-Poynting-residual-bound-runner-under-AX1090.md",
            "quiet static Poynting zero versus stress nonzero distinction",
            ["electrostatic_bound_field", "does **not** zero full EM stress-energy"],
        ),
        (
            "SRC3255_3234_doc",
            ROOT / "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md",
            "Poynting functional and no-F2 shortcut guard",
            ["Phi_Poynting", "F^2=0 does not imply"],
        ),
        (
            "SRC3255_3246_doc",
            ROOT / "3246-Y5-R2FR-first-Poynting-Jtot-score-row-or-boundary-frame-source-acquisition-under-AX1090.md",
            "Poynting regime classifier",
            ["REG3246_1_electrostatic", "EM stress/energy"],
        ),
        (
            "SRC3255_3250_identity",
            OUT / "P8_Y5_R2FR_3250_EM_STRESS_PROJECTION_AND_FLUX_NORM_IDENTITY.csv",
            "Maxwell stress projection and flux norm identities",
            ["EMF3250_0_projection", "EMF3250_1_boundary_L1_bound"],
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


def arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ARENA3255_0_static_coulomb_shell",
            "choice": "A_ext shell around source worldtube",
            "formal_definition": "A_ext(R_in,R_out) := {x on a static observed slice : R_in <= r_eobs(x,W_source) <= R_out}",
            "why_this_choice": "removes the Coulomb singularity with R_in>0 and keeps finite support with R_out<infty",
            "required_inputs": "W_source;observed static slice;r_eobs;R_in;R_out;orientation;regular shell",
            "current_status": "SYMBOLIC_ARENA_CONTRACT_READY",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3255_1_current_norm",
            "choice": "L2 energy-current norm",
            "formal_definition": "G_J[EM,EM] := integral_Aext u_EM(r)^2 dV_eobs for tau=unit static observer and J_EM=tau-energy-current",
            "why_this_choice": "matches the 3253 Gram/eigenvalue requirement while giving an analytic Coulomb shell integral",
            "required_inputs": "tau unit normalization;dV_eobs;J norm convention;frame correction if not locally inertial",
            "current_status": "NORM_CONVENTION_SELECTED_FOR_ENVELOPE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3255_2_unit_system",
            "choice": "SI shell formula with natural-unit translation deferred",
            "formal_definition": "E(r)=Q_eff/(4*pi*epsilon0*r^2), B=0, u_EM=epsilon0 E^2/2",
            "why_this_choice": "keeps dimensions visible and prevents hidden alpha/epsilon0 unit drift",
            "required_inputs": "epsilon0 or declared natural-unit replacement;kappa_EM;Q_eff units",
            "current_status": "SI_SYMBOLIC_FORMULA_SELECTED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3255_3_scope_guard",
            "choice": "envelope not material model",
            "formal_definition": "Q_eff is an effective unscreened or component charge envelope; neutral materials require internal Coulomb/binding source maps, not a net-charge shortcut",
            "why_this_choice": "keeps the formula useful without pretending bulk neutral matter has a simple external Coulomb field",
            "required_inputs": "screening/neutralization map or material EM binding fraction before any real body score",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": "false",
        },
    ]


def coulomb_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "CSE3255_0_field_profile",
            "quantity": "static Coulomb E-field",
            "formula": "E(r)=Q_eff/(4*pi*epsilon0*r^2), B(r)=0, R_in<=r<=R_out",
            "derivation": "spherical static Coulomb envelope on the observed shell; not a claim that real neutral material has this unscreened field",
            "required_inputs": "Q_eff;epsilon0;R_in;R_out;static observed frame",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CSE3255_1_energy_density",
            "quantity": "u_EM(r)",
            "formula": "u_EM(r)=epsilon0 E^2/2 = Q_eff^2/(32*pi^2*epsilon0*r^4)",
            "derivation": "standard Maxwell energy density for B=0",
            "required_inputs": "same unit convention as CSE3255_0",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CSE3255_2_L1_energy_shell",
            "quantity": "||J_EM||_L1 shell envelope",
            "formula": "U_EM_shell = integral u_EM dV = Q_eff^2/(8*pi*epsilon0)*(1/R_in - 1/R_out)",
            "derivation": "integrate u_EM(r)*4*pi*r^2 dr over [R_in,R_out]",
            "required_inputs": "Q_eff;epsilon0;R_in>0;R_out>R_in",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CSE3255_3_L2_energy_current_shell",
            "quantity": "G_J[EM,EM] shell envelope",
            "formula": "G_J[EM,EM]_shell = integral u_EM^2 dV = Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5)",
            "derivation": "integrate [Q_eff^2/(32*pi^2*epsilon0*r^4)]^2 * 4*pi*r^2 dr",
            "required_inputs": "same current norm;Q_eff;epsilon0;R_in>0;R_out>R_in",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CSE3255_4_L2_norm",
            "quantity": "||J_EM||_L2 shell envelope",
            "formula": "||J_EM||_L2 <= C_frame * |Q_eff|^2/(sqrt(1280)*pi^(3/2)*epsilon0)*sqrt(R_in^-5 - R_out^-5)",
            "derivation": "square root of CSE3255_3 with a frame/normalization safety factor C_frame",
            "required_inputs": "C_frame from tau/e_obs/current norm;do not set C_frame=1 unless local inertial/unit tau is sourced",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "CSE3255_5_poynting_zero_not_stress_zero",
            "quantity": "Poynting readout",
            "formula": "S_EM=(1/mu0)E x B = 0 for B=0, but u_EM and G_J[EM,EM]_shell are nonzero for Q_eff != 0",
            "derivation": "static electrostatic branch separates flux silence from stress-current silence",
            "required_inputs": "none beyond CSE3255_0; guardrail row",
            "valid_for_claim": "false",
        },
    ]


def input_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "IN3255_0_Q_eff",
            "input": "Q_eff",
            "definition": "effective charge or EM binding/source envelope feeding the Coulomb shell",
            "needed_for": "CSE3255_0 through CSE3255_4",
            "current_value": "MISSING_Q_EFF_OR_MATERIAL_BINDING_MAP",
            "source_requirement": "source profile, material EM binding model, or explicit neutralization/screening map",
            "valid_for_claim": "false",
        },
        {
            "input_id": "IN3255_1_R_in",
            "input": "R_in",
            "definition": "inner cutoff radius of static Coulomb shell",
            "needed_for": "finite U_EM_shell and finite G_J[EM,EM]",
            "current_value": "MISSING_R_IN_POSITIVE",
            "source_requirement": "source worldtube radius, material cutoff, or q-basic collar inner radius",
            "valid_for_claim": "false",
        },
        {
            "input_id": "IN3255_2_R_out",
            "input": "R_out",
            "definition": "outer cutoff radius of static Coulomb shell",
            "needed_for": "finite arena support and score comparability",
            "current_value": "MISSING_R_OUT_GT_R_IN",
            "source_requirement": "arena/collar outer radius or decay/truncation rule",
            "valid_for_claim": "false",
        },
        {
            "input_id": "IN3255_3_epsilon0_or_unit_lock",
            "input": "epsilon0/kappa_EM/unit convention",
            "definition": "unit and Maxwell normalization used by the observed EM stress",
            "needed_for": "dimensionally meaningful CSE3255 formulas",
            "current_value": "MISSING_UNIT_LOCK",
            "source_requirement": "parent EM owner theorem or explicit SI/natural-unit scoring convention",
            "valid_for_claim": "false",
        },
        {
            "input_id": "IN3255_4_tau_eobs",
            "input": "tau and e_obs frame",
            "definition": "unit static observer and observed coframe defining J_EM and dV",
            "needed_for": "C_frame and current norm",
            "current_value": "MISSING_TAU_EOBS_ARENA_LOCK",
            "source_requirement": "same-frame package from 3250 signed or specified as finite arena convention",
            "valid_for_claim": "false",
        },
        {
            "input_id": "IN3255_5_screening_neutrality",
            "input": "screening/neutralization/material map",
            "definition": "map from real material EM binding to the idealized Q_eff shell envelope",
            "needed_for": "applying the envelope to WEP/local matter rather than a toy charged shell",
            "current_value": "MISSING_SCREENING_OR_BINDING_SOURCE",
            "source_requirement": "material composition/binding model or no-claim toy-envelope label",
            "valid_for_claim": "false",
        },
    ]


def gram_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "GJU3255_0_symbolic_self_entry",
            "target": "G_J[EM,EM]",
            "previous_value": "MISSING_GJ_EM_EM_NUMERIC_VALUE",
            "new_symbolic_value": "G_J[EM,EM]_shell = C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5)",
            "new_status": "SYMBOLIC_STATIC_COULOMB_ENVELOPE_READY_NONCLAIM",
            "claim_effect": "not numeric; not valid for real neutral material without input pack",
            "valid_for_claim": "false",
        },
        {
            "update_id": "GJU3255_1_CTw_diagonal_feed",
            "target": "C_Tw diagonal upper bound",
            "previous_value": "C_Tw_upper^2 receives + ||J_EM||_J^2",
            "new_symbolic_value": "C_Tw_upper^2 receives + C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5)",
            "new_status": "FIRST_COMPONENT_DIAGONAL_FORMULA_FILLED",
            "claim_effect": "still requires all other component rows or exact Gram eigenvalue matrix for C_Tw",
            "valid_for_claim": "false",
        },
        {
            "update_id": "GJU3255_2_cross_entries_still_open",
            "target": "G_J[EM,d]",
            "previous_value": "MISSING_GJ_EM_D_CROSS_VALUES",
            "new_symbolic_value": "unchanged; need component stress overlap or orthogonality theorem",
            "new_status": "CROSS_TERMS_REMAIN_REQUIRED",
            "claim_effect": "prevents pretending diagonal shell alone is full C_Tw",
            "valid_for_claim": "false",
        },
    ]


def poynting_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "PZG3255_0_static_flux_zero",
            "statement": "For the static Coulomb envelope B=0, S_EM=(1/mu0)E x B=0 and normal Poynting flux vanishes.",
            "allowed_inference": "boundary Poynting flux component can be zero in this idealized static branch",
            "forbidden_inference": "do not infer T_EM=0, u_EM=0, J_EM=0, or G_J[EM,EM]=0",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "PZG3255_1_static_stress_nonzero",
            "statement": "For Q_eff != 0 and finite R_in<R_out, u_EM(r)=Q_eff^2/(32*pi^2*epsilon0*r^4)>0 and G_J[EM,EM]_shell>0.",
            "allowed_inference": "static Coulomb stress can contribute to source/current Gram rows",
            "forbidden_inference": "do not erase EM/Coulomb source coupling by citing quiet/static Poynting alone",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "PZG3255_2_neutral_material_warning",
            "statement": "For neutral matter, Q_eff may be zero externally while internal Coulomb/binding stress remains material-model dependent.",
            "allowed_inference": "external shell formula is an envelope/toy source until mapped to material binding",
            "forbidden_inference": "do not use Q_eff=0 external neutrality as proof that EM binding stress vanishes",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3255_0_static_envelope_derived",
            "claim": "static Coulomb shell envelope formulas are derived",
            "gate_pass": "true",
            "reason": "CSE3255 rows integrate standard Maxwell energy density over R_in<=r<=R_out",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3255_1_GJ_symbolic",
            "claim": "G_J[EM,EM] has a symbolic shell formula",
            "gate_pass": "true",
            "reason": "GJU3255_0 supplies the symbolic diagonal self-entry",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3255_2_GJ_numeric",
            "claim": "G_J[EM,EM] is numeric/source-backed",
            "gate_pass": "false",
            "reason": "Q_eff, R_in, R_out, unit lock, tau/e_obs, and screening/material map are missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3255_3_real_material",
            "claim": "static shell formula is a real material EM binding model",
            "gate_pass": "false",
            "reason": "neutrality/screening/internal binding map has not been supplied",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3255_4_local_GR_Newton_Maxwell",
            "claim": "local GR/Newton/Maxwell source branch is derived or bounded enough to claim",
            "gate_pass": "false",
            "reason": "only one symbolic diagonal component is filled; numeric matrix/cross terms/source coupling theorem remain open",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3255_0_progress",
            "decision": "Promote G_J[EM,EM] from missing to symbolic Coulomb-shell envelope",
            "because": "this is an actual calculable formula with cutoff dependence, not another target ledger",
            "next_action": "supply Q_eff/R_in/R_out/unit/tau/e_obs or derive the material binding map",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3255_1_no_overclaim",
            "decision": "Keep the shell formula nonclaim",
            "because": "real neutral matter needs screening/internal Coulomb binding, and C_Tw still needs cross terms or an orthogonality theorem",
            "next_action": "build a material EM binding projection or choose a toy charged-shell smoke input explicitly",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3255_2_best_next",
            "decision": "Attack material binding projection before trying numeric C_Tw",
            "because": "without mapping EM binding in neutral matter, Q_eff is just a toy shell parameter",
            "next_action": "derive/source f_EM,A and convert Coulomb shell envelope into component stress-current rows for real material classes",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3255_0_3256",
            "selection": "selected_primary",
            "next_checkpoint": "3256-Y5-R2FR-material-EM-binding-projection-or-toy-charged-shell-smoke-input-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3256_material_EM_binding_projection_or_toy_charged_shell_smoke_input.py",
            "objective": "Either derive/source the material EM binding projection f_EM,A for neutral matter, or create an explicitly labelled toy charged-shell input row for the symbolic G_J[EM,EM] envelope.",
            "guardrail": "Do not treat external neutrality or zero Poynting flux as zero EM stress; do not claim local GR/Newton/Maxwell pass.",
            "valid_for_claim": "false",
        }
    ]


def markdown_doc(
    sources: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    coulomb: list[dict[str, Any]],
    input_pack: list[dict[str, Any]],
    gram_update: list[dict[str, Any]],
    poynting_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3255 - EM Gram row input pack or static Coulomb stress envelope under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material binding, or public source-coupling success.",
            "## Summary\n"
            "- `3255` fills the first symbolic diagonal Gram formula for the EM/Coulomb source component.\n"
            "- Arena choice: a static observed Coulomb shell `A_ext(R_in,R_out)` with `R_in>0` and `R_out>R_in`.\n"
            "- For `E(r)=Q_eff/(4*pi*epsilon0*r^2)` and `B=0`, the energy density is `u_EM=Q_eff^2/(32*pi^2*epsilon0*r^4)`.\n"
            "- The shell energy is `U_EM=Q_eff^2/(8*pi*epsilon0)*(1/R_in-1/R_out)`.\n"
            "- The diagonal Gram self-entry is now symbolic: `G_J[EM,EM]_shell=C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5-R_out^-5)`.\n"
            "- This is not a real material claim yet: `Q_eff`, cutoffs, unit lock, tau/e_obs, and screening/internal binding projection are still required.",
            "## Arena Norm Unit Pack",
            md_table(
                arena,
                ["arena_id", "choice", "formal_definition", "why_this_choice", "required_inputs", "current_status", "valid_for_claim"],
            ),
            "## Static Coulomb Stress Envelope",
            md_table(
                coulomb,
                ["derivation_id", "quantity", "formula", "derivation", "required_inputs", "valid_for_claim"],
            ),
            "## GJ EM EM Input Requirements",
            md_table(
                input_pack,
                ["input_id", "input", "definition", "needed_for", "current_value", "source_requirement", "valid_for_claim"],
            ),
            "## GJ EM EM Symbolic Update",
            md_table(
                gram_update,
                ["update_id", "target", "previous_value", "new_symbolic_value", "new_status", "claim_effect", "valid_for_claim"],
            ),
            "## Poynting Zero Stress Nonzero Guard",
            md_table(
                poynting_guard,
                ["guard_id", "statement", "allowed_inference", "forbidden_inference", "valid_for_claim"],
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
            "`3255` is a genuine calculation step. `G_J[EM,EM]` is no longer just a missing entry: it has a symbolic Coulomb-shell envelope with explicit cutoff dependence. The next risk is physical interpretation, not algebra: a real neutral material needs an EM binding/screening projection before this can be used as evidence.",
        ]
    ) + "\n"


def validation_rows(
    sources: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    coulomb: list[dict[str, Any]],
    input_pack: list[dict[str, Any]],
    gram_update: list[dict[str, Any]],
    poynting_guard: list[dict[str, Any]],
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
    add("VAL3255_0_sources_exist_parse_hit", source_ok, "every cited source exists, parses, and has evidence hits", str(source_ok))

    outputs_parse = all(csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")
    add("VAL3255_1_output_csvs_parse", outputs_parse, "all 3255 output CSVs parse before validation write", str(outputs_parse))

    arena_shell = any(row["arena_id"] == "ARENA3255_0_static_coulomb_shell" and "R_in" in row["formal_definition"] for row in arena)
    add("VAL3255_2_arena_shell", arena_shell, "static Coulomb shell arena is declared", str(arena_shell))

    l1_formula = any(row["derivation_id"] == "CSE3255_2_L1_energy_shell" and "1/R_in - 1/R_out" in row["formula"] for row in coulomb)
    l2_formula = any(row["derivation_id"] == "CSE3255_3_L2_energy_current_shell" and "1280*pi^3" in row["formula"] and "R_in^-5" in row["formula"] for row in coulomb)
    add("VAL3255_3_coulomb_integrals", l1_formula and l2_formula, "L1 and L2 Coulomb shell integrals are present", f"L1={l1_formula} L2={l2_formula}")

    gram_symbolic = any(row["update_id"] == "GJU3255_0_symbolic_self_entry" and "Q_eff^4" in row["new_symbolic_value"] for row in gram_update)
    add("VAL3255_4_symbolic_gj_update", gram_symbolic, "G_J[EM,EM] symbolic update exists", str(gram_symbolic))

    inputs_missing = all("MISSING_" in row["current_value"] for row in input_pack)
    inputs_include_cutoffs = {"IN3255_0_Q_eff", "IN3255_1_R_in", "IN3255_2_R_out"}.issubset({row["input_id"] for row in input_pack})
    add("VAL3255_5_input_pack_missing", inputs_missing and inputs_include_cutoffs, "input pack includes Q_eff/R_in/R_out and keeps missing markers", f"missing={inputs_missing} cutoffs={inputs_include_cutoffs}")

    poynting_guard_ok = any("forbidden_inference" in row and "G_J[EM,EM]=0" in row["forbidden_inference"] for row in poynting_guard)
    stress_positive_ok = any("G_J[EM,EM]_shell>0" in row["statement"] for row in poynting_guard)
    add("VAL3255_6_poynting_guard", poynting_guard_ok and stress_positive_ok, "Poynting zero does not erase EM stress guard is present", f"zero_guard={poynting_guard_ok} positive={stress_positive_ok}")

    all_nonclaim = all(row.get("valid_for_claim") == "false" for collection in [arena, coulomb, input_pack, gram_update, poynting_guard] for row in collection)
    claims_blocked = all(row["claim_allowed"] == "false" for row in gates) and any(row["claim_gate_id"] == "CG3255_4_local_GR_Newton_Maxwell" and row["gate_pass"] == "false" for row in gates)
    add("VAL3255_7_nonclaim_claims_blocked", all_nonclaim and claims_blocked, "all rows nonclaim and local-GR/Newton/Maxwell gate blocked", f"nonclaim={all_nonclaim} claims={claims_blocked}")

    output_scope_ok = all(str(path).startswith(str(ROOT)) for path in [DOC, *OUTPUTS.values()])
    add("VAL3255_8_output_scope", output_scope_ok, "all generated files stay in post-checkpoint-work", str(output_scope_ok))

    formalization_3255_files = []
    if FW.exists():
        formalization_3255_files = [path for path in FW.rglob("*3255*") if path.is_file()]
    add("VAL3255_9_formalization_untouched", not formalization_3255_files, "no 3255 files are written under formalization-workbench", f"file_count={len(formalization_3255_files)}")

    add("VAL3255_10_next_target", bool(next_rows()), "3256 next target is selected", str(bool(next_rows())))

    overall = all(row["passed"] == "true" for row in rows)
    add("VAL3255_OVERALL", overall, "3255 validation overall", "all required validation rows passed" if overall else "one or more validation rows failed")
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    arena = arena_rows()
    coulomb = coulomb_rows()
    input_pack = input_pack_rows()
    gram_update = gram_update_rows()
    poynting_guard = poynting_guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["coulomb"], coulomb)
    write_csv(OUTPUTS["input_pack"], input_pack)
    write_csv(OUTPUTS["gram_update"], gram_update)
    write_csv(OUTPUTS["poynting_guard"], poynting_guard)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    validation = validation_rows(sources, arena, coulomb, input_pack, gram_update, poynting_guard, gates)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        markdown_doc(sources, arena, coulomb, input_pack, gram_update, poynting_guard, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3255_OVERALL")
    print(f"{overall['validation_id']}={overall['passed']}")
    print(DOC)
    for name, path in OUTPUTS.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
