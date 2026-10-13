export type SectionItem = {
  name: string;
  href: string;
  description?: string;
  external?: boolean;
};

export type Section = {
  name: string;
  items: SectionItem[];
};

export const sections: Section[] = [
  {
    name: "Explore",
    items: [
      {
        name: "About",
        href: "/about",
        description: "Journey, interests, and the people-first story.",
      },
      {
        name: "Projects",
        href: "/projects",
        description: "Where the code lives, and how to work with me.",
      },
      {
        name: "Art",
        href: "/art",
        description: "Particles, playfulness, and visual explorations.",
      },
      {
        name: "Blog",
        href: "/blog",
        description: "Writing, updates, and current curiosities.",
      },
    ],
  },
  {
    name: "Elsewhere",
    items: [
      {
        name: "Work with me",
        href: "https://petrlavrov.com",
        description: "Consulting on LLMs, automation and engineering. Book a call.",
        external: true,
      },
      {
        name: "Telegram — Лавров, который из Гугла",
        href: "https://t.me/petrlavrov",
        description: "AI tools I actually use, what I build with them, and life in between.",
        external: true,
      },
      {
        name: "GitHub — calmmage",
        href: "https://github.com/calmmage",
        description: "Code, bots and experiments.",
        external: true,
      },
      {
        name: "Constellations",
        href: "https://constellations.calmmage.com/",
        description: "Navigate an interactive night sky of personal projects.",
        external: true,
      },
      {
        name: "Instagram",
        href: "https://www.instagram.com/beware.life_is_awesome/",
        description: "Travel, photography, and moments from the trail.",
        external: true,
      },
    ],
  },
];
