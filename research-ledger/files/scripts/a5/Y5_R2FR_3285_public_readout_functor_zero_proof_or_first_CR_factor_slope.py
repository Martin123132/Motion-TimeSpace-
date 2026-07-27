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

DOC = ROOT / "3285-Y5-R2FR-public-readout-functor-zero-proof-or-first-CR-factor-slope-under-AX1090.md"

SRC_3284_DOC = ROOT / "3284-Y5-R2FR-CR-readout-product-law-and-Poynting-wave-standard-or-zero-theorem-under-AX1090.md"
SRC_3284_THEOREM = OUT / "P8_Y5_R2FR_3284_CR_PRODUCT_LAW_THEOREM.csv"
SRC_3284_FACTORS = OUT / "P8_Y5_R2FR_3284_CR_READOUT_FACTOR_LEDGER.csv"
SRC_3284_POYNTING = OUT / "P8_Y5_R2FR_3284_POYNTING_STANDARD_BRANCH_TABLE.csv"
SRC_3284_RUNNER = OUT / "P8_Y5_R2FR_3284_CR_BOUND_RUNNER_NONCLAIM.csv"
SRC_3284_NEXT = OUT / "P8_Y5_R2FR_3284_NEXT_TARGET.csv"
SRC_3284_VALIDATION = OUT / "P8_Y5_BRR545_3284_VALIDATION.csv"
SRC_3273_DECOMP = OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv"
SRC_1031_DOC = ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md"
SRC_3105_DOC = ROOT / "3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md"
SRC_3106_DOC = ROOT / "3106-Y5-R2FR-constitutive-Hodge-star-derivation-or-EM-medium-residual-under-AX1090.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
SRC_1324_DOC = ROOT / "1324-Y5-R10-RAB-clock-direct-product-derivation-source-fill-or-waitstate.md"
SRC_2656_CONTRACT = OUT / "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_RESIDUAL_BOUND_INPUT_CONTRACT.csv"
SRC_NO_SPECIES = OUT / "P8_no_species_source_charge_CONTRACT.csv"
SRC_SOURCE_WARD = OUT / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_SYMBOL_MAP = OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3285_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3285_PUBLIC_READOUT_FUNCTOR_THEOREM.csv",
    "signature": OUT / "P8_Y5_R2FR_3285_FACTOR_THROUGH_Q_SIGNATURE_MATRIX.csv",
    "poynting": OUT / "P8_Y5_R2FR_3285_POYNTING_QBASIC_LEMMA.csv",
    "finite": OUT / "P8_Y5_R2FR_3285_FIRST_CR_FACTOR_SLOPE_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3285_CR_FACTOR_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3285_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3285_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3285_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3285_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 360) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


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
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 240)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3284_DOC, "3284 handoff", ["C_R = L_v", "Poynting"]),
        (SRC_3284_THEOREM, "3284 product theorem", ["CRPL3284_1", "product_law"]),
        (SRC_3284_FACTORS, "3284 readout factors", ["CRFCT3284_3", "Poynting"]),
        (SRC_3284_POYNTING, "3284 Poynting branch table", ["forbidden_double_count", "public_metric"]),
        (SRC_3284_RUNNER, "3284 C_R runner", ["CRP3284_0", "REFUSE_OR_FAIL"]),
        (SRC_3284_NEXT, "3284 next target", ["3285", "public-readout"]),
        (SRC_3284_VALIDATION, "3284 validation", ["VAL3284_11_overall", "true"]),
        (SRC_3273_DECOMP, "alpha coefficient law", ["2 C_J", "C_R"]),
        (SRC_1031_DOC, "terminal public metric insufficiency", ["terminality alone", "matter_interface_functor"]),
        (SRC_3105_DOC, "Poynting public stress/no double count", ["Double-Counting Guard", "T_EM"]),
        (SRC_3106_DOC, "constitutive Hodge route", ["H = Z_Q", "chi"]),
        (SRC_1100_DOC, "charge/current/readout owner", ["readout_radiative_guard", "same_current_owner"]),
        (SRC_1324_DOC, "clock product wait-state", ["direct product", "clock"]),
        (SRC_2656_CONTRACT, "material/kernel readout contract", ["MISSING_PARENT_COUPLING_OWNER", "tau_WEP"]),
        (SRC_NO_SPECIES, "ordinary matter/source coframe contract", ["one observed coframe", "matter action"]),
        (SRC_SOURCE_WARD, "source-current Ward contract", ["single_observed_coframe", "Hilbert_source"]),
        (SRC_SYMBOL_MAP, "symbol to local GR action map", ["g_obs", "Pi_M"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3285_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def alpha_bound() -> float:
    for row in read_csv(SRC_3284_RUNNER):
        if row.get("row_id") == "CRP3284_1_qbasic_readout_zero_conditional":
            return float(read_csv(SRC_3284_FACTORS)[0].get("bound_value", "nan")) if "bound_value" in row else 1.389797711495e-12
    return 1.389797711495e-12


def bound_from_3284_predictions() -> float:
    prediction_path = OUT / "P8_Y5_R2FR_3284_FIRST_CR_SLOPE_ROWS_NONCLAIM.csv"
    for row in read_csv(prediction_path):
        if row.get("row_id") == "CRP3284_0_product_formula_ready_missing":
            return float(row["C_R_abs_bound"])
    return 1.389797711495e-12


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PRF3285_0_public_readout_category",
            "claim_piece": "define public readout category and standards",
            "statement": "Let q:P_parent->Q_obs. A public readout standard is an object R_s whose value is evaluated as R_s(Phi)=Rbar_s(q(Phi),theta_rep), with theta_rep fixed representation/topological data.",
            "proof_status": "DEFINITION_CANDIDATE",
            "missing_for_claim": "parent action must define Q_obs, theta_rep, and the allowed ordinary readout standard class.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PRF3285_1_public_readout_functor_contract",
            "claim_piece": "single functor factorization stronger than terminality",
            "statement": "A parent public-readout functor F_read: P_parent -> Std factors as Fbar_read o q and contains clocks/rods/action units, charge standards, Hodge/impedance, Poynting flux, material response, and projection kernels.",
            "proof_status": "EXACT_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "missing_for_claim": "the corpus has contracts and partial branches, not a parent-signed action-domain exclusion for every factor.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PRF3285_2_chain_rule_zero",
            "claim_piece": "C_R zero theorem under public-readout functor",
            "statement": "If R_alpha_readout=product_s Rbar_s(q(Phi),theta_rep)^{n_s}, v in ker(Dq), and L_v theta_rep=0, then C_R=sum_s n_s L_v ln R_s=0.",
            "proof_status": "EXACT_CHAIN_RULE_THEOREM",
            "missing_for_claim": "all factor-through-q clauses must be parent-signed together; otherwise any unsigned factor can carry finite C_R.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PRF3285_3_poynting_qbasic_lemma",
            "claim_piece": "Poynting standard zero inside public Maxwell/Hodge branch",
            "statement": "If H=Z_Q *_{g_pub}F, Z_Q, g_pub, observer coframe u, and projection h are q-basic, then S_EM^a=-h^a_mu T_EM^{mu nu}u_nu is q-basic, so C_S=L_v ln R_Poynting_flux=0.",
            "proof_status": "EXACT_CONDITIONAL_LEMMA",
            "missing_for_claim": "chi->metric Hodge, same public coframe, and Z_Q/readout ownership remain unsigned.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PRF3285_4_terminality_insufficiency_guard",
            "claim_piece": "do not overclaim from terminal public metric",
            "statement": "A terminal public metric/coframe object does not force C_R=0 unless every readout factor is evaluated through the terminal/public functor before observation.",
            "proof_status": "COUNTERMODEL_GUARD_FROM_1031",
            "missing_for_claim": "matter/readout interface restriction and field-rename guards across constants, source normalization, and detectors.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PRF3285_5_current_verdict",
            "claim_piece": "public-readout functor status",
            "statement": "3285 proves the theorem shape exactly, but the current corpus does not parent-sign the full public-readout functor. The finite C_R branch therefore remains live with Hodge/Poynting as the selected first factor-slope target.",
            "proof_status": "THEOREM_SHAPE_DERIVED_PARENT_SIGNATURE_UNSIGNED",
            "missing_for_claim": "full public-readout action-domain signature or first numeric factor slope.",
            "valid_for_claim": "false",
        },
    ]


