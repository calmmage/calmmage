import Link from "next/link"
import {Navigation} from "@/components/navigation"

const NGINX_CONFIG_PATH = "K:/Program Files/nginx/conf/nginx.conf"

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="mx-auto max-w-4xl px-6 pb-24 pt-24 md:pt-28">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-foreground md:text-5xl">Hi there! 👋</h1>
          <p className="mt-4 text-lg text-muted-foreground">
            <strong className="font-semibold text-foreground">Петр Лавров</strong> • 32 • Zurich
          </p>
          <p className="mt-6 text-base leading-relaxed text-muted-foreground md:text-lg">
            Husband, Father, Son, Brother, Friend.<br/>
            Engineer, Experimenter, Mentor, Student.<br/>
            Looking for deep meaningful connections<br/>
            with people who have energy, wisdom, and drive.
          </p>
        </header>

        <section className="mt-16 space-y-8">
          <div className="space-y-4 text-center">
            <h2 className="text-2xl font-semibold text-foreground">🛤️ Journey</h2>
            <div className="space-y-2 text-sm text-muted-foreground md:text-base">
              <p>BlankFactor ← Magic Leap ← Google ← Luxoft ← Yandex ← WorldQuant ← МГУ</p>
              <p>Zürich ← Moscow ← Perm</p>
              <p>LLMs ← AR ← SWE ← Finance ← Mathematics ← Physics</p>
            </div>
          </div>

          <div className="space-y-4 text-center">
            <h2 className="text-2xl font-semibold text-foreground">🎨 Projects &amp; Writing</h2>
            <div className="space-y-2 text-sm text-muted-foreground md:text-base">
              <p>
                <a className="text-primary hover:text-primary/80" href="https://constellations.calmmage.com/">
                  Constellations
                </a>{" "}
                - Interactive constellation visualizations
              </p>
              <p>
                <a className="text-primary hover:text-primary/80" href="https://petrlavrov.substack.com/">
                  Blog
                </a>{" "}
                - Thoughts on tech and life
              </p>
              <p>
                <a className="text-primary hover:text-primary/80" href="https://t.me/petrlavrov">
                  t.me/petrlavrov
                </a>{" "}
                - Life and philosophy
              </p>
              <p>
                <a className="text-primary hover:text-primary/80" href="https://t.me/calmmageDev">
                  t.me/calmmageDev
                </a>{" "}
                - About coding
              </p>
            </div>
          </div>

          <div className="space-y-4 text-center">
            <h2 className="text-2xl font-semibold text-foreground">🏔️ Life</h2>
            <p className="text-sm leading-relaxed text-muted-foreground md:text-base">
              📖 Reading • 📜 Poetry • 🛤️{" "}
              <a className="text-primary hover:text-primary/80" href="https://www.instagram.com/beware.life_is_awesome/">
                Travel &amp; photography
              </a>
              <br/>
              🧘{" "}
              <a className="text-primary hover:text-primary/80" href="https://internationalmeditationcentre.org/">
                Vipassana
              </a>{" "}
              • 🏔️ Mountaineering • 🏊 Swimming
              <br/>
              ⚔️{" "}
              <a className="text-primary hover:text-primary/80" href="https://youtu.be/Rl65iVOV12U">
                Beat Saber
              </a>{" "}
              • 🤹‍♀️ Juggling • 🤸‍♀️ Yoga23
            </p>
          </div>
        </section>

        <section className="mt-20 space-y-8">
          <div>
            <h2 className="text-xl font-semibold text-foreground">Additional Pages</h2>
            <p className="mt-2 text-sm text-muted-foreground md:text-base">
              Legacy notes now live here for quick reference.
            </p>
            <div className="mt-6 grid gap-4 md:grid-cols-2">
              <Link
                href="#hosting"
                className="rounded-lg border border-border/60 bg-card/40 p-4 text-sm text-foreground transition hover:border-primary/60 hover:bg-card/70 md:text-base"
              >
                NGINX setup help Page
              </Link>
              <Link
                href="#help"
                className="rounded-lg border border-border/60 bg-card/40 p-4 text-sm text-foreground transition hover:border-primary/60 hover:bg-card/70 md:text-base"
              >
                General calmmage Help Page
              </Link>
            </div>
          </div>

          <div id="help" className="space-y-4 rounded-xl border border-border/50 bg-card/30 p-6">
            <h2 className="text-2xl font-semibold text-foreground">Help &amp; Hosting</h2>
            <p className="text-sm text-muted-foreground md:text-base">
              This page provides information about my hosting and other related resources. Please find the relevant links
              below:
            </p>
            <div>
              <h3 className="text-lg font-semibold text-foreground">Personal Resources</h3>
              <ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-muted-foreground md:text-base">
                <li>
                  <a
                    className="text-primary hover:text-primary/80"
                    href="http://coolify.calmmage.com"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Coolify
                  </a>{" "}
                  - My personal deployment and container management tool
                </li>
                <li>
                  <a
                    className="text-primary hover:text-primary/80"
                    href="http://n8n.calmmage.com"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    N8N
                  </a>{" "}
                  - My personal automation tool
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">Public Resources</h3>
              <ul className="mt-2 list-disc space-y-2 pl-5 text-sm text-muted-foreground md:text-base">
                <li>
                  <a
                    className="text-primary hover:text-primary/80"
                    href="http://hetzner.calmmage.com"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Hetzner
                  </a>{" "}
                  - A publicly available Coolify instance
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">Contact</h3>
              <p className="text-sm text-muted-foreground md:text-base">
                For any queries or concerns, feel free to{" "}
                <a className="text-primary hover:text-primary/80" href="mailto:petrlavrov@calmmage.com">
                  email me
                </a>
                .
              </p>
            </div>
          </div>

          <div
            id="hosting"
            className="space-y-6 rounded-xl border border-border/50 bg-card/30 p-6 md:p-8"
          >
            <h2 className="text-2xl font-semibold text-foreground">NGINX Configuration Instructions</h2>
            <p className="text-sm text-muted-foreground md:text-base">
              Edit NGINX config at{" "}
              <code className="rounded bg-secondary px-1 py-0.5 text-foreground">{NGINX_CONFIG_PATH}</code> and reload NGINX when needed.
            </p>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-lg border border-border/60 bg-background/40 p-4 transition hover:border-primary/60 hover:bg-background/80">
                <h3 className="text-lg font-semibold text-foreground">Generating New SSL Certificate</h3>
                <p className="mt-2 text-sm text-muted-foreground md:text-base">
                  Launch Admin PowerShell and run:
                </p>
                <code className="mt-3 block rounded bg-secondary px-3 py-2 text-sm text-foreground">
                  certbot certonly --standalone -d calmmage.com
                </code>
              </div>

              <div className="rounded-lg border border-border/60 bg-background/40 p-4 transition hover:border-primary/60 hover:bg-background/80">
                <h3 className="text-lg font-semibold text-foreground">Port Forwarding</h3>
                <p className="mt-2 text-sm text-muted-foreground md:text-base">
                  Access your router at{" "}
                  <a className="text-primary hover:text-primary/80" href="http://192.168.1.1">
                    192.168.1.1
                  </a>{" "}
                  and navigate to Port Forwarding.
                </p>
              </div>

              <div className="rounded-lg border border-border/60 bg-background/40 p-4 transition hover:border-primary/60 hover:bg-background/80">
                <h3 className="text-lg font-semibold text-foreground">Adding New Subdomain Routing</h3>
                <p className="mt-2 text-sm text-muted-foreground md:text-base">
                  Edit the config and reload:
                </p>
                <code className="mt-3 block rounded bg-secondary px-3 py-2 text-sm text-foreground">
                  nginx -s reload
                </code>
              </div>

              <div className="rounded-lg border border-border/60 bg-background/40 p-4 transition hover:border-primary/60 hover:bg-background/80">
                <h3 className="text-lg font-semibold text-foreground">Setup domain calmmage.com</h3>
                <p className="mt-2 text-sm text-muted-foreground md:text-base">
                  Configure DNS settings at{" "}
                  <a
                    className="text-primary hover:text-primary/80"
                    href="https://apple-emu-f57h.squarespace.com/config/domains/managed/calmmage.com/dns-settings"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Squarespace DNS Settings
                  </a>
                  .
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}
