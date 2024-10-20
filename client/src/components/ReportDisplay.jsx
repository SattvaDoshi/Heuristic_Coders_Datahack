import React from 'react';

const ReportDisplay = ({ report }) => {
    // Check if the report is valid and has the expected structure
    if (!report || typeof report !== 'object') {
        return <div>No report available.</div>;
    }

    const { risk_level, risk_score, details } = report;

    return (
        <div className="text-gray-900 flex flex-col gap-2">
            {risk_level ? <h2 className="text-xl">{risk_level}</h2> : <h2 className="text-xl">Risk Level: Not available</h2>}
            {risk_score !== undefined ? <h3 className="text-xl">Risk Score: {risk_score}</h3> : <h3 className="text-xl">Risk Score: Not available</h3>}
            
            <div>
                <h3 className="font-medium text-xl opacity-90">Details:</h3>
                {details && typeof details === 'object' && Object.keys(details).length > 0 ? (
                    Object.keys(details).map((key) => (
                        <div key={key}>
                            <h4 className="font-medium pt-3 text-xl opacity-80">{key}</h4>
                            <p className="py-2">{details[key].description || 'Description not available.'}</p>
                            
                            <h5>Recommendations:</h5>
                            <ul className="pb-2">
                                {details[key].recommendations && details[key].recommendations.length > 0 ? (
                                    details[key].recommendations.map((rec, index) => (
                                        <li key={index}>{rec}</li>
                                    ))
                                ) : (
                                    <li>No recommendations available.</li>
                                )}
                            </ul>
                            
                            <h5>Potential Threats:</h5>
                            <ul>
                                {details[key].threats && details[key].threats.length > 0 ? (
                                    details[key].threats.map((threat, index) => (
                                        <li key={index}>{threat}</li>
                                    ))
                                ) : (
                                    <li>No potential threats available.</li>
                                )}
                            </ul>
                        </div>
                    ))
                ) : (
                    <p>No details available.</p>
                )}
            </div>
        </div>
    );
};

export default ReportDisplay;
