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
        name: 'Home',
        slug: '',
        description: 'Main page of the website',
      },
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
        // demo1-slow-circle
        // demo2-fast-circle
        // demo3-lemniscate
        // demo4-tube
        // demo5-square
        // demo6-heart
        // demo7-beating-heart
        subsections: [ // Add this array for the subsections
          {
            name: 'Subsection 1',
            slug: 'subsection-1',
            description: 'Description for Subsection 1',
          },
          {
            name: 'Subsection 2',
            slug: 'subsection-2',
            description: 'Description for Subsection 2',
          },
          // Add more subsections as needed
        ],
      },
    ],
  },
];
