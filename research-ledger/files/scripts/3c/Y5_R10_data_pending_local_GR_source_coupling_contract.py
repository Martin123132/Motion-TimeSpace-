from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1229"
TITLE = "1229-Y5-R10-data-pending-local-GR-source-coupling-contract"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
THEOREM_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
CLAUSE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv"
COUNTEREXAMPLE_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv"
FINITE_RESIDUAL_PATH = OUT_DIR / f"{PACK_ID}_FINITE_SOURCE_RESIDUAL_CONTRACT.csv"
DATA_PENDING_PATH = OUT_DIR / f"{PACK_ID}_DATA_PENDING_BRIDGE.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1229_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1229_0_1228_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1228_NEXT_TARGET.csv",
            "needle": "NEXT1228_0_1229",
            "purpose": "1228 handoff to analytic local-GR source-coupling contract while data is pending",
        },
        {
            "source_id": "SRC1229_1_1224_owner_clauses",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv",
            "needle": "OWN1224_0_single_action_scale",
            "purpose": "source-weight owner proof clauses that did not close",
        },
        {
            "source_id": "SRC1229_2_1224_obstructions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1224_0_wA_action_multiplier",
            "purpose": "active source-coupling counterexamples",
        },
        {
            "source_id": "SRC1229_3_1224_product",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv",
            "needle": "PROD1224_0_source_weight",
            "purpose": "finite source-weight product law",
        },
        {
            "source_id": "SRC1229_4_1225_tau_formula",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
            "needle": "FORM1225_0_tau_WEP_functional",
            "purpose": "symbolic tau_WEP projection that remains data-pending",
        },
        {
            "source_id": "SRC1229_5_1066_source_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_2_variation_before_readout",
            "purpose": "conditional route for excluding inert source-only scalars",
        },
        {
            "source_id": "SRC1229_6_1066_measure_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
            "needle": "FMQ1066_4_verdict",
            "purpose": "action-scale and field-measure normalization obstruction",
        },
        {
            "source_id": "SRC1229_7_1055_parent_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_4_source_label_forgetting",
            "purpose": "candidate parent action source-label forgetting clause",
        },
        {
            "source_id": "SRC1229_8_1055_adoption",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
            "needle": "ADG1055_3_source_label_forgetting",
            "purpose": "source-label forgetting adoption gate",
        },
        {
            "source_id": "SRC1229_9_1084_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle": "RIG1084_0_CMSM_arrays",
            "purpose": "official MICROSCOPE readout arrays remain absent",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    theorem_contract = [
        {
            "theorem_id": "THM1229_0_target",
            "name": "local-GR universal source coupling target",
            "formal_statement": "If S_matter descends to c_* Sbar_m[g_eff,Psi,theta] with species labels entering only through fields/representations and not through independent action scales, then delta S_matter/delta g_eff gives T_eff=c_* sum_A T_A; c_* is absorbed into G_N and the Newton/GR source side is universal.",
            "derivation_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "required_missing_clauses": "CLC1229_0;CLC1229_1;CLC1229_2;CLC1229_4;CLC1229_5;CLC1229_6",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv", "OWN1224_0_single_action_scale"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1229_1_iff",
            "name": "universal coupling iff condition",
            "formal_statement": "The local GR/Newton source limit is clean iff every ordinary-matter source multiplier w_A is either quotient-equivalent to one common w_* or lies in the null kernel of every local source, boundary, and readout projection used by WEP/PPN/clock/orbital arenas.",
            "derivation_status": "EXACT_CONTRACT_WRITTEN_NOT_PROVED",
            "required_missing_clauses": "quotient-equivalence proof or null-projection proof for all arenas",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_1_Hilbert_source_rescaling"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1229_2_countermodel",
            "name": "finite countermodel if source multipliers survive",
            "formal_statement": "For S_matter=sum_A (1+epsilon_A) S_A, isolated classical Euler-Lagrange equations can look unchanged while the Hilbert source is T_eff=sum_A (1+epsilon_A)T_A. Therefore epsilon_A is not removable unless the parent quotient/action-scale/measure proof identifies it as gauge.",
            "derivation_status": "OBSTRUCTION_ACTIVE",
            "required_missing_clauses": "single action scale; species-blind measure; source-label forgetting",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv", "OBS1224_0_wA_action_multiplier"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1229_3_residual_vector",
            "name": "local source residual vector",
            "formal_statement": "If delta w_A survives, the local residual source vector is q_source^nu=P_loc nabla_mu[sum_A delta w_A T_A^{mu nu}] plus boundary/projector/readout terms. Local GR requires q_source^nu=0 as a theorem or finite products below arena bounds.",
            "derivation_status": "RESIDUAL_CONTRACT_DERIVED_SYMBOLIC_ONLY",
            "required_missing_clauses": "parent Noether identity; boundary silence; numeric arena projections",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv", "FORM1225_1_source_weight_product"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    clause_audit = [
        {
            "clause_id": "CLC1229_0_single_action_scale",
            "required_clause": "one universal parent action scale, hbar, and normalization for all ordinary matter sectors",
            "why_needed": "otherwise w_A S_A rescales Hilbert source strength without necessarily changing isolated classical motion",
            "current_status": "UNSIGNED_PARENT_OWNER",
            "if_closed": "Delta_w source-normalization branch collapses to theorem-zero",
            "if_open": "finite Delta_w prior or data bound remains mandatory",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_4_verdict"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_1_connected_matter_category",
            "required_clause": "ordinary matter objects must be connected enough that a natural positive source scalar is constant",
            "why_needed": "disconnected/simple species components can carry independent natural constants",
            "current_status": "CONDITIONAL_NOT_DERIVED",
            "if_closed": "naturality forces common w_* across ordinary matter",
            "if_open": "species family w_A remains a legal countermodel",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_3_naturality_route"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_2_no_inert_source_scalars",
            "required_clause": "parent object language excludes source-only scalars with no observable, gauge, representation, or geometry type",
            "why_needed": "an inert source scalar can change active gravity while hiding from non-gravitational equations",
            "current_status": "CONDITIONAL_TYPING_LEMMA",
            "if_closed": "source-only w_A parameters become inadmissible parent arguments",
            "if_open": "source-only scalar route remains open",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_0_target"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_3_variation_before_readout",
            "required_clause": "Hilbert source current is varied before detector/readout/projector reduction",
            "why_needed": "post-variation readout selectors must not create species-source weights",
            "current_status": "HELPFUL_BUT_READOUT_UNSIGNED",
            "if_closed": "detector algebra cannot fake a source coupling difference",
            "if_open": "readout weighting can reintroduce an effective tau_WEP source factor",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_2_variation_before_readout"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_4_measure_coframe_connection_descent",
            "required_clause": "measure, coframe, connection, and quotient descent are species-blind up to the same common factor",
            "why_needed": "species-dependent Jacobians or frame descent can mimic w_A even if the bare action is common",
            "current_status": "UNSIGNED_DESCENT",
            "if_closed": "hidden geometric descent cannot reopen source labels",
            "if_open": "measure/coframe residual remains a local-GR obstruction",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv", "FMQ1066_3_measure_jacobian"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_5_boundary_projection_silence",
            "required_clause": "boundary terms and local projection maps do not carry representative/species coefficients",
            "why_needed": "a bulk theorem-zero can be spoiled by boundary or projection leakage in local arenas",
            "current_status": "UNSIGNED_BOUNDARY_LOCAL_PROJECTION",
            "if_closed": "bulk universal source coupling survives local projection",
            "if_open": "q_source^nu includes boundary/projector terms",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv", "FORM1225_0_tau_WEP_functional"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_6_noether_bianchi_closure",
            "required_clause": "parent diffeomorphism/Noether identity descends to nabla_mu T_eff^{mu nu}=0 in the observed local frame",
            "why_needed": "GR limit needs compatibility with Bianchi; nonconserved source residual must be exchanged with an explicit field sector",
            "current_status": "CONTRACT_WRITTEN_NOT_PROVED",
            "if_closed": "source residual vector is forced to zero or assigned to a derived exchange current",
            "if_open": "local GR pass remains blocked by conservation/covariance gap",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv", "OWN1224_1_universal_current_owner"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_7_single_GN_normalization",
            "required_clause": "only one common source factor may be absorbed into measured G_N",
            "why_needed": "measured-G absorption cannot hide composition-dependent source weights",
            "current_status": "GUARD_ACTIVE",
            "if_closed": "common c_* is harmless and GR/Newton normalization is clean",
            "if_open": "source-body calibration can mask but not remove WEP/PPN residuals",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv", "SCG1083_3_no_measured_G_absorption"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CLC1229_8_verdict",
            "required_clause": "all universal source-coupling clauses close together",
            "why_needed": "local GR/Newton reduction is only as strong as its weakest source-coupling clause",
            "current_status": "NOT_CLOSED",
            "if_closed": "move to disformal/current residual cleanup",
            "if_open": "continue action-scale/measure-owner proof or finite Delta_w sourcing",
            "source": "CLC1229_0 through CLC1229_7",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    counterexamples = [
        {
            "counterexample_id": "CEX1229_0_action_multiplier",
            "construction": "S_matter=sum_A w_A S_A with constant w_A",
            "what_it_preserves": "isolated classical Euler-Lagrange equation form for each species",
            "what_it_breaks": "universal Hilbert source normalization and source side of GR/Newton",
            "defeated_by": "CLC1229_0;CLC1229_2;CLC1229_6",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CEX1229_1_species_action_scale",
            "construction": "species-dependent effective hbar or path-integral action scale",
            "what_it_preserves": "classical-looking local dynamics in a narrow limit",
            "what_it_breaks": "quantum/statistical normalization and stress-source weighting",
            "defeated_by": "CLC1229_0",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CEX1229_2_measure_jacobian",
            "construction": "species-dependent field measure, coframe, or quotient Jacobian",
            "what_it_preserves": "bare parent action syntax",
            "what_it_breaks": "effective descended source normalization",
            "defeated_by": "CLC1229_4",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CEX1229_3_readout_reweighting",
            "construction": "detector/source projection applies species-weighted kernel after variation",
            "what_it_preserves": "bulk universal source equation",
            "what_it_breaks": "reported WEP/clock/orbital arena residual",
            "defeated_by": "CLC1229_3;CLC1229_5",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CEX1229_4_disconnected_species",
            "construction": "ordinary matter category has disconnected simple components with independent natural constants",
            "what_it_preserves": "naturality inside each component",
            "what_it_breaks": "cross-species universality",
            "defeated_by": "CLC1229_1;CLC1229_2",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_residual = [
        {
            "residual_id": "FR1229_0_delta_w",
            "quantity": "delta w_A := w_A-w_ref",
            "contract": "dimensionless species/source residual after removing one common G_N-absorbable factor",
            "arena": "all local source-coupling tests",
            "current_status": "MISSING_NUMERIC_PRIOR_OR_THEOREM_ZERO",
            "required_to_score": "parent action-scale theorem or sourced finite prior width",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FR1229_1_Tres",
            "quantity": "T_res^{mu nu}=sum_A delta w_A T_A^{mu nu}",
            "contract": "source-side stress residual that must vanish, be exchanged with a derived field current, or be bounded",
            "arena": "GR/Newton/PPN",
            "current_status": "SYMBOLIC_ONLY",
            "required_to_score": "source composition/profile and parent operator basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FR1229_2_qsource",
            "quantity": "q_source^nu=P_loc nabla_mu T_res^{mu nu}+boundary/projector terms",
            "contract": "local conservation/covariance residual vector",
            "arena": "local GR branch",
            "current_status": "DERIVED_AS_REQUIRED_OBJECT_NOT_ZERO",
            "required_to_score": "Noether descent, boundary silence, arena projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FR1229_3_WEP_product",
            "quantity": "abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15",
            "contract": "MICROSCOPE source-weight product bound if theorem-zero fails",
            "arena": "WEP/R10",
            "current_status": "NOT_SCOREABLE_DATA_PENDING",
            "required_to_score": "Delta_w_TiPt numeric prior; tau_WEP official projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FR1229_4_PPN_product",
            "quantity": "abs(delta w_source*tau_PPN) <= B_PPN",
            "contract": "PPN/local metric residual product, to be filled only with sourced arena projection",
            "arena": "PPN",
            "current_status": "PLACEHOLDER_CONTRACT_ONLY",
            "required_to_score": "tau_PPN projection; PPN bound source; local metric map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FR1229_5_clock_orbital_product",
            "quantity": "abs(delta w_source*tau_clock_or_orbital) <= B_clock_or_orbital",
            "contract": "clock/orbital source-coupling residual product",
            "arena": "clocks/orbital",
            "current_status": "PLACEHOLDER_CONTRACT_ONLY",
            "required_to_score": "arena kernel; source profile; published bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    data_pending = [
        {
            "bridge_id": "DATA1229_0_MICROSCOPE_pending",
            "data_branch_status": "READY_EMPTY_OR_WAITING",
            "analytic_branch_action": "continue parent source-coupling derivation",
            "forbidden_shortcut": "do not set tau_WEP to one or use surrogate arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "DATA1229_1_tau_feed",
            "data_branch_status": "SYMBOLIC_ONLY_NONCLAIM",
            "analytic_branch_action": "keep tau_WEP as projection object for finite branch",
            "forbidden_shortcut": "do not claim WEP/local-GR without official files and parent inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "DATA1229_2_GR_reduction",
            "data_branch_status": "NOT_REQUIRED_FOR_PURE_THEOREM_ATTEMPT",
            "analytic_branch_action": "prove universal source coupling from parent action or retain finite residual law",
            "forbidden_shortcut": "do not absorb composition-dependent residuals into measured G_N",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_update = [
        {
            "feed_id": "FEED1229_0_to_PROD1224",
            "target": "PROD1224_0_source_weight",
            "update": "finite residual product law retained; no numeric scoring promoted",
            "new_claim_rows": 0,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "feed_id": "FEED1229_1_to_FORM1225",
            "target": "FORM1225_0_tau_WEP_functional",
            "update": "data-pending tau_WEP remains official-file-gated",
            "new_claim_rows": 0,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "feed_id": "FEED1229_2_to_1230",
            "target": "universal action-scale/measure owner theorem",
            "update": "next derivation must close CLC1229_0 and CLC1229_4 or source finite Delta_w prior",
            "new_claim_rows": 0,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1229_0_no_local_GR_pass",
            "decision": "do not claim local GR/Newton source-coupling pass",
            "because": "universal action scale, source scalar exclusion, measure descent, boundary silence, and Noether/Bianchi closure are not parent-signed",
            "next_action": "attack action-scale/measure owner theorem before trying to score local-GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1229_1_keep_derivation_first",
            "decision": "try to prove source universality before relying on MICROSCOPE finite scoring",
            "because": "a theorem-zero would be cleaner and closer to GR reducing to Newton than a data patch",
            "next_action": "derive common action normalization from parent quotient/object language",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1229_2_keep_finite_backstop",
            "decision": "retain finite residual product branch if proof fails",
            "because": "active counterexamples are explicit and must be bounded rather than waved away",
            "next_action": "source Delta_w and tau arena projections only after derivation route stalls",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1229_0_theorem_zero",
            "claim": "Delta_w theorem-zero from parent source coupling",
            "status": "BLOCKED",
            "reason": "CLC1229_0 through CLC1229_6 not all closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1229_1_WEP",
            "claim": "MICROSCOPE/WEP source-weight pass",
            "status": "BLOCKED",
            "reason": "Delta_w and tau_WEP are not numeric/sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1229_2_PPN",
            "claim": "PPN/local metric pass",
            "status": "BLOCKED",
            "reason": "tau_PPN and source residual map are placeholders only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1229_3_local_GR",
            "claim": "local GR/Newton derivable reduction",
            "status": "BLOCKED",
            "reason": "universal source coupling is a written contract, not a parent-signed theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1229_4_public_claim",
            "claim": "public local-GR/source-coupling claim",
            "status": "BLOCKED",
            "reason": "1229 is an internal derivation gate only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1229_0_1230",
            "target_file": "1230-Y5-R10-universal-action-scale-measure-owner-theorem-or-finite-delta-w-prior.md",
            "target_script": "scripts/Y5_R10_universal_action_scale_measure_owner_theorem_or_finite_delta_w_prior.py",
            "task": "attack the source-coupling root: prove a universal parent action-scale/measure owner for ordinary matter, or produce a strict nonclaim finite Delta_w prior-source contract",
            "success_condition": "either CLC1229_0 and CLC1229_4 close as parent-signed clauses, or the finite source-weight branch gains exact sourced inputs needed for future scoring",
            "do_not_do": "do not claim local GR/WEP/PPN, do not absorb species residuals into measured G_N, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        THEOREM_CONTRACT_PATH,
        CLAUSE_AUDIT_PATH,
        COUNTEREXAMPLE_PATH,
        FINITE_RESIDUAL_PATH,
        DATA_PENDING_PATH,
        FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(THEOREM_CONTRACT_PATH, theorem_contract)
    write_csv(CLAUSE_AUDIT_PATH, clause_audit)
    write_csv(COUNTEREXAMPLE_PATH, counterexamples)
    write_csv(FINITE_RESIDUAL_PATH, finite_residual)
    write_csv(DATA_PENDING_PATH, data_pending)
    write_csv(FEED_PATH, feed_update)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            theorem_contract,
            clause_audit,
            counterexamples,
            finite_residual,
            data_pending,
            feed_update,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    theorem_not_promoted = all(is_false(row, "valid_for_claim") for row in theorem_contract) and any(
        "NOT_PARENT_SIGNED" in row["derivation_status"] or "OBSTRUCTION" in row["derivation_status"]
        for row in theorem_contract
    )
    verdict_blocked = any(row["clause_id"] == "CLC1229_8_verdict" and row["current_status"] == "NOT_CLOSED" for row in clause_audit)
    active_counterexamples = len([row for row in counterexamples if row["status"] == "ACTIVE"])
    finite_branch_present = any(row["residual_id"] == "FR1229_3_WEP_product" for row in finite_residual)
    data_branch_parked = any(row["bridge_id"] == "DATA1229_0_MICROSCOPE_pending" for row in data_pending)
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1230 = next_target[0]["target_file"].startswith("1230-Y5-R10-universal-action-scale-measure-owner")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1229_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1229_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1229_2_theorem_not_promoted",
            "source-coupling theorem remains conditional",
            theorem_not_promoted,
            "contracts written but not parent-signed",
        ),
        validation_row(
            "VAL1229_3_verdict_blocked",
            "universal source-coupling verdict remains blocked",
            verdict_blocked,
            "CLC1229_8_verdict=NOT_CLOSED",
        ),
        validation_row(
            "VAL1229_4_counterexamples_active",
            "active counterexamples are explicit",
            active_counterexamples >= 4,
            f"active_counterexamples={active_counterexamples}",
        ),
        validation_row(
            "VAL1229_5_finite_branch_present",
            "finite residual branch retained",
            finite_branch_present,
            "FR1229_3_WEP_product present",
        ),
        validation_row(
            "VAL1229_6_data_branch_parked",
            "MICROSCOPE data branch remains parked and nonclaim",
            data_branch_parked,
            "DATA1229_0_MICROSCOPE_pending present",
        ),
        validation_row(
            "VAL1229_7_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1229_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1229_9_next_target_1230",
            "next target attacks action-scale/measure owner",
            next_is_1230,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1229_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1229_11_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1229_12_overall",
            "overall 1229 validation",
            all(row["status"] == "PASS" for row in validation),
            "1229 sharpens universal source-coupling into exact theorem clauses and finite residual fallback without claims",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1229 does **not** claim local GR/Newton source-coupling closure. It writes the exact contract: either all species source multipliers are parent-identified with one common action/measure normalization, or a finite residual vector must be bounded in WEP/PPN/clock/orbital arenas.",
        "",
        "**Main progress:** the missing coupling is no longer vague. The root object is `delta w_A`; it either becomes theorem-zero via parent action-scale/measure/source-label clauses, or it enters `q_source^nu=P_loc nabla_mu[sum_A delta w_A T_A^{mu nu}]` and the WEP product `abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15`.",
        "",
        "**Data stance:** MICROSCOPE/CMSM files remain pending from 1228. No surrogate arrays, unity `tau_WEP`, measured-G absorption, WEP pass, PPN pass, or local-GR pass is allowed here.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Local-GR Source-Coupling Theorem Contract",
        markdown_table(theorem_contract, list(theorem_contract[0].keys())),
        "",
        "## Universal Source-Coupling Clause Audit",
        markdown_table(clause_audit, list(clause_audit[0].keys())),
        "",
        "## Source-Coupling Counterexample Ledger",
        markdown_table(counterexamples, list(counterexamples[0].keys())),
        "",
        "## Finite Source Residual Contract",
        markdown_table(finite_residual, list(finite_residual[0].keys())),
        "",
        "## Data-Pending Bridge",
        markdown_table(data_pending, list(data_pending[0].keys())),
        "",
        "## Runner Feed Update",
        markdown_table(feed_update, list(feed_update[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
