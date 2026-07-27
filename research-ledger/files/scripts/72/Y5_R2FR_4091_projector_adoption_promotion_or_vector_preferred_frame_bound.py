from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4091-Y5-R2FR-projector-adoption-promotion-or-vector-preferred-frame-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "PRIVATE_PROJECTOR_DOMAIN_PREFERRED_FRAME_ZERO_EXTENDED_PUBLIC_PROMOTION_STILL_PARENT_ADOPTION_BLOCKED"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4091_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4090_NEXT_TARGET.csv",
        "4091-Y5-R2FR-projector-adoption-promotion-or-vector-preferred-frame-bound.md",
        "4090 selects projector adoption promotion or neighbouring vector preferred-frame bound.",
    ),
    "SRC4091_01_ownership": (
        SOURCE_DIR / "P8_Y5_R2FR_4090_QBASIC_PROJECTOR_OWNERSHIP_LADDER.csv",
        "QBP4090_2_fixed_domain",
        "4090 q-basic/fixed-domain ownership ladder.",
    ),
    "SRC4091_02_alpha3": (
        SOURCE_DIR / "P8_Y5_R2FR_4090_ALPHA3_PROJECTOR_ZERO.csv",
        "EXACT_PRIVATE_BRANCH_ALPHA3_ZERO",
        "4090 already closes the harsh alpha3 flux channel in the private branch.",
    ),
    "SRC4091_03_adoption_gaps": (
        SOURCE_DIR / "P8_Y5_R2FR_4090_PARENT_ADOPTION_GAPS.csv",
        "PROMOTION_BLOCK_ACTIVE",
        "4090 records why public promotion is still blocked.",
    ),
    "SRC4091_04_4043_factor": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_PROJECTOR_STRESS_FACTORIZATION.csv",
        "feeds alpha1/alpha2 via local domain vector",
        "4043 factorizes projector/domain pieces and identifies which pieces feed alpha/xi rows.",
    ),
    "SRC4091_05_4061_kernel": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_DOMAIN_PROJECTOR_KERNEL_THEOREM.csv",
        "constraint, flux, anisotropy, and extra-denominator pieces vanish",
        "4061 gives the selected-branch domain/projector kernel zero.",
    ),
    "SRC4091_06_no_vector_attempt": (
        SOURCE_DIR / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
        "epsilon_domain_vector = 0",
        "Earlier no-vector theorem attempt separates scalar-selector vector, flux, anisotropy, and R11 gates.",
    ),
    "SRC4091_07_variation_chain": (
        SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "would set epsilon_vector, epsilon_flux, and epsilon_anisotropy to zero",
        "Parent-action variation chain shows how the domain force vector vanishes once local double-zero and no-boundary terms hold.",
    ),
    "SRC4091_08_ppn_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
        "BND4085_4_alpha2",
        "Source-stable PPN bounds for alpha1, alpha2, alpha3, and xi.",
    ),
    "SRC4091_09_projection": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_NONEH_PPN_PROJECTION_FORMULAS.csv",
        "PROJ4086_3_preferred_frame",
        "Preferred-frame projection formula mapping vector/domain markers to alpha_i and xi.",
    ),
    "SRC4091_10_component_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4089_PROJECTOR_COMPONENT_BOUND_VECTOR.csv",
        "PDB4089_2_alpha1",
        "4089 component product bounds for alpha1, alpha2, alpha3, and xi.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4091_11_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4091 projector adoption/vector preferred-frame gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def adoption_gate_rows() -> List[dict]:
    return [
        {
            "gate_id": "ADOPT4091_0_private_branch",
            "question": "Can 4090 q-basic projector/domain ownership be used inside the selected local branch?",
            "answer": "yes_for_private_selected_branch",
            "evidence": "QBP4090_0..4; DOM4061_0..2; PSF4043_0..4",
            "mathematical_use": "allowed to set projector metric-variation, domain-motion, wall-flux, local STF wall stress, and extra projector denominator pieces to zero in the private local collar",
            "promotion_status": "PRIVATE_BRANCH_ADOPTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "ADOPT4091_1_public_parent_action",
            "question": "Does the full parent action force the q-basic/topological projector rather than letting it be a closure branch?",
            "answer": "not_yet",
            "evidence": "ADOPT4090_0_private_vs_public",
            "mathematical_use": "blocks public local-GR/projector-sector promotion even though the private branch is internally coherent",
            "promotion_status": "PUBLIC_PROMOTION_BLOCKED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "ADOPT4091_2_global_boundary_harmonic",
            "question": "Are global boundary/harmonic modes source-blind or separately bounded?",
            "answer": "not_yet",
            "evidence": "ADOPT4090_1_global_boundary",
            "mathematical_use": "keeps a separate public gate outside the compact projector collar",
            "promotion_status": "SEPARATE_GATE_REMAINS",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "ADOPT4091_3_source_denominator",
            "question": "Is source normalization promoted across all sectors, not only projector/domain stress?",
            "answer": "not_yet",
            "evidence": "ADOPT4090_2_source_denominator",
            "mathematical_use": "keeps source-current/Hilbert-denominator promotion separate from this preferred-frame zero",
            "promotion_status": "SEPARATE_GATE_REMAINS",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def vector_zero_theorem_rows() -> List[dict]:
    return [
        {
            "zero_id": "VZ4091_0_vector_definition",
            "piece": "domain vector",
            "antecedent": "local domain support is q-basic/fixed and no source-support fitting is allowed",
            "derivation": "epsilon_domain_vector := P_loc^i_mu V_D^mu. In the fixed q-basic collar D_D P_D=0 and the domain/support motion term vanishes, so the surviving local domain velocity/normal marker is zero.",
            "formula": "D_D P_D=0 => epsilon_domain_vector=0",
            "selected_branch_value": "0",
            "feeds": "alpha1; alpha2",
            "status": "EXACT_PRIVATE_BRANCH_VECTOR_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "zero_id": "VZ4091_1_flux_import",
            "piece": "domain flux",
            "antecedent": "projector/domain collar has Phi_D=0 and tau_wall_TF=0",
            "derivation": "4090 already consolidated the q-basic/topological branch result that the flux channel feeding alpha3 is zero.",
            "formula": "Phi_D=0 and tau_wall_TF=0 => epsilon_domain_flux=0",
            "selected_branch_value": "0",
            "feeds": "alpha3",
            "status": "EXACT_PRIVATE_BRANCH_FLUX_ZERO_IMPORTED_FROM_4090",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "zero_id": "VZ4091_2_anisotropy_zero",
            "piece": "domain anisotropy",
            "antecedent": "constraint multiplier, wall STF stress, and topological projector metric-variation are zero in the selected collar",
            "derivation": "The only projector/domain STF sources identified in 4043 are projector metric variation, constraint stress, and wall STF stress. 4043/4061/4090 set each selected-branch value to zero, hence the preferred-location anisotropy residual vanishes.",
            "formula": "delta_g P_D=0, chi_local=lambda_local=0, tau_wall_TF=0 => epsilon_domain_anisotropy=0",
            "selected_branch_value": "0",
            "feeds": "xi",
            "status": "EXACT_PRIVATE_BRANCH_ANISOTROPY_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "zero_id": "VZ4091_3_vector_block",
            "piece": "preferred-frame/location block",
            "antecedent": "VZ4091_0, VZ4091_1, and VZ4091_2 hold inside the selected private local collar",
            "derivation": "PROJ4086_3 maps surviving vector/domain/coframe/projector markers to alpha1, alpha2, alpha3, and xi. With those markers zero in the selected branch, the entire projector/domain preferred-frame block is zero.",
            "formula": "epsilon_domain_vector=epsilon_domain_flux=epsilon_domain_anisotropy=0 => alpha1_domain=alpha2_domain=alpha3_domain=xi_domain=0",
            "selected_branch_value": "0",
            "feeds": "alpha1; alpha2; alpha3; xi",
            "status": "EXACT_PRIVATE_BRANCH_PREFERRED_FRAME_BLOCK_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def preferred_frame_residual_rows() -> List[dict]:
    return [
        {
            "row_id": "PFR4091_0_alpha1",
            "observable": "alpha1",
            "product_formula": "alpha1_domain = W_domain_alpha1 * epsilon_domain_vector",
            "selected_branch_substitution": "epsilon_domain_vector=0",
            "selected_branch_value": "0",
            "bound_value": "4.0e-5",
            "bound_source": "BND4085_3_alpha1_pulsar_companion; PDB4089_2_alpha1",
            "pass_statement": "|alpha1_domain|=0 <= 4.0e-5",
            "status": "PRIVATE_BRANCH_BOUND_SATISFIED_BY_THEOREM_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "PFR4091_1_alpha2",
            "observable": "alpha2",
            "product_formula": "alpha2_domain = W_domain_alpha2 * epsilon_domain_vector",
            "selected_branch_substitution": "epsilon_domain_vector=0",
            "selected_branch_value": "0",
            "bound_value": "2.0e-9",
            "bound_source": "BND4085_4_alpha2; PDB4089_3_alpha2",
            "pass_statement": "|alpha2_domain|=0 <= 2.0e-9",
            "status": "PRIVATE_BRANCH_BOUND_SATISFIED_BY_THEOREM_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "PFR4091_2_alpha3",
            "observable": "alpha3",
            "product_formula": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "selected_branch_substitution": "epsilon_domain_flux=0",
            "selected_branch_value": "0",
            "bound_value": "4.0e-20",
            "bound_source": "BND4085_5_alpha3; PDB4089_4_alpha3; A3Z4090_2_alpha3_zero",
            "pass_statement": "|alpha3_domain|=0 <= 4.0e-20",
            "status": "PRIVATE_BRANCH_BOUND_SATISFIED_BY_4090_THEOREM_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "PFR4091_3_xi",
            "observable": "xi",
            "product_formula": "xi_domain = W_domain_xi * epsilon_domain_anisotropy",
            "selected_branch_substitution": "epsilon_domain_anisotropy=0",
            "selected_branch_value": "0",
            "bound_value": "4.0e-9",
            "bound_source": "BND4085_6_xi; PDB4089_5_xi",
            "pass_statement": "|xi_domain|=0 <= 4.0e-9",
            "status": "PRIVATE_BRANCH_BOUND_SATISFIED_BY_THEOREM_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def fallback_contract_rows() -> List[dict]:
    return [
        {
            "contract_id": "PFF4091_0_alpha1_alpha2",
            "if_rejected": "If fixed q-basic domain/support motion is rejected.",
            "required_inputs": "W_domain_alpha1; W_domain_alpha2; epsilon_domain_vector; coframe; source normalization; local support rule; source path",
            "formula": "alpha1_domain=W_domain_alpha1*epsilon_domain_vector; alpha2_domain=W_domain_alpha2*epsilon_domain_vector",
            "pass_rule": "abs(alpha1_domain)<=4.0e-5 and abs(alpha2_domain)<=2.0e-9",
            "status": "SOURCE_READY_FALLBACK_CONTRACT",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "PFF4091_1_alpha3",
            "if_rejected": "If 4090 flux zero is rejected.",
            "required_inputs": "W_domain_alpha3; epsilon_domain_flux; wall flux definition; source path; units; no-cancellation policy",
            "formula": "alpha3_domain=W_domain_alpha3*epsilon_domain_flux",
            "pass_rule": "abs(alpha3_domain)<=4.0e-20",
            "status": "SOURCE_READY_FALLBACK_CONTRACT_ALREADY_DEFINED_IN_4090",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "PFF4091_2_xi",
            "if_rejected": "If selected-branch STF anisotropy zero is rejected.",
            "required_inputs": "W_domain_xi; epsilon_domain_anisotropy; local STF stress projection; external-environment normalization; source path",
            "formula": "xi_domain=W_domain_xi*epsilon_domain_anisotropy",
            "pass_rule": "abs(xi_domain)<=4.0e-9",
            "status": "SOURCE_READY_FALLBACK_CONTRACT",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "PFF4091_3_no_cancellation",
            "if_rejected": "If any preferred-frame/location row remains live.",
            "required_inputs": "row-wise products, not fitted total residuals",
            "formula": "score each alpha_i and xi separately",
            "pass_rule": "no cancellation between alpha1, alpha2, alpha3, xi, gamma, beta, zeta, or Gdot",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4091_0_private_vector_block",
            "decision": "promote within private selected branch",
            "because": "4090 q-basic ownership plus 4043/4061 factorization kills domain vector, flux, and STF anisotropy markers in the compact local collar.",
            "result": "alpha1_domain=alpha2_domain=alpha3_domain=xi_domain=0",
            "claim_effect": "private projector/domain preferred-frame block cleared",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4091_1_public_promotion",
            "decision": "do not promote public local-GR/projector-sector claim yet",
            "because": "parent action adoption, global boundary/harmonic source-blindness, and all-sector source-denominator promotion remain unsigned.",
            "result": "public claim remains false",
            "claim_effect": "honest nonclaim checkpoint",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4091_2_if_rejected",
            "decision": "use fallback products only if theorem-zero route is rejected",
            "because": "the product bounds are tiny, especially alpha2 and alpha3, so exact zero is the structurally stronger route.",
            "result": "fallback product contracts are ready for alpha1, alpha2, alpha3, xi",
            "claim_effect": "no row becomes score-valid without numeric/source-backed products",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4091_0_private_branch",
            "claim": "private selected-branch projector/domain preferred-frame residual block is zero",
            "allowed": "True",
            "reason": "within the adopted private q-basic/local collar, the relevant vector, flux and anisotropy markers vanish before coefficient fitting",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4091_1_public_projector_sector",
            "claim": "public projector-sector local-GR pass",
            "allowed": "False",
            "reason": "parent adoption and global gates are still unsigned",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4091_2_full_local_GR",
            "claim": "full MTS to local GR pass",
            "allowed": "False",
            "reason": "gamma/beta EH-only, source-current conservation, source denominator, boundary/harmonic, and non-EH/R11 families still require promotion or bounds",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4091_0",
            "next_target": "4092-Y5-R2FR-parent-adoption-axiom-free-qbasic-selector-or-source-denominator-promotion.md",
            "script": "scripts/Y5_R2FR_4092_parent_adoption_axiom_free_qbasic_selector_or_source_denominator_promotion.py",
            "why": "4091 clears the preferred-frame projector/domain block inside the private branch. Next must either derive parent adoption of the q-basic selector globally, or promote the source denominator/source-current gate that still blocks public local GR.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4091_1",
            "next_target": "preferred_frame_numeric_product_fill_if_private_branch_rejected",
            "script": "defer_until_qbasic_or_vector_zero_rejected",
            "why": "Do not chase tiny fitted products unless the exact q-basic/vector-zero route is rejected.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4091",
            "decision": DECISION,
            "private_projector_preferred_frame_block": "alpha1=alpha2=alpha3=xi=0",
            "public_projector_claim": "False",
            "full_local_GR_claim": "False",
            "next_required_gate": "parent_adoption_or_source_denominator_promotion",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4091 - Projector Adoption Promotion Or Vector Preferred-Frame Bound",
                "",
                "## Purpose",
                "",
                "4090 closed the harsh `alpha3` projector/domain flux row inside the private q-basic local branch. 4091 tests whether that same branch also kills the neighbouring preferred-frame/location rows, rather than leaving `alpha1`, `alpha2`, and `xi` as vague missing coefficients.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public local-GR/projector-sector claim: `false`",
                "- Private selected-branch result: `alpha1_domain = alpha2_domain = alpha3_domain = xi_domain = 0`",
                "",
                "## Derivation",
                "",
                "The 4086 preferred-frame projection says surviving local vector, domain, coframe, or projector markers feed",
                "",
                "```text",
                "alpha_i_nonEH = Pi_alpha_i[DeltaE_nonEH, V_extra, domain normal, coframe marker]",
                "xi_nonEH      = Pi_xi[anisotropic/domain marker]",
                "```",
                "",
                "The 4043/4061/4090 selected branch removes the relevant projector/domain markers:",
                "",
                "```text",
                "D_D P_D = 0                                     => epsilon_domain_vector = 0",
                "Phi_D = 0 and tau_wall_TF = 0                   => epsilon_domain_flux = 0",
                "delta_g P_D = 0, chi=lambda=0, tau_wall_TF=0    => epsilon_domain_anisotropy = 0",
                "```",
                "",
                "Therefore the whole projector/domain preferred-frame block collapses before fitting:",
                "",
                "```text",
                "alpha1_domain = W_domain_alpha1 * epsilon_domain_vector     = 0",
                "alpha2_domain = W_domain_alpha2 * epsilon_domain_vector     = 0",
                "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux       = 0",
                "xi_domain     = W_domain_xi     * epsilon_domain_anisotropy  = 0",
                "```",
                "",
                "This is the clean route. It avoids trying to tune products below `4e-5`, `2e-9`, `4e-20`, and `4e-9` respectively.",
                "",
                "## What This Actually Advances",
                "",
                "Before 4091, only the `alpha3` flux row had been consolidated in the private q-basic branch. After 4091, the same branch clears the sibling preferred-frame/location block:",
                "",
                "- `alpha1`: no local domain vector survives.",
                "- `alpha2`: same vector residual is zero.",
                "- `alpha3`: 4090 flux zero is imported.",
                "- `xi`: no local STF anisotropy survives.",
                "",
                "That means the projector/domain sector is no longer leaking preferred-frame structure inside the private selected local branch.",
                "",
                "## Why It Is Still Not Public",
                "",
                "The public claim is still blocked for the same honest reasons as 4090:",
                "",
                "- the parent action has not yet forced the q-basic/topological projector globally rather than as a selected private branch;",
                "- global boundary/harmonic source-blindness is not closed;",
                "- all-sector source-current/source-denominator promotion remains separate;",
                "- non-projector R11 families still need zero theorems or bounds.",
                "",
                "So this is not a public `MTS reduces to GR` claim. It is a real internal advance: the private q-basic local collar now kills the whole projector/domain preferred-frame block by theorem-zero.",
                "",
                "## Fallback If Rejected",
                "",
                "If the q-basic/vector-zero route is rejected, 4091 leaves explicit product contracts:",
                "",
                "```text",
                "|W_domain_alpha1 * epsilon_domain_vector|     <= 4.0e-5",
                "|W_domain_alpha2 * epsilon_domain_vector|     <= 2.0e-9",
                "|W_domain_alpha3 * epsilon_domain_flux|       <= 4.0e-20",
                "|W_domain_xi     * epsilon_domain_anisotropy| <= 4.0e-9",
                "```",
                "",
                "No cancellation between these rows is allowed.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4091_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4091_PROJECTOR_ADOPTION_GATE.csv`",
                "- `P8_Y5_R2FR_4091_VECTOR_ZERO_THEOREM.csv`",
                "- `P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR.csv`",
                "- `P8_Y5_R2FR_4091_FALLBACK_PRODUCT_CONTRACT.csv`",
                "- `P8_Y5_R2FR_4091_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4091_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4091_NEXT_TARGET.csv`",
                "- `P8_Y5_BRR545_4091_VALIDATION.csv`",
                "",
                "## Next",
                "",
                "4092 should stop circling product coefficients and aim at the remaining structural blocker: either derive parent adoption of the q-basic selector without an axiom, or promote the source denominator/source-current gate that keeps the private branch from becoming public local GR.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4091_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4091_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4091_PROJECTOR_ADOPTION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4091_PROJECTOR_ADOPTION_GATE.csv",
        "P8_Y5_R2FR_4091_VECTOR_ZERO_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4091_VECTOR_ZERO_THEOREM.csv",
        "P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR.csv",
        "P8_Y5_R2FR_4091_FALLBACK_PRODUCT_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4091_FALLBACK_PRODUCT_CONTRACT.csv",
        "P8_Y5_R2FR_4091_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4091_DECISION_GATE.csv",
        "P8_Y5_R2FR_4091_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4091_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4091_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4091_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4091_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4091_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4091_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_PROJECTOR_ADOPTION_GATE"], adoption_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_VECTOR_ZERO_THEOREM"], vector_zero_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR"], preferred_frame_residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_FALLBACK_PRODUCT_CONTRACT"], fallback_contract_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4091_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4091_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4091_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    residuals = parse_csv(outputs["P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR"])
    expected_observables = {"alpha1", "alpha2", "alpha3", "xi"}
    zero_observables = {
        row["observable"]
        for row in residuals
        if row.get("selected_branch_value") == "0"
        and "THEOREM_ZERO" in row.get("status", "")
        and row.get("valid_for_claim") == "False"
    }
    rows.append(
        {
            "check_id": "VAL4091_PREFERRED_FRAME_ZERO_VECTOR",
            "check": "private branch preferred-frame rows are zero but nonclaim",
            "passed": bool_string(zero_observables == expected_observables),
            "detail": f"zero_observables={sorted(zero_observables)} expected={sorted(expected_observables)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    adoption = parse_csv(outputs["P8_Y5_R2FR_4091_PROJECTOR_ADOPTION_GATE"])
    blocked = any(row.get("promotion_status") == "PUBLIC_PROMOTION_BLOCKED" for row in adoption)
    private = any(row.get("promotion_status") == "PRIVATE_BRANCH_ADOPTED" for row in adoption)
    rows.append(
        {
            "check_id": "VAL4091_ADOPTION_SCOPE",
            "check": "private branch adopted while public promotion remains blocked",
            "passed": bool_string(private and blocked),
            "detail": f"private={private}; public_blocked={blocked}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    fallback = parse_csv(outputs["P8_Y5_R2FR_4091_FALLBACK_PRODUCT_CONTRACT"])
    fallback_text = "\n".join(str(row) for row in fallback)
    fallback_ok = all(bound in fallback_text for bound in ["4.0e-5", "2.0e-9", "4.0e-20", "4.0e-9"])
    rows.append(
        {
            "check_id": "VAL4091_FALLBACK_PRODUCTS",
            "check": "fallback products carry all preferred-frame/location bounds",
            "passed": bool_string(fallback_ok),
            "detail": "requires alpha1, alpha2, alpha3, xi product bounds",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claim_rows = parse_csv(outputs["P8_Y5_R2FR_4091_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claim_rows)
    rows.append(
        {
            "check_id": "VAL4091_NO_PUBLIC_LOCAL_GR_CLAIM",
            "check": "4091 does not promote public local-GR/projector-sector claim",
            "passed": bool_string(no_public),
            "detail": "private theorem-zero only; public claims remain false",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4091_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4091_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4091_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4091 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
