from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3332-Y5-R2FR-PPN-epsilon-eff-and-floor-specialization-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3332_0_3331_doc",
        "path": ROOT / "3331-Y5-R2FR-PPN-weak-potential-normalization-and-Cmetric-bound-under-AX1090.md",
        "role": "normalized PPN budget handoff",
    },
    {
        "source_id": "SRC3332_1_3331_cppn",
        "path": OUT / "P8_Y5_R2FR_3331_CPPN_COMPOSITION.csv",
        "role": "C_PPN <= A_PPN C_metric and full PPN budget",
    },
    {
        "source_id": "SRC3332_2_3321_kernel",
        "path": OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv",
        "role": "Gaussian T_grad(lambda) transfer law",
    },
    {
        "source_id": "SRC3332_3_3321_solar_proxy",
        "path": OUT / "P8_Y5_R2FR_3321_SOLAR_PROXY_BOUND.csv",
        "role": "K_solar^m internal scale proxy",
    },
    {
        "source_id": "SRC3332_4_3327_composite",
        "path": OUT / "P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv",
        "role": "CLT/mixing composite envelope",
    },
    {
        "source_id": "SRC3332_5_3330_floors",
        "path": OUT / "P8_Y5_R2FR_3330_LOCAL_FLOOR_BOUNDS.csv",
        "role": "Gamma, epsilon_eff, composite, and direct floor handoff",
    },
    {
        "source_id": "SRC3332_6_3324_measured_G",
        "path": OUT / "P8_Y5_R2FR_3324_MEASURED_G_CLOSURE_THEOREM.csv",
        "role": "measured-G local GR/Newton/Maxwell closure",
    },
    {
        "source_id": "SRC3332_7_3325_matter_signature",
        "path": OUT / "P8_Y5_R2FR_3325_MATTER_SIGNATURE_CONTRACT.csv",
        "role": "metric matter/Maxwell signature and forbidden direct vertices",
    },
    {
        "source_id": "SRC3332_8_3325_direct_vertex",
        "path": OUT / "P8_Y5_R2FR_3325_DIRECT_VERTEX_AUDIT.csv",
        "role": "direct psi-matter/psi-EM vertex branch guard",
    },
    {
        "source_id": "SRC3332_9_3318_gamma_branch",
        "path": OUT / "P8_Y5_R2FR_3318_GAMMA_BRANCH_AUDIT.csv",
        "role": "Gamma readout/background versus independent local field branch",
    },
    {
        "source_id": "SRC3332_10_3318_no_pole",
        "path": OUT / "P8_Y5_R2FR_3318_NONPROPAGATION_THEOREM_ATTEMPT.csv",
        "role": "conditional no local finite Gamma pole theorem",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3332_SOURCE_REGISTER.csv",
    "budget": OUT / "P8_Y5_R2FR_3332_NORMALIZED_PPN_BUDGET.csv",
    "epsilon_eff": OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv",
    "gamma": OUT / "P8_Y5_R2FR_3332_GAMMA_FLOOR_BRANCHES.csv",
    "composite": OUT / "P8_Y5_R2FR_3332_COMPOSITE_PPN_SPECIALIZATION.csv",
    "direct_g": OUT / "P8_Y5_R2FR_3332_DIRECT_AND_G_CLOSURE_FLOORS.csv",
    "thresholds": OUT / "P8_Y5_R2FR_3332_PPN_THRESHOLD_ALLOCATION.csv",
    "gates": OUT / "P8_Y5_R2FR_3332_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3332_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3332_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3332_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def normalized_budget_rows() -> list[dict[str, Any]]:
    return [
        {
            "budget_id": "NB3332_0_master",
            "formula": "R_PPN <= |R_Gamma_PPN| + A_PPN(q_U,gauge) C_metric(lambda_PPN) epsilon_eff_PPN(lambda_PPN)^2 + epsilon_composite_PPN + epsilon_direct_PPN + epsilon_G_closure_PPN",
            "meaning": "3331 normalized PPN residual budget with every non-GR channel kept additive and non-cancelling",
            "derived_from": "3331 C_PPN composition plus 3328 local residual budget",
            "status": "PPN_FLOOR_BUDGET_SPECIALIZED",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "NB3332_1_tree_channel",
            "formula": "R_tree_PPN <= A_PPN C_metric [epsilon_bg_PPN T_grad(lambda_PPN)+epsilon_boundary_PPN+epsilon_kernel_aniso_PPN]^2",
            "meaning": "first-gradient/public-readout leakage after smoothing, normalized into PPN units",
            "derived_from": "3331 tree channel and 3321 epsilon_grad law",
            "status": "TREE_CHANNEL_SPECIALIZED",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "NB3332_2_no_cancellation_expansion",
            "formula": "R_tree_PPN <= 3 A_PPN C_metric [epsilon_bg_PPN^2 T_grad(lambda_PPN)^2 + epsilon_boundary_PPN^2 + epsilon_kernel_aniso_PPN^2]",
            "meaning": "safe positive upper bound using (a+b+c)^2 <= 3(a^2+b^2+c^2); no cancellation between background, boundary, and anisotropy is allowed",
            "derived_from": "NB3332_1 and elementary norm inequality",
            "status": "NO_CANCELLATION_TREE_BOUND",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "NB3332_3_floor_gate",
            "formula": "|R_Gamma_PPN| + epsilon_composite_PPN + epsilon_direct_PPN + epsilon_G_closure_PPN < B_PPN is required before the tree channel has any budget room",
            "meaning": "if the additive floors alone exceed the real PPN threshold, no amount of smoothing rescues the local branch",
            "derived_from": "NB3332_0",
            "status": "FLOOR_DOMINATION_GATE",
            "valid_for_claim": "false",
        },
    ]


def epsilon_eff_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EFF3332_0_transfer",
            "quantity": "T_grad(lambda_PPN)",
            "formula": "T_grad(lambda_PPN)=(ell_s/lambda_PPN) exp[-ell_s^2/(2 lambda_PPN^2)]",
            "condition": "Gaussian smoothing kernel and one-gradient leakage estimate",
            "interpretation": "shorter-than-smoothing modes are exponentially suppressed; much longer modes are suppressed only as ell_s/lambda_PPN",
            "status": "DERIVED_TRANSFER_IMPORTED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "EFF3332_1_epsilon_eff",
            "quantity": "epsilon_eff_PPN",
            "formula": "epsilon_eff_PPN <= epsilon_bg_PPN T_grad(lambda_PPN)+epsilon_boundary_PPN+epsilon_kernel_aniso_PPN",
            "condition": "first-gradient silence is imperfect but bounded",
            "interpretation": "PPN tree leakage is controlled by background gradients, local boundary leakage, and anisotropic smoothing defects",
            "status": "PPN_TREE_INPUT_SPECIALIZED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "EFF3332_2_exact_silence",
            "quantity": "tree-zero branch",
            "formula": "epsilon_bg_PPN=epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0 implies R_tree_PPN=0",
            "condition": "local first-gradient silence, boundary silence, and isotropic kernel are parent-signed in the PPN patch",
            "interpretation": "this is the clean derivation target, but it is not signed by the current corpus",
            "status": "CONDITIONAL_ZERO_BRANCH",
            "valid_for_claim": "false",
        },
        {
            "row_id": "EFF3332_3_tree_threshold",
            "quantity": "allowable epsilon_eff_PPN",
            "formula": "epsilon_eff_PPN <= sqrt(B_tree_PPN/[A_PPN C_metric]) with B_tree_PPN := B_PPN-|R_Gamma|-epsilon_composite-epsilon_direct-epsilon_G_closure",
            "condition": "B_tree_PPN>0 and real sourced B_PPN, A_PPN, C_metric",
            "interpretation": "this turns the PPN test into a required suppression amplitude once the non-tree floors are fixed",
            "status": "CLAIM_THRESHOLD_FORMULA_NONNUMERIC",
            "valid_for_claim": "false",
        },
        {
            "row_id": "EFF3332_4_background_ceiling",
            "quantity": "epsilon_bg_PPN ceiling",
            "formula": "epsilon_bg_PPN <= sqrt(B_tree_PPN/[3 A_PPN C_metric])/T_grad(lambda_PPN) if boundary and anisotropy receive separate equal no-cancellation allocations",
            "condition": "T_grad(lambda_PPN)>0 and equal tree-subbudget split",
            "interpretation": "the larger T_grad is, the smaller the allowed unresolved background-gradient amplitude becomes",
            "status": "BACKGROUND_GRADIENT_CEILING_FORMULA",
            "valid_for_claim": "false",
        },
    ]


