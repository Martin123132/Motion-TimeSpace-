from __future__ import annotations

import csv
import hashlib
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

DOC = ROOT / "3338-Y5-R2FR-PPN-projector-patch-geometry-source-contract-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3338_0_3337_doc",
        "path": ROOT / "3337-Y5-R2FR-PPN-commutator-contact-zero-or-bound-theorem-under-AX1090.md",
        "role": "3337 handoff for commutator/contact theorem",
    },
    {
        "source_id": "SRC3338_1_3337_commutator",
        "path": OUT / "P8_Y5_R2FR_3337_COMMUTATOR_THEOREM.csv",
        "role": "delta_comm exact-zero and bound theorem",
    },
    {
        "source_id": "SRC3338_2_3337_contact",
        "path": OUT / "P8_Y5_R2FR_3337_CONTACT_THEOREM.csv",
        "role": "contact zero-or-scale theorem",
    },
    {
        "source_id": "SRC3338_3_3337_requirements",
        "path": OUT / "P8_Y5_R2FR_3337_REQUIRED_INPUTS.csv",
        "role": "projector, patch, boundary, contact, and spectral missing inputs",
    },
    {
        "source_id": "SRC3338_4_3336_thresholds",
        "path": OUT / "P8_Y5_R2FR_3336_PPN_THRESHOLD_CANDIDATES.csv",
        "role": "Cassini gamma candidate steering threshold",
    },
    {
        "source_id": "SRC3338_5_3336_web_sources",
        "path": OUT / "P8_Y5_R2FR_3336_WEB_SOURCE_REGISTER.csv",
        "role": "Cassini and Will PPN source references already recorded",
    },
    {
        "source_id": "SRC3338_6_3331_cmetric",
        "path": OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv",
        "role": "PPN gauge/projector slot and C_metric factorization",
    },
    {
        "source_id": "SRC3338_7_3332_composite",
        "path": OUT / "P8_Y5_R2FR_3332_COMPOSITE_PPN_SPECIALIZATION.csv",
        "role": "PPN composite budget template",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3338_SOURCE_REGISTER.csv",
    "projector": OUT / "P8_Y5_R2FR_3338_PPN_PROJECTOR_CONTRACT.csv",
    "patch": OUT / "P8_Y5_R2FR_3338_PATCH_GEOMETRY_DERIVATION.csv",
    "scale_solver": OUT / "P8_Y5_R2FR_3338_PATCH_SCALE_SOLVER.csv",
    "contact": OUT / "P8_Y5_R2FR_3338_CONTACT_UNIVERSALITY_CONTRACT.csv",
    "acquisition": OUT / "P8_Y5_R2FR_3338_SOURCE_ACQUISITION_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3338_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3338_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3338_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3338_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
B_GAMMA = 2.3e-5
F_COMP = 0.30
B_COMP = F_COMP * B_GAMMA
SIGMA_DPI_REF = 1.0e-3
DELTA_COMM_ALLOWED = B_COMP / SIGMA_DPI_REF

R_SUN_NOMINAL_M = 6.957e8
AU_EXACT_M = 149_597_870_700.0


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


def source_rows() -> list[dict[str, Any]]:
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


def projector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PPROJ3338_0_gamma_trace_readout",
            "slot": "PPN gamma",
            "local_projector": "P_gamma[h,U] := delta^{ij} h_ij/(6 U) - 1",
            "derivation": "In isotropic PPN gauge, g_ij = delta_ij(1+2 gamma U)+O(U^2), so h_ij=g_ij-delta_ij and delta^{ij}h_ij=6 gamma U; subtracting 1 scores gamma-1 against GR.",
            "conditions": "weak-field isotropic PPN gauge; calibrated Newtonian potential U=G_N M/(c^2 r); source GM mode is fixed before residual scoring",
            "fourier_symbol": "on a frozen interior patch U=U0, P_gamma has constant symbol delta^{ij}/(6 U0) on the spatial-trace component",
            "commutator_status": "FOURIER_MULTIPLIER_BRANCH_IF_U_FROZEN",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PPROJ3338_1_beta_temporal_readout",
            "slot": "PPN beta",
            "local_projector": "P_beta[h00,U] := (2 U - h00)/(2 U^2) - 1",
            "derivation": "With g_00=-1+2U-2 beta U^2+O(U^3), h00=g_00+1, so beta=(2U-h00)/(2U^2); subtracting 1 scores beta-1.",
            "conditions": "same source U and gauge convention as gamma; higher-order terms must be separated from MTS residuals",
            "fourier_symbol": "constant local coefficient if U is frozen to U0; otherwise coefficient varies on L_var=U/|grad U|",
            "commutator_status": "SECONDARY_SLOT_NOT_CASSINI_PRIMARY",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PPROJ3338_2_gm_absorption_guard",
            "slot": "Newtonian source calibration",
            "local_projector": "project out pure GM/source-normalization shifts before PPN residual scoring",
            "derivation": "Measured G_N and the source mass define U. A residual that only rescales U is Newtonian calibration, not a gamma/beta anomaly.",
            "conditions": "MTS residual is evaluated after the Newtonian slot is fixed; no hidden re-fit inside the PPN projector",
            "fourier_symbol": "removes the source normalization mode from the residual vector",
            "commutator_status": "REQUIRED_FOR_NO_DOUBLE_COUNTING",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PPROJ3338_3_exact_commutator_route",
            "slot": "projector/smoothing compatibility",
            "local_projector": "P_PPN(k) S_ell(k)=S_ell(k) P_PPN(k) after local freezing and gauge fixing",
            "derivation": "The 3337 theorem applies if the readout map is a constant-coefficient projector on the patch and S_ell is scalar/isotropic in the PPN band.",
            "conditions": "interior patch; frozen U0; constant tetrad/frame; scalar smoothing kernel; no boundary leakage",
            "fourier_symbol": "matrix P_PPN(k) times scalar s_ell(k)",
            "commutator_status": "DELTA_COMM_ZERO_CONDITION",
            "valid_for_claim": "false",
        },
    ]


