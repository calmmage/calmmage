import type {LucideIcon} from "lucide-react"
import {Navigation} from "@/components/navigation"
import {lifeIcons, sectionIcons} from "@/lib/icons"
import {copy, type Locale} from "@/lib/i18n"
import {site} from "@/lib/site"

function SectionTitle({icon: Icon, children}: {icon: LucideIcon; children: string}) {
  return (
    <h2 className="flex items-center justify-center gap-2.5 text-2xl font-semibold text-foreground">
      <Icon aria-hidden className="h-[1.15em] w-[1.15em] text-primary" strokeWidth={1.5} />
      {children}
    </h2>
  )
}

export function AboutView({locale}: {locale: Locale}) {
  const t = copy[locale]
  const BookIcon = sectionIcons.bookChat

  return (
    <main className="min-h-screen bg-background">
      <Navigation locale={locale} />
      <div className="mx-auto max-w-4xl px-6 pb-24 pt-24 md:pt-28">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-foreground md:text-5xl">{t.name}</h1>
          <p className="mt-4 text-lg text-muted-foreground">{t.identity}</p>
          <p className="mt-6 text-base leading-relaxed text-muted-foreground md:text-lg">
            {t.bio.map((line, i) => (
              <span key={line}>
                {i > 0 && <br />}
                {line}
              </span>
            ))}
          </p>
          <a
            href={site.bookingUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-8 inline-flex items-center gap-2 rounded-lg border border-primary/50 px-5 py-2.5 text-sm font-medium text-primary transition-colors hover:bg-primary/10"
          >
            <BookIcon aria-hidden className="h-4 w-4" strokeWidth={1.5} />
            {t.bookChat}
          </a>
        </header>

        <section className="mt-16 space-y-8">
          <div className="space-y-4 text-center">
            <SectionTitle icon={sectionIcons.journey}>{t.journeyTitle}</SectionTitle>
            <div className="space-y-2 text-sm text-muted-foreground md:text-base">
              <p>{t.companies}</p>
              <p>{t.cities}</p>
              <p>{t.fields}</p>
            </div>
          </div>

          <div className="space-y-4 text-center">
            <SectionTitle icon={sectionIcons.projects}>{t.projectsTitle}</SectionTitle>
            <div className="space-y-2 text-sm text-muted-foreground md:text-base">
              {t.projects.map((project) => (
                <p key={project.href}>
                  <a className="text-primary hover:text-primary/80" href={project.href}>
                    {project.label}
                  </a>{" "}
                  — {project.blurb}
                </p>
              ))}
            </div>
          </div>

          <div className="space-y-5 text-center">
            <SectionTitle icon={sectionIcons.life}>{t.lifeTitle}</SectionTitle>
            <ul className="mx-auto flex max-w-xl flex-wrap items-center justify-center gap-x-5 gap-y-3 text-sm text-muted-foreground md:text-base">
              {t.life.map((item) => {
                const Icon = lifeIcons[item.icon]
                const inner = (
                  <>
                    <Icon aria-hidden className="h-4 w-4 text-primary" strokeWidth={1.5} />
                    {item.label}
                  </>
                )
                return (
                  <li key={item.icon}>
                    {item.href ? (
                      <a
                        href={item.href}
                        className="inline-flex items-center gap-1.5 text-primary hover:text-primary/80"
                      >
                        {inner}
                      </a>
                    ) : (
                      <span className="inline-flex items-center gap-1.5">{inner}</span>
                    )}
                  </li>
                )
              })}
            </ul>
          </div>
        </section>
      </div>
    </main>
  )
}
