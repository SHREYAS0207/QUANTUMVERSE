"use client";

interface ProbabilityCrossSectionProps {
  x: number[];
  z: number[];
  density: number[];
  gridSize?: number;
}

export default function ProbabilityCrossSection({
  x,
  z,
  density,
  gridSize = 80,
}: ProbabilityCrossSectionProps) {
  if (!x.length || !z.length || !density.length) {
    return (
      <div className="flex h-[420px] items-center justify-center rounded-2xl border border-white/10 bg-black text-sm text-white/40">
        No cross-section data available.
      </div>
    );
  }

  const minX = Math.min(...x);
  const maxX = Math.max(...x);


  const cells = x.map((xValue, index) => ({
    x: xValue,
    z: z[index],
    density: density[index],
  }));

  return (
    <div className="rounded-2xl border border-white/10 bg-black p-5">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-white">
          2D Probability-Density Cross-Section
        </h2>

        <p className="mt-1 text-sm text-white/50">
          Slice through the orbital at y = 0. Brighter regions represent
          higher electron probability density.
        </p>
      </div>

      <div
        className="relative mx-auto grid overflow-hidden rounded-xl border border-white/10 bg-black"
        style={{
          gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
          aspectRatio: "1 / 1",
          maxWidth: "560px",
        }}
      >
        {cells.map((cell, index) => {
          const intensity = Math.max(
            0,
            Math.min(1, cell.density)
          );

          const alpha = 0.03 + intensity * 0.97;

          return (
            <div
              key={index}
              title={`Density: ${cell.density.toFixed(3)}`}
              style={{
                background: `rgba(0, 217, 255, ${alpha})`,
              }}
            />
          );
        })}

        {/* Nucleus */}
        <div
          className="pointer-events-none absolute left-1/2 top-1/2 h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white shadow-[0_0_14px_rgba(255,255,255,0.9)]"
          title="Nucleus"
        />

        {/* X axis */}
        <div className="pointer-events-none absolute left-0 right-0 top-1/2 h-px bg-white/20" />

        {/* Z axis */}
        <div className="pointer-events-none absolute bottom-0 left-1/2 top-0 w-px bg-white/20" />
      </div>

      <div className="mx-auto mt-4 flex max-w-[560px] justify-between text-xs text-white/40">
        <span>
          x: {minX.toFixed(1)}
        </span>

        <span>
          x: {maxX.toFixed(1)}
        </span>
      </div>

      <div className="mt-3 flex items-center justify-center gap-3 text-xs text-white/50">
        <span>Low probability</span>

        <div className="h-2 w-32 rounded-full bg-gradient-to-r from-cyan-950 via-cyan-500 to-white" />

        <span>High probability</span>
      </div>
    </div>
  );
}