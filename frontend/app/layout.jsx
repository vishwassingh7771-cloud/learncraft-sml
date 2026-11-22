import { Atkinson_Hyperlegible, Plus_Jakarta_Sans } from 'next/font/google';
import './globals.css';

const body = Atkinson_Hyperlegible({ subsets: ['latin'], weight: ['400', '700'], variable: '--font-body' });
const display = Plus_Jakarta_Sans({ subsets: ['latin'], weight: ['600', '700', '800'], variable: '--font-display' });

export const metadata = {
  title: 'LearnCraft AI',
  description: 'Learn any topic at your reading level, then test yourself.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${body.variable} ${display.variable}`}>
      <body className="bg-slate-50 text-slate-800 min-h-screen font-sans">{children}</body>
    </html>
  );
}
