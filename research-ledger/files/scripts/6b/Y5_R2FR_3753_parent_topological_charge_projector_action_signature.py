from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3753"
BRANCH = "MTS_R2FR_Y5_PARENT_TOPOLOGICAL_CHARGE_PROJECTOR_ACTION_SIGNATURE_3753"
PCW = Path(__file__).resolve().parents[1]
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3753-Y5-R2FR-parent-topological-charge-projector-action-signature.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3753_0_3752_next": RESIDUALS / "P8_Y5_R2FR_3752_NEXT_TARGET.csv",
        "SRC3753_1_3752_theorems": RESIDUALS / "P8_Y5_R2FR_3752_ORTHOGONAL_TOPOLOGICAL_THEOREM_ROWS.csv",
        "SRC3753_2_3752_branches": RESIDUALS / "P8_Y5_R2FR_3752_PROJECTOR_BRANCH_MATRIX.csv",
        "SRC3753_3_parent_projector_contract": RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "SRC3753_4_variation_stress_contract": RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "SRC3753_5_qcoh_theorem": RESIDUALS / "P8_QCOH_PROJECTOR_ALGEBRA_THEOREM.csv",
        "SRC3753_6_topological_naturality": RESIDUALS / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        "SRC3753_7_gamma_naturality": RESIDUALS / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
        "SRC3753_8_3752_fallback_bounds": RESIDUALS / "P8_Y5_R2FR_3752_METRIC_STRESS_FALLBACK_BOUNDS.csv",
        "SRC3753_9_3750_cap": RESIDUALS / "P8_Y5_R2FR_3750_HIDDEN_OPERATOR_NORM_CAPS.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    purpose = {
        "SRC3753_0_3752_next": "imports exact 3753 objective",
        "SRC3753_1_3752_theorems": "imports contraction and metric-silence theorem conditions",
        "SRC3753_2_3752_branches": "imports topological/orthogonal versus Hodge branches",
        "SRC3753_3_parent_projector_contract": "imports PM0-PM8 parent projector contract",
        "SRC3753_4_variation_stress_contract": "imports PV0-PV8 projector stress contract",
        "SRC3753_5_qcoh_theorem": "imports algebraic projector precedent and parent-action warning",
        "SRC3753_6_topological_naturality": "imports Pi_top naturality route",
        "SRC3753_7_gamma_naturality": "imports independent-Gamma silence already obtained",
        "SRC3753_8_3752_fallback_bounds": "imports spectral-gap fallback",
        "SRC3753_9_3750_cap": "imports current H_op cap",
    }
    return [
        {
            **base(ts),
            "source_id": key,
            "source_path": str(path),
            "purpose": purpose[key],
            "exists": path.exists(),
            "claim_allowed": False,
        }
        for key, path in source_paths().items()
    ]


def cap_value() -> float:
    for row in read_csv(source_paths()["SRC3753_9_3750_cap"]):
        if row.get("cap_id") == "CAP3750_GLOBAL_MIN":
            return float(row["H_op_max_to_pass_placeholder_tol"])
    raise RuntimeError("CAP3750_GLOBAL_MIN missing")