def patch_geometry_rows() -> list[dict[str, Any]]:
    return [
        {
            "geometry_id": "PGEOM3338_0_variation_length_general",
            "quantity": "L_var",
            "formula": "L_var := U/|grad U| for the PPN readout coefficient 1/U",
            "derivation": "The gamma projector coefficient is proportional to 1/U, so |grad ln(1/U)|=|grad U|/U; the inverse logarithmic gradient is the commutator variation scale.",
            "source_status": "DERIVED_FROM_PROJECTOR_CONTRACT",
            "valid_for_claim": "false",
        },
        {
            "geometry_id": "PGEOM3338_1_monopole_reduction",
            "quantity": "solar-system monopole L_var",
            "formula": "if U=G_N M/(c^2 r), then L_var=r",
            "derivation": "|grad U|=U/r for a monopole exterior, hence U/|grad U|=r; along a ray the minimum scale is the impact parameter b.",
            "source_status": "NEEDS_CASSINI_GEOMETRY_SOURCE_FOR_b",
            "valid_for_claim": "false",
        },
        {
            "geometry_id": "PGEOM3338_2_boundary_tail",
            "quantity": "boundary leakage",
            "formula": "epsilon_boundary_comm <= C_boundary exp[-d_boundary^2/(2 ell_s^2)]",
            "derivation": "A Gaussian or similarly localized smoothing kernel loses mass across a patch boundary only through its tail outside the interior support.",
            "source_status": "KERNEL_CONVENTION_NEEDED",
            "valid_for_claim": "false",
        },
        {
            "geometry_id": "PGEOM3338_3_commutator_requirement",
            "quantity": "smoothing-to-variation ratio",
            "formula": "ell_s/L_var <= (delta_comm_allowed - boundary_tail - epsilon_gauge_res)/C_comm",
            "derivation": "Insert the 3337 bound delta_comm <= C_comm ell_s/L_var + boundary_tail + epsilon_gauge_res into the 3336 Cassini-gamma composite allocation.",
            "source_status": "NUMERIC_STEERING_FROM_3336_3337",
            "valid_for_claim": "false",
        },
        {
            "geometry_id": "PGEOM3338_4_contact_scale_requirement",
            "quantity": "contact correlation ratio",
            "formula": "ell_c/L_PPN <= (B_comp/C_contact)^(1/p_contact)",
            "derivation": "Rearrange epsilon_contact <= C_contact(ell_c/L_PPN)^p_contact and require it below the 3336 composite budget B_comp.",
            "source_status": "NUMERIC_STEERING_FROM_3337",
            "valid_for_claim": "false",
        },
    ]


