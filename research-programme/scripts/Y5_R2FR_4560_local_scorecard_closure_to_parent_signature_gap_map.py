from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4560"
CLAIM_ID = "L-402"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_SCORECARD_TO_PARENT_SIGNATURE_GAP_MAP_4560"
MARKER = "PPC4161_LOCAL_SCORECARD_CLOSURE_TO_PARENT_SIGNATURE_GAP_MAP_4560"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SIGNATURE_GAP_MAP_4560"
DECISION = "LOCAL_PRIVATE_SCORECARD_COMPLETE_PARENT_SIGNATURE_GAP_MAP_WRITTEN_PUBLIC_LOCAL_GR_STILL_BLOCKED"
NEXT_TARGET = "4561-Y5-R2FR-parent-EH-IR-selector-scale-law-or-explicit-EFT-residual-envelope.md"

FORMAL_PATH = FORMAL / "576-PPC4161-local-scorecard-closure-to-parent-signature-gap-map.md"
DOC_PATH = POST / "4560-Y5-R2FR-local-scorecard-closure-to-parent-signature-gap-map.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4559 = FORMAL / "575-PPC4161-R10-Yukawa-private-zero-or-real-bound-source-row.md"
DOC_4539 = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
DOC_4173 = FORMAL / "189-PPC4161-local-empirical-validation-pack.md"
POST_4181 = POST / "4181-Y5-R2FR-EH-local-metric-principal-block-origin-or-effective-GR-demotion.md"
POST_4184 = POST / "4184-Y5-R2FR-Palatini-IR-normal-form-selector-under-AMF-or-residual-EFT-bound.md"
POST_4185 = POST / "4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
POST_4187 = POST / "4187-Y5-R2FR-local-memory-support-projector-zero-law-for-cGamma-or-PPN-clock-bound.md"
POST_1022 = POST / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
SCORECARD_4559 = SOURCE_DIR / "P8_Y5_R2FR_4559_SCORECARD_AFTER_R10.csv"
RANKING_4559 = SOURCE_DIR / "P8_Y5_R2FR_4559_ACTIVE_PRODUCT_PRESSURE_RANKING_AFTER_R10.csv"
GATES_4559 = SOURCE_DIR / "P8_Y5_R2FR_4559_CLAIM_GATES.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4560_SOURCE_REGISTER.csv"
SCORECARD_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4560_LOCAL_PRIVATE_SCORECARD_AUDIT.csv"
PARENT_GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4560_PARENT_SIGNATURE_GAP_MAP.csv"
DEPENDENCY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4560_ZERO_TO_SIGNATURE_DEPENDENCY.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4560_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4560_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4560_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4560_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4560_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
        ("SRC4560_00_4559_doc", "4559 local scorecard completion", DOC_4559, "no active private product-pressure rows remain"),
        ("SRC4560_01_4559_ranking", "4559 active ranking none", RANKING_4559, "0,NONE"),
        ("SRC4560_02_4559_scorecard", "4559 scorecard all private zero", SCORECARD_4559, "PASS_PRIVATE_SELECTOR_ZERO_ANCHOR_ONLY_NONPUBLIC"),
        ("SRC4560_03_4559_gates", "4559 parent firewall", GATES_4559, "PASS_PARENT_FIREWALL"),
        ("SRC4560_04_4539_contract", "4539 parent action selector contract", DOC_4539, "PAC4539_4_IR_selector"),
        ("SRC4560_05_4539_failure", "4539 current parent failure", DOC_4539, "The current corpus cannot promote PPC4161-GP-HQNP"),
        ("SRC4560_06_packet_parent_flags", "packet parent flags", PACKET_PATH, "EH_origin_parent_derived = false"),
        ("SRC4560_07_packet_coupling", "packet calibrated source coupling", PACKET_PATH, "kappa_eff = kappa_* Z_0"),
        ("SRC4560_08_4181_EH", "4181 EH origin demotion", POST_4181, "strong formal candidate, not a completed derivation"),
        ("SRC4560_09_4184_IR", "4184 Palatini/IR residual map", POST_4184, "selector assumptions are not yet fully parent-derived"),
        ("SRC4560_10_4185_extra", "4185 extra invariant map", POST_4185, "c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, c_bdy"),
        ("SRC4560_11_4187_memory", "4187 memory support guard", POST_4187, "No local-GR, R10, PPN, clock or orbital success claim is allowed"),
        ("SRC4560_12_1022_quotient", "1022 quotient/vertical gap", POST_1022, "q/v_X/action/matter/boundary certificate"),
        ("SRC4560_13_4173_empirical", "4173 R10 anchor-only guard", DOC_4173, "R10 is anchor-only"),
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
                "role": "4560 local scorecard closure to parent signature gap map",
                "valid_for_claim": "False",
            }
        )
    return rows


