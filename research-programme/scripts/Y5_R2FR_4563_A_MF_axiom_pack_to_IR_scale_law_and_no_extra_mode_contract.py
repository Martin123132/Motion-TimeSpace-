from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4563"
CLAIM_ID = "L-405"
BRANCH_ID = "MTS_R2FR_Y5_A_MF_AXIOM_PACK_IR_SELECTOR_4563"
MARKER = "PPC4161_A_MF_AXIOM_PACK_TO_IR_SCALE_LAW_AND_NO_EXTRA_MODE_CONTRACT_4563"
PACKET_MARKER = "PPC4161_PACKET_A_MF_AXIOM_PACK_IR_SELECTOR_CONTRACT_4563"
DECISION = "A_MF_AXIOM_PACK_IR_NORMAL_FORM_CONTRACT_WRITTEN_PARENT_SCALE_GAP_UNSIGNED_RESIDUAL_TRIAGE_SELECTED"
NEXT_TARGET = "4564-Y5-R2FR-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"

FORMAL_PATH = FORMAL / "579-PPC4161-A-MF-axiom-pack-to-IR-scale-law-and-no-extra-mode-contract.md"
DOC_PATH = POST / "4563-Y5-R2FR-A-MF-axiom-pack-to-IR-scale-law-and-no-extra-mode-contract.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4561 = FORMAL / "577-PPC4161-parent-EH-IR-selector-scale-law-or-explicit-EFT-residual-envelope.md"
DOC_4562 = FORMAL / "578-PPC4161-A-MF-parent-origin-from-motion-time-space-or-effective-axiom-freeze.md"
POST_4184 = POST / "4184-Y5-R2FR-Palatini-IR-normal-form-selector-under-AMF-or-residual-EFT-bound.md"
POST_4185 = POST / "4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
CSV_4562_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4562_NEXT_TARGET.csv"
CSV_4184_AXIOMS = SOURCE_DIR / "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv"
CSV_4184_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4184_PALATINI_REDUCTION_THEOREM_CHAIN.csv"
CSV_4184_RESIDUALS = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"
CSV_4185_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4185_STATUS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4563_SOURCE_REGISTER.csv"
AXIOM_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_A_MF_AXIOM_PACK.csv"
IR_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_IR_SCALE_LAW_CONTRACT.csv"
NO_EXTRA_MODE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_NO_EXTRA_MODE_CONTRACT.csv"
NORMAL_FORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_NORMAL_FORM_AND_RESIDUAL_SELECTOR.csv"
TRIAGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_RESIDUAL_TRIAGE_MATRIX.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4563_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4563_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC4563_00_4562_formal",
            "4562 A_MF freeze and selected target",
            DOC_4562,
            "frozen as an explicit equivalence-principle-like axiom candidate",
        ),
        (
            "SRC4563_01_4562_next",
            "4562 next-target CSV",
            CSV_4562_NEXT,
            "4563-Y5-R2FR-A-MF-axiom-pack-to-IR-scale-law-and-no-extra-mode-contract.md",
        ),
        (
            "SRC4563_02_4561_selector_gap",
            "4561 EH/IR selector gap",
            DOC_4561,
            "A parent scale law must rank two-derivative EC/Palatini terms",
        ),
        (
            "SRC4563_03_4184_doc",
            "4184 conditional Palatini selector",
            POST_4184,
            "A_MF + local covariant 4-form + two-derivative IR order + no extra light modes",
        ),
        (
            "SRC4563_04_4185_doc",
            "4185 residual coefficient map",
            POST_4185,
            "c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, c_bdy.",
        ),
        (
            "SRC4563_05_4184_axioms",
            "4184 selector axiom CSV",
            CSV_4184_AXIOMS,
            "SEL4184_2_IR_order",
        ),
        (
            "SRC4563_06_4184_theorem",
            "4184 Palatini theorem chain CSV",
            CSV_4184_THEOREM,
            "TH4184_1_classification",
        ),
        (
            "SRC4563_07_4184_residuals",
            "4184 residual EFT ledger CSV",
            CSV_4184_RESIDUALS,
            "RB4184_1_cR2",
        ),
        (
            "SRC4563_08_4185_status",
            "4185 status CSV",
            CSV_4185_STATUS,
            "cD_deltaKappa_cGamma",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4563 A_MF axiom-pack to IR/no-extra-mode selector",
                "valid_for_claim": "False",
            }
        )
    return rows


