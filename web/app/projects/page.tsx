import {Navigation} from "@/components/navigation"

const demos = [
  {title: "Demo 6 — Heart", src: "/showcase/demo6-heart/index.html"},
  {title: "Demo 5 — Square", src: "/showcase/demo5-square/index.html"},
  {title: "Demo 1 — Fast Circle", src: "/showcase/demo1-fast-circle/index.html"},
  {title: "Demo 2 — Slow Circle", src: "/showcase/demo2-slow-circle/index.html"},
  {title: "Demo 3 — Lemniscate", src: "/showcase/demo3-lemniscate/index.html"},
  {title: "Demo 4 — Tube", src: "/showcase/demo4-tube/index.html"},
]

export default function ProjectsPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="mx-auto max-w-6xl px-6 pb-24 pt-24 md:pt-28">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-foreground md:text-5xl">Petr Lavrov Projects Showcase</h1>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground md:text-lg">
            Interactive demos, motion experiments, and code sketches collected from the original personal site.
          </p>
        </header>

        <div className="mt-16 grid gap-8 lg:grid-cols-2">
          {demos.map((demo) => (
            <div
              key={demo.title}
              className="h-full rounded-2xl border border-border/60 bg-card/40 p-4 backdrop-blur transition hover:border-primary/60 hover:bg-card/70"
            >
              <h2 className="text-lg font-semibold text-foreground">{demo.title}</h2>
              <div className="mt-4 overflow-hidden rounded-xl border border-border/60 bg-background/60">
                <iframe
                  title={demo.title}
                  src={demo.src}
                  loading="lazy"
                  scrolling="no"
                  className="h-[420px] w-full border-0"
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}
