import type {Metadata} from "next"
import {copy, type Locale} from "@/lib/i18n"
import {site} from "@/lib/site"

export function aboutMetadata(locale: Locale): Metadata {
  const t = copy[locale]
  const url = locale === "ru" ? `${site.url}/ru/about` : `${site.url}/about`

  return {
    title: {
      absolute: t.ogTitle,
    },
    description: t.ogDescription,
    alternates: {
      canonical: url,
      languages: {
        en: `${site.url}/about`,
        ru: `${site.url}/ru/about`,
      },
    },
    openGraph: {
      title: t.ogTitle,
      description: t.ogDescription,
      url,
      siteName: "Calmmage",
      locale: locale === "ru" ? "ru_RU" : "en_US",
      type: "profile",
    },
    twitter: {
      card: "summary_large_image",
      title: t.ogTitle,
      description: t.ogDescription,
    },
  }
}
