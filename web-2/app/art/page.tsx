import {Navigation} from "@/components/navigation"

export default function ArtPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navigation/>
      <div className="pt-20 px-6 max-w-4xl mx-auto">
        <div className="py-20 text-center">
          <h1 className="text-4xl font-bold text-foreground mb-4">Art</h1>
          <p className="text-muted-foreground text-lg">Coming soon...</p>
        </div>
      </div>
    </main>
  )
}
