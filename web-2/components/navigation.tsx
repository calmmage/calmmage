"use client"

import {useState} from "react"
import Link from "next/link"
import {cn} from "@/lib/utils"

const navItems = [
  {name: "Home", href: "/"},
  {name: "Blog", href: "/blog"},
  {name: "Projects", href: "/projects"},
  {name: "Art", href: "/art"},
  {name: "About Me", href: "/about"},
]

export function Navigation() {
  const [activeItem, setActiveItem] = useState("Home")

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-6xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-xl font-mono font-bold text-foreground hover:text-primary transition-colors">
            {"<dev />"}
          </Link>

          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                onClick={() => setActiveItem(item.name)}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-primary",
                  activeItem === item.name ? "text-primary" : "text-muted-foreground",
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <button className="md:hidden p-2 text-muted-foreground hover:text-primary transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>
      </div>
    </nav>
  )
}