def scale_solver_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    comm_scenarios = [
        ("SOLVE3338_comm_C1_clean", 1.0, 0.0, 0.0, "generic clean interior patch"),
        ("SOLVE3338_comm_C2_clean", 2.0, 0.0, 0.0, "moderate projector variation constant"),
        ("SOLVE3338_comm_C2_boundary", 2.0, 9.0e-4, 0.0, "uses 3337 ceiling-edge boundary allocation"),
        ("SOLVE3338_comm_C2_gauge", 2.0, 9.0e-4, 1.0e-3, "boundary plus residual gauge leakage"),
        ("SOLVE3338_comm_fail_boundary", 2.0, 7.0e-3, 0.0, "boundary already exceeds composite allocation"),
    ]
    for row_id, c_comm, boundary, eps_gauge, comment in comm_scenarios:
        numerator = DELTA_COMM_ALLOWED - boundary - eps_gauge
        ell_over_l_allowed = max(0.0, numerator / c_comm) if c_comm > 0 else math.inf
        rows.append(
            {
                "solver_id": row_id,
                "kind": "commutator_patch",
                "C_comm": f"{c_comm:.6e}",
                "boundary_tail": f"{boundary:.6e}",
                "epsilon_gauge_res": f"{eps_gauge:.6e}",
                "allowed_ratio": f"{ell_over_l_allowed:.6e}",
                "allowed_ell_s_if_Lvar_Rsun_m": f"{ell_over_l_allowed * R_SUN_NOMINAL_M:.6e}",
                "allowed_ell_s_if_Lvar_AU_m": f"{ell_over_l_allowed * AU_EXACT_M:.6e}",
                "budget": f"{DELTA_COMM_ALLOWED:.6e}",
                "passes_possible": bool_str(numerator > 0.0),
                "source_note": "R_sun/AU columns are nonclaim steering constants; source official constants before claim",
                "comment": comment,
                "valid_for_claim": "false",
            }
        )
    for power in (2, 4):
        allowed = (B_COMP ** (1.0 / power))
        rows.append(
            {
                "solver_id": f"SOLVE3338_contact_p{power}",
                "kind": "contact_scale",
                "C_contact": f"{1.0:.6e}",
                "p_contact": power,
                "allowed_ratio": f"{allowed:.6e}",
                "allowed_ell_c_if_Lppn_Rsun_m": f"{allowed * R_SUN_NOMINAL_M:.6e}",
                "allowed_ell_c_if_Lppn_AU_m": f"{allowed * AU_EXACT_M:.6e}",
                "budget": f"{B_COMP:.6e}",
                "passes_possible": "true",
                "source_note": "claim requires parent-owned ell_c and C_contact, not these steering scales",
                "comment": "contact scale-separation ceiling from 3337 theorem",
                "valid_for_claim": "false",
            }
        )
    return rows


