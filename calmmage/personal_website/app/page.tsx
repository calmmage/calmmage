'use client'

import { Sidebar } from "@/ui/sidebar";
import HomePage from "@/components/pages/homePage";
import { useEffect, useState } from "react";


export default function Page() {
  const [isMobile, setIsMobile] = useState(window && window.innerWidth <= 768);

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

          <HomePage />
      </div>
  );
}
