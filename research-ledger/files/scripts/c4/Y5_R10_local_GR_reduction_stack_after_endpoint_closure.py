from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "868-Y5-R10-local-GR-reduction-stack-after-endpoint-closure.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_868_SOURCE_REGISTER.csv"
REDUCTION_CHAIN_PATH = RESIDUALS / "P8_Y5_R10_868_LOCAL_GR_REDUCTION_CHAIN.csv"
BLOCKER_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_868_LOCAL_GR_BLOCKER_AUDIT.csv"
QLOC_DECOMPOSITION_PATH = RESIDUALS / "P8_Y5_R10_868_QLOC_DECOMPOSITION_CONTRACT.csv"
NEWTON_SOURCE_PATH = RESIDUALS / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv"
PPN_VECTOR_PATH = RESIDUALS / "P8_Y5_R10_868_PPN_VECTOR_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_868_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_868_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_868_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_868_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_868_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_868_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_867_VALIDATION.csv"

STATUS = "Y5_R10_868_local_GR_Newton_reduction_stack_rebuilt_after_endpoint_closure_nonclaim"
CLAIM_CEILING = "local_GR_reduction_chain_only_no_EH_no_q_loc_no_Newton_no_PPN_claim"
NEXT_TARGET = "869-Y5-R10-q_loc-residual-vector-decomposition-or-zero-theorem.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    REDUCTION_CHAIN_PATH,
    BLOCKER_AUDIT_PATH,
    QLOC_DECOMPOSITION_PATH,
    NEWTON_SOURCE_PATH,
    PPN_VECTOR_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "867_doc",
        "path": POST_CHECKPOINT / "867-Y5-R10-boundary-orientation-charge-metric-last-derivation-gate.md",
        "needles": [
            "endpoint branch now has a useful no-go",
            "LG867_0_return_to_local_GR_stack",
            "868-Y5-R10-local-GR-reduction-stack-after-endpoint-closure.md",
        ],
        "role": "endpoint closure freeze and local GR return handoff",
    },
    {
        "source_id": "867_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V867_8_local_GR_return_ready,pass",
            "V867_11_all_rows_nonclaim,pass",
            "V867_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "860_GR_contract",
        "path": POST_CHECKPOINT / "860-Y5-R10-parent-amplitude-law-and-GR-limit-derivation-contract.md",
        "needles": [
            "LG860_0_one_metric",
            "LG860_2_q_loc_suppression",
            "LG860_3_Newton_source",
        ],
        "role": "recent local GR/Newton gate stack",
    },
    {
        "source_id": "863_trace_zero",
        "path": POST_CHECKPOINT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needles": [
            "WTC863_4_local_projection_silence",
            "CZT863_0_chain_rule_zero",
            "LRF863_0_zero_branch",
        ],
        "role": "local projection silence and chain-rule zero theorem",
    },
    {
        "source_id": "864_quotient_split",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "PC864_0_parent_domains",
            "LGS864_0_conditional_split_lemma",
            "GN864_0_if_split_signed",
        ],
        "role": "local/global quotient split sufficient clause",
    },
    {
        "source_id": "347_local_GR_attempt",
        "path": POST_CHECKPOINT / "347-local-GR-parent-reduction-theorem-attempt.md",
        "needles": [
            "conditional_GR_reduction_only_no_local_GR_or_PPN_claim",
            "metric variation owned by parent",
            "`N5` projector stress cleared",
        ],
        "role": "older local GR conditional theorem and hard blocker",
    },
    {
        "source_id": "393_Newton_source",
        "path": POST_CHECKPOINT / "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "needles": [
            "G_eff = kappa_eff c^4/(8 pi)",
            "constant universal",
            "Newtonian/local-GR promoted",
        ],
        "role": "source-normalized Newtonian limit blocker",
    },
    {
        "source_id": "179_PPN_silence",
        "path": POST_CHECKPOINT / "179-local-GR-PPN-silence-contract.md",
        "needles": [
            "q_loc^nu -> 0",
            "gamma = beta = 1",
            "screened effective, not derived",
        ],
        "role": "local PPN silence contract and q_loc blocker",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": spec["source_id"],
            "path": str(spec["path"]),
            "exists": str(spec["path"].exists()).lower(),
            "needle_check": check_needles(spec["path"], spec["needles"]),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for spec in SOURCE_SPECS
    ]


