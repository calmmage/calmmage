import type {LucideIcon} from "lucide-react"
import {
  BookOpen,
  Calendar,
  Camera,
  Feather,
  Flower2,
  Mountain,
  MountainSnow,
  Orbit,
  Palette,
  PersonStanding,
  Route,
  Swords,
  Waves,
} from "lucide-react"
import type {LifeIconKey} from "@/lib/i18n"

export const lifeIcons: Record<LifeIconKey, LucideIcon> = {
  reading: BookOpen,
  poetry: Feather,
  travel: Camera,
  vipassana: Flower2,
  mountaineering: MountainSnow,
  swimming: Waves,
  beatsaber: Swords,
  juggling: Orbit,
  yoga: PersonStanding,
}

export const sectionIcons = {
  journey: Route,
  projects: Palette,
  life: Mountain,
  bookChat: Calendar,
} as const
