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
            minHeight: '100svh',
            backgroundImage: 'url(/grid.svg)'
          }}
          className="bg-gray-1100"
      >
        <div className="min-h-screen w-full relative flex flex-col md:flex-row">
          <Sidebar />
          <main className="flex-1 w-full overflow-auto pt-16 md:pt-0">
            <div className="h-full w-full p-4">
              {children}
            </div>
          </main>
        </div>
      </body>
      </html>
  );
}
