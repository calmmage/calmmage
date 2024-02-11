'use client';
// Sidebar.tsx
import Link from 'next/link';
import { sections } from '@/lib/sections';
import { GlobalNavItem } from '@/ui/global-nav';
import { useState } from "react";
import classNames from "classnames";
import CMIcon from "@/components/Icon";

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const onClose = () => setIsOpen(!isOpen);

  return (
      <div
          style={{
              height: '100svh',
              width: '300px',
              // flex flex-col =>
              display: 'flex',
              flexDirection: 'column',
          }}
          className={classNames(
              "top-0 z-10 flex h-screen w-[300px] flex-col border-b border-gray-800 bg-black",
              "lg:bottom-0 lg:z-auto lg:w-72 lg:border-b-0 lg:border-r lg:border-gray-800",
          )}
      >
          <div
              onClick={onClose}
              style={{ padding: '20px', cursor: 'pointer' }}
              className="flex h-14 px-4 py-4 lg:h-auto cursor-pointer"
          >
              <div className="group flex w-full">
                  <h3 className="font-semibold tracking-wide text-gray-400 group-hover:text-gray-50">
                      Calmmage Home
                  </h3>
              </div>

              <CMIcon iconName={isOpen ? 'close' : 'burger'} />
          </div>

          <div
              style={{
                  height: 'calc(100svh - 56px)',
                  width: '300px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '40px',
                  padding: '20px',
                  // это мы делаем анимацию при клике
                  transform: isOpen ? 'translateX(0)' : 'translateX(-300px)',
                  // время анимации
                  transition: '0.8s'
              }}
              className="bg-gray-900 text-white overflow-auto"
          >
              {sections.map((section) => (
                  <div
                      key={section.name}
                      style={{
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '20px'
                      }}
                      className="p-4 flex flex-col"
                  >
                      <div className="font-bold uppercase mb-2">{section.name}</div>
                      {section.items.map((item) => (
                          <GlobalNavItem key={item.slug} item={item} onClose={onClose} />
                      ))}
                  </div>
              ))}
          </div>
      </div>
  );
};

// export default Sidebar;
