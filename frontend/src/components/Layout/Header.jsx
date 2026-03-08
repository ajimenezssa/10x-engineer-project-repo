function Header() {
  return (
    <header className="bg-primary text-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-center space-x-1">
        {/* App Title */}
        <h1 className="text-xl font-bold">PromptLab</h1>

        {/* Logo */}
        <img
          src="/logo.svg"
          alt="PromptLab Logo"
          className="h-10 w-10 rounded-full align-middle"
        />
      </div>
    </header>
  );
}

export default Header;