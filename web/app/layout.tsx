import type {Metadata} from "next"
import {headers} from "next/headers"
import {GeistSans} from "geist/font/sans"
import {GeistMono} from "geist/font/mono"
import {Analytics} from "@vercel/analytics/next"
import {copy} from "@/lib/i18n"
import {site} from "@/lib/site"
import "./globals.css"

const en = copy.en

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: en.ogTitle,
    template: `%s · ${en.ogTitle}`,
  },
  description: en.ogDescription,
  openGraph: {
    title: en.ogTitle,
    description: en.ogDescription,
    url: site.url,
    siteName: "Calmmage",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: en.ogTitle,
    description: en.ogDescription,
  },
  generator: "calmmage.com",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const locale = headers().get("x-locale") === "ru" ? "ru" : "en"

  return (
    <html lang={locale}>
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
