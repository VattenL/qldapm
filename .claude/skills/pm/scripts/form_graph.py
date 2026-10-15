"""The Book of Forms as a dependency graph, built from references/knowledge/*.json.

Each form's receives_from, provides_to and alignment lists become edges: a flow
edge A -> B means information goes from A to B; an alignment edge means the two
documents must stay consistent. A relation declared by either side counts. Things
the book names without a form number (charter inputs, business case, agreements,
enterprise environmental factors, the project budget) are external nodes, shown
by the name the book gives them. The one composite is the scope baseline, which
the book defines as the scope statement 2.8, the WBS 2.9 and the WBS dictionary
2.10 together (Book of Forms form 2.9, PDF page 60, printed page 49, and form 2.10,
PDF page 63, printed page 52).

    form_graph.py 2.32              sources, consumers and alignment partners, with what flows
    form_graph.py --impact 2.9      forms to recheck when 2.9 changes, ordered by distance
    form_graph.py --impact 2.9 2.10 2.8 --depth 1   several forms changed together, files counted once
    form_graph.py --impact 3.3 --category Scope Cost   only the Impacts of Change categories named
    form_graph.py --order           creation order consistent with the dependencies
    form_graph.py --order --group Planning
    form_graph.py --check           A says it provides to B but B does not list A, and similar
    form_graph.py --markdown        print references/form-graph.md to standard output
    form_graph.py --markdown --out PATH   write it to PATH (the committed copy is references/form-graph.md)

--impact follows flow edges downstream transitively, then adds the alignment
partners of the changed form and of every form reached; a form reached only by
alignment is not followed further, since its own consumers change only if it does.
Distance counts edges. Forms with a file in docs/ are marked: docs/forms/<number>-*.md
(written 2-18 or 2.18), and the packages charter-package.en.md (1.1, 2.8) and
scope-package.en.md (2.7, 2.9, 2.10). A package also holds the content of forms it does not
reproduce (the charter's assumptions, milestones, risks and key stakeholder list stand in for
1.2, 2.14, 2.32 and 1.3): --impact marks those "stand-in section" and says to recheck the section,
without counting them among the forms that exist.

--impact lists the files in docs/ that hold the documents ("N documents in M files"), since
one file can hold several forms. It also prints the links the skill adds on top of the
book's lists, each tagged "skill mapping, not book text": the forms that the Impacts of
Change categories of 3.3 point at (Book of Forms form 3.3, PDF pages 181 to 182 (printed
pages 170 to 171); PMBOK 6 section 4.6.3.2, printed page 120 (PDF page 159), says any formally
controlled component or document may change), and the forms that may result in a change request
to 3.3 (CHANGE_SOURCES: 2.18, 2.32, 2.40, 3.6, 4.3, 4.4 and 4.6, each with its PMBOK 6 section).
The 3.3 categories include the Stakeholder Impact and Project Documents boxes the blank form
prints (PDF page 184, printed page 173), which are not Increase, Decrease or Modify areas.

--order cuts every dependency cycle by process sequence: inside a loop it drops the link that
runs from a form of a later PMBOK 6 process to a form of an earlier one (process group, then
chapter and section of the first process in pmbok_processes, then form number), so the form
of the earlier process is drafted first and revised once the later one exists. Plan Resource
Management 9.1 and Estimate Activity Resources 9.2 rank with 6.3, before Estimate Activity
Durations 6.4, because their outputs are inputs of 6.4 (PROCESS_ORDER). The monitoring forms 4.3,
4.4, 4.6 and 4.7, for which the book lists no source, take the plans and baselines they measure
against as prerequisites (ORDER_INPUTS, tagged as a skill mapping). A form whose
knowledge file has a "starts" field (the risk register 2.32, the risk report 2.33, the issue
log 3.1 and the decision log 3.2, which the book says are created at the start of the
project) takes its receives-from links as revision inputs, not prerequisites.

--check exits 1 when it finds an inconsistency between the files, and never edits
them. Exit code 2 is a usage error.
"""

import argparse
import heapq
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
KNOWLEDGE = SKILL / "references" / "knowledge"
INDEX = SKILL / "references" / "forms-index.md"
OUTPUT = SKILL / "references" / "form-graph.md"
DOCS = SKILL.parents[2] / "docs"

FORM_RE = re.compile(r"^\d\.\d+$")
GROUPS = ("Initiating", "Planning", "Executing", "Monitoring and Controlling", "Closing", "Agile")

COMPOSITES = {
    "Scope baseline": {
        "members": ("2.8", "2.9", "2.10"),
        "cite": "Book of Forms form 2.9, PDF page 60 (printed page 49) and form 2.10, PDF page 63 (printed page 52)",
    },
}

# Spellings the knowledge files use for one and the same named document.
ALIASES = {
    "Project budget (no form of this name in the book)": "Project budget",
    "Procurement documents (RFP, RFQ, etc.)": "Procurement documents",
    "Procurement documents (RFP, RFQ)": "Procurement documents",
    "Agreements (contracts)": "Agreements",
    "Project performance reports": "Project performance report",
}

FORWARD_COST = 8

# Forms each package holds, from the package's own "How this document is organised" table:
# the charter package reproduces 1.1 in Part 2 and uses 2.8 as the form for Part 1; the scope
# package reproduces 2.7 (Parts 1 and 1B), 2.9 and 2.10.
PACKAGES = {
    "charter-package.en.md": ("1.1", "2.8"),
    "scope-package.en.md": ("2.7", "2.9", "2.10"),
}

