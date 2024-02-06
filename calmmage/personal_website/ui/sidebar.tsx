'use client';
// Sidebar.tsx
import Link from 'next/link';
import { MenuAlt2Icon, XIcon } from '@heroicons/react/solid';
import { sections, type Item } from '@/lib/sections';
import { GlobalNavItem } from '@/ui/global-nav';
import { useState } from "react";

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const close = () => setIsOpen(false);
  return (
      <div
          className="fixed top-0 z-10 flex w-full flex-col border-b border-gray-800 bg-black lg:bottom-0 lg:z-auto lg:w-72 lg:border-b-0 lg:border-r lg:border-gray-800">

          <div className="flex h-14 items-center px-4 py-4 lg:h-auto">
              <Link
                  href="/"
                  className="group flex w-full items-center gap-x-2.5"
                  onClick={close}
              >
                  {/*<div className="h-7 w-7 rounded-full border border-white/30 group-hover:border-white/50">*/}
                  {/*    /!*<NextLogo />*!/*/}
                  {/*    <h1> NextLogo should have been here</h1>*/}
                  {/*</div>*/}

                  <h3 className="font-semibold tracking-wide text-gray-400 group-hover:text-gray-50">
                      Calmmage Home
                  </h3>
              </Link>
          </div>
          <div
              className="group flex items-center gap-x-2.5 top-0 left-0 h-full bg-gray-900 text-white w-64 overflow-auto">
              {sections.map((section) => (
                  <div key={section.name} className="p-4">
                      <div className="font-bold uppercase mb-2">{section.name}</div>
                      {section.items.map((item) => (
                          <GlobalNavItem key={item.slug} item={item} close={close}/>
                      ))}
                  </div>
              ))}
          </div>
      </div>
  );
};

// export default Sidebar;