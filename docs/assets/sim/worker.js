// Web worker: loads Pyodide, unpacks the model bundle and runs cordonlite. See driver.py.
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";
let py = null;

async function boot() {
  postMessage({ type: "status", text: "Downloading Python (about 25 MB, cached after the first visit)" });
  const { loadPyodide } = await import(PYODIDE + "pyodide.mjs");
  py = await loadPyodide({ indexURL: PYODIDE });
  postMessage({ type: "status", text: "Loading NumPy and pandas" });
  await py.loadPackage(["numpy", "pandas"], { messageCallback: () => {} });
  postMessage({ type: "status", text: "Unpacking the model" });
  const zip = await (await fetch("model.zip")).arrayBuffer();
  py.FS.mkdirTree("/home/pyodide/cordon_lite");
  py.unpackArchive(zip, "zip", { extractDir: "/home/pyodide/cordon_lite" });
  const driver = await (await fetch("driver.py")).text();
  py.FS.writeFile("/home/pyodide/cordon_lite/driver.py", driver);
  await py.runPythonAsync(`
import sys
sys.path.insert(0, "/home/pyodide/cordon_lite")
import driver
import numpy, pandas
versions = f"Python {sys.version.split()[0]}, NumPy {numpy.__version__}, pandas {pandas.__version__}"
`);
  postMessage({ type: "ready", versions: py.globals.get("versions") });
}

const booted = boot().catch((e) => postMessage({ type: "error", text: String(e) }));

onmessage = async (ev) => {
  await booted;
  if (!py) return;
  try {
    const run = py.globals.get("driver").run_web;
    const text = run(JSON.stringify(ev.data), (day) => postMessage({ type: "day", day }));
    postMessage({ type: "result", result: JSON.parse(text) });
  } catch (e) {
    postMessage({ type: "error", text: String(e) });
  }
};
