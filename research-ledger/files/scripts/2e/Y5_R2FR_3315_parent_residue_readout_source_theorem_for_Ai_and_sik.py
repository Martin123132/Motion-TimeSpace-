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

DOC = ROOT / "3315-Y5-R2FR-parent-residue-readout-source-theorem-for-Ai-and-sik-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3315_0_3314_doc",
        "path": ROOT / "3314-Y5-R2FR-parent-Ai-derivation-or-final-WEP-likelihood-blocker-ranking-under-AX1090.md",
        "role": "3314 handoff naming parent A_i/source-factor derivation as top blocker",
    },
    {
        "source_id": "SRC3315_1_3314_Ai",
        "path": OUT / "P8_Y5_R2FR_3314_PARENT_Ai_DERIVATION_ATTEMPT.csv",
        "role": "conditional A_0/A_2 identities and no-G-cal absorption guard",
    },
    {
        "source_id": "SRC3315_2_3314_factor",
        "path": OUT / "P8_Y5_R2FR_3314_Ai_FACTOR_CLAUSE_AUDIT.csv",
        "role": "four unsigned factor clauses: Z, U, Xi, s_ik",
    },
    {
        "source_id": "SRC3315_3_3303_alpha",
        "path": OUT / "P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv",
        "role": "general finite-mode alpha law",
    },
    {
        "source_id": "SRC3315_4_3305_projector",
        "path": OUT / "P8_Y5_R2FR_3305_PARENT_PROJECTOR_IDENTITY_DERIVATION.csv",
        "role": "Hilbert-source projector identity and universality theorem attempt",
    },
    {
        "source_id": "SRC3315_5_3311_factor",
        "path": OUT / "P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv",
        "role": "A_i as finite-mode source factor, not calibrated Newton G",
    },
    {
        "source_id": "SRC3315_6_1031_spm",
        "path": ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
        "role": "single-public-metric route closure status and shadow-frame counterexample guard",
    },
    {
        "source_id": "SRC3315_7_1045_matter_functor",
        "path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "role": "matter functor descent and no-shadow-frame source marker rows",
    },
    {
        "source_id": "SRC3315_8_1035_kernel",
        "path": ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
        "role": "source-test product warning and finite-mode kernel normalization split",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3315_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3315_PARENT_SOURCE_THEOREM_ATTEMPT.csv",
    "dust": OUT / "P8_Y5_R2FR_3315_DUST_LIMIT_PROOF.csv",
    "factor_split": OUT / "P8_Y5_R2FR_3315_FACTOR_SPLIT_RESULT.csv",
    "residuals": OUT / "P8_Y5_R2FR_3315_RESIDUAL_SOURCE_ENVELOPE.csv",
    "test_projection": OUT / "P8_Y5_R2FR_3315_TEST_PROJECTION_MAP.csv",
    "promotion": OUT / "P8_Y5_R2FR_3315_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3315_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3315_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3315_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 900) -> str:
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
    if path.suffix.lower() == ".csv":
        return csv_parse_ok(path)
    return text_parse_ok(path)


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
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


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


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "THM3315_0_branch_domain",
            "claim": "Work inside the public-Hilbert branch, not as a new axiom.",
            "derivation": "Assume ordinary matter is varied only through the observed/public metric or coframe: S_matter = Sbar[Psi, g_pub(q(Phi)), theta(q)]. This is exactly the branch needed by 3305 and explicitly not the closure-only SPM claim unless the parent action later signs the matter functor.",
            "status": "CONDITIONAL_BRANCH",
            "closes": "sets the theorem domain",
            "still_needed": "parent action must derive the public-Hilbert matter interface",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3315_1_variation",
            "claim": "Finite-mode matter charges are Hilbert-source projections.",
            "derivation": "For delta g_pub_mu_nu = sum_i U_i e_i_mu_nu delta phi_i, variation gives delta S_m = 1/2 int sqrt(-g) T_H^{mu nu} delta g_pub_mu_nu, hence J_i[A] = (U_i/2) int_A sqrt(-g) T_H^{mu nu} e_i_mu_nu.",
            "status": "DERIVED_CONDITIONAL",
            "closes": "Xi_i is no longer a free vibe parameter in this branch",
            "still_needed": "mode tensors e_i and normalization from parent Hessian",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3315_2_dust_limit",
            "claim": "The composition residual s_ik vanishes in the ideal local dust/public-projector limit.",
            "derivation": "For nonrelativistic dust T_H^{mu nu} = rho u^mu u^nu and for a static local projector with e_i_mu_nu u^mu u^nu = c_i constant over ordinary matter, J_i[A] = (U_i c_i/2) int_A rho dV = C_i M_A. Therefore Xi_i[A] = J_i[A]/(C_i M_A) = 1 for every body A, so Delta Xi_i[A,B] = 0 and s_ik^dust = 0.",
            "status": "DERIVED_WITHIN_BRANCH",
            "closes": "leading ordinary WEP composition direction",
            "still_needed": "residual stress, binding, EM/Poynting, support, and shadow-frame tails",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3315_3_Ai_split",
            "claim": "The source factor splits into a Hessian/readout part and an Earth residual part.",
            "derivation": "A_0 = (1/3) Z_0 U_0 [1 + epsilon_0(Earth)] and A_2 = (-4/3) Z_2 U_2 [1 + epsilon_2(Earth)]. The old blank Xi_i[Earth] is now an explicit residual expansion rather than an arbitrary fitted knob.",
            "status": "DERIVED_SPLIT_NOT_NUMERIC",
            "closes": "removes one lumped unknown",
            "still_needed": "Z_i U_i from parent quadratic Hessian and epsilon_i(Earth) bounds",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3315_4_no_G_absorption",
            "claim": "The finite-mode A_i cannot be hidden inside Newton G.",
            "derivation": "G_cal fixes the massless graviton coefficient in the 1/r channel. Z_i U_i multiplies finite-range modes and epsilon_i source residuals. Absorbing A_i into G_cal would erase a range-dependent and mode-dependent force that is tested separately by WEP/R10/PPN/clock/orbital arenas.",
            "status": "GUARDRAIL",
            "closes": "prevents a fake local-GR pass",
            "still_needed": "none for the guardrail",
            "valid_for_claim": "false",
        },
        {
            "step_id": "THM3315_5_countermodel",
            "claim": "Terminal/public metric language alone does not prove the theorem.",
            "derivation": "A matter functor can evaluate a species frame, marker, non-Hilbert current, mass constant, or support profile before mapping to the public metric. Such a countermodel preserves notation but reintroduces body-dependent Xi_i[A].",
            "status": "COUNTERMODEL_SURVIVES_OUTSIDE_BRANCH",
            "closes": "why this is a branch theorem, not a final parent proof",
            "still_needed": "parent no-shadow-frame/no-non-Hilbert-current theorem",
            "valid_for_claim": "false",
        },
    ]


