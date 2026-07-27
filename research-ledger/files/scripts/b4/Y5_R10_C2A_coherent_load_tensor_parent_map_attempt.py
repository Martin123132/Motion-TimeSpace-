from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "822-Y5-R10-C2A-coherent-load-tensor-parent-map-attempt.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_822_SOURCE_REGISTER.csv"
MAP_CLAUSES_PATH = RESIDUALS / "P8_Y5_R10_822_PARENT_MAP_CLAUSES.csv"
FLRW_REDUCTION_PATH = RESIDUALS / "P8_Y5_R10_822_FLRW_REDUCTION_AUDIT.csv"
FAILURE_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_822_FAILURE_LEDGER.csv"
PROMOTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_822_PROMOTION_CONTRACT.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_822_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_822_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_822_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_822_VALIDATION.csv"

STATUS = "Y5_R10_822_coherent_load_parent_map_partial_chain_boundary_blocked_nonclaim"
CLAIM_CEILING = "conditional_parent_map_skeleton_only_no_parent_derivation_no_data_run"
NEXT_TARGET = "823-Y5-R10-C2A-boundary-current-representative-or-domain-demotion.md"

SOURCE_SPECS = [
    {
        "source_id": "821_doc",
        "path": POST_CHECKPOINT / "821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md",
        "needles": [
            "the best next source-control candidate is coherent-load exposure `I_M=det(Q_coh)`",
            "Q parent action, domain selector, boundary current",
            "822-Y5-R10-C2A-coherent-load-tensor-parent-map-attempt.md",
        ],
        "role": "immediate handoff selecting Q_coh parent-map attempt",
    },
    {
        "source_id": "821_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_821_VALIDATION.csv",
        "needles": [
            "V821_3_primary_selected,pass,X821_0_coherent_load_exposure_IM",
            "V821_6_obligations_complete,pass",
            "V821_8_next_target_selected,pass,822-Y5-R10-C2A-coherent-load-tensor-parent-map-attempt.md",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "139_hazard",
        "path": POST_CHECKPOINT / "139-density-law-hazard-theorem-attempt.md",
        "needles": [
            "I_M = det(Q)",
            "Q^i_j = X delta^i_j",
            "A(N_D) = 1 - exp[-(N_D/u3)^3].",
            "Q^i_j parent action;",
            "hazard law cannot derive B_mem.",
        ],
        "role": "hazard/determinant chain and open blockers",
    },
    {
        "source_id": "138_pressure_kernel",
        "path": POST_CHECKPOINT / "138-coherent-volume-pressure-kernel-theorem.md",
        "needles": [
            "V_D = integral_D sqrt(h) d^3x.",
            "N_D = (1/3) ln(V_D0 / V_D).",
            "p_M = -rho_M + (1/3) d rho_M / dN_D.",
            "the parent domain selector D;",
            "local N_D = 0 and delta N_D = 0 theorem;",
        ],
        "role": "coherent-volume FLRW reduction and local/pressure blockers",
    },
    {
        "source_id": "143_domain_selector",
        "path": POST_CHECKPOINT / "143-domain-selector-variational-action-attempt.md",
        "needles": [
            "Q can be owned by coherent-volume load if D and u3 are derived.",
            "D is the main blocker.",
            "C_coh[D] =",
            "boundary not hand tuned = fail open.",
            "derive the J_rel representative / boundary exchange current.",
        ],
        "role": "domain-selector and boundary-current obstruction",
    },
    {
        "source_id": "85_XB_firewall",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "If `X_B` is arbitrary",
            "X_B = {",
            "FLRW memory remains allowed only with:",
            "source-power closure open.",
        ],
        "role": "universal firewall/routing discipline",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check_needles(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_path"
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
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
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def map_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "M822_0_domain",
            "map_step": "Choose coherent domain D before computing volume/load.",
            "attempted_derivation": "Use existing C_coh[D] and auxiliary selector language as a contract for coherent domains.",
            "result": "fails_parent_derivation",
            "reason": "143 shows the selector can constrain chi_D after D is supplied, but no zero-knob Euler equation selects D.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "M822_1_load_tensor",
            "map_step": "Define Q_coh^i_j as the coherent-domain load tensor.",
            "attempted_derivation": "Treat Q as the tensor whose isotropic FLRW reduction is Q^i_j=X_load delta^i_j.",
            "result": "contract_only",
            "reason": "The source set contains the required Q chain, but not a parent action/equation deriving Q_coh from MTS variables.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "M822_2_determinant_exposure",
            "map_step": "Set I_M=det(Q_coh).",
            "attempted_derivation": "If Q_coh is a positive orientation-preserving spatial endomorphism, det(Q_coh) is a scalar exposure candidate.",
            "result": "algebra_survives_conditionally",
            "reason": "Determinant exposure is coordinate-natural once Q exists, but positivity/orientation must be signed.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "M822_3_FLRW_scalar",
            "map_step": "For isotropic FLRW, Q^i_j=X_load delta^i_j so I_M=X_load^3.",
            "attempted_derivation": "The determinant of X_load times the 3D identity is X_load^3.",
            "result": "pass_conditional",
            "reason": "This conditionally explains p_source=3 from spatial dimension if the Q reduction is parent-owned.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "M822_4_volume_time",
            "map_step": "Identify X_load=N_D/u3 with N_D=(1/3)ln(V_D0/V_D).",
            "attempted_derivation": "For FLRW V_D proportional to a^3, N_D=-ln(a)=ln(1+z).",
            "result": "pass_conditional",
            "reason": "The volume variable gives the right redshift coordinate only if D is a real coherent domain and u3 is parent-owned.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "M822_5_survival_activation",
            "map_step": "Use A=1-exp(-I_M) and S_Gamma=B_mem dA/dN_source.",
            "attempted_derivation": "Additive independent exposure gives exponential survival; derivative gives the source density.",
            "result": "shape_survives_conditionally",
            "reason": "Hazard shape survives if I_M is parent exposure; B_mem and time/source orientation are not derived.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "M822_6_local_firewall",
            "map_step": "Require local stationary domains to have N_D=0, delta N_D=0, and no PPN-sized boundary stress.",
            "attempted_derivation": "Use X_B as the universal routing/firewall wrapper around the I_M branch.",
            "result": "blocked",
            "reason": "X_B helps structure the firewall, but local silence and boundary-current representative are not derived.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def flrw_reduction_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "F822_0_volume",
            "statement": "V_D=integral_D sqrt(h)d^3x and N_D=(1/3)ln(V_D0/V_D).",
            "result": "pass_conditional",
            "condition": "D is a coherent domain selected independently of outcome data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "F822_1_FLRW_time",
            "statement": "For FLRW V_D proportional to a^3, N_D=-ln(a)=ln(1+z).",
            "result": "pass_conditional",
            "condition": "domain comoves/homogeneous in the FLRW branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "F822_2_determinant",
            "statement": "If Q^i_j=X_load delta^i_j, then det(Q)=X_load^3.",
            "result": "pass_conditional",
            "condition": "Q_coh exists before FLRW reduction and is positive/oriented",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "F822_3_locked_shape",
            "statement": "If X_load=N_D/u3, then I_M=(N_D/u3)^3 and A=1-exp[-(N_D/u3)^3].",
            "result": "pass_conditional",
            "condition": "u3 is parent-owned and not imported from fit history",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "F822_4_pressure_kernel",
            "statement": "If rho_M(N_D) is supplied, metric variation gives p_M=-rho_M+(1/3)d rho_M/dN_D.",
            "result": "pass_conditional",
            "condition": "rho_M source density and boundary variation are owned by parent/action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def failure_rows(generated_utc: str) -> list[dict[str, object]]:
    failures = [
        ("B822_0_domain_selector", "D is not selected by a parent zero-knob action", "blocks Q_coh and N_D from being physical rather than chosen"),
        ("B822_1_boundary_current", "J_rel / moving-domain boundary current is not derived", "risks wall stress, local PPN hair, and local-to-FLRW leakage"),
        ("B822_2_Q_parent_action", "Q_coh is not derived from parent MTS variables", "determinant exposure remains an inserted tensor map"),
        ("B822_3_u3_normalization", "u3=1/4 is not parent-derived here", "cubic shape constant cannot be promoted"),
        ("B822_4_Bmem_amplitude", "B_mem is not fixed by the hazard/determinant map", "shape is not amplitude"),
        ("B822_5_orientation_sign", "source-time orientation and monotonicity of I_M are not signed", "positive source density is conditional"),
        ("B822_6_local_silence", "local N_D=0 and delta N_D=0 theorem is missing", "no R10/PPN/local-GR promotion"),
        ("B822_7_perturbations", "full perturbation action is missing", "no CMB/growth/lensing promotion"),
        ("B822_8_XB_factorization", "I_M branch is not yet mapped through universal X_B without retuning", "local/cosmology compatibility remains open"),
    ]
    return [
        {
            "blocker_id": blocker_id,
            "blocker": blocker,
            "impact": impact,
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for blocker_id, blocker, impact in failures
    ]


def promotion_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    clauses = [
        ("PC822_0_domain", "A parent variational or coarse-graining principle selects D without target-data outcome tuning."),
        ("PC822_1_Q", "The same parent principle defines Q_coh^i_j before FLRW specialization."),
        ("PC822_2_determinant", "Q_coh is positive/oriented or has a signed-exposure rule that keeps I_M physical."),
        ("PC822_3_FLRW", "FLRW reduction gives Q^i_j=X_load delta^i_j and X_load=N_D/u3."),
        ("PC822_4_u3", "u3 is derived from cell/dimension normalization or kept symbolic stress-only."),
        ("PC822_5_boundary", "J_rel or equivalent boundary representative removes wall stress and preserves conservation."),
        ("PC822_6_local", "Stationary/local domains give N_D=0, delta N_D=0, q_loc^nu=0 within PPN/R10 tolerance."),
        ("PC822_7_amplitude", "B_mem is derived/bounded/quarantined before evidence claims."),
        ("PC822_8_perturbations", "Perturbation action gives sound speed, slip, source, and growth/CMB response."),
        ("PC822_9_XB", "I_M activation is routed through universal X_B without sector retuning."),
    ]
    return [
        {
            "contract_id": contract_id,
            "requirement": requirement,
            "current_status": "not_satisfied",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for contract_id, requirement in clauses
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D822_0",
            "decision": "parent map does not close; retain a conditional Q_coh/I_M skeleton only",
            "reason": "determinant, FLRW, volume-time, and survival-shape steps work conditionally, but D, Q, J_rel, u3, B_mem, local silence, and perturbations remain unsigned",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D822_1",
            "decision": "attack boundary-current/domain representative next rather than run data",
            "reason": "143 and 822 both identify boundary/domain ownership as the choke point for local silence and parent promotion",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive a J_rel/domain representative that is local-stationary trivial, FLRW nontrivial, and boundary-stress safe, or demote the route",
            "allowed_work": "symbolic variation, conservation/Bianchi ledger, local/FLRW representative audit",
            "forbidden_work": "SN/BAO/CMB/growth fitting, parent-derived claim, local-GR claim",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_survived": "I_M=det(Q_coh) gives p_source=3 conditionally under isotropic FLRW and additive-hazard survival",
            "what_failed": "parent selection of D, parent definition of Q_coh, boundary current J_rel, u3, B_mem, local silence, perturbations",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    flrw_rows: list[dict[str, object]],
    failure_rows_: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V822_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_821, clean_821_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_821_VALIDATION.csv")
    add("V822_1_prior_821_clean", clean_821, clean_821_detail)
    add(
        "V822_2_determinant_clause_present",
        any(row["clause_id"] == "M822_2_determinant_exposure" for row in map_rows),
        "I_M=det(Q_coh) clause recorded",
    )
    add(
        "V822_3_FLRW_cubic_reduction_present",
        any(row["audit_id"] == "F822_2_determinant" for row in flrw_rows) and any(row["audit_id"] == "F822_3_locked_shape" for row in flrw_rows),
        "FLRW determinant and locked-shape reductions recorded",
    )
    failure_ids = {row["blocker_id"] for row in failure_rows_}
    add(
        "V822_4_domain_boundary_failures_recorded",
        {"B822_0_domain_selector", "B822_1_boundary_current", "B822_6_local_silence"}.issubset(failure_ids),
        "domain, boundary, and local-silence failures recorded",
    )
    add(
        "V822_5_promotion_contract_complete",
        len(contract_rows) >= 10 and all(row["current_status"] == "not_satisfied" for row in contract_rows),
        "promotion contract complete and unsatisfied",
    )
    add(
        "V822_6_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "parent map remains non-runnable",
    )
    add(
        "V822_7_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + map_rows + flrw_rows + failure_rows_ + contract_rows + decisions + next_rows + summary
    add(
        "V822_8_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V822_9_no_data_run_selected",
        all("fitting" in row["forbidden_work"] for row in next_rows),
        "no data run selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V822_10_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V822_11_validation_rows_ready", True, "validation table constructed")
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    flrw_rows: list[dict[str, object]],
    failure_rows_: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 822 - Y5 R10 C2A Coherent Load-Tensor Parent-Map Attempt",
            (
                "Current result: **the coherent-load route gives a real conditional skeleton, but not a parent-derived source law**. "
                "`I_M=det(Q_coh)` conditionally explains the cubic exposure in FLRW, yet the parent map fails at the domain selector, boundary current, load-tensor owner, and local-silence clauses."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim"]),
            "## Parent-Map Clauses\n\n" + markdown_table(map_rows, ["clause_id", "map_step", "result", "reason", "valid_for_claim"]),
            "## FLRW Reduction Audit\n\n" + markdown_table(flrw_rows, ["audit_id", "statement", "result", "condition", "valid_for_claim"]),
            "## Failure Ledger\n\n" + markdown_table(failure_rows_, ["blocker_id", "blocker", "impact", "status", "valid_for_claim"]),
            "## Promotion Contract\n\n" + markdown_table(contract_rows, ["contract_id", "requirement", "current_status", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is a productive failure. The determinant route is not hand-wavy anymore: it has a crisp conditional chain. But the theory does not get to call it derived until the boundary/domain representative is owned. Next move is the boundary-current representative gate.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    map_rows = map_clause_rows(generated_utc)
    flrw_rows = flrw_reduction_rows(generated_utc)
    failure_rows_ = failure_rows(generated_utc)
    contract_rows = promotion_contract_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, map_rows, flrw_rows, failure_rows_, contract_rows, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(MAP_CLAUSES_PATH, map_rows, ["clause_id", "map_step", "attempted_derivation", "result", "reason", "valid_for_claim", "generated_utc"])
    write_csv(FLRW_REDUCTION_PATH, flrw_rows, ["audit_id", "statement", "result", "condition", "valid_for_claim", "generated_utc"])
    write_csv(FAILURE_LEDGER_PATH, failure_rows_, ["blocker_id", "blocker", "impact", "status", "valid_for_claim", "generated_utc"])
    write_csv(PROMOTION_CONTRACT_PATH, contract_rows, ["contract_id", "requirement", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, map_rows, flrw_rows, failure_rows_, contract_rows, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"822 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
