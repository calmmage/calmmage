import Link from 'next/link';

export default function Page() {
    return (
        <div className="prose prose-sm prose-invert max-w-none">
            <h1 className="text-xl font-bold">Welcome to Petr Lavrov&apos;s Website</h1>
            <p>This is Petr Lavrov&apos;s personal site. More content coming soon!</p>
            <ul>
                <li><Link href="/basic/nginx">NGINX setup help Page</Link></li>
                <li><Link href="/basic/help">General calmmage Help Page</Link></li>
            </ul>
        </div>
    );
}
