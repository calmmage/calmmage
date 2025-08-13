'use client';
// Sidebar.tsx
import { sections } from '@/lib/sections';
import { GlobalNavItem } from '@/ui/global-nav';
import { useEffect, useState } from "react";
import classNames from "classnames";
import CMIcon from "@/components/Icon";

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const onClose = () => setIsOpen(!isOpen);

  useEffect(() => {
      if (typeof window !== 'undefined' && window.innerWidth <= 768) {
          setIsOpen(false);
          setIsMobile(true);
      }
  }, []);

  function getSidebarWidthHeader() {
      if (typeof window !== 'undefined' && window.innerWidth <= 768) {
          return '100%';
      } else if (isOpen) {
          return '300px';
      }

      return '80px';
  }

  function getSidebarWidthContent() {
    if (isOpen) {
        if (typeof window !== 'undefined' && window.innerWidth <= 768) {
            return '100%';
        }

        return '300px';
    } else if (typeof window !== 'undefined' && window.innerWidth <= 768) {
        return '0px';
    }

    return '80px';
  }

  return (
      <section
          style={{
              height: isMobile ? '64px' : '100svh',
              width: getSidebarWidthHeader(),
              minWidth: getSidebarWidthHeader(),
              display: 'flex',
              flexDirection: 'column',
              background: 'black',
              transition: '0.4s',
          }}
      >
          <div
              onClick={onClose}
              style={{
                  display: 'flex',
                  padding: '16px',
                  width: getSidebarWidthHeader(),
                  cursor: 'pointer',
                  justifyContent: 'space-between',
                  gap: '8px',
                  transition: '0.4s',
              }}
          >
              <h3 className="font-semibold tracking-wide text-gray-400 group-hover:text-gray-50">
                  {
                      (isOpen || isMobile) ? 'Calmmage Home' : 'CH'
                  }
              </h3>

              <CMIcon iconName={isOpen ? 'close' : 'burger'} />
          </div>

          <div
              style={{
                  height: 'calc(100svh - 56px)',
                  width: getSidebarWidthContent(),
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '40px',
                  transition: '0.4s',
                  boxShadow: '5px 6px 10px rgba(255, 255, 255, 0.2)',
                  position: isMobile ? 'fixed' : 'relative',
                  top: isMobile ? '64px' : '0',
                  zIndex: '100'
              }}
              className="bg-gray-900 text-white overflow-auto"
          >
              {
                  sections.map((section) => (
                      <div
                          key={section.name}
                          style={{
                              display: 'flex',
                              flexDirection: 'column',
                              justifyContent: 'center',
                              gap: '20px',
                              padding: '12px'
                          }}
                      >
                          <div className={classNames("font-bold p-[8px] uppercase", {
                              ['mx-auto']: !isOpen
                          })}>
                              {
                                  isOpen ? section.name : 'S'
                              }
                          </div>

                          {
                              section.items.map((item) => (
                                  <GlobalNavItem
                                      key={item.slug}
                                      item={item}
                                      onClose={onClose}
                                      isMenuOpen={isOpen}
                                      iconName={item.iconName}
                                  />
                              ))
                          }
                      </div>
                  ))
              }
          </div>
      </section>
  );
};
