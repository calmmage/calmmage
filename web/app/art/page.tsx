"use client"

import Link from "next/link"
import {Navigation} from "@/components/navigation"

const artPieces = [
  {
    title: "Interactive Particle Field",
    description:
      "Original background animation from the sidebar layout. Move the pointer and explore the depth of the particle cloud.",
    src: "/particles/index.html",
  },
]

const particleSimulations = [
  {title: "Heart", src: "/showcase/demo6-heart/index.html"},
  {title: "Square", src: "/showcase/demo5-square/index.html"},
  {title: "Fast Circle", src: "/showcase/demo1-fast-circle/index.html"},
  {title: "Slow Circle", src: "/showcase/demo2-slow-circle/index.html"},
  {title: "Lemniscate", src: "/showcase/demo3-lemniscate/index.html"},
  {title: "Tube", src: "/showcase/demo4-tube/index.html"},
]

export default function ArtPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="mx-auto max-w-5xl px-6 pb-24 pt-24 md:pt-28">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-foreground md:text-5xl">Art &amp; Motion</h1>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground md:text-lg">
            Experiments that sit between code and visual play. Everything below ships directly from the original site.
          </p>
        </header>

        <div className="mt-16 space-y-16">
          {artPieces.map((piece) => (
            <section
              key={piece.title}
              className="rounded-2xl border border-border/60 bg-card/40 p-6 backdrop-blur transition hover:border-primary/60 hover:bg-card/70"
            >
              <div className="space-y-4 text-center">
                <h2 className="text-2xl font-semibold text-foreground">{piece.title}</h2>
                <p className="text-sm leading-relaxed text-muted-foreground md:text-base">{piece.description}</p>
              </div>
              <div className="mt-8 overflow-hidden rounded-2xl border border-border/60 bg-background/60">
                <iframe
                  title={piece.title}
                  src={piece.src}
                  loading="lazy"
                  scrolling="no"
                  className="h-[520px] w-full border-0"
                />
              </div>
            </section>
          ))}
        </div>

        <section className="mt-24">
          <div className="mb-8 text-center">
            <h2 className="text-3xl font-semibold text-foreground">Particle Simulations</h2>
            <p className="mt-2 text-sm text-muted-foreground md:text-base">
              Interactive motion experiments. Click any simulation to view it full-page.
            </p>
          </div>

          <div className="grid gap-8 lg:grid-cols-2">
            {particleSimulations.map((demo) => (
              <Link
                key={demo.title}
                href={demo.src}
                target="_blank"
                rel="noopener noreferrer"
                className="group h-full rounded-2xl border border-border/60 bg-card/40 p-4 backdrop-blur transition hover:border-primary/60 hover:bg-card/70 cursor-pointer"
              >
                <h3 className="text-lg font-semibold text-foreground mb-4 group-hover:text-primary transition-colors">
                  {demo.title}
                </h3>
                <div className="overflow-hidden rounded-xl border border-border/60 bg-background/60 pointer-events-none">
                  <iframe
                    title={demo.title}
                    src={demo.src}
                    loading="lazy"
                    scrolling="no"
                    className="h-[420px] w-full border-0"
                  />
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}
