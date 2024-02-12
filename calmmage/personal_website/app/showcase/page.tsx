'use client'

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

            <div className="prose prose-sm prose-invert max-w-none">
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center'
                }}>
                    <h1 className="text-xl font-bold">Petr Lavrov Projects Showcase</h1>
                </div>
                <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                    <div className="w-full" style={{border: '2px dotted #101', padding: '10px'}}>
                        <iframe scrolling="no"
                                src="/showcase/demo1/index.html"
                                style={{width: '100%', height: '600px', border: 'none'}}
                                title="Demo 1"
                        ></iframe>
                    </div>
                    <div className="w-full" style={{border: '2px dotted #011', padding: '10px'}}>
                        <iframe scrolling="no"
                                src="/showcase/demo2/index.html"
                                style={{width: '100%', height: '600px', border: 'none'}}
                                title="Demo 2"
                        ></iframe>
                    </div>
                    <div className="w-full" style={{border: '2px dotted #101', padding: '10px'}}>
                        <iframe scrolling="no"
                                src="/showcase/demo3/index.html"
                                style={{width: '100%', height: '600px', border: 'none'}}
                                title="Demo 3"
                        ></iframe>
                    </div>
                    <div className="w-full" style={{border: '2px dotted #001', padding: '10px'}}>
                        <iframe scrolling="no"
                                src="/showcase/demo4/index.html"
                                style={{width: '100%', height: '600px', border: 'none'}}
                                title="Demo 4"
                        ></iframe>
                    </div>
                </div>
            </div>
        </div>
    );
}