def action_signature_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "AS3753_0_parent_data",
            "parent configuration includes (X_D, [Sigma_M], V_J, ell_M, Omega_M, B_top)",
            "X_D is the compact local exterior; [Sigma_M] is a fixed relative homology class; V_J is the source-current space; ell_M:V_J->R is the mass/charge functional; Omega_M in V_J is the normalized representative; B_top is a parent bilinear on the charge block",
            "defines projector before any PPN/orbital readout",
            "ACTION_SIGNATURE_REQUIRED",
        ),
        (
            "AS3753_1_topological_charge",
            "ell_M(J) := <[Sigma_M], J>",
            "ell_M is a de Rham/current pairing with a parent-owned homology class, not a fitted surface integral chosen after the solution",
            "metric-independent charge functional if [Sigma_M] is fixed by parent topology",
            "CANDIDATE_CONSTRUCTED",
        ),
        (
            "AS3753_2_normalized_representative",
            "d Omega_M=0 and ell_M(Omega_M)=1",
            "Omega_M is a closed charge representative normalized against ell_M; no Hodge star or local metric appears in this normalization",
            "makes Pi_M idempotent",
            "CANDIDATE_CONSTRUCTED",
        ),
        (
            "AS3753_3_projector_definition",
            "Pi_M J := Omega_M ell_M(J)",
            "rank-one topological projector on the mass/source charge channel",
            "Pi_M^2=Pi_M follows immediately from ell_M(Omega_M)=1",
            "EXACT_ALGEBRA",
        ),
        (
            "AS3753_4_dual_normalization",
            "B_top(Omega_M,Omega_M)=1 and ||ell_M||_{B_top,*}=1",
            "if B_top splits V_J=span(Omega_M) direct-sum ker ell_M orthogonally, Pi_M is the B_top-orthogonal projector",
            "imports 3752 contraction so ||Pi_M||<=1",
            "CONTRACTION_SIGNATURE",
        ),
        (
            "AS3753_5_parent_action_terms",
            "S_parent contains S_dyn + S_top[lambda_d dOmega_M + lambda_n(ell_M(Omega_M)-1) + lambda_B(B_top(Omega_M,Omega_M)-1)] + S_source[J_H,Pi_M]",
            "the multiplier sector enforces closure, normalization, and dual normalization before variation",
            "candidate parent-action extension; not yet public claim",
            "ACTION_SIGNATURE_WRITTEN",
        ),
        (
            "AS3753_6_no_metric_slots",
            "delta_g ell_M=0, delta_g Omega_M=0, delta_g B_top=0 in the topological block",
            "metric silence requires no g, e_obs, Hodge star, DeWitt metric, Gamma_ind transport, fitted mask, or collar selector in the definition of Pi_M",
            "gives delta_g Pi_M=0 for the projector itself",
            "METRIC_SILENCE_CONTRACT",
        ),
        (
            "AS3753_7_product_rule_owned",
            "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H",
            "the parent variation keeps the full product rule; only the second term is zero in the topological block",
            "ordinary source stress remains in delta J_H; no hidden deletion",
            "BIANCHI_GUARD",
        ),
        (
            "AS3753_8_readout_firewall",
            "P_read, empirical masks, orbital fitted GM, and active-domain choices enter only after delta S_parent",
            "prevents the topological projector from becoming a post-fit readout trick",
            "keeps PM/PV fallback rows active if violated",
            "FIREWALL",
        ),
    ]
    return [
        {
            **base(ts),
            "signature_id": signature_id,
            "action_clause": action_clause,
            "mathematical_content": mathematical_content,
            "what_it_closes": closes,
            "status": status,
            "claim_allowed": False,
        }
        for signature_id, action_clause, mathematical_content, closes, status in rows
    ]


