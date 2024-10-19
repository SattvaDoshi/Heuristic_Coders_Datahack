
// eslint-disable-next-line react/prop-types
const FeatureCard = ({ header, image, des }) => {
  return (
    <div className="flex flex-col w-2/3 md:w-1/3 bg-gray-100 bg-opacity-80 text-gray-900 h-[526px] rounded-lg shadow-md">
        <div className="md:h-2/5 bg-yellow-200">
            <img src={image} alt="Image" />
        </div>
        <div className="h-3/5 flex flex-col justify-center gap-2 p-4">
            <h1 className="font-bold text-2xl">{header}</h1>
            <div className="flex flex-col gap-1 pr-4 opacity-80">
                <p>{des[0]}</p>
                <p>{des[1]}</p>
                <p>{des[2]}</p>
            </div>
        </div>
    </div>
  )
}

export default FeatureCard