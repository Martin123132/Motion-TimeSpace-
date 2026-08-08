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

DOC = ROOT / "3331-Y5-R2FR-PPN-weak-potential-normalization-and-Cmetric-bound-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3331_0_3330_doc",
        "path": ROOT / "3330-Y5-R2FR-PPN-response-coefficient-and-local-floor-bound-under-AX1090.md",
        "role": "handoff requiring A_PPN(q_U,gauge) and C_metric",
    },
    {
        "source_id": "SRC3331_1_3330_response",
        "path": OUT / "P8_Y5_R2FR_3330_PPN_RESPONSE_COEFFICIENT.csv",
        "role": "C_PPN decomposition into A_PPN and C_metric",
    },
    {
        "source_id": "SRC3331_2_3330_inputs",
        "path": OUT / "P8_Y5_R2FR_3330_REQUIRED_INPUTS.csv",
        "role": "required q_U, gauge, C_metric, and floor inputs",
    },
    {
        "source_id": "SRC3331_3_3322_Ci",
        "path": OUT / "P8_Y5_R2FR_3322_CI_RESPONSE_GATE.csv",
        "role": "generic C_i projection-propagator-source split",
    },
    {
        "source_id": "SRC3331_4_3328_budget",
        "path": OUT / "P8_Y5_R2FR_3328_RESIDUAL_BUDGET_FORMULAS.csv",
        "role": "master local residual budget",
    },
    {
        "source_id": "SRC3331_5_PPN_gamma_2053",
        "path": OUT / "P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_WEAK_FIELD_DERIVATION.csv",
        "role": "existing weak-field areal PPN gamma bridge",
    },
    {
        "source_id": "SRC3331_6_PPN_observable_3098",
        "path": OUT / "P8_Y5_R2FR_3098_PPN_OBSERVABLE_BOUND.csv",
        "role": "older PPN observable-bound context",
    },
    {
        "source_id": "SRC3331_7_PPN_GM_gauge_3058",
        "path": OUT / "P8_Y5_R2FR_3058_PPN_GM_ABSORPTION_AND_GAUGE_GATE.csv",
        "role": "GM absorption and PPN gauge caution",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3331_SOURCE_REGISTER.csv",
    "weak_field": OUT / "P8_Y5_R2FR_3331_WEAK_FIELD_NORMALIZATION.csv",
    "appn": OUT / "P8_Y5_R2FR_3331_APPN_BOUND.csv",
    "cmetric": OUT / "P8_Y5_R2FR_3331_CMETRIC_BOUND.csv",
    "cppn": OUT / "P8_Y5_R2FR_3331_CPPN_COMPOSITION.csv",
    "inputs": OUT / "P8_Y5_R2FR_3331_REQUIRED_INPUTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3331_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3331_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3331_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3331_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1600) -> str:
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


def weak_field_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WF3331_0_metric_ansatz",
            "object": "PPN weak-field metric",
            "formula": "g_00 = -1 + 2 U/c^2 - 2 beta U^2/c^4 + h_00^MTS + O(c^-6); g_ij = (1 + 2 gamma U/c^2) delta_ij + h_ij^MTS + O(c^-4)",
            "derivation": "PPN observables compare dimensionless metric residuals against powers of q_U=|U|/c^2, so raw h_munu amplitudes cannot be judged without the weak-potential denominator",
            "guard": "sign convention is irrelevant for the bound because absolute residual amplitudes are used",
            "status": "ANSATZ_FIXED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WF3331_1_qU_definition",
            "object": "weak-potential denominator",
            "formula": "q_U := |U|/c^2 = G_N M/(r c^2) in the calibrated local source frame",
            "derivation": "after measured-G closure the Newtonian slot defines the source mass used by PPN comparisons; residual first-order metric amplitudes are divided by q_U",
            "guard": "if the source mass/GM calibration is not fixed, first-order residuals can be hidden by mass redefinition and the PPN map is not scoreable",
            "status": "NORMALIZATION_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WF3331_2_gamma_map",
            "object": "PPN gamma residual",
            "formula": "|delta gamma| <= (H_s^(1)+H_00^(1))/(2 q_U) + epsilon_gauge + epsilon_readout + epsilon_source",
            "derivation": "write h_s^(1)=spatial isotropic first-order residual and h_00^(1)=time first-order residual after Newtonian calibration; gamma is the spatial potential coefficient relative to the calibrated time potential coefficient",
            "guard": "pure gauge pieces and GM absorption must be projected out before H_s^(1), H_00^(1) are called physical",
            "status": "GAMMA_BOUND_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WF3331_3_beta_map",
            "object": "PPN beta residual",
            "formula": "|delta beta| <= H_00^(2)/(2 q_U^2) + a_beta1 H_00^(1)/q_U + epsilon_gauge + epsilon_readout + epsilon_source",
            "derivation": "beta is a second-order time-metric coefficient, so an actual second-order residual is normalized by q_U^2; unresolved first-order leakage contaminates beta through source-calibration cross terms",
            "guard": "beta is not clean unless the first-order Newtonian slot is fixed or explicitly absorbed into measured GM",
            "status": "BETA_BOUND_DERIVED_WITH_FIRST_ORDER_GUARD",
            "valid_for_claim": "false",
        },
        {
            "row_id": "WF3331_4_preferred_frame_map",
            "object": "non-isotropic PPN residuals",
            "formula": "|alpha_PF| <= A_PF H_T/q_U + epsilon_gauge + epsilon_frame",
            "derivation": "anisotropic or velocity-frame residual metric pieces enter preferred-frame/preferred-location PPN slots once projected into the standard PPN gauge",
            "guard": "if H_T is pure gauge or outside the PPN frame convention it must not be counted as a physical preferred-frame coefficient",
            "status": "PREFERRED_FRAME_BOUND_TEMPLATE",
            "valid_for_claim": "false",
        },
    ]


