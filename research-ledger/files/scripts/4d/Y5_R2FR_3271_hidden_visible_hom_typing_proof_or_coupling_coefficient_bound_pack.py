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

DOC = ROOT / "3271-Y5-R2FR-hidden-visible-hom-typing-proof-or-coupling-coefficient-bound-pack-under-AX1090.md"

SRC_3270_DOC = ROOT / "3270-Y5-R2FR-no-direct-visible-constant-vertex-or-finite-coefficient-fill-under-AX1090.md"
SRC_3270_THEOREM = OUT / "P8_Y5_R2FR_3270_NO_DIRECT_VERTEX_THEOREM_OR_NO_GO.csv"
SRC_3270_VERTEX = OUT / "P8_Y5_R2FR_3270_VISIBLE_VERTEX_CLASSIFICATION.csv"
SRC_3270_FINITE = OUT / "P8_Y5_R2FR_3270_FINITE_VERTEX_COEFFICIENT_ROWS_NONCLAIM.csv"
SRC_3270_RUNNER = OUT / "P8_Y5_R2FR_3270_VERTEX_DD_RUNNER_RESULTS_NONCLAIM.csv"
SRC_3270_NEXT = OUT / "P8_Y5_R2FR_3270_NEXT_TARGET.csv"
SRC_1933_QDT = OUT / "P8_Y5_PARENT_QLOC_1933_QUOTIENT_DESCENT_THEOREM.csv"
SRC_1933_TYPE = OUT / "P8_Y5_PARENT_QLOC_1933_COEFFICIENT_DESCENT_TYPING_AUDIT.csv"
SRC_1933_RES = OUT / "P8_Y5_PARENT_QLOC_1933_FIBER_RESIDUAL_LEDGER.csv"
SRC_2658_NQD = OUT / "P8_Y5_NQD_MOMS_2658_NEIGHBOURHOOD_DESCENT_ATTEMPT.csv"
SRC_2658_MOMS = OUT / "P8_Y5_NQD_MOMS_2658_MOMS_SIGNATURE_SOURCE_MAP.csv"
SRC_2659_ODT = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
SRC_2659_RED = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv"
SRC_2659_FIN = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_FINITE_COUPLING_RESIDUAL_VECTOR_NONCLAIM.csv"
SRC_2659_CM = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_COUNTERMODEL_LEDGER.csv"
SRC_1091_ODH = OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
SRC_1091_FIN = OUT / "P8_Y5_R10_1091_FINITE_RESIDUAL_ROUTE_MAP.csv"
SRC_980_NMF = OUT / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"
SRC_1051_NMM = OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
SRC_1105_MHM = OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv"
SRC_1105_SUB = OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_SUBCASE_MAP.csv"
SRC_3265_DELTA = OUT / "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv"
SRC_3266_GAIN = OUT / "P8_Y5_R2FR_3266_MATRIX_INVERSE_AND_RESIDUAL_GAINS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3271_SOURCE_REGISTER.csv",
    "fiber_theorem": OUT / "P8_Y5_R2FR_3271_QUOTIENT_FIBER_DESCENT_THEOREM.csv",
    "proof_matrix": OUT / "P8_Y5_R2FR_3271_HIDDEN_VISIBLE_TYPING_PROOF_MATRIX.csv",
    "connected_labels": OUT / "P8_Y5_R2FR_3271_CONNECTED_BRANCH_LABEL_LEMMA.csv",
    "envelopes": OUT / "P8_Y5_R2FR_3271_COEFFICIENT_ENVELOPES_NONCLAIM.csv",
    "bound_pack": OUT / "P8_Y5_R2FR_3271_COUPLING_BOUND_PACK_NONCLAIM.csv",
    "branch_runner": OUT / "P8_Y5_R2FR_3271_BRANCH_RUNNER_RESULTS.csv",
    "promotion": OUT / "P8_Y5_R2FR_3271_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3271_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3271_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3271_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


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


