import type { CMIcons } from "@/components/Icon";

export type Item = {
  name: string;
  slug: string;
  description?: string;
  iconName: keyof typeof CMIcons;
};

export const sections: { name: string; items: Item[] }[] = [
    {
        name: 'Sections',
        items: [
      {
        name: 'Home',
        slug: '',
        description: 'Main page of the website',
        iconName: 'home'
      },
      {
        name: 'Profile',
        slug: 'basic',
        description: 'About me',
        iconName: 'profile'
      },
      // {
      //   name: 'Knowledge',
      //   slug: 'calmmage_knowledge_base/getting-started',
      //   description: 'Separate knowledge base using Obsidian notes',
      //   iconName: 'knowledge'
      // },
      {
        name: 'Showcase',
        slug: 'showcase',
        description: 'Showcase some of my personal projects',
        iconName: 'showCase'
      },
        ],
    },
];