def scorecard_audit_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(SCORECARD_4559):
        rows.append(
            {
                "score_id": row.get("score_id", ""),
                "observable": row.get("observable", ""),
                "arena": row.get("arena", ""),
                "private_selector_prediction": row.get("private_selector_prediction", ""),
                "private_selector_status": row.get("private_selector_status", ""),
                "active_private_pressure": row.get("active_private_pressure", ""),
                "global_parent_status": row.get("global_parent_status", ""),
                "public_claim_allowed": row.get("public_claim_allowed", ""),
                "valid_for_claim": row.get("valid_for_claim", "False"),
                "4560_interpretation": "private_local_pressure_closed_public_parent_claim_still_false",
            }
        )
    ranking = read_csv(RANKING_4559)
    rows.append(
        {
            "score_id": "SC4560_ACTIVE_SUMMARY",
            "observable": ranking[0].get("observable", "MISSING") if ranking else "MISSING",
            "arena": ranking[0].get("arena", "MISSING") if ranking else "MISSING",
            "private_selector_prediction": "all_scorecard_rows_zero" if ranking and ranking[0].get("observable") == "NONE" else "MISSING",
            "private_selector_status": "LOCAL_PRIVATE_PRODUCT_PRESSURE_COMPLETE" if ranking and ranking[0].get("observable") == "NONE" else "ACTIVE_ROWS_REMAIN",
            "active_private_pressure": "False" if ranking and ranking[0].get("observable") == "NONE" else "True",
            "global_parent_status": "not_promoted_global_parent_unsigned",
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
            "4560_interpretation": "scorecard pressure complete but parent proof incomplete",
        }
    )
    return rows