def contact_universality_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "CUNI3338_0_absorbable_metric_contact",
            "condition": "contact tensor is universal and proportional to the same metric/Newtonian source tensor used to define measured G_N",
            "result": "epsilon_contact_PPN=0 after source calibration",
            "failure_mode": "none if no species, spin, orientation, or nonmetric residue survives",
            "needed_source": "parent coupling/current tensor decomposition",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CUNI3338_1_derivative_contact",
            "condition": "zeroth contact is absorbed but derivative finite-size residue remains analytic and isotropic",
            "result": "epsilon_contact_PPN <= C_contact(ell_c/L_PPN)^p_contact with p>=2, or p>=4 if second-order term is also forbidden/absorbed",
            "failure_mode": "large ell_c/L_PPN or unsourced C_contact leaves explicit floor",
            "needed_source": "ell_c, C_contact, p_contact from parent branch or empirical upper bound",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CUNI3338_2_nonuniversal_contact",
            "condition": "contact carries composition-dependent, nonmetric, spin, orientation, or clock-channel structure",
            "result": "cannot be absorbed into local G_N; becomes a WEP/clock/PPN residual source",
            "failure_mode": "local-GR branch blocked unless externally bounded below relevant experiment limits",
            "needed_source": "WEP/clock/orbital projection of the nonuniversal tensor",
            "valid_for_claim": "false",
        },
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "ACQ3338_0_Will_PPN_metric_convention",
            "quantity": "PPN metric convention for gamma and beta readouts",
            "current_status": "SOURCE_REFERENCE_RECORDED_IN_3336_WEB_REGISTER",
            "required_action": "quote/check exact sign and normalization convention against Will LRR before public use",
            "claim_blocker": "gamma/beta projector not source-owned in final notation",
            "valid_for_claim": "false",
        },
        {
            "input_id": "ACQ3338_1_Cassini_geometry",
            "quantity": "Cassini solar-conjunction impact parameter b and observable mapping to gamma",
            "current_status": "THRESHOLD_RECORDED_BUT_GEOMETRY_NOT_EXTRACTED",
            "required_action": "extract b/range geometry from Cassini source or use a conservative b>=R_sun bound with source",
            "claim_blocker": "L_var numerical floor not source-owned",
            "valid_for_claim": "false",
        },
        {
            "input_id": "ACQ3338_2_official_length_constants",
            "quantity": "R_sun, AU, and any solar-system patch scale constants",
            "current_status": "NONCLAIM_STEERING_VALUES_USED_IN_SOLVER",
            "required_action": "record official IAU/CODATA source rows before promoting any numeric scale",
            "claim_blocker": "length scale source provenance incomplete",
            "valid_for_claim": "false",
        },
        {
            "input_id": "ACQ3338_3_MTS_smoothing_length",
            "quantity": "ell_s used by the local PPN branch",
            "current_status": "PARENT_BRANCH_MISSING",
            "required_action": "derive ell_s from parent action/coarse-graining or define it as a bounded regulator with physical source",
            "claim_blocker": "cannot evaluate ell_s/L_var",
            "valid_for_claim": "false",
        },
        {
            "input_id": "ACQ3338_4_MTS_contact_length",
            "quantity": "ell_c, C_contact, and p_contact",
            "current_status": "PARENT_BRANCH_MISSING",
            "required_action": "derive from contact/current tensor or fit-independent parent correlation scale",
            "claim_blocker": "cannot evaluate contact floor",
            "valid_for_claim": "false",
        },
        {
            "input_id": "ACQ3338_5_contact_tensor_universality",
            "quantity": "whether contact/source coupling is universal metric or nonuniversal",
            "current_status": "PARENT_SIGNATURE_NEEDED",
            "required_action": "decompose source coupling into metric trace, traceless, species, spin, and clock components",
            "claim_blocker": "absorption into measured G_N not proven",
            "valid_for_claim": "false",
        },
        {
            "input_id": "ACQ3338_6_spectral_tail_after_composite_cleanup",
            "quantity": "two-particle spectral gap/tail in PPN band",
            "current_status": "STILL_MISSING_FROM_3337",
            "required_action": "bound epsilon_2p or prove gap/band suppression after patch geometry is fixed",
            "claim_blocker": "remaining composite floor not closed",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3338_0_gamma_projector_defined",
            "claim": "PPN gamma projector/readout is explicitly defined",
            "passed": "true",
            "reason": "gamma readout P_gamma[h,U]=delta^{ij}h_ij/(6U)-1 is derived from isotropic PPN form",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3338_1_Lvar_derived",
            "claim": "PPN readout variation scale is derived",
            "passed": "true",
            "reason": "L_var=U/|grad U| and monopole exterior gives L_var=r, with impact parameter b as local minimum",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3338_2_scale_solver_present",
            "claim": "commutator/contact ceilings have explicit allowed ratios",
            "passed": "true",
            "reason": "solver rows convert 3336/3337 budgets into ell_s/L_var and ell_c/L_PPN ceilings",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3338_3_numeric_claim_ready",
            "claim": "PPN patch geometry is numerically source-owned",
            "passed": "false",
            "reason": "Cassini geometry, official constants, ell_s, ell_c, C_contact, and contact tensor signature remain unpromoted",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3338_4_local_GR_claim",
            "claim": "MTS local-GR/PPN branch is claim-ready",
            "passed": "false",
            "reason": "3338 defines the projector and derives scale requirements, but does not supply parent smoothing/contact/spectral inputs",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3338_0",
            "question": "Did 3338 move beyond a missing-input ledger?",
            "answer": "yes",
            "reason": "it derives the gamma projector, shows L_var=U/|grad U|, reduces solar monopole variation to L_var=r, and solves allowed scale ratios",
            "next_action": "derive parent ell_s/ell_c/contact universality or source them from the MTS parent branch",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3338_1",
            "question": "Is the commutator scary after the patch derivation?",
            "answer": "conditionally not",
            "reason": "if ell_s is microscopic or even modestly smaller than the solar-system variation scale, ell_s/L_var can sit below the 3337 ceiling; if ell_s is astronomical, it fails",
            "next_action": "stop treating ell_s as vague; derive its physical value or bound",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3338_2",
            "question": "What is the new real bottleneck?",
            "answer": "parent source coupling and correlation scales",
            "reason": "the PPN projector geometry is now mostly a contract; the missing physics is whether the MTS contact/coupling is universal metric and what ell_s/ell_c are",
            "next_action": "build 3339 parent coupling decomposition into metric trace, traceless, spin/species, and clock channels",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3339-Y5-R2FR-parent-source-coupling-decomposition-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3339_parent_source_coupling_decomposition.py",
            "objective": "decompose the MTS source/contact coupling into universal metric trace, traceless metric, species/spin, clock, and boundary channels; derive whether measured-G absorption is legitimate",
            "must_include": "contact tensor signature; ell_s and ell_c ownership; WEP/clock risk routing; no local-GR claim unless nonmetric residues vanish or are source-bounded",
            "fallback_if_failed": "retain explicit source-coupling floor and move to empirical local bound acquisition",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    projector = projector_contract_rows()
    patch = patch_geometry_rows()
    solver = scale_solver_rows()
    contact = contact_universality_rows()
    acquisition = acquisition_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3338_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3338_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3338_2_outputs_parse",
            "check": "all 3338 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3338_3_gamma_projector",
            "check": "gamma projector includes trace/(6U)-1 and Fourier frozen-patch symbol",
            "passed": any("delta^{ij} h_ij/(6 U) - 1" in row["local_projector"] and "U0" in row["fourier_symbol"] for row in projector),
            "detail": "",
        },
        {
            "check_id": "VAL3338_4_Lvar_monopole",
            "check": "patch geometry derives L_var=U/|grad U| and monopole L_var=r",
            "passed": any("U/|grad U|" in row["formula"] for row in patch) and any("L_var=r" in row["formula"] for row in patch),
            "detail": "",
        },
        {
            "check_id": "VAL3338_5_scale_solver",
            "check": "solver includes commutator and contact allowed ratios with pass/fail cases",
            "passed": any(row["kind"] == "commutator_patch" and row["passes_possible"] == "false" for row in solver)
            and any(row["kind"] == "commutator_patch" and row["passes_possible"] == "true" for row in solver)
            and any(row["kind"] == "contact_scale" and int(row["p_contact"]) == 2 for row in solver)
            and any(row["kind"] == "contact_scale" and int(row["p_contact"]) == 4 for row in solver),
            "detail": "",
        },
        {
            "check_id": "VAL3338_6_contact_universality",
            "check": "contact contract distinguishes absorbable metric, derivative, and nonuniversal branches",
            "passed": {"CUNI3338_0_absorbable_metric_contact", "CUNI3338_1_derivative_contact", "CUNI3338_2_nonuniversal_contact"}.issubset(
                {row["contract_id"] for row in contact}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3338_7_acquisition_rows",
            "check": "acquisition rows include source convention, Cassini geometry, constants, ell_s, ell_c, contact tensor, and spectral tail",
            "passed": {"ACQ3338_0_Will_PPN_metric_convention", "ACQ3338_1_Cassini_geometry", "ACQ3338_2_official_length_constants", "ACQ3338_3_MTS_smoothing_length", "ACQ3338_4_MTS_contact_length", "ACQ3338_5_contact_tensor_universality", "ACQ3338_6_spectral_tail_after_composite_cleanup"}.issubset(
                {row["input_id"] for row in acquisition}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3338_8_no_claim",
            "check": "local-GR and numeric claim gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3338_3_numeric_claim_ready", "GATE3338_4_local_GR_claim"}
            )
            and all(row.get("valid_for_claim", "false") == "false" for row in projector + patch + solver + contact + acquisition + gates),
            "detail": "",
        },
        {
            "check_id": "VAL3338_9_next_3339",
            "check": "next target attacks parent source coupling rather than another missing ledger",
            "passed": any("source-coupling" in row["objective"] or "source/contact coupling" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3338_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3338_11_overall",
            "check": "3338 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3338 - PPN projector/patch geometry source contract under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3338 turns the PPN patch problem into a concrete contract rather than another missing-input list.",
        "",
        "The gamma readout branch is now explicit:",
        "",
        "`P_gamma[h,U] := delta^{ij} h_ij/(6 U) - 1`",
        "",
        "on a weak-field isotropic PPN patch with the Newtonian potential `U` already fixed by measured local `G_N M`.",
        "",
        "Freezing `U=U0` on an interior patch makes the gamma readout a constant-coefficient Fourier multiplier, so the 3337 commutator-zero theorem can apply.",
        "",
        "If `U` is not frozen, the variation scale is not mysterious:",
        "",
        "`L_var := U/|grad U|`",
        "",
        "and for an exterior solar monopole `U=G_N M/(c^2 r)`, this reduces to:",
        "",
        "`L_var = r`",
        "",
        "so a Cassini-like near-Sun path uses the impact parameter as the conservative local variation scale.",
        "",
        f"Using the 3336/3337 private steering budget gives `delta_comm_allowed = {DELTA_COMM_ALLOWED:.3e}` and `B_comp = {B_COMP:.3e}`.",
        "",
        "That converts the geometry into two real inequalities:",
        "",
        "`ell_s/L_var <= (delta_comm_allowed - boundary_tail - epsilon_gauge_res)/C_comm`",
        "",
        "`ell_c/L_PPN <= (B_comp/C_contact)^(1/p_contact)`",
        "",
        "This does not claim local GR/PPN success, but it tells us exactly what physical lengths and coupling signatures must be derived next.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("PPN Projector Contract", projector_contract_rows(), "contract_id"),
        ("Patch Geometry Derivation", patch_geometry_rows(), "geometry_id"),
        ("Patch Scale Solver", scale_solver_rows(), "solver_id"),
        ("Contact Universality Contract", contact_universality_rows(), "contract_id"),
        ("Source Acquisition Rows", acquisition_rows(), "input_id"),
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
            "- It derives the PPN gamma readout and patch scale law, but it does not supply parent-owned `ell_s`, `ell_c`, or contact tensor signatures.",
            "- The `R_sun` and `AU` numerical columns are steering scales only until official source rows are attached.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["projector"], projector_contract_rows())
    write_csv(OUTPUTS["patch"], patch_geometry_rows())
    write_csv(OUTPUTS["scale_solver"], scale_solver_rows())
    write_csv(OUTPUTS["contact"], contact_universality_rows())
    write_csv(OUTPUTS["acquisition"], acquisition_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