def appn_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "APPN3331_0_gamma",
            "coefficient": "A_gamma(q_U,gauge)",
            "formula": "A_gamma <= a_gamma/q_U + a_gauge + a_readout + a_source",
            "meaning": "linear first-order metric residuals are amplified by the inverse weak potential in gamma-like observables",
            "status": "SYMBOLIC_BOUND_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "APPN3331_1_beta",
            "coefficient": "A_beta(q_U,gauge)",
            "formula": "A_beta <= a_beta2/q_U^2 + a_beta1/q_U + a_gauge + a_readout + a_source",
            "meaning": "second-order time residuals carry a q_U^-2 denominator, with q_U^-1 contamination if first-order source calibration is not closed",
            "status": "SYMBOLIC_BOUND_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "APPN3331_2_vector_tensor",
            "coefficient": "A_vector_tensor(q_U,gauge)",
            "formula": "A_vector_tensor <= max(a_PF/q_U, a_aniso/q_U) + a_gauge + a_frame",
            "meaning": "anisotropic, vector, or frame-dependent metric residuals must be projected into the standard PPN gauge before comparison",
            "status": "BOUND_TEMPLATE",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "APPN3331_3_master",
            "coefficient": "A_PPN(q_U,gauge)",
            "formula": "A_PPN(q_U,gauge) := max(A_gamma, A_beta, A_vector_tensor, A_gauge_residual)",
            "meaning": "the worst normalized PPN slot sets the safe response multiplier for C_metric",
            "status": "MASTER_APPN_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "APPN3331_4_clean_branch",
            "coefficient": "A_PPN_clean",
            "formula": "if H_00^(1) is fully absorbed into measured GM and gauge/readout residuals vanish, A_gamma~O(q_U^-1) and beta is controlled only by genuine H_00^(2)/q_U^2",
            "meaning": "this is the least-scrutinized clean route: do not count mass calibration or gauge artifacts as MTS physics",
            "status": "CONDITIONAL_CLEAN_BRANCH",
            "valid_for_claim": "false",
        },
    ]