def parent_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "PS4560_0_domain_projector",
            "parent_signature_clause": "compact local collar and P_loc projector owned by parent before variation",
            "mathematical_contract": "delta(P_loc S_parent)=P_loc delta S_parent + boundary_zero through <=2PN",
            "current_status": "not_globally_parent_signed",
            "blocks_public_claim": "True",
            "if_signed": "local equations are read before empirical material/orbital labels enter",
            "evidence_pointer": "PAC4539_0_domain",
            "next_action": "derive P_loc/projector commutation or retain bounded transition-current rows",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_1_EH_IR_principal_block",
            "parent_signature_clause": "EH/Palatini principal block and IR/no-light-mode selector",
            "mathematical_contract": "S_parent|loc -> S_EC[e,omega] -> S_EH[g_obs] + boundary with extra <=2PN modes absent/heavy/bounded",
            "current_status": "conditional_theorem_current_MTS_derivation_false",
            "blocks_public_claim": "True",
            "if_signed": "gamma, beta, orbital combo, Newton baseline and R10 no-pole branch become parent-derived rather than effective",
            "evidence_pointer": "4181; PAC4539_4_IR_selector",
            "next_action": "attack parent EH/IR scale law or explicit residual EFT envelope",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_2_same_metric_source_coupling",
            "parent_signature_clause": "same-metric Hilbert source coupling and common kappa_eff normalization",
            "mathematical_contract": "G_mu_nu[g_obs]=kappa_eff T_H_mu_nu, kappa_eff=kappa_* Z_0, D_A ln kappa_eff=0",
            "current_status": "private_calibrated_branch_not_global_numeric_G_prediction",
            "blocks_public_claim": "True",
            "if_signed": "stress conservation, zeta channels, source normalization and Newtonian coupling are parent-owned",
            "evidence_pointer": "PPC4161_PACKET_CALIBRATED_SOURCE_COUPLING_4178",
            "next_action": "derive parent ownership of Z_0/kappa_* scale law or keep G_cal calibrated only",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_3_Hamiltonian_mass_charge",
            "parent_signature_clause": "Hamiltonian worldtube mass charge fixed before orbital readout",
            "mathematical_contract": "M_H^dress = H_tau[S_link]-H_ref and orbital GM is downstream test data only",
            "current_status": "private_same_object_identity_not_public_parent_theorem",
            "blocks_public_claim": "True",
            "if_signed": "Newton/Gauss/orbital readout avoids circular GM import at parent level",
            "evidence_pointer": "4170/4171 private chain",
            "next_action": "connect source charge to parent action with no readout re-entry",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_4_boundary_sector_no_flux",
            "parent_signature_clause": "global sector no-leak and compact boundary/interface no-flux",
            "mathematical_contract": "P_loc P_gal=P_loc P_cos=0 and all radiative/open-memory flux is routed through boundary/Hamiltonian charge",
            "current_status": "boundary_no_flux_parent_global_derived_false",
            "blocks_public_claim": "True",
            "if_signed": "alpha3, xi, zeta3 and local PPN rows do not receive hidden boundary/global sector leakage",
            "evidence_pointer": "PAC4539_5_sector_interfaces; packet boundary flags",
            "next_action": "derive support/no-flux theorem for P_loc against galaxy/cosmology/memory sectors",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_5_quotient_vertical_no_pole",
            "parent_signature_clause": "q-natural vertical silence / X absent before variation",
            "mathematical_contract": "q: Conf_parent -> Q_obs with Dq[v_X]=0; S_parent=S_red[q(Phi)] and matter descends through Obs(q(Phi))",
            "current_status": "conditional_route_missing_q_vX_action_matter_boundary_certificate",
            "blocks_public_claim": "True",
            "if_signed": "hidden scalar/vector/projector force channels and R10 finite-pole rows are removed before fitting",
            "evidence_pointer": "1022 q/v_X/action/matter/boundary certificate",
            "next_action": "construct q/v_X/action descent certificate after EH/IR root is stabilized",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_6_memory_support_silence",
            "parent_signature_clause": "local memory support/projector c_Gamma silence",
            "mathematical_contract": "P_loc Gamma_mem has vertical, compact-support, source-free, boundary-routed and no homogeneous tensor residue clauses",
            "current_status": "c_Gamma_parent_zero_false",
            "blocks_public_claim": "True",
            "if_signed": "memory hair cannot reopen xi, Gdot/G, R10 or clock residuals",
            "evidence_pointer": "4187 memory support projector contract",
            "next_action": "derive memory equation/support silence or retain finite c_Gamma coefficient bounds",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_7_edge_boundary_charge",
            "parent_signature_clause": "edge/boundary primitive and cohomology silence",
            "mathematical_contract": "Q_X=0/proper/exact with B_X primitive, no harmonic/corner leakage and source-projector orthogonality",
            "current_status": "blocked_by_boundary_primitive_and_cohomology_gaps",
            "blocks_public_claim": "True",
            "if_signed": "R10 edge charge, alpha3 boundary vector and local source-bound rows stay closed without tuning",
            "evidence_pointer": "1020/1021/1022 boundary route rows",
            "next_action": "derive B_X primitive or fill edge-bound source rows",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_8_empirical_full_data",
            "parent_signature_clause": "source-backed empirical evidence complete enough for public claims",
            "mathematical_contract": "full alpha(lambda) R10 curve/table, PPN/clock/WEP/orbital comparators with raw/source provenance and no anchor-only overclaim",
            "current_status": "private_comparator_passes_but_R10_anchor_only",
            "blocks_public_claim": "True",
            "if_signed": "public empirical robustness claims can be made after parent signatures and source-backed data pass",
            "evidence_pointer": "4173 R10 anchor-only guard; 4559 full-curve blocker",
            "next_action": "acquire full R10 alpha(lambda) curve/table and preserve nonclaim until parent route closes",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "PS4560_9_sector_unification",
            "parent_signature_clause": "same parent action owns local, galaxy, cosmology, time, EM and quantum/particle sectors",
            "mathematical_contract": "sector interface matrix with no local collar leakage and no contradiction between local-GR branch and cosmology/galaxy memory branches",
            "current_status": "not_adopted_global",
            "blocks_public_claim": "True",
            "if_signed": "unified field-theory framing becomes more than a local effective branch",
            "evidence_pointer": "AA4539_5_global_unification",
            "next_action": "build sector interface matrix after EH/IR and source-coupling signatures are stabilized",
            "valid_for_claim": "False",
        },
    ]


