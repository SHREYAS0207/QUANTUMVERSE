html = r'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>QuantumVerse 3D</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/gsap.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --cyan:#00d4ff;--purple:#a855f7;--dark:#04040f;--card:#0a0a1e;
  --glass:rgba(0,212,255,0.04);--border:rgba(0,212,255,0.15);
}
html,body{background:var(--dark);color:#fff;font-family:'Segoe UI',sans-serif;overflow-x:hidden;scroll-behavior:smooth;}

/* ===== NAVBAR ===== */
#navbar{
  position:fixed;top:0;left:0;right:0;z-index:1000;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 40px;height:64px;
  background:rgba(4,4,15,0.85);backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
}
.nav-logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px;cursor:pointer;}
.nav-logo span{background:linear-gradient(135deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.nav-logo-icon{width:34px;height:34px;border-radius:8px;background:linear-gradient(135deg,var(--cyan),var(--purple));display:flex;align-items:center;justify-content:center;font-size:16px;}
.nav-links{display:flex;gap:4px;}
.nav-link{
  padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:500;
  color:rgba(255,255,255,0.6);transition:all .2s;border:none;background:none;
}
.nav-link:hover,.nav-link.active{color:var(--cyan);background:rgba(0,212,255,0.08);}
.nav-cta{
  padding:9px 20px;border-radius:8px;background:linear-gradient(135deg,var(--cyan),var(--purple));
  color:#04040f;font-weight:700;font-size:13px;cursor:pointer;border:none;
  transition:opacity .2s;box-shadow:0 0 20px rgba(0,212,255,0.3);
}
.nav-cta:hover{opacity:.9;}

/* ===== SECTIONS ===== */
.section{min-height:100vh;padding:80px 40px 60px;display:none;flex-direction:column;align-items:center;}
.section.active{display:flex;}
#home{padding:0;overflow:hidden;}

/* ===== 3D CANVAS ===== */
#bg-canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}
#sim-canvas{width:100%;height:100%;display:block;}
.canvas-container{
  width:100%;flex:1;border-radius:16px;overflow:hidden;
  border:1px solid var(--border);background:#040410;position:relative;
  min-height:400px;
}

/* ===== HOME HERO ===== */
#home-content{
  position:relative;z-index:10;display:flex;flex-direction:column;
  align-items:center;justify-content:center;height:100vh;
  text-align:center;padding:0 20px;
}
.hero-badge{
  display:inline-flex;align-items:center;gap:8px;padding:6px 16px;
  border-radius:20px;border:1px solid var(--border);background:rgba(0,212,255,0.05);
  font-size:12px;color:var(--cyan);margin-bottom:24px;letter-spacing:.05em;
  animation:fadeUp .6s ease forwards;
}
.hero-title{
  font-size:clamp(40px,7vw,88px);font-weight:900;line-height:1.05;
  margin-bottom:20px;animation:fadeUp .7s .1s ease both;
}
.hero-title .line1{display:block;color:#fff;}
.hero-title .line2{display:block;background:linear-gradient(135deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero-sub{font-size:18px;color:rgba(255,255,255,.55);max-width:600px;line-height:1.7;margin-bottom:40px;animation:fadeUp .8s .2s ease both;}
.hero-btns{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;animation:fadeUp .9s .3s ease both;}
.btn-primary{
  padding:14px 32px;border-radius:10px;background:linear-gradient(135deg,var(--cyan),var(--purple));
  color:#04040f;font-weight:800;font-size:15px;cursor:pointer;border:none;
  box-shadow:0 0 30px rgba(0,212,255,0.35);transition:transform .2s,box-shadow .2s;
}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 0 50px rgba(0,212,255,0.5);}
.btn-outline{
  padding:14px 32px;border-radius:10px;border:1px solid var(--border);
  color:var(--cyan);font-weight:700;font-size:15px;cursor:pointer;background:rgba(0,212,255,0.04);
  transition:all .2s;
}
.btn-outline:hover{background:rgba(0,212,255,0.1);border-color:var(--cyan);}

.hero-stats{display:flex;gap:48px;margin-top:60px;animation:fadeUp 1s .4s ease both;}
.stat{text-align:center;}
.stat-num{font-size:32px;font-weight:900;background:linear-gradient(135deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.stat-lbl{font-size:12px;color:rgba(255,255,255,.45);margin-top:4px;letter-spacing:.08em;}

/* ===== CARDS ===== */
.page-title{font-size:36px;font-weight:800;margin-bottom:8px;text-align:center;}
.page-title span{background:linear-gradient(135deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.page-sub{color:rgba(255,255,255,.45);text-align:center;margin-bottom:40px;font-size:15px;}

.card{
  background:var(--glass);border:1px solid var(--border);
  border-radius:16px;padding:24px;backdrop-filter:blur(10px);
  transition:border-color .3s;
}
.card:hover{border-color:rgba(0,212,255,0.35);}
.card-title{font-size:14px;font-weight:700;color:var(--cyan);margin-bottom:16px;letter-spacing:.05em;text-transform:uppercase;}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px;width:100%;max-width:1100px;}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;width:100%;max-width:1100px;}
.full-w{width:100%;max-width:1100px;}

/* ===== CONTROLS ===== */
.controls{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;}
.ctrl-btn{
  padding:8px 18px;border-radius:8px;border:1px solid var(--border);
  background:rgba(0,212,255,0.06);color:var(--cyan);font-size:13px;
  font-weight:600;cursor:pointer;transition:all .2s;
}
.ctrl-btn:hover,.ctrl-btn.active{background:rgba(0,212,255,0.18);border-color:var(--cyan);}
.ctrl-btn.danger{color:#f87171;border-color:rgba(248,113,113,.3);}
.ctrl-btn.danger:hover{background:rgba(248,113,113,.1);}

slider-row{display:flex;align-items:center;gap:14px;margin-bottom:12px;}
label{font-size:12px;color:rgba(255,255,255,.55);min-width:120px;}
input[type=range]{
  flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.1);
  outline:none;cursor:pointer;accent-color:var(--cyan);
}
.val-display{font-size:12px;color:var(--cyan);min-width:40px;text-align:right;font-weight:700;}

/* ===== BLOCH ===== */
#bloch-container{position:relative;width:100%;height:420px;}
#bloch-canvas{width:100%;height:100%;}
.bloch-state-display{
  position:absolute;top:16px;left:16px;
  background:rgba(4,4,15,0.9);border:1px solid var(--border);
  border-radius:10px;padding:14px 18px;font-size:13px;line-height:1.8;
}
.bloch-eq{font-size:18px;font-weight:700;color:var(--cyan);margin-bottom:6px;}

/* ===== WAVE FUNCTION ===== */
#wf-canvas{width:100%;height:300px;border-radius:12px;}
.prob-bar-container{margin-top:16px;}
.prob-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.prob-label{font-size:12px;color:rgba(255,255,255,.6);min-width:32px;}
.prob-track{flex:1;height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden;}
.prob-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--cyan),var(--purple));transition:width .4s ease;}
.prob-pct{font-size:12px;color:var(--cyan);min-width:38px;text-align:right;font-weight:700;}

/* ===== DOUBLE SLIT ===== */
#slit-canvas{width:100%;height:380px;border-radius:12px;background:#040410;}
.slit-info{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px;}
.info-box{background:rgba(0,212,255,0.05);border:1px solid var(--border);border-radius:10px;padding:12px;text-align:center;}
.info-box-val{font-size:20px;font-weight:800;color:var(--cyan);}
.info-box-lbl{font-size:11px;color:rgba(255,255,255,.4);margin-top:3px;}

/* ===== ENTANGLEMENT ===== */
#ent-canvas{width:100%;height:400px;}
.ent-panel{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px;}
.qubit-card{
  background:rgba(0,212,255,0.03);border:1px solid var(--border);
  border-radius:12px;padding:16px;
}
.qubit-label{font-size:11px;color:rgba(255,255,255,.4);letter-spacing:.08em;margin-bottom:8px;}
.qubit-state{font-size:28px;font-weight:900;}
.qubit-prob{font-size:12px;color:rgba(255,255,255,.5);margin-top:6px;}

/* ===== CIRCUIT BUILDER ===== */
.circuit-grid{display:grid;gap:0;}
.qubit-row{display:flex;align-items:center;gap:0;margin-bottom:8px;}
.qubit-name{font-size:13px;color:var(--cyan);font-weight:700;min-width:32px;margin-right:12px;}
.wire{flex:1;height:2px;background:rgba(255,255,255,.15);position:relative;display:flex;align-items:center;}
.gate-slot{
  width:48px;height:48px;border-radius:8px;border:1px dashed rgba(255,255,255,.12);
  display:flex;align-items:center;justify-content:center;cursor:pointer;
  font-size:12px;font-weight:700;margin:0 6px;background:transparent;transition:all .2s;
  position:relative;
}
.gate-slot.filled{border-style:solid;border-color:var(--cyan);background:rgba(0,212,255,.1);color:var(--cyan);}
.gate-slot:hover{border-color:rgba(0,212,255,.5);background:rgba(0,212,255,.06);}
.gate-palette{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;}
.gate-chip{
  padding:8px 16px;border-radius:8px;border:1px solid var(--border);
  background:rgba(0,212,255,.06);color:var(--cyan);font-size:13px;font-weight:700;
  cursor:grab;transition:all .2s;user-select:none;
}
.gate-chip:hover{background:rgba(0,212,255,.15);transform:translateY(-2px);box-shadow:0 4px 20px rgba(0,212,255,.2);}
.gate-chip.selected{background:rgba(0,212,255,.2);border-color:var(--cyan);box-shadow:0 0 16px rgba(0,212,255,.3);}
.circuit-result{
  margin-top:20px;padding:20px;border-radius:12px;
  border:1px solid rgba(0,212,255,.15);background:rgba(0,212,255,.03);
}
.result-bar{display:flex;align-items:center;gap:12px;margin-bottom:8px;}
.result-state{font-size:13px;color:var(--cyan);font-weight:700;min-width:32px;font-family:monospace;}
.result-track{flex:1;height:10px;background:rgba(255,255,255,.06);border-radius:5px;overflow:hidden;}
.result-fill{height:100%;border-radius:5px;transition:width .6s cubic-bezier(.4,0,.2,1);}
.result-pct{font-size:12px;min-width:40px;text-align:right;font-weight:700;}

/* ===== ORBITAL ===== */
#orbital-canvas{width:100%;height:450px;}
.orbital-selector{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;}
.orbital-btn{
  padding:8px 20px;border-radius:20px;border:1px solid var(--border);
  background:transparent;color:rgba(255,255,255,.6);font-size:13px;cursor:pointer;transition:all .2s;
}
.orbital-btn.active{background:linear-gradient(135deg,var(--cyan),var(--purple));color:#04040f;font-weight:700;border-color:transparent;box-shadow:0 0 20px rgba(0,212,255,.3);}

/* ===== KEYFRAMES ===== */
@keyframes fadeUp{from{opacity:0;transform:translateY(30px);}to{opacity:1;transform:translateY(0);}}
@keyframes pulse{0%,100%{opacity:.6;}50%{opacity:1;}}
@keyframes spin{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-12px);}}

.pulse{animation:pulse 2s ease infinite;}
.float{animation:float 4s ease infinite;}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(0,212,255,.3);border-radius:2px;}

