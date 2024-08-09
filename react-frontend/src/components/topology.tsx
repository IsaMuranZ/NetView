import React from 'react';
import {Link} from "react-router-dom";

const NetworkTopology: React.FC = () => ( // These components don't return JSX elements because 
    // they are incorporated by the react-router-dom module into their appropriate pages
    <div className="p-4">
        <header className="flex justify-between items-center bg-blue-900 p-4 text-white">
            <h1 className="text-4xl font-datadog">NetView</h1>
            <Link to="/" className="text-xl font-datadog underline">Home</Link>
        </header>
        <div className="mt-4 flex justify-center">
            <img
                src="http://localhost:5000/topology"
                alt="Network Topology"
                className="border-2 border-gray-400 rounded-md shadow-lg"
            />
        </div>
    </div>
)
;

export default NetworkTopology;