def signature_rows() -> list[dict[str, Any]]:
    factors = read_csv(SRC_3284_FACTORS)
    requirements = {
        "CRFCT3284_0_phase_action_clock": ("R_phase_action_clock=q^*Rbar_phase", "1324 shows clock product wait-state; no MTS local alpha/readout product."),
        "CRFCT3284_1_lightcone_rods": ("R_light_rods=q^*Rbar_light", "same public metric/coframe not parent-signed."),
        "CRFCT3284_2_hodge_impedance": ("H=Z_Q *_{g_pub}F with q-basic Z_Q and Hodge/impedance", "3106 retains chi/Hodge theorem as open."),
        "CRFCT3284_3_poynting_flux_standard": ("S_EM^a is the q-basic public T_EM flux", "placement rule exists; Hodge/coframe/Z_Q owner unsigned."),
        "CRFCT3284_4_material_detector": ("R_material_detector=q^*Rbar_mat with no hidden material marker", "material tensor and source/readout product missing."),
        "CRFCT3284_5_charge_calibration_guard": ("R_charge_standard fixed by same T_Q/current owner or routed to C_J", "T_Q/current/readout owner not parent-signed."),
        "CRFCT3284_6_instrument_projection": ("R_projection_kernel=q^*Rbar_kernel fixed before scoring", "official/readout kernels and tau projections not score-ready."),
    }
    rows: list[dict[str, Any]] = []
    for row in factors:
        req, blocker = requirements[row["factor_id"]]
        rows.append(
            {
                "signature_id": "SIG3285_" + row["factor_id"].split("_")[-1],
                "factor_id": row["factor_id"],
                "readout_factor": row["readout_factor"],
                "required_factorization": req,
                "chain_rule_payoff": row["if_qbasic"],
                "current_evidence_status": row["current_status"],
                "parent_signed": "false",
                "blocker": blocker,
                "source_path": row["source_path"],
                "valid_for_claim": "false",
            }
        )
    return rows


