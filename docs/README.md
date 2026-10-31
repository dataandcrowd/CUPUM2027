# AKL Cordon website

A static site ("AKL Cordon") that explains how the Cordon-Lite simulation operates and runs it in the browser. Open `index.html`
through any static server (GitHub Pages: Settings > Pages > branch `main`, folder `/docs`), or locally:

    python3 -m http.server 8765 --directory docs      # then http://localhost:8765

Pages: `index.html` (overview with a live replay), `model.html` (how it works, with a cost explorer that
is checked against the Python values on load), `replay.html` (any morning of the stored seed-1 runs on
the map, with every commuter's history and reasons), `run.html` (the unmodified `cordonlite` package
running in Pyodide; browser runs are hashed and compared with the stored runs), `results.html` (the
chapter's findings recomputed from the stored runs) and `reference.html`.

The data behind the pages is written by `cordon_lite/scripts/build_docs_site.py` into `assets/data/`
and `assets/sim/model.zip`; rerun it after a change to the model, `config.toml`, the calibration or the
stored runs named in its `RUNS` table. `assets/img/` holds the chapter's figures. The site needs no build
step and no dependencies beyond the Pyodide CDN (the run page only).
