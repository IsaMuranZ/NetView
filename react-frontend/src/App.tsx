// src/App.tsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';
// Axios is a promise based http client that will be used to fetch data using our API
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';

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

const App: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [visibleDevices, setVisibleDevices] = useState(8);
  // The visible devices is the starting amount of devices displayed on the homescreen

  useEffect(() => {
    // Fetch devices from the backend
    // Axios makes the request, the then method takes the response and runs the setDevices() method.
    axios.get<Device[]>('http://localhost:5000/devices')
        .then(response => {
          console.log('Fetched devices:', response.data);
          setDevices(response.data);
        })
        .catch(error => {
          console.error('Error fetching devices:', error);
        });
  }, []);

  // Function that renders additional devices.
  const loadMoreDevices = () => {
      setVisibleDevices(prevVisibleDevices => prevVisibleDevices + 8);
  };

  //Function that returns human readable bytes.
  const humanBytes = (bytes:number) => {
      if(bytes > 1_000_000_000)
          return (bytes/1_000_000_000).toFixed(2) + 'gb'
      if(bytes > 1_000_000)
          return (bytes/1_000_000).toFixed(2) + 'mb'
      if(bytes > 1_000)
          return (bytes/1_000).toFixed(2) + 'kb'
      return bytes
  }

  // Helper function to split apart data in some of the device data fields
  const formatTooltipContent = (content: string) => {
      return content.split(',').map((item, index) => <div key={index}>{item.trim()}</div>);
  };

  return (
      <div className="p-4">
          <header className="flex justify-between items-center bg-blue-900 p-4 text-white">
              <h1 className="text-4xl font-datadog">NetView</h1>
              <a href="/networkvisual" className="text-xl font-datadog underline">Network Visualization</a>
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
                                  🛠️ Open Ports
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
};

export default App;