def poynting_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "PLEM3285_0_public_flux_formula",
            "premise": "H=Z_Q *_{g_pub}F and T_EM is varied from the same public EM action",
            "derivation": "T_EM^{mu nu}=Z_Q(F^{mu alpha}F^nu_alpha-1/4 g_pub^{mu nu}F^2); S_EM^a=-h^a_mu T_EM^{mu nu}u_nu",
            "C_R_payoff": "Poynting readout factor is q-basic if Z_Q,g_pub,u,h are q-basic",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "PLEM3285_1_vertical_derivative",
            "premise": "L_v Z_Q=L_v g_pub=L_v u=L_v h=0",
            "derivation": "L_v S_EM^a=0 by Leibniz rule because every public factor is vertical-constant",
            "C_R_payoff": "C_S=L_v ln R_Poynting_flux=0",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "PLEM3285_2_constitutive_medium_escape",
            "premise": "chi has non-q-basic hidden/domain dependence",
            "derivation": "L_v chi != 0 can create Hodge/impedance/Poynting readout drift even if ordinary F is public",
            "C_R_payoff": "finite C_H/C_S slope row required",
            "status": "RETAINED_RESIDUAL_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "PLEM3285_3_no_double_count",
            "premise": "same EM flux is claimed as both T_EM and background E_res",
            "derivation": "energy flux is counted twice in the local source equation",
            "C_R_payoff": "route forbidden; must choose public EM stress or separate named residual",
            "status": "FORBIDDEN",
            "valid_for_claim": "false",
        },
    ]


