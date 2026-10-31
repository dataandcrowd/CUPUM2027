// Shared site code: navigation, data loading, small SVG charts and the map replay. No dependencies.
(function () {
  const CL = (window.CL = {});
  const cache = {};
  CL.load = (name) => (cache[name] ||= fetch(`assets/data/${name}.json`).then((r) => {
    if (!r.ok) throw new Error(name);
    return r.json();
  }));
  CL.css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  CL.time = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(Math.floor(m % 60)).padStart(2, "0")}`;
  CL.el = (tag, attrs = {}, ...kids) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "html") e.innerHTML = v;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v);
    }
    kids.flat().forEach((c) => e.append(c));
    return e;
  };
  CL.esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  CL.mean = (a) => (a.length ? a.reduce((x, y) => x + y, 0) / a.length : 0);
  CL.corridorNames = ["East", "South-east", "South", "South-west", "West"];
  CL.archetypes = ["hybrid office worker", "on-site office worker", "shift or service worker", "trades worker with a work vehicle", "tertiary student"];

  // ------------------------------------------------------------ navigation
  const PAGES = [["index.html", "Start here"], ["model.html", "How it works"], ["replay.html", "Watch a morning"],
    ["run.html", "Try it yourself"], ["results.html", "What we found"], ["reference.html", "Under the hood"]];
  document.addEventListener("DOMContentLoaded", () => {
    const here = location.pathname.split("/").pop() || "index.html";
    const bar = CL.el("header", { class: "topbar" }, CL.el("div", { class: "topbar-in" },
      CL.el("a", { class: "brand", href: "index.html" }, CL.el("i"), "AKL Cordon"),
      CL.el("nav", { class: "nav", "aria-label": "Site" }, PAGES.map(([h, t]) =>
        CL.el("a", h === here ? { href: h, "aria-current": "page" } : { href: h }, t)))));
    document.body.prepend(bar);
    const foot = document.querySelector(".foot");
    if (foot && !foot.textContent.trim()) {
      foot.innerHTML = `AKL Cordon is the simulation behind the chapter “LLM agents in traffic behaviour modelling: a ‘cognitive clock’ for drivers in congestion” by Hyesop Shin (University of Auckland) and Milad Malekzadeh (Tampere University), CUPUM 2027.
      <a href="https://github.com/dataandcrowd/CUPUM2027">Code and data on GitHub</a>.`;
    }
  });

  // ------------------------------------------------------------ tooltip
  const tip = () => (CL._tip ||= document.body.appendChild(CL.el("div", { class: "tip", role: "status" })));
  CL.showTip = (ev, html) => {
    const t = tip();
    t.innerHTML = html;
    t.style.display = "block";
    const w = t.offsetWidth;
    t.style.left = Math.min(ev.clientX + 12, innerWidth - w - 8) + "px";
    t.style.top = ev.clientY + 14 + "px";
  };
  CL.hideTip = () => { if (CL._tip) CL._tip.style.display = "none"; };

  // ------------------------------------------------------------ charts
  const NS = "http://www.w3.org/2000/svg";
  const svgEl = (t, a = {}) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; };
  function ticks(lo, hi, n = 5) {
    const raw = (hi - lo) / n || 1, p = 10 ** Math.floor(Math.log10(raw)), f = raw / p;
    const step = (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p;
    const out = [];
    for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(Math.round(v * 1e6) / 1e6);
    return out;
  }
  function frame(el, opt) {
    el.innerHTML = "";
    el.classList.add("chart");
    if (opt.legend !== false && opt.series && opt.series.length > 1) {
      el.append(CL.el("div", { class: "legend" }, opt.series.map((s) =>
        CL.el("span", {}, CL.el("i", { style: `background:${s.color}` }), s.name))));
    }
    const W = opt.width || Math.max(el.clientWidth, 300) , H = opt.height || 230;
    const m = { l: 46, r: 12, t: 12, b: 30, ...(opt.margin || {}) };
    const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": opt.alt || "" });
    el.append(svg);
    return { svg, W, H, m, iw: W - m.l - m.r, ih: H - m.t - m.b };
  }
  function yAxis(f, y, lo, hi, label) {
    const line = CL.css("--line"), s = f.svg;
    for (const v of ticks(lo, hi, 4)) {
      s.append(svgEl("line", { x1: f.m.l, x2: f.W - f.m.r, y1: y(v), y2: y(v), stroke: line }));
      const t = svgEl("text", { x: f.m.l - 6, y: y(v) + 4, "text-anchor": "end" });
      t.textContent = v.toLocaleString("en-NZ");
      s.append(t);
    }
    if (label) {
      const t = svgEl("text", { x: f.m.l, y: 10, "text-anchor": "start" });
      t.textContent = label;
      s.append(t);
      f.m.labelled = true;
    }
  }
  // Grouped bars. opt: cats, series [{name,color,values}], yLabel, shade [i0,i1], every (x label step), fmt
  CL.bars = (el, opt) => {
    const all = opt.series.flatMap((s) => s.values);
    const lo = Math.min(0, ...all), hi = Math.max(0, ...all) * 1.05 || 1;
    const f = frame(el, { ...opt, margin: { t: 24, ...(opt.margin || {}) } });
    const y = (v) => f.m.t + f.ih * (1 - (v - lo) / (hi - lo));
    const bw = f.iw / opt.cats.length, n = opt.series.length, gap = Math.max(1, bw * 0.12), w = Math.max(1.5, (bw - gap * 2 - (n - 1) * 2) / n);
    if (opt.shade) f.svg.append(svgEl("rect", { x: f.m.l + opt.shade[0] * bw, y: f.m.t, width: (opt.shade[1] - opt.shade[0]) * bw, height: f.ih, fill: CL.css("--sunk") }));
    yAxis(f, y, lo, hi, opt.yLabel);
    opt.cats.forEach((c, i) => {
      opt.series.forEach((s, j) => {
        const v = s.values[i], x = f.m.l + i * bw + gap + j * (w + 2), h = Math.abs(y(v) - y(0));
        const r = svgEl("rect", { x, y: Math.min(y(v), y(0)), width: w, height: Math.max(h, 0.5), fill: s.color, rx: Math.min(2, w / 2) });
        f.svg.append(r);
      });
      const hit = svgEl("rect", { x: f.m.l + i * bw, y: f.m.t, width: bw, height: f.ih, fill: "transparent" });
      hit.addEventListener("mousemove", (ev) => CL.showTip(ev, `<b>${c}</b><br>` + opt.series.map((s) => `${s.name}: ${(opt.fmt || ((x) => x.toLocaleString("en-NZ")))(s.values[i])}`).join("<br>")));
      hit.addEventListener("mouseleave", CL.hideTip);
      f.svg.append(hit);
      if (i % (opt.every || 1) === 0) {
        const t = svgEl("text", { x: f.m.l + i * bw + (opt.every > 1 ? 0 : bw / 2), y: f.H - 10, "text-anchor": opt.every > 1 ? "start" : "middle" });
        t.textContent = c;
        f.svg.append(t);
      }
    });
    f.svg.append(svgEl("line", { x1: f.m.l, x2: f.W - f.m.r, y1: y(0), y2: y(0), stroke: CL.css("--ink-2") }));
    return { frame: f, y };
  };
  // Stacked bars by category. opt: cats, series, yLabel
  CL.stack = (el, opt) => {
    const totals = opt.cats.map((_, i) => opt.series.reduce((a, s) => a + s.values[i], 0));
    const hi = Math.max(...totals) || 1;
    const f = frame(el, { ...opt, margin: { t: 24, ...(opt.margin || {}) } });
    const y = (v) => f.m.t + f.ih * (1 - v / hi);
    yAxis(f, y, 0, hi, opt.yLabel);
    const bw = f.iw / opt.cats.length, w = bw * 0.72;
    opt.cats.forEach((c, i) => {
      let acc = 0;
      opt.series.forEach((s) => {
        const v = s.values[i];
        if (v > 0) f.svg.append(svgEl("rect", { x: f.m.l + i * bw + (bw - w) / 2, y: y(acc + v) + 1, width: w, height: Math.max(0.5, y(acc) - y(acc + v) - 1), fill: s.color, rx: 2 }));
        acc += v;
      });
      const hit = svgEl("rect", { x: f.m.l + i * bw, y: f.m.t, width: bw, height: f.ih, fill: "transparent" });
      hit.addEventListener("mousemove", (ev) => CL.showTip(ev, `<b>${c}</b><br>` + opt.series.map((s) => `${s.name}: ${(opt.fmt || ((x) => x.toLocaleString("en-NZ")))(s.values[i])}`).join("<br>")));
      hit.addEventListener("mouseleave", CL.hideTip);
      f.svg.append(hit);
      const t = svgEl("text", { x: f.m.l + i * bw + bw / 2, y: f.H - 10, "text-anchor": "middle" });
      t.textContent = c;
      f.svg.append(t);
    });
    if (opt.mark) f.svg.append(svgEl("line", { x1: f.m.l + opt.mark * bw, x2: f.m.l + opt.mark * bw, y1: f.m.t, y2: f.m.t + f.ih, stroke: CL.css("--ink-2"), "stroke-dasharray": "3 3" }));
    return f;
  };
  // Lines. opt: series [{name,color,points:[[x,y]],dash,step}], xFmt, xTicks, yLabel, mark {x,y}, yMin, yMax
  CL.lines = (el, opt) => {
    const xs = opt.series.flatMap((s) => s.points.map((p) => p[0])), ys = opt.series.flatMap((s) => s.points.map((p) => p[1]));
    const x0 = opt.xMin ?? Math.min(...xs), x1 = opt.xMax ?? Math.max(...xs), lo = opt.yMin ?? Math.min(0, ...ys), hi = opt.yMax ?? (Math.max(...ys) * 1.05 || 1);
    const f = frame(el, { ...opt, margin: { t: 24, ...(opt.margin || {}) } });
    const x = (v) => f.m.l + f.iw * (v - x0) / (x1 - x0), y = (v) => f.m.t + f.ih * (1 - (Math.min(v, hi) - lo) / (hi - lo));
    if (opt.shade) f.svg.append(svgEl("rect", { x: x(opt.shade[0]), y: f.m.t, width: x(opt.shade[1]) - x(opt.shade[0]), height: f.ih, fill: CL.css("--sunk") }));
    yAxis(f, y, lo, hi, opt.yLabel);
    (opt.xTicks || ticks(x0, x1, 6)).forEach((v) => {
      const t = svgEl("text", { x: x(v), y: f.H - 10, "text-anchor": "middle" });
      t.textContent = (opt.xFmt || String)(v);
      f.svg.append(t);
    });
    f.svg.append(svgEl("line", { x1: f.m.l, x2: f.W - f.m.r, y1: y(lo), y2: y(lo), stroke: CL.css("--ink-2") }));
    opt.series.forEach((s) => {
      const d = s.points.map((p, i) => `${i ? "L" : "M"}${x(p[0]).toFixed(1)} ${y(p[1]).toFixed(1)}`).join("");
      f.svg.append(svgEl("path", { d, fill: "none", stroke: s.color, "stroke-width": s.width || 2, "stroke-dasharray": s.dash || "", "stroke-linejoin": "round" }));
    });
    if (opt.mark) {
      f.svg.append(svgEl("circle", { cx: x(opt.mark.x), cy: y(opt.mark.y), r: 6, fill: opt.mark.color || CL.css("--ink"), stroke: CL.css("--surface"), "stroke-width": 2 }));
    }
    const hit = svgEl("rect", { x: f.m.l, y: f.m.t, width: f.iw, height: f.ih, fill: "transparent" });
    hit.addEventListener("mousemove", (ev) => {
      const r = hit.getBoundingClientRect(), xv = x0 + (ev.clientX - r.left) / r.width * (x1 - x0);
      const rows = opt.series.map((s) => {
        const p = s.points.reduce((a, b) => (Math.abs(b[0] - xv) < Math.abs(a[0] - xv) ? b : a));
        return `${s.name ? s.name + ": " : ""}${(opt.yFmt || ((v) => (+v.toFixed(2)).toLocaleString("en-NZ")))(p[1])}`;
      });
      CL.showTip(ev, `<b>${(opt.xFmt || String)(xv)}</b><br>` + rows.join("<br>"));
    });
    hit.addEventListener("mouseleave", CL.hideTip);
    f.svg.append(hit);
    return { frame: f, x, y };
  };

  // ------------------------------------------------------------ stored-run helpers
  // 15-min bins of cordon crossings from 06:00 to 10:00, in real cars (one agent = 20 cars)
  CL.BINS = Array.from({ length: 16 }, (_, i) => 360 + i * 15);
  CL.binLabels = CL.BINS.map(CL.time);
  CL.crossings = (run, days) => {
    const out = CL.BINS.map(() => 0);
    days.forEach((d) => run.gate_exit[d - 1].forEach((x) => {
      const i = Math.floor((x - 360) / 15);
      if (x >= 0 && i >= 0 && i < out.length) out[i] += 20 / days.length;
    }));
    return out;
  };
  CL.delayBins = (run, days) => {
    const s = CL.BINS.map(() => 0), n = CL.BINS.map(() => 0);
    days.forEach((d) => run.gate_exit[d - 1].forEach((x, a) => {
      const i = Math.floor((x - 360) / 15);
      if (x >= 0 && i >= 0 && i < s.length) { s[i] += run.road[d - 1][a] + run.queue[d - 1][a]; n[i]++; }
    }));
    return s.map((v, i) => (n[i] ? v / n[i] : 0));
  };
  CL.summary = (run, a = [2, 3, 4, 5], b = [6, 7, 8, 9, 10]) => {
    const f = (days) => {
      let cars = 0, pt = 0, wfh = 0, delay = 0, late = 0, fee = 0;
      days.forEach((d) => run.mode[d - 1].forEach((m, i) => {
        if (m === 0) { cars++; delay += run.road[d - 1][i] + run.queue[d - 1][i]; if (run.fee) fee += run.fee[d - 1][i]; }
        else if (m === 1) pt++; else wfh++;
        if (run.late && run.late[d - 1][i] > 0) late++;
      }));
      return { cars: cars / days.length, pt: pt / days.length, wfh: wfh / days.length, delay: delay / cars, late: late / days.length, fee: fee / days.length };
    };
    const base = f(a), charged = f(b);
    return { base, charged, response: charged.cars / base.cars - 1 };
  };

  // ------------------------------------------------------------ geometry
  let geo = null;
  CL.geometry = async () => {
    if (geo) return geo;
    const [map, agents] = await Promise.all([CL.load("map"), CL.load("agents")]);
    const n = agents.routes.length, pts = new Array(n);
    const home = agents.cols.x_nztm.map((x, i) => [(x - map.origin[0]) / map.grid_m, (agents.cols.y_nztm[i] - map.origin[1]) / map.grid_m]);
    geo = { map, agents, n, home, path(a) {
      if (pts[a]) return pts[a];
      const xs = [], ys = [], ts = [];
      let t = 0;
      agents.routes[a].forEach((sid, k) => {
        const p = map.sections[sid], ff = agents.route_ff[a][k];
        if (!p) { t += ff; return; }
        let total = 0;
        for (let i = 2; i < p.length; i += 2) total += Math.hypot(p[i] - p[i - 2], p[i + 1] - p[i - 1]);
        let acc = 0;
        for (let i = 0; i < p.length; i += 2) {
          if (i) acc += Math.hypot(p[i] - p[i - 2], p[i + 1] - p[i - 1]);
          xs.push(p[i]); ys.push(p[i + 1]); ts.push(t + (total ? ff * acc / total : 0));
        }
        t += ff;
      });
      if (!xs.length) { xs.push(home[a][0]); ys.push(home[a][1]); ts.push(0); }
      return (pts[a] = { xs, ys, ts, total: t || 1 });
    } };
    return geo;
  };
  CL.along = (p, frac) => {
    const t = frac * p.total, ts = p.ts;
    let lo = 0, hi = ts.length - 1;
    if (t >= ts[hi]) return [p.xs[hi], p.ys[hi]];
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (ts[m] <= t) lo = m; else hi = m; }
    const f = ts[hi] > ts[lo] ? (t - ts[lo]) / (ts[hi] - ts[lo]) : 0;
    return [p.xs[lo] + f * (p.xs[hi] - p.xs[lo]), p.ys[lo] + f * (p.ys[hi] - p.ys[lo])];
  };

  // Static map on a canvas. views: region or city centre. Returns a view with project/draw.
  CL.VIEWS = { region: null, city: { cx: 2780, cy: 4040, half: 300 } };
  CL.MapView = class {
    constructor(canvas, zoom = "region", aspect = 1.12) {
      this.c = canvas; this.zoom = zoom; this.aspect = aspect; this.base = null;
    }
    fit(g) {
      const dpr = Math.min(devicePixelRatio || 1, 2), w = Math.max(this.c.clientWidth, 200), h = Math.round(w * this.aspect);
      this.c.width = w * dpr; this.c.height = h * dpr; this.c.style.height = h + "px";
      this.w = w; this.h = h; this.dpr = dpr;
      const b = g.map.bbox;
      const v = CL.VIEWS[this.zoom] || { cx: (b[0] + b[2]) / 2, cy: (b[1] + b[3]) / 2, half: Math.max((b[2] - b[0]) / 2, (b[3] - b[1]) / 2 / this.aspect) * 1.0 };
      this.k = w / (2 * v.half);
      this.ox = w / 2 - v.cx * this.k; this.oy = h / 2 + v.cy * this.k;
      this.base = null;
    }
    px(x, y) { return [x * this.k + this.ox, this.oy - y * this.k]; }
    invert(px, py) { return [(px - this.ox) / this.k, (this.oy - py) / this.k]; }
    drawBase(g, highlight) {
      const off = document.createElement("canvas");
      off.width = this.c.width; off.height = this.c.height;
      const x = off.getContext("2d");
      x.scale(this.dpr, this.dpr);
      x.fillStyle = CL.css("--water"); x.fillRect(0, 0, this.w, this.h);
      const trace = (p, close) => {
        x.beginPath();
        for (let i = 0; i < p.length; i += 2) { const [a, b] = this.px(p[i], p[i + 1]); i ? x.lineTo(a, b) : x.moveTo(a, b); }
        if (close) x.closePath();
      };
      x.fillStyle = CL.css("--land");
      g.map.land.forEach((p) => { trace(p, true); x.fill(); });
      x.lineJoin = "round"; x.strokeStyle = CL.css("--road"); x.lineWidth = 0.6;
      g.map.roads.major.forEach((p) => { trace(p); x.stroke(); });
      x.strokeStyle = CL.css("--mwy"); x.lineWidth = 1;
      Object.values(g.map.sections).forEach((p) => { trace(p); x.stroke(); });
      x.lineWidth = 1.5;
      g.map.roads.motorway.forEach((p) => { trace(p); x.stroke(); });
      x.fillStyle = CL.css("--cordon"); x.globalAlpha = 0.14;
      g.map.cordon.forEach((p) => { trace(p, true); x.fill(); });
      x.globalAlpha = 1; x.strokeStyle = CL.css("--cordon"); x.lineWidth = 1.1;
      g.map.cordon.forEach((p) => { trace(p, true); x.stroke(); });
      this.base = off;
    }
    paintBase() { const x = this.c.getContext("2d"); x.setTransform(1, 0, 0, 1, 0, 0); x.drawImage(this.base, 0, 0); x.setTransform(this.dpr, 0, 0, this.dpr, 0, 0); return x; }
    strokeRoute(x, g, a, color) {
      const p = g.path(a);
      x.beginPath();
      p.xs.forEach((v, i) => { const [m, n] = this.px(v, p.ys[i]); i ? x.lineTo(m, n) : x.moveTo(m, n); });
      x.strokeStyle = color; x.lineWidth = 2.4; x.stroke();
    }
  };

  // ------------------------------------------------------------ the replay
  // new CL.Replay(root, {panels:[{label,color,run}], day, zoom, speed, autoplay, onSelect, scenarioSwitch})
  CL.Replay = class {
    constructor(root, opt) {
      this.root = root; this.opt = opt; this.panels = opt.panels; this.day = opt.day || 8; this.t = opt.start || 390;
      this.speed = opt.speed || 10; this.playing = false; this.zoom = opt.zoom || "region"; this.sel = null; this.views = [];
    }
    async init() {
      this.g = await CL.geometry();
      const seg = (vals, get, set, fmt = String) => {
        const s = CL.el("div", { class: "seg", role: "group" });
        vals.forEach((v) => s.append(CL.el("button", { "aria-pressed": String(get() === v), onclick: () => { set(v); [...s.children].forEach((b, i) => b.setAttribute("aria-pressed", String(vals[i] === get()))); } }, fmt(v))));
        return s;
      };
      this.playBtn = CL.el("button", { class: "primary", onclick: () => this.toggle() }, "Play");
      this.face = CL.el("div", { class: "clockface", "aria-live": "off" }, CL.time(this.t));
      this.slider = CL.el("input", { type: "range", class: "timeslider", min: 330, max: 640, step: 1, value: this.t, "aria-label": "Time of morning", oninput: (e) => { this.t = +e.target.value; this.frame(); } });
      const bar = CL.el("div", { class: "transport" }, this.playBtn, this.face, this.slider,
        CL.el("label", { class: "ctl" }, "Speed", seg([5, 10, 20], () => this.speed, (v) => (this.speed = v), (v) => `${v}×`)));
      const ctl = CL.el("div", { class: "ctls" },
        CL.el("label", { class: "ctl" }, "Morning", seg([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], () => this.day, (v) => { this.day = v; this.dayChanged(); })),
        CL.el("label", { class: "ctl" }, "Map", seg(["region", "city"], () => this.zoom, (v) => { this.zoom = v; this.views.forEach((w) => (w.zoom = v)); this.resize(); }, (v) => (v === "region" ? "Whole region" : "City centre"))));
      this.dayNote = CL.el("div", { class: "small muted" });
      this.mapsEl = CL.el("div", { class: "replay-maps" });
      this.root.append(ctl, bar, this.mapsEl, this.dayNote);
      this.setPanels(this.panels);
      new ResizeObserver(() => this.resize()).observe(this.mapsEl);
      if (this.opt.autoplay && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
        new IntersectionObserver((e, o) => { if (e[0].isIntersecting) { o.disconnect(); this.toggle(); } }).observe(this.root);
      }
    }
    setPanels(panels) {
      this.panels = panels; this.mapsEl.innerHTML = ""; this.views = [];
      panels.forEach((p) => {
        const c = CL.el("canvas", { role: "img", "aria-label": `Map of commuters, ${p.label}` });
        p.countEl = CL.el("div", { class: "counts" });
        const card = CL.el("div", { class: "mapcard" }, CL.el("h4", {}, CL.el("i", { style: `background:${p.color}` }), p.label), c, p.countEl);
        this.mapsEl.append(card);
        const v = new CL.MapView(c, this.zoom, this.opt.aspect || 1.12);
        this.views.push(v);
        c.addEventListener("click", (ev) => this.click(ev, p, v));
      });
      requestAnimationFrame(() => this.resize());
      this.dayChanged();
    }
    resize() {
      if (!this.views.length) return;
      this.views.forEach((v) => { v.fit(this.g); v.drawBase(this.g); });
      this.frame();
    }
    dayChanged() {
      const charged = this.day >= 6;
      const dis = this.panels.some((p) => p.run.disruption_corridor != null && (this.day === 3 || this.day === 8));
      this.dayNote.textContent = `Morning ${this.day}: ${charged ? "the charge is on" : "no charge yet"}${dis ? ", and buses and trains on the South-west corridor take twice as long" : ""}. Each dot is one simulated commuter, standing for 20 real cars.`;
      this.frame();
      this.opt.onDay && this.opt.onDay(this.day);
    }
    toggle() {
      this.playing = !this.playing;
      this.playBtn.textContent = this.playing ? "Pause" : "Play";
      if (this.playing) {
        if (this.t >= 638) this.t = 340;
        let last = performance.now();
        const step = (now) => {
          if (!this.playing) return;
          this.t += (now - last) / 1000 * this.speed; last = now;
          if (this.t >= 640) { this.t = 640; this.toggle(); }
          this.frame();
          requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      }
    }
    state(run, a, d, t) {
      const m = run.mode[d][a];
      if (m === 2) return { s: "wfh" };
      if (m === 1) return t >= run.depart[d][a] && t < run.arrive[d][a] ? { s: "pt" } : { s: t >= run.arrive[d][a] ? "in" : "home" };
      const dep = run.depart[d][a], ga = run.gate_arrive[d][a], gx = run.gate_exit[d][a];
      if (t < dep) return { s: "home" };
      if (t < ga) return { s: "drive", f: (t - dep) / Math.max(1, ga - dep) };
      if (gx < 0 || t < gx) return { s: "queue" };
      return { s: "in" };
    }
    frame() {
      if (!this.views.length || !this.views[0].base) return;
      this.face.textContent = CL.time(this.t);
      this.slider.value = this.t;
      const d = this.day - 1, g = this.g, t = this.t;
      const qc = CL.css("--queue"), ptc = CL.css("--pt");
      this.panels.forEach((p, k) => {
        const v = this.views[k], x = v.paintBase(), run = p.run;
        p.dots = [];
        const c = { drive: 0, queue: 0, pt: 0, in: 0 }, stack = {};
        x.globalAlpha = 0.95;
        const r = v.zoom === "city" ? 3.6 : 2.3;
        for (let a = 0; a < g.n; a++) {
          const st = this.state(run, a, d, t);
          if (st.s === "pt") {
            c.pt++;
            const [m, n] = v.px(g.home[a][0], g.home[a][1]);
            x.strokeStyle = ptc; x.lineWidth = 1; x.beginPath(); x.arc(m, n, r, 0, 7); x.stroke();
            p.dots.push([m, n, a]);
          } else if (st.s === "drive") {
            c.drive++;
            const q = CL.along(g.path(a), st.f), [m, n] = v.px(q[0], q[1]);
            x.fillStyle = p.color; x.beginPath(); x.arc(m, n, r, 0, 7); x.fill();
            p.dots.push([m, n, a]);
          } else if (st.s === "queue") {
            c.queue++;
            const pth = g.path(a), i = pth.xs.length - 1, key = pth.xs[i] + "," + pth.ys[i], h = (stack[key] = (stack[key] || 0) + 1);
            const q = CL.along(pth, Math.max(0, 1 - h * 0.09 / pth.total)), [m, n] = v.px(q[0], q[1]);
            x.fillStyle = qc; x.beginPath(); x.arc(m, n, r + 0.9, 0, 7); x.fill();
            p.dots.push([m, n, a]);
          } else if (st.s === "in") c.in++;
        }
        x.globalAlpha = 1;
        if (this.sel != null) {
          v.strokeRoute(x, g, this.sel, CL.css("--ink"));
          const st = this.state(run, this.sel, d, t);
          let q = null;
          if (st.s === "drive") q = CL.along(g.path(this.sel), st.f);
          else if (st.s === "queue") q = CL.along(g.path(this.sel), 1);
          else if (st.s === "pt" || st.s === "home") q = g.home[this.sel];
          if (q) { const [m, n] = v.px(q[0], q[1]); x.fillStyle = CL.css("--ink"); x.beginPath(); x.arc(m, n, 5, 0, 7); x.fill(); }
        }
        p.countEl.innerHTML = [["Driving", p.color, c.drive], ["At a gate", qc, c.queue], ["On PT", ptc, c.pt, 1], ["Arrived", CL.css("--ink-3"), c.in]]
          .map(([n, col, v2, ring]) => `<span><i ${ring ? `class="ring" style="border-color:${col}"` : `style="background:${col}"`}></i>${n} ${v2}</span>`).join("");
      });
      this.opt.onTime && this.opt.onTime(t);
    }
    click(ev, p, v) {
      const r = v.c.getBoundingClientRect(), mx = ev.clientX - r.left, my = ev.clientY - r.top;
      let best = null, bd = 196;
      (p.dots || []).forEach(([x, y, a]) => { const e = (x - mx) ** 2 + (y - my) ** 2; if (e < bd) { bd = e; best = a; } });
      if (best != null) this.select(best);
    }
    select(a) { this.sel = a; this.frame(); this.opt.onSelect && this.opt.onSelect(a); }
  };

  // ten-morning strip for one agent. rows: [{label, run}]
  CL.dayStrip = (el, a, rows) => {
    const g = CL.el("div", { class: "days" }, CL.el("div"));
    for (let d = 1; d <= 10; d++) g.append(CL.el("div", { class: "h" }, String(d)));
    rows.forEach(({ label, run }) => {
      g.append(CL.el("div", { class: "lab" }, label));
      const woke = new Set(run.decisions.filter((r) => r[0] === a).map((r) => r[1]));
      for (let d = 1; d <= 10; d++) {
        const m = run.mode[d - 1][a];
        g.append(CL.el("div", { class: `d m${m}${woke.has(d) ? " woke" : ""}`, title: woke.has(d) ? "Stopped to think this morning" : "Did the usual" },
          m === 0 ? CL.time(run.depart[d - 1][a]) : m === 1 ? "PT" : "WFH"));
      }
    });
    el.innerHTML = "";
    el.append(g, CL.el("div", { class: "small muted" }, "Each cell is one morning: the time they left by car, PT (bus or train), or WFH (worked from home). A dark outline means this person stopped to think that morning; on the other mornings they simply did what they always do. The charge starts on morning 6."));
  };
  CL.reasonList = (el, a, rows) => {
    const li = rows.flatMap(({ tag, cls, run }) => run.decisions.filter((r) => r[0] === a).map((r) => ({ tag, cls, r })))
      .sort((x, y) => x.r[1] - y.r[1]);
    el.innerHTML = li.length ? `<ul class="reasons">${li.map(({ tag, cls, r }) => `<li><span class="tag ${cls}">${tag}, morning ${r[1]}</span>${r[4] ? `<span class="small muted">${CL.esc(r[4].replace(/;/g, ", "))}: </span>` : ""}${CL.esc(r[5])}</li>`).join("")}</ul>`
      : `<p class="small muted">After morning 1 this person never stopped to think. They just kept doing what they always do.</p>`;
  };
  CL.personaHTML = (cols, a) => `<dl>
    <dt>Lives on</dt><dd>${CL.corridorNames[cols.corridor_id[a]]} corridor, ${cols.path_km[a].toFixed(1)} km from the city centre</dd>
    <dt>Who</dt><dd>${CL.archetypes[cols.archetype[a] - 1]}, starts ${CL.time(cols.tstar_min[a])}${cols.fixed_start[a] ? " (fixed)" : ""}</dd>
    <dt>Value of time</dt><dd>NZ$${cols.vot[a].toFixed(2)}/h</dd>
    <dt>Parking, fuel</dt><dd>NZ$${cols.parking_cost[a].toFixed(2)} and NZ$${cols.fuel_cost[a].toFixed(2)} a day</dd>
    <dt>PT</dt><dd>${cols.pt_allowed[a] ? `${Math.round(cols.pt_time_min[a])} min door to door` : "not possible"}</dd>
    <dt>Options</dt><dd>${[cols.wfh_allowed[a] && "can work from home", cols.early_shift_ok[a] && "may work 07:00 to 15:00", cols.company_car[a] && "employer pays the charge"].filter(Boolean).join(", ") || "none beyond driving or PT"}</dd>
    <dt>Most it would pay</dt><dd>${cols.company_car[a] ? "not limited" : cols.wtp_fee[a] == null ? "no limit" : `NZ$${cols.wtp_fee[a].toFixed(2)} to enter`}</dd></dl>`;
  CL.traitsHTML = (cols, a) => `<div class="traits">${[["Habit", "H"], ["Flexibility", "F"], ["PT openness", "P"], ["Charge sensitivity", "S"]]
    .map(([n, k]) => `<span>${n}</span><span class="bar" aria-label="${n} ${cols[k][a]} of 5">${[1, 2, 3, 4, 5].map((i) => `<i class="${i <= cols[k][a] ? "on" : ""}"></i>`).join("")}</span>`).join("")}</div>`;
})();
