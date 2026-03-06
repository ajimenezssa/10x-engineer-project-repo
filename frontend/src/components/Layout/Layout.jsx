import Header from "./Header";

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-light">
      <Header />

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* Main Content */}
        <div>
          {children}
        </div>

      </main>
    </div>
  );
}

export default Layout;