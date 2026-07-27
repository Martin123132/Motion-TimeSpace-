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
DOC = ROOT / "3383-Y5-R2FR-UOC-extra-MTSIR-local-PPN-residual-vector-or-zero-theorem-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3383_SOURCE_REGISTER.csv",
    "reduction": OUT / "P8_Y5_R2FR_3383_POST_UOC_PPN_REDUCTION.csv",
    "residual_vector": OUT / "P8_Y5_R2FR_3383_EXTRA_MTSIR_PPN_RESIDUAL_VECTOR.csv",
    "zero_theorem": OUT / "P8_Y5_R2FR_3383_ZERO_THEOREM_ATTEMPT.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3383_BOUND_ROWS_NONCLAIM.csv",
    "component_status": OUT / "P8_Y5_R2FR_3383_COMPONENT_STATUS_MATRIX.csv",
    "runner": OUT / "P8_Y5_R2FR_3383_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3383_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3383_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3383_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3383_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3383_0_3382_doc", ROOT / "3382-Y5-R2FR-UOC-local-GR-Newton-PPN-EM-stress-chain-under-AX1090.md", "3382 UOC local-GR/Newton/PPN/EM chain"),
    ("SRC3383_1_3382_ppn", OUT / "P8_Y5_R2FR_3382_PPN_RESIDUAL_VECTOR_UNDER_UOC.csv", "3382 PPN residual handoff"),
    ("SRC3383_2_3382_action", OUT / "P8_Y5_R2FR_3382_LOCAL_ACTION_BLOCK_UNDER_UOC.csv", "3382 UOC local action block"),
    ("SRC3383_3_3330_doc", ROOT / "3330-Y5-R2FR-PPN-response-coefficient-and-local-floor-bound-under-AX1090.md", "PPN response coefficient and local floor"),
    ("SRC3383_4_3331_doc", ROOT / "3331-Y5-R2FR-PPN-weak-potential-normalization-and-Cmetric-bound-under-AX1090.md", "PPN weak-potential normalization"),
    ("SRC3383_5_3332_doc", ROOT / "3332-Y5-R2FR-PPN-epsilon-eff-and-floor-specialization-under-AX1090.md", "PPN epsilon_eff and floor budget"),
    ("SRC3383_6_3333_doc", ROOT / "3333-Y5-R2FR-PPN-zero-floor-branch-certificate-under-AX1090.md", "PPN zero-floor branch certificate"),
    ("SRC3383_7_3331_cppn", OUT / "P8_Y5_R2FR_3331_CPPN_COMPOSITION.csv", "C_PPN <= A_PPN C_metric composition"),
    ("SRC3383_8_3332_budget", OUT / "P8_Y5_R2FR_3332_NORMALIZED_PPN_BUDGET.csv", "normalized PPN residual budget"),
    ("SRC3383_9_3333_budget", OUT / "P8_Y5_R2FR_3333_REDUCED_PPN_BUDGET.csv", "reduced PPN budget after zero floors"),
    ("SRC3383_10_3367_zero", OUT / "P8_Y5_R2FR_3367_RNONEH_ZERO_THEOREM_CONTRACT.csv", "non-EH charge zero theorem contract"),
    ("SRC3383_11_3367_decomp", OUT / "P8_Y5_R2FR_3367_RNONEH_CHARGE_DECOMPOSITION.csv", "non-EH charge decomposition"),
    ("SRC3383_12_3368_class", OUT / "P8_Y5_R2FR_3368_NONEH_OPERATOR_CLASSIFICATION.csv", "non-EH operator classification"),
    ("SRC3383_13_3372_transfer", OUT / "P8_Y5_R2FR_3372_HILBERT_SOURCE_TRANSFER_THEOREM_ATTEMPT.csv", "Hilbert-source transfer theorem"),
    ("SRC3383_14_3372_obstructions", OUT / "P8_Y5_R2FR_3372_TRANSFER_CHAIN_OBSTRUCTION_LEDGER.csv", "source-transfer obstruction ledger"),
    ("SRC3383_15_3373_commutator", OUT / "P8_Y5_R2FR_3373_PIM_CHAINMAP_COMMUTATOR_THEOREM_ATTEMPT.csv", "PiM commutator theorem"),
    ("SRC3383_16_3373_bounds", OUT / "P8_Y5_R2FR_3373_ICOMMUTATOR_OBSTRUCTION_ROWS_NONCLAIM.csv", "PiM commutator bound rows"),
    ("SRC3383_17_3374_same_object", OUT / "P8_Y5_R2FR_3374_SAME_OBJECT_LEMMA_ATTEMPT.csv", "topological-Hilbert same-object lemma"),
    ("SRC3383_18_3374_bounds", OUT / "P8_Y5_R2FR_3374_REQ_BOUND_ROWS_NONCLAIM.csv", "R_eq/B_zero bound rows"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def reduction_rows() -> list[dict[str, str]]:
    return [
        {
            "reduction_id": "RED3383_0_pre_uoc",
            "branch_stage": "before UOC",
            "symbolic_budget": "R_PPN <= source_prefactors + direct_vertices + G_closure + Gamma_floor + A_PPN C_metric epsilon_eff^2 + epsilon_composite + projector/boundary/topology",
            "meaning": "source coupling and extra local tensor effects were mixed",
            "status_after_3383": "SUPERSEDED_BY_UOC_SPLIT",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3383_1_under_uoc",
            "branch_stage": "under explicit UOC",
            "symbolic_budget": "R_PPN^UOC <= |R_Gamma_const_or_proxy| + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN + R_nonEH_tail + R_transfer_tail",
            "meaning": "source-prefactor/direct-G closure fog is removed; actual remaining local tensor/source-transfer tails are exposed",
            "status_after_3383": "ACTIVE_REDUCED_BUDGET_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3383_2_zero_target",
            "branch_stage": "zero theorem target",
            "symbolic_budget": "R_PPN^UOC=0 through tested order if all residual vector components are common-mode, exact zero-flux, projector-chainmap zero, public EM/Hilbert-owned, and Gamma/local-response silent",
            "meaning": "this is the exact theorem target, not a completed proof",
            "status_after_3383": "ZERO_THEOREM_CONTRACT",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "RED3383_3_bound_target",
            "branch_stage": "finite bound fallback",
            "symbolic_budget": "R_PPN^UOC < B_PPN componentwise with no-cancellation policy",
            "meaning": "if zero theorem fails, each residual must get a sourced numeric row",
            "status_after_3383": "BOUND_RUNNER_READY_NUMERIC_MISSING",
            "valid_for_claim": "false",
        },
    ]


def residual_vector_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "RV3383_0_common_EH_mode",
            "symbol": "a_common_EH",
            "definition": "universal source-blind EH-proportional local correction",
            "ppn_slot": "absorbed into measured G_ref/kappa if derivative-silent",
            "zero_or_absorb_route": "common EH-proportional mode only",
            "current_status": "ABSORBABLE_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "component_id": "RV3383_1_Gamma_floor",
            "symbol": "R_Gamma_const_or_proxy",
            "definition": "constant-curvature/local Gamma or saturation floor after pole/direct vertices are removed",
            "ppn_slot": "gamma,beta and nonconservative residuals through metric response",
            "zero_or_absorb_route": "Gamma readout/background with no independent local Hessian, or K_solar^m proxy below budget",
            "current_status": "PARTIAL_ZERO_FLOOR_BRANCH_NOT_FULLY_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "component_id": "RV3383_2_metric_response",
            "symbol": "A_PPN_C_metric_epsilon_eff2",
            "definition": "normalized metric operator response to residual MTS local fields",
            "ppn_slot": "full PPN vector through weak-field denominator q_U and gauge map",
            "zero_or_absorb_route": "C_metric=0, epsilon_eff=0, or sourced bound using A_PPN(q_U,gauge)",
            "current_status": "LIVE_PRIMARY_BOUND_OBJECT",
            "valid_for_claim": "false",
        },
        {
            "component_id": "RV3383_3_composite",
            "symbol": "epsilon_composite_PPN",
            "definition": "composite tree/mixing/background-gradient/boundary/kernel anisotropy residual",
            "ppn_slot": "gamma,beta,preferred-frame and clock/optical cross terms",
            "zero_or_absorb_route": "parent isotropy/no-gradient/no-boundary theorem or numeric envelope",
            "current_status": "LIVE_NUMERIC_OR_ZERO_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "component_id": "RV3383_4_nonEH_tail",
            "symbol": "R_nonEH_tail",
            "definition": "non-EH local operator charge contribution not common-mode absorbed",
            "ppn_slot": "Newton source normalization, PPN potentials, R10/orbital tails",
            "zero_or_absorb_route": "common EH proportional, exact zero-flux improvement, source-free massive tail, or bounded Yukawa/PPN row",
            "current_status": "LIVE_OPERATOR_CLASSIFICATION_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "component_id": "RV3383_5_transfer_tail",
            "symbol": "R_transfer_tail",
            "definition": "Hilbert-source transfer obstruction envelope",
            "ppn_slot": "source mass, measured GM, gamma/beta through source measure",
            "zero_or_absorb_route": "R_eq=0, I_commutator=0, B_zero_flux=0, epsilon_projector_stress=0, M_H_ref positive and same-frame",
            "current_status": "LIVE_CHAINMAP_TOPOLOGY_BOUND_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "component_id": "RV3383_6_hidden_EM",
            "symbol": "epsilon_EM_hidden",
            "definition": "hidden Hodge/direct EM vertex after public Maxwell branch",
            "ppn_slot": "EM stress, clocks, optical propagation, source charge",
            "zero_or_absorb_route": "public Maxwell/Hodge and no direct background/Poynting double count",
            "current_status": "ZERO_IN_PUBLIC_BRANCH_RESIDUAL_IF_HIDDEN_VERTEX_ADDED",
            "valid_for_claim": "false",
        },
        {
            "component_id": "RV3383_7_bianchi_exchange",
            "symbol": "epsilon_Bianchi_exchange",
            "definition": "divergence/exchange-current residue if K_MTS_IR is not separately conserved locally",
            "ppn_slot": "zeta_i, xi and nonconservative PPN components",
            "zero_or_absorb_route": "nabla_mu K_MTS_IR^munu=0 through PPN order or explicit exchange current below bounds",
            "current_status": "LIVE_CONSERVATION_GATE",
            "valid_for_claim": "false",
        },
    ]


def zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "ZERO3383_0_statement",
            "claim_piece": "post-UOC local PPN zero theorem",
            "statement": "Under UOC, local GR through PPN order follows if every extra MTS_IR contribution is either common EH-proportional and derivative-silent, exact zero-flux, projector-chainmap zero, public EM Hilbert stress, or high-order/bounded below the PPN budget.",
            "result": "VALID_CONDITIONAL_CONTRACT_NOT_CURRENT_CLAIM",
            "why_not_final": "several clauses are imported as conditional branch contracts rather than parent-signed MTS theorems",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZERO3383_1_common_mode",
            "claim_piece": "common EH mode",
            "statement": "a_common_EH E_EH can be absorbed into G_ref only if universal, source-blind and derivative-silent.",
            "result": "CONDITIONAL_PASS",
            "why_not_final": "operator classification marks parent_owned=false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZERO3383_2_direct_and_G_closure",
            "claim_piece": "direct vertex and measured-G closure floors",
            "statement": "UOC plus measured-G branch removes unlabelled direct source vertices and per-source G closure from the reduced budget.",
            "result": "BRANCH_ZERO_ACCEPTED_WITH_LABEL",
            "why_not_final": "this is a branch rule, not a derivation of G or UOC",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZERO3383_3_transfer_tail",
            "claim_piece": "Hilbert-source transfer tail",
            "statement": "R_transfer_tail vanishes only if Pi_M is a fixed q-basic chain map, the topological current is the same Hilbert source object, boundary flux is zero and M_H_ref is positive same-frame.",
            "result": "FAILS_AS_CURRENT_PROOF",
            "why_not_final": "3372-3374 leave R_eq, I_commutator, B_zero_flux, projector stress and M_H_ref unsigned/nonclaim",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZERO3383_4_metric_response",
            "claim_piece": "metric response floor",
            "statement": "A_PPN C_metric epsilon_eff^2 plus epsilon_composite must vanish or be bounded after gauge/GM modes are projected out.",
            "result": "FAILS_AS_CURRENT_PROOF",
            "why_not_final": "A_PPN, C_metric, epsilon_eff and composite source rows are not parent-signed numeric rows",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZERO3383_5_verdict",
            "claim_piece": "full PPN pass",
            "statement": "3383 reduces the local PPN problem but does not close it.",
            "result": "REDUCED_RESIDUAL_VECTOR_NOT_LOCAL_GR_PASS",
            "why_not_final": "live components remain in RV3383_1 through RV3383_5 and RV3383_7",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BND3383_0_Cmetric",
            "symbol": "C_metric",
            "bound_formula": "C_metric <= P_PPN^2 G_fix^2 W_src^2 D_readout^2 S_band^2 H_band(lambda) N_source",
            "required_inputs": "P_PPN,G_fix,W_src,D_readout,S_band,H_band,N_source,source_file",
            "current_status": "FORMULA_READY_NUMERIC_MISSING",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3383_1_RGamma",
            "symbol": "R_Gamma_const_or_proxy",
            "bound_formula": "|R_Gamma_const_or_proxy| < allocated_B_PPN_Gamma",
            "required_inputs": "Gamma local branch, constant/proxy certificate, allocated PPN budget",
            "current_status": "PARTIAL_ZERO_FLOOR_NUMERIC_OR_CERTIFICATE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3383_2_transfer",
            "symbol": "R_transfer_tail",
            "bound_formula": "(|R_eq_integral|+|I_commutator|+|B_zero_flux|)/|M_H_ref| + |epsilon_projector_stress|",
            "required_inputs": "R_eq_integral,I_commutator,B_zero_flux,M_H_ref,epsilon_projector_stress,source_file",
            "current_status": "SCHEMA_READY_NUMERIC_MISSING",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3383_3_nonEH",
            "symbol": "R_nonEH_tail",
            "bound_formula": "|R_nonEH[W,S]|/|M_H_ref| or PPN-projected operator norm",
            "required_inputs": "operator family, coefficient, source support, boundary flux, PPN projection, source_file",
            "current_status": "CLASSIFICATION_READY_NUMERIC_MISSING",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3383_4_bianchi",
            "symbol": "epsilon_Bianchi_exchange",
            "bound_formula": "||nabla_mu K_MTS_IR^munu - Q_exchange^nu||_PPN",
            "required_inputs": "local exchange current, conservation law, PPN component map, source_file",
            "current_status": "CONSERVATION_MAP_MISSING",
            "valid_for_claim": "false",
        },
    ]


