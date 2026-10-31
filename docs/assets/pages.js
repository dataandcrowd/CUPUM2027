// Per-page logic. Each page's function runs when its root element exists.
(function () {
  const $ = (s) => document.querySelector(s);
  const pct = (x, d = 0) => `${x > 0 ? "+" : ""}${(100 * x).toFixed(d)}%`;
  const RULE = () => CL.css("--rule"), LLM = () => CL.css("--llm"), BASE = () => CL.css("--base");
  const MODES = () => [["Car", CL.css("--car")], ["PT", CL.css("--pt")], ["Home", CL.css("--wfh")]];
  const DAYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
  const BASE_DAYS = [2, 3, 4, 5], CHARGED = [6, 7, 8, 9, 10];
  const modeCounts = (run, d) => [0, 1, 2].map((m) => run.mode[d - 1].filter((x) => x === m).length);
  const modeStack = (el, run, title) => CL.stack(el, {
    cats: DAYS, mark: 5, yLabel: title, legend: true,
    series: MODES().map(([name, color], m) => ({ name, color, values: DAYS.map((_, i) => modeCounts(run, i + 1)[m]) })),
  });

  // ------------------------------------------------------------ overview
  async function index() {
    const [rc, hc] = await Promise.all([CL.load("run_rclock"), CL.load("run_hclock")]);
    $("#flow").innerHTML = flowSVG();
    const rp = new CL.Replay($("#hero-replay"), {
      panels: [{ label: "Formula (R-clock)", color: RULE(), run: rc }, { label: "AI (H-clock)", color: LLM(), run: hc }],
      day: 8, start: 420, autoplay: true, speed: 20, aspect: 1.0,
      onDay: (d) => CL.bars($("#c-cross"), { cats: CL.binLabels, every: 4, shade: [8, 12], yLabel: "cars per 15 minutes",
        series: [{ name: "Formula", color: RULE(), values: CL.crossings(rc, [d]) }, { name: "AI", color: LLM(), values: CL.crossings(hc, [d]) }] }),
      onSelect: (a) => (location.href = `replay.html#agent=${a}`),
    });
    await rp.init();
    modeStack($("#c-mode-r"), rc, "Formula: people");
    modeStack($("#c-mode-h"), hc, "AI: people");
    headlineTiles($("#result-tiles"), rc, hc);
  }
  function headlineTiles(el, rc, hc) {
    const r = CL.summary(rc), h = CL.summary(hc);
    const calls = (run) => run.calls.rule + (run.calls.llm || 0);
    el.innerHTML = [
      [pct(r.response), "fewer cars entering the centre with the formula deciding (mornings 6 to 10 vs 2 to 5)"],
      [pct(h.response), "fewer cars with the AI deciding"],
      [`${r.base.delay.toFixed(1)} → ${r.charged.delay.toFixed(1)}`, "minutes lost to traffic and queuing per car trip, before and after, with the formula"],
      [`${h.base.delay.toFixed(1)} → ${h.charged.delay.toFixed(1)}`, "the same, with the AI"],
      [`${Math.round(r.base.late)} → ${Math.round(r.charged.late)}`, "people late for work each morning, with the formula"],
      [`${Math.round(h.base.late)} → ${Math.round(h.charged.late)}`, "people late for work each morning, with the AI"],
      [`${(calls(hc)).toLocaleString()}`, `decisions in ten mornings thanks to the alarm clock, out of 9,500 person-mornings (${hc.calls.llm} of them by the AI); the old way needs 9,200`],
    ].map(([b, s]) => `<div class="tile"><b>${b}</b><span>${s}</span></div>`).join("");
  }
  function flowSVG() {
    const box = (x, y, w, h, t, lines, cls = "") => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" fill="var(--sunk)" stroke="var(--line-strong)" ${cls}/>
      <text x="${x + 12}" y="${y + 24}" class="t">${t}</text>${lines.map((l, i) => `<text x="${x + 12}" y="${y + 46 + i * 18}" class="m">${l}</text>`).join("")}`;
    const arrow = (d) => `<path d="${d}" fill="none" stroke="var(--ink-2)" stroke-width="1.5" marker-end="url(#ah)"/>`;
    return `<svg class="flow" viewBox="0 0 980 330" role="img" aria-label="One simulated morning: the menu, the alarm, thinking or doing the usual, the traffic, the memory">
      <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--ink-2)"/></marker></defs>
      ${box(10, 60, 180, 112, "1  The menu", ["drive (at which time?),", "bus or train, or home;", "with yesterday's traffic,", "charge and costs"])}
      ${box(230, 60, 200, 112, "2  Did an alarm ring?", ["new charge, late", "yesterday, train", "disrupted, drive odd,", "usual choice gone"])}
      ${box(480, 20, 230, 126, "3  Stop and think", ["the formula: cheapest", "option, time counted as money", "or the AI: reads the story,", "answers with a new routine", "and a reason"])}
      ${box(480, 186, 230, 74, "Do the usual", ["most mornings:", "no thinking needed"])}
      ${box(760, 100, 210, 92, "4  The morning happens", ["slow roads, jammed", "motorways, a queue", "at the gate"])}
      ${box(230, 230, 200, 80, "5  Remember it", ["how long, how late,", "what it cost"])}
      ${arrow("M190 116 L226 116")}${arrow("M430 100 L476 85")}<text x="440" y="80" class="m" font-style="italic">yes</text>
      ${arrow("M430 140 L476 200")}<text x="440" y="178" class="m" font-style="italic">no</text>
      ${arrow("M710 90 L756 130")}${arrow("M710 222 L740 222 L740 160 L756 160")}
      ${arrow("M865 192 L865 270 L434 270")}${arrow("M230 270 L100 270 L100 176")}<text x="110" y="250" class="m" font-style="italic">next morning</text>
      <path d="M100 60 L100 10 L600 10 L600 16" fill="none" stroke="var(--ink-3)" stroke-dasharray="4 3" marker-end="url(#ah)"/><text x="300" y="6" class="m" font-style="italic" font-size="12">the old way: skip the alarm, everyone decides every morning</text>
    </svg>`;
  }

  // ------------------------------------------------------------ how it works
  async function model() {
    const [g, site, rc, hc, rd] = await Promise.all([CL.geometry(), CL.load("site"), CL.load("run_rclock"), CL.load("run_hclock"), CL.load("run_rdaily")]);
    const c = g.agents.cols, n = g.n, ink = CL.css("--ink-2");
    const hist = (el, vals, edges, title, fmt = (x) => x) => {
      const counts = edges.slice(0, -1).map((e, i) => vals.filter((v) => v >= e && v < edges[i + 1]).length);
      CL.bars(el, { cats: edges.slice(0, -1).map(fmt), every: Math.ceil(edges.length / 6), yLabel: title, series: [{ name: title, color: ink, values: counts }] });
    };
    const cat = (el, vals, labels, title) => CL.bars(el, { cats: labels, yLabel: title, series: [{ name: title, color: ink, values: labels.map((_, i) => vals.filter((v) => v === i).length) }] });
    hist($("#p-vot"), c.vot, [0, 4, 8, 12, 16, 20, 24, 28, 32, 40, 60], "Value of time, NZ$/h", (x) => `${x}`);
    cat($("#p-arch"), c.archetype.map((x) => x - 1), ["Hybrid", "On-site", "Shift", "Trades", "Student"], "Archetype");
    cat($("#p-corr"), c.corridor_id, CL.corridorNames, "Corridor");
    hist($("#p-tstar"), c.tstar_min, [420, 450, 480, 510, 540, 570, 600, 601], "Work start", CL.time);
    CL.bars($("#p-traits"), { cats: ["1", "2", "3", "4", "5"], yLabel: "Disposition level", series: [["H", "--rule"], ["F", "--llm"], ["P", "--pt"], ["S", "--wfh"]].map(([k, col]) => ({ name: k, color: CL.css(col), values: [1, 2, 3, 4, 5].map((l) => c[k].filter((v) => v === l).length) })) });
    hist($("#p-wtp"), c.wtp_fee.map((v, i) => (c.company_car[i] || v == null ? 999 : v)), [0, 3, 6, 9, 12, 18, 30, 60, 1000], "Most it would pay, NZ$", (x) => (x >= 1000 ? "" : `${x}`));

    // cost explorer
    const ce = new CostExplorer(g, site);
    const draw = () => {
      const a = Math.min(949, Math.max(0, +$("#ce-agent").value || 0)), fee = +$("#ce-fee").value;
      $("#ce-fee-v").textContent = fee;
      $("#ce-persona").innerHTML = CL.personaHTML(c, a) + CL.traitsHTML(c, a);
      const opts = ce.options(a, fee);
      const best = opts.filter((o) => o.offered).reduce((x, y) => (y.gc < x.gc ? y : x));
      CL.bars($("#ce-chart"), { cats: opts.map((o) => o.label), yLabel: "generalised cost, NZ$", margin: { b: 40 },
        series: [{ name: "cost", color: ink, values: opts.map((o) => o.gc) }], fmt: (v) => `NZ$${v.toFixed(2)}` });
      const svg = $("#ce-chart svg");
      [...svg.querySelectorAll("rect[rx]")].forEach((r, i) => {
        const o = opts[i];
        if (!o) return;
        r.setAttribute("fill", !o.offered ? CL.css("--line") : o.id === best.id ? CL.css("--rule") : o.standing ? CL.css("--ink") : ink);
      });
      [...svg.querySelectorAll("rect[fill=transparent]")].forEach((h, i) => {
        const o = opts[i];
        h.addEventListener("mousemove", (ev) => CL.showTip(ev, `<b>${o.label}</b> ${o.offered ? "" : "(not offered: charged above what this commuter would pay)"}<br>` +
          Object.entries(o.parts).filter(([, v]) => v).map(([k, v]) => `${k}: NZ$${v.toFixed(2)}`).join("<br>") + `<br><b>total NZ$${o.gc.toFixed(2)}</b>`));
      });
      const stand = opts.find((o) => o.standing);
      $("#ce-note").textContent = `Routine: ${stand ? stand.label : "none"}. Lowest cost at this charge: ${best.label} (blue${stand && stand.id !== best.id ? "; the routine is black" : ""})${opts.some((o) => !o.offered) ? "; grey options are not offered at this charge" : ""}. The rule then adds Gumbel noise (scale NZ$0.50), so the lowest-cost option is chosen most often, not always. Hover a bar for the parts.`;
    };
    $("#ce-agent").addEventListener("input", draw);
    $("#ce-fee").addEventListener("input", draw);
    $("#ce-random").addEventListener("click", () => { $("#ce-agent").value = Math.floor(Math.random() * 950); draw(); });
    draw();
    // self-check against the Python values of morning 6
    CL.load("cost_check").then((chk) => {
      let worst = 0, cnt = 0, where = "";
      for (let a = 0; a < n; a++) for (const o of ce.options(a, 6)) {
        const py = chk.gc[a][o.id];
        if (py == null) continue;
        cnt++;
        const d = Math.abs(py - o.gc);
        if (d > worst) { worst = d; where = `commuter ${a}, ${o.id}`; }
      }
      $("#ce-note").insertAdjacentHTML("afterend", `<p class="small muted">Self-check: ${cnt.toLocaleString()} options of ${n} commuters recomputed here against the Python values of morning 6; largest difference NZ$${worst.toExponential(1)}${worst > 0.005 ? ` (${where})` : ""}.</p>`);
    });

    // who was woken
    const woken = (el, run, title, keys) => CL.stack(el, { cats: DAYS, mark: 5, yLabel: title, legend: true,
      series: keys.map(([k, name, col]) => ({ name, color: col, values: run.days.map((d) => d.calls[k] || 0) })) });
    woken($("#w-rdaily"), rd, "Formula every day", [["rule", "Formula", RULE()], ["forced", "Only the bus left, no decision", CL.css("--ink-3")]]);
    woken($("#w-rclock"), rc, "Formula, alarm only", [["rule", "Formula", RULE()], ["forced", "Only the bus left", CL.css("--ink-3")]]);
    woken($("#w-hclock"), hc, "AI, alarm only", [["rule", "Formula (morning 1)", RULE()], ["llm", "AI", LLM()], ["forced", "Only the bus left", CL.css("--ink-3")]]);
    const trig = {};
    rc.decisions.forEach((r) => r[4].split(";").filter(Boolean).forEach((t) => (trig[t] = (trig[t] || 0) + 1)));
    const tk = Object.keys(trig).sort();
    CL.bars($("#w-trig"), { cats: tk.map((t) => ({ T2: "T2 the charge changed", T3: "T3 late yesterday", T4: "T4 train disrupted", T5: "T5 drive not as expected", T6: "T6 usual choice gone" }[t] || t)), yLabel: "Which alarm rang (formula version, after morning 1)", series: [{ name: "wakes", color: ink, values: tk.map((t) => trig[t]) }] });
    const ex = (run, who) => run.decisions.find((r) => r[2] === who && r[1] === 6 && r[5].length > 80);
    $("#rule-example").textContent = `“${ex(rc, "rule")[5]}”`;
    $("#llm-example").textContent = `“${ex(hc, "llm")[5]}”`;

    // fee and road charts
    const fee = site.fee_table;
    CL.lines($("#t-fee"), { series: [{ name: "charge", color: ink, points: Array.from({ length: 300 }, (_, i) => [330 + i, fee[330 + i]]) }], xFmt: CL.time, xTicks: [360, 420, 480, 540, 600], yLabel: "NZ$ per entry", yMax: 7, yFmt: (v) => `NZ$${v.toFixed(2)}` });
    const grid = g.agents.cost.grid, road = g.agents.cost.road;
    CL.lines($("#t-road"), { series: [{ name: "road delay", color: ink, points: grid.map((d, j) => [d, CL.mean(road.map((r) => r[j]))]) }], xFmt: CL.time, xTicks: [360, 420, 480, 540, 585], yLabel: "minutes over free flow (mean)", yFmt: (v) => `${v.toFixed(1)} min` });
  }

  // The generalised cost of options.py, in JavaScript, for the state of morning 6.
  class CostExplorer {
    constructor(g, site) { this.g = g; this.s = site; this.cost = g.agents.cost; this.c = g.agents.cols; }
    feeAt(minute, peak) { const t = this.s.fee_table; return Math.round(t[Math.min(Math.max(minute, 0), t.length - 1)] * peak / 6 * 1e4) / 1e4; }
    roundHalf(x) { return Math.floor(Math.abs(x) + 0.5) * (x >= 0 ? 1 : -1); }
    publicDelay(cor, gate) {
      const pts = this.cost.pub_delay[cor] || [], h = this.s.costs.bin / 2;
      if (!pts.length) return 0;
      const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
      if (gate < xs[0] - h || gate > xs[xs.length - 1] + h) return 0;
      if (gate <= xs[0]) return ys[0];
      if (gate >= xs[xs.length - 1]) return ys[ys.length - 1];
      let i = 1;
      while (xs[i] < gate) i++;
      return ys[i - 1] + (ys[i] - ys[i - 1]) * (gate - xs[i - 1]) / (xs[i] - xs[i - 1]);
    }
    sched(arr, start, phiS, a) { const early = Math.max(0, start - arr), late = Math.max(0, arr - start); return phiS * a * (this.s.costs.beta * early + this.s.costs.gamma * late); }
    options(a, peak) {
      const c = this.c, s = this.s, tr = s.traits, cst = s.costs;
      const vot = c.vot[a], va = vot / 60, phi = tr.phi[c.F[a] - 1], omega = tr.omega[c.P[a] - 1], eta = tr.eta[c.S[a] - 1], k = tr.kappa_h[c.H[a] - 1];
      const phiS = phi * c.sched_mult[a], tstar = c.tstar_min[a], early = c.early_shift_ok[a] && cst.early_start < tstar ? cst.early_start : null;
      const standing = this.cost.standing[a], ref = this.cost.ref_fee[a], ema = this.cost.ema[a];
      const toGate = c.fftt_to_gate_min[a], toDest = c.fftt_gate_to_dest_min[a], total = toGate + toDest, cor = c.corridor_id[a];
      const cfee = c.company_car[a] ? 0 : 1, wtp = c.company_car[a] || c.wtp_fee[a] == null ? Infinity : c.wtp_fee[a];
      const out = [], habit = (id) => (standing == null || id === standing ? 0 : k);
      const hasAlt = this.cost.opts[a].some((id) => !id.startsWith("CAR_"));
      for (const id of this.cost.opts[a]) {
        if (id.startsWith("CAR_")) {
          const d = +id.slice(4, 6) * 60 + +id.slice(6, 8), j = this.cost.grid.indexOf(d);
          const R = j >= 0 ? this.cost.road[a][j] : 0, gate = d + toGate + Math.floor(R + 0.5);
          const D = this.publicDelay(cor, gate) * ema, x = gate + this.roundHalf(D), arr = x + toDest;
          let sc = this.sched(arr, tstar, phiS, va), start = tstar;
          if (early != null) { const s1 = this.sched(arr, early, phiS, va) + cst.early_cost * phi; if (s1 < sc) { sc = s1; start = early; } }
          const f = this.feeAt(x, peak);
          const parts = { "travel time": va * (total + R + D), "arrival time": sc, "charge": cfee * (f + eta * Math.max(0, f - ref)), parking: c.parking_cost[a], fuel: c.fuel_cost[a], habit: habit(id) };
          out.push({ id, label: `Drive ${CL.time(d)}${start !== tstar ? " (07:00 start)" : ""}`, parts, gc: Object.values(parts).reduce((p, q) => p + q, 0), standing: id === standing, offered: !hasAlt || f <= wtp });
        } else if (id === "PT") {
          const tpt = c.pt_time_min[a], hw = cst.headway, rt = this.roundHalf(tpt);
          const svc = (start) => { const dep = hw * Math.floor((start - rt) / hw); return [dep, dep + rt]; };
          let [, arr] = svc(tstar), sc = this.sched(arr, tstar, phiS, va);
          if (early != null) { const [, arrE] = svc(early); const sE = this.sched(arrE, early, phiS, va) + cst.early_cost * phi; if (sE < sc) sc = sE; }
          const parts = { "PT trip (time, attitude, fare)": omega * (va * tpt + cst.pap) + c.pt_fare[a], "arrival time": sc, habit: habit("PT") };
          out.push({ id, label: "Take PT", parts, gc: Object.values(parts).reduce((p, q) => p + q, 0), standing: standing === "PT", offered: true });
        } else if (id === "WFH") {
          const parts = { "working from home": cst.wfh * phi + va * total + c.parking_cost[a] + c.fuel_cost[a], habit: habit("WFH") };
          out.push({ id, label: "Work from home", parts, gc: Object.values(parts).reduce((p, q) => p + q, 0), standing: standing === "WFH", offered: true });
        }
      }
      return out;
    }
  }

  // ------------------------------------------------------------ replay
  async function replay() {
    const g = await CL.geometry();
    const arms = { rdaily: ["Formula daily (R-daily)", BASE], rclock: ["Formula (R-clock)", RULE], hclock: ["AI (H-clock)", LLM] };
    const runs = {};
    const get = (k) => (runs[k] ||= CL.load(`run_${k}`));
    const panelsFor = async () => {
      const scn = $("#rp-scn").value, keys = $("#rp-arms").value.split(",");
      const rs = await Promise.all(keys.map((k) => get(k + scn)));
      return keys.map((k, i) => ({ key: k, label: arms[k][0], color: arms[k][1](), run: rs[i] }));
    };
    let panels = await panelsFor();
    const agentUI = (a) => {
      $("#rp-agent").value = a;
      $("#rp-persona").innerHTML = CL.personaHTML(g.agents.cols, a) + CL.traitsHTML(g.agents.cols, a);
      CL.dayStrip($("#rp-strip"), a, panels.map((p) => ({ label: p.label.split(" ")[0], run: p.run })));
      CL.reasonList($("#rp-reasons"), a, panels.map((p) => ({ tag: p.label, cls: p.key === "hclock" ? "l" : "r", run: p.run })));
    };
    const charts = (day) => {
      const minutes = Array.from({ length: 311 }, (_, i) => 330 + i);
      CL.lines($("#rp-queue"), { xFmt: CL.time, xTicks: [360, 420, 480, 540, 600], yLabel: "people queuing at a gate",
        series: panels.map((p) => ({ name: p.label, color: p.color, points: minutes.map((t) => [t, p.run.gate_arrive[day - 1].reduce((s, ga, a) => s + (p.run.mode[day - 1][a] === 0 && ga <= t && t < p.run.gate_exit[day - 1][a] ? 1 : 0), 0)]) })) });
      CL.bars($("#rp-cross"), { cats: CL.binLabels, every: 4, shade: [8, 12], yLabel: "cars per 15 minutes", series: panels.map((p) => ({ name: p.label, color: p.color, values: CL.crossings(p.run, [day]) })) });
    };
    const rp = new CL.Replay($("#rp-replay"), { panels, day: 8, start: 400, speed: 10, onSelect: agentUI, onDay: charts });
    await rp.init();
    const reload = async () => { panels = await panelsFor(); rp.setPanels(panels); agentUI(+$("#rp-agent").value); };
    $("#rp-scn").addEventListener("change", reload);
    $("#rp-arms").addEventListener("change", reload);
    $("#rp-agent").addEventListener("change", () => rp.select(Math.min(949, Math.max(0, +$("#rp-agent").value || 0))));
    $("#rp-random").addEventListener("click", () => rp.select(Math.floor(Math.random() * 950)));
    $("#rp-differ").addEventListener("click", () => {
      const [p, q] = panels;
      const cand = [];
      for (let a = 0; a < g.n; a++) if (CHARGED.some((d) => p.run.mode[d - 1][a] !== q.run.mode[d - 1][a] || p.run.depart[d - 1][a] !== q.run.depart[d - 1][a])) cand.push(a);
      rp.select(cand[Math.floor(Math.random() * cand.length)]);
    });
    const m = location.hash.match(/agent=(\d+)/);
    rp.select(m ? +m[1] : 6);
  }

  // ------------------------------------------------------------ run it yourself
  async function run() {
    const [g, site, rc] = await Promise.all([CL.geometry(), CL.load("site"), CL.load("run_rclock")]);
    const w = new Worker("assets/sim/worker.js", { type: "module" });
    const status = $("#rn-status"), bar = $("#rn-bar"), go = $("#rn-go");
    let running = false, replayObj = null, last = null;
    const settings = () => ({ arm: $("#rn-arm").value, seed: +$("#rn-seed").value, peak_fee: +$("#rn-fee").value, traits: $("#rn-traits").value,
      pt: +$("#rn-pt").value, overrides: +$("#rn-pt").value ? { "events.pt_disruption_day": [3, 8] } : {} });
    w.onmessage = async (ev) => {
      const m = ev.data;
      if (m.type === "status") status.textContent = m.text + "…";
      else if (m.type === "ready") { status.textContent = `Ready: ${m.versions} in your browser.`; go.disabled = false; go.textContent = "Run ten mornings"; }
      else if (m.type === "day") { bar.style.width = `${m.day * 10}%`; status.textContent = `Simulating morning ${m.day} of 10…`; }
      else if (m.type === "error") { status.textContent = "Error: " + m.text; running = false; go.disabled = false; }
      else if (m.type === "result") { running = false; go.disabled = false; bar.style.width = "100%"; await show(m.result); }
    };
    go.addEventListener("click", () => { if (running) return; running = true; go.disabled = true; bar.style.width = "0"; w.postMessage(settings()); });
    async function show(r) {
      last = r;
      r.decisions = []; r.disruption_corridor = r.settings.pt ? r.disruption_corridor : null;
      const s = r.settings, key = `${s.arm}|${s.seed}|${s.peak_fee}|${s.traits}|${s.pt}`, stored = site.fingerprints[key];
      const sm = CL.summary(r);
      status.textContent = `Done in ${r.seconds} seconds.`;
      $("#rn-out").hidden = false;
      $("#rn-tiles").innerHTML = [
        [pct(sm.response), "cars entering the centre, mornings 6 to 10 vs 2 to 5"],
        [`${(sm.base.cars / g.n).toFixed(2)} → ${(sm.charged.cars / g.n).toFixed(2)}`, "share driving"],
        [`${(sm.base.pt / g.n).toFixed(2)} → ${(sm.charged.pt / g.n).toFixed(2)}`, "share on the bus or train"],
        [`${sm.base.delay.toFixed(1)} → ${sm.charged.delay.toFixed(1)}`, "minutes lost per car trip, before and after"],
        [r.woken.reduce((a, b) => a + b, 0).toLocaleString(), "times someone stopped to think, in ten mornings"],
      ].map(([b, t]) => `<div class="tile"><b>${b}</b><span>${t}</span></div>`).join("");
      $("#rn-check").textContent = stored ? (stored.fp === r.fingerprint ? `Identical to the researchers' stored run ${stored.run}: every person's choice, departure and gate-crossing minute matched.`
        : `Differs from the researchers' stored run ${stored.run} (fingerprint ${r.fingerprint} vs ${stored.fp}).`) : "The researchers did not store a run with these settings, so there is nothing to compare with. You are in new territory.";
      modeStack($("#rn-mode"), r, "agents");
      CL.bars($("#rn-woken"), { cats: DAYS, yLabel: "people who stopped to think", series: [{ name: "decisions", color: RULE(), values: r.woken }] });
      CL.bars($("#rn-cross"), { cats: CL.binLabels, every: 4, shade: [8, 12], yLabel: "cars per 15 minutes", series: [{ name: "mornings 2 to 5", color: CL.css("--ink-3"), values: CL.crossings(r, BASE_DAYS) }, { name: "mornings 6 to 10", color: RULE(), values: CL.crossings(r, CHARGED) }] });
      CL.bars($("#rn-delay"), { cats: CL.binLabels, every: 4, shade: [8, 12], yLabel: "minutes per car trip", series: [{ name: "mornings 2 to 5", color: CL.css("--ink-3"), values: CL.delayBins(r, BASE_DAYS) }, { name: "mornings 6 to 10", color: RULE(), values: CL.delayBins(r, CHARGED) }], fmt: (v) => `${v.toFixed(1)} min` });
      const label = `${s.arm}, seed ${s.seed}, NZ$${s.peak_fee}${s.traits === "off" ? ", traits off" : ""}${s.pt ? ", PT disruption" : ""}`;
      if (!replayObj) { replayObj = new CL.Replay($("#rn-replay"), { panels: [{ label, color: RULE(), run: r }], day: 8, start: 420, speed: 10, aspect: 0.8 }); await replayObj.init(); }
      else replayObj.setPanels([{ label, color: RULE(), run: r }]);
      $("#rn-table tbody").insertAdjacentHTML("afterbegin", `<tr><td>${s.arm}</td><td>${s.seed}</td><td class="n">${s.peak_fee}</td><td>${s.traits}</td><td>${s.pt ? "d3, d8" : "none"}</td><td class="n">${(sm.base.cars / g.n).toFixed(3)}</td><td class="n">${(sm.charged.cars / g.n).toFixed(3)}</td><td class="n">${pct(sm.response, 1)}</td><td class="n">${sm.base.delay.toFixed(2)}</td><td class="n">${sm.charged.delay.toFixed(2)}</td><td class="n">${r.woken.reduce((a, b) => a + b, 0)}</td><td>${stored ? (stored.fp === r.fingerprint ? "yes" : "no") : "no stored run"}</td></tr>`);
    }
  }

  // ------------------------------------------------------------ results
  async function results() {
    const [g, rc, hc, rcp, hcp] = await Promise.all([CL.geometry(), CL.load("run_rclock"), CL.load("run_hclock"), CL.load("run_rclock_pt"), CL.load("run_hclock_pt")]);
    headlineTiles($("#rs-tiles"), rc, hc);
    const diff = (f) => ({ r: f(rc, CHARGED).map((v, i) => v - f(rc, BASE_DAYS)[i]), h: f(hc, CHARGED).map((v, i) => v - f(hc, BASE_DAYS)[i]) });
    const dc = diff(CL.crossings), dd = diff(CL.delayBins);
    CL.bars($("#rs-cross"), { cats: CL.binLabels, every: 4, shade: [8, 12], yLabel: "cars per 15 minutes, change", series: [{ name: "Formula (R-clock)", color: RULE(), values: dc.r }, { name: "AI (H-clock)", color: LLM(), values: dc.h }], fmt: (v) => `${v > 0 ? "+" : ""}${Math.round(v)} cars` });
    CL.bars($("#rs-delay"), { cats: CL.binLabels, every: 4, shade: [8, 12], yLabel: "minutes per car trip, change", series: [{ name: "Formula (R-clock)", color: RULE(), values: dd.r }, { name: "AI (H-clock)", color: LLM(), values: dd.h }], fmt: (v) => `${v > 0 ? "+" : ""}${v.toFixed(1)} min` });
    CL.stack($("#rs-mode"), { cats: ["Formula, m5", "Formula, m10", "AI, m5", "AI, m10"], yLabel: "people", legend: true,
      series: MODES().map(([name, color], m) => ({ name, color, values: [modeCounts(rc, 5)[m], modeCounts(rc, 10)[m], modeCounts(hc, 5)[m], modeCounts(hc, 10)[m]] })) });
    const grid = g.agents.cost.grid;
    const depShare = (run, d) => { const dep = run.depart[d - 1].filter((_, a) => run.mode[d - 1][a] === 0); return grid.map((t) => [t, dep.filter((x) => x === t).length / dep.length]); };
    CL.lines($("#rs-depart"), { xFmt: CL.time, xTicks: [360, 420, 480, 540, 585], yLabel: "share of car trips", yFmt: (v) => `${(100 * v).toFixed(1)}%`, series: [
      { name: "Formula, morning 5", color: RULE(), dash: "4 3", points: depShare(rc, 5) }, { name: "Formula, morning 10", color: RULE(), points: depShare(rc, 10) },
      { name: "AI, morning 5", color: LLM(), dash: "4 3", points: depShare(hc, 5) }, { name: "AI, morning 10", color: LLM(), points: depShare(hc, 10) }] });
    const labels = { corridor_id: CL.corridorNames, archetype: ["", "Hybrid office", "On-site office", "Shift / service", "Trades", "Student"], H: ["", "1", "2", "3", "4", "5"], F: ["", "1", "2", "3", "4", "5"], P: ["", "1", "2", "3", "4", "5"], S: ["", "1", "2", "3", "4", "5"], vot_quintile: ["", "Q1 (lowest)", "Q2", "Q3", "Q4", "Q5"] };
    const groupChart = () => {
      const key = $("#rs-group").value, col = g.agents.cols[key], vals = [...new Set(col)].sort((a, b) => a - b);
      const resp = (run, v) => { const idx = col.map((x, a) => (x === v ? a : -1)).filter((a) => a >= 0); const cars = (days) => days.reduce((s, d) => s + idx.filter((a) => run.mode[d - 1][a] === 0).length, 0) / days.length; return cars(CHARGED) / cars(BASE_DAYS) - 1; };
      CL.bars($("#rs-group-chart"), { cats: vals.map((v) => `${labels[key][v]} (${col.filter((x) => x === v).length})`), yLabel: "change in car trips after the charge", series: [{ name: "Formula (R-clock)", color: RULE(), values: vals.map((v) => resp(rc, v)) }, { name: "AI (H-clock)", color: LLM(), values: vals.map((v) => resp(hc, v)) }], fmt: (v) => pct(v, 1) });
      const svg = $("#rs-group-chart svg");
      svg.querySelectorAll("text").forEach((t) => { if (t.textContent.includes("%")) return; });
    };
    $("#rs-group").addEventListener("change", groupChart);
    groupChart();
    const dis = (el, day) => {
      const rows = [["Formula (R-clock)", rcp], ["AI (H-clock)", hcp]].map(([name, run]) => {
        const cor = run.disruption_corridor, aff = [];
        for (let a = 0; a < g.n; a++) if (g.agents.cols.corridor_id[a] === cor && run.mode[day - 2][a] === 1) aff.push(a);
        const on = [0, 1, 2].map((m) => aff.filter((a) => run.mode[day - 1][a] === m).length);
        const back = aff.filter((a) => run.mode[day][a] === 1).length;
        return { name, aff: aff.length, on, back };
      });
      CL.stack(el, { cats: rows.map((r) => `${r.name}: ${r.aff} affected`), yLabel: `morning ${day}${day >= 6 ? " (charged)" : " (no charge)"}`, legend: true,
        series: [["Drove instead", "--car"], ["Stayed on the bus or train", "--pt"], ["Worked from home", "--wfh"]].map(([n2, col], m) => ({ name: n2, color: CL.css(col), values: rows.map((r) => r.on[m]) })) });
      el.insertAdjacentHTML("beforeend", `<p class="small muted">Back on the bus the next morning: ${rows.map((r) => `${r.name.split(" ")[0]} ${r.aff ? Math.round(100 * r.back / r.aff) : 0}%`).join(", ")}.</p>`);
    };
    dis($("#rs-dis3"), 3);
    dis($("#rs-dis8"), 8);
    const replies = hc.decisions.filter((r) => r[2] === "llm");
    const list = () => {
      const want = $("#rs-sel").value, q = $("#rs-q").value.toLowerCase();
      const rows = replies.filter((r) => (!want || (want === "CAR" ? r[3].startsWith("CAR_") : r[3] === want)) && (!q || r[5].toLowerCase().includes(q)));
      $("#rs-count").textContent = `${rows.length} of ${replies.length} replies`;
      $("#rs-replies").innerHTML = `<ul class="reasons">${rows.slice(0, 300).map((r) => `<li><span class="tag l">person ${r[0]}, morning ${r[1]}</span><span class="small muted">chose ${r[3].startsWith("CAR_") ? "to drive at " + CL.time(+r[3].slice(4, 6) * 60 + +r[3].slice(6, 8)) : r[3] === "PT" ? "the bus or train" : "to work from home"}${r[6] && r[6].tag ? ", mainly " + String(r[6].tag).replace(/_/g, " ") : ""}: </span>${CL.esc(r[5])} <a class="small" href="replay.html#agent=${r[0]}">meet them</a></li>`).join("")}</ul>`;
    };
    $("#rs-sel").addEventListener("change", list);
    $("#rs-q").addEventListener("input", list);
    list();
  }

  // ------------------------------------------------------------ reference
  async function reference() {
    const site = await CL.load("site");
    $("#rf-params tbody").innerHTML = site.params.map((p) => `<tr><td>${p.group}</td><td><code>${p.key}</code></td><td>${Array.isArray(p.value) ? p.value.join(", ") : p.value}</td><td>${p.note}</td></tr>`).join("");
    const t = site.traits;
    $("#rf-traits tbody").innerHTML = [["Habit H", "kappa_H, switching cost NZ$", t.kappa_h, t.shares_H], ["Flexibility F", "phi, schedule-delay multiplier", t.phi, t.shares_F], ["PT openness P", "omega, PT multiplier", t.omega, t.shares_P], ["Charge sensitivity S", "eta, loss weight above the reference fee", t.eta, t.shares_S]]
      .map(([n, p, v, s]) => `<tr><td>${n}</td><td>${p}</td>${v.map((x) => `<td class="n">${x}</td>`).join("")}<td>${s.map((x) => `${Math.round(100 * x)}%`).join(" / ")}</td></tr>`).join("");
  }

  document.addEventListener("DOMContentLoaded", () => {
    const page = { "#hero-replay": index, "#ce-chart": model, "#rp-replay": replay, "#rn-go": run, "#rs-cross": results, "#rf-params": reference };
    for (const [sel, fn] of Object.entries(page)) if ($(sel)) fn().catch((e) => { console.error(e); document.querySelector(".page").insertAdjacentHTML("afterbegin", `<p class="note">Something failed to load: ${CL.esc(e.message || e)}</p>`); });
  });
})();