def compact(value: str, limit: int = 360) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    hits: list[str] = []
    lowered = [needle.lower() for needle in needles]
    for idx, line in enumerate(text, start=1):
        low = line.lower()
        if any(needle in low for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 240)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3270_DOC, "3270 handoff to hidden-visible typing proof", ["NEXT3270", "Hom(A_hid", "fallback is executable"]),
        (SRC_3270_THEOREM, "3270 no-direct-vertex theorem/no-go", ["NVT3270_0", "NVT3270_2", "Hom"]),
        (SRC_3270_VERTEX, "3270 visible vertex classification", ["alpha_F2", "source_weight", "hidden_frame"]),
        (SRC_3270_FINITE, "3270 finite visible coefficient rows", ["MISSING_PARENT_VALUE", "SOURCE_ONLY_SLOT_UNSIGNED"]),
        (SRC_3270_RUNNER, "3270 DD/residual runner", ["VCASE3270_3", "FAILS_NUMERIC_SMOKE"]),
        (SRC_3270_NEXT, "3270 selected next target", ["NEXT3270_0_3271", "Hom(A_hid"]),
        (SRC_1933_QDT, "exact quotient descent theorem", ["QDT1933_0", "fiber", "descends"]),
        (SRC_1933_TYPE, "coefficient descent typing audit", ["TYPE1933_1", "TYPE1933_3", "verdict"]),
        (SRC_1933_RES, "fiber residual ledger", ["RES1933_0", "source_weight", "mass"]),
        (SRC_2658_NQD, "neighbourhood descent attempt", ["NQD2658_2", "fibre-invariance", "COUNTERMODELS"]),
        (SRC_2658_MOMS, "MOMS source signature map", ["MOMS2658_1", "MOMS2658_4", "MOMS2658_6"]),
        (SRC_2659_ODT, "operator-domain theorem attempt", ["ODT2659_1", "ODT2659_6", "A_ord"]),
        (SRC_2659_RED, "operator-domain proof reduction matrix", ["RED2659_0", "RED2659_7"]),
        (SRC_2659_FIN, "finite coupling residual vector", ["FRV2659_0", "FRV2659_6"]),
        (SRC_2659_CM, "countermodel ledger", ["CM2659_0", "CM2659_5"]),
        (SRC_1091_ODH, "earlier operator-domain theorem attempt", ["ODH1091_1", "ODH1091_2", "verdict"]),
        (SRC_1091_FIN, "earlier finite residual route map", ["FR1091_0", "qbar_source"]),
        (SRC_980_NMF, "no-marker scalar obstruction", ["NMF980_2", "NMF980_3", "NMF980_7"]),
        (SRC_1051_NMM, "no-mixed/radiative closure audit", ["NMM1051", "verdict", "radiative"]),
        (SRC_1105_MHM, "master morphism theorem attempt", ["MHM1105_1", "MHM1105_6"]),
        (SRC_1105_SUB, "master morphism subcase map", ["SUB1105_0", "SUB1105_2", "SUB1105_4"]),
        (SRC_3265_DELTA, "two-arena DD material-charge matrix", ["MICROSCOPE", "EOTWASH", "Delta_Q"]),
        (SRC_3266_GAIN, "two-channel inverse bounds and residual gains", ["zero_residual", "Dhatm_bound", "De_bound"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3271_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def fiber_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "QFT3271_0_descent_iff_fiber_constant",
            "claim_piece": "quotient descent equivalence",
            "formal_statement": "For a surjective quotient/submersion q:P->Q with connected fibres, a visible coefficient c:P->V descends as c=cbar∘q iff c is constant on every q-fibre.",
            "proof": "If c=cbar∘q then equal q-values give equal c. Conversely define cbar(q(p))=c(p); fibre constancy makes this well-defined. Smoothness follows locally for a submersion.",
            "status": "EXACT_THEOREM",
            "effect": "No hidden-visible coefficient map is equivalent to proving fibre constancy for every visible coefficient.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QFT3271_1_vertical_derivative_zero",
            "claim_piece": "local vertical silence",
            "formal_statement": "If c descends and v in ker(Dq), then L_v c=dc(v)=0.",
            "proof": "c=q*cbar, so dc(v)=dcbar(Dq v)=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "effect": "This is the clean route to b_alpha=b_hatm=Delta_w=b_clock=0, but only after the relevant coefficient descends.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QFT3271_2_typed_visible_algebra",
            "claim_piece": "hidden-visible hom typing theorem",
            "formal_statement": "If A_ord = q* A_Q ⊗ A_fixed and ordinary coefficients are sections of A_ord only, then Hom(A_hid,Coeff_vis) has no nonconstant vertical component.",
            "proof": "Every allowed coefficient is a q-pullback times fixed representation data. QFT3271_1 kills the q-pullback derivative, and fixed data have zero vertical derivative by type.",
            "status": "EXACT_TYPED_DOMAIN_THEOREM",
            "effect": "This proves the desired beam if the parent action signs the ordinary visible coefficient algebra.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QFT3271_3_hidden_scalar_no_go",
            "claim_piece": "why the proof cannot come from covariance alone",
            "formal_statement": "If a nonconstant hidden scalar I survives and Coeff_vis accepts scalar functions, c=c0+epsilon I is a legal non-descended coefficient with L_v c=epsilon L_v I.",
            "proof": "c is a scalar coefficient and respects observed-frame covariance; it fails fibre constancy whenever I varies along q-fibres.",
            "status": "COUNTEREXAMPLE_THEOREM",
            "effect": "The parent must either trivialize hidden invariants or remove their target slots; symmetry slogans cannot do it.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QFT3271_4_current_MTS_status",
            "claim_piece": "current promotion status",
            "formal_statement": "Current MTS has exact quotient math and exact typed-domain theorem, but not the parent signature A_ord=q*A_Q⊗A_fixed plus readout/radiative/source stability.",
            "proof": "1933, 2658, 2659, 1091, 1105 all mark the parent signature or scalar obstruction as unsigned.",
            "status": "THEOREM_CONTRACT_BUILT_NOT_PARENT_SIGNED",
            "effect": "No local-GR/WEP/Maxwell claim is promoted; finite coefficient bounds become the honest fallback.",
            "valid_for_claim": "false",
        },
    ]


