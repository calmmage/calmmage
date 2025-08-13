import '@/styles/globals.css';
// import "./customized/globals.css";
import {Metadata} from 'next';
import {Sidebar} from '@/ui/sidebar';

export const metadata: Metadata = {
  title: {
    default: 'Calmmage',
    template: '%s | Calmmage',
  },
  description:
    'What did the cow say? "Moo!"',
  openGraph: {
    title: 'Calmmage Playground',
    description:
      'Hah! You got me!',
    images: [`/api/og?title=Calmmage`],
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
            backgroundImage: 'url(/grid.svg)'
          }}
          className="bg-gray-1100"
      >
        <div style={{
          height: '100svh',
          width: '100%',
          position: 'relative',
          display: 'flex',
        }}>
          <Sidebar />
          <div style={{
            flex: '1',
            height: '100%',
            overflow: 'auto'
          }}>
            {children}
          </div>
        </div>
      </body>
      </html>
  );
}