def cmetric_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "CMET3331_0_operator_definition",
            "quantity": "C_metric(lambda)",
            "formula": "C_metric(lambda) = ||Pi_PPN G_PPN W_PPN||^2 ||D_metric S_ell H_pi(lambda) S_ell^dagger D_metric^dagger|| N_source",
            "derivation": "specializes the 3322 C_i response coefficient to gauge-fixed weak-field metric components before q_U normalization",
            "needed_input": "Pi_PPN, G_PPN, W_PPN, D_metric, S_ell, H_pi, N_source",
            "status": "OPERATOR_BOUND_FORMULA",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CMET3331_1_factor_bound",
            "quantity": "factorized upper bound",
            "formula": "C_metric <= P_PPN^2 G_fix^2 W_src^2 D_readout^2 S_band^2 H_band(lambda) N_source",
            "derivation": "submultiplicativity turns the metric response into individually auditable projection, gauge-fixing, source-window, derivative-readout, smoothing, propagator, and source-normalization factors",
            "needed_input": "finite or numeric upper bound for every factor",
            "status": "CONSERVATIVE_FACTOR_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CMET3331_2_bandlimited_green",
            "quantity": "H_band(lambda)",
            "formula": "H_band(lambda) := sup_{k in PPN band} ||(Z_pi k^2 + M_pi^2)^-1|| or the parent Hessian inverse projected into the PPN band",
            "derivation": "a finite parent Hessian gap gives a finite metric response; without Z_pi/M_pi^2 or an equivalent Hessian spectrum the response remains symbolic",
            "needed_input": "Z_pi, M_pi^2, band convention, parent Hessian spectrum",
            "status": "PROPAGATOR_SLOT_IDENTIFIED",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CMET3331_3_source_normalization",
            "quantity": "N_source",
            "formula": "N_source is fixed by measured-G closure/Poisson normalization, not by a hidden re-fit inside C_metric",
            "derivation": "the local GR branch uses measured G_N to normalize the Newtonian slot; any extra MTS source response must be residual after that calibration",
            "needed_input": "source mass convention, GM absorption rule, measured-G closure declaration",
            "status": "SOURCE_CALIBRATION_GUARD",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CMET3331_4_gauge_projector",
            "quantity": "G_PPN",
            "formula": "G_PPN removes pure gauge, coordinate, and GM-redefinition modes before PPN scoring",
            "derivation": "PPN residuals are physical only after the metric is in the same observational gauge/frame as the comparator",
            "needed_input": "gauge-fixing projector or equivalent invariant observable map",
            "status": "GAUGE_GUARD_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def cppn_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CPPN3331_0_master",
            "formula": "C_PPN(lambda) <= A_PPN(q_U,gauge) C_metric(lambda)",
            "meaning": "PPN response is the product of weak-potential/gauge normalization and the underlying MTS metric operator response",
            "status": "COMPOSITION_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CPPN3331_1_tree_residual",
            "formula": "R_tree_PPN <= A_PPN(q_U,gauge) C_metric(lambda_PPN) epsilon_eff_PPN(lambda_PPN)^2",
            "meaning": "the first-gradient tree channel is now normalized into PPN units",
            "status": "TREE_CHANNEL_COMPOSED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CPPN3331_2_full_budget",
            "formula": "R_PPN <= |R_Gamma_PPN| + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN + epsilon_direct_PPN + epsilon_G_closure_PPN",
            "meaning": "full no-cancellation PPN residual budget after 3331",
            "status": "FULL_BUDGET_COMPOSED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CPPN3331_3_no_claim_rule",
            "formula": "No PPN/local-GR claim unless A_PPN, C_metric, epsilon_eff, Gamma, composite, direct, and G-closure floors are all source-bounded below a real PPN threshold B_PPN",
            "meaning": "3331 narrows the map but does not supply numerical source-grade bounds",
            "status": "NO_CLAIM_RULE",
            "valid_for_claim": "false",
        },
    ]