/* ===== RESPONSIVE ===== */
@media(max-width:768px){
  #navbar{padding:0 20px;}
  .nav-links{display:none;}
  .section{padding:80px 16px 40px;}
  .grid2,.grid3{grid-template-columns:1fr;}
  .hero-stats{gap:24px;}
  .stat-num{font-size:24px;}
}

/* Scrolling particles for home */
.particle-field{position:fixed;inset:0;z-index:1;pointer-events:none;overflow:hidden;}
.p-dot{
  position:absolute;border-radius:50%;pointer-events:none;
  animation:floatRandom linear infinite;
}
@keyframes floatRandom{
  0%{transform:translateY(100vh) scale(0);opacity:0;}
  10%{opacity:1;}
  90%{opacity:.5;}
  100%{transform:translateY(-20vh) scale(1.5);opacity:0;}
}
</style>
</head>
<body>

<!-- BACKGROUND THREE.JS CANVAS -->
<canvas id="bg-canvas"></canvas>

<!-- NAVBAR -->
<nav id="navbar">
  <div class="nav-logo" onclick="showSection('home')">
    <div class="nav-logo-icon">⚛️</div>
    <span>QuantumVerse</span>
  </div>
  <div class="nav-links">
    <button class="nav-link active" onclick="showSection('home')">Home</button>
    <button class="nav-link" onclick="showSection('bloch')">Bloch Sphere</button>
    <button class="nav-link" onclick="showSection('wavefunction')">Wave Function</button>
    <button class="nav-link" onclick="showSection('doubleslit')">Double Slit</button>
    <button class="nav-link" onclick="showSection('entanglement')">Entanglement</button>
    <button class="nav-link" onclick="showSection('circuit')">Circuit Builder</button>
    <button class="nav-link" onclick="showSection('orbital')">Orbitals</button>
  </div>
  <button class="nav-cta" onclick="showSection('circuit')">Launch Lab &#8594;</button>
</nav>

<!-- ===== HOME ===== -->
<section id="home" class="section active">
  <div id="home-content">
    <div class="hero-badge">
      <span style="width:7px;height:7px;border-radius:50%;background:var(--cyan);display:inline-block;animation:pulse 1.5s infinite"></span>
      QUANTUM COMPUTING SIMULATION PLATFORM
    </div>
    <h1 class="hero-title">
      <span class="line1">Explore the</span>
      <span class="line2">Quantum Universe</span>
    </h1>
    <p class="hero-sub">Interactive 3D quantum simulations &mdash; Bloch spheres, wave functions, double-slit experiments, entanglement, orbital visualizations and a full circuit builder. All real-time.</p>
    <div class="hero-btns">
      <button class="btn-primary" onclick="showSection('bloch')">&#128300; Start Simulating</button>
      <button class="btn-outline" onclick="showSection('circuit')">&#9654; Build Circuits</button>
    </div>
    <div class="hero-stats">
      <div class="stat"><div class="stat-num" id="counter-sims">0</div><div class="stat-lbl">SIMULATIONS</div></div>
      <div class="stat"><div class="stat-num" id="counter-gates">0</div><div class="stat-lbl">QUANTUM GATES</div></div>
      <div class="stat"><div class="stat-num" id="counter-qubits">0</div><div class="stat-lbl">QUBITS</div></div>
    </div>
  </div>
</section>

<!-- ===== BLOCH SPHERE ===== -->
<section id="bloch" class="section">
  <h2 class="page-title">&#127775; <span>Bloch Sphere</span></h2>
  <p class="page-sub">The Bloch sphere is a geometrical representation of the pure state space of a two-level quantum system (qubit).</p>
  <div class="grid2">
    <div class="card full-w" style="max-width:100%">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
        <div>
          <div class="card-title">3D Bloch Sphere</div>
          <div id="bloch-container">
            <canvas id="bloch-canvas"></canvas>
            <div class="bloch-state-display">
              <div class="bloch-eq" id="bloch-eq">|&#968;&#10217; = |0&#10217;</div>
              <div style="font-size:12px;color:rgba(255,255,255,.5)" id="bloch-coords">&theta; = 0&deg; &nbsp; &phi; = 0&deg;</div>
              <div style="font-size:12px;color:rgba(255,255,255,.5);margin-top:4px" id="bloch-probs">P(0) = 100% &nbsp; P(1) = 0%</div>
            </div>
          </div>
        </div>
        <div>
          <div class="card-title">Quantum States</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:20px">
            <button class="ctrl-btn active" onclick="setBlochState(0,0,'|0&#10217;')">|0&#10217;</button>
            <button class="ctrl-btn" onclick="setBlochState(180,0,'|1&#10217;')">|1&#10217;</button>
            <button class="ctrl-btn" onclick="setBlochState(90,0,'|+&#10217;')">|+&#10217;</button>
            <button class="ctrl-btn" onclick="setBlochState(90,180,'|-&#10217;')">|-&#10217;</button>
            <button class="ctrl-btn" onclick="setBlochState(90,90,'|i&#10217;')">|i&#10217;</button>
            <button class="ctrl-btn" onclick="setBlochState(90,270,'|-i&#10217;')">|-i&#10217;</button>
            <button class="ctrl-btn" onclick="setBlochState(45,0,'Custom')">T gate</button>
            <button class="ctrl-btn" onclick="startBlochOrbit()">&#9654; Orbit</button>
          </div>
          <div class="card-title" style="margin-top:16px">Adjust State</div>
          <div style="margin-bottom:12px">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
              <label style="min-width:80px;font-size:12px;color:rgba(255,255,255,.55)">&theta; (theta)</label>
              <input type="range" id="theta-slider" min="0" max="180" value="0" oninput="updateBlochFromSliders()" style="flex:1">
              <span class="val-display" id="theta-val">0&deg;</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px">
              <label style="min-width:80px;font-size:12px;color:rgba(255,255,255,.55)">&phi; (phi)</label>
              <input type="range" id="phi-slider" min="0" max="360" value="0" oninput="updateBlochFromSliders()" style="flex:1">
              <span class="val-display" id="phi-val">0&deg;</span>
            </div>
          </div>
          <div class="card-title" style="margin-top:20px">Apply Gate</div>
          <div class="controls">
            <button class="ctrl-btn" onclick="applyGate('H')">H</button>
            <button class="ctrl-btn" onclick="applyGate('X')">X</button>
            <button class="ctrl-btn" onclick="applyGate('Y')">Y</button>
            <button class="ctrl-btn" onclick="applyGate('Z')">Z</button>
            <button class="ctrl-btn" onclick="applyGate('S')">S</button>
            <button class="ctrl-btn" onclick="applyGate('T')">T</button>
          </div>
          <div style="margin-top:16px;padding:14px;background:rgba(0,212,255,.04);border-radius:10px;border:1px solid var(--border)">
            <div style="font-size:12px;color:rgba(255,255,255,.5);margin-bottom:8px">STATE VECTOR</div>
            <div style="font-size:14px;color:var(--cyan);font-family:monospace" id="state-vector">α|0⟩ + β|1⟩</div>
            <div style="font-size:12px;color:rgba(255,255,255,.4);margin-top:6px" id="alpha-beta">&alpha; = 1.00+0.00i &nbsp;&nbsp; &beta; = 0.00+0.00i</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ===== WAVE FUNCTION ===== -->
