#!/usr/bin/env node
// Imported-app spend-consent gate (offline, no network, no API spend).
//
// A shared (#a=) app is arbitrary JS in a null-origin sandbox that reaches NanoGPT only through the
// parent's __api__ bridge, borrowing the signed-in viewer's key. The pacing bucket (check-import-pacing)
// bounds a runaway LOOP, but on its own it still lets a freshly imported app fire its first cap-worth of
// paid calls the instant it loads — a silent balance drain with zero user interaction. The consent gate
// closes that: a spend-capable ("charge") call from an IMPORTED, not-yet-armed app is REFUSED until a
// real user gesture (a click that reaches the app's Run control, whose activation propagates up to the
// parent) arms the app; arming persists on the record so later sessions stay armed. Own / preview /
// exported apps are never `imported`, so they're never gated.
//
// This pins that contract by lifting the real gate (the CONSENT_GATE_START/END block) out of play.html
// and driving it in a node:vm sandbox with controllable curImported / curArmed / navigator.userActivation
// and a writeState() spy. Same offline technique as the sibling scripts/check-*.mjs — extract the shipped
// source, drive it, assert behavior.
import { readFileSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PLAY = join(ROOT, "play.html");
const html = readFileSync(PLAY, "utf8");

const A = "// CONSENT_GATE_START", B = "// CONSENT_GATE_END";
const a = html.indexOf(A), b = html.indexOf(B);
if (a < 0 || b < 0) { console.error("✗ bridge-consent: CONSENT_GATE markers not found in play.html"); process.exit(1); }
const block = html.slice(a + A.length, b);

// The block reads curImported / curArmed / navigator.userActivation and calls writeState() to persist.
// Supply them as mutable sandbox state so we can drive every branch headlessly.
const preamble =
  "var curImported = false, curArmed = false, __writes = 0;\n" +
  "var navigator = { userActivation: { isActive: false } };\n" +
  "function writeState(){ __writes++; return true; }\n";
const epilogue =
  "\nglobalThis.__gate = {" +
  "  allows: function(g){ return consentAllowsCharge(g); }," +
  "  hasGesture: function(){ return bridgeHasGesture(); }," +
  "  arm: function(){ return armImportedApp(); }," +
  "  setImported: function(v){ curImported = v; }," +
  "  setArmed: function(v){ curArmed = v; }," +
  "  armed: function(){ return curArmed; }," +
  "  setNav: function(v){ navigator = v; }," +
  "  setActive: function(v){ navigator = { userActivation: { isActive: v } }; }," +
  "  writes: function(){ return __writes; }," +
  "  resetWrites: function(){ __writes = 0; } };\n";

const ctx = { globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
new vm.Script(preamble + block + epilogue, { filename: "play.html#consent" }).runInContext(ctx);
const G = ctx.__gate;

let failed = 0;
const ok = (cond, msg) => { if (!cond) { failed++; console.log("  ✗ " + msg); } };

// ---- 1. OWN (non-imported) app: never gated, never armed, never persisted -------
{
  G.setImported(false); G.setArmed(false); G.resetWrites();
  ok(G.allows(false) === true, "own app: a charge call passes even with NO gesture");
  ok(G.allows(true) === true, "own app: a charge call passes with a gesture too");
  ok(G.armed() === false, "own app: consent must never arm an own app");
  ok(G.writes() === 0, "own app: consent must never persist for an own app");
}

// ---- 2. IMPORTED + unarmed + NO gesture: REFUSED (the drive-by-spend case) ------
{
  G.setImported(true); G.setArmed(false); G.resetWrites();
  ok(G.allows(false) === false, "imported+unarmed+no-gesture: charge MUST be refused (silent-drain guard)");
  ok(G.armed() === false, "a refused call must NOT arm the app");
  ok(G.writes() === 0, "a refused call must NOT persist an armed flag");
}

// ---- 3. IMPORTED + unarmed + REAL gesture: allowed AND arms + persists ----------
{
  G.setImported(true); G.setArmed(false); G.resetWrites();
  ok(G.allows(true) === true, "imported+unarmed+gesture: the first real Run gesture allows the charge");
  ok(G.armed() === true, "a gesture-backed charge must ARM the app");
  ok(G.writes() === 1, "arming must persist exactly once (writeState) so a reload stays armed");
}

// ---- 4. once ARMED, later calls pass with or without a live gesture ------------
// (persisted allow → a subsequent session can run unprompted; no re-consent per call)
{
  G.setImported(true); G.setArmed(true); G.resetWrites();
  ok(G.allows(false) === true, "armed app: a later charge passes even without a live gesture");
  ok(G.allows(true) === true, "armed app: a later charge passes with a gesture too");
  ok(G.writes() === 0, "armed app: no redundant re-persist on every later charge");
}

// ---- 5. bridgeHasGesture reflects navigator.userActivation.isActive -------------
{
  G.setActive(true);  ok(G.hasGesture() === true,  "hasGesture=true when userActivation.isActive is true");
  G.setActive(false); ok(G.hasGesture() === false, "hasGesture=false when userActivation.isActive is false");
  // graceful degradation: a very old engine with no userActivation must not brick a legit viewer
  G.setNav({});       ok(G.hasGesture() === true,  "hasGesture falls back to true when the API is absent (pacing still bounds loops)");
}

// ---- 6. armImportedApp is idempotent + own-app-safe -----------------------------
{
  G.setImported(true); G.setArmed(false); G.resetWrites();
  G.arm(); ok(G.armed() === true && G.writes() === 1, "arm(): arms + persists once");
  G.arm(); ok(G.writes() === 1, "arm(): a second call is a no-op (already armed)");
  G.setImported(false); G.setArmed(false); G.resetWrites();
  G.arm(); ok(G.armed() === false && G.writes() === 0, "arm(): refuses to arm / persist an own app");
}

// ---- 7. STRUCTURAL: the bridge actually WIRES the gate ahead of pacing ----------
// The gate is only real if the __api__ charge path consults it BEFORE spending. Assert the shipped
// handler calls consentAllowsCharge(bridgeHasGesture()) and that it sits before paceChargeCall().
{
  const ci = html.indexOf("consentAllowsCharge(bridgeHasGesture())");
  const pc = html.indexOf("if(!paceChargeCall())");   // the CALL site in the __api__ handler, not the definition
  ok(ci > 0, "the __api__ charge path must call consentAllowsCharge(bridgeHasGesture())");
  ok(ci > 0 && pc > 0 && ci < pc, "consent must be checked BEFORE pacing (refuse spend before it's metered)");
  ok(html.indexOf('if(!bridgeHasGesture()) return;') > 0, "the __download__ path must require a recent user gesture");
}

if (failed) { console.error(`\n✗ check-bridge-consent: ${failed} assertion(s) failed`); process.exit(1); }
console.log("✓ imported-app spend consent holds (own/armed pass; imported+unarmed refused without a gesture; a real Run gesture arms + persists once; download requires a gesture; gate wired ahead of pacing).");
