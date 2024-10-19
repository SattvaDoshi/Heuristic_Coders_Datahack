
const UploadFiles = () => {
  return (
    <div className="my-10 mx-8 md:mx-0 h-screen md:flex md:flex-row flex flex-col items-center text-gray-900 bg-gray-100 bg-opacity-80 rounded-md">
        <div className="flex flex-col gap-4 md:w-3/5 w-11/12 h-full justify-center pl-16">
            <h2 className="font-semibold text-5xl md:w-11/12 w-full leading-tight opacity-90 pr-4">Securely Upload Your Infrastructure Documents with ShieldAI</h2>
            <p className="text-xl md:w-4/5 w-full leading-7 opacity-80 pr-4 md:pr-8">Seamlessly upload your security documents for AI-driven analysis and real-time risk assessment, ensuring your data stays protected and compliant</p>
        </div>
        <div className="flex justify-center items-center w-full md:w-2/5 pb-16 md:pb-0">
            <div className="w-[400px] md:w-4/5 h-[200px] flex items-center justify-center border-2 border-dotted border-gray-900 rounded-xl">
                {/* <input className="bg-purple-400 bg-opacity-40 py-3 px-4 rounded-xl font-medium text-xl">Upload Files</input> */}
                {/* <input type="file" className="bg-purple-400 bg-opacity-40" /> */}
                <form action="/upload" method="post" className="flex flex-col gap-2 justify-center items-center">
                    <input type="file" id="file-upload" name="file" className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"/>
                    <button type="submit" className="mt-4 px-4 py-2 bg-purple-600 bg-opacity-50 text-white rounded-lg">Upload</button>
                </form>
            </div>
        </div>
    </div>
  )
}

export default UploadFiles