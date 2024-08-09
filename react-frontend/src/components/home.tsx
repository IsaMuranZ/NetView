import React from 'react';
import { Link } from 'react-router-dom';
// link to different pages on the application
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
// tooltips used on the main page

interface Device {
    ip: string;
    mac: string;
    hostname: string;
    status: string;
    open_ports: string;
    services: string;
    traffic_bytes: number;
    traffic_packets: number;
}


// This component is our home page component. It needs to list all the devices in a dashboard view
// The props include the devices structure (stores all our device data), visibleDevices/loadMoreDevices (load more button UX)
// humanBytes (convert bytes to a human readable format), and formatTooltipContent.
const Home: React.FC<{ devices: Device[], visibleDevices: number, loadMoreDevices: () => void, humanBytes: (bytes: number) => string, formatTooltipContent: (content: string)
        => JSX.Element[] }> = ({ devices, visibleDevices, loadMoreDevices, humanBytes, formatTooltipContent }) => ( // These components don't return JSX elements because 
    // they are incorporated by the react-router-dom module into their appropriate pages
    <div className="p-4">
        <header className="flex justify-between items-center bg-blue-900 p-4 text-white">
            <h1 className="text-4xl font-datadog">NetView</h1>
            <Link to="/topology" className="text-xl font-datadog underline">Network Visualization</Link>
        </header>
        <main className="mt-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {devices.slice(0, visibleDevices).map((device, index) => (
                    <div key={index} className="bg-white p-4 rounded shadow-md flex flex-col justify-between">
                        <div>
                            <h2 className="text-lg font-bold">{device.ip}</h2>
                            <p className="text-sm text-gray-600">{device.mac}</p>
                        </div>
                        <div className="mt-4 flex justify-between">
                            <button
                                className="bg-blue-500 text-white py-1 px-2 rounded hover:bg-blue-700 me-1"
                                data-tooltip-id={`openPortsTooltip-${index}`}
                                data-tooltip-content={device.open_ports}
                            >
                                🛠️ Ports
                            </button>
                            <Tooltip id={`openPortsTooltip-${index}`} place="bottom" className="text-lg">
                                {formatTooltipContent(device.open_ports)}
                            </Tooltip>

                            <button
                                className="bg-green-500 text-white py-1 px-2 rounded hover:bg-green-700 me-1"
                                data-tooltip-id={`servicesTooltip-${index}`}
                                data-tooltip-content={device.services}
                            >
                                💻 Services
                            </button>
                            <Tooltip id={`servicesTooltip-${index}`} place="bottom" className="text-lg">
                                {formatTooltipContent(device.services)}
                            </Tooltip>

                            <button
                                className="bg-purple-500 text-white py-1 px-2 rounded hover:bg-purple-700 me-1"
                                data-tooltip-id={`trafficTooltip-${index}`}
                                data-tooltip-content={`Traffic: ${humanBytes(device.traffic_bytes)}, Packets: ${device.traffic_packets}`}
                            >
                                📊 Traffic
                            </button>
                            <Tooltip id={`trafficTooltip-${index}`} place="bottom" className="text-lg">
                                {formatTooltipContent(`Traffic: ${humanBytes(device.traffic_bytes)}, Packets: ${device.traffic_packets}`)}
                            </Tooltip>
                        </div>
                    </div>
                ))}
            </div>
            {visibleDevices < devices.length && (
                <div className="mt-4 text-center">
                    <button
                        className="bg-blue-500 text-white py-2 px-4 rounded"
                        onClick={loadMoreDevices}
                    >
                        Load More
                    </button>
                </div>
            )}
        </main>
    </div>
);

export default Home;