def theorem_check_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "TC3753_0_idempotence",
            "Pi_M^2 J = Omega_M ell_M(Omega_M ell_M(J)) = Omega_M ell_M(Omega_M) ell_M(J) = Pi_M J",
            "requires ell_M(Omega_M)=1",
            "PASS_UNDER_SIGNATURE",
        ),
        (
            "TC3753_1_charge_preservation",
            "ell_M(Pi_M J)=ell_M(Omega_M)ell_M(J)=ell_M(J)",
            "requires ell_M(Omega_M)=1",
            "PASS_UNDER_SIGNATURE",
        ),
        (
            "TC3753_2_kernel_erasure",
            "if J in ker ell_M then Pi_M J=0",
            "follows from rank-one definition",
            "PASS_UNDER_SIGNATURE",
        ),
        (
            "TC3753_3_orthogonality",
            "V_J=span(Omega_M) orthogonal_B_top ker ell_M",
            "requires parent bilinear B_top, not a metric Hodge afterthought",
            "CONDITIONAL_PARENT_NORM",
        ),
        (
            "TC3753_4_contraction",
            "with TC3753_3 and B_top(Omega_M,Omega_M)=1, ||Pi_M||_{B_top->B_top}<=1",
            "imports 3752 contraction theorem",
            "PASS_IF_PARENT_NORM_SIGNED",
        ),
        (
            "TC3753_5_metric_silence",
            "delta_g Pi_M J = (delta_g Omega_M)ell_M(J)+Omega_M(delta_g ell_M)(J)=0",
            "requires metric-independent Omega_M and ell_M",
            "PASS_IF_TOPOLOGY_SIGNED",
        ),
        (
            "TC3753_6_gamma_silence",
            "delta_Gamma_ind Pi_M=0",
            "follows because Pi_M has no Gamma_ind argument slot",
            "PASS_INSIDE_TOPOLOGICAL_BRANCH",
        ),
        (
            "TC3753_7_flux_not_proved",
            "d(Pi_M J_H)=dOmega_M ell_M(J_H)+Omega_M d ell_M(J_H) is not automatically zero for evolving source charge",
            "needs Ward/Euler conservation of ell_M(J_H)",
            "OPEN_SOURCE_WARD_GAP",
        ),
        (
            "TC3753_8_newton_calibration_not_proved",
            "M_eff proportional ell_M(J_H) is conserved/topological, but not yet calibrated to universal GM or Poisson normalization",
            "needs EH/Poisson/asymptotic matching",
            "OPEN_G_CALIBRATION_GAP",
        ),
    ]
    return [
        {
            **base(ts),
            "check_id": check_id,
            "derivation_or_statement": statement,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for check_id, statement, requirement, status in rows
    ]


def variation_silence_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "VS3753_0_projector_metric",
            "delta_g Pi_M",
            "0 in AS3753 topological block",
            "PROJECTOR_STRESS_ZERO_CONDITIONAL",
            "does not erase ordinary stress from J_H",
        ),
        (
            "VS3753_1_projector_gamma",
            "delta_Gamma_ind Pi_M",
            "0 because no Gamma_ind slot",
            "GAMMA_PROJECTOR_ZERO",
            "consistent with 3572",
        ),
        (
            "VS3753_2_hodge_forbidden",
            "delta_g Pi_Hodge(g)",
            "nonzero unless separately cancelled/bounded",
            "FORBIDDEN_FOR_CLEAN_ROUTE",
            "activates spectral fallback",
        ),
        (
            "VS3753_3_domain",
            "delta_g [Sigma_M] or delta_g chi_D",
            "0 only if parent topology fixes class before metric variation",
            "UNSIGNED_DOMAIN_TOPOLOGY",
            "domain/homology proof still required",
        ),
        (
            "VS3753_4_boundary",
            "boundary/collar flux",
            "not closed by projector algebra alone",
            "OPEN_NO_FLUX_GAP",
            "needs Ward/no-flux theorem",
        ),
        (
            "VS3753_5_readout_masks",
            "delta_g P_read",
            "not allowed in S_parent",
            "REJECT_IF_USED",
            "readout firewall",
        ),
    ]
    return [
        {
            **base(ts),
            "silence_id": silence_id,
            "variation": variation,
            "result": result,
            "status": status,
            "scope_guard": guard,
            "claim_allowed": False,
        }
        for silence_id, variation, result, status, guard in rows
    ]