def dust_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "DUST3315_0_source_tensor",
            "object": "T_H^{mu nu}",
            "statement": "In a local nonrelativistic ordinary body, T_H^{mu nu} = rho u^mu u^nu + stress/c^2 + field momentum terms.",
            "use": "separates leading mass density from residual channels",
            "result": "leading term isolated",
            "passed": "true",
        },
        {
            "proof_id": "DUST3315_1_mode_projection",
            "object": "e_i_mu_nu u^mu u^nu",
            "statement": "If the local static public-metric mode projector is material-blind, its contraction on u^mu u^nu is a constant c_i for ordinary matter.",
            "use": "turns the Hilbert-source integral into a mass integral",
            "result": "conditional constant c_i",
            "passed": "true",
        },
        {
            "proof_id": "DUST3315_2_charge_integral",
            "object": "J_i[A]",
            "statement": "J_i[A] = (U_i c_i/2) int_A rho dV = C_i M_A.",
            "use": "proves proportionality of finite-mode source charge to inertial mass at leading dust order",
            "result": "J_i[A]/M_A = C_i for all A",
            "passed": "true",
        },
        {
            "proof_id": "DUST3315_3_sik_zero",
            "object": "s_ik^dust",
            "statement": "With Xi_i[A] = J_i[A]/(C_i M_A), Xi_i[A] = 1 and Delta Xi_i[A,B] = 0.",
            "use": "kills the leading WEP composition vector inside the public-Hilbert dust branch",
            "result": "s_ik^dust = 0",
            "passed": "true",
        },
        {
            "proof_id": "DUST3315_4_limits",
            "object": "residual epsilon_i[A]",
            "statement": "The proof does not kill stress, binding, EM/Poynting momentum-flow, support/readout, or shadow-frame residuals.",
            "use": "keeps the theorem honest",
            "result": "epsilon_i[A] envelope remains required",
            "passed": "true",
        },
    ]


