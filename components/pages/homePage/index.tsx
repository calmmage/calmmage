'use client';

import {sections} from "@/lib/sections";
import Link from "next/link";
import {useEffect, useState} from "react";

export default function HomePage() {
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        if (typeof window !== 'undefined' && window.innerWidth <= 768) {
            setIsMobile(true);
        }
    }, []);

    return (
        <section style={{
            position: 'relative',
            width: '100%',
            maxWidth: '100%',
            padding: '20px',
            minHeight: '100vh'
        }}>
            {/* Three.js Demo - Prominent Position */}
            <div
                style={{
                    position: 'relative',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    width: '100%',
                    height: isMobile ? '50vh' : '60vh',
                    marginBottom: '2rem'
                }}
            >
                <iframe
                    src="/particles/index.html"
                    title="Interactive Particles Animation - Three.js Demo"
                    scrolling="no"
                    style={{
                        width: isMobile ? '100%' : '100%',
                        height: '100%',
                        border: 'none'
                    }}
                />
            </div>

            {/* Navigation Sections */}
            <div
                className="space-y-8"
                style={{
                    maxWidth: '1024px',
                    margin: '0 auto',
                    padding: '0 20px',
                    position: 'relative',
                }}
            >
                <div className="space-y-10 text-white">
                    {
                        sections.map((section) => (
                            <div key={section.name} className="space-y-5">
                                <div className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                                    {section.name}
                                </div>

                                <div
                                    style={{
                                        display: 'flex',
                                        flexWrap: 'wrap',
                                        gap: '24px',
                                        width: '100%',
                                    }}
                                >
                                    {
                                        section.items.map(({ name, description, slug }) => (
                                            <Link
                                                href={`/${slug}`}
                                                key={name}
                                                style={{
                                                    width: isMobile ? '100%' : 'calc(50% - 12px)'
                                                }}
                                                className="group block space-y-1.5 rounded-lg bg-gray-900 px-5 py-3 hover:bg-gray-800"
                                            >
                                                <div className="font-medium text-gray-200 group-hover:text-gray-50">
                                                    {name}
                                                </div>

                                                {
                                                    description ? (
                                                        <div className="line-clamp-3 text-sm text-gray-400 group-hover:text-gray-300">
                                                            {description}
                                                        </div>
                                                    ) : null
                                                }
                                            </Link>
                                        ))
                                    }
                                </div>
                            </div>
                        ))
                    }
                </div>
            </div>
        </section>
    )
}