import { sections } from '@/lib/sections';
import Image from "next/image";
import Link from 'next/link';


export default function Page() {
  return (
      <div>

        {/*<div className="space-y-8" style={{ zIndex: 10 }}>*/}
        <div className="space-y-8" style={{ maxWidth: '1024px', margin: '0 auto' }}>
          {/*<h1 className="text-xl font-medium text-gray-300">Examples</h1>*/}

          <div className="space-y-10 text-white">
            {sections.map((section) => {
              return (
                  <div key={section.name} className="space-y-5">
                    <div className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                      {section.name}
                    </div>

                    <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
                      {section.items.map((item) => {
                        return (
                            <Link
                                href={`/${item.slug}`}
                                key={item.name}
                                className="group block space-y-1.5 rounded-lg bg-gray-900 px-5 py-3 hover:bg-gray-800"
                            >
                              <div className="font-medium text-gray-200 group-hover:text-gray-50">
                                {item.name}
                              </div>

                              {item.description ? (
                                  <div className="line-clamp-3 text-sm text-gray-400 group-hover:text-gray-300">
                                    {item.description}
                                  </div>
                              ) : null}
                            </Link>
                        );
                      })}
                    </div>
                  </div>
              );
            })}
          </div>
        </div>
        <div className="flex z-1 min-h-screen flex-col items-center justify-between p-24">
          <div style={{padding: '20px'}}>
            {/*<div style={{position: 'absolute', top: "0%", left: "30%", zIndex: -1}}>*/}
              <iframe scrolling="no"
                      src="/particles/index.html"
                      // style={{width: '1000px', height: '1000px', border: 'none', opacity: '100%'}}
                  style={{width: '100%', height: '100%', border: 'none'}}
                      title="Particles Animation"
              ></iframe>
            {/*</div>*/}
          </div>
        </div>
      </div>
  );
}