def proof_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "reduction_id": "RED3271_0_quotient_submersion",
            "needed_signature": "q:P->Q is the parent-visible quotient and local MTS variations are vertical",
            "mathematical_role": "defines fibres and ker(Dq)",
            "if_signed": "QFT3271_0 and QFT3271_1 can be applied coefficient-by-coefficient",
            "current_status": "CONDITIONAL_AVAILABLE",
            "source": "1933 QDT; 2658 NQD",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3271_1_visible_coefficient_algebra",
            "needed_signature": "A_ord=q*A_Q⊗A_fixed for visible ordinary coefficients",
            "mathematical_role": "forbids hidden fibre functions as coefficient arguments",
            "if_signed": "Hom(A_hid,Coeff_vis)=Const/0 by QFT3271_2",
            "current_status": "NOT_PARENT_SIGNED",
            "source": "2659 RED2659_0; 3270 NVT3270_1",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3271_2_fixed_representation_constants",
            "needed_signature": "alpha_EM, masses, charge lattice, clock constants and material labels are fixed representation/topological data",
            "mathematical_role": "zeros vertical derivatives of fixed data",
            "if_signed": "constant-sector and DD coefficients become theorem-zero rather than fitted",
            "current_status": "UNSIGNED_CONSTANT_SECTOR",
            "source": "2658 MOMS2658_3; 3269 FC3269_0-3",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3271_3_no_hidden_scalar_target",
            "needed_signature": "either hidden invariant algebra is trivial or hidden invariants have no target in Coeff_vis",
            "mathematical_role": "kills c=c0+epsilon I counterexample",
            "if_signed": "alpha/mass/source/clock/frame slots cannot receive hidden coefficient maps",
            "current_status": "SCALAR_COUNTEREXAMPLE_ACTIVE",
            "source": "980 NMF980_2; 1091 ODH1091_2; 1105 MHM1105_3",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3271_4_readout_radiative_stability",
            "needed_signature": "S_eff, clocks, material readout, source projection and boundary selectors preserve coefficient descent",
            "mathematical_role": "prevents re-entry after a bare no-hidden-visible rule",
            "if_signed": "tree-level proof survives observed tests",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "source": "1091 ODH1091_5; 1105 MHM1105_5",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3271_5_source_measure_current_owner",
            "needed_signature": "one action measure/current owner; no source-only species weights",
            "mathematical_role": "separates DD alpha/mass coefficients from epsilon/source-normalization residuals",
            "if_signed": "Delta_w_AB and source-only WEP/Newton source leakage vanish",
            "current_status": "SOURCE_COUPLING_BOTTLENECK_UNSIGNED",
            "source": "1065; 2659 RED2659_4; 3270 VTX3270_2",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def connected_label_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "CBL3271_0_discrete_label_constant",
            "statement": "A continuous map from a connected local branch into a discrete representation-label space is constant.",
            "proof": "The image of a connected set under a continuous map is connected; connected subsets of a discrete space are singletons.",
            "what_it_closes": "species labels and topological sectors can be locally fixed if the branch is connected and no domain wall/idempotent selector is crossed.",
            "what_it_does_not_close": "continuous constants like alpha_EM, mass ratios, clock ratios, source weights, conformal/disformal factors.",
            "current_status": "HELPFUL_PARTIAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "CBL3271_1_wall_or_selector_escape",
            "statement": "If a domain wall, material selector, idempotent branch label, or post-readout mask is allowed, the connected-label lemma does not apply globally.",
            "proof": "The branch is then either disconnected in the relevant topology or the label is not a continuous function on the same parent object.",
            "what_it_closes": "prevents overclaiming discrete-label constancy beyond a single connected local sector.",
            "what_it_does_not_close": "source-worldtube, support, boundary and readout selector debts.",
            "current_status": "GUARD",
            "valid_for_claim": "false",
        },
    ]


