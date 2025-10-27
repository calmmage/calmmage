import {Navigation} from "@/components/navigation"

const artPieces = [
  {
    title: "Interactive Particle Field",
    description:
      "Original background animation from the sidebar layout. Move the pointer and explore the depth of the particle cloud.",
    src: "/particles/index.html",
  },
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
      </div>
    </main>
  )
}