def obstruction_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "OBS3753_0_positive_metric_independent_norm",
            "A positive Hilbert norm is not automatically supplied by de Rham topology alone.",
            "If B_top is not parent-owned and positive on the charge block, contraction is only a normalization convention.",
            "source B_top from parent symplectic/charge sector or use rank-one bound ||Omega_M||||ell_M||_*",
        ),
        (
            "OBS3753_1_fixed_homology",
            "The local exterior class [Sigma_M] must be parent-fixed, not chosen from observed orbital/source surfaces.",
            "If not fixed, delta Sigma and domain motion produce preferred-frame/location residuals.",
            "derive fixed homology/domain theorem or retain domain projector bounds",
        ),
        (
            "OBS3753_2_flux_ward",
            "Pi_M algebra does not by itself prove d(Pi_M J_H)=0.",
            "Mass/source drift remains possible even with metric-silent projector.",
            "derive Ward/Euler source conservation for ell_M(J_H)",
        ),
        (
            "OBS3753_3_newton_G_calibration",
            "A conserved topological charge is not yet Newton's GM.",
            "Need universal coupling normalization from EH/Poisson/asymptotic matching.",
            "derive source-to-Poisson calibration law",
        ),
        (
            "OBS3753_4_em_maxwell_parallel",
            "The same topological charge pattern may later support EM charge, but Maxwell stress is not derived here.",
            "No EM claim from 3753.",
            "separate Maxwell/charge-current branch later",
        ),
    ]
    return [
        {
            **base(ts),
            "obstruction_id": obstruction_id,
            "obstruction": obstruction,
            "why_it_matters": why,
            "fallback_or_next_action": action,
            "claim_allowed": False,
        }
        for obstruction_id, obstruction, why, action in rows
    ]