def delta_rows() -> list[dict[str, str]]:
    return read_csv(SRC_3265_DELTA)


def gain_rows() -> list[dict[str, str]]:
    return read_csv(SRC_3266_GAIN)


def single_channel_bound(delta_key: str) -> tuple[float, str, str]:
    candidates: list[tuple[float, str, str]] = []
    for row in delta_rows():
        coeff = abs(float(row[delta_key]))
        if coeff == 0:
            continue
        bound = float(row["eta_abs_bound"]) / coeff
        candidates.append((bound, row["arena"], row["row_id"]))
    return min(candidates, key=lambda item: item[0])


def zero_residual_gain() -> dict[str, str]:
    for row in gain_rows():
        if row["scenario"] == "zero_residual":
            return row
    raise ValueError("zero_residual gain row missing")


def coefficient_envelope_rows() -> list[dict[str, Any]]:
    pure_hatm, hatm_arena, hatm_source = single_channel_bound("Delta_Qhatm_prime")
    pure_alpha, alpha_arena, alpha_source = single_channel_bound("Delta_Qe_prime")
    gains = zero_residual_gain()
    micro = next(row for row in delta_rows() if "MICROSCOPE" in row["arena"])
    eot = next(row for row in delta_rows() if "EOTWASH" in row["arena"])
    return [
        {
            "envelope_id": "ENV3271_0_pure_alpha_no_cancellation",
            "channel": "pure_alpha_or_EM_vertex",
            "assumption": "only C_e nonzero; C_g=C_hatm=epsilon_k=0",
            "formula": "abs(C_e) <= min_k eta_bound_k / abs(Delta_Qe_k)",
            "bound_value": fmt(pure_alpha),
            "bound_units": "dimensionless local logarithmic coefficient",
            "limiting_arena": alpha_arena,
            "source_row": alpha_source,
            "use": "strict private envelope for a single hidden alpha/F2 leak; no DD cancellation allowed",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3271_1_pure_hatm_no_cancellation",
            "channel": "pure_hatm_or_mass_vertex",
            "assumption": "only D_hatm=C_hatm-C_g nonzero; C_e=epsilon_k=0",
            "formula": "abs(D_hatm) <= min_k eta_bound_k / abs(Delta_Qhatm_k)",
            "bound_value": fmt(pure_hatm),
            "bound_units": "dimensionless local logarithmic coefficient",
            "limiting_arena": hatm_arena,
            "source_row": hatm_source,
            "use": "strict private envelope for a single hidden mass/hatm leak; no DD cancellation allowed",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3271_2_two_channel_zero_residual",
            "channel": "mixed_Dhatm_De",
            "assumption": "D_hatm and D_e may both be nonzero; epsilon_k=0; two-arena inverse used",
            "formula": "|D_hatm|<=abs(A^-1 row0).eta_bounds; |D_e|<=abs(A^-1 row1).eta_bounds",
            "bound_value": f"D_hatm<={gains['Dhatm_bound']};D_e<={gains['De_bound']}",
            "bound_units": "dimensionless local logarithmic coefficient",
            "limiting_arena": "two_arena_inverse",
            "source_row": "P8_Y5_R2FR_3266_MATRIX_INVERSE_AND_RESIDUAL_GAINS.csv:GAIN3266_1_zero_residual",
            "use": "mixed-channel conservative envelope when alpha/mass cancellation is allowed by the model",
            "valid_for_claim": "false",
        },
        {
            "envelope_id": "ENV3271_3_source_weight_epsilon",
            "channel": "source_weight_or_nonDD_epsilon",
            "assumption": "source-only term is not mapped into C_parent and must fit absolute eta residual directly",
            "formula": "epsilon_MICROSCOPE<=eta_MICROSCOPE_bound and epsilon_EOTWASH<=eta_EOTWASH_bound",
            "bound_value": f"epsilon_MICROSCOPE<={micro['eta_abs_bound']};epsilon_EOTWASH<={eot['eta_abs_bound']}",
            "bound_units": "absolute eta residual",
            "limiting_arena": "MICROSCOPE_TIPT_EARTH_FIELD",
            "source_row": "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv",
            "use": "source-only couplings cannot hide in alpha/mass C; they are separate residual budgets",
            "valid_for_claim": "false",
        },
    ]