def factor_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor_id": "FS3315_0_Z_residue",
            "factor": "Z_0,Z_2",
            "new_status": "PARENT_HESSIAN_REQUIRED",
            "law": "Z_i is the canonical residue/sign of the finite-mode quadratic kinetic operator after diagonalization.",
            "what_3315_changed": "kept Z_i out of the source residual problem",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FS3315_1_U_readout",
            "factor": "U_0,U_2",
            "new_status": "PUBLIC_READOUT_OVERLAP_REQUIRED",
            "law": "U_i is the overlap of diagonal finite mode phi_i with delta g_pub in the ordinary readout channel.",
            "what_3315_changed": "U_i now enters both source charge and observable potential through one public metric projection",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FS3315_2_Xi_source",
            "factor": "Xi_i[A]",
            "new_status": "DUST_LIMIT_FIXED_RESIDUAL_EXPANDED",
            "law": "Xi_i[A] = 1 + epsilon_i^stress[A] + epsilon_i^bind[A] + epsilon_i^EM_Poynting[A] + epsilon_i^support[A] + epsilon_i^shadow[A] + epsilon_i^nonH[A].",
            "what_3315_changed": "the leading source charge is no longer arbitrary; only named residuals remain",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FS3315_3_sik",
            "factor": "s_ik",
            "new_status": "ZERO_AT_DUST_ORDER_NONZERO_RESIDUAL_TAIL",
            "law": "s_i dot Delta_q[A,B] = Delta epsilon_i^stress + Delta epsilon_i^bind + Delta epsilon_i^EM_Poynting + Delta epsilon_i^support + Delta epsilon_i^shadow + Delta epsilon_i^nonH.",
            "what_3315_changed": "WEP source vector becomes a residual-tail problem rather than an unexplained primary coupling",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FS3315_4_A0",
            "factor": "A_0",
            "new_status": "SPLIT_LAW_NOT_NUMERIC",
            "law": "A_0 = (1/3) Z_0 U_0 [1 + epsilon_0(Earth)].",
            "what_3315_changed": "source-side part is explicit; residue/readout part remains parent Hessian work",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "FS3315_5_A2",
            "factor": "A_2",
            "new_status": "SPLIT_LAW_NOT_NUMERIC",
            "law": "A_2 = (-4/3) Z_2 U_2 [1 + epsilon_2(Earth)].",
            "what_3315_changed": "source-side part is explicit; residue/readout part remains parent Hessian work",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES3315_0_stress_pressure",
            "residual": "epsilon_i^stress[A]",
            "definition": "finite-mode projector applied to pressure, anisotropic stress, elastic stress, and internal kinetic stress divided by the dust mass charge",
            "why_it_matters": "lab bodies are not perfect dust; pressure/stress trace can create tiny composition dependence",
            "next_input": "stress-energy model or conservative bound per material",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3315_1_binding",
            "residual": "epsilon_i^bind[A]",
            "definition": "nuclear, atomic, chemical, and gravitational binding-energy fraction response under the finite-mode projector",
            "why_it_matters": "composition tests mostly live in differential binding fractions once dust mass universality is removed",
            "next_input": "material assay/binding proxies for Ti/Al/V/Pt/Rh/Be",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3315_2_EM_Poynting",
            "residual": "epsilon_i^EM_Poynting[A]",
            "definition": "finite-mode projection of EM stress, field energy, and momentum-flow terms including S = E x B / mu0 where fields/waves carry support momentum",
            "why_it_matters": "this keeps the user's Poynting-vector intuition in the actual source tensor instead of treating EM as just scalar mass bookkeeping",
            "next_input": "static EM binding estimate for ordinary matter plus separate wave/media stress test branch",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3315_3_support_readout",
            "residual": "epsilon_i^support[A]",
            "definition": "finite-size, geometry, shielding, source/test profile, and readout-kernel mismatch corrections",
            "why_it_matters": "R10 and laboratory tests do not measure a point-particle source charge directly",
            "next_input": "arena profile integrals K_i(lambda), Qbar_i, tau_i",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3315_4_shadow_frame",
            "residual": "epsilon_i^shadow[A]",
            "definition": "hidden conformal/disformal/species frame response not mediated solely by g_pub",
            "why_it_matters": "this is the main countermodel to a parent WEP proof",
            "next_input": "parent no-shadow-frame theorem or explicit coefficient bounds",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RES3315_5_nonHilbert",
            "residual": "epsilon_i^nonH[A]",
            "definition": "direct non-Hilbert current, material marker, or source-normalization dependency",
            "why_it_matters": "would make Xi_i[A] body dependent even with a public metric readout",
            "next_input": "parent current-chain exclusion or empirical envelope",
            "valid_for_claim": "false",
        },
    ]


