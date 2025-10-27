import {Navigation} from "@/components/navigation"

const feeds = [
  {
    title: "Substack — petrlavrov",
    href: "https://petrlavrov.substack.com/",
    description: "Thoughts on tech and life. Long-form reflections, experiments, and essays.",
  },
  {
    title: "Telegram — Life and philosophy",
    href: "https://t.me/petrlavrov",
    description: "Stream-of-consciousness notes, travel fragments, and moments captured in motion.",
  },
  {
    title: "Telegram — calmmageDev",
    href: "https://t.me/calmmageDev",
    description: "Shipping logs, engineering breakdowns, and behind-the-scenes context.",
  },
]

export default function BlogPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="mx-auto max-w-4xl px-6 pb-24 pt-24 md:pt-28">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-foreground md:text-5xl">Writing &amp; Streams</h1>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground md:text-lg">
            The feeds that stay active even when this site is quiet.
          </p>
        </header>

        <div className="mt-16 space-y-6">
          {feeds.map((feed) => (
            <a
              key={feed.title}
              href={feed.href}
              target="_blank"
              rel="noopener noreferrer"
              className="block rounded-2xl border border-border/60 bg-card/40 p-6 text-left transition hover:border-primary/60 hover:bg-card/70"
            >
              <h2 className="text-xl font-semibold text-foreground">{feed.title}</h2>
              <p className="mt-2 text-sm text-muted-foreground md:text-base">{feed.description}</p>
              <span className="mt-4 inline-flex items-center text-sm font-medium text-primary">
                Read now →
              </span>
            </a>
          ))}
        </div>
      </div>
    </main>
  )
}
