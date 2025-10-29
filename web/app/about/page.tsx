import {Navigation} from "@/components/navigation"

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

      </div>
    </main>
  )
}
