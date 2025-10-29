import Link from "next/link"
import {Navigation} from "@/components/navigation"
import {getBlogPosts} from "@/lib/blog"

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
  const posts = getBlogPosts()

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

        {posts.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-semibold text-foreground mb-6">Blog Posts</h2>
            <div className="space-y-6">
              {posts.map((post) => (
                <Link
                  key={post.slug}
                  href={`/blog/${post.slug}`}
                  className="block rounded-2xl border border-border/60 bg-card/40 p-6 text-left transition hover:border-primary/60 hover:bg-card/70"
                >
                  <h3 className="text-xl font-semibold text-foreground">{post.title}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">{post.date}</p>
                  {post.tags.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {post.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded-md bg-secondary px-2 py-1 text-xs text-secondary-foreground"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                  <span className="mt-4 inline-flex items-center text-sm font-medium text-primary">
                    Read more →
                  </span>
                </Link>
              ))}
            </div>
          </div>
        )}

        <div className="mt-16">
          <h2 className="text-2xl font-semibold text-foreground mb-6">External Feeds</h2>
          <div className="space-y-6">
            {feeds.map((feed) => (
              <a
                key={feed.title}
                href={feed.href}
                target="_blank"
                rel="noopener noreferrer"
                className="block rounded-2xl border border-border/60 bg-card/40 p-6 text-left transition hover:border-primary/60 hover:bg-card/70"
              >
                <h3 className="text-xl font-semibold text-foreground">{feed.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground md:text-base">{feed.description}</p>
                <span className="mt-4 inline-flex items-center text-sm font-medium text-primary">
                  Visit →
                </span>
              </a>
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}
