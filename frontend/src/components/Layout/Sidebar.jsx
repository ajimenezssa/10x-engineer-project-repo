function Sidebar() {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold text-dark mb-3">
        Collections
      </h2>
      <ul className="space-y-2 text-sm">
        <li>
          <a href="#" className="text-dark hover:text-accent">
            All Prompts
          </a>
        </li>
        <li>
          <a href="#" className="text-dark hover:text-accent">
            Writing
          </a>
        </li>
        <li>
          <a href="#" className="text-dark hover:text-accent">
            Coding
          </a>
        </li>
      </ul>
    </div>
  );
}
export default Sidebar;