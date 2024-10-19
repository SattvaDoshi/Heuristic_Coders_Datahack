import { Link } from "react-router-dom"
import { HashLink } from "react-router-hash-link"

const Footer = () => {
  return (
    <div className="h-24 max-w-7xl m-auto flex justify-between text-gray-200">
      <div className="flex items-center">
        <img src="public\shield.png" width={32} alt="Logo" />
        <h2 className="font-bold text-2xl">SheildAI</h2>
      </div>
      <div className="flex flex-col justify-center">
        <div className="flex justify-end">&copy; by Heuristic Coders</div>
        <div className="flex gap-4 items-center">
          <Link to="/">Home</Link>
          <HashLink to="/#feature">Features</HashLink>
          <Link to="/assesment">Upload</Link>
        </div>
      </div>
    </div>
  )
}

export default Footer