def dependency_rows() -> list[dict[str, Any]]:
    return [
        {
            "dependency_id": "ZD4560_0_alpha3",
            "private_zero": "alpha3=0",
            "local_basis": "private vector/source/boundary cubic channels classified to zero",
            "parent_signatures_required": "PS4560_1_EH_IR_principal_block;PS4560_2_same_metric_source_coupling;PS4560_4_boundary_sector_no_flux;PS4560_5_quotient_vertical_no_pole",
            "public_claim_status": "blocked_until_parent_signed",
            "valid_for_claim": "False",
        },
        {
            "dependency_id": "ZD4560_1_xi",
            "private_zero": "xi=0",
            "local_basis": "preferred-location/trace-free carriers absent inside compact centred branch",
            "parent_signatures_required": "PS4560_1_EH_IR_principal_block;PS4560_4_boundary_sector_no_flux;PS4560_6_memory_support_silence",
            "public_claim_status": "blocked_until_parent_signed",
            "valid_for_claim": "False",
        },
        {
            "dependency_id": "ZD4560_2_zeta3",
            "private_zero": "zeta3=0",
            "local_basis": "Hilbert total stress conservation, Maxwell-Hodge ownership and routed no-flux boundary",
            "parent_signatures_required": "PS4560_2_same_metric_source_coupling;PS4560_4_boundary_sector_no_flux;PS4560_9_sector_unification",
            "public_claim_status": "blocked_until_parent_signed",
            "valid_for_claim": "False",
        },
        {
            "dependency_id": "ZD4560_3_orbital_combo",
            "private_zero": "((2+2gamma-beta)/3)-1=0",
            "local_basis": "exact algebra from gamma=1 and beta=1 plus no orbital GM import",
            "parent_signatures_required": "PS4560_1_EH_IR_principal_block;PS4560_3_Hamiltonian_mass_charge;PS4560_4_boundary_sector_no_flux",
            "public_claim_status": "blocked_until_parent_signed",
            "valid_for_claim": "False",
        },
        {
            "dependency_id": "ZD4560_4_R10",
            "private_zero": "alpha_Yukawa(lambda=38.6um)=0",
            "local_basis": "pure EH/Newton no-extra-finite-range branch has no finite-mass Yukawa pole",
            "parent_signatures_required": "PS4560_1_EH_IR_principal_block;PS4560_5_quotient_vertical_no_pole;PS4560_6_memory_support_silence;PS4560_7_edge_boundary_charge;PS4560_8_empirical_full_data",
            "public_claim_status": "blocked_until_parent_signed_and_full_curve_sourced",
            "valid_for_claim": "False",
        },
        {
            "dependency_id": "ZD4560_5_Newton_GR_bridge",
            "private_zero": "Newton/GR local branch structural reduction",
            "local_basis": "Hamiltonian source charge, Poisson/Gauss readout, calibrated G_cal and full private PPN vector",
            "parent_signatures_required": "PS4560_0_domain_projector;PS4560_1_EH_IR_principal_block;PS4560_2_same_metric_source_coupling;PS4560_3_Hamiltonian_mass_charge",
            "public_claim_status": "blocked_until_parent_signed",
            "valid_for_claim": "False",
        },
    ]


