"use client"

import Link from "next/link"
import {cn} from "@/lib/utils"
import {aboutHref, type Locale} from "@/lib/i18n"

export function LanguageToggle({
  locale,
  className,
}: {
  locale: Locale
  className?: string
}) {
  return (
    <div className={cn("flex items-center gap-1 font-mono text-xs tracking-wide", className)}>
      <Link
        href={aboutHref("en")}
        hrefLang="en"
        className={cn(
          "rounded px-1.5 py-0.5 transition-colors",
          locale === "en"
            ? "text-foreground"
            : "text-muted-foreground hover:text-primary",
        )}
      >
        EN
      </Link>
      <span className="text-muted-foreground/40">/</span>
      <Link
        href={aboutHref("ru")}
        hrefLang="ru"
        className={cn(
          "rounded px-1.5 py-0.5 transition-colors",
          locale === "ru"
            ? "text-foreground"
            : "text-muted-foreground hover:text-primary",
        )}
      >
        RU
      </Link>
    </div>
  )
}
