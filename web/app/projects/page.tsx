import {Navigation} from "@/components/navigation"

export default function ProjectsPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="mx-auto max-w-6xl px-6 pb-24 pt-24 md:pt-28">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-foreground md:text-5xl">Projects</h1>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground md:text-lg">
            Code and experiments live on{" "}
            <a href="https://github.com/calmmage" className="text-primary hover:underline">GitHub</a>.
            {" "}Consulting on LLMs and automation:{" "}
            <a href="https://petrlavrov.com" className="text-primary hover:underline">petrlavrov.com</a>.
          </p>
        </header>
      </div>
    </main>
  )
}
