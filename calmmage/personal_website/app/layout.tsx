import '@/styles/globals.css';
// import "./customized/globals.css";
import { AddressBar } from '@/ui/address-bar';
import Byline from '@/ui/byline';
import { GlobalNav } from '@/ui/global-nav';
import { Sidebar } from '@/ui/sidebar';
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
// export default function RootLayout({
//   children,
// }: {
//   children: React.ReactNode;
// }) {
  return (
    <html lang="en">
      <body>
        {/*<GlobalNav />*/}
        <Sidebar />
        {/*{children}*/}
        <div className="flex justify-center pt-[150px]">
          <div className="mx-auto max-w-4xl space-y-8 px-2 pt-20 lg:px-8 lg:py-8">

            {/*<div className="bg-vc-border-gradient rounded-lg p-px shadow-lg shadow-black/20">*/}
            {/*  <div className="rounded-lg bg-black">*/}
            {/*    <AddressBar />*/}
            {/*  </div>*/}
            {/*</div>*/}

            {children}
        {/*    <div className="bg-vc-border-gradient rounded-lg p-px shadow-lg shadow-black/20">*/}
        {/*      <div className="rounded-lg bg-black p-3.5 lg:p-6">{children}</div>*/}
        {/*    </div>*/}
            <Byline className="fixed sm:hidden" />
          </div>
        </div>
      </body>
    </html>
  );
}