def reduced_hop_source_rows(ts: str, cap: float) -> list[dict[str, object]]:
    rows = [
        (
            "RHS3753_0_clean_topological_route",
            "H_op = C_pair * 1 * 1 * PPN_response_norm plus ordinary source-response terms",
            f"PPN_response_norm <= {cap:.12e} if C_pair normalized to one",
            "uses Pi_M contraction and delta_g Pi_M=0, but still needs source coupling calibration",
            "CONDITIONAL_PROGRESS",
        ),
        (
            "RHS3753_1_topological_oblique_route",
            "H_op = C_pair * ||Omega_M||_P ||ell_M||_{P,*} * PPN_response_norm",
            f"full product <= {cap:.12e}",
            "if B_top is not dual-normalized",
            "BOUND_ROUTE",
        ),
        (
            "RHS3753_2_spectral_fallback_route",
            "H_op includes C_spec ||delta_g A_P||/gap_P and domain/boundary terms",
            f"absolute product <= {cap:.12e}",
            "if projector is metric-built",
            "FALLBACK_ROUTE",
        ),
        (
            "RHS3753_3_source_coupling_next",
            "M_eff := k_M ell_M(J_H), mu_obs := G_eff M_eff",
            "derive k_M and G_eff from parent EH/Poisson matching",
            "this is where Newton coupling enters, not inside projector algebra",
            "NEXT_DERIVATION",
        ),
    ]
    return [
        {
            **base(ts),
            "row_id": row_id,
            "reduced_law_or_definition": law,
            "required_bound_or_equation": required,
            "condition": condition,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, law, required, condition, status in rows
    ]


def claim_gate_rows(ts: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(bool(row["exists"]) for row in grouped["sources"])
    exact_projector = any(row["signature_id"] == "AS3753_3_projector_definition" and row["status"] == "EXACT_ALGEBRA" for row in grouped["signatures"])
    metric_silence = any(row["check_id"] == "TC3753_5_metric_silence" and row["status"] == "PASS_IF_TOPOLOGY_SIGNED" for row in grouped["theorem_checks"])
    ward_open = any(row["check_id"] == "TC3753_7_flux_not_proved" and row["status"] == "OPEN_SOURCE_WARD_GAP" for row in grouped["theorem_checks"])
    gates = [
        ("CG3753_0_sources", "all 3753 source paths exist", all_sources, "path hygiene"),
        ("CG3753_1_action_signature", "parent action signature written", len(grouped["signatures"]) == 9, "constructive signature emitted"),
        ("CG3753_2_projector_algebra", "rank-one projector algebra closes", exact_projector, "Pi_M J=Omega_M ell_M(J)"),
        ("CG3753_3_metric_silence", "metric projector silence derived under topology signature", metric_silence, "conditional on parent-owned topology"),
        ("CG3753_4_flux_ward", "mass/source flux Ward identity derived", False, "explicitly open"),
        ("CG3753_5_newton_calibration", "topological charge calibrated to Newton GM", False, "explicitly open"),
        ("CG3753_6_no_hidden_closure", "open Ward gap is recorded", ward_open, "prevents smuggling closure"),
        ("CG3753_7_local_claim", "local GR/Newton/PPN claim allowed", False, "3753 is an action signature, not full local-GR proof"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3753_0_constructive_progress",
            "PARENT_TOPOLOGICAL_PROJECTOR_SIGNATURE_WRITTEN",
            "3753 supplies the exact form Pi_M J=Omega_M ell_M(J) and the parent multiplier conditions that make it idempotent and metric-silent.",
        ),
        (
            "DEC3753_1_no_overclaim",
            "SOURCE_WARD_AND_G_CALIBRATION_STILL_OPEN",
            "The projector branch can remove projector stress, but it does not by itself derive Newton's source coupling.",
        ),
        (
            "DEC3753_2_best_next",
            "DERIVE_WARD_POISSON_COUPLING",
            "The next useful leap is deriving d ell_M(J_H)=0 and matching M_eff to Poisson/EH normalization.",
        ),
        (
            "DEC3753_3_em_later",
            "EM_TOPOLOGICAL_CHARGE_ANALOG_RETAINED",
            "The same architecture may help EM charge, but Maxwell stress requires its own current/action branch.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for decision_id, decision, meaning in rows
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3753_0",
            "target_doc": "3754-Y5-R2FR-source-Ward-Poisson-calibration-law.md",
            "target_script": "scripts/Y5_R2FR_3754_source_Ward_Poisson_calibration_law.py",
            "objective": "derive or bound d ell_M(J_H)=0, M_eff=k_M ell_M(J_H), and the EH/Poisson matching that calibrates the topological source charge to Newtonian GM without treating G or source mass as a fitted readout mask",
            "why_this_next": "3753 writes the parent projector; local GR/Newton now hinges on source Ward conservation and calibrated coupling, not projector algebra",
            "claim_allowed": False,
        }
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3753_0",
            "status": "PARENT_TOPOLOGICAL_PROJECTOR_SIGNATURE_WRITTEN_WARD_POISSON_OPEN",
            "summary": "3753 constructs the exact parent-action signature for a metric-independent rank-one topological charge projector. Projector algebra and conditional metric silence close, but Ward flux conservation and Newton/Poisson calibration remain open.",
            "claim_allowed": False,
        }
    ]


def validation_rows(ts: str, paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    checks = [
        ("sources_exist", "all 3753 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("csv_parse", "all generated CSVs parse", all(len(read_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("signature_written", "action signature rows emitted", len(grouped["signatures"]) == 9),
        ("projector_definition", "rank-one projector definition emitted", any(row["signature_id"] == "AS3753_3_projector_definition" for row in grouped["signatures"])),
        ("idempotence_check", "idempotence passes under signature", any(row["check_id"] == "TC3753_0_idempotence" and row["status"] == "PASS_UNDER_SIGNATURE" for row in grouped["theorem_checks"])),
        ("ward_gap_open", "Ward gap kept open", any(row["check_id"] == "TC3753_7_flux_not_proved" and row["status"] == "OPEN_SOURCE_WARD_GAP" for row in grouped["theorem_checks"])),
        ("newton_gap_open", "Newton calibration gap kept open", any(row["check_id"] == "TC3753_8_newton_calibration_not_proved" and row["status"] == "OPEN_G_CALIBRATION_GAP" for row in grouped["theorem_checks"])),
        ("local_claim_blocked", "local claim gate remains false", any(row["gate_id"] == "CG3753_7_local_claim" and row["passed"] is False for row in grouped["claim_gates"])),
        ("next_target", "3754 source coupling target emitted", grouped["next_target"][0]["target_doc"] == "3754-Y5-R2FR-source-Ward-Poisson-calibration-law.md"),
        ("no_formalization_leak", "no 3753 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3753*"))),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": "",
        }
        for validation_id, description, passed in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]], cap: float) -> str:
    lines = [
        "# 3753 — Parent Topological Charge Projector Action Signature",
        "",
        "## Status",
        "",
        "`PARENT_TOPOLOGICAL_PROJECTOR_SIGNATURE_WRITTEN_WARD_POISSON_OPEN`.",
        "",
        "This is the constructive route requested by 3752. It writes the exact parent-owned projector shape rather than merely saying the projector is missing.",
        "",
        "## Parent Action Signature",
    ]
    for row in grouped["signatures"]:
        lines.append(f"- `{row['signature_id']}` `{row['status']}`: {row['action_clause']} — {row['what_it_closes']}")
    lines.extend(["", "## Theorem Checks"])
    for row in grouped["theorem_checks"]:
        lines.append(f"- `{row['check_id']}` `{row['status']}`: {row['derivation_or_statement']}")
    lines.extend(["", "## Variation Silence"])
    for row in grouped["variation_silence"]:
        lines.append(f"- `{row['silence_id']}` `{row['status']}`: `{row['variation']}` -> {row['result']}")
    lines.extend(["", "## Reduced H_op And Coupling Interface", f"- Imported cap remains `H_op <= {cap:.12e}`."])
    for row in grouped["reduced_source"]:
        lines.append(f"- `{row['row_id']}` `{row['status']}`: {row['reduced_law_or_definition']} | {row['required_bound_or_equation']}")
    lines.extend(["", "## Obstructions Kept Live"])
    for row in grouped["obstructions"]:
        lines.append(f"- `{row['obstruction_id']}`: {row['obstruction']} -> {row['fallback_or_next_action']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["sources"]:
        lines.append(f"- `{row['source_id']}` exists=`{row['exists']}`: `{row['source_path']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ts = stamp()
    cap = cap_value()
    paths = {
        "doc": DOC_PATH,
        "sources": RESIDUALS / "P8_Y5_R2FR_3753_SOURCE_REGISTER.csv",
        "signatures": RESIDUALS / "P8_Y5_R2FR_3753_PARENT_ACTION_SIGNATURE_ROWS.csv",
        "theorem_checks": RESIDUALS / "P8_Y5_R2FR_3753_PROJECTOR_THEOREM_CHECKS.csv",
        "variation_silence": RESIDUALS / "P8_Y5_R2FR_3753_VARIATION_SILENCE_CHECKS.csv",
        "obstructions": RESIDUALS / "P8_Y5_R2FR_3753_OBSTRUCTIONS_AND_FALLBACKS.csv",
        "reduced_source": RESIDUALS / "P8_Y5_R2FR_3753_REDUCED_HOP_AND_SOURCE_COUPLING.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3753_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3753_DECISION_ROWS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3753_NEXT_TARGET.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3753_STATUS.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3753_VALIDATION.csv",
    }
    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(ts),
        "signatures": action_signature_rows(ts),
        "theorem_checks": theorem_check_rows(ts),
        "variation_silence": variation_silence_rows(ts),
        "obstructions": obstruction_rows(ts),
        "reduced_source": reduced_hop_source_rows(ts, cap),
        "decisions": decision_rows(ts),
        "next_target": next_target_rows(ts),
        "status": status_rows(ts),
    }
    grouped["claim_gates"] = claim_gate_rows(ts, grouped)
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    DOC_PATH.write_text(render_doc(grouped, cap), encoding="utf-8")
    grouped["validation"] = validation_rows(ts, paths, grouped)
    write_csv(paths["validation"], grouped["validation"])
    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3753 validation failed: {failures}")
    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists() and str(cache.resolve()).startswith(str(PCW.resolve())):
        shutil.rmtree(cache)
    print("wrote 3753 checkpoint: parent topological charge projector signature written; Ward/Poisson coupling open")


if __name__ == "__main__":
    main()
