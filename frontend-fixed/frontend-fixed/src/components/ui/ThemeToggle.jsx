import { Sun, Moon } from "lucide-react";
import { useTheme } from "../../context/ThemeContext";

export default function ThemeToggle({ className = "" }) {
  const { theme, toggle } = useTheme();
  const isDark = theme === "dark";

  return (
    <button
      onClick={toggle}
      aria-label="Toggle color theme"
      className={`relative w-14 h-8 rounded-full glass flex items-center px-1 transition-colors duration-300 ${className}`}
    >
      <span
        className={`absolute top-1 left-1 w-6 h-6 rounded-full bg-gradient-to-br from-accentblue to-accentgreen shadow-glass-sm flex items-center justify-center transition-transform duration-300 ease-out ${
          isDark ? "translate-x-6" : "translate-x-0"
        }`}
      >
        {isDark ? <Moon className="w-3.5 h-3.5 text-white" /> : <Sun className="w-3.5 h-3.5 text-white" />}
      </span>
    </button>
  );
}
