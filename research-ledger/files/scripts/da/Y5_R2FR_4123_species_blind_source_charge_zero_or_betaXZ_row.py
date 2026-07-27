from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4123-Y5-R2FR-species-blind-source-charge-zero-or-betaXZ-row.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SPECIES_BLIND_SOURCE_CHARGE_CURRENT_SPINE_4123"
CHECKPOINT_ID = "4123"
DECISION = "SPECIES_BLIND_THEOREM_CONDITIONAL_BETAXZ_DIFFERENCE_ROW_FILLED_COMMON_MODE_GUARD_ACTIVE"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4123_00_4122_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4122_NEXT_TARGET.csv",
        "4123-Y5-R2FR-species-blind-source-charge-zero-or-betaXZ-row.md",
        "4122 selected species/material blindness as first comparator target.",
    ),
    "SRC4123_01_4122_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4122_STATUS.csv",
        "SOURCE_MASS_QUOTIENT_UNSIGNED_JXZ_NORMALIZATION_DEFINED_FIRST_COMPARATOR_SELECTED",
        "Current-chain source-mass normalization handoff.",
    ),
    "SRC4123_02_4122_comparator": (
        SOURCE_DIR / "P8_Y5_R2FR_4122_FIRST_COMPARATOR_CHANNEL.csv",
        "CMP4122_0_first_channel_species_source_charge",
        "Current-chain first comparator source-charge WEP target.",
    ),
    "SRC4123_03_4122_norm": (
        SOURCE_DIR / "P8_Y5_R2FR_4122_JXZ_NORMALIZATION_GATE.csv",
        "JXZN4122_1_source_charge",
        "Current-chain beta_A source-charge normalization.",
    ),
    "SRC4123_04_3637_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3637_STATUS.csv",
        "SPECIES_BLIND_THEOREM_CONDITIONAL_BETAX_DIFFERENCE_ROW_FILLED_COMMON_MODE_GUARD_ACTIVE",
        "Older beta_X species-blind checkpoint.",
    ),
    "SRC4123_05_3637_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3637_SPECIES_BLIND_THEOREM.csv",
        "SBT3637_3_common_mode_guard",
        "Older species-blind theorem with common-mode guard.",
    ),
    "SRC4123_06_3637_decomp": (
        SOURCE_DIR / "P8_Y5_R2FR_3637_BETAX_SPECIES_DECOMPOSITION.csv",
        "Delta beta_X_AB",
        "Older beta_X species decomposition.",
    ),
    "SRC4123_07_3637_guard": (
        SOURCE_DIR / "P8_Y5_R2FR_3637_COMMON_MODE_GUARD.csv",
        "CMG3637_1_common_fifth_force",
        "Older common-mode guard.",
    ),
    "SRC4123_08_3637_eta": (
        SOURCE_DIR / "P8_Y5_R2FR_3637_ETA_SOURCE_AB_BETAX_ROW.csv",
        "ETA3637_0_betaX_species_difference",
        "Older eta_source_AB beta-difference row.",
    ),
    "SRC4123_09_template": (
        SOURCE_DIR / "P8_source_normalization_residual_vector_TEMPLATE.csv",
        "P8_species_source_charge",
        "Source-normalization residual vector template.",
    ),
    "SRC4123_10_gm_runner": (
        SOURCE_DIR / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "P8_species_source_charge",
        "Existing source-normalization runner target.",
    ),
    "SRC4123_11_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4123_species_blind_source_charge_zero_or_betaXZ_row.py",
        "Reproducible generator for this 4123 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def species_theorem_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "SBT4123_0_species_charge_definition",
            "For each residual direction A_res in {X,Z} and each allowed source/test material label m, define beta_{A_res}^m:=partial_{A_res,N} ln mu_obs^m.",
            "Delta beta_{A_res}^{mn}:=beta_{A_res}^m-beta_{A_res}^n=partial_{A_res,N} ln(mu_obs^m/mu_obs^n)",
            "This is the differential source charge in eta_source_mn. It is distinct from common-mode source charge.",
            "DEFINITION_EXACT",
        ),
        (
            "SBT4123_1_species_blind_sufficient_condition",
            "If the parent matter/source functor uses one q-owned action density and species/material labels theta_m are q-owned or superselected, then beta_{A_res}^m=beta_{A_res}^n for all m,n.",
            "Lie_{A_res,N} theta_m=0 and no species-dependent source prefactor => Delta beta_{A_res}^{mn}=0",
            "The X/Z derivative sees only common q-data, so the material difference vanishes.",
            "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
        ),
        (
            "SBT4123_2_eta_zero_corollary",
            "If Delta beta_{A_res}^{mn}=0, source-charge WEP eta_source_mn is zero at the beta-difference level.",
            "eta_source_mn=2|beta_{A_res}^m-beta_{A_res}^n|/|2+beta_{A_res}^m+beta_{A_res}^n|=0",
            "The denominator is finite for small or allowed charges; exact equality kills the differential signal.",
            "CONDITIONAL_COROLLARY",
        ),
        (
            "SBT4123_3_common_mode_guard",
            "Species blindness does not imply beta_{A_res}^m=0. A common nonzero beta can pass eta_source_mn while still sourcing R10, Gdot, radial, EM, or source-normalization channels.",
            "beta_{A_res}^m=beta_{A_res}^n=beta_common != 0 => eta_source_mn=0 but J_A_source=rho_H beta_common/A_* may survive",
            "WEP constrains differential charge; fifth-force and source-normalization channels also see common charge.",
            "GUARD_PROVED",
        ),
        (
            "SBT4123_4_live_verdict",
            "The live corpus has the conditional theorem but not the parent no-marker/source-blind signature.",
            "Delta beta_X^{mn}=Delta beta_Z^{mn}=0 is not claim-live",
            "Existing gates retain species/material marker, EM-binding, clock marker, and source-prefactor failure modes.",
            "THEOREM_NOT_SIGNED_BETAXZ_ROW_REQUIRED",
        ),
    ]
    for theorem_id, statement, identity, derivation, status in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "identity": identity,
                "derivation": derivation,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def beta_decomposition_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "BXD4123_0_master_X",
            "Delta beta_X_mn",
            "Delta_mn beta_X=Delta_mn partial_XN ln G_eff + Delta_mn partial_XN ln M_eff + Delta_mn partial_XN ln(1+epsilon_mu) + Delta beta_X_marker_mn",
            "species/material dependence of normalized X source charge",
            "all terms vanish componentwise or a parent identity proves universal cancellation",
            "EXACT_DIFFERENCE_IDENTITY",
        ),
        (
            "BXD4123_1_master_Z",
            "Delta beta_Z_mn",
            "Delta_mn beta_Z=Delta_mn partial_ZN ln G_eff + Delta_mn partial_ZN ln M_eff + Delta_mn partial_ZN ln(1+epsilon_mu) + Delta beta_Z_marker_mn",
            "species/material dependence of normalized Z source charge",
            "all terms vanish componentwise or a parent identity proves universal cancellation",
            "EXACT_DIFFERENCE_IDENTITY",
        ),
        (
            "BXD4123_2_Geff",
            "Delta_mn partial_AN ln G_eff",
            "0 only if kappa/G_eff carries no species, composition, source-owner, or material label",
            "global coupling can create source-charge WEP violation if species-marked",
            "constant universal coupling superselection with no species labels",
            "OPEN_NOT_PARENT_DERIVED",
        ),
        (
            "BXD4123_3_Meff",
            "Delta_mn partial_AN ln M_eff",
            "0 only if Pi_M J_H is source-material blind and calibrated before readout",
            "projected source mass can carry composition dependence through Pi_M, J_H, or source support",
            "source Ward/Hilbert current and Pi_M are parent-owned and selector-blind",
            "OPEN_NOT_PARENT_DERIVED",
        ),
        (
            "BXD4123_4_epsilon_mu",
            "Delta_mn partial_AN ln(1+epsilon_mu)",
            "0 only if boundary/bulk/domain/memory/non-EH extra mass channel is absent or universal derivative-free",
            "hidden mass-channel hair can be composition dependent even after common geometry is selected",
            "mu_extra zero theorem or universal constant calibration with no species derivative",
            "FAILED_MISSING_COEFFICIENT_VECTOR",
        ),
        (
            "BXD4123_5_marker_EM_clock",
            "Delta beta_marker_mn",
            "sum_i(s_i^m-s_i^n)b_i including rest-mass, EM binding, clock, material, source prefactor, and readout labels",
            "ordinary matter can be geometrically universal while constants/markers carry X/Z dependence",
            "no-marker theorem or numeric b_i bounds",
            "MISSING_NO_MARKER_THEOREM",
        ),
    ]
    for decomp_id, quantity, formula, meaning, zero_condition, status in data:
        row = row_base()
        row.update(
            {
                "decomp_id": decomp_id,
                "quantity": quantity,
                "formula": formula,
                "meaning": meaning,
                "zero_condition": zero_condition,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def common_mode_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "CMG4123_0_wep_scope",
            "eta_source_mn constrains only Delta beta_A_mn, not beta_A_common.",
            "beta_A^m=beta_A^n=beta_common gives eta_source_mn=0 while alpha_A(lambda) can be nonzero.",
            "passing source-charge WEP cannot promote R10/local-GR silence",
        ),
        (
            "CMG4123_1_common_fifth_force",
            "common beta_A couples universally to source and test masses.",
            "universal Weyl/source prefactor leaves composition unchanged but mediates finite-range force if X/Z has a pole",
            "common-mode beta must go to R10/Gdot/radial/source-normalization rows",
        ),
        (
            "CMG4123_2_marker_loophole",
            "no observed coframe split does not exclude material/EM/clock marker dependence.",
            "m_m(A), alpha_EM(A), binding-energy fractions, or clock markers alter beta_A^m-beta_A^n with same geometry",
            "no-marker theorem or b_mass/b_alpha/b_clock rows remain required",
        ),
        (
            "CMG4123_3_EM_common_mode",
            "EM/Poynting source calibration may be common-mode or differential.",
            "EM source coupling can evade eta_source_AB if universal but still affect Maxwell/source-normalization channels",
            "EM common mode must stay in EM/Gdot/R10 rows unless theorem-zeroed",
        ),
    ]
    for guard_id, guard, counterexample, effect in data:
        row = row_base()
        row.update(
            {
                "guard_id": guard_id,
                "guard": guard,
                "counterexample": counterexample,
                "effect": effect,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def eta_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "ETA4123_0_betaX_species_difference",
            "eta_source_mn;eta_WEP_source_charge",
            "eta_source_mn=2|Delta beta_X_mn|/|2+beta_X^m+beta_X^n|",
            "eta_source_mn ~= |Delta beta_X_mn|",
            "Delta beta_X_mn=Delta_mn partial_XN ln G_eff + Delta_mn partial_XN ln M_eff + Delta_mn partial_XN ln(1+epsilon_mu) + Delta beta_X_marker_mn",
            "abs(eta_source_mn)<=2.8e-15 or derived universal source charge",
            "symbolic_executable_betaX_difference_not_numeric",
            "not_scoreable_until_beta_components_or_zero_theorem",
            "eta_source_mn=0 does not imply beta_X_common=0 or R10/local-GR silence",
        ),
        (
            "ETA4123_1_betaZ_species_difference",
            "eta_source_mn;eta_WEP_source_charge",
            "eta_source_mn=2|Delta beta_Z_mn|/|2+beta_Z^m+beta_Z^n|",
            "eta_source_mn ~= |Delta beta_Z_mn|",
            "Delta beta_Z_mn=Delta_mn partial_ZN ln G_eff + Delta_mn partial_ZN ln M_eff + Delta_mn partial_ZN ln(1+epsilon_mu) + Delta beta_Z_marker_mn",
            "abs(eta_source_mn)<=2.8e-15 or derived universal source charge",
            "symbolic_executable_betaZ_difference_not_numeric",
            "not_scoreable_until_beta_components_or_zero_theorem",
            "eta_source_mn=0 does not imply beta_Z_common=0 or R10/local-GR silence",
        ),
    ]
    for row_id, observable, predicted_value, small_charge, beta_difference, bound, derivation_status, score_status, common_guard in data:
        row = row_base()
        row.update(
            {
                "row_id": row_id,
                "observable": observable,
                "predicted_value": predicted_value,
                "small_charge_limit": small_charge,
                "beta_difference": beta_difference,
                "bound_or_target": bound,
                "derivation_status": derivation_status,
                "score_status": score_status,
                "common_mode_guard": common_guard,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4123_0_theorem",
            "Species-blind source-charge zero is conditionally derived if all species/material labels are q-owned and the source action has no species-prefactor X/Z slot.",
            "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "do not claim R1 source WEP until no-marker/source-blind clauses are parent-signed or beta components are bounded.",
        ),
        (
            "DEC4123_1_row",
            "eta_source_AB is expressed as beta_X and beta_Z species-difference skeletons tied to the 2.8e-15 target.",
            "BETAXZ_DIFFERENCE_ROWS_FILLED",
            "fill or prove zero for G_eff, M_eff, epsilon_mu, EM/clock/material marker beta components.",
        ),
        (
            "DEC4123_2_guard",
            "A WEP/source-charge pass would not kill common-mode beta_X/beta_Z; R10/Gdot/radial/source-normalization and EM common-mode rows remain active.",
            "COMMON_MODE_GUARD_LOCKED",
            "next target should attack no-marker theorem or common-mode beta normalization explicitly.",
        ),
        (
            "DEC4123_3_claim",
            "No R1 source-WEP, Newton, R10/R11, local-GR, PPN, Gdot, or EM-source claim is allowed from this checkpoint.",
            "NO_CLAIM",
            "use this as comparator machinery only.",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4123_0",
            "target_doc": "4124-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md",
            "target_script": "scripts/Y5_R2FR_4124_no_marker_source_theorem_or_beta_component_pack.py",
            "objective": "try to prove the no-marker/source-blind theorem for masses, EM constants, material labels, source prefactors, and clock/readout markers; if not, build beta component rows b_mass, b_alpha, b_source, b_clock, beta_common_X, and beta_common_Z",
            "success_gate": "marker/source labels are q-owned and Lie_X theta_m=Lie_Z theta_m=0, or beta_X/beta_Z rows gain component placeholders with units, sensitivities, observable links, and no-cancellation guards",
            "reason": "4123 shows the remaining R1/source-charge obstruction is marker/source-label ownership, with common-mode beta protected separately.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4123_0",
            "result": DECISION,
            "summary": (
                "4123 derives the conditional species-blind source-charge theorem and fills eta_source_AB as beta_X "
                "and beta_Z species-difference skeletons. The live corpus still lacks the parent no-marker/source-blind "
                "proof, so no WEP/source claim is promoted. Common-mode beta_X/beta_Z remains protected: eta_source_AB "
                "can vanish while universal source coupling still affects R10/Gdot/radial/source-normalization and EM channels."
            ),
            "species_blind_theorem_derived": "True",
            "beta_difference_rows_written": "True",
            "common_mode_guard_active": "True",
            "score_ready": "False",
            "claim_state": "no R1 source_WEP, Newton, R10, R11, local_GR, PPN, Gdot, or EM_source claim",
            "next_target": "4124 no-marker source theorem or beta component pack",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4123_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4123_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4123_SPECIES_BLIND_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4123_SPECIES_BLIND_THEOREM.csv",
        "P8_Y5_R2FR_4123_BETAXZ_SPECIES_DECOMPOSITION": SOURCE_DIR / "P8_Y5_R2FR_4123_BETAXZ_SPECIES_DECOMPOSITION.csv",
        "P8_Y5_R2FR_4123_COMMON_MODE_GUARD": SOURCE_DIR / "P8_Y5_R2FR_4123_COMMON_MODE_GUARD.csv",
        "P8_Y5_R2FR_4123_ETA_SOURCE_AB_BETAXZ_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4123_ETA_SOURCE_AB_BETAXZ_ROWS.csv",
        "P8_Y5_R2FR_4123_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4123_DECISION_GATES.csv",
        "P8_Y5_R2FR_4123_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4123_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4123_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4123_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4123 - Species-Blind Source-Charge Zero or BetaXZ Row",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- First comparator is now exact: `eta_source_AB` is a beta-difference row for both `X` and `Z` directions.",
        "- If species/material labels are q-owned and have no `X/Z` marker slot, `Delta beta_X=Delta beta_Z=0` conditionally.",
        "- Common-mode beta remains live: source-charge WEP can pass while R10/Gdot/radial/source-normalization or EM channels still fail.",
        "- No WEP/source or local-GR claim is made.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Species-Blind Theorem", "", "| theorem_id | identity | status |", "|---|---|---|"])
    for row in species_theorem_rows():
        sections.append(f"| {row['theorem_id']} | `{row['identity']}` | {row['status']} |")
    sections.extend(["", "## Beta Decomposition", "", "| decomp_id | quantity | status |", "|---|---|---|"])
    for row in beta_decomposition_rows():
        sections.append(f"| {row['decomp_id']} | {row['quantity']} | {row['status']} |")
    sections.extend(["", "## Common-Mode Guard", "", "| guard_id | effect |", "|---|---|"])
    for row in common_mode_rows():
        sections.append(f"| {row['guard_id']} | {row['effect']} |")
    sections.extend(["", "## Eta Source Rows", "", "| row_id | predicted_value | score_status |", "|---|---|---|"])
    for row in eta_rows():
        sections.append(f"| {row['row_id']} | `{row['predicted_value']}` | {row['score_status']} |")
    sections.extend(["", "## Next Target", "", "- `4124-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md`", "- Prove no-marker/source-blindness or build component rows for mass, EM constants, material labels, source prefactors, clock markers, and common-mode beta.", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4123_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4123_SPECIES_BLIND_THEOREM": species_theorem_rows,
        "P8_Y5_R2FR_4123_BETAXZ_SPECIES_DECOMPOSITION": beta_decomposition_rows,
        "P8_Y5_R2FR_4123_COMMON_MODE_GUARD": common_mode_rows,
        "P8_Y5_R2FR_4123_ETA_SOURCE_AB_BETAXZ_ROWS": eta_rows,
        "P8_Y5_R2FR_4123_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4123_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4123_STATUS": status_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4123_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4123_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4123_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4123_SPECIES_BLIND_THEOREM"]])
    theorem_ok = all(token in theorem_text for token in ["Delta beta", "eta_source", "common-mode", "THEOREM_NOT_SIGNED"])
    add("VAL4123_3_theorem", "species-blind theorem includes beta difference, eta, common mode, and no-claim verdict", theorem_ok, "theorem tokens checked")

    decomp_text = flatten_rows([outputs["P8_Y5_R2FR_4123_BETAXZ_SPECIES_DECOMPOSITION"]])
    decomp_ok = all(token in decomp_text for token in ["Delta beta_X", "Delta beta_Z", "G_eff", "M_eff", "epsilon_mu", "EM"])
    add("VAL4123_4_decomposition", "beta decomposition covers X, Z, Geff, Meff, epsilon_mu, and EM/marker terms", decomp_ok, "decomposition tokens checked")

    guard_text = flatten_rows([outputs["P8_Y5_R2FR_4123_COMMON_MODE_GUARD"]])
    guard_ok = all(token in guard_text for token in ["R10", "Gdot", "EM", "source-normalization"])
    add("VAL4123_5_common_mode", "common-mode guard keeps R10/Gdot/EM/source-normalization channels live", guard_ok, "guard tokens checked")

    eta_text = flatten_rows([outputs["P8_Y5_R2FR_4123_ETA_SOURCE_AB_BETAXZ_ROWS"]])
    eta_ok = all(token in eta_text for token in ["ETA4123_0_betaX", "ETA4123_1_betaZ", "2.8e-15", "not_scoreable"])
    add("VAL4123_6_eta_rows", "eta rows include betaX and betaZ difference skeletons tied to 2.8e-15 target", eta_ok, "eta tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4123_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4124-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md"
    add("VAL4123_7_next_target", "next target is 4124 no-marker source theorem", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4123_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no R1" in status_rows_local[0].get("claim_state", "")
    add("VAL4123_8_status", "status records theorem and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4123_9_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4123*")) or any(FORMALIZATION.rglob("4123-Y5-R2FR*"))
    add("VAL4123_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4123_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4123_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