# Content of a form that a package holds without reproducing the printed form: the project's
# stand-in for it. --impact marks these apart from the forms that exist, since the section is
# rechecked as the form but is not laid out as the printed form. Headings as in the package.
STAND_INS = {
    "1.2": ("charter-package.en.md", "1.6 Project Assumptions"),
    "1.3": ("charter-package.en.md", "Part 2A, Key stakeholder list"),
    "2.6": ("charter-package.en.md", "1.1.4 Functions, 1.1.5 Exception and failure behaviour, 1.3 Product Acceptance Criteria"),
    "2.14": ("charter-package.en.md", "Part 2A, Summary milestone schedule"),
    "2.32": ("charter-package.en.md", "Part 2A, Overall project risk"),
}

# Impacts of Change categories printed on 3.3 (Book of Forms form 3.3, PDF pages 181 to 182
# (printed pages 170 to 171)) mapped to the forms of the matching knowledge area. The mapping is
# the skill's, not the book's. Stakeholder Impact and Project Documents are printed on the blank form
# (PDF pages 184, printed pages 173) but are not Increase, Decrease or Modify areas. Resources and risk are not printed categories on 3.3, but PMBOK 6
# section 4.6.2.5, printed page 120 (PDF page 159), says most changes affect time, cost,
# resources or risks.
IMPACT_CATEGORIES = {
    "Scope": ("2.8", "2.9", "2.10"),
    "Quality": ("2.23", "2.24", "3.6"),
    "Requirements": ("2.6", "2.7"),
    "Cost": ("2.20", "2.21", "2.22"),
    "Schedule": ("2.14", "2.18"),
    "Stakeholder Impact": ("1.3", "1.4", "2.30", "2.40"),
    "Project Documents": ("1.2",),
    "Resources and risk": ("2.28", "2.31", "2.32"),
}
CATEGORY_CITE = ("Book of Forms form 3.3, PDF pages 181 to 182 (printed pages 170 to 171); PMBOK 6 section "
                 "4.6.3.2, printed page 120 (PDF page 159)")
SKILL_TAG = "skill mapping, not book text"

# Other links the skill adds: a form whose result may become a change request.
CHANGE_SOURCES = {
    "2.32": "a planned risk response may result in a change request (PMBOK 6 section 11.5.3.1, printed page "
            "447 (PDF page 486))",
    "2.18": "schedule changes and modifications to scope may result in a change request (PMBOK 6 section "
            "6.5.3.5, printed page 220 (PDF page 259); section 6.6.3.3, printed page 229 (PDF page 268))",
    "3.6": "a quality repair or a change to a plan component, document or process needs a change request "
           "(PMBOK 6 section 8.2.3.3, printed page 296 (PDF page 335))",
    "4.3": "analysis of project performance may result in a change request to the cost and schedule "
           "baselines (PMBOK 6 section 7.4.3.3, printed page 269 (PDF page 308))",
    "4.4": "analysis of project performance may result in a change request to the cost and schedule "
           "baselines (PMBOK 6 section 7.4.3.3, printed page 269 (PDF page 308))",
    "4.6": "Control Procurements may result in change requests to the plans and baselines (PMBOK 6 section "
           "12.3.3.4, printed page 499 (PDF page 538))",
    "2.40": "corrective and preventive actions on stakeholder engagement are change requests (PMBOK 6 section "
            "13.4.3.2, printed page 535 (PDF page 574))",
}

# Prerequisites the skill adds to --order for the monitoring forms. The book lists no source for them
# (their knowledge files have an empty receives_from), yet they measure against a plan or a baseline.
# The mapping is the skill's, not the book's.
_CTRL_COST = ("PMBOK 6 section 7.4, printed page 257 (PDF page 296): Control Costs takes the cost management "
              "plan and the cost baseline")
_CTRL_SCHEDULE = ("PMBOK 6 section 6.6, printed page 222 (PDF page 261): Control Schedule takes the schedule "
                  "management plan and the schedule baseline")
_CTRL_PROCUREMENT = ("PMBOK 6 section 12.3, printed page 492 (PDF page 531): Control Procurements takes the "
                     "procurement management plan and the schedule baseline")
_ALIGN_2_27 = ("Book of Forms form 2.27, PDF pages 120 to 121 (printed pages 109 to 110): the Alignment section "
               "lists the resource management plan and the book lists no source for the team charter, so drafting "
               "it after 2.26 is the skill's order")
_ALIGN_2_39 = ("Book of Forms form 2.39, PDF pages 166 to 167 (printed pages 155 to 156): the Alignment section "
               "lists the procurement management plan and the procurement strategy and the book lists no source "
               "for the criteria, so drafting them after 2.37 and 2.38 is the skill's order")
_ALIGN_4_8 = ("Book of Forms form 4.8, PDF page 233 (printed page 222): the Alignment section lists the "
              "procurement management plan and the procurement audit")
ORDER_INPUTS = {
    "2.27": (("2.26",), _ALIGN_2_27),
    "2.39": (("2.37", "2.38"), _ALIGN_2_39),
    "4.8": (("2.37", "4.7"), _ALIGN_4_8),
    "4.3": (("2.11", "2.18", "2.19", "2.22"), _CTRL_SCHEDULE + "; " + _CTRL_COST),
    "4.4": (("2.19", "2.22"), _CTRL_COST),
    "4.6": (("2.18", "2.37"), _CTRL_PROCUREMENT),
    "4.7": (("2.37",), _CTRL_PROCUREMENT),
}


def form_key(node):
    """Sort key: forms by number, then everything else by name."""
    if FORM_RE.match(node):
        a, b = node.split(".")
        return (0, int(a), int(b), "")
    return (1, 0, 0, node.lower())


def normalise(ref):
    ref = " ".join(ref.split())
    return ALIASES.get(ref, ref)


