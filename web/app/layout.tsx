import type {Metadata} from 'next'
import {GeistSans} from 'geist/font/sans'
import {GeistMono} from 'geist/font/mono'
import {Analytics} from '@vercel/analytics/next'
import './globals.css'

export const metadata: Metadata = {
  title: {
    default: 'Calmmage',
    template: '%s | Calmmage',
  },
  description: 'What did the cow say? "Moo!"',
  openGraph: {
    title: 'Calmmage Playground',
    description: 'Hah! You got me!',
    images: ['/api/og?title=Calmmage'],
  },
  twitter: {
    card: 'summary_large_image',
  },
  generator: 'calmmage.com',
}

export default function RootLayout({
                                     children,
                                   }: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
    <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
    {children}
    <Analytics/>
    </body>
    </html>
  )
}
