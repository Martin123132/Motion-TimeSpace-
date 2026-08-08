from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4376"
CLAIM_ID = "L-217"
MARKER = "PPC4161_TRANSITION_SOURCE_SHADOW_BAN_OR_EPROFILE_FIRST_SOURCE_DENSITY_ROW_4376"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SOURCE_SHADOW_BAN_OR_EPROFILE_FIRST_SOURCE_DENSITY_ROW_4376"
DECISION = "SOURCE_SHADOW_BAN_CONDITIONAL_ONLY_NOETHER_LIMIT_PROVED_EPROFILE_FIRST_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4377-Y5-R2FR-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md"

FORMAL_PATH = FORMAL / "392-PPC4161-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md"
DOC_PATH = POST / "4376-Y5-R2FR-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4376_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4376_00_4375_formal": (
        FORMAL / "391-PPC4161-transition-density-profile-owner-or-Emass-numeric-source-bound.md",
        "source-shadow/topological wrong-distribution density",
        "4375 names the exact profile blocker: a source-shadow or topological wrong-distribution density.",
    ),
    "SRC4376_01_4375_countermodel": (
        SOURCE_DIR / "P8_Y5_R2FR_4375_COUNTERMODELS.csv",
        "CM4375_0_zero_monopole_shadow",
        "zero-monopole source-shadow countermodel survives total mass equality.",
    ),
    "SRC4376_02_4375_clause": (
        SOURCE_DIR / "P8_Y5_R2FR_4375_PROFILE_OWNER_CLAUSES.csv",
        "PO4375_3_no_source_shadow_density",
        "4375 clause marking no-source-shadow density as the open key blocker.",
    ),
    "SRC4376_03_total_hilbert_owner": (
        SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv",
        "THO2615_3_source_shadow_ban",
        "2615 identifies the needed no separate source-shadow functional clause.",
    ),
    "SRC4376_04_noether_exchange": (
        SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
        "NEC2615_2_weight_collapse",
        "Noether exchange collapses weights inside live action exchange edges.",
    ),
    "SRC4376_05_no_source_prefactor": (
        SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv",
        "NSP2615_1_same_action_filter",
        "same-action filter rejects a source-only duplication when parent grammar forbids the extra functional.",
    ),
    "SRC4376_06_hidden_hom": (
        SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "ODT2659_1_exact_typed_theorem",
        "typed domain exclusion would make hidden/source-shadow slots ill-typed.",
    ),
    "SRC4376_07_domain_matrix": (
        SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv",
        "RED2659_1_functor_domain",
        "ordinary matter functor domain must exclude shadow frames and hidden current slots.",
    ),
    "SRC4376_08_owner_no_wA": (
        FORMAL / "377-PPC4161-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md",
        "single parent action-density line",
        "4361 assembles the owner/no-wA conditional theorem and lists unsigned parent clauses.",
    ),
    "SRC4376_09_visible_hilbert": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "T_H = -2/sqrt(-g_obs) delta S_vis/delta g_obs.",
        "4210 defines calibrated visible matter as a Hilbert source.",
    ),
    "SRC4376_10_source_charge": (
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "int_W rho_H dV_H = M_H^dress[W_H;tau]",
        "4211 supplies the integrated source-charge owner contract.",
    ),
    "SRC4376_11_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "Poynting/EM energy is Hilbert stress or boundary flux, not a second bulk source.",
    ),
    "SRC4376_12_selector": (
        SOURCE_DIR / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv",
        "WSC2577_1_worldtube_selector",
        "source worldtube must be fixed before readout.",
    ),
    "SRC4376_13_xi_zero": (
        FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md",
        "Source-label-forgetting Hilbert-owner branch:",
        "4332 gives the branch-local source-label/hidden-prefactor zero route.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def shadow_ban_attempt_rows() -> List[Dict[str, str]]:
    return [
        {
            "attempt_id": "SBA4376_0_define_shadow_density",
            "claim_piece": "source-shadow density profile",
            "formal_statement": "rho_eff = rho_H + rho_shadow with int_W rho_shadow dV_H = 0 and rho_shadow_perp != 0",
            "derivation_result": "SETUP_EXACT",
            "what_it_proves": "same integrated mass can coexist with a nonzero profile residual",
            "current_blocker": "not a proof of failure; it is the countermodel class to be banned or bounded",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SBA4376_1_same_action_Hilbert_filter",
            "claim_piece": "same-action Hilbert source filter",
            "formal_statement": "Allowed source density on W_H is only rho_H := T_H(n,n)/c^2 with T_H := -2/sqrt(-g_obs) delta S_vis/delta g_obs",
            "derivation_result": "EXACT_CONDITIONAL_ZERO",
            "what_it_proves": "if no additional source functional/current exists, rho_shadow=0 and E_profile=0",
            "current_blocker": "the no additional source functional/current premise is not parent-signed globally",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SBA4376_2_Noether_exchange_limitation",
            "claim_piece": "what Noether exchange can and cannot kill",
            "formal_statement": "sum_i w_i C_i^nu=0 collapses weights only on live exchange edges inside the action graph",
            "derivation_result": "LIMIT_THEOREM_DERIVED",
            "what_it_proves": "Noether exchange blocks relative weights in connected ordinary action sectors",
            "current_blocker": "it cannot kill a separate source-only functional absent from matter dynamics/exchange graph",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SBA4376_3_typed_domain_filter",
            "claim_piece": "no hidden/source-shadow operator slot",
            "formal_statement": "Allowed[S_ord] has domain Q_obs x MatterFields_Q x Rep_fixed and no Hom(source_label, source_density) target",
            "derivation_result": "EXACT_CONDITIONAL_TYPE_ERROR",
            "what_it_proves": "a rho_shadow or source-only w_A map is not a well-typed ordinary matter source object",
            "current_blocker": "ordinary matter functor/domain is a contract, not yet derived from a parent construction",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SBA4376_4_topological_profile_filter",
            "claim_piece": "topological representative is not enough",
            "formal_statement": "int_S J_top = int_W rho_H dV_H does not imply J_top density equals T_H(n,n)/c^2 as a distribution",
            "derivation_result": "DISTRIBUTIONAL_EQUALITY_REQUIRED",
            "what_it_proves": "a closed or linking charge can be correct at monopole level while carrying the wrong local profile",
            "current_blocker": "need J_top=J_H+dB with zero profile contribution, not only equal total charge",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SBA4376_5_current_verdict",
            "claim_piece": "source-shadow ban",
            "formal_statement": "same-action Hilbert derivative + typed no-source-shadow grammar + distributional topological equality => rho_shadow=0 => E_profile=0",
            "derivation_result": "CONDITIONAL_THEOREM_ASSEMBLED_NOT_PARENT_SIGNED",
            "what_it_proves": "the route is mathematically sharp; the exact missing signatures are named",
            "current_blocker": "source-shadow grammar and topological/profile equality remain unsigned in the current corpus",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def grammar_clause_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "GR4376_0_one_action",
            "required_clause": "ordinary active source comes from one source/matter action before readout",
            "mathematical_form": "S_vis = S_matter + S_Maxwell-Hodge + S_binding + dB_impr",
            "status": "PRIVATE_CONDITIONAL",
            "effect_if_signed": "source density is a Hilbert derivative, not an independently selected profile",
            "failure_mode": "separate source-shadow action or post-readout source map",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GR4376_1_Hilbert_derivative_only",
            "required_clause": "active bulk density is exactly T_H(n,n)/c^2",
            "mathematical_form": "rho_eff := T_H(n,n)/c^2 on W_H",
            "status": "CONDITIONAL_SOURCE_OWNER",
            "effect_if_signed": "rho_eff=rho_H pointwise",
            "failure_mode": "non-Hilbert current or source spurion enters rho_eff",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GR4376_2_no_source_only_functional",
            "required_clause": "no S_source used only by gravity while S_matter drives nongravitational dynamics",
            "mathematical_form": "not exists S_shadow[g_obs,theta,lambda_src] with delta S_shadow/delta g_obs contributing to E_munu",
            "status": "UNSIGNED_PARENT_GRAMMAR",
            "effect_if_signed": "rho_shadow=0",
            "failure_mode": "zero-monopole source-shadow density survives",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GR4376_3_no_nonHilbert_current",
            "required_clause": "no extra ordinary source current outside Hilbert stress",
            "mathematical_form": "J_src = kappa_univ T_Hilbert and J_NH=0, or J_NH retained as explicit residual",
            "status": "OPEN_PARALLEL_GATE",
            "effect_if_signed": "blocks source-label/current bypass",
            "failure_mode": "hidden non-Hilbert current carries material/source labels",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GR4376_4_no_hidden_visible_hom",
            "required_clause": "ordinary matter coefficients and source slots have no hidden/source-label Hom target",
            "mathematical_form": "A_ord=q^*A_Q plus A_fixed; source-label maps not factoring through q are ill-typed",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "effect_if_signed": "source-shadow/source-label coefficients are type errors",
            "failure_mode": "hidden/source labels feed source density or constants",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GR4376_5_variation_before_readout",
            "required_clause": "source support and profile are fixed before exterior/orbital/readout restriction",
            "mathematical_form": "W_H := supp(T_H(n,n)) before scoring; no readout-selected sigma_shadow",
            "status": "CONDITIONAL_NOT_GLOBAL",
            "effect_if_signed": "readout cannot manufacture a post-variation profile defect",
            "failure_mode": "support clipped or selected after seeing residuals",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GR4376_6_topological_distributional_equality",
            "required_clause": "topological/Hamiltonian current equals Hilbert density profile as a distribution",
            "mathematical_form": "J_top = J_H + dB_zero_profile, not merely int_S J_top=int_W rho_H dV",
            "status": "OPEN_FOR_PROFILE_CLAIM",
            "effect_if_signed": "topological wrong-distribution countermodel dies",
            "failure_mode": "correct total charge with wrong local distribution",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "GR4376_7_EM_Poynting_once",
            "required_clause": "EM/Poynting/binding energy enters once through Hilbert stress or boundary flux",
            "mathematical_form": "S_i=-T_EM(n,e_i); rho_EM=T_EM(n,n); no second bulk Poynting background",
            "status": "PRIVATE_MAXWELL_HODGE_BRANCH",
            "effect_if_signed": "prevents EM energy from masquerading as source-shadow bulk density",
            "failure_mode": "EM/binding/Poynting double count or omission",
            "valid_for_claim": "False",
        },
    ]


def eprofile_source_rows() -> List[Dict[str, str]]:
    return [
        {
            "row_id": "EP4376_0_rho_H_definition",
            "quantity": "rho_H(y)",
            "definition": "rho_H := T_H(n,n)/c^2 on W_H",
            "units": "mass_density",
            "source_requirement": "same S_vis/S_src Hilbert stress and same observer n",
            "formula_or_transfer": "T_H=-2/sqrt(-g_obs) delta S_vis/delta g_obs",
            "current_status": "DEFINITION_BACKED_SYMBOLIC_NOT_NUMERIC",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EP4376_1_rho_eff_split",
            "quantity": "rho_eff(y)-rho_H(y)",
            "definition": "rho_eff-rho_H := rho_shadow + rho_top_profile + rho_readout_profile",
            "units": "mass_density",
            "source_requirement": "real same-worldtube density/profile input or parent theorem-zero certificate",
            "formula_or_transfer": "rho_eff=rho_H if all source-shadow/topological/readout clauses close",
            "current_status": "MISSING_REAL_PROFILE_OR_ZERO_CERTIFICATE",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EP4376_2_sigma_shadow_perp",
            "quantity": "sigma_shadow_perp(y)",
            "definition": "sigma_shadow_perp := rho_shadow/rho_H - <rho_shadow/rho_H>_rho",
            "units": "dimensionless",
            "source_requirement": "rho_shadow profile on the same W_H with common monopole subtracted",
            "formula_or_transfer": "<f>_rho := M_H^-1 int_W rho_H f dV_H",
            "current_status": "SOURCE_PROFILE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EP4376_3_E_shadow",
            "quantity": "E_shadow",
            "definition": "E_shadow := ||sigma_shadow_perp||_inf",
            "units": "dimensionless",
            "source_requirement": "same-worldtube profile norm with rho_H>0 support convention",
            "formula_or_transfer": "E_profile receives E_shadow unless source-shadow ban is signed",
            "current_status": "BOUND_SYMBOL_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EP4376_4_Green_transfer",
            "quantity": "deltaPhi_shadow(x)",
            "definition": "Newtonian potential sourced by retained zero-monopole source-shadow profile",
            "units": "potential",
            "source_requirement": "rho_H, sigma_shadow_perp and fixed compact support W_H",
            "formula_or_transfer": "deltaPhi_shadow(x)=-G_cal int_W rho_H(y) sigma_shadow_perp(y)/|x-y| dV_y",
            "current_status": "TRANSFER_DERIVED_INPUT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EP4376_5_KN_score_gate",
            "quantity": "E_shadow pass gate",
            "definition": "compact exterior acceleration suppression for zero-monopole source-shadow profile",
            "units": "dimensionless",
            "source_requirement": "K_N(s), delta_N and E_shadow from sourced profile/bound rows",
            "formula_or_transfer": "|deltaa_shadow|/|a_N| <= K_N(s) E_shadow; E_shadow <= delta_N/K_N(s)",
            "current_status": "SCORE_SCHEMA_READY_CLAIM_BLOCKED",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EP4376_6_first_real_density_input",
            "quantity": "first rho_H/rho_eff profile row",
            "definition": "source-backed density profile, profile theorem-zero certificate, or finite bound for sigma_shadow_perp",
            "units": "mass_density_or_dimensionless_bound",
            "source_requirement": "source path, extraction method, worldtube, observer/frame, and validity flag",
            "formula_or_transfer": "must feed EP4376_2 through EP4376_5 before any local score",
            "current_status": "NOT_FILLED_THIS_CHECKPOINT",
            "valid_for_claim": "False",
        },
    ]


def noether_exchange_test_rows() -> List[Dict[str, str]]:
    return [
        {
            "test_id": "NET4376_0_inside_action_graph",
            "object_tested": "relative weights inside ordinary matter action graph",
            "mathematical_result": "0=sum_i w_i C_i^nu and live edge C_ij != 0 imply w_i=w_j along that edge",
            "kills_shadow": "False",
            "reason": "this acts only on currents/sectors present in the same Noether exchange graph",
            "status": "DERIVED_CONDITIONAL_COLLAPSE",
            "valid_for_claim": "False",
        },
        {
            "test_id": "NET4376_1_source_shadow_bypass",
            "object_tested": "separate source-only functional absent from matter dynamics",
            "mathematical_result": "S_shadow can be separately conserved or zero-monopole without appearing in the exchange equations",
            "kills_shadow": "False",
            "reason": "Noether exchange has no edge to a functional outside S_matter unless parent grammar puts it inside",
            "status": "BYPASS_SURVIVES",
            "valid_for_claim": "False",
        },
        {
            "test_id": "NET4376_2_topological_wrong_distribution",
            "object_tested": "closed/topological representative with correct total charge",
            "mathematical_result": "dJ_top=0 and equal surface charge do not force J_top density equal to T_H(n,n)/c^2",
            "kills_shadow": "False",
            "reason": "conservation/topology fixes charge class, not the local density profile",
            "status": "DISTRIBUTIONAL_EQUALITY_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "test_id": "NET4376_3_result",
            "object_tested": "source-shadow ban by Bianchi/Noether alone",
            "mathematical_result": "Noether exchange narrows source weights but does not prove no source-shadow density",
            "kills_shadow": "False",
            "reason": "the missing theorem is parent grammar/distributional equality, not another exchange identity",
            "status": "NOETHER_NOT_ENOUGH",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4376_0_source_shadow_zero",
            "claim_tested": "rho_shadow=0",
            "required_inputs": "same-action Hilbert derivative plus parent-signed no source-only functional/no non-Hilbert current/no hidden Hom",
            "status": "BLOCKED_PARENT_GRAMMAR_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4376_1_topological_profile_zero",
            "claim_tested": "topological representative preserves Hilbert density profile",
            "required_inputs": "distributional equality J_top=J_H+dB_zero_profile, not total charge equality only",
            "status": "BLOCKED_DISTRIBUTIONAL_EQUALITY_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4376_2_Eprofile_bound",
            "claim_tested": "finite E_profile source-shadow/profile pass",
            "required_inputs": "rho_H/rho_eff profile or bound for sigma_shadow_perp plus K_N(s) and arena delta_N",
            "status": "BOUND_SCHEMA_READY_INPUTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4376_3_local_GR",
            "claim_tested": "local GR/Newton/PPN/clock/orbital pass",
            "required_inputs": "E_profile plus E_PiH, E_I, E_ref, E_tau, E_boundary, E_transition, E_readout and other E_perp components closed",
            "status": "FORBIDDEN_COMPONENTS_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4376_0",
            "decision": DECISION,
            "summary": (
                "4376 proves the useful negative/positive split. A same-action Hilbert derivative plus typed no-source-shadow grammar would set rho_shadow=0 and E_profile=0, "
                "but Bianchi/Noether exchange alone only collapses weights inside the ordinary action graph and cannot kill a separate source-only functional or a topological wrong-distribution representative. "
                "Therefore the current branch remains nonclaim and the first E_profile source-density row is staged around sigma_shadow_perp, its Green transfer, and the K_N score gate."
            ),
            "next_target": NEXT_TARGET,
            "why_next": "the remaining leap is parent grammar/distributional equality, not another total-mass or Noether exchange argument.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4376_0_conditional_shadow_zero",
            "object": "source-shadow ban",
            "status": "CONDITIONAL_THEOREM_ASSEMBLED",
            "note": "exact if parent grammar excludes source-only functionals and non-Hilbert currents.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4376_1_Noether_limit",
            "object": "Bianchi/Noether exchange route",
            "status": "LIMIT_PROVED",
            "note": "collapses live exchange weights but cannot silence a separate source-shadow functional.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4376_2_topological_profile",
            "object": "topological wrong-distribution branch",
            "status": "RETAINED",
            "note": "needs distributional equality, not surface charge equality.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4376_3_Eprofile_source_row",
            "object": "sigma_shadow_perp source row",
            "status": "STAGED_NONCLAIM",
            "note": "definition and Green/K_N transfer are ready; source profile/value is missing.",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT4376_4_next",
            "object": "next derivation",
            "status": "PARENT_GRAMMAR_OR_PROFILE_EQUALITY_NEXT",
            "note": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4376_0",
            "target": NEXT_TARGET,
            "question": "Can the parent ordinary-source grammar forbid source-shadow functionals, or can the topological/Hamiltonian source be proved distributionally equal to Hilbert T00?",
            "preferred_route": "derive the action-domain theorem: allowed ordinary source object is only the Hilbert derivative on Q_obs with fixed representation data; no source-only functional/current slot exists.",
            "fallback_route": "source or bound sigma_shadow_perp/rho_eff-rho_H as a real same-worldtube density-profile row and score it through Green/K_N.",
            "avoid": "using Noether exchange, total charge equality, fitted GM, or Poynting-background language as a profile proof.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    shadow_attempts: List[Dict[str, str]],
    grammar: List[Dict[str, str]],
    eprofile: List[Dict[str, str]],
    noether: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: source-shadow ban or E_profile first source density row

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4376 goes straight at the countermodel left by 4375.

The clean zero route is sharp:

```text
same-action Hilbert source density
+ no source-only functional/current slot
+ no hidden/source-label Hom into ordinary source coefficients
+ variation before readout
+ topological representative equal to Hilbert T00 as a distribution
=> rho_shadow=0
=> rho_eff(y)=rho_H(y)
=> E_profile=0.
```

The important new result is also a warning: Noether/Bianchi exchange is not enough by itself. It collapses relative weights **inside** the ordinary action exchange graph, but a separate source-shadow density can bypass that graph unless the parent object language forbids it.

So the current corpus cannot claim the ban. The honest nonzero row is:

```text
sigma_shadow_perp := rho_shadow/rho_H - <rho_shadow/rho_H>_rho,
E_shadow := ||sigma_shadow_perp||_inf,
deltaPhi_shadow(x) = -G_cal int_W rho_H(y) sigma_shadow_perp(y)/|x-y| dV_y,
|deltaa_shadow|/|a_N| <= K_N(s) E_shadow.
```

This does not prove local GR. It creates the first explicit `E_profile` source-density row and identifies the next proof target: parent grammar/no-source-shadow or distributional Hilbert/topological profile equality.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Source-Shadow Ban Attempt

{md_table(shadow_attempts, ["attempt_id", "claim_piece", "formal_statement", "derivation_result", "what_it_proves", "current_blocker", "parent_signed"])}

## Grammar Clauses

{md_table(grammar, ["clause_id", "required_clause", "mathematical_form", "status", "effect_if_signed", "failure_mode"])}

## E_profile First Source Rows

{md_table(eprofile, ["row_id", "quantity", "definition", "units", "source_requirement", "formula_or_transfer", "current_status"])}

## Noether Exchange Test

{md_table(noether, ["test_id", "object_tested", "mathematical_result", "kills_shadow", "reason", "status"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4376: source-shadow ban or E_profile first source density row

Marker: `{MARKER}`

## What changed

- Assembled the conditional zero theorem: same-action Hilbert source plus no source-shadow grammar implies `rho_shadow=0`.
- Proved the Noether limitation: exchange collapse does not kill a source-only functional outside the action graph.
- Retained the topological wrong-distribution countermodel until distributional Hilbert equality is proved.
- Staged the first nonclaim `E_profile` source row: `sigma_shadow_perp`, Green transfer, and `K_N(s)` score gate.

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "why_next"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "fallback_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4376 Transition source-shadow ban or E_profile source row

Marker: `{MARKER}`

4376 proves the useful split. If the parent source grammar says the only active bulk source density is the same Hilbert derivative `T_H(n,n)/c^2`, with no source-only functional, no non-Hilbert current, no hidden/source-label Hom, and no post-readout profile selector, then:

```text
rho_shadow=0 => rho_eff(y)=rho_H(y) => E_profile=0.
```

But Noether exchange alone cannot do that job. It collapses weights on live ordinary action exchange edges; it does not touch a separate source-only functional outside the exchange graph. The finite row is therefore:

```text
sigma_shadow_perp := rho_shadow/rho_H - <rho_shadow/rho_H>_rho,
deltaPhi_shadow = -G_cal int_W rho_H sigma_shadow_perp/|x-y| dV,
|deltaa_shadow|/|a_N| <= K_N(s) E_shadow.
```

Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4376 packet update: source-shadow ban not yet parent-signed

Marker: `{PACKET_MARKER}`

Packet update: the local source-profile route has reached the exact fork. The zero branch needs a parent grammar theorem forbidding source-only density/current slots, plus distributional equality between any topological/Hamiltonian representative and Hilbert `T_H(n,n)/c^2`. Noether exchange is useful but insufficient because it only acts inside the ordinary action graph. Until that parent signature exists, the packet carries `sigma_shadow_perp` as the first explicit `E_profile` source-density row with the Green/K_N score gate.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4376 assembles the conditional source-shadow zero theorem: same-action Hilbert density plus no source-only functional/current slot, no hidden/source-label Hom, variation before readout, and distributional topological/Hilbert equality imply rho_shadow=0 and E_profile=0. "
                "It also proves the Noether limitation: Bianchi/Noether exchange collapses weights only inside live ordinary action exchange edges and cannot kill a separate source-only functional absent from the matter dynamics. "
                "Because the parent grammar and distributional equality are unsigned, the checkpoint stages the first nonclaim E_profile source-density row sigma_shadow_perp with Green transfer and K_N scoring. No local-GR/Newton/PPN/clock/orbital claim fires."
            ),
            "4376 source register, source-shadow ban attempt rows, grammar clauses, E_profile first source rows, Noether exchange test, claim gates, decision, status, next target and validation CSV.",
            "source_shadow_ban_conditional_Noether_limit_proved_Eprofile_source_row_staged_nonclaim",
            "Derive the parent grammar no-source-shadow theorem or distributional topological/Hilbert profile equality, otherwise fill real same-worldtube density profile rows for sigma_shadow_perp.",
            "Using Noether exchange, total charge equality, fitted GM, or Poynting-background language as a density-profile proof.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4376_SOURCE_REGISTER.csv")
    shadow_attempts = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4376_SHADOW_BAN_ATTEMPT.csv")
    grammar = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4376_GRAMMAR_CLAUSES.csv")
    eprofile = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4376_EPROFILE_FIRST_SOURCE_ROW.csv")
    noether = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4376_NOETHER_EXCHANGE_TEST.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4376_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4376_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited local source exists")
    add("VAL4376_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited local source needle resolves")
    add(
        "VAL4376_2_conditional_zero_theorem",
        any(row["attempt_id"] == "SBA4376_1_same_action_Hilbert_filter" and "rho_shadow=0" in row["what_it_proves"] for row in shadow_attempts),
        "same-action Hilbert source filter zero route exists",
    )
    add(
        "VAL4376_3_noether_limit",
        any(row["test_id"] == "NET4376_1_source_shadow_bypass" and row["kills_shadow"] == "False" for row in noether),
        "Noether exchange limitation against source-shadow bypass is recorded",
    )
    add(
        "VAL4376_4_topological_gate",
        any(row["clause_id"] == "GR4376_6_topological_distributional_equality" and "OPEN" in row["status"] for row in grammar),
        "topological wrong-distribution gate remains open",
    )
    add(
        "VAL4376_5_sigma_row",
        any(row["row_id"] == "EP4376_2_sigma_shadow_perp" and "sigma_shadow_perp" in row["definition"] for row in eprofile),
        "sigma_shadow_perp source row exists",
    )
    add(
        "VAL4376_6_green_and_kn",
        any("deltaPhi_shadow" in row["formula_or_transfer"] for row in eprofile)
        and any("K_N(s)" in row["formula_or_transfer"] for row in eprofile),
        "Green transfer and K_N gate exist",
    )
    add("VAL4376_7_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4376_8_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4376_9_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4376_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4376_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4376_12_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4376_13_no_claim_rows",
        all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path))
        and all(row.get("claim_allowed", "False") == "False" for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add("VAL4376_14_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    return validations


def main() -> None:
    sources = source_register_rows()
    shadow_attempts = shadow_ban_attempt_rows()
    grammar = grammar_clause_rows()
    eprofile = eprofile_source_rows()
    noether = noether_exchange_test_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4376_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4376_SHADOW_BAN_ATTEMPT.csv": shadow_attempts,
        "P8_Y5_R2FR_4376_GRAMMAR_CLAUSES.csv": grammar,
        "P8_Y5_R2FR_4376_EPROFILE_FIRST_SOURCE_ROW.csv": eprofile,
        "P8_Y5_R2FR_4376_NOETHER_EXCHANGE_TEST.csv": noether,
        "P8_Y5_R2FR_4376_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4376_DECISION.csv": decisions,
        "P8_Y5_R2FR_4376_STATUS.csv": statuses,
        "P8_Y5_R2FR_4376_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, shadow_attempts, grammar, eprofile, noether, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