def axiom_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "axiom_id": "AP4563_0_A_MF_explicit",
            "clause": "A_MF explicit axiom candidate",
            "content": "Local motion-frame changes X^A -> Lambda^A_B(x)X^B + a^A(x) are gauge redundancies; omega^AB, B^A and e^A=D_omega X^A+B^A are the covariant variables.",
            "use_in_4563": "adopted explicitly, not parent-derived",
            "claim_status": "private_conditional_only",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AP4563_1_locality",
            "clause": "local compact-collar action",
            "content": "The local branch is represented by a local covariant four-form built from e^A, omega^AB, matter, EM and routed boundary data.",
            "use_in_4563": "allows finite derivative classification",
            "claim_status": "selector_assumption",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AP4563_2_same_coframe",
            "clause": "same observed coframe",
            "content": "Matter, clocks, rods and Maxwell-Hodge/EM stress use the same e^A and g_obs=eta_AB e^A e^B; no shadow metric or species-dependent coframe is allowed.",
            "use_in_4563": "routes c_D into a single zero-or-bound gate",
            "claim_status": "private_clause_not_global_parent",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AP4563_3_boundary_routing",
            "clause": "boundary/current routing",
            "content": "Boundary, topological and edge terms are either exact/routed or retained as explicit c_bdy residuals.",
            "use_in_4563": "prevents hidden flux from masquerading as a bulk EH term",
            "claim_status": "private_clause_not_global_parent",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AP4563_4_source_calibration",
            "clause": "calibrated Hilbert source coupling",
            "content": "The Newton/GR limit uses one Hilbert source current and one kappa_eff/G_cal readout; delta_kappa remains live until parent-locked.",
            "use_in_4563": "keeps Newton's G calibrated rather than falsely derived",
            "claim_status": "residual_gate_open",
            "valid_for_claim": "False",
        },
        {
            "axiom_id": "AP4563_5_no_claim_firewall",
            "clause": "no public local-GR promotion",
            "content": "A_MF plus the private selector can support conditional local calculations but cannot be advertised as parent-derived MTS GR/Newton until scale/no-extra-mode/source gates close.",
            "use_in_4563": "discipline firewall",
            "claim_status": "public_claim_blocked",
            "valid_for_claim": "False",
        },
    ]


def ir_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "IR4563_0_derivative_order",
            "law": "two-derivative / one-curvature dominance",
            "mathematical_form": "S_bulk = ∫[a0 eps + a1 eps_ABCD e^A e^B R^CD] + O(D^4/M_*^2, T^2, nonlocal memory, boundary)",
            "derivation_status": "conditional_EFT_normal_form",
            "missing_parent_input": "parent scale M_* or ordering functional that suppresses all D^4/T^2/memory/disformal terms in local <=2PN branch",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IR4563_1_scale_gap",
            "law": "spectral gap for every non-EH carrier",
            "mathematical_form": "For each extra carrier u_X: H_X = Z_X(-Box + M_X^2) + ... with M_X L_test >> 1 or residue/projection zero.",
            "derivation_status": "derived_as_required_condition_not_satisfied",
            "missing_parent_input": "Z_X, M_X, residue R_X and arena projection K_X for torsion, R2, disformal, memory and boundary sectors",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IR4563_2_no_light_pole",
            "law": "no unscreened local finite-range pole",
            "mathematical_form": "alpha_X(lambda) ~ R_X exp(-r/lambda_X) must vanish by R_X=0, lambda_X << L_test, or pass an arena alpha(lambda)/PPN/clock bound.",
            "derivation_status": "contract_written",
            "missing_parent_input": "real bound rows or parent no-pole theorem for each channel",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IR4563_3_Palatini_selector",
            "law": "EC/Palatini principal block",
            "mathematical_form": "A_MF + locality + IR4563_0 + IR4563_1 + same coframe + routed boundary => S_EC/Palatini[e,omega] + Lambda + residual envelope.",
            "derivation_status": "conditional_selector_theorem_retained",
            "missing_parent_input": "IR4563_0 and IR4563_1 are not parent-derived",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IR4563_4_EH_reduction",
            "law": "spinless compact branch EC -> EH",
            "mathematical_form": "If torsion/nonmetricity equations are algebraic and zero/bounded, S_EC -> S_EH[g_obs;kappa_eff] + routed boundary.",
            "derivation_status": "conditional_reduction",
            "missing_parent_input": "torsion/nonmetricity residual zero-or-bound rows and source spin policy",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "IR4563_5_Newton_readout",
            "law": "Newtonian limit with calibrated source coupling",
            "mathematical_form": "nabla^2 Phi_N = 4 pi G_cal rho_H with G_cal = c^4 kappa_eff/(8 pi), while delta_kappa tracks any parent-source drift.",
            "derivation_status": "structural_limit_not_numeric_G_prediction",
            "missing_parent_input": "parent kappa/source normalization law if G is to be derived rather than calibrated",
            "valid_for_claim": "False",
        },
    ]