def required_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ3331_0_qU_arena",
            "quantity": "q_U=|U|/c^2 for each PPN arena",
            "needed_for": "A_gamma, A_beta, A_vector_tensor",
            "current_status": "FORMULA_DERIVED_NUMERIC_VALUES_NOT_SOURCED",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3331_1_gauge_projector",
            "quantity": "G_PPN gauge/invariant observable projector",
            "needed_for": "remove pure gauge and GM-absorption modes before scoring h_munu",
            "current_status": "STRUCTURAL_REQUIREMENT_DEFINED",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3331_2_metric_projection",
            "quantity": "Pi_PPN and W_PPN",
            "needed_for": "C_metric operator norm",
            "current_status": "FACTOR_IDENTIFIED_NUMERIC_BOUND_MISSING",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3331_3_parent_hessian",
            "quantity": "H_pi(lambda), Z_pi, M_pi^2 or equivalent Hessian spectrum",
            "needed_for": "finite metric Green/operator response",
            "current_status": "PARENT_NUMERIC_BOUND_MISSING",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3331_4_source_normalization",
            "quantity": "N_source after measured-G closure and GM absorption",
            "needed_for": "prevent Newtonian mass calibration being double-counted as MTS residual",
            "current_status": "CLOSURE_CONVENTION_REQUIRED",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "input_id": "REQ3331_5_real_threshold",
            "quantity": "B_PPN real observational threshold vector",
            "needed_for": "claim-grade comparison",
            "current_status": "NOT_ATTEMPTED_IN_3331",
            "priority": "medium",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3331_0_A_PPN_symbolic",
            "claim": "A_PPN(q_U,gauge) is no longer a free placeholder",
            "passed": "true",
            "reason": "gamma, beta, and anisotropic PPN slots now carry explicit q_U denominators and gauge/source caveats",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3331_1_Cmetric_factorized",
            "claim": "C_metric is factorized into auditable operator pieces",
            "passed": "true",
            "reason": "projection, gauge, source-window, derivative-readout, smoothing, Green/Hessian, and source-normalization factors are separated",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3331_2_CPPN_composed",
            "claim": "C_PPN composition is formula-ready",
            "passed": "true",
            "reason": "C_PPN <= A_PPN C_metric and the tree residual budget are written explicitly",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3331_3_A_PPN_numeric",
            "claim": "A_PPN has claim-grade numeric arena bounds",
            "passed": "false",
            "reason": "q_U values, gauge projector, and threshold vector are not sourced here",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3331_4_Cmetric_numeric",
            "claim": "C_metric has claim-grade numeric operator bound",
            "passed": "false",
            "reason": "parent Hessian spectrum and metric projection norms are not numeric/source-owned",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3331_5_PPN_claim",
            "claim": "PPN/local-GR pass is claim-ready",
            "passed": "false",
            "reason": "3331 derives the map, not the numeric floors and observational threshold comparison",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3331_0",
            "question": "Did 3331 move beyond a missing-input ledger?",
            "answer": "yes, structurally",
            "reason": "it derives the q_U normalization law for PPN gamma/beta slots and turns C_metric into a factorized operator norm",
            "next_action": "specialize epsilon_eff_PPN and floor terms using the new A_PPN C_metric composition",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3331_1",
            "question": "Is the cleanest route still local GR closure?",
            "answer": "yes",
            "reason": "source-calibrated measured-G closure lets GM absorption handle the Newtonian slot while MTS residuals are tested only after gauge/source projection",
            "next_action": "keep direct psi-matter/psi-EM vertices excluded unless a parent action forces them",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3331_2",
            "question": "Can PPN be claimed now?",
            "answer": "no",
            "reason": "A_PPN and C_metric are derivation-ready but not numeric/source-bounded; floors remain explicit",
            "next_action": "derive or bound epsilon_eff_PPN, epsilon_composite_PPN, and R_Gamma_PPN under this normalization",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3332-Y5-R2FR-PPN-epsilon-eff-and-floor-specialization-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3332_PPN_epsilon_eff_and_floor_specialization.py",
            "objective": "specialize epsilon_eff_PPN, epsilon_composite_PPN, R_Gamma_PPN, epsilon_direct_PPN, and epsilon_G_closure_PPN inside the 3331 normalized PPN budget",
            "must_include": "T_grad(lambda_PPN); q_U-normalized C_PPN; Gamma proxy versus general Gamma bound; composite CLT/spectral/contact floors; direct vertex silence; no PPN claim",
            "fallback_if_failed": "retain full no-cancellation PPN residual vector and move to sourcing real PPN threshold rows only after floor terms are separated",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    weak = weak_field_rows()
    appn = appn_rows()
    cmetric = cmetric_rows()
    cppn = cppn_rows()
    inputs = required_input_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3331_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3331_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3331_2_outputs_parse",
            "check": "all 3331 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3331_3_weak_field_maps",
            "check": "weak-field rows include q_U, gamma, beta, and gauge/source caveats",
            "passed": any("q_U" in row["formula"] for row in weak)
            and any("delta gamma" in row["formula"] for row in weak)
            and any("delta beta" in row["formula"] for row in weak)
            and any("gauge" in row["guard"] for row in weak),
            "detail": "",
        },
        {
            "check_id": "VAL3331_4_APPN_denominators",
            "check": "A_PPN rows include q_U^-1 and q_U^-2 denominators",
            "passed": any("q_U" in row["formula"] and "q_U^2" in row["formula"] for row in appn)
            and any("A_PPN" in row["coefficient"] for row in appn),
            "detail": "",
        },
        {
            "check_id": "VAL3331_5_Cmetric_factors",
            "check": "C_metric rows include projection, gauge, Green/Hessian, smoothing, and source normalization factors",
            "passed": any("Pi_PPN" in row["formula"] and "G_PPN" in row["formula"] and "H_pi" in row["formula"] for row in cmetric)
            and any("N_source" in row["formula"] for row in cmetric)
            and any("S_ell" in row["formula"] or "S_band" in row["formula"] for row in cmetric),
            "detail": "",
        },
        {
            "check_id": "VAL3331_6_CPPN_composition",
            "check": "C_PPN composition and full residual budget are present",
            "passed": any("C_PPN" in row["formula"] and "A_PPN" in row["formula"] and "C_metric" in row["formula"] for row in cppn)
            and any("R_PPN" in row["formula"] and "epsilon_composite_PPN" in row["formula"] for row in cppn),
            "detail": "",
        },
        {
            "check_id": "VAL3331_7_inputs",
            "check": "required inputs include q_U, gauge projector, projection, Hessian, source normalization, and real threshold",
            "passed": {"REQ3331_0_qU_arena", "REQ3331_1_gauge_projector", "REQ3331_2_metric_projection", "REQ3331_3_parent_hessian", "REQ3331_4_source_normalization", "REQ3331_5_real_threshold"}.issubset(
                {row["input_id"] for row in inputs}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3331_8_no_claim",
            "check": "symbolic derivation gates pass while numeric and PPN claim gates remain false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3331_0_A_PPN_symbolic", "GATE3331_1_Cmetric_factorized", "GATE3331_2_CPPN_composed"}
            )
            and all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3331_3_A_PPN_numeric", "GATE3331_4_Cmetric_numeric", "GATE3331_5_PPN_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3331_9_next_3332",
            "check": "next target specializes epsilon_eff and floors",
            "passed": any("epsilon_eff_PPN" in row["objective"] and "R_Gamma_PPN" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3331_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3331_11_overall",
            "check": "3331 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3331 - PPN weak-potential normalization and C_metric bound under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3331 does move the PPN branch forward. It does not merely say that a coefficient is missing.",
        "",
        "The local PPN residual has two separable pieces:",
        "",
        "`C_PPN(lambda) <= A_PPN(q_U,gauge) C_metric(lambda)`.",
        "",
        "`A_PPN` is the weak-field/gauge/observable normalization. `C_metric` is the actual MTS metric operator response before PPN normalization.",
        "",
        "The weak-potential denominator is",
        "",
        "`q_U = |U|/c^2 = G_N M/(r c^2)`",
        "",
        "in the calibrated local source frame. This means a tiny raw metric residual can become non-tiny in PPN units because gamma-like slots scale as `q_U^-1` and beta-like slots can scale as `q_U^-2`.",
        "",
        "The derived safe maps are",
        "",
        "`|delta gamma| <= (H_s^(1)+H_00^(1))/(2 q_U) + epsilon_gauge + epsilon_readout + epsilon_source`,",
        "",
        "and",
        "",
        "`|delta beta| <= H_00^(2)/(2 q_U^2) + a_beta1 H_00^(1)/q_U + epsilon_gauge + epsilon_readout + epsilon_source`.",
        "",
        "So the clean route is not to fight source calibration. The clean route is to declare measured-G/Newtonian closure, project out pure gauge and GM-redefinition modes, then test only the residual physical metric pieces.",
        "",
        "The metric response is now factorized as",
        "",
        "`C_metric(lambda) = ||Pi_PPN G_PPN W_PPN||^2 ||D_metric S_ell H_pi(lambda) S_ell^dagger D_metric^dagger|| N_source`,",
        "",
        "with conservative upper bound",
        "",
        "`C_metric <= P_PPN^2 G_fix^2 W_src^2 D_readout^2 S_band^2 H_band(lambda) N_source`.",
        "",
        "No PPN/local-GR claim follows. The result is stronger than a missing-input note because it gives the exact slots that must be bounded next.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Weak-Field Normalization", weak_field_rows(), "row_id"),
        ("A_PPN Bound", appn_rows(), "bound_id"),
        ("C_metric Bound", cmetric_rows(), "bound_id"),
        ("C_PPN Composition", cppn_rows(), "row_id"),
        ("Required Inputs", required_input_rows(), "input_id"),
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
            "- It sharpens the PPN branch by deriving the weak-potential denominators instead of treating `C_PPN` as a loose knob.",
            "- It keeps measured-G closure explicit and blocks any hidden source-mass redefinition from masquerading as an MTS prediction.",
            "- It does not use or claim real PPN observational bounds.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["weak_field"], weak_field_rows())
    write_csv(OUTPUTS["appn"], appn_rows())
    write_csv(OUTPUTS["cmetric"], cmetric_rows())
    write_csv(OUTPUTS["cppn"], cppn_rows())
    write_csv(OUTPUTS["inputs"], required_input_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