class Graph:
    def __init__(self):
        self.forms = {}       # number -> knowledge dict
        self.index = {}       # number -> row of forms-index.md
        self.flow = {}        # (src, dst) -> {declarer: what}
        self.align = {}       # (a, b) sorted -> {declarer: what}
        self.self_refs = []   # (form, kind, ref)

    def add_flow(self, src, dst, declarer, what):
        if src == dst:
            self.self_refs.append((declarer, "flow", src))
            return
        self.flow.setdefault((src, dst), {})[declarer] = what

    def add_align(self, a, b, declarer, what):
        if a == b:
            self.self_refs.append((declarer, "alignment", a))
            return
        key = tuple(sorted((a, b), key=form_key))
        self.align.setdefault(key, {})[declarer] = what

    def is_form(self, node):
        return node in self.forms

    def name(self, node):
        if node in self.forms:
            return self.forms[node]["name"]
        row = self.index.get(node)
        return row["name"] if row else node

    def label(self, node):
        if FORM_RE.match(node):
            return f"{node} {self.name(node)}"
        if node in COMPOSITES:
            return f"{node} (composite of {', '.join(COMPOSITES[node]['members'])})"
        return f"{node} (external)"

    def nodes(self):
        found = set(self.forms)
        for s, d in self.flow:
            found.update((s, d))
        for a, b in self.align:
            found.update((a, b))
        return found

    def upstream(self, node):
        return sorted((s for s, d in self.flow if d == node), key=form_key)

    def downstream(self, node):
        return sorted((d for s, d in self.flow if s == node), key=form_key)

    def partners(self, node):
        """Alignment partners as {partner: [(via, {declarer: what})]}.

        A form aligned with a composite is also aligned with each member, and a
        member is aligned with whatever its composite is aligned with.
        """
        out = defaultdict(list)
        mine = {node}
        for comp, info in COMPOSITES.items():
            if node in info["members"]:
                mine.add(comp)
        for (a, b), by in self.align.items():
            for x, y in ((a, b), (b, a)):
                if x in mine:
                    out[y].append((x if x != node else None, by))
        expanded = defaultdict(list)
        for p, items in out.items():
            expanded[p].extend(items)
            if p in COMPOSITES:
                for m in COMPOSITES[p]["members"]:
                    if m != node:
                        expanded[m].extend((p, by) for _, by in items)
        return expanded


def load_index(path):
    """forms-index.md rows: number -> name, group and both page ranges."""
    rows = {}
    if not Path(path).is_file():
        return rows
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 9 and FORM_RE.match(cells[0]):
            rows[cells[0]] = {
                "name": cells[1], "group": cells[3], "kind": cells[4],
                "prose": cells[5], "printed": cells[7],
            }
    return rows


def pages(row):
    """'PDF pages 139-140 (printed pages 128-129)' from an index row."""
    def one(span, word):
        lo, _, hi = span.partition("-")
        return f"{word} {lo}" if not hi or hi == lo else f"{word}s {span}"
    return f"{one(row['prose'], 'PDF page')} ({one(row['printed'], 'printed page')})"


