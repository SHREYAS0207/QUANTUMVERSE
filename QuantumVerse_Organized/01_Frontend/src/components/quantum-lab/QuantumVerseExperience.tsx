"use client";

import { useMemo, useState } from "react";
import { Activity, ArrowRight, Atom, BrainCircuit, CheckCircle2, Gauge, Sparkles } from "lucide-react";
import styles from "./QuantumVerseExperience.module.css";

type StateRow = { label: string; probability: number };

const states: StateRow[] = [
  { label: "|00⟩", probability: 50 },
  { label: "|01⟩", probability: 0 },
  { label: "|10⟩", probability: 0 },
  { label: "|11⟩", probability: 50 },
];

/**
 * SIH showcase surface for the existing dashboard/quantum-lab route.
 * It is intentionally API-agnostic: wire the existing simulation service to
 * `states` and `progress` after reviewing the visual layer.
 */
export function QuantumVerseExperience() {
  const [activeTab, setActiveTab] = useState<"overview" | "circuit" | "learn">("overview");
  const [running, setRunning] = useState(false);
  const progress = useMemo(() => (running ? 100 : 72), [running]);

  return (
    <section className={styles.page} aria-label="QuantumVerse learning dashboard">
      <div className={styles.ambient} aria-hidden="true" />
      <header className={styles.header}>
        <div className={styles.brand}><span className={styles.brandOrb}><Atom size={20} /></span><span>QuantumVerse</span></div>
        <div className={styles.badge}><Sparkles size={14} /> SIH 2026 · Problem 26140</div>
        <nav className={styles.tabs} aria-label="Dashboard sections">
          {(["overview", "circuit", "learn"] as const).map((tab) => (
            <button key={tab} className={activeTab === tab ? styles.activeTab : ""} onClick={() => setActiveTab(tab)}>{tab}</button>
          ))}
        </nav>
      </header>

      <div className={styles.heroGrid}>
        <article className={`${styles.panel} ${styles.hero}`}>
          <p className={styles.kicker}>Interactive quantum learning studio</p>
          <h1>See quantum.<br /><span>Build intuition.</span></h1>
          <p className={styles.subtitle}>Explore states, compose circuits, simulate outcomes, and learn through guided challenges in one visual workspace.</p>
          <div className={styles.actions}><button className={styles.primary} onClick={() => setRunning(true)}>{running ? "Simulation complete" : "Run guided simulation"} <ArrowRight size={16} /></button><button className={styles.secondary}>View learning path</button></div>
          <div className={styles.metrics}><div><strong>72%</strong><small>Progress</small></div><div><strong>18</strong><small>Circuits</small></div><div><strong>94%</strong><small>Accuracy</small></div></div>
        </article>
        <article className={`${styles.panel} ${styles.bloch}`}>
          <div className={`${styles.ring} ${styles.ringOne}`} /><div className={`${styles.ring} ${styles.ringTwo}`} /><div className={styles.axis} /><div className={styles.sphere}><div className={styles.latitude} /><div className={styles.longitude} /></div>
          <div className={styles.blochLabel}><Gauge size={15} /> Live state · Bell pair</div>
        </article>
      </div>

      <div className={styles.cards}>
        <article className={styles.panel}>
          <div className={styles.cardTitle}><div><p className={styles.kicker}>Current module</p><h2>Quantum states</h2></div><BrainCircuit size={22} /></div>
          <p className={styles.muted}>Visualize superposition and measurement probability.</p><div className={styles.progress}><i style={{ width: `${progress}%` }} /></div><small className={styles.muted}>{running ? "Simulation milestone unlocked" : "4 of 6 lessons complete"}</small>
        </article>
        <article className={styles.panel}><div className={styles.cardTitle}><div><p className={styles.kicker}>Circuit preview</p><h2>Bell state experiment</h2></div><Activity size={22} /></div><div className={styles.gates}><span>H</span><span>•</span><span>X</span><span>M</span></div><p className={styles.muted}>A guided circuit keeps first-time learners oriented.</p></article>
        <article className={styles.panel}><div className={styles.cardTitle}><div><p className={styles.kicker}>Measurement output</p><h2>Probability map</h2></div><CheckCircle2 size={22} /></div>{states.map((state) => <div className={styles.state} key={state.label}><span>{state.label}</span><div><i style={{ width: `${Math.max(state.probability, 2)}%` }} /></div><b>{state.probability}%</b></div>)}</article>
      </div>
    </section>
  );
}