def gamma_floor_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "GAM3332_0_readout_no_pole",
            "formula": "R_Gamma_PPN=0 for finite exchange if Gamma_G is a readout/background scalar, delta Gamma_G is not an independent local field, and local Gamma_0 is zero/constant after measured-G/cosmological-background subtraction",
            "condition": "3318 readout/background branch plus local background subtraction",
            "meaning": "Gamma does not create a PPN fifth-force pole in this branch; only a constant curvature residue can remain",
            "status": "CONDITIONAL_CLEAN_GAMMA_BRANCH",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GAM3332_1_constant_curvature",
            "formula": "R_Gamma_PPN <= A_Gamma_PPN |Gamma_local| L_PPN^2",
            "condition": "Gamma behaves as a local cosmological-constant-like curvature floor",
            "meaning": "PPN only sees a dimensionless local curvature scale over the experimental/system length",
            "status": "GENERAL_GAMMA_FLOOR",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GAM3332_2_solar_saturation_proxy",
            "formula": "R_Gamma_PPN_proxy <= A_K K_solar^m <= A_K 1e-122 for K_solar approximately 1e-61 and m>=2",
            "condition": "local Gamma residual is parent-linked to the corpus curvature-saturation proxy",
            "meaning": "this is extremely encouraging if signed, but it cannot be applied to psi/composite tails",
            "status": "ENCOURAGING_PROXY_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GAM3332_3_independent_x_rejected",
            "formula": "independent algebraic Gamma perturbation x is not used as a local-GR proof without stationarity, x^2 potential, or constraint equation",
            "condition": "3318 independent-x countercheck",
            "meaning": "prevents smuggling a Gamma zero by treating an unsourced algebraic field as harmless",
            "status": "COUNTERMODEL_GUARD",
            "valid_for_claim": "false",
        },
    ]