def component_status_rows() -> list[dict[str, str]]:
    return [
        {"status_id": "STAT3383_0_killed_by_UOC", "component_group": "source-prefactor/direct source frame", "current_status": "KILLED_IN_UOC_BRANCH", "remaining_action": "keep UOC label explicit", "valid_for_claim": "false"},
        {"status_id": "STAT3383_1_absorbable", "component_group": "constant universal EH-proportional mode", "current_status": "ABSORBABLE_IF_SOURCE_BLIND", "remaining_action": "prove derivative-silent common mode or leave as delta_G", "valid_for_claim": "false"},
        {"status_id": "STAT3383_2_public_em", "component_group": "EM/Poynting public branch", "current_status": "PLACED_IN_HILBERT_STRESS", "remaining_action": "derive EM origin later; do not double count", "valid_for_claim": "false"},
        {"status_id": "STAT3383_3_live", "component_group": "metric response/Gamma/composite/nonEH/transfer/Bianchi", "current_status": "LIVE_LOCAL_PPN_BLOCKERS", "remaining_action": "zero theorem or finite bound runner", "valid_for_claim": "false"},
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {"run_id": "RUN3383_0_reduce_budget", "test": "reduce PPN budget after UOC", "result": "PASS_REDUCED_VECTOR_DEFINED", "detail": "source-prefactor fog is removed and live MTS_IR terms are named", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3383_1_zero_theorem", "test": "prove all live residuals zero through PPN order", "result": "FAILS_CURRENT_PROOF", "detail": "transfer tail, metric response, Gamma/composite and Bianchi components remain unsigned", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3383_2_bound_rows", "test": "stage finite bound fallback", "result": "PASS_NONCLAIM_BOUND_SCHEMA", "detail": "C_metric, Gamma, transfer, nonEH and Bianchi rows have formulas and missing inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"run_id": "RUN3383_3_firewall", "test": "prevent local-GR overclaim", "result": "PASS_CLAIM_FIREWALL", "detail": "full PPN pass remains false despite UOC/Newton/EM progress", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3383_0_sources", "claim": "all 3383 source paths exist and parse", "gate_pass": bool_text(source_ok), "reason": "source register validates UOC, PPN, nonEH and source-transfer inputs", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3383_1_reduced_vector", "claim": "post-UOC residual vector is defined", "gate_pass": "true", "reason": "RV3383 components isolate live K_MTS_IR/source-transfer terms", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3383_2_zero_theorem", "claim": "all post-UOC PPN residuals vanish", "gate_pass": "false", "reason": "zero theorem clauses fail as current proof", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3383_3_bound_ready", "claim": "finite PPN bound runner is numeric-ready", "gate_pass": "false", "reason": "bound formulas exist but source-backed numeric inputs are missing", "claim_allowed": "false", "valid_for_claim": "false"},
        {"gate_id": "GATE3383_4_full_local_GR", "claim": "full local GR/PPN pass under UOC", "gate_pass": "false", "reason": "reduced residual vector still contains live components", "claim_allowed": "false", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3383_0_main",
            "decision": "After UOC, the local-GR blocker is no longer source coupling; it is the extra-MTSIR PPN residual vector.",
            "because": "Newton/source/EM stress are clean conditionally, but K_MTS_IR metric response, transfer tails and Bianchi/exchange terms remain live.",
            "next_action": "choose the highest-leverage live component: transfer tail zero theorem or C_metric/Gamma bound runner",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3383_1_not_grim",
            "decision": "This is progress, not a failure loop.",
            "because": "The problem has shrunk from 'coupling is vague' to five named post-UOC PPN components with explicit formulas/gates.",
            "next_action": "fill one component at a time rather than reopening all coupling arguments",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3383_2_best_next",
            "decision": "Best next target is Cmetric/Gamma reduced PPN budget or transfer-tail zero.",
            "because": "Those are the largest remaining blockers to saying the UOC branch really reaches local GR.",
            "next_action": "attempt Cmetric/Gamma zero/bound first because it touches the full PPN vector directly",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3384-Y5-R2FR-Cmetric-Gamma-post-UOC-PPN-zero-or-first-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3384_Cmetric_Gamma_post_UOC_PPN_zero_or_first_bound_row.py",
            "objective": "try to prove R_Gamma_const_or_proxy=0 and A_PPN C_metric epsilon_eff^2=0/bounded under UOC; if not, produce the first finite PPN bound row",
            "why_next": "3383 identifies Cmetric/Gamma as the direct full-PPN metric-response blocker after source coupling is cleaned",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3385-Y5-R2FR-transfer-tail-zero-or-finite-source-measure-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3385_transfer_tail_zero_or_finite_source_measure_bound.py",
            "objective": "try to close R_eq/I_commutator/B_zero/projector-stress/M_H_ref under UOC or build the finite transfer-tail bound runner",
            "why_next": "transfer-tail is the remaining same-source/same-object obstruction after UOC",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3383*")
        if hit.name.startswith(("3383-Y5", "P8_Y5_R2FR_3383", "P8_Y5_BRR545_3383", "Y5_R2FR_3383"))
    ] if FW.exists() else []
    component_ids = {row["component_id"] for row in rows_by_name["residual_vector"]}
    theorem_results = {row["result"] for row in rows_by_name["zero_theorem"]}
    bound_ids = {row["bound_id"] for row in rows_by_name["bound_rows"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3383_0_sources_exist_parse", "all cited 3383 source paths exist and parse", source_ok, ""),
        ("VAL3383_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3383_2_residual_vector", "residual vector covers common EH, Gamma, metric response, composite, nonEH, transfer, EM and Bianchi", {"RV3383_0_common_EH_mode", "RV3383_1_Gamma_floor", "RV3383_2_metric_response", "RV3383_3_composite", "RV3383_4_nonEH_tail", "RV3383_5_transfer_tail", "RV3383_6_hidden_EM", "RV3383_7_bianchi_exchange"}.issubset(component_ids), ""),
        ("VAL3383_3_zero_theorem_blocks_claim", "zero theorem includes conditional contract and current failures", "VALID_CONDITIONAL_CONTRACT_NOT_CURRENT_CLAIM" in theorem_results and "FAILS_AS_CURRENT_PROOF" in theorem_results and "REDUCED_RESIDUAL_VECTOR_NOT_LOCAL_GR_PASS" in theorem_results, ""),
        ("VAL3383_4_bound_rows", "bound rows cover Cmetric, Gamma, transfer, nonEH and Bianchi", {"BND3383_0_Cmetric", "BND3383_1_RGamma", "BND3383_2_transfer", "BND3383_3_nonEH", "BND3383_4_bianchi"}.issubset(bound_ids), ""),
        ("VAL3383_5_runner", "runner defines reduced vector, fails zero theorem, stages bound schema and blocks claim", {"PASS_REDUCED_VECTOR_DEFINED", "FAILS_CURRENT_PROOF", "PASS_NONCLAIM_BOUND_SCHEMA", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3383_6_gates", "gates pass reduced vector and block zero theorem, numeric bound and full local GR", gate_map.get("GATE3383_1_reduced_vector") == "true" and gate_map.get("GATE3383_2_zero_theorem") == "false" and gate_map.get("GATE3383_4_full_local_GR") == "false", ""),
        ("VAL3383_7_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3383_8_next_target", "next target moves to Cmetric/Gamma post-UOC PPN zero or bound", rows_by_name["next"][0]["target_id"].startswith("3384-Y5-R2FR-Cmetric-Gamma"), ""),
        ("VAL3383_9_write_scope_outside_formalization", "no 3383 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3383_10_overall", "3383 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3383 - Y5/R2FR UOC extra-MTSIR local PPN residual vector or zero theorem under AX1090",
        "",
        "## Summary",
        "- 3383 takes the post-UOC branch and isolates the remaining local PPN blocker as an explicit residual vector.",
        "- Main reduction: `R_PPN^UOC <= |R_Gamma_const_or_proxy| + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN + R_nonEH_tail + R_transfer_tail`.",
        "- What UOC already removed: source-prefactor ambiguity, hidden source-frame coupling, unlabelled direct source vertices, and per-source `G` closure.",
        "- What remains live: Gamma/local metric floor, normalized metric response, composite/background-gradient terms, non-EH local operator tails, source-transfer/topological/projector tails, and Bianchi/exchange-current safety.",
        "- Zero theorem attempt fails as current proof because transfer tails and metric-response/Gamma/composite terms remain unsigned or numeric-missing.",
        "- Best next strike: attack the Cmetric/Gamma post-UOC PPN term first, because that is the full-vector metric-response bottleneck.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Post-UOC PPN Reduction",
        md_table(rows_by_name["reduction"]),
        "## Extra-MTSIR PPN Residual Vector",
        md_table(rows_by_name["residual_vector"]),
        "## Zero Theorem Attempt",
        md_table(rows_by_name["zero_theorem"]),
        "## Bound Rows",
        md_table(rows_by_name["bound_rows"]),
        "## Component Status Matrix",
        md_table(rows_by_name["component_status"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "reduction": reduction_rows(),
        "residual_vector": residual_vector_rows(),
        "zero_theorem": zero_theorem_rows(),
        "bound_rows": bound_rows(),
        "component_status": component_status_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
