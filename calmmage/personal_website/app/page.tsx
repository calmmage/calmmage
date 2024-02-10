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
            <div style={{position: 'absolute', top: "0%", left: "30%", zIndex: -1}}>
              <iframe scrolling="no"
                      src="/particles/index.html"
                      style={{width: '1000px', height: '1000px', border: 'none', opacity: '100%'}}
                  // style={{width: '100%', height: '500px', border: 'none'}}
                      title="Particles Animation"
              ></iframe>
            </div>
          </div>
          <div
              className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
            <a
                href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
                className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                // className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                target="_blank"
                rel="noopener noreferrer"
            >
              <h2 className={`mb-3 text-2xl font-semibold`}>
                Docs{" "}
                <span
                    className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
              </h2>
              <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                Find in-depth information about Next.js features and API.
              </p>
            </a>

            <a
                href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
                className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                target="_blank"
                rel="noopener noreferrer"
            >
              <h2 className={`mb-3 text-2xl font-semibold`}>
                Learn{" "}
                <span
                    className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
              </h2>
              <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                Learn about Next.js in an interactive course with&nbsp;quizzes!
              </p>
            </a>

            <a
                href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
                className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                target="_blank"
                rel="noopener noreferrer"
            >
              <h2 className={`mb-3 text-2xl font-semibold`}>
                Templates{" "}
                <span
                    className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
              </h2>
              <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                Explore starter templates for Next.js.
              </p>
            </a>

            <a
                href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
                className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                target="_blank"
                rel="noopener noreferrer"
            >
              <h2 className={`mb-3 text-2xl font-semibold`}>
                Deploy{" "}
                <span
                    className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
              </h2>
              <p className={`m-0 max-w-[30ch] text-sm opacity-50 text-balance`}>
                Instantly deploy your Next.js site to a shareable URL with Vercel.
              </p>
            </a>
          </div>
        </div>
      </div>
  );
}
