import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3798"
BRANCH = "MTS_R2FR_Y5_MINIMAL_BPERP_HPERP_PROFILE_ANSATZ_OR_PARENT_ZERO_3798"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3798-Y5-R2FR-minimal-Bperp-Hperp-profile-ansatz-or-parent-zero.md"

P_3789 = PCW / "3789-Y5-R2FR-BQ-first-norm-and-patch-convention-or-field-map-fill.md"
P_3793 = PCW / "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md"
P_3796 = PCW / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md"
P_3797 = PCW / "3797-Y5-R2FR-first-Bperp-Hperp-profile-source-acquisition-R10-clock.md"
P_3504 = PCW / "3504-Y5-R2FR-observed-Hodge-flow-rule-from-q-eobs-or-DeltaHodge-bound.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3797_R10 = RESIDUALS / "P8_Y5_R2FR_3797_R10_BOUND_JOIN_LEDGER.csv"
C_3797_CLOCK = RESIDUALS / "P8_Y5_R2FR_3797_CLOCK_JOIN_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3798_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3798_LOCAL_HODGE_PROFILE_THEOREM.csv",
    "bound_rows": RESIDUALS / "P8_Y5_R2FR_3798_BPERP_FROM_HPERP_BOUND_ROWS.csv",
    "ansatz": RESIDUALS / "P8_Y5_R2FR_3798_MINIMAL_PROFILE_ANSATZ_ROWS.csv",
    "join_update": RESIDUALS / "P8_Y5_R2FR_3798_R10_CLOCK_NUMERATOR_UPDATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3798_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3798_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3798_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3798_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3798_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3798_0_3797_handoff",
        "path": P_3797,
        "needle": "build the smallest honest `Bperp/Hperp` profile",
        "role": "3797 selected minimal Bperp/Hperp profile or zero theorem",
    },
    {
        "source_id": "SRC3798_1_3793_decomposition",
        "path": P_3793,
        "needle": "B_Q=q_obs^*Bbar_Q+dchi+B_perp",
        "role": "Bperp and Hperp exact definitions",
    },
    {
        "source_id": "SRC3798_2_3789_Ugood",
        "path": P_3789,
        "needle": "H1(U)=0",
        "role": "contractible patch, norm, and local chart guard",
    },
    {
        "source_id": "SRC3798_3_3796_shear_gate",
        "path": P_3796,
        "needle": "rank(dY_Q)=4",
        "role": "Q-shear selector still unsigned",
    },
    {
        "source_id": "SRC3798_4_3504_hodge_context",
        "path": P_3504,
        "needle": "Hodge uniqueness",
        "role": "observed Hodge/coframe context and no-overclaim guard",
    },
    {
        "source_id": "SRC3798_5_3797_R10_join",
        "path": C_3797_R10,
        "needle": "R10J3797_0_bound_curve_candidate",
        "role": "R10 bound-side join waiting for numerator",
    },
    {
        "source_id": "SRC3798_6_3797_clock_join",
        "path": C_3797_CLOCK,
        "needle": "CLKJ3797_0_best_clock_product",
        "role": "clock bound-side join waiting for numerator/readout",
    },
    {
        "source_id": "SRC3798_7_spine",
        "path": P_SPINE,
        "needle": "3798-Y5-R2FR-minimal-Bperp-Hperp-profile-ansatz-or-parent-zero.md",
        "role": "live spine handoff",
    },
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path):
    try:
        load_csv(path)
        return True
    except Exception:
        return False


def bool_text(value):
    return "true" if value else "false"


