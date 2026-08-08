from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3637"
BRANCH_ID = "MTS_R2FR_Y5_SPECIES_BLIND_SOURCE_CHARGE_ZERO_OR_BETAX_ROW_3637"
DOC = ROOT / "3637-Y5-R2FR-species-blind-source-charge-zero-or-betaX-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def out_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3637_SOURCE_REGISTER.csv",
        "species_blind_theorem": RESIDUALS / "P8_Y5_R2FR_3637_SPECIES_BLIND_THEOREM.csv",
        "beta_decomposition": RESIDUALS / "P8_Y5_R2FR_3637_BETAX_SPECIES_DECOMPOSITION.csv",
        "common_mode_guard": RESIDUALS / "P8_Y5_R2FR_3637_COMMON_MODE_GUARD.csv",
        "eta_row": RESIDUALS / "P8_Y5_R2FR_3637_ETA_SOURCE_AB_BETAX_ROW.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3637_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3637_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3637_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_species_blind_source_charge_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3637_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    sources = [
        (
            "handoff_3636",
            RESIDUALS / "P8_Y5_R2FR_3636_NEXT_TARGET.csv",
            "species/material blindness",
            "3636 selected species-blind source charge as first comparator.",
        ),
        (
            "comparator_3636",
            RESIDUALS / "P8_Y5_R2FR_3636_FIRST_COMPARATOR_CHANNEL.csv",
            "eta_source_AB",
            "first comparator channel and beta difference formula.",
        ),
        (
            "source_hair_gate",
            RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
            "CGM3_species_source_charge",
            "existing derivative-hair source-charge gate.",
        ),
        (
            "source_norm_template",
            RESIDUALS / "P8_source_normalization_residual_vector_TEMPLATE.csv",
            "P8_species_source_charge",
            "template row for eta_source_AB.",
        ),
        (
            "local_residual_template",
            RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
            "R1_WEP_source_charge",
            "local residual R1 source-charge row.",
        ),
        (
            "constant_gm_runner",
            RESIDUALS / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
            "MISSING_NUMERIC_OR_DERIVED_ZERO_SOURCE_CHARGE",
            "current runner says source-charge prediction is missing.",
        ),
        (
            "local_gr_action_blocks",
            RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "universal_matter",
            "minimal local-GR action block requiring universal matter/source coupling.",
        ),
        (
            "fixed_point_conditions",
            RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "universal_observed_coframe",
            "fixed-point condition for common observed coframe and source readout.",
        ),
        (
            "qbar_source_guard_1027",
            ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            "common nonzero source charge",
            "guard that WEP/species-blindness does not kill common-mode source charge.",
        ),
        (
            "marker_guard_1028",
            ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "MISSING_NO_MARKER_THEOREM",
            "material/EM/clock marker theorem is still missing.",
        ),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
        }
        for source_id, path, needle, role in sources
    ]


