'use client';

import {sections} from "@/lib/sections";
import Link from "next/link";
import {useEffect, useState} from "react";

export default function HomePage() {
    const [isMobile, setIsMobile] = useState(window && window.innerWidth <= 768);

    useEffect(() => {
        if (window && window.innerWidth <= 768) {
            setIsMobile(true);
        }
    }, []);

    return (
        <section style={{
            position: 'relative',
            height: '100%',
            width: '100%',
            maxWidth: '100%',
            paddingTop: isMobile ? '20px' : '64px',
            overflow: 'hidden'
        }}>
            <div
                className="space-y-8"
                style={{
                    maxWidth: '1024px',
                    margin: '0 auto',
                    padding: '0 20px',
                    position: 'relative',
                }}
            >
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

            <div
                style={{
                    position: 'relative',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    width: isMobile ? '180svw' : '100%',
                    transform: isMobile ? 'translateX(-50%)' : 'translateX(0)',
                    left: isMobile ? '50%' : '0',
                    top: isMobile ? '-10%' : '0',
                }}
                className={"h-[65%] lg:h-[70%]"}
            >
                <iframe
                    src="/particles/index.html"
                    title="Particles Animation"
                    scrolling="no"
                    style={{
                        width: isMobile ? '100%' : '180%',
                        height: '100%',
                        border: 'none'
                    }}
                />
            </div>
        </section>
    )
}