def promotion_gate_rows(gaps: list[dict[str, Any]], scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
    no_active = any(row.get("score_id") == "SC4560_ACTIVE_SUMMARY" and row.get("observable") == "NONE" for row in scorecard)
    any_blocker = any(row.get("blocks_public_claim") == "True" for row in gaps)
    return [
        {
            "gate_id": "PG4560_0_local_private_scorecard",
            "requirement": "no active private product-pressure rows remain",
            "status": "PASS_PRIVATE_LOCAL" if no_active else "FAIL_ACTIVE_ROWS_REMAIN",
            "claim_effect": "local private branch internally scorecard-clean",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4560_1_parent_signatures",
            "requirement": "all parent signature clauses signed by current corpus",
            "status": "FAIL_UNSIGNED" if any_blocker else "PASS_PARENT_SIGNED",
            "claim_effect": "public/local-GR parent theorem remains blocked",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4560_2_no_closure_smuggling",
            "requirement": "private/effective branch cannot be promoted because local comparator rows pass",
            "status": "PASS_GUARD",
            "claim_effect": "prevents confusing compatibility with derivation",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4560_3_next_root",
            "requirement": "single next derivation root selected",
            "status": "PASS_NEXT_SELECTED",
            "claim_effect": "next target is EH/IR selector scale law or residual EFT envelope",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4560_0",
            "decision": DECISION,
            "summary": "4560 records a real state transition: the private local product-pressure scorecard is clean, but every route to a public parent-derived local-GR/Newton/R10 claim still depends on unsigned parent signatures. The map identifies the parent clauses, assigns each private zero to its required signatures, blocks public promotion, and selects the EH/IR principal-block scale law as the next root derivation target.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "The EH/IR principal block is the highest-leverage parent signature: gamma/beta, orbital, R10 no-pole, Newton baseline and most local GR compatibility depend on it.",
            "success_condition": "Derive a parent scale/normal-form law selecting the EC/Palatini/EH two-derivative block with no extra light <=2PN modes, or write explicit residual EFT envelopes into PPN/R10/clock/orbital arenas.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "next_target": NEXT_TARGET,
            "local_private_scorecard_complete": "True",
            "public_parent_local_GR_claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    deps: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4560_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    score_ok = bool(scorecard)
    score_ok = score_ok and all(row.get("active_private_pressure") == "False" for row in scorecard)
    score_ok = score_ok and all(row.get("public_claim_allowed") == "False" for row in scorecard)
    score_ok = score_ok and any(row.get("score_id") == "SC4560_ACTIVE_SUMMARY" and row.get("observable") == "NONE" for row in scorecard)
    rows.append(
        {
            "validation_id": "VAL4560_1_scorecard",
            "check": "local private scorecard has no active rows and no public claims",
            "status": "PASS" if score_ok else "FAIL",
            "details": f"{len(scorecard)} scorecard audit rows checked",
        }
    )

    required_tokens = [
        "EH/Palatini",
        "same-metric Hilbert",
        "Hamiltonian worldtube",
        "no-flux",
        "q-natural",
        "memory",
        "edge",
        "full alpha(lambda)",
        "sector interface",
    ]
    gap_text = " ".join(str(value) for row in gaps for value in row.values())
    gaps_ok = len(gaps) >= 9 and all(token in gap_text for token in required_tokens)
    gaps_ok = gaps_ok and all(row.get("blocks_public_claim") == "True" for row in gaps)
    gaps_ok = gaps_ok and all(row.get("valid_for_claim") == "False" for row in gaps)
    rows.append(
        {
            "validation_id": "VAL4560_2_parent_gaps",
            "check": "parent signature gap map covers required root clauses and blocks public claim",
            "status": "PASS" if gaps_ok else "FAIL",
            "details": f"{len(gaps)} parent gap rows checked",
        }
    )

    dep_text = " ".join(str(value) for row in deps for value in row.values())
    deps_ok = all(token in dep_text for token in ["alpha3=0", "xi=0", "zeta3=0", "alpha_Yukawa", "Newton/GR"])
    deps_ok = deps_ok and all(row.get("valid_for_claim") == "False" for row in deps)
    rows.append(
        {
            "validation_id": "VAL4560_3_dependencies",
            "check": "private zeros are mapped to parent signature dependencies",
            "status": "PASS" if deps_ok else "FAIL",
            "details": f"{len(deps)} dependency rows checked",
        }
    )

    gates_ok = any(row.get("status") == "PASS_PRIVATE_LOCAL" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "FAIL_UNSIGNED" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "PASS_NEXT_SELECTED" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4560_4_gates",
            "check": "promotion gates pass private/local but fail public parent signature",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "promotion gates checked",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4560_5_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4560_OVERALL",
            "check": "4560 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    deps: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4560 - local scorecard closure to parent signature gap map

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4559 cleared the local private product-pressure scorecard:

```text
active_private_pressure = NONE.
```

4560 turns that into the next honest object: a parent-signature gap map. The current state is:

```text
private local scorecard compatibility = clean
public parent-derived local-GR/Newton/R10 theorem = blocked
```

The block is not a small numeric miss. The private zeros still rely on parent signatures for the EH/Palatini principal block, same-metric Hilbert source coupling, Hamiltonian mass charge, boundary/no-flux separation, quotient/vertical no-pole silence, memory support silence, edge/boundary charge silence, empirical full-data gates and sector unification.

## Local Private Scorecard Audit

{markdown_table(scorecard)}

## Parent Signature Gap Map

{markdown_table(gaps)}

## Zero-To-Signature Dependency Map

{markdown_table(deps)}

## Promotion Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4560 maps the completed private local scorecard to the exact unsigned parent signatures required for any public parent-derived local-GR/Newton/R10 claim.",
        "current_evidence": "Generated source register, local private scorecard audit, parent signature gap map, zero-to-signature dependency map, promotion gates, status and validation CSVs.",
        "status": "private_local_scorecard_complete_parent_signature_gap_map_written_public_claim_blocked",
        "next_test": NEXT_TARGET,
        "failure_mode": "Treating clean private local compatibility as proof that the MTS parent action derives GR/Newton without signing EH/IR, source, boundary, quotient, memory and empirical gates.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "next root derivation target is the parent EH/IR selector scale law or explicit residual EFT envelope.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    scorecard = scorecard_audit_rows()
    gaps = parent_gap_rows()
    deps = dependency_rows()
    gates = promotion_gate_rows(gaps, scorecard)
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SCORECARD_AUDIT_CSV, scorecard)
    write_csv(PARENT_GAP_CSV, gaps)
    write_csv(DEPENDENCY_CSV, deps)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4560 - local scorecard closure to parent signature gap map\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, scorecard, gaps, deps, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, scorecard, gaps, deps, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4560 Local Scorecard Closure To Parent Signature Gap Map

Marker: `{MARKER}`  
The private local product-pressure scorecard is now clean, but public parent-derived local GR/Newton/R10 remains blocked:

```text
private local scorecard compatibility = clean
public parent theorem = blocked by unsigned parent signatures
```

The required parent signatures are now mapped: EH/Palatini IR principal block, same-metric Hilbert source coupling, Hamiltonian mass charge, global no-flux/support separation, quotient/vertical no-pole silence, memory support silence, edge/boundary charge silence, full empirical source data and sector unification. The next root target is the parent EH/IR selector scale law or an explicit residual EFT envelope.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4560 Packet Integration - Parent Signature Gap Map

Marker: `{PACKET_MARKER}`  
The packet may now say the private local product-pressure scorecard is complete. It must not say the MTS parent derives public local GR/Newton/R10 until the parent signatures in 4560 are proved. The next root is EH/IR principal-block selection: derive it from the parent action or keep an explicit residual EFT envelope.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4560_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
