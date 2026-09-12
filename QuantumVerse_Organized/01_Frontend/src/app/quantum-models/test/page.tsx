"use client";
import ProbabilityCrossSection from "@/components/quantum-models/ProbabilityCrossSection";
import { useMemo, useState } from "react";
import OrbitalViewer from "@/components/quantum-models/OrbitalViewer";

interface OrbitalPoint {
  x: number;
  y: number;
  z: number;
  density: number;
}

interface SimulationResponse {
  success: boolean;
  atom: string;
  n: number;
  l: number;
  m: number;
  orbital: string;
  energy_ev: number;
  bohr_radius_m: number;
  point_count: number;

  probability_cloud: {
    x: number[];
    y: number[];
    z: number[];
    density: number[];
  };

  cross_section: {
    x: number[];
    z: number[];
    density: number[];
  };

  error?: string | null;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function QuantumModelTestPage() {
  const [n, setN] = useState(2);
  const [l, setL] = useState(1);
  const [m, setM] = useState(0);

  const [result, setResult] = useState<SimulationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const maxL = n - 1;

  const availableM = useMemo(() => {
    const values: number[] = [];
    for (let value = -l; value <= l; value++) {
      values.push(value);
    }
    return values;
  }, [l]);

  const runSimulation = async () => {
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("qv_token");

      if (!token) {
        throw new Error("Please log in before running the simulation.");
      }

      const response = await fetch(
        `${API_URL}/quantum-models/atomic/simulate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            n,
            l,
            m,
            grid_size: 35,
            extent: 12,
            threshold: 0.03,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Simulation failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to run simulation."
      );
    } finally {
      setLoading(false);
    }
  };

  const points: OrbitalPoint[] = useMemo(() => {
    if (!result) return [];

    return result.probability_cloud.x.map((x, index) => ({
      x,
      y: result.probability_cloud.y[index],
      z: result.probability_cloud.z[index],
      density: result.probability_cloud.density[index],
    }));
  }, [result]);

  const handleNChange = (value: number) => {
    setN(value);

    const newMaxL = value - 1;

    if (l > newMaxL) {
      setL(newMaxL);

      if (m > newMaxL) {
        setM(0);
      }
    }
  };

  const handleLChange = (value: number) => {
    setL(value);

    if (Math.abs(m) > value) {
      setM(0);
    }
  };

  return (
    <main className="min-h-screen bg-black px-5 py-8 text-white">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold">
            Quantum Model — Hydrogen Atom
          </h1>

          <p className="mt-2 text-white/60">
            Analytical hydrogen wavefunction and 3D probability-density
            visualization.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[300px_1fr]">
          <section className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
            <h2 className="mb-5 text-lg font-semibold">
              Quantum State
            </h2>

            <div className="space-y-5">
              <div>
                <label className="mb-2 block text-sm text-white/60">
                  Principal quantum number — n
                </label>

                <select
                  value={n}
                  onChange={(e) => handleNChange(Number(e.target.value))}
                  className="w-full rounded-lg border border-white/10 bg-black px-3 py-2 text-white"
                >
                  {[1, 2, 3, 4, 5, 6].map((value) => (
                    <option key={value} value={value}>
                      n = {value}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm text-white/60">
                  Angular momentum — l
                </label>

                <select
                  value={l}
                  onChange={(e) => handleLChange(Number(e.target.value))}
                  className="w-full rounded-lg border border-white/10 bg-black px-3 py-2 text-white"
                >
                  {Array.from({ length: maxL + 1 }, (_, value) => (
                    <option key={value} value={value}>
                      l = {value}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm text-white/60">
                  Magnetic quantum number — m
                </label>

                <select
                  value={m}
                  onChange={(e) => setM(Number(e.target.value))}
                  className="w-full rounded-lg border border-white/10 bg-black px-3 py-2 text-white"
                >
                  {availableM.map((value) => (
                    <option key={value} value={value}>
                      m = {value}
                    </option>
                  ))}
                </select>
              </div>

              <button
                onClick={runSimulation}
                disabled={loading}
                className="w-full rounded-lg bg-cyan-500 px-4 py-3 font-semibold text-black transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Running Simulation..." : "Run Simulation"}
              </button>

              {error && (
                <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
                  {error}
                </div>
              )}
            </div>

            {result && (
              <div className="mt-6 space-y-3 border-t border-white/10 pt-5">
                <h3 className="font-semibold">Simulation Results</h3>

                <div className="text-sm text-white/60">
                  <div className="flex justify-between py-1">
                    <span>Atom</span>
                    <span className="text-white">{result.atom}</span>
                  </div>

                  <div className="flex justify-between py-1">
                    <span>Orbital</span>
                    <span className="text-white">{result.orbital}</span>
                  </div>

                  <div className="flex justify-between py-1">
                    <span>Energy</span>
                    <span className="text-white">
                      {result.energy_ev.toFixed(6)} eV
                    </span>
                  </div>

                  <div className="flex justify-between py-1">
                    <span>Cloud points</span>
                    <span className="text-white">
                      {result.point_count.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </section>

          <section className="min-w-0 space-y-6">
            <OrbitalViewer
              points={points}
              title={
                result
                  ? `${result.orbital} Hydrogen Orbital`
                  : "Hydrogen Orbital"
             }
            />

            {result && (
              <ProbabilityCrossSection
                x={result.cross_section.x}
                z={result.cross_section.z}
                density={result.cross_section.density}
                gridSize={80}
              />
          )}
        </section>
        </div>
      </div>
    </main>
  );
}