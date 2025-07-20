export type Item = {
    name: string;
    slug: string;
    description?: string;
    subsections?: Item[];
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
                subsections: [
                    {
                        name: 'Demo 1 - Slow Circle',
                        slug: 'demo1-slow-circle',
                        description: '3js animation of a slow moving circle',
                    },
                    {
                        name: 'Demo 2 - Fast Circle',
                        slug: 'demo2-fast-circle',
                        description: '3js animation of a fast moving circle'
                    },
                    {
                        name: 'Demo 3 - Lemniscate',
                        slug: 'demo3-lemniscate',
                        description: '3js animation of a lemniscate'
                    },
                    {
                        name: 'Demo 4 - Tube',
                        slug: 'demo4-tube',
                        description: '3js animation of a tube'
                    },
                    {
                        name: 'Demo 5 - Square',
                        slug: 'demo5-square',
                        description: '3js animation of a square'
                    },
                    {
                        name: 'Demo 6 - Heart',
                        slug: 'demo6-heart',
                        description: '3js animation of a heart'
                    },
                    {
                        name: 'Demo 7 - Beating Heart',
                        slug: 'demo7-beating-heart',
                        description: '3js animation of a beating heart'
                    },

                ],
            },
        ],
    },
];
