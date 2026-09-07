import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "VihokAI Global Library",
  description: "Global Library Gateway V1 - search books, research & media worldwide",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
