import {ImageResponse} from "next/og"
import {copy, type Locale} from "@/lib/i18n"

export const ogImageSize = {width: 1200, height: 630}

export function renderOgImage(locale: Locale) {
  const t = copy[locale]
  const subtitle = t.identity
  const cta = `${t.bookChat} →`

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: "80px",
          background: "#0c1016",
          color: "#f2f5f8",
        }}
      >
        <div
          style={{
            display: "flex",
            fontSize: 22,
            letterSpacing: "0.28em",
            textTransform: "uppercase",
            color: "#5ad0d4",
          }}
        >
          Calmmage
        </div>
        <div
          style={{
            display: "flex",
            marginTop: 28,
            fontSize: 72,
            fontWeight: 700,
            letterSpacing: "-0.04em",
          }}
        >
          {t.name}
        </div>
        <div
          style={{
            display: "flex",
            marginTop: 16,
            fontSize: 32,
            color: "#9aa3ad",
          }}
        >
          {subtitle}
        </div>
        <div
          style={{
            display: "flex",
            marginTop: 48,
            fontSize: 28,
            color: "#5ad0d4",
          }}
        >
          {cta}
        </div>
      </div>
    ),
    ogImageSize,
  )
}
