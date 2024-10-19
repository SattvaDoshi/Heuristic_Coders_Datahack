import Spline from "@splinetool/react-spline"

const Hero = () => {
  return (
    <div className="mt-10 h-screen md:flex md:flex-row flex flex-col items-center text-gray-900">
      <div className="flex flex-col gap-4 md:w-3/5 w-11/12 h-full justify-center pl-16 bg-gray-100 bg-opacity-80 rounded-md">
        <h2 className="font-semibold text-5xl md:w-11/12 w-full leading-tight opacity-90 pr-4">Transform Your Cybersecurity with ShieldAI</h2>
        <p className="text-xl md:w-4/5 w-full leading-7 opacity-80 pr-4 md:pr-8">Use ShieldAI's generative AI to effortlessly analyze cybersecurity documentation, generating detailed reports and risk scores to enhance your defenses and inform your decisions.</p>
      </div>
      <div className="hidden md:w-2/5 md:flex md:justify-start md:items-start">
        <Spline
          scene="https://prod.spline.design/Fr2IQttonzASL2yG/scene.splinecode" 
          width={676}
          height={549}
        />
      </div>
    </div>
  )
}

export default Hero