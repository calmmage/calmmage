// import "./customized/globals.css";

import '@/styles/globals.css';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'Calmmage Home',
    template: '%s | Calmmage Home',
  },
  description:
    'What did the cow say? "Moo!"',
  openGraph: {
    title: 'Calmmage Home Playground',
    description:
      'Hah! You got me!',
    images: [`/api/og?title=Calmmage Home`],
  },
  twitter: {
    card: 'summary_large_image',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <html lang="en">
      <body
          style={{
            height: '100svh',
            width: '100svw',
            backgroundImage: 'url(/grid.svg)',
            position: 'relative',
          }}
      >
        {children}
      </body>
      </html>
  );
}
