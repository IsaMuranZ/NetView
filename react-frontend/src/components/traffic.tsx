import React, {useEffect, useState} from 'react';
import {Link} from "react-router-dom";
import axios from "axios";

interface TrafficData{
    ip: string;
    bytes: number;
    packets: number;
    is_internal: boolean;
}

const Traffic:React.FC = () => {
    const [trafficData, setTrafficData] = useState<TrafficData[]>([]);

    useEffect(() => {
        axios.get<TrafficData[]>('http://localhost:5000/traffic')
            .then(response => {
                console.log('Fetched traffic data:', response.data);
                // Sort data to show internal IPs first
                const sortedData = response.data.sort((a, b) => {
                    return b.is_internal ? 1 : -1;
                });
                setTrafficData(sortedData);
            })
            .catch(error => {
                console.error('Error fetching traffic data:', error);
            });
    }, []);

    const humanBytes = (bytes: number) => {
        if(bytes > 1_000_000_000)
            return (bytes/1_000_000_000).toFixed(2) + ' GB';
        if(bytes > 1_000_000)
            return (bytes/1_000_000).toFixed(2) + ' MB';
        if(bytes > 1_000)
            return (bytes/1_000).toFixed(2) + ' KB';
        return bytes + ' B';
    }
    return(
        <div className="p-4">
            <header className="flex justify-between items-center bg-blue-900 p-4 text-white">
                <h1 className="text-4xl font-datadog">NetView-&gt;Traffic</h1>
                <Link to="/" className="text-xl font-datadog underline">Home</Link>
            </header>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
                {trafficData.map((data, index) => (
                    <div
                        key={index}
                        className={`p-4 rounded shadow-md ${
                            data.is_internal ? 'bg-green-200' : 'bg-yellow-200'
                        }`}
                    >
                        <h2 className="text-lg font-bold">{data.ip}</h2>
                        <p className="text-sm">Bytes: {humanBytes(data.bytes)}</p>
                        <p className="text-sm">Packets: {data.packets}</p>
                    </div>
                ))}
            </div>
            {/* Div tag for the sticky legend elemenet*/}
            <div className="fixed bottom-4 right-4 p-2 bg-white border border-gray-300 rounded shadow-lg transition-opacity duration-300 hover:opacity-25 opacity-100">
                <h3 className="font-bold mb-2">Legend</h3>
                <p><span className="inline-block w-4 h-4 bg-green-200 mr-2"></span>Internal Network</p>
                <p><span className="inline-block w-4 h-4 bg-yellow-200 mr-2"></span>External Network</p>
            </div>
        </div>
    )
}

export default Traffic;