<section id="wavefunction" class="section">
  <h2 class="page-title">&#127761; <span>Wave Function</span></h2>
  <p class="page-sub">Quantum superposition and wave function collapse &mdash; the probability density |&#968;(x)|&#178; evolves according to the Schr&#246;dinger equation.</p>
  <div class="full-w">
    <div class="card">
      <div class="card-title">Schr&#246;dinger Equation Simulator</div>
      <div class="controls">
        <button class="ctrl-btn active" id="wf-btn-super" onclick="setWFMode('superposition')">Superposition</button>
        <button class="ctrl-btn" id="wf-btn-packet" onclick="setWFMode('packet')">Wave Packet</button>
        <button class="ctrl-btn" id="wf-btn-box" onclick="setWFMode('box')">Particle in Box</button>
        <button class="ctrl-btn" id="wf-btn-tunnel" onclick="setWFMode('tunnel')">Tunneling</button>
        <button class="ctrl-btn danger" onclick="collapseWF()">&#9889; Collapse!</button>
      </div>
      <canvas id="wf-canvas" height="300"></canvas>
      <div class="prob-bar-container">
        <div style="font-size:12px;color:rgba(255,255,255,.4);margin-bottom:10px">MEASUREMENT PROBABILITIES</div>
        <div class="prob-row"><span class="prob-label">|0⟩</span><div class="prob-track"><div class="prob-fill" id="prob0-fill" style="width:50%"></div></div><span class="prob-pct" id="prob0-val">50%</span></div>
        <div class="prob-row"><span class="prob-label">|1⟩</span><div class="prob-track"><div class="prob-fill" id="prob1-fill" style="width:50%"></div></div><span class="prob-pct" id="prob1-val">50%</span></div>
      </div>
    </div>
    <div class="grid3" style="margin-top:20px">
      <div class="card">
        <div class="card-title">Energy Levels</div>
        <div id="energy-levels" style="display:flex;flex-direction:column;gap:8px"></div>
      </div>
      <div class="card">
        <div class="card-title">Parameters</div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
          <label style="font-size:12px;color:rgba(255,255,255,.55);min-width:100px">Frequency</label>
          <input type="range" id="wf-freq" min="1" max="10" value="3" style="flex:1">
        </div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
          <label style="font-size:12px;color:rgba(255,255,255,.55);min-width:100px">Amplitude</label>
          <input type="range" id="wf-amp" min="1" max="10" value="5" style="flex:1">
        </div>
        <div style="display:flex;align-items:center;gap:10px">
          <label style="font-size:12px;color:rgba(255,255,255,.55);min-width:100px">Phase</label>
          <input type="range" id="wf-phase" min="0" max="628" value="0" style="flex:1">
        </div>
      </div>
      <div class="card">
        <div class="card-title">Collapse Result</div>
        <div id="collapse-result" style="font-size:42px;text-align:center;padding:20px;color:var(--cyan);">?</div>
        <div id="collapse-info" style="font-size:12px;color:rgba(255,255,255,.4);text-align:center">Press Collapse! to measure</div>
      </div>
    </div>
  </div>
</section>

<!-- ===== DOUBLE SLIT ===== -->
<section id="doubleslit" class="section">
  <h2 class="page-title">&#127776; <span>Double Slit Experiment</span></h2>
  <p class="page-sub">The most beautiful experiment in physics. Quantum particles exhibit wave-particle duality &mdash; interference when unobserved, particle behavior when measured.</p>
  <div class="full-w">
    <div class="card">
      <div class="controls">
        <button class="ctrl-btn active" id="ds-quantum" onclick="setSlitMode('quantum')">&#128142; Quantum (Wave)</button>
        <button class="ctrl-btn" id="ds-classical" onclick="setSlitMode('classical')">&#9679; Classical (Particle)</button>
        <button class="ctrl-btn" id="ds-observed" onclick="setSlitMode('observed')">&#128065; Observed</button>
        <button class="ctrl-btn" onclick="clearSlit()">Clear</button>
      </div>
      <canvas id="slit-canvas" height="380"></canvas>
      <div class="slit-info">
        <div class="info-box"><div class="info-box-val" id="slit-particles">0</div><div class="info-box-lbl">PARTICLES FIRED</div></div>
        <div class="info-box"><div class="info-box-val" id="slit-mode-lbl">QUANTUM</div><div class="info-box-lbl">CURRENT MODE</div></div>
        <div class="info-box"><div class="info-box-val" id="slit-wavelength">500nm</div><div class="info-box-lbl">WAVELENGTH</div></div>
      </div>
    </div>
    <div style="margin-top:16px;display:flex;align-items:center;gap:14px;">
      <label style="font-size:13px;color:rgba(255,255,255,.55);">Wavelength</label>
      <input type="range" id="ds-wavelength" min="300" max="800" value="500" oninput="updateDsWavelength()" style="flex:1;max-width:300px;">
      <span style="font-size:13px;color:var(--cyan);" id="ds-wl-val">500nm</span>
      &nbsp;&nbsp;
      <label style="font-size:13px;color:rgba(255,255,255,.55);">Slit Width</label>
      <input type="range" id="ds-slit-w" min="1" max="10" value="4" style="max-width:200px;">
    </div>
  </div>
</section>

<!-- ===== ENTANGLEMENT ===== -->
<section id="entanglement" class="section">
  <h2 class="page-title">&#128279; <span>Quantum Entanglement</span></h2>
  <p class="page-sub">Entangled qubits share a quantum state. Measuring one instantly determines the other, regardless of distance &mdash; Einstein\'s \'spooky action at a distance\'.</p>
  <div class="full-w">
    <div class="card">
      <div class="card-title">Bell State Visualizer</div>
      <canvas id="ent-canvas" height="400"></canvas>
      <div class="ent-panel">
        <div class="qubit-card">
          <div class="qubit-label">QUBIT A (Alice)</div>
          <div class="qubit-state" id="q-alice" style="color:var(--cyan)">?</div>
          <div class="qubit-prob" id="q-alice-prob">Unmeasured &mdash; in superposition</div>
        </div>
        <div class="qubit-card">
          <div class="qubit-label">QUBIT B (Bob)</div>
          <div class="qubit-state" id="q-bob" style="color:var(--purple)">?</div>
          <div class="qubit-prob" id="q-bob-prob">Unmeasured &mdash; in superposition</div>
        </div>
      </div>
      <div class="controls" style="margin-top:16px">
        <button class="ctrl-btn" onclick="measureAlice()">Measure Alice</button>
        <button class="ctrl-btn" onclick="measureBob()">Measure Bob</button>
        <button class="ctrl-btn" onclick="resetEntanglement()">Reset (Re-entangle)</button>
        <button class="ctrl-btn" id="ent-state-btn" onclick="cycleEntState()">&Phi;+ State</button>
      </div>
    </div>
  </div>
</section>

<!-- ===== CIRCUIT BUILDER ===== -->
<section id="circuit" class="section">
  <h2 class="page-title">&#9889; <span>Quantum Circuit Builder</span></h2>
  <p class="page-sub">Drag gates onto qubit wires. Run the simulation to see measurement probabilities.</p>
  <div class="full-w">
    <div class="card">
      <div class="card-title">Gate Palette &mdash; click a gate then click a wire slot</div>
      <div class="gate-palette" id="gate-palette">
        <div class="gate-chip" onclick="selectGate('H')" id="gp-H">H</div>
        <div class="gate-chip" onclick="selectGate('X')" id="gp-X">X</div>
        <div class="gate-chip" onclick="selectGate('Y')" id="gp-Y">Y</div>
        <div class="gate-chip" onclick="selectGate('Z')" id="gp-Z">Z</div>
        <div class="gate-chip" onclick="selectGate('S')" id="gp-S">S</div>
        <div class="gate-chip" onclick="selectGate('T')" id="gp-T">T</div>
        <div class="gate-chip" onclick="selectGate('CNOT')" id="gp-CNOT">CNOT</div>
        <div class="gate-chip" onclick="selectGate('M')" id="gp-M" style="color:#f87171;border-color:rgba(248,113,113,.3)">M</div>
        <div class="gate-chip" onclick="selectGate(null)" style="color:rgba(255,255,255,.5)">Deselect</div>
      </div>
      <div class="card-title">Circuit (4 qubits &times; 8 steps)</div>
      <div id="circuit-grid"></div>
      <div class="controls" style="margin-top:16px">
        <button class="btn-primary" onclick="runCircuit()" style="font-size:13px;padding:10px 24px">&#9654; Run Simulation</button>
        <button class="ctrl-btn" onclick="clearCircuit()">Clear All</button>
        <button class="ctrl-btn" onclick="loadBellCircuit()">Load: Bell State</button>
        <button class="ctrl-btn" onclick="loadGHZCircuit()">Load: GHZ State</button>
        <button class="ctrl-btn" onclick="loadQFTCircuit()">Load: QFT</button>
      </div>
      <div class="circuit-result" id="circuit-result" style="display:none">
        <div class="card-title">Simulation Results (1024 shots)</div>
        <div id="result-bars"></div>
      </div>
    </div>
  </div>
</section>

<!-- ===== ORBITAL ===== -->
<section id="orbital" class="section">
  <h2 class="page-title">&#9883; <span>Atomic Orbitals</span></h2>
  <p class="page-sub">3D probability density clouds of electron positions in hydrogen-like atoms. Quantum mechanics predicts where electrons are most likely to be found.</p>
  <div class="full-w">
    <div class="card">
      <div class="card-title">Select Orbital</div>
      <div class="orbital-selector">
        <button class="orbital-btn active" onclick="setOrbital('1s')">1s</button>
        <button class="orbital-btn" onclick="setOrbital('2s')">2s</button>
        <button class="orbital-btn" onclick="setOrbital('2p')">2p</button>
        <button class="orbital-btn" onclick="setOrbital('3s')">3s</button>
        <button class="orbital-btn" onclick="setOrbital('3p')">3p</button>
        <button class="orbital-btn" onclick="setOrbital('3d')">3d</button>
        <button class="orbital-btn" onclick="setOrbital('4f')">4f</button>
      </div>
      <canvas id="orbital-canvas" height="450"></canvas>
      <div style="margin-top:12px;display:flex;gap:30px;justify-content:center;font-size:13px;color:rgba(255,255,255,.5)">
        <span>&#9679; <span style="color:var(--cyan)">High probability</span></span>
        <span>&#9679; <span style="color:var(--purple)">Medium probability</span></span>
        <span>&#9679; <span style="color:rgba(255,255,255,.2)">Low probability</span></span>
        <span id="orbital-info"></span>
      </div>
    </div>
  </div>