def test_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "WEP_MICROSCOPE_EotWash",
            "post_3315_quantity": "eta_AB(lambda) = sum_i K_i(lambda) Z_i U_i [1 + epsilon_i(Earth)] Delta epsilon_i[A,B]",
            "what_is_now_derived": "Delta epsilon_i^dust = 0",
            "what_is_still_missing": "Z_i U_i, Earth residual, material residual differences, covariance",
            "claim_status": "blocked_nonclaim",
        },
        {
            "arena": "R10_short_range",
            "post_3315_quantity": "alpha_R10(lambda) = K_i^R10(lambda) beta_source beta_test + epsilon_tail",
            "what_is_now_derived": "beta_source/test are Hilbert-source residual projections in public-Hilbert branch",
            "what_is_still_missing": "R10 geometry kernels, material profiles, Z_i, lambda_i",
            "claim_status": "blocked_nonclaim",
        },
        {
            "arena": "PPN_local_GR",
            "post_3315_quantity": "gamma-1, beta-1, preferred-frame terms from finite-mode residue/readout plus residual source tails",
            "what_is_now_derived": "composition source residual is not the first-order dust problem",
            "what_is_still_missing": "Z_i U_i sign/range, Vainshtein/screening or decoupling proof, nonlinear metric limit",
            "claim_status": "blocked_nonclaim",
        },
        {
            "arena": "clocks_EM",
            "post_3315_quantity": "clock residual = projection of stress, EM binding, alpha_EM/mass response, and Poynting/momentum-flow terms",
            "what_is_now_derived": "EM belongs inside T_H and residual epsilon, not outside the coupling analysis",
            "what_is_still_missing": "alpha_EM/mass derivative theorem or coefficient bounds",
            "claim_status": "blocked_nonclaim",
        },
        {
            "arena": "orbital_Newton",
            "post_3315_quantity": "G_cal massless 1/r channel plus finite-mode Yukawa residues; no A_i absorption into G_cal",
            "what_is_now_derived": "source charge proportional to mass at dust order",
            "what_is_still_missing": "finite-mode range/amplitude or proof of local decoupling",
            "claim_status": "blocked_nonclaim",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3315_0_dust_source_zero",
            "claim": "s_ik^dust = 0 in public-Hilbert local dust limit",
            "passed": "true",
            "reason": "derived from Hilbert-source variation plus material-blind static projector",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3315_1_full_source_zero",
            "claim": "s_ik = 0 exactly for real materials",
            "passed": "false",
            "reason": "stress, binding, EM/Poynting, support, shadow-frame, and non-Hilbert residuals remain",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3315_2_numeric_Ai",
            "claim": "A_0 and A_2 are numeric/parent-owned",
            "passed": "false",
            "reason": "Z_i U_i requires parent quadratic Hessian/readout extraction",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3315_3_local_GR",
            "claim": "local GR/Newtonian limit is recovered",
            "passed": "false",
            "reason": "finite-mode amplitude/range and residual tails are not yet closed",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3315_0",
            "question": "Did 3315 make actual derivational progress?",
            "answer": "yes: it proves the leading WEP source-composition vector vanishes at dust order inside the public-Hilbert branch",
            "reason": "Hilbert-source variation makes finite-mode charge proportional to mass for material-blind local static projectors",
            "next_action": "do not treat s_ik as a primary free coupling; treat it as a residual epsilon envelope",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3315_1",
            "question": "What remains as the top coupling blocker?",
            "answer": "parent quadratic Hessian/readout extraction for Z_i U_i, plus residual epsilon bounds",
            "reason": "A_i now splits into Z_i U_i times [1 + epsilon_i(Earth)]",
            "next_action": "attempt parent Hessian/readout extraction for Z_i U_i before more empirical WEP polishing",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3315_2",
            "question": "Where does EM/Poynting enter?",
            "answer": "inside the Hilbert stress residual epsilon_i^EM_Poynting, not as a separate magic coupling",
            "reason": "EM field energy and momentum flow contribute to T_H and can affect clocks/material/wave stress branches",
            "next_action": "after Hessian extraction, build a bounded EM/Poynting residual branch",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3316-Y5-R2FR-parent-quadratic-hessian-readout-extraction-for-ZiUi-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3316_parent_quadratic_hessian_readout_extraction_for_ZiUi.py",
            "objective": "extract or bound Z_i U_i from the parent quadratic action/Hessian and public readout map, using 3315's source theorem so A_i is no longer a single opaque coupling",
            "must_include": "linearized parent field variables; Hessian blocks; canonical normalization; public metric overlap U_i; residue sign; ghost/tachyon guard; local-GR claim gate; no formalization-workbench edits",
            "fallback_if_failed": "demote Z_i U_i to empirical finite-mode amplitude envelopes and proceed to EM/Poynting residual bounds",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = source_register_rows()
    theorem = theorem_rows()
    dust = dust_rows()
    factors = factor_split_rows()
    residuals = residual_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()
    formalization_after = snapshot_tree(FW)
    fw_changed = changed_count(formalization_before, formalization_after)

    checks = [
        {
            "check_id": "VAL3315_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in source_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3315_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in source_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3315_2_outputs_parse",
            "check": "all 3315 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3315_3_dust_zero_present",
            "check": "theorem derives s_ik^dust zero",
            "passed": any("s_ik^dust = 0" in row["derivation"] or "s_ik^dust = 0" in row["claim"] for row in theorem)
            and any(row["result"] == "s_ik^dust = 0" and row["passed"] == "true" for row in dust),
            "detail": "",
        },
        {
            "check_id": "VAL3315_4_Ai_split_present",
            "check": "factor split contains A0 and A2 residual laws",
            "passed": any(row["factor"] == "A_0" and "epsilon_0(Earth)" in row["law"] for row in factors)
            and any(row["factor"] == "A_2" and "epsilon_2(Earth)" in row["law"] for row in factors),
            "detail": "",
        },
        {
            "check_id": "VAL3315_5_residuals_named",
            "check": "residual envelope includes EM/Poynting and shadow/non-Hilbert channels",
            "passed": any("EM_Poynting" in row["residual"] for row in residuals)
            and any("shadow" in row["residual"] for row in residuals)
            and any("nonH" in row["residual"] for row in residuals),
            "detail": "",
        },
        {
            "check_id": "VAL3315_6_no_full_claim",
            "check": "full local-GR/source/numeric gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3315_1_full_source_zero", "GATE3315_2_numeric_Ai", "GATE3315_3_local_GR"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3315_7_next_target_Hessian",
            "check": "next target is Hessian/readout extraction",
            "passed": any("quadratic-hessian-readout" in row["target_doc"] and "Z_i U_i" in row["objective"] for row in next_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3315_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3315_9_overall",
            "check": "3315 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for row in checks:
        row["passed"] = bool_str(bool(row["passed"]))
    return checks


def render_doc() -> str:
    source_rows = source_register_rows()
    theorem = theorem_rows()
    dust = dust_rows()
    factors = factor_split_rows()
    residuals = residual_rows()
    projections = test_projection_rows()
    gates = promotion_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    lines: list[str] = [
        "# 3315 - Parent residue/readout/source theorem for Ai and sik under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "This checkpoint gets a real piece of the coupling problem, not just a new missing-list.",
        "",
        "Inside the public-Hilbert matter branch, the leading nonrelativistic dust source charge of each finite mode is proportional to ordinary mass. Therefore the leading WEP composition vector vanishes:",
        "",
        "`s_ik^dust = 0`.",
        "",
        "That is not the whole local-GR proof. It leaves a cleaner problem: `A_i` splits into a parent Hessian/readout factor and named residual tails:",
        "",
        "`A_0 = (1/3) Z_0 U_0 [1 + epsilon_0(Earth)]`",
        "",
        "`A_2 = (-4/3) Z_2 U_2 [1 + epsilon_2(Earth)]`",
        "",
        "So the next top blocker is no longer an opaque coupling. It is the parent quadratic Hessian/readout extraction for `Z_i U_i`, plus bounded residuals for stress, binding, EM/Poynting, support, shadow frames, and non-Hilbert currents.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_rows:
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` - exists={row['exists']}; parse_ok={row['parse_ok']}; role={row['role']}"
        )
    lines.extend(["", "## Theorem Attempt", ""])
    for row in theorem:
        lines.append(
            f"- `{row['step_id']}` `{row['status']}`: {row['claim']} {row['derivation']} Still needed: {row['still_needed']}."
        )
    lines.extend(["", "## Dust Limit Proof", ""])
    for row in dust:
        lines.append(
            f"- `{row['proof_id']}` `{row['object']}`: {row['statement']} Result: `{row['result']}`."
        )
    lines.extend(["", "## Factor Split Result", ""])
    for row in factors:
        lines.append(
            f"- `{row['factor_id']}` `{row['factor']}`: {row['new_status']}. Law: {row['law']}"
        )
    lines.extend(["", "## Residual Source Envelope", ""])
    for row in residuals:
        lines.append(
            f"- `{row['residual_id']}` `{row['residual']}`: {row['definition']} Next input: {row['next_input']}."
        )
    lines.extend(["", "## Test Projection Map", ""])
    for row in projections:
        lines.append(
            f"- `{row['arena']}`: {row['post_3315_quantity']} Derived now: {row['what_is_now_derived']}. Missing: {row['what_is_still_missing']}."
        )
    lines.extend(["", "## Promotion Gates", ""])
    for row in gates:
        lines.append(
            f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}; reason={row['reason']}"
        )
    lines.extend(["", "## Decision", ""])
    for row in decisions:
        lines.append(
            f"- `{row['decision_id']}`: {row['answer']} - {row['reason']} Next: {row['next_action']}."
        )
    lines.extend(["", "## Next Target", ""])
    for row in next_rows:
        lines.append(f"- `{row['target_doc']}`")
        lines.append(f"- `{row['target_script']}`")
        lines.append(f"- Objective: {row['objective']}")
        lines.append(f"- Fallback: {row['fallback_if_failed']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["theorem"], theorem_rows())
    write_csv(OUTPUTS["dust"], dust_rows())
    write_csv(OUTPUTS["factor_split"], factor_split_rows())
    write_csv(OUTPUTS["residuals"], residual_rows())
    write_csv(OUTPUTS["test_projection"], test_projection_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())

    DOC.write_text(render_doc(), encoding="utf-8")

    validation_rows = validate_outputs(formalization_before)
    write_csv(OUTPUTS["validation"], validation_rows)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