def composite_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "COMP3332_0_total",
            "formula": "epsilon_composite_PPN <= epsilon_1p_PPN + epsilon_2p_PPN(lambda_PPN) + epsilon_contact_PPN + epsilon_boundary_PPN + epsilon_kernel_aniso_PPN",
            "meaning": "PPN-specialized no-cancellation composite envelope",
            "condition": "all terms are positive budgets; no cancellation with tree or Gamma channels",
            "status": "COMPOSITE_FLOOR_SPECIALIZED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "COMP3332_1_effective_cells",
            "formula": "N_eff_PPN=(ell_s/ell_c_PPN)^d_eff/C_mix_PPN",
            "meaning": "number of effectively independent microscopic cells in the PPN smoothing patch",
            "condition": "finite correlation length ell_c_PPN and mixing constant C_mix_PPN",
            "status": "CLT_CELL_COUNT_IMPORTED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "COMP3332_2_one_particle",
            "formula": "epsilon_1p_PPN <= A_1P delta_comm_PPN sigma_Dpi + B_1P(C3_PPN/sqrt(N_eff_PPN)+delta_bias_PPN) sigma_Dpi^2 + rho_P1_PPN Q2_norm_PPN",
            "meaning": "mean-centering kills the first term only if the PPN projection/readout commutes with smoothing; otherwise the commutator defect delta_comm_PPN replaces delta_mean",
            "condition": "exact S_ell pi=0 plus PPN projector/gauge/readout commutation or a bounded commutator defect",
            "status": "ONE_PARTICLE_PPN_SPECIALIZED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "COMP3332_3_two_particle",
            "formula": "epsilon_2p_PPN(lambda_PPN) <= C_2P E_2p(lambda_PPN; dmu_2, m_gap_2pi), with E_2p carrying exp[-2 m_gap_2pi r_PPN] when gapped",
            "meaning": "longer-range composite loops are harmless only if a spectral gap or bandlimited falloff is supplied",
            "condition": "two-particle spectral density and gap/band envelope are source-owned",
            "status": "TWO_PARTICLE_SPECTRAL_SLOT",
            "valid_for_claim": "false",
        },
        {
            "row_id": "COMP3332_4_contact",
            "formula": "epsilon_contact_PPN <= C_contact (ell_c_PPN/L_PPN)^p_contact or an explicit renormalized local counterterm bound",
            "meaning": "short-distance composite contact terms must either shrink with scale separation or be absorbed into measured local coefficients",
            "condition": "contact scaling exponent or renormalization convention is supplied",
            "status": "CONTACT_FLOOR_BOUND_TEMPLATE",
            "valid_for_claim": "false",
        },
    ]


