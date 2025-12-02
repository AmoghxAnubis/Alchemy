import { Share_Tech_Mono } from "next/font/google";
import "./globals.css";

const techMono = Share_Tech_Mono({ 
  weight: "400",
  subsets: ["latin"],
  variable: "--font-tech",
});

export const metadata = {
  title: "ALCHEMIST // SYSTEM",
  description: "Digital Transmutation Engine",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={techMono.className}>{children}</body>
    </html>
  );
}