</section>

<script>
// ============================================================
// NAVIGATION
// ============================================================
function showSection(id){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  const links=document.querySelectorAll('.nav-link');
  links.forEach(l=>{if(l.textContent.toLowerCase().includes(id.substring(0,4).toLowerCase())) l.classList.add('active');});
  // Reinit canvas-based sims when their section is shown
  if(id==='bloch') initBloch();
  if(id==='wavefunction') initWF();
  if(id==='doubleslit') initDoubleSlit();
  if(id==='entanglement') initEntanglement();
  if(id==='circuit') initCircuit();
  if(id==='orbital') initOrbital();
}

// ============================================================
// BACKGROUND 3D (Three.js particle system)
// ============================================================
(function(){
  const canvas=document.getElementById('bg-canvas');
  const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
  renderer.setSize(window.innerWidth,window.innerHeight);

  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(60,window.innerWidth/window.innerHeight,.1,1000);
  camera.position.z=50;

  // Particle system
  const count=1200;
  const geo=new THREE.BufferGeometry();
  const pos=new Float32Array(count*3);
  const col=new Float32Array(count*3);
  for(let i=0;i<count;i++){
    pos[i*3]=(Math.random()-.5)*120;
    pos[i*3+1]=(Math.random()-.5)*120;
    pos[i*3+2]=(Math.random()-.5)*80;
    const t=Math.random();
    if(t<.5){col[i*3]=0;col[i*3+1]=.83;col[i*3+2]=1;}
    else{col[i*3]=.66;col[i*3+1]=.33;col[i*3+2]=.97;}
  }
  geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
  geo.setAttribute('color',new THREE.BufferAttribute(col,3));
  const mat=new THREE.PointsMaterial({size:.35,vertexColors:true,transparent:true,opacity:.7});
  const particles=new THREE.Points(geo,mat);
  scene.add(particles);

  // Quantum wave rings
  const rings=[];
  for(let i=0;i<4;i++){
    const r=new THREE.Mesh(
      new THREE.TorusGeometry(8+i*6,0.08,8,80),
      new THREE.MeshBasicMaterial({color:i%2?0xa855f7:0x00d4ff,transparent:true,opacity:.15+i*.05})
    );
    r.rotation.x=Math.random()*Math.PI;
    r.rotation.y=Math.random()*Math.PI;
    scene.add(r);
    rings.push(r);
  }

  // Central atom
  const nucleusMat=new THREE.MeshBasicMaterial({color:0x00d4ff,transparent:true,opacity:.9});
  const nucleus=new THREE.Mesh(new THREE.SphereGeometry(.5,16,16),nucleusMat);
  scene.add(nucleus);

  // Electron orbits
  const eMat=new THREE.MeshBasicMaterial({color:0xa855f7});
  const electrons=[];
  for(let i=0;i<3;i++){
    const e=new THREE.Mesh(new THREE.SphereGeometry(.18,8,8),eMat);
    scene.add(e);
    electrons.push({mesh:e,radius:4+i*3,speed:.5+i*.3,phase:i*(Math.PI*2/3),tilt:i*0.5});
  }

  let t=0;
  window.addEventListener('resize',()=>{
    camera.aspect=window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
  });

  function animate(){
    requestAnimationFrame(animate);
    t+=.008;
    particles.rotation.y=t*.05;
    particles.rotation.x=t*.02;
    rings.forEach((r,i)=>{ r.rotation.z=t*(0.15+i*.05); r.rotation.x=t*(0.1+i*.03); });
    electrons.forEach(e=>{
      const a=t*e.speed+e.phase;
      e.mesh.position.x=Math.cos(a)*e.radius;
      e.mesh.position.y=Math.sin(a)*e.radius*Math.sin(e.tilt);
      e.mesh.position.z=Math.sin(a)*e.radius*Math.cos(e.tilt);
    });
    renderer.render(scene,camera);
  }
  animate();
})();

// ============================================================
// COUNTER ANIMATION (home)
// ============================================================
function animCounter(id,target,suffix=''){
  const el=document.getElementById(id);
  let v=0;const step=target/60;
  const iv=setInterval(()=>{
    v=Math.min(v+step,target);
    el.textContent=Math.floor(v)+suffix;
    if(v>=target)clearInterval(iv);
  },16);
}
animCounter('counter-sims',247,'');
animCounter('counter-gates',16,'');
animCounter('counter-qubits',1024,'');

// ============================================================
// BLOCH SPHERE (Three.js)
// ============================================================
let blochRenderer,blochScene,blochCamera,blochVec,blochArrow,blochOrbitAngle=null;
let blochTheta=0,blochPhi=0;

function initBloch(){
  const canvas=document.getElementById('bloch-canvas');
  const container=document.getElementById('bloch-container');
  if(blochRenderer){blochRenderer.setSize(container.offsetWidth,container.offsetHeight);return;}

  blochRenderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
  blochRenderer.setPixelRatio(window.devicePixelRatio);
  blochRenderer.setSize(container.offsetWidth,420);

  blochScene=new THREE.Scene();
  blochCamera=new THREE.PerspectiveCamera(45,container.offsetWidth/420,0.1,100);
  blochCamera.position.set(3,2,3.5);
  blochCamera.lookAt(0,0,0);

  // Sphere wireframe
  const sphMat=new THREE.MeshBasicMaterial({color:0x00d4ff,transparent:true,opacity:.08,wireframe:false});
  blochScene.add(new THREE.Mesh(new THREE.SphereGeometry(1.5,32,32),sphMat));
  const wireMat=new THREE.MeshBasicMaterial({color:0x00d4ff,transparent:true,opacity:.12,wireframe:true});
  blochScene.add(new THREE.Mesh(new THREE.SphereGeometry(1.5,16,16),wireMat));

  // Axes
  const axMat=c=>new THREE.LineBasicMaterial({color:c,transparent:true,opacity:.5});
  const axis=(from,to,col)=>{
    const g=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...from),new THREE.Vector3(...to)]);
    return new THREE.Line(g,axMat(col));
  };
  blochScene.add(axis([0,-2,0],[0,2,0],0xffffff)); // Z
  blochScene.add(axis([-2,0,0],[2,0,0],0x00d4ff));  // X
  blochScene.add(axis([0,0,-2],[0,0,2],0xa855f7));  // Y

  // Poles
  const addLabel=(text,pos,col)=>{
    const c2=document.createElement('canvas');c2.width=128;c2.height=64;
    const ctx=c2.getContext('2d');ctx.fillStyle=col;
    ctx.font='bold 28px sans-serif';ctx.textAlign='center';
    ctx.fillText(text,64,40);
    const tex=new THREE.CanvasTexture(c2);
    const m=new THREE.SpriteMaterial({map:tex,transparent:true});
    const s=new THREE.Sprite(m);
    s.position.set(...pos);s.scale.set(.6,.3,.6);
    blochScene.add(s);
  };
  addLabel('|0⟩',[0,1.85,0],'#00d4ff');
  addLabel('|1⟩',[0,-1.85,0],'#a855f7');
  addLabel('X',[2.1,0,0],'#00d4ff');
  addLabel('Y',[0,0,2.1],'#a855f7');

  // State vector arrow
  const arrowDir=new THREE.Vector3(0,1,0);
  blochArrow=new THREE.ArrowHelper(arrowDir,new THREE.Vector3(0,0,0),1.5,0x00ff88,0.2,0.12);
  blochScene.add(blochArrow);

  // Equatorial circle
  const eqPts=[];
  for(let i=0;i<=64;i++){const a=i/64*Math.PI*2;eqPts.push(new THREE.Vector3(Math.cos(a)*1.5,0,Math.sin(a)*1.5));}
  blochScene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(eqPts),new THREE.LineBasicMaterial({color:0x00d4ff,transparent:true,opacity:.2})));

  // Mouse orbit
  let dragging=false,lastX=0,lastY=0,camTheta=Math.PI/4,camPhi=Math.PI/5,camR=4;
  canvas.addEventListener('mousedown',e=>{dragging=true;lastX=e.clientX;lastY=e.clientY;});
  window.addEventListener('mouseup',()=>dragging=false);
  window.addEventListener('mousemove',e=>{
    if(!dragging||document.getElementById('bloch').style.display==='none')return;
    const dx=e.clientX-lastX,dy=e.clientY-lastY;
    camTheta-=dx*.01;camPhi=Math.max(.1,Math.min(Math.PI-.1,camPhi+dy*.01));
    lastX=e.clientX;lastY=e.clientY;
    blochCamera.position.x=camR*Math.sin(camPhi)*Math.cos(camTheta);
    blochCamera.position.y=camR*Math.cos(camPhi);
    blochCamera.position.z=camR*Math.sin(camPhi)*Math.sin(camTheta);
    blochCamera.lookAt(0,0,0);
  });

  setBlochState(0,0,'|0⟩');

  function animateBloch(){
    requestAnimationFrame(animateBloch);
    if(blochOrbitAngle!==null){
      blochOrbitAngle+=.01;
      const t2=blochTheta*Math.PI/180,p2=blochOrbitAngle;
      updateBlochArrow(t2,p2,false);
    }
    blochRenderer.render(blochScene,blochCamera);
  }
  animateBloch();
}

