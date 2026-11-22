export const metadata = {
  title: 'LearnCraft AI - Personalized Study Assistant',
  description: 'AI-powered study assistant generating tailored curriculum modules and quizzes aligned with UN-SDG Goal 4.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
      </head>
      <body className="bg-slate-900 text-slate-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}
