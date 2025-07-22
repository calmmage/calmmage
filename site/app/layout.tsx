import '@/styles/globals.css';
// import "./customized/globals.css";
import {Sidebar} from '@/ui/sidebar';
import {Metadata} from 'next';

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
            flexDirection: 'column',
            height: '100svh',
            backgroundImage: 'url(/grid.svg)'
          }}
          className="flex bg-gray-1100"
      >
        <Sidebar />

        <div
            style={{ position: 'relative', height: '100svh' }}
            className="flex-grow">
          <div style={{ position: 'relative', height: '100%' }} className="mx-auto max-w-full space-y-8 px-2 lg:px-8 lg:py-8">
            {children}
            {/*<Byline className="fixed sm:hidden"/>*/}
          </div>
        </div>
      </body>
      </html>
  );
}
