import Link from "next/link"
import {Navigation} from "@/components/navigation"
import {HeroSection} from "@/components/hero-section"
import {sections} from "@/lib/sections"

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <HeroSection/>
      <section id="explore" className="relative z-10 bg-background">
        <div className="mx-auto max-w-6xl px-6 pb-24">
          {sections.map((section) => (
            <div key={section.name} className="border-b border-border/60 py-16">
              <div className="mb-8 flex items-center justify-between">
                <h2 className="text-sm font-semibold uppercase tracking-[0.3em] text-muted-foreground">
                  {section.name}
                </h2>
                <div className="h-px flex-1 bg-border/70 ml-6"/>
              </div>

              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {section.items.map((item) => {
                  const content = (
                    <div className="flex h-full flex-col justify-between rounded-xl border border-border/60 bg-card/40 p-6 transition-all duration-200 hover:-translate-y-1 hover:border-primary/60 hover:bg-card/70">
                      <div>
                        <h3 className="text-lg font-semibold text-foreground">{item.name}</h3>
                        {item.description ? (
                          <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
                            {item.description}
                          </p>
                        ) : null}
                      </div>
                      <span className="mt-6 text-sm font-medium text-primary">Open →</span>
                    </div>
                  )

                  return item.external ? (
                    <a
                      key={item.name}
                      href={item.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="h-full"
                    >
                      {content}
                    </a>
                  ) : (
                    <Link key={item.name} href={item.href} className="h-full">
                      {content}
                    </Link>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
