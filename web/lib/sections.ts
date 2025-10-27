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
        name: "Home",
        href: "/",
        description: "Start here for highlights and quick navigation.",
      },
      {
        name: "About",
        href: "/about",
        description: "Journey, interests, and the people-first story.",
      },
      {
        name: "Projects",
        href: "/projects",
        description: "Interactive demos and engineering experiments.",
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
        name: "Constellations",
        href: "https://constellations.calmmage.com/",
        description: "Navigate an interactive night sky of personal projects.",
        external: true,
      },
      {
        name: "Substack",
        href: "https://petrlavrov.substack.com/",
        description: "Thoughts on tech, life, and meaningful connections.",
        external: true,
      },
      {
        name: "Telegram — Life",
        href: "https://t.me/petrlavrov",
        description: "Philosophy, travel, and daily reflections.",
        external: true,
      },
      {
        name: "Telegram — Dev",
        href: "https://t.me/calmmageDev",
        description: "Engineering notes, experiments, and behind-the-scenes.",
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
