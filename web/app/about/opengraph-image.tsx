import {renderOgImage} from "@/lib/og-image"

export const runtime = "edge"
export const alt = "Petr Lavrov"
export const size = {width: 1200, height: 630}
export const contentType = "image/png"

export default function AboutOpenGraphImage() {
  return renderOgImage("en")
}
