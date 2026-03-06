function Header() {
  return (
    <header className="bg-primary text-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex flex-col items-center">
        
        {/* App Title */}
        <h1 className="text-xl font-bold mb-2">
          PromptLab
        </h1>

        {/* Logo Placeholder below title */}
        <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center text-primary font-bold">
          LOGO
        </div>

      </div>
    </header>
  );
}

export default Header;