function setBlochVec(tRad,pRad){
  const x=Math.sin(tRad)*Math.cos(pRad);
  const y=Math.cos(tRad);
  const z=Math.sin(tRad)*Math.sin(pRad);
  return new THREE.Vector3(x,y,z);
}

function updateBlochArrow(tRad,pRad,updateSliders=true){
  const dir=setBlochVec(tRad,pRad).normalize();
  blochArrow.setDirection(dir);
  const tDeg=Math.round(tRad*180/Math.PI);
  const pDeg=Math.round(pRad*180/Math.PI);
  document.getElementById('bloch-coords').textContent=`θ = ${tDeg}°   ϕ = ${pDeg}°`;
  const p0=Math.round(Math.cos(tRad/2)**2*100);
  const p1=100-p0;
  document.getElementById('bloch-probs').textContent=`P(0) = ${p0}%   P(1) = ${p1}%`;
  const alpha=Math.cos(tRad/2).toFixed(2);
  const betaR=(Math.sin(tRad/2)*Math.cos(pRad)).toFixed(2);
  const betaI=(Math.sin(tRad/2)*Math.sin(pRad)).toFixed(2);
  document.getElementById('alpha-beta').textContent=`α = ${alpha}+0.00i     β = ${betaR}+${betaI}i`;
  if(updateSliders){
    document.getElementById('theta-slider').value=tDeg;
    document.getElementById('phi-slider').value=((pDeg%360)+360)%360;
    document.getElementById('theta-val').textContent=tDeg+'°';
    document.getElementById('phi-val').textContent=pDeg+'°';
  }
}

function setBlochState(thetaDeg,phiDeg,label){
  blochOrbitAngle=null;
  blochTheta=thetaDeg;blochPhi=phiDeg;
  const tRad=thetaDeg*Math.PI/180,pRad=phiDeg*Math.PI/180;
  document.getElementById('bloch-eq').innerHTML=`|ψ⟩ = ${label||'custom'}`;
  updateBlochArrow(tRad,pRad);
  if(!blochArrow)return;
  gsap.to({t:0},{t:1,duration:.6,ease:'power2.out',onUpdate:function(){
    const prog=this.targets()[0].t;
    updateBlochArrow(tRad*prog,pRad*prog,false);
  }});
}

function updateBlochFromSliders(){
  blochOrbitAngle=null;
  const t2=+document.getElementById('theta-slider').value;
  const p2=+document.getElementById('phi-slider').value;
  document.getElementById('theta-val').textContent=t2+'°';
  document.getElementById('phi-val').textContent=p2+'°';
  blochTheta=t2;blochPhi=p2;
  updateBlochArrow(t2*Math.PI/180,p2*Math.PI/180,false);
}

function startBlochOrbit(){blochOrbitAngle=0;}

function applyGate(gate){
  let t=blochTheta,p=blochPhi;
  if(gate==='H'){t=t===0?90:t===180?90:t===90&&p===0?0:90;p=t===0?0:p===180?0:0;}
  else if(gate==='X'){t=180-t;}
  else if(gate==='Y'){t=180-t;p=(p+180)%360;}
  else if(gate==='Z'){p=(p+180)%360;}
  else if(gate==='S'){p=(p+90)%360;}
  else if(gate==='T'){p=(p+45)%360;}
  setBlochState(t,p,`${gate}|ψ⟩`);
}

// ============================================================
// WAVE FUNCTION SIMULATOR
// ============================================================
let wfCtx,wfMode='superposition',wfT=0,wfCollapsed=false,wfResult=null,wfAnimId;

function initWF(){
  const canvas=document.getElementById('wf-canvas');
  canvas.width=canvas.offsetWidth||800;
  canvas.height=300;
  wfCtx=canvas.getContext('2d');
  if(wfAnimId)cancelAnimationFrame(wfAnimId);
  drawEnergyLevels();
  animateWF();
}

function setWFMode(m){
  wfMode=m;wfCollapsed=false;wfResult=null;
  document.getElementById('collapse-result').textContent='?';
  document.getElementById('collapse-info').textContent='Press Collapse! to measure';
  ['super','packet','box','tunnel'].forEach(id=>{
    document.getElementById('wf-btn-'+id).classList.remove('active');
  });
  const map={superposition:'super',packet:'packet',box:'box',tunnel:'tunnel'};
  document.getElementById('wf-btn-'+map[m]).classList.add('active');
}

function collapseWF(){
  if(wfCollapsed)return;
  const prob0=wfMode==='superposition'?50:wfMode==='box'?25:60;
  wfResult=Math.random()*100<prob0?'|0⟩':'|1⟩';
  wfCollapsed=true;
  document.getElementById('collapse-result').textContent=wfResult;
  document.getElementById('collapse-result').style.color=wfResult==='|0⟩'?'#00d4ff':'#a855f7';
  document.getElementById('collapse-info').textContent='Wave function collapsed! State determined.';
  document.getElementById('prob0-fill').style.width=wfResult==='|0⟩'?'100%':'0%';
  document.getElementById('prob1-fill').style.width=wfResult==='|1⟩'?'100%':'0%';
  document.getElementById('prob0-val').textContent=wfResult==='|0⟩'?'100%':'0%';
  document.getElementById('prob1-val').textContent=wfResult==='|1⟩'?'100%':'0%';
  setTimeout(()=>{
    wfCollapsed=false;wfResult=null;
    document.getElementById('prob0-fill').style.width='50%';
    document.getElementById('prob1-fill').style.width='50%';
    document.getElementById('prob0-val').textContent='50%';
    document.getElementById('prob1-val').textContent='50%';
    document.getElementById('collapse-result').textContent='?';
    document.getElementById('collapse-result').style.color='var(--cyan)';
    document.getElementById('collapse-info').textContent='Press Collapse! to measure';
  },3000);
}

function drawEnergyLevels(){
  const cont=document.getElementById('energy-levels');
  cont.innerHTML='';
  [1,2,3,4].forEach(n=>{
    const E=-13.6/n**2;
    const d=document.createElement('div');
    d.style.cssText='display:flex;align-items:center;gap:10px;';
    d.innerHTML=`<span style="font-size:11px;color:rgba(255,255,255,.4);min-width:20px">n=${n}</span>
      <div style="flex:1;height:2px;background:linear-gradient(90deg,var(--cyan),var(--purple));opacity:${.3+n*.15}"></div>
      <span style="font-size:11px;color:var(--cyan);">${E.toFixed(2)} eV</span>`;
    cont.appendChild(d);
  });
}