def direct_and_g_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DG3332_0_direct_zero_branch",
            "floor": "epsilon_direct_PPN",
            "formula": "epsilon_direct_PPN=0 if Delta S_direct[psi,Psi_m,A]=0 for f(psi)L_matter, f(psi)F^2, psi J^mu A_mu, and nonmetric Poynting-background force terms",
            "condition": "3325 metric matter/Maxwell signature is adopted for the local closure branch",
            "meaning": "EM/Poynting is allowed through T_munu^EM, not as a separate background-field force in the clean local-GR theorem",
            "status": "CONDITIONAL_DIRECT_VERTEX_SILENCE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DG3332_1_direct_nonzero_branch",
            "floor": "epsilon_direct_PPN",
            "formula": "epsilon_direct_PPN >= ||delta S_direct/delta g_PPN|| or the corresponding fifth-force/clock/optics response norm",
            "condition": "any direct psi-matter, psi-EM, or Poynting-background vertex is present",
            "meaning": "a nonmetric direct vertex exits the clean local-GR branch and must face PPN, WEP, clock, and optics constraints separately",
            "status": "DIRECT_VERTEX_QUARANTINE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DG3332_2_measured_G_closure",
            "floor": "epsilon_G_closure_PPN",
            "formula": "epsilon_G_closure_PPN=0 in the declared measured-G closure where kappa_eff=8 pi G_N/c^4 and GM/source mass are calibrated before residual scoring",
            "condition": "3324 measured-G closure branch; no claim that G_N is derived",
            "meaning": "this is the honest local GR/Newton route: use measured G for the leading slot and test MTS only in residuals",
            "status": "MEASURED_G_CLOSURE_ZERO",
            "valid_for_claim": "false",
        },
        {
            "row_id": "DG3332_3_derived_G_branch",
            "floor": "epsilon_G_closure_PPN",
            "formula": "epsilon_G_closure_PPN >= |kappa_ind/kappa_N - 1| plus any source-normalization mismatch if the theory claims to derive G_N",
            "condition": "derived-G/induced-EH branch is attempted instead of measured-G closure",
            "meaning": "deriving Newton's constant is a deeper future target; until C_EH^ind is computed, it should not be mixed into the PPN local-GR claim",
            "status": "DERIVED_G_BRANCH_BLOCKED",
            "valid_for_claim": "false",
        },
    ]


