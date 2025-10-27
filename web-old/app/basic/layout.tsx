export default function BasicLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <section style={{position: 'relative', height: '100%'}}>
          <div
              className="space-y-8"
              style={{
                  maxWidth: '1024px',
                  margin: '0 auto',
                  padding: '0 20px',
                  position: 'relative',
              }}>
              {children}
          </div>
      </section>
  );
}
