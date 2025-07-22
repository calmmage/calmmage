import {sections} from '@/lib/sections';
import Link from 'next/link';
import classNames from "classnames";


export default function Page() {
  return (
      <section style={{ position: 'relative', height: '100%' }}>
        <div
          className="space-y-8"
          style={{
            maxWidth: '1024px',
            margin: '0 auto',
            padding: '0 20px',
            position: 'relative',
        }}>
          <div className="space-y-10 text-white">
            {
                sections.map((section) => (
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
                ))
            }
          </div>
        </div>

        <div
            style={{ position: 'relative' }}
            className={classNames(
                "flex z-1 h-[55%] flex-col items-center justify-between",
                "lg:h-[70%]"
            )}>
          <div style={{ padding: '20px', height: '100%', position: 'relative' }}>
              <iframe scrolling="no"
                      src="/particles/index.html"
                  style={{
                      width: '180svw',
                      height: '100%',
                      border: 'none'
                  }}
                      title="Particles Animation"
              />
          </div>
        </div>
      </section>
  );
}