def no_extra_mode_rows() -> list[dict[str, Any]]:
    specs = [
        ("NEM4563_0_cD", "c_D", "shadow/disformal coframe or second metric", "WEP; clocks; EM propagation; Poynting/Hilbert stress", "same-coframe parent functor or source-backed WEP/clock/EM bound", "root_priority"),
        ("NEM4563_1_deltaKappa", "delta_kappa", "source-coupling drift / kappa normalization mode", "Newton G; orbital GM; local Gdot; clock comparison", "parent Hilbert-source normalization or calibrated-G envelope", "root_priority"),
        ("NEM4563_2_cGamma", "c_Gamma", "local memory/support/projector mode", "PPN; clocks; R10; local G variation", "local memory screening/silence theorem or profile coefficient bound", "root_priority"),
        ("NEM4563_3_cT", "c_T", "torsion-square / spin-torsion carrier", "spin coupling; preferred-frame PPN; contact/R10", "torsion algebraic zero/heavy theorem or spin/source bound", "second_wave"),
        ("NEM4563_4_cR2", "c_R2/M_R", "curvature-square massive scalar/tensor pole", "R10 alpha(lambda); orbital precession; cosmology", "parent scale gap M_R or full alpha(lambda)/orbital bound", "second_wave"),
        ("NEM4563_5_cbdy", "c_bdy", "unrouted boundary/edge charge", "Hamiltonian mass leakage; radiation; transition current; R10 edge", "exact/routed boundary primitive or finite flux bound", "second_wave"),
    ]
    rows: list[dict[str, Any]] = []
    for mode_id, coefficient, carrier, arena, close_condition, priority in specs:
        rows.append(
            {
                "mode_id": mode_id,
                "coefficient": coefficient,
                "carrier": carrier,
                "observable_arena": arena,
                "zero_or_bound_condition": close_condition,
                "current_status": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
                "priority": priority,
                "valid_for_claim": "False",
            }
        )
    return rows


def normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "selector_id": "NF4563_0_principal_block",
            "term": "EC/Palatini/EH principal block",
            "normal_form_role": "leading unsuppressed local gravity action",
            "kept_or_residual": "kept_conditionally",
            "condition": "A_MF + locality + IR scale law + no-extra-mode + same coframe + routed boundary",
            "claim_status": "conditional_private",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "NF4563_1_vacuum_term",
            "term": "Lambda/vacuum four-form",
            "normal_form_role": "allowed local covariant zero-derivative term",
            "kept_or_residual": "kept_conditionally",
            "condition": "cosmology/vacuum sector must separately fix or fit its value",
            "claim_status": "not_local_GR_obstruction",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "NF4563_2_holst_topological",
            "term": "Holst/Nieh-Yan/topological parity sector",
            "normal_form_role": "topological/spin-sensitive or boundary-routed term",
            "kept_or_residual": "boundary_or_residual",
            "condition": "silent in spinless local branch or bounded in spin/torsion sector",
            "claim_status": "residual_if_unsilent",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "NF4563_3_extra_invariants",
            "term": "T^2, R^2, disformal, memory, boundary, source-drift terms",
            "normal_form_role": "everything not selected by EH principal block",
            "kept_or_residual": "residual_envelope",
            "condition": "must be zero, heavy, projection-silent or empirically bounded",
            "claim_status": "open",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "NF4563_4_verdict",
            "term": "local GR/Newton route",
            "normal_form_role": "conditional path to GR/Newton mechanics",
            "kept_or_residual": "not_public_claim",
            "condition": "public route opens only after parent scale gap/no-extra-mode/source gates close",
            "claim_status": "blocked_but_sharpened",
            "valid_for_claim": "False",
        },
    ]


