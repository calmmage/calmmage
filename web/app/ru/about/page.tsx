import type {Metadata} from "next"
import {AboutView} from "@/components/about-view"
import {aboutMetadata} from "@/lib/metadata"

export const metadata: Metadata = aboutMetadata("ru")

export default function AboutRuPage() {
  return <AboutView locale="ru" />
}
