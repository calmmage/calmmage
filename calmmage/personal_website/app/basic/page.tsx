'use client';

import Link from 'next/link';
import {Sidebar} from "@/ui/sidebar";
import {useEffect, useState} from "react";

export default function Page() {
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        if (window && window.innerWidth <= 768) {
            setIsMobile(true);
        }
    }, []);

    return (
        <div
            style={{
                height: '100svh',
                width: '100%',
                position: 'relative',
                display: 'flex',
                flexDirection: isMobile ? 'column' : 'row',
            }}
        >
            <Sidebar />

            <div style={{ padding: '20px 20px 0' }} className="prose prose-sm prose-invert max-w-none">
                <h1 className="text-xl font-bold">Welcome to Petr Lavrov&apos;s Website</h1>
                <p>This is Petr Lavrov&apos;s personal site. More content coming soon!</p>
                <ul>
                    <li><Link href="/basic/nginx">NGINX setup help Page</Link></li>
                    <li><Link href="/basic/help">General calmmage Help Page</Link></li>
                </ul>
            </div>
        </div>
    );
}
