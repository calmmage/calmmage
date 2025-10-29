"use client"

import {useState} from "react"
import {Navigation} from "@/components/navigation"

const particleSimulations = [
  {title: "Interactive Particle Field", src: "/particles/index.html"},
  {title: "Heart", src: "/showcase/demo6-heart/index.html"},
  {title: "Square", src: "/showcase/demo5-square/index.html"},
  {title: "Fast Circle", src: "/showcase/demo1-fast-circle/index.html"},
  {title: "Slow Circle", src: "/showcase/demo2-slow-circle/index.html"},
  {title: "Lemniscate", src: "/showcase/demo3-lemniscate/index.html"},
  {title: "Tube", src: "/showcase/demo4-tube/index.html"},
]

export default function ArtPage() {
  const [selectedDemo, setSelectedDemo] = useState<string | null>(null)

  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="flex gap-6 px-6 pb-24 pt-24 md:pt-28">
        {/* Sidebar */}
        <aside className="w-64 flex-shrink-0">
          <div className="sticky top-24 space-y-2">
            <button
              onClick={() => setSelectedDemo(null)}
              className="w-full rounded-lg border border-border/60 bg-card/40 px-4 py-3 text-left font-semibold text-foreground transition hover:border-primary/60 hover:bg-card/70"
            >
              Particle Simulations
            </button>
            <div className="space-y-1 pl-4">
              {particleSimulations.map((demo) => (
                <button
                  key={demo.title}
                  onClick={() => setSelectedDemo(demo.title)}
                  className={`w-full rounded-md px-3 py-2 text-left text-sm transition ${
                    selectedDemo === demo.title
                      ? "bg-primary/20 text-primary font-medium"
                      : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                  }`}
                >
                  {demo.title}
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <div className="flex-1">
          <header className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-foreground md:text-5xl">Art &amp; Motion</h1>
            <p className="mt-4 text-base leading-relaxed text-muted-foreground md:text-lg">
              Interactive motion experiments. Click any simulation to explore.
            </p>
          </header>

          {selectedDemo === null ? (
            // Grid view - all demos
            <div className="grid gap-6 md:grid-cols-2">
              {particleSimulations.map((demo) => (
                <div
                  key={demo.title}
                  className="rounded-2xl border border-border/60 bg-card/40 p-4 backdrop-blur transition hover:border-primary/60 hover:bg-card/70"
                >
                  <button
                    onClick={() => setSelectedDemo(demo.title)}
                    className="mb-3 text-lg font-semibold text-foreground hover:text-primary transition-colors"
                  >
                    {demo.title}
                  </button>
                  <div className="overflow-hidden rounded-xl border border-border/60 bg-background/60 aspect-square">
                    <iframe
                      title={demo.title}
                      src={demo.src}
                      loading="lazy"
                      scrolling="no"
                      className="h-full w-full border-0"
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            // Single demo view
            <div className="rounded-2xl border border-border/60 bg-card/40 p-6 backdrop-blur">
              <h2 className="mb-6 text-2xl font-semibold text-foreground">{selectedDemo}</h2>
              <div className="overflow-hidden rounded-xl border border-border/60 bg-background/60">
                <iframe
                  title={selectedDemo}
                  src={particleSimulations.find((d) => d.title === selectedDemo)?.src}
                  loading="lazy"
                  scrolling="no"
                  className="h-[600px] w-full border-0 md:h-[700px]"
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
