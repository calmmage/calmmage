"use client"

import Link from "next/link"
import {ParticleAnimation} from "./particle-animation"

export function HeroSection() {
  return (
    <section className="relative w-full h-screen flex items-center justify-center overflow-hidden">
      <ParticleAnimation/>

      <div className="relative z-10 text-center px-6 max-w-4xl mx-auto">
        <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-6 text-balance">Petr Lavrov</h1>
        <p className="text-xl md:text-2xl text-muted-foreground mb-8 text-balance leading-relaxed">
          Beauty. Simplicity. Freedom.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="#explore"
            className="px-8 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
          >
            View My Work
          </Link>
          <a
            href="mailto:petrlavrov@calmmage.com"
            className="px-8 py-3 border border-border text-foreground rounded-lg font-medium hover:bg-secondary transition-colors"
          >
            Get In Touch
          </a>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-muted-foreground rounded-full flex justify-center">
          <div className="w-1 h-3 bg-muted-foreground rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  )
}