def species_blind_theorem_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "theorem_id": "SBT3637_0_species_charge_definition",
            "statement": "For each allowed source/test material label A, define beta_X^A := partial_XN ln mu_obs^A.",
            "identity": "Delta beta_X_AB := beta_X^A - beta_X^B = partial_XN ln(mu_obs^A/mu_obs^B)",
            "derivation": "This is the differential source charge that appears in eta_source_AB. It is distinct from the common-mode source charge.",
            "status": "DEFINITION_EXACT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SBT3637_1_species_blind_sufficient_condition",
            "statement": "If the parent matter/source functor uses one q-owned action density and species labels theta_A are q-owned/superselected, then beta_X^A=beta_X^B for all A,B.",
            "identity": "Lie_XN theta_A=0 and no species-dependent source prefactor => Delta beta_X_AB=0",
            "derivation": "The X derivative sees only common q-data, so the species/material difference vanishes.",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SBT3637_2_eta_zero_corollary",
            "statement": "If Delta beta_X_AB=0, source-charge WEP eta_source_AB is zero at this beta-difference level.",
            "identity": "eta_source_AB = 2|beta_X^A-beta_X^B|/|2+beta_X^A+beta_X^B| = 0",
            "derivation": "The denominator is finite for small or allowed charges; exact equality of beta charges kills the differential signal.",
            "status": "CONDITIONAL_COROLLARY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SBT3637_3_common_mode_guard",
            "statement": "Species blindness does not imply beta_X^A=0. A common nonzero beta_X can pass eta_source_AB while still sourcing R10, clocks, or source normalization.",
            "identity": "beta_X^A=beta_X^B=beta_common != 0 => eta_source_AB=0 but J_X_source=rho_H beta_common/X_* may survive",
            "derivation": "WEP constrains differential charge; fifth-force and source-normalization channels also see common charge.",
            "status": "GUARD_PROVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SBT3637_4_live_verdict",
            "statement": "The live corpus has the conditional theorem but not the parent no-marker/source-blind signature.",
            "identity": "Delta beta_X_AB=0 is not claim-live",
            "derivation": "Existing gates retain species/material marker and source-prefactor failure modes.",
            "status": "THEOREM_NOT_SIGNED_BETAX_ROW_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def beta_decomposition_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "decomp_id": "BXD3637_0_master",
            "quantity": "Delta beta_X_AB",
            "formula": "Delta_AB beta_X = Delta_AB partial_XN ln G_eff + Delta_AB partial_XN ln M_eff + Delta_AB partial_XN ln(1+epsilon_mu)",
            "meaning": "species/material dependence of the normalized source charge",
            "zero_condition": "all three terms vanish componentwise or a parent identity proves universal cancellation",
            "status": "EXACT_DIFFERENCE_IDENTITY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decomp_id": "BXD3637_1_Geff",
            "quantity": "Delta_AB partial_XN ln G_eff",
            "formula": "0 only if kappa/G_eff carries no species, composition, source-owner, or material label",
            "meaning": "global coupling can create source-charge WEP violation if it is species-marked",
            "zero_condition": "constant universal coupling superselection with no species labels",
            "status": "OPEN_NOT_PARENT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decomp_id": "BXD3637_2_Meff",
            "quantity": "Delta_AB partial_XN ln M_eff",
            "formula": "0 only if Pi_M J_H is source-material blind and calibrated before readout",
            "meaning": "projected source mass can carry composition dependence through Pi_M, J_H, or source support",
            "zero_condition": "source Ward/Hilbert current and Pi_M are parent-owned and selector-blind",
            "status": "OPEN_NOT_PARENT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decomp_id": "BXD3637_3_epsilon_mu",
            "quantity": "Delta_AB partial_XN ln(1+epsilon_mu)",
            "formula": "0 only if boundary/bulk/domain/memory/non-EH extra mass channel is absent or universal derivative-free",
            "meaning": "hidden mass-channel hair can be composition dependent even after common geometry is selected",
            "zero_condition": "mu_extra zero theorem or universal constant calibration with no species derivative",
            "status": "FAILED_MISSING_COEFFICIENT_VECTOR",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decomp_id": "BXD3637_4_marker",
            "quantity": "material/EM/clock marker contribution",
            "formula": "Delta beta_marker_AB = sum_i (s_i^A-s_i^B) b_i, including mass, EM binding, clock, or material labels",
            "meaning": "ordinary matter can be geometrically universal while constants/markers carry X dependence",
            "zero_condition": "no-marker theorem or numeric b_i bounds",
            "status": "MISSING_NO_MARKER_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def common_mode_guard_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "guard_id": "CMG3637_0_wep_scope",
            "guard": "eta_source_AB only constrains Delta beta_X_AB, not beta_common.",
            "counterexample": "beta_X^A=beta_X^B=beta_common gives eta_source_AB=0 while alpha_X(lambda) can be nonzero.",
            "effect": "passing source-charge WEP cannot promote R10/local-GR silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "guard_id": "CMG3637_1_common_fifth_force",
            "guard": "common beta_X couples universally to source and test masses.",
            "counterexample": "universal Weyl/source prefactor leaves composition unchanged but mediates a finite-range force if X has a pole",
            "effect": "common-mode beta must go to R10/Gdot/radial/source-normalization rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "guard_id": "CMG3637_2_marker_loophole",
            "guard": "no observed coframe split does not exclude material/EM/clock marker dependence.",
            "counterexample": "m_A(X), alpha_EM(X), or binding-energy markers alter beta_X^A-beta_X^B with the same geometry",
            "effect": "no-marker theorem or b_A/b_alpha rows remain required",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def eta_row(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "ETA3637_0_betaX_species_difference",
            "model_id": "MTS_source_normalized_Newton_branch",
            "component_id": "P8_species_source_charge",
            "observable": "eta_source_AB;eta_WEP_source_charge",
            "predicted_value": "eta_source_AB = 2|Delta beta_X_AB|/|2+beta_X^A+beta_X^B|",
            "small_charge_limit": "eta_source_AB ~= |Delta beta_X_AB|",
            "beta_difference": "Delta beta_X_AB = Delta_AB partial_XN ln G_eff + Delta_AB partial_XN ln M_eff + Delta_AB partial_XN ln(1+epsilon_mu) + Delta beta_marker_AB",
            "units": "dimensionless",
            "bound_or_target": "abs(eta_source_AB) <= 2.8e-15 or derived universal source charge",
            "source_paths": f"{RESIDUALS / 'P8_source_normalization_residual_vector_TEMPLATE.csv'};{RESIDUALS / 'P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv'};{RESIDUALS / 'P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv'}",
            "derivation_status": "symbolic_executable_beta_difference_not_numeric",
            "score_status": "not_scoreable_until_beta_components_or_zero_theorem",
            "common_mode_guard": "eta_source_AB=0 does not imply beta_common=0 or R10/local-GR silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC3637_0_theorem",
            "decision": "Species-blind source-charge zero is conditionally derived if all species/material labels are q-owned and source action has no species-prefactor X slot.",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "next_action": "do not claim R1 source WEP until no-marker/source-blind clauses are parent-signed or beta components are bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3637_1_row",
            "decision": "The eta_source_AB row is now expressed as a beta_X species-difference skeleton tied to the existing 2.8e-15 target.",
            "status": "BETAX_DIFFERENCE_ROW_FILLED",
            "next_action": "fill or prove zero for Geff, Meff, epsilon_mu, and marker beta components",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3637_2_guard",
            "decision": "A WEP/source-charge pass would not kill common-mode beta_X; R10/Gdot/radial common-mode rows must remain active.",
            "status": "COMMON_MODE_GUARD_LOCKED",
            "next_action": "next target should attack no-marker theorem or common-mode beta normalization explicitly",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "SPECIES_BLIND_THEOREM_CONDITIONAL_BETAX_DIFFERENCE_ROW_FILLED_COMMON_MODE_GUARD_ACTIVE",
            "summary": "3637 derives the conditional species-blind source-charge theorem and fills the eta_source_AB row as a beta_X species-difference skeleton. The live corpus still lacks the parent no-marker/source-blind proof, so no WEP/source claim is promoted. Crucially, common-mode beta_X remains separate: eta_source_AB can vanish while a universal source coupling still affects R10/Gdot/radial/source-normalization channels.",
            "claim_ceiling": "no R1 source-WEP, Newton, R10/R11, local-GR, or PPN claim is allowed from 3637",
            "useful_result": "eta_source_AB is now Delta beta_X_AB with a 2.8e-15 target, and common beta is protected from accidental erasure",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3637_0",
            "target_doc": "3638-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md",
            "target_script": "scripts/Y5_R2FR_3638_no_marker_source_theorem_or_beta_component_pack.py",
            "objective": "try to prove the no-marker/source-blind theorem for masses, EM constants, material labels, source prefactors, and clock/readout markers; if not, build beta component rows b_A, b_alpha, b_source, and beta_common",
            "success_gate": "either marker/source labels are q-owned and Lie_X theta_A=0, or the beta_X row gains component placeholders with units, sensitivities, observable links, and no-cancellation guards",
            "reason": "3637 shows the remaining R1/source-charge obstruction is marker/source-label ownership, with common-mode beta protected separately.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "species_blind_source_charge_beta_row",
            "canonical_status": "CONDITIONAL_THEOREM_NOT_SIGNED_BETAX_ROW_ACTIVE",
            "usable_result": "eta_source_AB = 2|Delta beta_X_AB|/|2+beta_X^A+beta_X^B| with Delta beta_X_AB decomposed into Geff, Meff, epsilon_mu, and marker pieces; common beta_X remains active.",
            "hard_block": "prove no-marker/source-blind parent theorem or fill beta component pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    output = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(output)


def write_doc(
    src: list[dict[str, object]],
    theorem: list[dict[str, object]],
    decomp: list[dict[str, object]],
    guards: list[dict[str, object]],
    eta: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3637 Y5 R2FR species-blind source charge zero or betaX row",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Main result",
            (
                "The first comparator is now a clean beta-difference row:\n\n"
                "```text\n"
                "beta_X^A := partial_{X_N} ln(mu_obs^A)\n"
                "Delta beta_X_AB := beta_X^A - beta_X^B\n"
                "eta_source_AB = 2|Delta beta_X_AB| / |2 + beta_X^A + beta_X^B|.\n"
                "```\n\n"
                "If parent source/matter labels are species-blind quotient data, `Delta beta_X_AB=0`. That would pass the differential source-charge channel. But it does **not** kill a common `beta_X`; common beta still has to be handled by R10/Gdot/radial/source-normalization rows."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Species-blind theorem",
            table(theorem, ["theorem_id", "statement", "identity", "derivation", "status"]),
            "## Beta species decomposition",
            table(decomp, ["decomp_id", "quantity", "formula", "meaning", "zero_condition", "status"]),
            "## Common-mode guard",
            table(guards, ["guard_id", "guard", "counterexample", "effect"]),
            "## eta source beta row",
            table(eta, ["row_id", "observable", "predicted_value", "small_charge_limit", "beta_difference", "bound_or_target", "derivation_status", "score_status", "common_mode_guard"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(outputs: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3637_0_sources_exist", all(bool(row["exists"]) for row in src), "all cited source paths exist")
    add("VAL3637_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in outputs.items() if name != "validation"}
    add("VAL3637_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")

    details = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3637_3_csv_parse", parse_ok, "; ".join(details))

    theorem = read_csv(outputs["species_blind_theorem"])
    decomp = read_csv(outputs["beta_decomposition"])
    guards = read_csv(outputs["common_mode_guard"])
    eta = read_csv(outputs["eta_row"])
    decisions = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    nxt = read_csv(outputs["next_target"])

    add("VAL3637_4_species_blind_theorem_present", any("Delta beta_X_AB=0" in row["identity"] for row in theorem), "species-blind beta theorem row present")
    add("VAL3637_5_common_mode_guard_present", any("beta_common" in row["counterexample"] for row in guards), "common-mode beta guard present")
    add("VAL3637_6_beta_decomposition_complete", len(decomp) >= 5 and any(row["quantity"] == "material/EM/clock marker contribution" for row in decomp), "beta decomposition includes marker contribution")
    add("VAL3637_7_eta_row_filled", bool(eta) and "2|Delta beta_X_AB|" in eta[0]["predicted_value"] and eta[0]["bound_or_target"].startswith("abs(eta_source_AB)"), "eta_source_AB beta-difference row filled")
    add("VAL3637_8_wep_not_overpromoted", "common beta" in status[0]["useful_result"] and any(row["status"] == "COMMON_MODE_GUARD_LOCKED" for row in decisions), "WEP source pass cannot erase common beta")
    add("VAL3637_9_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in theorem + decomp + guards + eta + decisions + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3637*")) if FORMALIZATION.exists() else []
    add("VAL3637_10_no_formalization_leak", not leaks, "no 3637 files in formalization-workbench")
    add("VAL3637_11_next_target_written", bool(nxt) and "3638" in nxt[0]["target_doc"], "3638 no-marker/beta component target written")
    add("VAL3637_12_doc_written", DOC.exists() and "Delta beta_X_AB" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with beta difference")
    add("VAL3637_13_canonical_status_written", outputs["canonical_status"].exists() and "CONDITIONAL_THEOREM_NOT_SIGNED_BETAX_ROW_ACTIVE" in outputs["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical species-blind source status written")
    return rows


def main() -> None:
    t = now()
    outputs = out_paths()
    src = source_rows(t)
    theorem = species_blind_theorem_rows(t)
    decomp = beta_decomposition_rows(t)
    guards = common_mode_guard_rows(t)
    eta = eta_row(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(outputs["source_register"], src)
    write_csv(outputs["species_blind_theorem"], theorem)
    write_csv(outputs["beta_decomposition"], decomp)
    write_csv(outputs["common_mode_guard"], guards)
    write_csv(outputs["eta_row"], eta)
    write_csv(outputs["decision_gates"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], nxt)
    write_csv(outputs["canonical_status"], canonical)
    write_doc(src, theorem, decomp, guards, eta, decisions, status, nxt)

    validation = validate(outputs, src)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3637 validation failed: {failures}")
    print(f"wrote 3637 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