def source_register(timestamp):
    rows = []
    for spec in SOURCE_SPECS:
        exists = spec["path"].exists()
        needle_found = False
        if exists:
            needle_found = spec["needle"] in read_text(spec["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(spec["path"]),
                "exists": bool_text(exists),
                "needle": spec["needle"],
                "needle_found": bool_text(needle_found),
                "role": spec["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    specs = [
        (
            "LHP3798_0_gauge_split",
            "local one-form residue split",
            "On U_good, B_perp is a one-form residue after subtracting q_obs^*Bbar_Q and dchi; P_A removes exact local gauge pieces.",
            "EXACT_FROM_3793_PLUS_3789",
            "after P_A, only coexact plus boundary/harmonic pieces can matter locally",
            "needs chosen U_good and boundary condition",
        ),
        (
            "LHP3798_1_hodge_poincare",
            "contractible-patch Hodge/Poincare reduction",
            "For H1(U_good)=0 with relative/compact support boundary condition, B_perp=dphi+B_T and Hperp=dB_T; the harmonic one-form part is absent.",
            "MATHEMATICAL_LOCAL_THEOREM",
            "Bperp is not an independent profile once Hperp and boundary data are fixed",
            "boundary/support condition and H1(U)=0 must be source-specified per arena",
        ),
        (
            "LHP3798_2_green_reconstruction",
            "minimal Green-operator primitive",
            "Choose Coulomb representative delta_U B_T=0. Then B_T=delta_U G_U Hperp plus boundary terms, where G_U is the local Hodge Green operator.",
            "EXACT_CONDITIONAL_RECONSTRUCTION",
            "minimal profile ansatz can be Hperp-first rather than arbitrary Bperp-first",
            "requires local metric/coframe, boundary condition, and domain constant",
        ),
        (
            "LHP3798_3_norm_bound",
            "Bperp-from-Hperp amplitude bound",
            "||P_A B_perp||_A/A_ref <= Lambda_U ||Hperp||_F/F_ref + eta_boundary + eta_harmonic, with Lambda_U=C_U F_ref/A_ref.",
            "DERIVED_BOUND_FORM",
            "Bperp_norm_over_Aref is reduced to Hperp_norm_over_Fref plus named leakage terms",
            "C_U, A_ref, F_ref, eta_boundary, eta_harmonic missing for claim",
        ),
        (
            "LHP3798_4_zero_theorem",
            "local Bperp zero from Hperp zero",
            "If Hperp=0, H1(U_good)=0, and boundary/harmonic residues vanish, then P_A B_perp=0 and eps_BQ_descent_A=eps_dBQ_A=0 locally.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            "proves Bperp=0 is not a separate axiom once curvature and boundary are zero",
            "strict current corpus has not parent-signed Hperp=0",
        ),
        (
            "LHP3798_5_parent_Hperp_condition",
            "parent curvature descent condition",
            "Hperp=0 follows if H_Q=dB_Q is q_obs-basic, H_Q=q_obs^*Hbar_Q on U_good, and q_star/defect/Wilson data are silent.",
            "EXACT_CONDITIONAL_PARENT_ZERO",
            "local EM basicness reduces to parent curvature descent rather than arbitrary connection fitting",
            "current Q-shear/Pi4/projector owner remains unsigned",
        ),
    ]
    rows = []
    for theorem_id, claim_piece, mathematical_form, derivation_status, result_if_signed, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "theorem_id": theorem_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "derivation_status": derivation_status,
                "result_if_signed": result_if_signed,
                "missing_for_current_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def bound_rows(timestamp):
    specs = [
        (
            "BHB3798_0_Hperp_amp",
            "R10_lab;clock_lab",
            "epsilon_Hperp",
            "||q_star^-1 Lie_EA Hperp||_F/F_ref",
            "MISSING_PARENT_HPERP_PROFILE_OR_ZERO_THEOREM",
            "dimensionless",
            "primary curvature numerator",
        ),
        (
            "BHB3798_1_Lambda_U",
            "R10_lab;clock_lab",
            "Lambda_U",
            "C_U F_ref/A_ref",
            "MISSING_PATCH_POINCARE_CONSTANT_AND_REF_RATIO",
            "dimensionless",
            "converts curvature numerator into one-form numerator",
        ),
        (
            "BHB3798_2_eta_boundary",
            "R10_lab;clock_lab",
            "eta_boundary",
            "relative-boundary/support residue in the Green reconstruction",
            "MISSING_BOUNDARY_SUPPORT_CERTIFICATE_OR_BOUND",
            "dimensionless",
            "prevents hidden boundary primitive from faking Bperp=0",
        ),
        (
            "BHB3798_3_eta_harmonic",
            "R10_lab;clock_lab",
            "eta_harmonic",
            "harmonic/Wilson residue if H1(U) or defect support is not silent",
            "MISSING_HARMONIC_WILSON_ZERO_OR_BOUND",
            "dimensionless",
            "keeps global cycles out of the local zero theorem",
        ),
        (
            "BHB3798_4_epsilon_Bperp_bound",
            "R10_lab;clock_lab",
            "epsilon_Bperp_bound",
            "Bperp_norm_over_Aref <= Lambda_U*epsilon_Hperp + eta_boundary + eta_harmonic",
            "BOUND_FORM_READY_NUMERIC_INPUTS_MISSING",
            "dimensionless",
            "derived replacement for arbitrary Bperp profile row",
        ),
    ]
    rows = []
    for row_id, arena_id, quantity, formula, current_value, units, role in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "row_id": row_id,
                "arena_id": arena_id,
                "quantity": quantity,
                "formula": formula,
                "current_value": current_value,
                "units": units,
                "role": role,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def ansatz_rows(timestamp):
    specs = [
        (
            "ANS3798_0_shape",
            "Hperp_shape_Omega_U",
            "Hperp = h_U F_ref Omega_U, with ||Omega_U||_F=1, dOmega_U=0, and Omega_U exact/relative-exact on U_good",
            "symbolic_shape_not_numeric",
            "MISSING_PARENT_QSHEAR_CURVATURE_SHAPE",
        ),
        (
            "ANS3798_1_amplitude",
            "h_U",
            "h_U := epsilon_Hperp = ||q_star^-1 Lie_EA Hperp||_F/F_ref",
            "dimensionless_amplitude",
            "MISSING_PARENT_HPERP_AMPLITUDE",
        ),
        (
            "ANS3798_2_green_primitive",
            "Bperp_T",
            "Bperp_T = h_U F_ref delta_U G_U Omega_U plus boundary term; P_A Bperp=Bperp_T after exact gauge removal",
            "derived_from_shape",
            "MISSING_G_U_DOMAIN_AND_BOUNDARY_CONDITION",
        ),
        (
            "ANS3798_3_B_bound",
            "epsilon_Bperp",
            "epsilon_Bperp <= Lambda_U h_U + eta_boundary + eta_harmonic",
            "bound_ready_symbolic",
            "MISSING_LAMBDA_U_AND_LEAKAGE_VALUES",
        ),
        (
            "ANS3798_4_zero_branch",
            "zero_profile",
            "h_U=eta_boundary=eta_harmonic=0 implies Bperp/Hperp local silence",
            "conditional_zero_branch",
            "MISSING_PARENT_HPERP_ZERO_AND_BOUNDARY_CERTIFICATES",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "ansatz_id": ansatz_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for ansatz_id, symbol, definition, status, missing in specs
    ]


def join_update_rows(timestamp):
    specs = [
        (
            "JOIN3798_0_R10_alpha",
            "R10_lab",
            "alpha_predicted(lambda)",
            "alpha_predicted <= C_R10_H(lambda)*epsilon_Hperp + C_R10_B(lambda)*(Lambda_U*epsilon_Hperp+eta_boundary+eta_harmonic) + C_R10_lambda*|lambda_A| + C_R10_J*epsilon_J_Q",
            "MISSING_C_R10_PROJECTIONS_AND_EPSILON_HPERP",
        ),
        (
            "JOIN3798_1_clock_alpha",
            "clock_lab",
            "clock_alpha_product",
            "|DeltaK_alpha|*|tau_clock_time|*(C_CLK_H*epsilon_Hperp + C_CLK_B*(Lambda_U*epsilon_Hperp+eta_boundary+eta_harmonic) + |beta_ZA| + |lambda_A| + epsilon_J_Q) <= clock_product_bound",
            "MISSING_CLOCK_TRANSFER_COEFFICIENTS_TAU_AND_EPSILON_HPERP",
        ),
        (
            "JOIN3798_2_shared_numerator",
            "R10_lab;clock_lab",
            "shared_EM_numerator",
            "N_EM_local := epsilon_Hperp + Lambda_U*epsilon_Hperp + eta_boundary + eta_harmonic + |lambda_A| + |beta_ZA| + epsilon_J_Q",
            "MISSING_SHARED_NUMERATOR_VALUES",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "join_id": join_id,
            "arena_id": arena_id,
            "quantity": quantity,
            "formula": formula,
            "current_status": status,
            "valid_for_claim": "false",
            "blocks_claim": "true",
        }
        for join_id, arena_id, quantity, formula, status in specs
    ]


def gate_rows(timestamp):
    specs = [
        ("CG3798_0_sources", "true", "false", "all source paths and needles found"),
        ("CG3798_1_hodge_reduction", "true", "false", "local Hodge/Poincare reduction emitted"),
        ("CG3798_2_B_not_independent", "true", "false", "Bperp profile reduced to Hperp plus boundary/harmonic terms"),
        ("CG3798_3_parent_zero_claim", "false", "false", "Hperp=0 not parent-signed in strict current corpus"),
        ("CG3798_4_R10_clock_claim", "false", "false", "R10/clock projections still lack numerator and coefficients"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": gate_id,
            "pass": passed,
            "claim_allowed": claim_allowed,
            "details": details,
            "valid_for_claim": "false",
        }
        for gate_id, passed, claim_allowed, details in specs
    ]


def decision_rows(timestamp):
    specs = [
        (
            "DEC3798_0_progress",
            "Bperp is no longer an independent arbitrary profile on U_good.",
            "Hodge/Poincare reconstruction makes the one-form residue controlled by Hperp plus named boundary/harmonic residues.",
            "Replace Bperp-first sourcing with Hperp-first sourcing.",
        ),
        (
            "DEC3798_1_nonclaim",
            "No R10, clock, EM, alpha, or local-GR claim follows.",
            "The strict corpus has not parent-signed Hperp=0, Pi4/projector ownership, Lambda_U, or projection coefficients.",
            "Keep local claim closed.",
        ),
        (
            "DEC3798_2_next",
            "The next real derivation target is Hperp itself.",
            "If H_Q is q_obs-basic from parent Q/shear data, both Hperp and Bperp vanish locally; otherwise h_U is the first shared numerator.",
            "Move to 3799 Hperp curvature descent or h_U source row.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "action": action,
            "valid_for_claim": "false",
        }
        for decision_id, decision, rationale, action in specs
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_file": "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md",
            "target_script": "scripts/Y5_R2FR_3799_Hperp_curvature_descent_zero_or_first_hU_source_row.py",
            "objective": "Try to prove Hperp=H_Q-q_obs^*Hbar_Q=0 from parent Q-shear curvature descent; if not, fill the first h_U, Lambda_U, eta_boundary, and eta_harmonic source rows for R10/clock.",
            "avoid": "do not treat Bperp as independent after 3798; do not promote R10/clock claims; do not edit formalization-workbench or GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_BPERP_REDUCED_TO_HPERP",
            "plain_verdict": "3798 derives the local Hodge/Poincare reduction: after exact gauge removal on U_good, Bperp is controlled by Hperp plus boundary/harmonic leakage. This is progress because the numerator is now Hperp-first, but Hperp=0 is not parent-signed yet.",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(timestamp, grouped):
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"), "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3798 markdown document written"),
        ("hodge_theorem_present", any(row["theorem_id"] == "LHP3798_1_hodge_poincare" for row in grouped["theorem"]), "local Hodge/Poincare theorem row emitted"),
        ("bound_formula_present", any("Bperp_norm_over_Aref <=" in row["formula"] for row in grouped["bound_rows"]), "Bperp-from-Hperp bound formula emitted"),
        ("Hperp_primary_missing", any(row["quantity"] == "epsilon_Hperp" and "MISSING_" in row["current_value"] for row in grouped["bound_rows"]), "Hperp amplitude remains explicit missing input"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "all claim gates remain closed"),
        (
            "formalization_clean",
            not any((ROOT / "formalization-workbench").rglob("*3798*")),
            "no 3798 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "validation_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        keys = " ".join(f"`{row[key]}`" for key in key_fields)
        rest = "; ".join(
            f"{key}: {value}"
            for key, value in row.items()
            if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
        )
        lines.append(f"- {keys}: {rest}")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3798 - Minimal Bperp/Hperp Profile Ansatz or Parent Zero",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3798 gets an actual bite on the numerator. On a good local patch, once the exact gauge part is removed, `Bperp` is not a free extra knob. A local Hodge/Poincare reconstruction makes it the Green-operator primitive of `Hperp=dBperp`, up to boundary and harmonic/Wilson leakage.",
        "",
        "So the finite-profile branch tightens from two vague missing rows to one primary curvature numerator plus named leakages:",
        "",
        "`Bperp_norm_over_Aref <= Lambda_U*Hperp_norm_over_Fref + eta_boundary + eta_harmonic`.",
        "",
        "If `Hperp=0` and the boundary/harmonic terms vanish, then `Bperp` vanishes after gauge projection. The current corpus still does not prove `Hperp=0`; that is the next target.",
        "",
        "## Compact Result",
        "",
        "`B_perp = B_Q - q_obs^*Bbar_Q - dchi` and `Hperp=dBperp`.",
        "",
        "On `U_good` with `H1(U)=0`, `P_A Bperp` is controlled by `Hperp` through a local Green operator.",
        "",
        "Current verdict: `Bperp` reduced to `Hperp`; no local-GR/R10/clock claim.",
        "",
        render_section("Source Register", grouped["sources"], ["source_id"]),
        render_section("Local Hodge Profile Theorem", grouped["theorem"], ["theorem_id", "claim_piece"]),
        render_section("Bperp From Hperp Bound Rows", grouped["bound_rows"], ["row_id", "arena_id", "quantity"]),
        render_section("Minimal Profile Ansatz Rows", grouped["ansatz"], ["ansatz_id", "symbol"]),
        render_section("R10 Clock Numerator Update", grouped["join_update"], ["join_id", "arena_id", "quantity"]),
        render_section("Claim Gates", grouped["gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "bound_rows": bound_rows(timestamp),
        "ansatz": ansatz_rows(timestamp),
        "join_update": join_update_rows(timestamp),
        "gates": gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["bound_rows"], grouped["bound_rows"])
    write_csv(OUTPUTS["ansatz"], grouped["ansatz"])
    write_csv(OUTPUTS["join_update"], grouped["join_update"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3798 validation failed: {failures}")
    print("wrote 3798 checkpoint: Bperp reduced to Hperp plus boundary/harmonic leakage")


if __name__ == "__main__":
    main()
