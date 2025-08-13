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
                <div className="space-y-10 text-white">
                    {/* Personal Introduction */}
                    <div className="space-y-6 text-center">
                        <h1 className="text-4xl font-bold">Hi there! 👋</h1>
                        <p className="text-xl text-gray-300">
                            <strong>Петя Лавров</strong> • 30 • Zurich
                        </p>
                        <p className="text-lg text-gray-400 max-w-2xl mx-auto">
                            Engineer, experimenter, mentor, student. Looking for deep meaningful connections with people who have energy, wisdom, and drive.
                        </p>
                        
                        <div className="space-y-4">
                            <h2 className="text-2xl font-semibold">🛤️ Journey</h2>
                            <div className="space-y-2 text-gray-400">
                                <p>Magic Leap ← Google ← Luxoft ← Yandex ← WorldQuant ← МГУ</p>
                                <p>Zürich ← Moscow ← Perm</p>
                                <p>AR ← SWE ← Finance ← Mathematics ← Physics</p>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <h2 className="text-2xl font-semibold">🎨 Projects & Writing</h2>
                            <div className="space-y-2 text-gray-400">
                                <p><a href="https://constellations.calmmage.com/" className="text-blue-400 hover:text-blue-300">Constellations</a> - Interactive constellation visualizations</p>
                                <p><a href="https://petrlavrov.substack.com/" className="text-blue-400 hover:text-blue-300">Blog</a> - Thoughts on tech and life</p>
                                <p><a href="https://t.me/petrlavrov" className="text-blue-400 hover:text-blue-300">@petrlavrov</a> - Life and philosophy</p>
                                <p><a href="https://t.me/calmmageDev" className="text-blue-400 hover:text-blue-300">@calmmageDev</a> - About coding</p>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <h2 className="text-2xl font-semibold">🏔️ Life</h2>
                            <p className="text-gray-400">
                                📖 Reading • 📜 Poetry • 🛤️ Travel & photography • 🧘🏼 Vipassana • 🏔️ Mountaineering • 🏊 Swimming • ⚔️ Beat Saber • 🤹‍♀️ Juggling • 🤸‍♀️ Yoga23
                            </p>
                        </div>
                    </div>

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