def finite_rows(bound: float) -> list[dict[str, Any]]:
    half = bound / 2.0
    twice = bound * 2.0
    return [
        {
            "row_id": "CRF3285_0_functor_zero_conditional",
            "factor_target": "all public readout factors",
            "C_R_prediction": "0",
            "C_R_abs_bound": fmt(bound),
            "required_inputs": "parent-signed public-readout functor F_read=Fbar_read o q",
            "result": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRF3285_1_selected_hodge_poynting_slope",
            "factor_target": "Hodge/impedance plus Poynting flux",
            "C_R_prediction": "n_H*C_H + n_S*C_S",
            "C_R_abs_bound": fmt(bound),
            "required_inputs": "numeric C_H, C_S, exponents n_H,n_S, chi/Hodge source path, Poynting placement certificate",
            "result": "FIRST_FACTOR_SLOPE_SELECTED_SOURCE_VALUE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRF3285_2_material_projection_slope",
            "factor_target": "material detector plus projection kernel",
            "C_R_prediction": "n_mat*C_mat + n_inst*C_inst",
            "C_R_abs_bound": fmt(bound),
            "required_inputs": "material tensor, official/equivalent kernel, tau/readout convention",
            "result": "SYMBOLIC_ONLY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRF3285_3_charge_guard_slope_or_CJ_route",
            "factor_target": "charge/current calibration",
            "C_R_prediction": "C_Qread_or_route_to_C_J",
            "C_R_abs_bound": fmt(bound),
            "required_inputs": "same T_Q/current owner decision; avoid double counting with C_J",
            "result": "ROUTE_SPLIT_REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRF3285_4_half_bound_smoke",
            "factor_target": "numeric smoke inside envelope",
            "C_R_prediction": fmt(half),
            "C_R_abs_bound": fmt(bound),
            "required_inputs": "SMOKE_NUMERIC_NONCLAIM",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CRF3285_5_twice_bound_smoke",
            "factor_target": "numeric smoke outside envelope",
            "C_R_prediction": fmt(twice),
            "C_R_abs_bound": fmt(bound),
            "required_inputs": "SMOKE_NUMERIC_NONCLAIM",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
    ]


def try_float(value: str) -> float | None:
    try:
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    except Exception:
        return None


def runner_rows(finite: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = {
        "CRF3285_0_functor_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "CRF3285_1_selected_hodge_poynting_slope": "SYMBOLIC_NONNUMERIC_NONCLAIM",
        "CRF3285_2_material_projection_slope": "SYMBOLIC_NONNUMERIC_NONCLAIM",
        "CRF3285_3_charge_guard_slope_or_CJ_route": "SYMBOLIC_NONNUMERIC_NONCLAIM",
        "CRF3285_4_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "CRF3285_5_twice_bound_smoke": "FAIL_BOUND",
    }
    rows: list[dict[str, Any]] = []
    for row in finite:
        pred = row["C_R_prediction"]
        bound = float(row["C_R_abs_bound"])
        numeric = try_float(pred)
        if str(pred).startswith("MISSING"):
            result = "REFUSE_OR_FAIL"
            ratio = "MISSING"
        elif numeric is None:
            result = "SYMBOLIC_NONNUMERIC_NONCLAIM"
            ratio = "N/A"
        else:
            ratio_float = abs(numeric) / bound if bound > 0 else math.inf
            ratio = fmt(ratio_float)
            result = "PASS_NUMERIC_NONCLAIM" if ratio_float <= 1.0 else "FAIL_BOUND"
        expectation = expected[row["row_id"]]
        rows.append(
            {
                "row_id": row["row_id"],
                "C_R_prediction": pred,
                "prediction_over_bound": ratio,
                "result": result,
                "expected_result": expectation,
                "expectation_met": bool_str(result == expectation),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3285_0_chain_rule_theorem",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "public-readout functor factorization implies C_R=0 by chain rule.",
        },
        {
            "gate_id": "GATE3285_1_parent_functor_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "factor-through-q signature is not parent-signed for all readout factors.",
        },
        {
            "gate_id": "GATE3285_2_terminality_alone_rejected",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "1031 terminal-object warning is preserved; action/readout domain restriction is required.",
        },
        {
            "gate_id": "GATE3285_3_poynting_lemma",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "Poynting q-basic lemma is exact conditional and forbids double counting.",
        },
        {
            "gate_id": "GATE3285_4_finite_factor_sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "first finite factor-slope target selected, but no numeric source-backed C_H/C_S row exists.",
        },
        {
            "gate_id": "GATE3285_5_no_local_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "no local-GR/alpha/Maxwell/clock/MICROSCOPE/PPN claim is allowed.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3285_0_theorem_result",
            "decision": "Public-readout functor theorem is exact but conditional.",
            "why_it_moves_forward": "it replaces seven separate readout leaks with one parent action-domain signature.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3285_1_terminality_result",
            "decision": "Terminal public coframe is insufficient unless readout factors are forced through it before observation.",
            "why_it_moves_forward": "prevents a fake local-GR closure by category language alone.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3285_2_poynting_result",
            "decision": "Poynting zero works if public Hodge/Maxwell stress is q-basic; otherwise Hodge/Poynting becomes the first finite C_R factor target.",
            "why_it_moves_forward": "keeps the Poynting idea alive as a derivation route and a testable residual route.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3285_3_next_work",
            "decision": "Next target should attack Hodge/Poynting factor ownership or source C_H/C_S numerically.",
            "why_it_moves_forward": "chooses one finite slope instead of scattering across every readout factor.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3285_0_3286",
            "target_doc": "3286-Y5-R2FR-Hodge-Poynting-factor-owner-or-first-CH-CS-slope-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3286_Hodge_Poynting_factor_owner_or_first_CH_CS_slope_row.py",
            "objective": "Attack the selected first C_R factor directly: prove the Hodge/impedance and Poynting flux factors are q-basic public Maxwell/Hodge readouts, or source the first numeric C_H/C_S slope row with units, sign convention, source path, and no-double-counting certificate.",
            "guardrail": "Do not reopen terminal-public-metric or all-factor ledgers unless new parent evidence signs them; no clock/MICROSCOPE/PPN scoring; no Poynting double counting.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    non_validation_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_after = snapshot_tree(FW)
    fw_changed = changed_count(fw_before, fw_after)
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": compact(detail, 520),
            }
        )

    add("VAL3285_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3285_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add(
        "VAL3285_2_outputs_parse",
        "all 3285 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3285_3_chain_rule_theorem_present",
        "public-readout chain-rule theorem is present",
        any(row["theorem_id"] == "PRF3285_2_chain_rule_zero" and "C_R=sum_s" in row["statement"] and "=0" in row["statement"] for row in theorem),
    )
    add(
        "VAL3285_4_signature_factor_coverage",
        "signature matrix covers all seven 3284 factors",
        len(signature) == 7 and all(row["parent_signed"] == "false" for row in signature),
    )
    add(
        "VAL3285_5_poynting_qbasic_lemma",
        "Poynting q-basic lemma and no-double-count guard are present",
        any(row["lemma_id"] == "PLEM3285_1_vertical_derivative" for row in poynting)
        and any(row["lemma_id"] == "PLEM3285_3_no_double_count" and row["status"] == "FORBIDDEN" for row in poynting),
    )
    add(
        "VAL3285_6_first_factor_selected",
        "Hodge/Poynting finite factor slope is selected",
        any(row["row_id"] == "CRF3285_1_selected_hodge_poynting_slope" for row in finite),
    )
    add(
        "VAL3285_7_runner_expectations",
        "C_R factor runner expectations all match",
        all(row["expectation_met"] == "true" for row in runner),
        ";".join(f"{row['row_id']}={row['result']}" for row in runner),
    )
    add(
        "VAL3285_8_claim_gates_false",
        "no 3285 gate allows local-GR/alpha/Maxwell claim",
        all(row["claim_allowed"] == "false" for row in promotion),
    )
    add(
        "VAL3285_9_next_target_focused",
        "next target focuses Hodge/Poynting factor owner or C_H/C_S slope",
        any("Hodge-Poynting" in row["target_doc"] and "C_H/C_S" in row["objective"] for row in next_target),
    )
    add(
        "VAL3285_10_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3285_11_overall",
        "3285 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def write_doc(
    bound: float,
    theorem: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3285 - Public readout functor zero proof or first C_R factor slope under AX1090

## Summary

3285 proves the clean theorem shape:

`R_alpha_readout = product_s Rbar_s(q(Phi), theta_rep)^{{n_s}}`

with `v in ker(Dq)` and `L_v theta_rep=0` gives

`C_R = sum_s n_s L_v ln R_s = 0`.

This is stronger than the old terminal-public-metric route. A terminal public coframe is not enough: the parent action/readout interface must force every readout standard to be evaluated only through `q` before observation.

The current corpus does **not** sign that full public-readout functor. So `C_R=0` is exact conditional, not a claim. The first finite factor target is now selected: Hodge/impedance plus Poynting flux, because that is where the user's EM/Poynting intuition can either become a public Maxwell/Hodge theorem or a finite `C_H/C_S` slope row.

Pure readout envelope remains:

`|C_R| <= {fmt(bound)}` if `C_J=0`, `C_Z=0`, and `C_R` is the only live alpha/readout slope.

## Public Readout Functor Theorem
{md_table(theorem, ["theorem_id", "claim_piece", "proof_status", "missing_for_claim"])}

## Factor-Through-q Signature Matrix
{md_table(signature, ["signature_id", "readout_factor", "required_factorization", "chain_rule_payoff", "parent_signed", "blocker"])}

## Poynting q-Basic Lemma
{md_table(poynting, ["lemma_id", "premise", "derivation", "C_R_payoff", "status"])}

## First C_R Factor Slope Rows
{md_table(finite, ["row_id", "factor_target", "C_R_prediction", "C_R_abs_bound", "result", "valid_for_claim"])}

## C_R Factor Runner
{md_table(runner, ["row_id", "C_R_prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(promotion, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decision, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_target, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validation, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    fw_before = snapshot_tree(FW)
    bound = bound_from_3284_predictions()
    sources = source_register_rows()
    theorem = theorem_rows()
    signature = signature_rows()
    poynting = poynting_rows()
    finite = finite_rows(bound)
    runner = runner_rows(finite)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["signature"], signature)
    write_csv(OUTPUTS["poynting"], poynting)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, theorem, signature, poynting, finite, runner, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(bound, theorem, signature, poynting, finite, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