def load_graph(knowledge=KNOWLEDGE, index=INDEX):
    g = Graph()
    g.index = load_index(index)
    for path in sorted(Path(knowledge).glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        g.forms[data["form"]] = data
    for f, data in g.forms.items():
        for r in data.get("receives_from", []):
            g.add_flow(normalise(r["source"]), f, f, r["what"])
        for r in data.get("provides_to", []):
            g.add_flow(f, normalise(r["target"]), f, r["what"])
        for r in data.get("alignment", []):
            g.add_align(f, normalise(r["form"]), f, r["what_must_agree"])
    for comp, info in COMPOSITES.items():
        for m in info["members"]:
            if m in g.forms:
                g.flow.setdefault((m, comp), {}).setdefault(
                    "(book)", f"part of the {comp.lower()} ({info['cite']})")
    return g


def resolve(g, text):
    """A form number (2.32 or 2-32) or the exact name of an external node."""
    t = normalise(text)
    m = re.fullmatch(r"(\d)[-.](\d+)", t)
    if m:
        t = f"{m.group(1)}.{m.group(2)}"
    if t in g.nodes():
        return t
    low = {n.lower(): n for n in g.nodes()}
    return low.get(t.lower())


def docs_for(form, docs_dir):
    """Files in docs/ that hold the form, as paths relative to docs/."""
    docs_dir = Path(docs_dir)
    found = []
    a, b = form.split(".") if FORM_RE.match(form) else (None, None)
    forms_dir = docs_dir / "forms"
    if a and forms_dir.is_dir():
        pat = re.compile(rf"^{a}[-.]{b}-.+\.md$")
        found += [f"forms/{p.name}" for p in sorted(forms_dir.iterdir()) if pat.match(p.name)]
    for name, held in PACKAGES.items():
        if form in held and (docs_dir / name).is_file():
            found.append(name)
    return found


def stand_in_for(form, docs_dir):
    """(file, section) of the package section that stands in for a form with no file of its own, or None."""
    if form in STAND_INS and (Path(docs_dir) / STAND_INS[form][0]).is_file() and not docs_for(form, docs_dir):
        return STAND_INS[form]
    return None


def flow_text(g, src, dst, focus):
    by = g.flow[(src, dst)]
    if focus in by:
        text, who = by[focus], focus
    else:
        who, text = next(iter(by.items()))
    sides = sorted(by, key=form_key)
    if "(book)" in sides:
        tag = "book definition"
    elif len(sides) > 1:
        tag = "declared by both"
    else:
        tag = f"declared only by {sides[0]}"
    return text, who, tag


def show_form(g, node, out):
    out(f"{g.label(node)}" + (f" [{g.forms[node]['process_group']}]" if node in g.forms else ""))
    if node in g.forms and g.forms[node].get("pmbok_processes"):
        out("  PMBOK 6: " + "; ".join(g.forms[node]["pmbok_processes"]))
    for title, others, edge in (
        ("Upstream, receives from", g.upstream(node), lambda o: (o, node)),
        ("Downstream, provides to", g.downstream(node), lambda o: (node, o)),
    ):
        out(f"\n{title} ({len(others)}):")
        for o in others:
            text, who, tag = flow_text(g, *edge(o), node)
            out(f"  {g.label(o)} [{tag}]")
            out(f"      {text}")
    for comp, info in COMPOSITES.items():
        if node in info["members"]:
            out(f"\nAlso through {comp} (the book defines it as {', '.join(info['members'])} together, {info['cite']}):")
            for title, others, edge in (
                ("receives from", g.upstream(comp), lambda o: (o, comp)),
                ("provides to", g.downstream(comp), lambda o: (comp, o)),
            ):
                for o in others:
                    if o in info["members"]:
                        continue
                    text, who, tag = flow_text(g, *edge(o), comp)
                    out(f"  {title} {g.label(o)} [{tag}]")
                    out(f"      {text}")
    extra = skill_links(g, {node: 0})
    if extra:
        out(f"\nAlso, {SKILL_TAG}:")
        for _, why, targets in extra:
            out(f"  {why}: {', '.join(targets)}")
    if node == "3.2":
        out("\nThe book links 3.2 to no other form beyond 4.1 and 4.2. Every decision entry in decisions.md names 3.2 "
            "as the place to record it; that is the team's convention, not a book link.")
    parts = g.partners(node)
    out(f"\nAlignment partners ({len(parts)}):")
    if node in g.forms and not g.forms[node].get("alignment"):
        out("  (the book prints no Alignment section for this form; every partner below is named by the "
            "other form's Alignment section)")
    for p in sorted(parts, key=form_key):
        for via, by in parts[p]:
            who = node if node in by else next(iter(by))
            note = f" (through {via})" if via else ""
            tag = "declared by both" if len(by) > 1 else f"declared only by {next(iter(by))}"
            out(f"  {g.label(p)}{note} [{tag}]")
            out(f"      {by[who]}")
    if node in g.forms and g.forms[node].get("citation"):
        out(f"\nSource: {g.forms[node]['citation']}")
    elif node in COMPOSITES:
        out(f"\nSource: {COMPOSITES[node]['cite']}")


def impact(g, start, depth=None, categories=None):
    """Documents to recheck when `start` changes: {node: (distance, why)} without start.

    `start` is one form or a list of forms changed together. `depth` stops the search that
    many edges from the start forms. `categories` limits the 3.3 Impacts of Change mapping to
    the named categories (None means all)."""
    starts = [start] if isinstance(start, str) else list(start)
    dist = {s: 0 for s in starts}
    why = {}
    queue = deque(starts)
    while queue:
        n = queue.popleft()
        if depth is not None and dist[n] >= depth:
            continue
        for d in g.downstream(n):
            if d not in dist:
                dist[d] = dist[n] + 1
                why[d] = f"{n} provides to it"
                queue.append(d)
    result = {n: (dist[n], why[n]) for n in dist if n not in starts}
    for n in sorted(dist, key=lambda x: (dist[x], form_key(x))):
        for p, items in sorted(g.partners(n).items(), key=lambda kv: form_key(kv[0])):
            if p in COMPOSITES or p in starts or p in dist:
                continue
            if depth is not None and dist[n] + 1 > depth:
                continue
            if p not in result or result[p][0] > dist[n] + 1:
                via = items[0][0]
                note = f" through {via}" if via else ""
                result[p] = (dist[n] + 1, f"must agree with {n}{note}")
    for n, why_text, targets in skill_links(g, dist, categories):
        if depth is not None and dist[n] + 1 > depth:
            continue
        for t in targets:
            if t in starts or t not in g.forms:
                continue
            if t not in result or result[t][0] > dist[n] + 1:
                result[t] = (dist[n] + 1, f"{why_text}; {SKILL_TAG}")
    return result


def skill_links(g, reached, categories=None):
    """Links the skill adds to the book's lists: (form, reason, [target forms]) for each reached form."""
    out = []
    wanted = None if categories is None else {c.lower() for c in categories}
    if "3.3" in reached:
        for cat, forms in IMPACT_CATEGORIES.items():
            if wanted is None or cat.lower() in wanted:
                reason = ("impact analysis names resources and risks (PMBOK 6 section 4.6.2.5, printed page 120 "
                          "(PDF page 159))" if cat == "Resources and risk" else f"3.3 Impacts of Change: {cat}")
                out.append(("3.3", reason, list(forms)))
    for f, text in CHANGE_SOURCES.items():
        if f in reached:
            out.append((f, f"{f}: {text}", ["3.3"]))
    return out


def held_files(g, nodes, docs_dir):
    """{file: [forms it holds among nodes]} for the forms of `nodes` that live in docs/."""
    files = defaultdict(list)
    for n in sorted(nodes, key=form_key):
        if g.is_form(n):
            for f in docs_for(n, docs_dir):
                files[f].append(n)
    return files


def show_impact(g, start, docs_dir, out, depth=None, categories=None):
    starts = [start] if isinstance(start, str) else list(start)
    rows = impact(g, starts, depth, categories)
    limit = f", within {depth} edge{'s' if depth != 1 else ''}" if depth is not None else ""
    names = " and ".join(g.label(s) for s in starts)
    out(f"Recheck when {names} {'changes' if len(starts) == 1 else 'change'} ({len(rows)} documents{limit}):")
    ordered = sorted(rows, key=lambda n: (rows[n][0], form_key(n)))
    for n in ordered:
        d, why = rows[n]
        files = docs_for(n, docs_dir) if g.is_form(n) else []
        stand = stand_in_for(n, docs_dir) if g.is_form(n) else None
        if not g.is_form(n):
            where = "external, no form"
        elif files:
            where = "in docs: " + ", ".join(files)
        elif stand:
            where = f"stand-in section in docs: {stand[0]}, {stand[1]}; content of the form, not the printed form"
        else:
            where = "not in docs"
        out(f"  {d}  {g.label(n)}  [{where}]  ({why})")
    forms = [n for n in ordered if g.is_form(n)]
    files = held_files(g, forms, docs_dir)
    held = sum(1 for n in forms if docs_for(n, docs_dir))
    out(f"\n{held} of {len(forms)} forms exist in docs/, in {len(files)} file{'' if len(files) == 1 else 's'}.")
    for f, held_forms in files.items():
        out(f"  {f} holds {', '.join(held_forms)}")
    stands = [(n, stand_in_for(n, docs_dir)) for n in forms if stand_in_for(n, docs_dir)]
    if stands:
        out(f"{len(stands)} more {'has' if len(stands) == 1 else 'have'} a stand-in section in a package, counted "
            "apart from the forms that exist:")
        for n, (f, section) in stands:
            out(f"  {n} is held as {f}, {section}")
    if forms and not held and not stands:
        out(f"Nothing to compare: none of these {len(forms)} forms exists in docs/. Say so, list them as forms to "
            "create or update later, and do not paste the rows as if they were documents to recheck.")
    elif forms and held + len(stands) < len(forms):
        extra = f" and the {len(stands)} stand-in section{'' if len(stands) == 1 else 's'}" if stands else ""
        out(f"Compare only the {held} that exist{extra}; the other {len(forms) - held - len(stands)} are forms to "
            "create or update later, not documents to recheck. Name every form this output lists, none dropped and "
            "none added.")
    elif forms:
        out("Name every form this output lists, none dropped and none added.")
    for s in starts:
        if s in g.forms:
            ups = sorted(g.upstream(s), key=form_key)
            out(f"{g.label(s)} receives from ({len(ups)}): {', '.join(g.label(u) for u in ups) or 'no recorded source'}. "
                "The rows above run downstream; read these too when the question is what feeds or receives it.")
    mine = held_files(g, starts, docs_dir)
    if mine:
        out("Changed form lives in: " + "; ".join(f"{f} ({', '.join(fs)})" for f, fs in mine.items()))
    if any(s in g.forms for s in starts):
        out("Also record the decision in 3.2 Decision Log (alternatives and reason in Comments). The book links 3.2 "
            "to no other form; recording every decision there is the team's convention (decisions.md, section 3).")
    if any(SKILL_TAG in why for _, why in rows.values()):
        out(f"Rows tagged '{SKILL_TAG}' map the Impacts of Change categories printed on 3.3 to the forms of the "
            f"matching knowledge area ({CATEGORY_CITE}); read each form and keep those the change touches.")


def order_edges(g):
    """Form to form flow edges with composites folded away, as {(a, b): weight}."""
    edges = {}
    for (s, d), by in g.flow.items():
        if g.is_form(s) and g.is_form(d):
            edges[(s, d)] = len(by)
    for comp, info in COMPOSITES.items():
        preds = [s for s, d in g.flow if d == comp and g.is_form(s)]
        succs = [d for s, d in g.flow if s == comp and g.is_form(d)]
        for p in preds:
            for s in succs:
                if p != s and s not in info["members"]:
                    edges.setdefault((p, s), 1)
    return edges


def components(nodes, edges):
    """Strongly connected components (Tarjan), each a sorted list."""
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    idx, low, on, stack, out = {}, {}, set(), [], []

    def visit(v):
        idx[v] = low[v] = len(idx)
        stack.append(v)
        on.add(v)
        for w in sorted(adj[v], key=form_key):
            if w not in idx:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(sorted(comp, key=form_key))

    for v in sorted(nodes, key=form_key):
        if v not in idx:
            visit(v)
    return out


# PMBOK 6 numbers Plan Resource Management 9.1 and Estimate Activity Resources 9.2 after the schedule and
# cost chapters, yet 9.2 produces the resource requirements and the resource breakdown structure that
# Estimate Activity Durations 6.4 takes as inputs (PMBOK 6 section 6.4, printed page 195 (PDF page 234);
# section 9.2, printed pages 320 to 321 (PDF pages 359 to 360)), so --order ranks them with 6.3. The
# mapping is the skill's, not the book's.
PROCESS_ORDER = {(9, 1): (6, 3), (9, 2): (6, 3)}


def process_ranks(g):
    """{form: sort key} giving the process sequence: process group, then the chapter and section of
    the first PMBOK 6 process in pmbok_processes, then the form number. A form with no process
    (2.3, 3.2, 4.8, the agile forms) takes the rank of the nearest lower-numbered form of its
    group that has one."""
    group_pos = {name: i for i, name in enumerate(GROUPS)}
    base = {}
    for f, data in g.forms.items():
        procs = []
        for text in data.get("pmbok_processes", []):
            m = re.match(r"(\d+)\.(\d+)", text)
            if m:
                procs.append((int(m.group(1)), int(m.group(2))))
        if procs:
            base[f] = (group_pos[data["process_group"]],) + PROCESS_ORDER.get(min(procs), min(procs))
    ranks = {}
    for f in sorted(g.forms, key=form_key):
        if f in base:
            ranks[f] = base[f] + (form_key(f),)
            continue
        group = group_pos[g.forms[f]["process_group"]]
        earlier = [x for x in sorted(g.forms, key=form_key)
                   if form_key(x) < form_key(f) and x in base and base[x][0] == group]
        ranks[f] = (earlier and base[earlier[-1]] or (group, 0, 0)) + (form_key(f),)
    return ranks


def break_cycle(comp, edges, ranks=None):
    """Edges of a loop to drop: every link that runs from a form of a later process to a form of an
    earlier one (by `ranks`). What is left runs forward through the process sequence, so it cannot
    loop. Without `ranks`, the form number is the sequence."""
    inside = [e for e in edges if e[0] in comp and e[1] in comp]
    if ranks is None:
        ranks = {n: form_key(n) for n in comp}
    return sorted((e for e in inside if ranks[e[0]] > ranks[e[1]]), key=lambda e: (form_key(e[0]), form_key(e[1])))


def skill_prereq_edges(g):
    """[((source, form), cite)] for the prerequisites ORDER_INPUTS adds to --order."""
    return [((src, f), cite) for f, (sources, cite) in sorted(ORDER_INPUTS.items(), key=lambda kv: form_key(kv[0]))
            if f in g.forms for src in sources if src in g.forms]


def start_forms(g):
    """{form: (when, cite)} for forms whose knowledge file says when the book has them created."""
    return {f: (d["starts"]["when"], d["starts"]["cite"]) for f, d in g.forms.items() if d.get("starts")}


def creation_order(g):
    """(steps, cycles, dropped): steps is [(step, form, prerequisites)].

    A link from a form of a later process to a form of an earlier one is a revision input, never a
    prerequisite, so `dropped` holds all of them; `cycles` lists the loops they would have formed. The
    process sequence is PMBOK 6 order with 9.1 and 9.2 placed before 6.4 (see PROCESS_ORDER). Links into a
    form with a "starts" field are left out too (see start_forms; `revision_inputs` returns them), and
    the prerequisites of ORDER_INPUTS are added for the monitoring forms."""
    all_edges = order_edges(g)
    for e, _why in skill_prereq_edges(g):
        all_edges.setdefault(e, 1)
    starts = start_forms(g)
    edges = {e: w for e, w in all_edges.items() if e[1] not in starts}
    ranks = process_ranks(g)
    nodes = set(g.forms)
    cycles = []
    back = sorted((e for e in edges if ranks[e[0]] > ranks[e[1]]), key=lambda e: (form_key(e[0]), form_key(e[1])))
    for comp in components(nodes, edges):
        if len(comp) > 1:
            cycles.append((comp, sorted((e for e in back if e[0] in comp and e[1] in comp),
                                        key=lambda e: (form_key(e[0]), form_key(e[1])))))
    dropped = sorted(set(back) | {e for e in all_edges if e[1] in starts},
                     key=lambda e: (form_key(e[0]), form_key(e[1])))
    kept = {e: w for e, w in all_edges.items() if e not in set(dropped)}
    pre = defaultdict(set)
    for a, b in kept:
        pre[b].add(a)
    level = {}

    def depth(n):
        if n not in level:
            level[n] = 1 + max((depth(p) for p in pre[n]), default=-1)
        return level[n]

    for n in nodes:
        depth(n)
    steps = [(level[n] + 1, n, sorted(pre[n], key=form_key))
             for n in sorted(nodes, key=lambda n: (level[n], ranks[n]))]
    return steps, cycles, dropped


def revision_inputs(g):
    """{form: [forms]} that provide to a form created at the start of the project."""
    starts = start_forms(g)
    return {f: [s for s in order_sources(g, f)] for f in starts}


def order_sources(g, f):
    return sorted((s for (s, d) in order_edges(g) if d == f), key=form_key)


LATE_GROUPS = {
    "Executing": "the last update before closeout",
    "Monitoring and Controlling": "the last report or review before closeout",
    "Closing": "closeout",
}


def show_order(g, group, out):
    steps, cycles, dropped = creation_order(g)
    starts = start_forms(g)
    revise = revision_inputs(g)
    if group:
        want = [x for x in GROUPS if x.lower().startswith(group.lower())]
        if not want:
            return f"unknown group {group!r}; groups are: {', '.join(GROUPS)}"
        steps = [s for s in steps if g.forms[s[1]]["process_group"] in want]
    out("Creation order from the recorded links (a form comes after the forms it needs; forms with the same "
        "step number are independent). \"needs: nothing from another form\" means the book lists no source for "
        "the form, not that nothing is required; the monitoring forms, and the forms the book only aligns with a "
        "plan (2.27, 2.39, 4.8), list below what they measure against or agree with, as a skill mapping. Loops are cut by process sequence: the form of the earlier PMBOK 6 "
        "process is drafted first and revised once the later one exists, with Plan Resource Management and "
        "Estimate Activity Resources ranked before Estimate Activity Durations because their outputs are inputs "
        "of 6.4. Reports and logs of later groups are produced repeatedly, so their step says when the first "
        "version can exist, not when the last one does.")
    late_header_done = False
    for step, f, pre in sorted(steps, key=lambda s_: g.forms[s_[1]]["process_group"] in LATE_GROUPS):
        need = ", ".join(pre) if pre else "nothing from another form"
        if not pre and f not in starts:
            partners = sorted(g.partners(f), key=form_key)
            if partners:
                need += f" (the book lists no source; it must agree with {', '.join(partners)}, check them)"
        group_name = g.forms[f]["process_group"]
        line = f"  step {step:>2}  {g.label(f)} [{group_name}]  needs: {need}"
        if group_name in LATE_GROUPS:
            if not late_header_done:
                out(f"\nForms of the later groups are not part of the planning sequence above; the step is when a "
                    f"first version can exist, and each is final later ({SKILL_TAG}):")
                late_header_done = True
            line += f"  (first version at step {step}; final version: {LATE_GROUPS[group_name]})"
        if f in starts:
            line += f"  (created at {starts[f][0]}, {starts[f][1]}; revised as these exist: {', '.join(revise[f])})"
        out(line)
    mapped = {f: (srcs, cite) for f, (srcs, cite) in ORDER_INPUTS.items() if f in g.forms}
    if mapped and (not group or any(g.forms[f]["process_group"] in want for f in mapped)):
        out(f"\nPrerequisites added by the skill ({SKILL_TAG}):")
        for f, (srcs, cite) in sorted(mapped.items(), key=lambda kv: form_key(kv[0])):
            out(f"  {f} after {', '.join(srcs)}: {cite}")
    out(f"\nDependency cycles: {len(cycles)}")
    for comp, cut in cycles:
        out(f"  cycle among {len(comp)} forms: {', '.join(comp)}")
        for a, b in cut:
            kind = "declared by both" if len(g.flow[(a, b)]) > 1 else "declared only by " + next(iter(g.flow[(a, b)]))
            out(f"    broke {a} -> {b} ({kind}): {b} is drafted first without {a}, then revised once {a} exists")
    in_loops = {e for _, cut in cycles for e in cut}
    outside = defaultdict(list)
    for a, b in dropped:
        if (a, b) not in in_loops and b not in starts:
            outside[b].append(a)
    if outside:
        out(f"\nLinks from a later process to an earlier one outside any loop ({sum(map(len, outside.values()))}), "
            "also revision inputs, not prerequisites:")
        for b in sorted(outside, key=form_key):
            out(f"  {b} is revised once {', '.join(sorted(outside[b], key=form_key))} exist")
    if dropped:
        out("The cut edges are kept in the graph and in --impact; only the order ignores them.")
    return None


def check(g, out):
    """One-sided links and other disagreements between the files, printed grouped.

    Returns the findings as (missing form, field it should list, form that lists
    it) tuples, plus plain strings for the other problems."""
    one_sided, other = [], []
    refs = {n for n in g.nodes() if FORM_RE.match(n)}
    for n in sorted(refs - set(g.forms), key=form_key):
        other.append(f"{n} is named in the knowledge files but has no knowledge file")
    for (s, d), by in g.flow.items():
        if g.is_form(s) and g.is_form(d) and len(by) == 1:
            who = next(iter(by))
            if who == s:
                one_sided.append((d, "receives_from", s))
            elif who == d:
                one_sided.append((s, "provides_to", d))
    for (a, b), by in g.align.items():
        if g.is_form(a) and g.is_form(b) and len(by) == 1:
            who = next(iter(by))
            one_sided.append((b if who == a else a, "alignment", who))
    for f, kind, ref in g.self_refs:
        other.append(f"{f} lists itself under {kind}")
    for f, row in sorted(g.index.items(), key=lambda kv: form_key(kv[0])):
        if f not in g.forms:
            other.append(f"{f} is in forms-index.md but has no knowledge file")
        elif g.forms[f]["process_group"] != row["group"]:
            other.append(f"{f} is {g.forms[f]['process_group']} in its knowledge file and {row['group']} in forms-index.md")
        elif g.forms[f]["name"] != row["name"]:
            other.append(f"{f} is named {g.forms[f]['name']!r} in its knowledge file and {row['name']!r} in forms-index.md")
    if g.index:
        for f in sorted(set(g.forms) - set(g.index), key=form_key):
            other.append(f"{f} has a knowledge file but is not in forms-index.md")
    titles = {
        "provides_to": "does not list under provides_to, though these list it under receives_from",
        "receives_from": "does not list under receives_from, though these list it under provides_to",
        "alignment": "does not list under alignment, though these list it",
    }
    for field in ("provides_to", "receives_from", "alignment"):
        groups = defaultdict(list)
        for missing, f, lister in one_sided:
            if f == field:
                groups[missing].append(lister)
        count = sum(len(v) for v in groups.values())
        out(f"\n{field}: {count} one-sided links")
        for missing in sorted(groups, key=form_key):
            out(f"  {missing} {titles[field]}: " + ", ".join(sorted(groups[missing], key=form_key)))
    if other:
        out("\nOther:")
        for line in other:
            out(f"  {line}")
    total = len(one_sided) + len(other)
    out(f"\n{total} inconsistencies ({len(one_sided)} one-sided links, {len(other)} other)")
    return one_sided + other


def node_id(n):
    return "n" + re.sub(r"\W", "_", n)


def markdown(g):
    lines = [
        "# Form graph",
        "",
        "How the 66 forms of A Project Manager's Book of Forms (3rd edition) feed each other. Generated by "
        "`scripts/form_graph.py --markdown --out references/form-graph.md` from `references/knowledge/*.json` (each form's receives_from, "
        "provides_to and alignment) and `references/forms-index.md`; do not edit by hand. A link counts when "
        "either form lists it. The knowledge files record where the book is silent: for most links the book "
        "says a form provides to or receives from another, not which fields flow. Run "
        "`form_graph.py <form>` for the wording per link and `form_graph.py --check` for the links only one "
        "side lists. Every link is named in the prose or Alignment section of at least one form; \"declared "
        "only by X\" means the other form's list is silent, a gap in the book's lists and not a finding "
        "against a project. Treat such a link as real when rechecking documents and as weak when ordering "
        "them; the wording of what flows is sometimes a reading, and says so.",
        "",
        "Page numbers are the form's prose pages, the section that holds the Alignment and the "
        "information-flow paragraphs, as PDF page (printed page); PDF page = printed page + 11.",
        "",
        "Documents the book names without a form number (the charter's inputs, business case, agreements, "
        "project budget, schedule baseline and others) appear as plain names and are listed in the last section. "
        "The scope baseline is the one composite: the book defines it as 2.8, 2.9 and 2.10 together "
        f"({COMPOSITES['Scope baseline']['cite']}), so a form that receives from or aligns with it is linked to "
        "each of the three.",
        "",
    ]

    def join(items):
        return ", ".join(items) if items else ""

    for group in GROUPS:
        members = [f for f in sorted(g.forms, key=form_key) if g.forms[f]["process_group"] == group]
        if not members:
            continue
        lines += [f"## {group}", "",
                  "| Form | Name | Receives from | Provides to | Aligned with | Book pages |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for f in members:
            row = g.index.get(f)
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                f, g.name(f), join(g.upstream(f)), join(g.downstream(f)),
                join(sorted(g.partners(f), key=form_key)), pages(row) if row else ""))
        lines.append("")

    planning = [f for f in sorted(g.forms, key=form_key) if g.forms[f]["process_group"] == "Planning"]
    inside = set(planning)
    lines += ["## Planning flowchart", "",
              "Planning forms only; an arrow means the first form provides to the second. Links to and from "
              "forms of other groups, external documents and alignment are in the tables above.", "",
              "```mermaid", "flowchart LR"]
    for f in planning:
        lines.append(f'  {node_id(f)}["{f} {g.name(f)}"]')
    for (s, d) in sorted(g.flow, key=lambda e: (form_key(e[0]), form_key(e[1]))):
        if s in inside and d in inside:
            lines.append(f"  {node_id(s)} --> {node_id(d)}")
    lines += ["```", ""]

    steps, cycles, dropped = creation_order(g)
    lines += ["## Dependency cycles", ""]
    if not cycles:
        lines.append("None.")
    else:
        lines.append("Some forms depend on each other in a loop. `form_graph.py --order` cuts every link that runs "
                     "from a form of a later PMBOK 6 process to a form of an earlier one (process group, then "
                     "chapter and section, then form number; 9.1 and 9.2 rank before 6.4 because their outputs are "
                     "inputs of 6.4), so the earlier form is drafted first and revised "
                     "once the later one exists. Forms the book says are created at the start of the project "
                     "(2.32, 2.33, 3.1, 3.2) take their incoming links as revision inputs. The cut links stay "
                     "in the tables above. The loops and the links cut inside them:")
        lines.append("")
        for comp, cut in cycles:
            lines.append(f"- Loop among {len(comp)} forms: {', '.join(comp)}. Cut: "
                         + "; ".join(f"{a} to {b}" for a, b in cut) + ".")
    lines.append("")
    external = defaultdict(lambda: {"in": set(), "out": set(), "align": set()})
    for (s, d) in g.flow:
        if not FORM_RE.match(s):
            external[s]["out"].add(d)
        if not FORM_RE.match(d):
            external[d]["in"].add(s)
    for (a, b) in g.align:
        for x, y in ((a, b), (b, a)):
            if not FORM_RE.match(x):
                external[x]["align"].add(y)
    lines += ["## Documents named without a form number", "",
              "| Document | Feeds | Fed by | Aligned with |", "| --- | --- | --- | --- |"]
    for n in sorted(external, key=form_key):
        e = external[n]
        lines.append(f"| {n} | {join(sorted(e['out'], key=form_key))} | {join(sorted(e['in'], key=form_key))} | "
                     f"{join(sorted(e['align'], key=form_key))} |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("form", nargs="?", help="form number such as 2.32 or 2-32, or an external name such as 'Scope baseline'")
    ap.add_argument("--impact", metavar="FORM", nargs="+", help="forms to recheck when FORM (or several forms together) changes")
    ap.add_argument("--category", nargs="+", metavar="CATEGORY",
                    help="with --impact 3.3, only these Impacts of Change categories: "
                         + ", ".join(IMPACT_CATEGORIES))
    ap.add_argument("--depth", type=int, help="with --impact, stop this many edges from the changed form")
    ap.add_argument("--order", action="store_true", help="creation order consistent with the dependencies")
    ap.add_argument("--group", help="with --order, only this process group (prefix is enough)")
    ap.add_argument("--check", action="store_true", help="list links that only one side declares")
    ap.add_argument("--markdown", action="store_true", help="print the form graph as Markdown")
    ap.add_argument("--out", help="with --markdown, write the text to this file instead of printing it "
                                  "(the committed copy is references/form-graph.md)")
    ap.add_argument("--knowledge", default=KNOWLEDGE, help="directory of form JSON files")
    ap.add_argument("--index", default=INDEX, help="forms-index.md")
    ap.add_argument("--docs", default=DOCS, help="the docs/ directory")
    args = ap.parse_args(argv)

    if args.impact and args.form:
        args.impact = [args.form] + args.impact
        args.form = None
    modes = [bool(args.form), bool(args.impact), args.order, args.check, args.markdown]
    if sum(modes) != 1:
        ap.error("give exactly one of: a form, --impact FORM, --order, --check, --markdown")
    if args.out and not args.markdown:
        ap.error("--out goes with --markdown")
    if args.group and not args.order:
        ap.error("--group goes with --order")
    if args.depth is not None and (not args.impact or args.depth < 1):
        ap.error("--depth goes with --impact and must be at least 1")
    if args.category and not args.impact:
        ap.error("--category goes with --impact")
    if args.category:
        bad = [c for c in args.category if c.lower() not in {k.lower() for k in IMPACT_CATEGORIES}]
        if bad:
            ap.error(f"unknown category {bad[0]!r}; categories are: {', '.join(IMPACT_CATEGORIES)}")
    if not Path(args.knowledge).is_dir():
        print(f"no such directory: {args.knowledge}", file=sys.stderr)
        return 2
    g = load_graph(args.knowledge, args.index)

    def out(text=""):
        print(text)

    if args.form or args.impact:
        wanted = [args.form] if args.form else args.impact
        nodes = []
        for text in wanted:
            node = resolve(g, text)
            if node is None:
                print(f"unknown form or document: {text}", file=sys.stderr)
                return 2
            nodes.append(node)
        if args.impact:
            show_impact(g, nodes, args.docs, out, args.depth, args.category)
        else:
            show_form(g, nodes[0], out)
        return 0
    if args.order:
        problem = show_order(g, args.group, out)
        if problem:
            print(problem, file=sys.stderr)
            return 2
        return 0
    if args.check:
        return 1 if check(g, out) else 0
    text = markdown(g)
    if not args.out or args.out == "-":
        sys.stdout.write(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
