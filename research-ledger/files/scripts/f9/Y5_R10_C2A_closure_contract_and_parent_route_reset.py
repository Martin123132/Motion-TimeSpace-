from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "825-Y5-R10-C2A-closure-contract-and-parent-route-reset.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_825_SOURCE_REGISTER.csv"
CLOSURE_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_825_C2A_CLOSURE_CONTRACT.csv"
FIREWALL_PATH = RESIDUALS / "P8_Y5_R10_825_CLAIM_FIREWALL.csv"
PARENT_ROUTE_PATH = RESIDUALS / "P8_Y5_R10_825_PARENT_ROUTE_RESET.csv"
ACTION_CHECKLIST_PATH = RESIDUALS / "P8_Y5_R10_825_PARENT_ACTION_CHECKLIST.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_825_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_825_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_825_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_825_VALIDATION.csv"

STATUS = "Y5_R10_825_C2A_closure_firewalled_parent_route_reset_to_memory_action_coefficients_nonclaim"
CLAIM_CEILING = "closure_contract_and_parent_route_reset_only_no_data_run_no_local_GR_claim"
NEXT_TARGET = "826-Y5-R10-parent-memory-action-coefficient-checklist.md"

SOURCE_SPECS = [
    {
        "source_id": "824_doc",
        "path": POST_CHECKPOINT / "824-Y5-R10-C2A-Noether-boundary-stress-owner-or-closure-demotion.md",
        "needles": [
            "C2A domain route is demoted to explicit closure-only",
            "G824_2_closure_demotion",
            "825-Y5-R10-C2A-closure-contract-and-parent-route-reset.md",
        ],
        "role": "immediate demotion handoff",
    },
    {
        "source_id": "824_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_824_VALIDATION.csv",
        "needles": [
            "V824_5_closure_demotion_selected,pass",
            "V824_8_all_rows_nonclaim,pass",
            "V824_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "816_replacement_contract",
        "path": POST_CHECKPOINT / "816-Y5-R10-C1-shape-demotion-and-branch-replacement-contract.md",
        "needles": [
            "C2_parent_source_memory_law",
            "RR816_5_local_GR_firewall",
            "no_fit_renaming",
        ],
        "role": "replacement route discipline and no-fit hygiene",
    },
    {
        "source_id": "821_control_scalar_hunt",
        "path": POST_CHECKPOINT / "821-Y5-R10-C2A-parent-control-scalar-candidate-hunt.md",
        "needles": [
            "X821_0_coherent_load_exposure_IM",
            "X821_1_XB_firewall_wrapper",
            "If that parent map fails, C2A remains closure-only.",
        ],
        "role": "source-control candidate and C2A closure fallback",
    },
    {
        "source_id": "parent_equations_v1",
        "path": FORMALIZATION / "83-parent-equations-v1.md",
        "needles": [
            "no sector gets to invent its own source law.",
            "E7 is effective open-system dynamics, not a closed-action derivation.",
            "Gamma_eff owns the metric-proportional trace projection;",
        ],
        "role": "parent source/conservation spine",
    },
    {
        "source_id": "minimal_parent_sketch",
        "path": FORMALIZATION / "12-minimal-parent-theory-sketch.md",
        "needles": [
            "GR, Newtonian gravity, standard time dilation, and Maxwell/quantum behaviour where applicable must appear as limiting cases, not be contradicted.",
            "This is the route from research programme to field theory.",
        ],
        "role": "full programme scope and limits requirement",
    },
    {
        "source_id": "XB_firewall",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "If `X_B` is arbitrary",
            "transition shells remain local PPN obligations,",
            "source-power closure open.",
        ],
        "role": "universal local/cosmology firewall",
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


def closure_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "CC825_0_label",
            "object": "C2A_domain_transport_branch",
            "status": "explicit_closure_only",
            "allowed_use": "private bookkeeping grammar for local-frozen versus FLRW-comoving volume transport",
            "forbidden_use": "parent derivation, local-GR pass, data evidence, or replacement for a Noether boundary owner",
            "revival_condition": "derive parent S_D, T_D, unique J_rel class, domain Euler equation, and wall-stress bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC825_1_surviving_formulae",
            "object": "N_D and J_rel kinematic identities",
            "status": "conditional_bookkeeping",
            "allowed_use": "test algebraic consistency of N_D=(1/3)ln(V_D0/V_D), Phi_rel, and local/FLRW limits",
            "forbidden_use": "declaring D, u3, B_mem, or boundary stress parent-derived",
            "revival_condition": "all domain variables descend from a sourced parent action or coarse-graining theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC825_2_cosmology",
            "object": "C2A cosmology shape",
            "status": "not_strict_candidate",
            "allowed_use": "future closure benchmark clearly marked as not parent-derived",
            "forbidden_use": "running SN/BAO/CMB/growth as support for MTS field theory",
            "revival_condition": "source law, amplitude, perturbations, and local firewall are parent-locked before data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC825_3_local_GR",
            "object": "local GR/Newton/PPN branch",
            "status": "not_helped_by_C2A_closure",
            "allowed_use": "use C2A failures to identify what parent action must not do",
            "forbidden_use": "using local frozen assumption as a proof of q_loc=0",
            "revival_condition": "derive q_loc^nu -> 0 or a sourced PPN residual vector from parent equations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC825_4_public_language",
            "object": "claim wording",
            "status": "private_nonclaim",
            "allowed_use": "say C2A is a demoted closure route that sharpened the parent-action target",
            "forbidden_use": "say C2A explains dark energy, passes local GR, or derives the memory source",
            "revival_condition": "not applicable until all parent locks are satisfied",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def firewall_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "firewall_id": "FW825_0_claim_flag",
            "rule": "Every C2A closure artifact carries valid_for_claim=false.",
            "failure_if_violated": "hidden promotion of closure into field-theory claim",
            "enforcement": "validation scans generated rows for valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "firewall_id": "FW825_1_data_firewall",
            "rule": "No C2A closure row may be used as an evidential cosmology data branch.",
            "failure_if_violated": "post-hoc fit renamed as derivation",
            "enforcement": "next targets forbid data fitting as evidence until parent coefficients are sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "firewall_id": "FW825_2_local_firewall",
            "rule": "No C2A closure row may upgrade local GR/Newton/PPN status.",
            "failure_if_violated": "smuggled plateau/domain axiom",
            "enforcement": "local route remains tied to q_loc, K_hat, boundary, and PPN residual gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "firewall_id": "FW825_3_XB_universality",
            "rule": "X_B remains a universal firewall wrapper, not a retuned sector switch.",
            "failure_if_violated": "galaxy/cosmology/local branches become disguised curve fitting",
            "enforcement": "next parent route must source X_B coefficients before sector use",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "firewall_id": "FW825_4_formalization_guard",
            "rule": "This checkpoint remains in post-checkpoint-work and does not modify formalization-workbench.",
            "failure_if_violated": "private route experiment pollutes the main spine",
            "enforcement": "formalization_changed_after_cutoff must remain zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "PR825_0_memory_action_coefficients",
            "route": "Noether-safe memory/action coefficient route",
            "status": "selected_next",
            "why": "it stays closest to the parent equations, avoids an inserted domain wall, and attacks Gamma_eff/K_hat/q ownership directly",
            "main_blockers": "closed/open-system action, X_B coefficients, R(m;X_B), F_L, a_F, L_cg, B_mem, perturbations, local q/K_hat bounds",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "PR825_1_C2A_domain_route",
            "route": "coherent-domain determinant exposure route",
            "status": "demoted_to_closure",
            "why": "domain selector, boundary current, and wall stress were not Noether-owned",
            "main_blockers": "S_D, T_D, unique J_rel, D Euler equation, wall-stress bound",
            "next_action": "do not pursue as parent route until owner exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "PR825_2_nonlocal_quarantine",
            "route": "nonlocal/routed transition quarantine",
            "status": "fallback_closure_only",
            "why": "could quarantine transition residuals but currently lacks a parent kernel and observable-response proof",
            "main_blockers": "quarantine projector, total conservation, response zero, local PPN safety",
            "next_action": "retain as fallback if direct parent memory route fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "PR825_3_empirical_cosmology",
            "route": "SN/BAO/CMB/growth fit route",
            "status": "deferred",
            "why": "testing is valuable only after the strict branch has parent-sourced coefficients or is labelled as closure benchmark",
            "main_blockers": "shape/amplitude/perturbation locks missing",
            "next_action": "return after 826+ source locks",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "PR825_4_galaxy_empirical",
            "route": "galaxy/SPARC transport route",
            "status": "separate_empirical_pillar",
            "why": "galaxies remain important but should not dominate the unified-field derivation chat",
            "main_blockers": "parent routing and local-GR limit are upstream",
            "next_action": "keep separate from this parent derivation sequence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def action_checklist_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "checklist_id": "AC825_0_fields",
            "requirement": "Declare parent fields g_mu_nu, psi, m=Gamma_mem, u_mu/coarse-graining frame, and X_B without domain D as an inserted primitive.",
            "acceptance_gate": "every field has status, units, and variation/readout role",
            "if_missing": "parent route remains scaffold only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "checklist_id": "AC825_1_stress_variation",
            "requirement": "Vary the candidate parent memory/action sector to produce T_MTS, Gamma_eff, K_hat, and q^nu ownership.",
            "acceptance_gate": "Bianchi/Ward identity gives total conservation with no hidden source",
            "if_missing": "fails field-theory gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "checklist_id": "AC825_2_local_GR_limit",
            "requirement": "Derive Gamma_eff -> constant, div K_hat -> 0/bounded, and q_loc^nu -> 0/bounded in tested local systems.",
            "acceptance_gate": "explicit PPN/R10/clock/orbital residual vector or zero theorem",
            "if_missing": "no MTS -> GR -> Newton claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "checklist_id": "AC825_3_cosmology_source",
            "requirement": "Derive the cosmology memory source law, amplitude corridor, and perturbation closure from the same coefficients.",
            "acceptance_gate": "shape/amplitude/perturbation values are pre-data and non-arbitrary",
            "if_missing": "cosmology branch remains closure benchmark",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "checklist_id": "AC825_4_XB_coefficients",
            "requirement": "Source X_B, Pi_B, U_B, D_L, mu_B/gamma_B, m_L, S_cg, F_L, L_cg, and support powers from one universal rule.",
            "acceptance_gate": "same rule handles local, galaxy, and cosmology regimes without sector retuning",
            "if_missing": "firewall cannot be trusted",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "checklist_id": "AC825_5_no_fit_renaming",
            "requirement": "No fitted shape, hazard, switch, or amplitude may be renamed as derived after seeing data.",
            "acceptance_gate": "future data rows separate closure benchmarks from strict parent candidates",
            "if_missing": "empirical pass is scientifically unsafe",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D825_0",
            "decision": "C2A domain route is firewalled as closure-only",
            "reason": "824 failed to derive a Noether/boundary-stress owner, so C2A cannot function as parent field theory",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D825_1",
            "decision": "reset next derivation to parent memory/action coefficients",
            "reason": "the least-cheaty route now is to make T_MTS, Gamma_eff, K_hat, q, X_B, and local/cosmology coefficients descend from one parent source structure",
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
            "objective": "build a parent-memory action/coefficient checklist and attempt the first Noether-safe coefficient derivation without using the demoted C2A domain closure",
            "allowed_work": "symbolic action/coefficient audit, Ward identity, local-GR zero/bound conditions, cosmology source locks",
            "forbidden_work": "data fitting, C2A closure promotion, local-GR claim, public claim",
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
            "what_changed": "C2A is now explicitly firewalled as closure-only and the next derivation route is reset to parent memory/action coefficients",
            "why_it_matters": "prevents the useful domain grammar from smuggling in a local plateau or data-ready cosmology claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    firewall: list[dict[str, object]],
    parent_routes: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V825_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_824, clean_824_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_824_VALIDATION.csv")
    add("V825_1_prior_824_clean", clean_824, clean_824_detail)
    add(
        "V825_2_C2A_closure_contract_present",
        any(row["object"] == "C2A_domain_transport_branch" and row["status"] == "explicit_closure_only" for row in closure_rows),
        "C2A closure-only contract is present",
    )
    add(
        "V825_3_claim_firewalls_complete",
        {"FW825_0_claim_flag", "FW825_1_data_firewall", "FW825_2_local_firewall", "FW825_3_XB_universality"}.issubset({row["firewall_id"] for row in firewall}),
        "claim, data, local, and X_B firewalls present",
    )
    add(
        "V825_4_parent_route_selected",
        any(row["route_id"] == "PR825_0_memory_action_coefficients" and row["status"] == "selected_next" for row in parent_routes),
        "memory/action coefficient route selected",
    )
    add(
        "V825_5_domain_route_demoted",
        any(row["route_id"] == "PR825_1_C2A_domain_route" and row["status"] == "demoted_to_closure" for row in parent_routes),
        "domain route remains demoted",
    )
    add(
        "V825_6_action_checklist_complete",
        {"AC825_0_fields", "AC825_1_stress_variation", "AC825_2_local_GR_limit", "AC825_3_cosmology_source", "AC825_4_XB_coefficients", "AC825_5_no_fit_renaming"}.issubset({row["checklist_id"] for row in action_rows}),
        "parent action checklist covers fields, stress, local, cosmology, X_B, and no-fit rules",
    )
    add(
        "V825_7_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "branch remains non-runnable",
    )
    add(
        "V825_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + closure_rows + firewall + parent_routes + action_rows + decisions + next_rows + summary
    add(
        "V825_9_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V825_10_no_data_or_local_GR_claim",
        all("data fitting" in row["forbidden_work"] and "local-GR claim" in row["forbidden_work"] for row in next_rows),
        "no data or local-GR claim selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V825_11_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V825_12_validation_rows_ready", True, "validation table constructed")
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
    closure_rows: list[dict[str, object]],
    firewall: list[dict[str, object]],
    parent_routes: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 825 - Y5 R10 C2A Closure Contract And Parent Route Reset",
            (
                "Current result: **C2A is now an explicitly firewalled closure branch, not a parent-derived route**. "
                "The next serious derivation path resets to a Noether-safe parent memory/action coefficient audit, because that attacks `T_MTS`, `Gamma_eff`, `K_hat`, `q^nu`, `X_B`, local GR, and cosmology from one source structure instead of smuggling in a domain wall."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_changed", "why_it_matters", "next_target", "valid_for_claim"]),
            "## C2A Closure Contract\n\n" + markdown_table(closure_rows, ["contract_id", "object", "status", "allowed_use", "forbidden_use", "revival_condition", "valid_for_claim"]),
            "## Claim Firewall\n\n" + markdown_table(firewall, ["firewall_id", "rule", "failure_if_violated", "enforcement", "valid_for_claim"]),
            "## Parent Route Reset\n\n" + markdown_table(parent_routes, ["route_id", "route", "status", "why", "main_blockers", "next_action", "valid_for_claim"]),
            "## Parent Action Checklist\n\n" + markdown_table(action_rows, ["checklist_id", "requirement", "acceptance_gate", "if_missing", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is the right kind of retreat: not giving up, not hand-waving, just refusing to let a closure masquerade as derivation. "
            "The forward route is now cleaner: derive the memory/action coefficients or keep the cosmology branch honestly labelled as a benchmark.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    closure_rows = closure_contract_rows(generated_utc)
    firewall = firewall_rows(generated_utc)
    parent_routes = parent_route_rows(generated_utc)
    action_rows = action_checklist_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, closure_rows, firewall, parent_routes, action_rows, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_CONTRACT_PATH, closure_rows, ["contract_id", "object", "status", "allowed_use", "forbidden_use", "revival_condition", "valid_for_claim", "generated_utc"])
    write_csv(FIREWALL_PATH, firewall, ["firewall_id", "rule", "failure_if_violated", "enforcement", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_ROUTE_PATH, parent_routes, ["route_id", "route", "status", "why", "main_blockers", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(ACTION_CHECKLIST_PATH, action_rows, ["checklist_id", "requirement", "acceptance_gate", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_changed", "why_it_matters", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, closure_rows, firewall, parent_routes, action_rows, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"825 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