function animateWF(){
  wfAnimId=requestAnimationFrame(animateWF);
  wfT+=.04;
  if(!wfCtx)return;
  const W=wfCtx.canvas.width,H=wfCtx.canvas.height;
  wfCtx.clearRect(0,0,W,H);
  wfCtx.fillStyle='#04040f';wfCtx.fillRect(0,0,W,H);

  const freq=+document.getElementById('wf-freq').value||3;
  const amp=+document.getElementById('wf-amp').value||5;
  const phase=+document.getElementById('wf-phase').value*.01||0;
  const mid=H*.6;

  if(wfCollapsed){
    // Collapsed spike
    const cx=W*.5;
    const grad=wfCtx.createLinearGradient(cx-3,0,cx+3,H);
    grad.addColorStop(0,wfResult==='|0⟩'?'#00d4ff':'#a855f7');
    grad.addColorStop(1,'transparent');
    wfCtx.fillStyle=grad;
    wfCtx.fillRect(cx-3,H*.1,6,H*.8);
    return;
  }

  if(wfMode==='superposition'){
    // Two overlapping gaussians + real part
    const drawWave=(offset,color,alpha)=>{
      wfCtx.beginPath();
      wfCtx.strokeStyle=color;
      wfCtx.globalAlpha=alpha;
      wfCtx.lineWidth=2;
      for(let x=0;x<W;x++){
        const xn=(x/W-offset);
        const envelope=Math.exp(-xn*xn*20)*amp*40;
        const y=mid-Math.sin(x*.05*freq+wfT+phase)*envelope;
        x===0?wfCtx.moveTo(x,y):wfCtx.lineTo(x,y);
      }
      wfCtx.stroke();
      wfCtx.globalAlpha=1;
    };
    drawWave(.3,'#00d4ff',1);
    drawWave(.7,'#a855f7',1);
    // Probability density
    wfCtx.beginPath();
    wfCtx.strokeStyle='rgba(255,255,255,0.4)';
    wfCtx.setLineDash([4,4]);
    for(let x=0;x<W;x++){
      const xn1=x/W-.3,xn2=x/W-.7;
      const e=Math.exp(-xn1*xn1*20)+Math.exp(-xn2*xn2*20);
      const y=mid-e*amp*30;
      x===0?wfCtx.moveTo(x,y):wfCtx.lineTo(x,y);
    }
    wfCtx.stroke();wfCtx.setLineDash([]);
  } else if(wfMode==='packet'){
    wfCtx.beginPath();
    wfCtx.strokeStyle='#00d4ff';
    wfCtx.lineWidth=2;
    const center=(.5+.4*Math.sin(wfT*.3))*W;
    for(let x=0;x<W;x++){
      const xn=(x-center)/W;
      const envelope=Math.exp(-xn*xn*80)*amp*50;
      const y=mid-Math.cos((x-center)*.08*freq+wfT)*envelope;
      x===0?wfCtx.moveTo(x,y):wfCtx.lineTo(x,y);
    }
    wfCtx.stroke();
    // Prob density fill
    wfCtx.beginPath();
    const grad=wfCtx.createLinearGradient(0,mid-amp*60,0,mid);
    grad.addColorStop(0,'rgba(0,212,255,.15)');grad.addColorStop(1,'transparent');
    wfCtx.fillStyle=grad;
    wfCtx.moveTo(0,mid);
    for(let x=0;x<W;x++){const xn=(x-center)/W;const e=Math.exp(-xn*xn*80)*amp*50;wfCtx.lineTo(x,mid-Math.abs(Math.cos((x-center)*.08*freq+wfT))*e);}
    wfCtx.lineTo(W,mid);wfCtx.fill();
  } else if(wfMode==='box'){
    // Particle in a box - standing waves
    wfCtx.lineWidth=2;
    for(let n=1;n<=3;n++){
      const cols=['#00d4ff','#a855f7','rgba(255,255,255,.4)'];
      wfCtx.beginPath();
      wfCtx.strokeStyle=cols[n-1];
      for(let x=0;x<W;x++){
        const y=mid-(Math.sin(n*Math.PI*x/W)*amp*30*Math.cos(wfT*n*.5+phase));
        x===0?wfCtx.moveTo(x,y):wfCtx.lineTo(x,y);
      }
      wfCtx.stroke();
    }
    // Box walls
    wfCtx.strokeStyle='rgba(255,255,255,.3)';wfCtx.lineWidth=2;
    wfCtx.beginPath();wfCtx.moveTo(5,H*.1);wfCtx.lineTo(5,H*.95);wfCtx.moveTo(W-5,H*.1);wfCtx.lineTo(W-5,H*.95);wfCtx.stroke();
  } else if(wfMode==='tunnel'){
    // Barrier tunneling
    const barrierX=W*.5,barrierW=20;
    wfCtx.fillStyle='rgba(255,100,100,.15)';wfCtx.fillRect(barrierX-barrierW/2,H*.2,barrierW,H*.6);
    wfCtx.strokeStyle='rgba(255,100,100,.4)';wfCtx.strokeRect(barrierX-barrierW/2,H*.2,barrierW,H*.6);
    const center=(.15+.6*((wfT*.08)%1))*W;
    wfCtx.beginPath();wfCtx.strokeStyle='#00d4ff';wfCtx.lineWidth=2;
    for(let x=0;x<W;x++){
      const xn=(x-center)/W;
      let envelope=Math.exp(-xn*xn*60)*amp*45;
      if(x>barrierX+barrierW/2) envelope*=.12;
      else if(x>barrierX-barrierW/2) envelope*=.3;
      const y=mid-Math.cos((x-center)*.1*freq+wfT)*envelope;
      x===0?wfCtx.moveTo(x,y):wfCtx.lineTo(x,y);
    }
    wfCtx.stroke();
    // Tunneled part
    const tc=center+barrierW*8;
    if(tc>barrierX+barrierW){
      wfCtx.beginPath();wfCtx.strokeStyle='rgba(168,85,247,.7)';
      for(let x=barrierX+barrierW/2;x<W;x++){
        const xn=(x-tc)/W;
        const envelope=Math.exp(-xn*xn*80)*amp*8;
        const y=mid-Math.cos((x-tc)*.1*freq+wfT)*envelope;
        x===barrierX+barrierW/2?wfCtx.moveTo(x,y):wfCtx.lineTo(x,y);
      }
      wfCtx.stroke();
    }
  }

  // Axis
  wfCtx.strokeStyle='rgba(255,255,255,.1)';wfCtx.lineWidth=1;
  wfCtx.beginPath();wfCtx.moveTo(0,mid);wfCtx.lineTo(W,mid);wfCtx.stroke();
  wfCtx.fillStyle='rgba(255,255,255,.3)';wfCtx.font='11px sans-serif';
  wfCtx.fillText('ψ(x)',8,mid-20);
  wfCtx.fillText('x →',W-30,mid+15);
}

// ============================================================
// DOUBLE SLIT EXPERIMENT
// ============================================================
let slitCtx,slitMode='quantum',slitParticles=[],slitCount=0,slitAnimId2;
let slitScreen=[];

function initDoubleSlit(){
  const canvas=document.getElementById('slit-canvas');
  canvas.width=canvas.offsetWidth||900;
  canvas.height=380;
  slitCtx=canvas.getContext('2d');
  slitScreen=new Array(canvas.height).fill(0);
  if(slitAnimId2)cancelAnimationFrame(slitAnimId2);
  animateSlit();
}

function setSlitMode(m){
  slitMode=m;slitScreen.fill(0);slitParticles=[];
  ['quantum','classical','observed'].forEach(id=>{
    document.getElementById('ds-'+id).classList.remove('active');
  });
  document.getElementById('ds-'+m).classList.add('active');
  document.getElementById('slit-mode-lbl').textContent=m.toUpperCase();
}

function clearSlit(){
  slitScreen.fill(0);slitParticles=[];slitCount=0;
  document.getElementById('slit-particles').textContent='0';
}

function updateDsWavelength(){
  const v=document.getElementById('ds-wavelength').value;
  document.getElementById('ds-wl-val').textContent=v+'nm';
  document.getElementById('slit-wavelength').textContent=v+'nm';
}

function wavelengthToColor(wl){
  let r,g,b;
  if(wl>=380&&wl<440){r=(440-wl)/60;g=0;b=1;}
  else if(wl<490){r=0;g=(wl-440)/50;b=1;}
  else if(wl<510){r=0;g=1;b=(510-wl)/20;}
  else if(wl<580){r=(wl-510)/70;g=1;b=0;}
  else if(wl<645){r=1;g=(645-wl)/65;b=0;}
  else{r=1;g=0;b=0;}
  return `rgb(${Math.round(r*255)},${Math.round(g*255)},${Math.round(b*255)})`;
}

function animateSlit(){
  slitAnimId2=requestAnimationFrame(animateSlit);
  if(!slitCtx)return;
  const W=slitCtx.canvas.width,H=slitCtx.canvas.height;
  slitCtx.fillStyle='rgba(4,4,15,.25)';slitCtx.fillRect(0,0,W,H);

  const wl=+document.getElementById('ds-wavelength').value||500;
  const slitColor=wavelengthToColor(wl);
  const barrierX=W*.35,screenX=W*.85;
  const slitY1=H*.38,slitY2=H*.62,slitH=16;

  // Barrier
  slitCtx.fillStyle='rgba(255,255,255,.1)';
  slitCtx.fillRect(barrierX-2,0,4,slitY1-slitH/2);
  slitCtx.fillRect(barrierX-2,slitY1+slitH/2,4,slitY2-slitH/2-(slitY1+slitH/2));
  slitCtx.fillRect(barrierX-2,slitY2+slitH/2,4,H-(slitY2+slitH/2));

  // Source
  slitCtx.beginPath();
  slitCtx.arc(W*.1,H*.5,8,0,Math.PI*2);
  slitCtx.fillStyle=slitColor;slitCtx.fill();
  slitCtx.shadowColor=slitColor;slitCtx.shadowBlur=20;
  slitCtx.fill();slitCtx.shadowBlur=0;

  // Emit particles
  if(Math.random()<.6){
    const fromSlit=Math.random()<.5?slitY1:slitY2;
    const destY=slitMode==='quantum'
      ? getQuantumHitY(H,wl,slitY1,slitY2)
      : slitMode==='classical'
      ? fromSlit+(Math.random()-.5)*slitH*3
      : fromSlit+(Math.random()-.5)*slitH*1.5;
    slitParticles.push({x:barrierX+2,y:fromSlit,tx:screenX,ty:destY,prog:0,color:slitColor,speed:.04+Math.random()*.03});
    slitCount++;document.getElementById('slit-particles').textContent=slitCount;
  }

  // Draw waves (quantum only)
  if(slitMode==='quantum'){
    [slitY1,slitY2].forEach(sy=>{
      for(let r=20;r<W*.5;r+=30){
        const alpha=Math.max(0,(1-r/(W*.5))*.12);
        slitCtx.beginPath();
        slitCtx.arc(barrierX,sy,r,0,Math.PI*2);
        slitCtx.strokeStyle=`rgba(0,212,255,${alpha})`;
        slitCtx.lineWidth=1.5;
        slitCtx.stroke();
      }
    });
  }

  // Particles
  slitParticles=slitParticles.filter(p=>p.prog<1);
  slitParticles.forEach(p=>{
    p.prog+=p.speed;
    p.x=barrierX+(screenX-barrierX)*p.prog;
    p.y=p.y+(p.ty-p.y)*p.prog;
    slitCtx.beginPath();
    slitCtx.arc(p.x,p.y,2.5,0,Math.PI*2);
    slitCtx.fillStyle=p.color;slitCtx.fill();
    if(p.prog>.9){
      const yi=Math.round(p.ty);
      if(yi>=0&&yi<slitScreen.length) slitScreen[yi]++;
    }
  });

  // Detection screen
  slitCtx.fillStyle='rgba(255,255,255,.05)';
  slitCtx.fillRect(screenX-1,0,3,H);
  const maxS=Math.max(...slitScreen,1);
  slitScreen.forEach((v,y)=>{
    if(v>0){
      const w=v/maxS*40;
      const alpha=Math.min(1,v/maxS*.9);
      slitCtx.fillStyle=slitColor.replace(')',`,${alpha})`).replace('rgb','rgba');
      slitCtx.fillRect(screenX+2,y,w,1);
    }
  });

  // Labels
  slitCtx.fillStyle='rgba(255,255,255,.4)';slitCtx.font='11px sans-serif';
  slitCtx.fillText('Source',W*.06,H*.5-18);
  slitCtx.fillText('Barrier',barrierX-18,15);
  slitCtx.fillText('Screen',screenX+5,15);
}

