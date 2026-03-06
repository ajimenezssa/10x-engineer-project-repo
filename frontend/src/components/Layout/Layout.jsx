import Header from "./Header";
import Sidebar from "./Sidebar";

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-light">
      <Header />

      <main className="max-w-6xl mx-auto px-6 py-8">
        
        {/* Collections Section */}
        <div className="mb-8">
          <Sidebar />
        </div>

        {/* Main Content */}
        <div>
          {children}
        </div>

      </main>
    </div>
  );
}

export default Layout;