import { Outlet } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import Sidebar from "./Sidebar";
import MobileNav from "./MobileNav";

export default function AppShell() {
  return (
    <div className="min-h-screen flex">
      <div className="mesh-bg" />
      <Sidebar />
      <main className="flex-1 min-w-0 px-4 sm:px-6 lg:px-10 py-6 lg:py-10 pb-24 lg:pb-10 max-w-[1400px] mx-auto w-full">
        <AnimatePresence mode="wait">
          <Outlet />
        </AnimatePresence>
      </main>
      <MobileNav />
    </div>
  );
}
