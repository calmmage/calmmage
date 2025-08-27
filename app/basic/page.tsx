import Link from 'next/link';

export default function Page() {
    return (
        <div className="space-y-8 text-white max-w-4xl mx-auto p-6">
            {/* Personal Introduction */}
            <div className="space-y-6 text-center">
                <h1 className="text-4xl font-bold">Hi there! 👋</h1>
                <p className="text-xl text-gray-300">
                    <strong>Петя Лавров</strong> • 32 • Zurich
                </p>
                <p className="text-lg text-gray-400 max-w-2xl mx-auto">
                    Husband, Father, Son, Brother, Friend
                    Engineer, Experimenter, Mentor, Student.
                    Looking for deep meaningful connections
                    with people who have energy, wisdom, and drive.
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
                        <p><a href="https://t.me/petrlavrov" className="text-blue-400 hover:text-blue-300">t.me/petrlavrov</a> - Life and philosophy</p>
                        <p><a href="https://t.me/calmmageDev" className="text-blue-400 hover:text-blue-300">t.me/calmmageDev</a> - About coding</p>
                    </div>
                </div>

                <div className="space-y-4">
                    <h2 className="text-2xl font-semibold">🏔️ Life</h2>
                    <p className="text-gray-400">
                        📖 Reading • 📜 Poetry • 🛤️ Travel & photography • 🧘🏼 Vipassana • 🏔️ Mountaineering • 🏊 Swimming • ⚔️ Beat Saber • 🤹‍♀️ Juggling • 🤸‍♀️ Yoga23
                    </p>
                </div>
            </div>

            {/* Navigation Links */}
            <div className="space-y-4 text-center">
                <h2 className="text-2xl font-semibold">Additional Pages</h2>
                <div className="space-y-2">
                    <div><Link href="/basic/nginx" className="text-blue-400 hover:text-blue-300">NGINX setup help Page</Link></div>
                    <div><Link href="/basic/help" className="text-blue-400 hover:text-blue-300">General calmmage Help Page</Link></div>
                </div>
            </div>
        </div>
    );
}
