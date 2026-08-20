export const locales = ["en", "ru"] as const
export type Locale = (typeof locales)[number]

export type NavKey = "home" | "blog" | "projects" | "art" | "about"

export type LifeIconKey =
  | "reading"
  | "poetry"
  | "travel"
  | "vipassana"
  | "mountaineering"
  | "swimming"
  | "beatsaber"
  | "juggling"
  | "yoga"

export const navItems: {key: NavKey; href: string}[] = [
  {key: "home", href: "/"},
  {key: "blog", href: "/blog"},
  {key: "projects", href: "/projects"},
  {key: "art", href: "/art"},
  {key: "about", href: "/about"},
]

type LifeItem = {
  icon: LifeIconKey
  label: string
  href?: string
}

type Copy = {
  name: string
  identity: string
  bio: string[]
  bookChat: string
  journeyTitle: string
  companies: string
  cities: string
  fields: string
  projectsTitle: string
  projects: {label: string; href: string; blurb: string}[]
  lifeTitle: string
  life: LifeItem[]
  nav: Record<NavKey, string>
  ogTitle: string
  ogDescription: string
}

export const copy: Record<Locale, Copy> = {
  en: {
    name: "Petr Lavrov",
    identity: "33 · Zurich · Superlinear",
    bio: [
      "Husband, Father, Son, Brother, Friend.",
      "Engineer, Experimenter, Mentor, Student.",
      "Looking for deep meaningful connections",
      "with people who have energy, wisdom, and drive.",
    ],
    bookChat: "Book a chat",
    journeyTitle: "Journey",
    companies: "Superlinear (BlankFactor) ← Magic Leap ← Google ← Luxoft ← Yandex ← WorldQuant ← МГУ",
    cities: "Zurich ← Moscow ← Perm",
    fields: "LLMs ← AR ← SWE ← Finance ← Mathematics ← Physics",
    projectsTitle: "Projects & Writing",
    projects: [
      {
        label: "Constellations",
        href: "https://constellations.calmmage.com/",
        blurb: "Interactive constellation visualizations",
      },
      {
        label: "Blog",
        href: "https://petrlavrov.substack.com/",
        blurb: "Thoughts on tech and life",
      },
      {
        label: "t.me/petrlavrov",
        href: "https://t.me/petrlavrov",
        blurb: "Life and philosophy",
      },
      {
        label: "t.me/calmmageDev",
        href: "https://t.me/calmmageDev",
        blurb: "About coding",
      },
    ],
    lifeTitle: "Life",
    life: [
      {icon: "reading", label: "Reading"},
      {icon: "poetry", label: "Poetry"},
      {
        icon: "travel",
        label: "Travel & photography",
        href: "https://www.instagram.com/beware.life_is_awesome/",
      },
      {
        icon: "vipassana",
        label: "Vipassana",
        href: "https://internationalmeditationcentre.org/",
      },
      {icon: "mountaineering", label: "Mountaineering"},
      {icon: "swimming", label: "Swimming"},
      {
        icon: "beatsaber",
        label: "Beat Saber",
        href: "https://youtu.be/Rl65iVOV12U",
      },
      {icon: "juggling", label: "Juggling"},
      {icon: "yoga", label: "Yoga23"},
    ],
    nav: {
      home: "Home",
      blog: "Blog",
      projects: "Projects",
      art: "Art",
      about: "About",
    },
    ogTitle: "Petr Lavrov",
    ogDescription: "Engineer in Zurich · Superlinear. Curious? Book a chat.",
  },
  ru: {
    name: "Петр Лавров",
    identity: "33 · Цюрих · Superlinear",
    bio: [
      "Муж, отец, сын, брат, друг.",
      "Инженер, экспериментатор, наставник, студент.",
      "Ищу глубокие осмысленные связи",
      "с людьми, у которых есть энергия, мудрость и драйв.",
    ],
    bookChat: "Записаться на разговор",
    journeyTitle: "Путь",
    companies: "Superlinear (BlankFactor) ← Magic Leap ← Google ← Luxoft ← Yandex ← WorldQuant ← МГУ",
    cities: "Цюрих ← Москва ← Пермь",
    fields: "LLMs ← AR ← SWE ← Finance ← Mathematics ← Physics",
    projectsTitle: "Проекты и тексты",
    projects: [
      {
        label: "Constellations",
        href: "https://constellations.calmmage.com/",
        blurb: "Интерактивные визуализации созвездий",
      },
      {
        label: "Blog",
        href: "https://petrlavrov.substack.com/",
        blurb: "Мысли о технологиях и жизни",
      },
      {
        label: "t.me/petrlavrov",
        href: "https://t.me/petrlavrov",
        blurb: "Жизнь и философия",
      },
      {
        label: "t.me/calmmageDev",
        href: "https://t.me/calmmageDev",
        blurb: "Про код",
      },
    ],
    lifeTitle: "Жизнь",
    life: [
      {icon: "reading", label: "Чтение"},
      {icon: "poetry", label: "Поэзия"},
      {
        icon: "travel",
        label: "Путешествия и фотография",
        href: "https://www.instagram.com/beware.life_is_awesome/",
      },
      {
        icon: "vipassana",
        label: "Випассана",
        href: "https://internationalmeditationcentre.org/",
      },
      {icon: "mountaineering", label: "Альпинизм"},
      {icon: "swimming", label: "Плавание"},
      {
        icon: "beatsaber",
        label: "Beat Saber",
        href: "https://youtu.be/Rl65iVOV12U",
      },
      {icon: "juggling", label: "Жонглирование"},
      {icon: "yoga", label: "Yoga23"},
    ],
    nav: {
      home: "Главная",
      blog: "Блог",
      projects: "Проекты",
      art: "Арт",
      about: "Обо мне",
    },
    ogTitle: "Петр Лавров",
    ogDescription: "Инженер в Цюрихе · Superlinear. Записаться на разговор.",
  },
}

export function localeFromPath(pathname: string | null | undefined): Locale {
  return pathname?.startsWith("/ru") ? "ru" : "en"
}

export function localizedHref(href: string, locale: Locale): string {
  if (href === "/about") {
    return locale === "ru" ? "/ru/about" : "/about"
  }
  return href
}

export function aboutHref(locale: Locale): string {
  return locale === "ru" ? "/ru/about" : "/about"
}