def reduction_chain_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "chain_id": "GR868_0_local_quotient_owner",
            "required_theorem": "parent action defines q_loc[U] as the local observable quotient for compact non-cosmological regions",
            "sufficient_form": "q_FLRW sees Q_trace while Dq_loc[U][v_T]=0 and local matter/coframes factor only through q_loc[U]",
            "if_proved": "trace/cosmology memory can be globally visible but locally silent",
            "current_status": "conditional_clause_written_not_parent_derived",
            "blocks": "P_loc J_trace, Pi_I^matter, q_loc^nu",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "GR868_1_one_metric_matter",
            "required_theorem": "ordinary matter, photons, clocks, and rulers couple to one local observed metric/coframe",
            "sufficient_form": "S_matter=Sbar_matter[Obs_loc(q_loc(Phi)),Psi] with no direct MTS species markers",
            "if_proved": "WEP, clock, and light-cone deviations vanish at the direct-coupling level",
            "current_status": "conditional_chain_rule_shape_only",
            "blocks": "composition forces, clock drift, nonmetric light cones",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "GR868_2_boundary_nohair",
            "required_theorem": "endpoint/boundary/exact currents have zero local projection",
            "sufficient_form": "P_loc J_trace=0 and no local shear, vector, clock, or range-dependent boundary component survives",
            "if_proved": "cosmological endpoint closure does not become local fifth-force hair",
            "current_status": "open",
            "blocks": "PPN/WEP/clock/orbital leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "GR868_3_projector_stress",
            "required_theorem": "N5/projector variation is zero, pure gauge, boundary-only conserved, or retained explicitly",
            "sufficient_form": "T_projector=0 locally or nabla_mu T_projector^{mu nu}=0 with no exterior PPN support",
            "if_proved": "no fake GR by silently dropping a stress term",
            "current_status": "open_hard",
            "blocks": "EH exterior, Bianchi safety, gamma/beta residuals",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "GR868_4_EH_operator_selection",
            "required_theorem": "local metric variation reduces to Einstein-Hilbert plus cosmological constant and harmless boundary terms",
            "sufficient_form": "E_MTS^{mu nu}->0 locally or is absorbed into conserved boundary/gauge terms",
            "if_proved": "local field equations become GR before weak-field expansion",
            "current_status": "not_derived",
            "blocks": "modified gravity operator, gravitational slip, PPN gamma/beta",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "GR868_5_Bianchi_conservation",
            "required_theorem": "total local stress ledger is conserved and no inserted force exchange survives",
            "sufficient_form": "nabla_mu E_total^{mu nu}=0 and q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})=0",
            "if_proved": "local matter follows geodesic/conserved GR dynamics rather than hidden exchange dynamics",
            "current_status": "open",
            "blocks": "fifth-force, local energy exchange, source drift",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "GR868_6_Newton_source_normalization",
            "required_theorem": "weak-field limit has constant universal measured GM",
            "sufficient_form": "nabla^2 Phi=4 pi G rho with G_eff M_eff=GM_measured and no range/time/species dependence",
            "if_proved": "GR reduction also gives Newtonian mechanics, not merely an EH-shaped equation",
            "current_status": "conditional_algebra_only",
            "blocks": "delta_G, Gdot/G, finite-range force, WEP source charge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "GR868_7_PPN_residual_vector",
            "required_theorem": "PPN and local residual vector is zero or explicitly bounded against baselines",
            "sufficient_form": "gamma-1=0, beta-1=0, alpha_clock=0, eta_WEP=0, Phi-Psi=0, q_loc^nu=0 through required order",
            "if_proved": "local GR/PPN claim becomes promotable after evidence checks",
            "current_status": "screened_effective_not_parent_derived",
            "blocks": "public local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def blocker_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BL868_0_not_endpoint_limited_now",
            "blocker": "endpoint DeltaR branch",
            "current_status": "frozen_as_closure",
            "why_it_matters": "prevents more root algebra from masquerading as GR derivation",
            "next_action": "keep endpoint closure private while local GR stack is attacked directly",
            "claim_impact": "no DeltaR prediction claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL868_1_quotient_not_parent_owned",
            "blocker": "q_FLRW/q_loc functors and v_T classification",
            "current_status": "sufficient contract only",
            "why_it_matters": "all clean local zero theorems depend on local verticality",
            "next_action": "derive from parent action or move to residual vector",
            "claim_impact": "no q_loc zero claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL868_2_projector_stress",
            "blocker": "N5/projector stress and Bianchi safety",
            "current_status": "open_hard",
            "why_it_matters": "dropping it would fake EH exterior",
            "next_action": "prove zero/boundary/gauge/conserved fate or retain residual",
            "claim_impact": "no EH/local GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL868_3_source_normalization",
            "blocker": "measured GM absorption",
            "current_status": "conditional algebra only",
            "why_it_matters": "EH shape alone is not Newtonian source normalization",
            "next_action": "derive constant universal G_eff M_eff or retain delta_G/Gdot/fifth-force rows",
            "claim_impact": "no Newtonian-limit claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qloc_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "term_id": "QL868_0_trace_endpoint_flux",
            "term": "P_loc J_trace",
            "zero_route": "local/global quotient split plus boundary no-hair",
            "if_nonzero": "trace endpoint fifth-force/clock/PPN leakage",
            "current_status": "conditional_zero_only",
            "next_test": "derive local verticality or quantify retained source projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "QL868_1_coframe_pullback",
            "term": "Pi_I^matter",
            "zero_route": "matter action descends through q_loc and observed coframe has no endpoint/projector derivative",
            "if_nonzero": "matter stress sources selector/projector equations",
            "current_status": "chain_rule_shape_not_parent_signed",
            "next_test": "prove no-marker matter descent or retain counterstress coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "QL868_2_projector_bulk_force",
            "term": "F_P_bulk or T_projector",
            "zero_route": "metric-independent projector or conserved boundary-only projector stress",
            "if_nonzero": "modified exterior metric and PPN residuals",
            "current_status": "open_hard",
            "next_test": "N5 projector variation fate audit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "QL868_3_source_exchange",
            "term": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "zero_route": "Bianchi-safe total stress with no local exchange channel",
            "if_nonzero": "local acceleration/source drift/fifth-force residual",
            "current_status": "open",
            "next_test": "derive exact cancellation or build finite coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def newton_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "source_id": "NS868_0_EH_to_Poisson",
            "condition": "EH local branch is available",
            "required_form": "G_eff=kappa_eff c^4/(8 pi); nabla^2 Phi=4 pi G_eff rho_eff",
            "current_status": "conditional_algebra_written",
            "failure_if_missing": "no Newtonian limit even if local metric equation resembles GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "NS868_1_measured_GM",
            "condition": "source charge is constant, universal, range-independent, and species-independent",
            "required_form": "mu_obs=G_eff M_eff + mu_extra = GM_measured with mu_extra=0 or constant monopole only",
            "current_status": "not_parent_derived",
            "failure_if_missing": "delta_G, Gdot/G, WEP, or fifth-force rows remain active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "source_id": "NS868_2_source_charge_universality",
            "condition": "all matter compositions source the same local metric with the same normalization",
            "required_form": "no species-dependent Pi_M, no hidden source marker constants",
            "current_status": "open",
            "failure_if_missing": "composition-dependent acceleration survives even with one coframe",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ppn_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "ppn_id": "PV868_0_gamma_minus_one",
            "observable": "gamma-1 / gravitational slip",
            "zero_condition": "EH exterior plus no anisotropic/projector/boundary stress",
            "current_status": "not_parent_derived",
            "next_action": "derive EH/projector/no-hair or retain gamma coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ppn_id": "PV868_1_beta_minus_one",
            "observable": "beta-1 / nonlinear source hair",
            "zero_condition": "source-normalized Newtonian limit with no nonlinear MTS exterior support",
            "current_status": "not_parent_derived",
            "next_action": "derive constant GM theorem or retain beta coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ppn_id": "PV868_2_clock_WEP",
            "observable": "clock drift and WEP/composition force",
            "zero_condition": "one metric/coframe and universal source charge",
            "current_status": "screened_effective_not_parent_derived",
            "next_action": "derive matter descent/no-marker theorem or retain coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ppn_id": "PV868_3_q_loc",
            "observable": "q_loc^nu local exchange force",
            "zero_condition": "P_loc J_trace=0, Pi_I^matter=0, projector stress closed, Bianchi total stress conserved",
            "current_status": "central_open_target",
            "next_action": "build 869 q_loc decomposition or zero theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC868_0_selected",
            "route": "q_loc_residual_vector_decomposition_or_zero_theorem",
            "status": "selected",
            "reason": "q_loc^nu is the common hinge linking local quotient silence, Bianchi safety, projector stress, source normalization, and PPN residuals",
            "include": "P_loc J_trace, Pi_I^matter, projector stress, source exchange, Newton/PPN observable links",
            "exclude": "endpoint root algebra, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG868_0_no_local_GR_claim",
            "claim": "MTS derives local GR",
            "status": "forbidden",
            "reason": "868 writes the reduction stack but does not prove local quotient ownership, EH selection, or projector/no-hair closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG868_1_no_Newton_claim",
            "claim": "MTS derives Newtonian mechanics",
            "status": "forbidden",
            "reason": "source-normalized measured GM remains conditional and open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG868_2_no_PPN_claim",
            "claim": "PPN vector is zero",
            "status": "forbidden",
            "reason": "q_loc^nu, projector stress, and source normalization are not yet derived zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG868_3_allowed_private_result",
            "claim": "GR/Newton proof stack is now finite and ordered",
            "status": "allowed_private_nonclaim",
            "reason": "868 separates exact theorem gates from retained residual fallback rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D868_0",
            "finding": "endpoint_branch_removed_from_critical_path",
            "reason": "DeltaR endpoint roots are closure-only, so local GR work should not wait for endpoint promotion",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D868_1",
            "finding": "local_GR_chain_rebuilt",
            "reason": "the required chain is q_loc ownership -> one metric -> no-hair/projector -> EH/Bianchi -> Newton source -> PPN vector",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D868_2",
            "finding": "q_loc_is_next_common_hinge",
            "reason": "q_loc^nu collects trace flux, coframe pullback, projector stress, and source exchange in one local residual vector",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive q_loc^nu=0 from local quotient/no-hair/Bianchi/projector closure or decompose it into retained source-normalized residual coefficients",
            "include": "P_loc J_trace, Pi_I^matter, F_P_bulk/T_projector, source exchange, PPN/clock/WEP/orbital observable links",
            "exclude": "endpoint root algebra, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "rebuilt the local GR/Newton reduction spine after freezing the endpoint branch as closure",
            "best_partial_result": "local GR now has an ordered finite theorem stack and q_loc^nu is isolated as the next common hinge",
            "hard_blockers": "q_loc ownership, boundary no-hair, N5/projector stress, EH operator selection, source-normalized GM, PPN residual vector",
            "what_is_not_claimed": "local GR, Newtonian limit, PPN pass, q_loc zero",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_csv_rows_nonclaim(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists():
            offenders.append(f"{path.name}:missing")
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for index, row in enumerate(csv.DictReader(handle), start=2):
                if row.get("valid_for_claim") != "false":
                    offenders.append(f"{path.name}:{index}")
    if offenders:
        return False, ";".join(offenders)
    return True, "all generated rows valid_for_claim=false"


def csv_table(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    chain_rows: list[dict[str, object]],
    blocker_rows_: list[dict[str, object]],
    qloc_rows_: list[dict[str, object]],
    newton_rows_: list[dict[str, object]],
    ppn_rows_: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 868 - Local GR Reduction Stack After Endpoint Closure

Generated: `{generated_utc}`

Current result: **the project is now back on the GR/Newton spine**. The endpoint root mechanism is not being promoted; it is closure-only. The local reduction problem is now a finite theorem stack: own the local quotient, prove one-metric matter descent, prove boundary/projector no-hair, select the EH exterior, enforce Bianchi-safe `q_loc^nu=0`, normalize the Newtonian source, then zero or bound the PPN vector. The shared hinge is `q_loc^nu`: if it is derived zero, the local GR path gets serious; if not, it becomes a retained residual vector that must be tested instead of hidden.

## Nonclaim Summary

{csv_table(summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])}

## Local GR Reduction Chain

{csv_table(chain_rows, ["chain_id", "required_theorem", "sufficient_form", "if_proved", "current_status", "blocks", "valid_for_claim", "generated_utc"])}

## Local GR Blocker Audit

{csv_table(blocker_rows_, ["blocker_id", "blocker", "current_status", "why_it_matters", "next_action", "claim_impact", "valid_for_claim", "generated_utc"])}

## q_loc Decomposition Contract

{csv_table(qloc_rows_, ["term_id", "term", "zero_route", "if_nonzero", "current_status", "next_test", "valid_for_claim", "generated_utc"])}

## Newton Source Normalization Contract

{csv_table(newton_rows_, ["source_id", "condition", "required_form", "current_status", "failure_if_missing", "valid_for_claim", "generated_utc"])}

## PPN Vector Ledger

{csv_table(ppn_rows_, ["ppn_id", "observable", "zero_condition", "current_status", "next_action", "valid_for_claim", "generated_utc"])}

## Route Choice

{csv_table(route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Claim Guard

{csv_table(claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])}

## Decision

{csv_table(decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])}

## Next Target

{csv_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{csv_table(validation_rows, ["check_id", "result", "detail"])}
"""
    OUTPUT_DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat()

    source_rows = source_register_rows(generated_utc)
    chain_rows = reduction_chain_rows(generated_utc)
    blocker_rows_ = blocker_rows(generated_utc)
    qloc_rows_ = qloc_rows(generated_utc)
    newton_rows_ = newton_rows(generated_utc)
    ppn_rows_ = ppn_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    claim_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(REDUCTION_CHAIN_PATH, chain_rows, ["chain_id", "required_theorem", "sufficient_form", "if_proved", "current_status", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(BLOCKER_AUDIT_PATH, blocker_rows_, ["blocker_id", "blocker", "current_status", "why_it_matters", "next_action", "claim_impact", "valid_for_claim", "generated_utc"])
    write_csv(QLOC_DECOMPOSITION_PATH, qloc_rows_, ["term_id", "term", "zero_route", "if_nonzero", "current_status", "next_test", "valid_for_claim", "generated_utc"])
    write_csv(NEWTON_SOURCE_PATH, newton_rows_, ["source_id", "condition", "required_form", "current_status", "failure_if_missing", "valid_for_claim", "generated_utc"])
    write_csv(PPN_VECTOR_PATH, ppn_rows_, ["ppn_id", "observable", "zero_condition", "current_status", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])

    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    source_checks_pass = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    chain_complete_pass = len(chain_rows) == 8 and chain_rows[-1]["chain_id"] == "GR868_7_PPN_residual_vector"
    endpoint_removed_pass = any(row["blocker_id"] == "BL868_0_not_endpoint_limited_now" and row["current_status"] == "frozen_as_closure" for row in blocker_rows_)
    qloc_terms_pass = len(qloc_rows_) == 4 and any(row["term_id"] == "QL868_3_source_exchange" for row in qloc_rows_)
    newton_contract_pass = len(newton_rows_) == 3 and any(row["source_id"] == "NS868_1_measured_GM" for row in newton_rows_)
    ppn_vector_pass = len(ppn_rows_) == 4 and any(row["ppn_id"] == "PV868_3_q_loc" for row in ppn_rows_)
    route_selected_pass = any(row["route_id"] == "RC868_0_selected" and row["route"] == "q_loc_residual_vector_decomposition_or_zero_theorem" for row in route_rows)
    claim_allowed_false_pass = all(row["claim_allowed"] == "false" for row in decision_rows_)
    formalization_count = formalization_workbench_modified_count()

    validation_rows = [
        {"check_id": "V868_0_sources_exist_and_needles", "result": "pass" if source_checks_pass else "fail", "detail": "all source paths exist and needles are present" if source_checks_pass else "one or more source checks failed"},
        {"check_id": "V868_1_prior_867_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V868_2_reduction_chain_complete", "result": "pass" if chain_complete_pass else "fail", "detail": "8-step local GR/Newton chain recorded"},
        {"check_id": "V868_3_endpoint_removed_from_critical_path", "result": "pass" if endpoint_removed_pass else "fail", "detail": "endpoint branch remains closure-only"},
        {"check_id": "V868_4_q_loc_decomposition_ready", "result": "pass" if qloc_terms_pass else "fail", "detail": "trace, coframe, projector, and source-exchange q_loc terms recorded"},
        {"check_id": "V868_5_Newton_source_contract_ready", "result": "pass" if newton_contract_pass else "fail", "detail": "measured GM/source-normalization contract recorded"},
        {"check_id": "V868_6_PPN_vector_ready", "result": "pass" if ppn_vector_pass else "fail", "detail": "PPN vector includes q_loc central target"},
        {"check_id": "V868_7_route_selected", "result": "pass" if route_selected_pass else "fail", "detail": NEXT_TARGET},
        {"check_id": "V868_8_claim_allowed_false", "result": "pass" if claim_allowed_false_pass else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V868_9_all_rows_nonclaim", "result": "pending", "detail": "filled after csv nonclaim scan"},
        {"check_id": "V868_10_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V868_11_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]

    nonclaim_pass, nonclaim_detail = all_csv_rows_nonclaim(GENERATED_CSV_PATHS)
    for row in validation_rows:
        if row["check_id"] == "V868_9_all_rows_nonclaim":
            row["result"] = "pass" if nonclaim_pass else "fail"
            row["detail"] = nonclaim_detail

    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_markdown(
        generated_utc,
        source_rows,
        chain_rows,
        blocker_rows_,
        qloc_rows_,
        newton_rows_,
        ppn_rows_,
        route_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"status={STATUS}")
    print("partial_result=local GR/Newton stack rebuilt; q_loc^nu isolated as next common theorem-or-residual hinge")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")
    if failed:
        for row in failed:
            print(f"validation_failure={row['check_id']}:{row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
