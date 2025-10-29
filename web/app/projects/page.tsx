import {Navigation} from "@/components/navigation"

export default function ProjectsPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="mx-auto max-w-6xl px-6 pb-24 pt-24 md:pt-28">
        <header className="text-center">
          <h1 className="text-4xl font-bold text-foreground md:text-5xl">Projects</h1>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground md:text-lg">
            Coming soon...
          </p>
        </header>
      </div>
    </main>
  )
}