function getQuantumHitY(H,wl,slit1,slit2){
  const k=2*Math.PI/wl*10000;
  const d=(slit2-slit1)/H;
  let probs=[],total=0;
  for(let y=0;y<H;y++){
    const theta=(y/H-.5)*2;
    const phase=k*d*theta*5;
    const I=Math.pow(Math.cos(phase/2),2);
    probs.push(I);total+=I;
  }
  let r=Math.random()*total,cum=0;
  for(let y=0;y<H;y++){cum+=probs[y];if(cum>=r)return y;}
  return H*.5;
}

// ============================================================
// QUANTUM ENTANGLEMENT
// ============================================================
let entCtx,entT2=0,entMeasured={a:null,b:null},entAnimId3;
let entState=0;
const entStates=['\u03a6+','\u03a6-','\u03a8+','\u03a8-'];

function initEntanglement(){
  const canvas=document.getElementById('ent-canvas');
  canvas.width=canvas.offsetWidth||900;
  canvas.height=400;
  entCtx=canvas.getContext('2d');
  if(entAnimId3)cancelAnimationFrame(entAnimId3);
  animateEntanglement();
}

function animateEntanglement(){
  entAnimId3=requestAnimationFrame(animateEntanglement);
  if(!entCtx)return;
  const W=entCtx.canvas.width,H=entCtx.canvas.height;
  entCtx.fillStyle='rgba(4,4,15,.3)';entCtx.fillRect(0,0,W,H);
  entT2+=.03;

  const aX=W*.2,bX=W*.8,midY=H*.5;

  // Connection line (entanglement)
  if(!entMeasured.a&&!entMeasured.b){
    for(let i=0;i<8;i++){
      const t3=((entT2+i*.3)%1);
      const x=aX+(bX-aX)*t3;
      const wave=Math.sin(entT2*4+i)*20;
      const alpha=(1-Math.abs(t3-.5)*2)*.8;
      entCtx.beginPath();
      entCtx.arc(x,midY+wave*Math.sin(entT2),4,0,Math.PI*2);
      entCtx.fillStyle=`rgba(168,85,247,${alpha})`;entCtx.fill();
    }
    // Wavy line
    entCtx.beginPath();entCtx.setLineDash([6,6]);
    entCtx.strokeStyle='rgba(0,212,255,.2)';entCtx.lineWidth=1.5;
    for(let x=aX;x<=bX;x+=2){
      const y=midY+Math.sin(x*.05+entT2*3)*15;
      x===aX?entCtx.moveTo(x,y):entCtx.lineTo(x,y);
    }
    entCtx.stroke();entCtx.setLineDash([]);
  } else {
    // Collapsed - straight line
    entCtx.beginPath();
    entCtx.strokeStyle='rgba(255,255,255,.15)';entCtx.lineWidth=1.5;entCtx.setLineDash([4,4]);
    entCtx.moveTo(aX,midY);entCtx.lineTo(bX,midY);entCtx.stroke();entCtx.setLineDash([]);
  }

  // Qubit A
  drawEntQubit(entCtx,aX,midY,entMeasured.a,'Alice','#00d4ff',entT2);
  // Qubit B
  drawEntQubit(entCtx,bX,midY,entMeasured.b,'Bob','#a855f7',-entT2);

  // Labels
  entCtx.fillStyle='rgba(255,255,255,.3)';entCtx.font='12px sans-serif';entCtx.textAlign='center';
  entCtx.fillText(`Bell State |Φ${entStates[entState].slice(1)}`,W*.5,30);
  entCtx.fillText('Entangled — spooky action at a distance',W*.5,50);
  entCtx.textAlign='left';
}

function drawEntQubit(ctx,x,y,measured,name,color,t4){
  if(measured===null){
    // Spinning superposition
    for(let i=0;i<12;i++){
      const a=i/12*Math.PI*2+t4;
      const rx=Math.cos(a)*30,ry=Math.sin(a)*15;
      ctx.beginPath();
      ctx.arc(x+rx,y+ry,3,0,Math.PI*2);
      ctx.fillStyle=color.replace(')',`,.${3+Math.floor(Math.abs(Math.sin(i))*7)})`).replace('rgb','rgba');
      ctx.fill();
    }
    ctx.beginPath();ctx.arc(x,y,18,0,Math.PI*2);
    ctx.fillStyle=color.replace('#','').length===6?`rgba(${parseInt(color.slice(1,3),16)},${parseInt(color.slice(3,5),16)},${parseInt(color.slice(5,7),16)},.15)`:color;
    ctx.fill();
    ctx.strokeStyle=color;ctx.lineWidth=2;ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.9)';ctx.font='bold 13px sans-serif';ctx.textAlign='center';
    ctx.fillText('?',x,y+5);
  } else {
    // Collapsed
    ctx.beginPath();ctx.arc(x,y,24,0,Math.PI*2);
    ctx.fillStyle=measured?'rgba(0,212,255,.2)':'rgba(168,85,247,.2)';ctx.fill();
    ctx.strokeStyle=measured?'#00d4ff':'#a855f7';ctx.lineWidth=3;ctx.stroke();
    ctx.shadowColor=measured?'#00d4ff':'#a855f7';ctx.shadowBlur=20;
    ctx.fillStyle='rgba(255,255,255,.9)';ctx.font='bold 22px sans-serif';ctx.textAlign='center';
    ctx.fillText(measured?'|0⟩':'|1⟩',x,y+8);
    ctx.shadowBlur=0;
  }
  ctx.fillStyle='rgba(255,255,255,.6)';ctx.font='14px sans-serif';ctx.textAlign='center';
  ctx.fillText(name,x,y+50);
  ctx.textAlign='left';
}

function measureAlice(){
  if(entMeasured.a!==null)return;
  entMeasured.a=Math.random()<.5;
  if(entState===0||entState===2) entMeasured.b=entMeasured.a===entState<2?!entMeasured.a:entMeasured.a;
  // Bell state correlations
  if(entState===0) entMeasured.b=entMeasured.a; // Phi+
  else if(entState===1) entMeasured.b=!entMeasured.a; // Phi-
  else if(entState===2) entMeasured.b=entMeasured.a; // Psi+
  else entMeasured.b=!entMeasured.a; // Psi-
  updateEntUI();
}

function measureBob(){
  if(entMeasured.b!==null)return;
  entMeasured.b=Math.random()<.5;
  if(entState===0) entMeasured.a=entMeasured.b;
  else if(entState===1) entMeasured.a=!entMeasured.b;
  else if(entState===2) entMeasured.a=entMeasured.b;
  else entMeasured.a=!entMeasured.b;
  updateEntUI();
}

function updateEntUI(){
  const aEl=document.getElementById('q-alice'),bEl=document.getElementById('q-bob');
  const aP=document.getElementById('q-alice-prob'),bP=document.getElementById('q-bob-prob');
  if(entMeasured.a!==null){aEl.textContent=entMeasured.a?'|0⟩':'|1⟩';aP.textContent='Collapsed — definite state';}
  if(entMeasured.b!==null){bEl.textContent=entMeasured.b?'|0⟩':'|1⟩';bP.textContent='Instantly determined by Alice\'s measurement!';}
}

function resetEntanglement(){
  entMeasured={a:null,b:null};
  document.getElementById('q-alice').textContent='?';
  document.getElementById('q-bob').textContent='?';
  document.getElementById('q-alice-prob').textContent='Unmeasured — in superposition';
  document.getElementById('q-bob-prob').textContent='Unmeasured — in superposition';
}

function cycleEntState(){
  entState=(entState+1)%4;
  resetEntanglement();
  document.getElementById('ent-state-btn').textContent=entStates[entState]+' State';
}

// ============================================================
// CIRCUIT BUILDER
// ============================================================
const QUBITS=4,STEPS=8;
let circuitGates=Array.from({length:QUBITS},()=>Array(STEPS).fill(null));
let selectedGate=null;

function initCircuit(){
  const grid=document.getElementById('circuit-grid');
  grid.innerHTML='';
  for(let q=0;q<QUBITS;q++){
    const row=document.createElement('div');
    row.className='qubit-row';
    const lbl=document.createElement('span');
    lbl.className='qubit-name';
    lbl.textContent='q'+q;
    row.appendChild(lbl);
    const wireDiv=document.createElement('div');
    wireDiv.className='wire';
    for(let s=0;s<STEPS;s++){
      const slot=document.createElement('div');
      slot.className='gate-slot';
      slot.id=`gs-${q}-${s}`;
      slot.onclick=()=>placeGate(q,s);
      const g=circuitGates[q][s];
      if(g){slot.textContent=g;slot.classList.add('filled');}
      wireDiv.appendChild(slot);
    }
    row.appendChild(wireDiv);
    grid.appendChild(row);
    // Wire line
    const line=document.createElement('hr');
    line.style.cssText='border:none;border-top:1px solid rgba(255,255,255,.08);margin:4px 0 4px 32px;';
    grid.appendChild(line);
  }
}