def coupling_bound_pack_rows() -> list[dict[str, Any]]:
    envelopes = {row["envelope_id"]: row for row in coefficient_envelope_rows()}
    return [
        {
            "coefficient_id": "PACK3271_0_b_alpha",
            "coefficient": "b_alpha or C_e",
            "arena_pressure": "WEP/DD, clocks, R10, Maxwell normalization",
            "zero_route": "QFT3271_2 plus unique Maxwell subblock/readout closure",
            "strict_private_bound": envelopes["ENV3271_0_pure_alpha_no_cancellation"]["bound_value"],
            "bound_type": "single-channel no-cancellation envelope",
            "missing_for_claim": "parent alpha owner or sourced b_alpha value with tau/projection rows",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "PACK3271_1_D_hatm",
            "coefficient": "D_hatm=C_hatm-C_g",
            "arena_pressure": "WEP/DD mass and nuclear response",
            "zero_route": "QFT3271_2 plus fixed matter spectrum/binding descent",
            "strict_private_bound": envelopes["ENV3271_1_pure_hatm_no_cancellation"]["bound_value"],
            "bound_type": "single-channel no-cancellation envelope",
            "missing_for_claim": "parent matter spectrum owner or sourced b_hatm/b_nuc value",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "PACK3271_2_mixed_DD",
            "coefficient": "D_hatm and D_e together",
            "arena_pressure": "two-channel DD fit with possible model cancellation",
            "zero_route": "same as alpha plus mass zero routes",
            "strict_private_bound": envelopes["ENV3271_2_two_channel_zero_residual"]["bound_value"],
            "bound_type": "two-channel inverse envelope",
            "missing_for_claim": "real model coefficient vector and residual epsilons",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "PACK3271_3_Delta_w",
            "coefficient": "Delta_w_AB or qbar_source_label",
            "arena_pressure": "WEP/source normalization, Newtonian GM, local-GR source side",
            "zero_route": "no-source-only-slot grammar plus common measure/current owner",
            "strict_private_bound": envelopes["ENV3271_3_source_weight_epsilon"]["bound_value"],
            "bound_type": "absolute epsilon residual envelope",
            "missing_for_claim": "source-weight theorem-zero or sourced Delta_w*tau projection",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "PACK3271_4_frame_readout",
            "coefficient": "c_g, b_dis, b_clock, readout/radiative return",
            "arena_pressure": "PPN, clocks, orbital, R10/readout",
            "zero_route": "single observed coframe plus no-shadow/readout/radiative stability",
            "strict_private_bound": "NO_DD_BOUND_DO_NOT_PROJECT",
            "bound_type": "route to PPN/clock/orbital vector",
            "missing_for_claim": "arena projection maps with units; no tau=1 shortcut",
            "valid_for_claim": "false",
        },
    ]


