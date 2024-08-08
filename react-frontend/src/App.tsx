// src/App.tsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';
// Axios is a promise based http client that will be used to fetch data using our API


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
  const [visibleDevices, setVisibleDevices] = useState(4);
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
      setVisibleDevices(prevVisibleDevices => prevVisibleDevices + 4);
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
                      <div key={index} className="bg-white p-4 rounded shadow-md">
                          <p><strong>IP Address:</strong> {device.ip}</p>
                          <p><strong>MAC Address:</strong> {device.mac}</p>
                          <p><strong>Hostname:</strong> {device.hostname}</p>
                          <p><strong>Status:</strong> {device.status}</p>
                          <p><strong>Open Ports:</strong> {device.open_ports}</p>
                          <p><strong>Services:</strong> {device.services}</p>
                          <p><strong>Traffic (Bytes):</strong> {device.traffic_bytes}</p>
                          <p><strong>Traffic (Packets):</strong> {device.traffic_packets}</p>
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
