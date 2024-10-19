import { Link } from "react-router-dom"
import { HashLink } from 'react-router-hash-link';

const Navbar = () => {
  return (
    <div className="h-24 max-w-7xl m-auto flex items-center justify-between text-gray-200">
      <div className="flex items-center">
        <img src="public\shield.png" width={32} alt="Logo" />
        <h2 className="font-bold text-2xl">SheildAI</h2>
      </div>
      <div className="flex gap-9">
        <div className="flex gap-8 text-xl items-center">
          <Link to="/">Home</Link>
          <HashLink to="/#feature">Features</HashLink>
          <Link to="/assesment">Upload</Link>
        </div>
        <button className="font-semibold text-xl border border-purple-300 rounded-md px-2 py-1">Sign In</button>
      </div>
    </div>
  )
}

export default Navbar