def threshold_rows() -> list[dict[str, Any]]:
    return [
        {
            "threshold_id": "THR3332_0_budget_partition",
            "formula": "Choose positive fractions f_Gamma+f_tree+f_comp+f_direct+f_G=1 and require each floor <= f_i B_PPN",
            "purpose": "turns the no-cancellation PPN budget into independently checkable component gates",
            "claim_requirement": "real sourced B_PPN vector and component-specific allocation policy",
            "status": "ALLOCATION_RULE",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "THR3332_1_tree",
            "formula": "3 A_PPN C_metric [epsilon_bg^2 T_grad^2 + epsilon_boundary^2 + epsilon_kernel_aniso^2] <= f_tree B_PPN",
            "purpose": "tree leakage pass/fail gate after q_U normalization",
            "claim_requirement": "numeric A_PPN, C_metric, lambda_PPN, ell_s, and epsilon terms",
            "status": "TREE_GATE_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "THR3332_2_composite",
            "formula": "epsilon_1p+epsilon_2p+epsilon_contact+epsilon_boundary+epsilon_kernel_aniso <= f_comp B_PPN",
            "purpose": "composite leakage pass/fail gate",
            "claim_requirement": "CLT/mixing, spectral gap, contact, boundary, and anisotropy inputs",
            "status": "COMPOSITE_GATE_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "threshold_id": "THR3332_3_zero_floor_order",
            "formula": "first try to sign epsilon_direct=0 and epsilon_G_closure=0; then sign Gamma no-pole/proxy; only then spend tokens on numeric tree/composite fitting",
            "purpose": "best route of attack because direct/G floors can kill the clean branch before any smoothing calculation matters",
            "claim_requirement": "branch signatures remain explicit and not public-claimed",
            "status": "ROUTE_PRIORITY",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3332_0_budget_specialized",
            "claim": "normalized PPN budget has all floor terms separated",
            "passed": "true",
            "reason": "tree, Gamma, composite, direct, and G-closure channels are explicit and additive",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3332_1_tree_threshold_formula",
            "claim": "epsilon_eff_PPN has a q_U-normalized threshold formula",
            "passed": "true",
            "reason": "epsilon_eff <= sqrt(B_tree/(A_PPN C_metric)) and T_grad background ceiling are recorded",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3332_2_composite_specialized",
            "claim": "PPN composite floor is specialized beyond a generic missing note",
            "passed": "true",
            "reason": "one-particle commutator defect, CLT suppression, two-particle spectral tail, and contact floor are separated",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3332_3_zero_branches_identified",
            "claim": "direct-vertex and measured-G closure zero branches are explicit",
            "passed": "true",
            "reason": "epsilon_direct=0 and epsilon_G_closure=0 are allowed only under named branch signatures",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3332_4_PPN_numeric_pass",
            "claim": "PPN/local-GR residual is numerically below threshold",
            "passed": "false",
            "reason": "real B_PPN, A_PPN, C_metric, epsilon inputs, spectral inputs, and Gamma mapping are not numeric/source-owned here",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3332_5_local_GR_claim",
            "claim": "local GR/PPN pass is claim-ready",
            "passed": "false",
            "reason": "3332 is a derivation/gating checkpoint, not an empirical PPN comparator",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3332_0",
            "question": "Did 3332 improve the project?",
            "answer": "yes",
            "reason": "the local PPN problem is now a concrete no-cancellation residual budget with independent kill/pass gates rather than a vague coefficient hunt",
            "next_action": "try to sign the two cheapest zero floors: measured-G closure and direct-vertex silence",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3332_1",
            "question": "What is the riskiest remaining branch?",
            "answer": "composite and direct vertices",
            "reason": "Gamma has an encouraging proxy and measured-G closure can set the Newtonian slot, but unbounded composite or direct psi-matter/EM coupling would immediately re-open local tests",
            "next_action": "derive a PPN branch certificate that epsilon_direct=0 and epsilon_G_closure=0 under the clean local theorem, then isolate composite as the dominant open floor",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3332_2",
            "question": "What should not be claimed?",
            "answer": "PPN pass, derived Newton constant, or microscopic matter descent",
            "reason": "3332 gives the formula architecture and zero-branch conditions, not source-grade numeric bounds",
            "next_action": "keep public-facing claims blocked until a real threshold comparator is run",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3333-Y5-R2FR-PPN-zero-floor-branch-certificate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3333_PPN_zero_floor_branch_certificate.py",
            "objective": "attempt to sign epsilon_direct_PPN=0 and epsilon_G_closure_PPN=0 for the clean measured-G local-GR branch, and decide whether Gamma can be kept on the no-pole/proxy branch",
            "must_include": "standard metric matter/Maxwell stress route; explicit forbidden direct vertices; measured-G closure scope; no derived-G claim; Gamma readout/no-pole branch; failover to residual floors if any clause is unsigned",
            "fallback_if_failed": "retain direct and G-closure floors in the PPN budget and move to numeric source-bound acquisition only after declaring the clean branch incomplete",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    budget = normalized_budget_rows()
    eff = epsilon_eff_rows()
    gamma = gamma_floor_rows()
    comp = composite_rows()
    direct_g = direct_and_g_rows()
    thresholds = threshold_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3332_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3332_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3332_2_outputs_parse",
            "check": "all 3332 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3332_3_budget_terms",
            "check": "budget includes Gamma, tree, composite, direct, and G closure terms",
            "passed": any("R_Gamma_PPN" in row["formula"] and "epsilon_composite_PPN" in row["formula"] and "epsilon_direct_PPN" in row["formula"] and "epsilon_G_closure_PPN" in row["formula"] for row in budget),
            "detail": "",
        },
        {
            "check_id": "VAL3332_4_epsilon_eff",
            "check": "epsilon_eff specialization includes T_grad, threshold, and no-cancellation tree expansion",
            "passed": any("T_grad(lambda_PPN)" in row["formula"] for row in eff)
            and any("sqrt(B_tree_PPN" in row["formula"] for row in eff)
            and any("epsilon_bg_PPN^2" in row["formula"] for row in budget),
            "detail": "",
        },
        {
            "check_id": "VAL3332_5_gamma_branches",
            "check": "Gamma floor has no-pole, constant-curvature, proxy, and independent-x guard branches",
            "passed": {"GAM3332_0_readout_no_pole", "GAM3332_1_constant_curvature", "GAM3332_2_solar_saturation_proxy", "GAM3332_3_independent_x_rejected"}.issubset(
                {row["branch_id"] for row in gamma}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3332_6_composite_ppn",
            "check": "composite floor includes CLT, commutator, spectral, and contact pieces",
            "passed": any("delta_comm_PPN" in row["formula"] for row in comp)
            and any("N_eff_PPN" in row["formula"] for row in comp)
            and any("m_gap_2pi" in row["formula"] for row in comp)
            and any("epsilon_contact_PPN" in row["formula"] for row in comp),
            "detail": "",
        },
        {
            "check_id": "VAL3332_7_direct_and_G",
            "check": "direct vertex and measured-G closure branches are explicit",
            "passed": any("epsilon_direct_PPN=0" in row["formula"] for row in direct_g)
            and any("epsilon_G_closure_PPN=0" in row["formula"] for row in direct_g)
            and any("kappa_ind/kappa_N" in row["formula"] for row in direct_g),
            "detail": "",
        },
        {
            "check_id": "VAL3332_8_thresholds",
            "check": "threshold allocation includes component fractions and route priority",
            "passed": any("f_Gamma" in row["formula"] for row in thresholds)
            and any("f_tree" in row["formula"] for row in thresholds)
            and any("first try" in row["formula"] for row in thresholds),
            "detail": "",
        },
        {
            "check_id": "VAL3332_9_no_claim",
            "check": "symbolic gates pass while numeric PPN/local-GR claims remain false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3332_0_budget_specialized", "GATE3332_1_tree_threshold_formula", "GATE3332_2_composite_specialized", "GATE3332_3_zero_branches_identified"}
            )
            and all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3332_4_PPN_numeric_pass", "GATE3332_5_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3332_10_next_3333",
            "check": "next target is zero-floor branch certificate",
            "passed": any("epsilon_direct_PPN=0" in row["objective"] and "epsilon_G_closure_PPN=0" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3332_11_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3332_12_overall",
            "check": "3332 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3332 - PPN epsilon_eff and floor specialization under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3332 turns the normalized PPN branch into a no-cancellation floor budget.",
        "",
        "The working inequality is",
        "",
        "`R_PPN <= |R_Gamma_PPN| + A_PPN(q_U,gauge) C_metric(lambda_PPN) epsilon_eff_PPN(lambda_PPN)^2 + epsilon_composite_PPN + epsilon_direct_PPN + epsilon_G_closure_PPN`.",
        "",
        "The tree channel is now",
        "",
        "`R_tree_PPN <= A_PPN C_metric [epsilon_bg_PPN T_grad(lambda_PPN)+epsilon_boundary_PPN+epsilon_kernel_aniso_PPN]^2`,",
        "",
        "with",
        "",
        "`T_grad(lambda_PPN)=(ell_s/lambda_PPN) exp[-ell_s^2/(2 lambda_PPN^2)]`.",
        "",
        "A safe no-cancellation expansion is",
        "",
        "`R_tree_PPN <= 3 A_PPN C_metric [epsilon_bg_PPN^2 T_grad(lambda_PPN)^2 + epsilon_boundary_PPN^2 + epsilon_kernel_aniso_PPN^2]`.",
        "",
        "The key floor gate is brutal and useful:",
        "",
        "`|R_Gamma_PPN| + epsilon_composite_PPN + epsilon_direct_PPN + epsilon_G_closure_PPN < B_PPN`",
        "",
        "must hold before smoothing the tree channel can help.",
        "",
        "This gives the next best route: first try to sign the clean zero floors `epsilon_direct_PPN=0` and `epsilon_G_closure_PPN=0`; then keep Gamma on the no-pole/proxy branch if possible; then spend effort on tree/composite numeric bounds.",
        "",
        "No PPN/local-GR claim follows from 3332.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Normalized PPN Budget", normalized_budget_rows(), "budget_id"),
        ("Epsilon Eff Specialization", epsilon_eff_rows(), "row_id"),
        ("Gamma Floor Branches", gamma_floor_rows(), "branch_id"),
        ("Composite PPN Specialization", composite_rows(), "row_id"),
        ("Direct And G Closure Floors", direct_and_g_rows(), "row_id"),
        ("PPN Threshold Allocation", threshold_rows(), "threshold_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It specializes the PPN residual architecture rather than sourcing observational PPN thresholds.",
            "- It explicitly separates clean branch zeros from unproved microscopic derivations.",
            "- It keeps Maxwell/Poynting inside metric `T_munu^EM` for the local-GR branch and quarantines direct background-force vertices.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["budget"], normalized_budget_rows())
    write_csv(OUTPUTS["epsilon_eff"], epsilon_eff_rows())
    write_csv(OUTPUTS["gamma"], gamma_floor_rows())
    write_csv(OUTPUTS["composite"], composite_rows())
    write_csv(OUTPUTS["direct_g"], direct_and_g_rows())
    write_csv(OUTPUTS["thresholds"], threshold_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
