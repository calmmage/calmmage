"use client"

import Link from "next/link"
import {usePathname} from "next/navigation"
import {LanguageToggle} from "@/components/language-toggle"
import {copy, localeFromPath, localizedHref, navItems, type Locale} from "@/lib/i18n"
import {cn} from "@/lib/utils"

export function Navigation({locale}: {locale?: Locale}) {
  const pathname = usePathname()
  const resolvedLocale = locale ?? localeFromPath(pathname)
  const labels = copy[resolvedLocale].nav

  const isActive = (href: string) => {
    if (href === "/") {
      return pathname === "/" || pathname === "/ru"
    }
    if (href === "/about") {
      return pathname === "/about" || pathname === "/ru/about"
    }
    return pathname.startsWith(href)
  }

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
                key={item.key}
                href={localizedHref(item.href, resolvedLocale)}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-primary",
                  isActive(item.href) ? "text-primary" : "text-muted-foreground",
                )}
              >
                {labels[item.key]}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <LanguageToggle locale={resolvedLocale} />
            <button
              type="button"
              className="md:hidden p-2 text-muted-foreground hover:text-primary transition-colors"
              aria-label="Menu"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