def triage_rows() -> list[dict[str, Any]]:
    return [
        {
            "triage_id": "RT4563_0_first",
            "target": "c_D",
            "why_first": "If the same coframe fails, WEP/clocks/EM stress fail before any elegant EH action matters.",
            "route": "derive same-coframe parent functor from A_MF action descent, or build WEP/clock/EM bound interface",
            "success_condition": "no shadow metric/species coframe or a finite c_D bound with source path and units",
            "valid_for_claim": "False",
        },
        {
            "triage_id": "RT4563_1_second",
            "target": "delta_kappa",
            "why_first": "Newtonian mechanics needs source coupling; GR does not derive numerical G, but MTS must at least not hide a drifting source multiplier.",
            "route": "derive Hilbert-source normalization/kappa lock, or keep G_cal calibrated with explicit delta_kappa envelope",
            "success_condition": "parent source-coupling lock or calibrated-G residual row",
            "valid_for_claim": "False",
        },
        {
            "triage_id": "RT4563_2_third",
            "target": "c_Gamma",
            "why_first": "Local memory leakage can mimic G variation, PPN drift or R10 residuals even if the metric block is clean.",
            "route": "derive local memory support/projector silence, or source profile coefficients",
            "success_condition": "screening/silence theorem or profile-bound interface",
            "valid_for_claim": "False",
        },
        {
            "triage_id": "RT4563_3_second_wave",
            "target": "c_T, c_R2/M_R, c_bdy",
            "why_first": "These are serious but better handled after same-coframe/source/memory ownership is not leaking underneath the whole local limit.",
            "route": "torsion algebraic zero, curvature mass gap/R10 curve, boundary no-flux/exactness",
            "success_condition": "zero/heavy/bound rows for each residual",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG4563_0_A_MF_pack",
            "requirement": "A_MF is explicit, not smuggled",
            "status": "PASS_AXIOM_EXPLICIT",
            "claim_effect": "conditional route may proceed",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4563_1_IR_normal_form",
            "requirement": "normal form selector written under A_MF/locality/IR/no-extra assumptions",
            "status": "PASS_CONDITIONAL",
            "claim_effect": "EC/Palatini/EH is selected only under unsigned scale/no-extra clauses",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4563_2_parent_scale_gap",
            "requirement": "parent derives two-derivative dominance and spectral gap",
            "status": "FAIL_UNSIGNED_PARENT_SCALE_GAP",
            "claim_effect": "public local-GR derivation remains blocked",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4563_3_no_extra_modes",
            "requirement": "every extra invariant is zero, heavy, projection-silent or bounded",
            "status": "FAIL_RESIDUALS_OPEN",
            "claim_effect": "residual triage route selected",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4563_4_next_target",
            "requirement": "next work attacks the first leakage roots rather than repeating A_MF origin",
            "status": "PASS_NEXT_SELECTED",
            "claim_effect": f"next target = {NEXT_TARGET}",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4563_0_main",
            "decision": DECISION,
            "what_was_derived": "Under explicit A_MF plus locality, derivative-order dominance, no-extra-mode, same-coframe and boundary routing, the local normal form is EC/Palatini/EH plus a named residual envelope.",
            "what_failed": "The parent scale gap and no-extra-mode theorem are not derived from the current corpus; all residual coefficients remain nonclaim.",
            "action_taken": "Do not reopen A_MF origin; select c_D, delta_kappa and c_Gamma as the first leakage-root triad.",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "The normal-form theorem is now as strong as it can be under explicit A_MF. The biggest hidden-leak risks are same-coframe failure, source-coupling drift and local memory leakage.",
            "success_condition": "Derive zero laws for c_D, delta_kappa and c_Gamma from common action descent/source normalization/support silence, or create bounded nonclaim interfaces for each.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "A_MF_explicit_axiom": "True",
            "IR_normal_form_contract_written": "True",
            "parent_scale_gap_derived": "False",
            "no_extra_modes_closed": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "timestamp_utc": utc_now(),
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    axiom_pack: list[dict[str, Any]],
    ir_contract: list[dict[str, Any]],
    no_extra: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    triage: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append({"validation_id": "VAL4563_0_sources", "check": "all source paths and needles validate", "status": "PASS" if source_ok else "FAIL", "details": f"{len(sources)} sources"})

    pack_text = "\n".join(str(value) for row in axiom_pack for value in row.values())
    pack_ok = all(token in pack_text for token in ["A_MF", "e^A=D_omega X^A+B^A", "same observed coframe", "delta_kappa", "public_claim_blocked"])
    pack_ok = pack_ok and all(row["valid_for_claim"] == "False" for row in axiom_pack)
    rows.append({"validation_id": "VAL4563_1_axiom_pack", "check": "explicit A_MF axiom pack is complete and nonclaim", "status": "PASS" if pack_ok else "FAIL", "details": f"{len(axiom_pack)} clauses"})

    ir_text = "\n".join(str(value) for row in ir_contract for value in row.values())
    ir_ok = all(token in ir_text for token in ["two-derivative", "spectral gap", "EC/Palatini", "S_EH", "G_cal"])
    rows.append({"validation_id": "VAL4563_2_ir_contract", "check": "IR contract includes derivative order, spectral gap, Palatini/EH and Newton readout", "status": "PASS" if ir_ok else "FAIL", "details": f"{len(ir_contract)} IR rows"})

    coefficients = {row["coefficient"] for row in no_extra}
    needed = {"c_D", "delta_kappa", "c_Gamma", "c_T", "c_R2/M_R", "c_bdy"}
    no_extra_ok = needed.issubset(coefficients) and all(row["valid_for_claim"] == "False" for row in no_extra)
    rows.append({"validation_id": "VAL4563_3_no_extra_modes", "check": "all residual coefficients have zero-or-bound mode rows", "status": "PASS" if no_extra_ok else "FAIL", "details": ",".join(sorted(coefficients))})

    normal_text = "\n".join(str(value) for row in normal_form for value in row.values())
    normal_ok = all(token in normal_text for token in ["EC/Palatini/EH", "residual_envelope", "blocked_but_sharpened"])
    rows.append({"validation_id": "VAL4563_4_normal_form", "check": "normal-form selector keeps EH conditionally and residuals open", "status": "PASS" if normal_ok else "FAIL", "details": f"{len(normal_form)} normal-form rows"})

    triage_text = "\n".join(str(value) for row in triage for value in row.values())
    triage_ok = all(token in triage_text for token in ["c_D", "delta_kappa", "c_Gamma"]) and NEXT_TARGET in next_target[0]["next_target"]
    rows.append({"validation_id": "VAL4563_5_triage", "check": "next triage selects c_D/delta_kappa/c_Gamma leakage roots", "status": "PASS" if triage_ok else "FAIL", "details": NEXT_TARGET})

    gates_text = "\n".join(str(value) for row in gates for value in row.values())
    gates_ok = "PASS_CONDITIONAL" in gates_text and "FAIL_UNSIGNED_PARENT_SCALE_GAP" in gates_text and "FAIL_RESIDUALS_OPEN" in gates_text
    gates_ok = gates_ok and all(row["valid_for_claim"] == "False" for row in gates)
    rows.append({"validation_id": "VAL4563_6_gates", "check": "promotion gates pass conditional normal form but block public claim", "status": "PASS" if gates_ok else "FAIL", "details": f"{len(gates)} gates"})

    decision_ok = decision and decision[0]["decision"] == DECISION and decision[0]["valid_for_claim"] == "False"
    status_ok = status and status[0]["parent_scale_gap_derived"] == "False" and status[0]["IR_normal_form_contract_written"] == "True"
    rows.append({"validation_id": "VAL4563_7_decision_status", "check": "decision/status retain nonclaim and select next work", "status": "PASS" if decision_ok and status_ok else "FAIL", "details": NEXT_TARGET})

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL4563_8_overall", "check": "overall 4563 checkpoint validation", "status": "PASS" if overall else "FAIL", "details": "A_MF axiom-pack IR selector contract complete" if overall else "one or more validations failed"})
    return rows


def write_doc(
    path: Path,
    title: str,
    sources: list[dict[str, Any]],
    axiom_pack: list[dict[str, Any]],
    ir_contract: list[dict[str, Any]],
    no_extra: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    triage: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# {title}

Branch: `{BRANCH_ID}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4563 stops reopening the `A_MF` origin question and uses the 4562 result honestly: `A_MF` is an explicit axiom candidate.

Under that explicit axiom pack, the clean local-GR route is:

```text
A_MF
+ local covariant four-form
+ two-derivative / one-curvature IR dominance
+ no unscreened extra light modes
+ same observed coframe for matter, EM, clocks and rods
+ routed boundary/current terms
=> EC/Palatini principal block + vacuum term + residual envelope
=> EH[g_obs] + boundary in the spinless torsion-silent compact branch
=> Newtonian Poisson readout with calibrated G_cal, not a derived numeric G.
```

The real progress is the scale/no-extra-mode gate is now an exact contract:

```text
For every non-EH carrier u_X:
H_X = Z_X(-Box + M_X^2) + ...
local-GR survival requires M_X L_test >> 1,
or residue/projection zero,
or a source-backed empirical bound.
```

The current corpus does not yet derive that parent scale gap, so public local-GR/Newton/R10 is still blocked. The next best attack is the leakage-root triad: `c_D`, `delta_kappa`, `c_Gamma`.

## Source Register

{markdown_table(sources)}

## A_MF Axiom Pack

{markdown_table(axiom_pack)}

## IR Scale-Law Contract

{markdown_table(ir_contract)}

## No-Extra-Mode Contract

{markdown_table(no_extra)}

## Normal Form And Residual Selector

{markdown_table(normal_form)}

## Residual Triage Matrix

{markdown_table(triage)}

## Promotion Gates

{markdown_table(gates)}

## Decision

{markdown_table(decision)}

## Next Target

{markdown_table(next_target)}

## Validation

{markdown_table(validation)}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4563 uses the explicit A_MF axiom pack to write the IR normal-form/no-extra-mode contract: EC/Palatini/EH is selected only conditionally, while parent scale gap and residual coefficients remain open.",
        "current_evidence": "Generated source register, A_MF axiom pack, IR scale-law contract, no-extra-mode contract, normal-form/residual selector, triage matrix, gates, status and validation CSVs.",
        "status": "conditional_IR_normal_form_contract_written_parent_scale_gap_unsigned_residual_triage_selected",
        "next_test": NEXT_TARGET,
        "key_risk": "Promoting the conditional EC/Palatini/EH selector before the parent scale gap/no-extra-mode/source-coupling gates close.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "This is a selector contract and triage map, not a local-GR claim.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    axiom_pack = axiom_pack_rows()
    ir_contract = ir_contract_rows()
    no_extra = no_extra_mode_rows()
    normal_form = normal_form_rows()
    triage = triage_rows()
    gates = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()
    status = status_rows()
    validation = validate(sources, axiom_pack, ir_contract, no_extra, normal_form, triage, gates, decision, next_target, status)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(AXIOM_PACK_CSV, axiom_pack)
    write_csv(IR_CONTRACT_CSV, ir_contract)
    write_csv(NO_EXTRA_MODE_CSV, no_extra)
    write_csv(NORMAL_FORM_CSV, normal_form)
    write_csv(TRIAGE_CSV, triage)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)
    write_csv(VALIDATION_PATH, validation)

    write_doc(FORMAL_PATH, "4563 - A_MF axiom pack to IR scale law and no-extra-mode contract", sources, axiom_pack, ir_contract, no_extra, normal_form, triage, gates, decision, next_target, validation)
    write_doc(DOC_PATH, "4563 - Y5 R2FR A_MF Axiom Pack To IR Scale Law And No Extra Mode Contract", sources, axiom_pack, ir_contract, no_extra, normal_form, triage, gates, decision, next_target, validation)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4563 A_MF Axiom Pack To IR Selector Contract

Marker: `{MARKER}`  
`A_MF` is now used explicitly as an axiom candidate, not as a hidden parent theorem. Under `A_MF + locality + two-derivative/one-curvature IR dominance + no-extra-light-modes + same-coframe matter/EM + routed boundary`, the local normal form is:

```text
EC/Palatini principal block + vacuum term + residual envelope
=> EH[g_obs] + boundary in the spinless torsion-silent compact branch.
```

The parent scale gap is still unsigned. The exact no-extra-mode rule is now: every non-EH carrier must be zero, heavy with `M_X L_test >> 1`, projection-silent, or empirically bounded. The first leakage-root triad is `c_D`, `delta_kappa`, and `c_Gamma`; next target is `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4563 Packet Integration - A_MF Axiom Pack IR Selector Contract

Marker: `{PACKET_MARKER}`  
The packet may use `A_MF` only as an explicit axiom candidate. The conditional IR selector is sharpened to EC/Palatini/EH plus residual envelope, but parent scale gap and no-extra-mode closure remain false. First leakage-root target: `c_D`, `delta_kappa`, `c_Gamma`; next checkpoint `{NEXT_TARGET}`.
""",
    )

    cache_dir = Path(__file__).resolve().parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {FORMAL_PATH}")
    print(f"Wrote {VALIDATION_PATH}")
    print(f"Decision: {DECISION}")


if __name__ == "__main__":
    main()