def branch_runner_rows() -> list[dict[str, Any]]:
    env = {row["envelope_id"]: row for row in coefficient_envelope_rows()}
    return [
        {
            "case_id": "BR3271_0_typed_visible_algebra_signed",
            "premise": "A_ord=q*A_Q⊗A_fixed and readout/source/radiative closure are parent-signed",
            "result": "Hom(A_hid,Coeff_vis)=Const/0; vertical coefficient derivatives vanish",
            "alpha_status": "theorem_zero",
            "mass_status": "theorem_zero",
            "source_weight_status": "theorem_zero_if_measure_current_owner_signed",
            "frame_status": "theorem_zero_if_single_observed_frame_signed",
            "claim_status": "CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "BR3271_1_discrete_connected_labels_only",
            "premise": "connected branch and discrete representation labels, but no continuous coefficient typing",
            "result": "species labels/topological sectors locally constant; alpha, masses, source weights and frame coefficients remain live",
            "alpha_status": "retained",
            "mass_status": "retained",
            "source_weight_status": "retained",
            "frame_status": "retained",
            "claim_status": "PARTIAL_PROOF_ONLY",
            "valid_for_claim": "false",
        },
        {
            "case_id": "BR3271_2_hidden_scalar_survives",
            "premise": "nonconstant hidden scalar I_hid exists and coefficient target slot is legal",
            "result": "c=c0+epsilon I_hid violates fibre constancy and reopens visible couplings",
            "alpha_status": f"bound_if_pure_single_channel<={env['ENV3271_0_pure_alpha_no_cancellation']['bound_value']}",
            "mass_status": f"bound_if_pure_single_channel<={env['ENV3271_1_pure_hatm_no_cancellation']['bound_value']}",
            "source_weight_status": "epsilon_bound_required",
            "frame_status": "route_to_PPN_clock_orbital",
            "claim_status": "COUNTERMODEL_BRANCH_ACTIVE",
            "valid_for_claim": "false",
        },
        {
            "case_id": "BR3271_3_single_alpha_or_mass_testing_branch",
            "premise": "a future MTS parent predicts only one DD coefficient at a time",
            "result": "use strict no-cancellation envelopes before any two-channel cancellation fit",
            "alpha_status": env["ENV3271_0_pure_alpha_no_cancellation"]["bound_value"],
            "mass_status": env["ENV3271_1_pure_hatm_no_cancellation"]["bound_value"],
            "source_weight_status": "not_in_C_parent",
            "frame_status": "not_DD_projectable",
            "claim_status": "TESTING_BRANCH_READY_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    env = {row["envelope_id"]: row for row in coefficient_envelope_rows()}
    pure_alpha = float(env["ENV3271_0_pure_alpha_no_cancellation"]["bound_value"])
    pure_hatm = float(env["ENV3271_1_pure_hatm_no_cancellation"]["bound_value"])
    gains = zero_residual_gain()
    return [
        {
            "gate_id": "PG3271_0_exact_quotient_theorem",
            "gate": "descent iff fibre constancy theorem is exact",
            "passed": "true",
            "reason": "QFT3271_0/QFT3271_1 give the precise mathematical condition",
            "claim_allowed": "false",
        },
        {
            "gate_id": "PG3271_1_parent_visible_algebra_signed",
            "gate": "A_ord=q*A_Q⊗A_fixed is parent-signed",
            "passed": "false",
            "reason": "2659/1933 mark visible coefficient algebra typing as not parent-signed",
            "claim_allowed": "false",
        },
        {
            "gate_id": "PG3271_2_hidden_scalar_removed",
            "gate": "hidden scalar counterexample is removed or has no visible coefficient target",
            "passed": "false",
            "reason": "980/1091/1105 retain the scalar obstruction",
            "claim_allowed": "false",
        },
        {
            "gate_id": "PG3271_3_single_channel_bounds_sharpened",
            "gate": "single alpha/mass envelopes are stricter than mixed two-channel inverse bounds",
            "passed": bool_str(pure_alpha < float(gains["De_bound"]) and pure_hatm < float(gains["Dhatm_bound"])),
            "reason": f"pure_alpha={fmt(pure_alpha)} vs mixed_De={gains['De_bound']}; pure_hatm={fmt(pure_hatm)} vs mixed_Dhatm={gains['Dhatm_bound']}",
            "claim_allowed": "false",
        },
        {
            "gate_id": "PG3271_4_source_weight_separate",
            "gate": "source-only weights are kept out of C_parent and bounded as epsilon/source residuals",
            "passed": "true",
            "reason": "ENV3271_3 routes source weights to eta residual budgets, not alpha/mass DD coordinates",
            "claim_allowed": "false",
        },
        {
            "gate_id": "PG3271_5_local_GR",
            "gate": "local GR/Newton/Maxwell/PPN promotion",
            "passed": "false",
            "reason": "3271 closes a proof contract and bounds fallback coefficients; it does not close EH/source/Bianchi/PPN/readout gates",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    env = {row["envelope_id"]: row for row in coefficient_envelope_rows()}
    return [
        {
            "decision_id": "DEC3271_0_theorem_result",
            "verdict": "EXACT_DESCENT_THEOREM_LOCKED_PARENT_TYPING_UNSIGNED",
            "what_moved": "The coupling beam is now an exact fibre-constancy problem: visible coefficients descend iff they are constant on q-fibres; typed A_ord=q*A_Q⊗A_fixed would prove Hom(A_hid,Coeff_vis)=Const/0.",
            "hard_result": "Covariance/gauge symmetry is insufficient; a hidden scalar coefficient remains a counterexample unless its target slot is forbidden.",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3271_1_empirical_result",
            "verdict": "SINGLE_CHANNEL_DD_ENVELOPES_SHARPENED",
            "what_moved": f"Pure alpha leak bound is {env['ENV3271_0_pure_alpha_no_cancellation']['bound_value']}; pure mass/hatm leak bound is {env['ENV3271_1_pure_hatm_no_cancellation']['bound_value']} before cancellation games.",
            "hard_result": "If MTS predicts a single hidden-visible coupling, it faces the stricter no-cancellation envelope, not the looser mixed two-channel inverse.",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3271_0_3272",
            "selected": "primary",
            "target_doc": "3272-Y5-R2FR-parent-visible-coefficient-algebra-construction-or-first-real-coupling-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3272_parent_visible_coefficient_algebra_construction_or_first_real_coupling_row.py",
            "objective": "Try to construct the parent ordinary visible coefficient algebra A_ord=q*A_Q⊗A_fixed from MTS quotient/category primitives. If it cannot be signed, choose the first real finite coupling row: alpha/EM, D_hatm, or source-weight, using the strict 3271 envelopes.",
            "guardrail": "Do not repeat the theorem contract unless a new parent construction signs A_ord; otherwise move to the first sourced coefficient row.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def output_csvs_parse() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not csv_parse_ok(path):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    sources = source_register()
    env = {row["envelope_id"]: row for row in coefficient_envelope_rows()}
    gains = zero_residual_gain()
    gates = promotion_gate_rows()
    validations = [
        {
            "check_id": "VAL3271_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3271_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3271_2_outputs_parse",
            "check": "all 3271 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3271_3_exact_theorem_present",
            "check": "descent iff fibre constancy theorem and counterexample theorem are present",
            "passed": bool_str(any(row["theorem_id"] == "QFT3271_0_descent_iff_fiber_constant" for row in fiber_theorem_rows()) and any(row["theorem_id"] == "QFT3271_3_hidden_scalar_no_go" for row in fiber_theorem_rows())),
            "detail": "QFT3271_0 and QFT3271_3 found",
        },
        {
            "check_id": "VAL3271_4_single_channel_bounds_positive",
            "check": "single-channel alpha and hatm bounds are positive numeric values",
            "passed": bool_str(float(env["ENV3271_0_pure_alpha_no_cancellation"]["bound_value"]) > 0 and float(env["ENV3271_1_pure_hatm_no_cancellation"]["bound_value"]) > 0),
            "detail": f"alpha={env['ENV3271_0_pure_alpha_no_cancellation']['bound_value']};hatm={env['ENV3271_1_pure_hatm_no_cancellation']['bound_value']}",
        },
        {
            "check_id": "VAL3271_5_single_channel_stricter_than_mixed",
            "check": "single-channel envelopes are stricter than mixed two-channel inverse bounds",
            "passed": bool_str(float(env["ENV3271_0_pure_alpha_no_cancellation"]["bound_value"]) < float(gains["De_bound"]) and float(env["ENV3271_1_pure_hatm_no_cancellation"]["bound_value"]) < float(gains["Dhatm_bound"])),
            "detail": f"mixed_De={gains['De_bound']};mixed_Dhatm={gains['Dhatm_bound']}",
        },
        {
            "check_id": "VAL3271_6_source_weight_not_C_parent",
            "check": "source-weight branch remains an epsilon/source residual, not a DD C_parent coordinate",
            "passed": bool_str("epsilon" in env["ENV3271_3_source_weight_epsilon"]["channel"]),
            "detail": env["ENV3271_3_source_weight_epsilon"]["bound_value"],
        },
        {
            "check_id": "VAL3271_7_claim_gates_false",
            "check": "no 3271 gate allows WEP/local-GR promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3271_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3271_9_overall",
            "check": "3271 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3271_9_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    sources = read_csv(OUTPUTS["sources"])
    fiber = read_csv(OUTPUTS["fiber_theorem"])
    proof = read_csv(OUTPUTS["proof_matrix"])
    labels = read_csv(OUTPUTS["connected_labels"])
    envelopes = read_csv(OUTPUTS["envelopes"])
    pack = read_csv(OUTPUTS["bound_pack"])
    branches = read_csv(OUTPUTS["branch_runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3271 - Hidden-visible hom typing proof or coupling coefficient bound pack under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3271` locks the real mathematical throat: a visible coefficient descends through `q` iff it is constant on `q`-fibres.
- Therefore `Hom(A_hid,Coeff_vis)=Const/0` is not a vibe; it is exactly the parent claim that `A_ord=q*A_Q⊗A_fixed` and readout/source/radiative maps preserve that typing.
- The current MTS corpus still has the theorem contract, not the parent signature.
- New useful pressure: if a future parent predicts a single pure alpha or mass leak, it faces the strict no-cancellation envelopes in `3271`, not the looser mixed two-channel bounds.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## Quotient/Fibre Descent Theorem
{md_table(fiber, ["theorem_id", "claim_piece", "formal_statement", "proof", "status", "effect", "valid_for_claim"])}

## Hidden-Visible Typing Proof Matrix
{md_table(proof, ["reduction_id", "needed_signature", "mathematical_role", "if_signed", "current_status", "source", "parent_signed", "valid_for_claim"])}

## Connected-Branch Label Lemma
{md_table(labels, ["lemma_id", "statement", "proof", "what_it_closes", "what_it_does_not_close", "current_status", "valid_for_claim"])}

## Coefficient Envelopes
{md_table(envelopes, ["envelope_id", "channel", "assumption", "formula", "bound_value", "bound_units", "limiting_arena", "use", "valid_for_claim"])}

## Coupling Bound Pack
{md_table(pack, ["coefficient_id", "coefficient", "arena_pressure", "zero_route", "strict_private_bound", "bound_type", "missing_for_claim", "valid_for_claim"])}

## Branch Runner
{md_table(branches, ["case_id", "premise", "result", "alpha_status", "mass_status", "source_weight_status", "frame_status", "claim_status", "valid_for_claim"])}

## Promotion Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "hard_result", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_key = {
        "sources": source_register(),
        "fiber_theorem": fiber_theorem_rows(),
        "proof_matrix": proof_matrix_rows(),
        "connected_labels": connected_label_rows(),
        "envelopes": coefficient_envelope_rows(),
        "bound_pack": coupling_bound_pack_rows(),
        "branch_runner": branch_runner_rows(),
        "promotion": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
