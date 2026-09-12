"use client";

import Link from "next/link";

const models = [
  {
    title: "Hydrogen Atom",
    description:
      "Explore hydrogen electron probability distributions using analytical quantum wavefunctions.",
    details: [
      "Quantum numbers n, l, m",
      "3D orbital visualization",
      "2D probability-density cross-section",
      "Hydrogen energy levels",
    ],
    status: "Available",
    href: "/quantum-models/hydrogen",
  },
  {
    title: "Particle in a Box",
    description:
      "Study quantized energy states and wavefunctions for a particle confined to a one-dimensional box.",
    details: [
      "Energy eigenstates",
      "Wavefunction visualization",
      "Probability density",
      "Energy spectrum",
    ],
    status: "Coming Soon",
  },
  {
    title: "Quantum Harmonic Oscillator",
    description:
      "Visualize the quantized states of the quantum harmonic oscillator.",
    details: [
      "Energy eigenstates",
      "Wavefunctions",
      "Probability distributions",
      "Quantum numbers",
    ],
    status: "Coming Soon",
  },
  {
    title: "Quantum Tunneling",
    description:
      "Explore how quantum particles can pass through classically forbidden potential barriers.",
    details: [
      "Potential barrier",
      "Incident wavefunction",
      "Transmission probability",
      "Reflection probability",
    ],
    status: "Coming Soon",
  },
];

export default function QuantumModelsPage() {
  return (
    <main className="min-h-screen bg-black px-5 py-10 text-white">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <section className="mb-12">
          <div className="mb-3 inline-flex rounded-full border border-cyan-400/20 bg-cyan-400/5 px-3 py-1 text-xs font-medium text-cyan-300">
            PHYSICAL QUANTUM SYSTEMS
          </div>

          <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
            Quantum Models
          </h1>

          <p className="mt-4 max-w-3xl text-base leading-7 text-white/55 md:text-lg">
            Explore physical quantum systems through mathematical models,
            numerical calculations, and interactive visualizations.
          </p>
        </section>

        {/* Introduction */}
        <section className="mb-10 rounded-2xl border border-white/10 bg-white/[0.025] p-6">
          <div className="grid gap-8 md:grid-cols-3">
            <div>
              <div className="mb-3 text-2xl">ψ</div>
              <h2 className="font-semibold">Quantum Mathematics</h2>
              <p className="mt-2 text-sm leading-6 text-white/50">
                Work with wavefunctions, quantum numbers, energy eigenvalues,
                and probability densities.
              </p>
            </div>

            <div>
              <div className="mb-3 text-2xl">∣ψ∣²</div>
              <h2 className="font-semibold">Probability Density</h2>
              <p className="mt-2 text-sm leading-6 text-white/50">
                Visualize where a quantum particle is more or less likely to
                be detected.
              </p>
            </div>

            <div>
              <div className="mb-3 text-2xl">3D</div>
              <h2 className="font-semibold">Interactive Models</h2>
              <p className="mt-2 text-sm leading-6 text-white/50">
                Rotate, inspect, and explore quantum states through interactive
                visual representations.
              </p>
            </div>
          </div>
        </section>

        {/* Available models */}
        <section>
          <div className="mb-5">
            <h2 className="text-2xl font-semibold">
              Explore Models
            </h2>

            <p className="mt-1 text-sm text-white/45">
              Select a physical system to begin the simulation.
            </p>
          </div>

          <div className="grid gap-5 md:grid-cols-2">
            {models.map((model) => {
              const available = model.status === "Available";

              return (
                <div
                  key={model.title}
                  className="group rounded-2xl border border-white/10 bg-white/[0.025] p-6 transition hover:border-cyan-400/30 hover:bg-white/[0.04]"
                >
                  <div className="mb-5 flex items-start justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-semibold">
                        {model.title}
                      </h3>

                      <p className="mt-2 text-sm leading-6 text-white/50">
                        {model.description}
                      </p>
                    </div>

                    <span
                      className={`shrink-0 rounded-full px-2.5 py-1 text-xs ${
                        available
                          ? "bg-green-400/10 text-green-300"
                          : "bg-white/5 text-white/40"
                      }`}
                    >
                      {model.status}
                    </span>
                  </div>

                  <div className="mb-6 space-y-2">
                    {model.details.map((detail) => (
                      <div
                        key={detail}
                        className="flex items-center gap-2 text-sm text-white/55"
                      >
                        <span className="text-cyan-400">•</span>
                        {detail}
                      </div>
                    ))}
                  </div>
                    {available && model.href ? (
                        <Link
                            href={model.href}

                      className="inline-flex items-center rounded-lg bg-cyan-500 px-4 py-2.5 text-sm font-semibold text-black transition hover:bg-cyan-400"
                    >
                      Explore Model
                      <span className="ml-2">→</span>
                    </Link>
                  ) : (
                    <button
                      disabled
                      className="cursor-not-allowed rounded-lg border border-white/10 px-4 py-2.5 text-sm text-white/30"
                    >
                      Coming Soon
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Scientific note */}
        <section className="mt-10 rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.03] p-6">
          <h2 className="font-semibold text-cyan-200">
            A note about quantum models
          </h2>

          <p className="mt-2 max-w-4xl text-sm leading-7 text-white/55">
            These simulations describe quantum systems using mathematical
            models. For example, an atomic orbital represents a probability
            distribution derived from a wavefunction. It is not a classical
            path showing an electron traveling around the nucleus.
          </p>
        </section>
      </div>
    </main>
  );
}