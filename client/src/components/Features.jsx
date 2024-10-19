import FeatureCard from "./FeatureCard"

const features = [
  {
    header: "Automated Risk Assessment",
    subpoints: ["Analyzes cybersecurity documentation using AI", "Generates accurate risk scores based on your data", "Provides proactive insights to mitigate vulnerabilities"]
  },
  {
    header: "Comprehensive Reportingt",
    subpoints: ["Creates detailed, actionable cybersecurity reports", "Identifies key areas of improvement for better security", "Aligns with industry standards like GDPR and HIPAA."]
  },
  {
    header: "Real-time Decision Support",
    subpoints: ["Offers dynamic, AI-powered recommendations", "Continuously updates risk assessments as data changes", "Enables informed, real-time decision-making for stronger security"]
  },
]


const Features = () => {
  return (
    <div id="feature" className="h-auto md:h-screen bg-gray-100 py-16 bg-opacity-80 my-32 rounded-md flex flex-col md:flex md:flex-row gap-16 md:gap-8 md:px-10 md:justify-around items-center mx-8 md:mx-0">
      <FeatureCard header={features[0].header} des={features[0].subpoints} />
      <FeatureCard header={features[1].header} des={features[1].subpoints} />
      <FeatureCard header={features[2].header} des={features[2].subpoints} />
    </div>
  )
}

export default Features