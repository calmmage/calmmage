export type Item = {
  name: string;
  slug: string;
  description?: string;
};

export const sections: { name: string; items: Item[] }[] = [
  {
    name: 'Sections',
    items: [
      {
        name: 'Profile',
        slug: 'basic',
        description: 'About me',
      },
      {
        name: 'Knowledge Base',
        slug: 'calmmage_knowledge_base/getting-started',
        description: 'Separate knowledge base using Foam notes',
      },
      {
        name: 'Showcase',
        slug: 'showcase',
        description: 'Showcase some of my personal projects',
      },
    ],
  },
];
