import Footer from "./components/Footer"
import Navbar from "./components/Navbar"
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/Homepage";
import AssesmentPage from "./pages/AssesmentPage";

const App = () => {
  return (
    <div className="bg-gradient-to-r from-gray-600 to-gray-700">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/assesment" element={<AssesmentPage />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </div>
  )
}

export default App