function Header() {
  return (
    <header className="bg-primary text-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        
        {/* App Title */}
        <h1 className="text-xl font-bold">
          PromptLab
        </h1>

        {/* Navigation */}
        <nav className="flex items-center text-sm font-medium">
          
          <a href="#" className="hover:text-accent transition">
            Collections
          </a>

          <span> | </span>

          <a href="#" className="hover:text-accent transition">
            Prompts
          </a>

          <span> | </span>

          <a href="#" className="hover:text-accent transition">
            Dashboard
          </a>

        </nav>

      </div>
    </header>
  );
}

export default Header;