function selectGate(g){
  selectedGate=g;
  document.querySelectorAll('.gate-chip').forEach(c=>c.classList.remove('selected'));
  if(g) document.getElementById('gp-'+g)?.classList.add('selected');
}

function placeGate(q,s){
  if(!selectedGate){circuitGates[q][s]=null;}
  else{circuitGates[q][s]=selectedGate;}
  const slot=document.getElementById(`gs-${q}-${s}`);
  if(circuitGates[q][s]){
    slot.textContent=circuitGates[q][s];
    slot.classList.add('filled');
    const colors={H:'#00d4ff',X:'#a855f7',Y:'#22c55e',Z:'#f59e0b',S:'#ec4899',T:'#06b6d4',CNOT:'#8b5cf6',M:'#f87171'};
    slot.style.borderColor=colors[circuitGates[q][s]]||'var(--cyan)';
    slot.style.color=colors[circuitGates[q][s]]||'var(--cyan)';
    slot.style.background=`${colors[circuitGates[q][s]]||'#00d4ff'}15`;
  } else {
    slot.textContent='';slot.classList.remove('filled');
    slot.style.borderColor='';slot.style.color='';slot.style.background='';
  }
}

function clearCircuit(){
  circuitGates=Array.from({length:QUBITS},()=>Array(STEPS).fill(null));
  initCircuit();
  document.getElementById('circuit-result').style.display='none';
}

function loadBellCircuit(){
  clearCircuit();
  circuitGates[0][0]='H';circuitGates[0][1]='CNOT';circuitGates[1][1]='CNOT';
  circuitGates[0][2]='M';circuitGates[1][2]='M';
  initCircuit();
}

function loadGHZCircuit(){
  clearCircuit();
  circuitGates[0][0]='H';
  circuitGates[0][1]='CNOT';circuitGates[1][1]='CNOT';
  circuitGates[0][2]='CNOT';circuitGates[2][2]='CNOT';
  circuitGates[0][3]='M';circuitGates[1][3]='M';circuitGates[2][3]='M';
  initCircuit();
}

function loadQFTCircuit(){
  clearCircuit();
  circuitGates[0][0]='H';circuitGates[0][1]='S';circuitGates[0][2]='T';
  circuitGates[1][1]='H';circuitGates[1][2]='S';
  circuitGates[2][2]='H';
  circuitGates[0][4]='M';circuitGates[1][4]='M';circuitGates[2][4]='M';
  initCircuit();
}

function runCircuit(){
  // Quantum state simulation
  let state={'0000':1.0};
  const normalize=s=>{const t=Object.values(s).reduce((a,v)=>a+v*v,0);return Object.fromEntries(Object.entries(s).map(([k,v])=>[k,v/Math.sqrt(t)]));}

  for(let step=0;step<STEPS;step++){
    for(let q=0;q<QUBITS;q++){
      const g=circuitGates[q][step];
      if(!g||g==='M')continue;
      const newState={};
      for(const [bits,amp] of Object.entries(state)){
        const b=bits.split('');
        if(g==='H'){
          const k0=[...b];k0[q]='0';const k1=[...b];k1[q]='1';
          newState[k0.join('')]=(newState[k0.join('')]||0)+amp/Math.sqrt(2);
          newState[k1.join('')]=(newState[k1.join('')]||0)+(bits[q]==='0'?1:-1)*amp/Math.sqrt(2);
        } else if(g==='X'){
          const nb=[...b];nb[q]=b[q]==='0'?'1':'0';
          newState[nb.join('')]=(newState[nb.join('')]||0)+amp;
        } else if(g==='CNOT'&&q+1<QUBITS){
          const nb=[...b];
          if(b[q]==='1') nb[q+1]=b[q+1]==='0'?'1':'0';
          newState[nb.join('')]=(newState[nb.join('')]||0)+amp;
        } else if(g==='Z'){
          const nb=[...b];
          newState[bits]=(newState[bits]||0)+(b[q]==='1'?-1:1)*amp;
        } else {
          newState[bits]=(newState[bits]||0)+amp;
        }
      }
      state=newState;
    }
  }

  // Probabilities
  const probs={};
  for(const [k,v] of Object.entries(state)) probs[k]=(v*v);
  const total=Object.values(probs).reduce((a,v)=>a+v,0)||1;
  const sorted=Object.entries(probs).map(([k,v])=>([k,v/total])).sort((a,b)=>b[1]-a[1]).slice(0,8);

  const bars=document.getElementById('result-bars');
  bars.innerHTML='';
  const colors=['#00d4ff','#a855f7','#22c55e','#f59e0b','#ec4899','#06b6d4','#8b5cf6','#f87171'];
  sorted.forEach(([k,v],i)=>{
    const pct=Math.round(v*100);
    bars.innerHTML+=`<div class="result-bar">
      <span class="result-state">|${k}⟩</span>
      <div class="result-track"><div class="result-fill" style="width:${pct}%;background:${colors[i]}"></div></div>
      <span class="result-pct" style="color:${colors[i]}">${pct}%</span>
    </div>`;
  });
  document.getElementById('circuit-result').style.display='block';
}

// ============================================================
// ATOMIC ORBITAL VISUALIZER
// ============================================================
let orbCtx,orbAnimId,currentOrbital='1s';

function initOrbital(){
  const canvas=document.getElementById('orbital-canvas');
  canvas.width=canvas.offsetWidth||900;
  canvas.height=450;
  orbCtx=canvas.getContext('2d');
  if(orbAnimId)cancelAnimationFrame(orbAnimId);
  drawOrbital();
}

function setOrbital(o){
  currentOrbital=o;
  document.querySelectorAll('.orbital-btn').forEach(b=>b.classList.remove('active'));
  event.target.classList.add('active');
  const info={  '1s':'n=1, l=0, m=0 | Spherically symmetric, lowest energy',
    '2s':'n=2, l=0, m=0 | Spherical with one radial node','2p':'n=2, l=1, m=0 | Dumbbell along z-axis',
    '3s':'n=3, l=0 | Two radial nodes','3p':'n=3, l=1 | Dumbbell with node',
    '3d':'n=3, l=2 | Four-lobed cloverleaf','4f':'n=4, l=3 | Complex multi-lobe' };
  document.getElementById('orbital-info').textContent=info[o]||'';
}

function drawOrbital(){
  orbAnimId=requestAnimationFrame(drawOrbital);
  if(!orbCtx)return;
  const W=orbCtx.canvas.width,H=orbCtx.canvas.height;
  orbCtx.fillStyle='rgba(4,4,15,.2)';orbCtx.fillRect(0,0,W,H);
  const cx=W/2,cy=H/2,t5=Date.now()*.001;

  // Compute orbital density points
  const N=2000;
  for(let i=0;i<N;i++){
    const r=Math.random()*180;
    const theta=Math.random()*Math.PI*2;
    const phi2=Math.random()*Math.PI;
    let density=0;
    const ro=r*.05;
    switch(currentOrbital){
      case '1s': density=Math.exp(-ro)*Math.exp(-ro); break;
      case '2s': density=Math.pow(2-ro,2)*Math.exp(-ro/2)*.3; density*=density; break;
      case '2p': density=ro*Math.exp(-ro/2)*Math.abs(Math.cos(phi2)); density=density*density*.5; break;
      case '3s': density=Math.pow(27-18*ro+2*ro*ro,2)*Math.exp(-2*ro/3)*.001; break;
      case '3p': density=ro*(6-ro)*Math.exp(-ro/3)*Math.abs(Math.cos(phi2)); density=density*density*.003; break;
      case '3d': density=ro*ro*Math.exp(-ro/3)*Math.abs(Math.cos(phi2)*Math.sin(phi2)); density=density*density*.02; break;
      case '4f': density=ro*ro*ro*Math.exp(-ro/4)*Math.abs(Math.cos(phi2)*Math.pow(Math.sin(phi2),2)); density=density*density*.001; break;
    }
    if(Math.random()>density*20)continue;
    // 3D to 2D projection (rotating)
    const x3=r*Math.sin(phi2)*Math.cos(theta+t5*.3);
    const y3=r*Math.cos(phi2);
    const z3=r*Math.sin(phi2)*Math.sin(theta+t5*.3);
    const px=cx+x3;
    const py=cy+y3;
    const bright=Math.min(1,density*15);
    const blue=Math.floor((1-z3/180)*100);
    orbCtx.beginPath();
    orbCtx.arc(px,py,1.2,0,Math.PI*2);
    if(density>.3) orbCtx.fillStyle=`rgba(0,212,255,${bright*.8})`;
    else if(density>.1) orbCtx.fillStyle=`rgba(168,85,247,${bright*.6})`;
    else orbCtx.fillStyle=`rgba(255,255,255,${bright*.3})`;
    orbCtx.fill();
  }

  // Nucleus
  orbCtx.beginPath();orbCtx.arc(cx,cy,6,0,Math.PI*2);
  orbCtx.fillStyle='#fff';orbCtx.fill();
  orbCtx.shadowColor='#00d4ff';orbCtx.shadowBlur=20;orbCtx.fill();orbCtx.shadowBlur=0;
}

// ============================================================
// INIT
// ============================================================
window.onload=()=>{
  initCircuit();
};
</script>
</body>
</html>
'''

with open('/data/quantumverse_3d.html','w',encoding='utf-8') as f:
    f.write(html)
print('Written: quantumverse_3d.html', len(html), 'bytes')
